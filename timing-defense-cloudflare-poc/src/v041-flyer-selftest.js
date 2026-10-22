// Timing Defense v0.41 — deterministic FLYER authoritative-Y capability tests.

function player(slot=1,level=5,combo=0){return{slot,level,xp:0,xpNeed:60+12*(level-1),charge:0,combo,comboPeak:combo,kills:0,coin:0,damage:0,lastSeq:0,nextPassiveAt:999999999,upgrades:{atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0},killCoinEarned:0}}
function flyer(id=1,x=.50,baseY=.34,epoch=1000,hp=100000){return{id,type:'flyer',x,y:baseY,flyerBaseY:baseY,flyerEpochAt:epoch,refAt:epoch,hp,maxHp:hp,boss:false}}
function grunt(id=1,x=.50,y=.30,hp=100000){return{id,type:'grunt',x,y,refAt:1000,hp,maxHp:hp,boss:false}}
function actor(RoomClass,{cls='knight',level=5,combo=0,monsters=null,stage=1}={}){const a=Object.create(RoomClass.prototype),p=player(1,level,combo);a.room={version:'v041-flyer-selftest',code:'FLY001',method:'friend',status:'running',createdAt:0,revision:0,startAt:null,hostSession:'s1',aiFill:[],participants:[{session:'s1',slot:1,nickname:'A',classId:cls,ready:true,connected:true,activeConnectionId:'c1',joinedAt:0,host:true}],run:{id:`flyer-${cls}-${level}-${combo}`,seed:1,rngState:123456789,status:'combat',startAt:0,combatAt:0,stage,stageTarget:999,spawned:0,nextSpawnAt:999999999,baseHp:2000,baseHpMax:2000,kills:0,nextMonsterId:100,monsters:monsters||[flyer()],players:[p],ai:[],events:[],nextEventId:1,revision:0,shop:null,skillQueue:[],n3Queue:[]}};a.rng=()=>.99;return a}
function pack(name,pass,actual,expected){return{name,pass:!!pass,actual,expected}}

export function runV041FlyerSelfTest(RoomClass){
  const checks=[],eps=1e-9,epoch=1000,tPeak=epoch+Math.PI/(2*5)*1000,tTrough=epoch+3*Math.PI/(2*5)*1000;

  try{const a=actor(RoomClass),m=a.room.run.monsters[0],y0=a.yAt(m,epoch),yp=a.yAt(m,tPeak),yt=a.yAt(m,tTrough);checks.push(pack('FLYER_Y_DETERMINISTIC_PHASE',Math.abs(y0-.34)<eps&&Math.abs(yp-.36)<eps&&Math.abs(yt-.32)<eps,{y0,yp,yt},{base:.34,peak:.36,trough:.32}))}catch(e){checks.push(pack('FLYER_Y_PHASE_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass,{monsters:[flyer(1,.80,.34,epoch)]}),m=a.room.run.monsters[0];a.materialize(m,tTrough);const base=m.flyerBaseY,phase=m.flyerEpochAt,x=m.x,y=m.y,later=a.yAt(m,tTrough+200);const expectedX=.80-.100*((tTrough-epoch)/1000);checks.push(pack('FLYER_MATERIALIZE_PRESERVES_Y_PHASE',Math.abs(x-expectedX)<eps&&Math.abs(y-.32)<eps&&base===.34&&phase===epoch&&Math.abs(later-(.34+Math.sin(((tTrough+200-epoch)/1000)*5)*.020))<eps,{x,y,base,phase,later},{x:expectedX,y:.32,base:.34,phase:epoch}))}catch(e){checks.push(pack('FLYER_MATERIALIZE_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass,{monsters:[flyer(1,.50,.34,epoch)]}),snap=a.runPublic(tPeak),m=snap.monsters[0];checks.push(pack('FLYER_PUBLIC_SNAPSHOT_PHASE_METADATA',Math.abs(m.y-.36)<eps&&m.baseY===.34&&m.yEpochAt===epoch&&m.yAmp===.020&&m.yOmega===5&&m.size===.78,{monster:m,serverTime:snap.serverTime},{y:.36,baseY:.34,yEpochAt:epoch,yAmp:.020,yOmega:5,size:.78}))}catch(e){checks.push(pack('FLYER_PUBLIC_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass,{monsters:[flyer(1,.50,.34,epoch,100)]}),p=a.room.run.players[0],r=a.applyDamage(a.room.run.monsters[0],100,1,'NORMAL',epoch,true,'hit',false),e=a.room.run.events.at(-1);checks.push(pack('FLYER_COMBAT_IDENTITY_REWARD',r.killed&&r.actual===100&&p.kills===1&&p.coin===7&&p.killCoinEarned===7&&p.damage===100&&e.monsterType==='flyer'&&e.rawDamage===100,{r,p,e},{killed:true,actual:100,reward:7,damage:100}))}catch(e){checks.push(pack('FLYER_COMBAT_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass,{cls:'tank',level:6}),m=a.room.run.monsters[0],x=m.x,p=a.room.run.players[0];p.__v036TankLv6=true;a.applyDamage(m,100,1,'NORMAL',epoch,true,'hit',false);const dx=m.x-x,expected=.006*.90*1.30;checks.push(pack('FLYER_TANK_LV6_KNOCK_RESIST',Math.abs(dx-expected)<eps,{dx,expected},{knockResist:.90,lv6Mul:1.30}))}catch(e){checks.push(pack('FLYER_KNOCK_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const primaryBase=.34,secondaryBase=.36693417721518995;
    const a=actor(RoomClass,{cls:'archer',level:6,monsters:[flyer(1,.50,primaryBase,epoch),flyer(2,.72,secondaryBase,epoch)]});
    const r=a.playerAction(a.room.participants[0],{seq:1,xJudge:'PERFECT'},tTrough),skill=a.room.run.events.find(e=>e.type==='skill'&&e.actionId===r.actionId);
    checks.push(pack('FLYER_LV6_ARCHER_USES_AUTHORITATIVE_Y',skill?.targetId===2,{skill,primaryY:a.yAt(a.room.run.monsters.find(m=>m.id===1),tTrough),secondaryY:a.yAt(a.room.run.monsters.find(m=>m.id===2),tTrough)},{secondaryTargetId:2,note:'dynamic line distance .031 inside; static-base distance .051 outside'}));
  }catch(e){checks.push(pack('FLYER_ARCHER_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const secondEpoch=tTrough-Math.PI/(2*5)*1000;
    const a=actor(RoomClass,{cls:'mage',level:6,monsters:[flyer(1,.50,.30,epoch),flyer(2,.57,.43,secondEpoch)]});
    const r=a.playerAction(a.room.participants[0],{seq:1,xJudge:'PERFECT'},tTrough),skills=a.room.run.events.filter(e=>e.type==='skill'&&e.actionId===r.actionId);
    checks.push(pack('FLYER_LV6_MAGE_USES_AUTHORITATIVE_Y',skills.length===0,{skills,primaryY:.28,secondaryY:.45,dynamicGap:.17,staticBaseGap:.13},{skills:0,note:'dynamic gap outside .16 while static bases would be inside'}));
  }catch(e){checks.push(pack('FLYER_MAGE_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const primaryBase=.34,secondaryBase=.36693417721518995;
    const a=actor(RoomClass,{cls:'archer',level:5,combo:4,monsters:[flyer(1,.50,primaryBase,epoch),flyer(2,.72,secondaryBase,epoch)]});
    a.playerAction(a.room.participants[0],{seq:1,xJudge:'PERFECT'},tTrough);const n3=a.room.run.events.filter(e=>e.type==='n3');
    checks.push(pack('FLYER_N3_ARCHER_USES_AUTHORITATIVE_Y',n3.length===2&&n3.some(e=>e.targetId===2),n3.map(e=>({targetId:e.targetId,targetY:e.targetY,n3Raw:e.n3Raw})),{count:2,secondaryTargetId:2}));
  }catch(e){checks.push(pack('FLYER_N3_ARCHER_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[flyer(1,.70,.34,epoch)]}),m=a.room.run.monsters[0];a.materialize(m,tPeak);const persisted=JSON.parse(JSON.stringify(m));const b=actor(RoomClass,{monsters:[persisted]}),future=tPeak+777,ya=a.yAt(m,future),yb=b.yAt(persisted,future);checks.push(pack('FLYER_RECONNECT_RECONSTRUCTION_NO_PHASE_RESET',Math.abs(ya-yb)<eps&&persisted.flyerEpochAt===epoch&&persisted.flyerBaseY===.34,{ya,yb,epoch:persisted.flyerEpochAt,base:persisted.flyerBaseY},{sameY:true,epoch,base:.34}));
  }catch(e){checks.push(pack('FLYER_RECONNECT_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{const a=actor(RoomClass,{monsters:[grunt(1,.50,.37)]}),m=a.room.run.monsters[0];checks.push(pack('NON_FLYER_Y_UNCHANGED',a.yAt(m,tTrough)===.37,a.yAt(m,tTrough),.37))}catch(e){checks.push(pack('NON_FLYER_Y_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  const passed=checks.filter(x=>x.pass).length;return{ok:passed===checks.length,version:'0.41-cf.1-flyer-selftest',passed,total:checks.length,failed:checks.filter(x=>!x.pass).map(x=>x.name),checks};
}
