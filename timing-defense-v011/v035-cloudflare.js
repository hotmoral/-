// Timing Defense Cloudflare v0.35 — durable reconnect + Team Shop + Stage 2 parity.
(function(){
  const bridge=window.__TDCFBridge,mp=window.__TDMP34CF;
  if(!bridge||!mp)return;

  const ACTIVE_KEY='td-cf035-active-session';
  const UPGRADE_META={
    atk:{name:'ATK',sub:'+8% damage / rank',mult:1.0},
    crit:{name:'CRIT',sub:'+2% proc chance / rank',mult:1.1},
    critdmg:{name:'CRIT DMG',sub:'+15% proc damage / rank',mult:1.0},
    hp:{name:'WALL HP',sub:'+100 max HP / rank',mult:.9},
    def:{name:'DEF',sub:'-2.5% wall damage / rank',mult:1.1},
    knock:{name:'KNOCKBACK',sub:'+10% / rank',mult:.9}
  };
  const BASE_COST=[40,65,100,145,200,265,340,425,520,625];
  let lastShopHtml='',resuming=false,resumeSocket=null,lastStageStatus='';

  const style=document.createElement('style');
  style.textContent=`
  #v035cfReconnect,#v035cfShop{position:fixed;inset:0;z-index:96;font-family:Inter,system-ui,sans-serif;color:#f6faf7}
  #v035cfReconnect{display:none;align-items:center;justify-content:center;background:rgba(5,9,8,.90)}
  #v035cfReconnect.show{display:flex}
  .v035cfCard{width:min(430px,84vw);padding:20px 22px;border-radius:18px;border:1px solid rgba(255,255,255,.13);background:#172621;box-shadow:0 22px 70px rgba(0,0,0,.42);text-align:center}
  .v035cfRT{font:1000 19px system-ui}.v035cfRS{margin-top:7px;font:750 9px/1.5 system-ui;color:#9fb0a7}.v035cfRB{margin-top:13px;padding:8px 13px;border-radius:9px;border:1px solid rgba(255,255,255,.14);background:#efe0ac;color:#17201b;font:950 9px system-ui}
  #v035cfShop{display:none;background:linear-gradient(145deg,#172621 0%,#263b31 46%,#18251f 100%);padding:13px 18px 12px;box-sizing:border-box}
  #v035cfShop.show{display:block}
  .v035cfTop{height:40px;display:flex;align-items:flex-start;justify-content:space-between}.v035cfBrand{font:1000 15px system-ui;letter-spacing:.1em}.v035cfStage{font:950 9px system-ui;color:#f0d98c;padding:6px 10px;border:1px solid rgba(240,217,140,.24);border-radius:999px}
  .v035cfBody{height:calc(100% - 84px);display:grid;grid-template-columns:66% 34%;gap:10px;min-height:0}.v035cfPanel{border:1px solid rgba(255,255,255,.10);background:rgba(6,11,9,.37);border-radius:17px;padding:11px 12px;box-sizing:border-box;min-height:0;overflow:hidden}
  .v035cfTitle{font:1000 17px system-ui}.v035cfSub{font:750 8px/1.4 system-ui;color:#9fb0a7;margin-top:3px}.v035cfCoin{margin-top:8px;font:1000 13px system-ui;color:#f3df9b}
  .v035cfGrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin-top:9px}.v035cfUpgrade{border:1px solid rgba(255,255,255,.09);background:rgba(0,0,0,.18);border-radius:11px;padding:7px;min-width:0}.v035cfUN{font:950 9px system-ui;white-space:nowrap}.v035cfUS{font:700 7px/1.25 system-ui;color:#96a59d;min-height:18px;margin-top:2px}.v035cfUF{display:flex;align-items:center;justify-content:space-between;margin-top:5px;gap:4px}.v035cfRank{font:900 8px system-ui;color:#cbd7d1}
  .v035cfBuy{border:1px solid rgba(255,255,255,.12);background:#142019;color:#d8e1dc;border-radius:7px;padding:5px 7px;font:900 7.5px system-ui;white-space:nowrap}.v035cfBuy:not(:disabled){background:#efe0ac;color:#17201b;border-color:#efe0ac}.v035cfBuy:disabled{opacity:.38}
  .v035cfReadyTitle{font:1000 12px system-ui;letter-spacing:.05em}.v035cfPeople{display:flex;flex-direction:column;gap:7px;margin-top:9px}.v035cfPerson{display:flex;align-items:center;justify-content:space-between;padding:8px 9px;border:1px solid rgba(255,255,255,.08);border-radius:10px;background:rgba(255,255,255,.025)}.v035cfPN{font:900 9px system-ui}.v035cfPC{font:750 7px system-ui;color:#9eaaa4;margin-top:2px}.v035cfPS{font:1000 8px system-ui;color:#82938b}.v035cfPS.ready{color:#8ce2aa}
  .v035cfNote{margin-top:9px;padding:7px 8px;border-radius:9px;background:rgba(0,0,0,.18);font:700 7px/1.4 system-ui;color:#9fb0a7}.v035cfFoot{height:44px;display:flex;align-items:flex-end;justify-content:space-between;gap:8px}.v035cfAction{padding:8px 13px;border-radius:9px;border:1px solid rgba(255,255,255,.13);background:#121b17;color:#dce6df;font:950 9px system-ui}.v035cfAction.primary{background:#efe0ac;color:#17201b;border-color:#efe0ac}.v035cfAction:disabled{opacity:.35}.v035cfFootStatus{font:800 7px system-ui;color:#9eaaa4;text-align:center;flex:1}
  @media(max-height:590px){#v035cfShop{padding:8px 14px 7px}.v035cfTop{height:31px}.v035cfBody{height:calc(100% - 68px);gap:7px}.v035cfPanel{padding:7px 8px}.v035cfTitle{font-size:14px}.v035cfSub{font-size:6.8px}.v035cfCoin{margin-top:4px;font-size:11px}.v035cfGrid{gap:4px;margin-top:5px}.v035cfUpgrade{padding:5px}.v035cfUN{font-size:7.8px}.v035cfUS{font-size:6.1px;min-height:14px}.v035cfBuy{padding:4px 5px;font-size:6.5px}.v035cfPeople{gap:4px;margin-top:6px}.v035cfPerson{padding:5px 6px}.v035cfNote{margin-top:5px;padding:5px 6px;font-size:6.1px}.v035cfFoot{height:36px}.v035cfAction{padding:6px 10px;font-size:7.5px}}
  `;
  document.head.appendChild(style);

  const reconnect=document.createElement('div');
  reconnect.id='v035cfReconnect';
  reconnect.innerHTML='<div class="v035cfCard"><div class="v035cfRT">RUN RECOVERY</div><div id="v035cfRS" class="v035cfRS">Durable Object의 현재 상태를 복구하는 중입니다.</div><button id="v035cfRB" class="v035cfRB" style="display:none">새로 시작하기</button></div>';
  document.body.appendChild(reconnect);

  const shop=document.createElement('div');shop.id='v035cfShop';document.body.appendChild(shop);

  function roomFromUrl(){return(new URL(location.href)).searchParams.get('room')?.toUpperCase()||''}
  function readActive(){try{return JSON.parse(localStorage.getItem(ACTIVE_KEY)||'null')}catch(_){return null}}
  function writeActive(st=mp.state){
    const run=st?.run,session=bridge.session||mp.session,slot=bridge.slot||mp.slot;
    if(!st?.code||!run||!session||!slot)return;
    try{localStorage.setItem(ACTIVE_KEY,JSON.stringify({room:st.code,session,slot,runId:run.id,at:Date.now()}))}catch(_){}
  }
  function clearActive(){try{localStorage.removeItem(ACTIVE_KEY)}catch(_){} }
  function esc(s){return String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}
  function clsName(c){return c==='knight'?'KNIGHT':c==='rogue'?'ROGUE':c==='tank'?'TANK':c==='archer'?'ARCHER':'MAGE'}
  function localPlayer(run){return run?.players?.find(p=>p.slot===(bridge.slot||mp.slot))}
  function localParticipant(st=mp.state){return st?.participants?.find(p=>p.slot===(bridge.slot||mp.slot))}
  function isHost(){return !!localParticipant()?.host}
  function costFor(player,key){
    const rank=player?.upgrades?.[key]||0;
    if(rank>=10)return Infinity;
    return Math.round(BASE_COST[rank]*UPGRADE_META[key].mult);
  }

  async function post(action,payload={}){
    const st=mp.state,session=bridge.session||mp.session;
    if(!st?.code||!session)throw new Error('network-not-ready');
    const r=await fetch(`/api/room/${st.code}/${action}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session,...payload}),cache:'no-store'});
    const d=await r.json().catch(()=>null);
    if(!r.ok)throw new Error(d?.error||`HTTP ${r.status}`);
    if(Number.isFinite(d?.eventFloor))mp.lastEvent=Math.max(mp.lastEvent||0,d.eventFloor);
    if(d?.state)pushState(d.state,'v035-http');
    return d;
  }
  function pushState(st,source){
    if(!st)return;
    bridge.state=st;
    window.dispatchEvent(new CustomEvent('tdcf:state',{detail:{state:st,source}}));
  }

  async function buy(key){try{await post('shop-buy',{key})}catch(e){console.warn('v035 shop buy',e)}}
  async function toggleReady(){
    const run=mp.state?.run;if(!run?.shop)return;
    const ready=(run.shop.readySlots||[]).includes(bridge.slot||mp.slot);
    try{await post('shop-ready',{ready:!ready})}catch(e){console.warn('v035 shop ready',e)}
  }
  async function nextStage(){try{await post('shop-next')}catch(e){console.warn('v035 shop next',e)}}

  function syncLocalProgress(run){
    const p=localPlayer(run);if(!p)return;
    S.gold=p.coin??S.gold;
    if(p.upgrades)S.upgrades={...S.upgrades,...p.upgrades};
  }

  function renderShop(run){
    const local=localPlayer(run);if(!local)return;
    const readySlots=new Set(run.shop?.readySlots||[]),slot=bridge.slot||mp.slot,ready=readySlots.has(slot),host=isHost();
    const people=(mp.state?.participants||[]).map(p=>{
      const rp=run.players?.find(x=>x.slot===p.slot),r=readySlots.has(p.slot);
      return `<div class="v035cfPerson"><div><div class="v035cfPN">${esc(p.nickname)}${p.host?' · HOST':''}</div><div class="v035cfPC">${esc(clsName(p.classId))} · COIN ${rp?.coin??0}</div></div><div class="v035cfPS ${r?'ready':''}">${r?'READY ✓':'SHOPPING'}</div></div>`;
    }).join('');
    const cards=Object.entries(UPGRADE_META).map(([key,m])=>{
      const rank=local.upgrades?.[key]||0,cost=costFor(local,key),disabled=ready||rank>=10||local.coin<cost;
      return `<div class="v035cfUpgrade"><div class="v035cfUN">${m.name}</div><div class="v035cfUS">${m.sub}</div><div class="v035cfUF"><span class="v035cfRank">R${rank}</span><button class="v035cfBuy" data-buy="${key}" ${disabled?'disabled':''}>${rank>=10?'MAX':`${cost} C`}</button></div></div>`;
    }).join('');
    const html=`<div class="v035cfTop"><div class="v035cfBrand">TIMING DEFENSE</div><div class="v035cfStage">STAGE ${run.shop.stage} CLEAR</div></div>
    <div class="v035cfBody"><section class="v035cfPanel"><div class="v035cfTitle">TEAM SHOP</div><div class="v035cfSub">개인 코인으로 업그레이드를 구매합니다. READY 후에는 구매가 잠깁니다.</div><div class="v035cfCoin">COIN ${local.coin}</div><div class="v035cfGrid">${cards}</div></section>
    <section class="v035cfPanel"><div class="v035cfReadyTitle">NEXT STAGE READY</div><div class="v035cfPeople">${people}</div><div class="v035cfNote">모든 사람 플레이어가 READY가 되면 방장의 NEXT STAGE가 활성화됩니다. WALL HP/DEF는 현재 공용 본진에 서버 기준으로 반영되는 프로토타입 규칙입니다.</div></section></div>
    <div class="v035cfFoot"><button id="v035cfReady" class="v035cfAction ${ready?'':'primary'}">${ready?'READY ✓ · 수정하기':'READY'}</button><div class="v035cfFootStatus">${run.shop.canNext?'모든 플레이어 준비 완료':'다른 플레이어의 준비를 기다리는 중'}</div><button id="v035cfNext" class="v035cfAction ${host&&run.shop.canNext?'primary':''}" ${host&&run.shop.canNext?'':'disabled'}>NEXT STAGE →</button></div>`;
    if(html!==lastShopHtml){
      shop.innerHTML=html;lastShopHtml=html;
      shop.querySelectorAll('[data-buy]').forEach(b=>b.addEventListener('click',()=>buy(b.dataset.buy)));
      shop.querySelector('#v035cfReady')?.addEventListener('click',toggleReady);
      shop.querySelector('#v035cfNext')?.addEventListener('click',nextStage);
    }
  }

  function enterStagePresentation(run){
    if(run.stage!==2)return;
    if(run.status==='stage-starting'){
      if(lastStageStatus!=='stage-starting'){
        S.stage=2;S.stageMode='netStageWait';S.phase='idle';S.pendingTap=false;S.projectiles=[];mp.remoteShots.length=0;
        S.resultText='STAGE 2';S.resultTier='GOOD';S.resultUntil=performance.now()+900;
      }
    }else if(run.status==='intro'){
      S.stage=2;S.stageMode='netStageWait';S.phase='idle';
    }else if(run.status==='combat'&&lastStageStatus!=='combat'){
      S.stage=2;S.stageMode='combat';S.gameOver=false;S.runComplete=false;S.pendingTap=false;
      if(typeof startAttack==='function')startAttack(performance.now());
    }
  }

  function handleState(st){
    if(!st?.run)return;
    writeActive(st);syncLocalProgress(st.run);
    const run=st.run;
    if(run.status==='shop'){
      if(!shop.classList.contains('show')){
        S.stageMode='netshop';S.phase='idle';S.pendingTap=false;S.projectiles=[];mp.remoteShots.length=0;
        shop.classList.add('show');
      }
      renderShop(run);
    }else{
      if(shop.classList.contains('show')){shop.classList.remove('show');lastShopHtml=''}
      enterStagePresentation(run);
      if(run.status==='stage2-clear'){
        S.stage=2;S.stageMode='clear';S.phase='idle';S.runComplete=true;S.resultText='STAGE 2 SYNC CLEAR';S.resultTier='CRITICAL';S.resultUntil=performance.now()+999999;clearActive();
      }
      if(run.status==='gameover')clearActive();
    }
    lastStageStatus=run.status;
  }

  function openResumeSocket(room,session,slot,state){
    const p=state?.participants?.find(x=>x.slot===slot);
    if(!p)throw new Error('resume-participant-missing');
    const proto=location.protocol==='https:'?'wss:':'ws:',u=new URL(`${proto}//${location.host}/ws/${room}`);
    u.searchParams.set('session',session);u.searchParams.set('nickname',p.nickname||'PLAYER');u.searchParams.set('classId',p.classId||'knight');
    try{resumeSocket?.close()}catch(_){}
    const ws=new WebSocket(u);resumeSocket=ws;
    ws.addEventListener('open',()=>{reconnect.classList.remove('show');resuming=false});
    ws.addEventListener('close',()=>{if(resumeSocket===ws&&mp.state?.run&&!['stage2-clear','gameover'].includes(mp.state.run.status)){setTimeout(()=>{if(resumeSocket===ws)openResumeSocket(room,session,slot,mp.state)},800)}});
  }

  async function tryResume(){
    if(resuming)return;
    const rec=readActive(),room=roomFromUrl();
    if(!rec?.session||!rec?.runId||!rec?.slot||!room||rec.room!==room)return;
    resuming=true;reconnect.classList.add('show');
    const sub=reconnect.querySelector('#v035cfRS'),btn=reconnect.querySelector('#v035cfRB');
    btn.style.display='none';sub.textContent='Durable Object의 현재 전투 상태를 복구하는 중입니다.';
    try{
      const r=await fetch(`/api/room/${room}/resume`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session:rec.session}),cache:'no-store'});
      const d=await r.json().catch(()=>null);
      if(!r.ok)throw new Error(d?.error||`HTTP ${r.status}`);
      bridge.session=d.session;bridge.slot=d.slot;bridge.lastSeq=Math.max(Number(bridge.lastSeq)||0,Number(d.lastSeq)||0);
      mp.session=d.session;mp.slot=d.slot;mp.seq=Math.max(mp.seq||0,Number(d.lastSeq)||0);mp.lastEvent=Math.max(mp.lastEvent||0,Number(d.eventFloor)||0);
      bridge.state=d.state;mp.state=d.state;pushState(d.state,'v035-resume');
      openResumeSocket(room,d.session,d.slot,d.state);
    }catch(e){
      sub.textContent=`복구 실패: ${e.message}`;btn.style.display='inline-block';resuming=false;
    }
  }

  reconnect.querySelector('#v035cfRB')?.addEventListener('click',()=>{clearActive();location.href=location.origin+'/'});

  window.addEventListener('tdcf:welcome',e=>{if(e.detail?.state)handleState(e.detail.state)});
  window.addEventListener('tdcf:state',e=>{if(e.detail?.state)handleState(e.detail.state)});

  if(bridge.state?.run)handleState(bridge.state);
  setTimeout(tryResume,0);
})();