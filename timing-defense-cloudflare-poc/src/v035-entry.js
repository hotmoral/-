import baseWorker, { TimingDefenseRoom } from "./v034-entry.js";

const TYPES = {
  grunt: { hp: 320, speed: .070, baseDamage: 90, armor: 1, reward: 6, knockResist: .85 },
  runner:{ hp: 165, speed: .135, baseDamage: 60, armor: 1, reward: 5, knockResist: 1.00 }
};
const STAGES = {
  1:{count:8,gap:1120},
  2:{count:10,gap:1040}
};
const UPGRADE_META={
  atk:{mult:1.0},crit:{mult:1.1},critdmg:{mult:1.0},hp:{mult:.9},def:{mult:1.1},knock:{mult:.9}
};
const BASE_COST=[40,65,100,145,200,265,340,425,520,625];
const UPGRADE_KEYS=new Set(Object.keys(UPGRADE_META));
const JUDGES=new Set(["NORMAL","GOOD","PERFECT"]);
const WALL_X=.155;

function json(data,status=200){
  return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}});
}
function roomStub(env,code){
  const id=env.ROOMS.idFromName(String(code||"").toUpperCase());
  return env.ROOMS.get(id,{locationHint:"apac-ne"});
}
async function parseJson(request){return request.json().catch(()=>({}))}
function freshUpgrades(){return{atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0}}
function comboBonus(c){return c>=30?.15:c>=20?.12:c>=10?.08:c>=5?.05:0}
function baseDamage(t){return t==="PERFECT"?200:t==="GOOD"?140:t==="CRITICAL"?600:t==="SUPER"?400:t==="GREAT"?300:t==="HEAVY+"?230:t==="HEAVY"?180:100}
function strongTier(x,y){
  if(x==="PERFECT"&&y==="PERFECT")return"CRITICAL";
  const w=(x==="PERFECT"?2:x==="GOOD"?1:0)+(y==="PERFECT"?2:y==="GOOD"?1:0);
  return w>=3?"SUPER":w===2?"GREAT":w===1?"HEAVY+":"HEAVY";
}
function xpFor(t){
  const c=t==="CRITICAL",p=c||t==="PERFECT"||t==="SUPER",g=p||t==="GOOD"||t==="GREAT";
  return c?28:p?18:g?12:8;
}
function need(l){return 60+12*(l-1)}
function aiInterval(c){return c==="rogue"?1150:c==="tank"?1650:c==="archer"?1200:c==="mage"?1500:1400}
function stageHp(type,stage){
  const d=TYPES[type];
  return Math.round(d.hp*(1+(stage-1)*.13)*1.10);
}
function upgradeCost(player,key){
  const rank=player.upgrades?.[key]||0;
  if(rank>=10)return Infinity;
  return Math.round(BASE_COST[rank]*UPGRADE_META[key].mult);
}
function sortedParticipants(room){return [...(room?.participants||[])].sort((a,b)=>a.slot-b.slot)}
function shopReadySlots(run){return Array.isArray(run?.shop?.readySlots)?run.shop.readySlots:[]}

const baseMakeRun=TimingDefenseRoom.prototype.makeRun;
TimingDefenseRoom.prototype.makeRun=function(startAt){
  const run=baseMakeRun.call(this,startAt);
  for(const p of run.players)p.upgrades=freshUpgrades();
  run.shop=null;
  return run;
};

const basePlayerPublic=TimingDefenseRoom.prototype.playerPublic;
TimingDefenseRoom.prototype.playerPublic=function(player){
  return {...basePlayerPublic.call(this,player),upgrades:{...freshUpgrades(),...(player.upgrades||{})}};
};

const baseRunPublic=TimingDefenseRoom.prototype.runPublic;
TimingDefenseRoom.prototype.runPublic=function(at){
  const out=baseRunPublic.call(this,at);
  if(!out)return out;
  const run=this.room?.run;
  out.shop=run?.shop?{
    stage:run.shop.stage,
    readySlots:[...shopReadySlots(run)].sort((a,b)=>a-b),
    canNext:!!run.shop.canNext
  }:null;
  return out;
};

