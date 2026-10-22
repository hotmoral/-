// Timing Defense v0.44 — deterministic SUPPORTER event-driven aura tests.

function player(slot=1,level=5){return{slot,level,xp:0,xpNeed:60+12*(level-1),charge:0,combo:0,comboPeak:0,kills:0,coin:0,damage:0,lastSeq:0,nextPassiveAt:999999999,upgrades:{atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0},killCoinEarned:0}}
function supporter(id=1,x=.50,y=.40,refAt=1000,hp=100000,extra={}){return{id,type:'supporter',x,y,refAt,hp,maxHp:hp,boss:false,size:1,supportAuraSources:[],...extra}}
function grunt(id=2,x=.70,y=.40,refAt=1000,hp=100000,extra={}){return{id,type:'grunt',x,y,refAt,hp,maxHp:hp,boss:false,supportAuraSources:[],...extra}}
function runner(id=2,x=.75,y=.40,refAt=1000,hp=100000,extra={}){return{id,type:'runner',x,y,refAt,hp,maxHp:hp,boss:false,supportAuraSources:[],...extra}}
function flyer(id=2,x=.67,y=.46,refAt=1000,hp=100000,extra={}){return{id,type:'flyer',x,y,refAt,hp,maxHp:hp,boss:false,flyerBaseY:y,flyerEpochAt:refAt,supportAuraSources:[],...extra}}
function charger(id=2,x=.80,y=.40,refAt=1000,hp=100000,extra={}){return{id,type:'charger',x,y,refAt,hp,maxHp:hp,boss:false,chargerPhase:'advance',chargerPhaseAt:refAt,chargerRearmUntil:0,chargerTriggerX:.62,supportAuraSources:[],...extra}}
function splitter(id=2,x=.60,y=.40,refAt=1000,hp=100,extra={}){return{id,type:'splitter',x,y,refAt,hp,maxHp:hp,boss:false,canSplit:true,size:1,splitterGeneration:0,supportAuraSources:[],...extra}}
function participant(cls='knight'){return{session:'s1',slot:1,nickname:'A',classId:cls,ready:true,connected:true,activeConnectionId:'c1',joinedAt:0,host:true}}
function actor(RoomClass,{cls='knight',level=5,monsters=null,stage=1,defRank=0,nextMonsterId=100,supportAuraAt=null}={}){const a=Object.create(RoomClass.prototype),p=player(1,level);p.upgrades.def=defRank;a.room={version:'v044-supporter-selftest',code:'SUP001',method:'friend',status:'running',createdAt:0,revision:0,startAt:null,hostSession:'s1',aiFill:[],participants:[participant(cls)],run:{id:`supporter-${cls}-${level}`,seed:1,rngState:123456789,status:'combat',startAt:0,combatAt:0,stage,stageTarget:999,spawned:0,nextSpawnAt:999999999,baseHp:2000,baseHpMax:2000,kills:0,nextMonsterId,monsters:monsters||[supporter(),runner()],players:[p],ai:[],events:[],nextEventId:1,revision:0,shop:null,skillQueue:[],n3Queue:[],supportAuraAt}};a.rng=()=>.99;return a}
function pack(name,pass,actual,expected){return{name,pass:!!pass,actual,expected}}

