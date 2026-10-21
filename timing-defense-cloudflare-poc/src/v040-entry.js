import baseWorker, { TimingDefenseRoom } from "./v039-audit-entry.js";

// Timing Defense Cloudflare v0.40 — Stage 4 SHIELD / armor slice.
// Exact legacy encounter contract. No new numerical balance decision.

export const STAGE4={count:13,gap:940};
export const STAGE4_TYPES={
  grunt:{hp:320,speed:.070,size:1.00,baseDamage:90,knockResist:.85,armor:1.00,reward:6},
  runner:{hp:165,speed:.135,size:.70,baseDamage:60,knockResist:1.00,armor:1.00,reward:5},
  shield:{hp:540,speed:.057,size:1.08,baseDamage:120,knockResist:.62,armor:.72,reward:10},
  brute:{hp:900,speed:.040,size:1.34,baseDamage:180,knockResist:.38,armor:1.00,reward:14}
};
const SHIELD=STAGE4_TYPES.shield;
const WALL_X=.155;

function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}
function roomStub(env,code){const id=env.ROOMS.idFromName(String(code||"").toUpperCase());return env.ROOMS.get(id,{locationHint:"apac-ne"})}
function aiStageMul(stage){return 1+Math.max(0,(Number(stage)||1)-1)*.035}
function tierKnockBase(tier){
  const critical=tier==="CRITICAL",perfect=critical||tier==="PERFECT"||tier==="SUPER",good=perfect||tier==="GOOD"||tier==="GREAT";
  return critical?.047:perfect?.024:good?.013:.006;
}
export function stage4Type(r){return r<.36?"grunt":r<.62?"runner":r<.82?"shield":"brute"}
export function stage4Hp(type){const d=STAGE4_TYPES[type]||STAGE4_TYPES.grunt;return Math.round(d.hp*(1+(4-1)*.13)*1.10)}
export function shieldArmorDamage(incoming){return Math.max(1,Math.round((Number(incoming)||0)*SHIELD.armor))}
export function stage4WallDamage(type,defRank=0){
  const d=STAGE4_TYPES[type]||STAGE4_TYPES.grunt;
  const defense=Math.max(0,Math.min(.60,(Number(defRank)||0)*.025));
  return Math.max(1,Math.round(d.baseDamage*(1-defense)));
}

// SHIELD must not fall back to GRUNT movement/wall timing.
const baseXAt=TimingDefenseRoom.prototype.xAt;
TimingDefenseRoom.prototype.xAt=function(monster,at){
  if(monster?.type!=="shield")return baseXAt.call(this,monster,at);
  return monster.x-SHIELD.speed*Math.max(0,at-monster.refAt)/1000;
};
const baseWallAt=TimingDefenseRoom.prototype.wallAt;
TimingDefenseRoom.prototype.wallAt=function(monster){
  if(monster?.type!=="shield")return baseWallAt.call(this,monster);
  if(monster.x<=WALL_X)return monster.refAt;
  return monster.refAt+((monster.x-WALL_X)/SHIELD.speed)*1000;
};

// Exact SHIELD armor/reward/knock authority. Other types keep the already-
// validated v0.39 chain unchanged.
const baseApplyDamage=TimingDefenseRoom.prototype.applyDamage;
TimingDefenseRoom.prototype.applyDamage=function(monster,damage,slot,tier,at,knock=true,source="hit",proc=false){
  if(monster?.type!=="shield")return baseApplyDamage.call(this,monster,damage,slot,tier,at,knock,source,proc);
  const run=this.room?.run;if(!run||!monster)return{actual:0,killed:false};
  const player=run.players?.find(p=>p.slot===slot)||null;
  const ai=source==="ai"?run.ai?.find(a=>a.slot===slot)||null:null;
  let authoritativeDamage=damage;
  if(source==="ai")authoritativeDamage=Math.round(authoritativeDamage*aiStageMul(run.stage||1));

  this.materialize(monster,at);
  const actual=shieldArmorDamage(authoritativeDamage);
  monster.hp-=actual;

  if(knock){
    const rank=player?.upgrades?.knock||0;
    let mul=1+rank*.10;
    if(player?.__v036TankLv6&&source==="hit")mul*=1.30;
    const push=tierKnockBase(tier)*SHIELD.knockResist*mul;
    monster.x=Math.min(.985,monster.x+push);
  }

  let killed=false;
  if(monster.hp<=0){
    killed=true;run.kills++;
    if(player){player.kills++;player.coin+=SHIELD.reward;player.killCoinEarned=(player.killCoinEarned||0)+SHIELD.reward}
    if(ai){ai.kills=(ai.kills||0)+1;ai.killCoinEarned=(ai.killCoinEarned||0)+SHIELD.reward}
    run.monsters=run.monsters.filter(m=>m.id!==monster.id);
  }
  if(player)player.damage=(player.damage||0)+actual;
  if(ai)ai.damage=(ai.damage||0)+actual;

  this.event({type:source,slot,targetId:monster.id,tier,damage:actual,killed,procCrit:!!proc,stage:run.stage},at);
  return{actual,killed};
};

