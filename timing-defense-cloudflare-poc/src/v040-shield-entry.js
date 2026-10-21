import baseWorker, { TimingDefenseRoom } from "./v039-audit-entry.js";
import { meta, armorDamage } from "./monster-capability-v1.js";

// Timing Defense v0.40 capability slice A — SHIELD/common armor.
// Stage-number-independent: legacy Stage 4 remains blocked.
// The SHIELD coefficients are provisional sandbox anchors, not production balance freeze.

const SHIELD=meta('shield');
const WALL_X=.155;
function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}
function aiStageMul(stage){return 1+Math.max(0,(Number(stage)||1)-1)*.035}
function tierKnockBase(tier){
  const critical=tier==="CRITICAL",perfect=critical||tier==="PERFECT"||tier==="SUPER",good=perfect||tier==="GOOD"||tier==="GREAT";
  return critical?.047:perfect?.024:good?.013:.006;
}

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

const baseApplyDamage=TimingDefenseRoom.prototype.applyDamage;
TimingDefenseRoom.prototype.applyDamage=function(monster,damage,slot,tier,at,knock=true,source="hit",proc=false){
  if(monster?.type!=="shield")return baseApplyDamage.call(this,monster,damage,slot,tier,at,knock,source,proc);
  const run=this.room?.run;
  if(!run||!monster)return{actual:0,killed:false};
  const player=run.players?.find(p=>p.slot===slot)||null;
  const ai=source==="ai"?run.ai?.find(a=>a.slot===slot)||null:null;
  let authoritativeRaw=Math.max(0,Number(damage)||0);
  if(source==="ai")authoritativeRaw=Math.round(authoritativeRaw*aiStageMul(run.stage||1));

  this.materialize(monster,at);
  const actual=armorDamage("shield",authoritativeRaw);
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
    killed=true;run.kills=(run.kills||0)+1;
    if(player){
      player.kills=(player.kills||0)+1;
      player.coin=(player.coin||0)+SHIELD.reward;
      player.killCoinEarned=(player.killCoinEarned||0)+SHIELD.reward;
    }
    if(ai){
      ai.kills=(ai.kills||0)+1;
      ai.killCoinEarned=(ai.killCoinEarned||0)+SHIELD.reward;
    }
    run.monsters=run.monsters.filter(m=>m.id!==monster.id);
  }
  if(player)player.damage=(player.damage||0)+actual;
  if(ai)ai.damage=(ai.damage||0)+actual;

  this.event({
    type:source,slot,targetId:monster.id,tier,damage:actual,rawDamage:authoritativeRaw,
    armor:SHIELD.armor,monsterType:"shield",killed,procCrit:!!proc,stage:run.stage
  },at);
  return{actual,killed,rawDamage:authoritativeRaw,armor:SHIELD.armor};
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health")return json({
      ok:true,service:"timing-defense-v040-shield-capability",version:"0.40-cf.2",
      transport:"websocket-hibernation-per-socket-event-cursor",
      authority:"v039-plus-stage-independent-shield-armor",
      shield:{status:"capability-enabled",armor:SHIELD.armor,knockResist:SHIELD.knockResist,size:1.08,speed:SHIELD.speed,reward:SHIELD.reward,balance:"provisional"},
      campaign:{legacyStage4:"blocked",final50:"not-authored"},
      scope:"shield-common-armor-capability"
    });
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom, SHIELD };