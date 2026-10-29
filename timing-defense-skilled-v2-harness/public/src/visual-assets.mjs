const SVG_NS = 'http://www.w3.org/2000/svg';
const screen = document.querySelector('#screen');
const stageLabel = document.querySelector('#stage-label');
const reducedMotion = globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;
const DRAG_FOLLOW_TAU_MS = 30;
const DRAG_RELEASE_TAU_MS = 44;
const DRAG_EPSILON = 0.035;
const MIN_DRAG_SAMPLES = 24;
let lastIntroStage = null;
let dragPreview = null;

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

function cellCenter(cell, n) {
  const number = cellNumber(cell);
  if (!Number.isInteger(number)) return null;
  const row = Math.floor(number / n);
  const col = number % n;
  const step = 100 / n;
  return { x: (col + 0.5) * step, y: (row + 0.5) * step };
}

function clientToBoard(board, clientX, clientY) {
  const rect = board?.getBoundingClientRect();
  if (!rect?.width || !rect?.height) return null;
  return {
    x: Math.max(0, Math.min(100, ((clientX - rect.left) / rect.width) * 100)),
    y: Math.max(0, Math.min(100, ((clientY - rect.top) / rect.height) * 100)),
  };
}

function distanceSquared(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  return dx * dx + dy * dy;
}

function pointsToPath(points) {
  if (!points.length) return '';
  return points.map((point, index) =>
    `${index ? 'L' : 'M'}${point.x.toFixed(3)} ${point.y.toFixed(3)}`
  ).join(' ');
}

function sampleSourcePath(board, sampleCount) {
  const sourcePath = board.querySelector(':scope > .links .chain-path');
  if (!sourcePath?.getTotalLength || !sourcePath?.getPointAtLength) return null;
  let length;
  try { length = sourcePath.getTotalLength(); } catch { return null; }
  if (!Number.isFinite(length) || length <= 0) return null;

  const points = [];
  for (let index = 0; index < sampleCount; index++) {
    const ratio = sampleCount === 1 ? 0 : index / (sampleCount - 1);
    const point = sourcePath.getPointAtLength(length * ratio);
    points.push({ x: point.x, y: point.y });
  }
  return points;
}

function orientDraggedEnd(points, reference) {
  if (!reference || points.length < 2) return points;
  return distanceSquared(points[0], reference) <= distanceSquared(points.at(-1), reference)
    ? points
    : [...points].reverse();
}

function appendSocket(svg, point, radius, docked) {
  const group = svgNode('g', {}, `target-socket${docked ? ' is-docked' : ''}`);
  group.append(
    svgNode('circle', { cx: point.x, cy: point.y, r: radius * 1.34 }, 'socket-field'),
    svgNode('circle', { cx: point.x, cy: point.y, r: radius }, 'socket-ring'),
    svgNode('circle', { cx: point.x, cy: point.y, r: radius * 0.62 }, 'socket-inner'),
    svgNode('circle', { cx: point.x, cy: point.y, r: radius * 0.16 }, 'socket-core'),
  );

  for (const [dx, dy] of [[0, -1], [1, 0], [0, 1], [-1, 0]]) {
    const inner = radius * 0.76;
    const outer = radius * 1.08;
    group.append(svgNode('line', {
      x1: point.x + dx * inner,
      y1: point.y + dy * inner,
      x2: point.x + dx * outer,
      y2: point.y + dy * outer,
    }, 'socket-notch'));
  }
  svg.append(group);
}

function endpointGlyph(radius, selected, docked) {
  const group = svgNode('g', {}, `endpoint-handle${selected ? ' is-selected' : ''}${docked ? ' is-docked' : ''}`);
  group.append(
    svgNode('circle', { cx: 0, cy: 0, r: radius * 1.12 }, 'handle-shadow'),
    svgNode('circle', { cx: 0, cy: 0, r: radius * 0.74 }, 'handle-body'),
    svgNode('circle', { cx: 0, cy: 0, r: radius * 0.46 }, 'handle-ring'),
    svgNode('circle', { cx: 0, cy: 0, r: radius * 0.16 }, 'handle-pin'),
  );

  for (const [dx, dy] of [[0, -1], [1, 0], [0, 1], [-1, 0]]) {
    const inner = radius * 0.72;
    const outer = radius * 0.98;
    group.append(svgNode('line', {
      x1: dx * inner,
      y1: dy * inner,
      x2: dx * outer,
      y2: dy * outer,
    }, 'handle-lug'));
  }
  return group;
}

