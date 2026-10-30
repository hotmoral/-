import './visual-assets.mjs';

const body = document.body;
const screen = document.querySelector('#screen');
const splash = document.querySelector('#boot-splash');
const stageLabel = document.querySelector('#stage-label');
const campaignLabel = document.querySelector('#campaign-label');

const BOOT_MIN_MS = 220;
const HANDOFF_SWAP_MS = 90;
const HANDOFF_CLEANUP_MS = 340;
const META_CLEANUP_MS = 240;
const STAGE_SWIPE_MIN_PX = 48;
const STAGE_SWIPE_AXIS_RATIO = 1.2;
const STAGE_SWIPE_CLICK_SUPPRESS_MS = 350;
const CLEAR_CELEBRATION_MS = 760;
const CLEAR_SPARK_COUNT = 12;
const reducedMotion = globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches ?? false;
const bootStartedAt = performance.now();
let bootRevealScheduled = false;
let forwarding = false;
let pendingForward = null;
let stageSwipe = null;
let suppressStageMapClickUntil = 0;
let clearCelebrationTimer = null;
let activeClearCelebration = null;

const celebrationStyle = document.createElement('style');
celebrationStyle.textContent = `
.board-wrap.clear-impact{animation:linklineClearImpact .62s cubic-bezier(.16,.82,.2,1) both;overflow:visible}
.clear-celebration{position:absolute;inset:-2px;z-index:8;pointer-events:none;overflow:visible;border-radius:20px}
.clear-celebration::before{content:"";position:absolute;left:50%;top:50%;width:26%;aspect-ratio:1;border:3px solid rgba(18,104,255,.78);border-radius:50%;box-shadow:0 0 28px rgba(18,104,255,.32);transform:translate(-50%,-50%);animation:linklineClearRing .68s cubic-bezier(.12,.72,.18,1) both}
.clear-celebration::after{content:"";position:absolute;inset:-8%;border-radius:28px;background:radial-gradient(circle at 50% 50%,rgba(255,255,255,.90) 0 5%,rgba(18,104,255,.20) 17%,rgba(18,104,255,.07) 36%,transparent 62%);animation:linklineClearFlash .46s ease-out both}
.clear-spark{position:absolute;left:50%;top:50%;width:5px;height:20px;margin:-10px 0 0 -2.5px;border-radius:999px;background:var(--blue);box-shadow:0 0 10px rgba(18,104,255,.52);opacity:0;transform-origin:50% 50%;animation:linklineClearSpark .62s cubic-bezier(.12,.74,.18,1) both}
.screen.polish-success .success-kicker{animation:linklineClearKicker .42s .04s cubic-bezier(.16,.82,.2,1) both}
.screen.polish-success .success-title{animation:linklineClearTitle .46s .06s cubic-bezier(.16,.82,.2,1) both}
.screen.polish-success .success-actions{animation:successActionReveal .20s .08s cubic-bezier(.22,.72,.22,1) both;pointer-events:auto}
.linkline-board-ghost .performance-result{transition:opacity .18s ease,transform .22s cubic-bezier(.22,.72,.22,1)}
.linkline-board-ghost.is-leaving .performance-result{opacity:0;transform:scale(.985)}
.linkline-board-ghost.is-leaving{animation:linklineGhostLeaveSmooth .30s cubic-bezier(.22,.72,.22,1) both}
.board-wrap.linkline-incoming-board{opacity:0;transform:scale(.994);filter:blur(.35px);will-change:opacity,transform,filter}
.board-wrap.linkline-incoming-board.is-visible{opacity:1;transform:scale(1);filter:blur(0);transition:opacity .28s ease,transform .30s cubic-bezier(.18,.76,.22,1),filter .24s ease}
.linkline-incoming-ui{opacity:0;transform:translateY(4px);pointer-events:none;will-change:opacity,transform}
.linkline-incoming-ui.is-visible{opacity:1;transform:translateY(0);pointer-events:auto;transition:opacity .22s .04s ease,transform .26s .04s cubic-bezier(.18,.76,.22,1)}
.stage-node.performance-grade-ring{position:relative}
.stage-node.performance-grade-ring::after{content:"";position:absolute;inset:-4px;border:2px solid var(--performance-ring);border-radius:50%;pointer-events:none;box-shadow:0 1px 4px rgba(42,35,24,.08)}
.stage-node.performance-grade-s{--performance-ring:#c9a13b}
.stage-node.performance-grade-a{--performance-ring:#a7adb4}
.stage-node.performance-grade-b{--performance-ring:#b7794b}
@keyframes linklineClearImpact{0%{transform:scale(1);box-shadow:var(--shadow)}18%{transform:scale(.988);box-shadow:0 12px 38px rgba(18,104,255,.08)}46%{transform:scale(1.018);box-shadow:0 20px 62px rgba(18,104,255,.22)}100%{transform:scale(1);box-shadow:var(--shadow)}}
@keyframes linklineClearRing{0%{opacity:0;transform:translate(-50%,-50%) scale(.38)}16%{opacity:1}100%{opacity:0;transform:translate(-50%,-50%) scale(4.8)}}
@keyframes linklineClearFlash{0%{opacity:0;transform:scale(.92)}20%{opacity:1}100%{opacity:0;transform:scale(1.08)}}
@keyframes linklineClearSpark{0%{opacity:0;transform:translate(-50%,-50%) scale(.4) rotate(var(--rot))}16%{opacity:1}100%{opacity:0;transform:translate(-50%,-50%) translate(var(--dx),var(--dy)) scale(.18) rotate(var(--rot))}}
@keyframes linklineClearKicker{0%{opacity:0;transform:translateY(8px) scale(.92);letter-spacing:.08em}55%{opacity:1;transform:translateY(-2px) scale(1.08);letter-spacing:.19em}100%{opacity:1;transform:translateY(0) scale(1);letter-spacing:normal}}
@keyframes linklineClearTitle{0%{opacity:0;transform:translateY(10px) scale(.94)}52%{opacity:1;transform:translateY(-2px) scale(1.045)}100%{opacity:1;transform:translateY(0) scale(1)}}
@keyframes linklineGhostLeaveSmooth{0%{opacity:1;transform:scale(1);filter:blur(0)}100%{opacity:0;transform:scale(.992);filter:blur(.45px)}}
@media (prefers-reduced-motion:reduce){.board-wrap.clear-impact,.clear-celebration,.clear-spark,.screen.polish-success .success-kicker,.screen.polish-success .success-title{animation:none!important}}
`;
document.head.append(celebrationStyle);

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

