import './clear-result-ui.mjs';
import { gradePerformance } from './performance.mjs';
import { markCleared, performanceAt, recordPerformance } from './progress.mjs';

export const CLEAR_RESULT_EVENT = 'linkline:clear-result-v1';
let lastClearSnapshot = null;

function failedResult(reason, moves, shortestDistance = null) {
  return Object.freeze({ ok: false, reason, moves, shortestDistance });
}

function publishClearSnapshot(snapshot) {
  const target = globalThis.document;
  const EventCtor = globalThis.CustomEvent;
  if (!target?.dispatchEvent || typeof EventCtor !== 'function') return;
  target.dispatchEvent(new EventCtor(CLEAR_RESULT_EVENT, { detail: snapshot }));
}

function finish(nextProgress, position, moves, shortestDistance, performanceResult) {
  const bestMoves = performanceAt(nextProgress, position)?.bestMoves ?? null;
  lastClearSnapshot = Object.freeze({
    version: 1,
    position,
    moves,
    shortestDistance,
    bestMoves,
    grade: performanceResult?.ok ? performanceResult.grade : null,
  });
  publishClearSnapshot(lastClearSnapshot);
  return { progress: nextProgress, performanceResult };
}

export function latestClearSnapshot() {
  return lastClearSnapshot;
}

export function applyClearedAttempt(progress, position, availableCount, moves, baseline = null) {
  let nextProgress = position > progress.highestCleared
    ? markCleared(progress, position, availableCount)
    : progress;

  if (!baseline) return finish(nextProgress, position, moves, null, null);

  const shortestDistance = baseline.distances?.[position];
  if (!Number.isInteger(shortestDistance) || shortestDistance < 1) {
    return finish(
      nextProgress,
      position,
      moves,
      null,
      failedResult('PERFORMANCE_BASELINE_POSITION', moves),
    );
  }
  if (!Number.isInteger(moves) || moves < 1) {
    return finish(
      nextProgress,
      position,
      moves,
      shortestDistance,
      failedResult('PERFORMANCE_MOVES', moves, shortestDistance),
    );
  }

  const performanceResult = gradePerformance(moves, shortestDistance);
  if (performanceResult.ok) nextProgress = recordPerformance(nextProgress, position, performanceResult);
  return finish(nextProgress, position, moves, shortestDistance, performanceResult);
}
