function update(now,dt){
  if(S.gameOver||S.runComplete){
    for(const p of S.particles){p.age+=dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=420*dt}
    S.particles=S.particles.filter(p=>p.age<p.life);for(const f of S.floats)f.age+=dt;S.floats=S.floats.filter(f=>f.age<f.life);return
  }
  if(S.stageMode==='shop'){
    document.getElementById('shopTimer').textContent=performance.now()<S.shopInputUnlockAt?'입력 보호 중…':'NEXT 버튼으로 진행';
    return
  }

  if(S.pendingTap&&(S.phase==='x'||S.phase==='y')&&(now-S.phaseStart)>=cfg.inputLockMs){S.pendingTap=false;handleTap(now)}
  if((S.phase==='x'||S.phase==='y')&&(now-S.phaseStart)>cfg.oneWayMs[cfg.speed]*cfg.maxCycles*2){S.resultText='MISS';S.resultTier='MISS';S.resultUntil=now+320;S.phase='recover';S.phaseStart=now}
  for(const ai of S.ai)if(now>=ai.nextAt)aiAttack(ai,now);

  // Stage-controlled spawning. Every spawn starts beyond the right edge.
  if(now>=S.nextSpawnAt&&S.spawnedThisStage<S.stageTarget&&S.monsters.filter(m=>!m.dead).length<10){
    spawnMonster();S.spawnedThisStage++;S.nextSpawnAt=now+stagePlan(S.stage).gap+rand(-120,160)
  }

  // Movement is constrained to a safe visible vertical corridor.
  for(const m of S.monsters){
    if(m.dead)continue;const d=MONSTER_TYPES[m.type];m.age+=dt;m.hitFlash*=Math.pow(.002,dt);
    m.x-=W*d.speed*dt*(1+(S.stage-1)*.018);
    if(m.type==='flyer')m.y=clamp(m.baseY+Math.sin(m.age*5.0)*H*.020,m.minY,m.maxY);
    else if(m.type==='runner')m.y=clamp(m.baseY+Math.sin(m.age*8.5)*H*.005,m.minY,m.maxY);
    else m.y=clamp(m.y,m.minY,m.maxY);
    if(m.x<=wallFrontX()){
      m.dead=true;const defense=clamp(S.upgrades.def*.025,0,.60),incoming=Math.max(1,Math.round(d.baseDamage*(m.boss?1.45:1)*(1-defense)));
      S.baseHp=Math.max(0,S.baseHp-incoming);addFloat(`-${incoming}`,wallFrontX()+W*.012,m.y,18,'damage');addParticles(wallFrontX()+W*.006,m.y,6,1);
      if(S.baseHp<=0){S.gameOver=true;S.stageMode='gameover';S.resultText='GAME OVER';S.resultTier='CRITICAL';S.resultUntil=now+999999}
    }
  }
  S.monsters=S.monsters.filter(m=>!m.dead||m.hitFlash>.02);

  for(const p of S.projectiles){
    if(p.age<0){p.age+=dt;continue}p.age+=dt;let target=getMonster(p.targetId);if(!target){target=nearestMonster();p.targetId=target?.id??null}
    if(target){const a=monsterAimPoint(target);p.tx=a.x;p.ty=a.y}
    if(p.age>=p.life){p.dead=true;if(p.owner==='local')resolveLocalHit(p,now);else if(p.owner==='skill'){const mm=getMonster(p.targetId)||nearestMonster();visualImpact(p,mm,now,true)}else resolveAIHit(p,now)}
  }
  S.projectiles=S.projectiles.filter(p=>!p.dead);
  if(S.phase==='recover'&&now-S.phaseStart>390){S.attackNo++;S.lastAttackStart=now;startAttack(now)}

  // Stage clear only after all scheduled enemies have entered and been removed.
  const alive=S.monsters.some(m=>!m.dead);
  if(S.spawnedThisStage>=S.stageTarget&&!alive&&S.projectiles.length===0){
    if(!S.stageClearPendingAt)S.stageClearPendingAt=now+650;
    if(now>=S.stageClearPendingAt){if(S.stage>=10)finishRun(now);else beginShop(now)}
  }else S.stageClearPendingAt=0;

  S.playerKick*=Math.pow(.001,dt);S.flash*=Math.pow(.001,dt);
  for(const p of S.particles){p.age+=dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=420*dt}S.particles=S.particles.filter(p=>p.age<p.life);
  for(const f of S.floats)f.age+=dt;S.floats=S.floats.filter(f=>f.age<f.life);for(const p of S.pulses)p.age+=dt;S.pulses=S.pulses.filter(p=>p.age<p.life);
  for(const m of S.chargeMotes){m.age+=dt;if(m.age<0)continue;const t=clamp(m.age/m.life,0,1),e=easeOutCubic(t),u=1-e,mx=(m.sx+m.tx)/2+m.bend,my=(m.sy+m.ty)/2-34;m.x=u*u*m.sx+2*u*e*mx+e*e*m.tx;m.y=u*u*m.sy+2*u*e*my+e*e*m.ty}S.chargeMotes=S.chargeMotes.filter(m=>m.age<m.life)
}
function rr(x,y,w,h,r){const q=Math.min(r,w/2,h/2);ctx.beginPath();ctx.moveTo(x+q,y);ctx.arcTo(x+w,y,x+w,y+h,q);ctx.arcTo(x+w,y+h,x,y+h,q);ctx.arcTo(x,y+h,x,y,q);ctx.arcTo(x,y,x+w,y,q);ctx.closePath()}
function drawBackground(){const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#111820');g.addColorStop(1,'#070a0e');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.strokeStyle='rgba(255,255,255,.03)';for(let x=0;x<W;x+=42){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke()}for(let y=0;y<H;y+=42){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke()}
const wallX=W*.038,wallW=W*.105,wallTop=H*.215,wallBottom=H*.705;ctx.fillStyle='#111821';ctx.fillRect(wallX,wallTop,wallW,wallBottom-wallTop);ctx.strokeStyle='rgba(255,255,255,.11)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(wallX+wallW,wallTop);ctx.lineTo(wallX+wallW,wallBottom);ctx.stroke();for(let i=0;i<4;i++){const y=H*SLOT_Y[i]+H*.028;ctx.strokeStyle=i<S.teamSize?'rgba(255,255,255,.16)':'rgba(255,255,255,.05)';ctx.beginPath();ctx.moveTo(wallX+W*.008,y);ctx.lineTo(wallX+wallW+W*.018,y);ctx.stroke()}
ctx.fillStyle='rgba(255,255,255,.58)';ctx.font='800 10px system-ui';ctx.textAlign='left';ctx.fillText(`WALL HP ${S.baseHp}/${S.baseHpMax}`,wallX+5,wallTop-9);
const hpw=wallW-10,hpr=clamp(S.baseHp/S.baseHpMax,0,1);ctx.fillStyle='rgba(255,255,255,.09)';rr(wallX+5,wallTop-3,hpw,5,3);ctx.fill();ctx.fillStyle=hpr>.5?'rgba(160,220,210,.72)':hpr>.25?'rgba(255,211,106,.8)':'rgba(255,110,110,.85)';rr(wallX+5,wallTop-3,hpw*hpr,5,3);ctx.fill()}