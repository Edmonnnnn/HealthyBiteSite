// Chips are <button> so hash won't change automatically; we set it manually and reapply filters. Verify: backend 8810 + frontend 8080, open blog.html, click chips -> hash changes + list updates; reload with #blog-tips applies filter.
console.log("[HB] blog.js is loaded");

const HB_API_BASE = (window.hbGetApiBase && window.hbGetApiBase()) || "/api/v1";
const DEBUG_FILTERS = true;

let weeklyList;
let featuredCard;
let trendingList;
let successGrid;
let tipsGrid;
let allList;
let detailCard;
let filterChips;
let sectionsData = {};
let allPosts = [];
let searchInput;
let searchButton;
let searchQuery = "";
let allArticlesSection;
let scrollOnNextHash = false;
let initialHashScrollPending = true;
let blogTranslations = null;
let blogTranslationsLang = null;

let trendingTemplate;
let successTemplate;
let tipsTemplate;
let allTemplate;
const FILTER_KEYS = ["all", "success", "tips", "mindset", "routine"];
const FILTER_SECTION_MAP = {
  all: null,
  success: "success",
  tips: "tips",
  mindset: "mindset",
  routine: "routine",
};
const BLOG_STATE_LANG = "hb_blog_lang";
const BLOG_STATE_HASH = "hb_blog_hash";
const BLOG_STATE_QUERY = "hb_blog_query";
const BLOG_STATE_RETURN = "hb_blog_return";

function hbGetActiveLang() {
  try {
    const stored = localStorage.getItem("hb_lang");
    if (stored && window.hbNormalizeLang) return window.hbNormalizeLang(stored);
  } catch (e) {
    // ignore
  }
  const fallback = document.documentElement.lang || navigator.language || "en";
  return (window.hbNormalizeLang && window.hbNormalizeLang(fallback)) || "en";
}

function hbSafeText(el, value) {
  if (el && value != null) {
    el.textContent = value;
  }
}

function hbFormatReadingMinutes(minutes) {
  if (!minutes && minutes !== 0) return "";
  return `${minutes} min read`;
}

function blogTranslate(key, fallback) {
  if (blogTranslations && blogTranslationsLang) {
    const val = hbResolveKey(blogTranslations, key);
    if (val) return val;
  }
  return fallback;
}

function hbSetSession(key, value) {
  try {
    if (value == null) {
      sessionStorage.removeItem(key);
    } else {
      sessionStorage.setItem(key, value);
    }
  } catch (e) {
    // ignore
  }
}

function hbGetSession(key, fallback = null) {
  try {
    const val = sessionStorage.getItem(key);
    return val !== null ? val : fallback;
  } catch (e) {
    return fallback;
  }
}

async function loadBlogTranslations(lang) {
  try {
    const dict = await hbLoadTranslations(lang);
    if (dict) {
      blogTranslations = dict;
      blogTranslationsLang = lang;
    }
  } catch (e) {
    console.warn("[HB blog] Could not load translations for", lang, e);
  }
}

function scrollToArticles(options = { behavior: "smooth" }) {
  if (!allArticlesSection) return;
  allArticlesSection.scrollIntoView({ behavior: options.behavior || "smooth", block: "start" });
}

function hbCreateChip(label) {
  const span = document.createElement("span");
  span.className = "blog-chip subtle";
  span.textContent = label;
  return span;
}

function hbAttachSlugClick(element, slug, handler) {
  if (!element || !slug) return;
  element.dataset.slug = slug;
  element.addEventListener("click", (e) => {
    e.preventDefault();
    handler(slug);
  });
}

function handleError(err) {
  console.error("[HB blog] Error loading sections:", err);
}

function renderWeekly(items) {
  if (!weeklyList) return;
  weeklyList.innerHTML = "";
  (items || []).forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item.title || item.summary || item.eyebrow || "";
    if (item.slug) {
      li.classList.add("blog-weekly-link");
      hbAttachSlugClick(li, item.slug, openPost);
    }
    weeklyList.appendChild(li);
  });
}

