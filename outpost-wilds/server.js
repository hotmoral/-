const express = require('express');
const http = require('http');
const path = require('path');
const { WebSocketServer } = require('ws');

const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server });
app.use(express.static(path.join(__dirname, 'public')));

const PORT = process.env.PORT || 3000;
const WORLD = { w: 3600, h: 3600 };
const BASE = { x: 1800, y: 1800, r: 250, hp: 1000, maxHp: 1000, level: 1, wood: 0, stone: 0, meat: 0 };
const players = new Map();
const nodes = [];
const enemies = new Map();
let nextEnemyId = 1;
let worldTick = 0;
let dayClock = 0;
let raidSeq = 0;

function rand(a,b){ return a + Math.random()*(b-a); }
function clamp(v,a,b){ return Math.max(a, Math.min(b,v)); }
function dist(a,b){ return Math.hypot(a.x-b.x, a.y-b.y); }
function id(){ return Math.random().toString(36).slice(2,10); }
function send(ws, payload){ if(ws.readyState===1) ws.send(JSON.stringify(payload)); }
function broadcast(payload){ const s=JSON.stringify(payload); for(const c of wss.clients) if(c.readyState===1) c.send(s); }

function spawnNode(type, count){
  const cfg = type==='tree' ? {hp:5, r:28} : type==='rock' ? {hp:7, r:24} : {hp:4, r:22};
  for(let i=0;i<count;i++){
    let x,y;
    do { x=rand(120,WORLD.w-120); y=rand(120,WORLD.h-120); } while(Math.hypot(x-BASE.x,y-BASE.y)<420);
    nodes.push({id:id(), type, x,y, hp:cfg.hp, maxHp:cfg.hp, r:cfg.r, respawnAt:0});
  }
}
spawnNode('tree', 140); spawnNode('rock', 75); spawnNode('berry', 35);

function spawnEnemy(type, x, y, raid=false){
  const cfg = type==='wolf' ? {hp:42,speed:112,damage:8,r:20} : type==='boar' ? {hp:68,speed:82,damage:12,r:25} : {hp:95,speed:72,damage:15,r:27};
  const e={id:nextEnemyId++,type,x,y,hp:cfg.hp,maxHp:cfg.hp,speed:cfg.speed,damage:cfg.damage,r:cfg.r,raid,attackCd:0,wander:Math.random()*10};
  enemies.set(e.id,e); return e;
}
for(let i=0;i<18;i++) spawnEnemy(i%3===0?'boar':'wolf', rand(200,3400),rand(200,3400));

function publicPlayer(p){ return {id:p.id,name:p.name,x:p.x,y:p.y,hp:p.hp,maxHp:p.maxHp,wood:p.wood,stone:p.stone,meat:p.meat,weapon:p.weapon,color:p.color,dir:p.dir}; }
function snapshot(){
  return {
    type:'snapshot', worldTick, world:WORLD,
    base:BASE,
    day:{phase:dayPhase(),clock:dayClock,cycle:180},
    players:[...players.values()].map(publicPlayer),
    nodes:nodes.filter(n=>!n.respawnAt).map(n=>({id:n.id,type:n.type,x:n.x,y:n.y,hp:n.hp,maxHp:n.maxHp,r:n.r})),
    enemies:[...enemies.values()].map(e=>({id:e.id,type:e.type,x:e.x,y:e.y,hp:e.hp,maxHp:e.maxHp,r:e.r,raid:e.raid}))
  };
}
function dayPhase(){
  const t=dayClock%180;
  if(t<105) return 'day';
  if(t<125) return 'dusk';
  if(t<170) return 'night';
  return 'dawn';
}
function baseUpgradeCost(level){
  if(level===1) return {wood:70,stone:35,meat:18};
  if(level===2) return {wood:150,stone:110,meat:45};
  return {wood:9999,stone:9999,meat:9999};
}
function tryDeposit(p){
  if(Math.hypot(p.x-BASE.x,p.y-BASE.y)>BASE.r+70) return;
  if(p.wood+p.stone+p.meat===0) return;
  BASE.wood+=p.wood; BASE.stone+=p.stone; BASE.meat+=p.meat;
  p.wood=p.stone=p.meat=0;
  broadcast({type:'event',kind:'deposit',playerId:p.id});
  const c=baseUpgradeCost(BASE.level);
  if(BASE.wood>=c.wood && BASE.stone>=c.stone && BASE.meat>=c.meat && BASE.level<3){
    BASE.wood-=c.wood; BASE.stone-=c.stone; BASE.meat-=c.meat; BASE.level++;
    BASE.maxHp+=450; BASE.hp=BASE.maxHp;
    broadcast({type:'event',kind:'upgrade',level:BASE.level});
  }
}
function hitNode(p){
  let best=null,bd=95;
  for(const n of nodes){ if(n.respawnAt) continue; const d=Math.hypot(n.x-p.x,n.y-p.y); if(d<bd){best=n;bd=d;} }
  if(!best) return false;
  best.hp -= p.weapon==='axe'?2:1;
  broadcast({type:'event',kind:'impact',x:best.x,y:best.y,target:best.type});
  if(best.hp<=0){
    if(best.type==='tree') p.wood += 5+Math.floor(Math.random()*4);
    if(best.type==='rock') p.stone += 4+Math.floor(Math.random()*4);
    if(best.type==='berry') p.meat += 1;
    best.respawnAt=Date.now()+45000; best.hp=best.maxHp;
    broadcast({type:'event',kind:'gather',playerId:p.id,nodeType:best.type,x:best.x,y:best.y});
  }
  return true;
}
function hitEnemy(p){
  let best=null,bd=105;
  for(const e of enemies.values()){ const d=Math.hypot(e.x-p.x,e.y-p.y); if(d<bd){best=e;bd=d;} }
  if(!best) return false;
  const dmg=p.weapon==='spear'?18:12;
  best.hp-=dmg;
  const dx=best.x-p.x,dy=best.y-p.y,dl=Math.hypot(dx,dy)||1; best.x+=dx/dl*18; best.y+=dy/dl*18;
  broadcast({type:'event',kind:'slash',x:best.x,y:best.y,targetId:best.id});
  if(best.hp<=0){
    enemies.delete(best.id); p.meat += best.type==='boar'?8:5; if(Math.random()<0.35) p.wood+=2;
    broadcast({type:'event',kind:'kill',playerId:p.id,enemyType:best.type,x:best.x,y:best.y});
    setTimeout(()=>spawnEnemy(Math.random()<.35?'boar':'wolf',rand(200,3400),rand(200,3400)),15000);
  }
  return true;
}
function attack(p){
  if(Date.now()-p.lastAttack<360) return; p.lastAttack=Date.now();
  if(hitEnemy(p)) return;
  hitNode(p);
}
function spawnRaid(){
  raidSeq++;
  const count=4+BASE.level*3+Math.min(8,players.size*2);
  for(let i=0;i<count;i++){
    const a=Math.random()*Math.PI*2, radius=880+Math.random()*180;
    spawnEnemy(i%4===0?'brute':'wolf',BASE.x+Math.cos(a)*radius,BASE.y+Math.sin(a)*radius,true);
  }
  broadcast({type:'event',kind:'raid',raid:raidSeq,count});
}

wss.on('connection', ws=>{
  const pid=id();
  const p={id:pid,name:`생존자-${pid.slice(0,3)}`,x:BASE.x+rand(-80,80),y:BASE.y+rand(-80,80),hp:100,maxHp:100,wood:0,stone:0,meat:0,weapon:'spear',color:`hsl(${Math.floor(rand(0,360))} 65% 62%)`,dir:0,lastAttack:0,input:{x:0,y:0}};
  players.set(pid,p);
  send(ws,{type:'welcome',id:pid}); send(ws,snapshot());
  broadcast({type:'event',kind:'join',player:publicPlayer(p)});
  ws.on('message',raw=>{
    let m; try{m=JSON.parse(raw);}catch{return;}
    if(m.type==='input') { p.input.x=clamp(Number(m.x)||0,-1,1); p.input.y=clamp(Number(m.y)||0,-1,1); if(Math.hypot(p.input.x,p.input.y)>1){const l=Math.hypot(p.input.x,p.input.y);p.input.x/=l;p.input.y/=l;} }
    if(m.type==='attack') attack(p);
    if(m.type==='deposit') tryDeposit(p);
    if(m.type==='name' && typeof m.name==='string') p.name=m.name.trim().slice(0,14)||p.name;
  });
  ws.on('close',()=>{players.delete(pid);broadcast({type:'event',kind:'leave',playerId:pid});});
});

let last=Date.now();
setInterval(()=>{
  const now=Date.now(),dt=Math.min(.05,(now-last)/1000); last=now; worldTick++; dayClock=(dayClock+dt)%180;
  const phase=dayPhase();
  if(phase==='night' && !global._raidNight){ global._raidNight=true; spawnRaid(); }
  if(phase==='day') global._raidNight=false;

  for(const p of players.values()){
    const speed=220; p.x=clamp(p.x+p.input.x*speed*dt,35,WORLD.w-35);p.y=clamp(p.y+p.input.y*speed*dt,35,WORLD.h-35);
    if(Math.hypot(p.input.x,p.input.y)>.1) p.dir=Math.atan2(p.input.y,p.input.x);
    if(Math.hypot(p.x-BASE.x,p.y-BASE.y)<BASE.r+45) { p.hp=Math.min(p.maxHp,p.hp+10*dt); if(p.wood+p.stone+p.meat>0) tryDeposit(p); }
  }
  for(const e of enemies.values()){
    e.attackCd=Math.max(0,e.attackCd-dt);
    let target=null,td=Infinity;
    for(const p of players.values()){const d=dist(e,p);if(d<td){td=d;target=p;}}
    const db=Math.hypot(e.x-BASE.x,e.y-BASE.y);
    if(e.raid && (db<td || !target)){ target=BASE;td=db; }
    if(target && (td<520 || e.raid)){
      const dx=target.x-e.x,dy=target.y-e.y,l=Math.hypot(dx,dy)||1;
      if(td>(target===BASE?BASE.r+e.r:38)){e.x+=dx/l*e.speed*dt;e.y+=dy/l*e.speed*dt;}
      else if(e.attackCd<=0){
        e.attackCd=.85;
        if(target===BASE){ BASE.hp=Math.max(0,BASE.hp-e.damage); broadcast({type:'event',kind:'baseHit',hp:BASE.hp}); }
        else { target.hp=Math.max(0,target.hp-e.damage); if(target.hp<=0){target.hp=target.maxHp;target.x=BASE.x;target.y=BASE.y;target.wood=Math.floor(target.wood*.6);target.stone=Math.floor(target.stone*.6);target.meat=Math.floor(target.meat*.6);broadcast({type:'event',kind:'down',playerId:target.id});} }
      }
    } else {
      e.wander+=dt; e.x+=Math.cos(e.wander*.7+e.id)*e.speed*.12*dt; e.y+=Math.sin(e.wander*.6+e.id)*e.speed*.12*dt;
    }
  }
  for(const n of nodes) if(n.respawnAt && n.respawnAt<now){n.respawnAt=0;n.hp=n.maxHp;}
  if(worldTick%3===0) broadcast(snapshot());
},1000/30);

server.listen(PORT,()=>console.log(`Outpost Wilds listening on ${PORT}`));
