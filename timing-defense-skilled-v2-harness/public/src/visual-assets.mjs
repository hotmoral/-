const SVG_NS = 'http://www.w3.org/2000/svg';
const screen = document.querySelector('#screen');
const stageLabel = document.querySelector('#stage-label');
const reducedMotion = globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;

const MORPH_DURATION_MS = 76;
const MORPH_SAMPLE_COUNT = 48;
const DRAG_END_GRACE_MS = 280;
const MORPH_EPSILON = 0.018;

let dragState = null;

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

function distanceSquared(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  return dx * dx + dy * dy;
}

function pointsToPath(points) {
  if (!points?.length) return '';
  return points.map((point, index) =>
    `${index ? 'L' : 'M'}${point.x.toFixed(3)} ${point.y.toFixed(3)}`
  ).join(' ');
}

function sampleSourcePath(board, sampleCount = MORPH_SAMPLE_COUNT) {
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

function orientToEndpoint(points, endpointPoint) {
  if (!points?.length || !endpointPoint) return points;
  return distanceSquared(points[0], endpointPoint) <= distanceSquared(points.at(-1), endpointPoint)
    ? points
    : [...points].reverse();
}

function orientToPrevious(points, previous) {
  if (!points?.length || !previous?.length) return points;
  const direct =
    distanceSquared(points[0], previous[0]) +
    distanceSquared(points.at(-1), previous.at(-1));
  const reversed =
    distanceSquared(points.at(-1), previous[0]) +
    distanceSquared(points[0], previous.at(-1));
  return reversed < direct ? [...points].reverse() : points;
}

function visualMetrics(n) {
  const step = 100 / n;
  const endpointRadius = Math.min(4.2, Math.max(2.8, step * 0.16));
  return {
    endpointRadius,
    targetRadius: endpointRadius * 1.42,
    targetCoreRadius: Math.max(0.48, endpointRadius * 0.16),
    jointRadius: Math.min(1.4, Math.max(0.9, step * 0.055)),
  };
}

function appendTarget(svg, point, metrics, docked) {
  const group = svgNode('g', {}, `target-mark${docked ? ' is-docked' : ''}`);
  group.append(
    svgNode('circle', {
      cx: point.x,
      cy: point.y,
      r: metrics.targetRadius,
    }, 'target-ring'),
    svgNode('circle', {
      cx: point.x,
      cy: point.y,
      r: metrics.targetCoreRadius,
    }, 'target-core'),
  );
  svg.append(group);
}

function appendEndpoint(svg, point, metrics, selected, docked) {
  const node = svgNode('circle', {
    cx: point.x,
    cy: point.y,
    r: metrics.endpointRadius,
  }, `endpoint-dot${selected ? ' is-selected' : ''}${docked ? ' is-docked' : ''}`);
  svg.append(node);
  return node;
}

function createStaticChain(board, n) {
  const sourcePath = board.querySelector(':scope > .links .chain-path');
  const d = sourcePath?.getAttribute('d');
  if (!d) return null;

  const metrics = visualMetrics(n);
  const svg = svgNode('svg', {
    viewBox: '0 0 100 100',
    'aria-hidden': 'true',
  }, 'visual-chain-overlay');

  svg.append(
    svgNode('path', { d }, 'visual-chain-shadow'),
    svgNode('path', { d }, 'visual-chain-body'),
  );

  for (const cell of board.querySelectorAll('.cell.chain:not(.endpoint)')) {
    const point = cellCenter(cell, n);
    if (point) {
      svg.append(svgNode('circle', {
        cx: point.x,
        cy: point.y,
        r: metrics.jointRadius,
      }, 'visual-chain-joint'));
    }
  }
  return svg;
}

function createStaticMarks(board, n) {
  const svg = svgNode('svg', {
    viewBox: '0 0 100 100',
    'aria-hidden': 'true',
  }, 'visual-board-assets');
  const metrics = visualMetrics(n);

  for (const cell of board.querySelectorAll('.cell.target')) {
    const point = cellCenter(cell, n);
    if (point) appendTarget(svg, point, metrics, cell.classList.contains('endpoint'));
  }

  for (const cell of board.querySelectorAll('.cell.endpoint')) {
    const point = cellCenter(cell, n);
    if (!point) continue;
    appendEndpoint(
      svg,
      point,
      metrics,
      cell.classList.contains('selected'),
      cell.classList.contains('target'),
    );
  }
  return svg;
}

function createMorphOverlay(n, points, chainCellCount) {
  const metrics = visualMetrics(n);
  const svg = svgNode('svg', {
    viewBox: '0 0 100 100',
    'aria-hidden': 'true',
  }, 'visual-morph-overlay');
  const d = pointsToPath(points);

  const shadow = svgNode('path', { d }, 'morph-chain-shadow');
  const body = svgNode('path', { d }, 'morph-chain-body');
  svg.append(shadow, body);

  const joints = [];
  for (let index = 1; index < chainCellCount - 1; index++) {
    const sampleIndex = Math.round((index / (chainCellCount - 1)) * (points.length - 1));
    const point = points[sampleIndex];
    const node = svgNode('circle', {
      cx: point.x,
      cy: point.y,
      r: metrics.jointRadius,
    }, 'morph-chain-joint');
    joints.push({ node, sampleIndex });
    svg.append(node);
  }

  const startEndpoint = appendEndpoint(svg, points[0], metrics, true, false);
  const endEndpoint = appendEndpoint(svg, points.at(-1), metrics, false, false);
  startEndpoint.classList.add('morph-endpoint');
  endEndpoint.classList.add('morph-endpoint');

  return {
    svg,
    paths: [shadow, body],
    joints,
    endpoints: [startEndpoint, endEndpoint],
  };
}

function maxDelta(a, b) {
  let max = 0;
  for (let index = 0; index < Math.min(a.length, b.length); index++) {
    max = Math.max(max, Math.sqrt(distanceSquared(a[index], b[index])));
  }
  return max;
}

function stopMorph() {
  const morph = dragState?.morph;
  if (!morph) return;
  if (morph.raf) cancelAnimationFrame(morph.raf);
  morph.board?.classList.remove('is-chain-morphing');
  morph.svg?.remove();
  dragState.morph = null;
}

function updateMorphOverlay(morph, points) {
  const d = pointsToPath(points);
  for (const path of morph.paths) path.setAttribute('d', d);

  for (const joint of morph.joints) {
    const point = points[joint.sampleIndex];
    joint.node.setAttribute('cx', point.x);
    joint.node.setAttribute('cy', point.y);
  }

  const first = points[0];
  const last = points.at(-1);
  morph.endpoints[0].setAttribute('cx', first.x);
  morph.endpoints[0].setAttribute('cy', first.y);
  morph.endpoints[1].setAttribute('cx', last.x);
  morph.endpoints[1].setAttribute('cy', last.y);
}

function cleanupDragState() {
  if (!dragState) return;
  if (dragState.endTimer !== null) clearTimeout(dragState.endTimer);
  stopMorph();
  dragState.board?.classList.remove('visual-drag-active');
  dragState = null;
}

function scheduleDragCleanup() {
  if (!dragState) return;
  if (dragState.endTimer !== null) clearTimeout(dragState.endTimer);
  dragState.endTimer = setTimeout(cleanupDragState, reducedMotion ? 0 : DRAG_END_GRACE_MS);
}

function runMorphFrame(now) {
  const state = dragState;
  const morph = state?.morph;
  if (!state || !morph) return;

  if (!morph.board?.isConnected || !morph.svg?.isConnected) {
    morph.raf = 0;
    return;
  }

  const duration = reducedMotion ? 0 : MORPH_DURATION_MS;
  const raw = duration === 0 ? 1 : Math.min(1, Math.max(0, (now - morph.startedAt) / duration));
  const eased = 1 - Math.pow(1 - raw, 3);

  for (let index = 0; index < state.renderPoints.length; index++) {
    const from = morph.fromPoints[index];
    const to = morph.toPoints[index];
    state.renderPoints[index] = {
      x: from.x + (to.x - from.x) * eased,
      y: from.y + (to.y - from.y) * eased,
    };
  }

  updateMorphOverlay(morph, state.renderPoints);

  if (raw < 1) {
    morph.raf = requestAnimationFrame(runMorphFrame);
    return;
  }

  state.renderPoints = morph.toPoints.map((point) => ({ ...point }));
  morph.board.classList.remove('is-chain-morphing');
  morph.svg.remove();
  state.morph = null;

  if (state.ending) scheduleDragCleanup();
}

function beginMorph(board, n) {
  if (!dragState || dragState.stageKey !== stageLabel?.textContent?.trim()) return;

  let targetPoints = sampleSourcePath(board);
  if (!targetPoints?.length) return;
  targetPoints = orientToPrevious(targetPoints, dragState.renderPoints);

  const previous = dragState.renderPoints?.length === targetPoints.length
    ? dragState.renderPoints.map((point) => ({ ...point }))
    : targetPoints.map((point) => ({ ...point }));

  stopMorph();
  if (dragState.endTimer !== null) {
    clearTimeout(dragState.endTimer);
    dragState.endTimer = null;
  }
  dragState.board?.classList.remove('visual-drag-active');
  dragState.board = board;
  board.classList.add('visual-drag-active');

  if (maxDelta(previous, targetPoints) <= MORPH_EPSILON) {
    dragState.renderPoints = targetPoints.map((point) => ({ ...point }));
    if (dragState.ending) scheduleDragCleanup();
    return;
  }

  dragState.renderPoints = previous.map((point) => ({ ...point }));
  const chainCellCount = board.querySelectorAll('.cell.chain').length;
  const overlay = createMorphOverlay(n, dragState.renderPoints, chainCellCount);

  board.classList.add('is-chain-morphing');
  board.append(overlay.svg);

  dragState.morph = {
    ...overlay,
    board,
    fromPoints: previous,
    toPoints: targetPoints.map((point) => ({ ...point })),
    startedAt: performance.now(),
    raf: requestAnimationFrame(runMorphFrame),
  };
}

function decorateBoard(board) {
  if (!board || board.classList.contains('visual-assets-v4') || board.classList.contains('linkline-board-ghost')) return;

  const grid = board.querySelector(':scope > .board');
  const cells = grid?.querySelectorAll('.cell');
  const n = cells?.length ? Math.round(Math.sqrt(cells.length)) : 0;
  if (!grid || !n || n * n !== cells.length) return;

  const chain = createStaticChain(board, n);
  if (!chain) return;
  const marks = createStaticMarks(board, n);

  board.classList.add('visual-assets-v4');
  board.insertBefore(chain, grid);
  board.insertBefore(marks, grid);

  if (dragState) beginMorph(board, n);
}

function startDrag(event) {
  const cell = event.target.closest?.('.cell.endpoint');
  const board = cell?.closest?.('.board-wrap.visual-assets-v4');
  if (!board) return;

  cleanupDragState();

  const grid = board.querySelector(':scope > .board');
  const count = grid?.querySelectorAll('.cell')?.length ?? 0;
  const n = count ? Math.round(Math.sqrt(count)) : 0;
  if (!n || n * n !== count) return;

  const endpointPoint = cellCenter(cell, n);
  let points = sampleSourcePath(board);
  if (!points?.length || !endpointPoint) return;
  points = orientToEndpoint(points, endpointPoint);

  dragState = {
    pointerId: event.pointerId,
    stageKey: stageLabel?.textContent?.trim() || '',
    board,
    renderPoints: points.map((point) => ({ ...point })),
    morph: null,
    ending: false,
    endTimer: null,
  };
  board.classList.add('visual-drag-active');
}

function finishDrag(event) {
  if (!dragState || (event?.pointerId !== undefined && event.pointerId !== dragState.pointerId)) return;
  dragState.ending = true;
  scheduleDragCleanup();
}

const style = document.createElement('style');
style.dataset.linklineVisualAssets = 'v4';
style.textContent = `
.board-wrap.visual-assets-v4 > .links:not(.completion-pulse):not(.handoff-pulse):not(.arrival-pulse){opacity:0}
.board-wrap.visual-assets-v4 .cell.target::before,.board-wrap.visual-assets-v4 .cell.chain::after{opacity:0!important}
.board-wrap.visual-assets-v4 .cell.selected{box-shadow:none}
.visual-chain-overlay,.visual-board-assets,.visual-morph-overlay{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible}
.visual-chain-overlay{z-index:4}
.visual-board-assets{z-index:5}
.visual-morph-overlay{z-index:7}
.visual-chain-shadow,.visual-chain-body,.morph-chain-shadow,.morph-chain-body{fill:none;stroke-linecap:round;stroke-linejoin:round}
.visual-chain-shadow,.morph-chain-shadow{stroke:rgba(23,23,22,.13);stroke-width:3.25;filter:drop-shadow(0 1.2px 1.4px rgba(23,23,22,.10))}
.visual-chain-body,.morph-chain-body{stroke:#1d1d1b;stroke-width:2.30}
.visual-chain-joint,.morph-chain-joint{fill:#1d1d1b}
.endpoint-dot{fill:#1d1d1b;stroke:rgba(255,255,255,.88);stroke-width:.34}
.endpoint-dot.is-selected{stroke:#1268ff;stroke-width:.78}
.endpoint-dot.is-docked{fill:#1268ff;stroke:#fff;stroke-width:.46}
.target-ring{fill:rgba(18,104,255,.025);stroke:#1268ff;stroke-width:1.05}
.target-core{fill:rgba(18,104,255,.30)}
.target-mark.is-docked .target-ring{stroke-opacity:.42}
.target-mark.is-docked .target-core{opacity:0}
.board-wrap.visual-drag-active .target-ring{stroke-width:1.22;filter:drop-shadow(0 0 1.8px rgba(18,104,255,.18))}
.board-wrap.is-chain-morphing .visual-chain-overlay,
.board-wrap.is-chain-morphing .visual-board-assets .endpoint-dot{opacity:0}
@media (prefers-reduced-motion:reduce){.board-wrap.visual-drag-active .target-ring{filter:none}}
`;
document.head.append(style);

function scan() {
  if (!screen) return;

  if (!screen.classList.contains('view-game')) {
    cleanupDragState();
    return;
  }

  const stageKey = stageLabel?.textContent?.trim() || '';
  if (dragState && dragState.stageKey !== stageKey) cleanupDragState();

  for (const board of screen.querySelectorAll('.board-wrap')) decorateBoard(board);
}

const observer = new MutationObserver(scan);
if (screen) observer.observe(screen, { childList: true, subtree: true });
queueMicrotask(scan);

document.addEventListener('pointerdown', startDrag, { capture: true, passive: true });
document.addEventListener('pointerup', finishDrag, { capture: true, passive: true });
document.addEventListener('pointercancel', finishDrag, { capture: true, passive: true });

// Linkline visual asset system v4: minimal chain/endpoints/targets + short state-to-state morph only.
