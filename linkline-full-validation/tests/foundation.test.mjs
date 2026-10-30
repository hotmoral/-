import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import * as mechanic from '../src/mechanic.mjs';
import { assembleChunkedCampaign, CANONICAL_V4_CATALOG_FINGERPRINT, FROZEN_CATALOG_FINGERPRINT, FROZEN_ORDER_FINGERPRINT } from '../src/catalog.mjs';
import { initialProgress, isAvailablePrefixComplete, loadProgress, markCleared, saveProgress } from '../src/progress.mjs';

const manifest = JSON.parse(await readFile(new URL('../data/campaign-0001-1300.json', import.meta.url), 'utf8'));
const chunks = [];
for (const descriptor of manifest.chunks) {
  const bytes = await readFile(new URL(`../data/${descriptor.path}`, import.meta.url));
  assert.equal(createHash('sha256').update(bytes).digest('hex'), descriptor.sha256);
  chunks.push(JSON.parse(bytes.toString('utf8')));
}
const campaign = await assembleChunkedCampaign(manifest, chunks);
assert.equal(campaign.contentStatus, 'FROZEN_LAUNCH_COMPLETE');
assert.equal(campaign.puzzles.length, 1300);
assert.equal(campaign.materializedThroughPosition, 1300);
assert.equal(campaign.source.catalogFingerprint, FROZEN_CATALOG_FINGERPRINT);
assert.equal(campaign.source.canonicalV4CatalogFingerprint, CANONICAL_V4_CATALOG_FINGERPRINT);
assert.equal(campaign.source.orderFingerprint, FROZEN_ORDER_FINGERPRINT);
assert.equal(campaign.source.orderPrefixFingerprint, FROZEN_ORDER_FINGERPRINT);
assert.equal(campaign.source.validationFingerprint, '0f6fd5feefdf110ef436496e4d580b0c150aeb6c59eb1636ad200f24ad582639');
assert.equal(campaign.source.workgroupDManifestFingerprint, '79d2e559f3992395cf9b491e8a9ba6c7f3c135411a3acf480f83244231e685d6');
assert.equal(campaign.source.publicSelectionFingerprint, 'ae1af8798d71a1bd7bf487f382f5cb9ec82ba04b469dd67bd325c11a32b8f802');
assert.equal(campaign.source.repairCount, 6);

const ids = campaign.puzzles.map((row) => row.id);
const orderFingerprint = createHash('sha256').update(JSON.stringify(ids)).digest('hex');
assert.equal(orderFingerprint, FROZEN_ORDER_FINGERPRINT);
const prefix50Fingerprint = createHash('sha256').update(JSON.stringify(ids.slice(0, 50))).digest('hex');
assert.equal(prefix50Fingerprint, '032165effa1e64557aa66fdea736e604d7c0cf027c69e6259231e6240787cbbc');

const catalogIdentityPayload = [...campaign.puzzles]
  .sort((a, b) => a.n - b.n || a.length - b.length || a.id.localeCompare(b.id))
  .map((row) => ({ id: row.id, n: row.n, chainLength: row.length, initial: row.initial, targets: row.targets }));
function stableJson(value) {
  if (Array.isArray(value)) return `[${value.map(stableJson).join(',')}]`;
  if (value && typeof value === 'object') return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${stableJson(value[key])}`).join(',')}}`;
  return JSON.stringify(value);
}
const catalogFingerprint = createHash('sha256').update(stableJson(catalogIdentityPayload)).digest('hex');
assert.equal(catalogFingerprint, FROZEN_CATALOG_FINGERPRINT);

