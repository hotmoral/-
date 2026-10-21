// Timing Defense Cloudflare v0.35 cf.6 — network UX/state stability polish.
// No combat-balance coefficients are changed.
(function(){
  const bridge=window.__TDCFBridge,mp=window.__TDMP34CF;
  if(!bridge||!mp)return;

  function authoritativeClass(){
    const slot=bridge.slot||mp.slot;
    return mp.state?.participants?.find(p=>p.slot===slot)?.classId||null;
  }
  function pinClass(){
    if(!mp.active)return;
    const cls=authoritativeClass();
    if(cls&&S.playerClass!==cls)S.playerClass=cls;
  }

  window.addEventListener('tdcf:state',()=>pinClass());

  const baseUpdate=update;
  update=function(now,dt){pinClass();return baseUpdate(now,dt)};

  const baseDraw=draw;
  draw=function(now){pinClass();return baseDraw(now)};

  const baseHandleTap=handleTap;
  handleTap=function(now){pinClass();return baseHandleTap(now)};
})();
