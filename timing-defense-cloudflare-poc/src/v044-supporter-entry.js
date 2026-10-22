import baseWorker, { TimingDefenseRoom } from "./v043-splitter-entry.js";
import { meta } from "./monster-capability-v1.js";
import { CHARGER } from "./v042-charger-entry.js";

// Timing Defense v0.44 capability slice E — SUPPORTER authoritative movement aura.
// Stage-number-independent. No final campaign recipe is enabled here.
// Geometry/tuning below are PROVISIONAL capability-test semantics, not production balance freeze.

const SUPPORTER=Object.freeze({...meta('supporter'),size:1.00});
const WALL_X=.155;
const ROOT_EPS_MS=.001; // numerical side-of-boundary epsilon; not a gameplay tick
const ROOT_TOL_MS=.001;
const FLYER_SCAN_MS=5;

function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}
function aiStageMul(stage){return 1+Math.max(0,(Number(stage)||1)-1)*.035}
function tierKnockBase(tier){
  const critical=tier==='CRITICAL',perfect=critical||tier==='PERFECT'||tier==='SUPER',good=perfect||tier==='GOOD'||tier==='GREAT';
  return critical?.047:perfect?.024:good?.013:.006;
}
function ids(value){return Array.isArray(value)?value.map(Number).filter(Number.isFinite).sort((a,b)=>a-b):[]}
function sameIds(a,b){const x=ids(a),y=ids(b);return x.length===y.length&&x.every((v,i)=>v===y[i])}
function eligibleTarget(monster){return !!monster&&!monster.boss}
function auraSources(monster){return ids(monster?.supportAuraSources)}
function pairMembership(target,sourceId){return auraSources(target).includes(Number(sourceId))}
function ensureAuraState(monster){if(!monster)return monster;if(!Array.isArray(monster.supportAuraSources))monster.supportAuraSources=[];monster.supportAuraSources=ids(monster.supportAuraSources).filter(id=>id!==Number(monster.id));return monster}

TimingDefenseRoom.prototype.movementSpeedMultiplier=function(monster){
  ensureAuraState(monster);
  return auraSources(monster).length?SUPPORTER.auraSpeedMul:1;
};

const inheritedXAt=TimingDefenseRoom.prototype.xAt;
TimingDefenseRoom.prototype.xAt=function(monster,at){
  if(!monster)return 0;
  ensureAuraState(monster);
  const ref=Number(monster.refAt)||0,dt=Math.max(0,(Number(at)||0)-ref),mul=this.movementSpeedMultiplier(monster);
  if(monster.type==='supporter')return monster.x-SUPPORTER.speed*mul*dt/1000;
  if(mul===1)return inheritedXAt.call(this,monster,at);
  // All inherited current movement segments are linear in X. Scaling elapsed
  // time composes the aura without altering each archetype's own base speed/phase.
  return inheritedXAt.call(this,monster,ref+dt*mul);
};

TimingDefenseRoom.prototype.currentSegmentSpeed=function(monster,at=monster?.refAt||0){
  if(!monster)return 0;
  const t=Math.max(Number(at)||0,Number(monster.refAt)||0),span=10;
  const x0=this.xAt(monster,t),x1=this.xAt(monster,t+span);
  const v=(x0-x1)/(span/1000);
  return Number.isFinite(v)&&v>0?v:0;
};

// wallAt intentionally predicts only the current motion segment. Any aura
// crossing or CHARGER phase transition that comes first is itself a nextDueAt event.
TimingDefenseRoom.prototype.wallAt=function(monster){
  if(!monster)return Infinity;
  if(monster.x<=WALL_X)return Number(monster.refAt)||0;
  const speed=this.currentSegmentSpeed(monster,monster.refAt);
  if(!(speed>0))return Infinity;
  return Number(monster.refAt||0)+(monster.x-WALL_X)/speed*1000;
};

function chargerTransitionAt(room,monster){
  if(monster?.type!=='charger')return null;
  const phase=monster.chargerPhase||'advance';
  if(phase==='windup')return Number(monster.chargerPhaseAt||monster.refAt||0)+CHARGER.windupMs;
  if(phase!=='advance')return null;
  const speed=room.currentSegmentSpeed(monster,monster.refAt);
  if(!(speed>0))return null;
  const triggerX=Number.isFinite(Number(monster.chargerTriggerX))?Number(monster.chargerTriggerX):CHARGER.triggerX;
  const crossing=monster.x<=triggerX?Number(monster.refAt||0):Number(monster.refAt||0)+(monster.x-triggerX)/speed*1000;
  const due=Math.max(crossing,Number(monster.chargerRearmUntil)||0),wall=room.wallAt(monster);
  return wall<=due+.0001?null:due;
}

