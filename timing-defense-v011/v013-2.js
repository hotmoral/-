function spawnChargeMotes(level,source=null){
  const p=weaponWorldPos(),rgb=classColor(),count=5+level*3;
  const src=source||nearestMonster();
  const sx0=src?src.x:W*.68,sy0=src?src.y:H*.45;
  for(let i=0;i<count;i++)S.chargeMotes.push({
    sx:sx0+rand(-20,20),sy:sy0+rand(-18,18),tx:p.x+rand(-4,4),ty:p.y+rand(-4,4),
    x:0,y:0,age:-rand(0,.06),
    life:S.playerClass==='rogue'?rand(.25,.36):S.playerClass==='tank'?rand(.42,.56):S.playerClass==='archer'?rand(.28,.40):S.playerClass==='mage'?rand(.38,.54):rand(.34,.48),
    bend:rand(-24,24),size:rand(2.2,4.6),rgb,cls:S.playerClass
  })
}
function launchProjectile(owner,slot,cls,tier,damage,heavy=false,now=performance.now()){
  ensureMonsters();
  const start=weaponWorldPos(slot,cls),target=nearestMonster();
  const life=cls==='rogue'?.16:cls==='tank'?.25:cls==='archer'?.14:cls==='mage'?.28:.19;
  const fallback={x:W*.96,y:start.y};
  const end=target?monsterAimPoint(target):fallback;
  let proc=false;
  if(owner==='local'){
    const roll=maybeProcCrit(damage*attackMultiplier());damage=roll.damage;proc=roll.proc;
  }else if(owner==='ai')damage=Math.round(damage*(1+(S.stage-1)*.035));
  const skillPower=owner==='local'&&S.skillUnlocked;
  S.projectiles.push({owner,slot,cls,tier,damage,heavy,procCrit:proc,skillPower,pierceSkill:owner==='local'&&skillPower&&cls==='archer',burstSkill:owner==='local'&&skillPower&&cls==='mage',targetId:target?.id??null,sx:start.x,sy:start.y,tx:end.x,ty:end.y,x:start.x,y:start.y,age:0,life,rot:0});
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

  if(m.hp<=0){
    m.dead=true;
    S.kills++;S.stageKills++;
    if(local){S.gold+=d.reward;addFloat(`COIN +${d.reward}`,a.x,a.y-H*.08,12,'gain')}
  }
  return true;
}
function resolveLocalHit(p,now){
  let m=getMonster(p.targetId)||nearestMonster();
  visualImpact(p,m,now,true);
  if(m&&p.pierceSkill){const second=S.monsters.filter(x=>!x.dead&&x.id!==m.id&&x.x>=m.x).sort((a,b)=>a.x-b.x)[0];if(second){visualImpact({...p,damage:Math.round(p.damage*.52),procCrit:false,pierceSkill:false,skillPower:false},second,now,true);const a=monsterAimPoint(second);addFloat('PIERCE',a.x,a.y-42,11,'gain')}}
  if(m&&p.burstSkill){const near=S.monsters.filter(x=>!x.dead&&x.id!==m.id&&Math.abs(x.x-m.x)<W*.105&&Math.abs(x.y-m.y)<H*.16).slice(0,3);for(const other of near)visualImpact({...p,damage:Math.round(p.damage*.38),procCrit:false,burstSkill:false,skillPower:false},other,now,true);if(near.length){const a=monsterAimPoint(m);S.pulses.push({x:a.x,y:a.y,age:0,life:.32,maxR:95});addFloat('ARCANE BURST',a.x,a.y-50,11,'gain')}}

  const critical=p.tier==='CRITICAL',perfect=critical||p.tier==='PERFECT'||p.tier==='SUPER',good=perfect||p.tier==='GOOD'||p.tier==='GREAT';
  S.hitStopUntil=now+(critical?90:perfect?55:good?28:8);
  if(isHeavy())S.charge=0;
  else{S.charge=Math.min(3,S.charge+1);spawnChargeMotes(S.charge,m)}

  const gainXP=xpForTier(p.tier);
  awardXP(gainXP);addFloat(`EXP +${gainXP}`,W*.08,H*.82,12,'gain');

  if(S.xJudge==='NORMAL')S.stats.normal++;
  if(S.xJudge==='GOOD')S.stats.good++;
  if(S.xJudge==='PERFECT')S.stats.perfect++;
  if(S.yJudge){
    if(S.yJudge==='NORMAL')S.stats.normal++;
    if(S.yJudge==='GOOD')S.stats.good++;
    if(S.yJudge==='PERFECT')S.stats.perfect++
  }
  if(critical)S.stats.critical++;
  S.stats.cycleDurations.push((now-S.lastAttackStart)/1000);
  if(S.stats.cycleDurations.length>50)S.stats.cycleDurations.shift();
  updateStats();
  S.phase='recover';S.phaseStart=now
}
function resolveAIHit(p,now){
  const m=getMonster(p.targetId)||nearestMonster();
  visualImpact(p,m,now,false)
}
function updateStats(){const a=S.stats.cycleDurations,avg=a.length?a.reduce((x,y)=>x+y,0)/a.length:0;statsEl.innerHTML=`N ${S.stats.normal} · G ${S.stats.good} · P ${S.stats.perfect} · C ${S.stats.critical}<br>AVG ${avg.toFixed(2)}s`}
function handleTap(now){if(S.stageMode!=='combat'||S.gameOver||S.runComplete)return;if(now<S.hitStopUntil)return;if(S.phase!=='x'&&S.phase!=='y')return;if(now-S.phaseStart<cfg.inputLockMs){S.pendingTap=true;return}if(S.phase==='x'){S.xPos=sweepPos(now,S.dirX);S.xJudge=judgeX(S.xPos);if(isHeavy()){S.phase='y';S.phaseStart=now+85;S.pendingTap=false;S.resultText=S.xJudge;S.resultTier=S.xJudge;S.resultUntil=now+250;updateAttackLabel()}else{launchProjectile('local',0,S.playerClass,S.xJudge,baseDamage(S.xJudge),false,now);S.playerKick=S.playerClass==='tank'?8:S.playerClass==='rogue'?15:S.playerClass==='archer'?12:S.playerClass==='mage'?9:13}}else{S.yPos=sweepPos(now,S.dirY);S.yJudge=judgeY(S.yPos);const[tier,damage]=strongResult(S.xJudge,S.yJudge);S.lockedCrossUntil=now+520;launchProjectile('local',0,S.playerClass,tier,damage,true,now);S.playerKick=S.playerClass==='tank'?12:S.playerClass==='rogue'?23:S.playerClass==='archer'?18:S.playerClass==='mage'?14:21}}
function makeAI(){const pool=['knight','rogue','tank','archer','mage'].filter(c=>c!==S.playerClass);S.ai=[];const now=performance.now();for(let slot=1;slot<S.teamSize;slot++)S.ai.push({slot,cls:pool[(slot-1)%pool.length],charge:0,shotNo:0,nextAt:now+450+slot*220,shots:0})}
function aiInterval(cls){return cls==='rogue'?1150:cls==='tank'?1650:cls==='archer'?1200:cls==='mage'?1500:1400}function aiAttack(ai,now){ai.shotNo++;ai.shots++;const heavy=ai.charge>=3;let r=Math.random(),tier=r<.18?'PERFECT':r<.72?'GOOD':'NORMAL',damage=baseDamage(tier);if(heavy){tier=r<.15?'SUPER':r<.65?'GREAT':'HEAVY+';damage=tier==='SUPER'?400:tier==='GREAT'?300:230;ai.charge=0}else ai.charge++;launchProjectile('ai',ai.slot,ai.cls,tier,damage,heavy,now);ai.nextAt=now+aiInterval(ai.cls)+rand(-140,170)}
function reset(){
  S.attackNo=1;S.charge=0;S.xp=0;S.level=1;S.xpNeed=60;S.skillUnlocked=false;S.skillNoticeUntil=0;S.skillUnlockedStage=0;S.levelFlashUntil=0;S.lastXpGain=0;S.xpGainUntil=0;S.shopInputUnlockAt=0;S.gold=0;
  S.projectiles=[];S.particles=[];S.floats=[];S.pulses=[];S.chargeMotes=[];S.monsters=[];S.nextMonsterId=1;
  S.baseHpMax=2000;S.baseHp=2000;S.kills=0;S.gameOver=false;S.runComplete=false;S.stage=1;S.stageMode='combat';
  S.upgrades={atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0};
  S.stats={normal:0,good:0,perfect:0,critical:0,cycleDurations:[]};
  S.lastAttackStart=performance.now();makeAI();startAttack(performance.now());startStage(1,performance.now());updateStats();updateRunStatus()
}

document.querySelectorAll('[data-speed]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();cfg.speed=b.dataset.speed;document.querySelectorAll('[data-speed]').forEach(x=>x.classList.toggle('active',x===b));reset()}));
document.querySelectorAll('[data-class]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();S.playerClass=b.dataset.class;document.querySelectorAll('[data-class]').forEach(x=>x.classList.toggle('active',x===b));reset()}));
document.querySelectorAll('[data-team]').forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();S.teamSize=Number(b.dataset.team);document.querySelectorAll('[data-team]').forEach(x=>x.classList.toggle('active',x===b));reset()}));document.getElementById('resetBtn').addEventListener('click',e=>{e.stopPropagation();reset()});document.getElementById('nextBtn').addEventListener('click',e=>{e.stopPropagation();if(performance.now()<S.shopInputUnlockAt)return;nextStage()});
addEventListener('pointerdown',e=>{if(e.target.closest&&(e.target.closest('#controls')||e.target.closest('#classControls')||e.target.closest('#shop')))return;handleTap(performance.now())},{passive:true});addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();handleTap(performance.now())}});