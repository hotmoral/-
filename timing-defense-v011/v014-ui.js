// Timing Defense v0.14 patch
(function(){const style=document.createElement('style');style.textContent='#runStatus{display:none!important}';document.head.appendChild(style)})();
function addParticles(x,y,count,scale=1,rgb=null,spark=false){
  for(let i=0;i<count;i++){
    const a=rand(-Math.PI*.88,Math.PI*.88),sp=rand(85,255)*scale;
    S.particles.push({
      x,y,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp-rand(15,95),
      age:0,life:rand(spark?.18:.24,spark?.36:.50),
      size:rand(1.8,5.2)*scale,rgb,spark,
      rot:rand(-Math.PI,Math.PI),spin:rand(-7,7),
      len:rand(1.8,4.8)*scale
    })
  }
}

function drawProgressHUD(now){
  const g=squareGeom(),rgb=classColor(),barX=g.x+g.size+12,barY=g.y+5,barW=14,barH=g.size-10,ratio=clamp(S.xp/S.xpNeed,0,1),flash=now<S.levelFlashUntil;
  ctx.save();
  if(flash){ctx.shadowBlur=18;ctx.shadowColor=`rgba(${rgb},.9)`}
  ctx.fillStyle='rgba(0,0,0,.58)';rr(barX,barY,barW,barH,7);ctx.fill();
  ctx.strokeStyle=`rgba(${rgb},.30)`;ctx.lineWidth=1;rr(barX,barY,barW,barH,7);ctx.stroke();
  const fillH=Math.max(2,barH*ratio);ctx.fillStyle=`rgba(${rgb},${flash?.98:.82})`;rr(barX,barY+barH-fillH,barW,fillH,7);ctx.fill();
  ctx.shadowBlur=0;ctx.fillStyle='#f5f8fb';ctx.textAlign='center';ctx.font=`900 ${flash?13:11}px system-ui`;ctx.fillText(`LV ${S.level}`,barX+barW/2,barY-9);
  ctx.font='800 8px system-ui';ctx.fillStyle='rgba(255,255,255,.52)';ctx.fillText('EXP',barX+barW/2,barY+barH+12);
  if(now<S.xpGainUntil){
    ctx.textAlign='left';ctx.font='900 10px system-ui';ctx.fillStyle=`rgba(${rgb},.98)`;
    ctx.shadowBlur=8;ctx.shadowColor=`rgba(${rgb},.55)`;
    ctx.fillText(`+${S.lastXpGain}`,barX+barW+6,barY+barH*(1-ratio)+3)
  }
  ctx.restore()
}

