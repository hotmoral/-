// Timing Defense Cloudflare v0.40 — Stage 4 presentation/input guard.
// Stage 2-3 remain owned by the validated v0.37 guard. This layer handles Stage 4 only.
(function(){
  const mp=window.__TDMP34CF;
  if(!mp)return;

  const ACTIVE_PHASES=new Set(['x','y','projectile','recover','targetWait']);
  let armedKey='';
  function key(run){return `${run?.id||''}:${run?.stage||0}`}
  function supported(run){return !!run&&run.stage===4}
  function resetFor(run){const k=key(run);if(k!==armedKey)armedKey=''}

  function armIntro(run){
    if(!supported(run))return;
    resetFor(run);
    const k=key(run);if(armedKey===k&&S.stageMode==='intro')return;
    const now=performance.now();
    S.gameOver=false;S.runComplete=false;S.pendingTap=false;S.hitStopUntil=0;S.lockedCrossUntil=0;
    if(typeof startStage==='function')startStage(4,now);
    else{S.stage=4;S.stageMode='intro';S.phase='stageIntro';S.phaseStart=now;S.v020IntroStart=now;S.v020IntroUntil=now+1050}
    armedKey=k;
  }

  function armCombat(run){
    if(!supported(run))return;
    resetFor(run);
    const k=key(run),now=performance.now();
    if(armedKey!==k){if(typeof startStage==='function')startStage(4,now-1100);armedKey=k}
    S.stage=4;S.gameOver=false;S.runComplete=false;S.pendingTap=false;S.hitStopUntil=0;
    if(S.stageMode==='intro')S.v020IntroUntil=now;
    S.stageMode='combat';
    if(!ACTIVE_PHASES.has(S.phase)||S.phase==='stageIntro'||S.phase==='idle'){
      S.phase='targetWait';S.phaseStart=now;S.pendingTap=false;
    }
  }

  function syncStage(state){
    const run=state?.run;if(!supported(run))return;
    resetFor(run);
    if(run.status==='stage-starting'){
      S.stage=4;S.gameOver=false;S.runComplete=false;
      if(armedKey!==key(run)){S.stageMode='netStageWait';S.phase='idle';S.pendingTap=false;S.projectiles=[]}
      return;
    }
    if(run.status==='intro'){armIntro(run);return}
    if(run.status==='combat'){armCombat(run);return}
  }

  window.addEventListener('tdcf:state',e=>syncStage(e.detail?.state));
  const baseHandleTap=handleTap;
  handleTap=function(now){
    const run=mp.state?.run;
    if(supported(run)&&run.status==='combat')armCombat(run);
    return baseHandleTap(now);
  };
  syncStage(mp.state);
})();