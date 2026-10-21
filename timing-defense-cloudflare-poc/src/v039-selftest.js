// Timing Defense v0.39 — deterministic N3 Option B authority tests.

function player(slot=1,level=5,combo=0){
  return{slot,level,xp:0,xpNeed:60+12*(level-1),charge:0,combo,comboPeak:combo,kills:0,coin:0,damage:0,lastSeq:0,nextPassiveAt:999999999,
    upgrades:{atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0},killCoinEarned:0};
}
function monster(id,x,y,hp=100000,type='grunt',boss=false){return{id,type,x,y,refAt:1000,hp,maxHp:hp,boss}}
function geometry(cls){
  if(cls==='rogue')return[monster(1,.50,.30)];
  if(cls==='knight')return[monster(1,.50,.30),monster(2,.62,.30)];
  if(cls==='tank')return[monster(1,.50,.36),monster(2,.57,.39),monster(3,.60,.31)];
  if(cls==='archer')return[monster(1,.50,.30),monster(2,.72,.30),monster(3,.74,.52)];
  return[monster(1,.50,.40),monster(2,.56,.42),monster(3,.58,.36),monster(4,.60,.43),monster(5,.82,.40)];
}
function actor(RoomClass,{cls='knight',level=5,combo=4,charge=0,monsters=null}={}){
  const a=Object.create(RoomClass.prototype),p=player(1,level,combo);p.charge=charge;
  a.room={version:'n3-selftest',code:'N3T001',method:'friend',status:'running',startAt:null,hostSession:'s1',aiFill:[],
    participants:[{session:'s1',slot:1,nickname:'A',classId:cls,ready:true,connected:true,activeConnectionId:'c1',joinedAt:0,host:true}],
    run:{id:`n3-${cls}-${combo}`,seed:1,rngState:123456789,status:'combat',startAt:0,combatAt:0,stage:1,stageTarget:999,spawned:0,nextSpawnAt:999999999,
      baseHp:2000,baseHpMax:2000,kills:0,nextMonsterId:100,monsters:monsters||geometry(cls),players:[p],ai:[],events:[],nextEventId:1,revision:0,shop:null,skillQueue:[],n3Queue:[]}}
  a.rng=()=>.99;
  return a;
}
function budget(m){return m>=30?210:m>=20?150:m>=10?90:60}
function hitCount(cls,m){return cls==='rogue'?(m>=30?5:m>=20?4:m>=10?3:2):cls==='knight'||cls==='archer'?2:cls==='tank'?3:4}
function pack(name,pass,actual,expected){return{name,pass:!!pass,actual,expected}}

