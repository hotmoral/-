import {
  HUMAN_COLLECTION_ENABLED, RUNTIME_MODE, EXPORT_ELIGIBILITY,
  PILOT_BUNDLE_FINGERPRINT, ORDER_PLAN_FINGERPRINT, PRESENTATION_VERSION,
  WARMUPS, PARTICIPANT_COPY
} from './config.mjs';
import { applyMove, canonicalPath, isSolved, legalDestinations, stateSerialization } from './mechanic.mjs';
import { comprehensionFailure, comprehensionPass, assertCalibrationAllowed, nextAfterAttempt } from './flow.mjs';
import {
  EventLog, RuntimeClock, validateBundle, validateOrderPlan, resolveForm,
  reconstructAttempt, sha256, validateEventStream, randomOpaqueId, makeValidationExport
} from './protocol.mjs';

if (HUMAN_COLLECTION_ENABLED !== false) throw new Error('HUMAN_COLLECTION_MUST_REMAIN_DISABLED');
if (RUNTIME_MODE !== 'PRE_HUMAN_VALIDATION') throw new Error('RUNTIME_MODE_MISMATCH');

const screen=document.querySelector('#screen');
const clock=new RuntimeClock();
let bundle,plan;
let formId=null,formRows=null;
let participantAnonId=null,sessionId=null,sessionLog=null;
let comprehensionPassed=false;
let warmupIndex=0,warmupFailureCount=0;
let calibrationIndex=0;
let current=null,path=[],selected=null,inputEnabled=false,finished=false;
let attemptLog=null,attemptIdentity=null;
const attempts=[];

function el(tag,cls,text){const node=document.createElement(tag);if(cls)node.className=cls;if(text!==undefined)node.textContent=text;return node;}
function button(label,cls='primary'){const b=el('button',cls,label);b.type='button';return b;}
function clear(){screen.replaceChildren();}
function panel(title,body){clear();const p=el('div','panel');p.append(el('h1','',title));if(body)p.append(el('p','',body));screen.append(p);return p;}
function emitSession(type,payload={}){if(!sessionLog)throw new Error('NO_SESSION_LOG');return sessionLog.emit(type,payload,{});}
function attemptEmit(type,payload={}){if(!attemptLog)throw new Error('NO_ATTEMPT_LOG');return attemptLog.emit(type,payload,attemptIdentity);}

function lineOverlay(puzzlePath,n){
  const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 100 100');svg.classList.add('links');
  for(let i=1;i<puzzlePath.length;i++){
    const [a,b]=[puzzlePath[i-1],puzzlePath[i]];const [ar,ac]=[Math.floor(a/n),a%n], [br,bc]=[Math.floor(b/n),b%n];
    const line=document.createElementNS('http://www.w3.org/2000/svg','line');const pos=(r,c)=>[(c+.5)*100/n,(r+.5)*100/n];
    const [x1,y1]=pos(ar,ac),[x2,y2]=pos(br,bc);for(const [k,v] of Object.entries({x1,y1,x2,y2}))line.setAttribute(k,v);svg.append(line);
  }
  return svg;
}

function renderBoard(puzzle,onCell,{guidedEndpointCell=null,guidedDestination=null}={}){
  const wrap=el('div','board-wrap');const grid=el('div','board');grid.style.gridTemplateColumns=`repeat(${puzzle.n},1fr)`;grid.style.gridTemplateRows=`repeat(${puzzle.n},1fr)`;
  const occupied=new Map(path.map((cell,index)=>[cell,index]));const legal=new Set(selected===null?[]:legalDestinations(puzzle.n,path,selected));
  for(let cell=0;cell<puzzle.n*puzzle.n;cell++){
    const c=button('','cell');c.setAttribute('aria-label',`칸 ${cell}`);
    if(puzzle.targets.includes(cell))c.classList.add('target');
    if(occupied.has(cell)){const idx=occupied.get(cell);c.classList.add('chain');if(idx===0||idx===path.length-1)c.classList.add('endpoint');if(idx===selected)c.classList.add('selected');}
    if(legal.has(cell))c.classList.add('legal');
    if((selected===null&&cell===guidedEndpointCell)||(selected!==null&&cell===guidedDestination&&legal.has(cell)))c.classList.add('guide');
    c.addEventListener('click',()=>onCell(cell,occupied.get(cell),legal.has(cell)));grid.append(c);
  }
  wrap.append(lineOverlay(path,puzzle.n),grid);return wrap;
}

async function stateFp(){return sha256(stateSerialization(current.n,path));}

