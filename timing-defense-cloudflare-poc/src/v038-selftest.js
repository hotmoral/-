// Timing Defense v0.38 Slice C event-kernel deterministic self-test.

function fakeSocket(att={}){
  let attachment={...att};
  const sent=[];
  return{
    sent,
    deserializeAttachment(){return{...attachment}},
    serializeAttachment(v){attachment={...v}},
    send(text){sent.push(JSON.parse(text))},
    attachment(){return{...attachment}}
  };
}
function actor(RoomClass,events=[],nextEventId=null,sockets=[]){
  const a=Object.create(RoomClass.prototype);
  const run={id:'RUN038',events:[...events],nextEventId:nextEventId??((events.at(-1)?.id||0)+1),stage:1,status:'combat'};
  a.room={code:'T38001',run};
  a.ctx={getWebSockets:()=>sockets};
  a.publicState=()=>({code:'T38001',run:{id:run.id,stage:1,status:'combat',events:run.events.slice(-24)}});
  return a;
}
function pack(name,pass,actual,expected){return{name,pass:!!pass,actual,expected}}

export function runV038SelfTest(RoomClass){
  const checks=[];
  try{
    const a=actor(RoomClass,[],1,[]);
    for(let i=1;i<=600;i++)a.event({type:'diag',n:i},1000+i);
    const ev=a.room.run.events;
    checks.push(pack('EVENT_HISTORY_512_MONOTONIC',ev.length===512&&ev[0].id===89&&ev.at(-1).id===600&&a.room.run.nextEventId===601,{length:ev.length,first:ev[0]?.id,last:ev.at(-1)?.id,next:a.room.run.nextEventId},{length:512,first:89,last:600,next:601}));
  }catch(e){checks.push(pack('EVENT_HISTORY_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const events=Array.from({length:32},(_,i)=>({id:i+1,type:'stress',at:1000+i}));
    const ws=fakeSocket({session:'s1',slot:1,connectionId:'c1',eventRunId:'RUN038',eventCursor:0});
    const a=actor(RoomClass,events,33,[ws]);
    a.broadcastState(2000);
    const batch=ws.sent.find(x=>x.type==='event-batch'),state=ws.sent.find(x=>x.type==='state');
    checks.push(pack('BURST_OVER_24_DELIVERED_WHOLE',batch?.from===1&&batch?.to===32&&batch?.events?.length===32&&state?.state?.run?.events?.length===0,{from:batch?.from,to:batch?.to,count:batch?.events?.length,stateEvents:state?.state?.run?.events?.length},{from:1,to:32,count:32,stateEvents:0}));
    checks.push(pack('CURSOR_ADVANCES_AFTER_BATCH',ws.attachment().eventCursor===32,ws.attachment(),{eventCursor:32}));
  }catch(e){checks.push(pack('BURST_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const events=Array.from({length:10},(_,i)=>({id:101+i,type:'late',at:2000+i}));
    const ws=fakeSocket({session:'s1',slot:1,connectionId:'c1',eventRunId:'RUN038',eventCursor:90});
    const a=actor(RoomClass,events,111,[ws]);
    a.broadcastState(3000);
    const gap=ws.sent.find(x=>x.type==='event-gap');
    checks.push(pack('RETENTION_GAP_EXPLICIT',gap?.expected===91&&gap?.oldestId===101&&gap?.latestId===110,{gap,cursor:ws.attachment().eventCursor},{expected:91,oldestId:101,latestId:110,cursor:110}));
  }catch(e){checks.push(pack('GAP_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const events=[{id:1,type:'x',at:1},{id:2,type:'x',at:2}];
    const waiting=fakeSocket({session:'s1',slot:1,connectionId:'c1',eventRunId:'',eventCursor:0});
    const a=actor(RoomClass,events,3,[waiting]);
    a.broadcastState(100);
    const batch=waiting.sent.find(x=>x.type==='event-batch');
    checks.push(pack('PRE_RUN_SOCKET_RECEIVES_NEW_RUN_FROM_ZERO',batch?.from===1&&batch?.to===2&&waiting.attachment().eventRunId==='RUN038',{batch,att:waiting.attachment()},{from:1,to:2,runId:'RUN038'}));
  }catch(e){checks.push(pack('PRE_RUN_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const events=Array.from({length:5},(_,i)=>({id:i+1,type:'old',at:i}));
    const reconnect=fakeSocket({session:'s1',slot:1,connectionId:'c2'});
    const a=actor(RoomClass,events,6,[reconnect]);
    a.broadcastState(100);
    const batch=reconnect.sent.find(x=>x.type==='event-batch');
    checks.push(pack('RECONNECT_SOCKET_FLOORS_AT_LATEST',!batch&&reconnect.attachment().eventCursor===5&&reconnect.attachment().eventRunId==='RUN038',{batch:!!batch,att:reconnect.attachment()},{batch:false,eventCursor:5,runId:'RUN038'}));
  }catch(e){checks.push(pack('RECONNECT_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  try{
    const events=[{id:1,type:'x',at:1},{id:2,type:'x',at:2},{id:3,type:'x',at:3}];
    const aWs=fakeSocket({eventRunId:'RUN038',eventCursor:1}),bWs=fakeSocket({eventRunId:'RUN038',eventCursor:2}),cWs=fakeSocket({eventRunId:'RUN038',eventCursor:3});
    const a=actor(RoomClass,events,4,[aWs,bWs,cWs]);
    a.broadcastState(100);
    const ba=aWs.sent.find(x=>x.type==='event-batch'),bb=bWs.sent.find(x=>x.type==='event-batch'),bc=cWs.sent.find(x=>x.type==='event-batch');
    checks.push(pack('PER_SOCKET_INDEPENDENT_CURSORS',ba?.events?.map(e=>e.id).join(',')==='2,3'&&bb?.events?.map(e=>e.id).join(',')==='3'&&!bc,{a:ba?.events?.map(e=>e.id),b:bb?.events?.map(e=>e.id),c:bc?.events?.map(e=>e.id)},{a:[2,3],b:[3],c:[]}));
  }catch(e){checks.push(pack('CURSOR_EXCEPTION',false,String(e?.stack||e),'no exception'))}

  const passed=checks.filter(x=>x.pass).length;
  return{ok:passed===checks.length,version:'0.38-cf.2-selftest',passed,total:checks.length,failed:checks.filter(x=>!x.pass).map(x=>x.name),checks};
}