function renderFeatured(item) {
  if (!featuredCard || !item) return;
  hbSafeText(featuredCard.querySelector(".blog-badge"), item.eyebrow || "Featured");
  hbSafeText(featuredCard.querySelector("h2"), item.title);
  hbSafeText(featuredCard.querySelector(".blog-lead"), item.summary);
  const metas = featuredCard.querySelectorAll(".blog-meta span");
  if (metas.length >= 3) {
    hbSafeText(metas[0], item.publishedAt || item.eyebrow || "");
    hbSafeText(metas[2], hbFormatReadingMinutes(item.readingMinutes));
  }
  const link = featuredCard.querySelector(".blog-featured-link");
  if (link) {
    hbAttachSlugClick(link, item.slug, openPost);
  }
}

function renderTrending(items) {
  if (!trendingList || !trendingTemplate) return;
  trendingList.innerHTML = "";
  (items || []).forEach((item) => {
    const card = trendingTemplate.cloneNode(true);
    hbSafeText(card.querySelector(".blog-badge"), item.eyebrow || "");
    hbSafeText(card.querySelector("h4"), item.title);
    hbSafeText(card.querySelector("p"), item.summary);
    hbSafeText(card.querySelector(".blog-trending-meta"), hbFormatReadingMinutes(item.readingMinutes));
    hbAttachSlugClick(card, item.slug, openPost);
    trendingList.appendChild(card);
  });
}

function renderSuccess(items) {
  if (!successGrid || !successTemplate) return;
  successGrid.innerHTML = "";
  (items || []).forEach((item) => {
    const card = successTemplate.cloneNode(true);
    const thumb = card.querySelector(".blog-card-thumb");
    if (thumb) thumb.textContent = (item.title || "?").charAt(0).toUpperCase();
    hbSafeText(card.querySelector(".blog-badge"), item.eyebrow || "");
    hbSafeText(card.querySelector("h3"), item.title);
    hbSafeText(card.querySelector("p"), item.summary);
    const link = card.querySelector(".blog-link");
    if (link) {
      hbAttachSlugClick(link, item.slug, openPost);
    } else {
      hbAttachSlugClick(card, item.slug, openPost);
    }
    successGrid.appendChild(card);
  });
}

function renderTips(items) {
  if (!tipsGrid || !tipsTemplate) return;
  tipsGrid.innerHTML = "";
  (items || []).forEach((item) => {
    const card = tipsTemplate.cloneNode(true);
    hbSafeText(card.querySelector(".blog-badge"), item.eyebrow || item.tags?.[0] || "Guide");
    hbSafeText(card.querySelector("h3"), item.title);
    const list = card.querySelector("ul");
    if (list) {
      list.innerHTML = "";
      if (item.summary) {
        const li = document.createElement("li");
        li.textContent = item.summary;
        list.appendChild(li);
      }
      (item.tags || []).slice(0, 3).forEach((tag) => {
        const li = document.createElement("li");
        li.textContent = tag;
        list.appendChild(li);
      });
    }
    const link = card.querySelector(".blog-link");
    if (link) {
      hbAttachSlugClick(link, item.slug, openPost);
    } else {
      hbAttachSlugClick(card, item.slug, openPost);
    }
    tipsGrid.appendChild(card);
  });
}

function renderAll(items) {
  if (!allList || !allTemplate) return;
  allList.innerHTML = "";
  const listItems = items || [];
  if (listItems.length === 0) {
    const empty = document.createElement("div");
    empty.className = "blog-empty-state";
    const title = document.createElement("h3");
    title.className = "blog-empty-title";
    title.textContent = blogTranslate("blog.noResultsTitle", "No articles found");
    const hint = document.createElement("p");
    hint.className = "blog-empty-hint";
    hint.textContent = blogTranslate("blog.noResultsHint", "Try changing the filter or the search keyword.");
    empty.appendChild(title);
    empty.appendChild(hint);
    allList.appendChild(empty);
    return;
  }
  listItems.forEach((item) => {
    const card = allTemplate.cloneNode(true);
    hbSafeText(card.querySelector(".blog-badge"), item.eyebrow || "");
    hbSafeText(card.querySelector(".blog-list-meta"), hbFormatReadingMinutes(item.readingMinutes));
    hbSafeText(card.querySelector("h3"), item.title);
    hbSafeText(card.querySelector("p"), item.summary);
    const tagRow = card.querySelector(".blog-tag-row");
    if (tagRow) {
      tagRow.innerHTML = "";
      (item.tags || []).forEach((tag) => tagRow.appendChild(hbCreateChip(tag)));
    }
    const link = card.querySelector(".blog-link");
    if (link) {
      hbAttachSlugClick(link, item.slug, openPost);
    } else {
      hbAttachSlugClick(card, item.slug, openPost);
    }
    allList.appendChild(card);
  });
}

