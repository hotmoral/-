// Timing Defense v0.36 candidate-only simulated second human for single-device smoke.
// Enabled only with ?peerbot=1. Uses the real room WebSocket/API protocols.
(function(){
  const params=new URL(location.href).searchParams;
  if(params.get('peerbot')!=='1')return;
  const mp=window.__TDMP34CF,bridge=window.__TDCFBridge;
  if(!mp||!bridge)return;

  let ws=null,session='',slot=0,seq=0,state=null,joining=false,shopReadyStage=0,lastAttackAt=0;
  const cls=params.get('peerclass')||'archer';
  const nickname='SIM-PC';

  const badge=document.createElement('div');
  badge.id='v036PeerBot';
  badge.style.cssText='position:fixed;left:calc(env(safe-area-inset-left) + 8px);bottom:calc(env(safe-area-inset-bottom) + 8px);z-index:151;padding:6px 8px;border:1px solid rgba(255,255,255,.18);border-radius:8px;background:rgba(7,12,15,.9);color:#aee8bd;font:800 9px system-ui;pointer-events:none';
  badge.textContent='SIM-PC · WAIT';document.body.appendChild(badge);
  function status(s){badge.textContent='SIM-PC · '+s}
  function send(o){if(ws?.readyState===WebSocket.OPEN)ws.send(JSON.stringify(o))}
  function botParticipant(st=state){return st?.participants?.find(p=>p.slot===slot)||null}
  function botRunPlayer(st=state){return st?.run?.players?.find(p=>p.slot===slot)||null}

  async function ensureShopReady(st){
    const run=st?.run;if(!session||run?.status!=='shop'||!run.shop)return;
    if(run.shop.readySlots?.includes(slot)){status('SHOP READY');return}
    if(shopReadyStage===run.stage)return;
    shopReadyStage=run.stage;
    try{
      const r=await fetch(`/api/room/${st.code}/shop-ready`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session,ready:true}),cache:'no-store'});
      if(!r.ok)throw new Error('HTTP '+r.status);
      status('SHOP READY');
    }catch(e){shopReadyStage=0;status('SHOP RETRY')}
  }

  function maybeAttack(st){
    const run=st?.run;if(!run||run.status!=='combat'||!slot)return;
    const now=performance.now();if(now-lastAttackAt<1150)return;
    const rp=botRunPlayer(st);if(!rp)return;
    lastAttackAt=now;
    const heavy=(rp.charge||0)>=3;
    send({type:'action',seq:++seq,xJudge:'GOOD',yJudge:heavy?'GOOD':null});
    status('ATTACKING');
  }

  function onState(st){
    state=st;if(!st)return;
    const p=botParticipant(st);
    if(st.status==='waiting'&&p&&!p.ready){send({type:'ready',ready:true});status('READY')}
    if(st.run?.status==='shop')ensureShopReady(st);
    maybeAttack(st);
  }

  function openPeer(code){
    if(joining||ws||!code)return;joining=true;status('CONNECTING');
    const proto=location.protocol==='https:'?'wss:':'ws:';
    const u=new URL(`${proto}//${location.host}/ws/${code}`);
    u.searchParams.set('nickname',nickname);u.searchParams.set('classId',cls);
    ws=new WebSocket(u);
    ws.addEventListener('message',ev=>{
      let d;try{d=JSON.parse(ev.data)}catch(_){return}
      if(d.type==='welcome'){
        session=d.session||session;slot=d.slot||slot;seq=Math.max(seq,Number(d.lastSeq)||0);joining=false;status('JOINED');onState(d.state);
      }else if(d.type==='state')onState(d.state);
      else if(d.type==='action-result')seq=Math.max(seq,Number(d.result?.player?.lastSeq)||seq);
      else if(d.type==='error'&&d.error!=='stale-seq')status('ERR '+d.error);
    });
    ws.addEventListener('close',()=>{ws=null;joining=false;if(state?.status==='waiting'||state?.run&&!['stage2-clear','gameover'].includes(state.run.status)){status('RECONNECT');setTimeout(()=>openResume(code),700)}});
    ws.addEventListener('error',()=>status('SOCKET ERR'));
  }

  function openResume(code){
    if(joining||ws||!code||!session)return openPeer(code);
    joining=true;
    const proto=location.protocol==='https:'?'wss:':'ws:';
    const u=new URL(`${proto}//${location.host}/ws/${code}`);
    u.searchParams.set('session',session);u.searchParams.set('nickname',nickname);u.searchParams.set('classId',cls);
    ws=new WebSocket(u);
    ws.addEventListener('message',ev=>{let d;try{d=JSON.parse(ev.data)}catch(_){return}if(d.type==='welcome'){slot=d.slot||slot;seq=Math.max(seq,Number(d.lastSeq)||0);joining=false;status('REJOINED');onState(d.state)}else if(d.type==='state')onState(d.state)});
    ws.addEventListener('close',()=>{ws=null;joining=false});
  }

  function maybeJoin(st){
    if(!st?.code||st.status!=='waiting'||session||ws||joining)return;
    // Only inject the peer when the real local player is the sole human so we do not disturb normal tests.
    if((st.participants?.length||0)!==1)return status('SKIP · HUMANS '+(st.participants?.length||0));
    openPeer(st.code);
  }

  window.addEventListener('tdcf:welcome',e=>{const st=e.detail?.state;maybeJoin(st)});
  window.addEventListener('tdcf:state',e=>{const st=e.detail?.state;maybeJoin(st)});
  setInterval(()=>{if(state)maybeAttack(state)},250);
  if(bridge.state)maybeJoin(bridge.state);
  window.addEventListener('pagehide',()=>{try{ws?.close(1000,'peerbot-pagehide')}catch(_){}});
})();
