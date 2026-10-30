import { loadCampaign } from './catalog.mjs';
import { loadPerformanceBaseline } from './performance.mjs';
import { applyClearedAttempt } from './clear-outcome.mjs';
import { legalCells, activateCell, createPuzzleRuntime } from './runtime.mjs';
import { clearProgress, loadProgress, saveProgress } from './progress.mjs';
import { completionPercent, continuePosition, pageRows, stagePage, stageState } from './navigation.mjs';
import { roundedOrthogonalPath } from './path-geometry.mjs';

const appShell = document.querySelector('.app-shell');
const screen = document.querySelector('#screen');
const stageLabel = document.querySelector('#stage-label');
const campaignLabel = document.querySelector('#campaign-label');
const resetProgressButton = document.querySelector('#reset-progress');

let campaign;
let performanceBaseline = null;
let progress;
let current;
let runtime;
let stagePageAnchor = 1;

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function button(className, text, onClick) {
  const node = el('button', className, text);
  node.type = 'button';
  if (onClick) node.addEventListener('click', onClick);
  return node;
}

function iconBackButton(onClick, label = '뒤로가기') {
  const node = button('icon-back', '', onClick);
  node.setAttribute('aria-label', label);
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 32 32');
  svg.setAttribute('aria-hidden', 'true');
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', 'M19.5 7.5 11 16l8.5 8.5M11.5 16H26');
  svg.append(path);
  node.append(svg);
  return node;
}

function lockIcon() {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('aria-hidden', 'true');
  svg.setAttribute('width', '22');
  svg.setAttribute('height', '22');
  svg.setAttribute('fill', 'none');
  svg.setAttribute('stroke', 'currentColor');
  svg.setAttribute('stroke-width', '1.55');
  svg.setAttribute('stroke-linecap', 'round');
  svg.setAttribute('stroke-linejoin', 'round');

  const shackle = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  shackle.setAttribute('d', 'M8 10V7.8a4 4 0 0 1 8 0V10');
  const body = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
  body.setAttribute('x', '6.5');
  body.setAttribute('y', '10');
  body.setAttribute('width', '11');
  body.setAttribute('height', '9');
  body.setAttribute('rx', '1.4');
  const key = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  key.setAttribute('d', 'M12 13.2v2.7');
  svg.append(shackle, body, key);
  return svg;
}

function setHeader(title, meta = '') {
  stageLabel.textContent = title;
  campaignLabel.textContent = meta;
}

function clearScreen(viewClass) {
  screen.className = `screen ${viewClass}`;
  appShell.dataset.view = viewClass.replace(/^view-/, '');
  screen.replaceChildren();
}

function lineOverlay(puzzlePath, n, className = 'links') {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 100 100');
  svg.classList.add(className);
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', roundedOrthogonalPath(puzzlePath, n, { radiusRatio: 0.22 }));
  path.classList.add('chain-path');
  svg.append(path);
  return svg;
}

function isPreviewCorner(path, index, n) {
  if (index <= 0 || index >= path.length - 1) return false;
  const previous = path[index - 1];
  const currentCell = path[index];
  const next = path[index + 1];
  const pr = Math.floor(previous / n), pc = previous % n;
  const cr = Math.floor(currentCell / n), cc = currentCell % n;
  const nr = Math.floor(next / n), nc = next % n;
  const incoming = [cr - pr, cc - pc];
  const outgoing = [nr - cr, nc - cc];
  return incoming[0] !== outgoing[0] || incoming[1] !== outgoing[1];
}

