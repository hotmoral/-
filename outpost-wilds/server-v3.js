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
const ZONES = [
  { id:'camp', name:'개척 거점', hint:'안전지대 · 회복/반납/제작', color:'#775b39' },
  { id:'meadow', name:'바람 초원', hint:'초급 자원 · 늑대와 멧돼지', color:'#476a3d' },
  { id:'forest', name:'검은솔 숲', hint:'목재 밀집 · 포식자 주의', color:'#244b31' },
  { id:'quarry', name:'붉은 채석지', hint:'석재/광맥 밀집 · 야수 출몰', color:'#5c5145' },
  { id:'danger', name:'황폐 경계', hint:'고위험 · 우두머리 출몰', color:'#443735' }
];
const players = new Map();
const nodes = [];
const enemies = new Map();
let nextEnemyId = 1;
let worldTick = 0;
let dayClock = 12;
let raidSeq = 0;
let raidStartedThisNight = false;
let alphaRespawnAt = 0;

function rand(a,b){ return a + Math.random()*(b-a); }
function clamp(v,a,b){ return Math.max(a, Math.min(b,v)); }
function dist(a,b){ return Math.hypot(a.x-b.x, a.y-b.y); }
function id(){ return Math.random().toString(36).slice(2,10); }
function send(ws, payload){ if(ws.readyState===1) ws.send(JSON.stringify(payload)); }
function broadcast(payload){ const s=JSON.stringify(payload); for(const c of wss.clients) if(c.readyState===1) c.send(s); }
function carryOf(p){ return p.wood+p.stone+p.meat; }
function carryCap(){ return 30 + BASE.level*10; }
function zoneAt(x,y){
  const d=Math.hypot(x-BASE.x,y-BASE.y);
  if(d<470) return 'camp';
  if(d>1320) return 'danger';
  if(x<1420) return 'forest';
  if(x>2260) return 'quarry';
  return 'meadow';
}
function pointForZone(zone){
  for(let tries=0;tries<800;tries++){
    const x=rand(120,WORLD.w-120),y=rand(120,WORLD.h-120);
    if(zoneAt(x,y)===zone)return {x,y};
  }
  return {x:rand(160,3440),y:rand(160,3440)};
}
function weaponInfo(p){
  const defs=[
    null,
    {name:'조잡한 창',kind:'melee',damage:18,range:116,cooldown:330},
    {name:'강화 창',kind:'melee',damage:27,range:126,cooldown:300},
    {name:'사냥 활',kind:'ranged',damage:25,range:430,cooldown:540},
    {name:'철제 석궁',kind:'ranged',damage:39,range:560,cooldown:430}
  ];
  return defs[p.gearLevel]||defs[1];
}
function nextCraft(p){
  const costs={2:{merit:35,base:2,name:'강화 창'},3:{merit:90,base:3,name:'사냥 활'},4:{merit:170,base:4,name:'철제 석궁'}};
  return costs[p.gearLevel+1]||null;
}

function nodeConfig(type){
  if(type==='tree') return {hp:6,r:30};
  if(type==='rock') return {hp:8,r:26};
  if(type==='ore') return {hp:11,r:27};
  return {hp:4,r:22};
}
function spawnNode(type,count,zone){
  const cfg=nodeConfig(type);
  for(let i=0;i<count;i++){
    const p=pointForZone(zone);
    nodes.push({id:id(),type,x:p.x,y:p.y,hp:cfg.hp,maxHp:cfg.hp,r:cfg.r,respawnAt:0,zone});
  }
}
spawnNode('tree',95,'forest'); spawnNode('tree',46,'meadow'); spawnNode('tree',30,'danger');
spawnNode('rock',68,'quarry'); spawnNode('rock',27,'meadow'); spawnNode('rock',24,'danger');
spawnNode('ore',28,'quarry'); spawnNode('ore',14,'danger');
spawnNode('berry',34,'meadow'); spawnNode('berry',18,'forest');

