import { PERFORMANCE_GRADES, gradePerformance } from './performance.mjs';

export const PROGRESS_SCHEMA = 'LINKLINE_PRODUCT_PROGRESS';
export const PROGRESS_VERSION = 3;
export const PROGRESS_STORAGE_KEY = 'linkline.product.progress.v3';
export const LEGACY_PROGRESS_V2_STORAGE_KEY = 'linkline.product.progress.v2';

const GRADE_RANK = Object.freeze({ 'B+': 1, 'A+': 2, 'S+': 3 });

export function initialProgress(campaignId) {
  return {
    schema: PROGRESS_SCHEMA,
    version: PROGRESS_VERSION,
    campaignId,
    currentPosition: 1,
    highestCleared: 0,
    performance: {},
  };
}

function sanitizePositionFields(raw, availableCount) {
  const highestCleared = Math.max(0, Math.min(Number.isInteger(raw.highestCleared) ? raw.highestCleared : 0, availableCount));
  let currentPosition = Math.max(1, Math.min(Number.isInteger(raw.currentPosition) ? raw.currentPosition : highestCleared + 1, availableCount));
  if (highestCleared < availableCount && currentPosition <= highestCleared) currentPosition = highestCleared + 1;
  return { currentPosition, highestCleared };
}

function sanitizePerformance(rawPerformance, availableCount, baseline) {
  const performance = {};
  if (!rawPerformance || typeof rawPerformance !== 'object' || Array.isArray(rawPerformance)) return performance;
  for (const [key, record] of Object.entries(rawPerformance)) {
    if (!/^[1-9]\d*$/.test(key)) continue;
    const position = Number(key);
    if (position < 1 || position > availableCount) continue;
    if (!record || typeof record !== 'object' || Array.isArray(record)) continue;
    if (!Number.isInteger(record.bestMoves) || record.bestMoves < 1 || !PERFORMANCE_GRADES.includes(record.grade)) continue;
    if (baseline) {
      const shortestDistance = baseline.distances?.[position];
      if (!Number.isInteger(shortestDistance)) continue;
      const result = gradePerformance(record.bestMoves, shortestDistance);
      if (!result.ok || result.grade !== record.grade) continue;
    }
    performance[key] = { bestMoves: record.bestMoves, grade: record.grade };
  }
  return performance;
}

function sanitizeV3(raw, campaignId, availableCount, baseline) {
  if (!raw || raw.schema !== PROGRESS_SCHEMA || raw.version !== PROGRESS_VERSION || raw.campaignId !== campaignId) return null;
  const fields = sanitizePositionFields(raw, availableCount);
  return {
    schema: PROGRESS_SCHEMA,
    version: PROGRESS_VERSION,
    campaignId,
    ...fields,
    performance: sanitizePerformance(raw.performance, availableCount, baseline),
  };
}

function migrateV2(raw, campaignId, availableCount) {
  if (!raw || raw.schema !== PROGRESS_SCHEMA || raw.version !== 2 || raw.campaignId !== campaignId) return null;
  const fields = sanitizePositionFields(raw, availableCount);
  return {
    schema: PROGRESS_SCHEMA,
    version: PROGRESS_VERSION,
    campaignId,
    ...fields,
    performance: {},
  };
}

function readJson(storage, key) {
  try {
    const text = storage.getItem(key);
    return text ? JSON.parse(text) : null;
  } catch {
    return null;
  }
}

export function loadProgress(storage, campaignId, availableCount, baseline = null) {
  if (!storage) return initialProgress(campaignId);
  const current = sanitizeV3(readJson(storage, PROGRESS_STORAGE_KEY), campaignId, availableCount, baseline);
  if (current) return current;

  const migrated = migrateV2(readJson(storage, LEGACY_PROGRESS_V2_STORAGE_KEY), campaignId, availableCount);
  if (!migrated) return initialProgress(campaignId);
  try {
    saveProgress(storage, migrated);
  } catch {
    // Migration still succeeds in-memory if persistence is unavailable.
  }
  return migrated;
}

export function saveProgress(storage, progress) {
  if (!storage) return;
  storage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(progress));
  storage.removeItem(LEGACY_PROGRESS_V2_STORAGE_KEY);
}

export function clearProgress(storage) {
  if (!storage) return;
  storage.removeItem(PROGRESS_STORAGE_KEY);
  storage.removeItem(LEGACY_PROGRESS_V2_STORAGE_KEY);
}

export function markCleared(progress, position, availableCount) {
  const highestCleared = Math.max(progress.highestCleared, position);
  const currentPosition = Math.min(position + 1, availableCount);
  return { ...progress, highestCleared, currentPosition };
}

export function recordPerformance(progress, position, result) {
  if (!result?.ok || !PERFORMANCE_GRADES.includes(result.grade) || !Number.isInteger(result.moves) || result.moves < 1) return progress;
  const key = String(position);
  const existing = progress.performance?.[key];
  if (existing) {
    const existingRank = GRADE_RANK[existing.grade] || 0;
    const incomingRank = GRADE_RANK[result.grade] || 0;
    if (incomingRank < existingRank) return progress;
    if (incomingRank === existingRank && result.moves >= existing.bestMoves) return progress;
  }
  return {
    ...progress,
    performance: {
      ...(progress.performance || {}),
      [key]: { bestMoves: result.moves, grade: result.grade },
    },
  };
}

export function performanceAt(progress, position) {
  return progress.performance?.[String(position)] || null;
}

export function isAvailablePrefixComplete(progress, availableCount) {
  return availableCount > 0 && progress.highestCleared >= availableCount;
}