for (const puzzle of campaign.puzzles) assert.equal(mechanic.validatePuzzle(puzzle), true);
assert.equal(new Set(ids).size, 1300);
const nCounts = new Map();
const pairCounts = new Map();
for (const puzzle of campaign.puzzles) {
  nCounts.set(puzzle.n, (nCounts.get(puzzle.n) || 0) + 1);
  const pair = [...puzzle.targets].sort((a, b) => a - b);
  const key = `${puzzle.n}:${pair[0]}:${pair[1]}`;
  pairCounts.set(key, (pairCounts.get(key) || 0) + 1);
}
assert.deepEqual(Object.fromEntries([...nCounts].sort((a, b) => a[0] - b[0])), { 3: 36, 4: 120, 5: 514, 6: 630 });
for (const [key, count] of pairCounts) {
  const n = Number(key.split(':')[0]);
  assert.ok(count <= (n <= 4 ? 1 : 2), `target-pair cap exceeded: ${key} x${count}`);
}

const checkpoints = [
  [1, 'dd2456011274f25bddbd29047dae36f01f8799cdfa713b96fc0a501d4f610572', 4],
  [2, 'b43f13d505300ddabfe143f8f7945a24bd3d9185398c45924d9049831a14c609', 3],
  [50, '5544b852bed41ee8a964fb19beb8864bac6a573aa332fc2253da95797d4fc0ad', 4],
  [51, '39f3d3b069a6452be419a23e318a4d69ca742364805a56d363e7cb6ea7202b06', 4],
  [300, '1da26d2d6456b071fe473d3547eb9a7122f5c3968269ef17198eb3dccf0ce230', 5],
  [301, 'ab0c170f2502266873bf142aea243f353c48c6d26f1224aba5b7bed1db545009', 5],
  [521, '001eb54e87c8586386927af54b4c7953106d77d793c8a6b07e2e9f41143a7ab5', 6],
  [1041, '55230c9c18fc5644251c8c843ebe49fe2220c8e5c94bfba737a172cebd7802f1', 6],
  [1300, '62a5b123ae01ae2b6afc37560db5b93724ba3738334cff7a432fa14f1f792aba', 6],
];
for (const [position, id, n] of checkpoints) {
  const row = campaign.puzzles[position - 1];
  assert.equal(row.position, position);
  assert.equal(row.id, id);
  assert.equal(row.n, n);
}

const smoke = { n:3, length:3, initial:[0,1,2], targets:[1,3] };
let path = mechanic.canonicalPath(smoke.initial);
path = mechanic.applyMove(3, path, 0, 3);
assert.equal(mechanic.isSolved(path, smoke.targets), true);

const indexHtml = await readFile(new URL('../index.html', import.meta.url), 'utf8');
for (const marker of [
  'user-scalable=no', 'FIRST_RETRY_MS=52, RETRY_MS=8, MAX_RETRIES=24',
  'SAMPLE_RATIO=.12, MIN_SAMPLE_PX=3, MAX_SAMPLE_PX=8', "event.getCoalescedEvents==='function'",
  'document.documentElement.setPointerCapture(event.pointerId)',
  'document.documentElement.releasePointerCapture(event.pointerId)', 'performance.now()+350', 'delay===140?48:delay',
]) assert.ok(indexHtml.includes(marker), `missing v0.4 drag marker: ${marker}`);

const memory = new Map();
const storage = { getItem:(key)=>memory.has(key)?memory.get(key):null, setItem:(key,value)=>memory.set(key,value), removeItem:(key)=>memory.delete(key) };
let progress = initialProgress(campaign.campaignId);
progress = markCleared(progress, 50, 50);
saveProgress(storage, progress);
const afterFullExpansion = loadProgress(storage, campaign.campaignId, 1300);
assert.equal(afterFullExpansion.currentPosition, 51);
assert.equal(afterFullExpansion.highestCleared, 50);
assert.equal(isAvailablePrefixComplete(afterFullExpansion, 1300), false);
progress = markCleared(afterFullExpansion, 1300, 1300);
saveProgress(storage, progress);
const afterFinalReload = loadProgress(storage, campaign.campaignId, 1300);
assert.equal(afterFinalReload.currentPosition, 1300);
assert.equal(afterFinalReload.highestCleared, 1300);
assert.equal(isAvailablePrefixComplete(afterFinalReload, 1300), true);
console.log('PASS foundation difficulty-rebalanced: 1..1300 chunk/hash/catalog/order/pair caps, v0.4 drag, progress');
