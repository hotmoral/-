import fs from 'node:fs';
import assert from 'node:assert/strict';

const js = fs.readFileSync(new URL('../public/harness.js', import.meta.url), 'utf8');
const html = fs.readFileSync(new URL('../public/index.html', import.meta.url), 'utf8');

for (const id of ['H0','H1','H2','H3','H4','H5']) {
  assert.match(js, new RegExp(`\\b${id}:\\s*\\{`), `${id} missing from CFG`);
  assert.match(html, new RegExp(`value="${id}"`), `${id} selector option missing`);
}
assert.match(js, /H0:\s*\{[^\n]*goalInputs:\s*80/, 'H0 must expose >=40 inputs');
assert.match(js, /TARGET_REORDER/, 'H3 turnover evidence missing');
assert.match(js, /WINDUP_START/, 'H4 readable state evidence missing');
assert.match(js, /campaignPersistence:false/, 'campaign isolation flag missing');
assert.match(js, /externalTelemetry:false/, 'external telemetry must be disabled');
assert.doesNotMatch(js, /\/api\/room|WebSocket|starThreshold|tierRecords|achievement/i, 'campaign/network persistence token leaked into harness');
assert.match(js, /goodW:\s*\.42/, 'GOOD window mismatch');
assert.match(js, /perfectW:\s*\.17/, 'PERFECT window mismatch');
assert.match(js, /inputLockMs:\s*100/, 'input lock mismatch');
assert.match(js, /heavyYDelayMs:\s*85/, 'heavy Y delay mismatch');
assert.match(js, /recoverMs:\s*390/, 'recovery mismatch');
console.log('HARNESS_SELFTEST PASS');