function signalPreview(puzzle) {
  const wrap = el('div', 'signal-preview');
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 100 100');
  svg.classList.add('signal-preview-svg');

  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', roundedOrthogonalPath(puzzle.initial, puzzle.n, {
    scale: 76,
    offset: 12,
    radiusRatio: 0.22,
  }));
  path.classList.add('signal-line');
  svg.append(path);

  const pos = (cell) => {
    const r = Math.floor(cell / puzzle.n), c = cell % puzzle.n;
    return [12 + (c + 0.5) * 76 / puzzle.n, 12 + (r + 0.5) * 76 / puzzle.n];
  };

  puzzle.initial.forEach((cell, index) => {
    const endpoint = index === 0 || index === puzzle.initial.length - 1;
    if (!endpoint && isPreviewCorner(puzzle.initial, index, puzzle.n)) return;

    const [cx, cy] = pos(cell);
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', cx);
    circle.setAttribute('cy', cy);
    circle.setAttribute('r', endpoint ? 4.6 : 2.25);
    circle.classList.add('signal-node');
    svg.append(circle);
  });

  for (const cell of puzzle.targets) {
    const [cx, cy] = pos(cell);
    const haloOuter = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    haloOuter.setAttribute('cx', cx);
    haloOuter.setAttribute('cy', cy);
    haloOuter.setAttribute('r', 8.6);
    haloOuter.classList.add('signal-halo', 'outer');
    const halo = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    halo.setAttribute('cx', cx);
    halo.setAttribute('cy', cy);
    halo.setAttribute('r', 6.8);
    halo.classList.add('signal-halo');
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', cx);
    circle.setAttribute('cy', cy);
    circle.setAttribute('r', 4.4);
    circle.classList.add('signal-target');
    svg.append(haloOuter, halo, circle);
  }

  wrap.append(svg);
  return wrap;
}

function progressMeter() {
  const highest = progress.highestCleared;
  const total = campaign.puzzles.length;
  const meter = el('div', 'progress-meter');
  const track = el('div', 'progress-track');
  const fill = el('div', 'progress-fill');
  fill.style.width = `${Math.max(0, Math.min(100, (highest / total) * 100))}%`;
  track.append(fill);
  const labels = el('div', 'progress-labels');
  labels.append(el('span', '', `${highest} complete`), el('span', '', `${completionPercent(progress, total)}%`));
  meter.append(track, labels);
  return meter;
}

function homeProgressStrip(position) {
  const total = campaign.puzzles.length;
  const strip = el('div', 'home-progress-strip');
  const dots = el('div', 'home-progress-dots');
  const dotCount = 7;
  const activeCount = Math.max(1, Math.min(dotCount, Math.ceil((position / total) * dotCount)));
  for (let index = 0; index < dotCount; index++) {
    dots.append(el('span', index < activeCount ? 'active' : ''));
  }
  strip.append(dots, el('div', 'home-progress-meta', `${position} / ${campaign.launchTotal}`));
  return strip;
}

function renderHome() {
  const total = campaign.puzzles.length;
  const next = continuePosition(progress, total);
  const complete = progress.highestCleared >= total;
  clearScreen('view-home');
  setHeader('', '');

  const hero = el('section', 'home-hero');
  hero.append(signalPreview(campaign.puzzles[next - 1]));
  const stage = el('div', 'home-stage');
  stage.append(
    el('span', 'home-stage-label', complete ? 'Complete' : 'Stage'),
    el('strong', '', String(next).padStart(3, '0')),
  );
  hero.append(stage, homeProgressStrip(next));

  const actions = el('div', 'home-actions');
  actions.append(button(
    'primary pill large',
    complete ? 'REPLAY FINAL STAGE  →' : `${progress.highestCleared ? 'CONTINUE' : 'START'}  →`,
    () => openStage(next),
  ));
  const secondaryRow = el('div', 'home-secondary');
  secondaryRow.append(
    button('icon-action stage-select-action', 'STAGE SELECT', () => renderStageSelect(next)),
    button('icon-action settings-action', 'SETTINGS', renderSettings),
  );
  actions.append(secondaryRow);
  screen.append(hero, actions);
}

function resetPuzzle() {
  runtime = createPuzzleRuntime(current);
  renderGame();
}

function openStage(position) {
  current = campaign.puzzles[position - 1];
  if (!current) throw new Error(`POSITION_UNAVAILABLE:${position}`);
  runtime = createPuzzleRuntime(current);
  renderGame();
}

