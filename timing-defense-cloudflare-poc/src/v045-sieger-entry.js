import baseWorker, { TimingDefenseRoom } from "./v044-supporter-entry.js";
import { meta } from "./monster-capability-v1.js";

// Timing Defense v0.45 capability slice F — SIEGER authoritative objective-pressure kernel.
// Stage-number-independent. No final campaign recipe is enabled here.
// Numeric values/cadence are PROVISIONAL capability-test semantics only.

const BASE=meta('sieger');
const SIEGER=Object.freeze({...BASE,size:1.00,cooldownMs:Math.max(0,BASE.repeatMs-BASE.windupMs)});
const PHASES=new Set(['advance','windup','cooldown']);
const STAND_EPS=1e-9;

function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}
function aiStageMul(stage){return 1+Math.max(0,(Number(stage)||1)-1)*.035}
function tierKnockBase(tier){
  const critical=tier==='CRITICAL',perfect=critical||tier==='PERFECT'||tier==='SUPER',good=perfect||tier==='GOOD'||tier==='GREAT';
  return critical?.047:perfect?.024:good?.013:.006;
}
function teamDefense(run){
  const ranks=(run?.players||[]).reduce((n,p)=>n+(p.upgrades?.def||0),0);
  return Math.max(0,Math.min(.60,ranks*.025));
}
function ensureSiegerState(monster,at){
  if(monster?.type!=='sieger')return monster;
  if(!PHASES.has(monster.siegerPhase))monster.siegerPhase='advance';
  if(!Number.isFinite(Number(monster.siegerPhaseAt)))monster.siegerPhaseAt=Number(monster.refAt)||Number(at)||0;
  if(!Number.isFinite(Number(monster.size)))monster.size=SIEGER.size;
  if(monster.siegerNextAt!==null&&!Number.isFinite(Number(monster.siegerNextAt)))monster.siegerNextAt=null;
  return monster;
}
function siegeApproachSpeed(room,monster){
  const mul=typeof room.movementSpeedMultiplier==='function'?room.movementSpeedMultiplier(monster):1;
  return SIEGER.speed*mul;
}
function nextSiegerTransitionAt(room,monster){
  if(monster?.type!=='sieger')return null;
  ensureSiegerState(monster,monster.refAt||0);
  if(monster.siegerPhase==='advance'){
    if(monster.x<=SIEGER.standoffX+STAND_EPS)return Number(monster.refAt)||0;
    const speed=siegeApproachSpeed(room,monster);if(!(speed>0))return null;
    return Number(monster.refAt||0)+(monster.x-SIEGER.standoffX)/speed*1000;
  }
  if(monster.siegerPhase==='windup')return Number.isFinite(Number(monster.siegerNextAt))?Number(monster.siegerNextAt):Number(monster.siegerPhaseAt||monster.refAt||0)+SIEGER.windupMs;
  if(monster.siegerPhase==='cooldown')return Number.isFinite(Number(monster.siegerNextAt))?Number(monster.siegerNextAt):Number(monster.siegerPhaseAt||monster.refAt||0)+SIEGER.cooldownMs;
  return null;
}

const inheritedXAt=TimingDefenseRoom.prototype.xAt;
TimingDefenseRoom.prototype.xAt=function(monster,at){
  if(monster?.type!=='sieger')return inheritedXAt.call(this,monster,at);
  ensureSiegerState(monster,at);
  if(monster.siegerPhase!=='advance')return monster.x;
  const dt=Math.max(0,(Number(at)||0)-Number(monster.refAt||0));
  return monster.x-siegeApproachSpeed(this,monster)*dt/1000;
};

const inheritedWallAt=TimingDefenseRoom.prototype.wallAt;
TimingDefenseRoom.prototype.wallAt=function(monster){
  if(monster?.type==='sieger')return Infinity;
  return inheritedWallAt.call(this,monster);
};

