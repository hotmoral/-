// Timing Defense Cloudflare v0.35 cf.7 — Rogue charge stability + remote human timing projectile parity.
// Presentation only. No combat/balance/server-authority values are changed.
(function(){
  const mp=window.__TDMP34CF;
  if(!mp)return;

  const priorTimingSquare=drawTimingSquare;
  drawTimingSquare=function(now){
    if(S.playerClass!=='rogue')return priorTimingSquare(now);
    const priorClassColor=classColor;
    classColor=function(c){return priorClassColor(c==null?'rogue':c)};
    try{return priorTimingSquare(now)}finally{classColor=priorClassColor}
  };

  const humanTimingShots=new Map();
  function absorbRemoteHumanTimingShots(){
    if(!Array.isArray(mp.remoteShots)||!mp.remoteShots.length)return;
    const keep=[];
    for(const s of mp.remoteShots){
      if(s?.type==='hit'){
        if(!humanTimingShots.has(s.id))humanTimingShots.set(s.id,{...s,impacted:false});
      }else keep.push(s);
    }
    mp.remoteShots=keep;
  }
  function isHeavyTier(tier){return /^(HEAVY|HEAVY\+|GREAT|SUPER|CRITICAL)$/.test(tier||'')}
  function remoteLevelForVisualSlot(visualSlot){
    const vp=mp.visualParty?.find?.(x=>x.slot===visualSlot);
    if(!vp)return 1;
    return mp.state?.run?.players?.find?.(p=>p.slot===vp.roomSlot)?.level||1;
  }
  function impactRemoteHumanTimingShot(s){
    if(s.impacted)return;s.impacted=true;
    const m=typeof getMonster==='function'?getMonster(s.targetId):null;
    const a=m?monsterAimPoint(m):{x:s.tx,y:s.ty};
    if(m)m.hitFlash=1;
    addParticles(a.x,a.y,5,1);
    S.pulses.push({x:a.x,y:a.y,age:0,life:.20,maxR:58});
    addFloat(String(s.damage||0),a.x,a.y-H*.035,24,'damage');
  }
  function drawRemoteHumanTimingShots(){
    if(!humanTimingShots.size)return;
    const now=performance.now(),visuals=[],done=[];
    for(const [id,s] of humanTimingShots){
      const lifeMs=Math.max(1,s.life||180),elapsed=Math.max(0,now-s.started),t=Math.min(1,elapsed/lifeMs);
      const m=typeof getMonster==='function'?getMonster(s.targetId):null;
      const aim=m?monsterAimPoint(m):{x:s.tx,y:s.ty};
      s.tx=aim.x;s.ty=aim.y;
      const level=remoteLevelForVisualSlot(s.slot),heavy=isHeavyTier(s.tier);
      visuals.push({
        owner:'local',slot:s.slot,cls:s.cls,tier:s.tier||'NORMAL',damage:s.damage||0,heavy,
        skillPower:level>=6,targetId:s.targetId,sx:s.sx,sy:s.sy,tx:s.tx,ty:s.ty,
        x:s.sx,y:s.sy,age:elapsed/1000,life:lifeMs/1000,rot:t*Math.PI*2
      });
      if(t>=1){impactRemoteHumanTimingShot(s);done.push(id)}
    }
    if(visuals.length){
      const saved=S.projectiles;
      S.projectiles=visuals;
      try{drawProjectiles()}finally{S.projectiles=saved}
    }
    for(const id of done)humanTimingShots.delete(id);
  }

  const priorDraw=draw;
  draw=function(now){
    absorbRemoteHumanTimingShots();
    const out=priorDraw(now);
    drawRemoteHumanTimingShots();
    return out
  };
})();
