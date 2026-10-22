import baseWorker, { TimingDefenseRoom } from "./v042-charger-entry.js";
import { meta } from "./monster-capability-v1.js";

// Timing Defense v0.43 capability slice D — SPLITTER authoritative child-spawn kernel.
// Stage-number-independent. No legacy/final campaign recipe is enabled here.
// Numeric values and reward allocation below are PROVISIONAL capability-test accounting only.

const BASE=meta('splitter');
const SPLITTER=Object.freeze({...BASE,size:1.00,reward:4});
const CHILD=Object.freeze({
  hp:BASE.childHp,speed:BASE.childSpeed,wallDamage:BASE.childWallDamage,
  knockResist:BASE.knockResist,armor:BASE.armor,size:.62,reward:2
});
const PROVISIONAL_REWARD_ACCOUNTING=Object.freeze({parent:SPLITTER.reward,childEach:CHILD.reward,package:SPLITTER.reward+CHILD.reward*2,status:'provisional-not-production-frozen'});
const WALL_X=.155;

function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}
function aiStageMul(stage){return 1+Math.max(0,(Number(stage)||1)-1)*.035}
function tierKnockBase(tier){
  const critical=tier==='CRITICAL',perfect=critical||tier==='PERFECT'||tier==='SUPER',good=perfect||tier==='GOOD'||tier==='GREAT';
  return critical?.047:perfect?.024:good?.013:.006;
}
function isSplitterFamily(monster){return monster?.type==='splitter'||monster?.type==='splitter-child'}
function splitterMeta(monster){return monster?.type==='splitter-child'?CHILD:SPLITTER}
function ensureSplitterState(monster){
  if(!isSplitterFamily(monster))return monster;
  if(monster.type==='splitter'){
    if(monster.canSplit!==false)monster.canSplit=true;
    if(!Number.isFinite(Number(monster.size)))monster.size=SPLITTER.size;
    if(!Number.isFinite(Number(monster.splitterGeneration)))monster.splitterGeneration=0;
  }else{
    monster.canSplit=false;
    if(!Number.isFinite(Number(monster.size)))monster.size=CHILD.size;
    if(!Number.isFinite(Number(monster.splitterGeneration)))monster.splitterGeneration=1;
  }
  return monster;
}
function rewardFor(monster){return Number.isFinite(Number(monster?.reward))?Number(monster.reward):splitterMeta(monster).reward}

const baseXAt=TimingDefenseRoom.prototype.xAt;
TimingDefenseRoom.prototype.xAt=function(monster,at){
  if(!isSplitterFamily(monster))return baseXAt.call(this,monster,at);
  ensureSplitterState(monster);const d=splitterMeta(monster),dt=Math.max(0,(Number(at)||0)-Number(monster.refAt||0));
  return monster.x-d.speed*dt/1000;
};

const baseWallAt=TimingDefenseRoom.prototype.wallAt;
TimingDefenseRoom.prototype.wallAt=function(monster){
  if(!isSplitterFamily(monster))return baseWallAt.call(this,monster);
  ensureSplitterState(monster);const d=splitterMeta(monster);
  if(monster.x<=WALL_X)return monster.refAt;
  return monster.refAt+((monster.x-WALL_X)/d.speed)*1000;
};

TimingDefenseRoom.prototype.spawnSplitterChildren=function(parent,at){
  const run=this.room?.run;if(!run||parent?.type!=='splitter'||parent.canSplit===false)return[];
  ensureSplitterState(parent);const x=parent.x,y=parent.y,packageId=parent.splitterPackageId||`splitter:${run.id}:${parent.id}`;
  parent.splitterPackageId=packageId;
  const specs=[{dy:-.018,index:0},{dy:.018,index:1}],children=[];
  for(const spec of specs){
    const id=run.nextMonsterId++;
    children.push({
      id,type:'splitter-child',parentId:parent.id,splitterPackageId:packageId,splitterChildIndex:spec.index,splitterGeneration:1,canSplit:false,
      x,y:y+spec.dy,refAt:at,hp:CHILD.hp,maxHp:CHILD.hp,size:CHILD.size,reward:CHILD.reward,boss:false
    });
  }
  run.monsters.push(...children);
  return children;
};

