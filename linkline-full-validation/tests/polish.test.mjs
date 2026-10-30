import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const indexHtml = await readFile(new URL('../index.html', import.meta.url), 'utf8');
const polishCss = await readFile(new URL('../polish.css', import.meta.url), 'utf8');
const polishJs = await readFile(new URL('../src/polish.mjs', import.meta.url), 'utf8');

for (const marker of [
  'class="is-booting"',
  'id="boot-splash"',
  './polish.css',
  './src/polish.mjs',
  'CONNECTING SIGNAL',
]) assert.ok(indexHtml.includes(marker), `missing boot marker: ${marker}`);

for (const marker of [
  'BOOT_MIN_MS = 220',
  'HANDOFF_SWAP_MS = 90',
  'HANDOFF_CLEANUP_MS = 340',
  'MutationObserver',
  'decorateSolvedBoard',
  'decorateStageSelect',
  'createHandoffGhost',
  'prepareIncomingScene',
  'playCompletionSignal',
  'playClearCelebration',
  'CLEAR_CELEBRATION_MS = 760',
  'CLEAR_SPARK_COUNT = 12',
  'clear-celebration',
  'clear-impact',
  'linklineClearRing',
  'linklineClearSpark',
  'navigator?.vibrate?.([20, 26, 36])',
  'linkline-forwarding',
  'completion-pulse',
  'linkline-board-ghost',
  'linkline-incoming-board',
  'stage-node-arrival',
  'prefers-reduced-motion: reduce',
  'STAGE_SWIPE_MIN_PX = 48',
  'STAGE_SWIPE_AXIS_RATIO = 1.2',
  'stageSwipeDirection',
  'touchstart',
  'touchend',
  "touch-action', 'pan-y",
  '.stage-pager .pager-button',
]) assert.ok(polishJs.includes(marker) || polishCss.includes(marker), `missing polish marker: ${marker}`);

assert.ok(!polishJs.includes('TRANSITION_OUT_MS = 140'), 'transition timing must not collide with v0.4 140ms shim');
assert.ok(!polishJs.includes('document.startViewTransition'), 'next-stage polish must not depend on browser View Transition behavior');
assert.ok(!polishJs.includes("clonePathPulse(ghost, 'handoff-pulse')"), 'old and new board line sweeps must not overlap');
assert.ok(!polishJs.includes('next.click()'), 'NEXT STAGE must use the trusted native button handler, not a synthetic click replay');
assert.ok(!polishJs.includes('replayNext'), 'synthetic NEXT replay path must stay removed');
assert.ok(polishJs.includes('The trusted NEXT STAGE click is never prevented'), 'native click contract must stay documented in code');
assert.ok(!polishJs.includes('getTotalLength'), 'NEXT signal must not use a separate full-path drawing mechanism');
assert.ok(!polishJs.includes('path.animate'), 'NEXT signal must not use a separate Web Animations sweep');
assert.equal((polishJs.match(/playCompletionSignal\(/g) || []).length, 2, 'completion signal must exist only as helper plus clear-state call');
assert.equal((polishJs.match(/playClearCelebration\(/g) || []).length, 2, 'clear celebration must exist only as helper plus clear-state call');
assert.ok(polishJs.includes("return clonePathPulse(board, 'completion-pulse')"), 'clear signal helper must use completion-pulse');
assert.ok(polishJs.includes('playCompletionSignal(board);'), 'clear state must play the completion signal');
assert.ok(polishJs.includes('playClearCelebration(board);'), 'clear state must play the stronger celebration');
assert.ok(!polishJs.includes('playCompletionSignal(incomingBoard)'), 'NEXT STAGE must not replay the blue chain signal');
assert.ok(!polishJs.includes('playClearCelebration(incomingBoard)'), 'NEXT STAGE must not replay the clear celebration');
assert.ok(!polishJs.includes('const pulse = playCompletionSignal'), 'NEXT STAGE must not allocate an arrival completion pulse');
assert.ok(polishJs.includes(".completion-pulse, .handoff-pulse, .arrival-pulse, .clear-celebration"), 'handoff ghost must exclude transient clear celebration');
assert.ok(polishJs.includes("ghost.classList.remove('polish-solved', 'clear-impact'"), 'handoff ghost must exclude clear-impact state');
assert.ok(polishJs.includes('pagerButton.click();'), 'stage-select swipe must reuse the existing pager button handler');
assert.ok(polishJs.includes('horizontal <= vertical * STAGE_SWIPE_AXIS_RATIO'), 'stage-select swipe must reject vertical-dominant gestures');
assert.ok(polishCss.includes('.completion-pulse path'));
assert.ok(polishCss.includes('stroke-dasharray: 14 120'));
assert.ok(polishCss.includes('animation: pathConfirm .46s cubic-bezier(.2,.7,.2,1) both'));
assert.ok(!polishCss.includes('::view-transition-old('), 'root or board snapshot transitions must stay removed');
assert.ok(polishCss.includes('.screen.polish-success .success-actions'));
assert.ok(polishCss.includes('@keyframes linklineGhostLeave'));
assert.ok(polishCss.includes('.polish-stage-select .stage-node.locked'));
assert.ok(polishCss.includes('.polish-stage-select .stage-node.completed-current'));
assert.ok(polishCss.includes('@media (max-height: 760px)'));
assert.ok(polishCss.includes('@media (max-height: 620px)'));
assert.ok(polishCss.includes('@media (min-height: 900px)'));

console.log('PASS polish v4 clear-impact celebration + stage-select swipe: native NEXT retained; celebration stays clear-only');