function enemyConfig(type){
  if(type==='wolf') return {hp:46,speed:118,damage:8,r:21,aggro:540};
  if(type==='boar') return {hp:76,speed:90,damage:12,r:26,aggro:500};
  if(type==='brute') return {hp:126,speed:78,damage:18,r:30,aggro:590};
  return {hp:420,speed:86,damage:26,r:46,aggro:720};
}
function spawnEnemy(type,x,y,raid=false){
  const cfg=enemyConfig(type);
  const e={id:nextEnemyId++,type,x,y,hp:cfg.hp,maxHp:cfg.hp,speed:cfg.speed,damage:cfg.damage,r:cfg.r,aggro:cfg.aggro,raid,attackCd:0,wander:Math.random()*10,dir:0,boss:type==='alpha'};
  enemies.set(e.id,e); return e;
}
function spawnEnemyIn(type,zone,raid=false){ const p=pointForZone(zone); return spawnEnemy(type,p.x,p.y,raid); }
for(let i=0;i<11;i++)spawnEnemyIn('wolf','forest');
for(let i=0;i<7;i++)spawnEnemyIn('boar','meadow');
for(let i=0;i<7;i++)spawnEnemyIn(i%3===0?'brute':'wolf','quarry');
for(let i=0;i<8;i++)spawnEnemyIn(i%2===0?'brute':'wolf','danger');
function ensureAlpha(){
  if([...enemies.values()].some(e=>e.type==='alpha'))return;
  if(Date.now()<alphaRespawnAt)return;
  const e=spawnEnemy('alpha',3150,480,false);
  broadcast({type:'event',kind:'bossSpawn',x:e.x,y:e.y});
}
ensureAlpha();

function publicPlayer(p){
  const w=weaponInfo(p),craft=nextCraft(p);
  return {id:p.id,name:p.name,x:p.x,y:p.y,hp:p.hp,maxHp:p.maxHp,wood:p.wood,stone:p.stone,meat:p.meat,dir:p.dir,score:p.score,merit:p.merit,gearLevel:p.gearLevel,weapon:w.name,weaponKind:w.kind,carry:carryOf(p),carryCap:carryCap(),zone:zoneAt(p.x,p.y),craft};
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
  const alpha=[...enemies.values()].find(e=>e.type==='alpha');
  return {
    type:'snapshot',worldTick,world:WORLD,zones:ZONES,
    base:{...BASE,upgrade:upgradeProgress()},
    day:{phase:dayPhase(),clock:dayClock,cycle:190},
    boss:alpha?{active:true,id:alpha.id,x:alpha.x,y:alpha.y,hp:alpha.hp,maxHp:alpha.maxHp}:{active:false,respawnAt:alphaRespawnAt},
    players:[...players.values()].map(publicPlayer),
    nodes:nodes.filter(n=>!n.respawnAt).map(n=>({id:n.id,type:n.type,x:n.x,y:n.y,hp:n.hp,maxHp:n.maxHp,r:n.r,zone:n.zone})),
    enemies:[...enemies.values()].map(e=>({id:e.id,type:e.type,x:e.x,y:e.y,hp:e.hp,maxHp:e.maxHp,r:e.r,raid:e.raid,dir:e.dir,boss:e.boss}))
  };
}

