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
const BASE = { x: 1800, y: 1800, r: 255, hp: 1100, maxHp: 1100, level: 1, wood: 0, stone: 0, meat: 0 };
const players = new Map();
const nodes = [];
const enemies = new Map();
let nextEnemyId = 1;
let worldTick = 0;
let dayClock = 12;
let raidSeq = 0;
let raidStartedThisNight = false;

function rand(a,b){ return a + Math.random()*(b-a); }
function clamp(v,a,b){ return Math.max(a, Math.min(b,v)); }
function dist(a,b){ return Math.hypot(a.x-b.x, a.y-b.y); }
function id(){ return Math.random().toString(36).slice(2,10); }
function send(ws, payload){ if(ws.readyState===1) ws.send(JSON.stringify(payload)); }
function broadcast(payload){ const s=JSON.stringify(payload); for(const c of wss.clients) if(c.readyState===1) c.send(s); }
function carryOf(p){ return p.wood+p.stone+p.meat; }
function carryCap(){ return 30 + BASE.level*10; }
function playerTier(){ return Math.min(4, BASE.level); }
function weaponName(){ return ['','조잡한 창','돌날 창','철촉 창','수호자의 창'][playerTier()]; }

function spawnNode(type, count){
  const cfg = type==='tree' ? {hp:6, r:30} : type==='rock' ? {hp:8, r:26} : {hp:4, r:22};
  for(let i=0;i<count;i++){
    let x,y;
    do {
      const a=Math.random()*Math.PI*2, d=rand(430,1650);
      x=clamp(BASE.x+Math.cos(a)*d+rand(-260,260),110,WORLD.w-110);
      y=clamp(BASE.y+Math.sin(a)*d+rand(-260,260),110,WORLD.h-110);
    } while(Math.hypot(x-BASE.x,y-BASE.y)<420);
    nodes.push({id:id(), type, x,y, hp:cfg.hp, maxHp:cfg.hp, r:cfg.r, respawnAt:0});
  }
}
spawnNode('tree', 165); spawnNode('rock', 92); spawnNode('berry', 42);

function enemyConfig(type){
  if(type==='wolf') return {hp:46,speed:118,damage:8,r:21};
  if(type==='boar') return {hp:72,speed:88,damage:12,r:26};
  return {hp:110,speed:75,damage:17,r:29};
}
function spawnEnemy(type, x, y, raid=false){
  const cfg=enemyConfig(type);
  const e={id:nextEnemyId++,type,x,y,hp:cfg.hp,maxHp:cfg.hp,speed:cfg.speed,damage:cfg.damage,r:cfg.r,raid,attackCd:0,wander:Math.random()*10,dir:0};
  enemies.set(e.id,e); return e;
}
for(let i=0;i<22;i++){
  const a=Math.random()*Math.PI*2,d=rand(650,1600);
  spawnEnemy(i%4===0?'boar':'wolf',clamp(BASE.x+Math.cos(a)*d,150,3450),clamp(BASE.y+Math.sin(a)*d,150,3450));
}

function publicPlayer(p){
  return {id:p.id,name:p.name,x:p.x,y:p.y,hp:p.hp,maxHp:p.maxHp,wood:p.wood,stone:p.stone,meat:p.meat,dir:p.dir,score:p.score,tier:playerTier(),weapon:weaponName(),carry:carryOf(p),carryCap:carryCap()};
}
function dayPhase(){
  const t=dayClock%190;
  if(t<112) return 'day';
  if(t<132) return 'dusk';
  if(t<178) return 'night';
  return 'dawn';
}
function baseUpgradeCost(level){
  if(level===1) return {wood:70,stone:35,meat:18};
  if(level===2) return {wood:155,stone:105,meat:42};
  if(level===3) return {wood:260,stone:210,meat:85};
  if(level===4) return {wood:430,stone:390,meat:150};
  return null;
}
function upgradeProgress(){
  const cost=baseUpgradeCost(BASE.level);
  if(!cost) return {complete:true,cost:null,ratio:1};
  const ratios=[BASE.wood/cost.wood,BASE.stone/cost.stone,BASE.meat/cost.meat];
  return {complete:false,cost,ratio:Math.min(1,(ratios[0]+ratios[1]+ratios[2])/3)};
}
function snapshot(){
  return {
    type:'snapshot', worldTick, world:WORLD,
    base:{...BASE,upgrade:upgradeProgress()},
    day:{phase:dayPhase(),clock:dayClock,cycle:190},
    players:[...players.values()].map(publicPlayer),
    nodes:nodes.filter(n=>!n.respawnAt).map(n=>({id:n.id,type:n.type,x:n.x,y:n.y,hp:n.hp,maxHp:n.maxHp,r:n.r})),
    enemies:[...enemies.values()].map(e=>({id:e.id,type:e.type,x:e.x,y:e.y,hp:e.hp,maxHp:e.maxHp,r:e.r,raid:e.raid,dir:e.dir}))
  };
}