function appendEndpoint(svg, point, radius, selected, docked) {
  const group = endpointGlyph(radius, selected, docked);
  group.setAttribute('transform', `translate(${point.x} ${point.y})`);
  svg.append(group);
  return group;
}

function createChainOverlay(board, n) {
  const sourcePath = board.querySelector(':scope > .links .chain-path');
  const d = sourcePath?.getAttribute('d');
  if (!d) return null;

  const svg = svgNode('svg', { viewBox: '0 0 100 100', 'aria-hidden': 'true' }, 'visual-chain-overlay');
  svg.append(
    svgNode('path', { d }, 'visual-chain-shadow'),
    svgNode('path', { d }, 'visual-chain-body'),
    svgNode('path', { d }, 'visual-chain-sheen'),
  );

  const jointRadius = Math.min(1.65, Math.max(1.05, (100 / n) * 0.055));
  for (const cell of board.querySelectorAll('.cell.chain:not(.endpoint)')) {
    const point = cellCenter(cell, n);
    if (point) svg.append(svgNode('circle', { cx: point.x, cy: point.y, r: jointRadius }, 'visual-chain-joint'));
  }
  return svg;
}

function createBoardAssets(board, n) {
  const svg = svgNode('svg', { viewBox: '0 0 100 100', 'aria-hidden': 'true' }, 'visual-board-assets');
  const socketRadius = Math.min(8.2, Math.max(5.4, (100 / n) * 0.32));
  const endpointRadius = socketRadius * 0.88;
  const endpointEntries = [];

  for (const cell of board.querySelectorAll('.cell.target')) {
    const point = cellCenter(cell, n);
    if (!point) continue;
    appendSocket(svg, point, socketRadius, cell.classList.contains('endpoint'));
  }

  for (const cell of board.querySelectorAll('.cell.endpoint')) {
    const point = cellCenter(cell, n);
    if (!point) continue;
    const group = appendEndpoint(
      svg,
      point,
      endpointRadius,
      cell.classList.contains('selected'),
      cell.classList.contains('target'),
    );
    endpointEntries.push({ group, point });
  }
  return { svg, endpointRadius, endpointEntries };
}

function createDragOverlay(n, points, chainCellCount, endpointRadius) {
  const svg = svgNode('svg', { viewBox: '0 0 100 100', 'aria-hidden': 'true' }, 'visual-drag-preview');
  const d = pointsToPath(points);
  const shadow = svgNode('path', { d }, 'drag-chain-shadow');
  const body = svgNode('path', { d }, 'drag-chain-body');
  const sheen = svgNode('path', { d }, 'drag-chain-sheen');
  svg.append(shadow, body, sheen);

  const jointRadius = Math.min(1.65, Math.max(1.05, (100 / n) * 0.055));
  const joints = [];
  for (let index = 1; index < chainCellCount - 1; index++) {
    const sampleIndex = Math.round((index / (chainCellCount - 1)) * (points.length - 1));
    const point = points[sampleIndex];
    const node = svgNode('circle', { cx: point.x, cy: point.y, r: jointRadius }, 'drag-chain-joint');
    joints.push({ node, sampleIndex });
    svg.append(node);
  }

  const handle = endpointGlyph(endpointRadius, true, false);
  handle.classList.add('drag-follow-handle');
  handle.setAttribute('transform', `translate(${points[0].x} ${points[0].y})`);
  svg.append(handle);
  return { svg, paths: [shadow, body, sheen], joints, handle };
}

function markDraggedSource(endpointEntries, reference) {
  for (const entry of endpointEntries) entry.group.classList.remove('is-drag-source');
  if (!reference || !endpointEntries.length) return;
  const source = endpointEntries.reduce((best, entry) =>
    !best || distanceSquared(entry.point, reference) < distanceSquared(best.point, reference) ? entry : best
  , null);
  source?.group.classList.add('is-drag-source');
}

