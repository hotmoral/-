const SVG_NS = 'http://www.w3.org/2000/svg';
const screen = document.querySelector('#screen');
const stageLabel = document.querySelector('#stage-label');
const reducedMotion = globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;

const ROUTE_RADIUS_RATIO = 0.22;
const ROUTE_LINE_STEP = 0.72;
const ROUTE_CURVE_STEPS = 8;
const RENDER_SAMPLE_COUNT = 128;
const SETTLE_MS = 84;
const END_GRACE_MS = 520;
const SAMPLE_RATIO = 0.12;
const MIN_SAMPLE_PX = 3;
const MAX_SAMPLE_PX = 8;

let slideState = null;

function svgNode(tag, attrs = {}, className = '') {
  const node = document.createElementNS(SVG_NS, tag);
  for (const [name, value] of Object.entries(attrs)) node.setAttribute(name, String(value));
  if (className) node.setAttribute('class', className);
  return node;
}

function cellNumber(cell) {
  const value = Number(cell?.dataset?.cell);
  return Number.isInteger(value) ? value : null;
}

function cellCenterFromNumber(number, n) {
  if (!Number.isInteger(number)) return null;
  const row = Math.floor(number / n);
  const col = number % n;
  const step = 100 / n;
  return { x: (col + 0.5) * step, y: (row + 0.5) * step };
}

function cellCenter(cell, n) {
  return cellCenterFromNumber(cellNumber(cell), n);
}

function distanceSquared(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  return dx * dx + dy * dy;
}

function distance(a, b) {
  return Math.sqrt(distanceSquared(a, b));
}

function lerpPoint(a, b, t) {
  return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t };
}

function pointsToPath(points) {
  if (!points?.length) return '';
  return points.map((point, index) =>
    `${index ? 'L' : 'M'}${point.x.toFixed(3)} ${point.y.toFixed(3)}`
  ).join(' ');
}

function neighbors(n, cell) {
  const row = Math.floor(cell / n);
  const col = cell % n;
  const out = [];
  if (row > 0) out.push(cell - n);
  if (row + 1 < n) out.push(cell + n);
  if (col > 0) out.push(cell - 1);
  if (col + 1 < n) out.push(cell + 1);
  return out;
}

function pathMetrics(points) {
  const cumulative = [0];
  for (let index = 1; index < points.length; index++) {
    cumulative.push(cumulative.at(-1) + distance(points[index - 1], points[index]));
  }
  return { cumulative, total: cumulative.at(-1) || 0 };
}

function pointAtDistance(points, metrics, target) {
  if (!points.length) return null;
  if (target <= 0) return { ...points[0] };
  if (target >= metrics.total) return { ...points.at(-1) };

  let low = 1;
  let high = metrics.cumulative.length - 1;
  while (low < high) {
    const mid = (low + high) >> 1;
    if (metrics.cumulative[mid] < target) low = mid + 1;
    else high = mid;
  }

  const index = low;
  const before = metrics.cumulative[index - 1];
  const after = metrics.cumulative[index];
  const span = Math.max(1e-9, after - before);
  return lerpPoint(points[index - 1], points[index], (target - before) / span);
}

function sampleRange(points, fromDistance, length, count = RENDER_SAMPLE_COUNT) {
  const metrics = pathMetrics(points);
  const from = Math.max(0, Math.min(metrics.total, fromDistance));
  const usable = Math.max(0, Math.min(length, metrics.total - from));
  const out = [];
  for (let index = 0; index < count; index++) {
    const ratio = count === 1 ? 0 : index / (count - 1);
    out.push(pointAtDistance(points, metrics, from + usable * ratio));
  }
  return { points: out, usableLength: usable, metrics };
}

function appendLineSamples(out, from, to) {
  const length = distance(from, to);
  const steps = Math.max(1, Math.ceil(length / ROUTE_LINE_STEP));
  for (let step = 1; step <= steps; step++) out.push(lerpPoint(from, to, step / steps));
}