function maybeUpgradeBase(){
  const c=baseUpgradeCost(BASE.level);
  if(!c || BASE.level>=5) return;
  if(BASE.wood>=c.wood && BASE.stone>=c.stone && BASE.meat>=c.meat){
    BASE.wood-=c.wood; BASE.stone-=c.stone; BASE.meat-=c.meat; BASE.level++;
    BASE.maxHp += 420 + BASE.level*80; BASE.hp=BASE.maxHp;
    broadcast({type:'event',kind:'upgrade',level:BASE.level,weapon:weaponName()});
  }
}
function tryDeposit(p){
  if(Math.hypot(p.x-BASE.x,p.y-BASE.y)>BASE.r+85) return;
  if(carryOf(p)===0) return;
  const payload={wood:p.wood,stone:p.stone,meat:p.meat};
  BASE.wood+=p.wood; BASE.stone+=p.stone; BASE.meat+=p.meat;
  p.score += p.wood*2+p.stone*3+p.meat*4;
  p.wood=p.stone=p.meat=0;
  broadcast({type:'event',kind:'deposit',playerId:p.id,...payload});
  maybeUpgradeBase();
}
function addCarry(p,type,amount){
  const free=Math.max(0,carryCap()-carryOf(p));
  const got=Math.min(free,amount);
  if(got<=0){ broadcast({type:'event',kind:'carryFull',playerId:p.id}); return 0; }
  if(type==='wood')p.wood+=got;
  if(type==='stone')p.stone+=got;
  if(type==='meat')p.meat+=got;
  return got;
}
function hitNode(p){
  let best=null,bd=104;
  for(const n of nodes){ if(n.respawnAt) continue; const d=Math.hypot(n.x-p.x,n.y-p.y); if(d<bd){best=n;bd=d;} }
  if(!best) return false;
  const power=1+Math.floor((playerTier()-1)/2);
  best.hp -= power;
  broadcast({type:'event',kind:'impact',x:best.x,y:best.y,target:best.type,playerId:p.id});
  if(best.hp<=0){
    let kind,amount;
    if(best.type==='tree'){kind='wood';amount=6+Math.floor(Math.random()*4)+playerTier();}
    if(best.type==='rock'){kind='stone';amount=5+Math.floor(Math.random()*4)+Math.floor(playerTier()/2);}
    if(best.type==='berry'){kind='meat';amount=2+Math.floor(playerTier()/3);}
    const got=addCarry(p,kind,amount);
    p.score+=got;
    best.respawnAt=Date.now()+38000+Math.random()*18000; best.hp=best.maxHp;
    broadcast({type:'event',kind:'gather',playerId:p.id,nodeType:best.type,resource:kind,amount:got,x:best.x,y:best.y});
  }
  return true;
}
function hitEnemy(p){
  let best=null,bd=116;
  for(const e of enemies.values()){ const d=Math.hypot(e.x-p.x,e.y-p.y); if(d<bd){best=e;bd=d;} }
  if(!best) return false;
  const dmg=12+playerTier()*6;
  best.hp-=dmg;
  const dx=best.x-p.x,dy=best.y-p.y,dl=Math.hypot(dx,dy)||1; best.x+=dx/dl*20; best.y+=dy/dl*20;
  broadcast({type:'event',kind:'slash',x:best.x,y:best.y,targetId:best.id,playerId:p.id,damage:dmg});
  if(best.hp<=0){
    enemies.delete(best.id);
    const amount=addCarry(p,'meat',best.type==='boar'?9:best.type==='brute'?12:6);
    p.score += 18 + amount*2;
    broadcast({type:'event',kind:'kill',playerId:p.id,enemyType:best.type,amount,x:best.x,y:best.y});
    setTimeout(()=>{
      const a=Math.random()*Math.PI*2,d=rand(700,1500);
      spawnEnemy(Math.random()<.3?'boar':'wolf',clamp(BASE.x+Math.cos(a)*d,120,3480),clamp(BASE.y+Math.sin(a)*d,120,3480));
    },13000);
  }
  return true;
}
function attack(p){
  if(Date.now()-p.lastAttack<330) return;
  p.lastAttack=Date.now();
  broadcast({type:'event',kind:'swing',playerId:p.id,dir:p.dir,tier:playerTier()});
  if(hitEnemy(p)) return;
  hitNode(p);
}
function spawnRaid(){
  raidSeq++;
  const count=5+BASE.level*3+Math.min(10,players.size*2);
  for(let i=0;i<count;i++){
    const a=Math.random()*Math.PI*2, radius=900+Math.random()*220;
    const type=i%5===0 && BASE.level>=2?'brute':'wolf';
    spawnEnemy(type,BASE.x+Math.cos(a)*radius,BASE.y+Math.sin(a)*radius,true);
  }
  broadcast({type:'event',kind:'raid',raid:raidSeq,count});
}
function baseTowerFire(dt){
  if(BASE.level<3 || dayPhase()!=='night') return;
  if(!baseTowerFire.cd) baseTowerFire.cd=0;
  baseTowerFire.cd-=dt;
  if(baseTowerFire.cd>0)return;
  let target=null,td=410;
  for(const e of enemies.values()){
    if(!e.raid)continue;
    const d=Math.hypot(e.x-BASE.x,e.y-BASE.y);
    if(d<td){td=d;target=e;}
  }
  if(!target)return;
  baseTowerFire.cd=Math.max(.45,1.05-BASE.level*.12);
  target.hp-=18+BASE.level*4;
  broadcast({type:'event',kind:'towerShot',x1:BASE.x,y1:BASE.y,x2:target.x,y2:target.y});
  if(target.hp<=0) enemies.delete(target.id);
}

