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
const ids=['CARGO_CTRL_SIDE_TOP','CARGO_CTRL_FRONT','CARGO_CTRL_SIDE_BOTTOM','CARGO_CTRL_REAR','CARGO_CTRL_CORNER'];
assert.deepEqual(Array.from(TD.Mission.profiles,p=>p.setupId),ids);

const setup=Object.fromEntries(ids.map(id=>[id,TD.CraftGeometry.get(id)]));
for(const id of ids){assert.equal(setup[id].craftId,'CARGO');assert.equal(setup[id].portShape,'RECT');}
const r=id=>Math.hypot(setup[id].x,setup[id].y);
assert.ok(Math.abs(r('CARGO_CTRL_SIDE_TOP')-61)<EPS);
assert.ok(Math.abs(r('CARGO_CTRL_SIDE_BOTTOM')-61)<EPS);
assert.ok(Math.abs(r('CARGO_CTRL_FRONT')-98)<EPS);
assert.ok(Math.abs(r('CARGO_CTRL_REAR')-98)<EPS);
assert.ok(Math.abs(r('CARGO_CTRL_CORNER')-98)<1e-6);
assert.equal(setup.CARGO_CTRL_FRONT.angle,0);
assert.equal(setup.CARGO_CTRL_REAR.angle,Math.PI);
assert.equal(setup.CARGO_CTRL_SIDE_TOP.angle,-Math.PI/2);
assert.equal(setup.CARGO_CTRL_SIDE_BOTTOM.angle,Math.PI/2);
assert.equal(setup.CARGO_CTRL_CORNER.angle,Math.PI/4);

const motion=TD.Mission.profiles[0];
for(const p of TD.Mission.profiles){
  for(const key of ['ahead','lateral','bodyVx','bodyVy','omega']) assert.equal(p[key],motion[key],`${key} must remain controlled`);
}

for(let i=0;i<TD.Mission.profiles.length;i++){
  const s=TD.createState();
  s.viewport.W=1000;s.viewport.H=600;s.ship.x=137;s.ship.y=289;s.ship.angle=.37;s.mission.index=i;
  const before={x:s.ship.x,y:s.ship.y,angle:s.ship.angle,length:s.ship.length,width:s.ship.width};
  TD.Mission.placeCurrent(s);
  assert.equal(s.ship.x,before.x,'craft geometry must not move rotation center x');
  assert.equal(s.ship.y,before.y,'craft geometry must not move rotation center y');
  assert.equal(s.ship.angle,before.angle,'craft geometry must not rotate body as a setup side effect');
  assert.equal(s.ship.length,before.length,'visual geometry must not alter accepted torque lever');
  assert.equal(s.ship.width,before.width,'visual geometry must not alter accepted physical width');
  assert.equal(s.ship.craftId,'CARGO');assert.equal(s.ship.portShape,'RECT');
  const target=TD.Geometry.stationDockAnchor(s);
  assert.ok(Math.abs(normAngle(target.angle-(s.ship.angle+s.ship.dockAnchor.angle)))<EPS);
  const pose=TD.Geometry.bodyPoseForWorldAnchor(target.x,target.y,target.angle,s.ship.dockAnchor);
  s.ship.x=pose.x;s.ship.y=pose.y;s.ship.angle=pose.angle;s.ship.vx=target.vx;s.ship.vy=target.vy;s.ship.angVel=s.station.omega;
  const m=TD.Docking.metrics(s);
  assert.ok(m.dist<EPS,`stage ${i+1} dist`);assert.ok(m.rel<EPS,`stage ${i+1} rel`);assert.ok(m.dir<EPS,`stage ${i+1} dir`);assert.ok(m.spin<EPS,`stage ${i+1} spin`);assert.equal(TD.Docking.canDock(m),true,`stage ${i+1} canDock`);
}

console.log('Twin Dock anchor eccentricity controlled probe tests: PASS');
