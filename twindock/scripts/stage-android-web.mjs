import { cp, mkdir, readFile, rm } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';

const root = process.cwd();
const out = path.join(root, 'www');
const runtimeFiles = ['index.html', 'styles.css', 'transitions.css'];
const runtimeDir = 'src';

await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });

for (const file of runtimeFiles) {
  await cp(path.join(root, file), path.join(out, file));
}
await cp(path.join(root, runtimeDir), path.join(out, runtimeDir), { recursive: true });

const index = await readFile(path.join(out, 'index.html'), 'utf8');
const remoteRuntimeRef = /(?:src|href)=["']https?:\/\//i;
if (remoteRuntimeRef.test(index)) {
  throw new Error('Android parity package must not contain remote runtime asset references.');
}

const geometryAt = index.indexOf('./src/geometry.js');
const craftGeometryAt = index.indexOf('./src/craft-geometry.js');
const stateAt = index.indexOf('./src/state.js');
const missionAt = index.indexOf('./src/mission.js');
if (!(geometryAt >= 0 && craftGeometryAt > geometryAt && stateAt > craftGeometryAt && missionAt > stateAt)) {
  throw new Error('Required geometry -> craft-geometry -> state -> mission script order is not preserved.');
}

const rendererAt = index.indexOf('./src/renderer.js');
const craftProbeAt = index.indexOf('./src/craft-probe.js');
const presentationAt = index.indexOf('./src/presentation.js');
const mainAt = index.indexOf('./src/main.js');
if (!(rendererAt >= 0 && presentationAt > rendererAt && mainAt > presentationAt)) {
  throw new Error('Required renderer -> presentation -> main script order is not preserved.');
}
if (craftProbeAt >= 0 && !(craftProbeAt > rendererAt && craftProbeAt < presentationAt)) {
  throw new Error('Craft probe adapter must load between renderer and presentation.');
}

console.log('Twin Dock Android web staging complete:', out);