function drawSkillIcon(now){
  if(!S.skillUnlocked)return;
  const g=squareGeom(),rgb=classColor(),size=28,x=g.x-1,y=g.y-42;
  const pulse=now<S.skillNoticeUntil?(.65+.35*Math.sin(now*.018)):0;
  ctx.save();
  if(pulse){ctx.shadowBlur=12+10*pulse;ctx.shadowColor=`rgba(${rgb},.9)`}
  ctx.fillStyle='rgba(7,10,14,.92)';rr(x,y,size,size,6);ctx.fill();
  ctx.strokeStyle=`rgba(${rgb},${pulse?.95:.58})`;ctx.lineWidth=pulse?2.4:1.5;rr(x,y,size,size,6);ctx.stroke();
  ctx.translate(x+size/2,y+size/2);
  ctx.strokeStyle=`rgba(${rgb},.98)`;ctx.fillStyle=`rgba(${rgb},.95)`;ctx.lineCap='round';ctx.lineJoin='round';
  if(S.playerClass==='knight'){
    ctx.lineWidth=3;ctx.beginPath();ctx.arc(-2,2,9,-1.1,.65);ctx.stroke();
    ctx.lineWidth=1.4;ctx.strokeStyle='rgba(255,255,255,.8)';ctx.beginPath();ctx.arc(-1,1,6,-1.05,.55);ctx.stroke();
  }else if(S.playerClass==='rogue'){
    ctx.lineWidth=2.4;ctx.beginPath();ctx.moveTo(-8,7);ctx.lineTo(7,-8);ctx.moveTo(-7,-7);ctx.lineTo(8,8);ctx.stroke();
    ctx.fillStyle='#f5fbff';ctx.beginPath();ctx.moveTo(9,-10);ctx.lineTo(4,-5);ctx.lineTo(8,-2);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(10,10);ctx.lineTo(5,5);ctx.lineTo(2,9);ctx.closePath();ctx.fill();
  }else if(S.playerClass==='tank'){
    ctx.lineWidth=2.5;ctx.beginPath();ctx.arc(0,0,8,-.9,.9);ctx.stroke();
    ctx.globalAlpha=.55;ctx.beginPath();ctx.arc(0,0,12,-.72,.72);ctx.stroke();
  }else if(S.playerClass==='archer'){
    ctx.lineWidth=2.1;ctx.beginPath();ctx.moveTo(-10,5);ctx.lineTo(9,-5);ctx.stroke();
    ctx.fillStyle=`rgba(${rgb},1)`;ctx.beginPath();ctx.moveTo(11,-6);ctx.lineTo(5,-7);ctx.lineTo(8,-1);ctx.closePath();ctx.fill();
    ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(-9,2);ctx.lineTo(-6,7);ctx.moveTo(-7,0);ctx.lineTo(-4,5);ctx.stroke();
  }else{
    ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,5,0,Math.PI*2);ctx.stroke();
    for(let i=0;i<6;i++){const a=i*Math.PI/3;ctx.beginPath();ctx.moveTo(Math.cos(a)*8,Math.sin(a)*8);ctx.lineTo(Math.cos(a)*12,Math.sin(a)*12);ctx.stroke()}
    ctx.fillStyle='rgba(255,255,255,.8)';ctx.beginPath();ctx.arc(0,0,2.4,0,Math.PI*2);ctx.fill();
  }
  ctx.restore()
}

