// Timing Defense Cloudflare v0.35 — Stage 2 transition/input invariant guard.
// Presentation/input only. Server authority and numerical combat values are unchanged.
(function(){
  const mp=window.__TDMP34CF;
  if(!mp)return;

  const ACTIVE_PHASES=new Set(['x','y','projectile','recover','targetWait']);
  let introArmed=false,lastRunId=null;

  function resetForRun(run){
    if(run?.id&&run.id!==lastRunId){lastRunId=run.id;introArmed=false}
  }

  function armIntro(run){
    resetForRun(run);
    if(introArmed&&S.stageMode==='intro')return;
    const now=performance.now();
    S.gameOver=false;S.runComplete=false;S.pendingTap=false;S.hitStopUntil=0;S.lockedCrossUntil=0;
    if(typeof startStage==='function'){
      // Reuse the already validated v0.20/v0.21 stage flow:
      // STAGE N -> READY intro -> START! -> target-wait/combat.
      startStage(2,now);
    }else{
      S.stage=2;S.stageMode='intro';S.phase='stageIntro';S.phaseStart=now;
      S.v020IntroStart=now;S.v020IntroUntil=now+1050;
    }
    introArmed=true;
  }

  function armCombat(run){
    resetForRun(run);
    const now=performance.now();
    if(!introArmed){
      // If a delayed snapshot skipped the intro state, initialize through the
      // normal stage path but expire the intro immediately.
      if(typeof startStage==='function')startStage(2,now-1100);
      introArmed=true;
    }
    S.stage=2;S.gameOver=false;S.runComplete=false;S.pendingTap=false;S.hitStopUntil=0;
    if(S.stageMode==='intro')S.v020IntroUntil=now;
    S.stageMode='combat';
    if(!ACTIVE_PHASES.has(S.phase)||S.phase==='stageIntro'||S.phase==='idle'){
      S.phase='targetWait';S.phaseStart=now;S.pendingTap=false;
    }
  }

  function syncStage2(state){
    const run=state?.run;
    if(!run||run.stage!==2)return;
    resetForRun(run);
    if(run.status==='stage-starting'){
      S.stage=2;S.gameOver=false;S.runComplete=false;
      if(!introArmed){S.stageMode='netStageWait';S.phase='idle';S.pendingTap=false;S.projectiles=[]}
      return;
    }
    if(run.status==='intro'){armIntro(run);return}
    if(run.status==='combat'){armCombat(run);return}
  }

  // State snapshots drive the normal transition.
  window.addEventListener('tdcf:state',e=>syncStage2(e.detail?.state));

  // Tap-time invariant: even if a state event was missed, authoritative Stage 2
  // combat can never remain locally non-interactive.
  const baseHandleTap=handleTap;
  handleTap=function(now){
    const run=mp.state?.run;
    if(run?.stage===2&&run.status==='combat')armCombat(run);
    return baseHandleTap(now);
  };

  syncStage2(mp.state);
})();