function showStudyInfo(){
  const p=panel('Linkline 사전 검증','이 화면은 실제 연구 데이터 수집 전의 기술 검증용 웹앱입니다.');
  const notice=el('div','notice','현재 HUMAN_COLLECTION_ENABLED=false 입니다. 이 버전에서 만들어지는 파일은 연구 데이터가 아니라 TECHNICAL_VALIDATION_ONLY 검증 자료입니다.');
  const copy=el('div','copy');
  for(const [title,text] of [[PARTICIPANT_COPY.goalTitle,PARTICIPANT_COPY.goal],[PARTICIPANT_COPY.howTitle,PARTICIPANT_COPY.how],[PARTICIPANT_COPY.toolsTitle,PARTICIPANT_COPY.tools]]){
    const block=el('div','copy-block');block.append(el('h3','',title),el('p','',text));copy.append(block);
  }
  const operator=el('div','operator');operator.append(el('label','','기술 검증용 Form 선택'));
  const select=document.createElement('select');for(const id of ['F1','F2','F3','F4']){const o=document.createElement('option');o.value=id;o.textContent=id;select.append(o);}operator.append(select);
  const start=button('안내 확인하고 시작');
  start.onclick=()=>beginSession(select.value);
  p.append(notice,copy,operator,start);
}

function beginSession(chosenForm){
  if(formId!==null)throw new Error('FORM_ALREADY_LOCKED');
  if(!/^F[1-4]$/.test(chosenForm))throw new Error('FORM');
  formId=chosenForm;formRows=resolveForm(plan,bundle,formId);
  participantAnonId=randomOpaqueId('PARTICIPANT');sessionId=randomOpaqueId('SESSION');sessionLog=new EventLog({sessionId,participantAnonId,clock});
  emitSession('SESSION_STARTED',{mode:RUNTIME_MODE,formId,eligibility:EXPORT_ELIGIBILITY});
  emitSession('INSTRUCTION_COMPLETED');
  startWarmup(0);
}

function startWarmup(index){
  warmupIndex=index;current=WARMUPS[index];path=canonicalPath(current.initial);selected=null;inputEnabled=true;finished=false;
  emitSession('WARMUP_STARTED',{warmupIndex:index+1,warmupId:current.id});renderWarmup();
}

function renderWarmup(message=''){
  clear();const w=current;screen.append(el('div','warmup-label',w.label));
  const status=el('div','status',message);
  const guided=warmupIndex<2?{guidedEndpointCell:w.guidedEndpointCell,guidedDestination:w.guidedDestination}:{};
  screen.append(renderBoard(w,onWarmupCell,guided),status);
  if(warmupIndex===2){const stop=button('연습 종료','secondary');stop.onclick=failComprehension;screen.append(stop);}
}

function onWarmupCell(cell,idx,isLegal){
  if(!inputEnabled)return;
  const w=current;
  if(idx===0||idx===path.length-1){
    if(warmupIndex<2 && path[idx]!==w.guidedEndpointCell){renderWarmup('표시된 끝을 눌러 보세요.');return;}
    selected=idx;renderWarmup();return;
  }
  if(isLegal&&selected!==null){
    if(warmupIndex<2 && cell!==w.guidedDestination){renderWarmup('표시된 목표 칸을 눌러 보세요.');return;}
    path=applyMove(w.n,path,selected,cell);selected=null;
    if(isSolved(path,w.targets)){inputEnabled=false;emitSession('WARMUP_COMPLETED',{warmupIndex:warmupIndex+1,warmupId:w.id});showWarmupDone();}
    else renderWarmup();
  }
}

function showWarmupDone(){
  clear();const p=el('div','panel');p.append(el('h2','',warmupIndex===2?'연습 완료':'연습 완료'));
  const next=button(warmupIndex<2?'다음 연습':'문제 시작');
  next.onclick=()=>{
    if(warmupIndex<2)startWarmup(warmupIndex+1);
    else passComprehension();
  };
  p.append(next);screen.append(p);
}