TimingDefenseRoom.prototype.spawnStage4=function(at){
  const run=this.room?.run;
  if(!run||run.stage!==4||run.spawned>=run.stageTarget)return null;
  const type=stage4Type(this.rng()),id=run.nextMonsterId++,hp=stage4Hp(type);
  run.monsters.push({id,type,x:1.055+this.rng()*.04,y:.30+this.rng()*.32,refAt:at,hp,maxHp:hp});
  run.spawned++;
  this.event({type:"spawn",targetId:id,monsterType:type,stage:4},at);
  return run.monsters[run.monsters.length-1];
};

const baseBeginStage=TimingDefenseRoom.prototype.beginStage;
TimingDefenseRoom.prototype.beginStage=function(stage,at){
  if(stage!==4){if(stage>4)throw new Error("stage-not-supported");return baseBeginStage.call(this,stage,at)}
  const run=this.room?.run;if(!run)throw new Error("run-missing");
  run.stage=4;run.status="stage-starting";run.startAt=at+1500;run.combatAt=run.startAt+1050;
  run.stageTarget=STAGE4.count;run.spawned=0;run.nextSpawnAt=run.combatAt;run.monsters=[];run.shop=null;
  run.skillQueue=[];run.n3Queue=[];
  for(const p of run.players||[])p.nextPassiveAt=run.combatAt+2000;
  for(const a of run.ai||[])a.nextAt=run.combatAt+450+a.slot*220;
  this.room.status="starting";this.room.startAt=run.startAt;
  this.event({type:"stage-starting",stage:4,startAt:run.startAt,combatAt:run.combatAt},at);run.revision++;
};

function processStage4WallHits(room,at){
  const run=room.room?.run;
  if(!run||run.stage!==4||at<run.combatAt||!["stage-starting","intro","combat"].includes(run.status))return false;
  const due=[...run.monsters].map(monster=>({monster,hitAt:room.wallAt(monster)})).filter(x=>x.hitAt<=at+.5).sort((a,b)=>a.hitAt-b.hitAt||a.monster.id-b.monster.id);
  if(!due.length)return false;
  let changed=false;
  for(const {monster,hitAt} of due){
    if(run.status==="gameover")break;
    if(!run.monsters.some(m=>m.id===monster.id))continue;
    const exactAt=Math.min(at,hitAt);room.materialize(monster,exactAt);run.monsters=run.monsters.filter(m=>m.id!==monster.id);
    const defRank=(run.players||[]).reduce((n,p)=>n+(p.upgrades?.def||0),0),incoming=stage4WallDamage(monster.type,defRank);
    run.baseHp=Math.max(0,run.baseHp-incoming);
    room.event({type:"wall",targetId:monster.id,damage:incoming,baseHp:run.baseHp,stage:4,monsterType:monster.type},exactAt);
    changed=true;if(room.checkEnd(exactAt))break;
  }
  return changed;
}

const baseProcessAt=TimingDefenseRoom.prototype.processAt;
TimingDefenseRoom.prototype.processAt=function(at){
  const run=this.room?.run;let spawned=false;
  if(run?.stage===4&&at>=run.combatAt&&["stage-starting","intro","combat"].includes(run.status)){
    while(run.spawned<run.stageTarget&&run.nextSpawnAt<=at+.5){this.spawnStage4(run.nextSpawnAt);run.nextSpawnAt+=STAGE4.gap;spawned=true}
  }
  const wallChanged=processStage4WallHits(this,at),changed=baseProcessAt.call(this,at);
  if((spawned||wallChanged)&&this.room?.run&&!changed)this.room.run.revision++;
  return spawned||wallChanged||changed;
};

const baseNextDueAt=TimingDefenseRoom.prototype.nextDueAt;
TimingDefenseRoom.prototype.nextDueAt=function(){
  const base=baseNextDueAt.call(this),run=this.room?.run;
  if(!run||run.stage!==4||run.status!=="combat"||run.spawned>=run.stageTarget)return base;
  const due=run.nextSpawnAt;if(!Number.isFinite(due))return base;return base==null?due:Math.min(base,due);
};

// Stage 1-4 clear into Team Shop. Stage 5 remains blocked for this bounded slice.
TimingDefenseRoom.prototype.checkEnd=function(at){
  const run=this.room?.run;if(!run)return false;
  if(run.baseHp<=0&&run.status!=="gameover"){
    run.status="gameover";this.room.status="run-ended";this.event({type:"gameover"},at);return true;
  }
  if(run.status==="combat"&&run.spawned>=run.stageTarget&&run.monsters.length===0&&run.stage>=1&&run.stage<=4){this.enterShop(at);return true}
  return false;
};

