const express=require('express');
const http=require('http');
const path=require('path');
const{WebSocketServer}=require('ws');
const app=express(),server=http.createServer(app),wss=new WebSocketServer({server});
app.use(express.static(path.join(__dirname,'public')));
const PORT=process.env.PORT||3000,WORLD={w:3600,h:3600};
const BASE={x:1800,y:1800,r:255,hp:1100,maxHp:1100,level:1};
const ZONES=[
 {id:'camp',name:'개척 거점',hint:'안전지대 · 건물/거점 칸에 자원 투입',color:'#775b39'},
 {id:'meadow',name:'바람 초원',hint:'초급 자원 · 거점을 노리는 야수',color:'#476a3d'},
 {id:'forest',name:'검은솔 숲',hint:'목재 밀집 · 적의 진격로',color:'#244b31'},
 {id:'quarry',name:'붉은 채석지',hint:'석재/광맥 밀집 · 중장갑 야수',color:'#5c5145'},
 {id:'danger',name:'황폐 경계',hint:'고위험 · 정예/우두머리 출현',color:'#443735'}
];
const players=new Map(),nodes=[],enemies=new Map();
let nextEnemyId=1,worldTick=0,dayClock=12,raidSeq=0,raidStartedThisNight=false,breachedThisNight=false,lastPhase='day',pressureClock=0;
const MISSION={wood:0,stone:0,meat:0,gather:0,kills:0,boss:0,raids:0,invested:0,builds:0};

const FACILITY_TIERS={
 workshop:[
  {cost:{wood:45,stone:25,meat:0},base:2,req:{},mission:{gather:70},effect:'채집 효율'},
  {cost:{wood:90,stone:60,meat:10},base:3,req:{storage:1},mission:{gather:180},effect:'채집 효율'},
  {cost:{wood:170,stone:120,meat:25},base:5,req:{forge:2,storage:2},mission:{boss:1,invested:650},effect:'채집 효율'}],
 storage:[
  {cost:{wood:55,stone:30,meat:0},base:2,req:{},mission:{gather:60},effect:'적재량'},
  {cost:{wood:100,stone:70,meat:10},base:3,req:{workshop:1},mission:{invested:200},effect:'적재량'},
  {cost:{wood:180,stone:130,meat:30},base:5,req:{farm:2,wall:2},mission:{gather:500},effect:'적재량'}],
 farm:[
  {cost:{wood:55,stone:25,meat:10},base:2,req:{workshop:1},mission:{meat:25},effect:'식량 생산'},
  {cost:{wood:110,stone:60,meat:25},base:3,req:{storage:2},mission:{gather:240},effect:'식량 생산'},
  {cost:{wood:190,stone:100,meat:50},base:5,req:{infirmary:2},mission:{raids:2},effect:'식량 생산'}],
 watchtower:[
  {cost:{wood:70,stone:40,meat:15},base:2,req:{workshop:1},mission:{kills:5},effect:'방어 화력'},
  {cost:{wood:140,stone:90,meat:25},base:3,req:{forge:1,wall:1},mission:{raids:1},effect:'방어 화력'},
  {cost:{wood:240,stone:160,meat:45},base:5,req:{turret:1,wall:2},mission:{kills:40},effect:'방어 화력'}],
 forge:[
  {cost:{wood:85,stone:90,meat:20},base:3,req:{workshop:2},mission:{stone:100},effect:'무기 화력'},
  {cost:{wood:160,stone:170,meat:35},base:4,req:{storage:2,watchtower:2},mission:{kills:20},effect:'무기 화력'},
  {cost:{wood:270,stone:260,meat:60},base:6,req:{turret2:1,workshop:3},mission:{boss:1},effect:'무기 화력'}],
 infirmary:[
  {cost:{wood:70,stone:55,meat:30},base:3,req:{farm:1},mission:{meat:50},effect:'거점 회복'},
  {cost:{wood:135,stone:105,meat:55},base:4,req:{storage:2},mission:{raids:1},effect:'거점 회복'},
  {cost:{wood:220,stone:170,meat:90},base:5,req:{farm:3},mission:{raids:3},effect:'거점 회복'}],
 wall:[
  {cost:{wood:95,stone:120,meat:20},base:3,req:{watchtower:1,storage:1},mission:{raids:1},effect:'거점 내구도'},
  {cost:{wood:180,stone:220,meat:45},base:4,req:{forge:2,watchtower:2},mission:{kills:30},effect:'거점 내구도'},
  {cost:{wood:300,stone:360,meat:70},base:6,req:{turret2:2,storage:3},mission:{boss:2},effect:'거점 내구도'}],
 turret:[
  {cost:{wood:120,stone:150,meat:35},base:4,req:{watchtower:2,forge:1},mission:{kills:20},effect:'자동 방어'},
  {cost:{wood:220,stone:260,meat:65},base:5,req:{forge:2,wall:2},mission:{boss:1},effect:'자동 방어'},
  {cost:{wood:360,stone:420,meat:90},base:6,req:{forge:3,wall:2},mission:{boss:2},effect:'자동 방어'}],
 turret2:[
  {cost:{wood:155,stone:190,meat:45},base:5,req:{turret:2,wall:2},mission:{boss:1},effect:'외곽 방어'},
  {cost:{wood:280,stone:330,meat:75},base:6,req:{turret:3,watchtower:3},mission:{raids:3},effect:'외곽 방어'},
  {cost:{wood:420,stone:500,meat:110},base:6,req:{forge:3,wall:3},mission:{boss:2},effect:'외곽 방어'}]
};
const FACILITY_LABEL={workshop:'작업대',storage:'보급 창고',farm:'농장',watchtower:'망루',forge:'대장간',infirmary:'회복소',wall:'방벽',turret:'자동 터렛',turret2:'외곽 터렛'};
const facilityLevels=Object.fromEntries(Object.keys(FACILITY_TIERS).map(k=>[k,0]));
const facilityProgress=Object.fromEntries(Object.keys(FACILITY_TIERS).map(k=>[k,{wood:0,stone:0,meat:0}]));
const BASE_TIERS={
 2:{cost:{wood:70,stone:35,meat:18},req:{},mission:{gather:50}},
 3:{cost:{wood:150,stone:100,meat:40},req:{workshop:1,storage:1},mission:{gather:140,invested:100}},
 4:{cost:{wood:240,stone:200,meat:80},req:{workshop:2,watchtower:1,forge:1,infirmary:1},mission:{kills:15,raids:1}},
 5:{cost:{wood:390,stone:350,meat:140},req:{storage:2,farm:2,wall:2,turret:1},mission:{kills:30,raids:2,boss:1}},
 6:{cost:{wood:600,stone:560,meat:220},req:{workshop:3,watchtower:3,forge:2,infirmary:2,turret:2,turret2:1},mission:{gather:700,raids:3,boss:1,invested:1000}}
};
let baseProgress={wood:0,stone:0,meat:0};
const PAD_POS={base:{x:1800,y:2045},gear:{x:1800,y:1545},workshop:{x:1575,y:1900},storage:{x:1510,y:1770},farm:{x:1540,y:2070},watchtower:{x:2040,y:1670},forge:{x:1580,y:1645},infirmary:{x:2090,y:1780},wall:{x:2200,y:2020},turret:{x:2050,y:1910},turret2:{x:2070,y:2150}};

