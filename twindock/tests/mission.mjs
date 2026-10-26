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
const EPS=1e-9;
const near=(a,b,eps=EPS)=>assert.ok(Math.abs(a-b)<=eps,`${a} != ${b}`);

assert.equal(TD.Config.FORCE_SCALE,58);
assert.equal(TD.Config.INPUT_DEADZONE,0.10);
assert.equal(TD.Config.INPUT_EXPONENT,2.05);
assert.equal(TD.Config.MAX_SPEED,78);
assert.equal(TD.Config.MAX_ANGULAR_SPEED,0.90);
assert.deepEqual(Array.from(TD.Mission.profiles,p=>p.id),['SIDE_TOP','FRONT','SIDE_BOTTOM','REAR','CORNER']);
assert.deepEqual(Array.from(TD.Mission.profiles,p=>p.setupId),['CARGO_CTRL_SIDE_TOP','CARGO_CTRL_FRONT','CARGO_CTRL_SIDE_BOTTOM','CARGO_CTRL_REAR','CARGO_CTRL_CORNER']);

let baseline=null;
const stationComVelocities=[];
for(let i=0;i<TD.Mission.profiles.length;i++){
  const s=TD.createState();
  s.viewport.W=1000;s.viewport.H=600;s.mission.index=i;
  s.ship.x=777;s.ship.y=-222;s.ship.vx=31;s.ship.vy=-19;s.ship.angle=.83;s.ship.angVel=.61;s.angularDrive=9;
  TD.Mission.placeCurrent(s);
  near(s.ship.x,140);near(s.ship.y,276);near(s.ship.vx,0);near(s.ship.vy,0);near(s.ship.angle,0);near(s.ship.angVel,0);near(s.angularDrive,0);
  assert.equal(s.ship.craftId,'CARGO');assert.equal(s.ship.portShape,'RECT');
  const player=TD.Geometry.shipDockAnchor(s);
  const target=TD.Geometry.stationDockAnchor(s);
  const snapshot={dx:target.x-player.x,dy:target.y-player.y,vx:target.vx,vy:target.vy,omega:s.station.omega};
  if(!baseline) baseline=snapshot;
  else {
    near(snapshot.dx,baseline.dx);near(snapshot.dy,baseline.dy);
    near(snapshot.vx,baseline.vx);near(snapshot.vy,baseline.vy);near(snapshot.omega,baseline.omega);
  }
  near(target.angle,s.ship.dockAnchor.angle);
  stationComVelocities.push([s.station.vx,s.station.vy]);
  const pose=TD.Geometry.bodyPoseForWorldAnchor(target.x,target.y,target.angle,s.ship.dockAnchor);
  s.ship.x=pose.x;s.ship.y=pose.y;s.ship.angle=pose.angle;s.ship.vx=target.vx;s.ship.vy=target.vy;s.ship.angVel=s.station.omega;
  const m=TD.Docking.metrics(s);
  assert.ok(m.dist<EPS);assert.ok(m.rel<EPS);assert.ok(m.dir<EPS);assert.ok(m.spin<EPS);assert.equal(TD.Docking.canDock(m),true);
}

const rounded=new Set(stationComVelocities.map(([x,y])=>`${x.toFixed(6)},${y.toFixed(6)}`));
assert.ok(rounded.size>1,'station COM velocity should compensate differently so capture-anchor velocity stays identical');

const seq=TD.createState();seq.viewport.W=1000;seq.viewport.H=600;
let p=TD.Mission.reset(seq);assert.equal(p.id,'SIDE_TOP');
seq.ship.vx=99;seq.ship.vy=-88;seq.ship.angVel=.7;seq.ship.angle=1.1;seq.ship.x=999;seq.ship.y=999;
p=TD.Mission.advance(seq);assert.equal(p.id,'FRONT');
near(seq.ship.x,140);near(seq.ship.y,276);near(seq.ship.vx,0);near(seq.ship.vy,0);near(seq.ship.angle,0);near(seq.ship.angVel,0);

console.log('Twin Dock capture-anchor controlled mission tests: PASS');
