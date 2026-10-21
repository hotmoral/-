// Timing Defense v0.37 Slice B — Stage 3 shop terminal guard for this slice.
// Server already rejects Stage 4. This only prevents misleading NEXT UI.
(function(){
  const mp=window.__TDMP34CF;if(!mp)return;
  function apply(st=mp.state){
    const run=st?.run;if(run?.status!=='shop'||run?.shop?.stage!==3)return;
    const next=document.getElementById('v035cfNext');
    if(next){next.disabled=true;next.classList.remove('primary');next.textContent='STAGE 4 LOCKED'}
    const title=document.querySelector('#v035cfShop .v035cfReadyTitle');if(title)title.textContent='STAGE 3 COMPLETE';
    const foot=document.querySelector('#v035cfShop .v035cfFootStatus');if(foot)foot.textContent='Slice B 완료 · Stage 4는 아직 잠겨 있습니다.';
  }
  window.addEventListener('tdcf:state',e=>queueMicrotask(()=>apply(e.detail?.state)));
  apply();
})();