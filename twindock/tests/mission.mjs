import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..');
const context={window:{TwinDock:{}},performance:{now:()=>0},console};
vm.createContext(context);
for(const file of ['config.js','math.js','geometry.js','craft-geometry.js','state.js','docking.js','mission.js']){
  vm.runInContext(fs.readFileSync(path.join(root,'src',file),'utf8'),context,{filename:file});
}
const TD=context.window.TwinDock;
assert.equal(TD.Config.FORCE_SCALE,58);
assert.equal(TD.Config.INPUT_DEADZONE,0.10);
assert.equal(TD.Config.INPUT_EXPONENT,2.05);
assert.equal(TD.Config.MAX_SPEED,78);
assert.equal(TD.Config.MAX_ANGULAR_SPEED,0.90);
assert.deepEqual(Array.from(TD.Mission.profiles,p=>p.id),['SIDE_TOP','FRONT','SIDE_BOTTOM','REAR','CORNER']);
assert.deepEqual(Array.from(TD.Mission.profiles,p=>p.setupId),['CARGO_CTRL_SIDE_TOP','CARGO_CTRL_FRONT','CARGO_CTRL_SIDE_BOTTOM','CARGO_CTRL_REAR','CARGO_CTRL_CORNER']);
const first=TD.Mission.profiles[0];
for(const p of TD.Mission.profiles){
  assert.equal(p.ahead,first.ahead);assert.equal(p.lateral,first.lateral);assert.equal(p.bodyVx,first.bodyVx);assert.equal(p.bodyVy,first.bodyVy);assert.equal(p.omega,first.omega);
}
const s=TD.createState();s.viewport.W=1000;s.viewport.H=600;s.ship.x=100;s.ship.y=300;s.ship.angle=.23;
for(let i=0;i<TD.Mission.profiles.length;i++){
  s.mission.index=i;const p=TD.Mission.placeCurrent(s);
  assert.equal(s.ship.craftId,'CARGO');assert.equal(s.ship.portShape,'RECT');
  assert.equal(s.station.omega,-0.14);assert.ok(Math.hypot(s.station.vx,s.station.vy)>0);
  assert.equal(p.setupId,TD.Mission.profiles[i].setupId);
  assert.equal(s.station.dockAnchor.tracksRadius,true);assert.equal(s.station.dockAnchor.x,s.station.radius-TD.Config.PORT_CAPTURE_INSET);
}
s.mission.index=0;s.mission.finished=false;
let p=TD.Mission.reset(s);assert.equal(p.id,'SIDE_TOP');
for(let i=1;i<TD.Mission.profiles.length;i++){p=TD.Mission.advance(s);assert.equal(p,TD.Mission.profiles[i]);}
assert.equal(TD.Mission.advance(s),null);assert.equal(s.mission.finished,true);
s.mission.finished=false;s.mission.index=2;TD.Mission.placeCurrent(s);const port=TD.Docking.portState(s);assert.ok(Math.abs(port.pvx)>0 || Math.abs(port.pvy)>0);
const anchor=TD.Geometry.stationDockAnchor(s);assert.ok(Math.abs(anchor.vx)>0 || Math.abs(anchor.vy)>0);
console.log('Twin Dock controlled-anchor mission tests: PASS');
