// Timing Defense v0.43 — deterministic SPLITTER authoritative child-spawn tests.

function player(slot=1,level=5){return{slot,level,xp:0,xpNeed:60+12*(level-1),charge:0,combo:0,comboPeak:0,kills:0,coin:0,damage:0,lastSeq:0,nextPassiveAt:999999999,upgrades:{atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0},killCoinEarned:0}}
function parent(id=1,x=.70,y=.40,refAt=1000,hp=100000,extra={}){return{id,type:'splitter',x,y,refAt,hp,maxHp:hp,boss:false,canSplit:true,size:1,splitterGeneration:0,...extra}}
function child(id=1,x=.70,y=.40,refAt=1000,hp=120,extra={}){return{id,type:'splitter-child',parentId:9,splitterPackageId:'pkg',splitterChildIndex:0,splitterGeneration:1,canSplit:false,x,y,refAt,hp,maxHp:120,boss:false,size:.62,reward:2,...extra}}
function participant(cls='knight'){return{session:'s1',slot:1,nickname:'A',classId:cls,ready:true,connected:true,activeConnectionId:'c1',joinedAt:0,host:true}}
function actor(RoomClass,{cls='knight',level=5,monsters=null,stage=1,defRank=0,stageTarget=999,spawned=0,nextMonsterId=100}={}){const a=Object.create(RoomClass.prototype),p=player(1,level);p.upgrades.def=defRank;a.room={version:'v043-splitter-selftest',code:'SPL001',method:'friend',status:'running',createdAt:0,revision:0,startAt:null,hostSession:'s1',aiFill:[],participants:[participant(cls)],run:{id:`splitter-${cls}-${level}`,seed:1,rngState:123456789,status:'combat',startAt:0,combatAt:0,stage,stageTarget,spawned,nextSpawnAt:999999999,baseHp:2000,baseHpMax:2000,kills:0,nextMonsterId,monsters:monsters||[parent()],players:[p],ai:[],events:[],nextEventId:1,revision:0,shop:null,skillQueue:[],n3Queue:[]}};a.rng=()=>.99;return a}
function pack(name,pass,actual,expected){return{name,pass:!!pass,actual,expected}}

