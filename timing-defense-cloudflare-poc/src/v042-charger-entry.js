import baseWorker, { TimingDefenseRoom } from "./v041-flyer-entry.js";
import { meta } from "./monster-capability-v1.js";

// Timing Defense v0.42 capability slice C — CHARGER authoritative state machine.
// Stage-number-independent. No legacy/final campaign recipe is enabled here.
// All CHARGER coefficients below are PROVISIONAL capability-test anchors.

const CHARGER={...meta('charger'),size:1.00,triggerX:.62};
const WALL_X=.155;
const PHASES=new Set(['advance','windup','charge']);
function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}
function aiStageMul(stage){return 1+Math.max(0,(Number(stage)||1)-1)*.035}
function tierKnockBase(tier){
  const critical=tier==="CRITICAL",perfect=critical||tier==="PERFECT"||tier==="SUPER",good=perfect||tier==="GOOD"||tier==="GREAT";
  return critical?.047:perfect?.024:good?.013:.006;
}
function ensureChargerState(monster,at){
  if(monster?.type!=="charger")return monster;
  if(!PHASES.has(monster.chargerPhase))monster.chargerPhase='advance';
  if(!Number.isFinite(Number(monster.chargerPhaseAt)))monster.chargerPhaseAt=Number.isFinite(Number(monster.refAt))?Number(monster.refAt):Number(at)||0;
  if(!Number.isFinite(Number(monster.chargerRearmUntil)))monster.chargerRearmUntil=0;
  if(!Number.isFinite(Number(monster.chargerTriggerX)))monster.chargerTriggerX=CHARGER.triggerX;
  return monster;
}
function chargerPhaseSpeed(monster){
  const phase=monster?.chargerPhase||'advance';
  return phase==='charge'?CHARGER.chargeSpeed:phase==='windup'?0:CHARGER.speed;
}
function normalWallAt(monster,speed){
  if(monster.x<=WALL_X)return monster.refAt;
  return monster.refAt+((monster.x-WALL_X)/speed)*1000;
}
function nextAdvanceTriggerAt(monster){
  ensureChargerState(monster,monster?.refAt||0);
  if(monster.chargerPhase!=='advance')return null;
  const baseWall=normalWallAt(monster,CHARGER.speed);
  const crossing=monster.x<=monster.chargerTriggerX?monster.refAt:monster.refAt+((monster.x-monster.chargerTriggerX)/CHARGER.speed)*1000;
  const due=Math.max(crossing,Number(monster.chargerRearmUntil)||0);
  return baseWall<=due+.0001?null:due;
}
function nextChargerTransitionAt(monster){
  if(monster?.type!=="charger")return null;
  ensureChargerState(monster,monster.refAt||0);
  if(monster.chargerPhase==='advance')return nextAdvanceTriggerAt(monster);
  if(monster.chargerPhase==='windup')return monster.chargerPhaseAt+CHARGER.windupMs;
  return null;
}

const baseXAt=TimingDefenseRoom.prototype.xAt;
TimingDefenseRoom.prototype.xAt=function(monster,at){
  if(monster?.type!=="charger")return baseXAt.call(this,monster,at);
  ensureChargerState(monster,at);
  const speed=chargerPhaseSpeed(monster),dt=Math.max(0,(Number(at)||0)-Number(monster.refAt||0));
  return monster.x-speed*dt/1000;
};

const baseMaterialize=TimingDefenseRoom.prototype.materialize;
TimingDefenseRoom.prototype.materialize=function(monster,at){
  if(monster?.type!=="charger")return baseMaterialize.call(this,monster,at);
  ensureChargerState(monster,at);
  monster.x=this.xAt(monster,at);monster.refAt=at;
  return monster;
};

const baseWallAt=TimingDefenseRoom.prototype.wallAt;
TimingDefenseRoom.prototype.wallAt=function(monster){
  if(monster?.type!=="charger")return baseWallAt.call(this,monster);
  ensureChargerState(monster,monster.refAt||0);
  if(monster.x<=WALL_X)return monster.refAt;
  if(monster.chargerPhase==='charge')return normalWallAt(monster,CHARGER.chargeSpeed);
  if(monster.chargerPhase==='windup'){
    const chargeAt=monster.chargerPhaseAt+CHARGER.windupMs;
    return chargeAt+Math.max(0,monster.x-WALL_X)/CHARGER.chargeSpeed*1000;
  }
  const ordinaryWall=normalWallAt(monster,CHARGER.speed),triggerAt=nextAdvanceTriggerAt(monster);
  if(triggerAt==null||ordinaryWall<=triggerAt+.0001)return ordinaryWall;
  const xAtTrigger=monster.x-CHARGER.speed*Math.max(0,triggerAt-monster.refAt)/1000;
  return triggerAt+CHARGER.windupMs+Math.max(0,xAtTrigger-WALL_X)/CHARGER.chargeSpeed*1000;
};