const WEAPON_TIERS=[
 null,
 {name:'조잡한 창',kind:'melee',damage:18,range:116,autoRange:120,cooldown:330,baseCost:{wood:12,stone:5,meat:0}},
 {name:'강화 창',kind:'melee',damage:27,range:128,autoRange:132,cooldown:300,baseCost:{wood:24,stone:16,meat:0}},
 {name:'사냥 활',kind:'ranged',damage:25,range:430,autoRange:350,cooldown:540,baseCost:{wood:34,stone:36,meat:8}},
 {name:'철제 석궁',kind:'ranged',damage:39,range:560,autoRange:410,cooldown:430,baseCost:{wood:58,stone:72,meat:18}},
 {name:'연발 석궁',kind:'ranged',damage:52,range:620,autoRange:455,cooldown:330,baseCost:{wood:88,stone:112,meat:32}}
];
const SHARED_WEAPON={tier:1,level:1,progress:{wood:0,stone:0,meat:0}};
const rand=(a,b)=>a+Math.random()*(b-a),clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),dist=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y),id=()=>Math.random().toString(36).slice(2,10);
const send=(ws,p)=>ws.readyState===1&&ws.send(JSON.stringify(p));
const broadcast=p=>{const s=JSON.stringify(p);for(const c of wss.clients)if(c.readyState===1)c.send(s)};
const carryOf=p=>p.wood+p.stone+p.meat;
const carryCap=()=>30+BASE.level*10+facilityLevels.storage*12;
function zoneAt(x,y){const d=Math.hypot(x-BASE.x,y-BASE.y);if(d<470)return'camp';if(d>1320)return'danger';if(x<1420)return'forest';if(x>2260)return'quarry';return'meadow'}
function pointForZone(zone){for(let i=0;i<800;i++){const x=rand(120,3480),y=rand(120,3480);if(zoneAt(x,y)===zone)return{x,y}}return{x:rand(160,3440),y:rand(160,3440)}}
function weaponInfo(){const d=WEAPON_TIERS[SHARED_WEAPON.tier],lv=SHARED_WEAPON.level,w={...d};w.damage=Math.round(d.damage*(1+.12*(lv-1)))+facilityLevels.forge*2;w.range=d.range+(lv-1)*8;w.autoRange=d.autoRange+(lv-1)*8;w.cooldown=Math.max(220,d.cooldown-(lv-1)*12);w.level=lv;w.tier=SHARED_WEAPON.tier;w.display=`${d.name} LV.${lv}`;return w}
function scaleCost(cost,m){return{wood:Math.ceil(cost.wood*m),stone:Math.ceil(cost.stone*m),meat:Math.ceil(cost.meat*m)}}
function weaponUpgradeDef(){if(SHARED_WEAPON.tier===5&&SHARED_WEAPON.level===5)return null;let tier=SHARED_WEAPON.tier,level=SHARED_WEAPON.level+1,transition=false;if(level>5){tier++;level=1;transition=true}const d=WEAPON_TIERS[tier],m=(.68+level*.34)*(transition?1.35:1);const def={name:d.name,tier,level,cost:scaleCost(d.baseCost,m),base:1,req:{},mission:{}};
 if(tier===1){def.base=1;def.mission={gather:Math.max(20,level*35)}}
 if(tier===2){def.base=2;def.req={workshop:level>=3?2:1};def.mission={gather:100+level*45}}
 if(tier===3){def.base=3;def.req={forge:level>=4?2:1,workshop:2};def.mission={kills:8+level*5}}
 if(tier===4){def.base=4;def.req={forge:2,turret:level>=4?2:1};def.mission={kills:20+level*8,raids:level>=4?2:1}}
 if(tier===5){def.base=5;def.req={forge:3,turret:2,turret2:level>=4?2:1};def.mission={boss:level>=4?2:1,kills:35+level*10}}
 return def}
