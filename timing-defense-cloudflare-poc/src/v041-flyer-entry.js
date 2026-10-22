import baseWorker, { TimingDefenseRoom } from "./v040-shield-audit-entry.js";
import { meta, flyerY } from "./monster-capability-v1.js";

// Timing Defense v0.41 capability slice B — FLYER authoritative Y geometry.
// Stage-number-independent. No legacy Stage 5/6 encounter is enabled.
// FLYER coefficients remain provisional capability-test anchors.

const FLYER={...meta('flyer'),size:.78};
const WALL_X=.155;
function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}
function aiStageMul(stage){return 1+Math.max(0,(Number(stage)||1)-1)*.035}
function tierKnockBase(tier){
  const critical=tier==="CRITICAL",perfect=critical||tier==="PERFECT"||tier==="SUPER",good=perfect||tier==="GOOD"||tier==="GREAT";
  return critical?.047:perfect?.024:good?.013:.006;
}
function ensureFlyerPhase(monster,at){
  if(monster?.type!=="flyer")return monster;
  if(!Number.isFinite(Number(monster.flyerBaseY)))monster.flyerBaseY=Number.isFinite(Number(monster.y))?Number(monster.y):.46;
  if(!Number.isFinite(Number(monster.flyerEpochAt)))monster.flyerEpochAt=Number.isFinite(Number(monster.refAt))?Number(monster.refAt):Number(at)||0;
  return monster;
}

TimingDefenseRoom.prototype.yAt=function(monster,at){
  if(!monster)return 0;
  if(monster.type!=="flyer")return Number(monster.y)||0;
  ensureFlyerPhase(monster,at);
  return flyerY(monster.flyerBaseY,Math.max(0,(Number(at)||0)-monster.flyerEpochAt),'flyer');
};
TimingDefenseRoom.prototype.syncFlyerY=function(at){
  for(const m of this.room?.run?.monsters||[])if(m.type==="flyer"){ensureFlyerPhase(m,at);m.y=this.yAt(m,at)}
};

const baseMaterialize=TimingDefenseRoom.prototype.materialize;
TimingDefenseRoom.prototype.materialize=function(monster,at){
  if(monster?.type==="flyer"){ensureFlyerPhase(monster,at);monster.y=this.yAt(monster,at)}
  return baseMaterialize.call(this,monster,at);
};

const baseXAt=TimingDefenseRoom.prototype.xAt;
TimingDefenseRoom.prototype.xAt=function(monster,at){
  if(monster?.type!=="flyer")return baseXAt.call(this,monster,at);
  return monster.x-FLYER.speed*Math.max(0,(Number(at)||0)-monster.refAt)/1000;
};
const baseWallAt=TimingDefenseRoom.prototype.wallAt;
TimingDefenseRoom.prototype.wallAt=function(monster){
  if(monster?.type!=="flyer")return baseWallAt.call(this,monster);
  if(monster.x<=WALL_X)return monster.refAt;
  return monster.refAt+((monster.x-WALL_X)/FLYER.speed)*1000;
};

// FLYER needs its own ordinary combat identity instead of the older GRUNT fallback.
const baseApplyDamage=TimingDefenseRoom.prototype.applyDamage;
TimingDefenseRoom.prototype.applyDamage=function(monster,damage,slot,tier,at,knock=true,source="hit",proc=false){
  if(monster?.type!=="flyer")return baseApplyDamage.call(this,monster,damage,slot,tier,at,knock,source,proc);
  const run=this.room?.run;if(!run||!monster)return{actual:0,killed:false};
  const player=run.players?.find(p=>p.slot===slot)||null;
  const ai=source==="ai"?run.ai?.find(a=>a.slot===slot)||null:null;
  let raw=Math.max(0,Number(damage)||0);
  if(source==="ai")raw=Math.round(raw*aiStageMul(run.stage||1));
  this.materialize(monster,at);
  const actual=Math.max(1,Math.round(raw*(FLYER.armor??1)));
  monster.hp-=actual;
  if(knock){
    const rank=player?.upgrades?.knock||0;let mul=1+rank*.10;
    if(player?.__v036TankLv6&&source==="hit")mul*=1.30;
    const push=tierKnockBase(tier)*FLYER.knockResist*mul;
    monster.x=Math.min(.985,monster.x+push);
  }
  let killed=false;
  if(monster.hp<=0){
    killed=true;run.kills=(run.kills||0)+1;
    if(player){player.kills=(player.kills||0)+1;player.coin=(player.coin||0)+FLYER.reward;player.killCoinEarned=(player.killCoinEarned||0)+FLYER.reward}
    if(ai){ai.kills=(ai.kills||0)+1;ai.killCoinEarned=(ai.killCoinEarned||0)+FLYER.reward}
    run.monsters=run.monsters.filter(m=>m.id!==monster.id);
  }
  if(player)player.damage=(player.damage||0)+actual;if(ai)ai.damage=(ai.damage||0)+actual;
  this.event({type:source,slot,targetId:monster.id,tier,damage:actual,rawDamage:raw,armor:FLYER.armor??1,monsterType:"flyer",targetY:this.yAt(monster,at),killed,procCrit:!!proc,stage:run.stage},at);
  return{actual,killed,rawDamage:raw,armor:FLYER.armor??1};
};

// Geometry closures in the inherited Lv6/N3 layers call room.yAt().
// Syncing before authoritative actions also keeps any older static-y call sites coherent.
const basePlayerAction=TimingDefenseRoom.prototype.playerAction;
TimingDefenseRoom.prototype.playerAction=function(participant,body,at){this.syncFlyerY(at);return basePlayerAction.call(this,participant,body,at)};
const baseProcessAt=TimingDefenseRoom.prototype.processAt;
TimingDefenseRoom.prototype.processAt=function(at){this.syncFlyerY(at);return baseProcessAt.call(this,at)};

const baseRunPublic=TimingDefenseRoom.prototype.runPublic;
TimingDefenseRoom.prototype.runPublic=function(at){
  const out=baseRunPublic.call(this,at),run=this.room?.run;if(!out||!run)return out;
  const byId=new Map((run.monsters||[]).map(m=>[m.id,m]));
  out.monsters=(out.monsters||[]).map(sm=>{
    const m=byId.get(sm.id);if(!m||m.type!=="flyer")return sm;
    ensureFlyerPhase(m,at);
    return{...sm,y:this.yAt(m,at),baseY:m.flyerBaseY,yEpochAt:m.flyerEpochAt,yAmp:FLYER.oscAmp,yOmega:FLYER.oscOmega,size:FLYER.size};
  });
  return out;
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health")return json({
      ok:true,service:"timing-defense-v041-flyer-y-capability",version:"0.41-cf.1",
      transport:"websocket-hibernation-per-socket-event-cursor",
      authority:"v040-plus-stage-independent-flyer-y",
      flyer:{status:"capability-enabled",speed:FLYER.speed,size:FLYER.size,knockResist:FLYER.knockResist,oscAmp:FLYER.oscAmp,oscOmega:FLYER.oscOmega,balance:"provisional",groundImmunity:false},
      campaign:{legacyStage5_6:"blocked",final50:"not-authored"},scope:"flyer-authoritative-y-geometry"
    });
    if(request.method==="GET"&&url.pathname==="/"){
      const assetUrl=new URL(request.url);assetUrl.pathname="/v041-cloudflare.html";return env.ASSETS.fetch(new Request(assetUrl,request));
    }
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom, FLYER, ensureFlyerPhase };