function cleanupClearCelebration() {
  if (clearCelebrationTimer !== null) {
    clearTimeout(clearCelebrationTimer);
    clearCelebrationTimer = null;
  }
  activeClearCelebration?.burst?.remove();
  activeClearCelebration?.board?.classList.remove('clear-impact');
  activeClearCelebration = null;
  screen?.classList.remove('clear-celebrating');
}

function playClearCelebration(board) {
  cleanupClearCelebration();
  if (!board || reducedMotion) return;
  board.querySelector('.clear-celebration')?.remove();
  board.classList.remove('clear-impact');
  void board.offsetWidth;
  board.classList.add('clear-impact');
  screen?.classList.add('clear-celebrating');

  const burst = document.createElement('div');
  burst.className = 'clear-celebration';
  burst.setAttribute('aria-hidden', 'true');
  for (let index = 0; index < CLEAR_SPARK_COUNT; index++) {
    const angle = (Math.PI * 2 * index) / CLEAR_SPARK_COUNT;
    const distance = 86 + (index % 3) * 18;
    const spark = document.createElement('span');
    spark.className = 'clear-spark';
    spark.style.setProperty('--dx', `${Math.cos(angle) * distance}px`);
    spark.style.setProperty('--dy', `${Math.sin(angle) * distance}px`);
    spark.style.setProperty('--rot', `${(angle * 180) / Math.PI + 90}deg`);
    spark.style.animationDelay = `${(index % 2) * 28}ms`;
    burst.append(spark);
  }
  board.append(burst);
  activeClearCelebration = { board, burst };

  if (document.visibilityState !== 'hidden') {
    try { globalThis.navigator?.vibrate?.([20, 26, 36]); } catch {}
  }

  clearCelebrationTimer = setTimeout(cleanupClearCelebration, CLEAR_CELEBRATION_MS);
}

function decorateSolvedBoard() {
  if (!screen?.querySelector('.success-panel')) return;
  const board = screen.querySelector('.board-wrap');
  if (!board || board.classList.contains('polish-solved')) return;
  screen.classList.add('polish-success');
  board.classList.add('polish-solved');
  playCompletionSignal(board);
  playClearCelebration(board);
}

function stagePerformanceRecords() {
  try {
    const raw = JSON.parse(globalThis.localStorage?.getItem('linkline.product.progress.v3') || 'null');
    if (!raw || raw.schema !== 'LINKLINE_PRODUCT_PROGRESS' || raw.version !== 3) return {};
    return raw.performance && typeof raw.performance === 'object' ? raw.performance : {};
  } catch {
    return {};
  }
}

function decorateStageGradeRings() {
  const records = stagePerformanceRecords();
  for (const item of screen?.querySelectorAll('.stage-item') || []) {
    const position = item.querySelector('.stage-number')?.textContent?.trim();
    const node = item.querySelector('.stage-node');
    const grade = records?.[position]?.grade;
    if (!node || !['S+', 'A+', 'B+'].includes(grade)) continue;
    node.classList.add('performance-grade-ring');
    node.classList.add(grade === 'S+' ? 'performance-grade-s' : grade === 'A+' ? 'performance-grade-a' : 'performance-grade-b');
    node.dataset.performanceGrade = grade;
    const label = node.getAttribute('aria-label') || `Stage ${position}`;
    if (!label.includes(`${grade} 등급`)) node.setAttribute('aria-label', `${label}, ${grade} 등급`);
  }
}