TimingDefenseRoom.prototype.advanceOneChargerTo=function(monster,at){
  if(monster?.type!=="charger")return false;
  ensureChargerState(monster,at);let changed=false,guard=0;
  while(guard++<4){
    const due=nextChargerTransitionAt(monster);
    if(due==null||due>at+.5)break;
    this.materialize(monster,due);
    if(monster.chargerPhase==='advance'){
      monster.chargerPhase='windup';monster.chargerPhaseAt=due;monster.refAt=due;
      this.event({type:'monster-state',targetId:monster.id,monsterType:'charger',phase:'windup',reason:'trigger',phaseAt:due,windupMs:CHARGER.windupMs},due);changed=true;continue;
    }
    if(monster.chargerPhase==='windup'){
      monster.chargerPhase='charge';monster.chargerPhaseAt=due;monster.refAt=due;
      this.event({type:'monster-state',targetId:monster.id,monsterType:'charger',phase:'charge',reason:'windup-complete',phaseAt:due,chargeSpeed:CHARGER.chargeSpeed},due);changed=true;continue;
    }
    break;
  }
  return changed;
};
TimingDefenseRoom.prototype.advanceChargersTo=function(at){
  let changed=false;
  for(const m of this.room?.run?.monsters||[])if(m.type==='charger')changed=this.advanceOneChargerTo(m,at)||changed;
  return changed;
};

// CHARGER gets its own combat identity. Positive authoritative knockback during
// WINDUP cancels the current charge attempt and starts the provisional re-arm timer.
const baseApplyDamage=TimingDefenseRoom.prototype.applyDamage;
TimingDefenseRoom.prototype.applyDamage=function(monster,damage,slot,tier,at,knock=true,source="hit",proc=false){
  if(monster?.type!=="charger")return baseApplyDamage.call(this,monster,damage,slot,tier,at,knock,source,proc);
  const run=this.room?.run;if(!run||!monster)return{actual:0,killed:false};
  this.advanceOneChargerTo(monster,at);ensureChargerState(monster,at);this.materialize(monster,at);
  const phaseBefore=monster.chargerPhase,player=run.players?.find(p=>p.slot===slot)||null,ai=source==='ai'?run.ai?.find(a=>a.slot===slot)||null:null;
  let raw=Math.max(0,Number(damage)||0);if(source==='ai')raw=Math.round(raw*aiStageMul(run.stage||1));
  const actual=Math.max(1,Math.round(raw*(CHARGER.armor??1)));monster.hp-=actual;
  let push=0;
  if(knock){
    const rank=player?.upgrades?.knock||0;let mul=1+rank*.10;if(player?.__v036TankLv6&&source==='hit')mul*=1.30;
    push=tierKnockBase(tier)*CHARGER.knockResist*mul;monster.x=Math.min(.985,monster.x+push);
  }
  let killed=false;
  if(monster.hp<=0){
    killed=true;run.kills=(run.kills||0)+1;
    if(player){player.kills=(player.kills||0)+1;player.coin=(player.coin||0)+CHARGER.reward;player.killCoinEarned=(player.killCoinEarned||0)+CHARGER.reward}
    if(ai){ai.kills=(ai.kills||0)+1;ai.killCoinEarned=(ai.killCoinEarned||0)+CHARGER.reward}
    run.monsters=run.monsters.filter(m=>m.id!==monster.id);
  }
  if(player)player.damage=(player.damage||0)+actual;if(ai)ai.damage=(ai.damage||0)+actual;
  this.event({type:source,slot,targetId:monster.id,tier,damage:actual,rawDamage:raw,armor:CHARGER.armor??1,monsterType:'charger',chargerPhase:phaseBefore,killed,procCrit:!!proc,stage:run.stage},at);
  let interrupted=false;
  if(!killed&&phaseBefore==='windup'&&push>0){
    interrupted=true;monster.chargerPhase='advance';monster.chargerPhaseAt=at;monster.refAt=at;monster.chargerRearmUntil=at+CHARGER.rearmMs;
    this.event({type:'monster-state',targetId:monster.id,monsterType:'charger',phase:'advance',reason:'windup-interrupt',phaseAt:at,rearmUntil:monster.chargerRearmUntil,push},at);
  }
  return{actual,killed,rawDamage:raw,armor:CHARGER.armor??1,interrupted,push};
};

