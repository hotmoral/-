import {
  HUMAN_COLLECTION_ENABLED,RUNTIME_MODE,EXPORT_ELIGIBILITY,TESTER_PROFILE,
  PROTOCOL_VERSION,PRESENTATION_VERSION,EVENT_SCHEMA_VERSION,MECHANIC_BASELINE,
  MATCHED_SESSION_ID,SESSION_BUNDLE_FINGERPRINT,ANALYSIS_METADATA_FINGERPRINT,
  PAIR_FEEDBACK_POSITIONS,ORIENTATION_PATTERN,QUARANTINED_RESEARCH_EQUIVALENCE_IDS,
  PAIR_RESPONSE_VALUES
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
export async function normalizedFingerprint(obj,field){const copy=structuredClone(obj);delete copy[field];return sha256(canonical(copy));}
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
export async function researchEquivalenceId(puzzle){
  const variants=[];
  for(let transform=0;transform<8;transform++){
    const path=canonicalPath(puzzle.initial.map(cell=>transformCell(puzzle.n,cell,transform)));
    const goal=puzzle.targets.map(cell=>transformCell(puzzle.n,cell,transform)).sort((a,b)=>a-b);
    variants.push(JSON.stringify(['LL_A3_RESEARCH_EQ',1,puzzle.n,puzzle.length,goal,path]));
  }
  variants.sort();return sha256(variants[0]);
}

export async function validateAnalysisMetadata(metadata,bundle){
  const errors=[];
  if(metadata?.schema!=='LINKLINE_A3_NL5_RUNTIME_ANALYSIS_METADATA')errors.push('metadataSchema');
  if(metadata?.version!=='1.0.0')errors.push('metadataVersion');
  if(metadata?.sessionId!==MATCHED_SESSION_ID)errors.push('metadataSession');
  if(metadata?.metadataFingerprint!==ANALYSIS_METADATA_FINGERPRINT)errors.push('metadataFingerprintLiteral');
  if(await normalizedFingerprint(metadata,'metadataFingerprint')!==ANALYSIS_METADATA_FINGERPRINT)errors.push('metadataFingerprintSemantic');
  const map=metadata?.shortestDistanceByResearchEquivalenceIdV1||{};
  const expected=(bundle?.puzzles||[]).map(p=>p.researchEquivalenceIdV1).sort();
  if(JSON.stringify(Object.keys(map).sort())!==JSON.stringify(expected))errors.push('metadataIdentitySet');
  for(const [id,distance] of Object.entries(map))if(!Number.isInteger(distance)||distance<1)errors.push(`metadataDistance:${id}`);
  return [...new Set(errors)].sort();
}

export async function validateSessionBundle(bundle,metadata){
  const errors=[];
  if(bundle?.schema!=='LINKLINE_A3_NL_MATCHED_SESSION_BUNDLE')errors.push('schema');
  if(bundle?.version!=='0.2.0')errors.push('version');
  if(bundle?.runtimeMode!==RUNTIME_MODE)errors.push('runtimeMode');
  if(bundle?.testerProfile!==TESTER_PROFILE)errors.push('testerProfile');
  if(bundle?.sessionId!==MATCHED_SESSION_ID)errors.push('sessionId');
  if(bundle?.largerN!==5)errors.push('largerN');
  if(bundle?.pairCount!==6||bundle?.pairs?.length!==6)errors.push('pairCount');
  if(bundle?.puzzleCount!==12||bundle?.puzzles?.length!==12)errors.push('puzzleCount');
  if(bundle?.breakAfter!==6)errors.push('breakAfter');
  if(JSON.stringify(bundle?.pairFeedbackAfterPuzzlePositions)!==JSON.stringify(PAIR_FEEDBACK_POSITIONS))errors.push('pairFeedbackPositions');
  if(bundle?.sessionBundleFingerprint!==SESSION_BUNDLE_FINGERPRINT)errors.push('bundleFingerprintLiteral');
  if(await normalizedFingerprint(bundle,'sessionBundleFingerprint')!==SESSION_BUNDLE_FINGERPRINT)errors.push('bundleFingerprintSemantic');

  const quarantine=new Set(QUARANTINED_RESEARCH_EQUIVALENCE_IDS),ids=new Set();
  const lengthCounts=new Map([[6,0],[7,0],[9,0]]);
  for(let pairIndex=0;pairIndex<6;pairIndex++){
    const pair=bundle.pairs?.[pairIndex],position=pairIndex+1;
    if(pair?.pairPosition!==position)errors.push(`pairPosition:${position}`);
    if(pair?.axis!=='SAME_L')errors.push(`pairAxis:${position}`);
    if(pair?.orientation!==ORIENTATION_PATTERN[pairIndex])errors.push(`orientation:${position}`);
    const members=(bundle.puzzles||[]).slice(pairIndex*2,pairIndex*2+2);
    if(members.length!==2)continue;
    if(members.some(p=>p.pairId!==pair.pairId||p.pairPosition!==position||p.axis!=='SAME_L'))errors.push(`pairBinding:${position}`);
    if(members[0].length!==members[1].length||!lengthCounts.has(members[0].length))errors.push(`pairLength:${position}`);
    else lengthCounts.set(members[0].length,lengthCounts.get(members[0].length)+1);
    const control=members.find(p=>p.pairMember==='control'),larger=members.find(p=>p.pairMember==='larger');
    if(!control||!larger||control.n!==4||larger.n!==5)errors.push(`pairMembers:${position}`);
    if(pair.orientation==='CONTROL_FIRST'&&members[0]?.pairMember!=='control')errors.push(`pairOrder:${position}`);
    if(pair.orientation==='LARGER_FIRST'&&members[0]?.pairMember!=='larger')errors.push(`pairOrder:${position}`);
  }
  for(const [length,count] of lengthCounts)if(count!==2)errors.push(`lengthPairCount:${length}:${count}`);

  for(const [index,puzzle] of (bundle.puzzles||[]).entries()){
    try{
      validatePuzzle(puzzle);
      if(![4,5].includes(puzzle.n))errors.push(`boardSize:${index+1}`);
      if(await sha256(puzzleSerialization(puzzle))!==puzzle.puzzleFingerprint)errors.push(`puzzleFingerprint:${index+1}`);
      if(await researchEquivalenceId(puzzle)!==puzzle.researchEquivalenceIdV1)errors.push(`researchEquivalence:${index+1}`);
    }catch(error){errors.push(`puzzle:${index+1}:${error.message}`);}
    const id=puzzle.researchEquivalenceIdV1;
    if(!id||ids.has(id))errors.push(`duplicate:${index+1}`);else ids.add(id);
    if(quarantine.has(id))errors.push(`quarantine:${index+1}`);
    if(!Number.isInteger(metadata?.shortestDistanceByResearchEquivalenceIdV1?.[id]))errors.push(`missingShortest:${index+1}`);
  }
  errors.push(...await validateAnalysisMetadata(metadata,bundle));
  return [...new Set(errors)].sort();
}

export const EVENT_TYPES=new Set([
  'SESSION_STARTED','INSTRUCTION_COMPLETED','PUZZLE_PRESENTED','INPUT_ENABLED','INPUT_DISABLED',
  'ENDPOINT_SELECTED','ACTION_SUBMITTED','ACTION_ACCEPTED','ACTION_REJECTED','PUZZLE_RESTARTED',
  'VISIBILITY_PAUSED','VISIBILITY_RESUMED','PUZZLE_SOLVED','PUZZLE_ABANDONED',
  'PAIR_FEEDBACK_SHOWN','PAIR_FEEDBACK_SUBMITTED','BREAK_SHOWN','BREAK_CONTINUED','SESSION_ENDED'
]);
export function validateEventEnvelope(event){
  const errors=[];
  if(event.eventSchemaVersion!==EVENT_SCHEMA_VERSION)errors.push('eventSchemaVersion');
  if(event.protocolVersion!==PROTOCOL_VERSION)errors.push('protocolVersion');
  if(event.presentationVersion!==PRESENTATION_VERSION)errors.push('presentationVersion');
  if(event.mechanicBaseline!==MECHANIC_BASELINE)errors.push('mechanicBaseline');
  if(event.sessionBundleFingerprint!==SESSION_BUNDLE_FINGERPRINT)errors.push('sessionBundleFingerprint');
  if(event.analysisMetadataFingerprint!==ANALYSIS_METADATA_FINGERPRINT)errors.push('analysisMetadataFingerprint');
  if(event.testerProfile!==TESTER_PROFILE)errors.push('testerProfile');
  if(event.matchedSessionId!==MATCHED_SESSION_ID)errors.push('matchedSessionId');
  if(typeof event.sessionRunId!=='string'||!/^RUN-[0-9a-f]{32}$/.test(event.sessionRunId))errors.push('sessionRunId');
  if(!Number.isInteger(event.eventIndex)||event.eventIndex<0)errors.push('eventIndex');
  if(!Number.isInteger(event.sessionElapsedMs)||event.sessionElapsedMs<0)errors.push('sessionElapsedMs');
  if(!EVENT_TYPES.has(event.eventType))errors.push('eventType');
  if(!event.payload||typeof event.payload!=='object'||Array.isArray(event.payload))errors.push('payload');
  for(const key of ['attemptId','researchEquivalenceIdV1','puzzleFingerprint'])if(event[key]!==null&&typeof event[key]!=='string')errors.push(key);
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
    const event={eventSchemaVersion:EVENT_SCHEMA_VERSION,protocolVersion:PROTOCOL_VERSION,presentationVersion:PRESENTATION_VERSION,
      mechanicBaseline:MECHANIC_BASELINE,sessionBundleFingerprint:SESSION_BUNDLE_FINGERPRINT,
      analysisMetadataFingerprint:ANALYSIS_METADATA_FINGERPRINT,testerProfile:TESTER_PROFILE,matchedSessionId:MATCHED_SESSION_ID,
      sessionRunId:this.sessionRunId,attemptId:identity.attemptId??null,researchEquivalenceIdV1:identity.researchEquivalenceIdV1??null,
      puzzleFingerprint:identity.puzzleFingerprint??null,eventIndex:this.events.length,sessionElapsedMs:this.clock.now(),eventType,payload};
    const errors=validateEventEnvelope(event);if(errors.length)throw new Error('EVENT_ENVELOPE:'+errors.join(','));
    this.events.push(event);return event;
  }
}