function appendQuadraticSamples(out, from, control, to) {
  for (let step = 1; step <= ROUTE_CURVE_STEPS; step++) {
    const t = step / ROUTE_CURVE_STEPS;
    const mt = 1 - t;
    out.push({
      x: mt * mt * from.x + 2 * mt * t * control.x + t * t * to.x,
      y: mt * mt * from.y + 2 * mt * t * control.y + t * t * to.y,
    });
  }
}

function roundedPolylineSamples(controls, radius) {
  if (!controls?.length) return [];
  if (controls.length === 1) return [{ ...controls[0] }];

  const out = [{ ...controls[0] }];
  let cursor = controls[0];

  for (let index = 1; index < controls.length - 1; index++) {
    const previous = controls[index - 1];
    const current = controls[index];
    const next = controls[index + 1];
    const incoming = { x: current.x - previous.x, y: current.y - previous.y };
    const outgoing = { x: next.x - current.x, y: next.y - current.y };
    const incomingLength = Math.hypot(incoming.x, incoming.y);
    const outgoingLength = Math.hypot(outgoing.x, outgoing.y);
    const cross = incoming.x * outgoing.y - incoming.y * outgoing.x;

    if (!incomingLength || !outgoingLength || Math.abs(cross) < 1e-8) {
      appendLineSamples(out, cursor, current);
      cursor = current;
      continue;
    }

    const cornerRadius = Math.min(radius, incomingLength / 2, outgoingLength / 2);
    const entry = {
      x: current.x - incoming.x / incomingLength * cornerRadius,
      y: current.y - incoming.y / incomingLength * cornerRadius,
    };
    const exit = {
      x: current.x + outgoing.x / outgoingLength * cornerRadius,
      y: current.y + outgoing.y / outgoingLength * cornerRadius,
    };

    appendLineSamples(out, cursor, entry);
    appendQuadraticSamples(out, entry, current, exit);
    cursor = exit;
  }

  appendLineSamples(out, cursor, controls.at(-1));
  return out;
}

function projectPointToSamples(point, samples, maxDistance = Infinity, previousDistance = null, span = Infinity) {
  if (!point || samples.length < 2) return null;
  const metrics = pathMetrics(samples);
  let best = null;

  for (let index = 1; index < samples.length; index++) {
    const a = samples[index - 1];
    const b = samples[index];
    const dx = b.x - a.x;
    const dy = b.y - a.y;
    const len2 = dx * dx + dy * dy;
    if (len2 <= 1e-12) continue;

    const t = Math.max(0, Math.min(1, ((point.x - a.x) * dx + (point.y - a.y) * dy) / len2));
    const projected = { x: a.x + dx * t, y: a.y + dy * t };
    const along = metrics.cumulative[index - 1] + Math.sqrt(len2) * t;
    if (along > maxDistance + 1e-6) continue;
    if (previousDistance !== null && Math.abs(along - previousDistance) > span) continue;

    const d2 = distanceSquared(point, projected);
    if (!best || d2 < best.distanceSquared) best = { point: projected, distance: along, distanceSquared: d2 };
  }

  if (!best && previousDistance !== null) {
    return projectPointToSamples(point, samples, maxDistance, null, Infinity);
  }
  return best;
}

function boardInfo(board = slideState?.board) {
  const activeBoard = board?.isConnected ? board : screen?.querySelector('.board-wrap');
  const grid = activeBoard?.querySelector(':scope > .board');
  const cells = grid?.querySelectorAll('.cell');
  const n = cells?.length ? Math.round(Math.sqrt(cells.length)) : 0;
  if (!activeBoard || !grid || !n || n * n !== cells.length) return null;
  const rect = grid.getBoundingClientRect();
  return {
    board: activeBoard,
    grid,
    n,
    rect,
    cellW: rect.width / n,
    cellH: rect.height / n,
    cellSize: Math.min(rect.width / n, rect.height / n),
  };
}

function isSolvedView() {
  return Boolean(screen?.querySelector('.success-panel') || screen?.classList.contains('polish-success'));
}