function decorateStageSelect() {
  if (!screen?.classList.contains('view-stages') || screen.classList.contains('polish-stage-select')) return;
  screen.classList.add('polish-stage-select');
  screen.querySelector('.stage-map')?.style.setProperty('touch-action', 'pan-y');
  decorateStageGradeRings();
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
  ghost.querySelectorAll('.completion-pulse, .handoff-pulse, .arrival-pulse, .clear-celebration').forEach((node) => node.remove());
  ghost.classList.remove('polish-solved', 'clear-impact', 'linkline-arrival', 'linkline-incoming-board', 'linkline-handoff-out');
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

function prepareIncomingScene() {
  const board = screen?.querySelector('.board-wrap');
  if (!board || screen?.querySelector('.success-panel')) return null;
  board.classList.add('linkline-incoming-board');
  const ui = [...screen.querySelectorAll('.play-hint, .round-action-wrap')];
  ui.forEach((node) => node.classList.add('linkline-incoming-ui'));
  return { board, ui };
}

function finishForwardVisual(pending, incoming) {
  if (!pending) return;
  const { ghost } = pending;
  if (!incoming?.board) {
    ghost?.remove();
    screen?.classList.remove('linkline-forwarding');
    revealMeta();
    forwarding = false;
    return;
  }

  incoming.board.classList.add('is-visible');
  incoming.ui.forEach((node) => node.classList.add('is-visible'));
  revealMeta();
  ghost?.classList.add('is-leaving');

  setTimeout(() => {
    ghost?.remove();
    screen?.classList.remove('linkline-forwarding');
    incoming.board.classList.remove('linkline-incoming-board', 'is-visible');
    incoming.ui.forEach((node) => node.classList.remove('linkline-incoming-ui', 'is-visible'));
    forwarding = false;
  }, HANDOFF_CLEANUP_MS);
}

function stageSwipeDirection(deltaX, deltaY) {
  const horizontal = Math.abs(deltaX);
  const vertical = Math.abs(deltaY);
  if (horizontal < STAGE_SWIPE_MIN_PX) return 0;
  if (horizontal <= vertical * STAGE_SWIPE_AXIS_RATIO) return 0;
  return deltaX < 0 ? 1 : -1;
}

function stagePagerButton(direction) {
  const buttons = screen?.querySelectorAll('.stage-pager .pager-button');
  if (!buttons?.length) return null;
  return direction < 0 ? buttons[0] : buttons[buttons.length - 1];
}

function resetStageSwipe() {
  stageSwipe = null;
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

document.addEventListener('touchstart', (event) => {
  if (!screen?.classList.contains('view-stages') || event.touches.length !== 1) {
    resetStageSwipe();
    return;
  }
  const map = event.target.closest?.('.stage-map');
  if (!map) {
    resetStageSwipe();
    return;
  }
  const touch = event.touches[0];
  stageSwipe = { map, x: touch.clientX, y: touch.clientY };
}, { passive: true });

document.addEventListener('touchend', (event) => {
  if (!stageSwipe || !screen?.classList.contains('view-stages') || event.changedTouches.length !== 1) {
    resetStageSwipe();
    return;
  }
  const touch = event.changedTouches[0];
  const direction = stageSwipeDirection(touch.clientX - stageSwipe.x, touch.clientY - stageSwipe.y);
  const map = stageSwipe.map;
  resetStageSwipe();
  if (!direction || !map.isConnected) return;

  const pagerButton = stagePagerButton(direction);
  if (!pagerButton || pagerButton.disabled) return;

  suppressStageMapClickUntil = performance.now() + STAGE_SWIPE_CLICK_SUPPRESS_MS;
  pagerButton.click();
}, { passive: true });

document.addEventListener('touchcancel', resetStageSwipe, { passive: true });

document.addEventListener('click', (event) => {
  if (performance.now() >= suppressStageMapClickUntil) return;
  if (!event.target.closest?.('.stage-map')) return;
  event.preventDefault();
  event.stopPropagation();
  event.stopImmediatePropagation();
}, true);

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

  cleanupClearCelebration();
  forwarding = true;
  screen.classList.add('linkline-forwarding');
  prepareMetaExit();
  pendingForward = {
    target: next,
    ghost: createHandoffGhost(),
    startedAt: performance.now(),
  };
}, true);

// This bubble listener runs after the button's native openStage handler. The next board and its
// lower play controls are hidden before paint, then crossfade together against the old board ghost.
document.addEventListener('click', (event) => {
  if (!pendingForward) return;
  const next = event.target.closest?.('.success-actions .primary');
  if (!next || next !== pendingForward.target) return;

  const pending = pendingForward;
  pendingForward = null;
  screen.classList.add('linkline-forwarding');
  const incoming = prepareIncomingScene();
  const elapsed = performance.now() - pending.startedAt;
  const remaining = Math.max(0, HANDOFF_SWAP_MS - elapsed);
  setTimeout(() => finishForwardVisual(pending, incoming), remaining);
}, false);

// Linkline polish v4.3 Stage Select grade rings + smoother NEXT crossfade + one-shot clear celebration + native NEXT + stage-select swipe.