export function reconstructAttempt(events,shortestDistance){
  if(!Number.isInteger(shortestDistance)||shortestDistance<1)throw new Error('SHORTEST');
  const allowed=new Set(['PUZZLE_PRESENTED','INPUT_ENABLED','INPUT_DISABLED','ENDPOINT_SELECTED','ACTION_SUBMITTED','ACTION_ACCEPTED','ACTION_REJECTED','PUZZLE_RESTARTED','VISIBILITY_PAUSED','VISIBILITY_RESUMED','PUZZLE_SOLVED','PUZZLE_ABANDONED','SESSION_ENDED']);
  if(!Array.isArray(events)||events.length<3)throw new Error('EVENTS');
  const rows=events.map(e=>({eventIndex:e.eventIndex,sessionElapsedMs:e.sessionElapsedMs,eventType:e.eventType,payload:e.payload||{}}));
  let visible=true,input=false,started=false,firstInput=null,last=rows[0].sessionElapsedMs,terminal=null,terminalMs=null,pending=null,accepted=0,rejected=0,restarts=0,active=0,paused=0,firstAction=null;
  for(let i=0;i<rows.length;i++){
    const event=rows[i];if(!allowed.has(event.eventType)||event.eventIndex!==i)throw new Error('EVENT_SEQUENCE');
    if(i&&event.sessionElapsedMs<rows[i-1].sessionElapsedMs)throw new Error('TIME');
    if(i){const delta=event.sessionElapsedMs-last;if(started&&!visible)paused+=delta;if(started&&visible&&input)active+=delta;}last=event.sessionElapsedMs;
    if(terminal)throw new Error('AFTER_TERMINAL');
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
        if(!started||pending)throw new Error('TERMINAL');terminal=event.eventType==='PUZZLE_SOLVED'?'SOLVED':event.eventType==='PUZZLE_ABANDONED'?'ABANDONED_BY_TESTER':'SESSION_TERMINATED';terminalMs=event.sessionElapsedMs;break;
    }
  }
  if(!terminal||firstInput===null)throw new Error('NO_TERMINAL');
  const excess=terminal==='SOLVED'?accepted-shortestDistance:null;if(excess!==null&&excess<0)throw new Error('SHORTER_THAN_SHORTEST');
  return {terminalOutcome:terminal,shortestDistance,acceptedMoveCount:accepted,solvedExcessAcceptedMoves:excess,restartCount:restarts,rejectedActionCount:rejected,decisionActiveElapsedMs:active,wallElapsedMs:terminalMs-firstInput,firstActionLatencyMs:firstAction,visibilityPausedMs:paused};
}

