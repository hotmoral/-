const V61_CORE_GIT_BLOB_SHA = '4b67aa8f6316bab513f23797e7a970f33f6e449f';
const V61_CORE_PARTS = [
  './visual-assets-v6-core.part01.txt',
  './visual-assets-v6-core.part02.txt',
  './visual-assets-v6-core.part03.txt',
  './visual-assets-v6-core.part04.txt',
  './visual-assets-v6-core.part05.txt',
  './visual-assets-v6-core.part06.txt',
  './visual-assets-v6-core.part07.txt',
  './visual-assets-v6-core.part08.txt',
];

const weightStyle = document.createElement('style');
weightStyle.dataset.linklineVisualWeight = 'v6.1';
weightStyle.textContent = `
.visual-chain-body,.slide-chain-body{stroke-width:5.70!important}
`;
document.head.append(weightStyle);

const sourceParts = await Promise.all(V61_CORE_PARTS.map(async (relativePath) => {
  const response = await fetch(new URL(relativePath, import.meta.url), { cache: 'no-store' });
  if (!response.ok) throw new Error(`V61_CORE_PART_HTTP:${response.status}:${relativePath}`);
  return response.text();
}));
const source = sourceParts.join('');
const sourceBytes = new TextEncoder().encode(source);
const headerBytes = new TextEncoder().encode(`blob ${sourceBytes.length}\0`);
const gitObjectBytes = new Uint8Array(headerBytes.length + sourceBytes.length);
gitObjectBytes.set(headerBytes, 0);
gitObjectBytes.set(sourceBytes, headerBytes.length);
const digest = await crypto.subtle.digest('SHA-1', gitObjectBytes);
const gitBlobSha = [...new Uint8Array(digest)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
if (gitBlobSha !== V61_CORE_GIT_BLOB_SHA) throw new Error(`V61_CORE_SHA:${gitBlobSha}`);

const moduleUrl = URL.createObjectURL(new Blob([source], { type: 'text/javascript' }));
try {
  await import(moduleUrl);
} finally {
  URL.revokeObjectURL(moduleUrl);
}

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

// Linkline public Preview visual entry v6.1: exact Private canonical source is assembled from transparent parts, Git-blob verified, then executed.