function clientToBoard(clientX, clientY, info = boardInfo()) {
  if (!info?.rect?.width || !info.rect.height) return null;
  return {
    x: ((clientX - info.rect.left) / info.rect.width) * 100,
    y: ((clientY - info.rect.top) / info.rect.height) * 100,
  };
}

function gridCellAt(clientX, clientY, info = boardInfo()) {
  if (!info) return null;
  const { rect, n, cellW, cellH } = info;
  if (clientX < rect.left || clientX >= rect.right || clientY < rect.top || clientY >= rect.bottom) return null;
  const col = Math.max(0, Math.min(n - 1, Math.floor((clientX - rect.left) / cellW)));
  const row = Math.max(0, Math.min(n - 1, Math.floor((clientY - rect.top) / cellH)));
  return row * n + col;
}

function sourcePathSamples(board, count = 192) {
  const sourcePath = board.querySelector(':scope > .links .chain-path');
  if (!sourcePath?.getTotalLength || !sourcePath?.getPointAtLength) return null;
  let total;
  try { total = sourcePath.getTotalLength(); } catch { return null; }
  if (!Number.isFinite(total) || total <= 0) return null;

  const points = [];
  for (let index = 0; index < count; index++) {
    const ratio = count === 1 ? 0 : index / (count - 1);
    const point = sourcePath.getPointAtLength(total * ratio);
    points.push({ x: point.x, y: point.y });
  }
  return { points, total };
}

function orderChainCellsBySource(board, n, sourcePoints, draggedCell) {
  const entries = [];
  for (const cell of board.querySelectorAll('.cell.chain')) {
    const number = cellNumber(cell);
    const point = cellCenter(cell, n);
    if (!Number.isInteger(number) || !point) continue;
    let bestIndex = 0;
    let bestDistance = Infinity;
    for (let index = 0; index < sourcePoints.length; index++) {
      const d2 = distanceSquared(point, sourcePoints[index]);
      if (d2 < bestDistance) {
        bestDistance = d2;
        bestIndex = index;
      }
    }
    entries.push({ number, bestIndex });
  }

  entries.sort((a, b) => a.bestIndex - b.bestIndex);
  let ordered = entries.map((entry) => entry.number);
  if (ordered.at(-1) === draggedCell) ordered = ordered.reverse();
  if (ordered[0] !== draggedCell) return null;
  return ordered;
}

function visualMetrics(n) {
  const step = 100 / n;
  const endpointRadius = Math.min(5.0, Math.max(3.3, step * 0.19));
  return {
    endpointRadius,
    targetRadius: endpointRadius * 1.42,
    targetCoreRadius: Math.max(0.48, endpointRadius * 0.16),
    jointRadius: Math.min(1.75, Math.max(1.1, step * 0.07)),
  };
}

function appendTarget(svg, point, metrics, docked) {
  const group = svgNode('g', {}, `target-mark${docked ? ' is-docked' : ''}`);
  group.append(
    svgNode('circle', { cx: point.x, cy: point.y, r: metrics.targetRadius }, 'target-ring'),
    svgNode('circle', { cx: point.x, cy: point.y, r: metrics.targetCoreRadius }, 'target-core'),
  );
  svg.append(group);
}

function appendEndpoint(svg, point, metrics, selected, docked, className = '') {
  const node = svgNode('circle', {
    cx: point.x,
    cy: point.y,
    r: metrics.endpointRadius,
  }, `endpoint-dot${selected ? ' is-selected' : ''}${docked ? ' is-docked' : ''}${className ? ` ${className}` : ''}`);
  svg.append(node);
  return node;
}

function sourceNodePoints(board, chainCellCount) {
  const sourcePath = board.querySelector(':scope > .links .chain-path');
  if (!sourcePath?.getTotalLength || !sourcePath?.getPointAtLength || chainCellCount < 2) return null;
  let total;
  try { total = sourcePath.getTotalLength(); } catch { return null; }
  if (!Number.isFinite(total) || total <= 0) return null;

  const points = [];
  for (let index = 0; index < chainCellCount; index++) {
    const point = sourcePath.getPointAtLength(total * index / (chainCellCount - 1));
    points.push({ x: point.x, y: point.y });
  }
  return points;
}

