import {
  HUMAN_COLLECTION_ENABLED,RUNTIME_MODE,EXPORT_ELIGIBILITY,TESTER_PROFILE,PRESENTATION_VERSION,MECHANIC_BASELINE,
  MATCHED_SESSION_ID,SESSION_BUNDLE_FINGERPRINT,ANALYSIS_METADATA_FINGERPRINT,PAIR_RESPONSE_VALUES
} from './config.mjs';
import {applyMove,canonicalPath,isSolved,legalDestinations,stateSerialization} from './mechanic.mjs';
import {
  EventLog,RuntimeClock,validateSessionBundle,reconstructAttempt,sha256,validateEventStream,
  randomOpaqueId,validatePairFeedback,makeMatchedExport
} from './protocol.mjs';

if(HUMAN_COLLECTION_ENABLED!==false)throw new Error('HUMAN_COLLECTION_MUST_REMAIN_DISABLED');
if(RUNTIME_MODE!=='PRODUCT_OWNER_NL_MATCHED_TEST')throw new Error('RUNTIME_MODE_MISMATCH');
if(EXPORT_ELIGIBILITY!=='SINGLE_TESTER_NL_MATCHED_ONLY')throw new Error('EXPORT_ELIGIBILITY_MISMATCH');
if(TESTER_PROFILE!=='PRODUCT_OWNER_PRACTICED')throw new Error('TESTER_PROFILE_MISMATCH');