function onCell(cell) {
  if (runtime.solved) return;
  const previousSolved = runtime.solved;
  runtime = activateCell(current, runtime, cell);
  if (!previousSolved && runtime.solved) {
    const previousProgress = progress;
    const outcome = applyClearedAttempt(
      progress,
      current.position,
      campaign.puzzles.length,
      runtime.moves,
      performanceBaseline,
    );
    progress = outcome.progress;
    if (outcome.performanceResult && !outcome.performanceResult.ok) {
      console.error('PERFORMANCE_GRADING_INTEGRITY', outcome.performanceResult);
    }
    if (progress !== previousProgress) saveProgress(localStorage, progress);
  }
  renderGame();
}

function renderBoard() {
  const wrap = el('div', 'board-wrap');
  const grid = el('div', 'board');
  grid.style.gridTemplateColumns = `repeat(${current.n}, 1fr)`;
  grid.style.gridTemplateRows = `repeat(${current.n}, 1fr)`;
  const occupied = new Map(runtime.path.map((cell, index) => [cell, index]));
  const legal = new Set(legalCells(current, runtime));

  for (let cell = 0; cell < current.n * current.n; cell++) {
    const cellButton = el('button', 'cell');
    cellButton.type = 'button';
    cellButton.dataset.cell = String(cell);
    const index = occupied.get(cell);
    const endpoint = index === 0 || index === runtime.path.length - 1;
    const selected = endpoint && index === runtime.selectedEndpoint;
    const movable = endpoint && legalCells(current, { ...runtime, selectedEndpoint: index }).length > 0;

    if (current.targets.includes(cell)) cellButton.classList.add('target');
    if (occupied.has(cell)) {
      cellButton.classList.add('chain');
      if (endpoint) cellButton.classList.add('endpoint');
      if (selected) cellButton.classList.add('selected');
    }
    if (legal.has(cell)) cellButton.classList.add('legal');

    const labels = [`칸 ${cell}`];
    if (current.targets.includes(cell)) labels.push('목표');
    if (endpoint) labels.push(movable ? '이동 가능한 끝점' : '고정된 끝점');
    if (legal.has(cell)) labels.push('이동 가능');
    cellButton.setAttribute('aria-label', labels.join(', '));
    if (endpoint) cellButton.setAttribute('aria-pressed', selected ? 'true' : 'false');
    cellButton.addEventListener('click', () => onCell(cell));
    grid.append(cellButton);
  }
  wrap.append(lineOverlay(runtime.path, current.n), grid);
  return wrap;
}

function renderGame() {
  clearScreen('view-game');
  setHeader(`Stage ${String(current.position).padStart(3, '0')}`, `${current.position} / ${campaign.launchTotal}`);

  const nav = el('div', 'play-nav');
  nav.append(
    iconBackButton(renderHome, '홈으로'),
    button('ghost compact', 'STAGES', () => renderStageSelect(current.position)),
  );
  screen.append(nav, renderBoard());

  if (runtime.solved) {
    const success = el('section', 'success-panel');
    success.append(
      el('div', 'success-kicker', 'SIGNAL LINKED'),
      el('div', 'success-title', `Stage ${String(current.position).padStart(3, '0')} complete`),
    );
    const nextUnlocked = continuePosition(progress, campaign.puzzles.length);
    const nextPosition = current.position < campaign.puzzles.length && current.position + 1 <= nextUnlocked
      ? current.position + 1
      : null;
    const actions = el('div', 'success-actions');
    if (nextPosition) actions.append(button('primary pill', 'NEXT STAGE  →', () => openStage(nextPosition)));
    else actions.append(button('primary pill', 'BACK TO HOME', renderHome));
    success.append(actions);
    screen.append(success);
    return;
  }

  const hint = el('div', 'play-hint', '끝점을 끌어 두 목표에 연결하세요.');
  const restart = button('secondary round-action', '↻', resetPuzzle);
  const label = el('span', 'round-action-label', 'RESTART');
  const restartWrap = el('div', 'round-action-wrap');
  restartWrap.append(restart, label);
  screen.append(hint, restartWrap);
}