// Dedicated family combat path prevents SPLITTER and its children from silently
// falling back to GRUNT speed/knock/wall/reward semantics.
const baseApplyDamage=TimingDefenseRoom.prototype.applyDamage;
TimingDefenseRoom.prototype.applyDamage=function(monster,damage,slot,tier,at,knock=true,source='hit',proc=false){
  if(!isSplitterFamily(monster))return baseApplyDamage.call(this,monster,damage,slot,tier,at,knock,source,proc);
  const run=this.room?.run;if(!run||!monster)return{actual:0,killed:false};
  ensureSplitterState(monster);this.materialize(monster,at);const d=splitterMeta(monster);
  const player=run.players?.find(p=>p.slot===slot)||null,ai=source==='ai'?run.ai?.find(a=>a.slot===slot)||null:null;
  let raw=Math.max(0,Number(damage)||0);if(source==='ai')raw=Math.round(raw*aiStageMul(run.stage||1));
  const actual=Math.max(1,Math.round(raw*(d.armor??1)));monster.hp-=actual;
  let push=0;
  if(knock){
    const rank=player?.upgrades?.knock||0;let mul=1+rank*.10;if(player?.__v036TankLv6&&source==='hit')mul*=1.30;
    push=tierKnockBase(tier)*d.knockResist*mul;monster.x=Math.min(.985,monster.x+push);
  }
  let killed=false,children=[];
  if(monster.hp<=0){
    killed=true;run.kills=(run.kills||0)+1;const reward=rewardFor(monster);
    if(player){player.kills=(player.kills||0)+1;player.coin=(player.coin||0)+reward;player.killCoinEarned=(player.killCoinEarned||0)+reward}
    if(ai){ai.kills=(ai.kills||0)+1;ai.killCoinEarned=(ai.killCoinEarned||0)+reward}
    run.monsters=run.monsters.filter(m=>m.id!==monster.id);
    if(monster.type==='splitter'&&monster.canSplit!==false)children=this.spawnSplitterChildren(monster,at);
  }
  if(player)player.damage=(player.damage||0)+actual;if(ai)ai.damage=(ai.damage||0)+actual;
  this.event({
    type:source,slot,targetId:monster.id,tier,damage:actual,rawDamage:raw,armor:d.armor??1,monsterType:monster.type,parentId:monster.parentId??null,
    splitterPackageId:monster.splitterPackageId??null,splitterGeneration:monster.splitterGeneration??(monster.type==='splitter'?0:1),canSplit:monster.type==='splitter'&&monster.canSplit!==false,
    splitChildIds:children.map(c=>c.id),splitChildCount:children.length,splitChildY:children.map(c=>c.y),killed,procCrit:!!proc,stage:run.stage
  },at);
  return{actual,killed,rawDamage:raw,armor:d.armor??1,push,splitChildIds:children.map(c=>c.id)};
};

function processSplitterWallHits(room,at){
  const run=room.room?.run;if(!run||run.status!=='combat')return false;
  const due=(run.monsters||[]).filter(isSplitterFamily).map(monster=>({monster,hitAt:room.wallAt(monster)})).filter(x=>x.hitAt<=at+.5).sort((a,b)=>a.hitAt-b.hitAt||a.monster.id-b.monster.id);
  let changed=false;
  for(const {monster,hitAt} of due){
    if(!run.monsters.some(m=>m.id===monster.id))continue;
    ensureSplitterState(monster);room.materialize(monster,hitAt);run.monsters=run.monsters.filter(m=>m.id!==monster.id);
    const d=splitterMeta(monster),defRank=(run.players||[]).reduce((n,p)=>n+(p.upgrades?.def||0),0),defense=Math.max(0,Math.min(.60,defRank*.025));
    const incoming=Math.max(1,Math.round(d.wallDamage*(1-defense)));run.baseHp=Math.max(0,run.baseHp-incoming);
    room.event({type:'wall',targetId:monster.id,monsterType:monster.type,parentId:monster.parentId??null,damage:incoming,baseHp:run.baseHp,stage:run.stage},hitAt);changed=true;
    if(room.checkEnd(hitAt))break;
  }
  return changed;
}

const baseProcessAt=TimingDefenseRoom.prototype.processAt;
TimingDefenseRoom.prototype.processAt=function(at){
  const wallChanged=processSplitterWallHits(this,at),changed=baseProcessAt.call(this,at);
  if(wallChanged&&this.room?.run&&!changed)this.room.run.revision++;
  return wallChanged||changed;
};

const baseNextDueAt=TimingDefenseRoom.prototype.nextDueAt;
TimingDefenseRoom.prototype.nextDueAt=function(){
  let due=baseNextDueAt.call(this),run=this.room?.run;if(!run||run.status!=='combat')return due;
  for(const m of run.monsters||[])if(isSplitterFamily(m)){
    const w=this.wallAt(m);if(Number.isFinite(w))due=due==null?w:Math.min(due,w);
  }
  return due;
};

const baseRunPublic=TimingDefenseRoom.prototype.runPublic;
TimingDefenseRoom.prototype.runPublic=function(at){
  const out=baseRunPublic.call(this,at),run=this.room?.run;if(!out||!run)return out;
  const byId=new Map((run.monsters||[]).map(m=>[m.id,m]));
  out.monsters=(out.monsters||[]).map(sm=>{
    const m=byId.get(sm.id);if(!isSplitterFamily(m))return sm;ensureSplitterState(m);
    const d=splitterMeta(m);
    return{...sm,x:Math.max(WALL_X,this.xAt(m,at)),size:m.size??d.size,parentId:m.parentId??null,splitterPackageId:m.splitterPackageId??null,splitterGeneration:m.splitterGeneration??0,canSplit:!!m.canSplit,reward:rewardFor(m)};
  });
  return out;
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==='GET'&&url.pathname==='/api/health')return json({
      ok:true,service:'timing-defense-v043-splitter-kernel-capability',version:'0.43-cf.1',
      transport:'websocket-hibernation-per-socket-event-cursor',authority:'v042-plus-stage-independent-splitter-child-kernel',
      splitter:{status:'capability-enabled',parent:{hp:SPLITTER.hp,speed:SPLITTER.speed,wallDamage:SPLITTER.wallDamage,knockResist:SPLITTER.knockResist,size:SPLITTER.size},child:{hp:CHILD.hp,speed:CHILD.speed,wallDamage:CHILD.wallDamage,knockResist:CHILD.knockResist,size:CHILD.size},rewardAccounting:PROVISIONAL_REWARD_ACCOUNTING,balance:'provisional'},
      campaign:{legacyStage4_10:'blocked',final50:'not-authored'},scope:'splitter-authoritative-child-spawn-kernel'
    });
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom, SPLITTER, CHILD, PROVISIONAL_REWARD_ACCOUNTING, isSplitterFamily, splitterMeta, processSplitterWallHits };