export function runV043SplitterSelfTest(RoomClass){
  const checks=[],eps=1e-9,at=1000;

  try{
    const a=actor(RoomClass,{monsters:[parent(1,.70,.40,at,100)]}),m=a.room.run.monsters[0],r=a.applyDamage(m,100,1,'NORMAL',at,true,'hit',false),kids=a.room.run.monsters;
    const pass=r.killed&&kids.length===2&&kids[0].id===100&&kids[1].id===101&&kids.every(x=>x.type==='splitter-child'&&x.parentId===1&&x.canSplit===false&&x.splitterGeneration===1)&&Math.abs(kids[0].y-.382)<eps&&Math.abs(kids[1].y-.418)<eps;
    checks.push(pack('SPLITTER_PARENT_DEATH_SPAWNS_EXACTLY_TWO',pass,{r,kids},{ids:[100,101],ys:[.382,.418],canSplit:[false,false]}));
  }catch(e){checks.push(pack('SPLITTER_SPAWN_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[parent(1,.70,.40,at,100)]});a.applyDamage(a.room.run.monsters[0],100,1,'NORMAL',at,true,'hit',false);const events=a.room.run.events,e=events.at(-1);
    checks.push(pack('SPLITTER_DAMAGE_EVENT_REMAINS_LAST_EVENT',events.length===1&&e.type==='hit'&&e.killed&&e.splitChildCount===2&&e.splitChildIds.join(',')==='100,101',{count:events.length,event:e},{count:1,type:'hit',childIds:[100,101]}));
  }catch(e){checks.push(pack('SPLITTER_EVENT_ORDER_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[parent(1,.70,.40,at,100)]});const p=a.room.participants[0];a.playerAction(p,{seq:1,xJudge:'NORMAL',yJudge:null},at);const e=a.room.run.events.find(x=>x.type==='hit'&&x.targetId===1);
    checks.push(pack('SPLITTER_PLAYER_ACTION_ANNOTATION_SURVIVES_SPLIT',e?.xpGain===8&&e?.charge===1&&e?.combo===0&&e?.splitChildCount===2,{event:e},{xpGain:8,charge:1,combo:0,splitChildCount:2}));
  }catch(e){checks.push(pack('SPLITTER_PLAYER_ACTION_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[child(10,.70,.40,at,120)]}),before=a.room.run.nextMonsterId,r=a.applyDamage(a.room.run.monsters[0],120,1,'NORMAL',at,true,'hit',false);
    checks.push(pack('SPLITTER_CHILD_NEVER_RECURSIVELY_SPLITS',r.killed&&a.room.run.monsters.length===0&&a.room.run.nextMonsterId===before&&r.splitChildIds.length===0,{r,nextMonsterId:a.room.run.nextMonsterId,monsters:a.room.run.monsters},{noChildren:true}));
  }catch(e){checks.push(pack('SPLITTER_CHILD_RECURSION_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[parent(1,.70,.40,at,100)]}),p=a.room.run.players[0];a.applyDamage(a.room.run.monsters[0],100,1,'NORMAL',at,true,'hit',false);for(const id of [100,101])a.applyDamage(a.room.run.monsters.find(m=>m.id===id),120,1,'NORMAL',at+10,true,'hit',false);
    checks.push(pack('SPLITTER_PROVISIONAL_PACKAGE_REWARD_TOTAL_8',p.coin===8&&p.killCoinEarned===8&&p.kills===3&&a.room.run.kills===3,{coin:p.coin,killCoin:p.killCoinEarned,kills:p.kills,runKills:a.room.run.kills},{packageReward:8,parent:4,children:[2,2],entityKills:3}));
  }catch(e){checks.push(pack('SPLITTER_REWARD_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[parent(1,.70,.40,at),child(2,.70,.45,at)]}),p=a.room.run.monsters[0],c=a.room.run.monsters[1],px=a.xAt(p,2000),cx=a.xAt(c,2000);
    checks.push(pack('SPLITTER_PARENT_CHILD_OWN_SPEEDS',Math.abs(px-.635)<eps&&Math.abs(cx-.585)<eps,{parent:px,child:cx},{parent:.635,child:.585}));
  }catch(e){checks.push(pack('SPLITTER_SPEED_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[parent(1,.20,.40,at),child(2,.20,.45,at)],defRank:4});const pHit=a.wallAt(a.room.run.monsters[0]);a.processAt(pHit);const pe=a.room.run.events.find(e=>e.type==='wall'&&e.targetId===1);const c=a.room.run.monsters.find(m=>m.id===2),cHit=a.wallAt(c);a.processAt(cHit);const ce=a.room.run.events.find(e=>e.type==='wall'&&e.targetId===2);
    checks.push(pack('SPLITTER_PARENT_CHILD_WALL_DAMAGE_IDENTITY',pe?.damage===90&&ce?.damage===36&&a.room.run.baseHp===1874,{parent:pe,child:ce,baseHp:a.room.run.baseHp},{parentDamage:90,childDamage:36,baseHp:1874}));
  }catch(e){checks.push(pack('SPLITTER_WALL_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[parent(1,.70,.38,at,100),parent(2,.70,.46,at,100)],nextMonsterId:100});const ids=[];
    for(const pid of [1,2]){const m=a.room.run.monsters.find(x=>x.id===pid),r=a.applyDamage(m,100,1,'NORMAL',at,true,'hit',false);ids.push(...r.splitChildIds)}
    const kids=a.room.run.monsters.filter(m=>m.type==='splitter-child');
    checks.push(pack('SPLITTER_SIMULTANEOUS_PARENT_DEATH_ID_ORDER',ids.join(',')==='100,101,102,103'&&kids.map(k=>k.parentId).join(',')==='1,1,2,2',{ids,parents:kids.map(k=>k.parentId)},{ids:[100,101,102,103],parents:[1,1,2,2]}));
  }catch(e){checks.push(pack('SPLITTER_SIMULTANEOUS_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[parent(1,.70,.40,at,100)],stageTarget:1,spawned:1});a.applyDamage(a.room.run.monsters[0],100,1,'NORMAL',at,true,'hit',false);const ended=a.checkEnd(at);
    checks.push(pack('SPLITTER_CHILDREN_BLOCK_PREMATURE_STAGE_CLEAR',ended===false&&a.room.run.status==='combat'&&a.room.run.monsters.length===2,{ended,status:a.room.run.status,count:a.room.run.monsters.length},{ended:false,status:'combat',count:2}));
  }catch(e){checks.push(pack('SPLITTER_CLEAR_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{cls:'rogue',level:6,monsters:[parent(1,.70,.40,at,30)]}),p=a.room.run.players[0];a.triggerN3(p,'rogue',5,'splitter-n3',at);a.advanceTo(at+55);const n3=a.room.run.events.filter(e=>e.type==='n3');
    checks.push(pack('SPLITTER_ROGUE_N3_RETARGETS_CHILD_DETERMINISTICALLY',n3.length===2&&n3[0].targetId===1&&n3[0].splitChildIds.join(',')==='100,101'&&n3[1].targetId===100,{n3:n3.map(e=>({targetId:e.targetId,children:e.splitChildIds,at:e.at}))},{targets:[1,100],children:[100,101]}));
  }catch(e){checks.push(pack('SPLITTER_N3_RETARGET_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{cls:'tank',level:6,monsters:[child(10,.70,.40,at,100000)]}),p=a.room.run.players[0],m=a.room.run.monsters[0],x=m.x;a.triggerN3(p,'tank',5,'splitter-tank',at);const dx=m.x-x,expected=.006*.82*(1+.30);
    checks.push(pack('SPLITTER_CHILD_N3_TANK_KNOCK_META',Math.abs(dx-expected)<eps,{dx,expected},{knockResist:.82,lv6Extra:.30}));
  }catch(e){checks.push(pack('SPLITTER_TANK_META_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[parent(1,.70,.40,at,100)]});a.applyDamage(a.room.run.monsters[0],100,1,'NORMAL',at,true,'hit',false);const saved=JSON.parse(JSON.stringify(a.room.run.monsters)),b=actor(RoomClass,{monsters:saved,nextMonsterId:a.room.run.nextMonsterId}),future=1800;
    const same=saved.every(m=>Math.abs(a.xAt(m,future)-b.xAt(m,future))<eps&&Math.abs(a.wallAt(m)-b.wallAt(m))<eps&&m.canSplit===false);
    checks.push(pack('SPLITTER_CHILD_RECONNECT_RECONSTRUCTION',same,{a:saved.map(m=>({id:m.id,x:a.xAt(m,future),wall:a.wallAt(m),canSplit:m.canSplit})),b:saved.map(m=>({id:m.id,x:b.xAt(m,future),wall:b.wallAt(m),canSplit:m.canSplit}))},{same:true,canSplit:false}));
  }catch(e){checks.push(pack('SPLITTER_RECONNECT_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[parent(1,.70,.40,at,100),parent(2,.72,.43,at,100)]});a.applyDamage(a.room.run.monsters[0],100,1,'NORMAL',at,true,'hit',false);const second=a.room.run.monsters.find(m=>m.id===2);a.applyDamage(second,100,1,'NORMAL',at,true,'hit',false);const ids=a.room.run.events.map(e=>e.id),strict=ids.every((id,i)=>i===0||id===ids[i-1]+1);
    checks.push(pack('SPLITTER_EVENT_IDS_REMAIN_MONOTONIC',strict&&ids.length===2,{ids,events:a.room.run.events.map(e=>({id:e.id,target:e.targetId,children:e.splitChildIds}))},{ids:[1,2]}));
  }catch(e){checks.push(pack('SPLITTER_EVENT_ID_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const a=actor(RoomClass,{monsters:[parent(1,.70,.40,at,100)]});a.applyDamage(a.room.run.monsters[0],100,1,'NORMAL',at,true,'hit',false);const snap=a.runPublic(at+100),kids=snap.monsters.filter(m=>m.type==='splitter-child');
    checks.push(pack('SPLITTER_PUBLIC_CHILD_METADATA',kids.length===2&&kids.every(m=>m.canSplit===false&&m.splitterGeneration===1&&m.size===.62&&m.parentId===1&&m.reward===2),kids.map(m=>({id:m.id,parentId:m.parentId,canSplit:m.canSplit,generation:m.splitterGeneration,size:m.size,reward:m.reward})),{count:2,parentId:1,canSplit:false,generation:1,size:.62,reward:2}));
  }catch(e){checks.push(pack('SPLITTER_PUBLIC_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  const passed=checks.filter(x=>x.pass).length;return{ok:passed===checks.length,version:'0.43-cf.1-splitter-selftest',passed,total:checks.length,failed:checks.filter(x=>!x.pass).map(x=>x.name),checks};
}
