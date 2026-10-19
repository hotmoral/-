// Timing Defense v0.16 — signature Lv21 visuals and Tank shield overlay.
(function(){
  const baseDrawProjectiles=drawProjectiles;
  drawProjectiles=function(){
    baseDrawProjectiles();
    for(const p of S.projectiles){
      if(p.age<0||(!p.greaterBlade&&!p.groundImpact&&!p.greaterOrb))continue;
      const ang=Math.atan2(p.ty-p.sy,p.tx-p.sx),rgb=classColor(p.cls),pulse=.75+.25*Math.sin(performance.now()*.014);
      ctx.save();ctx.translate(p.x,p.y);ctx.rotate(ang);ctx.shadowColor=`rgba(${rgb},.88)`;ctx.shadowBlur=20;
      if(p.greaterBlade){ctx.scale(1.55,1.55);ctx.strokeStyle=`rgba(${rgb},.26)`;ctx.lineWidth=13;ctx.beginPath();ctx.arc(-9,0,36,-.98,.98);ctx.stroke();ctx.strokeStyle='rgba(255,250,224,.92)';ctx.lineWidth=3;ctx.beginPath();ctx.arc(1,0,32,-.92,.92);ctx.stroke()}
      else if(p.groundImpact){ctx.rotate(-ang);ctx.strokeStyle=`rgba(${rgb},.30)`;ctx.lineWidth=10;ctx.beginPath();ctx.ellipse(0,0,92*pulse,48*pulse,0,-.82,.82);ctx.stroke();ctx.strokeStyle='rgba(225,246,255,.86)';ctx.lineWidth=2.4;ctx.beginPath();ctx.ellipse(0,0,78*pulse,38*pulse,0,-.82,.82);ctx.stroke()}
      else if(p.greaterOrb){ctx.rotate(-ang);for(let i=0;i<3;i++){ctx.strokeStyle=`rgba(${rgb},${.52-i*.12})`;ctx.lineWidth=2.2-i*.4;ctx.beginPath();ctx.arc(0,0,22+i*8+3*Math.sin(performance.now()*.01+i),0,Math.PI*2);ctx.stroke()}ctx.fillStyle=`rgba(${rgb},.12)`;ctx.beginPath();ctx.arc(0,0,31*pulse,0,Math.PI*2);ctx.fill()}
      ctx.restore()
    }
  };

  function drawV016WallShield(now){
    if(!(S.v016WallShield>0&&now<S.v016WallShieldUntil))return;
    const x=wallFrontX(),top=H*.235,bottom=H*.685,rgb=classColor('tank'),ratio=clamp(S.v016WallShield/80,0,1),pulse=.72+.28*Math.sin(now*.016);
    ctx.save();ctx.shadowBlur=16;ctx.shadowColor=`rgba(${rgb},.75)`;ctx.strokeStyle=`rgba(${rgb},${.35+.30*pulse})`;ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x+5,top);ctx.quadraticCurveTo(x+28,H*.46,x+5,bottom);ctx.stroke();ctx.shadowBlur=0;
    ctx.fillStyle='rgba(0,0,0,.58)';rr(x+10,top-16,58,8,4);ctx.fill();ctx.fillStyle=`rgba(${rgb},.82)`;rr(x+10,top-16,58*ratio,8,4);ctx.fill();ctx.font='800 9px system-ui';ctx.textAlign='left';ctx.fillStyle=`rgba(${rgb},.92)`;ctx.fillText(`GUARD ${Math.ceil(S.v016WallShield)}`,x+10,top-22);ctx.restore()
  }

  const baseDraw=draw;
  draw=function(now){baseDraw(now);drawV016WallShield(now)};
})();
