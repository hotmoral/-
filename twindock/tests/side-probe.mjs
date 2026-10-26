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
const near=(a,b,eps=EPS)=>assert.ok(Math.abs(a-b)<=eps,`${a} != ${b}`);

const side=TD.createState();
side.viewport.W=1000;side.viewport.H=600;side.ship.x=100;side.ship.y=300;side.ship.angle=.41;side.mission.index=0;
TD.Mission.placeCurrent(side);
const sideTarget=TD.Geometry.stationDockAnchor(side);
assert.equal(side.ship.geometryId,'CARGO_CTRL_SIDE_TOP');
assert.equal(side.ship.anchorClass,'SIDE');
near(normAngle(sideTarget.angle-(side.ship.angle+side.ship.dockAnchor.angle)),0);
near(Math.hypot(side.ship.dockAnchor.x,side.ship.dockAnchor.y),61);

const corner=TD.createState();
corner.viewport.W=1000;corner.viewport.H=600;corner.ship.x=100;corner.ship.y=300;corner.ship.angle=.41;corner.mission.index=4;
TD.Mission.placeCurrent(corner);
const cornerTarget=TD.Geometry.stationDockAnchor(corner);
assert.equal(corner.ship.geometryId,'CARGO_CTRL_CORNER');
assert.equal(corner.ship.anchorClass,'CORNER');
near(normAngle(cornerTarget.angle-(corner.ship.angle+corner.ship.dockAnchor.angle)),0);
near(Math.hypot(corner.ship.dockAnchor.x,corner.ship.dockAnchor.y),98,1e-6);
assert.notEqual(corner.station.omega,0);

const pose=TD.Geometry.bodyPoseForWorldAnchor(cornerTarget.x,cornerTarget.y,cornerTarget.angle,corner.ship.dockAnchor);
corner.ship.x=pose.x;corner.ship.y=pose.y;corner.ship.angle=pose.angle;
corner.ship.vx=cornerTarget.vx;corner.ship.vy=cornerTarget.vy;corner.ship.angVel=corner.station.omega;
const m=TD.Docking.metrics(corner);
assert.ok(m.dist<EPS);assert.ok(m.rel<EPS);assert.ok(m.dir<EPS);assert.ok(m.spin<EPS);assert.equal(TD.Docking.canDock(m),true);
near(m.shipAnchor.x,m.stationAnchor.x);near(m.shipAnchor.y,m.stationAnchor.y);near(normAngle(m.shipAnchor.angle-m.stationAnchor.angle),0);

const fullRigidRel=Math.hypot(m.shipAnchor.vx-m.stationAnchor.vx,m.shipAnchor.vy-m.stationAnchor.vy);
assert.ok(fullRigidRel>1,'eccentric player anchor rigid velocity should differ materially from accepted COM-relative metric when spinning');
assert.ok(m.rel<EPS,'accepted metric intentionally remains ship COM linear velocity vs station anchor velocity');

console.log('Twin Dock controlled non-front anchor contract tests: PASS');
