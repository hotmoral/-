// Timing Defense v0.19 — transient PERFECT combo pop near Timing Square.
// Uses v0.18 combo state contract so v018-auto-combo.js can keep using it.
(function(){
  function initCombo(clear=false){
    if(clear||typeof S.v018Combo!=='number')S.v018Combo=0;
    if(clear||typeof S.v018ComboPeak!=='number')S.v018ComboPeak=0;
    if(clear||!Array.isArray(S.v018PendingMilestones))S.v018PendingMilestones=[];
    if(clear||typeof S.v019ComboPopUntil!=='number')S.v019ComboPopUntil=0;
    if(clear||typeof S.v019ComboPopStart!=='number')S.v019ComboPopStart=0;
    if(clear||typeof S.v019ComboPopValue!=='number')S.v019ComboPopValue=0;
  }
  initCombo(false);

  function milestoneFor(c){
    if(c===5||c===10||c===20||c===30)return c;
    if(c>30&&c%10===0)return c;
    return 0;
  }
  function recordJudge(judge,now){
    if(judge==='PERFECT'){
      S.v018Combo++;
      S.v018ComboPeak=Math.max(S.v018ComboPeak,S.v018Combo);
      S.v019ComboPopValue=S.v018Combo;
      S.v019ComboPopStart=now;
      S.v019ComboPopUntil=now+460;
      const m=milestoneFor(S.v018Combo);
      if(m)S.v018PendingMilestones.push(m);
    }else{
      S.v018Combo=0;
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
      S.v018Combo=0;
    }
  };

  const baseReset=reset;
  reset=function(){baseReset();initCombo(true)};

  function drawBurst(x,y,rgb,power,t){
    if(power<1)return;
    const n=power>=4?8:power>=3?6:4;
    const rad=(13+power*3)*(1+.28*Math.sin(Math.PI*t));
    ctx.save();
    ctx.strokeStyle=`rgba(${rgb},${.45*(1-t)})`;
    ctx.lineWidth=power>=4?2:1.2;
    for(let i=0;i<n;i++){
      const a=(-.95+i*(1.9/Math.max(1,n-1))) + (i%2?.08:-.05);
      const r0=rad*.68,r1=rad;
      ctx.beginPath();
      ctx.moveTo(x+Math.cos(a)*r0,y+Math.sin(a)*r0);
      ctx.lineTo(x+Math.cos(a)*r1,y+Math.sin(a)*r1);
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawComboPop(now){
    if(now>=S.v019ComboPopUntil||S.stageMode!=='combat'||S.gameOver||S.runComplete)return;
    const c=S.v019ComboPopValue||0;if(c<1)return;
    const elapsed=Math.max(0,now-S.v019ComboPopStart),life=Math.max(1,S.v019ComboPopUntil-S.v019ComboPopStart),t=clamp(elapsed/life,0,1);
    const tier=c>=30?4:c>=20?3:c>=10?2:c>=5?1:0;
    const g=squareGeom(),rgb=classColor();
    const rise=12*easeOutCubic(t),fade=t<.62?1:1-clamp((t-.62)/.38,0,1);
    const punch=t<.20?(0.72+2.15*t):(1.15-.15*clamp((t-.20)/.25,0,1));
    const font=[12,14,17,20,23][tier];
    const tilt=(-.075-(c%3)*.012);
    const x=g.x+g.size*.50,y=g.y-24-rise;

    drawBurst(x,y,rgb,tier,t);

    ctx.save();
    ctx.translate(x,y);
    ctx.rotate(tilt);
    ctx.scale(punch,punch);
    ctx.globalAlpha=fade;
    ctx.textAlign='center';
    ctx.textBaseline='middle';
    ctx.font=`1000 ${font}px system-ui`;
    ctx.lineJoin='round';
    ctx.lineWidth=tier>=3?5:tier>=1?4:3;
    ctx.strokeStyle='rgba(3,6,10,.90)';
    ctx.shadowBlur=tier>=4?20:tier>=3?14:tier>=2?9:tier>=1?5:0;
    ctx.shadowColor=`rgba(${rgb},.95)`;
    const text=`${c} COMBO!`;
    ctx.strokeText(text,0,0);
    ctx.fillStyle=tier===0?'rgba(245,248,251,.92)':`rgba(${rgb},1)`;
    ctx.fillText(text,0,0);
    if(tier>=3){
      ctx.globalAlpha=fade*.55;
      ctx.font=`900 ${Math.max(8,font-8)}px system-ui`;
      ctx.fillStyle='#fff';
      ctx.fillText(c>=30?'PERFECT STREAK':'STREAK',0,font*.82);
    }
    ctx.restore();
  }

  const baseDraw=draw;
  draw=function(now){baseDraw(now);drawComboPop(now)};
})();