document.title='Linkline — Matched Test';
const modeNode=document.querySelector('.mode');if(modeNode)modeNode.textContent='비교 테스트';
const screen=document.querySelector('#screen');
const clock=new RuntimeClock();
let bundle=null,metadata=null,sessionRunId=null,sessionLog=null;
let attemptIndex=0,current=null,path=[],selected=null,inputEnabled=false,finished=false;
let attemptLog=null,attemptIdentity=null;
const attempts=[],pairFeedback=[];

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
  const p=panel('Linkline 비교 테스트','12문제를 두 문제씩 이어서 풀고, 각 두 문제 뒤에 짧은 비교 질문에 답합니다.');
  const notice=el('div','notice','결과는 이 기기에서 JSON 파일로만 내보내며 자동 업로드하지 않습니다. 문제를 푸는 동안 예상 난이도나 비교 기준은 표시하지 않습니다.');
  const copy=el('div','copy');
  for(const [title,text] of [
    ['목표','연결된 줄의 두 끝을 두 목표 칸에 하나씩 놓으면 해결됩니다. 어느 끝이 어느 목표 칸에 들어가도 됩니다.'],
    ['조작','줄의 끝을 손가락으로 잡고 빈칸을 따라 끌 수 있습니다. 손을 떼지 않고 방향을 꺾어 계속 움직일 수 있고, 끝을 누른 뒤 표시된 칸을 다시 누르는 방식도 사용할 수 있습니다.'],
    ['기록','문제마다 해결 여부, 이동·재시작, 활성 시간과 선택적 1~5 체감 난이도를 기록합니다. 두 문제 뒤에는 체감 난이도와 읽기·조작 부담을 비교합니다.']
  ]){const block=el('div','copy-block');block.append(el('h3','',title),el('p','',text));copy.append(block);}
  const start=button('테스트 시작');start.onclick=beginSession;p.append(notice,copy,start);
}
function beginSession(){
  if(sessionRunId!==null)throw new Error('SESSION_ALREADY_STARTED');
  sessionRunId=randomOpaqueId('RUN');sessionLog=new EventLog({sessionRunId,clock});
  emitSession('SESSION_STARTED',{mode:RUNTIME_MODE,eligibility:EXPORT_ELIGIBILITY,testerProfile:TESTER_PROFILE,matchedSessionId:MATCHED_SESSION_ID});
  emitSession('INSTRUCTION_COMPLETED');startAttempt(0);
}
function identityFor(puzzle,index){return {attemptId:`ATTEMPT-${String(index+1).padStart(2,'0')}-${sessionRunId.slice(-8)}`,researchEquivalenceIdV1:puzzle.researchEquivalenceIdV1,puzzleFingerprint:puzzle.puzzleFingerprint};}
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
function finishAttempt(label){
  finished=true;inputEnabled=false;
  const shortest=metadata.shortestDistanceByResearchEquivalenceIdV1[current.researchEquivalenceIdV1];
  const observation=reconstructAttempt(attemptLog.events,shortest);showRating(label,observation);
}
function showRating(label,observation){
  clear();const p=el('div','panel');p.append(el('h2','',label),el('p','','방금 문제는 얼마나 어렵게 느껴졌나요?'));
  const rating=el('div','rating');const labels=['매우 쉬웠다','쉬웠다','보통이었다','어려웠다','매우 어려웠다'];
  labels.forEach((text,i)=>{const b=button('','rating-button');b.append(el('span','',String(i+1)),document.createTextNode(text));b.onclick=()=>commitAttempt(observation,i+1);rating.append(b);});
  const skip=button('응답하지 않기','secondary');skip.onclick=()=>commitAttempt(observation,null);p.append(rating,skip);screen.append(p);
}
function commitAttempt(observation,selfRatedDifficulty){
  attempts.push({attemptId:attemptIdentity.attemptId,researchEquivalenceIdV1:current.researchEquivalenceIdV1,puzzleFingerprint:current.puzzleFingerprint,events:attemptLog.events,summary:{...observation,selfRatedDifficulty}});
  const completedPosition=attemptIndex+1;
  if(completedPosition%2===0){showPairQuestion(completedPosition/2,'DIFFICULTY',null);return;}
  startAttempt(attemptIndex+1);
}
function showPairQuestion(pairPosition,question,firstAnswer){
  const pair=bundle.pairs[pairPosition-1];
  emitSession('PAIR_FEEDBACK_SHOWN',{pairId:pair.pairId,pairPosition,afterPuzzlePosition:pairPosition*2,question});
  const title=question==='DIFFICULTY'?'방금 두 문제 비교':'화면과 조작 비교';
  const prompt=question==='DIFFICULTY'?'두 문제 중 어느 쪽이 더 어렵게 느껴졌나요?':'두 문제 중 어느 쪽이 이 기기에서 읽거나 조작하기 더 어려웠나요?';
  const p=panel(title,prompt);const stack=el('div','stack');
  for(const [value,label] of [['FIRST','첫 번째'],['SAME','비슷함'],['SECOND','두 번째']]){
    const b=button(label,'secondary');b.onclick=()=>{
      if(question==='DIFFICULTY')showPairQuestion(pairPosition,'DEVICE_BURDEN',value);
      else submitPairFeedback(pairPosition,firstAnswer,value);
    };stack.append(b);
  }
  p.append(stack);
}
function submitPairFeedback(pairPosition,difficultyResponse,deviceBurdenResponse){
  if(!PAIR_RESPONSE_VALUES.includes(difficultyResponse)||!PAIR_RESPONSE_VALUES.includes(deviceBurdenResponse))throw new Error('PAIR_RESPONSE');
  const pair=bundle.pairs[pairPosition-1];const row={pairId:pair.pairId,pairPosition,afterPuzzlePosition:pairPosition*2,difficultyResponse,deviceBurdenResponse};
  pairFeedback.push(row);emitSession('PAIR_FEEDBACK_SUBMITTED',row);
  if(pairPosition===3){showBreak();return;}
  if(pairPosition===6){completeSession();return;}
  startAttempt(attemptIndex+1);
}
function showBreak(){
  emitSession('BREAK_SHOWN',{afterAttempt:6,afterPair:3});clear();const p=el('div','panel');p.append(el('div','break-mark','BREAK'),el('h2','','여기까지 6문제를 풀었습니다.'),el('p','','원하면 잠시 쉬었다가 계속하세요.'));
  const b=button('계속하기');b.onclick=()=>{emitSession('BREAK_CONTINUED',{nextAttempt:7,nextPair:4});startAttempt(6);};p.append(b);screen.append(p);
}
function validateExportPayload(payload){
  const errors=[];
  if(payload.schema!=='A3_PRODUCT_OWNER_NL_MATCHED_EXPORT'||payload.version!=='1.0.0')errors.push('schema');
  if(payload.eligibility!==EXPORT_ELIGIBILITY||payload.humanCollectionEnabled!==false)errors.push('collection');
  if(payload.runtimeMode!==RUNTIME_MODE||payload.testerProfile!==TESTER_PROFILE||payload.matchedSessionId!==MATCHED_SESSION_ID)errors.push('identity');
  if(payload.mechanicBaseline!==MECHANIC_BASELINE||payload.presentationVersion!==PRESENTATION_VERSION)errors.push('baseline');
  if(payload.sessionBundleFingerprint!==SESSION_BUNDLE_FINGERPRINT||payload.analysisMetadataFingerprint!==ANALYSIS_METADATA_FINGERPRINT)errors.push('fingerprint');
  if(payload.attempts.length!==12)errors.push('attemptCount');
  const ids=payload.attempts.map(row=>row.researchEquivalenceIdV1),expected=bundle.puzzles.map(row=>row.researchEquivalenceIdV1);if(JSON.stringify(ids)!==JSON.stringify(expected))errors.push('attemptOrder');
  for(let i=0;i<payload.attempts.length;i++){
    const expectedShortest=metadata.shortestDistanceByResearchEquivalenceIdV1[expected[i]];
    if(payload.attempts[i].summary.shortestDistance!==expectedShortest)errors.push(`shortest:${i+1}`);
  }
  errors.push(...validatePairFeedback(payload.pairFeedback,bundle));
  const directIdentifierKeys=new Set(['name','email','phone','address','exactLocation','ipAddress','userAgent','deviceFingerprint']);
  const walk=value=>{if(!value||typeof value!=='object')return;for(const [key,child] of Object.entries(value)){if(directIdentifierKeys.has(key))errors.push(`directIdentifier:${key}`);walk(child);}};walk(payload);
  return [...new Set(errors)].sort();
}
function completeSession(){
  emitSession('SESSION_ENDED',{reason:'NL_MATCHED_COMPLETE'});
  const streamErrors=[...validateEventStream(sessionLog.events),...attempts.flatMap((row,index)=>validateEventStream(row.events).map(error=>`attempt${index+1}:${error}`))];
  const payload=makeMatchedExport({sessionEvents:sessionLog.events,attempts,pairFeedback,sessionRunId});const all=[...streamErrors,...validateExportPayload(payload)];
  clear();const p=el('div','panel');p.append(el('h2','','테스트 완료'),el('p','','12문제와 비교 질문을 모두 마쳤습니다.'));
  const notice=el('div','notice',all.length?'내보내기 검사에 실패했습니다. 이 화면을 그대로 알려주세요.':'결과 JSON을 이 기기에 저장한 뒤 이 채팅에 파일을 올려주세요.');p.append(notice);
  const exportButton=button('결과 JSON 내보내기','secondary');exportButton.disabled=all.length>0;exportButton.onclick=()=>downloadJson(payload);p.append(exportButton);
  if(all.length)p.append(el('div','debug',all.join(' · ')));screen.append(p);
}
function downloadJson(data){const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='linkline-nl6-matched-repair-1.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),0);}

document.addEventListener('visibilitychange',()=>{if(!attemptLog||finished)return;if(document.hidden)attemptEmit('VISIBILITY_PAUSED');else attemptEmit('VISIBILITY_RESUMED');});
window.addEventListener('pagehide',()=>{if(attemptLog&&!finished){try{attemptEmit('SESSION_ENDED',{reason:'PAGEHIDE'});}catch{}}});

async function init(){
  const [bundleResponse,metadataResponse]=await Promise.all([fetch('./data/session_bundle.json'),fetch('./data/analysis_metadata.json')]);
  if(!bundleResponse.ok||!metadataResponse.ok)throw new Error('RUNTIME_DATA_LOAD');
  bundle=await bundleResponse.json();metadata=await metadataResponse.json();
  const errors=await validateSessionBundle(bundle,metadata);if(errors.length)throw new Error('PREFLIGHT_INPUT_INVALID:'+errors.join(','));showInfo();
}
init().catch(error=>{clear();const p=el('div','panel');p.append(el('h2','','초기화 실패'),el('p','',error.message));screen.append(p);console.error(error);});