const missionLabel={gather:'누적 채집',wood:'목재 채집',stone:'돌/광석 채집',meat:'식량 획득',kills:'적 처치',boss:'우두머리 처치',raids:'습격 방어',invested:'건설 투입',builds:'건설 완료'};
function missionProgressText(m={}){const out=[];for(const[k,v]of Object.entries(m)){const cur=MISSION[k]||0;if(cur<v)out.push(`${missionLabel[k]} ${cur}/${v}`)}return out}
function dependencyText(req={}){const out=[];for(const[k,v]of Object.entries(req))if((facilityLevels[k]||0)<v)out.push(`${FACILITY_LABEL[k]} LV.${v}`);return out}
function reqReason(def){if(!def)return'';if(BASE.level<(def.base||1))return`거점 LV.${def.base} 필요`;const deps=dependencyText(def.req);if(deps.length)return`${deps.slice(0,2).join(' + ')} 필요`;const ms=missionProgressText(def.mission);if(ms.length)return`선행 임무 · ${ms[0]}`;return''}
function publicPads(){const out=[],bd=BASE_TIERS[BASE.level+1]||null,bReason=reqReason(bd);out.push({id:'base',kind:'base',label:bd?`거점 LV.${BASE.level+1}`:`거점 LV.${BASE.level} MAX`,x:PAD_POS.base.x,y:PAD_POS.base.y,size:112,cost:bd?.cost||null,progress:{...baseProgress},complete:!bd,locked:!!bd&&!!bReason,reason:bReason,level:BASE.level,targetLevel:bd?BASE.level+1:BASE.level,requires:bd?.req||{},mission:bd?.mission||{}});
 for(const[k,tiers]of Object.entries(FACILITY_TIERS)){const lv=facilityLevels[k],def=tiers[lv]||null,reason=reqReason(def);out.push({id:k,kind:'facility',label:def?`${FACILITY_LABEL[k]} LV.${lv+1}`:`${FACILITY_LABEL[k]} LV.${lv} MAX`,x:PAD_POS[k].x,y:PAD_POS[k].y,size:104,cost:def?.cost||null,progress:{...facilityProgress[k]},complete:!def,locked:!!def&&!!reason,reason,level:lv,targetLevel:def?lv+1:lv,requires:def?.req||{},mission:def?.mission||{},effect:def?.effect||''})}
 const gd=weaponUpgradeDef(),gr=reqReason(gd),w=weaponInfo();out.push({id:'gear',kind:'gear',label:gd?`공용 무기 · ${gd.name} LV.${gd.level}`:`공용 무기 · ${w.display} MAX`,x:PAD_POS.gear.x,y:PAD_POS.gear.y,size:108,cost:gd?.cost||null,progress:{...SHARED_WEAPON.progress},complete:!gd,locked:!!gd&&!!gr,reason:gr,level:SHARED_WEAPON.level,targetLevel:gd?.level||SHARED_WEAPON.level,weaponTier:SHARED_WEAPON.tier,targetTier:gd?.tier||SHARED_WEAPON.tier,requires:gd?.req||{},mission:gd?.mission||{}});return out}
