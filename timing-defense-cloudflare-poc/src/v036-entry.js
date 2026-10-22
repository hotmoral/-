import baseWorker, { TimingDefenseRoom } from "./v035-audit-entry.js";

// Timing Defense Cloudflare v0.36 Slice A
// - N1: restore exact legacy heavy-tier EXP values.
// - N2: restore exact legacy AI stage damage scaling (+3.5% per stage after Stage 1).
// - Lv6 human skill combat authority for Stage 1-2 only.
// - N3 combo milestone bonus attacks remain intentionally deferred for explicit discussion.

const XP_EXACT = {
  NORMAL: 8,
  GOOD: 12,
  PERFECT: 18,
  HEAVY: 10,
  "HEAVY+": 14,
  GREAT: 18,
  SUPER: 23,
  CRITICAL: 28
};
const TYPE_META = {
  grunt: { knockResist: .85, size: 1.00 },
  runner:{ knockResist: 1.00, size: .70 },
  brute: { knockResist: .38, size: 1.34 },
  shield:{ knockResist: .62, size: 1.08 },
  flyer: { knockResist: .90, size: .78 }
};
const SLOT_Y = [.30, .41, .52, .63];

function json(data,status=200){
  return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}});
}
function roomStub(env,code){
  const id=env.ROOMS.idFromName(String(code||"").toUpperCase());
  return env.ROOMS.get(id,{locationHint:"apac-ne"});
}
async function parseJson(request){return request.json().catch(()=>({}))}
function need(level){return 60+12*(level-1)}
function exactXp(tier){return XP_EXACT[tier]??8}
function aiStageMul(stage){return 1+Math.max(0,(Number(stage)||1)-1)*.035}
function participantForSlot(room,slot){return room?.participants?.find(p=>p.slot===slot)||null}
function latestEvent(run,predicate,minId=0){
  for(let i=(run?.events?.length||0)-1;i>=0;i--){
    const e=run.events[i];if((e.id||0)>=minId&&predicate(e))return e;
  }
  return null;
}
function grantExtraXp(player,amount){
  let left=Math.max(0,Math.round(amount||0));
  if(!left)return;
  player.xp+=left;
  while(player.xp>=player.xpNeed){
    player.xp-=player.xpNeed;player.level++;player.xpNeed=need(player.level);
  }
}
function tierKnockBase(tier){
  const critical=tier==="CRITICAL",perfect=critical||tier==="PERFECT"||tier==="SUPER",good=perfect||tier==="GOOD"||tier==="GREAT";
  return critical?.047:perfect?.024:good?.013:.006;
}
function pointAt(room,monster,at){
  if(!monster)return null;
  const d=TYPE_META[monster.type]||TYPE_META.grunt;
  const y=typeof room.yAt==='function'?room.yAt(monster,at):monster.y;
  return {id:monster.id,type:monster.type,x:room.xAt(monster,at),y,size:d.size||1};
}
function actorOrigin(slot){return{x:.105,y:SLOT_Y[Math.max(0,Math.min(3,(slot||1)-1))]||.30}}
function archerPierceTargets(room,primary,slot,at,maxCount=2){
  if(!primary)return[];
  const a=actorOrigin(slot),b={x:primary.x,y:primary.y-.035*(primary.size||1)};
  const dx=b.x-a.x,dy=b.y-a.y,len2=dx*dx+dy*dy||1;
  const out=[];
  for(const m of room.room?.run?.monsters||[]){
    if(m.id===primary.id)continue;
    const q=pointAt(room,m,at);if(!q)continue;
    const qy=q.y-.035*(q.size||1),t=((q.x-a.x)*dx+(qy-a.y)*dy)/len2;
    if(t<=1.025)continue;
    const px=a.x+t*dx,py=a.y+t*dy,dist=Math.hypot(q.x-px,qy-py);
    if(dist<=.042*(q.size||1))out.push({m,t,q});
  }
  out.sort((x,y)=>x.t-y.t);
  return out.slice(0,maxCount);
}
function mageSplashTargets(room,primary,at,maxCount=3){
  if(!primary)return[];
  const out=[];
  for(const m of room.room?.run?.monsters||[]){
    if(m.id===primary.id)continue;
    const q=pointAt(room,m,at);if(!q)continue;
    if(Math.abs(q.x-primary.x)<.105&&Math.abs(q.y-primary.y)<.16)out.push({m,q});
  }
  return out.slice(0,maxCount);
}
function annotateLastSkillEvent(run,minId,meta){
  const e=latestEvent(run,x=>x.type==="skill",minId);
  if(e)Object.assign(e,meta);
  return e;
}

