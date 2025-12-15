// frontend/js/lang.js

const HB_SUPPORTED_LANGS = ["en", "ru", "am"];
const HB_DEFAULT_LANG = "en";

function hbNormalizeLang(raw) {
  if (!raw) return HB_DEFAULT_LANG;
  const primary = raw.toString().split(".")[0].split("_")[0].slice(0, 2).toLowerCase();
  return HB_SUPPORTED_LANGS.includes(primary) ? primary : HB_DEFAULT_LANG;
}

function hbGetApiBase() {
  const { protocol, hostname, port, pathname } = window.location || {};
  const hasPrefix = pathname === "/HealthyBite" || pathname.startsWith("/HealthyBite/");
  const basePrefix = hasPrefix ? "/HealthyBite" : "";
  let effectivePort = port || "";
  if (!hasPrefix && (hostname === "localhost" || hostname === "127.0.0.1") && port === "8080") {
    effectivePort = "8810";
  }
  const portPart = effectivePort ? `:${effectivePort}` : "";
  return `${protocol}//${hostname}${portPart}${basePrefix}/api/v1`;
}

function hbGetInitialLang() {
  try {
    const saved = localStorage.getItem("hb_lang");
    if (saved) {
      const normalized = hbNormalizeLang(saved);
      if (HB_SUPPORTED_LANGS.includes(normalized)) {
        return normalized;
      }
    }
  } catch (e) {
    // ignore localStorage errors
  }

  const browser = hbNormalizeLang(navigator.language || navigator.userLanguage || "");
  return HB_SUPPORTED_LANGS.includes(browser) ? browser : HB_DEFAULT_LANG;
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
  document.documentElement.lang = initialLang;
  hbSwitchLanguage(initialLang);

  document.querySelectorAll(".lang-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const lang = btn.dataset.lang;
      if (!HB_SUPPORTED_LANGS.includes(lang)) return;
      hbSwitchLanguage(lang);
    });
  });
});

// expose helpers for other scripts
window.hbNormalizeLang = hbNormalizeLang;
window.hbGetApiBase = hbGetApiBase;
window.hbGetCurrentLang = function () {
  const stored = (() => {
    try {
      return localStorage.getItem("hb_lang");
    } catch (e) {
      return null;
    }
  })();
  const raw = stored || document.documentElement.lang || navigator.language || "en";
  const normalized = hbNormalizeLang(raw);
  document.documentElement.lang = normalized;
  return normalized;
};