export function runV039SelfTest(RoomClass){
  const checks=[],milestones=[5,10,20,30,40],classes=['rogue','knight','tank','archer','mage'],at=1000;

  for(const cls of classes){
    for(const m of milestones){
      try{
        const a=actor(RoomClass,{cls,level:5,combo:m-1});
        const r=a.playerAction(a.room.participants[0],{seq:1,xJudge:'PERFECT'},at);
        a.processN3Queue(at+500);
        const ev=a.room.run.events.filter(e=>e.type==='n3');
        const sum=ev.reduce((n,e)=>n+(Number(e.damage)||0),0),raw=ev.reduce((n,e)=>n+(Number(e.n3Raw)||0),0);
        const expectedCount=hitCount(cls,m),expectedBudget=budget(m);
        const meta=ev.every(e=>e.n3===true&&e.n3Milestone===m&&e.n3Budget===expectedBudget&&e.procCrit===false&&e.parentTier==='N3'&&e.tier==='NORMAL');
        checks.push(pack(`N3_${cls.toUpperCase()}_${m}_BUDGET_GEOMETRY`,ev.length===expectedCount&&sum===expectedBudget&&raw===expectedBudget&&meta,
          {count:ev.length,sum,raw,milestones:[...new Set(ev.map(e=>e.n3Milestone))],indices:ev.map(e=>e.hitIndex),tier:ev.map(e=>e.tier)},
          {count:expectedCount,sum:expectedBudget,raw:expectedBudget,milestone:m,tier:'NORMAL'}));
        checks.push(pack(`N3_${cls.toUpperCase()}_${m}_PROC_ISOLATION`,a.room.run.players[0].xp===18&&a.room.run.players[0].charge===1&&a.room.run.players[0].combo===m&&r.xpGain===18,
          {xp:a.room.run.players[0].xp,charge:a.room.run.players[0].charge,combo:a.room.run.players[0].combo,xpGain:r.xpGain},
          {xp:18,charge:1,combo:m,xpGain:18}));
      }catch(e){checks.push(pack(`N3_${cls.toUpperCase()}_${m}_EXCEPTION`,false,String(e?.stack||e),'no exception'))}
    }
  }

  try{
    const a=actor(RoomClass,{cls:'knight',level:5,combo:4,monsters:[monster(1,.50,.30)]});
    a.playerAction(a.room.participants[0],{seq:1,xJudge:'PERFECT'},at);
    const ev=a.room.run.events.filter(e=>e.type==='n3');
    checks.push(pack('N3_UNUSED_SECONDARY_NOT_REDIRECTED',ev.length===1&&ev[0].n3Raw===40&&ev[0].n3Budget===60,{count:ev.length,raw:ev.map(e=>e.n3Raw),sum:ev.reduce((n,e)=>n+e.damage,0)},{count:1,primaryRaw:40,maxBudget:60}));
  }catch(e){checks.push(pack('N3_UNUSED_SECONDARY_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{cls:'knight',level:5,combo:4,monsters:[monster(1,.50,.30,230),monster(2,.62,.30,100000)]});
    a.playerAction(a.room.participants[0],{seq:1,xJudge:'PERFECT'},at);
    const p=a.room.run.players[0],kill=a.room.run.events.find(e=>e.type==='n3'&&e.killed);
    checks.push(pack('N3_KILL_COIN_CONTRIBUTION',!!kill&&p.kills===1&&p.coin===6&&p.killCoinEarned===6&&p.damage>=250,{kill:!!kill,kills:p.kills,coin:p.coin,killCoin:p.killCoinEarned,damage:p.damage},{kill:true,kills:1,coin:6,killCoin:6,damageAtLeast:250}));
  }catch(e){checks.push(pack('N3_KILL_ATTRIBUTION_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{cls:'rogue',level:5,combo:4,monsters:[monster(1,.50,.30,100000,'grunt',true)]});
    a.playerAction(a.room.participants[0],{seq:1,xJudge:'PERFECT'},at);a.processN3Queue(at+500);
    const ev=a.room.run.events.filter(e=>e.type==='n3');
    checks.push(pack('N3_ROGUE_BOSS_SCALAR_070',ev.length===2&&ev.reduce((n,e)=>n+e.damage,0)===42&&ev.every(e=>e.n3Raw===30&&e.n3AppliedRaw===21),{count:ev.length,raw:ev.map(e=>e.n3Raw),applied:ev.map(e=>e.n3AppliedRaw),sum:ev.reduce((n,e)=>n+e.damage,0)},{count:2,raw:[30,30],applied:[21,21],sum:42}));
  }catch(e){checks.push(pack('N3_BOSS_SCALAR_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const mk=(level)=>actor(RoomClass,{cls:'tank',level,combo:4,monsters:[monster(1,.40,.30,1),monster(2,.60,.30,100000)]});
    const a=mk(5),b=mk(6),aTarget=a.room.run.monsters[1],bTarget=b.room.run.monsters[1],ax=aTarget.x,bx=bTarget.x;
    a.playerAction(a.room.participants[0],{seq:1,xJudge:'PERFECT'},at);b.playerAction(b.room.participants[0],{seq:1,xJudge:'PERFECT'},at);
    const d5=aTarget.x-ax,d6=bTarget.x-bx;
    checks.push(pack('N3_TANK_LV6_KNOCK_IDENTITY',Math.abs(d6/d5-1.30)<1e-8,{lv5:d5,lv6:d6,ratio:d6/d5},{ratio:1.30}));
  }catch(e){checks.push(pack('N3_TANK_LV6_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{cls:'rogue',level:6,combo:29,monsters:[monster(1,.50,.30,100000)]});
    const r=a.playerAction(a.room.participants[0],{seq:1,xJudge:'PERFECT'},at);
    a.processAt(at+500);
    const related=a.room.run.events.filter(e=>e.actionId===r.actionId||String(e.actionId||'').startsWith(`${r.actionId}:n3:`));
    const hit=related.filter(e=>e.type==='hit').length,skill=related.filter(e=>e.type==='skill').length,n3=related.filter(e=>e.type==='n3').length;
    checks.push(pack('N3_COEXISTS_WITH_LV6_ROGUE',hit===1&&skill===1&&n3===5&&related.length===7,{hit,skill,n3,total:related.length,types:related.map(e=>e.type)},{hit:1,skill:1,n3:5,total:7}));
  }catch(e){checks.push(pack('N3_LV6_COEXISTENCE_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{cls:'knight',level:5,combo:4,charge:3});
    a.playerAction(a.room.participants[0],{seq:1,xJudge:'PERFECT',yJudge:'PERFECT'},at);
    const ev=a.room.run.events.filter(e=>e.type==='n3');
    checks.push(pack('N3_HEAVY_X_Y_COUNTS_INDEPENDENTLY',ev.length===2&&ev.every(e=>e.n3Milestone===5)&&a.room.run.players[0].combo===6,{n3Count:ev.length,milestones:ev.map(e=>e.n3Milestone),combo:a.room.run.players[0].combo},{n3Count:2,milestone:5,combo:6}));
  }catch(e){checks.push(pack('N3_HEAVY_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{cls:'knight',level:5,combo:9,charge:3});
    a.playerAction(a.room.participants[0],{seq:1,xJudge:'NORMAL',yJudge:'PERFECT'},at);
    const ev=a.room.run.events.filter(e=>e.type==='n3');
    checks.push(pack('N3_RESET_BLOCKS_FALSE_MILESTONE',ev.length===0&&a.room.run.players[0].combo===1,{n3Count:ev.length,combo:a.room.run.players[0].combo},{n3Count:0,combo:1}));
  }catch(e){checks.push(pack('N3_RESET_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  const passed=checks.filter(x=>x.pass).length;
  return{ok:passed===checks.length,version:'0.39-cf.1-selftest',passed,total:checks.length,failed:checks.filter(x=>!x.pass).map(x=>x.name),checks};
}
