const HARNESS_VERSION = 'skilled-v2-controlled-harness-v0.1';
const INPUT_SURFACE_VERSION = 'skilled-v2-playable-harness-v0.1';
const TRACE_SCHEMA_VERSION = 'skilled-v2-trace-schema-v0.1';

const CFG = {
  inputLockMs: 100,
  goodW: .42,
  perfectW: .17,
  sweepMin: .06,
  sweepSpan: .88,
  heavyYDelayMs: 85,
  recoverMs: 390,
  maxCycles: 3,
  contexts: {
    H0: { name: 'TIMING_BASELINE', pressureContext: 'BASELINE', oneWayMs: 1100, targetPolicy: 'stable', stateful: false, goalInputs: 80 },
    H1: { name: 'SUSTAINED_TEMPO', pressureContext: 'TEMPO', oneWayMs: 900, targetPolicy: 'low-turnover', stateful: false, goalInputs: 72 },
    H2: { name: 'DURABLE_RHYTHM', pressureContext: 'DURABLE', oneWayMs: 1100, targetPolicy: 'stable', stateful: false, goalInputs: 80 },
    H3: { name: 'TURNOVER_DENSITY', pressureContext: 'TURNOVER', oneWayMs: 1100, targetPolicy: 'high-turnover', stateful: false, goalInputs: 72 },
    H4: { name: 'STATEFUL_READ', pressureContext: 'STATEFUL', oneWayMs: 1100, targetPolicy: 'low-turnover', stateful: true, goalInputs: 72 },
    H5: { name: 'MIXED_PRESSURE', pressureContext: 'MIXED', oneWayMs: 960, targetPolicy: 'mixed', stateful: true, goalInputs: 90 }
  }
};

const $ = id => document.getElementById(id);
const canvas = $('game');
const ctx = canvas.getContext('2d');
let dpr = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
let W = 0, H = 0;

function resize() {
  W = canvas.clientWidth;
  H = canvas.clientHeight;
  canvas.width = Math.floor(W * dpr);
  canvas.height = Math.floor(H * dpr);
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}
addEventListener('resize', resize, {passive:true});
resize();

