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
const { normAngle }=TD.MathUtil;
const EPS=1e-9;
const expected=['REFERENCE','CARGO_RECT_SIDE','SHUTTLE_TRAPEZOID_FRONT','TUG_TRAPEZOID_CORNER','CARGO_RECT_FRONT'];
const classes=['FRONT','SIDE','FRONT','CORNER','FRONT'];
assert.deepEqual(Array.from(TD.Mission.profiles,p=>p.setupId),expected);
for(let i=1;i<classes.length;i++) assert.notEqual(classes[i]==='FRONT',classes[i-1]==='FRONT','adjacent stages must alternate front vs non-front anchor class');

const sequence=TD.createState();sequence.viewport.W=1000;sequence.viewport.H=600;sequence.ship.x=120;sequence.ship.y=280;sequence.ship.angle=.27;
let profile=TD.Mission.reset(sequence);assert.equal(sequence.ship.geometryId,expected[0]);
for(let i=1;i<expected.length;i++){
  profile=TD.Mission.advance(sequence);
  assert.equal(profile,TD.Mission.profiles[i]);
  assert.equal(sequence.ship.geometryId,expected[i]);
  assert.equal(sequence.ship.anchorClass,classes[i]);
}

for(let i=0;i<TD.Mission.profiles.length;i++){
  const s=TD.createState();
  s.viewport.W=1000;s.viewport.H=600;s.ship.x=130;s.ship.y=310;s.ship.angle=.37;s.mission.index=i;
  TD.Mission.placeCurrent(s);
  const target=TD.Geometry.stationDockAnchor(s);
  const expectedSetup=TD.CraftGeometry.get(expected[i]);
  assert.equal(s.ship.geometryId,expectedSetup.id);
  assert.equal(s.ship.dockAnchor.x,expectedSetup.x);
  assert.equal(s.ship.dockAnchor.y,expectedSetup.y);
  assert.equal(s.ship.dockAnchor.angle,expectedSetup.angle);
  assert.ok(Math.abs(normAngle(target.angle-(s.ship.angle+s.ship.dockAnchor.angle)))<EPS);

  const pose=TD.Geometry.bodyPoseForWorldAnchor(target.x,target.y,target.angle,s.ship.dockAnchor);
  s.ship.x=pose.x;s.ship.y=pose.y;s.ship.angle=pose.angle;
  s.ship.vx=target.vx;s.ship.vy=target.vy;s.ship.angVel=s.station.omega;
  const m=TD.Docking.metrics(s);
  assert.ok(m.dist<EPS,`stage ${i+1} dist`);
  assert.ok(m.rel<EPS,`stage ${i+1} rel`);
  assert.ok(m.dir<EPS,`stage ${i+1} dir`);
  assert.ok(m.spin<EPS,`stage ${i+1} spin`);
  assert.equal(TD.Docking.canDock(m),true,`stage ${i+1} canDock`);
}

console.log('Twin Dock alternating anchor-class mission probe tests: PASS');
