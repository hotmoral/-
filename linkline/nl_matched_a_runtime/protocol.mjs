import {
  HUMAN_COLLECTION_ENABLED,RUNTIME_MODE,EXPORT_ELIGIBILITY,TESTER_PROFILE,
  PROTOCOL_VERSION,PRESENTATION_VERSION,EVENT_SCHEMA_VERSION,MECHANIC_BASELINE,
  POOL_FINGERPRINT,ORDER_PLAN_FINGERPRINT,SELF_TEST_PHASE,SELF_TEST_SESSION_ID,SESSION_BUNDLE_FINGERPRINT
} from './config.mjs';
import {validatePuzzle,puzzleSerialization,canonicalPath} from './mechanic.mjs';

function canonical(value){
  if(Array.isArray(value))return '['+value.map(canonical).join(',')+']';
  if(value&&typeof value==='object')return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',')+'}';
  return JSON.stringify(value);
}
export async function sha256(value){
  const bytes=new TextEncoder().encode(value);
  const digest=await globalThis.crypto.subtle.digest('SHA-256',bytes);
  return [...new Uint8Array(digest)].map(b=>b.toString(16).padStart(2,'0')).join('');
}
export async function normalizedFingerprint(obj,field){
  const copy={...obj};delete copy[field];return sha256(canonical(copy));
}
export function randomOpaqueId(prefix='RUN'){
  const bytes=new Uint8Array(16);globalThis.crypto.getRandomValues(bytes);
  return `${prefix}-`+[...bytes].map(b=>b.toString(16).padStart(2,'0')).join('');
}
function transformCell(n,cell,transform){
  let row=Math.floor(cell/n),col=cell%n;
  if(transform>=4){col=n-1-col;transform-=4;}
  for(let i=0;i<transform;i++){const nextRow=col,nextCol=n-1-row;row=nextRow;col=nextCol;}
  return row*n+col;
}
async function researchEquivalenceId(puzzle){
  const variants=[];
  for(let transform=0;transform<8;transform++){
    const path=canonicalPath(puzzle.initial.map(cell=>transformCell(puzzle.n,cell,transform)));
    const goal=puzzle.targets.map(cell=>transformCell(puzzle.n,cell,transform)).sort((a,b)=>a-b);
    variants.push(JSON.stringify(['LL_A3_RESEARCH_EQ',1,puzzle.n,puzzle.length,goal,path]));
  }
  variants.sort();
  return sha256(variants[0]);
}
const ANALYSIS_LEAK_KEYS=new Set([
  'pairId','label','side','features','shortestDistance','selectionDescriptors','distanceBin',
  'structuralStratumKey','coarseFamilyKey','shortestActionSequenceCount','shortestDagStateCount',
  'mandatoryInternalStateCount','initialMeanRegret','initialMaxRegret','solvedExcessMoveCount',
  'candidateScore','predictedDifficulty','modelScore','confirmationThreshold','matchingRule'
]);
export async function validateSessionBundle(bundle){
  const errors=[];
  if(bundle.schema!=='LINKLINE_A3_NL_MATCHED_SESSION_BUNDLE')errors.push('schema');
  if(bundle.version!=='1.0.0')errors.push('version');
  if(bundle.phase!==SELF_TEST_PHASE)errors.push('phase');
  if(bundle.sessionId!==SELF_TEST_SESSION_ID)errors.push('sessionId');
  if(bundle.poolFingerprint!==POOL_FINGERPRINT)errors.push('poolFingerprint');
  if(bundle.orderPlanFingerprint!==ORDER_PLAN_FINGERPRINT)errors.push('orderPlanFingerprint');
  if(bundle.sessionBundleFingerprint!==SESSION_BUNDLE_FINGERPRINT)errors.push('bundleFingerprintLiteral');
  if(await normalizedFingerprint(bundle,'sessionBundleFingerprint')!==SESSION_BUNDLE_FINGERPRINT)errors.push('bundleFingerprintSemantic');
  if(bundle.breakAfter!==6)errors.push('breakAfter');
  if(bundle.puzzleCount!==12||bundle.puzzles?.length!==12)errors.push('puzzleCount');
  const ids=new Set(),initialKeys=new Set();
  for(const puzzle of bundle.puzzles||[]){
    try{
      validatePuzzle(puzzle);
      if(![4,5].includes(puzzle.n))errors.push(`boardSize:${puzzle.researchPuzzleId}`);
      if(await sha256(puzzleSerialization(puzzle))!==puzzle.puzzleFingerprint)errors.push(`puzzleFingerprint:${puzzle.researchPuzzleId}`);
      if(await researchEquivalenceId(puzzle)!==puzzle.researchEquivalenceIdV1)errors.push(`researchEquivalence:${puzzle.researchPuzzleId}`);
    }catch(error){errors.push(`puzzle:${puzzle.researchPuzzleId}:${error.message}`);}
    const id=puzzle.researchEquivalenceIdV1;
    if(!id||ids.has(id))errors.push(`duplicate:${id||'missing'}`);ids.add(id);
    if(puzzle.researchPuzzleId!==`A3NL-${id}`)errors.push(`researchPuzzleId:${id}`);
    const initialKey=`${puzzle.n}:${canonicalPath(puzzle.initial).join(',')}`;
    if(initialKeys.has(initialKey))errors.push(`duplicateInitial:${initialKey}`);initialKeys.add(initialKey);
  }
  const walk=value=>{
    if(!value||typeof value!=='object')return;
    for(const [key,child] of Object.entries(value)){
      if(ANALYSIS_LEAK_KEYS.has(key))errors.push(`analysisLeak:${key}`);
      walk(child);
    }
  };
  walk(bundle);
  return [...new Set(errors)].sort();
}
export const EVENT_TYPES=new Set([
  'SESSION_STARTED','INSTRUCTION_COMPLETED','PUZZLE_PRESENTED','INPUT_ENABLED','INPUT_DISABLED',
  'ENDPOINT_SELECTED','ACTION_SUBMITTED','ACTION_ACCEPTED','ACTION_REJECTED','PUZZLE_RESTARTED',
  'VISIBILITY_PAUSED','VISIBILITY_RESUMED','PUZZLE_SOLVED','PUZZLE_ABANDONED','BREAK_SHOWN',
  'BREAK_CONTINUED','SESSION_ENDED'
]);
export function validateEventEnvelope(event){
  const errors=[];
  if(event.eventSchemaVersion!==EVENT_SCHEMA_VERSION)errors.push('eventSchemaVersion');
  if(event.protocolVersion!==PROTOCOL_VERSION)errors.push('protocolVersion');
  if(event.presentationVersion!==PRESENTATION_VERSION)errors.push('presentationVersion');
  if(event.mechanicBaseline!==MECHANIC_BASELINE)errors.push('mechanicBaseline');
  if(event.poolFingerprint!==POOL_FINGERPRINT)errors.push('poolFingerprint');
  if(event.orderPlanFingerprint!==ORDER_PLAN_FINGERPRINT)errors.push('orderPlanFingerprint');
  if(event.sessionBundleFingerprint!==SESSION_BUNDLE_FINGERPRINT)errors.push('sessionBundleFingerprint');
  if(event.testerProfile!==TESTER_PROFILE)errors.push('testerProfile');
  if(event.selfTestSessionId!==SELF_TEST_SESSION_ID)errors.push('selfTestSessionId');
  if(typeof event.sessionRunId!=='string'||!/^RUN-[0-9a-f]{32}$/.test(event.sessionRunId))errors.push('sessionRunId');
  if(!Number.isInteger(event.eventIndex)||event.eventIndex<0)errors.push('eventIndex');
  if(!Number.isInteger(event.sessionElapsedMs)||event.sessionElapsedMs<0)errors.push('sessionElapsedMs');
  if(!EVENT_TYPES.has(event.eventType))errors.push('eventType');
  if(!event.payload||typeof event.payload!=='object'||Array.isArray(event.payload))errors.push('payload');
  for(const key of ['attemptId','puzzleResearchId','researchEquivalenceIdV1','puzzleFingerprint'])
    if(event[key]!==null&&typeof event[key]!=='string')errors.push(key);
  return errors;
}
export function validateEventStream(events){
  const errors=[];let last=-1;
  for(let i=0;i<events.length;i++){
    for(const error of validateEventEnvelope(events[i]))errors.push(`${i}:${error}`);
    if(events[i].eventIndex!==i)errors.push(`${i}:contiguousIndex`);
    if(events[i].sessionElapsedMs<last)errors.push(`${i}:monotonicTime`);
    last=events[i].sessionElapsedMs;
  }
  return [...new Set(errors)].sort();
}
export class RuntimeClock{constructor(){this.start=performance.now();}now(){return Math.max(0,Math.floor(performance.now()-this.start));}}
export class SyntheticClock{constructor(){this.ms=0;}advance(ms){if(!Number.isInteger(ms)||ms<0)throw new Error('CLOCK');this.ms+=ms;return this.ms;}now(){return this.ms;}}
export class EventLog{
  constructor({sessionRunId,clock}={}){
    if(HUMAN_COLLECTION_ENABLED!==false)throw new Error('HUMAN_COLLECTION_MUST_BE_DISABLED');
    if(!sessionRunId||!clock)throw new Error('EVENT_LOG_INIT');
    this.sessionRunId=sessionRunId;this.clock=clock;this.events=[];
  }
  emit(eventType,payload={},identity={}){
    const event={
      eventSchemaVersion:EVENT_SCHEMA_VERSION,protocolVersion:PROTOCOL_VERSION,
      presentationVersion:PRESENTATION_VERSION,mechanicBaseline:MECHANIC_BASELINE,
      poolFingerprint:POOL_FINGERPRINT,orderPlanFingerprint:ORDER_PLAN_FINGERPRINT,
      sessionBundleFingerprint:SESSION_BUNDLE_FINGERPRINT,testerProfile:TESTER_PROFILE,
      selfTestSessionId:SELF_TEST_SESSION_ID,sessionRunId:this.sessionRunId,
      attemptId:identity.attemptId??null,puzzleResearchId:identity.puzzleResearchId??null,
      researchEquivalenceIdV1:identity.researchEquivalenceIdV1??null,
      puzzleFingerprint:identity.puzzleFingerprint??null,eventIndex:this.events.length,
      sessionElapsedMs:this.clock.now(),eventType,payload
    };
    const errors=validateEventEnvelope(event);if(errors.length)throw new Error('EVENT_ENVELOPE:'+errors.join(','));
    this.events.push(event);return event;
  }
}
export function reconstructAttempt(events){
  const allowed=new Set([
    'PUZZLE_PRESENTED','INPUT_ENABLED','INPUT_DISABLED','ENDPOINT_SELECTED','ACTION_SUBMITTED',
    'ACTION_ACCEPTED','ACTION_REJECTED','PUZZLE_RESTARTED','VISIBILITY_PAUSED','VISIBILITY_RESUMED',
    'PUZZLE_SOLVED','PUZZLE_ABANDONED','SESSION_ENDED'
  ]);
  if(!Array.isArray(events)||events.length<3)throw new Error('EVENTS');
  const rows=events.map(e=>({eventIndex:e.eventIndex,sessionElapsedMs:e.sessionElapsedMs,eventType:e.eventType,payload:e.payload||{}}));
  let visible=true,input=false,started=false,firstInput=null,last=rows[0].sessionElapsedMs,terminal=null,terminalMs=null,pending=null,accepted=0,rejected=0,restarts=0,active=0,paused=0,firstAction=null;
  for(let i=0;i<rows.length;i++){
    const event=rows[i];
    if(!allowed.has(event.eventType)||event.eventIndex!==i)throw new Error('EVENT_SEQUENCE');
    if(i&&event.sessionElapsedMs<rows[i-1].sessionElapsedMs)throw new Error('TIME');
    if(i){const delta=event.sessionElapsedMs-last;if(started&&!visible)paused+=delta;if(started&&visible&&input)active+=delta;}
    last=event.sessionElapsedMs;if(terminal)throw new Error('AFTER_TERMINAL');
    switch(event.eventType){
      case 'PUZZLE_PRESENTED':if(i!==0)throw new Error('PRESENTED');break;
      case 'INPUT_ENABLED':if(!visible||input)throw new Error('INPUT_ENABLE');input=true;if(!started){started=true;firstInput=event.sessionElapsedMs;}break;
      case 'INPUT_DISABLED':if(!input)throw new Error('INPUT_DISABLE');input=false;break;
      case 'VISIBILITY_PAUSED':if(!visible)throw new Error('PAUSE');visible=false;break;
      case 'VISIBILITY_RESUMED':if(visible)throw new Error('RESUME');visible=true;break;
      case 'ENDPOINT_SELECTED':if(!started||!input||!visible)throw new Error('SELECT');break;
      case 'ACTION_SUBMITTED':if(!started||!input||!visible||pending)throw new Error('SUBMIT');pending=[event.payload.source,event.payload.destination];break;
      case 'ACTION_ACCEPTED':case 'ACTION_REJECTED':
        if(!pending||pending[0]!==event.payload.source||pending[1]!==event.payload.destination)throw new Error('RESULT');
        pending=null;if(event.eventType==='ACTION_ACCEPTED'){accepted++;if(firstAction===null)firstAction=active;}else rejected++;break;
      case 'PUZZLE_RESTARTED':if(!started||!input||!visible||pending)throw new Error('RESTART');restarts++;break;
      case 'PUZZLE_SOLVED':case 'PUZZLE_ABANDONED':case 'SESSION_ENDED':
        if(!started||pending)throw new Error('TERMINAL');
        terminal=event.eventType==='PUZZLE_SOLVED'?'SOLVED':event.eventType==='PUZZLE_ABANDONED'?'ABANDONED_BY_TESTER':'SESSION_TERMINATED';terminalMs=event.sessionElapsedMs;break;
    }
  }
  if(!terminal||firstInput===null)throw new Error('NO_TERMINAL');
  return {terminalOutcome:terminal,acceptedMoveCount:accepted,restartCount:restarts,rejectedActionCount:rejected,decisionActiveElapsedMs:active,wallElapsedMs:terminalMs-firstInput,firstActionLatencyMs:firstAction,visibilityPausedMs:paused};
}
export function makeSelfCalibrationExport({sessionEvents,attempts,sessionRunId}){
  if(HUMAN_COLLECTION_ENABLED!==false)throw new Error('COLLECTION_LOCK');
  return {schema:'A3_PRODUCT_OWNER_SELF_CALIBRATION_EXPORT',version:'1.0.0',eligibility:EXPORT_ELIGIBILITY,humanCollectionEnabled:false,runtimeMode:RUNTIME_MODE,testerProfile:TESTER_PROFILE,selfTestSessionId:SELF_TEST_SESSION_ID,sessionRunId,presentationVersion:PRESENTATION_VERSION,mechanicBaseline:MECHANIC_BASELINE,poolFingerprint:POOL_FINGERPRINT,orderPlanFingerprint:ORDER_PLAN_FINGERPRINT,sessionBundleFingerprint:SESSION_BUNDLE_FINGERPRINT,sessionEvents,attempts};
}
