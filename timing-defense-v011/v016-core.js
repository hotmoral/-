// Timing Defense v0.16 — Lv6/Lv11/Lv16/Lv21 playable skill block
// Layered on top of v0.15. Keeps v0.15 as the rollback/stable prototype.

const V016_UNLOCKS=[6,11,16,21,26,31];
const V016_SKILL_NAMES={
  knight:['ENHANCED BLADE WAVE','BREAKTHROUGH SLASH','SHARP EDGE','GREAT BLADE WAVE','FRONTLINE COLLAPSE','HEAVEN-SPLITTING SLASH'],
  rogue:['DOUBLE DAGGER','WEAK-POINT DETECTION','ASSASSIN RHYTHM','BLADE BARRAGE','CHAIN THROW','DAGGER STORM'],
  tank:['IMPACT WAVE+','IRON WALL','PERFECT GUARD','GROUND IMPACT','AFTERSHOCK ZONE','ABSOLUTE BARRIER'],
  archer:['PIERCING ARROW','STRONG BOW','PRECISION PENETRATION','TRIPLE SHOT','IMPALING SHOT','SKY-PIERCING ARROW'],
  mage:['ARCANE BURST','EXPANDED MAGIC CIRCLE','RESONANCE','GREATER ARCANE ORB','CHAIN EXPLOSION','ARCANE COLLAPSE']
};

function v016Has(level){return S.level>=level}
function v016SkillCount(){return V016_UNLOCKS.filter(v=>S.level>=v).length}
function v016ContainsPerfect(){return S.xJudge==='PERFECT'||S.yJudge==='PERFECT'}
function v016InitState(clear=false){
  if(clear||!Array.isArray(S.v016DelayedBlasts))S.v016DelayedBlasts=[];
  if(clear||typeof S.v016WallShield!=='number')S.v016WallShield=0;
  if(clear||typeof S.v016WallShieldUntil!=='number')S.v016WallShieldUntil=0;
  if(clear||typeof S.v016RecoverMs!=='number')S.v016RecoverMs=390;
  if(clear||typeof S.v016SkillNoticeLevel!=='number')S.v016SkillNoticeLevel=0;
  S.skillUnlocked=S.level>=6;
}
v016InitState(false);

const v016BaseReset=reset;
reset=function(){v016BaseReset();v016InitState(true)};

function v016SkillName(level,cls=S.playerClass){
  const idx=V016_UNLOCKS.indexOf(level);
  return idx>=0?(V016_SKILL_NAMES[cls]||V016_SKILL_NAMES.knight)[idx]:'';
}

awardXP=function(amount){
  if(S.stageMode!=='combat')return;
  S.lastXpGain=amount;S.xpGainUntil=performance.now()+650;S.xp+=amount;
  while(S.xp>=S.xpNeed){
    S.xp-=S.xpNeed;S.level++;S.xpNeed=levelNeed(S.level);S.levelFlashUntil=performance.now()+850;
    addFloat(`LEVEL ${S.level}`,squareGeom().x+squareGeom().size+30,squareGeom().y+18,20,'gain');
    const idx=V016_UNLOCKS.indexOf(S.level);
    if(idx>=0){
      S.skillUnlocked=true;S.skillUnlockedStage=S.stage;S.skillNoticeUntil=performance.now()+4200;S.v016SkillNoticeLevel=S.level;
      S.resultText=`SKILL ${idx+1} · ${v016SkillName(S.level)}`;S.resultTier='PERFECT';S.resultUntil=performance.now()+1500;
    }
  }
  S.skillUnlocked=S.level>=6;updateRunStatus()
};

attackMultiplier=function(){
  let mul=1+S.upgrades.atk*.08;
  if(S.playerClass==='knight'&&v016Has(6))mul+=.12;
  if(S.playerClass==='archer'&&v016Has(11))mul+=.10;
  return mul
};

maybeProcCrit=function(damage){
  let chance=S.upgrades.crit*.02;
  if(S.playerClass==='rogue'&&v016Has(11))chance+=.06;
  if(chance>0&&Math.random()<chance)return{damage:Math.round(damage*(1.5+S.upgrades.critdmg*.15)),proc:true};
  return{damage:Math.round(damage),proc:false}
};

knockMultiplier=function(p){
  let mul=1+S.upgrades.knock*.10;
  if(p.cls==='tank'&&v016Has(6))mul*=p.heavy&&v016Has(21)?2.0:1.30;
  if(p.cls==='knight'&&v016Has(16)&&p.hasPerfect)mul*=1.20;
  return mul
};

