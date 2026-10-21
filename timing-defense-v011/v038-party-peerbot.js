// Timing Defense v0.38 candidate-only 4-human single-device smoke harness.
// Enabled only with ?partybot=3. The local browser remains the real player/host.
// Three additional HUMAN websocket sessions are created through the native WebSocket
// constructor so they never replace the local bridge/session/slot.
(function(){
  const params=new URL(location.href).searchParams;
  if(params.get('partybot')!=='3')return;
  const mp=window.__TDMP34CF,bridge=window.__TDCFBridge;
  if(!mp||!bridge)return;

  const configs=[
    {nickname:'SIM-A',classId:'archer',interval:1250,offset:0},
    {nickname:'SIM-M',classId:'mage',interval:1450,offset:280},
    {nickname:'SIM-T',classId:'tank',interval:1650,offset:560}
  ];
  let PeerWebSocket=null,joining=false,lastState=null;
  const bots=configs.map((cfg,i)=>({cfg,index:i,ws:null,session:'',slot:0,seq:0,state:null,shopReadyStage:0,lastAttackAt:-cfg.offset,joined:false}));

  const badge=document.createElement('div');
  badge.id='v038PartyBot';
  badge.style.cssText='position:fixed;left:50%;top:calc(env(safe-area-inset-top) + 5px);transform:translateX(-50%);z-index:151;padding:3px 7px;border:1px solid rgba(255,255,255,.14);border-radius:7px;background:rgba(7,12,15,.78);color:#aee8bd;font:800 8px system-ui;pointer-events:none;display:none';
  badge.textContent='SIM-HUMANS ×3';
  document.body.appendChild(badge);

  function nativeCtor(){
    if(PeerWebSocket)return PeerWebSocket;
    const c=bridge.socket?.constructor;
    if(c&&c!==window.WebSocket)PeerWebSocket=c;
    else if(c&&String(c).includes('[native code]'))PeerWebSocket=c;
    return PeerWebSocket;
  }
  function setBadge(st){
    const combat=st?.run?.status==='combat';
    badge.style.display=combat?'block':'none';
    if(combat){
      const active=bots.filter(b=>b.ws?.readyState===1).length;
      badge.textContent=`4H SMOKE · SIM ${active}/3`;
    }
  }
  function send(bot,payload){if(bot.ws?.readyState===1)try{bot.ws.send(JSON.stringify(payload))}catch(_){} }
  function botParticipant(bot,st=bot.state){return st?.participants?.find(p=>p.slot===bot.slot)||null}
  function botRunPlayer(bot,st=bot.state){return st?.run?.players?.find(p=>p.slot===bot.slot)||null}

  async function ensureShopReady(bot,st){
    const run=st?.run;
    if(!bot.session||run?.status!=='shop'||!run.shop)return;
    if(run.shop.readySlots?.includes(bot.slot))return;
    if(bot.shopReadyStage===run.stage)return;
    bot.shopReadyStage=run.stage;
    try{
      const r=await fetch(`/api/room/${st.code}/shop-ready`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session:bot.session,ready:true}),cache:'no-store'});
      if(!r.ok)throw new Error('HTTP '+r.status);
    }catch(_){bot.shopReadyStage=0}
  }

  function maybeAttack(bot,st){
    const run=st?.run;
    if(!run||run.status!=='combat'||!bot.slot)return;
    const now=performance.now();
    if(now-bot.lastAttackAt<bot.cfg.interval)return;
    const rp=botRunPlayer(bot,st);if(!rp)return;
    bot.lastAttackAt=now;
    const heavy=(rp.charge||0)>=3;
    send(bot,{type:'action',seq:++bot.seq,xJudge:bot.index===1?'PERFECT':'GOOD',yJudge:heavy?'GOOD':null});
  }

  function onBotState(bot,st){
    bot.state=st;lastState=st;setBadge(st);
    const p=botParticipant(bot,st);
    if(st?.status==='waiting'&&p&&!p.ready)send(bot,{type:'ready',ready:true});
    if(st?.run?.status==='shop')ensureShopReady(bot,st);
    maybeAttack(bot,st);
  }

  function wire(bot,sock){
    bot.ws=sock;
    sock.addEventListener('message',ev=>{
      let d;try{d=JSON.parse(ev.data)}catch(_){return}
      if(d.type==='welcome'){
        bot.session=d.session||bot.session;
        bot.slot=Number(d.slot)||bot.slot;
        bot.seq=Math.max(bot.seq,Number(d.lastSeq)||0);
        bot.joined=true;
        onBotState(bot,d.state);
      }else if(d.type==='state')onBotState(bot,d.state);
      else if(d.type==='error'&&d.error!=='stale-seq')console.warn('v038 partybot',bot.cfg.nickname,d.error);
    });
    sock.addEventListener('close',()=>{bot.ws=null;setBadge(lastState)});
    sock.addEventListener('error',()=>console.warn('v038 partybot socket error',bot.cfg.nickname));
  }

  function openBot(bot,code){
    if(bot.ws||bot.joined||!code)return false;
    const Ctor=nativeCtor();if(!Ctor)return false;
    const proto=location.protocol==='https:'?'wss:':'ws:';
    const u=new URL(`${proto}//${location.host}/ws/${code}`);
    u.searchParams.set('nickname',bot.cfg.nickname);
    u.searchParams.set('classId',bot.cfg.classId);
    wire(bot,new Ctor(u));
    return true;
  }

  async function joinAll(st){
    if(joining||!st?.code||st.status!=='waiting')return;
    if((st.participants?.length||0)!==1)return;
    joining=true;
    try{
      for(const bot of bots){
        openBot(bot,st.code);
        const start=performance.now();
        while(!bot.joined&&performance.now()-start<5000)await new Promise(r=>setTimeout(r,80));
        if(!bot.joined)throw new Error(`${bot.cfg.nickname}-join-timeout`);
        await new Promise(r=>setTimeout(r,120));
      }
    }catch(e){console.warn('v038 partybot join',e)}
    finally{joining=false}
  }

  function maybeJoin(st){
    lastState=st;setBadge(st);
    if(!bots.every(b=>b.joined))joinAll(st);
  }

  window.addEventListener('tdcf:welcome',e=>maybeJoin(e.detail?.state));
  window.addEventListener('tdcf:state',e=>maybeJoin(e.detail?.state));
  setInterval(()=>{for(const bot of bots)if(bot.state)maybeAttack(bot,bot.state)},220);
  if(bridge.state)maybeJoin(bridge.state);
  window.addEventListener('pagehide',()=>{for(const bot of bots)try{bot.ws?.close(1000,'partybot-pagehide')}catch(_){}});
})();