function createStaticChain(board, n) {
  const sourcePath = board.querySelector(':scope > .links .chain-path');
  const d = sourcePath?.getAttribute('d');
  const chainCellCount = board.querySelectorAll('.cell.chain').length;
  const nodePoints = sourceNodePoints(board, chainCellCount);
  if (!d || !nodePoints?.length) return null;

  const metrics = visualMetrics(n);
  const svg = svgNode('svg', { viewBox: '0 0 100 100', 'aria-hidden': 'true' }, 'visual-chain-overlay');
  svg.append(
    svgNode('path', { d }, 'visual-chain-shadow'),
    svgNode('path', { d }, 'visual-chain-body'),
  );

  for (let index = 1; index < nodePoints.length - 1; index++) {
    const point = nodePoints[index];
    svg.append(svgNode('circle', { cx: point.x, cy: point.y, r: metrics.jointRadius }, 'visual-chain-joint'));
  }
  return { svg, nodePoints };
}

function createStaticMarks(board, n) {
  const svg = svgNode('svg', { viewBox: '0 0 100 100', 'aria-hidden': 'true' }, 'visual-board-assets');
  const metrics = visualMetrics(n);

  for (const cell of board.querySelectorAll('.cell.target')) {
    const point = cellCenter(cell, n);
    if (point) appendTarget(svg, point, metrics, cell.classList.contains('endpoint'));
  }

  for (const cell of board.querySelectorAll('.cell.endpoint')) {
    const point = cellCenter(cell, n);
    if (!point) continue;
    appendEndpoint(svg, point, metrics, cell.classList.contains('selected'), cell.classList.contains('target'));
  }
  return svg;
}

function createSlideOverlay(n, chainCellCount) {
  const metrics = visualMetrics(n);
  const svg = svgNode('svg', { viewBox: '0 0 100 100', 'aria-hidden': 'true' }, 'visual-slide-overlay');
  const shadow = svgNode('path', { d: '' }, 'slide-chain-shadow');
  const body = svgNode('path', { d: '' }, 'slide-chain-body');
  svg.append(shadow, body);

  const nodes = [];
  for (let index = 0; index < chainCellCount; index++) {
    const endpoint = index === 0 || index === chainCellCount - 1;
    const node = endpoint
      ? appendEndpoint(svg, { x: 0, y: 0 }, metrics, index === 0, false, 'slide-node')
      : svgNode('circle', { cx: 0, cy: 0, r: metrics.jointRadius }, 'slide-chain-joint slide-node');
    if (!endpoint) svg.append(node);
    nodes.push(node);
  }
  return { svg, paths: [shadow, body], nodes };
}

function updateOverlayGeometry(overlay, points) {
  if (!overlay || !points?.length) return;
  const d = pointsToPath(points);
  for (const path of overlay.paths) path.setAttribute('d', d);

  const denominator = Math.max(1, overlay.nodes.length - 1);
  for (let index = 0; index < overlay.nodes.length; index++) {
    const sampleIndex = Math.round((index / denominator) * (points.length - 1));
    const point = points[sampleIndex];
    overlay.nodes[index].setAttribute('cx', point.x);
    overlay.nodes[index].setAttribute('cy', point.y);
  }
}

function currentCandidateCell(pointerPoint) {
  if (!slideState || !pointerPoint) return null;
  const head = slideState.chainCells[0];
  const headPoint = cellCenterFromNumber(head, slideState.n);
  const occupied = new Set(slideState.chainCells);
  let best = null;

  for (const candidate of neighbors(slideState.n, head)) {
    if (occupied.has(candidate)) continue;
    const target = cellCenterFromNumber(candidate, slideState.n);
    const vx = target.x - headPoint.x;
    const vy = target.y - headPoint.y;
    const length = Math.hypot(vx, vy);
    if (!length) continue;
    const projection = ((pointerPoint.x - headPoint.x) * vx + (pointerPoint.y - headPoint.y) * vy) / length;
    if (projection <= 0) continue;
    if (!best || projection > best.projection) best = { cell: candidate, projection };
  }
  return best?.cell ?? null;
}

