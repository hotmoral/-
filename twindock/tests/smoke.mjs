import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..');
const context={window:{TwinDock:{}},performance:{now:()=>0},console};
vm.createContext(context);
for(const file of ['config.js','math.js','geometry.js','state.js','docking.js']){
  vm.runInContext(fs.readFileSync(path.join(root,'src',file),'utf8'),context,{filename:file});
}
const TD=context.window.TwinDock;
const { normAngle }=TD.MathUtil;
const EPS=1e-9;
const near=(a,b,eps=EPS)=>assert.ok(Math.abs(a-b)<=eps,`${a} != ${b}`);

assert.equal(TD.MathUtil.inputCurve(0.05),0);
assert.ok(TD.MathUtil.inputCurve(0.5)>0 && TD.MathUtil.inputCurve(0.5)<1);
assert.equal(TD.MathUtil.seeded01(42),TD.MathUtil.seeded01(42));

function legacyMetrics(state){
  const C=TD.Config,ship=state.ship,station=state.station;
  const ux=Math.cos(station.angle),uy=Math.sin(station.angle);
  const px=station.cx+ux*station.radius,py=station.cy+uy*station.radius;
  const targetAngle=normAngle(station.angle+Math.PI);
  const fx=Math.cos(ship.angle),fy=Math.sin(ship.angle);
  const probeX=ship.x+fx*C.VISUAL_PROBE_X,probeY=ship.y+fy*C.VISUAL_PROBE_X;
  const tx=Math.cos(targetAngle),ty=Math.sin(targetAngle);
  const captureX=px+tx*C.PORT_CAPTURE_INSET,captureY=py+ty*C.PORT_CAPTURE_INSET;
  const rx=captureX-station.cx,ry=captureY-station.cy;
  const captureVx=station.vx-station.omega*ry,captureVy=station.vy+station.omega*rx;
  const rvx=ship.vx-captureVx,rvy=ship.vy-captureVy;
  return {
    p:{ux,uy,px,py,pvx:station.vx-station.omega*uy*station.radius,pvy:station.vy+station.omega*ux*station.radius,targetAngle},
    probeX,probeY,captureX,captureY,captureVx,captureVy,
    dist:Math.hypot(probeX-captureX,probeY-captureY),
    rel:Math.hypot(rvx,rvy),
    dir:Math.abs(normAngle(ship.angle-targetAngle)),
    spin:Math.abs(ship.angVel-station.omega)
  };
}

for(let i=0;i<256;i++){
  const r=j=>TD.MathUtil.seeded01(i*17+j);
  const s=TD.createState();
  s.ship.x=(r(1)-.5)*1600;s.ship.y=(r(2)-.5)*1000;s.ship.vx=(r(3)-.5)*140;s.ship.vy=(r(4)-.5)*140;s.ship.angle=(r(5)*2-1)*Math.PI;s.ship.angVel=(r(6)*2-1)*.9;
  s.station.cx=(r(7)-.5)*1800;s.station.cy=(r(8)-.5)*1200;s.station.vx=(r(9)-.5)*30;s.station.vy=(r(10)-.5)*30;s.station.angle=(r(11)*2-1)*Math.PI;s.station.omega=(r(12)*2-1)*.22;s.station.radius=55+r(13)*125;
  s.station.dockAnchor.x=s.station.radius-TD.Config.PORT_CAPTURE_INSET;s.station.dockAnchor.y=0;s.station.dockAnchor.angle=Math.PI;s.station.dockAnchor.tracksRadius=true;
  const old=legacyMetrics(s),m=TD.Docking.metrics(s);
  for(const key of ['probeX','probeY','captureX','captureY','captureVx','captureVy','dist','rel','dir','spin']) near(m[key],old[key]);
  for(const key of ['ux','uy','px','py','pvx','pvy']) near(m.p[key],old.p[key]);
  near(normAngle(m.p.targetAngle-old.p.targetAngle),0);
}

const s=TD.createState();
s.viewport.W=1000;s.viewport.H=600;
s.station.cx=790;s.station.cy=270;s.station.radius=72;s.station.angle=Math.PI;s.station.omega=TD.Config.STATION_OMEGA;
s.station.dockAnchor.x=s.station.radius-TD.Config.PORT_CAPTURE_INSET;
const stationAnchor=TD.Geometry.stationDockAnchor(s);
const pose=TD.Geometry.bodyPoseForWorldAnchor(stationAnchor.x,stationAnchor.y,stationAnchor.angle,s.ship.dockAnchor);
s.ship.x=pose.x;s.ship.y=pose.y;s.ship.angle=pose.angle;s.ship.angVel=s.station.omega;s.ship.vx=stationAnchor.vx;s.ship.vy=stationAnchor.vy;
let m=TD.Docking.metrics(s);
assert.ok(m.dist<EPS);assert.ok(m.rel<EPS);assert.ok(m.dir<EPS);assert.ok(m.spin<EPS);assert.equal(TD.Docking.canDock(m),true);

const arbitrary=TD.createState();
arbitrary.station.cx=430;arbitrary.station.cy=260;arbitrary.station.vx=7;arbitrary.station.vy=-4;arbitrary.station.angle=.73;arbitrary.station.omega=-.12;
arbitrary.station.dockAnchor={x:34,y:-27,angle:-1.05,tracksRadius:false};
arbitrary.ship.dockAnchor={x:-16,y:21,angle:1.31};
const target=TD.Geometry.stationDockAnchor(arbitrary);
const bodyPose=TD.Geometry.bodyPoseForWorldAnchor(target.x,target.y,target.angle,arbitrary.ship.dockAnchor);
arbitrary.ship.x=bodyPose.x;arbitrary.ship.y=bodyPose.y;arbitrary.ship.angle=bodyPose.angle;arbitrary.ship.vx=target.vx;arbitrary.ship.vy=target.vy;arbitrary.ship.angVel=arbitrary.station.omega;
m=TD.Docking.metrics(arbitrary);
assert.ok(m.dist<EPS);assert.ok(m.rel<EPS);assert.ok(m.dir<EPS);assert.ok(m.spin<EPS);assert.equal(TD.Docking.canDock(m),true);
near(m.shipAnchor.x,m.stationAnchor.x);near(m.shipAnchor.y,m.stationAnchor.y);near(normAngle(m.shipAnchor.angle-m.stationAnchor.angle),0);

console.log('Twin Dock smoke / Geometry v2 reference parity tests: PASS');
