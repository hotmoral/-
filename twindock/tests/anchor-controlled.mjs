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
const ids=['CARGO_CTRL_SIDE_TOP','CARGO_CTRL_FRONT','CARGO_CTRL_SIDE_BOTTOM','CARGO_CTRL_REAR','CARGO_CTRL_CORNER'];
assert.deepEqual(Array.from(TD.Mission.profiles,p=>p.setupId),ids);

const setup=Object.fromEntries(ids.map(id=>[id,TD.CraftGeometry.get(id)]));
for(const id of ids){assert.equal(setup[id].craftId,'CARGO');assert.equal(setup[id].portShape,'RECT');}
const r=id=>Math.hypot(setup[id].x,setup[id].y);
near(r('CARGO_CTRL_SIDE_TOP'),61);near(r('CARGO_CTRL_SIDE_BOTTOM'),61);
near(r('CARGO_CTRL_FRONT'),98);near(r('CARGO_CTRL_REAR'),98);near(r('CARGO_CTRL_CORNER'),98,1e-6);

const snapshots=[];
for(let i=0;i<TD.Mission.profiles.length;i++){
  const s=TD.createState();
  s.viewport.W=1200;s.viewport.H=700;s.mission.index=i;
  const physicalLength=s.ship.length,physicalWidth=s.ship.width;
  s.ship.x=-500;s.ship.y=900;s.ship.vx=44;s.ship.vy=-33;s.ship.angle=-2.2;s.ship.angVel=.8;s.angularDrive=-3;
  TD.Mission.placeCurrent(s);

  assert.equal(s.ship.length,physicalLength,'trial reset must not alter accepted physical torque lever');
  assert.equal(s.ship.width,physicalWidth,'trial reset must not alter accepted physical width');
  near(s.ship.x,s.viewport.W*.14);near(s.ship.y,s.viewport.H*.46);
  near(s.ship.vx,0);near(s.ship.vy,0);near(s.ship.angle,0);near(s.ship.angVel,0);near(s.angularDrive,0);

  const player=TD.Geometry.shipDockAnchor(s);
  const target=TD.Geometry.stationDockAnchor(s);
  snapshots.push({
    dx:target.x-player.x,dy:target.y-player.y,
    targetVx:target.vx,targetVy:target.vy,targetOmega:s.station.omega,
    stationVx:s.station.vx,stationVy:s.station.vy,
    playerX:player.x,playerY:player.y
  });
}

for(let i=1;i<snapshots.length;i++){
  near(snapshots[i].dx,snapshots[0].dx);near(snapshots[i].dy,snapshots[0].dy);
  near(snapshots[i].targetVx,snapshots[0].targetVx);near(snapshots[i].targetVy,snapshots[0].targetVy);
  near(snapshots[i].targetOmega,snapshots[0].targetOmega);
}
assert.notEqual(snapshots[1].playerX,snapshots[3].playerX,'front and rear player anchors must remain geometrically distinct');
assert.ok(new Set(snapshots.map(x=>`${x.stationVx.toFixed(6)},${x.stationVy.toFixed(6)}`)).size>1,'station COM compensation should vary by orientation');

console.log('Twin Dock capture-anchor causal-control tests: PASS');