function renderPostDetail(post) {
  if (!detailCard) return;
  let backBtn = detailCard.querySelector("#blog-detail-back");
  if (!backBtn) {
    backBtn = document.createElement("button");
    backBtn.id = "blog-detail-back";
    backBtn.type = "button";
    backBtn.className = "blog-link blog-back-link";
    backBtn.dataset.i18n = "blog.backToAll";
    backBtn.addEventListener("click", handleBackToList);
    detailCard.insertBefore(backBtn, detailCard.firstChild);
  }
  hbSafeText(backBtn, blogTranslate("blog.backToAll", "Back to all articles"));

  const badge = detailCard.querySelector("#blog-detail-badge");
  const meta = detailCard.querySelector("#blog-detail-meta");
  const title = detailCard.querySelector("#blog-detail-title");
  const tags = detailCard.querySelector("#blog-detail-tags");
  const content = detailCard.querySelector("#blog-detail-content");

  hbSafeText(badge, post.eyebrow || post.title || "");
  const minutes = hbFormatReadingMinutes(post.readingMinutes);
  const published = post.publishedAt ? `${post.publishedAt}${minutes ? " • " : ""}` : "";
  hbSafeText(meta, `${published}${minutes}`);
  hbSafeText(title, post.title || "");

  if (tags) {
    tags.innerHTML = "";
    (post.tags || []).forEach((tag) => tags.appendChild(hbCreateChip(tag)));
  }

  if (content) {
    content.innerHTML = "";
    (post.contentBlocks || []).forEach((block) => {
      if (!block || !block.type) return;
      if (block.type === "paragraph") {
        const p = document.createElement("p");
        p.textContent = block.text || "";
        content.appendChild(p);
      } else if (block.type === "tip") {
        const tip = document.createElement("div");
        tip.className = "blog-tip-block";
        if (block.title) {
          const titleEl = document.createElement("div");
          titleEl.className = "blog-tip-title";
          titleEl.textContent = block.title;
          tip.appendChild(titleEl);
        }
        const textEl = document.createElement("p");
        textEl.textContent = block.text || "";
        tip.appendChild(textEl);
        content.appendChild(tip);
      } else if (block.type === "list") {
        const ul = document.createElement("ul");
        (block.items || []).forEach((itm) => {
          const li = document.createElement("li");
          li.textContent = itm;
          ul.appendChild(li);
        });
        content.appendChild(ul);
      } else if (block.type === "quote") {
        const q = document.createElement("blockquote");
        q.textContent = block.text || "";
        content.appendChild(q);
      } else if (block.type === "image") {
        const img = document.createElement("img");
        img.src = block.url || "";
        img.alt = block.alt || post.title || "Blog image";
        content.appendChild(img);
      } else {
        const p = document.createElement("p");
        p.textContent = block.text || "";
        content.appendChild(p);
      }
    });
  }

  detailCard.hidden = false;
  detailCard.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function openPost(slug) {
  if (!slug) return;
  const currentLang =
    window.hbNormalizeLang?.(window.hbGetCurrentLang?.() || hbGetActiveLang()) ||
    hbGetActiveLang();
  hbSetSession(BLOG_STATE_LANG, currentLang);
  hbSetSession(BLOG_STATE_HASH, window.location.hash || "#blog-all");
  hbSetSession(BLOG_STATE_QUERY, searchInput?.value || "");
  hbSetSession(BLOG_STATE_RETURN, "1");
  try {
    const res = await fetch(`${HB_API_BASE}/blog/posts/${slug}?lang=${currentLang}`, {
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) {
      console.error("[HB blog] Failed to load post", slug, res.status);
      return;
    }
    const post = await res.json();
    renderPostDetail(post);
  } catch (err) {
    console.error("[HB blog] Error loading post detail", err);
  }
}

function renderSections(data) {
  if (!data) return;
  const sections = data.sections || {};
  renderWeekly(sections.weekly?.items);
  renderFeatured((sections.featured?.items || [])[0]);
  renderTrending(sections.trending?.items);
  renderSuccess(sections.success?.items);
  renderTips(sections.tips?.items);
  renderAll(sections.all?.items);
}

function normalizeAllPosts(sections) {
  const collected = new Map();
  Object.entries(sections || {}).forEach(([key, section]) => {
    (section?.items || []).forEach((item) => {
      if (!item || !item.slug) return;
      const slug = item.slug;
      const sectionKey = (item.section || key || "").toString().trim().toLowerCase() || "all";
      if (collected.has(slug)) return;
      collected.set(slug, { ...item, section: sectionKey });
    });
  });
  return Array.from(collected.values());
}

function getFilterFromHash(hash) {
  if (!hash || !hash.startsWith("#blog-")) return null;
  const key = hash.replace("#blog-", "");
  return FILTER_KEYS.includes(key) ? key : null;
}

function setActiveChip(key) {
  (filterChips || []).forEach((chip) => {
    chip.classList.toggle("is-active", chip.dataset.filterKey === key);
  });
}

function updateHash(key) {
  const newHash = `#blog-${key}`;
  if (window.location.hash === newHash) return;
  window.location.hash = newHash;
}

function applyFilter(key, opts = { updateHash: true }) {
  if (!FILTER_KEYS.includes(key)) {
    key = "all";
  }
  const desiredSection = FILTER_SECTION_MAP[key];
  const normalizedSection = desiredSection ? desiredSection.toLowerCase() : null;
  const totalPosts = allPosts.length;
  const baseItems = normalizedSection
    ? allPosts.filter((p) => (p.section || "").toLowerCase() === normalizedSection)
    : [...allPosts];
  const q = (searchQuery || "").trim().toLowerCase();
  const items = q
    ? baseItems.filter((p) => {
        const haystack = [
          p.title || "",
          p.subtitle || "",
          p.summary || "",
        ]
          .join(" ")
          .toLowerCase();
        return haystack.includes(q);
      })
    : baseItems;
  if (DEBUG_FILTERS) {
    console.log("[HB blog] filter debug", {
      hash: window.location.hash,
      key,
      section: normalizedSection,
      totalPosts,
      afterSectionFilter: baseItems.length,
      afterSearchFilter: items.length,
      searchQuery: q,
      slugs: items.map((p) => p.slug),
    });
  }
  renderAll(items);
  setActiveChip(key);
  if (opts.updateHash) {
    updateHash(key);
  }
  if (opts.scroll) {
    scrollToArticles({ behavior: "smooth" });
  }
  return {
    key,
    section: normalizedSection,
    counts: {
      totalPosts,
      afterSectionFilter: baseItems.length,
      afterSearchFilter: items.length,
    },
    items,
  };
}

function applyFilterFromHash(options = {}) {
  const key = getFilterFromHash(window.location.hash) || "all";
  const shouldScroll =
    options.scroll === true ||
    (options.scroll === undefined && (scrollOnNextHash || (initialHashScrollPending && window.location.hash)));
  const result = applyFilter(key, { updateHash: false, scroll: shouldScroll });
  initialHashScrollPending = false;
  scrollOnNextHash = false;
  if (DEBUG_FILTERS) {
    console.log("[HB blog] applyFilterFromHash", {
      hash: window.location.hash,
      key,
      count: result?.counts?.afterSearchFilter ?? 0,
    });
  }
}

async function loadSections(lang) {
  const url = `${HB_API_BASE}/blog/sections?lang=${lang}`;
  console.log("[HB] will call fetch for blog sections:", url);
  const response = await fetch(url);
  console.log("[HB] fetch returned response:", response.status);
  const data = await response.json();
  renderSections(data);
  sectionsData = data.sections || {};
  allPosts = normalizeAllPosts(sectionsData);
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("[HB] init blog page");
  const blogRoot = document.querySelector(".blog-hero");
  if (!blogRoot) return;

  weeklyList = document.getElementById("blog-weekly-list");
  featuredCard = document.getElementById("blog-featured-card");
  trendingList = document.getElementById("blog-trending-list");
  successGrid = document.getElementById("blog-success-grid");
  tipsGrid = document.getElementById("blog-tips-grid");
  allList = document.getElementById("blog-all-list");
  detailCard = document.getElementById("blog-article-detail");

  trendingTemplate = trendingList ? trendingList.querySelector(".blog-trending-item") : null;
  successTemplate = successGrid ? successGrid.querySelector(".blog-card") : null;
  tipsTemplate = tipsGrid ? tipsGrid.querySelector(".blog-guide-card") : null;
  allTemplate = allList ? allList.querySelector(".blog-list-card") : null;

  if (trendingList) trendingList.innerHTML = "";
  if (successGrid) successGrid.innerHTML = "";
  if (tipsGrid) tipsGrid.innerHTML = "";
  if (allList) allList.innerHTML = "";
  allArticlesSection = document.getElementById("all-articles");

  const filterRow = document.querySelector(".blog-filter-row");
  filterChips = Array.from(filterRow?.querySelectorAll(".blog-chip") || []);
  filterChips.forEach((chip, idx) => {
    const key = chip.dataset.filterKey || FILTER_KEYS[idx] || "all";
    chip.dataset.filterKey = key;
  });
  const textMap = {
    "all": "all",
    "success stories": "success",
    "tips & guides": "tips",
    "mindful eating": "mindset",
    "busy days": "routine",
  };
  const resolveFilterKey = (chip) => {
    const label = (chip.textContent || "").trim().toLowerCase();
    return (
      chip.dataset.filter ||
      chip.dataset.key ||
      chip.dataset.filterKey ||
      textMap[label]
    );
  };
  document.addEventListener(
    "click",
    (e) => {
      const chip = e.target.closest("button");
      if (!chip) return;
      // Root cause: chips are buttons (no href), so hash never changes automatically—set it manually on click with exact mapping.
      const label = (chip.textContent || "").trim().toLowerCase();
      if (!chip.classList.contains("blog-chip") && !textMap[label]) {
        return;
      }
      const key = resolveFilterKey(chip);
      e.preventDefault();
      if (!key) return;
      scrollOnNextHash = true;
      const nextHash = `#blog-${key}`;
      if (DEBUG_FILTERS) {
        console.log("[HB blog] chip click", { label, key, nextHash });
      }
      if (window.location.hash !== nextHash) {
        window.location.hash = nextHash;
      } else {
        applyFilterFromHash();
      }
    },
    true
  );
  window.addEventListener("hashchange", applyFilterFromHash);
  const applySearch = () => {
    searchQuery = (searchInput?.value || "").trim();
    if (DEBUG_FILTERS) {
      console.log("[HB blog] search change", { query: searchQuery });
    }
    applyFilterFromHash({ scroll: false });
  };
  searchInput = document.getElementById("blog-search-input");
  searchButton = document.getElementById("blog-search-btn");
  if (searchInput) {
    searchInput.addEventListener("input", applySearch);
    searchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        applySearch();
      }
    });
  }
  if (searchButton) {
    searchButton.addEventListener("click", (e) => {
      e.preventDefault();
      applySearch();
    });
  }

  const lang =
    window.hbNormalizeLang?.(window.hbGetCurrentLang?.() || localStorage.getItem("hb_lang")) ||
    "en";
  loadBlogTranslations(lang);
  document.querySelectorAll(".lang-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const nextLang = btn.dataset.lang || "en";
      loadBlogTranslations(nextLang);
    });
  });

  const pendingReturn = hbGetSession(BLOG_STATE_RETURN) === "1";
  if (pendingReturn) {
    const storedQuery = hbGetSession(BLOG_STATE_QUERY, "");
    if (searchInput) {
      searchInput.value = storedQuery;
    }
    searchQuery = (storedQuery || "").trim();
    const storedHash = hbGetSession(BLOG_STATE_HASH, "#blog-all");
    if (storedHash && window.location.hash !== storedHash) {
      window.location.hash = storedHash;
    }
  }

  loadSections(lang)
    .then(() => {
      applyFilterFromHash({ scroll: pendingReturn });
      if (pendingReturn) {
        hbSetSession(BLOG_STATE_RETURN, null);
      }
    })
    .catch(handleError);
});

function handleBackToList() {
  const storedHash = hbGetSession(BLOG_STATE_HASH, "#blog-all");
  const storedQuery = hbGetSession(BLOG_STATE_QUERY, "");
  const validKey = getFilterFromHash(storedHash) || "all";
  const targetHash = `#blog-${validKey}`;
  if (searchInput) {
    searchInput.value = storedQuery;
  }
  searchQuery = (storedQuery || "").trim();
  detailCard.hidden = true;
  hbSetSession(BLOG_STATE_RETURN, null);
  hbSetSession(BLOG_STATE_HASH, null);
  hbSetSession(BLOG_STATE_QUERY, null);
  if (window.location.hash !== targetHash) {
    scrollOnNextHash = true;
    window.location.hash = targetHash;
  } else {
    applyFilterFromHash({ scroll: true });
  }
}