function decorateBoard(board) {
  if (!board || board.classList.contains('visual-assets-v1') || board.classList.contains('linkline-board-ghost')) return;
  const grid = board.querySelector(':scope > .board');
  const cells = grid?.querySelectorAll('.cell');
  const n = cells?.length ? Math.round(Math.sqrt(cells.length)) : 0;
  if (!grid || !n || n * n !== cells.length) return;

  const chain = createChainOverlay(board, n);
  const assets = createBoardAssets(board, n);
  if (!chain) return;

  board.classList.add('visual-assets-v1');
  board.insertBefore(chain, grid);
  board.insertBefore(assets.svg, grid);

  const stageKey = stageLabel?.textContent?.trim() || '';
  if (!reducedMotion && stageKey && stageKey !== lastIntroStage && !board.closest('.linkline-board-ghost')) {
    lastIntroStage = stageKey;
    board.classList.add('visual-assets-intro');
    setTimeout(() => board.classList.remove('visual-assets-intro'), 920);
  }

  if (dragPreview) attachDragPreview(board, n, assets);
}

function deformChain(basePoints, pointer) {
  if (!basePoints?.length || !pointer) return basePoints ?? [];
  const offsetX = pointer.x - basePoints[0].x;
  const offsetY = pointer.y - basePoints[0].y;
  const denominator = Math.max(1, basePoints.length - 1);

  return basePoints.map((point, index) => {
    const t = index / denominator;
    const weight = Math.pow(1 - t, 2.15);
    return {
      x: point.x + offsetX * weight,
      y: point.y + offsetY * weight,
    };
  });
}

function maxDelta(points, targets) {
  let max = 0;
  for (let index = 0; index < points.length; index++) {
    max = Math.max(max, Math.sqrt(distanceSquared(points[index], targets[index])));
  }
  return max;
}

function updateDragOverlay() {
  if (!dragPreview?.svg?.isConnected) return;
  const d = pointsToPath(dragPreview.renderPoints);
  for (const path of dragPreview.paths) path.setAttribute('d', d);
  for (const joint of dragPreview.joints) {
    const point = dragPreview.renderPoints[joint.sampleIndex];
    joint.node.setAttribute('cx', point.x);
    joint.node.setAttribute('cy', point.y);
  }
  const endpoint = dragPreview.renderPoints[0];
  dragPreview.handle.setAttribute('transform', `translate(${endpoint.x} ${endpoint.y})`);
}

function stopDragFrame() {
  if (dragPreview?.raf) cancelAnimationFrame(dragPreview.raf);
  if (dragPreview) dragPreview.raf = 0;
}

function cleanupDragPreview() {
  if (!dragPreview) return;
  stopDragFrame();
  dragPreview.board?.classList.remove('visual-drag-following');
  dragPreview.svg?.remove();
  dragPreview = null;
}

function runDragFrame(now) {
  if (!dragPreview) return;
  if (!dragPreview.board?.isConnected || !dragPreview.svg?.isConnected) {
    dragPreview.raf = 0;
    return;
  }

  const pointer = dragPreview.releasing
    ? dragPreview.basePoints[0]
    : clientToBoard(dragPreview.board, dragPreview.clientX, dragPreview.clientY) || dragPreview.basePoints[0];
  const desired = dragPreview.releasing
    ? dragPreview.basePoints
    : deformChain(dragPreview.basePoints, pointer);

  const previousTime = dragPreview.lastTime || now;
  const dt = Math.min(48, Math.max(0, now - previousTime));
  dragPreview.lastTime = now;
  const tau = dragPreview.releasing ? DRAG_RELEASE_TAU_MS : DRAG_FOLLOW_TAU_MS;
  const alpha = reducedMotion ? 1 : 1 - Math.exp(-dt / tau);

  for (let index = 0; index < dragPreview.renderPoints.length; index++) {
    const point = dragPreview.renderPoints[index];
    const target = desired[index];
    point.x += (target.x - point.x) * alpha;
    point.y += (target.y - point.y) * alpha;
  }

  updateDragOverlay();
  const delta = maxDelta(dragPreview.renderPoints, desired);

  if (dragPreview.releasing && delta <= DRAG_EPSILON) {
    cleanupDragPreview();
    return;
  }

  dragPreview.raf = requestAnimationFrame(runDragFrame);
}

function ensureDragFrame() {
  if (!dragPreview || dragPreview.raf) return;
  dragPreview.lastTime = performance.now();
  dragPreview.raf = requestAnimationFrame(runDragFrame);
}

