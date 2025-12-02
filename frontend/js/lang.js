// frontend/js/lang.js

const HB_SUPPORTED_LANGS = ["en", "ru", "am"];
const HB_DEFAULT_LANG = "en";

function hbGetInitialLang() {
  try {
    const saved = localStorage.getItem("hb_lang");
    if (saved && HB_SUPPORTED_LANGS.includes(saved)) {
      return saved;
    }
  } catch (e) {
    // ignore localStorage errors
  }

  const browser =
    (navigator.language || navigator.userLanguage || "")
      .slice(0, 2)
      .toLowerCase();

  if (HB_SUPPORTED_LANGS.includes(browser)) {
    return browser;
  }
  return HB_DEFAULT_LANG;
}

// Определяем тип страницы: ai, blog, ...
function hbGetPageKey() {
  const el = document.querySelector("[data-hb-page]");
  return el ? el.getAttribute("data-hb-page") : null;
}

// Загружаем один JSON с защитой
async function hbLoadJson(url) {
  try {
    const res = await fetch(url, { cache: "no-cache" });
    if (!res.ok) {
      console.warn("[HB i18n] Failed to load", url, res.status);
      return null;
    }
    return await res.json();
  } catch (e) {
    console.error("[HB i18n] Error loading", url, e);
    return null;
  }
}

// Грузим базовый словарь + страничный словарь и мержим
async function hbLoadTranslations(lang) {
  const dict = {};

  // базовый файл (nav, footer, home, about, contact и т.п.)
  const base = await hbLoadJson(`lang/${lang}.json`);
  if (base) Object.assign(dict, base);

  // страничный файл (ai / blog), если указан data-hb-page
  const pageKey = hbGetPageKey(); // "ai" | "blog" | null
  if (pageKey) {
    const pageDict = await hbLoadJson(`lang/${lang}.${pageKey}.json`);
    if (pageDict) Object.assign(dict, pageDict);
  }

  return dict;
}

function hbResolveKey(dict, key) {
  return key.split(".").reduce(
    (acc, part) => (acc && acc[part] != null ? acc[part] : undefined),
    dict
  );
}

function hbApplyTranslations(dict) {
  if (!dict) return;

  // Перевод текста по data-i18n
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    const text = hbResolveKey(dict, key);
    if (!text) return;

    if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
      if (el.hasAttribute("placeholder")) {
        el.placeholder = text;
      }
    } else {
      el.textContent = text;
    }
  });

  // Перевод title, если есть
  const metaTitle = hbResolveKey(dict, "meta.title");
  if (metaTitle) {
    document.title = metaTitle;
  }
}

function hbSetActiveLangButton(lang) {
  document.querySelectorAll(".lang-btn").forEach((btn) => {
    btn.classList.toggle("is-active", btn.dataset.lang === lang);
  });
}

async function hbSwitchLanguage(lang) {
  const dict = await hbLoadTranslations(lang);
  if (!dict) return;
  hbApplyTranslations(dict);
  hbSetActiveLangButton(lang);
  try {
    localStorage.setItem("hb_lang", lang);
  } catch (e) {
    // ignore
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const initialLang = hbGetInitialLang();
  hbSwitchLanguage(initialLang);

  document.querySelectorAll(".lang-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const lang = btn.dataset.lang;
      if (!HB_SUPPORTED_LANGS.includes(lang)) return;
      hbSwitchLanguage(lang);
    });
  });
});