function routeControls(candidateCell = null) {
  if (!slideState) return [];
  const controls = slideState.routeCells.map((cell) => cellCenterFromNumber(cell, slideState.n));
  if (Number.isInteger(candidateCell) && candidateCell !== slideState.routeCells.at(-1)) {
    controls.push(cellCenterFromNumber(candidateCell, slideState.n));
  }
  return controls.filter(Boolean);
}

function fullTrail(candidateCell = null) {
  if (!slideState) return null;
  const forwardControls = routeControls(candidateCell);
  const chainControls = slideState.initialChainCells
    .slice(1)
    .map((cell) => cellCenterFromNumber(cell, slideState.n));
  const controls = [...forwardControls].reverse().concat(chainControls).filter(Boolean);
  if (controls.length < 2) return null;
  const radius = (100 / slideState.n) * ROUTE_RADIUS_RATIO;
  const samples = roundedPolylineSamples(controls, radius);
  const routeEnd = cellCenterFromNumber(slideState.routeCells[0], slideState.n);
  const routeProjection = projectPointToSamples(routeEnd, samples);
  return {
    samples,
    metrics: pathMetrics(samples),
    routeLimit: routeProjection?.distance ?? 0,
    controls,
  };
}

function expectedBoardMatches(board) {
  if (!slideState || !board?.isConnected) return false;
  const actual = new Set([...board.querySelectorAll('.cell.chain')].map(cellNumber).filter(Number.isInteger));
  if (actual.size !== slideState.chainCells.length) return false;
  return slideState.chainCells.every((cell) => actual.has(cell));
}

function attachSlideOverlay(board, n) {
  if (!slideState || !board?.isConnected) return;
  if (slideState.board === board && slideState.overlay?.svg?.isConnected) return;

  slideState.board?.classList.remove('visual-slide-active');
  slideState.overlay?.svg?.remove();

  const overlay = createSlideOverlay(n, slideState.initialChainCells.length);
  slideState.board = board;
  slideState.overlay = overlay;
  board.classList.add('visual-slide-active');
  board.append(overlay.svg);
  updateOverlayGeometry(overlay, slideState.renderPoints);
}

function renderActiveSlide() {
  if (!slideState || slideState.ending) return;
  if (isSolvedView()) {
    cleanupSlideState();
    return;
  }
  const info = boardInfo();
  const pointer = clientToBoard(slideState.clientX, slideState.clientY, info);
  if (!pointer) return;

  const candidate = currentCandidateCell(pointer);
  slideState.candidateCell = candidate;
  const trail = fullTrail(candidate);
  if (!trail?.samples?.length) return;

  const step = 100 / slideState.n;
  const previous = slideState.headOffset;
  const projected = projectPointToSamples(
    pointer,
    trail.samples,
    trail.routeLimit + 1e-6,
    Number.isFinite(previous) ? previous : null,
    step * 1.35,
  );
  if (!projected) return;

  const rawProgress = Math.max(0, trail.routeLimit - projected.distance);
  slideState.maxForwardProgress = Math.max(slideState.maxForwardProgress, rawProgress);
  const forwardProgress = Math.min(trail.routeLimit, slideState.maxForwardProgress);
  slideState.headOffset = Math.max(0, trail.routeLimit - forwardProgress);
  const segment = sampleRange(trail.samples, slideState.headOffset, slideState.chainLength);
  if (!segment.points?.length) return;
  slideState.renderPoints = segment.points;
  updateOverlayGeometry(slideState.overlay, slideState.renderPoints);
}

