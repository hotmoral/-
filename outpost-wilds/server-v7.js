const express=require('express');
const http=require('http');
const path=require('path');
const{WebSocketServer}=require('ws');

const app=express(),server=http.createServer(app),wss=new WebSocketServer({server});
app.use(express.static(path.join(__dirname,'public')));
const PORT=process.env.PORT||3000,WORLD={w:3600,h:3600};
const BASE={x:1800,y:1800,r:255,hp:1100,maxHp:1100,level:1};
const ZONES=[
 {id:'camp',name:'개척 거점',hint:'안전지대 · 건설 칸에 자원 투입',color:'#775b39'},
 {id:'meadow',name:'바람 초원',hint:'초급 자원 · 늑대와 멧돼지',color:'#476a3d'},
 {id:'forest',name:'검은솔 숲',hint:'목재 밀집 · 포식자 주의',color:'#244b31'},
 {id:'quarry',name:'붉은 채석지',hint:'석재/광맥 밀집 · 야수 출몰',color:'#5c5145'},
 {id:'danger',name:'황폐 경계',hint:'고위험 · 우두머리 출몰',color:'#443735'}
];

const players=new Map(),nodes=[],enemies=new Map();
let nextEnemyId=1,worldTick=0,dayClock=12,raidSeq=0,raidStartedThisNight=false,alphaRespawnAt=0;

const FACILITY_DEF={
 workshop:{label:'작업대',cost:{wood:45,stone:25,meat:0},base:2,requires:[]},
 storage:{label:'보급 창고',cost:{wood:55,stone:30,meat:0},base:2,requires:[]},
 farm:{label:'농장',cost:{wood:55,stone:25,meat:10},base:2,requires:['workshop']},
 watchtower:{label:'망루',cost:{wood:70,stone:40,meat:15},base:2,requires:['workshop']},
 forge:{label:'대장간',cost:{wood:85,stone:90,meat:20},base:3,requires:['workshop']},
 infirmary:{label:'회복소',cost:{wood:70,stone:55,meat:30},base:3,requires:['workshop']},
 wall:{label:'방벽 강화',cost:{wood:95,stone:120,meat:20},base:3,requires:['watchtower']},
 turret:{label:'자동 터렛',cost:{wood:120,stone:150,meat:35},base:4,requires:['watchtower','forge']},
 turret2:{label:'외곽 터렛',cost:{wood:155,stone:190,meat:45},base:5,requires:['turret','wall']}
};
const facilities=Object.fromEntries(Object.keys(FACILITY_DEF).map(k=>[k,false]));
const facilityProgress=Object.fromEntries(Object.keys(FACILITY_DEF).map(k=>[k,{wood:0,stone:0,meat:0}]));
let baseProgress={wood:0,stone:0,meat:0};
const PAD_POS={
 base:{x:1800,y:2045},gear:{x:1800,y:1545},
 workshop:{x:1575,y:1900},storage:{x:1510,y:1770},farm:{x:1540,y:2070},
 watchtower:{x:2040,y:1670},forge:{x:1580,y:1645},infirmary:{x:2090,y:1780},
 wall:{x:2200,y:2020},turret:{x:2050,y:1910},turret2:{x:2070,y:2150}
};

const rand=(a,b)=>a+Math.random()*(b-a),clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y),id=()=>Math.random().toString(36).slice(2,10);
const send=(ws,p)=>ws.readyState===1&&ws.send(JSON.stringify(p));
const broadcast=p=>{const s=JSON.stringify(p);for(const c of wss.clients)if(c.readyState===1)c.send(s)};
const carryOf=p=>p.wood+p.stone+p.meat;
const carryCap=()=>30+BASE.level*10+(facilities.storage?15:0);

function zoneAt(x,y){const d=Math.hypot(x-BASE.x,y-BASE.y);if(d<470)return'camp';if(d>1320)return'danger';if(x<1420)return'forest';if(x>2260)return'quarry';return'meadow'}
function pointForZone(zone){for(let i=0;i<800;i++){const x=rand(120,3480),y=rand(120,3480);if(zoneAt(x,y)===zone)return{x,y}}return{x:rand(160,3440),y:rand(160,3440)}}
function weaponInfo(p){return[
 null,
 {name:'조잡한 창',kind:'melee',damage:18,range:116,autoRange:120,cooldown:330},
 {name:'강화 창',kind:'melee',damage:27,range:128,autoRange:132,cooldown:300},
 {name:'사냥 활',kind:'ranged',damage:25,range:430,autoRange:350,cooldown:540},
 {name:'철제 석궁',kind:'ranged',damage:39,range:560,autoRange:410,cooldown:430},
 {name:'연발 석궁',kind:'ranged',damage:52,range:620,autoRange:455,cooldown:330}
 ][p.gearLevel]||null}