function processChargerWallHits(room,at){
  const run=room.room?.run;if(!run||run.status!=='combat')return false;
  const due=(run.monsters||[]).filter(m=>m.type==='charger').map(monster=>({monster,hitAt:room.wallAt(monster)})).filter(x=>x.hitAt<=at+.5).sort((a,b)=>a.hitAt-b.hitAt||a.monster.id-b.monster.id);
  let changed=false;
  for(const {monster,hitAt} of due){
    if(!run.monsters.some(m=>m.id===monster.id))continue;
    room.advanceOneChargerTo(monster,hitAt);room.materialize(monster,hitAt);run.monsters=run.monsters.filter(m=>m.id!==monster.id);
    const defRank=(run.players||[]).reduce((n,p)=>n+(p.upgrades?.def||0),0),defense=Math.max(0,Math.min(.60,defRank*.025));
    const incoming=Math.max(1,Math.round(CHARGER.wallDamage*(1-defense)));run.baseHp=Math.max(0,run.baseHp-incoming);
    room.event({type:'wall',targetId:monster.id,monsterType:'charger',damage:incoming,baseHp:run.baseHp,stage:run.stage},hitAt);changed=true;
    if(room.checkEnd(hitAt))break;
  }
  return changed;
}

const basePlayerAction=TimingDefenseRoom.prototype.playerAction;
TimingDefenseRoom.prototype.playerAction=function(participant,body,at){this.advanceChargersTo(at);return basePlayerAction.call(this,participant,body,at)};
const baseProcessAt=TimingDefenseRoom.prototype.processAt;
TimingDefenseRoom.prototype.processAt=function(at){
  const phaseChanged=this.advanceChargersTo(at),wallChanged=processChargerWallHits(this,at),changed=baseProcessAt.call(this,at);
  if((phaseChanged||wallChanged)&&this.room?.run&&!changed)this.room.run.revision++;
  return phaseChanged||wallChanged||changed;
};
const baseNextDueAt=TimingDefenseRoom.prototype.nextDueAt;
TimingDefenseRoom.prototype.nextDueAt=function(){
  let due=baseNextDueAt.call(this),run=this.room?.run;if(!run||run.status!=='combat')return due;
  for(const m of run.monsters||[])if(m.type==='charger'){
    const t=nextChargerTransitionAt(m),w=this.wallAt(m);
    if(Number.isFinite(t))due=due==null?t:Math.min(due,t);
    if(Number.isFinite(w))due=due==null?w:Math.min(due,w);
  }
  return due;
};

const baseRunPublic=TimingDefenseRoom.prototype.runPublic;
TimingDefenseRoom.prototype.runPublic=function(at){
  const out=baseRunPublic.call(this,at),run=this.room?.run;if(!out||!run)return out;
  const byId=new Map((run.monsters||[]).map(m=>[m.id,m]));
  out.monsters=(out.monsters||[]).map(sm=>{
    const m=byId.get(sm.id);if(!m||m.type!=='charger')return sm;ensureChargerState(m,at);
    return{...sm,x:Math.max(WALL_X,this.xAt(m,at)),size:CHARGER.size,chargerPhase:m.chargerPhase,chargerPhaseAt:m.chargerPhaseAt,chargerRearmUntil:m.chargerRearmUntil,chargerTriggerX:m.chargerTriggerX,chargerWindupMs:CHARGER.windupMs,chargerBaseSpeed:CHARGER.speed,chargerChargeSpeed:CHARGER.chargeSpeed};
  });
  return out;
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==='GET'&&url.pathname==='/api/health')return json({
      ok:true,service:'timing-defense-v042-charger-state-capability',version:'0.42-cf.1',
      transport:'websocket-hibernation-per-socket-event-cursor',authority:'v041-plus-stage-independent-charger-state',
      charger:{status:'capability-enabled',hp:CHARGER.hp,baseSpeed:CHARGER.speed,windupMs:CHARGER.windupMs,chargeSpeed:CHARGER.chargeSpeed,triggerX:CHARGER.triggerX,rearmMs:CHARGER.rearmMs,knockResist:CHARGER.knockResist,reward:CHARGER.reward,balance:'provisional'},
      campaign:{legacyStage4_10:'blocked',final50:'not-authored'},scope:'charger-authoritative-state-machine'
    });
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom, CHARGER, ensureChargerState, nextChargerTransitionAt, processChargerWallHits };
