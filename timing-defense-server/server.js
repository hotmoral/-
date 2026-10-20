'use strict';

const http=require('http'),crypto=require('crypto');
const {URL}=require('url');

const PORT=Number(process.env.PORT||10000);
const ORIGIN=process.env.ALLOWED_ORIGIN||'https://timing-defense-v011.onrender.com';
const ROOM_TTL=72e5, STALE=45e3, RECONNECT_GRACE=180e3, RANDOM_TTL=9e4;
const CLASSES=new Set(['knight','rogue','tank','archer','mage']);
const METHODS=new Set(['friend','link','random']);
const JUDGES=new Set(['NORMAL','GOOD','PERFECT']);
const UPGRADE_KEYS=new Set(['atk','crit','critdmg','hp','def','knock']);
const UPGRADE_META={
  atk:{mult:1.0},crit:{mult:1.1},critdmg:{mult:1.0},hp:{mult:.9},def:{mult:1.1},knock:{mult:.9}
};
const BASE_COST=[40,65,100,145,200,265,340,425,520,625];
const MT={
  grunt:{hp:320,speed:.070,baseDamage:90,armor:1,reward:6,knockResist:.85},
  runner:{hp:165,speed:.135,baseDamage:60,armor:1,reward:5,knockResist:1.00}
};
const STAGES={
  1:{count:8,gap:1120,pick:()=> 'grunt'},
  2:{count:10,gap:1040,pick:()=>Math.random()<.62?'grunt':'runner'}
};

const rooms=new Map(),streams=new Map(),tickets=new Map(),queue=[];
const now=()=>Date.now(),rid=(n=16)=>crypto.randomBytes(n).toString('hex');

