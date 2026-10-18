/* Outpost Wilds V11: formal wave feedback without adding another HUD panel. */
const v11OldHud=updateHud;
updateHud=function(){
  v11OldHud();if(!snap)return;
  const w=snap.wave;
  if(w?.active){
    $('phaseLabel').textContent=`습격 ${w.raid}`;
    if(w.phase==='warning')$('clockLabel').textContent=`⚠ 접근 중 · ${Math.ceil(w.timer)}초`;
    else if(w.phase==='intermission')$('clockLabel').textContent=`정비 · 다음 WAVE ${Math.min(w.totalStages,w.stage+1)}/${w.totalStages} · ${Math.ceil(w.timer)}초`;
    else if(w.phase==='combat')$('clockLabel').textContent=`WAVE ${w.stage}/${w.totalStages} · 잔여 ${w.remaining}${w.bossName?` · ${w.bossName}`:''}`;
  }
};

const v11OldEvent=eventFx;
eventFx=function(m){
  v11OldEvent(m);
  if(m.kind==='waveWarning'){toast(`습격 ${m.raid} 접근 · 방어 위치를 준비하세요`,'phaseDanger');nightFlash=.45;}
  if(m.kind==='waveStage'){toast(`WAVE ${m.stage}/${m.totalStages} · ${m.count}마리 진격${m.boss?` · ${m.boss}`:''}`,m.stage>=3?'phaseDanger':'phaseAlert');if(m.stage>=3){nightFlash=.45;shake=5;}}
  if(m.kind==='waveIntermission'&&m.nextStage>=3)toast(`최종 WAVE 접근 · ${Math.ceil(m.seconds)}초`,'phaseAlert');
  if(m.kind==='waveClear'){if(m.success)toast(`습격 ${m.raid} 방어 성공 · 거점 HP ${m.baseHp}`,'phaseAlert');else toast(`습격 ${m.raid} 종료 · 방벽 돌파 기록`,'phaseDanger');}
};
