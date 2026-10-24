import {
  HUMAN_COLLECTION_ENABLED,RUNTIME_MODE,EXPORT_ELIGIBILITY,TESTER_PROFILE,PRESENTATION_VERSION,MECHANIC_BASELINE,
  POOL_FINGERPRINT,ORDER_PLAN_FINGERPRINT,SELF_TEST_SESSION_ID,SESSION_BUNDLE_FINGERPRINT,SESSION_START_LABEL,SESSION_COMPLETE_LABEL
} from './config.mjs';
import {applyMove,canonicalPath,isSolved,legalDestinations,stateSerialization} from './mechanic.mjs';
import {EventLog,RuntimeClock,validateSessionBundle,reconstructAttempt,sha256,validateEventStream,randomOpaqueId,makeSelfCalibrationExport} from './protocol.mjs';

if(HUMAN_COLLECTION_ENABLED!==false)throw new Error('HUMAN_COLLECTION_MUST_REMAIN_DISABLED');
if(RUNTIME_MODE!=='PRODUCT_OWNER_SELF_CALIBRATION')throw new Error('RUNTIME_MODE_MISMATCH');
if(EXPORT_ELIGIBILITY!=='SINGLE_TESTER_CALIBRATION_ONLY')throw new Error('EXPORT_ELIGIBILITY_MISMATCH');
if(TESTER_PROFILE!=='PRODUCT_OWNER_PRACTICED')throw new Error('TESTER_PROFILE_MISMATCH');

document.title='Linkline — Product Owner Self Calibration';
const modeNode=document.querySelector('.mode');if(modeNode)modeNode.textContent='자가 보정';
const screen=document.querySelector('#screen');
const clock=new RuntimeClock();
let bundle=null,sessionRunId=null,sessionLog=null;
let attemptIndex=0,current=null,path=[],selected=null,inputEnabled=false,finished=false;
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
    const [a,b]=[puzzlePath[i-1],puzzlePath[i]];const [ar,ac]=[Math.floor(a/n),a%n],[br,bc]=[Math.floor(b/n),b%n];
    const line=document.createElementNS('http://www.w3.org/2000/svg','line');const pos=(r,c)=>[(c+.5)*100/n,(r+.5)*100/n];
    const [x1,y1]=pos(ar,ac),[x2,y2]=pos(br,bc);for(const [key,value] of Object.entries({x1,y1,x2,y2}))line.setAttribute(key,value);svg.append(line);
  }
  return svg;
}

function renderBoard(puzzle,onCell){
  const wrap=el('div','board-wrap');const grid=el('div','board');grid.style.gridTemplateColumns=`repeat(${puzzle.n},1fr)`;grid.style.gridTemplateRows=`repeat(${puzzle.n},1fr)`;
  const occupied=new Map(path.map((cell,index)=>[cell,index]));const legal=new Set(selected===null?[]:legalDestinations(puzzle.n,path,selected));
  for(let cell=0;cell<puzzle.n*puzzle.n;cell++){
    const c=button('','cell');c.setAttribute('aria-label',`칸 ${cell}`);
    if(puzzle.targets.includes(cell))c.classList.add('target');
    if(occupied.has(cell)){const idx=occupied.get(cell);c.classList.add('chain');if(idx===0||idx===path.length-1)c.classList.add('endpoint');if(idx===selected)c.classList.add('selected');}
    if(legal.has(cell))c.classList.add('legal');
    c.addEventListener('click',()=>onCell(cell,occupied.get(cell),legal.has(cell)));grid.append(c);
  }
  wrap.append(lineOverlay(path,puzzle.n),grid);return wrap;
}

async function stateFp(){return sha256(stateSerialization(current.n,path));}

function showInfo(){
  const p=panel('Product Owner 자가 보정','이번 세션은 처음 보는 12문제의 상대 난이도를 기록하기 위한 1인 테스트입니다.');
  const notice=el('div','notice','외부 참가자 데이터 수집은 꺼져 있습니다. 결과는 이 기기에서 JSON으로만 내보내며 자동 업로드하지 않습니다.');
  const copy=el('div','copy');
  for(const [title,text] of [
    ['목표','연결된 줄의 두 끝을 두 목표 칸에 하나씩 놓으면 해결됩니다. 어느 끝이 어느 목표 칸에 들어가도 됩니다.'],
    ['조작','줄의 끝을 잡고 드래그하면 지나간 빈칸을 따라 줄이 움직입니다. 끝을 누른 뒤 표시된 칸을 다시 누르는 탭 방식도 사용할 수 있습니다.'],
    ['기록','문제마다 해결 여부, 이동·재시작, 활성 시간, 중단 여부와 선택적 1~5 체감 난이도를 기록합니다. 최단거리나 구조 분석값은 화면과 export에 포함하지 않습니다.']
  ]){const block=el('div','copy-block');block.append(el('h3','',title),el('p','',text));copy.append(block);}
  const start=button(SESSION_START_LABEL);start.onclick=beginSession;
  p.append(notice,copy,start);
}