TimingDefenseRoom.prototype.xAt=function(monster,at){
  const d=TYPES[monster.type]||TYPES.grunt;
  return monster.x-d.speed*Math.max(0,at-monster.refAt)/1000;
};
TimingDefenseRoom.prototype.wallAt=function(monster){
  const d=TYPES[monster.type]||TYPES.grunt;
  if(monster.x<=WALL_X)return monster.refAt;
  return monster.refAt+((monster.x-WALL_X)/d.speed)*1000;
};

TimingDefenseRoom.prototype.spawn=function(at){
  const run=this.room.run,stage=run.stage||1;
  let type="grunt";
  if(stage===2)type=this.rng()<.62?"grunt":"runner";
  const id=run.nextMonsterId++,hp=stageHp(type,stage);
  run.monsters.push({
    id,type,x:1.055+this.rng()*.04,y:.30+this.rng()*.32,refAt:at,hp,maxHp:hp
  });
  run.spawned++;
  this.event({type:"spawn",targetId:id,monsterType:type,stage},at);
};

TimingDefenseRoom.prototype.applyDamage=function(monster,damage,slot,tier,at,knock=true,source="hit",proc=false){
  const run=this.room.run;
  if(!monster)return{actual:0,killed:false};
  const d=TYPES[monster.type]||TYPES.grunt;
  this.materialize(monster,at);
  const actual=Math.max(1,Math.round(damage*d.armor));
  monster.hp-=actual;
  const player=run.players.find(p=>p.slot===slot);
  if(knock){
    const c=tier==="CRITICAL",p=c||tier==="PERFECT"||tier==="SUPER",g=p||tier==="GOOD"||tier==="GREAT";
    const base=c?.047:p?.024:g?.013:.006;
    const mul=player?1+(player.upgrades?.knock||0)*.10:1;
    monster.x=Math.min(.985,monster.x+base*d.knockResist*mul);
  }
  let killed=false;
  if(monster.hp<=0){
    killed=true;run.kills++;
    if(player){player.kills++;player.coin+=d.reward}
    run.monsters=run.monsters.filter(m=>m.id!==monster.id);
  }
  if(player)player.damage+=actual;
  this.event({type:source,slot,targetId:monster.id,tier,damage:actual,killed,procCrit:!!proc,stage:run.stage},at);
  return{actual,killed};
};

TimingDefenseRoom.prototype.playerAction=function(participant,body,at){
  const run=this.room.run;
  if(!run||run.status!=="combat")throw new Error("run-not-combat");
  const player=run.players.find(p=>p.slot===participant.slot);
  if(!player)throw new Error("player-not-in-run");
  const seq=Number(body.seq);
  if(!Number.isFinite(seq)||seq<=player.lastSeq)throw new Error("stale-seq");
  player.lastSeq=seq;
  player.upgrades={...freshUpgrades(),...(player.upgrades||{})};
  const x=JUDGES.has(body.xJudge)?body.xJudge:"NORMAL";
  const heavy=player.charge>=3;
  const y=heavy&&JUDGES.has(body.yJudge)?body.yJudge:null;
  let tier,predictedCombo;
  if(heavy){
    this.recordCombo(player,x);
    predictedCombo=y==="PERFECT"?player.combo+1:0;
    tier=strongTier(x,y||"NORMAL");
    this.recordCombo(player,y||"NORMAL");
  }else{
    predictedCombo=x==="PERFECT"?player.combo+1:0;
    tier=x;
    this.recordCombo(player,x);
  }
  let damage=baseDamage(tier)*(1+comboBonus(predictedCombo))*(1+(player.upgrades.atk||0)*.08);
  const chance=(player.upgrades.crit||0)*.02;
  let proc=false;
  if(chance>0&&this.rng()<chance){
    damage*=1.5+(player.upgrades.critdmg||0)*.15;proc=true;
  }
  const monster=this.nearest(at);
  const result=this.applyDamage(monster,Math.round(damage),player.slot,tier,at,true,"hit",proc);
  const gain=xpFor(tier);
  player.xp+=gain;
  while(player.xp>=player.xpNeed){player.xp-=player.xpNeed;player.level++;player.xpNeed=need(player.level)}
  player.charge=heavy?0:Math.min(3,player.charge+1);
  const event=run.events[run.events.length-1];
  if(event?.type==="hit"&&event.slot===player.slot){
    Object.assign(event,{xpGain:gain,level:player.level,charge:player.charge,combo:player.combo,xJudge:x,yJudge:y,procCrit:proc});
  }
  run.revision++;
  this.checkEnd(at);
  return{tier,...result,xpGain:gain,player:this.playerPublic(player)};
};