wss.on('connection', ws=>{
  const pid=id();
  const p={id:pid,name:`생존자-${pid.slice(0,3)}`,x:BASE.x+rand(-75,75),y:BASE.y+rand(-75,75),hp:100,maxHp:100,wood:0,stone:0,meat:0,dir:0,lastAttack:0,input:{x:0,y:0},score:0};
  players.set(pid,p);
  send(ws,{type:'welcome',id:pid}); send(ws,snapshot());
  broadcast({type:'event',kind:'join',player:publicPlayer(p)});
  ws.on('message',raw=>{
    let m; try{m=JSON.parse(raw);}catch{return;}
    if(m.type==='input'){
      p.input.x=clamp(Number(m.x)||0,-1,1); p.input.y=clamp(Number(m.y)||0,-1,1);
      if(Math.hypot(p.input.x,p.input.y)>1){const l=Math.hypot(p.input.x,p.input.y);p.input.x/=l;p.input.y/=l;}
    }
    if(m.type==='attack') attack(p);
    if(m.type==='deposit') tryDeposit(p);
    if(m.type==='name' && typeof m.name==='string') p.name=m.name.trim().slice(0,14)||p.name;
  });
  ws.on('close',()=>{players.delete(pid);broadcast({type:'event',kind:'leave',playerId:pid});});
});

let last=Date.now();
setInterval(()=>{
  const now=Date.now(),dt=Math.min(.05,(now-last)/1000); last=now; worldTick++; dayClock=(dayClock+dt)%190;
  const phase=dayPhase();
  if(phase==='night' && !raidStartedThisNight){ raidStartedThisNight=true; spawnRaid(); }
  if(phase==='day') raidStartedThisNight=false;
  if(phase==='day') BASE.hp=Math.min(BASE.maxHp,BASE.hp+2.2*dt);

  for(const p of players.values()){
    const speed=224;
    p.x=clamp(p.x+p.input.x*speed*dt,35,WORLD.w-35); p.y=clamp(p.y+p.input.y*speed*dt,35,WORLD.h-35);
    if(Math.hypot(p.input.x,p.input.y)>.08) p.dir=Math.atan2(p.input.y,p.input.x);
    if(Math.hypot(p.x-BASE.x,p.y-BASE.y)<BASE.r+52){
      p.hp=Math.min(p.maxHp,p.hp+12*dt);
      if(carryOf(p)>0) tryDeposit(p);
    }
  }

  for(const e of enemies.values()){
    e.attackCd=Math.max(0,e.attackCd-dt);
    let target=null,td=Infinity;
    for(const p of players.values()){const d=dist(e,p);if(d<td){td=d;target=p;}}
    const db=Math.hypot(e.x-BASE.x,e.y-BASE.y);
    if(e.raid && (db<td || !target)){ target=BASE; td=db; }
    if(target && (td<540 || e.raid)){
      const dx=target.x-e.x,dy=target.y-e.y,l=Math.hypot(dx,dy)||1; e.dir=Math.atan2(dy,dx);
      if(td>(target===BASE?BASE.r*.7+e.r:39)){e.x+=dx/l*e.speed*dt;e.y+=dy/l*e.speed*dt;}
      else if(e.attackCd<=0){
        e.attackCd=.82;
        if(target===BASE){
          BASE.hp=Math.max(0,BASE.hp-e.damage);
          broadcast({type:'event',kind:'baseHit',hp:BASE.hp,x:e.x,y:e.y});
          if(BASE.hp<=0){BASE.hp=BASE.maxHp*.45; broadcast({type:'event',kind:'baseBreach'});}
        } else {
          target.hp=Math.max(0,target.hp-e.damage);
          broadcast({type:'event',kind:'hurt',playerId:target.id,amount:e.damage});
          if(target.hp<=0){
            target.hp=target.maxHp; target.x=BASE.x; target.y=BASE.y;
            target.wood=Math.floor(target.wood*.6); target.stone=Math.floor(target.stone*.6); target.meat=Math.floor(target.meat*.6);
            broadcast({type:'event',kind:'down',playerId:target.id});
          }
        }
      }
    } else {
      e.wander+=dt; e.dir=e.wander*.65+e.id;
      e.x=clamp(e.x+Math.cos(e.dir)*e.speed*.11*dt,80,WORLD.w-80);
      e.y=clamp(e.y+Math.sin(e.dir)*e.speed*.11*dt,80,WORLD.h-80);
    }
  }
  baseTowerFire(dt);
  for(const n of nodes) if(n.respawnAt && n.respawnAt<now){n.respawnAt=0;n.hp=n.maxHp;}
  if(worldTick%3===0) broadcast(snapshot());
},1000/30);

server.listen(PORT,()=>console.log(`Outpost Wilds listening on ${PORT}`));
