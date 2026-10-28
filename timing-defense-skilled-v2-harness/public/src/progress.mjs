export const PROGRESS_SCHEMA = 'LINKLINE_PRODUCT_PROGRESS';
export const PROGRESS_VERSION = 1;
export const PROGRESS_STORAGE_KEY = 'linkline.product.progress.v1';

export function initialProgress(campaignId) {
  return {
    schema: PROGRESS_SCHEMA,
    version: PROGRESS_VERSION,
    campaignId,
    currentPosition: 1,
    highestCleared: 0,
  };
}

function sanitize(raw, campaignId, availableCount) {
  if (!raw || raw.schema !== PROGRESS_SCHEMA || raw.version !== PROGRESS_VERSION || raw.campaignId !== campaignId) {
    return initialProgress(campaignId);
  }
  const highestCleared = Math.max(0, Math.min(Number.isInteger(raw.highestCleared) ? raw.highestCleared : 0, availableCount));
  let currentPosition = Math.max(1, Math.min(Number.isInteger(raw.currentPosition) ? raw.currentPosition : highestCleared + 1, availableCount));
  if (highestCleared < availableCount && currentPosition <= highestCleared) currentPosition = highestCleared + 1;
  return { schema: PROGRESS_SCHEMA, version: PROGRESS_VERSION, campaignId, currentPosition, highestCleared };
}

export function loadProgress(storage, campaignId, availableCount) {
  if (!storage) return initialProgress(campaignId);
  try {
    const raw = JSON.parse(storage.getItem(PROGRESS_STORAGE_KEY));
    return sanitize(raw, campaignId, availableCount);
  } catch {
    return initialProgress(campaignId);
  }
}

export function saveProgress(storage, progress) {
  if (!storage) return;
  storage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(progress));
}

export function clearProgress(storage) {
  if (storage) storage.removeItem(PROGRESS_STORAGE_KEY);
}

export function markCleared(progress, position, availableCount) {
  const highestCleared = Math.max(progress.highestCleared, position);
  const currentPosition = Math.min(position + 1, availableCount);
  return { ...progress, highestCleared, currentPosition };
}

export function isAvailablePrefixComplete(progress, availableCount) {
  return availableCount > 0 && progress.highestCleared >= availableCount;
}
