// Timing Defense v0.39 candidate-only Samsung Browser N3 smoke helper.
// Enabled only with ?n3smoke=1. It never changes normal-game behavior.
(function(){
  const params=new URL(location.href).searchParams;
  if(params.get('n3smoke')!=='1')return;
  const bridge=window.__TDCFBridge;
  if(!bridge)return;

  let armedRunId='',armingRunId='',doneRunId='';
  const badge=document.createElement('div');
  badge.id='v039N3SmokeBadge';
  badge.style.cssText='position:fixed;left:50%;top:calc(env(safe-area-inset-top) + 5px);transform:translateX(-50%);z-index:154;padding:4px 8px;border:1px solid rgba(255,255,255,.16);border-radius:8px;background:rgba(7,12,15,.82);color:#d8f3df;font:800 9px system-ui;pointer-events:none;display:none;white-space:nowrap';
  badge.textContent='N3 SMOKE';
  document.body.appendChild(badge);

  function localParticipant(st){return st?.participants?.find(p=>p.slot===bridge.slot)||null}
  function localRunPlayer(st){return st?.run?.players?.find(p=>p.slot===bridge.slot)||null}
  function setBadge(st){
    const run=st?.run,id=run?.id||'';
    if(run?.status!=='combat'){badge.style.display='none';return}
    badge.style.display='block';
    if(doneRunId===id)badge.textContent='N3 FIRED · 화면 확인';
    else if(armedRunId===id)badge.textContent='N3 ARMED · PERFECT 1회';
    else if(armingRunId===id)badge.textContent='N3 ARMING…';
    else badge.textContent='N3 SMOKE · 준비 중';
  }

  async function arm(st){
    const run=st?.run,id=run?.id||'';
    if(!id||run.status!=='combat'||!(run.monsters?.length>0))return;
    if(armedRunId===id||armingRunId===id||doneRunId===id)return;
    const p=localParticipant(st);
    if(!p?.host||!bridge.session||!st.code)return;
    armingRunId=id;setBadge(st);
    try{
      const r=await fetch(`/api/room/${st.code}/debug-n3-arm`,{
        method:'POST',headers:{'Content-Type':'application/json'},cache:'no-store',
        body:JSON.stringify({session:bridge.session,combo:29,level:6})
      });
      const d=await r.json().catch(()=>null);
      if(!r.ok)throw new Error(d?.error||`HTTP ${r.status}`);
      armedRunId=id;
    }catch(_){
      armedRunId='';
    }finally{
      armingRunId='';setBadge(bridge.state||st);
    }
  }

  function observeN3(st){
    const run=st?.run,id=run?.id||'';
    if(!id)return;
    const events=run.events||[];
    if(events.some(e=>e?.type==='n3'&&e?.slot===bridge.slot)){
      doneRunId=id;armedRunId='';
    }
    // If the user misses the armed PERFECT, authoritative combo drops below 29.
    // Re-arm automatically so the visual smoke can be retried without restarting the room.
    const rp=localRunPlayer(st);
    if(doneRunId!==id&&armedRunId===id&&rp&&Number(rp.combo)<29)armedRunId='';
    setBadge(st);arm(st);
  }

  window.addEventListener('tdcf:state',e=>observeN3(e.detail?.state));
  window.addEventListener('tdcf:welcome',e=>observeN3(e.detail?.state));
  if(bridge.state)observeN3(bridge.state);
})();
