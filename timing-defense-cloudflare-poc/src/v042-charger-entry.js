import baseWorker, { TimingDefenseRoom } from "./v041-flyer-audit-entry.js";
import { meta, chargerNext } from "./monster-capability-v1.js";

// Timing Defense v0.42 capability slice C — CHARGER authoritative state machine.
// Stage-number-independent. No legacy encounter recipe is enabled.
// All coefficients are provisional capability-test anchors, not production balance freeze.

const CHARGER={...meta('charger'),size:1.00}; // size=1.00 is a neutral geometry test anchor only.
const TRIGGER_X=.62;
const WALL_X=.155;
function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}
function aiStageMul(stage){return 1+Math.max(0,(Number(stage)||1)-1)*.035}
function tierKnockBase(tier){
  const critical=tier==="CRITICAL",perfect=critical||tier==="PERFECT"||tier==="SUPER",good=perfect||tier==="GOOD"||tier==="GREAT";
  return critical?.047:perfect?.024:good?.013:.006;
}
function ensureCharger(monster,at=0){
  if(monster?.type!=="charger")return monster;
  if(!["advance","windup","charge","resolved"].includes(monster.chargerPhase))monster.chargerPhase="advance";
  if(!Number.isFinite(Number(monster.chargerPhaseAt)))monster.chargerPhaseAt=Number.isFinite(Number(monster.refAt))?Number(monster.refAt):Number(at)||0;
  if(!Number.isFinite(Number(monster.chargerRearmUntil)))monster.chargerRearmUntil=0;
  return monster;
}
function phaseSpeed(monster){
  ensureCharger(monster);
  return monster.chargerPhase==="charge"?CHARGER.chargeSpeed:monster.chargerPhase==="windup"||monster.chargerPhase==="resolved"?0:CHARGER.speed;
}
function transitionDue(monster){
  ensureCharger(monster);
  if(monster.chargerPhase==="windup")return monster.chargerPhaseAt+CHARGER.windupMs;
  if(monster.chargerPhase!=="advance")return null;
  const cross=monster.x<=TRIGGER_X?monster.refAt:monster.refAt+((monster.x-TRIGGER_X)/CHARGER.speed)*1000;
  return Math.max(cross,Number(monster.chargerRearmUntil)||0);
}

const baseXAt=TimingDefenseRoom.prototype.xAt;
TimingDefenseRoom.prototype.xAt=function(monster,at){
  if(monster?.type!=="charger")return baseXAt.call(this,monster,at);
  ensureCharger(monster,at);const speed=phaseSpeed(monster);
  return monster.x-speed*Math.max(0,(Number(at)||0)-monster.refAt)/1000;
};
const baseWallAt=TimingDefenseRoom.prototype.wallAt;
TimingDefenseRoom.prototype.wallAt=function(monster){
  if(monster?.type!=="charger")return baseWallAt.call(this,monster);
  ensureCharger(monster);
  if(monster.chargerPhase==="windup")return Infinity;
  if(monster.x<=WALL_X)return monster.refAt;
  const speed=phaseSpeed(monster);return speed>0?monster.refAt+((monster.x-WALL_X)/speed)*1000:Infinity;
};
const baseMaterialize=TimingDefenseRoom.prototype.materialize;
TimingDefenseRoom.prototype.materialize=function(monster,at){
  if(monster?.type!=="charger")return baseMaterialize.call(this,monster,at);
  ensureCharger(monster,at);monster.x=this.xAt(monster,at);monster.refAt=at;return monster;
};

