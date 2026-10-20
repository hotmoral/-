// Timing Defense v0.35 — reconnect recovery + authoritative team shop + Stage 2 handoff.
// Loaded after v0.34. Server remains authoritative; this layer adds session resume/shop UX/stage transition wiring.
(function(){
  const API='https://timing-defense-mp.onrender.com';
  const mp=window.__TDMP34;
  if(!mp)return;

  const ACTIVE_KEY='tdmp35-active-session';
  const UPGRADE_META={
    atk:{name:'ATK',sub:'+8% damage / rank',mult:1.0},
    crit:{name:'CRIT',sub:'+2% proc chance / rank',mult:1.1},
    critdmg:{name:'CRIT DMG',sub:'+15% proc damage / rank',mult:1.0},
    hp:{name:'WALL HP',sub:'+100 max HP / rank',mult:.9},
    def:{name:'DEF',sub:'-2.5% wall damage / rank',mult:1.1},
    knock:{name:'KNOCKBACK',sub:'+10% / rank',mult:.9}
  };
  const BASE_COST=[40,65,100,145,200,265,340,425,520,625];

  let lastRunSig='',heartbeat=null,resuming=false,reconnectShown=false,lastShopHtml='';
  const baseFetch=window.fetch.bind(window);

  function roomCodeFromUrl(){return (new URL(location.href)).searchParams.get('room')?.toUpperCase()||''}
  function readActive(){try{return JSON.parse(localStorage.getItem(ACTIVE_KEY)||'null')}catch(_){return null}}
  function writeActive(){
    const st=mp.state,run=st?.run;
    if(!st?.code||!mp.session||!run)return;
    try{localStorage.setItem(ACTIVE_KEY,JSON.stringify({room:st.code,session:mp.session,slot:mp.slot,runId:run.id,at:Date.now()}))}catch(_){}
  }
  function clearActive(){try{localStorage.removeItem(ACTIVE_KEY)}catch(_){} }

  window.fetch=async function(input,init){
    const res=await baseFetch(input,init);
    try{
      const url=typeof input==='string'?input:input?.url||'';
      if(url.startsWith(API+'/')){
        const d=await res.clone().json().catch(()=>null);
        if(d?.eventFloor&&Number.isFinite(d.eventFloor))mp.lastEvent=Math.max(mp.lastEvent||0,d.eventFloor);
        if(d?.state?.run)setTimeout(writeActive,0)
      }
    }catch(_){}
    return res
  };

  const style=document.createElement('style');
  style.textContent=`
    #v035Reconnect,#v035Shop{position:fixed;inset:0;z-index:95;font-family:Inter,system-ui,sans-serif;color:#f6faf7}
    #v035Reconnect{display:none;align-items:center;justify-content:center;background:rgba(5,9,8,.88)}
    #v035Reconnect.show{display:flex}
    .v035ReconnectCard{width:min(420px,82vw);padding:20px 22px;border-radius:18px;border:1px solid rgba(255,255,255,.13);background:#172621;box-shadow:0 22px 70px rgba(0,0,0,.4);text-align:center}
    .v035ReconnectTitle{font:1000 19px system-ui}.v035ReconnectSub{margin-top:7px;font:750 9px/1.5 system-ui;color:#9fb0a7}
    .v035ReconnectBtn{margin-top:13px;padding:8px 13px;border-radius:9px;border:1px solid rgba(255,255,255,.14);background:#efe0ac;color:#17201b;font:950 9px system-ui}
    #v035Shop{display:none;background:linear-gradient(145deg,#172621 0%,#263b31 46%,#18251f 100%);padding:13px 18px 12px;box-sizing:border-box}
    #v035Shop.show{display:block}
    .v035ShopTop{height:40px;display:flex;align-items:flex-start;justify-content:space-between}
    .v035ShopBrand{font:1000 15px system-ui;letter-spacing:.1em}.v035ShopStage{font:950 9px system-ui;color:#f0d98c;padding:6px 10px;border:1px solid rgba(240,217,140,.24);border-radius:999px}
    .v035ShopBody{height:calc(100% - 84px);display:grid;grid-template-columns:66% 34%;gap:10px;min-height:0}
    .v035Panel{border:1px solid rgba(255,255,255,.10);background:rgba(6,11,9,.37);border-radius:17px;padding:11px 12px;box-sizing:border-box;min-height:0;overflow:hidden}
    .v035Title{font:1000 17px system-ui}.v035Sub{font:750 8px/1.4 system-ui;color:#9fb0a7;margin-top:3px}
    .v035Coin{margin-top:8px;font:1000 13px system-ui;color:#f3df9b}
    .v035Grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin-top:9px}
    .v035Upgrade{border:1px solid rgba(255,255,255,.09);background:rgba(0,0,0,.18);border-radius:11px;padding:7px;min-width:0}
    .v035UpgradeName{font:950 9px system-ui;white-space:nowrap}.v035UpgradeSub{font:700 7px/1.25 system-ui;color:#96a59d;min-height:18px;margin-top:2px}
    .v035UpgradeFoot{display:flex;align-items:center;justify-content:space-between;margin-top:5px;gap:4px}.v035Rank{font:900 8px system-ui;color:#cbd7d1}
    .v035Buy{border:1px solid rgba(255,255,255,.12);background:#142019;color:#d8e1dc;border-radius:7px;padding:5px 7px;font:900 7.5px system-ui;white-space:nowrap}
    .v035Buy:not(:disabled){background:#efe0ac;color:#17201b;border-color:#efe0ac}.v035Buy:disabled{opacity:.38}
    .v035ReadyTitle{font:1000 12px system-ui;letter-spacing:.05em}.v035People{display:flex;flex-direction:column;gap:7px;margin-top:9px}
    .v035Person{display:flex;align-items:center;justify-content:space-between;padding:8px 9px;border:1px solid rgba(255,255,255,.08);border-radius:10px;background:rgba(255,255,255,.025)}
    .v035PersonName{font:900 9px system-ui}.v035PersonClass{font:750 7px system-ui;color:#9eaaa4;margin-top:2px}.v035PersonState{font:1000 8px system-ui;color:#82938b}.v035PersonState.ready{color:#8ce2aa}
    .v035ShopNote{margin-top:9px;padding:7px 8px;border-radius:9px;background:rgba(0,0,0,.18);font:700 7px/1.4 system-ui;color:#9fb0a7}
    .v035ShopFoot{height:44px;display:flex;align-items:flex-end;justify-content:space-between;gap:8px}
    .v035Action{padding:8px 13px;border-radius:9px;border:1px solid rgba(255,255,255,.13);background:#121b17;color:#dce6df;font:950 9px system-ui}
    .v035Action.primary{background:#efe0ac;color:#17201b;border-color:#efe0ac}.v035Action:disabled{opacity:.35}
    .v035FootStatus{font:800 7px system-ui;color:#9eaaa4;text-align:center;flex:1}
    @media(max-height:590px){
      #v035Shop{padding:8px 14px 7px}.v035ShopTop{height:31px}.v035ShopBody{height:calc(100% - 68px);gap:7px}
      .v035Panel{padding:7px 8px}.v035Title{font-size:14px}.v035Sub{font-size:6.8px}.v035Coin{margin-top:4px;font-size:11px}
      .v035Grid{gap:4px;margin-top:5px}.v035Upgrade{padding:5px}.v035UpgradeName{font-size:7.8px}.v035UpgradeSub{font-size:6.1px;min-height:14px}
      .v035Buy{padding:4px 5px;font-size:6.5px}.v035People{gap:4px;margin-top:6px}.v035Person{padding:5px 6px}.v035ShopNote{margin-top:5px;padding:5px 6px;font-size:6.1px}
      .v035ShopFoot{height:36px}.v035Action{padding:6px 10px;font-size:7.5px}
    }
  `;
  document.head.appendChild(style);

  const reconnect=document.createElement('div');reconnect.id='v035Reconnect';
  reconnect.innerHTML=`<div class="v035ReconnectCard"><div class="v035ReconnectTitle">RUN RECOVERY</div><div id="v035ReconnectSub" class="v035ReconnectSub">서버의 현재 전투 상태를 불러오는 중입니다.</div><button id="v035ReconnectBtn" class="v035ReconnectBtn" style="display:none">LOBBY로 돌아가기</button></div>`;
  document.body.appendChild(reconnect);

  const shop=document.createElement('div');shop.id='v035Shop';document.body.appendChild(shop);

  function costFor(local,key){
    const rank=local?.upgrades?.[key]||0;if(rank>=10)return Infinity;
    return Math.round(BASE_COST[rank]*UPGRADE_META[key].mult)
  }
  function clsName(id){return id==='knight'?'KNIGHT':id==='rogue'?'ROGUE':id==='tank'?'TANK':id==='archer'?'ARCHER':'MAGE'}
  function localPlayer(run){return run?.players?.find(p=>p.slot===mp.slot)}
  function isHost(){return mp.state?.hostSlot===mp.slot}
  function post(action,payload={}){
    if(!mp.state?.code||!mp.session)return Promise.reject(Error('network-not-ready'));
    return fetch(`${API}/api/room/${mp.state.code}/${action}`,{
      method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session:mp.session,...payload})
    }).then(async r=>{const d=await r.json().catch(()=>null);if(!r.ok)throw Error(d?.error||`HTTP ${r.status}`);return d})
  }

  async function buy(key){try{await post('shop-buy',{key})}catch(e){console.warn('shop buy',e)}}
  async function toggleReady(){
    const run=mp.state?.run;if(!run?.shop)return;
    const ready=run.shop.readySlots?.includes(mp.slot);
    try{await post('shop-ready',{ready:!ready})}catch(e){console.warn('shop ready',e)}
  }
  async function nextStage(){try{await post('shop-next')}catch(e){console.warn('shop next',e)}}

  function renderShop(run){
    const local=localPlayer(run);if(!local)return;
    const readySlots=new Set(run.shop?.readySlots||[]),ready=readySlots.has(mp.slot),host=isHost();
    const people=(mp.state?.participants||[]).map(p=>{
      const rp=run.players?.find(x=>x.slot===p.slot),r=readySlots.has(p.slot);
      return `<div class="v035Person"><div><div class="v035PersonName">${escapeHtml(p.nickname)}${p.host?' · HOST':''}</div><div class="v035PersonClass">${escapeHtml(clsName(p.classId))} · COIN ${rp?.coin??0}</div></div><div class="v035PersonState ${r?'ready':''}">${r?'READY ✓':'SHOPPING'}</div></div>`
    }).join('');
    const cards=Object.entries(UPGRADE_META).map(([key,m])=>{
      const rank=local.upgrades?.[key]||0,cost=costFor(local,key),disabled=ready||rank>=10||local.coin<cost;
      return `<div class="v035Upgrade"><div class="v035UpgradeName">${m.name}</div><div class="v035UpgradeSub">${m.sub}</div><div class="v035UpgradeFoot"><span class="v035Rank">R${rank}</span><button class="v035Buy" data-buy="${key}" ${disabled?'disabled':''}>${rank>=10?'MAX':`${cost} C`}</button></div></div>`
    }).join('');
    const html=`<div class="v035ShopTop"><div class="v035ShopBrand">TIMING DEFENSE</div><div class="v035ShopStage">STAGE ${run.shop.stage} CLEAR</div></div>
      <div class="v035ShopBody">
        <section class="v035Panel"><div class="v035Title">TEAM SHOP</div><div class="v035Sub">개인 코인으로 업그레이드를 구매합니다. READY 후에는 구매가 잠깁니다.</div><div class="v035Coin">COIN ${local.coin}</div><div class="v035Grid">${cards}</div></section>
        <section class="v035Panel"><div class="v035ReadyTitle">NEXT STAGE READY</div><div class="v035People">${people}</div><div class="v035ShopNote">모든 사람 플레이어가 READY가 되면 방장의 NEXT STAGE가 활성화됩니다. WALL HP/DEF 구매는 현재 공용 본진에 서버 기준으로 반영되는 프로토타입 규칙입니다.</div></section>
      </div>
      <div class="v035ShopFoot"><button id="v035ReadyBtn" class="v035Action ${ready?'':'primary'}">${ready?'READY ✓ · 수정하기':'READY'}</button><div class="v035FootStatus">${run.shop.canNext?'모든 플레이어 준비 완료':'다른 플레이어의 준비를 기다리는 중'}</div><button id="v035NextBtn" class="v035Action ${host&&run.shop.canNext?'primary':''}" ${host&&run.shop.canNext?'':'disabled'}>NEXT STAGE →</button></div>`;
    if(html!==lastShopHtml){
      shop.innerHTML=html;lastShopHtml=html;
      shop.querySelectorAll('[data-buy]').forEach(b=>b.addEventListener('click',()=>buy(b.dataset.buy)));
      shop.querySelector('#v035ReadyBtn')?.addEventListener('click',toggleReady);
      shop.querySelector('#v035NextBtn')?.addEventListener('click',nextStage)
    }
  }
  function escapeHtml(s){return String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]))}

  function syncLocalUpgrades(run){
    const p=localPlayer(run);if(!p)return;
    S.gold=p.coin??S.gold;
    if(p.upgrades)S.upgrades={...S.upgrades,...p.upgrades}
  }

  function handleRunState(){
    const run=mp.state?.run;if(!run)return;
    writeActive();syncLocalUpgrades(run);
    const sig=`${run.id}:${run.stage}:${run.status}:${run.shop?.readySlots?.join(',')||''}:${run.revision||0}`;

    if(run.status==='shop'){
      if(!shop.classList.contains('show')){
        S.stageMode='netshop';S.phase='idle';S.pendingTap=false;S.projectiles=[];S.resultUntil=0;
        mp.remoteShots.length=0;shop.classList.add('show')
      }
      renderShop(run)
    }else{
      if(shop.classList.contains('show')){shop.classList.remove('show');lastShopHtml=''}
      if(run.status==='stage-starting'){
        S.stage=run.stage;S.stageMode='netStageWait';S.phase='stageIntro';S.pendingTap=false;S.projectiles=[];mp.remoteShots.length=0
      }else if(run.status==='intro'){
        if(S.v035IntroStage!==run.stage){
          S.v035IntroStage=run.stage;
          mp.monsterById.clear();mp.remoteShots.length=0;
          startStage(run.stage,performance.now())
        }
      }else if(run.status==='combat'){
        if(S.stage!==run.stage)S.stage=run.stage;
        if(S.stageMode!=='combat'&&S.stageMode!=='intro'){
          S.stageMode='combat';S.phase='targetWait';S.phaseStart=performance.now();S.pendingTap=false
        }
      }else if(run.status==='stage2-clear'){
        S.stage=2;S.stageMode='clear';S.phase='idle';S.resultText='STAGE 2 SYNC CLEAR';S.resultTier='PERFECT';S.resultUntil=performance.now()+999999
      }
    }
    lastRunSig=sig
  }

  const baseHandleTap=handleTap;
  handleTap=function(now){
    const st=mp.state?.run?.status;
    if(mp.active&&(st==='shop'||st==='stage-starting'||st==='intro'||st==='stage2-clear'))return;
    return baseHandleTap(now)
  };

  async function tryResume(){
    const rec=readActive(),room=roomCodeFromUrl();
    if(!rec?.session||!rec?.runId||!room||rec.room!==room)return;
    resuming=true;reconnectShown=true;reconnect.classList.add('show');
    try{
      const r=await fetch(`${API}/api/room/${room}/resume`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session:rec.session})});
      const d=await r.json().catch(()=>null);
      if(!r.ok)throw Error(d?.error||`HTTP ${r.status}`);
      if(Number.isFinite(d?.eventFloor))mp.lastEvent=Math.max(mp.lastEvent||0,d.eventFloor);
      reconnect.classList.remove('show');resuming=false;
      if(heartbeat)clearInterval(heartbeat);
      heartbeat=setInterval(()=>post('heartbeat').catch(()=>{}),20000)
    }catch(e){
      clearActive();resuming=false;
      reconnect.querySelector('#v035ReconnectSub').textContent='기존 전투 세션을 복구하지 못했습니다. 방이 만료됐거나 세션 유효 시간이 지났습니다.';
      const btn=reconnect.querySelector('#v035ReconnectBtn');btn.style.display='inline-block';btn.onclick=()=>{const u=new URL(location.href);u.searchParams.delete('room');location.href=u.toString()}
    }
  }

  setInterval(()=>{
    if(mp.state?.run&&mp.session)writeActive();
    if(mp.active)handleRunState();
    if(reconnectShown&&mp.active&&!resuming)reconnect.classList.remove('show')
  },100);

  tryResume();
})();