import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..');
const context={window:{TwinDock:{}},performance:{now:()=>0},console};
vm.createContext(context);
for(const file of ['config.js','math.js','geometry.js','state.js','docking.js','mission.js']){
  vm.runInContext(fs.readFileSync(path.join(root,'src',file),'utf8'),context,{filename:file});
}
const TD=context.window.TwinDock;
assert.equal(TD.Config.FORCE_SCALE,58);
assert.equal(TD.Config.INPUT_DEADZONE,0.10);
assert.equal(TD.Config.INPUT_EXPONENT,2.05);
assert.equal(TD.Config.MAX_SPEED,78);
assert.equal(TD.Config.MAX_ANGULAR_SPEED,0.90);
assert.deepEqual(Array.from(TD.Mission.profiles,p=>p.id),['STATIC','TRANSLATE','ROTATE','COMBINED','FINAL']);
const s=TD.createState();s.viewport.W=1000;s.viewport.H=600;s.ship.x=100;s.ship.y=300;s.ship.angle=0;
let p=TD.Mission.reset(s);assert.equal(p.id,'STATIC');assert.equal(s.station.omega,0);assert.equal(s.station.vx,0);assert.equal(s.station.vy,0);assert.equal(s.station.dockAnchor.tracksRadius,true);assert.equal(s.station.dockAnchor.x,s.station.radius-TD.Config.PORT_CAPTURE_INSET);
p=TD.Mission.advance(s);assert.equal(p.id,'TRANSLATE');assert.equal(s.station.omega,0);assert.ok(Math.hypot(s.station.vx,s.station.vy)>0);
p=TD.Mission.advance(s);assert.equal(p.id,'ROTATE');assert.notEqual(s.station.omega,0);assert.equal(Math.hypot(s.station.vx,s.station.vy),0);
p=TD.Mission.advance(s);assert.equal(p.id,'COMBINED');assert.notEqual(s.station.omega,0);assert.ok(Math.hypot(s.station.vx,s.station.vy)>0);
p=TD.Mission.advance(s);assert.equal(p.id,'FINAL');assert.equal(s.station.omega,0.18);assert.ok(Math.hypot(s.station.vx,s.station.vy)>0);
assert.equal(TD.Mission.advance(s),null);assert.equal(s.mission.finished,true);
s.mission.finished=false;s.mission.index=1;TD.Mission.placeCurrent(s);const port=TD.Docking.portState(s);assert.ok(Math.abs(port.pvx)>0 || Math.abs(port.pvy)>0);
const anchor=TD.Geometry.stationDockAnchor(s);assert.ok(Math.abs(anchor.vx)>0 || Math.abs(anchor.vy)>0);
console.log('Twin Dock mission tests: PASS');