function publicPlayer(p){const w=weaponInfo();return{id:p.id,name:p.name,x:p.x,y:p.y,hp:p.hp,maxHp:p.maxHp,wood:p.wood,stone:p.stone,meat:p.meat,dir:p.facing>0?0:Math.PI,facing:p.facing,score:p.score,merit:p.merit,gearLevel:w.tier,weaponLevel:w.level,weapon:w.display,weaponKind:w.kind,autoRange:w.autoRange,carry:carryOf(p),carryCap:carryCap(),zone:zoneAt(p.x,p.y),autoTarget:p.autoTarget||null}}

function nodeConfig(t){if(t==='tree')return{hp:6,r:30};if(t==='rock')return{hp:8,r:26};if(t==='ore')return{hp:11,r:27};return{hp:4,r:22}}
function spawnNode(type,count,zone){const c=nodeConfig(type);for(let i=0;i<count;i++){const p=pointForZone(zone);nodes.push({id:id(),type,x:p.x,y:p.y,hp:c.hp,maxHp:c.hp,r:c.r,respawnAt:0,zone})}}
spawnNode('tree',95,'forest');spawnNode('tree',46,'meadow');spawnNode('tree',30,'danger');spawnNode('rock',68,'quarry');spawnNode('rock',27,'meadow');spawnNode('rock',24,'danger');spawnNode('ore',28,'quarry');spawnNode('ore',14,'danger');spawnNode('berry',34,'meadow');spawnNode('berry',18,'forest');

function enemyConfig(t){const defs={
 wolf:{hp:46,speed:118,damage:8,r:21,aggro:540,reward:6,merit:4},
 boar:{hp:76,speed:90,damage:12,r:26,aggro:500,reward:9,merit:6},
 brute:{hp:126,speed:78,damage:18,r:30,aggro:590,reward:12,merit:10},
 direwolf:{hp:98,speed:132,damage:16,r:24,aggro:650,reward:10,merit:8},
 tusker:{hp:165,speed:92,damage:24,r:31,aggro:610,reward:14,merit:12},
 mauler:{hp:235,speed:82,damage:32,r:35,aggro:660,reward:18,merit:16},
 siegebeast:{hp:360,speed:68,damage:45,r:42,aggro:700,reward:24,merit:22},
 alpha:{hp:680,speed:92,damage:30,r:48,aggro:760,reward:30,merit:50,boss:true,name:'잿빛 포식자'},
 broodmother:{hp:930,speed:78,damage:38,r:54,aggro:820,reward:38,merit:70,boss:true,name:'가시등 어미'},
 colossus:{hp:1450,speed:62,damage:58,r:65,aggro:900,reward:55,merit:100,boss:true,name:'황폐의 거수'}
 };const d={...(defs[t]||defs.wolf)},scale=1+(BASE.level-1)*.075;d.hp=Math.round(d.hp*scale);d.damage=Math.round(d.damage*(1+(BASE.level-1)*.055));return d}