// Override the v0.42 transition executor so CHARGER trigger timing composes with aura speed.
TimingDefenseRoom.prototype.advanceOneChargerTo=function(monster,at){
  if(monster?.type!=='charger')return false;
  if(!['advance','windup','charge'].includes(monster.chargerPhase))monster.chargerPhase='advance';
  if(!Number.isFinite(Number(monster.chargerPhaseAt)))monster.chargerPhaseAt=Number(monster.refAt)||Number(at)||0;
  if(!Number.isFinite(Number(monster.chargerRearmUntil)))monster.chargerRearmUntil=0;
  if(!Number.isFinite(Number(monster.chargerTriggerX)))monster.chargerTriggerX=CHARGER.triggerX;
  let changed=false,guard=0;
  while(guard++<4){
    const due=chargerTransitionAt(this,monster);
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

TimingDefenseRoom.prototype.auraPointAt=function(monster,at){
  return{x:this.xAt(monster,at),y:typeof this.yAt==='function'?this.yAt(monster,at):(Number(monster?.y)||0)};
};
TimingDefenseRoom.prototype.auraPairInsideAt=function(source,target,at){
  if(!source||!target||source.id===target.id||source.type!=='supporter'||!eligibleTarget(target))return false;
  const a=this.auraPointAt(source,at),b=this.auraPointAt(target,at);
  return Math.hypot(a.x-b.x,a.y-b.y)<=SUPPORTER.auraRadius+1e-12;
};

TimingDefenseRoom.prototype.reconcileSupportAuraAt=function(at){
  const run=this.room?.run;if(!run)return false;
  const supporters=(run.monsters||[]).filter(m=>m.type==='supporter').sort((a,b)=>a.id-b.id),targets=(run.monsters||[]).filter(eligibleTarget).sort((a,b)=>a.id-b.id);
  const plan=[];
  for(const target of targets){
    ensureAuraState(target);
    const next=[];
    for(const source of supporters){
      if(source.id===target.id)continue;
      if(this.auraPairInsideAt(source,target,at))next.push(source.id);
    }
    next.sort((a,b)=>a-b);
    if(!sameIds(target.supportAuraSources,next))plan.push({target,next,old:auraSources(target)});
  }
  // Position is continuous. Materialize with OLD membership through the exact transition timestamp.
  for(const {target} of plan)this.materialize(target,at);
  for(const {target,next} of plan){target.supportAuraSources=next;target.supportAuraChangedAt=at}
  run.supportAuraAt=at;
  return plan.length>0;
};

function staticPairCrossing(room,source,target,start,end,currentInside){
  const a=room.auraPointAt(source,start),b=room.auraPointAt(target,start),vs=room.currentSegmentSpeed(source,start),vt=room.currentSegmentSpeed(target,start);
  const dx=b.x-a.x,dy=b.y-a.y,dv=vt-vs,r=SUPPORTER.auraRadius;
  const A=dv*dv,B=-2*dx*dv,C=dx*dx+dy*dy-r*r;
  if(A<1e-18)return null;
  const disc=B*B-4*A*C;if(disc<0)return null;
  const root=Math.sqrt(Math.max(0,disc)),roots=[(-B-root)/(2*A),(-B+root)/(2*A)].filter(s=>s>ROOT_EPS_MS/1000).sort((x,y)=>x-y);
  for(const sec of roots){
    const t=start+sec*1000;if(t>end+ROOT_TOL_MS)continue;
    const probe=Math.min(end,t+ROOT_EPS_MS),after=room.auraPairInsideAt(source,target,probe);
    if(after!==currentInside)return probe;
  }
  return null;
}

function dynamicFlyerCrossing(room,source,target,start,end,currentInside){
  if(end<=start+ROOT_EPS_MS)return null;
  let lo=start,state=currentInside;
  for(let t=Math.min(end,start+FLYER_SCAN_MS);t<=end+1e-9;t=Math.min(end,t+FLYER_SCAN_MS)){
    const next=room.auraPairInsideAt(source,target,t);
    if(next!==state){
      let a=lo,b=t;
      while(b-a>ROOT_TOL_MS){const mid=(a+b)/2;if(room.auraPairInsideAt(source,target,mid)===state)a=mid;else b=mid}
      return b;
    }
    if(t>=end)break;lo=t;
  }
  return null;
}

TimingDefenseRoom.prototype.nextSupportAuraCrossingAt=function(start,horizon){
  const run=this.room?.run;if(!run||run.status!=='combat')return null;
  const supporters=(run.monsters||[]).filter(m=>m.type==='supporter').sort((a,b)=>a.id-b.id),targets=(run.monsters||[]).filter(eligibleTarget).sort((a,b)=>a.id-b.id);
  let best=null;
  for(const source of supporters)for(const target of targets){
    if(source.id===target.id)continue;
    const current=pairMembership(target,source.id),t=target.type==='flyer'?dynamicFlyerCrossing(this,source,target,start,horizon,current):staticPairCrossing(this,source,target,start,horizon,current);
    if(Number.isFinite(t)&&(best==null||t<best))best=t;
  }
  return best;
};

function processSupporterWallHits(room,at){
  const run=room.room?.run;if(!run||run.status!=='combat')return false;
  const due=(run.monsters||[]).filter(m=>m.type==='supporter').map(monster=>({monster,hitAt:room.wallAt(monster)})).filter(x=>x.hitAt<=at+.5).sort((a,b)=>a.hitAt-b.hitAt||a.monster.id-b.monster.id);
  let changed=false;
  for(const {monster,hitAt} of due){
    if(!run.monsters.some(m=>m.id===monster.id))continue;
    room.materialize(monster,hitAt);run.monsters=run.monsters.filter(m=>m.id!==monster.id);
    const defRank=(run.players||[]).reduce((n,p)=>n+(p.upgrades?.def||0),0),defense=Math.max(0,Math.min(.60,defRank*.025)),incoming=Math.max(1,Math.round(SUPPORTER.wallDamage*(1-defense)));
    run.baseHp=Math.max(0,run.baseHp-incoming);room.event({type:'wall',targetId:monster.id,monsterType:'supporter',damage:incoming,baseHp:run.baseHp,stage:run.stage},hitAt);changed=true;
    room.reconcileSupportAuraAt(hitAt);
    if(room.checkEnd(hitAt))break;
  }
  return changed;
}

const inheritedApplyDamage=TimingDefenseRoom.prototype.applyDamage;
TimingDefenseRoom.prototype.applyDamage=function(monster,damage,slot,tier,at,knock=true,source='hit',proc=false){
  this.reconcileSupportAuraAt(at);
  if(monster?.type!=='supporter'){
    const out=inheritedApplyDamage.call(this,monster,damage,slot,tier,at,knock,source,proc);
    this.reconcileSupportAuraAt(at);return out;
  }
  const run=this.room?.run;if(!run||!monster)return{actual:0,killed:false};
  ensureAuraState(monster);this.materialize(monster,at);
  const player=run.players?.find(p=>p.slot===slot)||null,ai=source==='ai'?run.ai?.find(a=>a.slot===slot)||null:null;
  let raw=Math.max(0,Number(damage)||0);if(source==='ai')raw=Math.round(raw*aiStageMul(run.stage||1));
  const actual=Math.max(1,Math.round(raw*(SUPPORTER.armor??1)));monster.hp-=actual;
  let push=0;
  if(knock){const rank=player?.upgrades?.knock||0;let mul=1+rank*.10;if(player?.__v036TankLv6&&source==='hit')mul*=1.30;push=tierKnockBase(tier)*SUPPORTER.knockResist*mul;monster.x=Math.min(.985,monster.x+push)}
  let killed=false;
  if(monster.hp<=0){
    killed=true;run.kills=(run.kills||0)+1;
    if(player){player.kills=(player.kills||0)+1;player.coin=(player.coin||0)+SUPPORTER.reward;player.killCoinEarned=(player.killCoinEarned||0)+SUPPORTER.reward}
    if(ai){ai.kills=(ai.kills||0)+1;ai.killCoinEarned=(ai.killCoinEarned||0)+SUPPORTER.reward}
    run.monsters=run.monsters.filter(m=>m.id!==monster.id);
  }
  if(player)player.damage=(player.damage||0)+actual;if(ai)ai.damage=(ai.damage||0)+actual;
  this.event({type:source,slot,targetId:monster.id,tier,damage:actual,rawDamage:raw,armor:SUPPORTER.armor??1,monsterType:'supporter',killed,procCrit:!!proc,stage:run.stage},at);
  this.reconcileSupportAuraAt(at);
  return{actual,killed,rawDamage:raw,armor:SUPPORTER.armor??1,push};
};

const inheritedProcessAt=TimingDefenseRoom.prototype.processAt;
TimingDefenseRoom.prototype.processAt=function(at){
  let changed=this.reconcileSupportAuraAt(at);
  const supporterWall=processSupporterWallHits(this,at);changed=supporterWall||changed;
  if(supporterWall)changed=this.reconcileSupportAuraAt(at)||changed;
  const baseChanged=inheritedProcessAt.call(this,at);changed=baseChanged||changed;
  changed=this.reconcileSupportAuraAt(at)||changed;
  if(changed&&this.room?.run)this.room.run.revision++;
  return changed;
};

const inheritedNextDueAt=TimingDefenseRoom.prototype.nextDueAt;
TimingDefenseRoom.prototype.nextDueAt=function(){
  let due=inheritedNextDueAt.call(this),run=this.room?.run;if(!run||run.status!=='combat')return due;
  const start=Number.isFinite(Number(run.supportAuraAt))?Number(run.supportAuraAt):Math.max(0,...(run.monsters||[]).map(m=>Number(m.refAt)||0));
  // Replace the inherited CHARGER estimate with an earlier aura-aware estimate when needed.
  for(const m of run.monsters||[])if(m.type==='charger'){
    const t=chargerTransitionAt(this,m);if(Number.isFinite(t))due=due==null?t:Math.min(due,t);
  }
  let horizon=Number.isFinite(due)?due:start+30000;if(horizon<=start+ROOT_EPS_MS)horizon=start+ROOT_EPS_MS;
  const crossing=this.nextSupportAuraCrossingAt(start,horizon);if(Number.isFinite(crossing))due=due==null?crossing:Math.min(due,crossing);
  return due;
};

const inheritedRunPublic=TimingDefenseRoom.prototype.runPublic;
TimingDefenseRoom.prototype.runPublic=function(at){
  const out=inheritedRunPublic.call(this,at),run=this.room?.run;if(!out||!run)return out;
  const byId=new Map((run.monsters||[]).map(m=>[m.id,m]));
  out.monsters=(out.monsters||[]).map(sm=>{
    const m=byId.get(sm.id);if(!m)return sm;ensureAuraState(m);
    const speed=this.currentSegmentSpeed(m,at),extra={supportAuraActive:auraSources(m).length>0,supportAuraSources:auraSources(m),moveSpeedMul:this.movementSpeedMultiplier(m),effectiveXSpeed:speed};
    if(m.type==='supporter')Object.assign(extra,{size:SUPPORTER.size,auraRadius:SUPPORTER.auraRadius,auraSpeedMul:SUPPORTER.auraSpeedMul});
    return{...sm,...extra};
  });
  return out;
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==='GET'&&url.pathname==='/api/health')return json({
      ok:true,service:'timing-defense-v044-supporter-aura-capability',version:'0.44-cf.1',
      transport:'websocket-hibernation-per-socket-event-cursor',authority:'v043-plus-event-driven-supporter-aura',
      supporter:{status:'capability-enabled',hp:SUPPORTER.hp,speed:SUPPORTER.speed,wallDamage:SUPPORTER.wallDamage,knockResist:SUPPORTER.knockResist,reward:SUPPORTER.reward,auraRadius:SUPPORTER.auraRadius,auraSpeedMul:SUPPORTER.auraSpeedMul,stacking:false,geometry:'provisional-authoritative-2d-euclidean',balance:'provisional'},
      movement:{mode:'event-driven-boundary-crossing',fixedTick:false,rootToleranceMs:ROOT_TOL_MS},
      campaign:{legacyStage4_10:'blocked',final50:'not-authored'},scope:'supporter-authoritative-dynamic-speed-aura'
    });
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom, SUPPORTER, ROOT_EPS_MS, ROOT_TOL_MS, processSupporterWallHits, chargerTransitionAt };
