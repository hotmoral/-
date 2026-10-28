const body = document.body;
const screen = document.querySelector('#screen');
const splash = document.querySelector('#boot-splash');
const stageLabel = document.querySelector('#stage-label');
const campaignLabel = document.querySelector('#campaign-label');

const BOOT_MIN_MS = 220;
const HANDOFF_SWAP_MS = 180;
const HANDOFF_CLEANUP_MS = 380;
const META_CLEANUP_MS = 240;
const reducedMotion = globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;
const bootStartedAt = performance.now();
let bootRevealScheduled = false;
let forwarding = false;
let pendingForward = null;

function revealBootWhenReady() {
  if (bootRevealScheduled || !body.classList.contains('is-booting')) return;
  bootRevealScheduled = true;
  const minimum = reducedMotion ? 0 : BOOT_MIN_MS;
  const remaining = Math.max(0, minimum - (performance.now() - bootStartedAt));
  setTimeout(() => {
    body.classList.remove('is-booting');
    body.classList.add('is-ready');
    splash?.setAttribute('aria-hidden', 'true');
    setTimeout(() => splash?.remove(), reducedMotion ? 0 : 420);
  }, remaining);
}

function clonePathPulse(board, className) {
  const links = board?.querySelector('.links');
  const grid = board?.querySelector('.board');
  if (!links || !grid) return null;
  const pulse = links.cloneNode(true);
  pulse.classList.add(className);
  pulse.setAttribute('aria-hidden', 'true');
  board.insertBefore(pulse, grid);
  return pulse;
}

function playCompletionSignal(board) {
  if (!board) return null;
  board.querySelector('.completion-pulse')?.remove();
  return clonePathPulse(board, 'completion-pulse');
}

function decorateSolvedBoard() {
  if (!screen?.querySelector('.success-panel')) return;
  const board = screen.querySelector('.board-wrap');
  if (!board || board.classList.contains('polish-solved')) return;
  screen.classList.add('polish-success');
  board.classList.add('polish-solved');
  playCompletionSignal(board);
}

function decorateStageSelect() {
  if (!screen?.classList.contains('view-stages') || screen.classList.contains('polish-stage-select')) return;
  screen.classList.add('polish-stage-select');
  const current = screen.querySelector('.stage-node.current, .stage-node.completed-current');
  if (!current) return;
  current.setAttribute('aria-current', 'step');
  current.classList.add('stage-node-arrival');
  setTimeout(() => current.classList.remove('stage-node-arrival'), 560);
}

function createHandoffGhost() {
  const board = screen?.querySelector('.board-wrap');
  if (!board) return null;
  const rect = board.getBoundingClientRect();
  const ghost = board.cloneNode(true);
  ghost.querySelectorAll('.completion-pulse, .handoff-pulse, .arrival-pulse').forEach((node) => node.remove());
  ghost.classList.remove('polish-solved', 'linkline-arrival', 'linkline-incoming-board', 'linkline-handoff-out');
  ghost.classList.add('linkline-board-ghost');
  ghost.setAttribute('aria-hidden', 'true');
  Object.assign(ghost.style, {
    left: `${rect.left}px`,
    top: `${rect.top}px`,
    width: `${rect.width}px`,
    height: `${rect.height}px`,
  });
  document.body.append(ghost);
  return ghost;
}

function prepareMetaExit() {
  stageLabel?.classList.remove('linkline-meta-in');
  campaignLabel?.classList.remove('linkline-meta-in');
  stageLabel?.classList.add('linkline-meta-out');
  campaignLabel?.classList.add('linkline-meta-out');
}

function revealMeta() {
  for (const node of [stageLabel, campaignLabel]) {
    if (!node) continue;
    node.classList.remove('linkline-meta-out');
    node.classList.add('linkline-meta-in');
  }
  setTimeout(() => {
    stageLabel?.classList.remove('linkline-meta-in');
    campaignLabel?.classList.remove('linkline-meta-in');
  }, META_CLEANUP_MS);
}

function prepareIncomingBoard() {
  const board = screen?.querySelector('.board-wrap');
  if (!board || screen?.querySelector('.success-panel')) return null;
  board.classList.add('linkline-incoming-board');
  return board;
}

function finishForwardVisual(pending, incomingBoard) {
  if (!pending) return;
  const { ghost } = pending;
  if (!incomingBoard) {
    ghost?.remove();
    screen?.classList.remove('linkline-forwarding');
    revealMeta();
    forwarding = false;
    return;
  }

  incomingBoard.classList.add('is-visible');
  revealMeta();
  ghost?.classList.add('is-leaving');

  setTimeout(() => {
    ghost?.remove();
    screen?.classList.remove('linkline-forwarding');
    incomingBoard.classList.remove('linkline-incoming-board', 'is-visible');
    forwarding = false;
  }, HANDOFF_CLEANUP_MS);
}

function scan() {
  if (!screen) return;
  if (screen.classList.contains('view-home') || screen.classList.contains('view-error')) {
    revealBootWhenReady();
  }
  decorateSolvedBoard();
  decorateStageSelect();
}

const observer = new MutationObserver(scan);
if (screen) {
  observer.observe(screen, { childList: true, subtree: true, attributes: true, attributeFilter: ['class'] });
}
queueMicrotask(scan);

// Capture only prepares the visual handoff. The trusted NEXT STAGE click is never prevented;
// the app's native button handler advances the stage synchronously at the target phase.
document.addEventListener('click', (event) => {
  const next = event.target.closest?.('.success-actions .primary');
  if (!next || reducedMotion || !screen || !next.textContent.includes('NEXT STAGE')) return;

  if (forwarding) {
    event.preventDefault();
    event.stopPropagation();
    event.stopImmediatePropagation();
    return;
  }

  forwarding = true;
  screen.classList.add('linkline-forwarding');
  prepareMetaExit();
  pendingForward = {
    target: next,
    ghost: createHandoffGhost(),
    startedAt: performance.now(),
  };
}, true);

// This bubble listener runs after the button's native openStage handler. The new board is hidden
// before the browser can paint, then revealed on the original 180 ms visual boundary.
document.addEventListener('click', (event) => {
  if (!pendingForward) return;
  const next = event.target.closest?.('.success-actions .primary');
  if (!next || next !== pendingForward.target) return;

  const pending = pendingForward;
  pendingForward = null;
  const incomingBoard = prepareIncomingBoard();
  const elapsed = performance.now() - pending.startedAt;
  const remaining = Math.max(0, HANDOFF_SWAP_MS - elapsed);
  setTimeout(() => finishForwardVisual(pending, incomingBoard), remaining);
}, false);

// Linkline polish v3 clear-only completion signal production build marker.