TimingDefenseRoom.prototype.nextChargerTransitionAt=function(monster){return monster?.type==="charger"?transitionDue(monster):null};
TimingDefenseRoom.prototype.processChargerTransitions=function(at){
  const run=this.room?.run;if(!run||run.status!=="combat")return false;
  let changed=false;
  for(const monster of [...run.monsters].filter(m=>m.type==="charger").sort((a,b)=>a.id-b.id)){
    let guard=0;
    while(run.monsters.some(m=>m.id===monster.id)&&guard++<4){
      ensureCharger(monster,at);const due=transitionDue(monster);
      if(!Number.isFinite(due)||due>at+.5)break;
      this.materialize(monster,due);
      if(monster.chargerPhase==="advance"){
        const next=chargerNext({phase:"advance",phaseAt:monster.chargerPhaseAt,rearmUntil:monster.chargerRearmUntil},{at:due,atTrigger:true});
        monster.chargerPhase=next.phase;monster.chargerPhaseAt=due;monster.chargerRearmUntil=next.rearmUntil||0;monster.refAt=due;
        this.event({type:"charger-phase",targetId:monster.id,phase:"windup",phaseAt:due,windupEndAt:due+CHARGER.windupMs,triggerX:TRIGGER_X},due);changed=true;
      }else if(monster.chargerPhase==="windup"){
        const next=chargerNext({phase:"windup",phaseAt:monster.chargerPhaseAt,rearmUntil:monster.chargerRearmUntil},{at:due});
        monster.chargerPhase=next.phase;monster.chargerPhaseAt=due;monster.refAt=due;
        this.event({type:"charger-phase",targetId:monster.id,phase:"charge",phaseAt:due,chargeSpeed:CHARGER.chargeSpeed},due);changed=true;
      }else break;
    }
  }
  return changed;
};

const baseApplyDamage=TimingDefenseRoom.prototype.applyDamage;
TimingDefenseRoom.prototype.applyDamage=function(monster,damage,slot,tier,at,knock=true,source="hit",proc=false){
  if(monster?.type!=="charger")return baseApplyDamage.call(this,monster,damage,slot,tier,at,knock,source,proc);
  const run=this.room?.run;if(!run||!monster)return{actual:0,killed:false};
  ensureCharger(monster,at);this.materialize(monster,at);
  const player=run.players?.find(p=>p.slot===slot)||null;
  const ai=source==="ai"?run.ai?.find(a=>a.slot===slot)||null:null;
  let raw=Math.max(0,Number(damage)||0);if(source==="ai")raw=Math.round(raw*aiStageMul(run.stage||1));
  const actual=Math.max(1,Math.round(raw*(CHARGER.armor??1)));monster.hp-=actual;

  let push=0,interrupted=false;
  if(knock){
    const rank=player?.upgrades?.knock||0;let mul=1+rank*.10;
    if(player?.__v036TankLv6&&source==="hit")mul*=1.30;
    push=tierKnockBase(tier)*CHARGER.knockResist*mul;
    if(push>0)monster.x=Math.min(.985,monster.x+push);
    if(push>0&&monster.hp>0&&monster.chargerPhase==="windup"){
      const next=chargerNext({phase:"windup",phaseAt:monster.chargerPhaseAt,rearmUntil:monster.chargerRearmUntil},{at,knockback:push});
      monster.chargerPhase=next.phase;monster.chargerPhaseAt=at;monster.chargerRearmUntil=next.rearmUntil;monster.refAt=at;interrupted=true;
      this.event({type:"charger-phase",targetId:monster.id,phase:"advance",phaseAt:at,interrupted:true,rearmUntil:next.rearmUntil},at);
    }
  }

  let killed=false;
  if(monster.hp<=0){
    killed=true;run.kills=(run.kills||0)+1;
    if(player){player.kills=(player.kills||0)+1;player.coin=(player.coin||0)+CHARGER.reward;player.killCoinEarned=(player.killCoinEarned||0)+CHARGER.reward}
    if(ai){ai.kills=(ai.kills||0)+1;ai.killCoinEarned=(ai.killCoinEarned||0)+CHARGER.reward}
    run.monsters=run.monsters.filter(m=>m.id!==monster.id);
  }
  if(player)player.damage=(player.damage||0)+actual;if(ai)ai.damage=(ai.damage||0)+actual;
  this.event({type:source,slot,targetId:monster.id,tier,damage:actual,rawDamage:raw,armor:CHARGER.armor??1,monsterType:"charger",killed,procCrit:!!proc,stage:run.stage,chargerInterrupted:interrupted},at);
  return{actual,killed,rawDamage:raw,armor:CHARGER.armor??1,chargerInterrupted:interrupted,push};
};