function v016ProjectileLife(cls,heavy=false){
  let life=cls==='rogue'?.16:cls==='tank'?.25:cls==='archer'?.14:cls==='mage'?.28:.19;
  if(cls==='archer'&&v016Has(11))life/=1.25;
  if(cls==='mage'&&heavy&&v016Has(21))life*=1.18;
  return life
}

function v016PushProjectile(obj){
  obj.x=obj.sx;obj.y=obj.sy;obj.age=obj.age??0;obj.rot=obj.rot??0;
  S.projectiles.push(obj);return obj
}

launchProjectile=function(owner,slot,cls,tier,damage,heavy=false,now=performance.now()){
  ensureMonsters();
  const start=weaponWorldPos(slot,cls),target=nearestMonster(),fallback={x:W*.96,y:start.y},end=target?monsterAimPoint(target):fallback;
  const life=v016ProjectileLife(cls,heavy);
  let proc=false,hasPerfect=owner==='local'&&v016ContainsPerfect();
  if(owner==='local'){
    let scaled=damage*attackMultiplier();
    if(cls==='knight'&&v016Has(16)&&hasPerfect)scaled*=1.18;
    if(cls==='knight'&&v016Has(21)&&heavy)scaled*=1.20;
    if(cls==='mage'&&v016Has(21)&&heavy)scaled*=1.20;
    const roll=maybeProcCrit(scaled);damage=roll.damage;proc=roll.proc;
  }else if(owner==='ai')damage=Math.round(damage*(1+(S.stage-1)*.035));

  const rank=owner==='local'?v016SkillCount():0;
  const main=v016PushProjectile({
    owner,slot,cls,tier,damage,heavy,procCrit:proc,hasPerfect,
    skillPower:owner==='local'&&rank>=1,v016SkillRank:rank,
    targetId:target?.id??null,sx:start.x,sy:start.y,tx:end.x,ty:end.y,life,
    armorIgnore:owner==='local'&&cls==='archer'&&v016Has(16)&&hasPerfect,
    pierceMax:owner==='local'&&cls==='archer'&&v016Has(6)?2:0,
    piercePreserve:owner==='local'&&cls==='archer'&&v016Has(16)&&hasPerfect,
    greaterBlade:owner==='local'&&cls==='knight'&&v016Has(21)&&heavy,
    groundImpact:owner==='local'&&cls==='tank'&&v016Has(21)&&heavy,
    greaterOrb:owner==='local'&&cls==='mage'&&v016Has(21)&&heavy
  });

  if(owner==='local'&&cls==='rogue'&&v016Has(6)){
    const followCount=heavy&&v016Has(21)?4:1;
    const followScale=heavy&&v016Has(21)?.45:.55;
    for(let i=0;i<followCount;i++){
      const delay=heavy&&v016Has(21)?.035*(i+1):.055;
      v016PushProjectile({owner:'skill',skillResolve:'rogue',slot,cls,tier:'SKILL',damage:Math.round(damage*followScale),heavy:false,procCrit:false,hasPerfect:false,
        skillPower:true,v016SkillRank:rank,targetId:target?.id??null,sx:start.x,sy:start.y+(i%2?8:-8),tx:end.x,ty:end.y+(i%2?5:-5),life:life+.025,age:-delay,isDagger:true});
    }
  }

  if(owner==='local'&&cls==='archer'&&heavy&&v016Has(21)){
    for(const off of [-11,11]){
      v016PushProjectile({owner:'skill',skillResolve:'archer',slot,cls,tier:'SKILL',damage:Math.round(damage*.65),heavy:true,procCrit:false,hasPerfect,
        skillPower:true,v016SkillRank:rank,targetId:target?.id??null,sx:start.x,sy:start.y+off,tx:end.x,ty:end.y+off,lineOffsetY:off,life:life+.018,
        armorIgnore:v016Has(16)&&hasPerfect,pierceMax:v016Has(6)?2:0,piercePreserve:v016Has(16)&&hasPerfect,tripleArrow:true});
    }
  }

  if(owner==='local'){
    S.phase='projectile';S.resultText=proc?`${tier}! · PROC CRIT`:(tier==='CRITICAL'?'CRITICAL!':tier+'!');S.resultTier=tier;S.resultUntil=now+420
  }
  return main
};

