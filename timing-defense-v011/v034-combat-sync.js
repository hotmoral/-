// Timing Defense v0.34 — multiplayer render smoothing + remote attack VFX.
// Server remains authoritative. Client interpolates/extrapolates snapshots and renders remote fire locally.
(function(){
  const API='https://timing-defense-mp.onrender.com';
  const root=document.getElementById('v022Lobby'),waiting=document.getElementById('v027Waiting');
  if(!root||!waiting)return;

  const mp={
    session:null,slot:null,state:null,stream:null,startTimer:null,active:false,seq:0,lastEvent:0,
    visualParty:[],partySig:'',monsterById:new Map(),remoteShots:[],serverOffsetMs:0,lastSnapshotPerf:0
  };
  window.__TDMP34=mp;

  const rawFetch=window.fetch.bind(window);
  window.fetch=async function(input,init){
    const res=await rawFetch(input,init);
    try{
      const url=typeof input==='string'?input:input?.url||'';
      if(url.startsWith(API+'/')){
        const d=await res.clone().json().catch(()=>null);
        if(d){
          if(d.session)mp.session=d.session;
          if(Number.isInteger(d.slot))mp.slot=d.slot;
          if(d.status?.session){mp.session=d.status.session;mp.slot=d.status.slot}
          if(d.state)acceptState(d.state);
          if(d.status?.code&&d.status?.session)attach(d.status.code);
        }
      }
    }catch(_){}
    return res
  };

  function attach(code){
    if(!code||!mp.session)return;
    try{mp.stream?.close()}catch(_){}
    mp.stream=new EventSource(`${API}/api/room/${code}/stream?session=${encodeURIComponent(mp.session)}`);
    mp.stream.addEventListener('state',e=>{try{acceptState(JSON.parse(e.data))}catch(_){}})
  }

  function acceptState(st){
    if(!st)return;
    mp.state=st;
    if(Number.isFinite(st.serverTime))mp.serverOffsetMs=Date.now()-st.serverTime;
    if(!mp.slot&&mp.session){
      const nick=(document.getElementById('v022Nick')?.value||S.v022Nickname||'').trim();
      const cls=S.playerClass;
      const matches=st.participants?.filter(p=>p.nickname===nick&&p.classId===cls)||[];
      if(matches.length===1)mp.slot=matches[0].slot
    }
    if(st.code&&mp.session&&!mp.stream)attach(st.code);
    ensureParty();
    if(st.run){
      processEvents(st.run);
      if(!mp.active)scheduleStart(st);
      else syncRun(st.run)
    }
  }

  function scheduleStart(st){
    if(mp.startTimer||mp.active||!st.run?.startAt)return;
    const delay=Math.max(0,st.run.startAt-(st.serverTime||Date.now()));
    mp.startTimer=setTimeout(()=>{mp.startTimer=null;beginRun()},delay)
  }

  function beginRun(){
    if(mp.active||!mp.state?.run)return;
    const self=mp.state.participants?.find(p=>p.slot===mp.slot);
    root.style.display='none';waiting.classList.remove('show');S.v022LobbyOpen=false;
    S.playerClass=self?.classId||S.playerClass;S.teamSize=1;
    reset();
    mp.active=true;S.v033NetworkRun=true;S.v034NetworkRun=true;
    S.v018AutoNextAt=Infinity;S.nextSpawnAt=Infinity;S.stageTarget=999;S.ai=[];
    mp.monsterById.clear();mp.remoteShots.length=0;
    ensureParty(true);syncRun(mp.state.run)
  }

  function partySignature(){
    if(!mp.state)return'';
    const humans=(mp.state.participants||[]).map(p=>`${p.slot}:${p.nickname}:${p.classId}`).sort().join('|');
    const ais=(mp.state.aiFill||[]).map(a=>`${a.pos}:${a.cls}`).sort().join('|');
    return `${mp.slot}#${humans}#${ais}`
  }

  function ensureParty(force=false){
    if(!mp.state)return;
    const sig=partySignature();
    if(!force&&sig===mp.partySig)return;
    mp.partySig=sig;
    const list=[];
    for(const p of mp.state.participants||[])if(p.slot!==mp.slot)list.push({cls:p.classId,label:p.nickname,roomSlot:p.slot,human:true});
    for(const a of mp.state.aiFill||[])list.push({cls:a.cls,label:`CPU ${a.pos}`,roomSlot:a.pos,human:false});
    list.sort((a,b)=>a.roomSlot-b.roomSlot);
    mp.visualParty=list.slice(0,3).map((x,i)=>({...x,slot:i+1,charge:0,shotNo:0,nextAt:Infinity,shots:0}));
    if(mp.active)S.ai=mp.visualParty
  }

  function actorInfo(roomSlot){
    if(roomSlot===mp.slot)return{cls:S.playerClass,visualSlot:0,human:true,label:S.v022Nickname||'YOU'};
    const vp=mp.visualParty.find(x=>x.roomSlot===roomSlot);
    if(vp)return{cls:vp.cls,visualSlot:vp.slot,human:vp.human,label:vp.label};
    const hp=mp.state?.participants?.find(p=>p.slot===roomSlot);
    if(hp)return{cls:hp.classId,visualSlot:1,human:true,label:hp.nickname};
    const ai=mp.state?.aiFill?.find(a=>a.pos===roomSlot);
    if(ai)return{cls:ai.cls,visualSlot:1,human:false,label:`CPU ${roomSlot}`};
    return null
  }

  function remoteLife(cls,tier){
    const heavy=/^(HEAVY|HEAVY\+|GREAT|SUPER|CRITICAL)$/.test(tier||'');
    const base=cls==='rogue'?.18:cls==='archer'?.18:cls==='tank'?.28:cls==='mage'?.30:.22;
    return base*(heavy?1.10:1)
  }

  function queueRemoteShot(e,m){
    const actor=actorInfo(e.slot);if(!actor||!m)return;
    const isRemoteHit=e.type==='hit'&&e.slot!==mp.slot;
    const serverOnlyVisual=e.type==='ai'||e.type==='passive';
    if(!isRemoteHit&&!serverOnlyVisual)return;
    const start=weaponWorldPos(actor.visualSlot,actor.cls);
    const aim=monsterAimPoint(m);
    mp.remoteShots.push({
      id:e.id,cls:actor.cls,slot:actor.visualSlot,tier:e.tier||'NORMAL',type:e.type,
      targetId:e.targetId,sx:start.x,sy:start.y,tx:aim.x,ty:aim.y,
      started:performance.now(),life:remoteLife(actor.cls,e.tier)*1000,damage:e.damage||0,impacted:false
    });
    if(mp.remoteShots.length>28)mp.remoteShots.splice(0,mp.remoteShots.length-28)
  }

  function applyRemoteImpact(shot){
    if(shot.impacted)return;shot.impacted=true;
    const m=getMonster?.(shot.targetId);if(!m)return;
    const a=monsterAimPoint(m);m.hitFlash=1;
    addParticles(a.x,a.y,shot.type==='hit'?5:2,1);
    S.pulses.push({x:a.x,y:a.y,age:0,life:.20,maxR:58});
    addFloat(String(shot.damage||0),a.x,a.y-H*.035,shot.type==='hit'?24:16,'damage')
  }

  function processEvents(run){
    for(const e of run.events||[]){
      if(e.id<=mp.lastEvent)continue;
      mp.lastEvent=e.id;
      const m=getMonster?.(e.targetId);
      if((e.type==='hit'||e.type==='ai'||e.type==='passive')&&m){
        const remoteVisual=(e.type==='hit'&&e.slot!==mp.slot)||e.type==='ai'||e.type==='passive';
        if(remoteVisual)queueRemoteShot(e,m);
        else{
          const a=monsterAimPoint(m);m.hitFlash=1;
          addParticles(a.x,a.y,5,1);S.pulses.push({x:a.x,y:a.y,age:0,life:.20,maxR:58});
        }
      }
      if(e.type==='wall')addFloat(`-${e.damage}`,W*.17,H*.34,18,'damage');
      if(e.type==='hit'&&e.slot===mp.slot&&e.xpGain){const n=performance.now();S.v023XpAmount=e.xpGain;S.v023XpStart=n;S.v023XpUntil=n+720}
      if(e.type==='stage-clear'){S.resultText='STAGE 1 SYNC CLEAR';S.resultTier='PERFECT';S.resultUntil=performance.now()+999999}
    }
  }

  function makeMonster(sm){
    const x=sm.x*W,y=sm.y*H;
    return{id:sm.id,type:sm.type,boss:!!sm.boss,scaleMul:1,x,y,baseY:y,minY:H*.26,maxY:H*.62,hp:sm.hp,maxHp:sm.maxHp,age:0,hitFlash:0,dead:false,v018HpAdjusted:true,v034TargetX:x,v034TargetY:y,v034TargetAt:performance.now()}
  }

  function syncRun(run){
    if(!mp.active||!run)return;
    mp.lastSnapshotPerf=performance.now();
    const local=run.players?.find(p=>p.slot===mp.slot);
    S.baseHp=run.baseHp;S.baseHpMax=run.baseHpMax;S.stage=run.stage||1;S.kills=run.kills||0;S.spawnedThisStage=run.spawned||0;
    if(local){
      S.level=local.level;S.xp=local.xp;S.xpNeed=local.xpNeed;S.charge=local.charge;S.gold=local.coin;
      S.v018Combo=local.combo;S.v018ComboPeak=Math.max(S.v018ComboPeak||0,local.comboPeak||0)
    }

    const seen=new Set(),next=[];
    for(const sm of run.monsters||[]){
      seen.add(sm.id);
      let m=mp.monsterById.get(sm.id);
      if(!m){m=makeMonster(sm);mp.monsterById.set(sm.id,m)}
      const tx=sm.x*W,ty=sm.y*H;
      m.type=sm.type;m.boss=!!sm.boss;m.hp=sm.hp;m.maxHp=sm.maxHp;m.dead=false;
      m.v034TargetX=tx;m.v034TargetY=ty;m.v034TargetAt=mp.lastSnapshotPerf;
      m.baseY=ty;m.minY=H*.26;m.maxY=H*.62;
      if(Math.abs(m.x-tx)>W*.22||Math.abs(m.y-ty)>H*.30){m.x=tx;m.y=ty}
      next.push(m)
    }
    for(const[id]of mp.monsterById)if(!seen.has(id))mp.monsterById.delete(id);
    S.monsters=next;
    S.nextMonsterId=Math.max(1,...S.monsters.map(m=>m.id+1));
    S.nextSpawnAt=Infinity;S.stageTarget=999;S.v018AutoNextAt=Infinity;
    ensureParty();
    if(run.status==='gameover'){S.gameOver=true;S.stageMode='gameover';S.phase='idle';S.resultText='GAME OVER';S.resultTier='CRITICAL';S.resultUntil=performance.now()+999999}
    if(run.status==='stage1-clear'){S.stageMode='clear';S.phase='idle';S.resultText='STAGE 1 SYNC CLEAR';S.resultTier='PERFECT';S.resultUntil=performance.now()+999999}
  }

  const baseResolveLocalHit=resolveLocalHit;
  resolveLocalHit=function(p,now){
    if(!mp.active||!mp.state?.code||!mp.session)return baseResolveLocalHit(p,now);
    const tier=p.tier||'NORMAL',critical=tier==='CRITICAL',perfect=critical||tier==='PERFECT'||tier==='SUPER',good=perfect||tier==='GOOD'||tier==='GREAT';
    S.hitStopUntil=now+(critical?90:perfect?55:good?28:8);
    const heavy=isHeavy();S.charge=heavy?0:Math.min(3,S.charge+1);S.phase='recover';S.phaseStart=now;
    const payload={session:mp.session,seq:++mp.seq,xJudge:S.xJudge||'NORMAL',yJudge:S.yJudge||null};
    rawFetch(`${API}/api/room/${mp.state.code}/action`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
      .then(async r=>{const d=await r.json().catch(()=>null);if(d?.state)acceptState(d.state)}).catch(()=>{});
    return true
  };

  function smoothMonsters(now,dt){
    const alpha=1-Math.exp(-Math.max(0,dt)*18);
    for(const m of S.monsters){
      const age=Math.min(.16,Math.max(0,(now-(m.v034TargetAt||now))/1000));
      const speed=MONSTER_TYPES[m.type]?.speed||0;
      const tx=(m.v034TargetX??m.x)-W*speed*age;
      const ty=m.v034TargetY??m.y;
      m.x+= (tx-m.x)*alpha;
      m.y+= (ty-m.y)*alpha;
    }
  }

  const baseUpdate=update;
  update=function(now,dt){
    if(!mp.active)return baseUpdate(now,dt);
    const visual=mp.visualParty,saveSpeeds={};
    for(const k of Object.keys(MONSTER_TYPES)){saveSpeeds[k]=MONSTER_TYPES[k].speed;MONSTER_TYPES[k].speed=0}
    S.ai=[];S.nextSpawnAt=Infinity;S.stageTarget=999;S.v018AutoNextAt=Infinity;
    try{baseUpdate(now,dt)}finally{
      for(const k of Object.keys(saveSpeeds))MONSTER_TYPES[k].speed=saveSpeeds[k];
      smoothMonsters(now,dt);
      S.ai=visual;S.nextSpawnAt=Infinity;S.stageTarget=999;S.v018AutoNextAt=Infinity
    }
  };

  const baseBeginShop=beginShop;beginShop=function(now){if(mp.active)return;return baseBeginShop(now)};
  const baseFinishRun=finishRun;finishRun=function(now){if(mp.active)return;return baseFinishRun(now)};

  const baseDrawCharacter=drawCharacter;
  drawCharacter=function(slot,cls,local=false){
    baseDrawCharacter(slot,cls,local);
    if(mp.active&&!local){
      const x=mp.visualParty.find(a=>a.slot===slot);
      if(x?.human){
        const b=charBase(slot);ctx.save();ctx.fillStyle='rgba(10,16,13,.78)';ctx.fillRect(b.x-34,b.y+H*.034,68,13);
        ctx.fillStyle='rgba(255,255,255,.82)';ctx.font='800 8px system-ui';ctx.textAlign='center';ctx.fillText(x.label,b.x,b.y+H*.046);ctx.restore()
      }
    }
  };

  function remoteColor(cls){
    if(cls==='rogue')return{main:'#1f252a',hi:'#f2f5f7',glow:'rgba(230,235,238,.50)'};
    if(cls==='tank')return{main:'#1e5f9a',hi:'#83d3ff',glow:'rgba(75,181,255,.48)'};
    if(cls==='archer')return{main:'#28743b',hi:'#9af0a0',glow:'rgba(90,210,110,.45)'};
    if(cls==='mage')return{main:'#6c3aa6',hi:'#d5a8ff',glow:'rgba(185,115,255,.50)'};
    return{main:'#9b651c',hi:'#ffe08a',glow:'rgba(255,195,70,.50)'}
  }

  function drawShotShape(s,x,y,t){
    const c=remoteColor(s.cls),heavy=/^(HEAVY|HEAVY\+|GREAT|SUPER|CRITICAL)$/.test(s.tier||'');
    ctx.save();ctx.translate(x,y);ctx.shadowBlur=heavy?16:9;ctx.shadowColor=c.glow;
    if(s.cls==='rogue'){
      const ang=Math.atan2(s.ty-s.sy,s.tx-s.sx);ctx.rotate(ang);ctx.fillStyle=c.main;ctx.strokeStyle=c.hi;ctx.lineWidth=1.8;
      ctx.beginPath();ctx.moveTo(14,0);ctx.lineTo(-5,-4);ctx.lineTo(-11,0);ctx.lineTo(-5,4);ctx.closePath();ctx.fill();ctx.stroke();
      ctx.globalAlpha=.38;ctx.strokeStyle=c.hi;ctx.beginPath();ctx.moveTo(-18,0);ctx.lineTo(-5,0);ctx.stroke();
    }else if(s.cls==='archer'){
      const ang=Math.atan2(s.ty-s.sy,s.tx-s.sx);ctx.rotate(ang);ctx.strokeStyle=c.main;ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(-17,0);ctx.lineTo(13,0);ctx.stroke();
      ctx.strokeStyle=c.hi;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(-18,0);ctx.lineTo(16,0);ctx.moveTo(16,0);ctx.lineTo(9,-5);ctx.moveTo(16,0);ctx.lineTo(9,5);ctx.stroke();
    }else if(s.cls==='tank'){
      ctx.strokeStyle=c.hi;ctx.lineWidth=heavy?5:3;ctx.beginPath();ctx.ellipse(0,0,heavy?28:20,heavy?15:11,0,-.8,.8);ctx.stroke();
      ctx.globalAlpha=.28;ctx.strokeStyle=c.main;ctx.beginPath();ctx.ellipse(-7,0,heavy?22:15,heavy?12:8,0,-.8,.8);ctx.stroke();
    }else if(s.cls==='mage'){
      const r=heavy?12:8;ctx.fillStyle=c.main;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();ctx.strokeStyle=c.hi;ctx.lineWidth=2;ctx.beginPath();ctx.arc(0,0,r+3,0,Math.PI*2);ctx.stroke();
      ctx.globalAlpha=.34;ctx.beginPath();ctx.arc(-12,0,r*.7,0,Math.PI*2);ctx.fill();
    }else{
      ctx.strokeStyle=c.main;ctx.lineWidth=heavy?7:5;ctx.beginPath();ctx.arc(0,0,heavy?31:24,-.9,.9);ctx.stroke();
      ctx.strokeStyle=c.hi;ctx.lineWidth=2.2;ctx.beginPath();ctx.arc(0,0,heavy?31:24,-.9,.9);ctx.stroke();
    }
    ctx.restore()
  }

  function drawRemoteShots(now){
    if(!mp.active||!mp.remoteShots.length)return;
    const keep=[];
    for(const s of mp.remoteShots){
      const m=getMonster?.(s.targetId);
      if(m){const a=monsterAimPoint(m);s.tx=a.x;s.ty=a.y}
      const t=clamp((now-s.started)/Math.max(1,s.life),0,1),e=easeOutCubic(t);
      const x=s.sx+(s.tx-s.sx)*e,y=s.sy+(s.ty-s.sy)*e;
      drawShotShape(s,x,y,t);
      if(t>=1)applyRemoteImpact(s);else keep.push(s)
    }
    mp.remoteShots=keep
  }

  const baseDraw=draw;
  draw=function(now){baseDraw(now);drawRemoteShots(now)};

  setInterval(()=>{if(mp.state?.code&&mp.session&&!mp.stream)attach(mp.state.code)},800);
})();