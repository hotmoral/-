// Timing Defense v0.17 — UX continuity + AI internal growth parity candidate
(function(){
  const V017_SLOT_Y=[.285,.405,.525,.645];
  charBase=function(slot){return{x:W*.105,y:H*(V017_SLOT_Y[slot]??V017_SLOT_Y[0]),scale:.41}};

  const baseDrawTimingSquare=drawTimingSquare;
  drawTimingSquare=function(now){
    const inactive=S.stageMode==='combat'&&!S.gameOver&&!S.runComplete&&S.phase!=='x'&&S.phase!=='y';
    if(!inactive){baseDrawTimingSquare(now);return}
    const old=S.lockedCrossUntil;
    if(now>S.lockedCrossUntil)S.lockedCrossUntil=now+1;
    ctx.save();ctx.globalAlpha*=.42;baseDrawTimingSquare(now);ctx.restore();
    S.lockedCrossUntil=old
  };

  const AI_TIMING={pN:.28,pG:.54,pP:.18};
  function aiJudge(){const r=Math.random();return r<AI_TIMING.pN?'NORMAL':r<AI_TIMING.pN+AI_TIMING.pG?'GOOD':'PERFECT'}
  function aiSkillCount(level){return V016_UNLOCKS.filter(v=>level>=v).length}
  function aiHas(ai,lv){return (ai.level||1)>=lv}
  function awardAiXP(ai,amount){
    if(S.stageMode!=='combat')return;
    ai.xp=(ai.xp||0)+amount;ai.xpNeed=ai.xpNeed||60;ai.level=ai.level||1;
    while(ai.xp>=ai.xpNeed){ai.xp-=ai.xpNeed;ai.level++;ai.xpNeed=levelNeed(ai.level)}
  }
  function aiLife(cls,heavy,level){
    let life=cls==='rogue'?.16:cls==='tank'?.25:cls==='archer'?.14:cls==='mage'?.28:.19;
    if(cls==='archer'&&level>=11)life/=1.25;
    if(cls==='mage'&&heavy&&level>=21)life*=1.18;
    return life
  }
  function aiKnockBase(tier){return tier==='CRITICAL'?.011:(tier==='PERFECT'||tier==='SUPER')?.007:(tier==='GOOD'||tier==='GREAT')?.004:.002}
  function aiExtraKnock(m,p,mul){
    if(!m||!m.alive||mul<=1)return;
    const d=MONSTER_TYPES[m.type],boss=m.boss?.40:1;
    m.x=Math.min(W*.985,m.x+aiKnockBase(p.tier)*d.knockResist*boss*(mul-1)*W)
  }

  const baseMakeAI=makeAI;
  makeAI=function(){
    baseMakeAI();
    for(const ai of S.ai){ai.level=1;ai.xp=0;ai.xpNeed=60;ai.lastJudge='NORMAL';ai.lastHasPerfect=false}
  };

  function pushAiFollowProjectile(obj){obj.x=obj.sx;obj.y=obj.sy;obj.age=obj.age??0;obj.rot=obj.rot??0;S.projectiles.push(obj);return obj}

  function aiLaunch(ai,tier,damage,heavy,hasPerfect,now){
    const level=ai.level||1,cls=ai.cls;
    let scaled=damage;
    if(cls==='knight'&&level>=6)scaled*=1.12;
    if(cls==='archer'&&level>=11)scaled*=1.10;
    if(cls==='knight'&&level>=16&&hasPerfect)scaled*=1.18;
    if(cls==='knight'&&level>=21&&heavy)scaled*=1.20;
    if(cls==='mage'&&level>=21&&heavy)scaled*=1.20;

    const main=launchProjectile('ai',ai.slot,cls,tier,scaled,heavy,now);
    if(!main)return null;
    main.actorLevel=level;main.hasPerfect=hasPerfect;main.skillPower=level>=6;main.v016SkillRank=aiSkillCount(level);main.life=aiLife(cls,heavy,level);
    main.armorIgnore=cls==='archer'&&level>=16&&hasPerfect;
    main.pierceMax=cls==='archer'&&level>=6?2:0;
    main.piercePreserve=cls==='archer'&&level>=16&&hasPerfect;
    main.greaterBlade=cls==='knight'&&level>=21&&heavy;
    main.groundImpact=cls==='tank'&&level>=21&&heavy;
    main.greaterOrb=cls==='mage'&&level>=21&&heavy;
    main.lockLine=cls==='archer';

    if(cls==='rogue'&&level>=11&&Math.random()<.06){main.damage=Math.round(main.damage*1.5);main.procCrit=true}

    const start={x:main.sx,y:main.sy},end={x:main.tx,y:main.ty};
    if(cls==='rogue'&&level>=6){
      const count=heavy&&level>=21?4:1,scale=heavy&&level>=21?.45:.55;
      for(let i=0;i<count;i++)pushAiFollowProjectile({owner:'ai',aiSkill:'rogue',slot:ai.slot,cls,tier:'SKILL',damage:Math.round(main.damage*scale),heavy:false,procCrit:false,hasPerfect:false,skillPower:true,actorLevel:level,targetId:main.targetId,sx:start.x,sy:start.y+(i%2?8:-8),tx:end.x,ty:end.y+(i%2?5:-5),life:main.life+.025,age:heavy?.035*(i+1)*-1:-.055,isDagger:true});
    }
    if(cls==='archer'&&heavy&&level>=21){
      for(const off of [-11,11])pushAiFollowProjectile({owner:'ai',aiSkill:'archer',slot:ai.slot,cls,tier:'SKILL',damage:Math.round(main.damage*.65),heavy:true,procCrit:false,hasPerfect,skillPower:true,actorLevel:level,targetId:main.targetId,sx:start.x,sy:start.y+off,tx:end.x,ty:end.y+off,lineOffsetY:off,life:main.life+.018,armorIgnore:level>=16&&hasPerfect,pierceMax:level>=6?2:0,piercePreserve:level>=16&&hasPerfect,tripleArrow:true,lockLine:true});
    }
    return main
  }

  aiAttack=function(ai,now){
    ai.shotNo++;ai.shots++;
    const heavy=ai.charge>=3;
    let tier,damage,hasPerfect=false;
    if(heavy){
      const x=aiJudge(),y=aiJudge(),res=strongResult(x,y);tier=res[0];damage=res[1];hasPerfect=x==='PERFECT'||y==='PERFECT';ai.charge=0
    }else{
      tier=aiJudge();damage=baseDamage(tier);hasPerfect=tier==='PERFECT';ai.charge++
    }
    ai.lastJudge=tier;ai.lastHasPerfect=hasPerfect;
    aiLaunch(ai,tier,damage,heavy,hasPerfect,now);
    awardAiXP(ai,xpForTier(tier));
    let wait=aiInterval(ai.cls)+rand(-140,170);
    if(ai.cls==='rogue'&&aiHas(ai,16)&&hasPerfect)wait*=.80;
    ai.nextAt=now+wait
  };

  function aiKnightPierce(p,primary,now){
    const level=p.actorLevel||1;if(!primary||level<11)return;
    const max=p.heavy?(level>=21?3:2):1,yTol=H*(p.heavy?.19:.12),xTol=W*(p.heavy?.28:.20),km=level>=16&&p.hasPerfect?1.20:1;
    const targets=S.monsters.filter(x=>!x.dead&&x.id!==primary.id&&x.x>=primary.x&&x.x-primary.x<=xTol&&Math.abs(x.y-primary.y)<=yTol).sort((a,b)=>a.x-b.x).slice(0,max);
    for(const m of targets){visualImpact({...p,damage:Math.round(p.damage*.85),procCrit:false},m,now,false);aiExtraKnock(m,p,km)}
  }
  function aiTankGround(p,primary,now){
    const level=p.actorLevel||1;if(!primary||level<21||!p.groundImpact)return;
    const targets=S.monsters.filter(x=>!x.dead&&x.id!==primary.id&&Math.abs(x.x-primary.x)<=W*.16&&Math.abs(x.y-primary.y)<=H*.19);
    for(const m of targets){visualImpact({...p,procCrit:false},m,now,false);aiExtraKnock(m,p,2.0)}
  }
  function aiMageBurst(p,primary,now){
    const level=p.actorLevel||1;if(!primary||level<6)return;
    let rx=W*.105,ry=H*.16,splash=.50;if(level>=11){rx*=1.35;ry*=1.35;splash=.60}if(p.greaterOrb){rx*=1.60;ry*=1.60}
    const near=S.monsters.filter(x=>!x.dead&&x.id!==primary.id&&Math.abs(x.x-primary.x)<rx&&Math.abs(x.y-primary.y)<ry).slice(0,3);
    for(const m of near)visualImpact({...p,tier:'SKILL',damage:Math.round(p.damage*splash),procCrit:false,hasPerfect:false,armorIgnore:false},m,now,false);
    if(level>=16&&p.hasPerfect){S.v017AiDelayedBlasts.push({at:now+180,x:primary.x,y:primary.y,excludeId:primary.id,rx,ry,damage:Math.round(p.damage*.55),source:{...p,tier:'SKILL',procCrit:false,hasPerfect:false,armorIgnore:false}})}
  }
  function resolveAiDelayed(now){
    if(!S.v017AiDelayedBlasts?.length)return;const keep=[];
    for(const b of S.v017AiDelayedBlasts){
      if(now<b.at){keep.push(b);continue}
      const targets=S.monsters.filter(m=>!m.dead&&m.id!==b.excludeId).map(m=>{const nx=(m.x-b.x)/b.rx,ny=(m.y-b.y)/b.ry;return{m,d:Math.hypot(nx,ny)}}).filter(x=>x.d>=.32&&x.d<=1.05).sort((a,b)=>a.d-b.d).slice(0,4);
      for(const {m} of targets)visualImpact({...b.source,damage:b.damage},m,now,false)
    }
    S.v017AiDelayedBlasts=keep
  }
  S.v017AiDelayedBlasts=[];

  resolveAIHit=function(p,now){
    let m=p.cls==='archer'&&p.lockLine?v016ArcherPrimary(p):(getMonster(p.targetId)||nearestMonster());if(!m)return;
    visualImpact(p,m,now,false);
    const level=p.actorLevel||1;
    if(p.cls==='knight')aiKnightPierce(p,m,now);
    if(p.cls==='tank'){
      const km=level>=6?(p.heavy&&level>=21?2.0:1.30):1;aiExtraKnock(m,p,km);aiTankGround(p,m,now)
    }
    if(p.cls==='knight'&&level>=16&&p.hasPerfect)aiExtraKnock(m,p,1.20);
    if(p.cls==='archer')v016ArcherPierce(p,m,now,false);
    if(p.cls==='mage')aiMageBurst(p,m,now)
  };

  const baseUpdate=update;
  update=function(now,dt){
    const localIron=S.playerClass==='tank'&&v016Has(11),aiIron=S.ai.some(ai=>ai.cls==='tank'&&(ai.level||1)>=11),apply=aiIron&&!localIron;
    let saved=null;
    if(apply){saved={};for(const [k,d] of Object.entries(MONSTER_TYPES)){saved[k]=d.baseDamage;d.baseDamage*=.90}}
    try{baseUpdate(now,dt)}finally{if(saved)for(const [k,v] of Object.entries(saved))MONSTER_TYPES[k].baseDamage=v}
    if(S.stageMode==='combat')resolveAiDelayed(now)
  };

  const baseAiAttack=aiAttack;
  aiAttack=function(ai,now){
    baseAiAttack(ai,now);
    if(ai.cls==='tank'&&aiHas(ai,16)&&ai.lastHasPerfect)v016GrantTankShield(now)
  };

  const v017Reset=reset;
  reset=function(){v017Reset();S.v017AiDelayedBlasts=[]};
})();
