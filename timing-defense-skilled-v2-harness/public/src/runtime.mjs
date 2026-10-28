import { applyMove, canonicalPath, isSolved, legalDestinations } from './mechanic.mjs';

export function createPuzzleRuntime(puzzle) {
  return {
    path: canonicalPath(puzzle.initial),
    selectedEndpoint: null,
    solved: false,
  };
}

export function legalCells(puzzle, runtime) {
  if (runtime.solved || runtime.selectedEndpoint === null) return [];
  return legalDestinations(puzzle.n, runtime.path, runtime.selectedEndpoint);
}

export function activateCell(puzzle, runtime, cell) {
  if (runtime.solved) return runtime;

  const index = runtime.path.indexOf(cell);
  const isEndpoint = index === 0 || index === runtime.path.length - 1;

  if (isEndpoint) {
    if (runtime.selectedEndpoint === index) {
      return { ...runtime, selectedEndpoint: null };
    }
    const legal = legalDestinations(puzzle.n, runtime.path, index);
    if (legal.length === 0) {
      return { ...runtime, selectedEndpoint: null };
    }
    return { ...runtime, selectedEndpoint: index };
  }

  if (runtime.selectedEndpoint === null) return runtime;
  const legal = legalDestinations(puzzle.n, runtime.path, runtime.selectedEndpoint);
  if (!legal.includes(cell)) return runtime;

  const path = applyMove(puzzle.n, runtime.path, runtime.selectedEndpoint, cell);
  return {
    path,
    selectedEndpoint: null,
    solved: isSolved(path, puzzle.targets),
  };
}