function beginSession(){
  if(sessionRunId!==null)throw new Error('SESSION_ALREADY_STARTED');
  sessionRunId=randomOpaqueId('RUN');sessionLog=new EventLog({sessionRunId,clock});
  emitSession('SESSION_STARTED',{mode:RUNTIME_MODE,eligibility:EXPORT_ELIGIBILITY,testerProfile:TESTER_PROFILE,selfTestSessionId:SELF_TEST_SESSION_ID});
  emitSession('INSTRUCTION_COMPLETED');startAttempt(0);
}

function identityFor(puzzle,index){return {attemptId:`ATTEMPT-${SELF_TEST_SESSION_ID}-${String(index+1).padStart(2,'0')}-${sessionRunId.slice(-8)}`,puzzleResearchId:puzzle.researchPuzzleId,researchEquivalenceIdV1:puzzle.researchEquivalenceIdV1,puzzleFingerprint:puzzle.puzzleFingerprint};}

function startAttempt(index){
  attemptIndex=index;if(index>=12){completeSession();return;}
  current=bundle.puzzles[index];path=canonicalPath(current.initial);selected=null;inputEnabled=true;finished=false;
  attemptLog=new EventLog({sessionRunId,clock});attemptIdentity=identityFor(current,index);attemptEmit('PUZZLE_PRESENTED');attemptEmit('INPUT_ENABLED');renderAttempt();
}

function renderAttempt(message=''){
  clear();screen.append(el('div','progress',`문제 ${attemptIndex+1} / 12`));const status=el('div','status',message);
  screen.append(renderBoard(current,onCell),status);
  const actions=el('div','actions');const restart=button('처음부터','secondary');restart.onclick=restartAttempt;const abandon=button('문제 끝내기','danger');abandon.onclick=abandonAttempt;actions.append(restart,abandon);screen.append(actions);
}

async function onCell(cell,idx,isLegal){
  if(!inputEnabled||finished||document.hidden)return;
  if(idx===0||idx===path.length-1){selected=idx;attemptEmit('ENDPOINT_SELECTED',{endpointIndex:idx});renderAttempt();return;}
  if(!isLegal||selected===null)return;
  const source=path[selected];attemptEmit('ACTION_SUBMITTED',{source,destination:cell});const pre=await stateFp();path=applyMove(current.n,path,selected,cell);selected=null;const post=await stateFp();attemptEmit('ACTION_ACCEPTED',{source,destination:cell,preStateFingerprint:pre,postStateFingerprint:post});
  inputEnabled=false;attemptEmit('INPUT_DISABLED');renderAttempt();
  setTimeout(()=>{if(isSolved(path,current.targets)){attemptEmit('PUZZLE_SOLVED');finishAttempt('완료');}else{inputEnabled=true;attemptEmit('INPUT_ENABLED');renderAttempt();}},140);
}

function restartAttempt(){if(!inputEnabled||finished)return;attemptEmit('PUZZLE_RESTARTED');path=canonicalPath(current.initial);selected=null;renderAttempt();}
function abandonAttempt(){if(finished)return;if(confirm('현재 문제를 여기서 끝낼까요?')){attemptEmit('PUZZLE_ABANDONED');finishAttempt('문제를 종료했습니다.');}}
function finishAttempt(label){finished=true;inputEnabled=false;const observation=reconstructAttempt(attemptLog.events);showRating(label,observation);}

function showRating(label,observation){
  clear();const p=el('div','panel');p.append(el('h2','',label),el('p','','방금 문제는 얼마나 어렵게 느껴졌나요?'));
  const rating=el('div','rating');const labels=['매우 쉬웠다','쉬웠다','보통이었다','어려웠다','매우 어려웠다'];
  labels.forEach((text,i)=>{const b=button('','rating-button');b.append(el('span','',String(i+1)),document.createTextNode(text));b.onclick=()=>commitAttempt(observation,i+1);rating.append(b);});
  const skip=button('응답하지 않기','secondary');skip.onclick=()=>commitAttempt(observation,null);p.append(rating,skip);screen.append(p);
}

function commitAttempt(observation,selfRatedDifficulty){
  attempts.push({attemptId:attemptIdentity.attemptId,puzzleResearchId:current.researchPuzzleId,researchEquivalenceIdV1:current.researchEquivalenceIdV1,puzzleFingerprint:current.puzzleFingerprint,events:attemptLog.events,summary:{...observation,selfRatedDifficulty}});
  if(attemptIndex===5){showBreak();return;}if(attemptIndex===11){completeSession();return;}startAttempt(attemptIndex+1);
}

