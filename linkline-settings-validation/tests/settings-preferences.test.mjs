import assert from 'node:assert/strict';
import {
  PRODUCT_PROGRESS_STORAGE_KEY,
  PRODUCT_SETTINGS_SCHEMA,
  PRODUCT_SETTINGS_STORAGE_KEY,
  PRODUCT_SETTINGS_VERSION,
  initialProductSettings,
  loadPerformanceSummary,
  loadProductSettings,
  saveProductSettings,
  setProductSetting,
  summarizePerformanceRecords,
} from '../src/settings-preferences.mjs';

const memory = new Map();
const storage = {
  getItem: (key) => memory.has(key) ? memory.get(key) : null,
  setItem: (key, value) => memory.set(key, value),
};

assert.deepEqual(loadProductSettings(storage), initialProductSettings());
assert.equal(loadProductSettings(storage).vibration, true);
assert.equal(loadProductSettings(storage).sound, true);

const vibrationDisabled = setProductSetting(storage, 'vibration', false);
assert.equal(vibrationDisabled.vibration, false);
assert.equal(vibrationDisabled.sound, true);

const soundDisabled = setProductSetting(storage, 'sound', false);
assert.equal(soundDisabled.vibration, false);
assert.equal(soundDisabled.sound, false);

const stored = JSON.parse(memory.get(PRODUCT_SETTINGS_STORAGE_KEY));
assert.equal(stored.schema, PRODUCT_SETTINGS_SCHEMA);
assert.equal(stored.version, PRODUCT_SETTINGS_VERSION);
assert.equal(stored.vibration, false);
assert.equal(stored.sound, false);

saveProductSettings(storage, { vibration: true, sound: true });
assert.equal(loadProductSettings(storage).vibration, true);
assert.equal(loadProductSettings(storage).sound, true);

memory.set(PRODUCT_SETTINGS_STORAGE_KEY, '{broken-json');
assert.deepEqual(loadProductSettings(storage), initialProductSettings());

memory.set(PRODUCT_SETTINGS_STORAGE_KEY, JSON.stringify({ schema: 'WRONG', version: 1, vibration: false, sound: false }));
assert.deepEqual(loadProductSettings(storage), initialProductSettings());

assert.throws(() => setProductSetting(storage, 'unknown', true), /UNKNOWN_PRODUCT_SETTING/);

const summary = summarizePerformanceRecords({
  highestCleared: 8,
  performance: {
    1: { bestMoves: 1, grade: 'S+' },
    2: { bestMoves: 3, grade: 'A+' },
    3: { bestMoves: 5, grade: 'B+' },
    4: { bestMoves: 4, grade: 'S+' },
    5: { bestMoves: 9, grade: 'INVALID' },
    6: null,
  },
});
assert.deepEqual(summary, { completed: 8, sPlus: 2, aPlus: 1, bPlus: 1 });

memory.set(PRODUCT_PROGRESS_STORAGE_KEY, JSON.stringify({
  schema: 'LINKLINE_PRODUCT_PROGRESS',
  version: 3,
  campaignId: 'LINKLINE-LAUNCH-1300-V1',
  currentPosition: 9,
  highestCleared: 8,
  performance: {
    1: { bestMoves: 1, grade: 'S+' },
    2: { bestMoves: 3, grade: 'A+' },
    3: { bestMoves: 5, grade: 'B+' },
  },
}));
assert.deepEqual(loadPerformanceSummary(storage), { completed: 8, sPlus: 1, aPlus: 1, bPlus: 1 });

memory.set(PRODUCT_PROGRESS_STORAGE_KEY, JSON.stringify({ schema: 'WRONG', version: 3, highestCleared: 99 }));
assert.deepEqual(loadPerformanceSummary(storage), { completed: 0, sPlus: 0, aPlus: 0, bPlus: 0 });

memory.set(PRODUCT_PROGRESS_STORAGE_KEY, '{broken-json');
assert.deepEqual(loadPerformanceSummary(storage), { completed: 0, sPlus: 0, aPlus: 0, bPlus: 0 });

console.log('PASS product settings persist feedback preferences and summarize best-ever grade records safely');
