// Timing Defense v0.20 — turn-boundary target gating, stage intro, HUD cleanup, and wider party spacing.
// Balance values are intentionally unchanged from v0.19/v0.18.
(function(){
  const V020_SLOT_Y=[.265,.425,.585,.745];
  const INTRO_MS=1050;

  function hasVisibleTarget(){return !!nearestMonster()}
  function activeLocalTurn(){return !!S.v020TurnEligible && (S.phase==='x'||S.phase==='y'||S.phase==='projectile'||S.phase==='recover')}

  // Wider vertical separation while preserving character size.
  charBase=function(slot){return{x:W*.105,y:H*(V020_SLOT_Y[slot]??V020_SLOT_Y[0]),scale:.41}};

  // Attacks must never force-spawn an invisible enemy. Stage scheduling owns spawning.
  ensureMonsters=function(){};

  // A turn may only START while at least one valid on-screen target exists.
  // Once started, it remains valid until the whole timing turn finishes, even if AI/passive damage removes the last target mid-sweep.
  const baseStartAttack=startAttack;
  startAttack=function(now){
    if(S.stageMode==='combat'&&!S.gameOver&&!S.runComplete&&!hasVisibleTarget()){
      S.phase='targetWait';
      S.phaseStart=now;
      S.pendingTap=false;
      S.v020TurnEligible=false;
      return
    }
    S.v020TurnEligible=S.stageMode==='combat'&&hasVisibleTarget();
    baseStartAttack(now)
  };

  // AI also waits for an actually visible target; waiting never grants AI XP or consumes an AI attack/charge.
  const baseAiAttack=aiAttack;
  aiAttack=function(ai,now){
    if(S.stageMode!=='combat'||!hasVisibleTarget()){
      ai.nextAt=now+120;
      return
    }
    return baseAiAttack(ai,now)
  };

  // If the final enemy disappears during an already-started player turn, allow that turn to finish before opening shop/clear.
  const baseBeginShop=beginShop;
  beginShop=function(now){
    if(activeLocalTurn())return;
    return baseBeginShop(now)
  };
  const baseFinishRun=finishRun;
  finishRun=function(now){
    if(activeLocalTurn())return;
    return baseFinishRun(now)
  };

  // Every stage gets a real intro gate. Nothing moves/attacks/spawns until the intro fully disappears.
  const baseStartStage=startStage;
  startStage=function(stage,now=performance.now()){
    baseStartStage(stage,now);
    S.v020IntroStart=now;
    S.v020IntroUntil=now+INTRO_MS;
    S.v020TurnEligible=false;
    S.stageMode='intro';
    S.phase='stageIntro';
    S.pendingTap=false;
    S.projectiles=[];
    S.resultUntil=0;
    S.nextSpawnAt=now+INTRO_MS;
  };

  // Reject taps during intro / target-wait. Active turns are never cancelled merely because the target vanishes.
  const baseHandleTap=handleTap;
  handleTap=function(now){
    if(S.stageMode!=='combat')return;
    if(S.phase==='targetWait'||S.phase==='stageIntro')return;
    return baseHandleTap(now)
  };

  const baseUpdate=update;
  update=function(now,dt){
    if(S.stageMode==='intro'){
      if(now<S.v020IntroUntil)return;
      S.stageMode='combat';
      S.phase='targetWait';
      S.phaseStart=now;
      S.pendingTap=false;
      S.nextSpawnAt=now;
    }

    baseUpdate(now,dt);

    // Stage update may have moved a scheduled monster into view. Start a fresh turn only at this boundary.
    if(S.stageMode==='combat'&&S.phase==='targetWait'&&hasVisibleTarget()){
      startAttack(now)
    }
  };

  // Make Timing Square visibly paused rather than disappearing while waiting for the next target.
  const baseDrawTimingSquare=drawTimingSquare;
  drawTimingSquare=function(now){
    if(S.stageMode==='intro')return;
    if(S.stageMode==='combat'&&S.phase==='targetWait'){
      const oldLock=S.lockedCrossUntil;
      if(now>S.lockedCrossUntil)S.lockedCrossUntil=now+1;
      ctx.save();ctx.globalAlpha*=.34;baseDrawTimingSquare(now);ctx.restore();
      S.lockedCrossUntil=oldLock;
      return
    }
    baseDrawTimingSquare(now)
  };

  function isJudgmentText(text){
    return typeof text==='string'&&/^(NORMAL|GOOD|PERFECT|CRITICAL|SUPER|GREAT|HEAVY\+?|MISS)(!| ·|$)/.test(text)
  }
  function drawJudgment(now,text,tier){
    if(!text||now>=S.resultUntil||S.stageMode!=='combat')return;
    const g=squareGeom(),rgb=classColor();
    const x=g.x+g.size+38,y=g.y+g.size*.40;
    const strong=tier==='CRITICAL'||tier==='SUPER'||tier==='PERFECT';
    ctx.save();
    ctx.textAlign='left';ctx.textBaseline='middle';
    ctx.font=`950 ${tier==='CRITICAL'?15:strong?13:11}px system-ui`;
    ctx.lineWidth=3;ctx.lineJoin='round';
    ctx.strokeStyle='rgba(3,6,10,.86)';
    ctx.fillStyle=strong?`rgba(${rgb},.98)`:'rgba(239,245,251,.88)';
    ctx.shadowBlur=strong?8:0;ctx.shadowColor=`rgba(${rgb},.72)`;
    ctx.strokeText(text,x,y);ctx.fillText(text,x,y);
    ctx.restore()
  }

  function drawStageIntro(now){
    if(S.stageMode!=='intro')return;
    const start=S.v020IntroStart||now,end=S.v020IntroUntil||now+1;
    const t=clamp((now-start)/Math.max(1,end-start),0,1);
    const fade=t<.18?t/.18:t>.76?(1-t)/.24:1;
    const scale=.88+.12*easeOutCubic(Math.min(1,t/.28));
    ctx.save();
    ctx.globalAlpha=clamp(fade,0,1);
    ctx.translate(W*.5,H*.48);ctx.scale(scale,scale);
    ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.shadowBlur=22;ctx.shadowColor='rgba(255,255,255,.16)';
    ctx.fillStyle='#f7fbff';ctx.font='1000 42px system-ui';ctx.fillText(`STAGE ${S.stage}`,0,-5);
    ctx.shadowBlur=0;ctx.fillStyle='rgba(220,231,241,.70)';ctx.font='850 13px system-ui';ctx.fillText('READY',0,29);
    ctx.restore()
  }

  // Hide the old centered judgment only; preserve skill/acquisition notices.
  const baseDraw=draw;
  draw=function(now){
    const savedUntil=S.resultUntil;
    const savedText=S.resultText;
    const savedTier=S.resultTier;
    const suppress=S.stageMode==='intro'||isJudgmentText(savedText);
    if(suppress)S.resultUntil=0;
    baseDraw(now);
    S.resultUntil=savedUntil;
    if(isJudgmentText(savedText))drawJudgment(now,savedText,savedTier);
    drawStageIntro(now)
  };

  // Remove test-mode header clutter and move class switching upward.
  const title=document.getElementById('title');if(title)title.textContent='TIMING DEFENSE';
  const cc=document.getElementById('classControls');if(cc){cc.style.top='calc(env(safe-area-inset-top) + 31px)'}

  const baseReset=reset;
  reset=function(){
    baseReset();
    S.v020TurnEligible=false;
  };

  // The base page starts before patch layers load. Re-arm the current stage once so Stage 1 also obeys the intro gate.
  startStage(S.stage||1,performance.now());
})();
