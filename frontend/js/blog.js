// Verify: backend on 8810 + frontend on 8080, open blog.html, click chips to see list filter, reload with #blog-tips to confirm persistence.
console.log("[HB] blog.js is loaded");

const HB_API_BASE = "http://127.0.0.1:8810";

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
let initialFilterKey = "all";

let trendingTemplate;
let successTemplate;
let tipsTemplate;
let allTemplate;
const FILTER_KEYS = ["all", "success", "tips", "mindset", "routine"];
const FILTER_SECTION_MAP = {
  all: null,
  success: "success",
  tips: "tips",
  mindset: "featured",
  routine: "weekly",
};

function hbGetActiveLang() {
  try {
    const stored = localStorage.getItem("hb_lang");
    if (stored) return stored;
  } catch (e) {
    // ignore
  }
  return document.documentElement.lang || "en";
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
  (items || []).forEach((item) => {
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
  try {
    const lang =
      window.hbGetCurrentLang?.() ||
      hbGetActiveLang();
    const res = await fetch(`${HB_API_BASE}/api/v1/blog/posts/${slug}?lang=${lang}`, {
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
  const seen = new Set();
  const collected = [];
  Object.entries(sections || {}).forEach(([key, section]) => {
    (section?.items || []).forEach((item) => {
      if (!item || !item.slug) return;
      if (seen.has(item.slug)) return;
      seen.add(item.slug);
      collected.push({ ...item, section: item.section || key });
    });
  });
  return collected;
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
  const url = new URL(window.location.href);
  url.hash = newHash;
  history.replaceState(null, "", url.toString());
}

function applyFilter(key) {
  if (!FILTER_KEYS.includes(key)) {
    key = "all";
  }
  const available = new Set(Object.keys(sectionsData || {}));
  const desiredSection = FILTER_SECTION_MAP[key];
  const section = desiredSection && available.has(desiredSection) ? desiredSection : null;
  const items = section ? allPosts.filter((p) => p.section === section) : allPosts;
  renderAll(items);
  setActiveChip(key);
  updateHash(key);
}

async function loadSections(lang) {
  const url = `${HB_API_BASE}/api/v1/blog/sections?lang=${lang}`;
  console.log("[HB] will call fetch for blog sections:", url);
  const response = await fetch(url);
  console.log("[HB] fetch returned response:", response.status);
  const data = await response.json();
  renderSections(data);
  sectionsData = data.sections || {};
  allPosts = normalizeAllPosts(sectionsData);
  applyFilter(initialFilterKey);
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

  const filterRow = document.querySelector(".blog-filter-row");
  filterChips = Array.from(filterRow?.querySelectorAll(".blog-chip") || []);
  filterChips.forEach((chip, idx) => {
    const key = chip.dataset.filterKey || FILTER_KEYS[idx] || "all";
    chip.dataset.filterKey = key;
    chip.addEventListener("click", (e) => {
      e.preventDefault();
      applyFilter(key);
    });
  });
  initialFilterKey = getFilterFromHash(window.location.hash) || "all";

  const lang =
    window.hbGetCurrentLang?.() ||
    localStorage.getItem("hb_lang") ||
    "en";

  loadSections(lang).catch(handleError);
});