function code(){
  const a='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  for(let n=0;n<100;n++){
    let c='';for(let i=0;i<6;i++)c+=a[crypto.randomInt(a.length)];
    if(!rooms.has(c))return c
  }
  throw Error('room-code-exhausted')
}
function nick(v){const s=String(v||'').trim().slice(0,12);return s||'PLAYER'}
function cls(v){return CLASSES.has(v)?v:'knight'}
function method(v){return METHODS.has(v)?v:'friend'}
function freshUpgrades(){return{atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0}}
function aiFill(v){
  if(!Array.isArray(v))return[];
  const u=new Set(),o=[];
  for(const x of v){
    const p=Number(x?.pos),c=cls(x?.cls);
    if(p<2||p>4||u.has(p))continue;
    u.add(p);o.push({pos:p,cls:c});if(o.length>=2)break
  }
  return o.sort((a,b)=>a.pos-b.pos)
}
function cors(req,res){
  const o=req.headers.origin;
  if(o&&(o===ORIGIN||process.env.ALLOW_ANY_ORIGIN==='1')){
    res.setHeader('Access-Control-Allow-Origin',o);res.setHeader('Vary','Origin')
  }else if(!o)res.setHeader('Access-Control-Allow-Origin',ORIGIN);
  res.setHeader('Access-Control-Allow-Methods','GET,POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers','Content-Type');
  res.setHeader('Cache-Control','no-store')
}
function send(res,s,d){res.statusCode=s;res.setHeader('Content-Type','application/json; charset=utf-8');res.end(JSON.stringify(d))}
function text(res,s,d){res.statusCode=s;res.setHeader('Content-Type','text/plain; charset=utf-8');res.end(d)}
function body(req){
  return new Promise((ok,bad)=>{
    let b='';
    req.on('data',c=>{b+=c;if(b.length>65536){bad(Error('body-too-large'));req.destroy()}});
    req.on('end',()=>{if(!b)return ok({});try{ok(JSON.parse(b))}catch(_){bad(Error('invalid-json'))}});
    req.on('error',bad)
  })
}
const hs=r=>[...r.participants.values()].sort((a,b)=>a.slot-b.slot);
const roomFor=c=>rooms.get(String(c||'').toUpperCase());
const part=(r,s)=>r?.participants.get(String(s||''));
function nextSlot(r){
  const b=new Set(r.aiFill.map(x=>x.pos));
  for(const p of r.participants.values())b.add(p.slot);
  for(let i=1;i<=4;i++)if(!b.has(i))return i;
  return null
}
const need=l=>60+12*(l-1);
const comboBonus=c=>c>=30?.15:c>=20?.12:c>=10?.08:c>=5?.05:0;
function baseDamage(t){return t==='PERFECT'?200:t==='GOOD'?140:t==='CRITICAL'?600:t==='SUPER'?400:t==='GREAT'?300:t==='HEAVY+'?230:t==='HEAVY'?180:100}
function strong(x,y){
  if(x==='PERFECT'&&y==='PERFECT')return'CRITICAL';
  const w=(x==='PERFECT'?2:x==='GOOD'?1:0)+(y==='PERFECT'?2:y==='GOOD'?1:0);
  return w>=3?'SUPER':w===2?'GREAT':w===1?'HEAVY+':'HEAVY'
}
function xp(t){const c=t==='CRITICAL',p=c||t==='PERFECT'||t==='SUPER',g=p||t==='GOOD'||t==='GREAT';return c?28:p?18:g?12:8}
function rec(p,j){p.combo=j==='PERFECT'?p.combo+1:0;p.comboPeak=Math.max(p.comboPeak,p.combo)}
function grant(p,n){p.xp+=n;while(p.xp>=p.xpNeed){p.xp-=p.xpNeed;p.level++;p.xpNeed=need(p.level)}}
function upgradeCost(p,key){
  const rank=p.upgrades?.[key]||0;
  if(rank>=10)return Infinity;
  return Math.round(BASE_COST[rank]*UPGRADE_META[key].mult)
}
function nearest(run){return[...run.monsters.values()].filter(m=>!m.dead).sort((a,b)=>a.x-b.x)[0]||null}
function playerPublic(p){return{
  slot:p.slot,level:p.level,xp:p.xp,xpNeed:p.xpNeed,charge:p.charge,combo:p.combo,comboPeak:p.comboPeak,
  kills:p.kills,coin:p.coin,damage:p.damage,upgrades:{...p.upgrades}
}}
function runPublic(r){
  if(!r)return null;
  const shop=r.shop?{
    stage:r.shop.stage,
    readySlots:[...r.shop.readySlots].sort((a,b)=>a-b),
    canNext:r.shop.canNext
  }:null;
  return{
    id:r.id,seed:r.seed,status:r.status,startAt:r.startAt,combatAt:r.combatAt,stage:r.stage,
    stageTarget:r.stageTarget,spawned:r.spawned,baseHp:r.baseHp,baseHpMax:r.baseHpMax,kills:r.kills,
    revision:r.revision,serverTime:now(),shop,
    monsters:[...r.monsters.values()].filter(m=>!m.dead).map(m=>({
      id:m.id,type:m.type,x:m.x,y:m.y,hp:m.hp,maxHp:m.maxHp,boss:false
    })),
    players:[...r.players.values()].map(playerPublic),
    events:r.events.slice(-24)
  }
}
function state(r){
  const h=hs(r).map(p=>({
    slot:p.slot,nickname:p.nickname,classId:p.classId,ready:!!p.ready,
    host:p.session===r.hostSession,connected:now()-p.lastSeen<=STALE
  }));
  const occ=new Set(h.map(p=>p.slot));for(const a of r.aiFill)occ.add(a.pos);
  const open=[];for(let i=1;i<=4;i++)if(!occ.has(i))open.push(i);
  const ready=h.length>=2&&h.every(p=>p.ready);
  return{
    code:r.code,method:r.method,status:r.status,createdAt:r.createdAt,
    hostSlot:h.find(p=>p.host)?.slot||null,participants:h,aiFill:r.aiFill,openHumanSlots:open,
    canStart:ready&&r.status==='waiting',startAt:r.startAt||null,revision:r.revision,serverTime:now(),
    run:runPublic(r.run)
  }
}
function broadcast(r){
  r.revision++;
  const set=streams.get(r.code);if(!set?.size)return;
  const payload=`event: state\ndata: ${JSON.stringify(state(r))}\n\n`;
  for(const x of [...set])try{x.write(payload)}catch(_){set.delete(x)}
}
function closeStreams(c){
  const s=streams.get(c);if(!s)return;
  for(const r of s)try{r.end()}catch(_){}
  streams.delete(c)
}
function createRoom(x){
  const c=code(),s=rid(),r={
    code:c,method:method(x.method),createdAt:now(),updatedAt:now(),status:'waiting',startAt:null,
    hostSession:s,aiFill:aiFill(x.aiFill),participants:new Map(),revision:0,run:null
  };
  r.participants.set(s,{session:s,slot:1,nickname:nick(x.nickname),classId:cls(x.classId),ready:false,lastSeen:now()});
  rooms.set(c,r);return{room:r,session:s,slot:1}
}
function joinRoom(r,x){
  if(r.status!=='waiting')throw Error('room-not-joinable');
  const slot=nextSlot(r);if(!slot)throw Error('room-full');
  const s=rid();
  r.participants.set(s,{session:s,slot,nickname:nick(x.nickname),classId:cls(x.classId),ready:false,lastSeen:now()});
  r.updatedAt=now();broadcast(r);return{session:s,slot}
}
function leave(r,s){
  const p=part(r,s);if(!p)return false;
  r.participants.delete(s);r.updatedAt=now();
  if(r.hostSession===s)r.hostSession=hs(r)[0]?.session||null;
  if(!r.participants.size){rooms.delete(r.code);closeStreams(r.code)}else broadcast(r);
  return true
}
function makePlayer(slot){
  return{
    slot,level:1,xp:0,xpNeed:60,charge:0,combo:0,comboPeak:0,kills:0,coin:0,damage:0,
    lastSeq:0,nextPassiveAt:0,upgrades:freshUpgrades()
  }
}
function makeRun(r,startAt){
  const run={
    id:rid(8),seed:crypto.randomInt(1,0x7fffffff),status:'starting',startAt,combatAt:startAt+1050,
    stage:1,stageTarget:8,spawned:0,nextSpawnAt:startAt+1050,baseHp:2000,baseHpMax:2000,kills:0,
    nextMonsterId:1,monsters:new Map(),players:new Map(),ai:new Map(),events:[],nextEventId:1,
    revision:0,lastTick:now(),lastBroadcast:0,shop:null
  };
  for(const p of r.participants.values()){
    const ps=makePlayer(p.slot);ps.nextPassiveAt=run.combatAt+2000;run.players.set(p.slot,ps)
  }
  for(const a of r.aiFill)run.ai.set(a.pos,{slot:a.pos,cls:a.cls,charge:0,nextAt:run.combatAt+450+a.pos*220});
  return run
}
function ev(run,e){run.events.push({id:run.nextEventId++,...e,at:now()});if(run.events.length>48)run.events.splice(0,run.events.length-48)}
function stagePlan(stage){return STAGES[stage]||null}
function stageHp(type,stage){
  const d=MT[type];return Math.round(d.hp*(1+(stage-1)*.13)*1.10)
}
function spawn(run){
  const plan=stagePlan(run.stage);if(!plan)return;
  const type=plan.pick(),d=MT[type],id=run.nextMonsterId++,hp=stageHp(type,run.stage);
  run.monsters.set(id,{
    id,type,x:1.055+Math.random()*.04,y:.30+Math.random()*.32,hp,maxHp:hp,dead:false
  });
  run.spawned++;ev(run,{type:'spawn',targetId:id,monsterType:type,stage:run.stage})
}
function totalDefRank(run){
  let n=0;for(const p of run.players.values())n+=p.upgrades?.def||0;return n
}
function damageWithUpgrades(ps,tier,predCombo){
  let damage=baseDamage(tier)*(1+comboBonus(predCombo))*(1+(ps.upgrades?.atk||0)*.08);
  const chance=(ps.upgrades?.crit||0)*.02;
  let proc=false;
  if(chance>0&&Math.random()<chance){
    damage*=1.5+(ps.upgrades?.critdmg||0)*.15;proc=true
  }
  return{damage:Math.round(damage),proc}
}
function apply(run,m,damage,slot,tier,knock=true,source='hit',proc=false){
  if(!m||m.dead)return{actual:0,killed:false};
  const d=MT[m.type],actual=Math.max(1,Math.round(damage*d.armor));m.hp-=actual;
  const ps=run.players.get(slot);
  if(knock){
    const c=tier==='CRITICAL',p=c||tier==='PERFECT'||tier==='SUPER',g=p||tier==='GOOD'||tier==='GREAT';
    const base=c?.047:p?.024:g?.013:.006;
    const mul=ps?1+(ps.upgrades?.knock||0)*.10:1;
    m.x=Math.min(.985,m.x+base*d.knockResist*mul)
  }
  let killed=false;
  if(m.hp<=0){
    m.dead=true;killed=true;run.kills++;
    if(ps){ps.kills++;ps.coin+=d.reward}
  }
  if(ps)ps.damage+=actual;
  ev(run,{type:source,slot,targetId:m.id,tier,damage:actual,killed,procCrit:!!proc,stage:run.stage});
  return{actual,killed}
}
function playerAction(r,ps,b){
  const run=r.run;if(!run||run.status!=='combat')throw Error('run-not-combat');
  const seq=Number(b.seq);if(!Number.isFinite(seq)||seq<=ps.lastSeq)throw Error('stale-seq');
  ps.lastSeq=seq;
  const x=JUDGES.has(b.xJudge)?b.xJudge:'NORMAL',heavy=ps.charge>=3,y=heavy&&JUDGES.has(b.yJudge)?b.yJudge:null;
  let tier,pred;
  if(heavy){rec(ps,x);pred=y==='PERFECT'?ps.combo+1:0;tier=strong(x,y||'NORMAL');rec(ps,y||'NORMAL')}
  else{pred=x==='PERFECT'?ps.combo+1:0;tier=x;rec(ps,x)}
  const rolled=damageWithUpgrades(ps,tier,pred);
  const m=nearest(run),result=apply(run,m,rolled.damage,ps.slot,tier,true,'hit',rolled.proc);
  const gain=xp(tier);grant(ps,gain);ps.charge=heavy?0:Math.min(3,ps.charge+1);
  const e=run.events[run.events.length-1];
  if(e){e.xpGain=gain;e.level=ps.level;e.charge=ps.charge;e.combo=ps.combo;e.xJudge=x;e.yJudge=y}
  run.revision++;r.updatedAt=now();broadcast(r);
  return{tier,...result,xpGain:gain,player:playerPublic(ps)}
}
function aiTier(a){
  const r=Math.random(),heavy=a.charge>=3;
  if(heavy){a.charge=0;return r<.15?'SUPER':r<.65?'GREAT':'HEAVY+'}
  a.charge++;return r<.18?'PERFECT':r<.72?'GOOD':'NORMAL'
}
function aiInt(c){return c==='rogue'?1150:c==='tank'?1650:1400}
function enterShop(r,t){
  const run=r.run;if(!run||run.status==='shop')return;
  const reward=55+run.stage*12;
  for(const p of run.players.values())p.coin+=reward;
  run.status='shop';r.status='shop';run.monsters.clear();run.shop={stage:run.stage,readySlots:new Set(),canNext:false};
  ev(run,{type:'shop-open',stage:run.stage,reward});run.revision++;r.updatedAt=t
}
function setShopReady(r,ps,ready){
  const run=r.run;if(!run||run.status!=='shop'||!run.shop)throw Error('shop-not-open');
  if(ready)run.shop.readySlots.add(ps.slot);else run.shop.readySlots.delete(ps.slot);
  const humanSlots=hs(r).map(p=>p.slot);
  run.shop.canNext=humanSlots.length>=1&&humanSlots.every(s=>run.shop.readySlots.has(s));
  ev(run,{type:'shop-ready',slot:ps.slot,ready:!!ready,stage:run.stage});
  run.revision++;r.updatedAt=now();broadcast(r)
}
function buyShop(r,ps,key){
  const run=r.run;if(!run||run.status!=='shop')throw Error('shop-not-open');
  if(run.shop?.readySlots.has(ps.slot))throw Error('shop-ready-locked');
  if(!UPGRADE_KEYS.has(key))throw Error('invalid-upgrade');
  const cost=upgradeCost(ps,key);if(!Number.isFinite(cost))throw Error('upgrade-max');
  if(ps.coin<cost)throw Error('not-enough-coin');
  ps.coin-=cost;ps.upgrades[key]++;
  if(key==='hp'){run.baseHpMax+=100;run.baseHp=Math.min(run.baseHpMax,run.baseHp+100)}
  ev(run,{type:'shop-buy',slot:ps.slot,key,rank:ps.upgrades[key],cost,stage:run.stage});
  run.revision++;r.updatedAt=now();broadcast(r);
  return{key,rank:ps.upgrades[key],cost,coin:ps.coin}
}
function beginStage(run,stage,t){
  const plan=stagePlan(stage);if(!plan)throw Error('stage-not-supported');
  run.stage=stage;run.status='stage-starting';run.startAt=t+1500;run.combatAt=run.startAt+1050;
  run.stageTarget=plan.count;run.spawned=0;run.nextSpawnAt=run.combatAt;run.monsters.clear();run.shop=null;
  for(const p of run.players.values())p.nextPassiveAt=run.combatAt+2000;
  for(const a of run.ai.values())a.nextAt=run.combatAt+450+a.slot*220;
  ev(run,{type:'stage-starting',stage,startAt:run.startAt,combatAt:run.combatAt});
  run.revision++
}
function shopNext(r,session){
  const run=r.run;if(!run||run.status!=='shop'||!run.shop)throw Error('shop-not-open');
  if(r.hostSession!==session)throw Error('host-only');
  if(!run.shop.canNext)throw Error('shop-not-ready');
  if(run.stage!==1)throw Error('next-stage-not-supported');
  beginStage(run,2,now());r.status='starting';r.startAt=run.startAt;r.updatedAt=now();broadcast(r)
}
function tick(r,t){
  const run=r.run;if(!run)return false;
  let changed=false,dt=Math.min(.2,Math.max(0,(t-run.lastTick)/1000));run.lastTick=t;

  if((run.status==='starting'||run.status==='stage-starting')&&t>=run.startAt){
    run.status=t<run.combatAt?'intro':'combat';r.status='running';changed=true
  }
  if(run.status==='intro'&&t>=run.combatAt){run.status='combat';r.status='running';changed=true}
  if(run.status!=='combat')return changed;

  const plan=stagePlan(run.stage);if(!plan)return changed;
  while(t>=run.nextSpawnAt&&run.spawned<run.stageTarget&&[...run.monsters.values()].filter(m=>!m.dead).length<10){
    spawn(run);run.nextSpawnAt+=plan.gap;changed=true
  }
  for(const m of run.monsters.values()){
    if(m.dead)continue;
    const d=MT[m.type];m.x-=d.speed*dt;
    if(m.x<=.155){
      m.dead=true;
      const defense=Math.min(.60,totalDefRank(run)*.025);
      const incoming=Math.max(1,Math.round(d.baseDamage*(1-defense)));
      run.baseHp=Math.max(0,run.baseHp-incoming);
      ev(run,{type:'wall',targetId:m.id,damage:incoming,baseHp:run.baseHp,stage:run.stage});changed=true
    }
  }
  for(const ps of run.players.values()){
    if(t>=ps.nextPassiveAt){
      const m=nearest(run);
      if(m){apply(run,m,40,ps.slot,'AUTO',false,'passive');changed=true;ps.nextPassiveAt=t+2000}
      else ps.nextPassiveAt=t+250
    }
  }
  for(const a of run.ai.values()){
    if(t>=a.nextAt){
      const m=nearest(run);
      if(m){const tier=aiTier(a);apply(run,m,baseDamage(tier),a.slot,tier,true,'ai');changed=true;a.nextAt=t+aiInt(a.cls)+Math.round(-140+Math.random()*310)}
      else a.nextAt=t+120
    }
  }
  for(const[k,m]of[...run.monsters])if(m.dead)run.monsters.delete(k);

  if(run.baseHp<=0){
    run.status='gameover';r.status='run-ended';ev(run,{type:'gameover',stage:run.stage});changed=true
  }else if(run.spawned>=run.stageTarget&&!nearest(run)){
    if(run.stage===1){enterShop(r,t);changed=true}
    else if(run.stage===2){run.status='stage2-clear';r.status='stage2-clear';ev(run,{type:'stage-clear',stage:2});changed=true}
  }
  if(changed)run.revision++;
  return changed
}
function matchRandom(){
  while(queue.length>=2){
    const a=queue.shift(),b=queue.shift(),ta=tickets.get(a),tb=tickets.get(b);
    if(!ta||!tb||ta.status!=='searching'||tb.status!=='searching')continue;
    const ca=createRoom({nickname:ta.nickname,classId:ta.classId,aiFill:[],method:'random'});
    const jb=joinRoom(ca.room,{nickname:tb.nickname,classId:tb.classId});
    Object.assign(ta,{status:'matched',code:ca.room.code,session:ca.session,slot:1,host:true,updatedAt:now()});
    Object.assign(tb,{status:'matched',code:ca.room.code,session:jb.session,slot:jb.slot,host:false,updatedAt:now()});
    broadcast(ca.room)
  }
}