function spawnEnemy(type,x,y,raid=false){const c=enemyConfig(type),e={id:nextEnemyId++,type,x,y,hp:c.hp,maxHp:c.hp,speed:c.speed,damage:c.damage,r:c.r,aggro:c.aggro,reward:c.reward,merit:c.merit,raid,attackCd:0,dir:0,boss:!!c.boss,bossName:c.name||''};enemies.set(e.id,e);return e}
function perimeterPoint(radius=1220){const a=Math.random()*Math.PI*2,r=radius+rand(-120,180);return{x:clamp(BASE.x+Math.cos(a)*r,80,WORLD.w-80),y:clamp(BASE.y+Math.sin(a)*r,80,WORLD.h-80)}}
function enemyPool(level=BASE.level){if(level<=1)return['wolf','wolf','boar'];if(level===2)return['wolf','boar','direwolf','brute'];if(level===3)return['direwolf','tusker','brute','mauler'];if(level===4)return['direwolf','tusker','mauler','siegebeast'];return['tusker','mauler','siegebeast','direwolf']}
function pickEnemy(level=BASE.level){const a=enemyPool(level);return a[Math.floor(Math.random()*a.length)]}
function spawnPressureEnemy(raid=false){const pt=perimeterPoint(raid?1050:1300);return spawnEnemy(pickEnemy(),pt.x,pt.y,raid)}
function desiredAmbient(){return 5+BASE.level*2+Math.min(4,players.size)}
for(let i=0;i<7;i++)spawnPressureEnemy(false);
function bossTypeForLevel(){if(BASE.level<=2)return'alpha';if(BASE.level<=4)return'broodmother';return'colossus'}
function bossCadence(){if(BASE.level<=1)return 999;if(BASE.level===2)return 3;return 2}
function activeBoss(){return[...enemies.values()].find(e=>e.boss)||null}
function dayPhase(){const t=dayClock%190;if(t<112)return'day';if(t<132)return'dusk';if(t<178)return'night';return'dawn'}
function snapshot(){const b=activeBoss();return{type:'snapshot',worldTick,world:WORLD,zones:ZONES,base:{...BASE},facilities:{...facilityLevels},missions:{...MISSION},sharedWeapon:{tier:SHARED_WEAPON.tier,level:SHARED_WEAPON.level,name:weaponInfo().name,display:weaponInfo().display},day:{phase:dayPhase(),clock:dayClock,cycle:190},boss:b?{active:true,id:b.id,x:b.x,y:b.y,hp:b.hp,maxHp:b.maxHp,name:b.bossName,type:b.type}:{active:false},players:[...players.values()].map(publicPlayer),nodes:nodes.filter(n=>!n.respawnAt).map(n=>({id:n.id,type:n.type,x:n.x,y:n.y,hp:n.hp,maxHp:n.maxHp,r:n.r,zone:n.zone})),enemies:[...enemies.values()].map(e=>({id:e.id,type:e.type,x:e.x,y:e.y,hp:e.hp,maxHp:e.maxHp,r:e.r,raid:e.raid,dir:e.dir,boss:e.boss,bossName:e.bossName})),pads:publicPads().filter(p=>p.kind!=='gear'),personalPads:publicPads().filter(p=>p.kind==='gear')}}
function addCarry(p,t,a){const free=Math.max(0,carryCap()-carryOf(p)),g=Math.min(free,a);if(g<=0){broadcast({type:'event',kind:'carryFull',playerId:p.id});return 0}p[t]+=g;return g}
function nearestNode(p,max=112){if(carryOf(p)>=carryCap())return null;let b=null,d=max;for(const n of nodes){if(n.respawnAt)continue;const q=Math.hypot(n.x-p.x,n.y-p.y);if(q<d){b=n;d=q}}return b}
function gatherNode(p,n){const now=Date.now();p.facing=n.x<p.x?-1:1;p.autoTarget={kind:'resource',id:n.id};const cd=Math.max(250,360-facilityLevels.workshop*25);if(now-p.lastGather<cd)return false;p.lastGather=now;const power=1+Math.floor((BASE.level-1)/2)+Math.floor((facilityLevels.workshop+1)/2);n.hp-=power;broadcast({type:'event',kind:'swing',playerId:p.id,dir:p.facing>0?0:Math.PI,tier:SHARED_WEAPON.tier,ranged:false,auto:true});broadcast({type:'event',kind:'impact',x:n.x,y:n.y,target:n.type,playerId:p.id});if(n.hp<=0){let kind,amount;if(n.type==='tree'){kind='wood';amount=6+Math.floor(Math.random()*4)+Math.floor(BASE.level/2)}if(n.type==='rock'){kind='stone';amount=5+Math.floor(Math.random()*4)+Math.floor(BASE.level/2)}if(n.type==='ore'){kind='stone';amount=9+Math.floor(Math.random()*5)+BASE.level}if(n.type==='berry'){kind='meat';amount=2+Math.floor(BASE.level/3)}const got=addCarry(p,kind,amount);p.score+=got;p.merit+=n.type==='ore'?3:1;MISSION[kind]+=got;MISSION.gather+=got;n.respawnAt=Date.now()+38000+Math.random()*18000;n.hp=n.maxHp;broadcast({type:'event',kind:'gather',playerId:p.id,nodeType:n.type,resource:kind,amount:got,merit:p.merit,x:n.x,y:n.y})}return true}
function finishEnemy(p,e){enemies.delete(e.id);const amount=addCarry(p,'meat',e.reward||6),mg=e.merit||4;p.merit+=mg;p.score+=18+amount*2+mg;MISSION.meat+=amount;MISSION.gather+=amount;MISSION.kills++;if(e.boss)MISSION.boss++;broadcast({type:'event',kind:'kill',playerId:p.id,enemyType:e.type,enemyName:e.bossName||e.type,amount,meritGain:mg,x:e.x,y:e.y,boss:e.boss});if(e.boss)broadcast({type:'event',kind:'bossDown',playerId:p.id,name:e.bossName,x:e.x,y:e.y});else if(!e.raid)setTimeout(()=>spawnPressureEnemy(false),14000)}
function finishDefenseEnemy(e){enemies.delete(e.id);MISSION.kills++;if(e.boss){MISSION.boss++;broadcast({type:'event',kind:'bossDown',playerId:null,name:e.bossName,x:e.x,y:e.y})}else if(!e.raid)setTimeout(()=>spawnPressureEnemy(false),14000)}
function nearestEnemy(p,range){let b=null,d=range;for(const e of enemies.values()){const q=dist(e,p);if(q<d){b=e;d=q}}return b}
function attackEnemy(p,e){const w=weaponInfo(),now=Date.now();if(!e)return false;p.facing=e.x<p.x?-1:1;p.autoTarget={kind:'enemy',id:e.id};if(now-p.lastAttack<w.cooldown)return false;p.lastAttack=now;broadcast({type:'event',kind:'swing',playerId:p.id,dir:p.facing>0?0:Math.PI,tier:w.tier,ranged:w.kind==='ranged',auto:true});if(w.kind==='ranged'){e.hp-=w.damage;broadcast({type:'event',kind:'projectile',weapon:w.tier>=4?'bolt':'arrow',x1:p.x,y1:p.y,x2:e.x,y2:e.y,targetId:e.id,playerId:p.id,damage:w.damage});if(e.hp<=0)finishEnemy(p,e);return true}e.hp-=w.damage;const dx=e.x-p.x,dy=e.y-p.y,l=Math.hypot(dx,dy)||1;e.x+=dx/l*20;e.y+=dy/l*20;broadcast({type:'event',kind:'slash',x:e.x,y:e.y,targetId:e.id,playerId:p.id,damage:w.damage});if(e.hp<=0)finishEnemy(p,e);return true}
function remaining(cost,prog,k){return Math.max(0,(cost?.[k]||0)-(prog?.[k]||0))}
function takeForProject(p,cost,prog,rate=3){let total=0;for(const k of['wood','stone','meat']){const n=Math.min(p[k],remaining(cost,prog,k),rate);if(n>0){p[k]-=n;prog[k]+=n;total+=n}}return total}
function done(cost,prog){return['wood','stone','meat'].every(k=>(prog[k]||0)>=(cost[k]||0))}
function insidePad(p,pos,size=104){return Math.abs(p.x-pos.x)<=size*.52&&Math.abs(p.y-pos.y)<=size*.52}
function completeFacility(fid,p){facilityLevels[fid]++;facilityProgress[fid]={wood:0,stone:0,meat:0};MISSION.builds++;if(fid==='wall'){const bonus=300+facilityLevels.wall*150;BASE.maxHp+=bonus;BASE.hp=Math.min(BASE.maxHp,BASE.hp+bonus)}broadcast({type:'event',kind:facilityLevels[fid]===1?'constructionComplete':'facilityUpgrade',project:fid,label:FACILITY_LABEL[fid],level:facilityLevels[fid],x:PAD_POS[fid].x,y:PAD_POS[fid].y,playerId:p.id})}
function completeBase(p){BASE.level++;BASE.maxHp+=420+BASE.level*80;BASE.hp=BASE.maxHp;baseProgress={wood:0,stone:0,meat:0};MISSION.builds++;broadcast({type:'event',kind:'upgrade',level:BASE.level,playerId:p.id,x:PAD_POS.base.x,y:PAD_POS.base.y});const count=2+BASE.level;for(let i=0;i<count;i++)spawnPressureEnemy(true);broadcast({type:'event',kind:'enemyTier',level:BASE.level})}
function completeWeapon(p){const def=weaponUpgradeDef();if(!def)return;const from=weaponInfo().display;SHARED_WEAPON.tier=def.tier;SHARED_WEAPON.level=def.level;SHARED_WEAPON.progress={wood:0,stone:0,meat:0};const to=weaponInfo().display;broadcast({type:'event',kind:'weaponUpgrade',playerId:p.id,from,to,tier:SHARED_WEAPON.tier,level:SHARED_WEAPON.level,all:true,x:PAD_POS.gear.x,y:PAD_POS.gear.y})}
function processPads(p,now){if(now-(p.lastPad||0)<180)return false;let active=null;const bd=BASE_TIERS[BASE.level+1];if(bd&&!reqReason(bd)&&insidePad(p,PAD_POS.base,112))active={id:'base',cost:bd.cost,prog:baseProgress,type:'base'};
 if(!active)for(const[k,tiers]of Object.entries(FACILITY_TIERS)){const lv=facilityLevels[k],def=tiers[lv];if(!def||reqReason(def))continue;if(insidePad(p,PAD_POS[k],104)){active={id:k,cost:def.cost,prog:facilityProgress[k],type:'facility'};break}}
 if(!active){const wd=weaponUpgradeDef();if(wd&&!reqReason(wd)&&insidePad(p,PAD_POS.gear,108))active={id:'gear',cost:wd.cost,prog:SHARED_WEAPON.progress,type:'gear'}}
 if(!active)return false;p.lastPad=now;const used=takeForProject(p,active.cost,active.prog,3);if(used<=0)return false;MISSION.invested+=used;p.autoTarget={kind:'pad',id:active.id};p.merit+=used;broadcast({type:'event',kind:'padDeposit',project:active.id,playerId:p.id,amount:used,x:PAD_POS[active.id].x,y:PAD_POS[active.id].y});if(done(active.cost,active.prog)){if(active.type==='base')completeBase(p);else if(active.type==='facility')completeFacility(active.id,p);else completeWeapon(p)}return true}
