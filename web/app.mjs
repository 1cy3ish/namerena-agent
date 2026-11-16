import { CATEGORY_GROUPS, CATEGORIES, CATEGORY_LABELS, categoryFor, contextsFor,
  createIndex, findTerms, parseRoute, routeHash, tokensFor } from "./search.mjs";

const $ = selector => document.querySelector(selector);
const PAGE_SIZE = 24;
const CONTEXT_LABELS = { official: "官方", tswn: "tswn", community: "社区" };
const SOURCE_LABELS = { official: "官方说明", repository: "固定提交的实现资料", community: "社区资料",
  legacy: "历史资料", deployment: "部署观察", maintainer: "维护者提供", maintainer_statement: "维护者说明" };
let knowledge, index, termMap, sourceMap;
let limit = PAGE_SIZE;
let previousRoute = parseRoute(location.hash);
let inputTimer;

const escapeHTML = value => String(value ?? "").replace(/[&<>"']/g, char => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
})[char]);
const escapeRegex = value => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

function highlight(value, query) {
  const words = [...new Set(tokensFor(query))].sort((a, b) => b.length - a.length);
  if (!words.length) return escapeHTML(value);
  const pattern = new RegExp(`(${words.map(escapeRegex).join("|")})`, "giu");
  return String(value ?? "").split(pattern).map((part, i) =>
    i % 2 ? `<mark>${escapeHTML(part)}</mark>` : escapeHTML(part)).join("");
}

function safeURL(value) {
  try {
    const url = new URL(value);
    return ["https:", "http:"].includes(url.protocol) ? url.href : "";
  } catch { return ""; }
}

function setMenu(open) {
  $("#sidebar").classList.toggle("is-open", open);
  $("#menu-toggle").setAttribute("aria-expanded", String(open));
  $("#menu-toggle").setAttribute("aria-label", open ? "关闭分类导航" : "打开分类导航");
  $("#nav-backdrop").hidden = !open;
}

function updateRoute(patch, { replace = false } = {}) {
  const route = { ...parseRoute(location.hash), ...patch };
  const hash = routeHash(route);
  if (replace) {
    history.replaceState(null, "", hash);
    renderRoute();
  } else if (location.hash !== hash) {
    location.hash = hash;
  } else {
    renderRoute();
  }
}

function renderNavigation(route) {
  const currentTerm = termMap.get(route.term);
  const selected = currentTerm ? categoryFor(currentTerm)?.id : route.category;
  const itemHTML = (category, label, count, all = false) => `<a class="nav-link" href="${escapeHTML(routeHash({ ...route, category, term: "" }))}"${selected === category ? ' aria-current="page"' : ""}>
    <span class="nav-name">${all ? '<span class="nav-all-icon" aria-hidden="true">▦</span>' : ""}${escapeHTML(label)}</span><span class="nav-count">${count}</span></a>`;
  $("#category-nav").innerHTML = itemHTML("all", "全部词条", knowledge.terms.length, true) + CATEGORY_GROUPS.map(group =>
    `<h2 class="nav-group-title">${escapeHTML(group.title)}</h2>` + group.items.map(category =>
      itemHTML(category.id, category.label, knowledge.terms.filter(term => category.categories.includes(term.category)).length)
    ).join("")).join("");
}

function cardHTML(term, route) {
  const contexts = contextsFor(term, sourceMap);
  return `<a class="term-card" href="${escapeHTML(routeHash({ ...route, term: term.id }))}">
    <div class="card-top"><span class="category-label">${escapeHTML(CATEGORY_LABELS[term.category] ?? term.category)}</span><span class="card-arrow" aria-hidden="true">↗</span></div>
    <h3>${highlight(term.term, route.q)}</h3>
    <div class="card-aliases">${term.aliases.length ? highlight(term.aliases.join(" / "), route.q) : "—"}</div>
    <p class="card-definition">${highlight(term.definition, route.q)}</p>
    <div class="card-footer"><span class="card-contexts">${contexts.map(context => `<span>${CONTEXT_LABELS[context]}</span>`).join("") || "资料整理"}</span>${term.status === "unverified" ? '<span class="pending-label">待核实</span>' : '<span aria-hidden="true">查看词条 →</span>'}</div>
  </a>`;
}

