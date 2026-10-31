import { validatePuzzle } from './mechanic.mjs';

export const CAMPAIGN_SCHEMA = 'LINKLINE_PRODUCT_CAMPAIGN';
export const CAMPAIGN_CHUNKED_SCHEMA = 'LINKLINE_PRODUCT_CAMPAIGN_CHUNKED';
export const CAMPAIGN_CHUNK_SCHEMA = 'LINKLINE_PRODUCT_CAMPAIGN_CHUNK';
export const CAMPAIGN_SCHEMA_VERSION = '1.1.0';
export const FROZEN_CAMPAIGN_ID = 'LINKLINE-LAUNCH-1300-V1';
export const FROZEN_LAUNCH_TOTAL = 1300;
export const FROZEN_CATALOG_FINGERPRINT = '2780ffd37952ea27f396ce5f152bfda5530537a83c33711e79a496136b8207d7';
export const CANONICAL_V4_CATALOG_FINGERPRINT = '78f5fcf54f0a825d702e0a9b988233622cc4a5cd272e382891ee6c002fce6efe';
export const FROZEN_ORDER_FINGERPRINT = '8766908f3774754ec9384c4531cb8ca8fbe81ed404a8829bb585d25ee3a65f65';
export const IDENTITY_DERIVATION = 'LINKLINE_A3_RESEARCH_EQ_D4_SHA256_V1';

function compareArrays(a, b) {
  for (let i = 0; i < Math.min(a.length, b.length); i++) {
    if (a[i] !== b[i]) return a[i] - b[i];
  }
  return a.length - b.length;
}

function canonicalPath(path) {
  const forward = [...path];
  const reverse = [...path].reverse();
  return compareArrays(forward, reverse) <= 0 ? forward : reverse;
}

function transformCell(n, cell, transform) {
  let row = Math.floor(cell / n);
  let col = cell % n;
  let turns = transform;
  if (turns >= 4) {
    col = n - 1 - col;
    turns -= 4;
  }
  for (let i = 0; i < turns; i++) {
    [row, col] = [col, n - 1 - row];
  }
  return row * n + col;
}

function researchSerialization(puzzle) {
  const variants = [];
  for (let transform = 0; transform < 8; transform++) {
    const path = canonicalPath(puzzle.initial.map((cell) => transformCell(puzzle.n, cell, transform)));
    const targets = puzzle.targets.map((cell) => transformCell(puzzle.n, cell, transform)).sort((a, b) => a - b);
    variants.push(JSON.stringify(['LL_A3_RESEARCH_EQ', 1, puzzle.n, puzzle.length, targets, path]));
  }
  variants.sort();
  return variants[0];
}

async function sha256Hex(text) {
  const subtle = globalThis.crypto?.subtle;
  if (!subtle) throw new Error('CRYPTO_SUBTLE_UNAVAILABLE');
  const digest = await subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(digest)].map((value) => value.toString(16).padStart(2, '0')).join('');
}

export async function deriveResearchIdentity(puzzle) {
  return sha256Hex(researchSerialization(puzzle));
}

function validateFrozenBase(campaign) {
  if (campaign.campaignId !== FROZEN_CAMPAIGN_ID) throw new Error('CAMPAIGN_FROZEN_ID');
  if (campaign.launchTotal !== FROZEN_LAUNCH_TOTAL) throw new Error('CAMPAIGN_FROZEN_TOTAL');
  if (campaign.materializedFromPosition !== 1) throw new Error('CAMPAIGN_PREFIX_START');
  if (campaign.materializedThroughPosition !== campaign.puzzles.length) throw new Error('CAMPAIGN_PREFIX_END');
  const source = campaign.source;
  if (!source || source.catalogFingerprint !== FROZEN_CATALOG_FINGERPRINT) throw new Error('CAMPAIGN_CATALOG_FINGERPRINT');
  if (source.canonicalV4CatalogFingerprint !== CANONICAL_V4_CATALOG_FINGERPRINT) throw new Error('CAMPAIGN_CANONICAL_V4_FINGERPRINT');
  if (source.orderFingerprint !== FROZEN_ORDER_FINGERPRINT) throw new Error('CAMPAIGN_ORDER_FINGERPRINT');
  if (typeof source.orderPrefixFingerprint !== 'string' || !/^[0-9a-f]{64}$/.test(source.orderPrefixFingerprint)) throw new Error('CAMPAIGN_PREFIX_FINGERPRINT');
}

function validateFrozenComplete(campaign) {
  validateFrozenBase(campaign);
  if (campaign.puzzles.length !== FROZEN_LAUNCH_TOTAL) throw new Error('CAMPAIGN_COMPLETE_COUNT');
  if (campaign.materializedThroughPosition !== FROZEN_LAUNCH_TOTAL) throw new Error('CAMPAIGN_COMPLETE_END');
  if (campaign.source.orderPrefixFingerprint !== FROZEN_ORDER_FINGERPRINT) throw new Error('CAMPAIGN_COMPLETE_ORDER_FINGERPRINT');
}