async function handler(req,res){
  cors(req,res);
  if(req.method==='OPTIONS'){res.statusCode=204;return res.end()}
  const u=new URL(req.url,`http://${req.headers.host||'localhost'}`),p=u.pathname;

  if(req.method==='GET'&&p==='/health')
    return send(res,200,{ok:true,service:'timing-defense-mp',version:'0.3.0',rooms:rooms.size,randomSearching:queue.length,time:now()});

  if(req.method==='POST'&&p==='/api/room/create'){
    try{const b=await body(req),x=createRoom(b);broadcast(x.room);return send(res,201,{ok:true,session:x.session,slot:x.slot,state:state(x.room)})}
    catch(e){return send(res,400,{ok:false,error:e.message})}
  }
  if(req.method==='POST'&&p==='/api/room/join'){
    try{
      const b=await body(req),r=roomFor(b.code);if(!r)return send(res,404,{ok:false,error:'room-not-found'});
      const j=joinRoom(r,b);return send(res,200,{ok:true,session:j.session,slot:j.slot,state:state(r)})
    }catch(e){return send(res,409,{ok:false,error:e.message})}
  }

  const m=p.match(/^\/api\/room\/([A-Z0-9]{6})(?:\/(state|update|leave|start|stream|heartbeat|action|resume|shop-buy|shop-ready|shop-next))?$/i);
  if(m){
    const c=m[1].toUpperCase(),a=m[2]||'state',r=roomFor(c);
    if(!r)return send(res,404,{ok:false,error:'room-not-found'});

    if(req.method==='GET'&&a==='state')return send(res,200,{ok:true,state:state(r)});

    if(req.method==='GET'&&a==='stream'){
      const s=u.searchParams.get('session'),pp=part(r,s);
      if(!pp)return send(res,401,{ok:false,error:'invalid-session'});
      pp.lastSeen=now();
      res.statusCode=200;res.setHeader('Content-Type','text/event-stream; charset=utf-8');res.setHeader('Connection','keep-alive');res.setHeader('X-Accel-Buffering','no');
      res.write(`event: state\ndata: ${JSON.stringify(state(r))}\n\n`);
      if(!streams.has(c))streams.set(c,new Set());streams.get(c).add(res);
      req.on('close',()=>streams.get(c)?.delete(res));return
    }

    if(req.method==='POST'&&a==='resume'){
      const b=await body(req),pp=part(r,b.session);
      if(!pp)return send(res,401,{ok:false,error:'invalid-session'});
      pp.lastSeen=now();r.updatedAt=now();
      const st=state(r),eventFloor=r.run?Math.max(0,r.run.nextEventId-1):0;
      if(st.run)st.run.events=[];
      return send(res,200,{ok:true,session:pp.session,slot:pp.slot,eventFloor,state:st})
    }

    if(req.method==='POST'&&a==='heartbeat'){
      const b=await body(req),pp=part(r,b.session);if(!pp)return send(res,401,{ok:false,error:'invalid-session'});
      pp.lastSeen=now();r.updatedAt=now();return send(res,200,{ok:true})
    }

    if(req.method==='POST'&&a==='update'){
      const b=await body(req),pp=part(r,b.session);if(!pp)return send(res,401,{ok:false,error:'invalid-session'});
      if(r.status!=='waiting')return send(res,409,{ok:false,error:'room-locked'});
      if(typeof b.ready==='boolean')pp.ready=b.ready;
      if(b.nickname!==undefined)pp.nickname=nick(b.nickname);
      if(b.classId!==undefined)pp.classId=cls(b.classId);
      pp.lastSeen=now();r.updatedAt=now();broadcast(r);return send(res,200,{ok:true,state:state(r)})
    }

    if(req.method==='POST'&&a==='leave'){
      const b=await body(req);leave(r,b.session);return send(res,200,{ok:true})
    }

    if(req.method==='POST'&&a==='start'){
      const b=await body(req),pp=part(r,b.session);if(!pp)return send(res,401,{ok:false,error:'invalid-session'});
      if(r.hostSession!==b.session)return send(res,403,{ok:false,error:'host-only'});
      const st=state(r);if(!st.canStart)return send(res,409,{ok:false,error:'not-ready',state:st});
      r.status='starting';r.startAt=now()+2500;r.run=makeRun(r,r.startAt);r.updatedAt=now();broadcast(r);
      return send(res,200,{ok:true,state:state(r)})
    }

    if(req.method==='POST'&&a==='action'){
      try{
        const b=await body(req),pp=part(r,b.session);if(!pp)return send(res,401,{ok:false,error:'invalid-session'});
        pp.lastSeen=now();const ps=r.run?.players.get(pp.slot);if(!ps)return send(res,409,{ok:false,error:'run-player-missing'});
        return send(res,200,{ok:true,result:playerAction(r,ps,b),state:state(r)})
      }catch(e){return send(res,409,{ok:false,error:e.message,state:state(r)})}
    }

    if(req.method==='POST'&&a==='shop-buy'){
      try{
        const b=await body(req),pp=part(r,b.session);if(!pp)return send(res,401,{ok:false,error:'invalid-session'});
        const ps=r.run?.players.get(pp.slot);if(!ps)return send(res,409,{ok:false,error:'run-player-missing'});
        pp.lastSeen=now();const result=buyShop(r,ps,String(b.key||''));
        return send(res,200,{ok:true,result,state:state(r)})
      }catch(e){return send(res,409,{ok:false,error:e.message,state:state(r)})}
    }

    if(req.method==='POST'&&a==='shop-ready'){
      try{
        const b=await body(req),pp=part(r,b.session);if(!pp)return send(res,401,{ok:false,error:'invalid-session'});
        const ps=r.run?.players.get(pp.slot);if(!ps)return send(res,409,{ok:false,error:'run-player-missing'});
        pp.lastSeen=now();setShopReady(r,ps,!!b.ready);
        return send(res,200,{ok:true,state:state(r)})
      }catch(e){return send(res,409,{ok:false,error:e.message,state:state(r)})}
    }

    if(req.method==='POST'&&a==='shop-next'){
      try{
        const b=await body(req),pp=part(r,b.session);if(!pp)return send(res,401,{ok:false,error:'invalid-session'});
        pp.lastSeen=now();shopNext(r,b.session);
        return send(res,200,{ok:true,state:state(r)})
      }catch(e){return send(res,409,{ok:false,error:e.message,state:state(r)})}
    }
  }

  if(req.method==='POST'&&p==='/api/random/search'){
    try{
      const b=await body(req),t=rid(10);
      tickets.set(t,{ticket:t,status:'searching',nickname:nick(b.nickname),classId:cls(b.classId),createdAt:now(),updatedAt:now()});
      queue.push(t);matchRandom();return send(res,202,{ok:true,ticket:t,status:tickets.get(t)})
    }catch(e){return send(res,400,{ok:false,error:e.message})}
  }
  if(req.method==='GET'&&p==='/api/random/status'){
    const t=u.searchParams.get('ticket'),x=tickets.get(t);if(!x)return send(res,404,{ok:false,error:'ticket-not-found'});
    return send(res,200,{ok:true,status:x})
  }
  if(req.method==='POST'&&p==='/api/random/cancel'){
    const b=await body(req),x=tickets.get(b.ticket);if(x&&x.status==='searching'){x.status='cancelled';x.updatedAt=now()}
    return send(res,200,{ok:true})
  }
  text(res,404,'not found')
}