function baseCost(){return[null,{wood:70,stone:35,meat:18},{wood:150,stone:100,meat:40},{wood:240,stone:200,meat:80},{wood:390,stone:350,meat:140}][BASE.level]||null}
function gearDef(p){return{
 2:{name:'강화 창',cost:{wood:25,stone:15,meat:0},base:2,requires:['workshop']},
 3:{name:'사냥 활',cost:{wood:35,stone:40,meat:10},base:3,requires:['forge']},
 4:{name:'철제 석궁',cost:{wood:60,stone:75,meat:20},base:4,requires:['turret']},
 5:{name:'연발 석궁',cost:{wood:90,stone:120,meat:35},base:5,requires:['turret2']}
 }[p.gearLevel+1]||null}
function reqReason(def){if(BASE.level<def.base)return`거점 LV.${def.base} 필요`;for(const r of def.requires)if(!facilities[r])return`${FACILITY_DEF[r].label} 선행 건설 필요`;return''}
function baseReqReason(){if(BASE.level===2&&(!facilities.workshop||!facilities.storage))return'작업대 + 보급 창고 필요';if(BASE.level===3&&(!facilities.watchtower||!facilities.forge||!facilities.infirmary))return'망루 + 대장간 + 회복소 필요';if(BASE.level===4&&(!facilities.turret||!facilities.wall||!facilities.farm))return'자동 터렛 + 방벽 + 농장 필요';return''}
function publicPads(p){const out=[],bc=baseCost(),bReason=baseReqReason();out.push({id:'base',kind:'base',label:BASE.level>=5?'거점 최대 레벨':`거점 LV.${BASE.level+1}`,x:PAD_POS.base.x,y:PAD_POS.base.y,size:112,cost:bc,progress:{...baseProgress},complete:BASE.level>=5,locked:!!bReason,reason:bReason});
 for(const[k,d]of Object.entries(FACILITY_DEF)){const reason=facilities[k]?'':reqReason(d);out.push({id:k,kind:'facility',label:d.label,x:PAD_POS[k].x,y:PAD_POS[k].y,size:104,cost:d.cost,progress:{...facilityProgress[k]},complete:facilities[k],locked:!facilities[k]&&!!reason,reason})}
 const gd=gearDef(p),gp=p.gearProgress||{wood:0,stone:0,meat:0};out.push({id:'gear',kind:'gear',label:gd?`장비 → ${gd.name}`:'최고 장비',x:PAD_POS.gear.x,y:PAD_POS.gear.y,size:108,cost:gd?.cost||null,progress:{...gp},complete:!gd,locked:!!gd&&!!reqReason(gd),reason:gd?reqReason(gd):''});return out}
function publicPlayer(p){const w=weaponInfo(p);return{id:p.id,name:p.name,x:p.x,y:p.y,hp:p.hp,maxHp:p.maxHp,wood:p.wood,stone:p.stone,meat:p.meat,dir:p.facing>0?0:Math.PI,facing:p.facing,score:p.score,merit:p.merit,gearLevel:p.gearLevel,weapon:w.name,weaponKind:w.kind,carry:carryOf(p),carryCap:carryCap(),zone:zoneAt(p.x,p.y),autoTarget:p.autoTarget||null}}

function nodeConfig(t){if(t==='tree')return{hp:6,r:30};if(t==='rock')return{hp:8,r:26};if(t==='ore')return{hp:11,r:27};return{hp:4,r:22}}
function spawnNode(type,count,zone){const c=nodeConfig(type);for(let i=0;i<count;i++){const p=pointForZone(zone);nodes.push({id:id(),type,x:p.x,y:p.y,hp:c.hp,maxHp:c.hp,r:c.r,respawnAt:0,zone})}}
spawnNode('tree',95,'forest');spawnNode('tree',46,'meadow');spawnNode('tree',30,'danger');spawnNode('rock',68,'quarry');spawnNode('rock',27,'meadow');spawnNode('rock',24,'danger');spawnNode('ore',28,'quarry');spawnNode('ore',14,'danger');spawnNode('berry',34,'meadow');spawnNode('berry',18,'forest');