TimingDefenseRoom.prototype.enterShop=function(at){
  const run=this.room?.run;
  if(!run||run.status==="shop")return;
  const reward=55+run.stage*12;
  for(const p of run.players)p.coin+=reward;
  run.status="shop";
  this.room.status="shop";
  run.monsters=[];
  run.shop={stage:run.stage,readySlots:[],canNext:false};
  this.event({type:"shop-open",stage:run.stage,reward},at);
  run.revision++;
};

TimingDefenseRoom.prototype.recalcShopReady=function(){
  const run=this.room?.run;
  if(!run?.shop)return;
  const ready=new Set(shopReadySlots(run));
  const humanSlots=sortedParticipants(this.room).map(p=>p.slot);
  run.shop.canNext=humanSlots.length>=1&&humanSlots.every(slot=>ready.has(slot));
};

TimingDefenseRoom.prototype.setShopReady=function(player,ready,at){
  const run=this.room?.run;
  if(!run||run.status!=="shop"||!run.shop)throw new Error("shop-not-open");
  const set=new Set(shopReadySlots(run));
  if(ready)set.add(player.slot);else set.delete(player.slot);
  run.shop.readySlots=[...set];
  this.recalcShopReady();
  this.event({type:"shop-ready",slot:player.slot,ready:!!ready,stage:run.stage},at);
  run.revision++;
};

TimingDefenseRoom.prototype.buyShop=function(player,key,at){
  const run=this.room?.run;
  if(!run||run.status!=="shop"||!run.shop)throw new Error("shop-not-open");
  if(shopReadySlots(run).includes(player.slot))throw new Error("shop-ready-locked");
  if(!UPGRADE_KEYS.has(key))throw new Error("invalid-upgrade");
  player.upgrades={...freshUpgrades(),...(player.upgrades||{})};
  const cost=upgradeCost(player,key);
  if(!Number.isFinite(cost))throw new Error("upgrade-max");
  if(player.coin<cost)throw new Error("not-enough-coin");
  player.coin-=cost;player.upgrades[key]++;
  if(key==="hp"){run.baseHpMax+=100;run.baseHp=Math.min(run.baseHpMax,run.baseHp+100)}
  this.event({type:"shop-buy",slot:player.slot,key,rank:player.upgrades[key],cost,stage:run.stage},at);
  run.revision++;
  return{key,rank:player.upgrades[key],cost,coin:player.coin};
};

TimingDefenseRoom.prototype.beginStage=function(stage,at){
  const plan=STAGES[stage];
  if(!plan)throw new Error("stage-not-supported");
  const run=this.room?.run;
  if(!run)throw new Error("run-missing");
  run.stage=stage;
  run.status="stage-starting";
  run.startAt=at+1500;
  run.combatAt=run.startAt+1050;
  run.stageTarget=plan.count;
  run.spawned=0;
  run.nextSpawnAt=run.combatAt;
  run.monsters=[];
  run.shop=null;
  for(const p of run.players)p.nextPassiveAt=run.combatAt+2000;
  for(const a of run.ai)a.nextAt=run.combatAt+450+a.slot*220;
  this.room.status="running";
  this.event({type:"stage-starting",stage,startAt:run.startAt},at);
  run.revision++;
};