const baseMakeRun=TimingDefenseRoom.prototype.makeRun;
TimingDefenseRoom.prototype.makeRun=function(startAt){
  const run=baseMakeRun.call(this,startAt);
  run.skillQueue=[];
  return run;
};

// N2 and Tank Lv6 authoritative knockback layer.
const baseApplyDamage=TimingDefenseRoom.prototype.applyDamage;
TimingDefenseRoom.prototype.applyDamage=function(monster,damage,slot,tier,at,knock=true,source="hit",proc=false){
  const run=this.room?.run;
  const player=run?.players?.find(p=>p.slot===slot)||null;
  let authoritativeDamage=damage;
  if(source==="ai")authoritativeDamage=Math.round(authoritativeDamage*aiStageMul(run?.stage||1));
  const tankLv6=!!(player?.__v036TankLv6&&source==="hit"&&knock&&monster);
  const target=monster;
  const result=baseApplyDamage.call(this,target,authoritativeDamage,slot,tier,at,knock,source,proc);
  if(tankLv6&&target&&!result?.killed&&run?.monsters?.some(m=>m.id===target.id)){
    const d=TYPE_META[target.type]||TYPE_META.grunt;
    const rank=player?.upgrades?.knock||0;
    const extra=tierKnockBase(tier)*d.knockResist*(1+rank*.10)*.30;
    target.x=Math.min(.985,target.x+extra);
  }
  return result;
};

function queueRogueSecond(room,{slot,targetId,damage,actionId,parentTier,at}){
  const run=room.room?.run;if(!run)return;
  run.skillQueue=Array.isArray(run.skillQueue)?run.skillQueue:[];
  run.skillQueue.push({
    kind:"rogue-double-dagger",dueAt:at+55,slot,targetId,damage,actionId,parentTier,hitIndex:1
  });
  run.skillQueue.sort((a,b)=>a.dueAt-b.dueAt||a.slot-b.slot||a.hitIndex-b.hitIndex);
}

TimingDefenseRoom.prototype.processV036SkillQueue=function(at){
  const run=this.room?.run;
  if(!run||run.status!=="combat"||!Array.isArray(run.skillQueue)||!run.skillQueue.length)return false;
  const due=run.skillQueue.filter(x=>x.dueAt<=at+.5);
  if(!due.length)return false;
  run.skillQueue=run.skillQueue.filter(x=>x.dueAt>at+.5);
  let changed=false;
  for(const fx of due){
    if(run.status!=="combat")break;
    if(fx.kind==="rogue-double-dagger"){
      let target=run.monsters.find(m=>m.id===fx.targetId)||this.nearest(fx.dueAt);
      if(!target)continue;
      const q=pointAt(this,target,fx.dueAt),eventFloor=run.nextEventId||1;
      this.applyDamage(target,fx.damage,fx.slot,"SKILL",fx.dueAt,true,"skill",false);
      annotateLastSkillEvent(run,eventFloor,{
        actionId:fx.actionId,hitIndex:fx.hitIndex,skillKind:fx.kind,parentTier:fx.parentTier,
        sourceClass:"rogue",targetX:q?.x??null,targetY:q?.y??null
      });
      changed=true;
      if(this.checkEnd(fx.dueAt))break;
    }
  }
  return changed;
};

const baseProcessAt=TimingDefenseRoom.prototype.processAt;
TimingDefenseRoom.prototype.processAt=function(at){
  const changed=baseProcessAt.call(this,at);
  const skillChanged=this.processV036SkillQueue(at);
  if(skillChanged&&this.room?.run)this.room.run.revision++;
  return changed||skillChanged;
};