function failComprehension(){
  if(warmupIndex!==2||comprehensionPassed)return;
  const outcome=comprehensionFailure(warmupFailureCount);warmupFailureCount=outcome.failureCount;
  if(outcome.result==='RETRY'){
    emitSession('COMPREHENSION_GATE_RESULT',{result:outcome.result,failureCount:warmupFailureCount});
    const p=panel('움직이는 방법을 한 번 더 확인한 뒤 다시 해보세요.','줄의 두 끝 중 하나를 누르면 갈 수 있는 빈칸이 표시됩니다. 표시된 칸을 누르면 줄 전체가 따라 움직입니다.');
    const retry=button('연습 3 다시 하기');retry.onclick=()=>startWarmup(2);p.append(retry);return;
  }
  emitSession('COMPREHENSION_GATE_RESULT',{result:outcome.result,failureCount:warmupFailureCount});
  emitSession('SESSION_ENDED',{reason:'COMPREHENSION_NOT_ESTABLISHED'});
  const p=panel('이번 테스트는 여기서 종료됩니다.','참여해 주셔서 감사합니다.');p.append(el('div','notice','Calibration은 시작되지 않았습니다.')); 
}

function passComprehension(){
  if(warmupIndex!==2)throw new Error('COMPREHENSION_SEQUENCE');
  const outcome=comprehensionPass(warmupFailureCount);comprehensionPassed=outcome.calibrationAllowed;emitSession('COMPREHENSION_GATE_RESULT',{result:outcome.result,failureCount:outcome.failureCount});startCalibration(0);
}

function identityFor(row,index){return {attemptId:`ATTEMPT-${formId}-${String(index+1).padStart(2,'0')}-${sessionId.slice(-8)}`,puzzleResearchId:row.puzzle.researchPuzzleId,researchEquivalenceIdV1:row.puzzle.id,puzzleFingerprint:row.puzzle.puzzleFingerprint};}

function startCalibration(index){
  assertCalibrationAllowed(comprehensionPassed);
  calibrationIndex=index;if(index>=12){completeSession();return;}
  const row=formRows[index];current=row.puzzle;path=canonicalPath(current.initial);selected=null;inputEnabled=true;finished=false;
  attemptLog=new EventLog({sessionId,participantAnonId,clock});attemptIdentity=identityFor(row,index);attemptEmit('PUZZLE_PRESENTED');attemptEmit('INPUT_ENABLED');renderCalibration();
}

function renderCalibration(message=''){
  clear();screen.append(el('div','progress',`문제 ${calibrationIndex+1} / 12`));const status=el('div','status',message);
  screen.append(renderBoard(current,onCalibrationCell),status);
  const actions=el('div','actions');const restart=button('처음부터','secondary');restart.onclick=restartAttempt;const abandon=button('문제 끝내기','danger');abandon.onclick=abandonAttempt;actions.append(restart,abandon);screen.append(actions);
}

async function onCalibrationCell(cell,idx,isLegal){
  if(!inputEnabled||finished||document.hidden)return;
  if(idx===0||idx===path.length-1){selected=idx;attemptEmit('ENDPOINT_SELECTED',{endpointIndex:idx});renderCalibration();return;}
  if(!isLegal||selected===null)return;
  const source=path[selected];attemptEmit('ACTION_SUBMITTED',{source,destination:cell});const pre=await stateFp();path=applyMove(current.n,path,selected,cell);selected=null;const post=await stateFp();attemptEmit('ACTION_ACCEPTED',{source,destination:cell,preStateFingerprint:pre,postStateFingerprint:post});
  inputEnabled=false;attemptEmit('INPUT_DISABLED');renderCalibration();
  setTimeout(()=>{
    if(isSolved(path,current.targets)){attemptEmit('PUZZLE_SOLVED');finishAttempt('완료');}
    else{inputEnabled=true;attemptEmit('INPUT_ENABLED');renderCalibration();}
  },140);
}

function restartAttempt(){if(!inputEnabled||finished)return;attemptEmit('PUZZLE_RESTARTED');path=canonicalPath(current.initial);selected=null;renderCalibration();}
function abandonAttempt(){if(finished)return;if(confirm('현재 문제를 여기서 끝낼까요?')){attemptEmit('PUZZLE_ABANDONED');finishAttempt('문제를 종료했습니다.');}}

function finishAttempt(label){
  finished=true;inputEnabled=false;const observation=reconstructAttempt(attemptLog.events,current.shortestDistance);
  showRating(label,observation);
}

function showRating(label,observation){
  clear();const p=el('div','panel');p.append(el('h2','',label),el('p','','방금 문제는 얼마나 어렵게 느껴졌나요?'));
  const rating=el('div','rating');
  const labels=['매우 쉬웠다','쉬웠다','보통이었다','어려웠다','매우 어려웠다'];
  labels.forEach((text,i)=>{const b=button('', 'rating-button');b.append(el('span','',String(i+1)),document.createTextNode(text));b.onclick=()=>commitAttempt(observation,i+1);rating.append(b);});
  const skip=button('응답하지 않기','secondary');skip.onclick=()=>commitAttempt(observation,null);p.append(rating,skip);screen.append(p);
}

