// Timing Defense v0.14 patch
function drawEffects(now){
  for(const p of S.pulses){
    const t=p.age/p.life,r=p.maxR*easeOutCubic(t);ctx.globalAlpha=(1-t)*.62;
    ctx.strokeStyle=p.rgb?`rgba(${p.rgb},.95)`:'#fff';ctx.lineWidth=2;ctx.beginPath();ctx.arc(p.x,p.y,r,0,Math.PI*2);ctx.stroke();ctx.globalAlpha=1
  }
  for(const p of S.particles){
    const t=p.age/p.life;ctx.save();ctx.globalAlpha=1-t;ctx.translate(p.x,p.y);ctx.rotate((p.rot||0)+(p.spin||0)*p.age);
    const c=p.rgb?`rgba(${p.rgb},.98)`:'#e9f2fa';ctx.fillStyle=c;ctx.shadowColor=p.rgb?`rgba(${p.rgb},.8)`:'rgba(255,255,255,.5)';ctx.shadowBlur=p.spark?8:3;
    if(p.spark){ctx.fillRect(-p.size*.35,-p.len*2,p.size*.7,p.len*4)}else{ctx.fillRect(-p.size/2,-p.size/2,p.size,p.size)}
    ctx.restore()
  }
  for(const f of S.floats){
    const t=f.age/f.life;ctx.save();ctx.globalAlpha=1-clamp((t-.62)/.38,0,1);ctx.translate(f.x,f.y-30*easeOutCubic(t));ctx.font=`900 ${f.size}px system-ui`;ctx.textAlign='center';ctx.fillStyle=f.kind==='gain'?'rgba(220,230,240,.78)':'#f7fbff';ctx.fillText(f.text,0,0);ctx.restore()
  }
  if(now<S.resultUntil){ctx.save();ctx.font=`900 ${S.resultTier==='CRITICAL'?31:23}px system-ui`;ctx.textAlign='center';ctx.fillStyle='#f7fbff';ctx.shadowBlur=S.resultTier==='CRITICAL'?14:0;ctx.shadowColor=`rgba(${classColor()},.8)`;ctx.fillText(S.resultText,W*.32,H*.27);ctx.restore()}
  if(S.flash>.01){ctx.fillStyle=`rgba(255,255,255,${S.flash*.14})`;ctx.fillRect(0,0,W,H)}
  if(S.gameOver||S.runComplete){
    ctx.fillStyle='rgba(5,8,12,.70)';ctx.fillRect(0,0,W,H);ctx.fillStyle='#f7fbff';ctx.textAlign='center';ctx.font='900 32px system-ui';ctx.fillText(S.runComplete?'STAGE 10 CLEAR':'GAME OVER',W*.56,H*.39);
    ctx.font='800 13px system-ui';ctx.fillStyle='rgba(255,255,255,.78)';ctx.fillText(`STAGE ${S.stage} · LV ${S.level} · KILLS ${S.kills} · COIN ${S.gold}`,W*.56,H*.45);ctx.font='700 12px system-ui';ctx.fillStyle='rgba(255,255,255,.56)';ctx.fillText('RESET으로 새 런 시작',W*.56,H*.50)
  }
}

function draw(now){
  ctx.save();
  if(now<S.shakeUntil){const f=(S.shakeUntil-now)/145;ctx.translate(rand(-S.shakeMag,S.shakeMag)*f,rand(-S.shakeMag,S.shakeMag)*f)}
  drawBackground();drawCharacter(0,S.playerClass,true);for(const ai of S.ai)drawCharacter(ai.slot,ai.cls,false);drawChargeMotes();drawProjectiles();drawMonsters();drawEffects(now);
  drawTimingSquare(now);drawProgressHUD(now);drawSkillIcon(now);
  ctx.restore();
  ctx.fillStyle='rgba(255,255,255,.38)';ctx.font='10px system-ui';ctx.textAlign='left';ctx.fillText(`TEAM ${S.teamSize}/4 · STAGE ${S.stage} · KILLS ${S.kills}`,12,H-10);
  ctx.textAlign='right';ctx.fillText(`COIN ${S.gold} · WALL ${S.baseHp}/${S.baseHpMax} · ENEMIES ${S.monsters.filter(m=>!m.dead).length}`,W-12,H-10)
}