TimingDefenseRoom.prototype.advanceOneSiegerTo=function(monster,at){
  const run=this.room?.run;if(!run||monster?.type!=='sieger'||run.status!=='combat')return false;
  ensureSiegerState(monster,at);let changed=false,guard=0;
  while(guard++<12&&run.status==='combat'&&run.monsters.some(m=>m.id===monster.id)){
    const due=nextSiegerTransitionAt(this,monster);
    if(due==null||due>at+.5)break;
    this.materialize(monster,due);
    if(monster.siegerPhase==='advance'){
      monster.x=SIEGER.standoffX;monster.refAt=due;monster.siegerPhase='windup';monster.siegerPhaseAt=due;monster.siegerNextAt=due+SIEGER.windupMs;
      this.event({type:'monster-state',targetId:monster.id,monsterType:'sieger',phase:'windup',reason:'standoff-arrival',phaseAt:due,nextAt:monster.siegerNextAt},due);changed=true;continue;
    }
    if(monster.siegerPhase==='windup'){
      const defense=teamDefense(run),incoming=Math.max(1,Math.round(SIEGER.shotDamage*(1-defense)));
      run.baseHp=Math.max(0,run.baseHp-incoming);
      monster.siegerPhase='cooldown';monster.siegerPhaseAt=due;monster.siegerNextAt=due+SIEGER.cooldownMs;monster.refAt=due;
      this.event({type:'wall',targetId:monster.id,monsterType:'sieger',siegeShot:true,source:'siege-shot',damage:incoming,rawDamage:SIEGER.shotDamage,defense,baseHp:run.baseHp,stage:run.stage,phase:'cooldown',nextAt:monster.siegerNextAt},due);changed=true;
      if(this.checkEnd(due))break;
      continue;
    }
    if(monster.siegerPhase==='cooldown'){
      monster.siegerPhase='windup';monster.siegerPhaseAt=due;monster.siegerNextAt=due+SIEGER.windupMs;monster.refAt=due;
      this.event({type:'monster-state',targetId:monster.id,monsterType:'sieger',phase:'windup',reason:'cooldown-complete',phaseAt:due,nextAt:monster.siegerNextAt},due);changed=true;continue;
    }
  }
  return changed;
};
TimingDefenseRoom.prototype.advanceSiegersTo=function(at){
  let changed=false;
  for(const m of [...(this.room?.run?.monsters||[])].sort((a,b)=>a.id-b.id))if(m.type==='sieger')changed=this.advanceOneSiegerTo(m,at)||changed;
  return changed;
};

const inheritedApplyDamage=TimingDefenseRoom.prototype.applyDamage;
TimingDefenseRoom.prototype.applyDamage=function(monster,damage,slot,tier,at,knock=true,source='hit',proc=false){
  if(monster?.type!=='sieger')return inheritedApplyDamage.call(this,monster,damage,slot,tier,at,knock,source,proc);
  const run=this.room?.run;if(!run||!monster)return{actual:0,killed:false};
  if(typeof this.reconcileSupportAuraAt==='function')this.reconcileSupportAuraAt(at);
  this.advanceOneSiegerTo(monster,at);ensureSiegerState(monster,at);this.materialize(monster,at);
  const player=run.players?.find(p=>p.slot===slot)||null,ai=source==='ai'?run.ai?.find(a=>a.slot===slot)||null:null;
  let raw=Math.max(0,Number(damage)||0);if(source==='ai')raw=Math.round(raw*aiStageMul(run.stage||1));
  const actual=Math.max(1,Math.round(raw*(SIEGER.armor??1)));monster.hp-=actual;
  let push=0;
  if(knock){
    const rank=player?.upgrades?.knock||0;let mul=1+rank*.10;if(player?.__v036TankLv6&&source==='hit')mul*=1.30;
    push=tierKnockBase(tier)*SIEGER.knockResist*mul;monster.x=Math.min(.985,monster.x+push);
  }
  let killed=false,repositioned=false;
  if(monster.hp<=0){
    killed=true;run.kills=(run.kills||0)+1;
    if(player){player.kills=(player.kills||0)+1;player.coin=(player.coin||0)+SIEGER.reward;player.killCoinEarned=(player.killCoinEarned||0)+SIEGER.reward}
    if(ai){ai.kills=(ai.kills||0)+1;ai.killCoinEarned=(ai.killCoinEarned||0)+SIEGER.reward}
    run.monsters=run.monsters.filter(m=>m.id!==monster.id);
  }else if(push>0&&(monster.siegerPhase==='windup'||monster.siegerPhase==='cooldown')&&monster.x>SIEGER.standoffX+STAND_EPS){
    repositioned=true;monster.siegerPhase='advance';monster.siegerPhaseAt=at;monster.siegerNextAt=null;monster.refAt=at;
  }
  if(player)player.damage=(player.damage||0)+actual;if(ai)ai.damage=(ai.damage||0)+actual;
  this.event({type:source,slot,targetId:monster.id,tier,damage:actual,rawDamage:raw,armor:SIEGER.armor??1,monsterType:'sieger',siegerPhase:monster.siegerPhase,siegerRepositioned:repositioned,killed,procCrit:!!proc,stage:run.stage},at);
  if(typeof this.reconcileSupportAuraAt==='function')this.reconcileSupportAuraAt(at);
  return{actual,killed,rawDamage:raw,armor:SIEGER.armor??1,push,repositioned};
};