function attachDragPreview(board, n, assets = null) {
  if (!dragPreview || !board?.isConnected) return;
  if (dragPreview.board === board && dragPreview.svg?.isConnected) {
    ensureDragFrame();
    return;
  }

  const chainCellCount = board.querySelectorAll('.cell.chain').length;
  const sampleCount = Math.max(MIN_DRAG_SAMPLES, chainCellCount * 8);
  let basePoints = sampleSourcePath(board, sampleCount);
  if (!basePoints?.length) return;

  const pointer = clientToBoard(board, dragPreview.clientX, dragPreview.clientY);
  const reference = dragPreview.renderPoints?.[0] || pointer;
  basePoints = orientDraggedEnd(basePoints, reference);

  const boardAssets = assets || createBoardAssets(board, n);
  if (!assets) board.insertBefore(boardAssets.svg, board.querySelector(':scope > .board'));

  if (!dragPreview.renderPoints || dragPreview.renderPoints.length !== basePoints.length) {
    dragPreview.renderPoints = basePoints.map((point) => ({ ...point }));
  }

  stopDragFrame();
  dragPreview.board?.classList.remove('visual-drag-following');
  dragPreview.svg?.remove();

  const overlay = createDragOverlay(n, dragPreview.renderPoints, chainCellCount, boardAssets.endpointRadius);
  dragPreview.board = board;
  dragPreview.basePoints = basePoints.map((point) => ({ ...point }));
  dragPreview.svg = overlay.svg;
  dragPreview.paths = overlay.paths;
  dragPreview.joints = overlay.joints;
  dragPreview.handle = overlay.handle;
  dragPreview.raf = 0;
  dragPreview.lastTime = 0;

  markDraggedSource(boardAssets.endpointEntries, basePoints[0]);
  board.classList.add('visual-drag-following');
  board.append(overlay.svg);
  updateDragOverlay();
  ensureDragFrame();
}

function startDragPreview(event) {
  const cell = event.target.closest?.('.cell.endpoint');
  const board = cell?.closest?.('.board-wrap.visual-assets-v1');
  if (!board || dragPreview) return;

  const grid = board.querySelector(':scope > .board');
  const count = grid?.querySelectorAll('.cell')?.length ?? 0;
  const n = count ? Math.round(Math.sqrt(count)) : 0;
  if (!n || n * n !== count) return;

  dragPreview = {
    pointerId: event.pointerId,
    clientX: event.clientX,
    clientY: event.clientY,
    board: null,
    basePoints: [],
    renderPoints: null,
    svg: null,
    paths: [],
    joints: [],
    handle: null,
    raf: 0,
    lastTime: 0,
    releasing: false,
  };
  attachDragPreview(board, n);
}

function updateDragPreview(event) {
  if (!dragPreview || dragPreview.releasing || event.pointerId !== dragPreview.pointerId) return;
  dragPreview.clientX = event.clientX;
  dragPreview.clientY = event.clientY;
  ensureDragFrame();
}

function finishDragPreview(event) {
  if (!dragPreview || (event?.pointerId !== undefined && event.pointerId !== dragPreview.pointerId)) return;
  if (!dragPreview.board?.isConnected || !dragPreview.basePoints.length) {
    cleanupDragPreview();
    return;
  }
  dragPreview.releasing = true;
  ensureDragFrame();
}