export function validateCampaign(campaign) {
  if (!campaign || campaign.schema !== CAMPAIGN_SCHEMA) throw new Error('CAMPAIGN_SCHEMA');
  if (campaign.version !== CAMPAIGN_SCHEMA_VERSION) throw new Error('CAMPAIGN_VERSION');
  if (typeof campaign.campaignId !== 'string' || !campaign.campaignId) throw new Error('CAMPAIGN_ID');
  if (!Number.isInteger(campaign.launchTotal) || campaign.launchTotal < 1) throw new Error('CAMPAIGN_LAUNCH_TOTAL');
  if (!Array.isArray(campaign.puzzles) || campaign.puzzles.length < 1) throw new Error('CAMPAIGN_EMPTY');
  const ids = new Set();
  for (let i = 0; i < campaign.puzzles.length; i++) {
    const row = campaign.puzzles[i];
    if (row.position !== i + 1) throw new Error('CAMPAIGN_POSITION');
    if (typeof row.id !== 'string' || !/^[0-9a-f]{64}$/.test(row.id) || ids.has(row.id)) throw new Error('CAMPAIGN_IDENTITY');
    ids.add(row.id);
    validatePuzzle(row);
  }
  if (campaign.puzzles.length > campaign.launchTotal) throw new Error('CAMPAIGN_OVERFLOW');
  if (campaign.contentStatus === 'FROZEN_LAUNCH_COMPLETE') validateFrozenComplete(campaign);
  else throw new Error('CAMPAIGN_CONTENT_STATUS');
  return true;
}

function validateChunkDescriptor(row, expectedFrom) {
  if (!row || row.fromPosition !== expectedFrom) throw new Error('CAMPAIGN_CHUNK_DESCRIPTOR_FROM');
  if (!Number.isInteger(row.throughPosition) || row.throughPosition < row.fromPosition) throw new Error('CAMPAIGN_CHUNK_DESCRIPTOR_THROUGH');
  if (typeof row.path !== 'string' || !row.path || row.path.includes('..')) throw new Error('CAMPAIGN_CHUNK_DESCRIPTOR_PATH');
  if (typeof row.sha256 !== 'string' || !/^[0-9a-f]{64}$/.test(row.sha256)) throw new Error('CAMPAIGN_CHUNK_DESCRIPTOR_SHA');
}

export async function assembleChunkedCampaign(manifest, chunks) {
  if (!manifest || manifest.schema !== CAMPAIGN_CHUNKED_SCHEMA) throw new Error('CAMPAIGN_MANIFEST_SCHEMA');
  if (manifest.version !== CAMPAIGN_SCHEMA_VERSION) throw new Error('CAMPAIGN_MANIFEST_VERSION');
  if (manifest.identityDerivation !== IDENTITY_DERIVATION) throw new Error('CAMPAIGN_IDENTITY_DERIVATION');
  if (!Array.isArray(manifest.chunks) || manifest.chunks.length < 1) throw new Error('CAMPAIGN_MANIFEST_EMPTY');
  if (!Array.isArray(chunks) || chunks.length !== manifest.chunks.length) throw new Error('CAMPAIGN_CHUNK_COUNT');
  const puzzles = [];
  let expectedFrom = 1;
  for (let i = 0; i < manifest.chunks.length; i++) {
    const descriptor = manifest.chunks[i];
    validateChunkDescriptor(descriptor, expectedFrom);
    const chunk = chunks[i];
    if (!chunk || chunk.schema !== CAMPAIGN_CHUNK_SCHEMA || chunk.version !== CAMPAIGN_SCHEMA_VERSION) throw new Error('CAMPAIGN_CHUNK_SCHEMA');
    if (chunk.fromPosition !== descriptor.fromPosition || chunk.throughPosition !== descriptor.throughPosition) throw new Error('CAMPAIGN_CHUNK_RANGE');
    if (!Array.isArray(chunk.rows) || chunk.rows.length !== descriptor.throughPosition - descriptor.fromPosition + 1) throw new Error('CAMPAIGN_CHUNK_ROWS');
    if (JSON.stringify(chunk.rowEncoding) !== JSON.stringify(['n','length','initial','targets'])) throw new Error('CAMPAIGN_CHUNK_ENCODING');
    const pending = chunk.rows.map(async (values, rowIndex) => {
      if (!Array.isArray(values) || values.length !== 4) throw new Error('CAMPAIGN_CHUNK_ROW');
      const [n, length, initial, targets] = values;
      const puzzle = { position: descriptor.fromPosition + rowIndex, n, length, initial, targets };
      validatePuzzle(puzzle);
      return { ...puzzle, id: await deriveResearchIdentity(puzzle) };
    });
    puzzles.push(...await Promise.all(pending));
    expectedFrom = descriptor.throughPosition + 1;
  }
  if (expectedFrom !== manifest.materializedThroughPosition + 1) throw new Error('CAMPAIGN_MANIFEST_RANGE');
  const { chunks: _descriptors, identityDerivation: _identityDerivation, ...metadata } = manifest;
  const campaign = { ...metadata, schema: CAMPAIGN_SCHEMA, puzzles };
  validateCampaign(campaign);
  return campaign;
}

function relativeChunkUrl(manifestUrl, chunkPath) {
  const value = String(manifestUrl);
  const slash = value.lastIndexOf('/');
  return `${slash >= 0 ? value.slice(0, slash + 1) : ''}${chunkPath}`;
}

export async function loadCampaign(url, fetchImpl = globalThis.fetch) {
  if (typeof fetchImpl !== 'function') throw new Error('FETCH_UNAVAILABLE');
  const response = await fetchImpl(url, { cache: 'no-store' });
  if (!response.ok) throw new Error(`CAMPAIGN_FETCH_${response.status}`);
  const root = await response.json();
  if (root.schema !== CAMPAIGN_CHUNKED_SCHEMA) throw new Error('CAMPAIGN_ROOT_SCHEMA');
  const chunks = [];
  for (const descriptor of root.chunks || []) {
    const chunkResponse = await fetchImpl(relativeChunkUrl(url, descriptor.path), { cache: 'no-store' });
    if (!chunkResponse.ok) throw new Error(`CAMPAIGN_CHUNK_FETCH_${chunkResponse.status}`);
    chunks.push(await chunkResponse.json());
  }
  return assembleChunkedCampaign(root, chunks);
}
