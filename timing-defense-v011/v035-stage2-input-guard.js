// Timing Defense Cloudflare v0.35 — Stage 2 local-input invariant guard.
// Presentation/input only. Server authority and numerical combat values are unchanged.
(function(){
  const mp=window.__TDMP34CF;
  if(!mp)return;

  const ACTIVE_PHASES=new Set(['x','y','projectile','recover']);

  function ensureStage2Input(state){
    const run=state?.run;
    if(!run||run.stage!==2||run.status!=='combat')return;

    S.stage=2;
    S.stageMode='combat';
    S.gameOver=false;
    S.runComplete=false;

    // Team Shop / stage-transition states can leave the local timing loop idle.
    // Re-arm only when the local combat phase is not already active so normal
    // projectile/recover timing is never restarted on every server snapshot.
    if(!ACTIVE_PHASES.has(S.phase)){
      const now=performance.now();
      S.pendingTap=false;
      S.hitStopUntil=0;
      S.lockedCrossUntil=0;
      S.resultUntil=0;
      if(typeof startAttack==='function')startAttack(now);
    }
  }

  window.addEventListener('tdcf:state',e=>ensureStage2Input(e.detail?.state));
  ensureStage2Input(mp.state);
})();