const baseNextDueAt=TimingDefenseRoom.prototype.nextDueAt;
TimingDefenseRoom.prototype.nextDueAt=function(){
  const baseDue=baseNextDueAt.call(this),run=this.room?.run;
  if(!run||run.status!=="combat"||!Array.isArray(run.skillQueue)||!run.skillQueue.length)return baseDue;
  const skillDue=run.skillQueue.reduce((n,x)=>Math.min(n,x.dueAt),Infinity);
  if(!Number.isFinite(skillDue))return baseDue;
  return baseDue==null?skillDue:Math.min(baseDue,skillDue);
};

const baseBeginStage=TimingDefenseRoom.prototype.beginStage;
TimingDefenseRoom.prototype.beginStage=function(stage,at){
  const out=baseBeginStage.call(this,stage,at);
  if(this.room?.run)this.room.run.skillQueue=[];
  return out;
};

const basePlayerAction=TimingDefenseRoom.prototype.playerAction;
TimingDefenseRoom.prototype.playerAction=function(participant,body,at){
  const run=this.room?.run;
  if(!run||run.status!=="combat")return basePlayerAction.call(this,participant,body,at);
  const player=run.players.find(p=>p.slot===participant.slot);
  if(!player)return basePlayerAction.call(this,participant,body,at);

  const seq=Number(body.seq),actionId=`${run.id}:${player.slot}:${Number.isFinite(seq)?seq:"x"}`;
  const classId=participant.classId||participantForSlot(this.room,player.slot)?.classId||"knight";
  const levelBefore=player.level||1,lv6=levelBefore>=6;
  const primaryTarget=this.nearest(at),primaryPoint=pointAt(this,primaryTarget,at);
  const eventFloor=run.nextEventId||1;
  const originalAtk=player.upgrades?.atk||0;

  if(lv6&&classId==="knight"){
    player.upgrades={...(player.upgrades||{}),atk:originalAtk+1.5};
  }
  player.__v036TankLv6=lv6&&classId==="tank";

  let result;
  try{result=basePlayerAction.call(this,participant,body,at)}
  finally{
    player.__v036TankLv6=false;
    if(lv6&&classId==="knight")player.upgrades.atk=originalAtk;
  }

  const primaryEvent=latestEvent(run,e=>e.type==="hit"&&e.slot===player.slot,eventFloor);
  const desiredXp=exactXp(result?.tier),oldXp=Number(result?.xpGain)||0,diff=Math.max(0,desiredXp-oldXp);
  if(diff)grantExtraXp(player,diff);
  if(primaryEvent){
    Object.assign(primaryEvent,{
      actionId,hitIndex:0,sourceClass:classId,skillLv6:lv6,xpGain:desiredXp,level:player.level,charge:player.charge,combo:player.combo
    });
    if(lv6&&classId==="knight")primaryEvent.skillKind="knight-enhanced-blade-wave";
    if(lv6&&classId==="tank")primaryEvent.skillKind="tank-impact-wave-plus";
  }
  if(result){
    result.xpGain=desiredXp;
    result.player=this.playerPublic(player);
    result.actionId=actionId;
    result.skillLv6=lv6;
  }

  let immediateSkillChanged=false;
  if(lv6&&primaryEvent&&primaryPoint){
    const primaryRaw=Math.max(1,Math.round(primaryEvent.rawDamage??primaryEvent.damage??0));
    if(classId==="rogue"){
      queueRogueSecond(this,{slot:player.slot,targetId:primaryPoint.id,damage:Math.max(1,Math.round(primaryRaw*.55)),actionId,parentTier:result.tier,at});
    }else if(classId==="archer"){
      const targets=archerPierceTargets(this,primaryPoint,player.slot,at,2);
      let hitIndex=1;
      for(const {m,q} of targets){
        const floor=run.nextEventId||1;
        this.applyDamage(m,Math.max(1,Math.round(primaryRaw*.52)),player.slot,result.tier,at,true,"skill",false);
        annotateLastSkillEvent(run,floor,{
          actionId,hitIndex:hitIndex++,skillKind:"archer-piercing-arrow",parentTier:result.tier,sourceClass:"archer",
          originTargetId:primaryPoint.id,originX:primaryPoint.x,originY:primaryPoint.y,targetX:q.x,targetY:q.y
        });
        immediateSkillChanged=true;
        if(run.status!=="combat")break;
      }
    }else if(classId==="mage"){
      const targets=mageSplashTargets(this,primaryPoint,at,3);
      let hitIndex=1;
      for(const {m,q} of targets){
        const floor=run.nextEventId||1;
        this.applyDamage(m,Math.max(1,Math.round(primaryRaw*.50)),player.slot,"SKILL",at,true,"skill",false);
        annotateLastSkillEvent(run,floor,{
          actionId,hitIndex:hitIndex++,skillKind:"mage-arcane-burst",parentTier:result.tier,sourceClass:"mage",
          originTargetId:primaryPoint.id,originX:primaryPoint.x,originY:primaryPoint.y,targetX:q.x,targetY:q.y
        });
        immediateSkillChanged=true;
        if(run.status!=="combat")break;
      }
    }
  }

  if(immediateSkillChanged&&run.status==="combat")this.checkEnd(at);
  if(immediateSkillChanged)run.revision++;
  return result;
};

