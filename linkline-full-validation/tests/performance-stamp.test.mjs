import assert from 'node:assert/strict';
import { gradePerformance, validatePerformanceBaseline } from '../src/performance.mjs';
import { clearProgress, initialProgress, loadProgress, performanceAt, recordPerformance, saveProgress } from '../src/progress.mjs';
import { activateCell, createPuzzleRuntime } from '../src/runtime.mjs';

const campaignId = 'LINKLINE-LAUNCH-1300-V1';
const baseline = validatePerformanceBaseline({
  schema: 'LINKLINE_PERFORMANCE_BASELINE',
  version: '1.0.0',
  campaignId,
  launchTotal: 3,
  metric: 'M3_V1_SHORTEST_DISTANCE',
  moveUnit: 'accepted authoritative one-cell M2 action',
  rowEncoding: ['position', 'shortestDistance'],
  rows: [[1, 4], [2, 1], [3, 7]],
}, campaignId, 3);

assert.equal(gradePerformance(4, 4).grade, 'S+');
assert.equal(gradePerformance(5, 4).grade, 'A+');
assert.equal(gradePerformance(6, 4).grade, 'B+');
assert.equal(gradePerformance(12, 4).grade, 'B+');
assert.deepEqual(gradePerformance(3, 4), { ok: false, reason: 'PERFORMANCE_BELOW_OPTIMUM', moves: 3, shortestDistance: 4 });

let progress = initialProgress(campaignId);
progress = recordPerformance(progress, 1, gradePerformance(7, 4));
assert.deepEqual(performanceAt(progress, 1), { bestMoves: 7, grade: 'B+' });
progress = recordPerformance(progress, 1, gradePerformance(6, 4));
assert.deepEqual(performanceAt(progress, 1), { bestMoves: 6, grade: 'B+' });
progress = recordPerformance(progress, 1, gradePerformance(5, 4));
assert.deepEqual(performanceAt(progress, 1), { bestMoves: 5, grade: 'A+' });
progress = recordPerformance(progress, 1, gradePerformance(4, 4));
assert.deepEqual(performanceAt(progress, 1), { bestMoves: 4, grade: 'S+' });
const frozenBest = progress;
progress = recordPerformance(progress, 1, gradePerformance(8, 4));
assert.strictEqual(progress, frozenBest);
progress = recordPerformance(progress, 1, gradePerformance(3, 4));
assert.strictEqual(progress, frozenBest);

const movePuzzle = { n: 3, length: 3, initial: [0, 1, 2], targets: [6, 8] };
let runtime = createPuzzleRuntime(movePuzzle);
assert.equal(runtime.moves, 0);
runtime = activateCell(movePuzzle, runtime, 2);
assert.equal(runtime.moves, 0);
runtime = activateCell(movePuzzle, runtime, 4);
assert.equal(runtime.moves, 0);
runtime = activateCell(movePuzzle, runtime, 5);
assert.equal(runtime.moves, 1);
runtime = activateCell(movePuzzle, runtime, 5);
assert.equal(runtime.moves, 1);
runtime = activateCell(movePuzzle, runtime, 8);
assert.equal(runtime.moves, 2);

const memory = new Map();
const storage = {
  getItem: (key) => memory.has(key) ? memory.get(key) : null,
  setItem: (key, value) => memory.set(key, value),
  removeItem: (key) => memory.delete(key),
};
memory.set('linkline.product.progress.v2', JSON.stringify({
  schema: 'LINKLINE_PRODUCT_PROGRESS', version: 2, campaignId, currentPosition: 3, highestCleared: 2,
}));
const migrated = loadProgress(storage, campaignId, 3, baseline);
assert.equal(migrated.version, 3);
assert.equal(migrated.currentPosition, 3);
assert.equal(migrated.highestCleared, 2);
assert.deepEqual(migrated.performance, {});
assert.ok(memory.has('linkline.product.progress.v3'));
assert.equal(memory.has('linkline.product.progress.v2'), false);

memory.set('linkline.product.progress.v3', JSON.stringify({
  ...migrated,
  performance: {
    1: { bestMoves: 4, grade: 'S+' },
    2: { bestMoves: 2, grade: 'B+' },
    3: { bestMoves: 6, grade: 'S+' },
  },
}));
const sanitized = loadProgress(storage, campaignId, 3, baseline);
assert.deepEqual(sanitized.performance, {
  1: { bestMoves: 4, grade: 'S+' },
});

saveProgress(storage, sanitized);
memory.set('linkline.product.progress.v2', JSON.stringify({ schema: 'LINKLINE_PRODUCT_PROGRESS', version: 2, campaignId, currentPosition: 3, highestCleared: 2 }));
clearProgress(storage);
assert.equal(memory.has('linkline.product.progress.v3'), false);
assert.equal(memory.has('linkline.product.progress.v2'), false);
assert.deepEqual(loadProgress(storage, campaignId, 3, baseline), initialProgress(campaignId));

console.log('PASS Performance Stamp v1 grading, move accounting, best-ever persistence, v2->v3 migration, integrity filtering');
