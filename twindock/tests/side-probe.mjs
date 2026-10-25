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
const { normAngle }=TD.MathUtil;
const EPS=1e-9;
const near=(a,b,eps=EPS)=>assert.ok(Math.abs(a-b)<=eps,`${a} != ${b}`);

const reference=TD.createState();
reference.viewport.W=1000;reference.viewport.H=600;reference.ship.x=100;reference.ship.y=300;reference.ship.angle=.41;
TD.Mission.reset(reference);
near(normAngle(reference.station.angle-(reference.ship.angle+Math.PI)),0);
const refTarget=TD.Geometry.stationDockAnchor(reference);
near(normAngle(refTarget.angle-reference.ship.angle),0);
assert.equal(reference.ship.geometryId,'REFERENCE');
assert.equal(reference.ship.dockAnchor.x,TD.Config.VISUAL_PROBE_X);
assert.equal(reference.ship.dockAnchor.y,0);
assert.equal(reference.ship.dockAnchor.angle,0);

const side=TD.createState();
side.viewport.W=1000;side.viewport.H=600;side.ship.x=100;side.ship.y=300;side.ship.angle=.41;
side.ship.geometryId='SIDE';
side.ship.dockAnchor.x=2;side.ship.dockAnchor.y=-31;side.ship.dockAnchor.angle=-Math.PI/2;
side.mission.index=2;
TD.Mission.placeCurrent(side);
const sideTarget=TD.Geometry.stationDockAnchor(side);
near(normAngle(sideTarget.angle-(side.ship.angle+side.ship.dockAnchor.angle)),0);
assert.ok(Math.hypot(side.ship.dockAnchor.x-TD.Config.VISUAL_PROBE_X,side.ship.dockAnchor.y)>40);
assert.notEqual(side.station.omega,0);

const pose=TD.Geometry.bodyPoseForWorldAnchor(sideTarget.x,sideTarget.y,sideTarget.angle,side.ship.dockAnchor);
side.ship.x=pose.x;side.ship.y=pose.y;side.ship.angle=pose.angle;
side.ship.vx=sideTarget.vx;side.ship.vy=sideTarget.vy;side.ship.angVel=side.station.omega;
const m=TD.Docking.metrics(side);
assert.ok(m.dist<EPS);assert.ok(m.rel<EPS);assert.ok(m.dir<EPS);assert.ok(m.spin<EPS);assert.equal(TD.Docking.canDock(m),true);
near(m.shipAnchor.x,m.stationAnchor.x);near(m.shipAnchor.y,m.stationAnchor.y);near(normAngle(m.shipAnchor.angle-m.stationAnchor.angle),0);

const fullRigidRel=Math.hypot(m.shipAnchor.vx-m.stationAnchor.vx,m.shipAnchor.vy-m.stationAnchor.vy);
assert.ok(fullRigidRel>1,'side anchor rigid velocity should differ materially from accepted COM-relative metric when spinning');
assert.ok(m.rel<EPS,'accepted metric intentionally remains ship COM linear velocity vs station anchor velocity');

console.log('Twin Dock side-anchor probe contract tests: PASS');