function renderSlideFrame(now) {
  if (!slideState) return;
  slideState.raf = 0;

  if (!slideState.board?.isConnected) {
    const currentBoard = screen?.querySelector('.board-wrap.visual-assets-v5');
    if (currentBoard) attachSlideOverlay(currentBoard, slideState.n);
  }

  if (!slideState.ending) {
    renderActiveSlide();
    return;
  }

  const settle = slideState.settle;
  if (!settle) return;
  const duration = reducedMotion ? 0 : SETTLE_MS;
  const t = duration === 0 ? 1 : Math.min(1, Math.max(0, (now - settle.startedAt) / duration));
  slideState.headOffset = settle.from + (settle.to - settle.from) * t;
  const segment = sampleRange(settle.trail.samples, slideState.headOffset, slideState.chainLength);
  slideState.renderPoints = segment.points;
  updateOverlayGeometry(slideState.overlay, slideState.renderPoints);

  if (t < 1) {
    ensureFrame();
    return;
  }

  slideState.settled = true;
  if (expectedBoardMatches(slideState.board)) cleanupSlideState();
  else scheduleEndCleanup();
}

function ensureFrame() {
  if (!slideState || slideState.raf) return;
  slideState.raf = requestAnimationFrame(renderSlideFrame);
}

function commitVisualCell(cell) {
  if (!slideState || !Number.isInteger(cell)) return false;
  const head = slideState.chainCells[0];
  if (cell === head) return true;
  const occupied = new Set(slideState.chainCells);
  if (occupied.has(cell) || !neighbors(slideState.n, head).includes(cell)) return false;

  slideState.routeCells.push(cell);
  slideState.chainCells = [cell, ...slideState.chainCells.slice(0, -1)];
  return true;
}

function appendTraceCellVisual(number, segDx, segDy) {
  if (!slideState || number === null || number === slideState.traceCell) return;
  const from = slideState.traceCell;
  if (!Number.isInteger(from)) {
    slideState.traceCell = number;
    return;
  }

  let fromRow = Math.floor(from / slideState.n);
  let fromCol = from % slideState.n;
  const toRow = Math.floor(number / slideState.n);
  const toCol = number % slideState.n;

  while (fromRow !== toRow || fromCol !== toCol) {
    if (fromRow !== toRow && fromCol !== toCol) {
      const axis = slideState.headingAxis || (Math.abs(segDx) > Math.abs(segDy) ? 'H' : 'V');
      if (axis === 'H') {
        fromCol += Math.sign(toCol - fromCol);
        slideState.headingAxis = 'H';
      } else {
        fromRow += Math.sign(toRow - fromRow);
        slideState.headingAxis = 'V';
      }
    } else if (fromRow !== toRow) {
      fromRow += Math.sign(toRow - fromRow);
      slideState.headingAxis = 'V';
    } else {
      fromCol += Math.sign(toCol - fromCol);
      slideState.headingAxis = 'H';
    }

    const accepted = commitVisualCell(fromRow * slideState.n + fromCol);
    if (!accepted) break;
  }
  slideState.traceCell = number;
}

function samplePointerTo(clientX, clientY) {
  if (!slideState || slideState.ending) return;
  if (isSolvedView()) {
    cleanupSlideState();
    return;
  }
  const info = boardInfo();
  if (!info) return;

  const x0 = slideState.lastX;
  const y0 = slideState.lastY;
  const dx = clientX - x0;
  const dy = clientY - y0;
  const length = Math.hypot(dx, dy);
  const step = Math.max(MIN_SAMPLE_PX, Math.min(MAX_SAMPLE_PX, info.cellSize * SAMPLE_RATIO));
  const count = Math.max(1, Math.ceil(length / step));

  for (let index = 1; index <= count; index++) {
    const t = index / count;
    const cell = gridCellAt(x0 + dx * t, y0 + dy * t, info);
    appendTraceCellVisual(cell, dx, dy);
  }

  slideState.lastX = clientX;
  slideState.lastY = clientY;
  slideState.clientX = clientX;
  slideState.clientY = clientY;
  ensureFrame();
}

