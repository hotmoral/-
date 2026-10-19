const canvas=document.getElementById('game'),ctx=canvas.getContext('2d'),attackLabelEl=document.getElementById('attackLabel'),statsEl=document.getElementById('stats');
let DPR=Math.max(1,Math.min(2.2,devicePixelRatio||1)),W=0,H=0;
function resize(){W=innerWidth;H=innerHeight;canvas.width=Math.floor(W*DPR);canvas.height=Math.floor(H*DPR);canvas.style.width=W+'px';canvas.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0)}addEventListener('resize',resize,{passive:true});resize();
const cfg={speed:'normal',oneWayMs:{slow:1350,normal:1100,fast:900},inputLockMs:100,maxCycles:3,goodW:.42,goodH:.42,perfectW:.17,perfectH:.17};
const SLOT_Y=[.30,.41,.52,.63];
const MONSTER_TYPES={
  grunt:{name:'GRUNT',hp:320,speed:.070,size:1.00,baseDamage:90,knockResist:.85,armor:1.00,reward:6},
  runner:{name:'RUNNER',hp:165,speed:.135,size:.70,baseDamage:60,knockResist:1.00,armor:1.00,reward:5},
  brute:{name:'BRUTE',hp:900,speed:.040,size:1.34,baseDamage:180,knockResist:.38,armor:1.00,reward:14},
  shield:{name:'SHIELD',hp:540,speed:.057,size:1.08,baseDamage:120,knockResist:.62,armor:.72,reward:10},
  flyer:{name:'FLYER',hp:225,speed:.100,size:.78,baseDamage:70,knockResist:.90,armor:1.00,reward:7}
};
const S={playerClass:'knight',teamSize:1,attackNo:1,charge:0,phase:'x',phaseStart:performance.now(),dirX:1,dirY:1,target:null,xPos:null,yPos:null,xJudge:null,yJudge:null,resultText:'',resultTier:'',resultUntil:0,lockedCrossUntil:0,hitStopUntil:0,shakeUntil:0,shakeMag:0,playerKick:0,monsterKick:0,monsterSquash:1,flash:0,xp:0,level:1,xpNeed:60,skillUnlocked:false,skillNoticeUntil:0,skillUnlockedStage:0,levelFlashUntil:0,lastXpGain:0,xpGainUntil:0,shopInputUnlockAt:0,gold:0,projectiles:[],particles:[],floats:[],pulses:[],chargeMotes:[],lastAttackStart:performance.now(),pendingTap:false,ai:[],monsters:[],nextMonsterId:1,nextSpawnAt:0,baseHp:2000,baseHpMax:2000,kills:0,gameOver:false,runComplete:false,stage:1,stageMode:'combat',stageTarget:0,spawnedThisStage:0,stageKills:0,shopEndAt:0,stageClearPendingAt:0,upgrades:{atk:0,crit:0,critdmg:0,hp:0,def:0,knock:0},stats:{normal:0,good:0,perfect:0,critical:0,cycleDurations:[]},errors:[]};
function rand(a,b){return a+Math.random()*(b-a)}function clamp(v,a,b){return Math.max(a,Math.min(b,v))}function easeOutCubic(t){return 1-Math.pow(1-t,3)}
function className(c=S.playerClass){return c==='knight'?'KNIGHT':c==='rogue'?'ROGUE':c==='tank'?'TANK':c==='archer'?'ARCHER':'MAGE'}function classColor(c=S.playerClass){if(c==='rogue')return'170,225,255';if(c==='tank')return'130,210,255';if(c==='archer')return'170,235,170';if(c==='mage')return'204,170,255';return'255,211,106'}function skillName(c=S.playerClass){return c==='knight'?'BLADE WAVE+':c==='rogue'?'DOUBLE DAGGER':c==='tank'?'IMPACT WAVE+':c==='archer'?'PIERCING ARROW':'ARCANE BURST'}function skillShort(c=S.playerClass){return c==='knight'?'BW+':c==='rogue'?'2D':c==='tank'?'IW+':c==='archer'?'PIERCE':'BURST'}function isHeavy(){return S.charge>=3}
function charBase(slot){return{x:W*.105,y:H*SLOT_Y[slot],scale:.41}}
function squareGeom(){const b=charBase(0),size=Math.min(H*.285,W*.115,145);return{size,x:b.x+W*.058,y:b.y-size*.42}}
function weaponWorldPos(slot=0,cls=S.playerClass){const b=charBase(slot),sc=b.scale;if(cls==='rogue')return{x:b.x+47*sc,y:b.y-18*sc};if(cls==='tank')return{x:b.x+46*sc,y:b.y-10*sc};if(cls==='archer')return{x:b.x+51*sc,y:b.y-20*sc};if(cls==='mage')return{x:b.x+45*sc,y:b.y-28*sc};return{x:b.x+53*sc,y:b.y-20*sc}}
function wallFrontX(){return W*.155}
function stagePlan(stage){
  const counts=[0,8,10,12,13,10,14,15,16,17,18];
  const gaps=[0,1120,1040,980,940,1080,900,860,820,780,760];
  return{count:counts[stage]||18,gap:gaps[stage]||760,bossLast:stage===5||stage===10};
}
function pickMonsterType(stage=S.stage,index=0){
  if((stage===5||stage===10)&&index===stagePlan(stage).count-1)return'brute';
  const r=Math.random();
  if(stage<=1)return'grunt';
  if(stage===2)return r<.62?'grunt':'runner';
  if(stage===3)return r<.44?'grunt':r<.78?'runner':'brute';
  if(stage===4)return r<.36?'grunt':r<.62?'runner':r<.82?'shield':'brute';
  if(stage<=6)return r<.27?'grunt':r<.48?'runner':r<.68?'shield':r<.86?'brute':'flyer';
  return r<.20?'grunt':r<.42?'runner':r<.62?'shield':r<.80?'flyer':'brute';
}
function safeSpawnY(type,scaleMul=1){
  const d=MONSTER_TYPES[type],osc=type==='flyer'?H*.024:0;
  const topMargin=82*d.size*scaleMul+osc+12;
  const minY=Math.max(H*.26,topMargin);
  const maxY=Math.min(H*.62,H-72);
  if(maxY<=minY)return H*.46;
  return rand(minY,maxY);
}
function spawnMonster(type=null,xOverride=null,yOverride=null){
  type=type||pickMonsterType(S.stage,S.spawnedThisStage);
  const d=MONSTER_TYPES[type],isBoss=(S.stage===5||S.stage===10)&&S.spawnedThisStage===stagePlan(S.stage).count-1;
  const scaleMul=isBoss?(S.stage===10?1.42:1.25):1;
  const hpScale=(1+(S.stage-1)*.13)*(isBoss?(S.stage===10?4.0:2.7):1);
  const margin=Math.max(68,W*.045)*d.size*scaleMul;
  const m={
    id:S.nextMonsterId++,type,boss:isBoss,scaleMul,
    x:xOverride??(W+margin+rand(0,W*.055)),
    y:yOverride??safeSpawnY(type,scaleMul),baseY:0,minY:0,maxY:0,
    hp:Math.round(d.hp*hpScale),maxHp:Math.round(d.hp*hpScale),
    age:0,hitFlash:0,dead:false
  };
  m.baseY=m.y;
  const osc=type==='flyer'?H*.024:0,d2=MONSTER_TYPES[type],topMargin=82*d2.size*scaleMul+osc+12;
  m.minY=Math.max(H*.26,topMargin);m.maxY=Math.min(H*.62,H-72);if(m.maxY<=m.minY){m.minY=H*.36;m.maxY=H*.56}
  m.baseY=clamp(m.baseY,m.minY,m.maxY);m.y=m.baseY;
  S.monsters.push(m);
  return m;
}
function getMonster(id){return S.monsters.find(m=>m.id===id&&!m.dead)}
function nearestMonster(){
  let best=null;
  for(const m of S.monsters){if(m.dead)continue;if(!best||m.x<best.x)best=m}
  return best;
}
function ensureMonsters(){
  if(S.stageMode!=='combat')return;
  if(S.monsters.some(m=>!m.dead))return;
  if(S.spawnedThisStage<S.stageTarget){spawnMonster();S.spawnedThisStage++}
}
function monsterAimPoint(m){
  const d=MONSTER_TYPES[m.type],sc=m.scaleMul||1;
  return{x:m.x-W*.012*d.size*sc,y:m.y-H*.035*d.size*sc};
}
const UPGRADE_META={
  atk:{name:'ATK',sub:'+8% damage / rank',mult:1.0},
  crit:{name:'CRIT',sub:'+2% proc chance / rank',mult:1.1},
  critdmg:{name:'CRIT DMG',sub:'+15% proc damage / rank',mult:1.0},
  hp:{name:'WALL HP',sub:'+100 max HP / rank',mult:.9},
  def:{name:'DEF',sub:'-2.5% wall damage / rank',mult:1.1},
  knock:{name:'KNOCKBACK',sub:'+10% / rank',mult:.9}
};
const BASE_COST=[40,65,100,145,200,265,340,425,520,625];
function upgradeCost(key){const r=S.upgrades[key];return r>=10?Infinity:Math.round(BASE_COST[r]*UPGRADE_META[key].mult)}
function levelNeed(level){return 60+12*(level-1)}
function awardXP(amount){
  if(S.stageMode!=='combat')return;
  S.lastXpGain=amount;S.xpGainUntil=performance.now()+650;S.xp+=amount;
  while(S.xp>=S.xpNeed){
    S.xp-=S.xpNeed;S.level++;S.xpNeed=levelNeed(S.level);S.levelFlashUntil=performance.now()+850;
    addFloat(`LEVEL ${S.level}`,squareGeom().x+squareGeom().size+30,squareGeom().y+18,20,'gain');
    if(S.level===6&&!S.skillUnlocked){
      S.skillUnlocked=true;S.skillUnlockedStage=S.stage;S.skillNoticeUntil=performance.now()+4200;
      S.resultText=`SKILL I · ${skillName()}`;S.resultTier='PERFECT';S.resultUntil=performance.now()+1500;
    }
  }
  updateRunStatus()
}
function xpForTier(tier){
  if(tier==='CRITICAL')return 28;
  if(tier==='SUPER')return 23;
  if(tier==='GREAT')return 18;
  if(tier==='HEAVY+')return 14;
  if(tier==='HEAVY')return 10;
  if(tier==='PERFECT')return 18;
  if(tier==='GOOD')return 12;
  return 8;
}
function attackMultiplier(){return 1+S.upgrades.atk*.08+(S.skillUnlocked&&S.playerClass==='knight'?.12:0)}
function knockMultiplier(p){return (1+S.upgrades.knock*.10)*(S.skillUnlocked&&p.cls==='tank'?1.30:1)}
function maybeProcCrit(damage){
  const chance=S.upgrades.crit*.02;
  if(chance>0&&Math.random()<chance){return{damage:Math.round(damage*(1.5+S.upgrades.critdmg*.15)),proc:true}}
  return{damage:Math.round(damage),proc:false}
}
function updateRunStatus(){
  const el=document.getElementById('runStatus');
  if(el)el.textContent=`STAGE ${S.stage}/10 · LV ${S.level} · EXP ${S.xp}/${S.xpNeed}${S.skillUnlocked?' · SKILL ON':''}`
}
function renderShop(){
  const grid=document.getElementById('upgradeGrid');if(!grid)return;
  grid.innerHTML='';
  for(const key of Object.keys(UPGRADE_META)){
    const meta=UPGRADE_META[key],rank=S.upgrades[key],cost=upgradeCost(key);
    const row=document.createElement('div');row.className='upgrade';
    const txt=document.createElement('div');txt.className='upgradeText';txt.innerHTML=`<div class="upgradeName">${meta.name} · R${rank}</div><div class="upgradeSub">${meta.sub}</div>`;
    const btn=document.createElement('button');btn.textContent=rank>=10?'MAX':`${cost} C`;btn.disabled=performance.now()<S.shopInputUnlockAt||rank>=10||S.gold<cost;
    btn.addEventListener('click',e=>{e.stopPropagation();buyUpgrade(key)});
    row.append(txt,btn);grid.append(row)
  }
  document.getElementById('shopCoin').textContent=`COIN ${S.gold}`;const sk=document.getElementById('shopSkill');if(sk)sk.textContent=S.skillUnlockedStage===S.stage?`이번 스테이지 습득 · SKILL I · ${skillName()}`:(S.skillUnlocked?`보유 스킬 · SKILL I · ${skillName()}`:'');const nb=document.getElementById('nextBtn');if(nb)nb.disabled=performance.now()<S.shopInputUnlockAt;
}
function buyUpgrade(key){
  if(S.stageMode!=='shop'||performance.now()<S.shopInputUnlockAt)return;const cost=upgradeCost(key);if(!isFinite(cost)||S.gold<cost)return;
  S.gold-=cost;S.upgrades[key]++;
  if(key==='hp'){S.baseHpMax+=100;S.baseHp=Math.min(S.baseHpMax,S.baseHp+100)}
  renderShop()
}
function startStage(stage,now=performance.now()){
  S.stage=stage;S.stageMode='combat';S.stageTarget=stagePlan(stage).count;S.spawnedThisStage=0;S.stageKills=0;S.monsters=[];S.projectiles=[];S.nextSpawnAt=now+650;S.stageClearPendingAt=0;
  document.getElementById('shop').classList.remove('show');
  S.resultText=`STAGE ${stage}`;S.resultTier='GOOD';S.resultUntil=now+900;startAttack(now);updateRunStatus();
}
function beginShop(now){
  if(S.stageMode!=='combat'||S.stage>=10)return;
  S.stageMode='shop';S.phase='idle';S.projectiles=[];S.shopInputUnlockAt=now+650;
  const reward=55+S.stage*12;S.gold+=reward;
  document.getElementById('shopStage').textContent=`Stage ${S.stage} clear · reward +${reward} coin`;
  document.getElementById('shopTimer').textContent='NEXT 버튼으로 진행';
  document.getElementById('shop').classList.add('show');renderShop();
  setTimeout(()=>{if(S.stageMode==='shop')renderShop()},700);
}
function finishRun(now){
  S.stageMode='clear';S.runComplete=true;S.phase='idle';S.projectiles=[];
  S.resultText='PROTOTYPE CLEAR';S.resultTier='CRITICAL';S.resultUntil=now+999999;updateRunStatus();
}
function nextStage(){if(S.stageMode!=='shop'||performance.now()<S.shopInputUnlockAt)return;startStage(S.stage+1,performance.now())}
function newTarget(){const m=.08,gx=rand(m+cfg.goodW/2,1-m-cfg.goodW/2),gy=rand(m+cfg.goodH/2,1-m-cfg.goodH/2),px=clamp(gx+rand(-.10,.10),gx-cfg.goodW/2+cfg.perfectW/2,gx+cfg.goodW/2-cfg.perfectW/2),py=clamp(gy+rand(-.10,.10),gy-cfg.goodH/2+cfg.perfectH/2,gy+cfg.goodH/2-cfg.perfectH/2);S.target={gx,gy,px,py}}
function startAttack(now){S.phase='x';S.phaseStart=now;S.dirX=S.attackNo%2?1:-1;S.dirY=S.attackNo%2?-1:1;S.xPos=S.yPos=null;S.xJudge=S.yJudge=null;S.pendingTap=false;newTarget();updateAttackLabel()}
function updateAttackLabel(){const suffix=isHeavy()?(S.phase==='x'?'HEAVY · X':S.phase==='y'?'HEAVY · Y':'HEAVY'):'NORMAL · X';attackLabelEl.textContent=`${className()} · ATTACK ${S.attackNo} · ${suffix}`}
function sweepPos(now,dir){const one=cfg.oneWayMs[cfg.speed],leg=Math.max(0,now-S.phaseStart)/one,whole=Math.floor(leg),f=leg-whole;let t=whole%2===0?f:1-f;if(dir<0)t=1-t;return .06+.88*t}
function judgeX(x){const t=S.target;if(Math.abs(x-t.px)<=cfg.perfectW/2)return'PERFECT';if(Math.abs(x-t.gx)<=cfg.goodW/2)return'GOOD';return'NORMAL'}function judgeY(y){const t=S.target;if(Math.abs(y-t.py)<=cfg.perfectH/2)return'PERFECT';if(Math.abs(y-t.gy)<=cfg.goodH/2)return'GOOD';return'NORMAL'}
function strongResult(x,y){if(x==='PERFECT'&&y==='PERFECT')return['CRITICAL',600];const w=(x==='PERFECT'?2:x==='GOOD'?1:0)+(y==='PERFECT'?2:y==='GOOD'?1:0);if(w>=3)return['SUPER',400];if(w===2)return['GREAT',300];if(w===1)return['HEAVY+',230];return['HEAVY',180]}function baseDamage(j){return j==='PERFECT'?200:j==='GOOD'?140:100}
function addFloat(text,x,y,size=25,kind='damage'){S.floats.push({text,x,y,size,kind,age:0,life:kind==='critical'?.70:.50})}function addParticles(x,y,count,scale=1){for(let i=0;i<count;i++){const a=rand(-Math.PI*.8,Math.PI*.8),sp=rand(70,220)*scale;S.particles.push({x,y,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp-rand(10,80),age:0,life:rand(.24,.48),size:rand(2,5)*scale})}}