function enemyConfig(t){if(t==='wolf')return{hp:46,speed:118,damage:8,r:21,aggro:540};if(t==='boar')return{hp:76,speed:90,damage:12,r:26,aggro:500};if(t==='brute')return{hp:126,speed:78,damage:18,r:30,aggro:590};return{hp:420,speed:86,damage:26,r:46,aggro:720}}
function spawnEnemy(type,x,y,raid=false){const c=enemyConfig(type),e={id:nextEnemyId++,type,x,y,hp:c.hp,maxHp:c.hp,speed:c.speed,damage:c.damage,r:c.r,aggro:c.aggro,raid,attackCd:0,wander:Math.random()*10,dir:0,boss:type==='alpha'};enemies.set(e.id,e);return e}
function spawnEnemyIn(t,z,r=false){const p=pointForZone(z);return spawnEnemy(t,p.x,p.y,r)}
for(let i=0;i<11;i++)spawnEnemyIn('wolf','forest');for(let i=0;i<7;i++)spawnEnemyIn('boar','meadow');for(let i=0;i<7;i++)spawnEnemyIn(i%3===0?'brute':'wolf','quarry');for(let i=0;i<8;i++)spawnEnemyIn(i%2===0?'brute':'wolf','danger');
function ensureAlpha(){if([...enemies.values()].some(e=>e.type==='alpha')||Date.now()<alphaRespawnAt)return;const e=spawnEnemy('alpha',3150,480);broadcast({type:'event',kind:'bossSpawn',x:e.x,y:e.y})}ensureAlpha();
function dayPhase(){const t=dayClock%190;if(t<112)return'day';if(t<132)return'dusk';if(t<178)return'night';return'dawn'}
function padsForSnapshot(){const any=[...players.values()][0]||{gearLevel:1,gearProgress:{wood:0,stone:0,meat:0}};return publicPads(any).filter(p=>p.kind!=='gear')}
function snapshot(){const a=[...enemies.values()].find(e=>e.type==='alpha');return{type:'snapshot',worldTick,world:WORLD,zones:ZONES,base:{...BASE},facilities:{...facilities},day:{phase:dayPhase(),clock:dayClock,cycle:190},boss:a?{active:true,id:a.id,x:a.x,y:a.y,hp:a.hp,maxHp:a.maxHp}:{active:false,respawnAt:alphaRespawnAt},players:[...players.values()].map(publicPlayer),nodes:nodes.filter(n=>!n.respawnAt).map(n=>({id:n.id,type:n.type,x:n.x,y:n.y,hp:n.hp,maxHp:n.maxHp,r:n.r,zone:n.zone})),enemies:[...enemies.values()].map(e=>({id:e.id,type:e.type,x:e.x,y:e.y,hp:e.hp,maxHp:e.maxHp,r:e.r,raid:e.raid,dir:e.dir,boss:e.boss})),pads:padsForSnapshot()}}

function addCarry(p,t,a){const free=Math.max(0,carryCap()-carryOf(p)),g=Math.min(free,a);if(g<=0){broadcast({type:'event',kind:'carryFull',playerId:p.id});return 0}p[t]+=g;return g}
function nearestNode(p,max=112){if(carryOf(p)>=carryCap())return null;let b=null,d=max;for(const n of nodes){if(n.respawnAt)continue;const q=Math.hypot(n.x-p.x,n.y-p.y);if(q<d){b=n;d=q}}return b}
function gatherNode(p,n){const now=Date.now();p.facing=n.x<p.x?-1:1;p.autoTarget={kind:'resource',id:n.id};if(now-p.lastGather<360)return false;p.lastGather=now;const power=1+Math.floor((BASE.level-1)/2)+(p.gearLevel>=2?1:0);n.hp-=power;broadcast({type:'event',kind:'swing',playerId:p.id,dir:p.facing>0?0:Math.PI,tier:p.gearLevel,ranged:false,auto:true});broadcast({type:'event',kind:'impact',x:n.x,y:n.y,target:n.type,playerId:p.id});if(n.hp<=0){let kind,amount;if(n.type==='tree'){kind='wood';amount=6+Math.floor(Math.random()*4)+Math.floor(BASE.level/2)}if(n.type==='rock'){kind='stone';amount=5+Math.floor(Math.random()*4)+Math.floor(BASE.level/2)}if(n.type==='ore'){kind='stone';amount=9+Math.floor(Math.random()*5)+BASE.level}if(n.type==='berry'){kind='meat';amount=2+Math.floor(BASE.level/3)}const got=addCarry(p,kind,amount);p.score+=got;p.merit+=n.type==='ore'?3:1;n.respawnAt=Date.now()+38000+Math.random()*18000;n.hp=n.maxHp;broadcast({type:'event',kind:'gather',playerId:p.id,nodeType:n.type,resource:kind,amount:got,merit:p.merit,x:n.x,y:n.y})}return true}