const v016BaseVisualImpact=visualImpact;
visualImpact=function(p,m,now,local){
  if(!m)return false;
  const d=MONSTER_TYPES[m.type],oldArmor=d.armor,oldKnock=d.knockResist,oldDamage=p.damage;
  try{
    if(p.armorIgnore)d.armor=1;
    if(m.boss)d.knockResist=oldKnock*.40;
    if(m.boss&&p.cls==='rogue')p.damage=Math.max(1,Math.round(oldDamage*.70));
    return v016BaseVisualImpact(p,m,now,local)
  }finally{
    d.armor=oldArmor;d.knockResist=oldKnock;p.damage=oldDamage
  }
};

function v016LineTargets(p,primary,maxCount){
  if(!primary||maxCount<=0)return[];
  const ax=p.sx,ay=p.sy,bx=p.tx,by=p.ty,dx=bx-ax,dy=by-ay,len2=dx*dx+dy*dy||1;
  const pa=monsterAimPoint(primary),pt=((pa.x-ax)*dx+(pa.y-ay)*dy)/len2;
  const out=[];
  for(const m of S.monsters){
    if(m.dead||m.id===primary.id)continue;
    const q=monsterAimPoint(m),t=((q.x-ax)*dx+(q.y-ay)*dy)/len2;
    if(t<=pt+.025)continue;
    const px=ax+t*dx,py=ay+t*dy,dist=Math.hypot(q.x-px,q.y-py);
    const md=MONSTER_TYPES[m.type],hitR=H*.042*md.size*(m.scaleMul||1);
    if(dist<=hitR)out.push({m,t})
  }
  out.sort((a,b)=>a.t-b.t);return out.slice(0,maxCount).map(x=>x.m)
}

function v016ArcherPierce(p,primary,now,local=true){
  const max=p.pierceMax||0;if(!primary||max<=0)return;
  const targets=v016LineTargets(p,primary,max);
  for(const other of targets){
    const dmg=p.piercePreserve?p.damage:Math.round(p.damage*.52);
    visualImpact({...p,damage:dmg,procCrit:false,hasPerfect:false},other,now,local);
    const a=monsterAimPoint(other);addFloat('PIERCE',a.x,a.y-42,11,'gain')
  }
}

function v016KnightPierce(p,primary,now){
  if(!primary||!v016Has(11))return;
  const max=p.heavy?(v016Has(21)?3:2):1;
  const yTol=H*(p.heavy?.19:.12),xTol=W*(p.heavy?.28:.20);
  const targets=S.monsters.filter(x=>!x.dead&&x.id!==primary.id&&x.x>=primary.x&&x.x-primary.x<=xTol&&Math.abs(x.y-primary.y)<=yTol).sort((a,b)=>a.x-b.x).slice(0,max);
  for(const other of targets){visualImpact({...p,damage:Math.round(p.damage*.85),procCrit:false},other,now,true);const a=monsterAimPoint(other);addFloat('BREAK',a.x,a.y-42,11,'gain')}
}

function v016TankGroundImpact(p,primary,now){
  if(!primary||!p.groundImpact)return;
  const targets=S.monsters.filter(x=>!x.dead&&x.id!==primary.id&&Math.abs(x.x-primary.x)<=W*.16&&Math.abs(x.y-primary.y)<=H*.19);
  for(const other of targets)visualImpact({...p,procCrit:false},other,now,true);
  if(targets.length){const a=monsterAimPoint(primary);addFloat('GROUND IMPACT',a.x,a.y-52,11,'gain')}
}

function v016MageBurst(p,primary,now){
  if(!primary||p.cls!=='mage'||!v016Has(6))return;
  let rx=W*.105,ry=H*.16,splash=.50;
  if(v016Has(11)){rx*=1.35;ry*=1.35;splash=.60}
  if(p.greaterOrb){rx*=1.60;ry*=1.60}
  const near=S.monsters.filter(x=>!x.dead&&x.id!==primary.id&&Math.abs(x.x-primary.x)<rx&&Math.abs(x.y-primary.y)<ry).slice(0,3);
  for(const other of near)visualImpact({...p,tier:'SKILL',damage:Math.round(p.damage*splash),procCrit:false,hasPerfect:false,armorIgnore:false},other,now,true);
  if(near.length){const a=monsterAimPoint(primary);S.pulses.push({x:a.x,y:a.y,age:0,life:.32,maxR:p.greaterOrb?142:105,rgb:classColor('mage')});addFloat('ARCANE BURST',a.x,a.y-50,11,'gain')}
  if(v016Has(16)&&p.hasPerfect){
    S.v016DelayedBlasts.push({at:now+180,x:primary.x,y:primary.y,excludeId:primary.id,rx,ry,damage:Math.round(p.damage*.55),source:{...p,tier:'SKILL',procCrit:false,hasPerfect:false,armorIgnore:false}})
  }
}

