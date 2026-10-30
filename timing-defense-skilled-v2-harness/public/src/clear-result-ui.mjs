const CLEAR_RESULT_EVENT = 'linkline:clear-result-v1';
const STAMP_ASSETS = Object.freeze({
  'S+': './assets/performance-stamps/s-plus.png',
  'A+': './assets/performance-stamps/a-plus.png',
  'B+': './assets/performance-stamps/b-plus.png',
});

let pendingSnapshot = null;

function crownIcon() {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 24 24');
  svg.setAttribute('aria-hidden', 'true');
  svg.classList.add('performance-crown');
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', 'M3.4 7.4 7.7 11l4.2-6 4.4 6 4.3-3.6-1.6 9.2H5zM5.4 19h13.2');
  svg.append(path);
  return svg;
}

function stat(label, value, className = '') {
  const item = document.createElement('div');
  item.className = `performance-stat ${className}`.trim();

  const heading = document.createElement('div');
  heading.className = 'performance-stat-label';
  if (className.includes('best')) heading.append(crownIcon());
  heading.append(document.createTextNode(label));

  const number = document.createElement('div');
  number.className = 'performance-stat-value';
  number.textContent = Number.isInteger(value) ? String(value) : '—';

  const unit = document.createElement('div');
  unit.className = 'performance-stat-unit';
  unit.textContent = 'MOVES';

  item.append(heading, number, unit);
  return item;
}

function createPerformanceResult(snapshot) {
  const result = document.createElement('section');
  result.className = 'performance-result';
  result.setAttribute('aria-label', '클리어 성적');

  const title = document.createElement('div');
  title.className = 'performance-frame-title';
  title.append(
    document.createTextNode('STAGE '),
    Object.assign(document.createElement('strong'), { textContent: 'CLEAR' }),
  );
  result.append(title);

  const center = document.createElement('div');
  center.className = 'performance-frame-center';
  if (snapshot.grade && STAMP_ASSETS[snapshot.grade]) {
    const rank = document.createElement('div');
    rank.className = 'performance-rank';
    const image = document.createElement('img');
    image.className = 'performance-stamp';
    image.src = STAMP_ASSETS[snapshot.grade];
    image.alt = `${snapshot.grade} 등급`;
    rank.append(image);
    center.append(rank);
  }
  result.append(center);

  const stats = document.createElement('div');
  stats.className = 'performance-stats';
  stats.append(
    stat('목표', snapshot.shortestDistance),
    stat('이번 기록', snapshot.moves, 'current'),
    stat('최고 기록', snapshot.bestMoves, 'best'),
  );
  result.append(stats);
  return result;
}

function retryCurrentStage(position) {
  const screen = document.querySelector('#screen');
  if (!screen || !Number.isInteger(position)) return;

  const stagesButton = [...screen.querySelectorAll('.play-nav button')]
    .find((node) => node.textContent?.trim() === 'STAGES');
  if (!stagesButton) return;

  stagesButton.click();
  const stageItems = [...document.querySelectorAll('#screen .stage-item')];
  const currentItem = stageItems.find((item) => {
    const label = item.querySelector('.stage-number')?.textContent?.trim();
    return Number(label) === position;
  });
  currentItem?.querySelector('.stage-node:not(:disabled)')?.click();
}

function createRetryControl(snapshot) {
  const wrap = document.createElement('div');
  wrap.className = 'performance-retry-wrap round-action-wrap';

  const retry = document.createElement('button');
  retry.type = 'button';
  retry.className = 'secondary round-action performance-retry';
  retry.setAttribute('aria-label', `Stage ${snapshot.position} 다시 도전`);
  retry.addEventListener('click', () => retryCurrentStage(snapshot.position));

  const label = document.createElement('span');
  label.className = 'round-action-label';
  label.textContent = 'RETRY';
  wrap.append(retry, label);
  return wrap;
}

