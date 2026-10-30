import './settings-preferences.mjs';
import './settings-about.mjs';
import './visual-assets-v61-core.mjs';

const weightStyle = document.createElement('style');
weightStyle.dataset.linklineVisualWeight = 'v6.1';
weightStyle.textContent = `
.visual-chain-body,.slide-chain-body{stroke-width:5.70!important}
`;
document.head.append(weightStyle);

const HANDOFF_SYNC_MS = 90;
const handoffSyncStyle = document.createElement('style');
handoffSyncStyle.dataset.linklineHandoffSync = 'v1';
handoffSyncStyle.textContent = `
.linkline-meta-snapshot,.linkline-exit-snapshot{position:fixed;pointer-events:none;margin:0;will-change:opacity,transform}
.linkline-meta-snapshot{z-index:980;transition:opacity .12s ease,transform .14s ease}
.linkline-meta-snapshot.is-leaving{opacity:0;transform:translateY(-2px)}
.linkline-exit-snapshot{z-index:940;transition:opacity .12s ease,transform .14s ease}
.linkline-exit-snapshot.is-leaving{opacity:0;transform:translateY(-3px) scale(.995)}
.linkline-board-ghost.linkline-clear-exit-now .performance-result{opacity:0;transform:scale(.985);transition:opacity .09s ease,transform .11s cubic-bezier(.22,.72,.22,1)}
`;
document.head.append(handoffSyncStyle);

let handoffSyncToken = 0;

function fixedSnapshot(node, className) {
  if (!node) return null;
  const rect = node.getBoundingClientRect();
  const clone = node.cloneNode(true);
  clone.classList.add(className);
  clone.setAttribute('aria-hidden', 'true');
  Object.assign(clone.style, {
    left: `${rect.left}px`,
    top: `${rect.top}px`,
    width: `${rect.width}px`,
    height: `${rect.height}px`,
  });
  document.body.append(clone);
  return clone;
}

function removeSnapshots(nodes) {
  nodes.forEach((node) => node?.remove());
}

document.addEventListener('click', (event) => {
  const next = event.target.closest?.('.success-actions .primary');
  if (!next || !next.textContent?.includes('NEXT STAGE')) return;

  const token = ++handoffSyncToken;
  const stageLabel = document.querySelector('#stage-label');
  const campaignLabel = document.querySelector('#campaign-label');
  const metaSnapshots = [
    fixedSnapshot(stageLabel, 'linkline-meta-snapshot'),
    fixedSnapshot(campaignLabel, 'linkline-meta-snapshot'),
  ].filter(Boolean);
  const exitSnapshots = [
    fixedSnapshot(document.querySelector('#screen .performance-retry-wrap'), 'linkline-exit-snapshot'),
    fixedSnapshot(document.querySelector('#screen .success-panel'), 'linkline-exit-snapshot'),
  ].filter(Boolean);

  if (stageLabel) stageLabel.style.visibility = 'hidden';
  if (campaignLabel) campaignLabel.style.visibility = 'hidden';

  requestAnimationFrame(() => {
    if (token !== handoffSyncToken) return;
    exitSnapshots.forEach((node) => node.classList.add('is-leaving'));
  });

  queueMicrotask(() => {
    if (token !== handoffSyncToken) return;
    document.querySelectorAll('.linkline-board-ghost').forEach((node) => node.classList.add('linkline-clear-exit-now'));
  });

  setTimeout(() => {
    if (token !== handoffSyncToken) return;
    metaSnapshots.forEach((node) => node.classList.add('is-leaving'));
    if (stageLabel) stageLabel.style.visibility = '';
    if (campaignLabel) campaignLabel.style.visibility = '';
    setTimeout(() => {
      if (token !== handoffSyncToken) return;
      removeSnapshots(metaSnapshots);
      removeSnapshots(exitSnapshots);
    }, 180);
  }, HANDOFF_SYNC_MS);
}, true);

// Linkline visual asset entry v6.1: persistent shared-intent drag layer with direct pointer geometry and 5.70 chain body stroke.
