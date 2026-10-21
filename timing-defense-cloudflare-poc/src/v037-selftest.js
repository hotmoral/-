// Timing Defense v0.37 Slice B deterministic server self-test.
// Executes the actual patched TimingDefenseRoom prototype in isolated state.

function player(slot=1,level=6){
  return {slot,level,xp:0,xpNeed:60+12*(level-1),charge:0,combo:0,comboPeak:0,kills:0,coin:0,damage:0,lastSeq:0,nextPassiveAt:999999999,upgrades:{atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0},killCoinEarned:0};
}
function makeActor(RoomClass,{stage=3,twoHumans=true,withAi=false}={}){
  const actor=Object.create(RoomClass.prototype);
  const participants=[{session:'s1',slot:1,nickname:'A',classId:'rogue',ready:true,connected:true,activeConnectionId:'c1',joinedAt:0,host:true}];
  const players=[player(1,6)];
  if(twoHumans){participants.push({session:'s2',slot:2,nickname:'B',classId:'archer',ready:true,connected:true,activeConnectionId:'c2',joinedAt:0});players.push(player(2,6));}
  actor.room={
    version:'selftest',code:'TST037',method:'friend',status:'running',startAt:null,hostSession:'s1',aiFill:withAi?[{pos:3,cls:'knight'}]:[],participants,
    run:{id:'self-v037',seed:1,rngState:123456789,status:'combat',startAt:0,combatAt:0,stage,stageTarget:12,spawned:0,nextSpawnAt:999999999,
      baseHp:2000,baseHpMax:2000,kills:0,nextMonsterId:1,monsters:[],players,ai:withAi?[{slot:3,cls:'knight',charge:0,nextAt:999999999,kills:0,damage:0,killCoinEarned:0}]:[],events:[],nextEventId:1,revision:0,shop:null,skillQueue:[]}
  };
  return actor;
}
function brute(id=1,hp=1247,x=.55,y=.40){return{id,type:'brute',x,y,refAt:1000,hp,maxHp:hp}}
function approx(a,b,eps=1e-9){return Math.abs(a-b)<=eps}
function pack(name,pass,actual,expected){return{name,pass:!!pass,actual,expected}}

export async function runV037SelfTest(RoomClass){
  const checks=[];
  try{
    const a=makeActor(RoomClass,{twoHumans:false});
    const m=brute();
    const x=a.xAt(m,2000),wall=a.wallAt(m);
    checks.push(pack('BRUTE_MOVEMENT_CONTRACT',approx(x,.51,1e-12)&&approx(wall,10875,1e-9),{xAt2s:x,wallAt:wall},{xAt2s:.51,wallAt:10875}));
  }catch(e){checks.push(pack('BRUTE_MOVEMENT_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=makeActor(RoomClass,{twoHumans:false});
    const seq=[.43,0,0,.44,0,0,.779,0,0,.78,0,0];a.rng=()=>seq.shift()??0;
    a.beginStage(3,1000);
    const due=a.nextDueAt();
    for(let i=0;i<4;i++)a.spawnStage3(a.room.run.combatAt+i*980);
    const types=a.room.run.monsters.map(m=>m.type),hps=a.room.run.monsters.map(m=>m.hp);
    checks.push(pack('STAGE3_PLAN_AND_THRESHOLDS',a.room.run.stageTarget===12&&due===a.room.run.combatAt&&types.join(',')==='grunt,runner,runner,brute'&&hps.join(',')==='444,229,229,1247',{target:a.room.run.stageTarget,gap:980,nextDue:due,combatAt:a.room.run.combatAt,types,hps},{target:12,gap:980,types:['grunt','runner','runner','brute'],hps:[444,229,229,1247]}));
  }catch(e){checks.push(pack('STAGE3_PLAN_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=makeActor(RoomClass,{twoHumans:false});
    const m=brute(1,100);a.room.run.monsters=[m];
    const beforeX=m.x,r=a.applyDamage(m,100,1,'NORMAL',1000,true,'hit',false),p=a.room.run.players[0];
    checks.push(pack('BRUTE_HUMAN_DAMAGE_REWARD',r.actual===100&&r.killed===true&&p.coin===14&&p.killCoinEarned===14&&p.kills===1&&p.damage===100,{actual:r.actual,killed:r.killed,coin:p.coin,killCoin:p.killCoinEarned,kills:p.kills,damage:p.damage,xDelta:m.x-beforeX},{actual:100,killed:true,coin:14,killCoin:14,kills:1,damage:100}));
  }catch(e){checks.push(pack('BRUTE_HUMAN_DAMAGE_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=makeActor(RoomClass,{twoHumans:false});
    const m=brute(1,5000);a.room.run.monsters=[m];
    const x0=m.x;a.applyDamage(m,100,1,'NORMAL',1000,true,'hit',false);const normal=m.x-x0;
    const b=makeActor(RoomClass,{twoHumans:false});const m2=brute(1,5000);b.room.run.monsters=[m2];b.room.run.players[0].__v036TankLv6=true;
    const x1=m2.x;b.applyDamage(m2,100,1,'NORMAL',1000,true,'hit',false);const tank=m2.x-x1;
    checks.push(pack('BRUTE_KNOCK_AND_TANK_LV6',approx(normal,.006*.38,1e-10)&&approx(tank/normal,1.30,1e-8),{normal,tank,ratio:tank/normal},{normal:.00228,ratio:1.30}));
  }catch(e){checks.push(pack('BRUTE_KNOCK_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=makeActor(RoomClass,{twoHumans:false,withAi:true});
    const m=brute(1,5000);a.room.run.monsters=[m];
    const r=a.applyDamage(m,100,3,'NORMAL',1000,true,'ai',false),ai=a.room.run.ai[0];
    checks.push(pack('BRUTE_AI_STAGE3_SCALE',r.actual===107&&ai.damage===107,{actual:r.actual,aiDamage:ai.damage},{actual:107,aiDamage:107}));
  }catch(e){checks.push(pack('BRUTE_AI_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=makeActor(RoomClass,{stage:2});
    a.room.run.stageTarget=10;a.room.run.spawned=10;a.room.run.monsters=[];a.room.run.status='combat';
    const c1=a.room.run.players[0].coin,c2=a.room.run.players[1].coin;
    const ended=a.checkEnd(2000);
    checks.push(pack('STAGE2_CLEAR_TO_SHOP',ended&&a.room.run.status==='shop'&&a.room.run.shop?.stage===2&&a.room.run.players[0].coin-c1===79&&a.room.run.players[1].coin-c2===79,{ended,status:a.room.run.status,shopStage:a.room.run.shop?.stage,reward1:a.room.run.players[0].coin-c1,reward2:a.room.run.players[1].coin-c2},{ended:true,status:'shop',shopStage:2,reward:79}));
  }catch(e){checks.push(pack('STAGE2_SHOP_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=makeActor(RoomClass,{stage:3});
    a.room.run.stageTarget=12;a.room.run.spawned=12;a.room.run.monsters=[];a.room.run.status='combat';
    const c1=a.room.run.players[0].coin,c2=a.room.run.players[1].coin;
    const ended=a.checkEnd(3000);
    checks.push(pack('STAGE3_CLEAR_TO_SHOP',ended&&a.room.run.status==='shop'&&a.room.run.shop?.stage===3&&a.room.run.players[0].coin-c1===91&&a.room.run.players[1].coin-c2===91,{ended,status:a.room.run.status,shopStage:a.room.run.shop?.stage,reward1:a.room.run.players[0].coin-c1,reward2:a.room.run.players[1].coin-c2},{ended:true,status:'shop',shopStage:3,reward:91}));
  }catch(e){checks.push(pack('STAGE3_SHOP_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=makeActor(RoomClass,{stage:2});
    a.room.run.status='shop';a.room.run.shop={stage:2,readySlots:[1,2],canNext:true};
    a.advanceTo=()=>false;a.persist=async()=>{};a.broadcastState=()=>{};a.scheduleNext=async()=>{};a.publicState=()=>({code:a.room.code,run:a.room.run});
    const req=new Request('https://room.internal/v035/shop-next',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({session:'s1'})});
    const resp=await a.fetch(req),body=await resp.json();
    checks.push(pack('SHOP_STAGE2_TO_STAGE3',resp.status===200&&body.ok&&a.room.run.stage===3&&a.room.run.stageTarget===12&&a.room.run.status==='stage-starting',{status:resp.status,ok:body.ok,stage:a.room.run.stage,target:a.room.run.stageTarget,runStatus:a.room.run.status},{status:200,stage:3,target:12,runStatus:'stage-starting'}));
  }catch(e){checks.push(pack('SHOP_STAGE3_ENTRY_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=makeActor(RoomClass,{stage:3});
    a.room.run.status='shop';a.room.run.shop={stage:3,readySlots:[1,2],canNext:true};
    a.advanceTo=()=>false;a.persist=async()=>{};a.broadcastState=()=>{};a.scheduleNext=async()=>{};a.publicState=()=>({code:a.room.code,run:a.room.run});
    const req=new Request('https://room.internal/v035/shop-next',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({session:'s1'})});
    const resp=await a.fetch(req),body=await resp.json();
    checks.push(pack('STAGE4_SERVER_BLOCK',resp.status===409&&body.error==='stage4-blocked'&&a.room.run.stage===3,{status:resp.status,error:body.error,stage:a.room.run.stage},{status:409,error:'stage4-blocked',stage:3}));
  }catch(e){checks.push(pack('STAGE4_BLOCK_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  const passed=checks.filter(x=>x.pass).length;
  return {ok:passed===checks.length,version:'0.37-cf.1-selftest',passed,total:checks.length,failed:checks.filter(x=>!x.pass).map(x=>x.name),checks};
}