const server=http.createServer((req,res)=>handler(req,res).catch(e=>{
  console.error(e);if(!res.headersSent)cors(req,res);if(!res.writableEnded)send(res,500,{ok:false,error:'internal'})
}));

setInterval(()=>{
  const t=now();
  for(const r of [...rooms.values()]){
    let changed=tick(r,t);
    for(const[s,p]of[...r.participants]){
      if(t-p.lastSeen>RECONNECT_GRACE){r.participants.delete(s);changed=true}
    }
    if(changed){
      if(!r.participants.has(r.hostSession))r.hostSession=hs(r)[0]?.session||null;
      if(!r.participants.size){rooms.delete(r.code);closeStreams(r.code);continue}
      if(r.run?.shop){
        const humanSlots=hs(r).map(p=>p.slot);
        r.run.shop.canNext=humanSlots.length>=1&&humanSlots.every(s=>r.run.shop.readySlots.has(s))
      }
    }
    if(r.run&&(r.status==='running'||r.status==='starting'||r.status==='shop')&&t-r.run.lastBroadcast>=100){
      r.run.lastBroadcast=t;broadcast(r)
    }else if(changed)broadcast(r);
    if(t-r.updatedAt>ROOM_TTL){rooms.delete(r.code);closeStreams(r.code)}
  }
  for(const[t,x]of tickets)if(now()-x.updatedAt>RANDOM_TTL)tickets.delete(t);
  for(const[c,s]of streams){
    for(const r of [...s])try{r.write(`: ping ${t}\n\n`)}catch(_){s.delete(r)}
    if(!s.size)streams.delete(c)
  }
},50).unref();

server.listen(PORT,'0.0.0.0',()=>console.log(`timing-defense-mp listening on ${PORT}`));