function processFarm(p,now){const lv=facilityLevels.farm;if(!lv||!insidePad(p,PAD_POS.farm,112)||now-(p.lastFarm||0)<Math.max(750,1500-lv*180)||carryOf(p)>=carryCap())return false;p.lastFarm=now;const got=addCarry(p,'meat',1+Math.floor(lv/2));if(got){MISSION.meat+=got;MISSION.gather+=got;p.autoTarget={kind:'facility',id:'farm'};broadcast({type:'event',kind:'gather',playerId:p.id,nodeType:'farm',resource:'meat',amount:got,merit:p.merit,x:PAD_POS.farm.x,y:PAD_POS.farm.y});return true}return false}
function autoAction(p,now){p.autoTarget=null;const w=weaponInfo(),enemy=nearestEnemy(p,w.autoRange);if(enemy){attackEnemy(p,enemy);return'enemy'}const node=nearestNode(p,114);if(node){gatherNode(p,node);return'resource'}if(processPads(p,now))return'pad';if(processFarm(p,now))return'farm';return null}
function spawnRaid(){raidSeq++;breachedThisNight=false;const count=5+BASE.level*3+Math.min(10,players.size*2);for(let i=0;i<count;i++){const pt=perimeterPoint(980+Math.random()*180);spawnEnemy(pickEnemy(),pt.x,pt.y,true)}let boss=null;if(BASE.level>=2&&raidSeq%bossCadence()===0&&!activeBoss()){const pt=perimeterPoint(1120);boss=spawnEnemy(bossTypeForLevel(),pt.x,pt.y,true);broadcast({type:'event',kind:'bossRaid',raid:raidSeq,name:boss.bossName,type:boss.type,x:boss.x,y:boss.y})}broadcast({type:'event',kind:'raid',raid:raidSeq,count:count+(boss?1:0),boss:boss?.bossName||null,baseLevel:BASE.level})}
function defenseFire(dt){if(!defenseFire.cd)defenseFire.cd={watchtower:0,turret:0,turret2:0};for(const k of Object.keys(defenseFire.cd))defenseFire.cd[k]-=dt;const fire=(fid,baseRange,baseDamage,all,baseCd)=>{const lv=facilityLevels[fid];if(!lv||defenseFire.cd[fid]>0)return;let target=null,d=baseRange+lv*35;for(const e of enemies.values()){if(!all&&!e.raid)continue;const q=Math.hypot(e.x-PAD_POS[fid].x,e.y-PAD_POS[fid].y);if(q<d){d=q;target=e}}if(!target)return;defenseFire.cd[fid]=Math.max(.24,baseCd-lv*.08);target.hp-=baseDamage+lv*8;broadcast({type:'event',kind:'towerShot',source:fid,x1:PAD_POS[fid].x,y1:PAD_POS[fid].y,x2:target.x,y2:target.y});if(target.hp<=0)finishDefenseEnemy(target)};fire('watchtower',430,18,false,1.03);fire('turret',520,28,true,.58);fire('turret2',580,34,true,.5)}
function updateEnemy(e,dt){e.attackCd=Math.max(0,e.attackCd-dt);let target=null,td=e.aggro;for(const p of players.values()){const d=dist(e,p);if(d<td){td=d;target=p}}if(!target){target=BASE;td=Math.hypot(e.x-BASE.x,e.y-BASE.y)}const dx=target.x-e.x,dy=target.y-e.y,l=Math.hypot(dx,dy)||1;e.dir=Math.atan2(dy,dx);const stop=target===BASE?BASE.r*.7+e.r:42;if(td>stop){e.x=clamp(e.x+dx/l*e.speed*dt,60,WORLD.w-60);e.y=clamp(e.y+dy/l*e.speed*dt,60,WORLD.h-60);return}if(e.attackCd>0)return;e.attackCd=e.boss?1.05:.82;if(target===BASE){BASE.hp=Math.max(0,BASE.hp-e.damage);broadcast({type:'event',kind:'baseHit',hp:BASE.hp,x:e.x,y:e.y});if(BASE.hp<=0){breachedThisNight=true;BASE.hp=BASE.maxHp*.45;broadcast({type:'event',kind:'baseBreach'})}}else{target.hp=Math.max(0,target.hp-e.damage);broadcast({type:'event',kind:'hurt',playerId:target.id,amount:e.damage});if(target.hp<=0){target.hp=target.maxHp;target.x=BASE.x;target.y=BASE.y;target.wood=Math.floor(target.wood*.6);target.stone=Math.floor(target.stone*.6);target.meat=Math.floor(target.meat*.6);broadcast({type:'event',kind:'down',playerId:target.id})}}}
function maintainPressure(dt){pressureClock-=dt;if(pressureClock>0)return;pressureClock=4;let normal=0;for(const e of enemies.values())if(!e.raid&&!e.boss)normal++;const need=desiredAmbient();for(let i=normal;i<need;i++)spawnPressureEnemy(false)}

