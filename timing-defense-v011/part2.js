    const roll=maybeProcCrit(damage*attackMultiplier());damage=roll.damage;proc=roll.proc;
  }else if(owner==='ai')damage=Math.round(damage*(1+(S.stage-1)*.035));
  const skillPower=owner==='local'&&S.skillUnlocked;
  S.projectiles.push({owner,slot,cls,tier,damage,heavy,procCrit:proc,skillPower,targetId:target?.id??null,sx:start.x,sy:start.y,tx:end.x,ty:end.y,x:start.x,y:start.y,age:0,life,rot:0});
  if(owner==='local'&&skillPower&&cls==='rogue'){
    S.projectiles.push({owner:'skill',slot,cls,tier:'SKILL',damage:Math.round(damage*.60),heavy:false,procCrit:false,skillPower:true,targetId:target?.id??null,sx:start.x,sy:start.y+9,tx:end.x,ty:end.y+5,x:start.x,y:start.y+9,age:-.055,life:life+.035,rot:.6});
  }
  if(owner==='local'){
    S.phase='projectile';S.resultText=proc?`${tier}! · PROC CRIT`:(tier==='CRITICAL'?'CRITICAL!':tier+'!');S.resultTier=tier;S.resultUntil=now+420
  }
}
function visualImpact(p,m,now,local){
  if(!m)return false;
  const critical=p.tier==='CRITICAL',perfect=critical||p.tier==='PERFECT'||p.tier==='SUPER',good=perfect||p.tier==='GOOD'||p.tier==='GREAT';
  const d=MONSTER_TYPES[m.type];
  const actual=Math.max(1,Math.round(p.damage*d.armor));
  m.hp-=actual;
  m.hitFlash=1;
  const knockBase=local?(critical?W*.047:perfect?W*.024:good?W*.013:W*.006):(critical?W*.011:perfect?W*.007:good?W*.004:W*.002);
  const kMul=local?knockMultiplier(p):1;
  m.x=Math.min(W*.985,m.x+knockBase*d.knockResist*kMul);
  if(local&&(critical||perfect)){S.shakeUntil=now+(critical?145:95);S.shakeMag=critical?4.8:2.8}
  if(local)S.flash=critical?.9:perfect?.45:.12;
  const a=monsterAimPoint(m);
  addParticles(a.x,a.y,critical?16:perfect?9:good?4:2,critical?1.18:1);
  S.pulses.push({x:a.x,y:a.y,age:0,life:critical?.34:.22,maxR:critical?105:68});
  addFloat(String(actual),a.x,a.y-H*.035,local?(critical||p.procCrit?42:perfect?32:good?27:22):17,local&&(critical||p.procCrit)?'critical':'damage');
  if(p.procCrit)addFloat('PROC CRIT',a.x,a.y-H*.085,14,'gain');
  if(m.hp<=0){m.dead=true;S.kills++;S.stageKills++;if(local){S.gold+=d.reward;addFloat(`COIN +${d.reward}`,a.x,a.y-H*.08,12,'gain')}}
  return true;
}
function resolveLocalHit(p,now){
  let m=getMonster(p.targetId)||nearestMonster();visualImpact(p,m,now,true);
  const critical=p.tier==='CRITICAL',perfect=critical||p.tier==='PERFECT'||p.tier==='SUPER',good=perfect||p.tier==='GOOD'||p.tier==='GREAT';
  S.hitStopUntil=now+(critical?90:perfect?55:good?28:8);
  if(isHeavy())S.charge=0;else{S.charge=Math.min(3,S.charge+1);spawnChargeMotes(S.charge,m)}
  const gainXP=critical?28:perfect?18:good?12:8;awardXP(gainXP);addFloat(`EXP +${gainXP}`,W*.08,H*.82,12,'gain');
  if(S.xJudge==='NORMAL')S.stats.normal++;if(S.xJudge==='GOOD')S.stats.good++;if(S.xJudge==='PERFECT')S.stats.perfect++;if(S.yJudge){if(S.yJudge==='NORMAL')S.stats.normal++;if(S.yJudge==='GOOD')S.stats.good++;if(S.yJudge==='PERFECT')S.stats.perfect++}if(critical)S.stats.critical++;
  S.stats.cycleDurations.push((now-S.lastAttackStart)/1000);if(S.stats.cycleDurations.length>50)S.stats.cycleDurations.shift();updateStats();S.phase='recover';S.phaseStart=now
}
function resolveAIHit(p,now){const m=getMonster(p.targetId)||nearestMonster();visualImpact(p,m,now,false)}
function updateStats(){const a=S.stats.cycleDurations,avg=a.length?a.reduce((x,y)=>x+y,0)/a.length:0;statsEl.innerHTML=`N ${S.stats.normal} · G ${S.stats.good} · P ${S.stats.perfect} · C ${S.stats.critical}<br>AVG ${avg.toFixed(2)}s`}
function handleTap(now){if(S.stageMode!=='combat'||S.gameOver||S.runComplete)return;if(now<S.hitStopUntil)return;if(S.phase!=='x'&&S.phase!=='y')return;if(now-S.phaseStart<cfg.inputLockMs){S.pendingTap=true;return}if(S.phase==='x'){S.xPos=sweepPos(now,S.dirX);S.xJudge=judgeX(S.xPos);if(isHeavy()){S.phase='y';S.phaseStart=now+85;S.pendingTap=false;S.resultText=S.xJudge+' · X LOCK';S.resultTier=S.xJudge;S.resultUntil=now+270;updateAttackLabel()}else{launchProjectile('local',0,S.playerClass,S.xJudge,baseDamage(S.xJudge),false,now);S.playerKick=S.playerClass==='tank'?8:S.playerClass==='rogue'?15:13}}else{S.yPos=sweepPos(now,S.dirY);S.yJudge=judgeY(S.yPos);const[tier,damage]=strongResult(S.xJudge,S.yJudge);S.lockedCrossUntil=now+520;launchProjectile('local',0,S.playerClass,tier,damage,true,now);S.playerKick=S.playerClass==='tank'?12:S.playerClass==='rogue'?23:21}}
function makeAI(){const classes=['rogue','tank','knight'];S.ai=[];const now=performance.now();for(let slot=1;slot<S.teamSize;slot++)S.ai.push({slot,cls:classes[(slot-1)%classes.length],charge:0,shotNo:0,nextAt:now+450+slot*220,shots:0})}
function aiInterval(cls){return cls==='rogue'?1150:cls==='tank'?1650:1400}function aiAttack(ai,now){ai.shotNo++;ai.shots++;const heavy=ai.charge>=3;let r=Math.random(),tier=r<.18?'PERFECT':r<.72?'GOOD':'NORMAL',damage=baseDamage(tier);if(heavy){tier=r<.15?'SUPER':r<.65?'GREAT':'HEAVY+';damage=tier==='SUPER'?400:tier==='GREAT'?300:230;ai.charge=0}else ai.charge++;launchProjectile('ai',ai.slot,ai.cls,tier,damage,heavy,now);ai.nextAt=now+aiInterval(ai.cls)+rand(-140,170)}
function reset(){S.attackNo=1;S.charge=0;S.xp=0;S.level=1;S.xpNeed=60;S.skillUnlocked=false;S.skillNoticeUntil=0;S.gold=0;S.projectiles=[];S.particles=[];S.floats=[];S.pulses=[];S.chargeMotes=[];S.monsters=[];S.nextMonsterId=1;S.baseHpMax=2000;S.baseHp=2000;S.kills=0;S.gameOver=false;S.runComplete=false;S.stage=1;S.stageMode='combat';S.upgrades={atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0};S.stats={normal:0,good:0,perfect:0,critical:0,cycleDurations:[]};S.lastAttackStart=performance.now();makeAI();startAttack(performance.now());startStage(1,performance.now());updateStats();updateRunStatus()}
document.querySelectorAll('[data-speed]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();cfg.speed=b.dataset.speed;document.querySelectorAll('[data-speed]').forEach(x=>x.classList.toggle('active',x===b));reset()}));
document.querySelectorAll('[data-class]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();S.playerClass=b.dataset.class;document.querySelectorAll('[data-class]').forEach(x=>x.classList.toggle('active',x===b));reset()}));
document.querySelectorAll('[data-team]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();S.teamSize=Number(b.dataset.team);document.querySelectorAll('[data-team]').forEach(x=>x.classList.toggle('active',x===b));reset()}));document.getElementById('resetBtn').addEventListener('click',e=>{e.stopPropagation();reset()});document.getElementById('nextBtn').addEventListener('click',e=>{e.stopPropagation();nextStage()});
addEventListener('pointerdown',e=>{if(e.target.closest&&(e.target.closest('#controls')||e.target.closest('#classControls')||e.target.closest('#shop')))return;handleTap(performance.now())},{passive:true});addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();handleTap(performance.now())}});
function update(now,dt){
  if(S.gameOver||S.runComplete){for(const p of S.particles){p.age+=dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=420*dt}S.particles=S.particles.filter(p=>p.age<p.life);for(const f of S.floats)f.age+=dt;S.floats=S.floats.filter(f=>f.age<f.life);return}
  if(S.stageMode==='shop'){const remain=Math.max(0,S.shopEndAt-now);document.getElementById('shopTimer').textContent=`NEXT ${(remain/1000).toFixed(1)}`;if(remain<=0)nextStage();return}
  if(S.pendingTap&&(S.phase==='x'||S.phase==='y')&&(now-S.phaseStart)>=cfg.inputLockMs){S.pendingTap=false;handleTap(now)}
  if((S.phase==='x'||S.phase==='y')&&(now-S.phaseStart)>cfg.oneWayMs[cfg.speed]*cfg.maxCycles*2){S.resultText='MISS';S.resultTier='MISS';S.resultUntil=now+320;S.phase='recover';S.phaseStart=now}
  for(const ai of S.ai)if(now>=ai.nextAt)aiAttack(ai,now);
  if(now>=S.nextSpawnAt&&S.spawnedThisStage<S.stageTarget&&S.monsters.filter(m=>!m.dead).length<10){spawnMonster();S.spawnedThisStage++;S.nextSpawnAt=now+stagePlan(S.stage).gap+rand(-120,160)}
  for(const m of S.monsters){if(m.dead)continue;const d=MONSTER_TYPES[m.type];m.age+=dt;m.hitFlash*=Math.pow(.002,dt);m.x-=W*d.speed*dt*(1+(S.stage-1)*.018);if(m.type==='flyer')m.y=clamp(m.baseY+Math.sin(m.age*5.0)*H*.020,m.minY,m.maxY);else if(m.type==='runner')m.y=clamp(m.baseY+Math.sin(m.age*8.5)*H*.005,m.minY,m.maxY);else m.y=clamp(m.y,m.minY,m.maxY);if(m.x<=wallFrontX()){m.dead=true;const defense=clamp(S.upgrades.def*.025,0,.60),incoming=Math.max(1,Math.round(d.baseDamage*(m.boss?1.45:1)*(1-defense)));S.baseHp=Math.max(0,S.baseHp-incoming);addFloat(`-${incoming}`,wallFrontX()+W*.012,m.y,18,'damage');addParticles(wallFrontX()+W*.006,m.y,6,1);if(S.baseHp<=0){S.gameOver=true;S.stageMode='gameover';S.resultText='GAME OVER';S.resultTier='CRITICAL';S.resultUntil=now+999999}}}
  S.monsters=S.monsters.filter(m=>!m.dead||m.hitFlash>.02);
  for(const p of S.projectiles){if(p.age<0){p.age+=dt;continue}p.age+=dt;let target=getMonster(p.targetId);if(!target){target=nearestMonster();p.targetId=target?.id??null}if(target){const a=monsterAimPoint(target);p.tx=a.x;p.ty=a.y}if(p.age>=p.life){p.dead=true;if(p.owner==='local')resolveLocalHit(p,now);else if(p.owner==='skill'){const mm=getMonster(p.targetId)||nearestMonster();visualImpact(p,mm,now,true)}else resolveAIHit(p,now)}}
  S.projectiles=S.projectiles.filter(p=>!p.dead);if(S.phase==='recover'&&now-S.phaseStart>390){S.attackNo++;S.lastAttackStart=now;startAttack(now)}
  const alive=S.monsters.some(m=>!m.dead);if(S.spawnedThisStage>=S.stageTarget&&!alive&&S.projectiles.length===0){if(!S.stageClearPendingAt)S.stageClearPendingAt=now+650;if(now>=S.stageClearPendingAt){if(S.stage>=10)finishRun(now);else beginShop(now)}}else S.stageClearPendingAt=0;
  S.playerKick*=Math.pow(.001,dt);S.flash*=Math.pow(.001,dt);for(const p of S.particles){p.age+=dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=420*dt}S.particles=S.particles.filter(p=>p.age<p.life);for(const f of S.floats)f.age+=dt;S.floats=S.floats.filter(f=>f.age<f.life);for(const p of S.pulses)p.age+=dt;S.pulses=S.pulses.filter(p=>p.age<p.life);for(const m of S.chargeMotes){m.age+=dt;if(m.age<0)continue;const t=clamp(m.age/m.life,0,1),e=easeOutCubic(t),u=1-e,mx=(m.sx+m.tx)/2+m.bend,my=(m.sy+m.ty)/2-34;m.x=u*u*m.sx+2*u*e*mx+e*e*m.tx;m.y=u*u*m.sy+2*u*e*my+e*e*m.ty}S.chargeMotes=S.chargeMotes.filter(m=>m.age<m.life)
}
function rr(x,y,w,h,r){const q=Math.min(r,w/2,h/2);ctx.beginPath();ctx.moveTo(x+q,y);ctx.arcTo(x+w,y,x+w,y+h,q);ctx.arcTo(x+w,y+h,x,y+h,q);ctx.arcTo(x,y+h,x,y,q);ctx.arcTo(x,y,x+w,y,q);ctx.closePath()}
function drawBackground(){const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,'#111820');g.addColorStop(1,'#070a0e');ctx.fillStyle=g;ctx.fillRect(0,0,W,H);ctx.strokeStyle='rgba(255,255,255,.03)';for(let x=0;x<W;x+=42){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke()}for(let y=0;y<H;y+=42){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke()}const wallX=W*.038,wallW=W*.105,wallTop=H*.215,wallBottom=H*.705;ctx.fillStyle='#111821';ctx.fillRect(wallX,wallTop,wallW,wallBottom-wallTop);ctx.strokeStyle='rgba(255,255,255,.11)';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(wallX+wallW,wallTop);ctx.lineTo(wallX+wallW,wallBottom);ctx.stroke();for(let i=0;i<4;i++){const y=H*SLOT_Y[i]+H*.028;ctx.strokeStyle=i<S.teamSize?'rgba(255,255,255,.16)':'rgba(255,255,255,.05)';ctx.beginPath();ctx.moveTo(wallX+W*.008,y);ctx.lineTo(wallX+wallW+W*.018,y);ctx.stroke()}ctx.fillStyle='rgba(255,255,255,.58)';ctx.font='800 10px system-ui';ctx.textAlign='left';ctx.fillText(`WALL HP ${S.baseHp}/${S.baseHpMax}`,wallX+5,wallTop-9);const hpw=wallW-10,hpr=clamp(S.baseHp/S.baseHpMax,0,1);ctx.fillStyle='rgba(255,255,255,.09)';rr(wallX+5,wallTop-3,hpw,5,3);ctx.fill();ctx.fillStyle=hpr>.5?'rgba(160,220,210,.72)':hpr>.25?'rgba(255,211,106,.8)':'rgba(255,110,110,.85)';rr(wallX+5,wallTop-3,hpw*hpr,5,3);ctx.fill()}