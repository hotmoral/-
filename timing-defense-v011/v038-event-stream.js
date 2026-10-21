// Timing Defense Cloudflare v0.38 — client event-stream bridge.
// Must load immediately after v033-cloudflare-bridge.js and before combat listeners.
(function(){
  const bridge=window.__TDCFBridge;
  if(!bridge)return;

  let activeRunId='',lastBatchTo=0,gap=null;
  window.__TD038EventStream={get runId(){return activeRunId},get lastBatchTo(){return lastBatchTo},get gap(){return gap}};

  function emitSynthetic(events,runId){
    const st=bridge.state;if(!st?.run||st.run.id!==runId)return;
    const synthetic={...st,run:{...st.run,events:[...events]}};
    window.dispatchEvent(new CustomEvent('tdcf:state',{detail:{state:synthetic,source:'v038-event-batch'}}));
  }
  function attach(ws){
    if(!ws||ws.__td038Attached)return;ws.__td038Attached=true;
    ws.addEventListener('message',ev=>{
      let d;try{d=JSON.parse(ev.data)}catch{return}
      if(d?.type==='event-batch'&&Array.isArray(d.events)){
        const from=Number(d.from)||0,to=Number(d.to)||0,runId=String(d.runId||'');
        if(!runId||to<from)return;
        if(activeRunId&&runId!==activeRunId){lastBatchTo=0;gap=null}
        activeRunId=runId;
        if(lastBatchTo&&from>lastBatchTo+1){
          gap={runId,expected:lastBatchTo+1,actual:from,at:Date.now()};
          window.dispatchEvent(new CustomEvent('tdcf:event-gap',{detail:gap}));
        }
        emitSynthetic(d.events,runId);
        lastBatchTo=Math.max(lastBatchTo,to);
        return;
      }
      if(d?.type==='event-gap'){
        gap={runId:String(d.runId||''),expected:Number(d.expected)||0,oldestId:Number(d.oldestId)||0,latestId:Number(d.latestId)||0,at:Date.now()};
        activeRunId=gap.runId||activeRunId;
        lastBatchTo=Math.max(lastBatchTo,gap.latestId||0);
        window.dispatchEvent(new CustomEvent('tdcf:event-gap',{detail:gap}));
      }
    });
  }

  // v033 emits tdcf:socket synchronously during construction, before its own message listener.
  window.addEventListener('tdcf:socket',e=>attach(e.detail?.socket));
  if(bridge.socket)attach(bridge.socket);

  window.addEventListener('tdcf:state',e=>{
    const run=e.detail?.state?.run;
    if(!run)return;
    if(activeRunId&&run.id!==activeRunId){activeRunId=run.id;lastBatchTo=0;gap=null}
    else if(!activeRunId)activeRunId=run.id;
  });
})();
