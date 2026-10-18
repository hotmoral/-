const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const WebSocket = require('ws');

const PORT = process.env.PORT || 3000;
const ROOT = path.join(__dirname, 'public');
const rooms = new Map();

const WEAPONS = {
  knife:   {label:'투척칼', speed:12.5, power:0.095, gravity:0.23, wind:0.65, damage:38, radius:22, crater:0},
  grenade: {label:'수류탄', speed:9.2,  power:0.082, gravity:0.27, wind:1.00, damage:52, radius:88, crater:66},
  pistol:  {label:'권총',   speed:27.0, power:0.060, gravity:0.060, wind:0.24, damage:25, radius:18, crater:0},
  rifle:   {label:'소총',   speed:34.0, power:0.066, gravity:0.040, wind:0.16, damage:34, radius:17, crater:0}
};

function send(ws, type, data={}) {
  if (ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify({type, ...data}));
}
function broadcast(room, type, data={}) {
  for (const c of room.clients) send(c.ws, type, data);
}
function roomIdSafe(id) { return /^[A-Z0-9]{5,10}$/.test(id || ''); }
function terrainY(room, x) {
  const i = Math.max(0, Math.min(room.terrain.length - 1, Math.round(x / room.terrainStep)));
  return room.terrain[i];
}
function makeTerrain(seed) {
  let h = 520;
  const step = 6;
  const arr = [];
  let s = parseInt(crypto.createHash('sha256').update(seed).digest('hex').slice(0,8),16) >>> 0;
  const rnd = () => ((s = (1664525*s + 1013904223) >>> 0) / 4294967296);
  for (let x=0; x<=1000; x+=step) {
    const target = 475 + Math.sin(x/105)*38 + Math.sin(x/47)*13 + (rnd()-0.5)*9;
    h += (target-h)*0.13;
    arr.push(Math.max(360, Math.min(555, h)));
  }
  return {arr, step};
}
function makeRoom(id) {
  const {arr, step} = makeTerrain(id);
  const room = {
    id, clients:new Set(), slots:[null,null], terrain:arr, terrainStep:step,
    players:[{x:135,hp:100},{x:865,hp:100}], turn:0, moveLeft:70,
    wind:(Math.random()*0.10-0.05), resolving:false, winner:null, round:1, rematch:new Set()
  };
  for (const p of room.players) p.y = terrainY(room,p.x)-28;
  return room;
}
function publicState(room) {
  return {
    id:room.id, terrain:room.terrain, terrainStep:room.terrainStep,
    players:room.players, turn:room.turn, moveLeft:room.moveLeft, wind:room.wind,
    resolving:room.resolving, winner:room.winner, round:room.round,
    connected:room.slots.map(Boolean)
  };
}
function resetRound(room) {
  const {arr,step}=makeTerrain(room.id+'-'+(++room.round));
  room.terrain=arr; room.terrainStep=step;
  room.players=[{x:135,hp:100},{x:865,hp:100}];
  for (const p of room.players) p.y=terrainY(room,p.x)-28;
  room.turn=room.round%2; room.moveLeft=70; room.wind=Math.random()*0.10-0.05;
  room.resolving=false; room.winner=null; room.rematch.clear();
}
function crater(room, cx, radius) {
  for (let i=0;i<room.terrain.length;i++) {
    const x=i*room.terrainStep, dx=Math.abs(x-cx);
    if (dx<radius) {
      const d=Math.sqrt(Math.max(0, radius*radius-dx*dx));
      room.terrain[i]=Math.min(590, room.terrain[i]+d*0.45);
    }
  }
  for (const p of room.players) p.y=terrainY(room,p.x)-28;
}
function damageAt(room, x, y, weapon) {
  room.players.forEach((p)=>{
    const dx=p.x-x, dy=(p.y-10)-y, dist=Math.hypot(dx,dy);
    if (dist <= weapon.radius) {
      let dmg=weapon.damage;
      if (weapon.radius>30) dmg=Math.max(9, Math.round(weapon.damage*(1-dist/weapon.radius)));
      p.hp=Math.max(0,p.hp-dmg);
    }
  });
  const dead=room.players.map((p,i)=>p.hp<=0?i:null).filter(i=>i!==null);
  if (dead.length) room.winner = dead.length===2 ? 'draw' : 1-dead[0];
}
function simulateShot(room, shooter, payload) {
  const weapon = WEAPONS[payload.weapon] || WEAPONS.knife;
  const angle = Math.max(5, Math.min(85, Number(payload.angle)||45))*Math.PI/180;
  const power = Math.max(20, Math.min(100, Number(payload.power)||60));
  const dir = shooter===0 ? 1 : -1;
  let x=room.players[shooter].x + dir*14, y=room.players[shooter].y-28;
  const v=weapon.speed + power*weapon.power;
  let vx=Math.cos(angle)*v*dir, vy=-Math.sin(angle)*v;
  const pathPts=[];
  let hit=null;
  for (let t=0;t<600;t++) {
    vx += room.wind*weapon.wind;
    vy += weapon.gravity;
    x += vx; y += vy;
    if (t%2===0) pathPts.push([+x.toFixed(1),+y.toFixed(1)]);
    for (let i=0;i<2;i++) {
      const p=room.players[i];
      if (i===shooter && t<6) continue;
      if (Math.hypot(x-p.x,y-(p.y-10))<16) { hit={x,y,kind:'player',target:i}; break; }
    }
    if (hit) break;
    if (x<0 || x>1000 || y>610 || y>=terrainY(room,x)) { hit={x,y,kind:'terrain'}; break; }
  }
  if (!hit) hit={x,y,kind:'out'};
  if (weapon.crater && hit.kind!=='out') crater(room,hit.x,weapon.crater);
  if (hit.kind!=='out') damageAt(room,hit.x,hit.y,weapon);
  return {path:pathPts, impact:{x:+hit.x.toFixed(1),y:+hit.y.toFixed(1),kind:hit.kind}, weapon:payload.weapon};
}
function movePlayer(room, idx, delta) {
  if (room.winner!==null || room.resolving || room.turn!==idx) return;
  const mag=Math.abs(delta); if (!mag || mag>room.moveLeft) return;
  const nx=Math.max(38,Math.min(962,room.players[idx].x+delta));
  const actual=Math.abs(nx-room.players[idx].x); if (actual>room.moveLeft+0.01) return;
  room.players[idx].x=nx; room.players[idx].y=terrainY(room,nx)-28; room.moveLeft-=actual;
}