TimingDefenseRoom.prototype.processChargerWallHits=function(at){
  const run=this.room?.run;if(!run||run.status!=="combat")return false;
  const due=[...run.monsters].filter(m=>m.type==="charger").map(m=>({m,hitAt:this.wallAt(m)})).filter(x=>Number.isFinite(x.hitAt)&&x.hitAt<=at+.5).sort((a,b)=>a.hitAt-b.hitAt||a.m.id-b.m.id);
  let changed=false;
  for(const {m,hitAt} of due){
    if(!run.monsters.some(x=>x.id===m.id))continue;const exactAt=Math.min(at,hitAt);this.materialize(m,exactAt);m.chargerPhase="resolved";m.chargerPhaseAt=exactAt;
    run.monsters=run.monsters.filter(x=>x.id!==m.id);
    const defRank=(run.players||[]).reduce((n,p)=>n+(p.upgrades?.def||0),0),defense=Math.max(0,Math.min(.60,defRank*.025));
    const incoming=Math.max(1,Math.round(CHARGER.wallDamage*(1-defense)));run.baseHp=Math.max(0,run.baseHp-incoming);
    this.event({type:"wall",targetId:m.id,monsterType:"charger",damage:incoming,baseHp:run.baseHp,stage:run.stage},exactAt);changed=true;
    if(this.checkEnd(exactAt))break;
  }
  return changed;
};

const baseProcessAt=TimingDefenseRoom.prototype.processAt;
TimingDefenseRoom.prototype.processAt=function(at){
  const transitions=this.processChargerTransitions(at),walls=this.processChargerWallHits(at),base=baseProcessAt.call(this,at);
  if((transitions||walls)&&this.room?.run&&!base)this.room.run.revision++;
  return transitions||walls||base;
};
const baseNextDueAt=TimingDefenseRoom.prototype.nextDueAt;
TimingDefenseRoom.prototype.nextDueAt=function(){
  const base=baseNextDueAt.call(this),run=this.room?.run;if(!run||run.status!=="combat")return base;
  let due=base==null?Infinity:base;
  for(const m of run.monsters||[]){if(m.type!=="charger")continue;const t=transitionDue(m);if(Number.isFinite(t))due=Math.min(due,t)}
  return Number.isFinite(due)?due:null;
};

const baseRunPublic=TimingDefenseRoom.prototype.runPublic;
TimingDefenseRoom.prototype.runPublic=function(at){
  const out=baseRunPublic.call(this,at),run=this.room?.run;if(!out||!run)return out;const byId=new Map((run.monsters||[]).map(m=>[m.id,m]));
  out.monsters=(out.monsters||[]).map(sm=>{const m=byId.get(sm.id);if(!m||m.type!=="charger")return sm;ensureCharger(m,at);return{...sm,x:this.xAt(m,at),chargerPhase:m.chargerPhase,chargerPhaseAt:m.chargerPhaseAt,chargerRearmUntil:m.chargerRearmUntil,chargerTriggerX:TRIGGER_X,chargerWindupMs:CHARGER.windupMs,chargerChargeSpeed:CHARGER.chargeSpeed,size:CHARGER.size}});
  return out;
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health")return json({
      ok:true,service:"timing-defense-v042-charger-capability",version:"0.42-cf.1",transport:"websocket-hibernation-per-socket-event-cursor",authority:"v041-plus-stage-independent-charger-state-machine",
      charger:{status:"capability-enabled",hp:CHARGER.hp,speed:CHARGER.speed,chargeSpeed:CHARGER.chargeSpeed,windupMs:CHARGER.windupMs,rearmMs:CHARGER.rearmMs,triggerX:TRIGGER_X,knockResist:CHARGER.knockResist,reward:CHARGER.reward,size:CHARGER.size,balance:"provisional"},
      campaign:{legacyStage4_10:"blocked",final50:"not-authored"},scope:"charger-authoritative-state-machine"
    });
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom, CHARGER, TRIGGER_X, ensureCharger, transitionDue };
