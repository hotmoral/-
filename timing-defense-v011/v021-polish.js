// Timing Defense v0.21 — combat HUD polish, natural battlefield, centered result board, START cue.
// Balance values remain unchanged from v0.18-v0.20.
(function(){
  const JUDGE_LIFE=330;
  const START_LIFE=430;

  const baseAddFloat=addFloat;
  addFloat=function(text,x,y,size=25,kind='damage'){
    if(typeof text==='string'&&/^EXP \+/.test(text))return;
    return baseAddFloat(text,x,y,size,kind)
  };

  const hint=document.getElementById('hint'); if(hint)hint.style.display='none';
  const stats=document.getElementById('stats'); if(stats)stats.style.display='none';

  drawProgressHUD=function(now){
    const g=squareGeom(),rgb=classColor(),barX=g.x+g.size+12,barY=g.y+5,barW=14,barH=g.size-10;
    const ratio=clamp(S.xp/S.xpNeed,0,1),flash=now<S.levelFlashUntil;
    ctx.save();
    if(flash){ctx.shadowBlur=18;ctx.shadowColor=`rgba(${rgb},.9)`}
    ctx.fillStyle='rgba(0,0,0,.58)';rr(barX,barY,barW,barH,7);ctx.fill();
    ctx.strokeStyle=`rgba(${rgb},.34)`;ctx.lineWidth=1;rr(barX,barY,barW,barH,7);ctx.stroke();
    const fillH=Math.max(2,barH*ratio);
    ctx.fillStyle=`rgba(${rgb},${flash?.98:.84})`;rr(barX,barY+barH-fillH,barW,fillH,7);ctx.fill();
    ctx.shadowBlur=0;
    ctx.fillStyle='#f5f8fb';ctx.textAlign='center';ctx.font=`900 ${flash?13:11}px system-ui`;ctx.fillText(`LV ${S.level}`,barX+barW/2,barY-9);
    ctx.font='800 8px system-ui';ctx.fillStyle='rgba(255,255,255,.60)';ctx.fillText('EXP',barX+barW/2,barY+barH+12);
    if(now<S.xpGainUntil){
      ctx.textAlign='left';ctx.textBaseline='middle';ctx.font='950 10px system-ui';ctx.fillStyle=`rgba(${rgb},.98)`;
      ctx.shadowBlur=8;ctx.shadowColor=`rgba(${rgb},.55)`;
      ctx.fillText(`+EXP ${S.lastXpGain}`,barX+barW+7,barY+barH*(1-ratio)+2)
    }
    ctx.restore()
  };

  drawBackground=function(){
    const sky=ctx.createLinearGradient(0,0,0,H*.72);
    sky.addColorStop(0,'#7596a6');sky.addColorStop(.48,'#a8b7ad');sky.addColorStop(1,'#d1c49e');
    ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);
    const sunX=W*.76,sunY=H*.16;
    const sun=ctx.createRadialGradient(sunX,sunY,3,sunX,sunY,H*.22);
    sun.addColorStop(0,'rgba(255,239,191,.30)');sun.addColorStop(1,'rgba(255,239,191,0)');
    ctx.fillStyle=sun;ctx.fillRect(0,0,W,H*.55);
    ctx.fillStyle='rgba(79,101,96,.58)';ctx.beginPath();ctx.moveTo(0,H*.49);
    for(let x=0;x<=W;x+=W*.09){const y=H*(.36+.055*Math.sin(x/W*9.3)+.035*Math.sin(x/W*17.7));ctx.lineTo(x,y)}
    ctx.lineTo(W,H*.62);ctx.lineTo(0,H*.62);ctx.closePath();ctx.fill();
    ctx.fillStyle='rgba(49,76,64,.76)';ctx.beginPath();ctx.moveTo(0,H*.58);
    for(let x=0;x<=W;x+=W*.075){const y=H*(.47+.045*Math.sin(x/W*11.1+1.2)+.025*Math.sin(x/W*20.2));ctx.lineTo(x,y)}
    ctx.lineTo(W,H*.70);ctx.lineTo(0,H*.70);ctx.closePath();ctx.fill();
    const ground=ctx.createLinearGradient(0,H*.54,0,H);
    ground.addColorStop(0,'#465f43');ground.addColorStop(.55,'#31483a');ground.addColorStop(1,'#1e302a');
    ctx.fillStyle=ground;ctx.fillRect(0,H*.55,W,H*.45);
    ctx.fillStyle='rgba(213,194,143,.16)';ctx.beginPath();ctx.moveTo(W*.12,H*.71);ctx.lineTo(W,H*.64);ctx.lineTo(W,H*.82);ctx.lineTo(W*.12,H*.78);ctx.closePath();ctx.fill();
    ctx.fillStyle='rgba(29,55,43,.48)';
    for(const p of [[.30,.48,.028],[.37,.51,.021],[.84,.47,.030],[.91,.50,.022]]){
      const x=W*p[0],y=H*p[1],r=H*p[2];ctx.fillRect(x-r*.12,y,r*.24,H*.11);
      ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.arc(x-r*.72,y+r*.28,r*.68,0,Math.PI*2);ctx.arc(x+r*.66,y+r*.24,r*.62,0,Math.PI*2);ctx.fill()
    }
    const wallX=W*.038,wallW=W*.105,wallTop=H*.185,wallBottom=H*.83;
    const stone=ctx.createLinearGradient(wallX,0,wallX+wallW,0);stone.addColorStop(0,'#283335');stone.addColorStop(1,'#3d4b49');
    ctx.fillStyle=stone;ctx.fillRect(wallX,wallTop,wallW,wallBottom-wallTop);
    ctx.strokeStyle='rgba(220,232,221,.22)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(wallX+wallW,wallTop);ctx.lineTo(wallX+wallW,wallBottom);ctx.stroke();
    ctx.strokeStyle='rgba(255,255,255,.055)';ctx.lineWidth=1;
    for(let y=wallTop+22;y<wallBottom;y+=24){ctx.beginPath();ctx.moveTo(wallX,y);ctx.lineTo(wallX+wallW,y);ctx.stroke()}
    for(let i=0;i<4;i++){
      const y=charBase(i).y+H*.028;ctx.strokeStyle=i<S.teamSize?'rgba(235,242,230,.24)':'rgba(255,255,255,.07)';ctx.lineWidth=1.2;
      ctx.beginPath();ctx.moveTo(wallX+W*.008,y);ctx.lineTo(wallX+wallW+W*.018,y);ctx.stroke()
    }
    ctx.fillStyle='rgba(245,249,244,.80)';ctx.font='800 10px system-ui';ctx.textAlign='left';ctx.fillText(`WALL HP ${S.baseHp}/${S.baseHpMax}`,wallX+5,wallTop-9);
    const hpw=wallW-10,hpr=clamp(S.baseHp/S.baseHpMax,0,1);
    ctx.fillStyle='rgba(0,0,0,.24)';rr(wallX+5,wallTop-3,hpw,5,3);ctx.fill();
    ctx.fillStyle=hpr>.5?'rgba(161,225,197,.90)':hpr>.25?'rgba(255,211,106,.90)':'rgba(255,110,110,.92)';rr(wallX+5,wallTop-3,hpw*hpr,5,3);ctx.fill()
  };

  function isJudgmentText(text){return typeof text==='string'&&/^(NORMAL|GOOD|PERFECT|CRITICAL|SUPER|GREAT|HEAVY\+?|MISS)(!| ·|$)/.test(text)}
  function cleanJudgment(text){return String(text||'').split(' · ')[0].replace(/!+$/,'')}
  function judgeStyle(tier){
    const map={NORMAL:{size:13,color:'#dfe7ee',glow:0},GOOD:{size:17,color:'#7de0a2',glow:5},PERFECT:{size:22,color:'#ffd65a',glow:13},HEAVY:{size:15,color:'#d6e0ea',glow:2},'HEAVY+':{size:18,color:'#84ddf5',glow:7},GREAT:{size:19,color:'#80c5ff',glow:8},SUPER:{size:21,color:'#d49dff',glow:12},CRITICAL:{size:25,color:'#fff2a8',glow:18},MISS:{size:14,color:'#ff7a7a',glow:4}};
    return map[tier]||map.NORMAL
  }
  function armJudgment(now){
    if(!isJudgmentText(S.resultText))return;
    S.v021JudgeText=cleanJudgment(S.resultText);S.v021JudgeTier=S.resultTier||S.v021JudgeText;S.v021JudgeStart=now;S.v021JudgeUntil=now+JUDGE_LIFE
  }

  const baseHandleTap=handleTap;
  handleTap=function(now){const beforeUntil=S.resultUntil;const out=baseHandleTap(now);if(S.resultUntil!==beforeUntil&&isJudgmentText(S.resultText))armJudgment(now);return out};

  const baseUpdate=update;
  update=function(now,dt){
    const wasIntro=S.stageMode==='intro',beforeUntil=S.resultUntil;baseUpdate(now,dt);
    if(wasIntro&&S.stageMode==='combat'){S.v021StartPopStart=now;S.v021StartPopUntil=now+START_LIFE}
    if(S.resultUntil!==beforeUntil&&isJudgmentText(S.resultText))armJudgment(now)
  };

  function drawJudgmentPop(now){
    if(!S.v021JudgeUntil||now>=S.v021JudgeUntil||S.stageMode!=='combat')return;
    const g=squareGeom(),t=clamp((now-S.v021JudgeStart)/JUDGE_LIFE,0,1),st=judgeStyle(S.v021JudgeTier);
    const punch=t<.18?(.70+2.05*t):(1.07-.07*clamp((t-.18)/.25,0,1));
    const fade=t<.60?1:1-clamp((t-.60)/.40,0,1);
    const x=g.x+g.size*.5,y=g.y+g.size*.48-5*easeOutCubic(t);
    ctx.save();ctx.translate(x,y);ctx.scale(punch,punch);ctx.globalAlpha=fade;ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.font=`1000 ${st.size}px system-ui`;ctx.lineJoin='round';ctx.lineWidth=3.6;ctx.strokeStyle='rgba(5,8,11,.78)';
    ctx.shadowBlur=st.glow;ctx.shadowColor=st.color;ctx.strokeText(S.v021JudgeText,0,0);ctx.fillStyle=st.color;ctx.fillText(S.v021JudgeText,0,0);ctx.restore()
  }

  function drawStartPop(now){
    if(!S.v021StartPopUntil||now>=S.v021StartPopUntil||S.stageMode!=='combat')return;
    const t=clamp((now-S.v021StartPopStart)/START_LIFE,0,1),fade=t<.55?1:1-(t-.55)/.45;
    const scale=.78+.30*Math.sin(Math.min(1,t/.35)*Math.PI*.5);
    ctx.save();ctx.globalAlpha=clamp(fade,0,1);ctx.translate(W*.5,H*.47);ctx.scale(scale,scale);ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.font='1000 46px system-ui';ctx.lineWidth=6;ctx.strokeStyle='rgba(23,35,31,.55)';ctx.shadowBlur=18;ctx.shadowColor='rgba(255,241,188,.42)';ctx.strokeText('START!',0,0);ctx.fillStyle='#fff0b8';ctx.fillText('START!',0,0);ctx.restore()
  }

  function fresh(){return{kills:0,damage:0,coin:0,perfects:0,combo:0,maxCombo:0}}
  function resultRows(){
    const out=[{slot:0,label:'YOU',cls:S.playerClass,kills:S.v019Stats?.[0]?.kills||0,damage:S.v019Stats?.[0]?.damage||0,coin:S.v019Stats?.[0]?.coin||0,level:S.level||1,levelScore:(S.level||1)*100000+(S.xp||0),maxCombo:S.v018ComboPeak||0,perfects:S.stats?.perfect||0}];
    for(const ai of S.ai){const st=S.v019Stats?.[ai.slot]||fresh();out.push({slot:ai.slot,label:`CPU ${ai.slot}`,cls:ai.cls,kills:st.kills||0,damage:st.damage||0,coin:st.coin||0,level:ai.level||1,levelScore:(ai.level||1)*100000+(ai.xp||0),maxCombo:st.maxCombo||0,perfects:st.perfects||0})}
    return out.sort((a,b)=>a.slot-b.slot)
  }
  const resultMetrics=[{key:'kills',label:'KILLS',fmt:v=>String(v),tie:r=>r.damage},{key:'damage',label:'DMG',fmt:v=>v>=10000?`${(v/1000).toFixed(1)}K`:String(Math.round(v)),tie:r=>r.kills},{key:'coin',label:'COIN',fmt:v=>String(v),tie:r=>r.kills},{key:'level',score:'levelScore',label:'LV',fmt:v=>String(v),tie:r=>r.perfects},{key:'maxCombo',label:'MAX COMBO',fmt:v=>String(v),tie:r=>r.perfects}];
  function resultRanks(rs,m){const k=m.score||m.key,sorted=[...rs].sort((a,b)=>((b[k]||0)-(a[k]||0))||((m.tie?m.tie(b):0)-(m.tie?m.tie(a):0))||(a.slot-b.slot));const map={};sorted.forEach((r,i)=>map[r.slot]=i+1);return map}
  const rankColor={1:'#ffd65a',2:'#d9e2ea',3:'#c98b5d',4:'#7f93a6'};
  function drawCenteredResult(){
    if(!(S.gameOver||S.runComplete))return;
    const rs=resultRows(),n=rs.length,pw=Math.min(W*.76,1040),ph=Math.min(H*.69,520),px=(W-pw)/2,py=(H-ph)/2;
    const pad=30,leftW=Math.min(210,pw*.245),tableX=px+pad,tableW=pw-pad*2,metricW=(tableW-leftW)/resultMetrics.length;
    const headerY=py+96,rowStart=py+119,rowGap=6,rowH=Math.min(48,(ph-154-(n-1)*rowGap)/Math.max(1,n));
    const rankBy={};for(const m of resultMetrics)rankBy[m.key]=resultRanks(rs,m);
    ctx.save();ctx.fillStyle='rgba(8,14,18,.89)';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='rgba(12,19,22,.97)';rr(px,py,pw,ph,20);ctx.fill();ctx.strokeStyle='rgba(255,255,255,.16)';ctx.lineWidth=1.3;rr(px,py,pw,ph,20);ctx.stroke();
    ctx.textAlign='left';ctx.textBaseline='alphabetic';ctx.fillStyle='#f7fbff';ctx.font='1000 30px system-ui';ctx.fillText(S.runComplete?'STAGE 10 CLEAR':`GAME OVER · STAGE ${S.stage}`,px+pad,py+43);
    ctx.fillStyle='rgba(255,255,255,.57)';ctx.font='760 11px system-ui';ctx.fillText(`TEAM CONTRIBUTION  ·  WALL ${S.baseHp}/${S.baseHpMax}  ·  KILL COIN`,px+pad,py+66);
    ctx.fillStyle='rgba(255,255,255,.43)';ctx.font='850 10px system-ui';ctx.fillText('PLAYER / CLASS',tableX+8,headerY);ctx.textAlign='center';resultMetrics.forEach((m,i)=>ctx.fillText(m.label,tableX+leftW+metricW*(i+.5),headerY));
    ctx.strokeStyle='rgba(255,255,255,.09)';ctx.beginPath();ctx.moveTo(tableX,headerY+10);ctx.lineTo(tableX+tableW,headerY+10);ctx.stroke();
    rs.forEach((r,ri)=>{
      const y=rowStart+ri*(rowH+rowGap),rgb=classColor(r.cls);ctx.fillStyle=ri%2===0?'rgba(255,255,255,.040)':'rgba(255,255,255,.022)';rr(tableX,y,tableW,rowH,9);ctx.fill();
      ctx.fillStyle=`rgba(${rgb},.96)`;ctx.beginPath();ctx.arc(tableX+12,y+rowH*.5,5,0,Math.PI*2);ctx.fill();ctx.textAlign='left';ctx.fillStyle='#f4f8fc';ctx.font='950 12px system-ui';ctx.fillText(`${ri+1}. ${r.label}`,tableX+26,y+rowH*.43);ctx.fillStyle=`rgba(${rgb},.84)`;ctx.font='820 9px system-ui';ctx.fillText(className(r.cls),tableX+26,y+rowH*.72);
      resultMetrics.forEach((m,mi)=>{const rank=rankBy[m.key][r.slot],cx=tableX+leftW+metricW*(mi+.5),col=rankColor[rank]||rankColor[4];ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=col;ctx.beginPath();ctx.arc(cx-metricW*.24,y+rowH*.50,7.5,0,Math.PI*2);ctx.fill();ctx.fillStyle='rgba(8,11,16,.94)';ctx.font='1000 8px system-ui';ctx.fillText(String(rank),cx-metricW*.24,y+rowH*.50+.3);ctx.fillStyle=rank===1?'#ffe49a':rank===2?'#eef4f8':rank===3?'#e1ad85':'rgba(221,231,240,.72)';ctx.font=`${rank===1?1000:880} 12px system-ui`;ctx.fillText(m.fmt(r[m.key]||0),cx+metricW*.06,y+rowH*.50+.2);if(rank===1){ctx.strokeStyle='rgba(255,214,90,.50)';ctx.lineWidth=1.4;ctx.beginPath();ctx.moveTo(cx-metricW*.02,y+rowH*.72);ctx.lineTo(cx+metricW*.28,y+rowH*.72);ctx.stroke()}})
    });
    ctx.textAlign='center';ctx.textBaseline='alphabetic';ctx.font='720 10px system-ui';ctx.fillStyle='rgba(255,255,255,.43)';ctx.fillText('항목별 순위  ·  1위 금색 강조  ·  RESET으로 새 런 시작',px+pw*.5,py+ph-18);ctx.restore()
  }

  const baseDraw=draw;
  draw=function(now){
    const judge=isJudgmentText(S.resultText)&&S.stageMode==='combat';
    const result=!!(S.gameOver||S.runComplete);
    const saveUntil=S.resultUntil,saveGameOver=S.gameOver,saveRunComplete=S.runComplete;
    if(judge)S.resultUntil=0;
    if(result){S.gameOver=false;S.runComplete=false}
    baseDraw(now);
    S.resultUntil=saveUntil;S.gameOver=saveGameOver;S.runComplete=saveRunComplete;
    if(judge)drawJudgmentPop(now);
    drawStartPop(now);
    if(result)drawCenteredResult();
    const cc=document.getElementById('classControls');if(cc)cc.style.visibility=result?'hidden':'visible'
  };
})();