function finishEnemy(p,e){enemies.delete(e.id);const reward=e.type==='alpha'?24:e.type==='brute'?12:e.type==='boar'?9:6,amount=addCarry(p,'meat',reward),mg=e.type==='alpha'?45:e.type==='brute'?10:e.type==='boar'?6:4;p.merit+=mg;p.score+=18+amount*2+mg;broadcast({type:'event',kind:'kill',playerId:p.id,enemyType:e.type,amount,meritGain:mg,x:e.x,y:e.y});if(e.type==='alpha'){alphaRespawnAt=Date.now()+90000;broadcast({type:'event',kind:'bossDown',playerId:p.id,respawnAt:alphaRespawnAt});return}if(!e.raid)setTimeout(()=>{const z=e.type==='brute'?'danger':e.type==='boar'?'meadow':'forest',pt=pointForZone(z);spawnEnemy(Math.random()<.22?'boar':e.type,pt.x,pt.y)},13000)}
function nearestEnemy(p,range){let b=null,d=range;for(const e of enemies.values()){const q=dist(e,p);if(q<d){b=e;d=q}}return b}
function attackEnemy(p,e){const w=weaponInfo(p),now=Date.now();if(!e)return false;p.facing=e.x<p.x?-1:1;p.autoTarget={kind:'enemy',id:e.id};if(now-p.lastAttack<w.cooldown)return false;p.lastAttack=now;broadcast({type:'event',kind:'swing',playerId:p.id,dir:p.facing>0?0:Math.PI,tier:p.gearLevel,ranged:w.kind==='ranged',auto:true});if(w.kind==='ranged'){e.hp-=w.damage;broadcast({type:'event',kind:'projectile',weapon:p.gearLevel>=4?'bolt':'arrow',x1:p.x,y1:p.y,x2:e.x,y2:e.y,targetId:e.id,playerId:p.id,damage:w.damage});if(e.hp<=0)finishEnemy(p,e);return true}e.hp-=w.damage;const dx=e.x-p.x,dy=e.y-p.y,l=Math.hypot(dx,dy)||1;e.x+=dx/l*20;e.y+=dy/l*20;broadcast({type:'event',kind:'slash',x:e.x,y:e.y,targetId:e.id,playerId:p.id,damage:w.damage});if(e.hp<=0)finishEnemy(p,e);return true}

function remaining(cost,prog,k){return Math.max(0,(cost?.[k]||0)-(prog?.[k]||0))}
function takeForProject(p,cost,prog,rate=3){let total=0;for(const k of['wood','stone','meat']){const n=Math.min(p[k],remaining(cost,prog,k),rate);if(n>0){p[k]-=n;prog[k]+=n;total+=n}}return total}
function done(cost,prog){return['wood','stone','meat'].every(k=>(prog[k]||0)>=(cost[k]||0))}
function insidePad(p,pos,size=104){return Math.abs(p.x-pos.x)<=size*.52&&Math.abs(p.y-pos.y)<=size*.52}
function completeFacility(fid,p){facilities[fid]=true;if(fid==='wall'){BASE.maxHp+=600;BASE.hp=Math.min(BASE.maxHp,BASE.hp+600)}broadcast({type:'event',kind:'constructionComplete',project:fid,label:FACILITY_DEF[fid].label,x:PAD_POS[fid].x,y:PAD_POS[fid].y,playerId:p.id})}
function completeBase(p){BASE.level++;BASE.maxHp+=420+BASE.level*80;BASE.hp=BASE.maxHp;baseProgress={wood:0,stone:0,meat:0};broadcast({type:'event',kind:'upgrade',level:BASE.level,playerId:p.id,x:PAD_POS.base.x,y:PAD_POS.base.y})}
function processPads(p,now){if(now-(p.lastPad||0)<180)return false;let active=null;const bc=baseCost(),br=baseReqReason();if(bc&&insidePad(p,PAD_POS.base,112)&&!br)active={id:'base',cost:bc,prog:baseProgress,type:'base'};
 if(!active)for(const[k,d]of Object.entries(FACILITY_DEF)){if(facilities[k]||reqReason(d))continue;if(insidePad(p,PAD_POS[k],104)){active={id:k,cost:d.cost,prog:facilityProgress[k],type:'facility'};break}}
 if(!active){const gd=gearDef(p);if(gd&&!reqReason(gd)&&insidePad(p,PAD_POS.gear,108)){if(!p.gearProgress||p.gearTarget!==p.gearLevel+1){p.gearTarget=p.gearLevel+1;p.gearProgress={wood:0,stone:0,meat:0}}active={id:'gear',cost:gd.cost,prog:p.gearProgress,type:'gear',gd}}}
 if(!active)return false;p.lastPad=now;const used=takeForProject(p,active.cost,active.prog,3);if(used<=0)return false;p.autoTarget={kind:'pad',id:active.id};p.merit+=used;broadcast({type:'event',kind:'padDeposit',project:active.id,playerId:p.id,amount:used,x:PAD_POS[active.id].x,y:PAD_POS[active.id].y});if(done(active.cost,active.prog)){if(active.type==='base')completeBase(p);else if(active.type==='facility')completeFacility(active.id,p);else{p.gearLevel++;p.gearProgress={wood:0,stone:0,meat:0};p.gearTarget=p.gearLevel+1;broadcast({type:'event',kind:'gearUpgrade',playerId:p.id,weapon:weaponInfo(p).name,x:PAD_POS.gear.x,y:PAD_POS.gear.y})}}return true}