function positionRetryControl(control, boardWrap, success) {
  requestAnimationFrame(() => {
    if (!control.isConnected || !boardWrap.isConnected || !success.isConnected) return;
    const boardBottom = boardWrap.offsetTop + boardWrap.offsetHeight;
    const successTop = success.offsetTop;
    const available = successTop - boardBottom;
    const top = boardBottom + Math.max(0, (available - control.offsetHeight) / 2);
    control.style.top = `${Math.round(top)}px`;
  });
}

function decorateClearResult() {
  if (!pendingSnapshot || typeof document === 'undefined') return;
  const screen = document.querySelector('#screen');
  const success = screen?.querySelector('.success-panel');
  const boardWrap = screen?.querySelector('.board-wrap');
  if (!success || !boardWrap) return;

  if (!boardWrap.querySelector('.performance-result')) {
    boardWrap.classList.add('performance-clear-active');
    boardWrap.append(createPerformanceResult(pendingSnapshot));
  }

  if (!screen.querySelector('.performance-retry-wrap')) {
    const retry = createRetryControl(pendingSnapshot);
    screen.append(retry);
    positionRetryControl(retry, boardWrap, success);
  }
}

function installStyles() {
  if (document.querySelector('#performance-stamp-styles')) return;
  const style = document.createElement('style');
  style.id = 'performance-stamp-styles';
  style.textContent = `
.screen.view-game{position:relative}
.board-wrap.performance-clear-active>.board,.board-wrap.performance-clear-active>.links{filter:blur(1.7px) brightness(.80) saturate(.82);opacity:.56;transform:scale(1.004);transition:filter .22s ease,opacity .22s ease,transform .22s ease}
.performance-result{position:absolute;inset:0;z-index:8;display:grid;grid-template-rows:auto minmax(0,1fr) auto;align-items:center;justify-items:center;padding:7.5% 6.5% 6.5%;overflow:hidden;border-radius:inherit;pointer-events:none;background:radial-gradient(circle at 50% 45%,rgba(255,253,248,.76) 0 27%,rgba(255,253,248,.52) 48%,rgba(250,247,239,.34) 72%,rgba(18,104,255,.065) 100%);box-shadow:inset 0 0 0 1px rgba(255,255,255,.68),inset 0 0 34px rgba(18,104,255,.10)}
.performance-result::before{content:"";position:absolute;width:104%;aspect-ratio:1;left:-14%;top:-48%;border:2px solid rgba(18,104,255,.42);border-radius:50%;box-shadow:0 0 24px rgba(18,104,255,.08);transform:rotate(-8deg);opacity:.72}
.performance-result::after{content:"";position:absolute;width:58%;aspect-ratio:1;left:21%;top:19%;border:1px dashed rgba(70,67,61,.23);border-radius:50%;box-shadow:0 0 0 9px rgba(255,255,255,.30),0 0 0 11px rgba(18,104,255,.13);opacity:.86}
.performance-frame-title{position:relative;z-index:2;margin-top:1%;transform:translateY(10px);color:var(--ink);font-family:"Helvetica Neue",Arial,system-ui,sans-serif;font-size:clamp(18px,5.1vw,26px);font-weight:320;line-height:1;letter-spacing:.25em;white-space:nowrap;text-shadow:0 1px 0 rgba(255,255,255,.5)}
.performance-frame-title strong{font-weight:670;letter-spacing:.20em}
.performance-frame-center{position:relative;z-index:3;width:100%;height:100%;display:grid;place-items:center;min-height:0}
.performance-rank{position:relative;width:min(33%,136px);aspect-ratio:1;display:grid;place-items:center;overflow:visible;border-radius:50%;background:rgba(255,253,248,.62);box-shadow:0 0 0 1px rgba(255,255,255,.78),0 0 0 7px rgba(18,104,255,.05),0 9px 26px rgba(42,35,24,.05)}
.performance-rank::before{content:"";position:absolute;inset:-11%;border:1px solid rgba(18,104,255,.20);border-radius:50%}
.performance-stamp{width:94%;height:94%;max-width:none;max-height:none;object-fit:contain;object-position:center;display:block;overflow:visible;filter:drop-shadow(0 5px 8px rgba(42,35,24,.10))}
.performance-stats{position:relative;z-index:4;width:100%;min-height:82px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));align-items:stretch;padding:8px 6px;border:1px solid rgba(23,23,22,.17);border-radius:21px;background:rgba(255,253,248,.94);box-shadow:0 7px 22px rgba(42,35,24,.055),0 0 0 1px rgba(255,255,255,.7)}
.performance-stat{position:relative;display:grid;justify-items:center;align-content:center;gap:1px;min-width:0;padding:0 7px;font-variant-numeric:tabular-nums}
.performance-stat+.performance-stat::before{content:"";position:absolute;left:0;top:12%;bottom:12%;width:1px;background:rgba(23,23,22,.18)}
.performance-stat-label{min-height:16px;display:flex;align-items:center;justify-content:center;gap:4px;color:#696660;font-size:9px;font-weight:620;letter-spacing:.08em;white-space:nowrap}
.performance-crown{width:13px;height:13px;flex:0 0 13px;fill:none;stroke:var(--blue);stroke-width:1.75;stroke-linecap:round;stroke-linejoin:round}
.performance-stat-value{color:var(--ink);font-family:"Helvetica Neue",Arial,system-ui,sans-serif;font-size:29px;line-height:.98;font-weight:470;letter-spacing:-.035em}
.performance-stat.current .performance-stat-value{color:var(--blue)}
.performance-stat-unit{color:#8f8b84;font-size:7px;font-weight:620;letter-spacing:.18em}
.performance-retry-wrap{position:absolute;z-index:12;left:50%;transform:translateX(-50%);gap:5px;pointer-events:auto}
.performance-retry{width:54px;height:54px;min-width:54px;min-height:54px;line-height:1}
.performance-retry-wrap .round-action-label{font-size:8px;letter-spacing:.19em}
.screen.polish-success .performance-result{animation:performanceOverlayReveal .26s .06s ease-out both}
.screen.polish-success .performance-retry-wrap{animation:performanceRetryReveal .22s .16s ease-out both}
@keyframes performanceOverlayReveal{from{opacity:0;transform:scale(.992)}to{opacity:1;transform:scale(1)}}
@keyframes performanceRetryReveal{from{opacity:0;transform:translate(-50%,4px)}to{opacity:1;transform:translate(-50%,0)}}
@media(max-width:370px){.performance-result{padding:7% 5.5% 5.5%}.performance-frame-title{font-size:18px;transform:translateY(9px)}.performance-rank{width:min(31%,110px)}.performance-stats{min-height:76px;padding-left:3px;padding-right:3px}.performance-stat{padding:0 4px}.performance-stat-label{font-size:8px;letter-spacing:.05em}.performance-stat-value{font-size:26px}.performance-retry{width:50px;height:50px;min-width:50px;min-height:50px}}
@media(max-height:680px){.performance-result{padding:6% 5.5% 5%}.performance-frame-title{font-size:16px;transform:translateY(7px)}.performance-rank{width:min(29%,96px)}.performance-stats{min-height:66px;padding-top:5px;padding-bottom:5px}.performance-stat-label{font-size:8px}.performance-stat-value{font-size:23px}.performance-stat-unit{font-size:6.5px}.performance-retry{width:46px;height:46px;min-width:46px;min-height:46px}}
@media(prefers-reduced-motion:reduce){.screen.polish-success .performance-result,.screen.polish-success .performance-retry-wrap{animation:none}.board-wrap.performance-clear-active>.board,.board-wrap.performance-clear-active>.links{transition:none}}
`;
  document.head.append(style);
}

if (typeof document !== 'undefined') {
  installStyles();
  document.addEventListener(CLEAR_RESULT_EVENT, (event) => {
    pendingSnapshot = event.detail ?? null;
    queueMicrotask(decorateClearResult);
  });
  const screen = document.querySelector('#screen');
  if (screen && typeof MutationObserver !== 'undefined') {
    const observer = new MutationObserver(decorateClearResult);
    observer.observe(screen, { childList: true, subtree: true });
  }
}