function renderBrowse(route) {
  const category = CATEGORIES.find(item => item.id === route.category);
  const terms = findTerms(index, route);
  const filtered = Boolean(route.q || category || route.source !== "all");
  $("#page-heading").innerHTML = `${escapeHTML(category?.label ?? "名字竞技场百科")}<span class="heading-dot">.</span>`;
  $("#page-description").textContent = category?.description ?? "从玩法与评分，到工具与圈内黑话。";
  $("#breadcrumb-current").textContent = category?.label ?? "全部词条";
  $("#search-input").value = route.q;
  $("#source-select").value = route.source;
  $("#results-title").textContent = route.q ? "搜索结果" : category?.label ?? "全部词条";
  $("#result-count").textContent = terms.length;
  $("#start-guide").hidden = filtered;
  $("#search-status").textContent = route.q
    ? `“${route.q}” · 找到 ${terms.length} 个词条，名称与别名优先`
    : filtered ? `${category?.label ?? "全部分类"} · ${$("#source-select").selectedOptions[0].textContent} · 共 ${terms.length} 个词条`
      : "按分类探索，或搜索你遇到的一个词。";
  $("#results").innerHTML = terms.slice(0, limit).map(term => cardHTML(term, route)).join("");
  $("#empty-state").hidden = terms.length !== 0;
  $("#load-more").hidden = terms.length <= limit;
  $("#load-more").innerHTML = `继续浏览 <span class="more-count">${Math.min(PAGE_SIZE, terms.length - limit)}</span> 个词条 <span aria-hidden="true">↓</span>`;
  document.title = `${route.q ? `搜索：${route.q}` : category?.label ?? "名字竞技场知识库"} · 名竞百科`;
}

function sourceHTML(source, number) {
  const url = safeURL(source.url);
  const title = `${escapeHTML(source.title)}${url ? ' <span aria-hidden="true">↗</span>' : ""}`;
  const date = source.accessed_at ?? source.recorded_at;
  return `<div class="source-entry">
    <div class="source-entry-title"><span class="source-number">${String(number).padStart(2, "0")}</span>${url ? `<a href="${escapeHTML(url)}" target="_blank" rel="noopener noreferrer">${title}</a>` : title}</div>
    <small>${escapeHTML(SOURCE_LABELS[source.type] ?? "参考资料")}${date ? ` · 核查/记录于 ${escapeHTML(date)}` : ""}${source.commit ? ` · 提交 ${escapeHTML(source.commit.slice(0, 7))}` : ""}</small>
    ${source.notes ? `<p>${escapeHTML(source.notes)}</p>` : ""}
  </div>`;
}

function factsHTML(term) {
  const detail = knowledge.details[term.id];
  if (!detail) return "";
  const labels = { category: "官方分类", attribute: "技能属性", damage: "伤害", input: "完整输入", origin: "出处" };
  const facts = Object.entries(labels).filter(([key]) => detail[key]);
  return facts.length ? `<dl class="facts-grid">${facts.map(([key, label]) => `<div class="fact"><dt>${label}</dt><dd>${escapeHTML(detail[key])}</dd></div>`).join("")}</dl>` : "";
}

function renderDetail(route) {
  const term = termMap.get(route.term);
  const backHash = escapeHTML(routeHash({ ...route, term: "" }));
  if (!term) {
    $("#breadcrumb-current").textContent = "未收录词条";
    $("#detail-view").innerHTML = `<a class="back-link" href="${backHash}">← 返回词条列表</a><div class="empty-state"><h1 id="article-title" tabindex="-1">这个词条尚未收录</h1><p>链接可能已经变更，可以返回列表搜索。</p></div>`;
    document.title = "未收录词条 · 名竞百科";
    return;
  }
  $("#breadcrumb-current").textContent = term.term;
  document.title = `${term.term} · 名竞百科`;
  const sources = term.source_ids.map(id => sourceMap.get(id)).filter(Boolean);
  const contexts = contextsFor(term, sourceMap);
  const notes = term.context_notes ?? [];
  const siblings = knowledge.terms.filter(other => other.category === term.category && other.id !== term.id).slice(0, 5);
  $("#detail-view").innerHTML = `
    <a class="back-link" href="${backHash}"><span aria-hidden="true">←</span> 返回词条列表${route.q ? ` · ${escapeHTML(route.q)}` : ""}</a>
    <div class="article-layout"><article>
      <header class="article-header">
        <div class="article-category">${escapeHTML(CATEGORY_LABELS[term.category] ?? term.category)}${term.status === "unverified" ? '<span class="pending-label">待核实</span>' : ""}</div>
        <h1 id="article-title" tabindex="-1">${escapeHTML(term.term)}</h1>
        ${term.aliases.length ? `<div class="article-aliases"><span>也称</span>${term.aliases.map(alias => `<span class="alias-chip">${escapeHTML(alias)}</span>`).join("")}</div>` : ""}
        <div class="article-meta"><span>核查于 ${escapeHTML(term.checked_at)}</span><span>${sources.length} 项来源</span><span>${contexts.map(context => CONTEXT_LABELS[context]).join(" · ")}</span></div>
      </header>
      <section class="article-section" id="article-definition"><h2>词条释义</h2><p class="article-lead">${escapeHTML(term.definition)}</p>
        ${term.status === "unverified" ? '<p class="notice">该词的具体含义或门槛仍待核实，请保留原句和来源语境。</p>' : ""}
        ${factsHTML(term)}
        <div class="scope-box"><strong>适用范围</strong><p>${escapeHTML(term.scope)}</p></div>
      </section>
      ${notes.length ? `<section class="article-section" id="article-context"><h2>不同语境中的解释</h2>${notes.map(note => `<div class="context-note"><h3>${note.context_id.startsWith("tswn-") ? "tswn 实现补充" : "社区语境补充"}</h3><p>${escapeHTML(note.explanation)}</p><p class="context-scope">${escapeHTML(note.scope)} · 核查于 ${escapeHTML(note.checked_at)}</p></div>`).join("")}</section>` : ""}
      <section class="article-section" id="article-sources"><h2>参考来源</h2>${sources.map((source, i) => sourceHTML(source, i + 1)).join("")}<p class="source-disclaimer">核查日期表示资料整理时间。实现、历史说明与社区活动分别保留自己的适用范围。</p></section>
      ${siblings.length ? `<section class="article-section" id="article-related"><h2>同类词条</h2><div class="related-links">${siblings.map(other => `<a href="${escapeHTML(routeHash({ ...route, term: other.id }))}">${escapeHTML(other.term)} ↗</a>`).join("")}</div></section>` : ""}
    </article><aside class="article-toc" aria-label="本页目录"><h2>本页内容</h2><a href="${escapeHTML(routeHash(route))}" data-scroll="article-definition">词条释义</a>${notes.length ? `<a href="${escapeHTML(routeHash(route))}" data-scroll="article-context">语境补充</a>` : ""}<a href="${escapeHTML(routeHash(route))}" data-scroll="article-sources">参考来源 <span>(${sources.length})</span></a>${siblings.length ? `<a href="${escapeHTML(routeHash(route))}" data-scroll="article-related">同类词条</a>` : ""}<p class="toc-note">同一个词，在不同实现与时期中可能有不同含义。</p></aside></div>`;
}

function renderRoute() {
  if (!knowledge) return;
  const route = parseRoute(location.hash);
  if (["q", "category", "source"].some(key => route[key] !== previousRoute[key])) limit = PAGE_SIZE;
  renderNavigation(route);
  $("#browse-view").hidden = Boolean(route.term);
  $("#detail-view").hidden = !route.term;
  if (route.term) renderDetail(route); else renderBrowse(route);
  const changedPage = route.term !== previousRoute.term || route.category !== previousRoute.category;
  previousRoute = route;
  setMenu(false);
  if (changedPage) {
    window.scrollTo({ top: 0, behavior: "instant" });
    if (route.term) $("#article-title")?.focus({ preventScroll: true });
  }
}

async function loadKnowledge() {
  $("#loading").hidden = false;
  $("#error-view").hidden = true;
  try {
    const response = await fetch(new URL("./data/knowledge.json", import.meta.url));
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data.terms) || !Array.isArray(data.sources)) throw new Error("知识文件格式异常");
    knowledge = data;
    termMap = new Map(data.terms.map(term => [term.id, term]));
    sourceMap = new Map(data.sources.map(source => [source.id, source]));
    index = createIndex(data.terms, data.sources);
    $("#term-count").textContent = data.terms.length;
    $("#source-count").textContent = data.sources.length;
    $("#checked-date").textContent = data.checked_at;
    $("#checked-date").dateTime = data.checked_at;
    renderRoute();
  } catch (error) {
    $("#browse-view").hidden = true;
    $("#detail-view").hidden = true;
    $("#error-view").hidden = false;
    $("#error-message").textContent = location.protocol === "file:"
      ? "请在项目目录运行 python scripts/serve_wiki.py，再打开终端中显示的本地网址。"
      : `知识文件加载失败（${error.message}）。请检查本地服务是否运行，或重新加载。`;
  } finally { $("#loading").hidden = true; }
}

function scheduleSearch(event) {
  clearTimeout(inputTimer);
  if (event.isComposing) return;
  inputTimer = setTimeout(() => updateRoute({ q: event.target.value, term: "" }, { replace: true }), 140);
}
$("#search-input").addEventListener("input", scheduleSearch);
$("#search-input").addEventListener("compositionstart", () => clearTimeout(inputTimer));
$("#search-input").addEventListener("compositionend", scheduleSearch);
$("#search-form").addEventListener("submit", event => {
  event.preventDefault();
  clearTimeout(inputTimer);
  updateRoute({ q: $("#search-input").value, term: "" });
});
$("#source-select").addEventListener("change", event => updateRoute({ source: event.target.value }));
$("#load-more").addEventListener("click", () => {
  const previousCount = $("#results").children.length;
  limit += PAGE_SIZE;
  renderBrowse(parseRoute(location.hash));
  $("#results").children[previousCount]?.focus({ preventScroll: true });
});
$("#clear-filters").addEventListener("click", () => updateRoute({ q: "", category: "all", source: "all", term: "" }));
$("#retry-load").addEventListener("click", loadKnowledge);
$("#menu-toggle").addEventListener("click", () => setMenu($("#menu-toggle").getAttribute("aria-expanded") !== "true"));
$("#nav-backdrop").addEventListener("click", () => setMenu(false));
document.addEventListener("click", event => {
  if (event.target.closest(".skip-link")) {
    event.preventDefault();
    $("#main").focus();
    $("#main").scrollIntoView();
    return;
  }
  const query = event.target.closest("[data-query]");
  if (query) updateRoute({ q: query.dataset.query, term: "" });
  const anchor = event.target.closest("[data-scroll]");
  if (anchor) { event.preventDefault(); document.getElementById(anchor.dataset.scroll)?.scrollIntoView(); }
});
document.addEventListener("keydown", event => {
  if (event.key === "Escape") { setMenu(false); $("#menu-toggle").focus({ preventScroll: true }); }
  const editing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName) || document.activeElement?.isContentEditable;
  if (((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") || (event.key === "/" && !editing)) {
    event.preventDefault();
    if (parseRoute(location.hash).term) updateRoute({ term: "" }, { replace: true });
    $("#search-input").focus();
    $("#search-input").select();
    $("#search-form").scrollIntoView({ block: "center" });
  }
});
window.addEventListener("hashchange", () => { clearTimeout(inputTimer); renderRoute(); });
loadKnowledge();
