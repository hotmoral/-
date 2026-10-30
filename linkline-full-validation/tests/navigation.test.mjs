import assert from 'node:assert/strict';
import { completionPercent, continuePosition, pageRows, stagePage, stageState } from '../src/navigation.mjs';

const total = 1300;
assert.equal(continuePosition({ highestCleared: 0 }, total), 1);
assert.equal(continuePosition({ highestCleared: 50 }, total), 51);
assert.equal(continuePosition({ highestCleared: 1300 }, total), 1300);
assert.equal(stageState(50, { highestCleared: 50 }, total), 'completed');
assert.equal(stageState(51, { highestCleared: 50 }, total), 'current');
assert.equal(stageState(52, { highestCleared: 50 }, total), 'locked');
assert.equal(stageState(1300, { highestCleared: 1300 }, total), 'completed-current');
assert.deepEqual(stagePage(237, total), { pageIndex: 7, start: 211, end: 240, pageSize: 30 });
assert.deepEqual(pageRows(stagePage(237, total)), [
  [211, 212, 213, 214, 215],
  [216, 217, 218, 219, 220],
  [221, 222, 223, 224, 225],
  [226, 227, 228, 229, 230],
  [231, 232, 233, 234, 235],
  [236, 237, 238, 239, 240],
]);
assert.equal(completionPercent({ highestCleared: 650 }, total), 50);
console.log('PASS navigation: continue/current/locked semantics, 30-stage paging, progress percentage');