const style = document.createElement('style');
style.dataset.linklineVisualAssets = 'v3';
style.textContent = `
.board-wrap.visual-assets-v1 > .links:not(.completion-pulse):not(.handoff-pulse):not(.arrival-pulse){opacity:0}
.board-wrap.visual-assets-v1 .cell.target::before,.board-wrap.visual-assets-v1 .cell.chain::after{opacity:0!important}
.board-wrap.visual-assets-v1 .cell.selected{box-shadow:none}
.visual-chain-overlay,.visual-board-assets,.visual-drag-preview{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
.visual-chain-overlay{z-index:4}
.visual-board-assets{z-index:5}
.visual-drag-preview{z-index:7}
.visual-chain-shadow,.visual-chain-body,.visual-chain-sheen,.drag-chain-shadow,.drag-chain-body,.drag-chain-sheen{fill:none;stroke-linecap:round;stroke-linejoin:round}
.visual-chain-shadow,.drag-chain-shadow{stroke:rgba(23,23,22,.20);stroke-width:3.55;filter:drop-shadow(0 2px 2px rgba(23,23,22,.14))}
.visual-chain-body,.drag-chain-body{stroke:#171716;stroke-width:2.35}
.visual-chain-sheen,.drag-chain-sheen{stroke:rgba(255,253,248,.38);stroke-width:.46;opacity:.86}
.visual-chain-joint,.drag-chain-joint{fill:#171716;stroke:rgba(255,253,248,.82);stroke-width:.34;filter:drop-shadow(0 1px 1px rgba(23,23,22,.18))}
.socket-field{fill:rgba(18,104,255,.045);stroke:rgba(18,104,255,.10);stroke-width:.55}
.socket-ring{fill:rgba(250,247,239,.84);stroke:#1268ff;stroke-width:1.18;filter:drop-shadow(0 0 2.2px rgba(18,104,255,.18))}
.socket-inner{fill:none;stroke:rgba(18,104,255,.42);stroke-width:.72;stroke-dasharray:1.5 1.25}
.socket-core{fill:rgba(18,104,255,.17)}
.socket-notch{stroke:#1268ff;stroke-width:1.06;stroke-linecap:round}
.handle-shadow{fill:rgba(23,23,22,.10)}
.handle-body{fill:#171716;stroke:#fffdf8;stroke-width:.52;filter:drop-shadow(0 1px 1.4px rgba(23,23,22,.28))}
.handle-ring{fill:none;stroke:rgba(255,253,248,.72);stroke-width:.62}
.handle-pin{fill:#fffdf8}
.handle-lug{stroke:#171716;stroke-width:1.22;stroke-linecap:round}
.endpoint-handle.is-selected .handle-shadow{fill:rgba(18,104,255,.19)}
.endpoint-handle.is-selected .handle-body{stroke:#1268ff;stroke-width:.88}
.endpoint-handle.is-selected .handle-pin{fill:#1268ff}
.endpoint-handle.is-docked .handle-body{fill:#1268ff;stroke:#fffdf8}
.endpoint-handle.is-docked .handle-lug{stroke:#1268ff}
.target-socket.is-docked .socket-field{fill:rgba(18,104,255,.10);stroke:rgba(18,104,255,.20)}
.board-wrap.dragging .target-socket:not(.is-docked),.board-wrap.visual-drag-following .target-socket:not(.is-docked){animation:linklineSocketReady .54s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center}
.board-wrap.dragging .endpoint-handle.is-selected{filter:drop-shadow(0 0 3px rgba(18,104,255,.35))}
.board-wrap.visual-drag-following .visual-chain-overlay{opacity:.10}
.board-wrap.visual-drag-following .endpoint-handle.is-drag-source{opacity:.12}
.drag-follow-handle{filter:drop-shadow(0 3px 4px rgba(23,23,22,.18))}
.visual-assets-intro .endpoint-handle{animation:linklineHandleCue .46s cubic-bezier(.2,.76,.22,1) both;transform-box:fill-box;transform-origin:center}
.visual-assets-intro .target-socket{animation:linklineSocketCue .62s .18s cubic-bezier(.2,.76,.22,1) both;transform-box:fill-box;transform-origin:center}
@keyframes linklineHandleCue{0%{opacity:.72;transform:scale(.82)}55%{opacity:1;transform:scale(1.16)}100%{opacity:1;transform:scale(1)}}
@keyframes linklineSocketCue{0%{opacity:.48;transform:scale(.86)}52%{opacity:1;transform:scale(1.12)}100%{opacity:1;transform:scale(1)}}
@keyframes linklineSocketReady{from{filter:drop-shadow(0 0 1px rgba(18,104,255,.12));transform:scale(1)}to{filter:drop-shadow(0 0 4px rgba(18,104,255,.34));transform:scale(1.06)}}
@media (prefers-reduced-motion:reduce){.visual-assets-intro .endpoint-handle,.visual-assets-intro .target-socket,.board-wrap.dragging .target-socket,.board-wrap.visual-drag-following .target-socket{animation:none!important}}
`;
document.head.append(style);

function scan() {
  if (!screen) return;
  if (!screen.classList.contains('view-game')) {
    lastIntroStage = null;
    cleanupDragPreview();
    return;
  }
  for (const board of screen.querySelectorAll('.board-wrap')) decorateBoard(board);
}

const observer = new MutationObserver(scan);
if (screen) observer.observe(screen, { childList: true, subtree: true });
queueMicrotask(scan);

document.addEventListener('pointerdown', startDragPreview, { capture: true, passive: true });
document.addEventListener('pointermove', updateDragPreview, { capture: true, passive: true });
document.addEventListener('pointerup', finishDragPreview, { capture: true, passive: true });
document.addEventListener('pointercancel', finishDragPreview, { capture: true, passive: true });

// Linkline visual asset system v3: full-chain continuous drag follow over unchanged discrete mechanics.