// Extend Team Shop NEXT from Stage 3 -> 4. Stage 4 -> 5 remains blocked.
const baseRoomFetch=TimingDefenseRoom.prototype.fetch;
TimingDefenseRoom.prototype.fetch=async function(request){
  const url=new URL(request.url);
  if(request.method==="POST"&&url.pathname==="/v035/shop-next"&&this.room?.run?.stage>=3){
    const body=await request.json().catch(()=>({})),now=Date.now();
    const participant=this.room.participants.find(p=>p.session===String(body.session||""));
    if(!participant)return json({ok:false,error:"invalid-session"},401);
    const advanced=this.advanceTo(now);if(advanced){await this.persist();this.broadcastState(now)}
    try{
      if(this.room.hostSession!==participant.session)throw new Error("host-only");
      const run=this.room.run;if(!run?.shop||run.status!=="shop")throw new Error("shop-not-open");
      if(!run.shop.canNext)throw new Error("not-ready");
      if(run.stage===3){
        this.beginStage(4,now);await this.persist();this.broadcastState(now);await this.scheduleNext();
        return json({ok:true,result:{stage:4,startAt:this.room.run.startAt},state:this.publicState(now)});
      }
      throw new Error("stage5-blocked");
    }catch(error){await this.scheduleNext();return json({ok:false,error:error.message||"v040-shop-next-failed",state:this.publicState(now)},409)}
  }
  if(request.method==="POST"&&url.pathname==="/v040/debug-stage4"){
    const body=await request.json().catch(()=>({})),session=String(body.session||""),p=this.room?.participants?.find(x=>x.session===session);
    if(!p)return json({ok:false,error:"invalid-session"},401);if(this.room.hostSession!==session)return json({ok:false,error:"host-only"},403);
    if(!this.room.run)return json({ok:false,error:"run-missing"},409);
    const now=Date.now();this.beginStage(4,now);await this.persist();this.broadcastState(now);await this.scheduleNext();
    return json({ok:true,state:this.publicState(now)});
  }
  if(request.method==="POST"&&url.pathname==="/v040/debug-shield-sandbox"){
    const body=await request.json().catch(()=>({})),session=String(body.session||""),p=this.room?.participants?.find(x=>x.session===session);
    if(!p)return json({ok:false,error:"invalid-session"},401);if(this.room.hostSession!==session)return json({ok:false,error:"host-only"},403);
    const run=this.room?.run;if(!run||run.stage!==4)return json({ok:false,error:"stage4-required"},409);
    const now=Date.now();run.status="combat";run.startAt=now;run.combatAt=now;run.stageTarget=1;run.spawned=1;run.nextSpawnAt=Number.POSITIVE_INFINITY;
    run.monsters=[{id:run.nextMonsterId++,type:"shield",x:.78,y:.42,refAt:now,hp:stage4Hp("shield"),maxHp:stage4Hp("shield")}];
    run.skillQueue=[];run.n3Queue=[];this.event({type:"debug-stage4-shield",targetId:run.monsters[0].id,stage:4},now);run.revision++;
    await this.persist();this.broadcastState(now);await this.scheduleNext();return json({ok:true,state:this.publicState(now)});
  }
  return baseRoomFetch.call(this,request);
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health")return json({
      ok:true,service:"timing-defense-cloudflare-v040-stage4-shield",version:"0.40-cf.1",
      transport:"websocket-hibernation-per-socket-event-cursor",authority:"durable-object-stage1-stage4-lv6-n3",
      stage4:{count:13,gap:940,composition:{grunt:.36,runner:.26,shield:.20,brute:.18}},
      shield:{hp:540,speed:.057,size:1.08,baseDamage:120,knockResist:.62,armor:.72,reward:10,stage4Hp:826},
      n3:"option-b-frozen",stage5:"blocked",scope:"stage4-shield-armor-authority"
    });
    const m4=url.pathname.match(/^\/api\/room\/([A-Za-z0-9]+)\/debug-stage4$/);
    if(request.method==="POST"&&m4){const stub=roomStub(env,m4[1]);return stub.fetch(new Request("https://room.internal/v040/debug-stage4",request))}
    const ms=url.pathname.match(/^\/api\/room\/([A-Za-z0-9]+)\/debug-shield-sandbox$/);
    if(request.method==="POST"&&ms){const stub=roomStub(env,ms[1]);return stub.fetch(new Request("https://room.internal/v040/debug-shield-sandbox",request))}
    if(request.method==="GET"&&url.pathname==="/"){
      const assetUrl=new URL(request.url);assetUrl.pathname="/v040-cloudflare.html";return env.ASSETS.fetch(new Request(assetUrl,request));
    }
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom };