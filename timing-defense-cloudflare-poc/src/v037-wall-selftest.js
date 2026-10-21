// Focused regression for Stage 3 authoritative wall contacts.
function makeActor(RoomClass,defRank=0){
  const actor=Object.create(RoomClass.prototype);
  actor.room={
    version:'selftest',code:'WALL37',method:'friend',status:'running',startAt:null,hostSession:'s1',aiFill:[],
    participants:[{session:'s1',slot:1,nickname:'A',classId:'tank',ready:true,connected:true,activeConnectionId:'c1',joinedAt:0,host:true}],
    run:{id:'wall-v037',seed:1,rngState:1,status:'combat',startAt:0,combatAt:0,stage:3,stageTarget:12,spawned:1,nextSpawnAt:999999999,
      baseHp:2000,baseHpMax:2000,kills:0,nextMonsterId:2,
      monsters:[{id:1,type:'brute',x:.155,y:.4,refAt:1000,hp:1247,maxHp:1247}],
      players:[{slot:1,level:6,xp:0,xpNeed:120,charge:0,combo:0,comboPeak:0,kills:0,coin:0,damage:0,lastSeq:0,nextPassiveAt:999999999,upgrades:{atk:0,crit:0,critdmg:0,hp:0,def:defRank,knock:0},killCoinEarned:0}],
      ai:[],events:[],nextEventId:1,revision:0,shop:null,skillQueue:[]}
  };
  return actor;
}

export function runV037WallSelfTest(RoomClass){
  const checks=[];
  const runCase=(name,defRank,expected)=>{
    try{
      const a=makeActor(RoomClass,defRank);a.processAt(1000);
      const ev=a.room.run.events.find(e=>e.type==='wall');
      checks.push({name,pass:a.room.run.baseHp===2000-expected&&ev?.damage===expected&&ev?.monsterType==='brute'&&a.room.run.monsters.length===0,actual:{baseHp:a.room.run.baseHp,damage:ev?.damage,type:ev?.monsterType,remaining:a.room.run.monsters.length},expected:{baseHp:2000-expected,damage:expected,type:'brute',remaining:0}});
    }catch(e){checks.push({name,pass:false,actual:String(e?.stack||e),expected:'no exception'})}
  };
  runCase('BRUTE_WALL_DAMAGE_180',0,180);
  runCase('BRUTE_WALL_DEF_10_PERCENT',4,162);
  const passed=checks.filter(x=>x.pass).length;
  return{ok:passed===checks.length,version:'0.37-cf.1-wall-selftest',passed,total:checks.length,failed:checks.filter(x=>!x.pass).map(x=>x.name),checks};
}