export function runV044SupporterSelfTest(RoomClass){
  const checks=[],eps=1e-7,start=1000;

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start)]});a.reconcileSupportAuraAt(start);const s=a.room.run.monsters[0];
    checks.push(pack('SUPPORTER_NEVER_SELF_BUFFS',a.movementSpeedMultiplier(s)===1&&s.supportAuraSources.length===0,{mul:a.movementSpeedMultiplier(s),sources:s.supportAuraSources},{mul:1,sources:[]}));
  }catch(e){checks.push(pack('SUPPORTER_SELF_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start),runner(2,.75,.40,start)]});a.reconcileSupportAuraAt(start);const t=a.nextSupportAuraCrossingAt(start,4000),expected=start+(.25-.18)/(.135-.055)*1000+.001;
    checks.push(pack('SUPPORTER_STATIC_ENTRY_CROSSING_TIME',Math.abs(t-expected)<.01,{t,expected},{toleranceMs:.01}));
  }catch(e){checks.push(pack('SUPPORTER_ENTRY_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start),runner(2,.75,.40,start)]});a.reconcileSupportAuraAt(start);const t=a.nextSupportAuraCrossingAt(start,4000),target=a.room.run.monsters[1],before=a.xAt(target,t);a.reconcileSupportAuraAt(t);const after=a.xAt(target,t),sources=target.supportAuraSources;
    checks.push(pack('SUPPORTER_ENTRY_POSITION_CONTINUOUS',sources.join(',')==='1'&&Math.abs(before-after)<eps&&a.movementSpeedMultiplier(target)===1.18,{before,after,sources,mul:a.movementSpeedMultiplier(target)},{continuous:true,sources:[1],mul:1.18}));
  }catch(e){checks.push(pack('SUPPORTER_ENTRY_CONTINUITY_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start),runner(2,.75,.40,start)]});a.reconcileSupportAuraAt(start);const enter=a.nextSupportAuraCrossingAt(start,4000);a.reconcileSupportAuraAt(enter);const exit=a.nextSupportAuraCrossingAt(enter,8000);a.reconcileSupportAuraAt(exit);const target=a.room.run.monsters[1];
    checks.push(pack('SUPPORTER_EXIT_REMOVES_MULTIPLIER',Number.isFinite(exit)&&exit>enter&&target.supportAuraSources.length===0&&a.movementSpeedMultiplier(target)===1,{enter,exit,sources:target.supportAuraSources,mul:a.movementSpeedMultiplier(target)},{exitAfterEnter:true,sources:[],mul:1}));
  }catch(e){checks.push(pack('SUPPORTER_EXIT_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.38,start),supporter(3,.52,.42,start),grunt(2,.62,.40,start)]});a.reconcileSupportAuraAt(start);const t=a.room.run.monsters.find(m=>m.id===2);
    checks.push(pack('SUPPORTER_OVERLAP_NON_STACKING',t.supportAuraSources.join(',')==='1,3'&&a.movementSpeedMultiplier(t)===1.18,{sources:t.supportAuraSources,mul:a.movementSpeedMultiplier(t)},{sources:[1,3],mul:1.18}));
  }catch(e){checks.push(pack('SUPPORTER_OVERLAP_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start),supporter(3,.58,.40,start)]});a.reconcileSupportAuraAt(start);const s1=a.room.run.monsters[0],s3=a.room.run.monsters[1];
    checks.push(pack('SUPPORTER_CAN_COVER_OTHER_SUPPORTER_NOT_SELF',s1.supportAuraSources.join(',')==='3'&&s3.supportAuraSources.join(',')==='1'&&a.movementSpeedMultiplier(s1)===1.18&&a.movementSpeedMultiplier(s3)===1.18,{s1:s1.supportAuraSources,s3:s3.supportAuraSources},{s1:[3],s3:[1]}));
  }catch(e){checks.push(pack('SUPPORTER_OTHER_SUPPORTER_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start,50),grunt(2,.62,.40,start)]});a.reconcileSupportAuraAt(start);const t=a.room.run.monsters[1],xBefore=a.xAt(t,1500);const s=a.room.run.monsters[0];a.applyDamage(s,50,1,'NORMAL',1500,true,'hit',false);const xAtDeath=t.x,expectedFuture=xAtDeath-.070*.1,actualFuture=a.xAt(t,1600);
    checks.push(pack('SUPPORTER_DEATH_DROPS_AURA_AT_EXACT_TIMESTAMP',t.supportAuraSources.length===0&&Math.abs(xAtDeath-xBefore)<eps&&Math.abs(actualFuture-expectedFuture)<eps,{xBefore,xAtDeath,actualFuture,expectedFuture,sources:t.supportAuraSources},{continuous:true,mulAfter:1}));
  }catch(e){checks.push(pack('SUPPORTER_DEATH_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start),grunt(2,.66,.40,start)]});a.reconcileSupportAuraAt(start);const t=a.room.run.monsters[1];const before=t.supportAuraSources.slice();a.applyDamage(t,10,1,'CRITICAL',start,true,'hit',false);
    checks.push(pack('SUPPORTER_KNOCKBACK_RECONCILES_TOPOLOGY',before.join(',')==='1'&&t.supportAuraSources.length===0,{before,after:t.supportAuraSources,x:t.x},{before:[1],after:[]}));
  }catch(e){checks.push(pack('SUPPORTER_KNOCK_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start,50),supporter(3,.52,.43,start),grunt(2,.62,.40,start)]});a.reconcileSupportAuraAt(start);const target=a.room.run.monsters.find(m=>m.id===2);a.applyDamage(a.room.run.monsters.find(m=>m.id===1),50,1,'NORMAL',start,true,'hit',false);
    checks.push(pack('SUPPORTER_SOURCE_REMOVAL_PRESERVES_OTHER_SOURCE',target.supportAuraSources.join(',')==='3'&&a.movementSpeedMultiplier(target)===1.18,{sources:target.supportAuraSources,mul:a.movementSpeedMultiplier(target)},{sources:[3],mul:1.18}));
  }catch(e){checks.push(pack('SUPPORTER_SOURCE_REMOVAL_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start),flyer(2,.67,.46,start)]});a.reconcileSupportAuraAt(start);const t1=a.nextSupportAuraCrossingAt(start,3500);const snapshot=JSON.parse(JSON.stringify(a.room.run.monsters)),b=actor(RoomClass,{monsters:snapshot,supportAuraAt:start}),t2=b.nextSupportAuraCrossingAt(start,3500);
    checks.push(pack('SUPPORTER_FLYER_Y_CROSSING_DETERMINISTIC',Number.isFinite(t1)&&Math.abs(t1-t2)<.001,{t1,t2},{sameCrossing:true}));
  }catch(e){checks.push(pack('SUPPORTER_FLYER_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.65,.40,start),charger(2,.80,.40,start)]});a.reconcileSupportAuraAt(start);const c=a.room.run.monsters[1],advanceSpeed=a.currentSegmentSpeed(c,start);c.chargerPhase='windup';c.refAt=start;c.chargerPhaseAt=start;const windupSpeed=a.currentSegmentSpeed(c,start);c.chargerPhase='charge';c.refAt=start;c.chargerPhaseAt=start;const chargeSpeed=a.currentSegmentSpeed(c,start);
    checks.push(pack('SUPPORTER_CHARGER_PHASE_COMPOSITION',Math.abs(advanceSpeed-.060*1.18)<eps&&windupSpeed===0&&Math.abs(chargeSpeed-.210*1.18)<eps,{advanceSpeed,windupSpeed,chargeSpeed},{advance:.0708,windup:0,charge:.2478}));
  }catch(e){checks.push(pack('SUPPORTER_CHARGER_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start),splitter(2,.60,.40,start,100)]});a.reconcileSupportAuraAt(start);const p=a.room.run.monsters[1];a.applyDamage(p,100,1,'NORMAL',start,true,'hit',false);const kids=a.room.run.monsters.filter(m=>m.type==='splitter-child');
    checks.push(pack('SUPPORTER_SPLITTER_CHILDREN_RECONCILE_ON_SPAWN',kids.length===2&&kids.every(k=>k.supportAuraSources.join(',')==='1'&&a.movementSpeedMultiplier(k)===1.18),kids.map(k=>({id:k.id,sources:k.supportAuraSources,mul:a.movementSpeedMultiplier(k)})),{count:2,sources:[1],mul:1.18}));
  }catch(e){checks.push(pack('SUPPORTER_SPLITTER_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const direct=actor(RoomClass,{monsters:[supporter(1,.50,.40,start),runner(2,.75,.40,start)]});direct.reconcileSupportAuraAt(start);const xDirect=direct.xAt(direct.room.run.monsters[1],1700);
    const polled=actor(RoomClass,{monsters:[supporter(1,.50,.40,start),runner(2,.75,.40,start)]});polled.reconcileSupportAuraAt(start);polled.reconcileSupportAuraAt(1200);polled.reconcileSupportAuraAt(1400);const xPolled=polled.xAt(polled.room.run.monsters[1],1700);
    checks.push(pack('SUPPORTER_NO_POLL_FREQUENCY_DRIFT_BEFORE_CROSSING',Math.abs(xDirect-xPolled)<eps,{xDirect,xPolled},{same:true}));
  }catch(e){checks.push(pack('SUPPORTER_POLL_DRIFT_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start),runner(2,.75,.40,start)]});a.reconcileSupportAuraAt(start);const saved=JSON.parse(JSON.stringify(a.room.run.monsters)),b=actor(RoomClass,{monsters:saved,supportAuraAt:a.room.run.supportAuraAt});const ta=a.nextSupportAuraCrossingAt(start,4000),tb=b.nextSupportAuraCrossingAt(start,4000),xa=a.xAt(a.room.run.monsters[1],1600),xb=b.xAt(b.room.run.monsters[1],1600);
    checks.push(pack('SUPPORTER_RECONNECT_RECONSTRUCTION',Math.abs(ta-tb)<.001&&Math.abs(xa-xb)<eps,{ta,tb,xa,xb},{sameCrossing:true,sameX:true}));
  }catch(e){checks.push(pack('SUPPORTER_RECONNECT_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.20,.40,start),grunt(2,.30,.40,start)]});a.reconcileSupportAuraAt(start);const s=a.room.run.monsters[0],t=a.room.run.monsters[1],hitAt=a.wallAt(s);a.processAt(hitAt);const e=a.room.run.events.find(x=>x.type==='wall'&&x.targetId===1);
    checks.push(pack('SUPPORTER_WALL_REMOVAL_DROPS_AURA',e?.damage===70&&!a.room.run.monsters.some(m=>m.id===1)&&t.supportAuraSources.length===0,{event:e,targetSources:t.supportAuraSources},{damage:70,targetSources:[]}));
  }catch(e){checks.push(pack('SUPPORTER_WALL_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start,100)]}),p=a.room.run.players[0],r=a.applyDamage(a.room.run.monsters[0],100,1,'NORMAL',start,true,'hit',false),e=a.room.run.events.at(-1);
    checks.push(pack('SUPPORTER_COMBAT_IDENTITY_REWARD',r.killed&&p.coin===8&&p.killCoinEarned===8&&p.kills===1&&e.monsterType==='supporter',{r,p,e},{reward:8,killed:true}));
  }catch(e){checks.push(pack('SUPPORTER_REWARD_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[supporter(1,.50,.40,start),runner(2,.75,.40,start)]});a.reconcileSupportAuraAt(start);const crossing=a.nextSupportAuraCrossingAt(start,4000),due=a.nextDueAt();
    checks.push(pack('SUPPORTER_NEXT_DUE_INCLUDES_AURA_CROSSING',Number.isFinite(crossing)&&Math.abs(due-crossing)<.01,{crossing,due},{same:true}));
  }catch(e){checks.push(pack('SUPPORTER_NEXT_DUE_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  const passed=checks.filter(x=>x.pass).length;return{ok:passed===checks.length,version:'0.44-cf.1-supporter-selftest',passed,total:checks.length,failed:checks.filter(x=>!x.pass).map(x=>x.name),checks};
}
