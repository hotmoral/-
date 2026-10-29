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

// Linkline public Preview visual entry v6.1: exact Private canonical source is assembled from transparent parts, Git-blob verified, then executed.
