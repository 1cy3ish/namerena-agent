import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { CATEGORIES, createIndex, findTerms, parseRoute, routeHash } from "../web/search.mjs";

const terms = JSON.parse(readFileSync(new URL("../knowledge/glossary.json", import.meta.url))).terms;
const sources = JSON.parse(readFileSync(new URL("../knowledge/sources.json", import.meta.url))).sources;
const index = createIndex(terms, sources);

test("every existing term belongs to exactly one browsing category", () => {
  for (const term of terms) {
    assert.equal(CATEGORIES.filter(category => category.categories.includes(term.category)).length, 1, term.id);
  }
  assert.equal(findTerms(index).length, terms.length);
});

test("QP alias ranks before mentions in registration policies", () => {
  const result = findTerms(index, { q: "QP" });
  assert.equal(result[0].id, "enhanced-team-rating");
  assert.ok(result.some(term => term.id === "ladder-qp-verification"));
});

test("case and full-width input produce the same results", () => {
  assert.deepEqual(findTerms(index, { q: "  ＱＰ  " }), findTerms(index, { q: "qp" }));
});

test("multiple keywords require all words, regardless of order", () => {
  const result = findTerms(index, { q: "周赛 激活" });
  assert.ok(result.some(term => term.id === "ladder-weekly-activation"));
  assert.deepEqual(result.map(term => term.id).sort(), findTerms(index, { q: "激活 周赛" }).map(term => term.id).sort());
  assert.equal(findTerms(index, { q: "周赛 zzz-no-such-word" }).length, 0);
});

test("search includes contextual explanations of existing terms", () => {
  assert.ok(findTerms(index, { q: "队友" }).some(term => term.id === "enhanced-team-rating"));
});

test("category and source filters compose without hiding mixed evidence", () => {
  const result = findTerms(index, { q: "qp", category: "rating", source: "community" });
  assert.ok(result.some(term => term.id === "enhanced-team-rating"));
  assert.ok(result.every(term => term.category === "rating"));
  assert.equal(findTerms(index, { category: "forum", source: "official" }).length, 0);
});

test("deep links preserve Chinese and special input characters", () => {
  const route = { category: "input", q: "名字+装备 @战队 # seed:S1@!", source: "official", term: "random-seed" };
  assert.deepEqual(parseRoute(routeHash(route)), route);
});

test("unknown filters fall back to a usable full index", () => {
  assert.deepEqual(parseRoute("#category=missing&source=missing"), { q: "", term: "", category: "all", source: "all" });
});
