// Timing Defense Cloudflare v0.39 — authoritative N3 milestone presentation.
// Gameplay state remains server-owned. This layer suppresses the legacy local
// milestone-damage path and renders only server-confirmed `type:n3` events.
(function(){
  const mp=window.__TDMP34CF;if(!mp)return;

  let floor=Number(mp.lastEvent)||0,runId='';
  const shots=[],bursts=[];

  // Legacy v0.18 consumes v018PendingMilestones inside resolveLocalHit and would
  // create client-mutating combo projectiles. In network mode the server is the
  // only N3 authority, so consume that local pending list before the legacy path.
  const priorResolveLocalHit=resolveLocalHit;
  resolveLocalHit=function(p,now){
    if(mp.active&&Array.isArray(S.v018PendingMilestones)&&S.v018PendingMilestones.length)S.v018PendingMilestones.length=0;
    return priorResolveLocalHit(p,now);
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
  function originPoint(e,a){
    if(e.hitIndex>0&&Number.isFinite(e.originX)&&Number.isFinite(e.originY))return{x:e.originX*W,y:e.originY*H};
    return weaponWorldPos(a.slot,a.cls);
  }
  function impact(x,y,damage,cls,strong=false){
    const rgb=classColor(cls);addParticles(x,y,strong?7:4,strong?1.25:1,rgb,false);
    S.pulses.push({x,y,age:0,life:strong?.28:.20,maxR:strong?82:58,rgb});
    addFloat(String(damage||0),x,y-H*.035,strong?19:17,'damage');
  }
  function milestonePulse(e,a,to){
    if(Number(e.hitIndex)!==0)return;
    const m=Number(e.n3Milestone)||0,rgb=classColor(a.cls);
    S.pulses.push({x:to.x,y:to.y,age:0,life:.36,maxR:m>=30?112:m>=20?94:m>=10?80:68,rgb});
  }
  function queueN3(e){
    const a=actor(e.slot);if(!a)return;
    const to=targetPoint(e),from=originPoint(e,a),now=performance.now(),kind=String(e.n3Kind||'');
    milestonePulse(e,a,to);
    if(kind==='mage-arcane-burst'||kind==='tank-shock-burst'){
      bursts.push({id:e.id,cls:a.cls,x:to.x,y:to.y,started:now,life:kind==='tank-shock-burst'?220:270,damage:e.damage||0,strong:Number(e.hitIndex)===0,impacted:false});
      return;
    }
    const life=a.cls==='rogue'?150:a.cls==='archer'?135:165;
    shots.push({id:e.id,cls:a.cls,tier:'NORMAL',slot:a.slot,sx:from.x,sy:from.y,tx:to.x,ty:to.y,started:now,life,damage:e.damage||0,targetId:e.targetId,strong:Number(e.hitIndex)===0});
  }
  function process(st,source=''){
    const run=st?.run,id=run?.id||'';
    if(id&&id!==runId){runId=id;shots.length=0;bursts.length=0;floor=source==='v035-resume'?Math.max(Number(mp.lastEvent)||0,0):0}
    if(source==='v035-resume'){floor=Math.max(floor,Number(mp.lastEvent)||0);return}
    let max=floor;
    for(const e of run?.events||[]){
      const eid=Number(e.id)||0;max=Math.max(max,eid);if(eid<=floor)continue;
      if(e.type==='n3'&&e.n3===true)queueN3(e);
    }
    floor=max;
  }
  window.addEventListener('tdcf:state',e=>process(e.detail?.state,e.detail?.source||''));

  function drawN3(){
    const now=performance.now();
    for(let i=shots.length-1;i>=0;i--){
      const s=shots[i],t=Math.max(0,Math.min(1,(now-s.started)/s.life));
      const visual={owner:'local',slot:s.slot,cls:s.cls,tier:'NORMAL',damage:s.damage,heavy:false,skillPower:true,targetId:s.targetId,
        sx:s.sx,sy:s.sy,tx:s.tx,ty:s.ty,x:s.sx,y:s.sy,age:(now-s.started)/1000,life:s.life/1000,rot:t*Math.PI*2};
      const saved=S.projectiles;S.projectiles=[visual];try{drawProjectiles()}finally{S.projectiles=saved}
      if(t>=1){impact(s.tx,s.ty,s.damage,s.cls,s.strong);shots.splice(i,1)}
    }
    for(let i=bursts.length-1;i>=0;i--){
      const b=bursts[i],t=Math.max(0,Math.min(1,(now-b.started)/b.life)),rgb=classColor(b.cls);
      ctx.save();ctx.globalAlpha=1-t;ctx.strokeStyle=`rgba(${rgb},.92)`;ctx.lineWidth=b.strong?3:2;ctx.beginPath();ctx.arc(b.x,b.y,16+(b.strong?72:52)*t,0,Math.PI*2);ctx.stroke();ctx.restore();
      if(!b.impacted){b.impacted=true;impact(b.x,b.y,b.damage,b.cls,b.strong)}
      if(t>=1)bursts.splice(i,1);
    }
  }
  const baseDraw=draw;draw=function(now){const out=baseDraw(now);drawN3();return out};

  window.__TD039N3={get floor(){return floor},get pending(){return shots.length+bursts.length}};
})();