TimingDefenseRoom.prototype.checkEnd=function(at){
  const run=this.room?.run;
  if(!run)return false;
  if(run.baseHp<=0&&run.status!=="gameover"){
    run.status="gameover";this.room.status="run-ended";this.event({type:"gameover"},at);return true;
  }
  if(run.status==="combat"&&run.spawned>=run.stageTarget&&run.monsters.length===0){
    if(run.stage===1){this.enterShop(at);return true}
    if(run.stage===2){
      run.status="stage2-clear";this.room.status="run-ended";this.event({type:"stage2-clear",stage:2},at);run.revision++;return true;
    }
  }
  return false;
};

TimingDefenseRoom.prototype.processAt=function(at){
  const run=this.room?.run;
  if(!run)return false;
  let changed=false;
  if((run.status==="starting"||run.status==="stage-starting")&&at>=run.startAt){
    run.status=at<run.combatAt?"intro":"combat";this.room.status="running";changed=true;
  }
  if(run.status==="intro"&&at>=run.combatAt){run.status="combat";changed=true}
  if(run.status!=="combat"){if(changed)run.revision++;return changed}
  const plan=STAGES[run.stage];
  while(plan&&run.spawned<run.stageTarget&&run.nextSpawnAt<=at){
    this.spawn(run.nextSpawnAt);run.nextSpawnAt+=plan.gap;changed=true;
  }
  const wallHits=[...run.monsters].filter(m=>this.wallAt(m)<=at+.5).sort((a,b)=>this.wallAt(a)-this.wallAt(b)||a.id-b.id);
  for(const monster of wallHits){
    if(!run.monsters.find(m=>m.id===monster.id))continue;
    const hitAt=Math.min(at,this.wallAt(monster));
    this.materialize(monster,hitAt);
    run.monsters=run.monsters.filter(m=>m.id!==monster.id);
    const d=TYPES[monster.type]||TYPES.grunt;
    const defRank=run.players.reduce((n,p)=>n+(p.upgrades?.def||0),0);
    const defense=Math.max(0,Math.min(.60,defRank*.025));
    const incoming=Math.max(1,Math.round(d.baseDamage*(1-defense)));
    run.baseHp=Math.max(0,run.baseHp-incoming);
    this.event({type:"wall",targetId:monster.id,damage:incoming,baseHp:run.baseHp,stage:run.stage},hitAt);
    changed=true;
    if(this.checkEnd(hitAt))break;
  }
  if(run.status!=="combat"){if(changed)run.revision++;return changed}
  for(const player of [...run.players].sort((a,b)=>a.slot-b.slot)){
    if(player.nextPassiveAt>at)continue;
    const eventAt=player.nextPassiveAt,monster=this.nearest(eventAt);
    if(monster){
      this.applyDamage(monster,40,player.slot,"AUTO",eventAt,false,"passive",false);
      player.nextPassiveAt=eventAt+2000;changed=true;
      if(this.checkEnd(eventAt))break;
    }else{player.nextPassiveAt=eventAt+250;changed=true}
  }
  if(run.status!=="combat"){if(changed)run.revision++;return changed}
  for(const ai of [...run.ai].sort((a,b)=>a.slot-b.slot)){
    if(ai.nextAt>at)continue;
    const eventAt=ai.nextAt,monster=this.nearest(eventAt);
    if(monster){
      const tier=this.aiTier(ai);
      this.applyDamage(monster,baseDamage(tier),ai.slot,tier,eventAt,true,"ai",false);
      ai.nextAt=eventAt+aiInterval(ai.cls)+Math.round(-140+this.rng()*310);
      changed=true;
      if(this.checkEnd(eventAt))break;
    }else{ai.nextAt=eventAt+120;changed=true}
  }
  if(changed)run.revision++;
  return changed;
};

TimingDefenseRoom.prototype.nextDueAt=function(){
  const run=this.room?.run;
  if(!run||["shop","stage2-clear","gameover"].includes(run.status))return null;
  if(run.status==="starting"||run.status==="stage-starting")return run.startAt;
  if(run.status==="intro")return run.combatAt;
  if(run.status!=="combat")return null;
  const plan=STAGES[run.stage];
  let due=Infinity;
  if(plan&&run.spawned<run.stageTarget)due=Math.min(due,run.nextSpawnAt);
  for(const p of run.players)due=Math.min(due,p.nextPassiveAt);
  for(const a of run.ai)due=Math.min(due,a.nextAt);
  for(const m of run.monsters)due=Math.min(due,this.wallAt(m));
  return Number.isFinite(due)?due:null;
};

