/* Outpost Wilds V18.4: cinematic raid warning/countdown HUD. */
(function(){
  const RAID_EVENT_KINDS=new Set(['waveWarning','waveStage','waveIntermission','waveClear','finalNightStart','finalWaveStage','finalIntermission','finalBoss','bossPhase2','finalFailed']);
  let lastSecond=-1,lastPhase='',lastStage=-1,outcome=null,outcomeUntil=0,flashText='',flashUntil=0;

  function ensure(){
    let el=document.getElementById('v184RaidHud');
    if(el)return el;
    el=document.createElement('div');
    el.id='v184RaidHud';
    el.setAttribute('aria-live','assertive');
    el.innerHTML='<div class="v184Frame"><div class="v184Stripe"></div><div class="v184Copy"><small class="v184Eyebrow"></small><b class="v184Title"></b><span class="v184Meta"></span><div class="v184Pips"></div></div><div class="v184Counter"><strong>0</strong><small>초</small></div><div class="v184Flash"></div></div>';
    document.body.appendChild(el);
    return el;
  }

  function pips(stage,total){
    let html='';
    for(let i=1;i<=Math.max(1,total||1);i++)html+=`<i class="${i<stage?'done':i===stage?'now':''}"></i>`;
    return html;
  }
  function combatTitle(w){
    if(w.bossName)return `${w.bossName} 출현`;
    if(w.final){const names=['','첫 번째 파동','추격자 파동','중장갑 파동','공성 파동','최종 방어전'];return names[w.stage]||`FINAL WAVE ${w.stage}`;}
    const names=['','첫 번째 파동','정예 파동','최종 파동'];return names[w.stage]||`WAVE ${w.stage}`;
  }
  function tick(el,sec){
    if(sec===lastSecond)return;
    lastSecond=sec;
    el.classList.remove('tick');void el.offsetWidth;el.classList.add('tick');
    el.classList.toggle('critical',sec<=3);
  }
  function setFlash(text,ms=1500){flashText=text;flashUntil=performance.now()+ms;const el=ensure();el.querySelector('.v184Flash').textContent=text;el.classList.remove('flash');void el.offsetWidth;el.classList.add('flash');}
  function suppressLegacyToast(){if(typeof toastEl!=='undefined'){toastEl.className='';toastEl.textContent='';}if(typeof toastTimer!=='undefined')clearTimeout(toastTimer);}

  function render(){
    const el=ensure(),now=performance.now(),w=snap?.wave;
    const active=!!w?.active;
    if(!active&&outcome&&now<outcomeUntil){
      el.className=`show outcome ${outcome.success?'success':'failure'}`;
      el.querySelector('.v184Eyebrow').textContent=outcome.success?'NIGHT RAID CLEARED':'DEFENSE BREACHED';
      el.querySelector('.v184Title').textContent=outcome.success?'침공 방어 성공':'침공 종료 · 방어선 돌파';
      el.querySelector('.v184Meta').textContent=outcome.success?`거점 HP ${outcome.baseHp} · 다음 밤을 준비하세요`:'방벽과 거점을 복구하세요';
      el.querySelector('.v184Counter strong').textContent=outcome.success?'✓':'!';
      el.querySelector('.v184Counter small').textContent='';
      el.querySelector('.v184Pips').innerHTML='';
      document.body.classList.add('v184-raid-active');document.body.classList.remove('v184-raid-warning');
      return;
    }
    if(!active){
      el.className='';document.body.classList.remove('v184-raid-active','v184-raid-warning','v184-raid-final');lastPhase='';lastStage=-1;lastSecond=-1;return;
    }

    const phase=w.phase||'combat',final=!!w.final,total=Math.max(1,w.totalStages||3),stage=Math.max(0,w.stage||0),sec=Math.max(0,Math.ceil(Number(w.timer)||0));
    document.body.classList.add('v184-raid-active');document.body.classList.toggle('v184-raid-warning',phase==='warning');document.body.classList.toggle('v184-raid-final',final);
    el.className=`show ${phase}${final?' final':''}${w.bossName?' boss':''}`;
    const eyebrow=el.querySelector('.v184Eyebrow'),title=el.querySelector('.v184Title'),meta=el.querySelector('.v184Meta'),count=el.querySelector('.v184Counter strong'),unit=el.querySelector('.v184Counter small'),dots=el.querySelector('.v184Pips');

    if(phase==='warning'){
      eyebrow.textContent=final?'FINAL NIGHT · 최고 경계':'NIGHT RAID · 침공 경보';
      title.textContent=final?'최후의 밤이 시작된다':`제 ${w.raid}차 야간 침공`;
      meta.textContent=final?'모든 방어선을 점검하세요 · 5개 파동이 연속으로 몰려옵니다':'거점으로 복귀 · 방벽과 방어 시설을 확인하세요';
      count.textContent=sec;unit.textContent='초';dots.innerHTML=pips(1,total);tick(el,sec);
    }else if(phase==='intermission'){
      const next=Math.min(total,stage+1);
      eyebrow.textContent=final?'FINAL NIGHT · 짧은 정비':'침공 지속 · 정비 시간';
      title.textContent=`WAVE ${next}/${total} 접근 중`;
      meta.textContent=next===total?'최종 파동 접근 · 방벽 수리와 위치 재정비':'잠깐의 정적 · 수리하고 방어 위치를 다시 잡으세요';
      count.textContent=sec;unit.textContent='초';dots.innerHTML=pips(next,total);tick(el,sec);
    }else{
      eyebrow.textContent=`${final?'FINAL NIGHT':'NIGHT RAID'} · WAVE ${stage}/${total}`;
      title.textContent=combatTitle(w);
      meta.textContent=w.bossName?`${w.bossName}이 방어선을 압박합니다`:(stage===total?'마지막 파동 · 거점을 끝까지 사수하세요':'현재 파동을 제거해야 다음 단계로 넘어갑니다');
      count.textContent=Math.max(0,w.remaining||0);unit.textContent='잔여';dots.innerHTML=pips(stage,total);el.classList.remove('critical');lastSecond=-1;
    }
    if(lastPhase!==phase||lastStage!==stage){lastPhase=phase;lastStage=stage;el.classList.remove('phaseChange');void el.offsetWidth;el.classList.add('phaseChange');}
    const flash=el.querySelector('.v184Flash');if(now>=flashUntil){flash.textContent='';el.classList.remove('flash');}else flash.textContent=flashText;
  }

  const prevHud=updateHud;
  updateHud=function(){prevHud();render();};

  const prevEvent=eventFx;
  eventFx=function(m){
    prevEvent(m);
    if(RAID_EVENT_KINDS.has(m.kind))suppressLegacyToast();
    if(m.kind==='waveWarning'){outcome=null;setFlash('⚠ 침공 경보 발령',1900);}
    if(m.kind==='waveStage')setFlash(`WAVE ${m.stage}/${m.totalStages} 돌입`,1500);
    if(m.kind==='waveIntermission')setFlash(`다음 WAVE ${m.nextStage} 접근`,1300);
    if(m.kind==='bossRaid')setFlash(`⚠ ${m.name} 출현`,2300);
    if(m.kind==='waveClear'){outcome={success:!!m.success,baseHp:m.baseHp};outcomeUntil=performance.now()+3200;setFlash(m.success?'방어 성공':'방어선 돌파',1800);render();}
    if(m.kind==='finalNightStart'){outcome=null;setFlash('FINAL NIGHT',2400);}
    if(m.kind==='finalWaveStage')setFlash(`FINAL WAVE ${m.stage}/${m.totalStages}`,1700);
    if(m.kind==='finalIntermission')setFlash(`다음 FINAL WAVE 접근`,1400);
    if(m.kind==='finalBoss')setFlash(`⚠ ${m.name} 출현`,2600);
    if(m.kind==='bossPhase2')setFlash(`⚠ ${m.name} 격노`,2100);
    if(m.kind==='finalFailed'){outcome={success:false,baseHp:Math.round(snap?.base?.hp||0)};outcomeUntil=performance.now()+3500;setFlash('FINAL NIGHT 실패',2200);render();}
  };

  setInterval(()=>{if(snap?.wave?.active||(outcome&&performance.now()<outcomeUntil))render();},120);
  window.__OW_V184__={raidHud:true,warningSeconds:10,finalWarningSeconds:12,intermissionSeconds:5,finalIntermissionSeconds:6};
})();