function stopFrame() {
  if (slideState?.raf) cancelAnimationFrame(slideState.raf);
  if (slideState) slideState.raf = 0;
}

function cleanupSlideState() {
  if (!slideState) return;
  stopFrame();
  if (slideState.endTimer !== null) clearTimeout(slideState.endTimer);
  slideState.board?.classList.remove('visual-slide-active');
  slideState.overlay?.svg?.remove();
  slideState = null;
}

function scheduleEndCleanup() {
  if (!slideState) return;
  if (slideState.endTimer !== null) clearTimeout(slideState.endTimer);
  slideState.endTimer = setTimeout(cleanupSlideState, reducedMotion ? 0 : END_GRACE_MS);
}

function startSlide(event) {
  const cell = event.target.closest?.('.cell.endpoint');
  const board = cell?.closest?.('.board-wrap.visual-assets-v5');
  if (!board || isSolvedView()) return;

  cleanupSlideState();

  const info = boardInfo(board);
  const draggedCell = cellNumber(cell);
  const source = sourcePathSamples(board);
  if (!info || !Number.isInteger(draggedCell) || !source) return;

  const ordered = orderChainCellsBySource(board, info.n, source.points, draggedCell);
  if (!ordered?.length) return;

  const initialControls = ordered.map((number) => cellCenterFromNumber(number, info.n));
  const radius = (100 / info.n) * ROUTE_RADIUS_RATIO;
  const initialSamples = roundedPolylineSamples(initialControls, radius);
  const initialMetrics = pathMetrics(initialSamples);
  if (!initialMetrics.total) return;

  const renderPoints = sampleRange(initialSamples, 0, initialMetrics.total).points;
  slideState = {
    pointerId: event.pointerId,
    stageKey: stageLabel?.textContent?.trim() || '',
    board,
    n: info.n,
    initialChainCells: [...ordered],
    chainCells: [...ordered],
    routeCells: [draggedCell],
    traceCell: draggedCell,
    chainLength: initialMetrics.total,
    clientX: event.clientX,
    clientY: event.clientY,
    lastX: event.clientX,
    lastY: event.clientY,
    headOffset: null,
    maxForwardProgress: 0,
    candidateCell: null,
    headingAxis: null,
    renderPoints,
    overlay: null,
    raf: 0,
    ending: false,
    settled: false,
    settle: null,
    endTimer: null,
  };

  attachSlideOverlay(board, info.n);
  ensureFrame();
}

function updateSlide(event) {
  if (!slideState || event.pointerId !== slideState.pointerId || slideState.ending) return;
  if (isSolvedView()) {
    cleanupSlideState();
    return;
  }
  const points = typeof event.getCoalescedEvents === 'function' ? event.getCoalescedEvents() : [];
  const stream = points.length ? points : [event];
  for (const point of stream) samplePointerTo(point.clientX, point.clientY);
  if (stream.at(-1) !== event) samplePointerTo(event.clientX, event.clientY);
}

function finishSlide(event) {
  if (!slideState || (event?.pointerId !== undefined && event.pointerId !== slideState.pointerId)) return;
  if (isSolvedView()) {
    cleanupSlideState();
    return;
  }
  if (Number.isFinite(event.clientX) && Number.isFinite(event.clientY)) samplePointerTo(event.clientX, event.clientY);

  renderActiveSlide();
  if (!slideState) return;
  slideState.ending = true;
  const releaseCandidate = slideState.candidateCell;
  const trail = fullTrail(releaseCandidate);
  if (!trail?.samples?.length) {
    cleanupSlideState();
    return;
  }

  const committedHead = cellCenterFromNumber(slideState.chainCells[0], slideState.n);
  const committedProjection = projectPointToSamples(committedHead, trail.samples, trail.routeLimit + 1e-6);
  const from = Number.isFinite(slideState.headOffset) ? slideState.headOffset : (committedProjection?.distance ?? 0);
  const to = committedProjection?.distance ?? from;
  slideState.settle = { trail, from, to, startedAt: performance.now() };
  ensureFrame();
}