function processFarm(p,now){if(!facilities.farm||!insidePad(p,PAD_POS.farm,112)||now-(p.lastFarm||0)<1300||carryOf(p)>=carryCap())return false;p.lastFarm=now;const got=addCarry(p,'meat',1);if(got){p.autoTarget={kind:'facility',id:'farm'};broadcast({type:'event',kind:'gather',playerId:p.id,nodeType:'farm',resource:'meat',amount:got,merit:p.merit,x:PAD_POS.farm.x,y:PAD_POS.farm.y});return true}return false}
function autoAction(p,now){p.autoTarget=null;const w=weaponInfo(p),enemy=nearestEnemy(p,w.autoRange);if(enemy){attackEnemy(p,enemy);return'enemy'}const node=nearestNode(p,114);if(node){gatherNode(p,node);return'resource'}if(processPads(p,now))return'pad';if(processFarm(p,now))return'farm';return null}

function spawnRaid(){raidSeq++;const count=5+BASE.level*3+Math.min(10,players.size*2);for(let i=0;i<count;i++){const a=Math.random()*Math.PI*2,r=900+Math.random()*220,t=i%5===0&&BASE.level>=2?'brute':'wolf';spawnEnemy(t,BASE.x+Math.cos(a)*r,BASE.y+Math.sin(a)*r,true)}if(BASE.level>=4&&raidSeq%3===0){const a=Math.random()*Math.PI*2;spawnEnemy('alpha',BASE.x+Math.cos(a)*1080,BASE.y+Math.sin(a)*1080,true)}broadcast({type:'event',kind:'raid',raid:raidSeq,count})}
function defenseFire(dt){if(!defenseFire.cd)defenseFire.cd={watchtower:0,turret:0,turret2:0};for(const k of Object.keys(defenseFire.cd))defenseFire.cd[k]-=dt;const fire=(fid,range,damage,all,cd)=>{if(!facilities[fid]||defenseFire.cd[fid]>0)return;let target=null,d=range;for(const e of enemies.values()){if(!all&&!e.raid)continue;const q=Math.hypot(e.x-PAD_POS[fid].x,e.y-PAD_POS[fid].y);if(q<d){d=q;target=e}}if(!target)return;defenseFire.cd[fid]=cd;target.hp-=damage;broadcast({type:'event',kind:'towerShot',source:fid,x1:PAD_POS[fid].x,y1:PAD_POS[fid].y,x2:target.x,y2:target.y});if(target.hp<=0){enemies.delete(target.id);if(target.type==='alpha')alphaRespawnAt=Date.now()+90000}};fire('watchtower',470,24,false,.95);fire('turret',570,36,true,.46);fire('turret2',620,42,true,.38)}

