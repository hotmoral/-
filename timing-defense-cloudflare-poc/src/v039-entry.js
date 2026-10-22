import baseWorker, { TimingDefenseRoom } from "./v038-audit-entry.js";

// Timing Defense Cloudflare v0.39 — N3 Option B authority slice.
// Frozen contract:
// - triggers 5/10/20/30/every +10 thereafter,
// - raw-equivalent max budgets 60/90/150/210,
// - deterministic remainder-safe allocation,
// - no EXP/charge/combo/crit/recursive skill/N3 proc,
// - normal armor/kill/coin/contribution semantics,
// - NORMAL-equivalent generic knockback,
// - Rogue boss scalar .70 retained.

const JUDGES=new Set(["NORMAL","GOOD","PERFECT"]);
const SLOT_Y=[.30,.41,.52,.63];
const TYPE_META={
  grunt:{knockResist:.85,size:1.00},
  runner:{knockResist:1.00,size:.70},
  brute:{knockResist:.38,size:1.34},
  shield:{knockResist:.62,size:1.08},
  flyer:{knockResist:.90,size:.78},
  charger:{knockResist:.80,size:1.00}
};

function json(data,status=200){return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}})}
function roomStub(env,code){const id=env.ROOMS.idFromName(String(code||"").toUpperCase());return env.ROOMS.get(id,{locationHint:"apac-ne"})}
function need(level){return 60+12*(level-1)}
function cleanJudge(v){return JUDGES.has(v)?v:"NORMAL"}
function milestoneFor(c){
  if(c===5||c===10||c===20||c===30)return c;
  if(c>30&&c%10===0)return c;
  return 0;
}
function budgetFor(m){return m>=30?210:m>=20?150:m>=10?90:60}
function rogueCount(m){return m>=30?5:m>=20?4:m>=10?3:2}
function milestonesCrossed(comboBefore,heavy,x,y){
  let c=Math.max(0,Number(comboBefore)||0);const out=[];
  const judges=heavy?[cleanJudge(x),cleanJudge(y)]:[cleanJudge(x)];
  for(const j of judges){
    if(j==="PERFECT"){
      c++;const m=milestoneFor(c);if(m)out.push(m);
    }else c=0;
  }
  return out;
}
function allocateBudget(budget,weights){
  const exact=weights.map(w=>budget*w),out=exact.map(Math.floor);
  let rem=budget-out.reduce((a,b)=>a+b,0);
  const order=exact.map((v,i)=>({i,f:v-Math.floor(v)})).sort((a,b)=>b.f-a.f||a.i-b.i);
  for(let k=0;k<rem;k++)out[order[k%order.length].i]++;
  return out;
}
function latestEvent(run,pred,minId=0){
  for(let i=(run?.events?.length||0)-1;i>=0;i--){const e=run.events[i];if((e.id||0)>=minId&&pred(e))return e}
  return null;
}
function pointAt(room,monster,at){
  if(!monster)return null;const d=TYPE_META[monster.type]||TYPE_META.grunt;
  const y=typeof room.yAt==='function'?room.yAt(monster,at):monster.y;
  return{id:monster.id,type:monster.type,x:room.xAt(monster,at),y,size:d.size||1,boss:!!monster.boss};
}
function actorOrigin(slot){return{x:.105,y:SLOT_Y[Math.max(0,Math.min(3,(slot||1)-1))]||.30}}
function knightSecondary(room,primary,at){
  const list=[];
  for(const m of room.room?.run?.monsters||[]){
    if(m.id===primary.id)continue;const q=pointAt(room,m,at);if(!q)continue;
    if(q.x>=primary.x&&q.x-primary.x<=.20&&Math.abs(q.y-primary.y)<=.13)list.push(q);
  }
  list.sort((a,b)=>a.x-b.x||Math.abs(a.y-primary.y)-Math.abs(b.y-primary.y)||a.id-b.id);
  return list[0]||null;
}
function tankSecondaries(room,primary,at){
  const list=[];
  for(const m of room.room?.run?.monsters||[]){
    if(m.id===primary.id)continue;const q=pointAt(room,m,at);if(!q)continue;
    if(Math.abs(q.x-primary.x)<=.13&&Math.abs(q.y-primary.y)<=.16){
      list.push({...q,dist:Math.hypot(q.x-primary.x,q.y-primary.y)});
    }
  }
  list.sort((a,b)=>a.dist-b.dist||a.id-b.id);return list.slice(0,2);
}
function archerSecondary(room,primary,slot,at){
  const a=actorOrigin(slot),b={x:primary.x,y:primary.y-.035*(primary.size||1)};
  const dx=b.x-a.x,dy=b.y-a.y,len2=dx*dx+dy*dy||1,out=[];
  for(const m of room.room?.run?.monsters||[]){
    if(m.id===primary.id)continue;const q=pointAt(room,m,at);if(!q)continue;
    const qy=q.y-.035*(q.size||1),t=((q.x-a.x)*dx+(qy-a.y)*dy)/len2;
    if(t<=1.025)continue;
    const px=a.x+t*dx,py=a.y+t*dy,dist=Math.hypot(q.x-px,qy-py);
    if(dist<=.042*(q.size||1))out.push({...q,t});
  }
  out.sort((x,y)=>x.t-y.t||x.id-y.id);return out[0]||null;
}
function mageSecondaries(room,primary,at){
  const list=[];
  for(const m of room.room?.run?.monsters||[]){
    if(m.id===primary.id)continue;const q=pointAt(room,m,at);if(!q)continue;
    if(Math.abs(q.x-primary.x)<.12&&Math.abs(q.y-primary.y)<.17){
      list.push({...q,dist:Math.hypot(q.x-primary.x,q.y-primary.y)});
    }
  }
  list.sort((a,b)=>a.dist-b.dist||a.id-b.id);return list.slice(0,3);
}
function n3Weights(cls,milestone){
  if(cls==="rogue")return Array.from({length:rogueCount(milestone)},()=>1/rogueCount(milestone));
  if(cls==="knight")return[.67,.33];
  if(cls==="tank")return[.60,.20,.20];
  if(cls==="archer")return[.70,.30];
  return[.55,.15,.15,.15];
}
function n3Kind(cls){return cls==="rogue"?"rogue-daggers":cls==="knight"?"knight-split-wave":cls==="tank"?"tank-shock-burst":cls==="archer"?"archer-line-burst":"mage-arcane-burst"}
function extraTankLv6Knock(room,target,player){
  if(!target||!player||player.level<6||!room.room?.run?.monsters?.some(m=>m.id===target.id))return;
  const d=TYPE_META[target.type]||TYPE_META.grunt,rank=player.upgrades?.knock||0;
  let extra=.006*d.knockResist*(1+rank*.10)*.30;
  if(target.boss)extra*=.40;
  target.x=Math.min(.985,target.x+extra);
}
function annotateN3(run,floor,meta){
  const e=latestEvent(run,x=>x.type==="n3",floor);if(e)Object.assign(e,meta);return e;
}
function applyN3Hit(room,{player,cls,target,raw,milestone,budget,actionId,hitIndex,hitCount,at,primaryPoint=null}){
  const run=room.room?.run;if(!run||!target)return null;
  const q=pointAt(room,target,at),floor=run.nextEventId||1;
  const bossScalar=(cls==="rogue"&&target.boss)?.70:1;
  const appliedRaw=Math.max(1,Math.round(raw*bossScalar));
  const result=room.applyDamage(target,appliedRaw,player.slot,"NORMAL",at,true,"n3",false);
  if(cls==="tank")extraTankLv6Knock(room,target,player);
  annotateN3(run,floor,{
    actionId,hitIndex,hitCount,n3:true,n3Milestone:milestone,n3Budget:budget,n3Raw:raw,n3AppliedRaw:appliedRaw,
    n3Kind:n3Kind(cls),sourceClass:cls,parentTier:"N3",procCrit:false,
    originTargetId:primaryPoint?.id??null,originX:primaryPoint?.x??null,originY:primaryPoint?.y??null,
    targetX:q?.x??null,targetY:q?.y??null
  });
  return result;
}

const baseMakeRun=TimingDefenseRoom.prototype.makeRun;
TimingDefenseRoom.prototype.makeRun=function(startAt){const run=baseMakeRun.call(this,startAt);run.n3Queue=[];return run};

const baseBeginStage=TimingDefenseRoom.prototype.beginStage;
TimingDefenseRoom.prototype.beginStage=function(stage,at){const out=baseBeginStage.call(this,stage,at);if(this.room?.run)this.room.run.n3Queue=[];return out};

TimingDefenseRoom.prototype.queueN3Rogue=function({player,targetId,parts,milestone,budget,actionId,at}){
  const run=this.room?.run;if(!run)return;
  run.n3Queue=Array.isArray(run.n3Queue)?run.n3Queue:[];
  for(let i=0;i<parts.length;i++)run.n3Queue.push({kind:"n3-rogue",dueAt:at+i*55,slot:player.slot,targetId,raw:parts[i],milestone,budget,actionId,hitIndex:i,hitCount:parts.length});
  run.n3Queue.sort((a,b)=>a.dueAt-b.dueAt||a.slot-b.slot||a.hitIndex-b.hitIndex);
};

TimingDefenseRoom.prototype.processN3Queue=function(at){
  const run=this.room?.run;
  if(!run||run.status!=="combat"||!Array.isArray(run.n3Queue)||!run.n3Queue.length)return false;
  const due=run.n3Queue.filter(x=>x.dueAt<=at+.5);if(!due.length)return false;
  run.n3Queue=run.n3Queue.filter(x=>x.dueAt>at+.5);
  let changed=false;
  for(const fx of due){
    if(run.status!=="combat")break;
    const player=run.players?.find(p=>p.slot===fx.slot);if(!player)continue;
    let target=run.monsters.find(m=>m.id===fx.targetId)||this.nearest(fx.dueAt);if(!target)continue;
    applyN3Hit(this,{player,cls:"rogue",target,raw:fx.raw,milestone:fx.milestone,budget:fx.budget,actionId:fx.actionId,hitIndex:fx.hitIndex,hitCount:fx.hitCount,at:fx.dueAt,primaryPoint:pointAt(this,target,fx.dueAt)});
    changed=true;if(this.checkEnd(fx.dueAt))break;
  }
  return changed;
};

TimingDefenseRoom.prototype.triggerN3=function(player,cls,milestone,baseActionId,at){
  const run=this.room?.run;if(!run||run.status!=="combat")return false;
  const target=this.nearest(at);if(!target)return false;
  const primary=pointAt(this,target,at);if(!primary)return false;
  const budget=budgetFor(milestone),parts=allocateBudget(budget,n3Weights(cls,milestone));
  const actionId=`${baseActionId||`${run.id}:${player.slot}`}:n3:${milestone}`;

  if(cls==="rogue"){
    this.queueN3Rogue({player,targetId:target.id,parts,milestone,budget,actionId,at});
    return this.processN3Queue(at);
  }

  let changed=false;
  applyN3Hit(this,{player,cls,target,raw:parts[0],milestone,budget,actionId,hitIndex:0,hitCount:parts.length,at,primaryPoint:primary});changed=true;
  if(run.status!=="combat")return changed;

  if(cls==="knight"){
    const q=knightSecondary(this,primary,at);const m=q&&run.monsters.find(x=>x.id===q.id);
    if(m)applyN3Hit(this,{player,cls,target:m,raw:parts[1],milestone,budget,actionId,hitIndex:1,hitCount:parts.length,at,primaryPoint:primary});
  }else if(cls==="tank"){
    const qs=tankSecondaries(this,primary,at);
    for(let i=0;i<2;i++){const q=qs[i],m=q&&run.monsters.find(x=>x.id===q.id);if(m)applyN3Hit(this,{player,cls,target:m,raw:parts[i+1],milestone,budget,actionId,hitIndex:i+1,hitCount:parts.length,at,primaryPoint:primary})}
  }else if(cls==="archer"){
    const q=archerSecondary(this,primary,player.slot,at),m=q&&run.monsters.find(x=>x.id===q.id);
    if(m)applyN3Hit(this,{player,cls,target:m,raw:parts[1],milestone,budget,actionId,hitIndex:1,hitCount:parts.length,at,primaryPoint:primary});
  }else{
    const qs=mageSecondaries(this,primary,at);
    for(let i=0;i<3;i++){const q=qs[i],m=q&&run.monsters.find(x=>x.id===q.id);if(m)applyN3Hit(this,{player,cls:"mage",target:m,raw:parts[i+1],milestone,budget,actionId,hitIndex:i+1,hitCount:parts.length,at,primaryPoint:primary})}
  }
  if(run.status==="combat")this.checkEnd(at);
  return changed;
};

const basePlayerAction=TimingDefenseRoom.prototype.playerAction;
TimingDefenseRoom.prototype.playerAction=function(participant,body,at){
  const run=this.room?.run,player=run?.players?.find(p=>p.slot===participant.slot)||null;
  if(!run||run.status!=="combat"||!player)return basePlayerAction.call(this,participant,body,at);
  const comboBefore=player.combo||0,heavyBefore=(player.charge||0)>=3,x=cleanJudge(body.xJudge),y=cleanJudge(body.yJudge);
  const result=basePlayerAction.call(this,participant,body,at);
  if(run.status!=="combat")return result;
  const cls=participant.classId||"knight",milestones=milestonesCrossed(comboBefore,heavyBefore,x,y);
  let changed=false;
  for(const m of milestones){if(this.triggerN3(player,cls,m,result?.actionId||`${run.id}:${player.slot}:${body.seq}`,at))changed=true}
  if(changed)run.revision++;
  return result;
};

const baseProcessAt=TimingDefenseRoom.prototype.processAt;
TimingDefenseRoom.prototype.processAt=function(at){
  const changed=baseProcessAt.call(this,at),n3Changed=this.processN3Queue(at);
  if(n3Changed&&this.room?.run)this.room.run.revision++;
  return changed||n3Changed;
};

const baseNextDueAt=TimingDefenseRoom.prototype.nextDueAt;
TimingDefenseRoom.prototype.nextDueAt=function(){
  const base=baseNextDueAt.call(this),q=this.room?.run?.n3Queue;
  if(!Array.isArray(q)||!q.length)return base;
  const due=q.reduce((n,x)=>Math.min(n,x.dueAt),Infinity);if(!Number.isFinite(due))return base;
  return base==null?due:Math.min(base,due);
};

// Candidate-only host endpoint used by automated four-human N3 stress.
const baseRoomFetch=TimingDefenseRoom.prototype.fetch;
TimingDefenseRoom.prototype.fetch=async function(request){
  const url=new URL(request.url);
  if(request.method==="POST"&&url.pathname==="/v039/debug-n3-arm"){
    const body=await request.json().catch(()=>({})),session=String(body.session||"");
    const p=this.room?.participants?.find(x=>x.session===session);
    if(!p)return json({ok:false,error:"invalid-session"},401);
    if(this.room.hostSession!==session)return json({ok:false,error:"host-only"},403);
    const run=this.room?.run;if(!run||run.status!=="combat")return json({ok:false,error:"run-not-combat"},409);
    const combo=[4,9,19,29,39].includes(Number(body.combo))?Number(body.combo):29;
    const level=Number(body.level)===5?5:6;
    for(const rp of run.players||[]){rp.combo=combo;rp.comboPeak=Math.max(rp.comboPeak||0,combo);rp.level=level;rp.xp=0;rp.xpNeed=need(level);rp.charge=0}
    const now=Date.now();
    for(const m of run.monsters||[]){this.materialize(m,now);m.hp=100000;m.maxHp=100000;m.x=Math.max(.72,m.x);m.refAt=now}
    this.event({type:"debug-n3-arm",combo,level,stage:run.stage},now);run.revision++;
    await this.persist();this.broadcastState(now);await this.scheduleNext();
    return json({ok:true,combo,level,state:this.publicState(now)});
  }
  return baseRoomFetch.call(this,request);
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health")return json({
      ok:true,service:"timing-defense-cloudflare-v039-n3-authority",version:"0.39-cf.1",
      transport:"websocket-hibernation-per-socket-event-cursor",authority:"durable-object-stage1-stage3-lv6-n3",
      n3:{status:"option-b-enabled",milestones:[5,10,20,30,"every+10"],budgets:[60,90,150,210],knockback:"normal-equivalent",recursive:false},
      stage4:"blocked",scope:"n3-authority-validation"
    });
    const m=url.pathname.match(/^\/api\/room\/([A-Za-z0-9]+)\/debug-n3-arm$/);
    if(request.method==="POST"&&m){
      const stub=roomStub(env,m[1]);return stub.fetch(new Request("https://room.internal/v039/debug-n3-arm",request));
    }
    if(request.method==="GET"&&url.pathname==="/"){
      const assetUrl=new URL(request.url);assetUrl.pathname="/v039-cloudflare.html";return env.ASSETS.fetch(new Request(assetUrl,request));
    }
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom, allocateBudget, milestonesCrossed, budgetFor };