const baseExplicitLeave=TimingDefenseRoom.prototype.explicitLeave;
TimingDefenseRoom.prototype.explicitLeave=async function(session){
  const result=await baseExplicitLeave.call(this,session);
  if(this.room?.run?.shop){
    this.recalcShopReady();
    await this.persist();
    this.broadcastState(Date.now());
  }
  return result;
};

const baseRoomFetch=TimingDefenseRoom.prototype.fetch;
TimingDefenseRoom.prototype.fetch=async function(request){
  const url=new URL(request.url);
  if(url.pathname.startsWith("/v035/")){
    if(!this.room)return json({ok:false,error:"room-not-found"},404);
    const body=await parseJson(request);
    const now=Date.now();
    const participant=this.room.participants.find(p=>p.session===String(body.session||""));
    if(!participant)return json({ok:false,error:"invalid-session"},401);
    const advanced=this.advanceTo(now);
    if(advanced){await this.persist();this.broadcastState(now)}
    const player=this.room.run?.players?.find(p=>p.slot===participant.slot);
    if(url.pathname==="/v035/resume"){
      const eventFloor=this.room.run?Math.max(0,(this.room.run.nextEventId||1)-1):0;
      const state=this.publicState(now);
      if(state?.run)state.run={...state.run,events:[]};
      return json({ok:true,session:participant.session,slot:participant.slot,lastSeq:player?.lastSeq||0,eventFloor,state});
    }
    try{
      let result=null;
      if(url.pathname==="/v035/shop-buy"){
        if(!player)throw new Error("run-player-missing");
        result=this.buyShop(player,String(body.key||""),now);
      }else if(url.pathname==="/v035/shop-ready"){
        if(!player)throw new Error("run-player-missing");
        this.setShopReady(player,!!body.ready,now);
        result={ready:shopReadySlots(this.room.run).includes(player.slot)};
      }else if(url.pathname==="/v035/shop-next"){
        if(this.room.hostSession!==participant.session)throw new Error("host-only");
        const run=this.room.run;
        if(!run?.shop||run.status!=="shop")throw new Error("shop-not-open");
        if(!run.shop.canNext)throw new Error("not-ready");
        if(run.stage!==1)throw new Error("stage-not-supported");
        this.beginStage(2,now);result={stage:2,startAt:this.room.run.startAt};
      }else return json({ok:false,error:"not-found"},404);
      await this.persist();this.broadcastState(now);await this.scheduleNext();
      return json({ok:true,result,state:this.publicState(now)});
    }catch(error){
      await this.scheduleNext();
      return json({ok:false,error:error.message||"v035-action-failed",state:this.publicState(now)},409);
    }
  }
  return baseRoomFetch.call(this,request);
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health"){
      return json({
        ok:true,
        service:"timing-defense-cloudflare-v035-parity",
        version:"0.35-cf.1",
        transport:"websocket-hibernation",
        authority:"durable-object-event-driven-stage2-shop",
        presentation:"v034-render-parity-retained",
        locationHint:"apac-ne",
        scope:"room-stage1-shop-stage2-reconnect"
      });
    }
    if(request.method==="GET"&&url.pathname==="/"){
      const assetUrl=new URL(request.url);assetUrl.pathname="/v035-cloudflare.html";
      return env.ASSETS.fetch(new Request(assetUrl,request));
    }
    const m=url.pathname.match(/^\/api\/room\/([A-Z0-9]{6})\/(resume|shop-buy|shop-ready|shop-next)$/i);
    if(request.method==="POST"&&m){
      const code=m[1].toUpperCase(),action=m[2].toLowerCase();
      const text=await request.text();
      return roomStub(env,code).fetch(new Request(`https://room.internal/v035/${action}`,{
        method:"POST",headers:{"content-type":"application/json"},body:text
      }));
    }
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom };
