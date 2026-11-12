export function neighbors(n, cell) {
  const r = Math.floor(cell / n), c = cell % n;
  const out = [];
  if (r > 0) out.push(cell - n);
  if (r + 1 < n) out.push(cell + n);
  if (c > 0) out.push(cell - 1);
  if (c + 1 < n) out.push(cell + 1);
  return out.sort((a,b)=>a-b);
}

export function validatePuzzle(p) {
  if (!p || !Number.isInteger(p.n) || p.n < 2) throw new Error('PUZZLE_N');
  if (!Array.isArray(p.initial) || p.initial.length !== p.length) throw new Error('PUZZLE_LENGTH');
  if (new Set(p.initial).size !== p.initial.length) throw new Error('PUZZLE_OVERLAP');
  if (!Array.isArray(p.targets) || p.targets.length !== 2 || p.targets[0] === p.targets[1]) throw new Error('PUZZLE_TARGETS');
  for (const cell of [...p.initial, ...p.targets]) if (!Number.isInteger(cell) || cell < 0 || cell >= p.n*p.n) throw new Error('PUZZLE_RANGE');
  for (let i=1;i<p.initial.length;i++) if (!neighbors(p.n,p.initial[i-1]).includes(p.initial[i])) throw new Error('PUZZLE_PATH');
  return true;
}

export function canonicalPath(path) {
  const forward=[...path], reverse=[...path].reverse();
  for(let i=0;i<forward.length;i++){
    if(forward[i] < reverse[i]) return forward;
    if(forward[i] > reverse[i]) return reverse;
  }
  return forward;
}

export function endpointIndices(path) { return [0, path.length - 1]; }
export function isEndpoint(path, index) { return index === 0 || index === path.length - 1; }

export function legalDestinations(n, path, endpointIndex) {
  if (!isEndpoint(path, endpointIndex)) return [];
  const occupied = new Set(path);
  return neighbors(n, path[endpointIndex]).filter(c => !occupied.has(c));
}

export function applyMove(n, path, endpointIndex, destination) {
  if (!isEndpoint(path, endpointIndex)) throw new Error('INTERIOR_SELECTED');
  if (!legalDestinations(n,path,endpointIndex).includes(destination)) throw new Error('ILLEGAL_DESTINATION');
  if (endpointIndex === 0) return canonicalPath([destination, ...path.slice(0,-1)]);
  return canonicalPath([...path.slice(1), destination]);
}

export function isSolved(path, targets) {
  const a = [path[0], path[path.length-1]].sort((x,y)=>x-y);
  const b = [...targets].sort((a,b)=>a-b);
  return a[0] === b[0] && a[1] === b[1];
}

export function stateSerialization(n, path) {
  const canonical=canonicalPath(path);
  return `[\"LL_MECH\",1,${n},${canonical.length},[${canonical.join(',')}]]`;
}

export function puzzleSerialization(puzzle) {
  validatePuzzle(puzzle);
  const canonical=canonicalPath(puzzle.initial);
  const targets=[...puzzle.targets].sort((a,b)=>a-b);
  return `[\"LL_INSTANCE\",1,${puzzle.n},${puzzle.length},[${targets.join(',')}],[${canonical.join(',')}]]`;
}

export function enumerateActions(n, path) {
  const out=[];
  for (const endpointIndex of endpointIndices(path)) {
    for (const destination of legalDestinations(n,path,endpointIndex)) out.push({endpointIndex,destination});
  }
  return out;
}