function showBreak(){
  emitSession('BREAK_SHOWN',{afterAttempt:6});clear();const p=el('div','panel');p.append(el('div','break-mark','BREAK'),el('h2','','여기까지 6문제를 풀었습니다.'),el('p','','원하면 잠시 쉬었다가 계속하세요.'));
  const b=button('계속하기');b.onclick=()=>{emitSession('BREAK_CONTINUED',{nextAttempt:7});startAttempt(6);};p.append(b);screen.append(p);
}

function validateExportPayload(payload){
  const errors=[];
  if(payload.schema!=='A3_PRODUCT_OWNER_SELF_CALIBRATION_EXPORT')errors.push('schema');
  if(payload.eligibility!==EXPORT_ELIGIBILITY)errors.push('eligibility');
  if(payload.humanCollectionEnabled!==false)errors.push('collectionLock');
  if(payload.runtimeMode!==RUNTIME_MODE)errors.push('runtimeMode');
  if(payload.testerProfile!==TESTER_PROFILE)errors.push('testerProfile');
  if(payload.selfTestSessionId!==SELF_TEST_SESSION_ID)errors.push('selfTestSessionId');
  if(payload.poolFingerprint!==POOL_FINGERPRINT||payload.orderPlanFingerprint!==ORDER_PLAN_FINGERPRINT||payload.sessionBundleFingerprint!==SESSION_BUNDLE_FINGERPRINT)errors.push('fingerprint');
  if(payload.attempts.length!==12)errors.push('attemptCount');
  const ids=payload.attempts.map(row=>row.researchEquivalenceIdV1);const expected=bundle.puzzles.map(row=>row.researchEquivalenceIdV1);if(JSON.stringify(ids)!==JSON.stringify(expected))errors.push('attemptOrder');
  const directIdentifierKeys=new Set(['name','email','phone','address','exactLocation','ipAddress','userAgent','deviceFingerprint']);
  const analysisLeakKeys=new Set(['shortestDistance','features','selectionDescriptors','distanceBin','structuralStratumKey','coarseFamilyKey','solvedExcessMoveCount']);
  const walk=value=>{if(!value||typeof value!=='object')return;for(const [key,child] of Object.entries(value)){if(directIdentifierKeys.has(key))errors.push(`directIdentifier:${key}`);if(analysisLeakKeys.has(key))errors.push(`analysisLeak:${key}`);walk(child);}};walk(payload);
  return [...new Set(errors)].sort();
}

function completeSession(){
  emitSession('SESSION_ENDED',{reason:'SELF_CALIBRATION_COMPLETE'});
  const streamErrors=[...validateEventStream(sessionLog.events),...attempts.flatMap((row,index)=>validateEventStream(row.events).map(error=>`attempt${index+1}:${error}`))];
  const payload=makeSelfCalibrationExport({sessionEvents:sessionLog.events,attempts,sessionRunId});const all=[...streamErrors,...validateExportPayload(payload)];
  clear();const p=el('div','panel');p.append(el('h2','',SESSION_COMPLETE_LABEL),el('p','','12문제를 모두 마쳤습니다.'));
  const notice=el('div','notice',all.length?'내보내기 검사에 실패했습니다.':'자가 보정 JSON을 이 기기에 저장할 수 있습니다. 저장 후 이 채팅에 파일을 올려주세요.');p.append(notice);
  const exportButton=button('자가 보정 JSON 내보내기','secondary');exportButton.disabled=all.length>0;exportButton.onclick=()=>downloadJson(payload);p.append(exportButton);
  p.append(el('div','debug',`mode=${RUNTIME_MODE} · session=${SELF_TEST_SESSION_ID} · attempts=${attempts.length} · pool=${POOL_FINGERPRINT.slice(0,10)}…`));screen.append(p);
}

function downloadJson(data){const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`linkline-${SELF_TEST_SESSION_ID.toLowerCase()}-self-calibration.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),0);}

document.addEventListener('visibilitychange',()=>{if(!attemptLog||finished)return;if(document.hidden)attemptEmit('VISIBILITY_PAUSED');else attemptEmit('VISIBILITY_RESUMED');});
window.addEventListener('pagehide',()=>{if(attemptLog&&!finished){try{attemptEmit('SESSION_ENDED',{reason:'PAGEHIDE'});}catch{}}});

async function init(){
  const response=await fetch('./data/session_bundle.json');if(!response.ok)throw new Error('SESSION_BUNDLE_LOAD');bundle=await response.json();
  const errors=await validateSessionBundle(bundle);if(errors.length)throw new Error('PREFLIGHT_INPUT_INVALID:'+errors.join(','));showInfo();
}

init().catch(error=>{clear();const p=el('div','panel');p.append(el('h2','','초기화 실패'),el('p','',error.message));screen.append(p);console.error(error);});