function v016GrantTankShield(now){S.v016WallShield=80;S.v016WallShieldUntil=now+3000}
function v016ResolveDelayed(now){
  if(!S.v016DelayedBlasts.length)return;
  const keep=[];
  for(const b of S.v016DelayedBlasts){
    if(now<b.at){keep.push(b);continue}
    const targets=S.monsters.filter(m=>!m.dead&&m.id!==b.excludeId).map(m=>{const nx=(m.x-b.x)/b.rx,ny=(m.y-b.y)/b.ry;return{m,d:Math.hypot(nx,ny)}}).filter(x=>x.d>=.32&&x.d<=1.05).sort((a,b)=>a.d-b.d).slice(0,4);
    for(const {m} of targets)visualImpact({...b.source,damage:b.damage},m,now,true);
    S.pulses.push({x:b.x,y:b.y,age:0,life:.35,maxR:128,rgb:classColor('mage')});if(targets.length)addFloat('RESONANCE',b.x,b.y-58,11,'gain')
  }
  S.v016DelayedBlasts=keep
}

resolveLocalHit=function(p,now){
  let m=getMonster(p.targetId)||nearestMonster();if(m)visualImpact(p,m,now,true);
  if(m&&p.cls==='knight')v016KnightPierce(p,m,now);
  if(m&&p.cls==='tank')v016TankGroundImpact(p,m,now);
  if(m&&p.cls==='archer')v016ArcherPierce(p,m,now,true);
  if(m&&p.cls==='mage')v016MageBurst(p,m,now);
  const critical=p.tier==='CRITICAL',perfect=critical||p.tier==='PERFECT'||p.tier==='SUPER',good=perfect||p.tier==='GOOD'||p.tier==='GREAT';
  S.hitStopUntil=now+(critical?90:perfect?55:good?28:8);
  if(isHeavy())S.charge=0;else{S.charge=Math.min(3,S.charge+1);spawnChargeMotes(S.charge,m)}
  const gainXP=xpForTier(p.tier);awardXP(gainXP);addFloat(`EXP +${gainXP}`,W*.08,H*.82,12,'gain');
  if(S.xJudge==='NORMAL')S.stats.normal++;if(S.xJudge==='GOOD')S.stats.good++;if(S.xJudge==='PERFECT')S.stats.perfect++;
  if(S.yJudge){if(S.yJudge==='NORMAL')S.stats.normal++;if(S.yJudge==='GOOD')S.stats.good++;if(S.yJudge==='PERFECT')S.stats.perfect++}
  if(critical)S.stats.critical++;
  S.stats.cycleDurations.push((now-S.lastAttackStart)/1000);if(S.stats.cycleDurations.length>50)S.stats.cycleDurations.shift();updateStats();
  if(S.playerClass==='tank'&&v016Has(16)&&p.hasPerfect)v016GrantTankShield(now);
  S.v016RecoverMs=(S.playerClass==='rogue'&&v016Has(16)&&p.hasPerfect)?312:390;
  S.phase='recover';S.phaseStart=now
};

function v016ResolveSkillHit(p,now){const m=getMonster(p.targetId)||nearestMonster();if(!m)return;visualImpact(p,m,now,true);if(p.skillResolve==='archer')v016ArcherPierce(p,m,now,true)}

