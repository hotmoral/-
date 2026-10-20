// Timing Defense v0.18 — experimental passive basic attack + PERFECT combo rewards.
// Candidate values from v8: passive 40/2.0s, ordinary HP +10%, combo +5/8/12/15%.
(function(){
  const AUTO_DAMAGE=40;
  const AUTO_INTERVAL_MS=2000;
  const ORDINARY_HP_MUL=1.10;

  function comboBonusFor(c){
    if(c>=30)return .15;
    if(c>=20)return .12;
    if(c>=10)return .08;
    if(c>=5)return .05;
    return 0;
  }
  function predictedComboAtLaunch(){
    if(isHeavy())return S.yJudge==='PERFECT'?(S.v018Combo||0)+1:0;
    return S.xJudge==='PERFECT'?(S.v018Combo||0)+1:0;
  }

  const baseLaunchProjectile=launchProjectile;
  launchProjectile=function(owner,slot,cls,tier,damage,heavy=false,now=performance.now()){
    if(owner==='local'){
      const predicted=predictedComboAtLaunch();
      const bonus=comboBonusFor(predicted);
      if(bonus>0)damage=Math.round(damage*(1+bonus));
    }
    return baseLaunchProjectile(owner,slot,cls,tier,damage,heavy,now)
  };

  const baseSpawnMonster=spawnMonster;
  spawnMonster=function(type=null,xOverride=null,yOverride=null){
    const m=baseSpawnMonster(type,xOverride,yOverride);
    if(m&&!m.boss&&!m.v018HpAdjusted){
      m.hp=Math.round(m.hp*ORDINARY_HP_MUL);
      m.maxHp=Math.round(m.maxHp*ORDINARY_HP_MUL);
      m.v018HpAdjusted=true;
    }
    return m
  };

  function passiveLife(cls){return cls==='rogue'?.16:cls==='tank'?.25:cls==='archer'?.14:cls==='mage'?.28:.19}
  function firePassive(now){
    const target=nearestMonster();if(!target)return false;
    const cls=S.playerClass,start=weaponWorldPos(0,cls),end=monsterAimPoint(target);
    v016PushProjectile({owner:'passive',passive:true,slot:0,cls,tier:'AUTO',damage:AUTO_DAMAGE,heavy:false,procCrit:false,hasPerfect:false,
      skillPower:false,v016SkillRank:0,actorLevel:1,targetId:target.id,sx:start.x,sy:start.y,tx:end.x,ty:end.y,
      life:passiveLife(cls),armorIgnore:false,pierceMax:0,piercePreserve:false,lockLine:cls==='archer'});
    return true
  }

  const baseVisualImpact=visualImpact;
  visualImpact=function(p,m,now,local){
    if(p&&p.passive&&m){
      const d=MONSTER_TYPES[m.type],old=d.knockResist;d.knockResist=0;
      try{return baseVisualImpact(p,m,now,true)}finally{d.knockResist=old}
    }
    return baseVisualImpact(p,m,now,local)
  };

  const baseResolveAIHit=resolveAIHit;
  resolveAIHit=function(p,now){
    if(p&&p.passive){
      const m=p.cls==='archer'&&p.lockLine?v016ArcherPrimary(p):(getMonster(p.targetId)||nearestMonster());
      if(m)visualImpact(p,m,now,true);
      return
    }
    return baseResolveAIHit(p,now)
  };

  function rewardTier(m){return m>=30?'CRITICAL':m>=20?'SUPER':m>=10?'PERFECT':'GOOD'}
  function rewardBudget(m){return m>=30?210:m>=20?150:m>=10?90:60}
  function pushComboProjectile(obj){
    obj.owner='skill';obj.skillPower=false;obj.v016SkillRank=0;obj.procCrit=false;obj.hasPerfect=false;obj.age=obj.age??0;
    return v016PushProjectile(obj)
  }
  function comboTarget(){return nearestMonster()}
  function comboBaseProjectile(cls,tier,damage,target,age=0,extra={}){
    const start=weaponWorldPos(0,cls),end=target?monsterAimPoint(target):{x:W*.96,y:start.y};
    return {slot:0,cls,tier,damage,heavy:false,targetId:target?.id??null,sx:start.x,sy:start.y,tx:end.x,ty:end.y,
      life:passiveLife(cls)+.035,age,comboReward:true,...extra}
  }
  function triggerComboReward(milestone,now){
    const target=comboTarget();if(!target)return;
    const cls=S.playerClass,budget=rewardBudget(milestone),tier=rewardTier(milestone);
    const label=milestone>=30?`${milestone} COMBO!`:`COMBO ${milestone}`;
    const g=squareGeom();addFloat(label,g.x+g.size*.46,g.y-42,milestone>=30?20:milestone>=20?17:14,'gain');

    if(cls==='rogue'){
      const count=milestone>=30?5:milestone>=20?4:milestone>=10?3:2;
      const per=Math.max(1,Math.round(budget/count));
      for(let i=0;i<count;i++)pushComboProjectile(comboBaseProjectile(cls,tier,per,target,-.035*i,{comboKind:'rogue'}));
      return
    }
    if(cls==='knight'){
      pushComboProjectile(comboBaseProjectile(cls,tier,Math.round(budget*.67),target,0,{comboKind:'knight',comboBudget:budget}));return
    }
    if(cls==='tank'){
      pushComboProjectile(comboBaseProjectile(cls,tier,Math.round(budget*.60),target,0,{comboKind:'tank',comboBudget:budget}));return
    }
    if(cls==='archer'){
      pushComboProjectile(comboBaseProjectile(cls,tier,Math.round(budget*.70),target,0,{comboKind:'archer',comboBudget:budget,lockLine:true}));return
    }
    pushComboProjectile(comboBaseProjectile(cls,tier,Math.round(budget*.55),target,0,{comboKind:'mage',comboBudget:budget}));
  }

  const baseResolveSkillHit=v016ResolveSkillHit;
  v016ResolveSkillHit=function(p,now){
    if(!p?.comboReward)return baseResolveSkillHit(p,now);
    let m=p.cls==='archer'&&p.lockLine?v016ArcherPrimary(p):(getMonster(p.targetId)||nearestMonster());if(!m)return;
    visualImpact(p,m,now,true);
    const budget=p.comboBudget||p.damage;

    if(p.comboKind==='knight'){
      const candidates=S.monsters.filter(x=>!x.dead&&x.id!==m.id&&x.x>=m.x&&x.x-m.x<=W*.20&&Math.abs(x.y-m.y)<=H*.13).sort((a,b)=>a.x-b.x);
      if(candidates[0])visualImpact({...p,damage:Math.max(1,Math.round(budget*.33)),procCrit:false},candidates[0],now,true)
    }else if(p.comboKind==='tank'){
      const near=S.monsters.filter(x=>!x.dead&&x.id!==m.id&&Math.abs(x.x-m.x)<=W*.13&&Math.abs(x.y-m.y)<=H*.16).slice(0,2);
      for(const q of near)visualImpact({...p,damage:Math.max(1,Math.round(budget*.20)),procCrit:false},q,now,true)
    }else if(p.comboKind==='archer'){
      const line=v016LineTargets(p,m,1);
      if(line[0])visualImpact({...p,damage:Math.max(1,Math.round(budget*.30)),procCrit:false},line[0],now,true)
    }else if(p.comboKind==='mage'){
      const near=S.monsters.filter(x=>!x.dead&&x.id!==m.id&&Math.abs(x.x-m.x)<=W*.12&&Math.abs(x.y-m.y)<=H*.17).slice(0,3);
      for(const q of near)visualImpact({...p,damage:Math.max(1,Math.round(budget*.15)),procCrit:false},q,now,true)
    }
  };

  const baseResolveLocalHit=resolveLocalHit;
  resolveLocalHit=function(p,now){
    baseResolveLocalHit(p,now);
    if(S.v018PendingMilestones?.length){
      const list=S.v018PendingMilestones.splice(0);
      for(const m of list)triggerComboReward(m,now)
    }
  };

  function initAuto(clear=false){
    if(clear||typeof S.v018AutoNextAt!=='number')S.v018AutoNextAt=performance.now()+AUTO_INTERVAL_MS;
  }
  initAuto(false);

  const baseUpdate=update;
  update=function(now,dt){
    baseUpdate(now,dt);
    if(S.stageMode!=='combat'||S.gameOver||S.runComplete)return;
    if(now>=S.v018AutoNextAt){
      if(firePassive(now))S.v018AutoNextAt=now+AUTO_INTERVAL_MS;
      else S.v018AutoNextAt=now+250;
    }
  };

  const baseReset=reset;
  reset=function(){baseReset();initAuto(true)};
})();
