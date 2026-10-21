// Timing Defense Cloudflare v0.35 cf.6 — network UX/state stability polish.
// No combat-balance coefficients are changed. Server state remains authoritative.
(function(){
  const bridge=window.__TDCFBridge,mp=window.__TDMP34CF;
  if(!bridge||!mp)return;

  // ---------------------------------------------------------------------------
  // 1) Keep the local combat class pinned to the authoritative room participant.
  //    This prevents legacy/default Knight palette fallbacks from leaking into a
  //    Rogue/Tank/Archer/Mage network run between state/render layers.
  // ---------------------------------------------------------------------------
  function authoritativeClass(){
    const slot=bridge.slot||mp.slot;
    return mp.state?.participants?.find(p=>p.slot===slot)?.classId||null;
  }
  function pinClass(){
    if(!mp.active)return;
    const cls=authoritativeClass();
    if(cls&&S.playerClass!==cls)S.playerClass=cls;
  }

  // ---------------------------------------------------------------------------
  // 2) Team Shop: keep economy server-confirmed, but expose the in-flight state
  //    immediately and reject duplicate taps for the same upgrade.
  // ---------------------------------------------------------------------------
  const pendingBuys=new Map();
  function localRunPlayer(st=mp.state){
    const slot=bridge.slot||mp.slot;
    return st?.run?.players?.find(p=>p.slot===slot)||null;
  }
  function localRank(key,st=mp.state){return localRunPlayer(st)?.upgrades?.[key]??0}
  function syncPendingButtons(){
    document.querySelectorAll('#v035cfShop [data-buy]').forEach(btn=>{
      const key=btn.dataset.buy,pending=pendingBuys.has(key);
      if(pending){
        if(!btn.dataset.cf6Label)btn.dataset.cf6Label=btn.textContent||'';
        btn.textContent='처리중…';btn.disabled=true;btn.setAttribute('aria-busy','true');
      }else if(btn.dataset.cf6Label){
        btn.textContent=btn.dataset.cf6Label;delete btn.dataset.cf6Label;btn.removeAttribute('aria-busy');
      }
    });
  }
  function clearPending(key){
    const entry=pendingBuys.get(key);if(!entry)return;
    clearTimeout(entry.timer);pendingBuys.delete(key);syncPendingButtons();
  }
  function markPending(key){
    if(!key||pendingBuys.has(key))return false;
    const entry={baseline:localRank(key),started:performance.now(),timer:null};
    entry.timer=setTimeout(()=>clearPending(key),5000);
    pendingBuys.set(key,entry);syncPendingButtons();return true;
  }
  function requestUrl(input){
    try{return new URL(typeof input==='string'?input:input?.url,location.href)}catch(_){return null}
  }
  function parseBody(body){
    if(typeof body!=='string')return null;
    try{return JSON.parse(body)}catch(_){return null}
  }

  const nativeFetch=window.fetch.bind(window);
  window.fetch=async function(input,init={}){
    const url=requestUrl(input),method=String(init?.method||input?.method||'GET').toUpperCase();
    const shopMatch=url?.pathname.match(/^\/api\/room\/[A-Z0-9]{6}\/shop-buy$/i);
    if(shopMatch&&method==='POST'){
      const body=parseBody(init?.body),key=body?.key;
      if(key&&pendingBuys.has(key))throw new Error('shop-buy-pending');
      if(key)markPending(key);
      try{
        const response=await nativeFetch(input,init);
        if(!response.ok&&key)clearPending(key);
        return response;
      }catch(error){
        if(key)clearPending(key);
        throw error;
      }
    }
    return nativeFetch(input,init);
  };

  document.addEventListener('click',event=>{
    const btn=event.target?.closest?.('#v035cfShop [data-buy]');
    if(!btn)return;
    if(pendingBuys.has(btn.dataset.buy)){
      event.preventDefault();event.stopImmediatePropagation();
    }
  },true);

  window.addEventListener('tdcf:state',event=>{
    pinClass();
    const st=event.detail?.state||mp.state;
    for(const [key,pending] of [...pendingBuys]){
      if(localRank(key,st)>pending.baseline)clearPending(key);
    }
    syncPendingButtons();
  });

  const baseUpdate=update;
  update=function(now,dt){pinClass();return baseUpdate(now,dt)};

  const baseDraw=draw;
  draw=function(now){pinClass();return baseDraw(now)};

  const baseHandleTap=handleTap;
  handleTap=function(now){pinClass();return baseHandleTap(now)};
})();
