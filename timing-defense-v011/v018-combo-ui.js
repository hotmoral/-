// Timing Defense v0.18 — visible PERFECT streak counter only.
// No combo damage/reward tuning in this patch.
(function(){
  function initCombo(clear=false){
    if(clear||typeof S.v018Combo!=='number')S.v018Combo=0;
    if(clear||typeof S.v018ComboPulseUntil!=='number')S.v018ComboPulseUntil=0;
    if(clear||typeof S.v018ComboPeak!=='number')S.v018ComboPeak=0;
  }
  initCombo(false);

  function recordJudge(judge,now){
    if(judge==='PERFECT'){
      S.v018Combo++;
      S.v018ComboPeak=Math.max(S.v018ComboPeak,S.v018Combo);
      S.v018ComboPulseUntil=now+230;
    }else{
      S.v018Combo=0;
      S.v018ComboPulseUntil=0;
    }
  }

  const baseHandleTap=handleTap;
  handleTap=function(now){
    const before=S.phase;
    baseHandleTap(now);
    if((before==='x'||before==='y')&&S.phase!==before){
      const judge=before==='x'?S.xJudge:S.yJudge;
      if(judge)recordJudge(judge,now);
    }
  };

  const baseUpdate=update;
  update=function(now,dt){
    const before=S.phase;
    baseUpdate(now,dt);
    if((before==='x'||before==='y')&&S.phase==='recover'&&S.resultText==='MISS'){
      S.v018Combo=0;S.v018ComboPulseUntil=0;
    }
  };

  const baseReset=reset;
  reset=function(){baseReset();initCombo(true)};

  function drawCombo(now){
    const c=S.v018Combo||0;if(c<1||S.stageMode!=='combat'||S.gameOver||S.runComplete)return;
    const g=squareGeom(),rgb=classColor(),pulse=now<S.v018ComboPulseUntil?1-clamp((S.v018ComboPulseUntil-now)/230,0,1):0;
    let font=11,glow=0,alpha=.72;
    if(c>=30){font=20;glow=16;alpha=1}
    else if(c>=20){font=18;glow=12;alpha=.98}
    else if(c>=10){font=15;glow=8;alpha=.94}
    else if(c>=5){font=13;glow=4;alpha=.86}
    const scale=1+(now<S.v018ComboPulseUntil?Math.sin(pulse*Math.PI)*.10:0);
    const text=`${c} COMBO`,x=g.x+2,y=g.y-26;
    ctx.save();ctx.translate(x,y);ctx.scale(scale,scale);ctx.textAlign='left';ctx.textBaseline='middle';ctx.font=`900 ${font}px system-ui`;
    const w=ctx.measureText(text).width+12,h=font+10;
    ctx.fillStyle='rgba(5,9,14,.66)';rr(-5,-h/2,w,h,7);ctx.fill();
    ctx.shadowBlur=glow;ctx.shadowColor=`rgba(${rgb},.88)`;ctx.fillStyle=`rgba(${rgb},${alpha})`;ctx.fillText(text,1,0);ctx.shadowBlur=0;
    if(c>=20){ctx.strokeStyle=`rgba(${rgb},${c>=30?.62:.38})`;ctx.lineWidth=c>=30?1.7:1.1;rr(-5,-h/2,w,h,7);ctx.stroke()}
    ctx.restore()
  }

  const baseDraw=draw;
  draw=function(now){baseDraw(now);drawCombo(now)};
})();
