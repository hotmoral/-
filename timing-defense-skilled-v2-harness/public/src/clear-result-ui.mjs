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
  const result = document.createElement('div');
  result.className = 'performance-result';
  result.setAttribute('aria-label', '클리어 성적');

  if (snapshot.grade && STAMP_ASSETS[snapshot.grade]) {
    const rank = document.createElement('div');
    rank.className = 'performance-rank';
    const image = document.createElement('img');
    image.className = 'performance-stamp';
    image.src = STAMP_ASSETS[snapshot.grade];
    image.alt = `${snapshot.grade} 등급`;
    rank.append(image);
    result.append(rank);
  }

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

function decorateClearResult() {
  if (!pendingSnapshot || typeof document === 'undefined') return;
  const screen = document.querySelector('#screen');
  const success = screen?.querySelector('.success-panel');
  if (!success || success.querySelector('.performance-result')) return;

  const actions = success.querySelector('.success-actions');
  const result = createPerformanceResult(pendingSnapshot);
  if (actions) success.insertBefore(result, actions);
  else success.append(result);
}

function installStyles() {
  if (document.querySelector('#performance-stamp-styles')) return;
  const style = document.createElement('style');
  style.id = 'performance-stamp-styles';
  style.textContent = `
.performance-result{width:min(100%,410px);margin:4px auto 2px;display:grid;justify-items:center;gap:18px}
.performance-rank{position:relative;width:92px;height:92px;display:grid;place-items:center;isolation:isolate}
.performance-rank::before,.performance-rank::after{content:"";position:absolute;border-radius:50%;pointer-events:none;z-index:-1}
.performance-rank::before{inset:-8px;border:1px solid rgba(18,104,255,.16);box-shadow:0 0 0 7px rgba(18,104,255,.025)}
.performance-rank::after{inset:-15px;border:1px dashed rgba(70,67,61,.16);transform:rotate(-12deg)}
.performance-stamp{width:100%;height:100%;object-fit:contain;display:block;filter:drop-shadow(0 5px 9px rgba(42,35,24,.10))}
.performance-stats{width:100%;min-height:86px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));align-items:stretch;padding:9px 6px;border:1px solid rgba(23,23,22,.13);border-radius:20px;background:rgba(255,253,248,.82);box-shadow:0 10px 32px rgba(42,35,24,.045)}
.performance-stat{position:relative;display:grid;justify-items:center;align-content:center;gap:1px;min-width:0;padding:0 7px;font-variant-numeric:tabular-nums}
.performance-stat+.performance-stat::before{content:"";position:absolute;left:0;top:13%;bottom:13%;width:1px;background:rgba(23,23,22,.14)}
.performance-stat-label{min-height:16px;display:flex;align-items:center;justify-content:center;gap:4px;color:#77736d;font-size:9px;font-weight:620;letter-spacing:.10em;white-space:nowrap}
.performance-crown{width:13px;height:13px;flex:0 0 13px;fill:none;stroke:var(--blue);stroke-width:1.75;stroke-linecap:round;stroke-linejoin:round}
.performance-stat-value{color:var(--ink);font-family:"Helvetica Neue",Arial,system-ui,sans-serif;font-size:29px;line-height:.98;font-weight:470;letter-spacing:-.035em}
.performance-stat.current .performance-stat-value{color:var(--blue)}
.performance-stat-unit{color:#8f8b84;font-size:7px;font-weight:620;letter-spacing:.18em}
.screen.polish-success .performance-result{animation:performanceResultReveal .24s .09s ease-out both}
@keyframes performanceResultReveal{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:370px){.performance-result{gap:14px}.performance-rank{width:80px;height:80px}.performance-stats{min-height:80px;padding-left:3px;padding-right:3px}.performance-stat{padding:0 4px}.performance-stat-label{font-size:8px;letter-spacing:.06em}.performance-stat-value{font-size:26px}}
@media(max-height:680px){.performance-result{gap:10px;margin-top:1px}.performance-rank{width:68px;height:68px}.performance-rank::before{inset:-5px}.performance-rank::after{inset:-10px}.performance-stats{min-height:70px;padding-top:6px;padding-bottom:6px}.performance-stat-label{font-size:8px}.performance-stat-value{font-size:24px}.performance-stat-unit{font-size:6.5px}}
@media(prefers-reduced-motion:reduce){.screen.polish-success .performance-result{animation:none}}
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
