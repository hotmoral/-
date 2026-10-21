import baseWorker, { TimingDefenseRoom } from "./v037-entry.js";

// Timing Defense Cloudflare v0.38 Slice C foundation.
// N3 is NOT enabled here. This patch hardens multiplayer event delivery first.
const EVENT_HISTORY_LIMIT=512;

function json(data,status=200){
  return new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}});
}
function streamMeta(run){
  if(!run)return{oldestId:0,latestId:0,retained:0,historyLimit:EVENT_HISTORY_LIMIT};
  const events=Array.isArray(run.events)?run.events:[];
  const next=Number.isFinite(Number(run.nextEventId))?Number(run.nextEventId):((events.at(-1)?.id||0)+1);
  return{
    oldestId:events.length?(Number(events[0].id)||0):Math.max(0,next-1),
    latestId:Math.max(0,next-1),
    retained:events.length,
    historyLimit:EVENT_HISTORY_LIMIT
  };
}

// Replace the legacy 48-event ring with a larger authoritative history.
// IDs remain strictly monotonic within a run. The normalization is intentional:
// production runs already initialize events/nextEventId, while deterministic
// regression harnesses may construct a minimal run without those fields.
TimingDefenseRoom.prototype.event=function(data,at){
  const run=this.room?.run;
  if(!run)return null;
  if(!Array.isArray(run.events))run.events=[];
  if(!Number.isFinite(Number(run.nextEventId))){
    const lastId=Number(run.events.at(-1)?.id)||0;
    run.nextEventId=lastId+1;
  }
  const event={id:run.nextEventId++,...data,at};
  run.events.push(event);
  if(run.events.length>EVENT_HISTORY_LIMIT)run.events.splice(0,run.events.length-EVENT_HISTORY_LIMIT);
  return event;
};

const baseRunPublic=TimingDefenseRoom.prototype.runPublic;
TimingDefenseRoom.prototype.runPublic=function(at){
  const out=baseRunPublic.call(this,at),run=this.room?.run;
  if(out&&run)out.eventStream=streamMeta(run);
  return out;
};

function saveAttachment(ws,att){
  try{ws.serializeAttachment(att)}catch(_){}
}
function sendJson(ws,payload){
  try{ws.send(JSON.stringify(payload));return true}catch(_){return false}
}

// State broadcasts no longer depend on the legacy public `events.slice(-24)` tail.
// Every accepted socket gets its own monotonic event cursor in the hibernation attachment.
TimingDefenseRoom.prototype.broadcastState=function(at=Date.now()){
  const sockets=this.ctx?.getWebSockets?.()||[],run=this.room?.run||null;
  const state=this.publicState(at);
  if(state?.run)state.run={...state.run,events:[]};
  const meta=streamMeta(run),latest=meta.latestId,oldest=meta.oldestId,runId=run?.id||"";

  for(const ws of sockets){
    const att={...(ws.deserializeAttachment?.()||{})};
    const hasStreamIdentity=Object.prototype.hasOwnProperty.call(att,"eventRunId");

    if(!run){
      att.eventRunId="";att.eventCursor=0;saveAttachment(ws,att);
      sendJson(ws,{type:"state",state});
      continue;
    }

    // A socket that existed before this run starts at event 0.
    // A newly-created socket in an already-running run is a reconnect and starts at latest;
    // resume/eventFloor already reconciles gameplay state and prevents historical VFX replay.
    if(!hasStreamIdentity){
      att.eventRunId=runId;att.eventCursor=latest;saveAttachment(ws,att);
    }else if(att.eventRunId!==runId){
      att.eventRunId=runId;att.eventCursor=0;saveAttachment(ws,att);
    }

    let cursor=Math.max(0,Number(att.eventCursor)||0);
    if(cursor<latest){
      const available=(run.events||[]).filter(e=>(Number(e.id)||0)>cursor);
      const first=available[0]?.id??null;
      if(!available.length||first>cursor+1){
        sendJson(ws,{type:"event-gap",runId,expected:cursor+1,oldestId:oldest,latestId:latest});
        // Explicitly advance after declaring the gap. Never silently pretend continuity.
        cursor=latest;
      }else{
        const ok=sendJson(ws,{type:"event-batch",runId,from:available[0].id,to:available[available.length-1].id,events:available});
        if(ok)cursor=available[available.length-1].id;
      }
      att.eventCursor=cursor;saveAttachment(ws,att);
    }

    sendJson(ws,{type:"state",state});
  }
};

const worker={
  async fetch(request,env,ctx){
    const url=new URL(request.url);
    if(request.method==="GET"&&url.pathname==="/api/health"){
      return json({
        ok:true,
        service:"timing-defense-cloudflare-v038-party-event-kernel",
        version:"0.38-cf.2",
        transport:"websocket-hibernation-per-socket-event-cursor",
        authority:"durable-object-stage1-stage3-lv6",
        eventDelivery:{history:EVENT_HISTORY_LIMIT,mode:"per-socket-monotonic-batch",gap:"explicit"},
        n3:"option-b-frozen-not-yet-enabled",
        stage4:"blocked",
        scope:"slice-c-event-kernel-larger-party-validation",
        fix:"event-initialization-normalization"
      });
    }
    if(request.method==="GET"&&url.pathname==="/"){
      const assetUrl=new URL(request.url);assetUrl.pathname="/v038-cloudflare.html";
      return env.ASSETS.fetch(new Request(assetUrl,request));
    }
    return baseWorker.fetch(request,env,ctx);
  }
};

export default worker;
export { TimingDefenseRoom, EVENT_HISTORY_LIMIT };