wss.on('connection',ws=>{const pid=id(),p={id:pid,ws,name:`생존자-${pid.slice(0,3)}`,x:BASE.x+rand(-75,75),y:BASE.y+rand(-75,75),hp:100,maxHp:100,wood:0,stone:0,meat:0,facing:1,lastAttack:0,lastGather:0,lastPad:0,lastFarm:0,input:{x:0,y:0},score:0,merit:0,gearLevel:1,gearTarget:2,gearProgress:{wood:0,stone:0,meat:0},autoTarget:null};players.set(pid,p);send(ws,{type:'welcome',id:pid});send(ws,{...snapshot(),personalPads:publicPads(p).filter(x=>x.kind==='gear')});broadcast({type:'event',kind:'join',player:publicPlayer(p)});ws.on('message',raw=>{let m;try{m=JSON.parse(raw)}catch{return}if(m.type==='input'){p.input.x=clamp(Number(m.x)||0,-1,1);p.input.y=clamp(Number(m.y)||0,-1,1);if(Math.hypot(p.input.x,p.input.y)>1){const l=Math.hypot(p.input.x,p.input.y);p.input.x/=l;p.input.y/=l}}if(m.type==='name'&&typeof m.name==='string')p.name=m.name.trim().slice(0,14)||p.name});ws.on('close',()=>{players.delete(pid);broadcast({type:'event',kind:'leave',playerId:pid})})});

let last=Date.now();
setInterval(()=>{const now=Date.now(),dt=Math.min(.05,(now-last)/1000);last=now;worldTick++;dayClock=(dayClock+dt)%190;const phase=dayPhase();if(phase==='night'&&!raidStartedThisNight){raidStartedThisNight=true;spawnRaid()}if(phase==='day')raidStartedThisNight=false;if(phase==='day')BASE.hp=Math.min(BASE.maxHp,BASE.hp+2.2*dt);ensureAlpha();
 for(const p of players.values()){const q=Math.max(0,Math.min(1,carryOf(p)/carryCap())),speed=212*Math.max(.86,1-.14*Math.pow(q,1.35));p.x=clamp(p.x+p.input.x*speed*dt,35,WORLD.w-35);p.y=clamp(p.y+p.input.y*speed*dt,35,WORLD.h-35);if(Math.abs(p.input.x)>.08)p.facing=p.input.x<0?-1:1;const heal=facilities.infirmary?24:12;if(Math.hypot(p.x-BASE.x,p.y-BASE.y)<BASE.r+52)p.hp=Math.min(p.maxHp,p.hp+heal*dt);autoAction(p,now)}
 for(const e of enemies.values()){e.attackCd=Math.max(0,e.attackCd-dt);let target=null,td=Infinity;for(const p of players.values()){const d=dist(e,p);if(d<td){td=d;target=p}}const db=Math.hypot(e.x-BASE.x,e.y-BASE.y);if(e.raid&&(db<td||!target)){target=BASE;td=db}if(target&&(td<e.aggro||e.raid)){const dx=target.x-e.x,dy=target.y-e.y,l=Math.hypot(dx,dy)||1;e.dir=Math.atan2(dy,dx);if(td>(target===BASE?BASE.r*.7+e.r:42)){e.x+=dx/l*e.speed*dt;e.y+=dy/l*e.speed*dt}else if(e.attackCd<=0){e.attackCd=e.type==='alpha'?1.05:.82;if(target===BASE){BASE.hp=Math.max(0,BASE.hp-e.damage);broadcast({type:'event',kind:'baseHit',hp:BASE.hp,x:e.x,y:e.y});if(BASE.hp<=0){BASE.hp=BASE.maxHp*.45;broadcast({type:'event',kind:'baseBreach'})}}else{target.hp=Math.max(0,target.hp-e.damage);broadcast({type:'event',kind:'hurt',playerId:target.id,amount:e.damage});if(target.hp<=0){target.hp=target.maxHp;target.x=BASE.x;target.y=BASE.y;target.wood=Math.floor(target.wood*.6);target.stone=Math.floor(target.stone*.6);target.meat=Math.floor(target.meat*.6);broadcast({type:'event',kind:'down',playerId:target.id})}}}}else{e.wander+=dt;e.dir=e.wander*.65+e.id;e.x=clamp(e.x+Math.cos(e.dir)*e.speed*.11*dt,80,WORLD.w-80);e.y=clamp(e.y+Math.sin(e.dir)*e.speed*.11*dt,80,WORLD.h-80)}}
 defenseFire(dt);for(const n of nodes)if(n.respawnAt&&n.respawnAt<now){n.respawnAt=0;n.hp=n.maxHp}if(worldTick%3===0){for(const p of players.values())send(p.ws,{...snapshot(),personalPads:publicPads(p).filter(x=>x.kind==='gear')})}
},1000/30);

server.listen(PORT,()=>console.log(`Outpost Wilds V7 listening on ${PORT}`));