function drawTimingSquare(now){
  if(S.phase!=='x'&&S.phase!=='y'&&now>S.lockedCrossUntil)return;
  const g=squareGeom(),t=S.target,rgb=classColor(),x=g.x,y=g.y,s=g.size,cy=y-22,heavy=isHeavy();
  ctx.save();
  if(heavy){
    const pulse=.5+.5*Math.sin(now*.012),expand=3+3*pulse;
    ctx.shadowBlur=18+10*pulse;ctx.shadowColor=`rgba(${rgb},.78)`;
    ctx.strokeStyle=`rgba(${rgb},${.42+.35*pulse})`;ctx.lineWidth=2.4;
    rr(x-expand,y-expand,s+expand*2,s+expand*2,14);ctx.stroke();
    ctx.shadowBlur=0;
    for(let i=0;i<8;i++){
      const side=i%4,k=Math.floor(i/4),j=(now*.0017+i*.137)%1;
      let x1=x,y1=y,x2=x,y2=y;
      if(side===0){x1=x+j*s;y1=y-7-k*3;x2=x1+(i%2?7:-7);y2=y1-6}
      if(side===1){x1=x+s+7+k*3;y1=y+j*s;x2=x1+6;y2=y1+(i%2?7:-7)}
      if(side===2){x1=x+j*s;y1=y+s+7+k*3;x2=x1+(i%2?7:-7);y2=y1+6}
      if(side===3){x1=x-7-k*3;y1=y+j*s;x2=x1-6;y2=y1+(i%2?7:-7)}
      ctx.strokeStyle=`rgba(${rgb},${.35+.45*pulse})`;ctx.lineWidth=1.5;
      ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo((x1+x2)/2+rand(-2,2),(y1+y2)/2+rand(-2,2));ctx.lineTo(x2,y2);ctx.stroke()
    }
  }
  ctx.textAlign='center';ctx.font='900 10px system-ui';
  ctx.fillStyle=heavy?`rgba(${rgb},1)`:`rgba(${rgb},.78)`;
  ctx.fillText(heavy?'HEAVY READY':`CHARGE ${S.charge}/3`,x+s/2,cy-11);
  const gap=22,start=x+s/2-gap;
  for(let i=0;i<3;i++){
    const on=i<S.charge;
    ctx.fillStyle=on?`rgba(${rgb},.98)`:'rgba(255,255,255,.12)';
    if(on){ctx.shadowBlur=8;ctx.shadowColor=`rgba(${rgb},.55)`}else ctx.shadowBlur=0;
    ctx.beginPath();ctx.arc(start+i*gap,cy,6.5,0,Math.PI*2);ctx.fill()
  }
  ctx.shadowBlur=0;
  ctx.fillStyle='rgba(5,8,12,.70)';rr(x,y,s,s,12);ctx.fill();
  ctx.fillStyle=`rgba(${rgb},${heavy?.16:.085})`;rr(x,y,s,s,12);ctx.fill();
  ctx.strokeStyle=`rgba(${rgb},${heavy?.90:.48})`;ctx.lineWidth=heavy?3.2:2;rr(x,y,s,s,12);ctx.stroke();
  const gx=x+(t.gx-cfg.goodW/2)*s,gy=y+(t.gy-cfg.goodH/2)*s,gw=cfg.goodW*s,gh=cfg.goodH*s;
  ctx.fillStyle=heavy?'rgba(81,201,141,.36)':'rgba(81,201,141,.23)';rr(gx,gy,gw,gh,8);ctx.fill();
  const px=x+(t.px-cfg.perfectW/2)*s,py=y+(t.py-cfg.perfectH/2)*s,pw=cfg.perfectW*s,ph=cfg.perfectH*s;
  ctx.fillStyle=heavy?'rgba(255,211,106,.92)':'rgba(255,211,106,.66)';rr(px,py,pw,ph,5);ctx.fill();
  if(!heavy&&S.phase==='x'){
    ctx.fillStyle='rgba(81,201,141,.055)';ctx.fillRect(gx,y,gw,s);
    ctx.fillStyle='rgba(255,211,106,.08)';ctx.fillRect(px,y,pw,s)
  }
  let xp=S.xPos;if(S.phase==='x')xp=sweepPos(now,S.dirX);
  if(xp!==null){
    const xx=x+xp*s;ctx.strokeStyle='#fff';ctx.lineWidth=S.xPos!==null?2.4:3;
    if(heavy){ctx.shadowBlur=10;ctx.shadowColor=`rgba(${rgb},.85)`}
    ctx.beginPath();ctx.moveTo(xx,y+5);ctx.lineTo(xx,y+s-5);ctx.stroke();ctx.shadowBlur=0
  }
  let yp=S.yPos;if(S.phase==='y')yp=sweepPos(now,S.dirY);
  if(yp!==null){
    const yy=y+yp*s;ctx.strokeStyle='#fff';ctx.lineWidth=S.yPos!==null?2.4:3;
    if(heavy){ctx.shadowBlur=10;ctx.shadowColor=`rgba(${rgb},.85)`}
    ctx.beginPath();ctx.moveTo(x+5,yy);ctx.lineTo(x+s-5,yy);ctx.stroke();ctx.shadowBlur=0
  }
  if(S.xPos!==null&&S.yPos!==null){
    const xx=x+S.xPos*s,yy=y+S.yPos*s;
    ctx.fillStyle=S.resultTier==='CRITICAL'?'#fff':`rgba(${rgb},1)`;
    ctx.shadowBlur=12;ctx.shadowColor=`rgba(${rgb},.9)`;
    ctx.beginPath();ctx.arc(xx,yy,S.resultTier==='CRITICAL'?7:5,0,Math.PI*2);ctx.fill()
  }
  ctx.restore()
}