function commitAttempt(observation,selfRatedDifficulty){
  attempts.push({attemptId:attemptIdentity.attemptId,puzzleId:current.id,events:attemptLog.events,summary:{...observation,selfRatedDifficulty}});
  const next=nextAfterAttempt(calibrationIndex);if(next.kind==='BREAK')showBreak();else if(next.kind==='COMPLETE')completeSession();else startCalibration(next.nextIndex);
}

function showBreak(){
  clear();const p=el('div','panel');p.append(el('div','break-mark','BREAK'),el('h2','','여기까지 6문제를 풀었습니다.'),el('p','','원하면 잠시 쉬었다가 계속하세요.'));
  const b=button('계속하기');b.onclick=()=>startCalibration(6);p.append(b);screen.append(p);
}

function validateExportPayload(payload){
  const errors=[];
  if(payload.eligibility!=='TECHNICAL_VALIDATION_ONLY')errors.push('eligibility');
  if(payload.humanCollectionEnabled!==false)errors.push('collectionLock');
  if(payload.runtimeMode!=='PRE_HUMAN_VALIDATION')errors.push('runtimeMode');
  if(payload.attempts.length!==12)errors.push('attemptCount');
  const directIdentifierKeys=new Set(['name','email','phone','address','exactLocation','ipAddress','userAgent','deviceFingerprint']);
  const walk=(value)=>{if(!value||typeof value!=='object')return;for(const [k,v] of Object.entries(value)){if(directIdentifierKeys.has(k))errors.push(`directIdentifier:${k}`);walk(v);}};walk(payload);
  return [...new Set(errors)].sort();
}

function completeSession(){
  emitSession('SESSION_ENDED',{reason:'TECHNICAL_VALIDATION_COMPLETE'});
  const streamErrors=[...validateEventStream(sessionLog.events),...attempts.flatMap((row,index)=>validateEventStream(row.events).map(e=>`attempt${index+1}:${e}`))];
  const exportBundle=makeValidationExport({formId,sessionEvents:sessionLog.events,attempts,participantAnonId,sessionId});
  const exportErrors=validateExportPayload(exportBundle);const all=[...streamErrors,...exportErrors];
  clear();const p=el('div','panel');p.append(el('h2','','모든 문제가 끝났습니다.'),el('p','','참여해 주셔서 감사합니다.'));
  const notice=el('div','notice',all.length?'기술 검증 내보내기 검사에 실패했습니다.':'기술 검증용 로컬 JSON을 만들 수 있습니다. 실제 연구 데이터로 사용할 수 없는 검증 전용 파일입니다.');p.append(notice);
  const exportButton=button('기술 검증 JSON 내보내기','secondary');exportButton.disabled=all.length>0;exportButton.onclick=()=>downloadJson(exportBundle);p.append(exportButton);
  const meta=el('div','debug',`mode=${RUNTIME_MODE} · eligibility=${EXPORT_ELIGIBILITY} · form=${formId} · attempts=${attempts.length} · bundle=${PILOT_BUNDLE_FINGERPRINT.slice(0,10)}… · order=${ORDER_PLAN_FINGERPRINT.slice(0,10)}…`);p.append(meta);screen.append(p);
}

function downloadJson(data){const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`linkline-a3-${formId}-technical-validation.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),0);}

document.addEventListener('visibilitychange',()=>{if(!attemptLog||finished)return;if(document.hidden)attemptEmit('VISIBILITY_PAUSED');else attemptEmit('VISIBILITY_RESUMED');});
window.addEventListener('pagehide',()=>{if(attemptLog&&!finished){try{attemptEmit('SESSION_ENDED');}catch{}}});

async function init(){
  const [b,p]=await Promise.all([fetch('./data/pilot_bundle_v0_1.json').then(r=>{if(!r.ok)throw new Error('BUNDLE_LOAD');return r.json();}),fetch('./data/order_plan_v0_1.json').then(r=>{if(!r.ok)throw new Error('ORDER_LOAD');return r.json();})]);
  bundle=b;plan=p;const errors=[...await validateBundle(bundle),...await validateOrderPlan(plan,bundle)];if(errors.length)throw new Error('PREFLIGHT_INPUT_INVALID:'+errors.join(','));showStudyInfo();
}

init().catch(error=>{clear();const p=el('div','panel');p.append(el('h2','','초기화 실패'),el('p','',error.message));screen.append(p);console.error(error);});