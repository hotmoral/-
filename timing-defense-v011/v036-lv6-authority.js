// Timing Defense Cloudflare v0.36 Slice A — Lv6 authoritative skill-event presentation.
// Damage/state remain server authoritative. This layer renders authoritative secondary skill events.
(function(){
  const mp=window.__TDMP34CF;
  if(!mp)return;

  let floor=Number(mp.lastEvent)||0,runId='';
  const shots=[];
  const bursts=[];

  // Network authority rule: legacy v0.16 creates Rogue's second dagger locally.
  // Remove only that newly-created network-mode secondary projectile so it cannot
  // execute local visualImpact() and transiently mutate HP/kills/coin. The server
  // authoritative skill event below drives the secondary projectile presentation.
  const priorLaunchProjectile=launchProjectile;
  launchProjectile=function(owner,slot,cls,tier,damage,heavy=false,now=performance.now()){
    const before=Array.isArray(S.projectiles)?S.projectiles.length:0;
    const out=priorLaunchProjectile(owner,slot,cls,tier,damage,heavy,now);
    if(mp.active&&owner==='local'&&cls==='rogue'&&S.level>=6&&Array.isArray(S.projectiles)){
      S.projectiles=S.projectiles.filter((p,i)=>i<before||!(p?.owner==='skill'&&p?.skillResolve==='rogue'));
    }
    return out;
  };

  function actor(roomSlot){
    if(roomSlot===mp.slot)return{local:true,slot:0,cls:S.playerClass};
    const vp=mp.visualParty?.find?.(x=>x.roomSlot===roomSlot);
    if(vp)return{local:false,slot:vp.slot,cls:vp.cls};
    const p=mp.state?.participants?.find?.(x=>x.slot===roomSlot);
    if(p)return{local:false,slot:1,cls:p.classId};
    return null;
  }
  function targetPoint(e){
    const m=typeof getMonster==='function'?getMonster(e.targetId):null;
    if(m)return monsterAimPoint(m);
    if(Number.isFinite(e.targetX)&&Number.isFinite(e.targetY))return{x:e.targetX*W,y:e.targetY*H};
    return{x:W*.62,y:H*.45};
  }
  function impact(x,y,damage,cls){
    const rgb=classColor(cls);
    addParticles(x,y,4,1,rgb,false);
    S.pulses.push({x,y,age:0,life:.22,maxR:62,rgb});
    addFloat(String(damage||0),x,y-H*.035,18,'damage');
  }
  function queueSkill(e){
    const a=actor(e.slot);if(!a)return;
    const to=targetPoint(e),now=performance.now();
    if(e.skillKind==='rogue-double-dagger'){
      const from=weaponWorldPos(a.slot,'rogue');
      shots.push({id:e.id,kind:'projectile',cls:'rogue',tier:'SKILL',heavy:false,slot:a.slot,sx:from.x,sy:from.y,tx:to.x,ty:to.y,started:now,life:180,damage:e.damage||0,targetId:e.targetId});
    }else if(e.skillKind==='archer-piercing-arrow'){
      const from=Number.isFinite(e.originX)&&Number.isFinite(e.originY)?{x:e.originX*W,y:e.originY*H}:weaponWorldPos(a.slot,'archer');
      shots.push({id:e.id,kind:'projectile',cls:'archer',tier:e.parentTier||e.tier||'NORMAL',heavy:/^(HEAVY|HEAVY\+|GREAT|SUPER|CRITICAL)$/.test(e.parentTier||''),slot:a.slot,sx:from.x,sy:from.y,tx:to.x,ty:to.y,started:now,life:145,damage:e.damage||0,targetId:e.targetId});
    }else if(e.skillKind==='mage-arcane-burst'){
      bursts.push({id:e.id,cls:'mage',x:to.x,y:to.y,started:now,life:260,damage:e.damage||0,impacted:false});
    }
  }
  function process(st,source=''){
    const run=st?.run,id=run?.id||'';
    if(id&&id!==runId){
      runId=id;shots.length=0;bursts.length=0;
      floor=source==='v035-resume'?Math.max(Number(mp.lastEvent)||0,0):0;
    }
    // v0.35 resume supplies an eventFloor and an intentionally empty event list.
    // Adopt that floor here as well so the next normal snapshot cannot replay
    // historical Lv6 secondary VFX.
    if(source==='v035-resume'){
      floor=Math.max(floor,Number(mp.lastEvent)||0);
      return;
    }
    const events=run?.events||[];
    let max=floor;
    for(const e of events){
      max=Math.max(max,Number(e.id)||0);
      if((Number(e.id)||0)<=floor)continue;
      if(e.type==='skill')queueSkill(e);
    }
    floor=max;
  }
  window.addEventListener('tdcf:state',e=>process(e.detail?.state,e.detail?.source||''));

  function drawSkillShots(){
    const now=performance.now();
    for(let i=shots.length-1;i>=0;i--){
      const s=shots[i],t=Math.max(0,Math.min(1,(now-s.started)/s.life));
      const visual={owner:'local',slot:s.slot,cls:s.cls,tier:s.tier,damage:s.damage,heavy:s.heavy,skillPower:true,targetId:s.targetId,
        sx:s.sx,sy:s.sy,tx:s.tx,ty:s.ty,x:s.sx,y:s.sy,age:(now-s.started)/1000,life:s.life/1000,rot:t*Math.PI*2};
      const saved=S.projectiles;S.projectiles=[visual];try{drawProjectiles()}finally{S.projectiles=saved}
      if(t>=1){impact(s.tx,s.ty,s.damage,s.cls);shots.splice(i,1)}
    }
    for(let i=bursts.length-1;i>=0;i--){
      const b=bursts[i],t=Math.max(0,Math.min(1,(now-b.started)/b.life));
      ctx.save();ctx.globalAlpha=1-t;ctx.strokeStyle='rgba(213,168,255,.92)';ctx.lineWidth=2.5;ctx.beginPath();ctx.arc(b.x,b.y,18+54*t,0,Math.PI*2);ctx.stroke();ctx.restore();
      if(!b.impacted){b.impacted=true;impact(b.x,b.y,b.damage,b.cls)}
      if(t>=1)bursts.splice(i,1);
    }
  }

  const baseDraw=draw;
  draw=function(now){const out=baseDraw(now);drawSkillShots();return out};
})();
