import baseWorker, { TimingDefenseRoom } from "./v036-cf2-entry.js";

// Timing Defense Cloudflare v0.37 Slice B
// Stage 3 only. Stage 4 remains blocked.
// Exact legacy Stage 3 encounter contract, while preserving the existing
// ordinary non-boss +10% HP experiment already validated in Stage 1-2.

const STAGE3={count:12,gap:980};
const WALL_X=.155;
const BRUTE={hp:900,speed:.040,size:1.34,baseDamage:180,knockResist:.38,armor:1.00,reward:14};

function json(data,status=200){
  return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}});
}
function aiStageMul(stage){return 1+Math.max(0,(Number(stage)||1)-1)*.035}
function tierKnockBase(tier){
  const critical=tier==="CRITICAL",perfect=critical||tier==="PERFECT"||tier==="SUPER",good=perfect||tier==="GOOD"||tier==="GREAT";
  return critical?.047:perfect?.024:good?.013:.006;
}
function stage3Hp(type){
  const base=type==="brute"?900:type==="runner"?165:320;
  return Math.round(base*(1+(3-1)*.13)*1.10);
}
function stage3Type(r){return r<.44?"grunt":r<.78?"runner":"brute"}

// BRUTE movement must not fall back to GRUNT speed.
const baseXAt=TimingDefenseRoom.prototype.xAt;
TimingDefenseRoom.prototype.xAt=function(monster,at){
  if(monster?.type!=="brute")return baseXAt.call(this,monster,at);
  return monster.x-BRUTE.speed*Math.max(0,at-monster.refAt)/1000;
};
const baseWallAt=TimingDefenseRoom.prototype.wallAt;
TimingDefenseRoom.prototype.wallAt=function(monster){
  if(monster?.type!=="brute")return baseWallAt.call(this,monster);
  if(monster.x<=WALL_X)return monster.refAt;
  return monster.refAt+((monster.x-WALL_X)/BRUTE.speed)*1000;
};

// BRUTE combat path uses its exact reward / wall / knock contract while
// retaining the already-approved v0.36 N2 + Lv6 semantics.
const baseApplyDamage=TimingDefenseRoom.prototype.applyDamage;
TimingDefenseRoom.prototype.applyDamage=function(monster,damage,slot,tier,at,knock=true,source="hit",proc=false){
  if(monster?.type!=="brute")return baseApplyDamage.call(this,monster,damage,slot,tier,at,knock,source,proc);
  const run=this.room?.run;
  if(!run||!monster)return{actual:0,killed:false};
  const player=run.players?.find(p=>p.slot===slot)||null;
  const ai=source==="ai"?run.ai?.find(a=>a.slot===slot)||null:null;
  let authoritativeDamage=damage;
  if(source==="ai")authoritativeDamage=Math.round(authoritativeDamage*aiStageMul(run.stage||1));

  this.materialize(monster,at);
  const actual=Math.max(1,Math.round(authoritativeDamage*BRUTE.armor));
  monster.hp-=actual;

  if(knock){
    const rank=player?.upgrades?.knock||0;
    let mul=1+rank*.10;
    if(player?.__v036TankLv6&&source==="hit")mul*=1.30;
    const push=tierKnockBase(tier)*BRUTE.knockResist*mul;
    monster.x=Math.min(.985,monster.x+push);
  }

  let killed=false;
  if(monster.hp<=0){
    killed=true;run.kills++;
    if(player){
      player.kills++;player.coin+=BRUTE.reward;
      player.killCoinEarned=(player.killCoinEarned||0)+BRUTE.reward;
    }
    if(ai){
      ai.kills=(ai.kills||0)+1;
      ai.killCoinEarned=(ai.killCoinEarned||0)+BRUTE.reward;
    }
    run.monsters=run.monsters.filter(m=>m.id!==monster.id);
  }
  if(player)player.damage=(player.damage||0)+actual;
  if(ai)ai.damage=(ai.damage||0)+actual;

  this.event({type:source,slot,targetId:monster.id,tier,damage:actual,killed,procCrit:!!proc,stage:run.stage},at);
  return{actual,killed};
};

TimingDefenseRoom.prototype.spawnStage3=function(at){
  const run=this.room?.run;
  if(!run||run.stage!==3||run.spawned>=run.stageTarget)return null;
  const type=stage3Type(this.rng());
  const id=run.nextMonsterId++,hp=stage3Hp(type);
  run.monsters.push({
    id,type,x:1.055+this.rng()*.04,y:.30+this.rng()*.32,refAt:at,hp,maxHp:hp
  });
  run.spawned++;
  this.event({type:"spawn",targetId:id,monsterType:type,stage:3},at);
  return run.monsters[run.monsters.length-1];
};