function maybeUpgradeBase(){
  const c=baseUpgradeCost(BASE.level);
  if(!c || BASE.level>=5) return;
  if(BASE.wood>=c.wood && BASE.stone>=c.stone && BASE.meat>=c.meat){
    BASE.wood-=c.wood; BASE.stone-=c.stone; BASE.meat-=c.meat; BASE.level++;
    BASE.maxHp += 420 + BASE.level*80; BASE.hp=BASE.maxHp;
    broadcast({type:'event',kind:'upgrade',level:BASE.level});
  }
}
function tryDeposit(p){
  if(Math.hypot(p.x-BASE.x,p.y-BASE.y)>BASE.r+85) return;
  if(carryOf(p)===0) return;
  const payload={wood:p.wood,stone:p.stone,meat:p.meat};
  BASE.wood+=p.wood; BASE.stone+=p.stone; BASE.meat+=p.meat;
  p.score += p.wood*2+p.stone*3+p.meat*4;
  p.merit += Math.ceil((p.wood+p.stone+p.meat)/3);
  p.wood=p.stone=p.meat=0;
  broadcast({type:'event',kind:'deposit',playerId:p.id,...payload,merit:p.merit});
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
function nearestNode(p,max=108){
  let best=null,bd=max;
  for(const n of nodes){if(n.respawnAt)continue;const d=Math.hypot(n.x-p.x,n.y-p.y);if(d<bd){best=n;bd=d;}}
  return best;
}
function hitNode(p){
  const best=nearestNode(p);if(!best)return false;
  const power=1+Math.floor((BASE.level-1)/2)+(p.gearLevel>=2?1:0);
  best.hp-=power;
  broadcast({type:'event',kind:'impact',x:best.x,y:best.y,target:best.type,playerId:p.id});
  if(best.hp<=0){
    let kind,amount;
    if(best.type==='tree'){kind='wood';amount=6+Math.floor(Math.random()*4)+Math.floor(BASE.level/2);}
    if(best.type==='rock'){kind='stone';amount=5+Math.floor(Math.random()*4)+Math.floor(BASE.level/2);}
    if(best.type==='ore'){kind='stone';amount=9+Math.floor(Math.random()*5)+BASE.level;}
    if(best.type==='berry'){kind='meat';amount=2+Math.floor(BASE.level/3);}
    const got=addCarry(p,kind,amount);
    p.score+=got;p.merit+=best.type==='ore'?3:1;
    best.respawnAt=Date.now()+38000+Math.random()*18000;best.hp=best.maxHp;
    broadcast({type:'event',kind:'gather',playerId:p.id,nodeType:best.type,resource:kind,amount:got,merit:p.merit,x:best.x,y:best.y});
  }
  return true;
}
function finishEnemy(p,e){
  enemies.delete(e.id);
  const reward=e.type==='alpha'?24:e.type==='brute'?12:e.type==='boar'?9:6;
  const amount=addCarry(p,'meat',reward);
  const meritGain=e.type==='alpha'?45:e.type==='brute'?10:e.type==='boar'?6:4;
  p.merit+=meritGain;p.score+=18+amount*2+meritGain;
  broadcast({type:'event',kind:'kill',playerId:p.id,enemyType:e.type,amount,meritGain,x:e.x,y:e.y});
  if(e.type==='alpha'){
    alphaRespawnAt=Date.now()+90000;
    broadcast({type:'event',kind:'bossDown',playerId:p.id,respawnAt:alphaRespawnAt});
    return;
  }
  if(!e.raid)setTimeout(()=>{
    const z=e.type==='brute'?'danger':e.type==='boar'?'meadow':'forest';
    const pt=pointForZone(z);spawnEnemy(Math.random()<.22?'boar':e.type,pt.x,pt.y,false);
  },13000);
}
function hitEnemyMelee(p){
  const w=weaponInfo(p);let best=null,bd=w.range;
  for(const e of enemies.values()){const d=Math.hypot(e.x-p.x,e.y-p.y);if(d<bd){best=e;bd=d;}}
  if(!best)return false;
  best.hp-=w.damage;
  const dx=best.x-p.x,dy=best.y-p.y,dl=Math.hypot(dx,dy)||1;best.x+=dx/dl*20;best.y+=dy/dl*20;
  broadcast({type:'event',kind:'slash',x:best.x,y:best.y,targetId:best.id,playerId:p.id,damage:w.damage});
  if(best.hp<=0)finishEnemy(p,best);
  return true;
}
function hitEnemyRanged(p){
  const w=weaponInfo(p);let best=null,score=Infinity;
  for(const e of enemies.values()){
    const dx=e.x-p.x,dy=e.y-p.y,d=Math.hypot(dx,dy);if(d>w.range)continue;
    const ang=Math.abs(Math.atan2(Math.sin(Math.atan2(dy,dx)-p.dir),Math.cos(Math.atan2(dy,dx)-p.dir)));
    const s=d+(ang>.9?250:ang*70);if(s<score){score=s;best=e;}
  }
  if(!best)return false;
  best.hp-=w.damage;
  broadcast({type:'event',kind:'projectile',weapon:p.gearLevel===4?'bolt':'arrow',x1:p.x,y1:p.y,x2:best.x,y2:best.y,targetId:best.id,playerId:p.id,damage:w.damage});
  if(best.hp<=0)finishEnemy(p,best);
  return true;
}
function attack(p){
  const w=weaponInfo(p),now=Date.now();if(now-p.lastAttack<w.cooldown)return;p.lastAttack=now;
  broadcast({type:'event',kind:'swing',playerId:p.id,dir:p.dir,tier:p.gearLevel,ranged:w.kind==='ranged'});
  const hitEnemy=w.kind==='ranged'?hitEnemyRanged(p):hitEnemyMelee(p);
  if(!hitEnemy)hitNode(p);
}
function craft(p){
  if(Math.hypot(p.x-BASE.x,p.y-BASE.y)>BASE.r+115){send(p.ws,{type:'event',kind:'craftDenied',reason:'거점 작업대로 돌아가세요'});return;}
  const c=nextCraft(p);if(!c){send(p.ws,{type:'event',kind:'craftDenied',reason:'현재 최고 장비입니다'});return;}
  if(BASE.level<c.base){send(p.ws,{type:'event',kind:'craftDenied',reason:`거점 LV.${c.base}에서 제작 가능`});return;}
  if(p.merit<c.merit){send(p.ws,{type:'event',kind:'craftDenied',reason:`공헌도 ${c.merit} 필요 · 현재 ${p.merit}`});return;}
  p.merit-=c.merit;p.gearLevel++;
  send(p.ws,{type:'event',kind:'crafted',gearLevel:p.gearLevel,weapon:weaponInfo(p).name,merit:p.merit});
  broadcast({type:'event',kind:'playerCrafted',playerId:p.id,weapon:weaponInfo(p).name});
}
function spawnRaid(){
  raidSeq++;
  const count=5+BASE.level*3+Math.min(10,players.size*2);
  for(let i=0;i<count;i++){
    const a=Math.random()*Math.PI*2,radius=900+Math.random()*220;
    const type=i%5===0&&BASE.level>=2?'brute':'wolf';
    spawnEnemy(type,BASE.x+Math.cos(a)*radius,BASE.y+Math.sin(a)*radius,true);
  }
  if(BASE.level>=4&&raidSeq%3===0){const a=Math.random()*Math.PI*2;spawnEnemy('alpha',BASE.x+Math.cos(a)*1080,BASE.y+Math.sin(a)*1080,true);}
  broadcast({type:'event',kind:'raid',raid:raidSeq,count});
}
function baseTowerFire(dt){
  if(BASE.level<3||dayPhase()!=='night')return;
  if(!baseTowerFire.cd)baseTowerFire.cd=0;baseTowerFire.cd-=dt;if(baseTowerFire.cd>0)return;
  let target=null,td=430;
  for(const e of enemies.values()){if(!e.raid)continue;const d=Math.hypot(e.x-BASE.x,e.y-BASE.y);if(d<td){td=d;target=e;}}
  if(!target)return;baseTowerFire.cd=Math.max(.4,1.05-BASE.level*.12);target.hp-=18+BASE.level*4;
  broadcast({type:'event',kind:'towerShot',x1:BASE.x,y1:BASE.y,x2:target.x,y2:target.y});
  if(target.hp<=0){enemies.delete(target.id);if(target.type==='alpha')alphaRespawnAt=Date.now()+90000;}
}

wss.on('connection',ws=>{
  const pid=id();
  const p={id:pid,ws,name:`생존자-${pid.slice(0,3)}`,x:BASE.x+rand(-75,75),y:BASE.y+rand(-75,75),hp:100,maxHp:100,wood:0,stone:0,meat:0,dir:0,lastAttack:0,input:{x:0,y:0},score:0,merit:0,gearLevel:1};
  players.set(pid,p);send(ws,{type:'welcome',id:pid});send(ws,snapshot());broadcast({type:'event',kind:'join',player:publicPlayer(p)});
  ws.on('message',raw=>{
    let m;try{m=JSON.parse(raw);}catch{return;}
    if(m.type==='input'){
      p.input.x=clamp(Number(m.x)||0,-1,1);p.input.y=clamp(Number(m.y)||0,-1,1);
      if(Math.hypot(p.input.x,p.input.y)>1){const l=Math.hypot(p.input.x,p.input.y);p.input.x/=l;p.input.y/=l;}
    }
    if(m.type==='attack')attack(p);
    if(m.type==='deposit')tryDeposit(p);
    if(m.type==='craft')craft(p);
    if(m.type==='name'&&typeof m.name==='string')p.name=m.name.trim().slice(0,14)||p.name;
  });
  ws.on('close',()=>{players.delete(pid);broadcast({type:'event',kind:'leave',playerId:pid});});
});

let last=Date.now();
setInterval(()=>{
  const now=Date.now(),dt=Math.min(.05,(now-last)/1000);last=now;worldTick++;dayClock=(dayClock+dt)%190;
  const phase=dayPhase();
  if(phase==='night'&&!raidStartedThisNight){raidStartedThisNight=true;spawnRaid();}
  if(phase==='day')raidStartedThisNight=false;
  if(phase==='day')BASE.hp=Math.min(BASE.maxHp,BASE.hp+2.2*dt);
  ensureAlpha();

  for(const p of players.values()){
    const z=zoneAt(p.x,p.y),speed=z==='quarry'?212:z==='danger'?218:224;
    p.x=clamp(p.x+p.input.x*speed*dt,35,WORLD.w-35);p.y=clamp(p.y+p.input.y*speed*dt,35,WORLD.h-35);
    if(Math.hypot(p.input.x,p.input.y)>.08)p.dir=Math.atan2(p.input.y,p.input.x);
    if(Math.hypot(p.x-BASE.x,p.y-BASE.y)<BASE.r+52){p.hp=Math.min(p.maxHp,p.hp+12*dt);if(carryOf(p)>0)tryDeposit(p);}
  }

  for(const e of enemies.values()){
    e.attackCd=Math.max(0,e.attackCd-dt);
    let target=null,td=Infinity;
    for(const p of players.values()){const d=dist(e,p);if(d<td){td=d;target=p;}}
    const db=Math.hypot(e.x-BASE.x,e.y-BASE.y);
    if(e.raid&&(db<td||!target)){target=BASE;td=db;}
    if(target&&(td<e.aggro||e.raid)){
      const dx=target.x-e.x,dy=target.y-e.y,l=Math.hypot(dx,dy)||1;e.dir=Math.atan2(dy,dx);
      if(td>(target===BASE?BASE.r*.7+e.r:42)){e.x+=dx/l*e.speed*dt;e.y+=dy/l*e.speed*dt;}
      else if(e.attackCd<=0){
        e.attackCd=e.type==='alpha'?1.05:.82;
        if(target===BASE){BASE.hp=Math.max(0,BASE.hp-e.damage);broadcast({type:'event',kind:'baseHit',hp:BASE.hp,x:e.x,y:e.y});if(BASE.hp<=0){BASE.hp=BASE.maxHp*.45;broadcast({type:'event',kind:'baseBreach'});}}
        else {target.hp=Math.max(0,target.hp-e.damage);broadcast({type:'event',kind:'hurt',playerId:target.id,amount:e.damage});if(target.hp<=0){target.hp=target.maxHp;target.x=BASE.x;target.y=BASE.y;target.wood=Math.floor(target.wood*.6);target.stone=Math.floor(target.stone*.6);target.meat=Math.floor(target.meat*.6);broadcast({type:'event',kind:'down',playerId:target.id});}}
      }
    } else {
      e.wander+=dt;e.dir=e.wander*.65+e.id;e.x=clamp(e.x+Math.cos(e.dir)*e.speed*.11*dt,80,WORLD.w-80);e.y=clamp(e.y+Math.sin(e.dir)*e.speed*.11*dt,80,WORLD.h-80);
    }
  }
  baseTowerFire(dt);
  for(const n of nodes)if(n.respawnAt&&n.respawnAt<now){n.respawnAt=0;n.hp=n.maxHp;}
  if(worldTick%3===0)broadcast(snapshot());
},1000/30);

server.listen(PORT,()=>console.log(`Outpost Wilds listening on ${PORT}`));
