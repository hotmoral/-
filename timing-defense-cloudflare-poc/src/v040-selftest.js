import { STAGE4, STAGE4_TYPES, stage4Type, stage4Hp, shieldArmorDamage, stage4WallDamage } from "./v040-entry.js";

function player(slot=1,level=6,combo=0){return{slot,level,xp:0,xpNeed:60+12*(level-1),charge:0,combo,comboPeak:combo,kills:0,coin:0,damage:0,lastSeq:0,nextPassiveAt:999999999,upgrades:{atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0},killCoinEarned:0}}
function monster(id,x,y,hp=100000,type='shield'){return{id,type,x,y,refAt:1000,hp,maxHp:hp,boss:false}}
function pack(name,pass,actual,expected){return{name,pass:!!pass,actual,expected}}
function actor(RoomClass,{cls='knight',level=6,combo=0,monsters=null,stage=4}={}){
  const a=Object.create(RoomClass.prototype),p=player(1,level,combo);
  a.room={version:'v040-selftest',code:'S4T001',method:'friend',status:'running',startAt:null,hostSession:'s1',aiFill:[],
    participants:[{session:'s1',slot:1,nickname:'A',classId:cls,ready:true,connected:true,activeConnectionId:'c1',joinedAt:0,host:true}],
    run:{id:`v040-${cls}-${combo}`,seed:1,rngState:123456789,status:'combat',startAt:0,combatAt:0,stage,stageTarget:13,spawned:13,nextSpawnAt:999999999,
      baseHp:2000,baseHpMax:2000,kills:0,nextMonsterId:100,monsters:monsters||[monster(1,.60,.40)],players:[p],ai:[],events:[],nextEventId:1,revision:0,shop:null,skillQueue:[],n3Queue:[]}}
  a.rng=()=>.99;
  return a;
}

export function runV040SelfTest(RoomClass){
  const checks=[],add=(n,p,a,e)=>checks.push(pack(n,p,a,e)),at=1000;

  try{
    add('STAGE4_PLAN',STAGE4.count===13&&STAGE4.gap===940,STAGE4,{count:13,gap:940});
    const probes=[[0,'grunt'],[.359999,'grunt'],[.36,'runner'],[.619999,'runner'],[.62,'shield'],[.819999,'shield'],[.82,'brute'],[.999,'brute']];
    const got=probes.map(([r])=>stage4Type(r));
    add('STAGE4_COMPOSITION_THRESHOLDS',got.every((x,i)=>x===probes[i][1]),got,probes.map(x=>x[1]));
    const hp={grunt:stage4Hp('grunt'),runner:stage4Hp('runner'),shield:stage4Hp('shield'),brute:stage4Hp('brute')};
    add('STAGE4_HP_EXACT',hp.grunt===489&&hp.runner===252&&hp.shield===826&&hp.brute===1376,hp,{grunt:489,runner:252,shield:826,brute:1376});
    add('SHIELD_META_EXACT',STAGE4_TYPES.shield.hp===540&&STAGE4_TYPES.shield.speed===.057&&STAGE4_TYPES.shield.size===1.08&&STAGE4_TYPES.shield.baseDamage===120&&STAGE4_TYPES.shield.knockResist===.62&&STAGE4_TYPES.shield.armor===.72&&STAGE4_TYPES.shield.reward===10,STAGE4_TYPES.shield,{hp:540,speed:.057,size:1.08,baseDamage:120,knockResist:.62,armor:.72,reward:10});
    add('SHIELD_ARMOR_ROUNDING',shieldArmorDamage(101)===73&&shieldArmorDamage(1)===1,{d101:shieldArmorDamage(101),d1:shieldArmorDamage(1)},{d101:73,d1:1});
    add('SHIELD_WALL_DEF',stage4WallDamage('shield',0)===120&&stage4WallDamage('shield',4)===108,{r0:stage4WallDamage('shield',0),r4:stage4WallDamage('shield',4)},{r0:120,r4:108});
  }catch(e){add('STAGE4_PURE_CONTRACT_EXCEPTION',false,String(e?.stack||e),'no exception')}

  try{
    const a=actor(RoomClass),m=a.room.run.monsters[0];
    const x=a.xAt(m,2000),wall=a.wallAt(m);
    add('SHIELD_MOVEMENT_SPEED',Math.abs(x-(.60-.057))<1e-12,x,.543);
    add('SHIELD_WALL_TIME',Math.abs(wall-(1000+((.60-.155)/.057)*1000))<1e-8,wall,1000+((.60-.155)/.057)*1000);
  }catch(e){add('SHIELD_MOVEMENT_EXCEPTION',false,String(e?.stack||e),'no exception')}

  try{
    const a=actor(RoomClass),m=a.room.run.monsters[0];
    const r=a.applyDamage(m,101,1,'NORMAL',at,false,'hit',false);
    add('SHIELD_PLAYER_ARMOR_AUTHORITY',r.actual===73&&m.hp===99927,{actual:r.actual,hp:m.hp},{actual:73,hp:99927});
  }catch(e){add('SHIELD_PLAYER_ARMOR_EXCEPTION',false,String(e?.stack||e),'no exception')}

  try{
    const a=actor(RoomClass),m=a.room.run.monsters[0];a.room.run.ai=[{slot:2,kills:0,damage:0,killCoinEarned:0}];
    const r=a.applyDamage(m,100,2,'NORMAL',at,false,'ai',false);
    add('SHIELD_AI_STAGE4_SCALE_THEN_ARMOR',r.actual===80,r.actual,80);
  }catch(e){add('SHIELD_AI_SCALE_EXCEPTION',false,String(e?.stack||e),'no exception')}

  try{
    const a=actor(RoomClass,{monsters:[monster(1,.60,.40,100,'shield')]}),p=a.room.run.players[0],m=a.room.run.monsters[0];
    const r=a.applyDamage(m,1000,1,'NORMAL',at,false,'hit',false);
    add('SHIELD_KILL_REWARD_CONTRIBUTION',r.killed&&p.kills===1&&p.coin===10&&p.killCoinEarned===10&&p.damage===720&&a.room.run.kills===1,{result:r,kills:p.kills,coin:p.coin,killCoin:p.killCoinEarned,damage:p.damage,runKills:a.room.run.kills},{killed:true,reward:10,damage:720});
  }catch(e){add('SHIELD_KILL_REWARD_EXCEPTION',false,String(e?.stack||e),'no exception')}

  try{
    const a=actor(RoomClass,{cls:'tank',level:6}),p=a.room.run.players[0],m=a.room.run.monsters[0],before=m.x;p.__v036TankLv6=true;
    a.applyDamage(m,1,1,'NORMAL',at,true,'hit',false);p.__v036TankLv6=false;
    const push=m.x-before,expected=.006*.62*1.30;
    add('SHIELD_TANK_LV6_KNOCK_META',Math.abs(push-expected)<1e-10,push,expected);
  }catch(e){add('SHIELD_TANK_LV6_KNOCK_EXCEPTION',false,String(e?.stack||e),'no exception')}

  try{
    const primary=monster(1,.50,.30,100000,'grunt'),edge=monster(2,.72,.3468,100000,'shield'),a=actor(RoomClass,{cls:'archer',level:6,monsters:[primary,edge]});
    a.playerAction(a.room.participants[0],{seq:1,xJudge:'PERFECT'},at);
    const skill=a.room.run.events.filter(e=>e.type==='skill'&&e.targetId===2);
    add('LV6_ARCHER_USES_SHIELD_SIZE_108',skill.length===1,{skillTargets:skill.map(e=>e.targetId)},[2]);
  }catch(e){add('LV6_ARCHER_SHIELD_SIZE_EXCEPTION',false,String(e?.stack||e),'no exception')}

  try{
    const primary=monster(1,.50,.30,100000,'grunt'),edge=monster(2,.72,.3468,100000,'shield'),a=actor(RoomClass,{cls:'archer',level:6,combo:4,monsters:[primary,edge]});
    a.triggerN3(a.room.run.players[0],'archer',5,'edge',at);
    const n3=a.room.run.events.filter(e=>e.type==='n3');
    add('N3_ARCHER_USES_SHIELD_SIZE_108',n3.length===2&&n3.some(e=>e.targetId===2),{count:n3.length,targets:n3.map(e=>e.targetId)},{count:2,targetsInclude:2});
  }catch(e){add('N3_ARCHER_SHIELD_SIZE_EXCEPTION',false,String(e?.stack||e),'no exception')}

  try{
    const a=actor(RoomClass,{cls:'tank',level:6,combo:4,monsters:[monster(1,.60,.40,100000,'shield')]}),m=a.room.run.monsters[0],before=m.x;
    a.triggerN3(a.room.run.players[0],'tank',5,'tankn3',at);
    const push=m.x-before,expected=.006*.62*1.30;
    add('N3_TANK_USES_SHIELD_KNOCK_062',Math.abs(push-expected)<1e-10,push,expected);
  }catch(e){add('N3_TANK_SHIELD_KNOCK_EXCEPTION',false,String(e?.stack||e),'no exception')}

  try{
    const a=actor(RoomClass,{stage:3});a.room.run.status='shop';a.room.run.shop={stage:3,canNext:true};
    a.beginStage(4,at);
    const r=a.room.run;
    add('BEGIN_STAGE4_CONTRACT',r.stage===4&&r.status==='stage-starting'&&r.stageTarget===13&&r.spawned===0&&r.nextSpawnAt===r.combatAt&&Array.isArray(r.skillQueue)&&r.skillQueue.length===0&&Array.isArray(r.n3Queue)&&r.n3Queue.length===0,{stage:r.stage,status:r.status,target:r.stageTarget,spawned:r.spawned,next:r.nextSpawnAt,combat:r.combatAt},{stage:4,status:'stage-starting',target:13});
  }catch(e){add('BEGIN_STAGE4_EXCEPTION',false,String(e?.stack||e),'no exception')}

  try{
    const a=actor(RoomClass);let entered=0;a.enterShop=()=>{entered++;a.room.run.status='shop';return true};a.room.run.monsters=[];a.room.run.spawned=13;a.room.run.stageTarget=13;a.room.run.status='combat';
    const ended=a.checkEnd(at);
    add('STAGE4_CLEAR_ENTERS_SHOP',ended&&entered===1&&a.room.run.status==='shop',{ended,entered,status:a.room.run.status},{ended:true,entered:1,status:'shop'});
  }catch(e){add('STAGE4_CLEAR_EXCEPTION',false,String(e?.stack||e),'no exception')}

  try{
    const a=actor(RoomClass);let error='';try{a.beginStage(5,at)}catch(e){error=e.message||String(e)}
    add('STAGE5_REMAINS_BLOCKED',error==='stage-not-supported',error,'stage-not-supported');
  }catch(e){add('STAGE5_BLOCK_EXCEPTION',false,String(e?.stack||e),'no exception')}

  const passed=checks.filter(x=>x.pass).length;
  return{ok:passed===checks.length,version:'0.40-cf.1-selftest',passed,total:checks.length,failed:checks.filter(x=>!x.pass).map(x=>x.name),checks};
}