const style = document.createElement('style');
style.dataset.linklineVisualAssets = 'v5';
style.textContent = `
.board-wrap.visual-assets-v5 > .links:not(.completion-pulse):not(.handoff-pulse):not(.arrival-pulse){opacity:0}
.board-wrap.visual-assets-v5 .cell.target::before,.board-wrap.visual-assets-v5 .cell.chain::after{opacity:0!important}
.board-wrap.visual-assets-v5 .cell.selected{box-shadow:none}
.visual-chain-overlay,.visual-board-assets,.visual-slide-overlay{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
.visual-chain-overlay{z-index:4}
.visual-board-assets{z-index:5}
.visual-slide-overlay{z-index:7}
.visual-chain-shadow,.visual-chain-body,.slide-chain-shadow,.slide-chain-body{fill:none;stroke-linecap:round;stroke-linejoin:round}
.visual-chain-shadow,.slide-chain-shadow{stroke:rgba(23,23,22,.13);stroke-width:3.95;filter:drop-shadow(0 1.2px 1.4px rgba(23,23,22,.10))}
.visual-chain-body,.slide-chain-body{stroke:#1d1d1b;stroke-width:2.85}
.visual-chain-joint,.slide-chain-joint{fill:#1d1d1b}
.endpoint-dot{fill:#1d1d1b;stroke:rgba(255,255,255,.88);stroke-width:.40}
.endpoint-dot.is-selected{stroke:#1268ff;stroke-width:.88}
.endpoint-dot.is-docked{fill:#1268ff;stroke:#fff;stroke-width:.54}
.target-ring{fill:rgba(18,104,255,.025);stroke:#1268ff;stroke-width:1.12}
.target-core{fill:rgba(18,104,255,.30)}
.target-mark.is-docked .target-ring{stroke-opacity:.42}
.target-mark.is-docked .target-core{opacity:0}
.board-wrap.visual-slide-active .visual-chain-overlay,
.board-wrap.visual-slide-active .visual-board-assets .endpoint-dot{opacity:0}
.board-wrap.visual-slide-active .target-ring{stroke-width:1.26;filter:drop-shadow(0 0 1.6px rgba(18,104,255,.16))}
@media (prefers-reduced-motion:reduce){.board-wrap.visual-slide-active .target-ring{filter:none}}
`;
document.head.append(style);

function decorateBoard(board) {
  if (!board || board.classList.contains('visual-assets-v5') || board.classList.contains('linkline-board-ghost')) return;
  const info = boardInfo(board);
  if (!info) return;

  const chain = createStaticChain(board, info.n);
  if (!chain) return;
  const marks = createStaticMarks(board, info.n);

  board.classList.add('visual-assets-v5');
  board.insertBefore(chain.svg, info.grid);
  board.insertBefore(marks, info.grid);

  if (slideState) attachSlideOverlay(board, info.n);
}

function scan() {
  if (!screen) return;

  if (!screen.classList.contains('view-game')) {
    cleanupSlideState();
    return;
  }

  if (slideState && isSolvedView()) cleanupSlideState();

  const stageKey = stageLabel?.textContent?.trim() || '';
  if (slideState && slideState.stageKey !== stageKey) cleanupSlideState();

  for (const board of screen.querySelectorAll('.board-wrap')) decorateBoard(board);

  if (slideState?.ending && slideState.settled && expectedBoardMatches(slideState.board)) cleanupSlideState();
}

const observer = new MutationObserver(scan);
if (screen) observer.observe(screen, { childList: true, subtree: true });
queueMicrotask(scan);

document.addEventListener('pointerdown', startSlide, { capture: true, passive: true });
document.addEventListener('pointermove', updateSlide, { capture: true, passive: true });
document.addEventListener('pointerup', finishSlide, { capture: true, passive: true });
document.addEventListener('pointercancel', finishSlide, { capture: true, passive: true });

// Linkline visual asset system v5.2: direct 1:1 fixed-length forward-only chain slide with heavier chain/node visual weight; clear state terminates the visual drag immediately.