function uid() {
  if (crypto.randomUUID) return crypto.randomUUID();
  return `t-${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
}

function localPlayerId() {
  const key = 'td-skilled-v2-anon-id';
  let id = localStorage.getItem(key);
  if (!id) { id = `anon-${uid()}`; localStorage.setItem(key, id); }
  return id;
}

function nextAttemptIndex(harnessId) {
  const key = `td-skilled-v2-attempt-${harnessId}`;
  const n = Number(localStorage.getItem(key) || 0) + 1;
  localStorage.setItem(key, String(n));
  return n;
}

const S = {
  running: false,
  harnessId: 'H0',
  traceId: null,
  attemptIndex: 0,
  records: [],
  t0: 0,
  phase: 'idle',
  phaseStart: 0,
  dirX: 1,
  dirY: -1,
  target: null,
  targetId: 1,
  charge: 0,
  combo: 0,
  longestCombo: 0,
  seq: 0,
  inputCount: 0,
  attackCount: 0,
  lastActionAt: null,
  lastTargetIdAtAction: null,
  targetChangedSincePriorAction: false,
  noTargetSince: null,
  targetAvailableAt: 0,
  pendingTurnoverAt: null,
  heavyXJudge: null,
  pendingTap: false,
  lastResult: '',
  lastResultUntil: 0,
  charger: { active: false, windupStart: null, resolved: false, nextAtInput: 12 },
  validation: null,
  animationId: null
};

function nowMs() { return performance.now() - S.t0; }
function currentCfg() { return CFG.contexts[S.harnessId]; }
function rand(a,b) { return a + Math.random() * (b-a); }
function clamp(v,a,b) { return Math.max(a, Math.min(b,v)); }

function newTarget() {
  const m = .08;
  const gx = rand(m + CFG.goodW/2, 1 - m - CFG.goodW/2);
  const gy = rand(m + CFG.goodW/2, 1 - m - CFG.goodW/2);
  const px = clamp(gx + rand(-.10,.10), gx - CFG.goodW/2 + CFG.perfectW/2, gx + CFG.goodW/2 - CFG.perfectW/2);
  const py = clamp(gy + rand(-.10,.10), gy - CFG.goodW/2 + CFG.perfectW/2, gy + CFG.goodW/2 - CFG.perfectW/2);
  S.target = {gx, gy, px, py};
  S.targetId++;
  S.targetAvailableAt = nowMs();
  S.targetChangedSincePriorAction = true;
}

function stableInitialTarget() {
  S.target = {gx:.50, gy:.50, px:.50, py:.50};
  S.targetId = 1;
  S.targetAvailableAt = 0;
}

function sweepPos(now, dir) {
  const cfg = currentCfg();
  const leg = Math.max(0, now - S.phaseStart) / cfg.oneWayMs;
  const whole = Math.floor(leg);
  const f = leg - whole;
  let t = whole % 2 === 0 ? f : 1 - f;
  if (dir < 0) t = 1 - t;
  return CFG.sweepMin + CFG.sweepSpan * t;
}

function judge(value, axis) {
  const t = S.target;
  if (!t) return 'INVALID';
  const p = axis === 'x' ? t.px : t.py;
  const g = axis === 'x' ? t.gx : t.gy;
  if (Math.abs(value - p) <= CFG.perfectW/2) return 'PERFECT';
  if (Math.abs(value - g) <= CFG.goodW/2) return 'GOOD';
  return 'NORMAL';
}

function comboBreakCause(judgment, tactical=false) {
  if (judgment === 'PERFECT') return 'NONE';
  if (tactical) return 'TACTICAL_RESPONSE';
  if (S.targetChangedSincePriorAction) return 'TARGET_TURNOVER';
  if (!S.target) return 'NO_TARGET';
  return judgment === 'INVALID' ? 'INVALID_INPUT' : 'TIMING';
}

function updateCombo(judgment) {
  const before = S.combo;
  if (judgment === 'PERFECT') S.combo++;
  else S.combo = 0;
  S.longestCombo = Math.max(S.longestCombo, S.combo);
  return {before, after:S.combo};
}

function addRecord(record) { S.records.push(record); }

function stateEvent(state, extra={}) {
  addRecord({
    recordType:'STATE', traceId:S.traceId, harnessVersion:HARNESS_VERSION,
    harnessId:S.harnessId, atMs:Math.round(nowMs()), monsterId:extra.monsterId ?? S.targetId,
    monsterType:extra.monsterType || (S.harnessId === 'H4' || S.harnessId === 'H5' ? 'CHARGER' : 'HARNESS_TARGET'),
    state, ...extra
  });
}

function startSessionRecord() {
  addRecord({
    recordType:'SESSION_START', traceId:S.traceId, harnessVersion:HARNESS_VERSION,
    harnessId:S.harnessId, attemptIndex:S.attemptIndex,
    calibrationFlags:{lane:'HARNESS_ONLY',campaignPersistence:false,externalTelemetry:false,traceSchema:TRACE_SCHEMA_VERSION},
    anonymousPlayerId:localPlayerId(), classId:$('classId').value, powerMode:'HARNESS_NEUTRAL',
    startedAt:new Date().toISOString(),
    deviceContext:{userAgent:navigator.userAgent,viewport:[innerWidth,innerHeight],dpr:devicePixelRatio||1},
    inputSurfaceVersion:INPUT_SURFACE_VERSION
  });
}

function endSession(completedAsDesigned, reasons=[]) {
  if (!S.running) return;
  S.running = false;
  S.phase = 'idle';
  addRecord({recordType:'SESSION_END',traceId:S.traceId,harnessVersion:HARNESS_VERSION,harnessId:S.harnessId,endedAtMs:Math.round(nowMs()),completedAsDesigned:!!completedAsDesigned,exclusionReasons:reasons});
  S.validation = validateTrace(S.records);
  renderSummary();
  updateControls();
}

function scheduleTargetTurnover(delay=300) {
  if (S.pendingTurnoverAt != null || !S.running) return;
  S.target = null;
  S.noTargetSince = nowMs();
  stateEvent('NO_TARGET_START',{monsterId:S.targetId,monsterType:'HARNESS_TARGET'});
  const before = S.targetId;
  S.pendingTurnoverAt = performance.now() + delay;
  setTimeout(() => {
    if (!S.running) return;
    newTarget();
    stateEvent('NO_TARGET_END',{monsterId:S.targetId,monsterType:'HARNESS_TARGET'});
    stateEvent('TARGET_REORDER',{monsterId:S.targetId,monsterType:'HARNESS_TARGET',targetBefore:before,targetAfter:S.targetId});
    S.noTargetSince = null;
    S.pendingTurnoverAt = null;
  }, delay);
}

function maybeTurnoverAfterAttack() {
  const cfg = currentCfg();
  if (cfg.targetPolicy === 'stable') return;
  if (cfg.targetPolicy === 'low-turnover' && S.attackCount > 0 && S.attackCount % 10 === 0) scheduleTargetTurnover(280);
  if (cfg.targetPolicy === 'high-turnover' && S.attackCount > 0 && S.attackCount % 3 === 0) scheduleTargetTurnover(320);
  if (cfg.targetPolicy === 'mixed' && S.attackCount > 0 && S.attackCount % 5 === 0) scheduleTargetTurnover(300);
}

function maybeStartWindup() {
  const cfg = currentCfg();
  if (!cfg.stateful || S.charger.active || S.inputCount < S.charger.nextAtInput) return;
  S.charger.active = true;
  S.charger.resolved = false;
  S.charger.windupStart = nowMs();
  S.charger.nextAtInput += S.harnessId === 'H4' ? 12 : 16;
  stateEvent('WINDUP_START',{monsterId:9000 + S.attackCount, monsterType:'CHARGER', readableSinceMs:Math.round(S.charger.windupStart)});
  setTimeout(() => {
    if (!S.running || !S.charger.active || S.charger.resolved) return;
    S.charger.resolved = true;
    stateEvent('FULL_ACTIVATION',{monsterId:9000 + S.attackCount,monsterType:'CHARGER'});
    S.charger.active = false;
  }, 1200);
}

function recordInput(judgment, axis, heavyOpportunity, heavyAttempted, heavyCompleted, ppAttempted, ppCompleted) {
  const at = nowMs();
  const combo = updateCombo(judgment);
  const chargeBefore = S.charge;
  let chargeAfter = S.charge;
  if (heavyCompleted) { S.charge = 0; chargeAfter = 0; }
  else if (!heavyOpportunity) { S.charge = Math.min(3,S.charge+1); chargeAfter = S.charge; }

  const tactical = S.charger.active;
  let responseLatencyMs = null;
  if (tactical && !S.charger.resolved) {
    responseLatencyMs = Math.round(at - S.charger.windupStart);
    S.charger.resolved = true;
    const success = judgment === 'PERFECT' || judgment === 'GOOD';
    stateEvent(success ? 'INTERRUPTED' : 'WINDUP_END',{monsterId:9000 + S.attackCount,monsterType:'CHARGER',relatedActionSeq:S.seq + 1});
    S.charger.active = false;
  }

  const targetChanged = S.lastTargetIdAtAction != null && S.lastTargetIdAtAction !== S.targetId;
  const reacquireDelayMs = targetChanged ? Math.max(0,Math.round(at - S.targetAvailableAt)) : null;
  const noTargetWaitMsBeforeAction = S.noTargetSince != null ? Math.max(0,Math.round(at - S.noTargetSince)) : 0;
  const breakCause = combo.after < combo.before ? comboBreakCause(judgment,tactical) : (judgment === 'PERFECT' ? 'NONE' : comboBreakCause(judgment,tactical));

  S.seq++;
  addRecord({
    recordType:'ACTION',traceId:S.traceId,harnessVersion:HARNESS_VERSION,harnessId:S.harnessId,
    seq:S.seq,atMs:Math.round(at),pressureContext:currentCfg().pressureContext,judgment,
    comboBefore:combo.before,comboAfter:combo.after,comboBreakCause:breakCause,
    chargeBefore,chargeAfter,heavyOpportunity:!!heavyOpportunity,heavyAttempted:!!heavyAttempted,
    heavyCompleted:!!heavyCompleted,ppAttempted:!!ppAttempted,ppCompleted:!!ppCompleted,
    targetId:S.target ? S.targetId : null,targetType:S.harnessId === 'H1' ? 'RUNNER' : S.harnessId === 'H2' ? 'BRUTE' : tactical ? 'CHARGER' : 'HARNESS_TARGET',
    targetGeneration:0,targetChangedSincePriorAction:!!targetChanged,noTargetWaitMsBeforeAction,
    interActionMs:S.lastActionAt == null ? null : Math.round(at-S.lastActionAt),reacquireDelayMs,axis,tacticalResponseLatencyMs:responseLatencyMs
  });
  S.lastActionAt = at;
  S.lastTargetIdAtAction = S.target ? S.targetId : S.lastTargetIdAtAction;
  S.targetChangedSincePriorAction = false;
  S.inputCount++;
}

function completeAttack() {
  S.attackCount++;
  maybeTurnoverAfterAttack();
  maybeStartWindup();
  if (S.inputCount >= currentCfg().goalInputs) { endSession(true, []); return; }
  S.phase = 'recover';
  S.phaseStart = performance.now();
  setTimeout(() => {
    if (!S.running) return;
    S.phase = 'x';
    S.phaseStart = performance.now();
    S.dirX = S.attackCount % 2 ? -1 : 1;
    S.dirY = S.attackCount % 2 ? 1 : -1;
  }, CFG.recoverMs);
}

function handleTap() {
  if (!S.running || !S.target) return;
  const now = performance.now();
  if (S.phase !== 'x' && S.phase !== 'y') return;
  if (now - S.phaseStart < CFG.inputLockMs) { S.pendingTap = true; return; }
  const heavyOpportunity = S.charge >= 3;
  if (S.phase === 'x') {
    const j = judge(sweepPos(now,S.dirX),'x');
    if (heavyOpportunity) {
      S.heavyXJudge = j;
      recordInput(j,'x',true,true,false,true,false);
      S.phase = 'y-wait';
      S.phaseStart = now;
      setTimeout(() => { if (S.running) { S.phase='y'; S.phaseStart=performance.now(); } }, CFG.heavyYDelayMs);
      S.lastResult = `${j} · X LOCK`;
    } else {
      recordInput(j,'x',false,false,false,false,false);
      S.lastResult = j;
      completeAttack();
    }
  } else {
    const j = judge(sweepPos(now,S.dirY),'y');
    const pp = S.heavyXJudge === 'PERFECT' && j === 'PERFECT';
    recordInput(j,'y',true,true,true,true,pp);
    S.lastResult = pp ? 'P×P · CRITICAL' : `${S.heavyXJudge}+${j}`;
    S.heavyXJudge = null;
    completeAttack();
  }
  S.lastResultUntil = performance.now() + 500;
  renderStats();
}

function startRun() {
  if (S.running) endSession(false,['RESTARTED']);
  S.harnessId = $('harnessId').value;
  S.traceId = uid();
  S.attemptIndex = nextAttemptIndex(S.harnessId);
  S.records = [];
  S.running = true;
  S.t0 = performance.now();
  S.phase='x';S.phaseStart=S.t0;S.dirX=1;S.dirY=-1;S.charge=0;S.combo=0;S.longestCombo=0;S.seq=0;
  S.inputCount=0;S.attackCount=0;S.lastActionAt=null;S.lastTargetIdAtAction=null;S.targetChangedSincePriorAction=false;
  S.noTargetSince=null;S.pendingTurnoverAt=null;S.heavyXJudge=null;S.lastResult='';S.validation=null;
  S.charger={active:false,windupStart:null,resolved:false,nextAtInput:S.harnessId==='H4'?10:14};
  stableInitialTarget();
  startSessionRecord();
  renderSummary();updateControls();renderStats();
}

function abortRun(){if(S.running)endSession(false,['ABORTED_BY_USER']);}

function validateTrace(records) {
  const errors=[];
  const starts=records.filter(r=>r.recordType==='SESSION_START');
  const ends=records.filter(r=>r.recordType==='SESSION_END');
  const actions=records.filter(r=>r.recordType==='ACTION');
  const states=records.filter(r=>r.recordType==='STATE');
  if(starts.length!==1)errors.push(`SESSION_START count ${starts.length}`);
  if(ends.length!==1)errors.push(`SESSION_END count ${ends.length}`);
  for(let i=1;i<actions.length;i++)if(actions[i].seq<=actions[i-1].seq)errors.push('ACTION seq not strictly increasing');
  for(const a of actions){
    if(a.heavyCompleted&&!a.heavyAttempted)errors.push(`seq ${a.seq}: heavy completion without attempt`);
    if(a.ppCompleted&&!a.ppAttempted)errors.push(`seq ${a.seq}: P×P completion without attempt`);
    if(a.heavyAttempted&&!a.heavyOpportunity)errors.push(`seq ${a.seq}: heavy attempt without opportunity`);
    if(a.comboAfter<a.comboBefore&&a.comboBreakCause==='NONE')errors.push(`seq ${a.seq}: combo break unexplained`);
    if(a.pressureContext!==currentCfg().pressureContext)errors.push(`seq ${a.seq}: pressure context mismatch`);
  }
  if(S.harnessId==='H0'&&actions.length<40)errors.push('H0 completed with <40 action opportunities');
  if(S.harnessId==='H3'&&!states.some(s=>s.state==='TARGET_REORDER'))errors.push('H3 missing turnover evidence');
  if(S.harnessId==='H4'&&!states.some(s=>s.state==='WINDUP_START'))errors.push('H4 missing readable stateful evidence');
  return{ok:errors.length===0,errors,actionCount:actions.length,stateCount:states.length};
}

function jsonl(){return S.records.map(r=>JSON.stringify(r)).join('\n');}
async function copyTrace(){if(!S.records.length)return;await navigator.clipboard.writeText(jsonl());$('copyTrace').textContent='복사됨';setTimeout(()=>$('copyTrace').textContent='JSONL 복사',900);}
function downloadTrace(){if(!S.records.length)return;const blob=new Blob([jsonl()+'\n'],{type:'application/x-ndjson'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=`${S.harnessId}-${S.traceId}.jsonl`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
function resetIdentity(){localStorage.removeItem('td-skilled-v2-anon-id');$('anonId').textContent=localPlayerId();}
function renderStats(){$('combo').textContent=S.combo;$('longest').textContent=S.longestCombo;$('charge').textContent=`${S.charge}/3`;$('inputs').textContent=`${S.inputCount}/${currentCfg().goalInputs}`;$('phase').textContent=S.phase.toUpperCase();}
function renderSummary(){const v=S.validation;$('traceInfo').textContent=S.traceId?`${S.harnessId} · ${S.traceId}`:'아직 실행 안 됨';$('validation').textContent=v?(v.ok?`PASS · actions ${v.actionCount} · states ${v.stateCount}`:`FAIL · ${v.errors.join(' | ')}`):'검증 대기';$('validation').className=v?(v.ok?'ok':'err'):'';$('recordCount').textContent=String(S.records.length);}
function updateControls(){$('start').disabled=S.running;$('abort').disabled=!S.running;$('harnessId').disabled=S.running;$('classId').disabled=S.running;}

function draw(){
  ctx.clearRect(0,0,W,H);ctx.fillStyle='#0c1210';ctx.fillRect(0,0,W,H);
  const pad=24,box=Math.min(W-2*pad,H-2*pad,440),x=(W-box)/2,y=(H-box)/2;
  ctx.fillStyle='#121b17';ctx.fillRect(x,y,box,box);ctx.strokeStyle='rgba(255,255,255,.12)';ctx.lineWidth=2;ctx.strokeRect(x,y,box,box);
  if(S.target){
    const gx=x+(S.target.gx-CFG.goodW/2)*box,gy=y+(S.target.gy-CFG.goodW/2)*box;
    ctx.fillStyle='rgba(194,225,207,.10)';ctx.fillRect(gx,gy,CFG.goodW*box,CFG.goodW*box);ctx.strokeStyle='rgba(194,225,207,.55)';ctx.strokeRect(gx,gy,CFG.goodW*box,CFG.goodW*box);
    const px=x+(S.target.px-CFG.perfectW/2)*box,py=y+(S.target.py-CFG.perfectW/2)*box;
    ctx.fillStyle='rgba(239,223,168,.14)';ctx.fillRect(px,py,CFG.perfectW*box,CFG.perfectW*box);ctx.strokeStyle='#efdfa8';ctx.lineWidth=2;ctx.strokeRect(px,py,CFG.perfectW*box,CFG.perfectW*box);
  }
  if(S.running&&(S.phase==='x'||S.phase==='y')){
    const p=sweepPos(performance.now(),S.phase==='x'?S.dirX:S.dirY);ctx.strokeStyle=S.phase==='x'?'#80d6ff':'#ffb9d6';ctx.lineWidth=4;
    if(S.phase==='x'){const sx=x+p*box;ctx.beginPath();ctx.moveTo(sx,y);ctx.lineTo(sx,y+box);ctx.stroke();}else{const sy=y+p*box;ctx.beginPath();ctx.moveTo(x,sy);ctx.lineTo(x+box,sy);ctx.stroke();}
  }
  if(S.charger.active){const t=Math.max(0,Math.min(1,(nowMs()-S.charger.windupStart)/1200));ctx.fillStyle=`rgba(255,92,92,${.08+.18*t})`;ctx.fillRect(x,y,box,box);ctx.fillStyle='#ffb2b2';ctx.font='900 24px system-ui';ctx.textAlign='center';ctx.fillText('CHARGER WINDUP',W/2,y+34);}
  if(!S.target&&S.running){ctx.fillStyle='#e6d17f';ctx.font='800 20px system-ui';ctx.textAlign='center';ctx.fillText('TARGET TURNOVER',W/2,H/2);}
  if(performance.now()<S.lastResultUntil){ctx.fillStyle='#f3f6f4';ctx.font='900 22px system-ui';ctx.textAlign='center';ctx.fillText(S.lastResult,W/2,y+box-18);}
  if(S.pendingTap&&(S.phase==='x'||S.phase==='y')&&performance.now()-S.phaseStart>=CFG.inputLockMs){S.pendingTap=false;handleTap();}
  if(S.running&&(S.phase==='x'||S.phase==='y')){
    const max=currentCfg().oneWayMs*CFG.maxCycles*2;
    if(performance.now()-S.phaseStart>max){
      const heavy=S.charge>=3;recordInput('MISS',S.phase==='x'?'x':'y',heavy,heavy,heavy&&S.phase==='y',heavy,false);S.lastResult='MISS';S.lastResultUntil=performance.now()+500;
      if(S.phase==='x'&&heavy){S.heavyXJudge='MISS';S.phase='y';S.phaseStart=performance.now();}else completeAttack();
    }
  }
  requestAnimationFrame(draw);
}

$('start').addEventListener('click',startRun);
$('abort').addEventListener('click',abortRun);
$('copyTrace').addEventListener('click',()=>copyTrace().catch(()=>{}));
$('downloadTrace').addEventListener('click',downloadTrace);
$('resetIdentity').addEventListener('click',resetIdentity);
$('harnessId').addEventListener('change',()=>{S.harnessId=$('harnessId').value;renderStats();});
$('game').addEventListener('pointerdown',e=>{e.preventDefault();handleTap();},{passive:false});
addEventListener('keydown',e=>{if(e.code==='Space'){e.preventDefault();handleTap();}});

$('anonId').textContent=localPlayerId();
renderStats();renderSummary();updateControls();draw();