const server=http.createServer((req,res)=>{
  let pathname=new URL(req.url,'http://localhost').pathname;
  if (pathname==='/') pathname='/index.html';
  const file=path.normalize(path.join(ROOT,pathname));
  if (!file.startsWith(ROOT)) {res.writeHead(403);return res.end('forbidden');}
  fs.readFile(file,(err,data)=>{
    if(err){res.writeHead(404);return res.end('not found');}
    const ext=path.extname(file); const mime={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript'}[ext]||'application/octet-stream';
    res.writeHead(200,{'Content-Type':mime,'Cache-Control':'no-cache'});res.end(data);
  });
});
const wss=new WebSocket.Server({server});
wss.on('connection',(ws,req)=>{
  const u=new URL(req.url,'http://localhost'); const rid=(u.searchParams.get('room')||'').toUpperCase();
  if(!roomIdSafe(rid)){send(ws,'error',{message:'잘못된 방 코드입니다.'});return ws.close();}
  const room=rooms.get(rid)||makeRoom(rid); rooms.set(rid,room);
  let role='spectator', index=null;
  if(!room.slots[0]){index=0;role='player';room.slots[0]=ws;}
  else if(!room.slots[1]){index=1;role='player';room.slots[1]=ws;}
  const client={ws,index}; room.clients.add(client);
  send(ws,'hello',{role,index,state:publicState(room)}); broadcast(room,'state',{state:publicState(room)});
  ws.on('message',raw=>{
    let m; try{m=JSON.parse(raw);}catch{return;}
    if(role!=='player')return;
    if(m.type==='move'){
      const d=Math.max(-24,Math.min(24,Number(m.delta)||0)); movePlayer(room,index,d); broadcast(room,'state',{state:publicState(room)});
    }
    if(m.type==='fire' && room.turn===index && !room.resolving && room.winner===null){
      room.resolving=true; broadcast(room,'state',{state:publicState(room)});
      const shot=simulateShot(room,index,m);
      broadcast(room,'shot',{shot,state:publicState(room)});
      setTimeout(()=>{
        room.resolving=false;
        if(room.winner===null){room.turn=1-room.turn;room.moveLeft=70;room.wind=Math.random()*0.10-0.05;}
        broadcast(room,'state',{state:publicState(room)});
      },Math.min(3600,Math.max(900,shot.path.length*17)));
    }
    if(m.type==='rematch' && room.winner!==null){
      room.rematch.add(index);
      if(room.rematch.size===2){resetRound(room);broadcast(room,'state',{state:publicState(room)});}
      else send(ws,'notice',{message:'상대의 재대결 선택을 기다리는 중입니다.'});
    }
  });
  ws.on('close',()=>{
    room.clients.delete(client);
    if(index!==null && room.slots[index]===ws) room.slots[index]=null;
    broadcast(room,'state',{state:publicState(room)});
    if(room.clients.size===0) setTimeout(()=>{if(room.clients.size===0)rooms.delete(rid);},60000);
  });
});
server.listen(PORT,()=>console.log('Stick Fortress Duel on',PORT));
