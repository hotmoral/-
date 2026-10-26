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

const shuttle=TD.CraftGeometry.craft('SHUTTLE');
const cargo=TD.CraftGeometry.craft('CARGO');
const tug=TD.CraftGeometry.craft('TUG');
assert.ok(cargo.visualLength>shuttle.visualLength*2,'cargo must be dramatically longer than reference shuttle');
assert.ok(cargo.visualWidth>shuttle.visualWidth*2,'cargo must also read as a materially larger hull');
assert.ok(tug.visualWidth>shuttle.visualWidth*2,'tug must be dramatically wider than reference shuttle');
assert.equal(TD.CraftGeometry.port('CIRCLE').label,'원형');
assert.equal(TD.CraftGeometry.port('RECT').label,'직사각형');
assert.equal(TD.CraftGeometry.port('TRAPEZOID').label,'사다리꼴');

const reference=TD.CraftGeometry.get('REFERENCE');
const shuttleTrap=TD.CraftGeometry.get('SHUTTLE_TRAPEZOID_FRONT');
assert.equal(reference.craftId,shuttleTrap.craftId);
assert.equal(reference.x,shuttleTrap.x);assert.equal(reference.y,shuttleTrap.y);assert.equal(reference.angle,shuttleTrap.angle);
assert.notEqual(reference.portShape,shuttleTrap.portShape,'stage 1 vs 3 isolates port-shape semantics on the same shuttle anchor');

const cargoSide=TD.CraftGeometry.get('CARGO_RECT_SIDE');
const cargoFront=TD.CraftGeometry.get('CARGO_RECT_FRONT');
assert.equal(cargoSide.craftId,cargoFront.craftId);assert.equal(cargoSide.portShape,cargoFront.portShape);
assert.notEqual(cargoSide.anchorClass,cargoFront.anchorClass,'stage 2 vs 5 isolates cargo anchor location while keeping hull and port shape');
assert.ok(Math.hypot(cargoSide.x,cargoSide.y)>60);
const tugCorner=TD.CraftGeometry.get('TUG_TRAPEZOID_CORNER');
assert.ok(Math.hypot(tugCorner.x,tugCorner.y)>70,'corner anchor must be strongly eccentric');
assert.equal(tugCorner.anchorClass,'CORNER');

for(let i=0;i<TD.Mission.profiles.length;i++){
  const s=TD.createState();
  s.viewport.W=1000;s.viewport.H=600;s.ship.x=120;s.ship.y=300;s.ship.angle=.33;s.mission.index=i;
  const physicalLength=s.ship.length,physicalWidth=s.ship.width;
  TD.Mission.placeCurrent(s);
  assert.equal(s.ship.length,physicalLength,'visual craft family probe must not retune physical torque lever');
  assert.equal(s.ship.width,physicalWidth,'visual craft family probe must not mutate accepted physical width');
  const target=TD.Geometry.stationDockAnchor(s);
  assert.ok(Math.abs(normAngle(target.angle-(s.ship.angle+s.ship.dockAnchor.angle)))<EPS);
  const pose=TD.Geometry.bodyPoseForWorldAnchor(target.x,target.y,target.angle,s.ship.dockAnchor);
  s.ship.x=pose.x;s.ship.y=pose.y;s.ship.angle=pose.angle;s.ship.vx=target.vx;s.ship.vy=target.vy;s.ship.angVel=s.station.omega;
  const m=TD.Docking.metrics(s);
  assert.ok(m.dist<EPS);assert.ok(m.rel<EPS);assert.ok(m.dir<EPS);assert.ok(m.spin<EPS);assert.equal(TD.Docking.canDock(m),true);
}

console.log('Twin Dock craft-family + port-shape probe tests: PASS');