// Stage 1-2 use the validated implementation unchanged. Only Stage 3 is new.
const baseBeginStage=TimingDefenseRoom.prototype.beginStage;
TimingDefenseRoom.prototype.beginStage=function(stage,at){
  if(stage!==3){
    if(stage>3)throw new Error("stage-not-supported");
    return baseBeginStage.call(this,stage,at);
  }
  const run=this.room?.run;
  if(!run)throw new Error("run-missing");
  run.stage=3;
  run.status="stage-starting";
  run.startAt=at+1500;
  run.combatAt=run.startAt+1050;
  run.stageTarget=STAGE3.count;
  run.spawned=0;
  run.nextSpawnAt=run.combatAt;
  run.monsters=[];
  run.shop=null;
  run.skillQueue=[];
  for(const p of run.players||[])p.nextPassiveAt=run.combatAt+2000;
  for(const a of run.ai||[])a.nextAt=run.combatAt+450+a.slot*220;
  this.room.status="starting";
  this.room.startAt=run.startAt;
  this.event({type:"stage-starting",stage:3,startAt:run.startAt,combatAt:run.combatAt},at);
  run.revision++;
};

// The v0.35 kernel has no Stage 3 plan. Pre-spawn every Stage 3 monster due at
// the requested authoritative time, then let the validated v0.36 kernel process
// wall hits, passive attacks, AI attacks and scheduled Lv6 effects.
const baseProcessAt=TimingDefenseRoom.prototype.processAt;
TimingDefenseRoom.prototype.processAt=function(at){
  const run=this.room?.run;
  let stage3Spawned=false;
  if(run?.stage===3&&at>=run.combatAt&&["stage-starting","intro","combat"].includes(run.status)){
    while(run.spawned<run.stageTarget&&run.nextSpawnAt<=at+.5){
      this.spawnStage3(run.nextSpawnAt);
      run.nextSpawnAt+=STAGE3.gap;
      stage3Spawned=true;
    }
  }
  const changed=baseProcessAt.call(this,at);
  if(stage3Spawned&&this.room?.run&&!changed)this.room.run.revision++;
  return stage3Spawned||changed;
};

const baseNextDueAt=TimingDefenseRoom.prototype.nextDueAt;
TimingDefenseRoom.prototype.nextDueAt=function(){
  const baseDue=baseNextDueAt.call(this),run=this.room?.run;
  if(!run||run.stage!==3||run.status!=="combat"||run.spawned>=run.stageTarget)return baseDue;
  const spawnDue=run.nextSpawnAt;
  if(!Number.isFinite(spawnDue))return baseDue;
  return baseDue==null?spawnDue:Math.min(baseDue,spawnDue);
};

// Slice B invariant: Stage 1, 2 and 3 clear into Team Shop. Stage 4 is blocked.
TimingDefenseRoom.prototype.checkEnd=function(at){
  const run=this.room?.run;
  if(!run)return false;
  if(run.baseHp<=0&&run.status!=="gameover"){
    run.status="gameover";this.room.status="run-ended";this.event({type:"gameover"},at);return true;
  }
  if(run.status==="combat"&&run.spawned>=run.stageTarget&&run.monsters.length===0){
    if(run.stage>=1&&run.stage<=3){this.enterShop(at);return true}
  }
  return false;
};

// Extend the existing host-only Team Shop NEXT contract from Stage 1->2 to
// Stage 2->3. A Stage 3 shop is valid, but Stage 4 remains server-blocked.
const baseRoomFetch=TimingDefenseRoom.prototype.fetch;
TimingDefenseRoom.prototype.fetch=async function(request){
  const url=new URL(request.url);
  if(request.method==="POST"&&url.pathname==="/v035/shop-next"&&this.room?.run?.stage>=2){
    const body=await request.json().catch(()=>({})),now=Date.now();
    const participant=this.room.participants.find(p=>p.session===String(body.session||""));
    if(!participant)return json({ok:false,error:"invalid-session"},401);
    const advanced=this.advanceTo(now);
    if(advanced){await this.persist();this.broadcastState(now)}
    try{
      if(this.room.hostSession!==participant.session)throw new Error("host-only");
      const run=this.room.run;
      if(!run?.shop||run.status!=="shop")throw new Error("shop-not-open");
      if(!run.shop.canNext)throw new Error("not-ready");
      if(run.stage===2){
        this.beginStage(3,now);
        await this.persist();this.broadcastState(now);await this.scheduleNext();
        return json({ok:true,result:{stage:3,startAt:this.room.run.startAt},state:this.publicState(now)});
      }
      throw new Error("stage4-blocked");
    }catch(error){
      await this.scheduleNext();
      return json({ok:false,error:error.message||"v037-shop-next-failed",state:this.publicState(now)},409);
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
        service:"timing-defense-cloudflare-v037-stage3",
        version:"0.37-cf.1",
        transport:"websocket-hibernation",
        authority:"durable-object-stage1-stage3-lv6",
        presentation:"generic-stage-flow-stage3-brute",
        locationHint:"apac-ne",
        scope:"stage1-stage3-brute-team-shop",
        stage3:{count:12,gap:980,composition:{grunt:.44,runner:.34,brute:.22}},
        brute:{hp:900,speed:.040,baseDamage:180,knockResist:.38,armor:1,reward:14},
        stage4:"blocked",
        n3:"deferred-explicit-discussion-required"
      });
    }
    if(request.method==="GET"&&url.pathname==="/"){
      const assetUrl=new URL(request.url);assetUrl.pathname="/v037-cloudflare.html";
      return env.ASSETS.fetch(new Request(assetUrl,request));
    }
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom };