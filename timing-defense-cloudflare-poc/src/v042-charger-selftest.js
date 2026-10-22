// Timing Defense v0.42 — deterministic CHARGER authoritative-state tests.

function player(slot=1,level=5){return{slot,level,xp:0,xpNeed:60+12*(level-1),charge:0,combo:0,comboPeak:0,kills:0,coin:0,damage:0,lastSeq:0,nextPassiveAt:999999999,upgrades:{atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0},killCoinEarned:0}}
function charger(id=1,x=.68,y=.38,refAt=1000,hp=100000,extra={}){return{id,type:'charger',x,y,refAt,hp,maxHp:hp,boss:false,...extra}}
function grunt(id=1,x=.68,y=.38,refAt=1000,hp=100000){return{id,type:'grunt',x,y,refAt,hp,maxHp:hp,boss:false}}
function actor(RoomClass,{cls='knight',level=5,monsters=null,stage=1,defRank=0}={}){const a=Object.create(RoomClass.prototype),p=player(1,level);p.upgrades.def=defRank;a.room={version:'v042-charger-selftest',code:'CHG001',method:'friend',status:'running',createdAt:0,revision:0,startAt:null,hostSession:'s1',aiFill:[],participants:[{session:'s1',slot:1,nickname:'A',classId:cls,ready:true,connected:true,activeConnectionId:'c1',joinedAt:0,host:true}],run:{id:`charger-${cls}-${level}`,seed:1,rngState:123456789,status:'combat',startAt:0,combatAt:0,stage,stageTarget:999,spawned:0,nextSpawnAt:999999999,baseHp:2000,baseHpMax:2000,kills:0,nextMonsterId:100,monsters:monsters||[charger()],players:[p],ai:[],events:[],nextEventId:1,revision:0,shop:null,skillQueue:[],n3Queue:[]}};a.rng=()=>.99;return a}
function pack(name,pass,actual,expected){return{name,pass:!!pass,actual,expected}}

export function runV042ChargerSelfTest(RoomClass){
  const checks=[],eps=1e-9,start=1000,trigger=2000,chargeAt=2650;

  try{const a=actor(RoomClass),due=a.nextDueAt();checks.push(pack('CHARGER_NEXT_DUE_IS_TRIGGER',Math.abs(due-trigger)<eps,due,trigger))}catch(e){checks.push(pack('CHARGER_NEXT_DUE_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass),m=a.room.run.monsters[0];a.advanceChargersTo(trigger);checks.push(pack('CHARGER_ADVANCE_TO_WINDUP',m.chargerPhase==='windup'&&Math.abs(m.x-.62)<eps&&Math.abs(m.chargerPhaseAt-trigger)<eps,{phase:m.chargerPhase,x:m.x,phaseAt:m.chargerPhaseAt},{phase:'windup',x:.62,phaseAt:trigger}))}catch(e){checks.push(pack('CHARGER_TRIGGER_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass),m=a.room.run.monsters[0];a.advanceChargersTo(trigger);const x=a.xAt(m,2500);checks.push(pack('CHARGER_WINDUP_STOPS_X',Math.abs(x-.62)<eps,x,.62))}catch(e){checks.push(pack('CHARGER_WINDUP_X_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass),m=a.room.run.monsters[0];a.advanceChargersTo(chargeAt);checks.push(pack('CHARGER_WINDUP_TO_CHARGE',m.chargerPhase==='charge'&&Math.abs(m.chargerPhaseAt-chargeAt)<eps&&Math.abs(m.x-.62)<eps,{phase:m.chargerPhase,phaseAt:m.chargerPhaseAt,x:m.x},{phase:'charge',phaseAt:chargeAt,x:.62}))}catch(e){checks.push(pack('CHARGER_CHARGE_TRANSITION_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass),m=a.room.run.monsters[0];a.advanceChargersTo(chargeAt);const x=a.xAt(m,2750),expected=.62-.210*.1;checks.push(pack('CHARGER_CHARGE_SPEED',Math.abs(x-expected)<eps,x,expected))}catch(e){checks.push(pack('CHARGER_CHARGE_SPEED_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass),m=a.room.run.monsters[0],predicted=a.wallAt(m);a.advanceChargersTo(chargeAt);const after=a.wallAt(m),expected=chargeAt+(.62-.155)/.210*1000;checks.push(pack('CHARGER_WALL_PREDICTION_CONTINUOUS',Math.abs(predicted-expected)<eps&&Math.abs(after-expected)<eps,{predicted,after},expected))}catch(e){checks.push(pack('CHARGER_WALL_PREDICTION_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass),m=a.room.run.monsters[0];a.advanceChargersTo(trigger);const r=a.applyDamage(m,100,1,'NORMAL',2300,true,'hit',false),expectedX=.62+.006*.80;checks.push(pack('CHARGER_WINDUP_KNOCK_INTERRUPTS',r.interrupted&&m.chargerPhase==='advance'&&m.chargerRearmUntil===3200&&Math.abs(m.x-expectedX)<eps,{r,phase:m.chargerPhase,rearm:m.chargerRearmUntil,x:m.x},{interrupted:true,phase:'advance',rearm:3200,x:expectedX}))}catch(e){checks.push(pack('CHARGER_INTERRUPT_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass),m=a.room.run.monsters[0];a.advanceChargersTo(trigger);a.applyDamage(m,100,1,'NORMAL',2300,true,'hit',false);a.advanceChargersTo(3199);const before=m.chargerPhase;a.advanceChargersTo(3200);checks.push(pack('CHARGER_REARM_BLOCK_THEN_RETRIGGER',before==='advance'&&m.chargerPhase==='windup'&&Math.abs(m.chargerPhaseAt-3200)<eps,{before,after:m.chargerPhase,phaseAt:m.chargerPhaseAt},{before:'advance',after:'windup',phaseAt:3200}))}catch(e){checks.push(pack('CHARGER_REARM_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass),m=a.room.run.monsters[0];a.advanceChargersTo(trigger);const r=a.applyDamage(m,100,1,'NORMAL',2300,false,'hit',false);checks.push(pack('CHARGER_NO_KNOCK_NO_INTERRUPT',!r.interrupted&&m.chargerPhase==='windup',{interrupted:r.interrupted,phase:m.chargerPhase},{interrupted:false,phase:'windup'}))}catch(e){checks.push(pack('CHARGER_NO_KNOCK_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass,{cls:'tank',level:6}),m=a.room.run.monsters[0],p=a.room.run.players[0],x=m.x;p.__v036TankLv6=true;const r=a.applyDamage(m,100,1,'NORMAL',start,true,'hit',false),dx=m.x-x,expected=.006*.80*1.30;checks.push(pack('CHARGER_TANK_LV6_KNOCK_IDENTITY',Math.abs(dx-expected)<eps&&Math.abs(r.push-expected)<eps,{dx,push:r.push},{expected,knockResist:.80,lv6Mul:1.30}))}catch(e){checks.push(pack('CHARGER_TANK_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass,{monsters:[charger(1,.68,.38,start,100)]}),p=a.room.run.players[0],r=a.applyDamage(a.room.run.monsters[0],100,1,'NORMAL',start,true,'hit',false),e=a.room.run.events.at(-1);checks.push(pack('CHARGER_COMBAT_IDENTITY_REWARD',r.killed&&r.actual===100&&p.kills===1&&p.coin===8&&p.killCoinEarned===8&&p.damage===100&&e.monsterType==='charger',{r,p,e},{killed:true,reward:8,damage:100}))}catch(e){checks.push(pack('CHARGER_REWARD_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass,{stage:3}),m=a.room.run.monsters[0];a.room.run.ai=[{slot:2,kills:0,damage:0,killCoinEarned:0,nextAt:999999999}];const r=a.applyDamage(m,100,2,'NORMAL',start,false,'ai',false),e=a.room.run.events.at(-1);checks.push(pack('CHARGER_AI_STAGE_MULTIPLIER',r.rawDamage===107&&r.actual===107&&e.rawDamage===107,{r,e},{rawDamage:107,actual:107}))}catch(e){checks.push(pack('CHARGER_AI_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass),m=a.room.run.monsters[0];a.advanceChargersTo(chargeAt);const snap=a.runPublic(2750),sm=snap.monsters[0];checks.push(pack('CHARGER_PUBLIC_PHASE_METADATA',sm.chargerPhase==='charge'&&Math.abs(sm.chargerPhaseAt-chargeAt)<eps&&sm.chargerWindupMs===650&&sm.chargerBaseSpeed===.060&&sm.chargerChargeSpeed===.210&&sm.chargerTriggerX===.62&&sm.size===1,{sm},{phase:'charge',phaseAt:chargeAt,windupMs:650,baseSpeed:.060,chargeSpeed:.210,triggerX:.62,size:1}))}catch(e){checks.push(pack('CHARGER_PUBLIC_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass),m=a.room.run.monsters[0];a.advanceChargersTo(trigger);a.applyDamage(m,10,1,'NORMAL',2300,true,'hit',false);const persisted=JSON.parse(JSON.stringify(m)),b=actor(RoomClass,{monsters:[persisted]}),future=3000,xa=a.xAt(m,future),xb=b.xAt(persisted,future),wa=a.wallAt(m),wb=b.wallAt(persisted);checks.push(pack('CHARGER_RECONNECT_RECONSTRUCTION',Math.abs(xa-xb)<eps&&Math.abs(wa-wb)<eps&&persisted.chargerPhase==='advance'&&persisted.chargerRearmUntil===3200,{xa,xb,wa,wb,phase:persisted.chargerPhase,rearm:persisted.chargerRearmUntil},{sameX:true,sameWall:true,phase:'advance',rearm:3200}))}catch(e){checks.push(pack('CHARGER_RECONNECT_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass),m=a.room.run.monsters[0];
    a.room.run.skillQueue=[{kind:'rogue-double-dagger',dueAt:2050,slot:1,targetId:m.id,damage:10,actionId:'late-alarm',parentTier:'NORMAL',hitIndex:1}];
    a.advanceTo(3000);
    const states=a.room.run.events.filter(e=>e.type==='monster-state').map(e=>({at:e.at,phase:e.phase,reason:e.reason}));
    const skill=a.room.run.events.find(e=>e.type==='skill'&&e.actionId==='late-alarm');
    const triggerEvent=states.find(e=>e.reason==='trigger'),interruptEvent=states.find(e=>e.reason==='windup-interrupt'),retriggerEvent=states.filter(e=>e.reason==='trigger').at(-1);
    const pass=!!skill&&Math.abs(skill.at-2050)<eps&&!!triggerEvent&&Math.abs(triggerEvent.at-trigger)<eps&&!!interruptEvent&&Math.abs(interruptEvent.at-2050)<eps&&m.chargerPhase==='windup'&&Math.abs(m.chargerPhaseAt-2950)<eps&&Math.abs(retriggerEvent.at-2950)<eps;
    checks.push(pack('CHARGER_ADVANCE_TO_REPLAYS_DUE_EVENTS_CHRONOLOGICALLY',pass,{states,skillAt:skill?.at,phase:m.chargerPhase,phaseAt:m.chargerPhaseAt},{triggerAt:2000,skillInterruptAt:2050,retriggerAt:2950,phase:'windup'}));
  }catch(e){checks.push(pack('CHARGER_CHRONOLOGY_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass,{monsters:[charger(1,.20,.38,start,100000)],defRank:4}),m=a.room.run.monsters[0];m.chargerPhase='charge';m.chargerPhaseAt=start;m.refAt=start;const hitAt=a.wallAt(m);a.processAt(hitAt);const e=a.room.run.events.find(x=>x.type==='wall'&&x.monsterType==='charger');checks.push(pack('CHARGER_WALL_DAMAGE_DEFENSE',e?.damage===99&&a.room.run.baseHp===1901,{event:e,baseHp:a.room.run.baseHp},{damage:99,baseHp:1901}))}catch(e){checks.push(pack('CHARGER_WALL_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass,{monsters:[grunt()]}),m=a.room.run.monsters[0],x=a.xAt(m,2000);checks.push(pack('NON_CHARGER_MOVEMENT_DELEGATES',Math.abs(x-.61)<eps,x,.61))}catch(e){checks.push(pack('NON_CHARGER_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  const passed=checks.filter(x=>x.pass).length;return{ok:passed===checks.length,version:'0.42-cf.1-charger-selftest',passed,total:checks.length,failed:checks.filter(x=>!x.pass).map(x=>x.name),checks};
}
