import assert from 'node:assert/strict';
import {
  LEGACY_PROGRESS_V2_STORAGE_KEY,
  PROGRESS_SCHEMA,
  PROGRESS_STORAGE_KEY,
  PROGRESS_VERSION,
  clearProgress,
  initialProgress,
  loadProgress,
  markCleared,
  saveProgress,
} from '../src/progress.mjs';

const campaignId = 'LINKLINE-LAUNCH-1300-V1';
const memory = new Map();
const storage = {
  getItem: (key) => memory.has(key) ? memory.get(key) : null,
  setItem: (key, value) => memory.set(key, value),
  removeItem: (key) => memory.delete(key),
};

memory.set(LEGACY_PROGRESS_V2_STORAGE_KEY, JSON.stringify({
  schema: PROGRESS_SCHEMA,
  version: 2,
  campaignId,
  currentPosition: 106,
  highestCleared: 105,
}));

const migrated = loadProgress(storage, campaignId, 1300);
assert.equal(PROGRESS_VERSION, 3);
assert.equal(PROGRESS_STORAGE_KEY, 'linkline.product.progress.v3');
assert.equal(migrated.currentPosition, 106);
assert.equal(migrated.highestCleared, 105);
assert.deepEqual(migrated.performance, {});
assert.ok(memory.has(PROGRESS_STORAGE_KEY));
assert.equal(memory.has(LEGACY_PROGRESS_V2_STORAGE_KEY), false);

clearProgress(storage);
assert.equal(memory.has(PROGRESS_STORAGE_KEY), false);
assert.equal(memory.has(LEGACY_PROGRESS_V2_STORAGE_KEY), false);
const reset = loadProgress(storage, campaignId, 1300);
assert.deepEqual(reset, initialProgress(campaignId));

const clearedStage1 = markCleared(reset, 1, 1300);
saveProgress(storage, clearedStage1);
const reloaded = loadProgress(storage, campaignId, 1300);
assert.equal(reloaded.currentPosition, 2);
assert.equal(reloaded.highestCleared, 1);
assert.equal(reloaded.version, 3);
assert.deepEqual(reloaded.performance, {});

console.log('PASS progress v3 migrates v2, reset removes both keys, and new progress persists');