export function validatePairFeedback(rows,bundle){
  const errors=[];
  if(rows.length!==6)errors.push('pairFeedbackCount');
  for(let i=0;i<rows.length;i++){
    const row=rows[i],pair=bundle.pairs[i];
    if(row.pairPosition!==i+1||row.pairId!==pair.pairId)errors.push(`pairFeedbackBinding:${i+1}`);
    if(row.afterPuzzlePosition!==PAIR_FEEDBACK_POSITIONS[i])errors.push(`pairFeedbackPosition:${i+1}`);
    for(const key of ['difficultyResponse','deviceBurdenResponse'])if(!PAIR_RESPONSE_VALUES.includes(row[key]))errors.push(`pairFeedbackValue:${i+1}:${key}`);
  }
  return [...new Set(errors)].sort();
}

export function makeMatchedExport({sessionEvents,attempts,pairFeedback,sessionRunId}){
  if(HUMAN_COLLECTION_ENABLED!==false)throw new Error('COLLECTION_LOCK');
  return {schema:'A3_PRODUCT_OWNER_NL_MATCHED_EXPORT',version:'1.0.0',eligibility:EXPORT_ELIGIBILITY,humanCollectionEnabled:false,
    runtimeMode:RUNTIME_MODE,testerProfile:TESTER_PROFILE,matchedSessionId:MATCHED_SESSION_ID,sessionRunId,
    presentationVersion:PRESENTATION_VERSION,mechanicBaseline:MECHANIC_BASELINE,sessionBundleFingerprint:SESSION_BUNDLE_FINGERPRINT,
    analysisMetadataFingerprint:ANALYSIS_METADATA_FINGERPRINT,sessionEvents,attempts,pairFeedback};
}
