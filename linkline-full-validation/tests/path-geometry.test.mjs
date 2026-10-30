import assert from 'node:assert/strict';
import { roundedOrthogonalPath } from '../src/path-geometry.mjs';

assert.equal(
  roundedOrthogonalPath([0, 1, 2], 3),
  'M 16.667 16.667 L 50 16.667 L 83.333 16.667',
);

assert.equal(
  roundedOrthogonalPath([0, 1, 4], 3),
  'M 16.667 16.667 L 42.667 16.667 Q 50 16.667 50 24 L 50 50',
);

assert.equal(
  roundedOrthogonalPath([6, 3, 4], 3),
  'M 16.667 83.333 L 16.667 57.333 Q 16.667 50 24 50 L 50 50',
);

assert.equal(
  roundedOrthogonalPath([0], 3),
  'M 16.667 16.667',
);

console.log('PASS path geometry: straight segments preserved and orthogonal corners rounded');