function stageButton(position) {
  const state = stageState(position, progress, campaign.puzzles.length);
  const className = `stage-node ${state}`;
  const completed = state === 'completed' || state === 'completed-current';
  const node = button(className, completed ? '✓' : state === 'locked' ? '' : String(position), null);
  if (state === 'locked') node.append(lockIcon());
  node.setAttribute(
    'aria-label',
    `Stage ${position}${state === 'locked' ? ', 잠김' : state.includes('completed') ? ', 완료' : ', 현재'}`,
  );
  if (state === 'locked') node.disabled = true;
  else node.addEventListener('click', () => openStage(position));
  const item = el('div', 'stage-item');
  item.append(node, el('span', 'stage-number', String(position)));
  return item;
}

function renderStageSelect(anchor = stagePageAnchor) {
  const total = campaign.puzzles.length;
  stagePageAnchor = Math.max(1, Math.min(total, anchor));
  const page = stagePage(stagePageAnchor, total);
  const currentPosition = continuePosition(progress, total);
  clearScreen('view-stages');
  setHeader('', '');

  const head = el('div', 'stage-select-head');
  const copy = el('div');
  copy.append(
    el('div', 'eyebrow', `${String(page.start).padStart(3, '0')} — ${String(page.end).padStart(3, '0')}`),
    el('h1', 'section-title', 'Stage Select'),
  );
  head.append(iconBackButton(renderHome, '홈으로'), copy);
  screen.append(head, progressMeter());

  const map = el('div', 'stage-map');
  const rows = pageRows(page);
  rows.forEach((positions, rowIndex) => {
    const row = el('div', `stage-row ${rowIndex % 2 ? 'reverse' : ''}`);
    const shown = rowIndex % 2 ? [...positions].reverse() : positions;
    shown.forEach((position) => row.append(stageButton(position)));
    map.append(row);
  });
  screen.append(map);

  const pager = el('div', 'stage-pager');
  const prev = button('secondary pager-button', '←', () => renderStageSelect(Math.max(1, page.start - 1)));
  prev.disabled = page.start === 1;
  const currentPage = button('ghost pager-current', `CURRENT ${currentPosition}`, () => renderStageSelect(currentPosition));
  const next = button('secondary pager-button', '→', () => renderStageSelect(Math.min(total, page.end + 1)));
  next.disabled = page.end === total;
  pager.append(prev, currentPage, next);
  screen.append(pager);
}

function renderSettings() {
  clearScreen('view-settings');
  setHeader('', '');
  const head = el('div', 'stage-select-head');
  const copy = el('div');
  copy.append(el('div', 'eyebrow', 'PRODUCT'), el('h1', 'section-title', 'Settings'));
  head.append(iconBackButton(renderHome, '홈으로'), copy);

  const card = el('section', 'settings-card');
  card.append(
    el('div', 'settings-label', 'PROGRESS'),
    el('div', 'settings-value', `${progress.highestCleared} / ${campaign.puzzles.length} complete`),
    el('p', 'settings-copy', '진행 초기화는 완료 기록을 지우고 Stage 001부터 다시 시작합니다.'),
  );
  const reset = button('danger-outline', 'RESET PROGRESS', () => {
    if (!globalThis.confirm || globalThis.confirm('진행 기록을 초기화할까요?')) {
      clearProgress(localStorage);
      progress = loadProgress(localStorage, campaign.campaignId, campaign.puzzles.length, performanceBaseline);
      renderHome();
    }
  });
  card.append(reset);
  screen.append(head, card);
}

async function boot() {
  campaign = await loadCampaign('./data/campaign-0001-1300.json');
  try {
    performanceBaseline = await loadPerformanceBaseline(
      './data/performance-baseline-v1.json',
      campaign.campaignId,
      campaign.puzzles.length,
    );
  } catch (error) {
    performanceBaseline = null;
    console.error('PERFORMANCE_BASELINE_UNAVAILABLE', error);
  }
  progress = loadProgress(localStorage, campaign.campaignId, campaign.puzzles.length, performanceBaseline);
  stagePageAnchor = continuePosition(progress, campaign.puzzles.length);
  resetProgressButton.hidden = true;
  renderHome();
}

boot().catch((error) => {
  console.error(error);
  clearScreen('view-error');
  setHeader('Error', '');
  screen.append(el('div', 'error', `앱을 시작할 수 없습니다: ${error.message}`));
});