const inheritedProcessAt=TimingDefenseRoom.prototype.processAt;
TimingDefenseRoom.prototype.processAt=function(at){
  const siegeChanged=this.advanceSiegersTo(at),baseChanged=inheritedProcessAt.call(this,at);
  if(siegeChanged&&this.room?.run&&!baseChanged)this.room.run.revision++;
  return siegeChanged||baseChanged;
};

const inheritedNextDueAt=TimingDefenseRoom.prototype.nextDueAt;
TimingDefenseRoom.prototype.nextDueAt=function(){
  let due=inheritedNextDueAt.call(this),run=this.room?.run;if(!run||run.status!=='combat')return due;
  for(const m of run.monsters||[])if(m.type==='sieger'){
    const t=nextSiegerTransitionAt(this,m);if(Number.isFinite(t))due=due==null?t:Math.min(due,t);
  }
  return due;
};

const inheritedRunPublic=TimingDefenseRoom.prototype.runPublic;
TimingDefenseRoom.prototype.runPublic=function(at){
  const out=inheritedRunPublic.call(this,at),run=this.room?.run;if(!out||!run)return out;
  const byId=new Map((run.monsters||[]).map(m=>[m.id,m]));
  out.monsters=(out.monsters||[]).map(sm=>{
    const m=byId.get(sm.id);if(m?.type!=='sieger')return sm;ensureSiegerState(m,at);
    return{...sm,x:this.xAt(m,at),size:SIEGER.size,siegerPhase:m.siegerPhase,siegerPhaseAt:m.siegerPhaseAt,siegerNextAt:m.siegerNextAt,siegerStandoffX:SIEGER.standoffX,siegerWindupMs:SIEGER.windupMs,siegerRepeatMs:SIEGER.repeatMs,siegerShotDamage:SIEGER.shotDamage,effectiveXSpeed:typeof this.currentSegmentSpeed==='function'?this.currentSegmentSpeed(m,at):null};
  });
  return out;
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==='GET'&&url.pathname==='/api/health')return json({
      ok:true,service:'timing-defense-v045-sieger-kernel-capability',version:'0.45-cf.1',
      transport:'websocket-hibernation-per-socket-event-cursor',authority:'v044-plus-stage-independent-sieger-kernel',
      sieger:{status:'capability-enabled',hp:SIEGER.hp,approachSpeed:SIEGER.speed,knockResist:SIEGER.knockResist,reward:SIEGER.reward,standoffX:SIEGER.standoffX,windupMs:SIEGER.windupMs,shotDamage:SIEGER.shotDamage,repeatMs:SIEGER.repeatMs,cooldownMs:SIEGER.cooldownMs,balance:'provisional'},
      campaign:{legacyStage4_10:'blocked',final50:'not-authored'},scope:'sieger-authoritative-standoff-repeated-wall-attack'
    });
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom, SIEGER, ensureSiegerState, nextSiegerTransitionAt, teamDefense };
