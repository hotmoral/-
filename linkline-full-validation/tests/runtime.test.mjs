import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { assembleChunkedCampaign } from '../src/catalog.mjs';
import { activateCell, createPuzzleRuntime, legalCells } from '../src/runtime.mjs';
import { initialProgress, isAvailablePrefixComplete, loadProgress, markCleared, saveProgress } from '../src/progress.mjs';

const manifest = JSON.parse(await readFile(new URL('../data/campaign-0001-1300.json', import.meta.url), 'utf8'));
const chunks = [];
for (const descriptor of manifest.chunks) {
  chunks.push(JSON.parse(await readFile(new URL(`../data/${descriptor.path}`, import.meta.url), 'utf8')));
}
const campaign = await assembleChunkedCampaign(manifest, chunks);
const first = campaign.puzzles[0];
assert.equal(first.id, 'dd2456011274f25bddbd29047dae36f01f8799cdfa713b96fc0a501d4f610572');
assert.equal(first.n, 4);
assert.equal(first.length, 4);
assert.deepEqual(first.initial, [1, 2, 6, 7]);
assert.deepEqual(first.targets, [5, 6]);

let runtime = createPuzzleRuntime(first);
assert.deepEqual(runtime.path, first.initial);
assert.equal(runtime.solved, false);
assert.equal(runtime.selectedEndpoint, null);

// Rebalanced V4 stage 1 solves in one legal endpoint extension: 1 -> 5.
const moves = [[1, 5]];
for (const [endpointCell, destinationCell] of moves) {
  runtime = activateCell(first, runtime, endpointCell);
  assert.notEqual(runtime.selectedEndpoint, null);
  assert.ok(legalCells(first, runtime).includes(destinationCell));
  runtime = activateCell(first, runtime, destinationCell);
}
assert.equal(runtime.solved, true);
assert.deepEqual([runtime.path[0], runtime.path.at(-1)].sort((a, b) => a - b), [...first.targets].sort((a, b) => a - b));

const solvedSnapshot = structuredClone(runtime);
runtime = activateCell(first, runtime, runtime.path[0]);
assert.deepEqual(runtime, solvedSnapshot);

const smoke = { n: 3, length: 3, initial: [0, 1, 2], targets: [1, 3] };
runtime = createPuzzleRuntime(smoke);
runtime = activateCell(smoke, runtime, 0);
assert.notEqual(runtime.selectedEndpoint, null);
runtime = activateCell(smoke, runtime, 0);
assert.equal(runtime.selectedEndpoint, null);

const blocked = { n: 3, length: 4, initial: [0, 3, 4, 1], targets: [1, 4] };
runtime = createPuzzleRuntime(blocked);
runtime = activateCell(blocked, runtime, 0);
assert.equal(runtime.selectedEndpoint, null);

const memory = new Map();
const storage = {
  getItem: (key) => memory.has(key) ? memory.get(key) : null,
  setItem: (key, value) => memory.set(key, value),
  removeItem: (key) => memory.delete(key),
};
let progress = initialProgress(campaign.campaignId);
progress = markCleared(progress, 50, 50);
saveProgress(storage, progress);
const afterExpansion = loadProgress(storage, campaign.campaignId, 1300);
assert.equal(afterExpansion.currentPosition, 51);
assert.equal(afterExpansion.highestCleared, 50);
assert.equal(isAvailablePrefixComplete(afterExpansion, 1300), false);

progress = { ...afterExpansion, currentPosition: 1299, highestCleared: 1298 };
progress = markCleared(progress, 1299, 1300);
assert.equal(progress.currentPosition, 1300);
assert.equal(progress.highestCleared, 1299);
assert.equal(isAvailablePrefixComplete(progress, 1300), false);
progress = markCleared(progress, 1300, 1300);
saveProgress(storage, progress);
const finalReload = loadProgress(storage, campaign.campaignId, 1300);
assert.equal(finalReload.currentPosition, 1300);
assert.equal(finalReload.highestCleared, 1300);
assert.equal(isAvailablePrefixComplete(finalReload, 1300), true);

console.log('PASS runtime V4: stage 1 input/solve, legacy-50 continuation, 1299->1300 completion');