// Candidate-only host debug endpoint for bounded Lv5/Lv6 device/API validation.
const baseRoomFetch=TimingDefenseRoom.prototype.fetch;
TimingDefenseRoom.prototype.fetch=async function(request){
  const url=new URL(request.url);
  if(request.method==="POST"&&url.pathname==="/v036/debug-level"){
    if(!this.room)return json({ok:false,error:"room-not-found"},404);
    const body=await parseJson(request),session=String(body.session||"");
    const participant=this.room.participants.find(p=>p.session===session);
    if(!participant)return json({ok:false,error:"invalid-session"},401);
    if(this.room.hostSession!==session)return json({ok:false,error:"host-only"},403);
    const level=Number(body.level),slot=Number(body.slot)||participant.slot;
    if(level!==5&&level!==6)return json({ok:false,error:"level-must-be-5-or-6"},400);
    const player=this.room.run?.players?.find(p=>p.slot===slot);
    if(!player)return json({ok:false,error:"run-player-missing"},409);
    player.level=level;player.xp=0;player.xpNeed=need(level);
    this.event({type:"debug-level",slot,level,stage:this.room.run.stage},Date.now());
    this.room.run.revision++;
    await this.persist();this.broadcastState(Date.now());await this.scheduleNext();
    return json({ok:true,slot,level,state:this.publicState(Date.now())});
  }
  return baseRoomFetch.call(this,request);
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health"){
      return json({
        ok:true,
        service:"timing-defense-cloudflare-v036-slice-a",
        version:"0.36-cf.1",
        transport:"websocket-hibernation",
        authority:"durable-object-stage1-stage2-lv6",
        presentation:"v035-pass-plus-lv6-authoritative-secondary-events",
        locationHint:"apac-ne",
        scope:"stage1-stage2-n1-n2-lv6-authority",
        n1:"legacy-heavy-xp-restored",
        n2:"legacy-ai-stage-damage-scaling-restored",
        n3:"deferred-explicit-discussion-required"
      });
    }
    if(request.method==="GET"&&url.pathname==="/"){
      const assetUrl=new URL(request.url);assetUrl.pathname="/v036-cloudflare.html";
      return env.ASSETS.fetch(new Request(assetUrl,request));
    }
    const m=url.pathname.match(/^\/api\/room\/([A-Z0-9]{6})\/debug-level$/i);
    if(request.method==="POST"&&m){
      const text=await request.text();
      return roomStub(env,m[1].toUpperCase()).fetch(new Request("https://room.internal/v036/debug-level",{
        method:"POST",headers:{"content-type":"application/json"},body:text
      }));
    }
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom };