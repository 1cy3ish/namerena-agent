export const CATEGORY_GROUPS = [
  { title: "游戏与玩法", items: [
    { id: "concept", label: "基础概念", categories: ["concept"], description: "先认识名竞，再理解名字背后的规则。" },
    { id: "input", label: "命名与输入", categories: ["input"], description: "名字、战队、分组与特殊输入。" },
    { id: "gameplay", label: "游戏玩法", categories: ["gameplay"], description: "从自动对战，到测号与实力评估。" },
    { id: "attribute", label: "角色属性", categories: ["attribute"], description: "角色属性及其在对战中的作用。" },
    { id: "skill", label: "技能词典", categories: ["skill"], description: "攻击、辅助与被动技能的含义和实现。" },
    { id: "mechanics", label: "对战机制", categories: ["mechanics"], description: "状态、判胜与战斗过程中的细节。" },
    { id: "special", label: "特殊角色与装备", categories: ["boss", "minion", "equipment"], description: "Boss、召唤物与特殊装备。" },
  ] },
  { title: "测号与开发", items: [
    { id: "rating", label: "评分体系", categories: ["rating"], description: "读懂评分缩写，也分清不同工具的计分语境。" },
    { id: "tool", label: "命令与工具", categories: ["tool", "command"], description: "测号、开箱、转换与网页工具。" },
    { id: "development", label: "引擎与接口", categories: ["implementation", "api"], description: "重写实现、数据结构与工具开发接口。" },
  ] },
  { title: "社区与赛事", items: [
    { id: "community", label: "社区黑话", categories: ["community"], description: "天梯、帮测、战队基地与社区常用说法。" },
    { id: "competition", label: "比赛与赛制", categories: ["competition"], description: "周赛、锦标赛与参赛相关术语。" },
    { id: "forum", label: "论坛分区", categories: ["forum-tag"], description: "认识论坛中的各个讨论分区。" },
  ] },
];

export const CATEGORIES = CATEGORY_GROUPS.flatMap(group => group.items);
export const CATEGORY_LABELS = {
  concept: "基础概念", gameplay: "游戏玩法", input: "命名与输入", rating: "评分体系",
  command: "命令", tool: "工具", attribute: "角色属性", mechanics: "对战机制", boss: "Boss",
  implementation: "引擎实现", minion: "召唤物", equipment: "装备", api: "开发接口",
  skill: "技能", community: "社区黑话", competition: "比赛与赛制", "forum-tag": "论坛分区",
};

export const normalize = value => String(value ?? "").normalize("NFKC").toLocaleLowerCase("zh-CN").trim();
export const tokensFor = query => normalize(query).split(/\s+/u).filter(Boolean);
export const categoryFor = term => CATEGORIES.find(category => category.categories.includes(term.category));

export function contextsFor(term, sourceMap) {
  const types = new Set((term.source_ids ?? []).map(id => sourceMap.get(id)?.type));
  return [
    types.has("official") && "official",
    (types.has("repository") || types.has("deployment")) && "tswn",
    (types.has("community") || types.has("maintainer") || types.has("maintainer_statement")) && "community",
  ].filter(Boolean);
}

export function createIndex(terms, sources) {
  const sourceMap = new Map(sources.map(source => [source.id, source]));
  return terms.map(term => ({
    term,
    name: normalize(term.term),
    aliases: (term.aliases ?? []).map(normalize),
    text: normalize([term.term, ...(term.aliases ?? []), term.definition, term.scope,
      ...(term.context_notes ?? []).flatMap(note => [note.explanation, note.scope])].join("\n")),
    contexts: contextsFor(term, sourceMap),
  }));
}

export function findTerms(index, { q = "", category = "all", source = "all" } = {}) {
  const words = tokensFor(q);
  const selected = CATEGORIES.find(item => item.id === category);
  return index.filter(entry =>
    (!selected || selected.categories.includes(entry.term.category)) &&
    (source === "all" || entry.contexts.includes(source)) &&
    words.every(word => entry.text.includes(word))
  ).map(entry => ({
    term: entry.term,
    score: words.reduce((score, word) => score + (
      entry.name === word ? 100 : entry.aliases.includes(word) ? 90 :
      entry.name.startsWith(word) ? 65 : entry.name.includes(word) ? 50 :
      entry.aliases.some(alias => alias.includes(word)) ? 35 : 1
    ), 0),
  })).sort((a, b) => b.score - a.score).map(entry => entry.term);
}

export function parseRoute(hash) {
  const params = new URLSearchParams(hash.replace(/^#/, ""));
  const category = params.get("category") ?? "all";
  const source = params.get("source") ?? "all";
  return { q: params.get("q") ?? "", term: params.get("term") ?? "",
    category: CATEGORIES.some(item => item.id === category) ? category : "all",
    source: ["all", "official", "tswn", "community"].includes(source) ? source : "all" };
}

export function routeHash(route) {
  const params = new URLSearchParams();
  for (const key of ["category", "q", "source", "term"]) {
    if (route[key] && route[key] !== "all") params.set(key, route[key]);
  }
  return params.size ? `#${params}` : "#";
}
