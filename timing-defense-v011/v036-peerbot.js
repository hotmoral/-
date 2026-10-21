// Timing Defense v0.36 candidate-only simulated second human for single-device smoke.
// Enabled only with ?peerbot=1. Uses the real room protocol but deliberately bypasses
// the v0.33 primary-socket wrapper so the simulated peer can never become the local player.
(function(){
  const params=new URL(location.href).searchParams;
  if(params.get('peerbot')!=='1')return;
  const mp=window.__TDMP34CF,bridge=window.__TDCFBridge;
  if(!mp||!bridge)return;

  let ws=null,session='',slot=0,seq=0,state=null,joining=false,shopReadyStage=0,lastAttackAt=0;
  let PeerWebSocket=null;
  const cls=params.get('peerclass')||'archer';
  const nickname='SIM-PC';

  const badge=document.createElement('div');
  badge.id='v036PeerBot';
  badge.style.cssText='position:fixed;left:50%;top:calc(env(safe-area-inset-top) + 5px);transform:translateX(-50%);z-index:151;padding:3px 7px;border:1px solid rgba(255,255,255,.14);border-radius:7px;background:rgba(7,12,15,.78);color:#aee8bd;font:800 8px system-ui;pointer-events:none;display:none';
  badge.textContent='SIM-PC';document.body.appendChild(badge);
  function status(s){badge.textContent='SIM-PC · '+s}
  function setBadgeForState(st){badge.style.display=st?.run?.status==='combat'?'block':'none'}
  function send(o){if(ws?.readyState===1)ws.send(JSON.stringify(o))}
  function botParticipant(st=state){return st?.participants?.find(p=>p.slot===slot)||null}
  function botRunPlayer(st=state){return st?.run?.players?.find(p=>p.slot===slot)||null}
  function nativeCtor(){
    // The primary socket returned by the bridge wrapper is a native WebSocket instance.
    // Its prototype constructor is therefore the original browser WebSocket constructor.
    // Using it directly prevents v033-cloudflare-bridge from replacing bridge.socket/session/slot.
    if(PeerWebSocket)return PeerWebSocket;
    const c=bridge.socket?.constructor;
    if(c&&c!==window.WebSocket)PeerWebSocket=c;
    else if(c&&String(c).includes('[native code]'))PeerWebSocket=c;
    return PeerWebSocket;
  }

  async function ensureShopReady(st){
    const run=st?.run;if(!session||run?.status!=='shop'||!run.shop)return;
    if(run.shop.readySlots?.includes(slot))return;
    if(shopReadyStage===run.stage)return;
    shopReadyStage=run.stage;
    try{
      const r=await fetch(`/api/room/${st.code}/shop-ready`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session,ready:true}),cache:'no-store'});
      if(!r.ok)throw new Error('HTTP '+r.status);
    }catch(e){shopReadyStage=0}
  }

  function maybeAttack(st){
    const run=st?.run;if(!run||run.status!=='combat'||!slot)return;
    const now=performance.now();if(now-lastAttackAt<1150)return;
    const rp=botRunPlayer(st);if(!rp)return;
    lastAttackAt=now;
    const heavy=(rp.charge||0)>=3;
    send({type:'action',seq:++seq,xJudge:'GOOD',yJudge:heavy?'GOOD':null});
    status('ATTACK');
  }

  function onState(st){
    state=st;if(!st)return;setBadgeForState(st);
    const p=botParticipant(st);
    if(st.status==='waiting'&&p&&!p.ready)send({type:'ready',ready:true});
    if(st.run?.status==='shop')ensureShopReady(st);
    maybeAttack(st);
  }

  function wirePeer(sock,code,resume){
    ws=sock;
    ws.addEventListener('message',ev=>{
      let d;try{d=JSON.parse(ev.data)}catch(_){return}
      if(d.type==='welcome'){
        session=d.session||session;slot=d.slot||slot;seq=Math.max(seq,Number(d.lastSeq)||0);joining=false;status(resume?'REJOINED':'JOINED');onState(d.state);
      }else if(d.type==='state')onState(d.state);
      else if(d.type==='error'&&d.error!=='stale-seq')status('ERR');
    });
    ws.addEventListener('close',()=>{
      ws=null;joining=false;
      if(state?.run&&!['stage2-clear','gameover'].includes(state.run.status)){setTimeout(()=>openResume(code),700)}
    });
    ws.addEventListener('error',()=>status('SOCKET ERR'));
  }

  function openPeer(code){
    if(joining||ws||!code)return;
    const Ctor=nativeCtor();if(!Ctor)return setTimeout(()=>openPeer(code),100);
    joining=true;
    const proto=location.protocol==='https:'?'wss:':'ws:';
    const u=new URL(`${proto}//${location.host}/ws/${code}`);
    u.searchParams.set('nickname',nickname);u.searchParams.set('classId',cls);
    wirePeer(new Ctor(u),code,false);
  }

  function openResume(code){
    if(joining||ws||!code||!session)return;
    const Ctor=nativeCtor();if(!Ctor)return setTimeout(()=>openResume(code),100);
    joining=true;
    const proto=location.protocol==='https:'?'wss:':'ws:';
    const u=new URL(`${proto}//${location.host}/ws/${code}`);
    u.searchParams.set('session',session);u.searchParams.set('nickname',nickname);u.searchParams.set('classId',cls);
    wirePeer(new Ctor(u),code,true);
  }

  function maybeJoin(st){
    if(!st?.code||st.status!=='waiting'||session||ws||joining)return;
    if((st.participants?.length||0)!==1)return;
    openPeer(st.code);
  }

  window.addEventListener('tdcf:welcome',e=>maybeJoin(e.detail?.state));
  window.addEventListener('tdcf:state',e=>{const st=e.detail?.state;setBadgeForState(st);maybeJoin(st)});
  setInterval(()=>{if(state)maybeAttack(state)},250);
  if(bridge.state)maybeJoin(bridge.state);
  window.addEventListener('pagehide',()=>{try{ws?.close(1000,'peerbot-pagehide')}catch(_){}});
})();