update=function(now,dt){
  if(S.gameOver||S.runComplete){for(const p of S.particles){p.age+=dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=420*dt}S.particles=S.particles.filter(p=>p.age<p.life);for(const f of S.floats)f.age+=dt;S.floats=S.floats.filter(f=>f.age<f.life);return}
  if(S.stageMode==='shop'){document.getElementById('shopTimer').textContent=performance.now()<S.shopInputUnlockAt?'입력 보호 중…':'NEXT 버튼으로 진행';return}
  if(S.v016WallShield>0&&now>=S.v016WallShieldUntil)S.v016WallShield=0;v016ResolveDelayed(now);
  if(S.pendingTap&&(S.phase==='x'||S.phase==='y')&&(now-S.phaseStart)>=cfg.inputLockMs){S.pendingTap=false;handleTap(now)}
  if((S.phase==='x'||S.phase==='y')&&(now-S.phaseStart)>cfg.oneWayMs[cfg.speed]*cfg.maxCycles*2){S.resultText='MISS';S.resultTier='MISS';S.resultUntil=now+320;S.phase='recover';S.phaseStart=now}
  for(const ai of S.ai)if(now>=ai.nextAt)aiAttack(ai,now);
  if(now>=S.nextSpawnAt&&S.spawnedThisStage<S.stageTarget&&S.monsters.filter(m=>!m.dead).length<10){spawnMonster();S.spawnedThisStage++;S.nextSpawnAt=now+stagePlan(S.stage).gap+rand(-120,160)}
  for(const m of S.monsters){
    if(m.dead)continue;const d=MONSTER_TYPES[m.type];m.age+=dt;m.hitFlash*=Math.pow(.002,dt);m.x-=W*d.speed*dt*(1+(S.stage-1)*.018);
    if(m.type==='flyer')m.y=clamp(m.baseY+Math.sin(m.age*5.0)*H*.020,m.minY,m.maxY);else if(m.type==='runner')m.y=clamp(m.baseY+Math.sin(m.age*8.5)*H*.005,m.minY,m.maxY);else m.y=clamp(m.y,m.minY,m.maxY);
    if(m.x<=wallFrontX()){
      m.dead=true;const defense=clamp(S.upgrades.def*.025,0,.60),ironWall=(S.playerClass==='tank'&&v016Has(11))?.10:0;
      let incoming=Math.max(1,Math.round(d.baseDamage*(m.boss?1.45:1)*(1-defense)*(1-ironWall))),absorbed=0;
      if(S.v016WallShield>0&&now<S.v016WallShieldUntil){absorbed=Math.min(incoming,S.v016WallShield);S.v016WallShield-=absorbed;incoming-=absorbed;if(absorbed)addFloat(`GUARD ${absorbed}`,wallFrontX()+W*.012,m.y-18,14,'gain')}
      if(incoming>0){S.baseHp=Math.max(0,S.baseHp-incoming);addFloat(`-${incoming}`,wallFrontX()+W*.012,m.y,18,'damage')}
      addParticles(wallFrontX()+W*.006,m.y,6,1,classColor('tank'),absorbed>0);if(S.baseHp<=0){S.gameOver=true;S.stageMode='gameover';S.resultText='GAME OVER';S.resultTier='CRITICAL';S.resultUntil=now+999999}
    }
  }
  S.monsters=S.monsters.filter(m=>!m.dead||m.hitFlash>.02);
  for(const p of S.projectiles){
    if(p.age<0){p.age+=dt;continue}p.age+=dt;let target=getMonster(p.targetId);if(!target){target=nearestMonster();p.targetId=target?.id??null}
    if(target){const a=monsterAimPoint(target);p.tx=a.x;p.ty=a.y+(p.lineOffsetY||0)}
    if(p.age>=p.life){p.dead=true;if(p.owner==='local')resolveLocalHit(p,now);else if(p.owner==='skill')v016ResolveSkillHit(p,now);else resolveAIHit(p,now)}
  }
  S.projectiles=S.projectiles.filter(p=>!p.dead);
  if(S.phase==='recover'&&now-S.phaseStart>(S.v016RecoverMs||390)){S.v016RecoverMs=390;S.attackNo++;S.lastAttackStart=now;startAttack(now)}
  const alive=S.monsters.some(m=>!m.dead);
  if(S.spawnedThisStage>=S.stageTarget&&!alive&&S.projectiles.length===0){if(!S.stageClearPendingAt)S.stageClearPendingAt=now+650;if(now>=S.stageClearPendingAt){if(S.stage>=10)finishRun(now);else beginShop(now)}}else S.stageClearPendingAt=0;
  S.playerKick*=Math.pow(.001,dt);S.flash*=Math.pow(.001,dt);
  for(const p of S.particles){p.age+=dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=420*dt}S.particles=S.particles.filter(p=>p.age<p.life);
  for(const f of S.floats)f.age+=dt;S.floats=S.floats.filter(f=>f.age<f.life);for(const p of S.pulses)p.age+=dt;S.pulses=S.pulses.filter(p=>p.age<p.life);
  for(const m of S.chargeMotes){m.age+=dt;if(m.age<0)continue;const t=clamp(m.age/m.life,0,1),e=easeOutCubic(t),u=1-e,mx=(m.sx+m.tx)/2+m.bend,my=(m.sy+m.ty)/2-34;m.x=u*u*m.sx+2*u*e*mx+e*e*m.tx;m.y=u*u*m.sy+2*u*e*my+e*e*m.ty}S.chargeMotes=S.chargeMotes.filter(m=>m.age<m.life)
};
