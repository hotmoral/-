// Timing Defense v0.40 — Stage 4 terminal guard.
// Stage 3 NEXT is intentionally enabled in this slice; Stage 5 remains blocked.
(function(){
  const mp=window.__TDMP34CF;if(!mp)return;
  function apply(st=mp.state){
    const run=st?.run;if(run?.status!=='shop'||run?.shop?.stage!==4)return;
    const next=document.getElementById('v035cfNext');
    if(next){next.disabled=true;next.classList.remove('primary');next.textContent='STAGE 5 LOCKED'}
    const title=document.querySelector('#v035cfShop .v035cfReadyTitle');if(title)title.textContent='STAGE 4 COMPLETE';
    const foot=document.querySelector('#v035cfShop .v035cfFootStatus');if(foot)foot.textContent='v0.40 완료 · Stage 5는 아직 잠겨 있습니다.';
  }
  window.addEventListener('tdcf:state',e=>queueMicrotask(()=>apply(e.detail?.state)));
  apply();
})();