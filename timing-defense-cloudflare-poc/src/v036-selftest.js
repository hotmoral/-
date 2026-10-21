// Timing Defense Cloudflare v0.36 Slice A deterministic server self-test.
// Executes the actual patched TimingDefenseRoom prototype in isolated in-memory rooms.
// No Durable Object storage or production room state is mutated.

function player(slot=1,level=5){
  return {slot,level,xp:0,xpNeed:60+12*(level-1),charge:0,combo:0,comboPeak:0,kills:0,coin:0,damage:0,lastSeq:0,nextPassiveAt:999999999,upgrades:{atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0},killCoinEarned:0};
}
function monster(id,x=.55,y=.335,hp=5000,type='grunt'){
  return {id,type,x,y,refAt:1000,hp,maxHp:hp};
}
function makeActor(RoomClass,{cls='knight',level=5,stage=1,charge=0,monsters=null,twoHumans=false,withAi=false}={}){
  const actor=Object.create(RoomClass.prototype);
  const p1=player(1,level);p1.charge=charge;
  const participants=[{session:'s1',slot:1,nickname:'A',classId:cls,ready:true,connected:true,activeConnectionId:'c1',joinedAt:0}];
  const players=[p1];
  if(twoHumans){participants.push({session:'s2',slot:2,nickname:'B',classId:'knight',ready:true,connected:true,activeConnectionId:'c2',joinedAt:0});players.push(player(2,5));}
  const list=monsters||[monster(1)];
  actor.room={
    version:'selftest',code:'TST001',method:'friend',status:'running',startAt:null,hostSession:'s1',aiFill:withAi?[{pos:3,cls:'knight'}]:[],participants,
    run:{id:`self-${cls}-${level}-${stage}`,seed:1,rngState:123456789,status:'combat',startAt:0,combatAt:0,stage,stageTarget:999,spawned:0,nextSpawnAt:999999999,
      baseHp:2000,baseHpMax:2000,kills:0,nextMonsterId:100,monsters:list,players,ai:withAi?[{slot:3,cls:'knight',charge:0,nextAt:999999999,kills:0,damage:0,killCoinEarned:0}]:[],events:[],nextEventId:1,revision:0,shop:null,skillQueue:[]}
  };
  return actor;
}
function approx(a,b,eps=1e-9){return Math.abs(a-b)<=eps}
function pack(name,pass,actual,expected,extra={}){return{name,pass:!!pass,actual,expected,...extra}}

export function runV036SelfTest(RoomClass){
  const checks=[];
  const at=1000;
  try{
    // N1 exact heavy-tier EXP through the real playerAction wrapper.
    const a=makeActor(RoomClass,{cls:'knight',level:5,charge:3});
    const r=a.playerAction(a.room.participants[0],{seq:1,xJudge:'GOOD',yJudge:'NORMAL'},at);
    checks.push(pack('N1_HEAVY_PLUS_EXP',r.xpGain===14&&a.room.run.players[0].xp===14,{tier:r.tier,xpGain:r.xpGain,xp:a.room.run.players[0].xp},{tier:'HEAVY+',xpGain:14,xp:14}));
    let stale=false;try{a.playerAction(a.room.participants[0],{seq:1,xJudge:'NORMAL'},at+1)}catch(e){stale=e?.message==='stale-seq'}
    checks.push(pack('DUPLICATE_SEQ_REJECTED',stale,stale,true));
  }catch(e){checks.push(pack('N1_AND_SEQ_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    // N2 exact AI stage multiplier through the real applyDamage wrapper.
    const s1=makeActor(RoomClass,{stage:1,withAi:true});
    const r1=s1.applyDamage(s1.room.run.monsters[0],100,3,'NORMAL',at,true,'ai',false);
    const s2=makeActor(RoomClass,{stage:2,withAi:true});
    const r2=s2.applyDamage(s2.room.run.monsters[0],100,3,'NORMAL',at,true,'ai',false);
    const s10=makeActor(RoomClass,{stage:10,withAi:true});
    const r10=s10.applyDamage(s10.room.run.monsters[0],100,3,'NORMAL',at,true,'ai',false);
    checks.push(pack('N2_AI_STAGE_SCALE',r1.actual===100&&r2.actual===103&&r10.actual===132,{stage1:r1.actual,stage2:r2.actual,stage10:r10.actual},{stage1:100,stage2:103,stage10:132}));
  }catch(e){checks.push(pack('N2_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const lv5=makeActor(RoomClass,{cls:'knight',level:5}),lv6=makeActor(RoomClass,{cls:'knight',level:6});
    const r5=lv5.playerAction(lv5.room.participants[0],{seq:1,xJudge:'NORMAL'},at);
    const r6=lv6.playerAction(lv6.room.participants[0],{seq:1,xJudge:'NORMAL'},at);
    checks.push(pack('LV6_KNIGHT_DAMAGE',r5.actual===100&&r6.actual===112,{lv5:r5.actual,lv6:r6.actual},{lv5:100,lv6:112}));
  }catch(e){checks.push(pack('KNIGHT_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=makeActor(RoomClass,{cls:'rogue',level:6});
    const before=a.room.run.monsters[0].hp;
    const r=a.playerAction(a.room.participants[0],{seq:1,xJudge:'NORMAL'},at);
    const queued=a.room.run.skillQueue.length===1&&a.room.run.skillQueue[0].damage===55;
    a.processV036SkillQueue(at+55);
    const ev=a.room.run.events.filter(e=>e.actionId===r.actionId);
    const after=a.room.run.monsters[0].hp;
    const ids=ev.map(e=>e.hitIndex),damages=ev.map(e=>e.damage),types=ev.map(e=>e.type);
    checks.push(pack('LV6_ROGUE_SECOND_DAGGER',queued&&before-after===155&&ev.length===2&&ids[0]===0&&ids[1]===1&&damages[0]===100&&damages[1]===55&&types[0]==='hit'&&types[1]==='skill',{queued,totalDamage:before-after,eventCount:ev.length,hitIndices:ids,damages,types,actionIds:[...new Set(ev.map(e=>e.actionId))]},{queued:true,totalDamage:155,eventCount:2,hitIndices:[0,1],damages:[100,55],types:['hit','skill'],oneActionId:true}));
    const once=a.processV036SkillQueue(at+110)===false;
    checks.push(pack('LV6_ROGUE_SECONDARY_EXACTLY_ONCE',once,a.room.run.events.filter(e=>e.type==='skill').length,1));
  }catch(e){checks.push(pack('ROGUE_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const m5=monster(1,.55,.335),m6=monster(1,.55,.335);
    const lv5=makeActor(RoomClass,{cls:'tank',level:5,monsters:[m5]}),lv6=makeActor(RoomClass,{cls:'tank',level:6,monsters:[m6]});
    const x5=m5.x,x6=m6.x;
    lv5.playerAction(lv5.room.participants[0],{seq:1,xJudge:'NORMAL'},at);
    lv6.playerAction(lv6.room.participants[0],{seq:1,xJudge:'NORMAL'},at);
    const d5=m5.x-x5,d6=m6.x-x6,ratio=d6/d5;
    checks.push(pack('LV6_TANK_KNOCKBACK',approx(ratio,1.30,1e-8),{lv5Delta:d5,lv6Delta:d6,ratio},1.30));
  }catch(e){checks.push(pack('TANK_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const ms=[monster(1,.50,.335),monster(2,.70,.335),monster(3,.90,.335),monster(4,.72,.50)];
    const a=makeActor(RoomClass,{cls:'archer',level:6,monsters:ms});
    const r=a.playerAction(a.room.participants[0],{seq:1,xJudge:'NORMAL'},at);
    const ev=a.room.run.events.filter(e=>e.actionId===r.actionId);
    const skills=ev.filter(e=>e.type==='skill');
    checks.push(pack('LV6_ARCHER_STRICT_LINE',skills.length===2&&skills.every(e=>e.damage===52)&&skills.map(e=>e.targetId).join(',')==='2,3',{skillCount:skills.length,damages:skills.map(e=>e.damage),targets:skills.map(e=>e.targetId),offLineHp:ms[3].hp},{skillCount:2,damages:[52,52],targets:[2,3],offLineUntouched:true}));
  }catch(e){checks.push(pack('ARCHER_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const ms=[monster(1,.50,.40),monster(2,.56,.42),monster(3,.58,.36),monster(4,.60,.43),monster(5,.80,.40)];
    const a=makeActor(RoomClass,{cls:'mage',level:6,monsters:ms});
    const r=a.playerAction(a.room.participants[0],{seq:1,xJudge:'NORMAL'},at);
    const ev=a.room.run.events.filter(e=>e.actionId===r.actionId),skills=ev.filter(e=>e.type==='skill');
    checks.push(pack('LV6_MAGE_SPLASH',skills.length===3&&skills.every(e=>e.damage===50)&&skills.map(e=>e.targetId).join(',')==='2,3,4',{skillCount:skills.length,damages:skills.map(e=>e.damage),targets:skills.map(e=>e.targetId),farHp:ms[4].hp},{skillCount:3,damages:[50,50,50],targets:[2,3,4],farUntouched:true}));
  }catch(e){checks.push(pack('MAGE_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=makeActor(RoomClass,{cls:'knight',level:5,twoHumans:true,monsters:[]});
    a.room.run.stage=1;a.room.run.status='combat';
    const c1=a.room.run.players[0].coin,c2=a.room.run.players[1].coin;
    a.enterShop(at);
    const rewardOk=a.room.run.players[0].coin-c1===67&&a.room.run.players[1].coin-c2===67&&a.room.run.status==='shop';
    a.setShopReady(a.room.run.players[0],true,at+1);const partial=a.room.run.shop.canNext===false;
    a.setShopReady(a.room.run.players[1],true,at+2);const all=a.room.run.shop.canNext===true;
    a.beginStage(2,at+3);
    const stage2=a.room.run.stage===2&&a.room.run.status==='stage-starting'&&a.room.run.stageTarget===10&&Array.isArray(a.room.run.skillQueue)&&a.room.run.skillQueue.length===0;
    checks.push(pack('STAGE1_SHOP_STAGE2_FLOW',rewardOk&&partial&&all&&stage2,{rewardOk,partial,all,stage:a.room.run.stage,status:a.room.run.status,target:a.room.run.stageTarget},{rewardOk:true,partial:true,all:true,stage:2,status:'stage-starting',target:10}));
  }catch(e){checks.push(pack('STAGE_FLOW_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  const passed=checks.filter(x=>x.pass).length;
  return {ok:passed===checks.length,version:'0.36-cf.3-selftest',passed,total:checks.length,failed:checks.filter(x=>!x.pass).map(x=>x.name),checks};
}
