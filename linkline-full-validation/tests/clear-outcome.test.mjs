import assert from 'node:assert/strict';
import { access, readFile } from 'node:fs/promises';
import { applyClearedAttempt, latestClearSnapshot } from '../src/clear-outcome.mjs';
import { initialProgress, performanceAt } from '../src/progress.mjs';

const campaignId = 'LINKLINE-LAUNCH-1300-V1';
const baseline = { distances: [undefined, 4, 1, 7] };

let progress = initialProgress(campaignId);
let outcome = applyClearedAttempt(progress, 1, 3, 5, baseline);
progress = outcome.progress;
assert.equal(progress.highestCleared, 1);
assert.equal(progress.currentPosition, 2);
assert.deepEqual(performanceAt(progress, 1), { bestMoves: 5, grade: 'A+' });
assert.equal(outcome.performanceResult.grade, 'A+');
assert.deepEqual(latestClearSnapshot(), {
  version: 1,
  position: 1,
  moves: 5,
  shortestDistance: 4,
  bestMoves: 5,
  grade: 'A+',
});

outcome = applyClearedAttempt(progress, 1, 3, 7, baseline);
assert.strictEqual(outcome.progress, progress);
assert.deepEqual(performanceAt(outcome.progress, 1), { bestMoves: 5, grade: 'A+' });
assert.deepEqual(latestClearSnapshot(), {
  version: 1,
  position: 1,
  moves: 7,
  shortestDistance: 4,
  bestMoves: 5,
  grade: 'B+',
});

const advanced = { ...progress, currentPosition: 3, highestCleared: 2 };
outcome = applyClearedAttempt(advanced, 1, 3, 4, baseline);
assert.equal(outcome.progress.currentPosition, 3);
assert.equal(outcome.progress.highestCleared, 2);
assert.deepEqual(performanceAt(outcome.progress, 1), { bestMoves: 4, grade: 'S+' });
assert.deepEqual(latestClearSnapshot(), {
  version: 1,
  position: 1,
  moves: 4,
  shortestDistance: 4,
  bestMoves: 4,
  grade: 'S+',
});

outcome = applyClearedAttempt(initialProgress(campaignId), 1, 3, 3, baseline);
assert.equal(outcome.progress.highestCleared, 1);
assert.equal(outcome.progress.currentPosition, 2);
assert.equal(performanceAt(outcome.progress, 1), null);
assert.equal(outcome.performanceResult.reason, 'PERFORMANCE_BELOW_OPTIMUM');
assert.deepEqual(latestClearSnapshot(), {
  version: 1,
  position: 1,
  moves: 3,
  shortestDistance: 4,
  bestMoves: null,
  grade: null,
});

outcome = applyClearedAttempt(initialProgress(campaignId), 1, 3, 0, baseline);
assert.equal(outcome.progress.highestCleared, 1);
assert.equal(outcome.performanceResult.reason, 'PERFORMANCE_MOVES');

outcome = applyClearedAttempt(initialProgress(campaignId), 1, 3, 4, null);
assert.equal(outcome.progress.highestCleared, 1);
assert.equal(outcome.performanceResult, null);
assert.equal(latestClearSnapshot().shortestDistance, null);
assert.equal(latestClearSnapshot().moves, 4);

const appSource = await readFile(new URL('../src/app.mjs', import.meta.url), 'utf8');
assert.match(
  appSource,
  /loadPerformanceBaseline\s*\(\s*['"]\.\/data\/performance-baseline-v1\.json['"]\s*,/,
  'missing clear-flow wiring marker: performance baseline loader',
);
for (const marker of [
  'applyClearedAttempt(',
  'runtime.moves,',
  'loadProgress(localStorage, campaign.campaignId, campaign.puzzles.length, performanceBaseline)',
]) {
  assert.ok(appSource.includes(marker), `missing clear-flow wiring marker: ${marker}`);
}

const uiSource = await readFile(new URL('../src/clear-result-ui.mjs', import.meta.url), 'utf8');
for (const marker of [
  "stat('목표', snapshot.shortestDistance)",
  "stat('이번 기록', snapshot.moves, 'current')",
  "stat('최고 기록', snapshot.bestMoves, 'best')",
  "'S+': '/assets/performance-stamps/s-plus-approved.svg?stamp=approved-v3'",
  "'A+': '/assets/performance-stamps/a-plus-approved.svg?stamp=approved-v3'",
  "'B+': '/assets/performance-stamps/b-plus-approved.svg?stamp=approved-v3'",
]) {
  assert.ok(uiSource.includes(marker), `missing clear-result UI marker: ${marker}`);
}
for (const asset of ['s-plus-approved.svg', 'a-plus-approved.svg', 'b-plus-approved.svg']) {
  const assetUrl = new URL(`../assets/performance-stamps/${asset}`, import.meta.url);
  await access(assetUrl);
  const svg = await readFile(assetUrl, 'utf8');
  assert.match(svg, /<svg\b/i, `missing SVG root: ${asset}`);
  assert.match(svg, /viewBox=["']0 0 672 672["']/i, `unexpected SVG viewBox: ${asset}`);
  assert.doesNotMatch(svg, /<image\b/i, `raster image embedded in SVG: ${asset}`);
}

console.log('PASS clear outcome + clear result UI snapshot, replay best retention, and vector grade assets');