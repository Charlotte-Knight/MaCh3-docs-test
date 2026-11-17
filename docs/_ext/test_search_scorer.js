const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const source = fs.readFileSync(
  path.join(__dirname, "../_static/search-scorer.js"), "utf8",
);
const scorer = vm.runInNewContext(`${source}\nScorer`);
const result = (docname, score, anchor = "", kind = undefined) =>
  [docname, "", anchor, "", score, "", kind];

assert.equal(scorer.score(result("api/class_example", 31)), 11);
assert.equal(scorer.score(result("api/_navigation/symbols/index", 5)), -15);
assert.equal(scorer.score(result("user-guide/example", 15)), 15);
assert.equal(scorer.score(result("pymach3/samples", 15)), 15);
assert.equal(scorer.score(result("pymach3/samples", 26, "#pyMaCh3._pyMaCh3.samples", "object")), 6);
assert.equal(scorer.score(result("pymach3/splines", 26, "#module-pyMaCh3._pyMaCh3.splines")), 6);
assert.equal(scorer.score(result("pymach3/splines", 15, "#api-reference", "title")), -5);
assert.equal(scorer.score(result("pymach3/splines", 15, "#event-by-event-splines", "title")), 15);
assert.equal(scorer.score(result("user-guide/example", 15, "#api-reference", "title")), 15);
assert.equal(scorer.score(result("tutorials/index", 5)), 5);
assert.equal(scorer.score(result("api-guide/example", 5)), 5);
