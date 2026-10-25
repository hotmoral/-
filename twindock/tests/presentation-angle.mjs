import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..');
const context={window:{TwinDock:{Renderer:()=>({resize(){},makeStars(){},draw(){}})}}};
vm.createContext(context);
for(const file of ['math.js','presentation.js']){
  vm.runInContext(fs.readFileSync(path.join(root,'src',file),'utf8'),context,{filename:file});
}
const unwrap=context.window.TwinDock.Presentation.unwrapAngle;
let visual=3.10,prev=3.10;
for(const current of [3.12,3.14,-3.13,-3.10,-3.00]){
  const next=unwrap(visual,prev,current);
  assert.ok(Math.abs(next-visual)<0.2,'visual angle must remain continuous across wrap');
  visual=next;prev=current;
}
assert.ok(visual>Math.PI,'continuous visual angle should unwrap past +pi rather than jump negative');
console.log('Twin Dock presentation angle test: PASS');