wss.on('connection',ws=>{const pid=id(),p={id:pid,ws,name:`생존자-${pid.slice(0,3)}`,x:BASE.x+rand(-75,75),y:BASE.y+rand(-75,75),hp:100,maxHp:100,wood:0,stone:0,meat:0,facing:1,lastAttack:0,lastGather:0,lastPad:0,lastFarm:0,input:{x:0,y:0},score:0,merit:0,autoTarget:null};players.set(pid,p);send(ws,{type:'welcome',id:pid});send(ws,snapshot());broadcast({type:'event',kind:'join',player:publicPlayer(p)});ws.on('message',raw=>{let m;try{m=JSON.parse(raw)}catch{return}if(m.type==='input'){p.input.x=clamp(Number(m.x)||0,-1,1);p.input.y=clamp(Number(m.y)||0,-1,1);if(Math.hypot(p.input.x,p.input.y)>1){const l=Math.hypot(p.input.x,p.input.y);p.input.x/=l;p.input.y/=l}}if(m.type==='name'&&typeof m.name==='string')p.name=m.name.trim().slice(0,14)||p.name});ws.on('close',()=>{players.delete(pid);broadcast({type:'event',kind:'leave',playerId:pid})})});
let last=Date.now();
setInterval(()=>{const now=Date.now(),dt=Math.min(.05,(now-last)/1000);last=now;worldTick++;dayClock=(dayClock+dt)%190;const phase=dayPhase();if(phase==='night'&&!raidStartedThisNight){raidStartedThisNight=true;spawnRaid()}if(lastPhase==='night'&&phase==='dawn'&&raidStartedThisNight&&!breachedThisNight){MISSION.raids++;broadcast({type:'event',kind:'mission',mission:'raids',value:MISSION.raids})}if(phase==='day')raidStartedThisNight=false;lastPhase=phase;if(phase==='day')BASE.hp=Math.min(BASE.maxHp,BASE.hp+2.2*dt);maintainPressure(dt);
 for(const p of players.values()){const q=Math.max(0,Math.min(1,carryOf(p)/carryCap())),speed=212*Math.max(.86,1-.14*Math.pow(q,1.35));p.x=clamp(p.x+p.input.x*speed*dt,35,WORLD.w-35);p.y=clamp(p.y+p.input.y*speed*dt,35,WORLD.h-35);if(Math.abs(p.input.x)>.08)p.facing=p.input.x<0?-1:1;const heal=12+facilityLevels.infirmary*7;if(Math.hypot(p.x-BASE.x,p.y-BASE.y)<BASE.r+52)p.hp=Math.min(p.maxHp,p.hp+heal*dt);autoAction(p,now)}
 for(const e of [...enemies.values()])if(enemies.has(e.id))updateEnemy(e,dt);
 defenseFire(dt);for(const n of nodes)if(n.respawnAt&&n.respawnAt<now){n.respawnAt=0;n.hp=n.maxHp}if(worldTick%3===0){const s=snapshot();for(const p of players.values())send(p.ws,s)}
},1000/30);
server.listen(PORT,()=>console.log(`Outpost Wilds V10 listening on ${PORT}`));
