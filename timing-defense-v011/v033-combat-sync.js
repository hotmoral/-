// Timing Defense v0.33 — authoritative multiplayer Stage 1 combat slice.
// START -> synchronized local run entry; server owns monsters/base HP/Stage1 world state.
(function(){
  const API='https://timing-defense-mp.onrender.com';
  const root=document.getElementById('v022Lobby'),waiting=document.getElementById('v027Waiting');
  if(!root||!waiting)return;

  const mp={session:null,slot:null,state:null,stream:null,startTimer:null,active:false,seq:0,lastEvent:0,visualParty:[]};
  window.__TDMP33=mp;

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
    if(!st)return;mp.state=st;
    if(!mp.slot&&mp.session){
      const nick=(document.getElementById('v022Nick')?.value||S.v022Nickname||'').trim();
      const cls=S.playerClass;
      const matches=st.participants?.filter(p=>p.nickname===nick&&p.classId===cls)||[];
      if(matches.length===1)mp.slot=matches[0].slot
    }
    if(st.code&&mp.session&&!mp.stream)attach(st.code);
    if(st.run){
      processEvents(st.run);
      if(!mp.active)scheduleStart(st);
      else syncRun(st.run)
    }
  }
  function scheduleStart(st){
    if(mp.startTimer||mp.active||!st.run?.startAt)return;
    const delay=Math.max(0,(st.run.startAt-(st.serverTime||Date.now())));
    mp.startTimer=setTimeout(()=>{mp.startTimer=null;beginRun()},delay)
  }
  function beginRun(){
    if(mp.active||!mp.state?.run)return;
    const self=mp.state.participants?.find(p=>p.slot===mp.slot);
    root.style.display='none';waiting.classList.remove('show');S.v022LobbyOpen=false;
    S.playerClass=self?.classId||S.playerClass;S.teamSize=1;
    reset();
    mp.active=true;S.v033NetworkRun=true;S.v018AutoNextAt=Infinity;S.nextSpawnAt=Infinity;S.stageTarget=999;S.ai=[];
    rebuildParty();syncRun(mp.state.run)
  }
  function rebuildParty(){
    if(!mp.state)return;
    const list=[];
    for(const p of mp.state.participants||[])if(p.slot!==mp.slot)list.push({cls:p.classId,label:p.nickname,roomSlot:p.slot,human:true});
    for(const a of mp.state.aiFill||[])list.push({cls:a.cls,label:`CPU ${a.pos}`,roomSlot:a.pos,human:false});
    mp.visualParty=list.slice(0,3).map((x,i)=>({...x,slot:i+1,charge:0,shotNo:0,nextAt:Infinity,shots:0}));
    if(mp.active)S.ai=mp.visualParty
  }
  function processEvents(run){
    for(const e of run.events||[]){
      if(e.id<=mp.lastEvent)continue;mp.lastEvent=e.id;
      const m=getMonster?.(e.targetId);
      if((e.type==='hit'||e.type==='ai'||e.type==='passive')&&m){
        const a=monsterAimPoint(m);m.hitFlash=1;addParticles(a.x,a.y,e.type==='hit'?5:2,1);S.pulses.push({x:a.x,y:a.y,age:0,life:.20,maxR:58});
        addFloat(String(e.damage||0),a.x,a.y-H*.035,e.type==='hit'?24:16,'damage')
      }
      if(e.type==='wall')addFloat(`-${e.damage}`,W*.17,H*.34,18,'damage');
      if(e.type==='hit'&&e.slot===mp.slot&&e.xpGain){const n=performance.now();S.v023XpAmount=e.xpGain;S.v023XpStart=n;S.v023XpUntil=n+720}
      if(e.type==='stage-clear'){S.resultText='STAGE 1 SYNC CLEAR';S.resultTier='PERFECT';S.resultUntil=performance.now()+999999}
    }
  }
  function syncRun(run){
    if(!mp.active||!run)return;
    const local=run.players?.find(p=>p.slot===mp.slot);
    S.baseHp=run.baseHp;S.baseHpMax=run.baseHpMax;S.stage=run.stage||1;S.kills=run.kills||0;S.spawnedThisStage=run.spawned||0;
    if(local){S.level=local.level;S.xp=local.xp;S.xpNeed=local.xpNeed;S.charge=local.charge;S.gold=local.coin;S.v018Combo=local.combo;S.v018ComboPeak=Math.max(S.v018ComboPeak||0,local.comboPeak||0)}
    const old=new Map(S.monsters.map(m=>[m.id,m]));
    S.monsters=(run.monsters||[]).map(sm=>{const o=old.get(sm.id);return{id:sm.id,type:sm.type,boss:!!sm.boss,scaleMul:1,x:sm.x*W,y:sm.y*H,baseY:sm.y*H,minY:H*.26,maxY:H*.62,hp:sm.hp,maxHp:sm.maxHp,age:o?.age||0,hitFlash:o?.hitFlash||0,dead:false,v018HpAdjusted:true}});
    S.nextMonsterId=Math.max(1,...S.monsters.map(m=>m.id+1));S.nextSpawnAt=Infinity;S.stageTarget=999;S.v018AutoNextAt=Infinity;
    rebuildParty();
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
    rawFetch(`${API}/api/room/${mp.state.code}/action`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).then(async r=>{const d=await r.json().catch(()=>null);if(d?.state)acceptState(d.state)}).catch(()=>{});
    return true
  };

  const baseUpdate=update;
  update=function(now,dt){
    if(!mp.active)return baseUpdate(now,dt);
    const visual=mp.visualParty,saveSpeeds={};
    for(const k of Object.keys(MONSTER_TYPES)){saveSpeeds[k]=MONSTER_TYPES[k].speed;MONSTER_TYPES[k].speed=0}
    S.ai=[];S.nextSpawnAt=Infinity;S.stageTarget=999;S.v018AutoNextAt=Infinity;
    try{baseUpdate(now,dt)}finally{for(const k of Object.keys(saveSpeeds))MONSTER_TYPES[k].speed=saveSpeeds[k];S.ai=visual;S.nextSpawnAt=Infinity;S.stageTarget=999;S.v018AutoNextAt=Infinity}
  };

  const baseBeginShop=beginShop;beginShop=function(now){if(mp.active)return;return baseBeginShop(now)};
  const baseFinishRun=finishRun;finishRun=function(now){if(mp.active)return;return baseFinishRun(now)};

  const baseDrawCharacter=drawCharacter;
  drawCharacter=function(slot,cls,local=false){
    baseDrawCharacter(slot,cls,local);
    if(mp.active&&!local){const x=mp.visualParty.find(a=>a.slot===slot);if(x?.human){const b=charBase(slot);ctx.save();ctx.fillStyle='rgba(10,16,13,.78)';ctx.fillRect(b.x-34,b.y+H*.034,68,13);ctx.fillStyle='rgba(255,255,255,.82)';ctx.font='800 8px system-ui';ctx.textAlign='center';ctx.fillText(x.label,b.x,b.y+H*.046);ctx.restore()}}
  };

  // Invitation/random sessions are discovered from fetch responses; this poll closes the small race before SSE attach.
  setInterval(()=>{if(mp.state?.code&&mp.session&&!mp.stream)attach(mp.state.code)},800);
})();