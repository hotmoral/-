import {
  HUMAN_COLLECTION_ENABLED, RUNTIME_MODE, EXPORT_ELIGIBILITY,
  PROTOCOL_VERSION, PRESENTATION_VERSION, EVENT_SCHEMA_VERSION, ORDER_PLAN_VERSION,
  MECHANIC_BASELINE, CALIBRATION_MANIFEST_FINGERPRINT, ORDER_PLAN_FINGERPRINT,
  PILOT_BUNDLE_FINGERPRINT
} from './config.mjs';
import { validatePuzzle, puzzleSerialization } from './mechanic.mjs';

function canonical(value) {
  if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
  if (value && typeof value === 'object') return '{' + Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+canonical(value[k])).join(',') + '}';
  return JSON.stringify(value);
}

export async function sha256(value) {
  const bytes = new TextEncoder().encode(value);
  const digest = await globalThis.crypto.subtle.digest('SHA-256', bytes);
  return [...new Uint8Array(digest)].map(b=>b.toString(16).padStart(2,'0')).join('');
}

export async function normalizedFingerprint(obj, field) {
  const c={...obj}; delete c[field]; return sha256(canonical(c));
}

export function randomOpaqueId(prefix='LL') {
  const bytes = new Uint8Array(16);
  globalThis.crypto.getRandomValues(bytes);
  const body=[...bytes].map(b=>b.toString(16).padStart(2,'0')).join('');
  return `${prefix}-${body}`;
}

export async function validateBundle(bundle) {
  const errors=[];
  if (bundle.schema !== 'A3_PILOT_PUZZLE_BUNDLE') errors.push('schema');
  if (bundle.mechanicBaseline !== MECHANIC_BASELINE) errors.push('mechanicBaseline');
  if (bundle.sourceCalibrationManifestFingerprint !== CALIBRATION_MANIFEST_FINGERPRINT) errors.push('manifestFingerprint');
  if (bundle.sourceOrderPlanFingerprint !== ORDER_PLAN_FINGERPRINT) errors.push('orderPlanFingerprint');
  if (bundle.reserveCount !== 0) errors.push('reserveCount');
  if (bundle.puzzleCount !== 24 || bundle.puzzles?.length !== 24) errors.push('puzzleCount');
  if (bundle.bundleFingerprint !== PILOT_BUNDLE_FINGERPRINT || await normalizedFingerprint(bundle,'bundleFingerprint') !== PILOT_BUNDLE_FINGERPRINT) errors.push('bundleFingerprint');
  const ids=new Set();
  for (const p of bundle.puzzles || []) {
    try {
      validatePuzzle(p);
      if (await sha256(puzzleSerialization(p)) !== p.puzzleFingerprint) errors.push(`puzzleFingerprint:${p.id}`);
    } catch(e) { errors.push(`puzzle:${p.id}:${e.message}`); }
    if (ids.has(p.id)) errors.push(`duplicate:${p.id}`); ids.add(p.id);
    if (!Number.isInteger(p.shortestDistance) || p.shortestDistance < 1) errors.push(`distance:${p.id}`);
    if (!p.puzzleFingerprint || !p.researchPuzzleId) errors.push(`identity:${p.id}`);
  }
  return [...new Set(errors)].sort();
}

export async function validateOrderPlan(plan,bundle) {
  const errors=[];
  if (plan.planFingerprint !== ORDER_PLAN_FINGERPRINT) errors.push('planFingerprintLiteral');
  if (await normalizedFingerprint(plan,'planFingerprint') !== ORDER_PLAN_FINGERPRINT) errors.push('planFingerprintSemantic');
  if (plan.calibrationManifestFingerprint !== CALIBRATION_MANIFEST_FINGERPRINT) errors.push('manifestFingerprint');
  if (plan.formCount !== 4 || plan.forms?.length !== 4) errors.push('formCount');
  const ids=new Set(bundle.puzzles.map(p=>p.id)), seen=new Map();
  for (const form of plan.forms || []) {
    if (form.attempts?.length !== 12) errors.push(`formSize:${form.formId}`);
    const local=new Set();
    for (const [i,a] of (form.attempts||[]).entries()) {
      if (!ids.has(a.id)) errors.push(`unknown:${a.id}`);
      if (local.has(a.id)) errors.push(`duplicateInForm:${form.formId}:${a.id}`); local.add(a.id);
      if (a.position !== i) errors.push(`position:${form.formId}:${i}`);
      if (a.block !== 1 + Math.floor(i/6)) errors.push(`block:${form.formId}:${i}`);
      const p=bundle.puzzles.find(x=>x.id===a.id);
      if (p && a.n !== p.n) errors.push(`n:${a.id}`);
      seen.set(a.id,(seen.get(a.id)||0)+1);
    }
  }
  for (const id of ids) if (seen.get(id)!==2) errors.push(`appearance:${id}:${seen.get(id)||0}`);
  return [...new Set(errors)].sort();
}

export function resolveForm(plan,bundle,formId) {
  const form=plan.forms.find(f=>f.formId===formId); if(!form) throw new Error('UNKNOWN_FORM');
  const byId=new Map(bundle.puzzles.map(p=>[p.id,p]));
  return form.attempts.map(a=>({ ...a, puzzle: structuredClone(byId.get(a.id)) }));
}

export const EVENT_TYPES = new Set([
  'SESSION_STARTED','INSTRUCTION_COMPLETED','WARMUP_STARTED','WARMUP_COMPLETED','COMPREHENSION_GATE_RESULT',
  'PUZZLE_PRESENTED','INPUT_ENABLED','INPUT_DISABLED','ENDPOINT_SELECTED','ACTION_SUBMITTED','ACTION_ACCEPTED','ACTION_REJECTED',
  'PUZZLE_RESTARTED','VISIBILITY_PAUSED','VISIBILITY_RESUMED','PUZZLE_SOLVED','PUZZLE_ABANDONED','SESSION_ENDED'
]);

export function validateEventEnvelope(e) {
  const errors=[];
  if(e.eventSchemaVersion!==EVENT_SCHEMA_VERSION)errors.push('eventSchemaVersion');
  if(e.protocolVersion!==PROTOCOL_VERSION)errors.push('protocolVersion');
  if(e.presentationVersion!==PRESENTATION_VERSION)errors.push('presentationVersion');
  if(e.orderPlanVersion!==ORDER_PLAN_VERSION)errors.push('orderPlanVersion');
  if(e.mechanicBaseline!==MECHANIC_BASELINE)errors.push('mechanicBaseline');
  if(e.calibrationManifestFingerprint!==CALIBRATION_MANIFEST_FINGERPRINT)errors.push('manifestFingerprint');
  if(typeof e.participantAnonId!=='string'||!/^[A-Z]+-[0-9a-f]{32}$/.test(e.participantAnonId))errors.push('participantAnonId');
  if(typeof e.sessionId!=='string'||!/^[A-Z]+-[0-9a-f]{32}$/.test(e.sessionId))errors.push('sessionId');
  if(!Number.isInteger(e.eventIndex)||e.eventIndex<0)errors.push('eventIndex');
  if(!Number.isInteger(e.sessionElapsedMs)||e.sessionElapsedMs<0)errors.push('sessionElapsedMs');
  if(!EVENT_TYPES.has(e.eventType))errors.push('eventType');
  if(!e.payload||typeof e.payload!=='object'||Array.isArray(e.payload))errors.push('payload');
  for(const k of ['attemptId','puzzleResearchId','researchEquivalenceIdV1','puzzleFingerprint']) if(e[k]!==null&&typeof e[k]!=='string')errors.push(k);
  return errors;
}

export function validateEventStream(events) {
  const errors=[]; let last=-1;
  for(let i=0;i<events.length;i++){
    for(const e of validateEventEnvelope(events[i]))errors.push(`${i}:${e}`);
    if(events[i].eventIndex!==i)errors.push(`${i}:contiguousIndex`);
    if(events[i].sessionElapsedMs<last)errors.push(`${i}:monotonicTime`);
    last=events[i].sessionElapsedMs;
  }
  return [...new Set(errors)].sort();
}

export class RuntimeClock {
  constructor(){this.start=performance.now();}
  now(){return Math.max(0,Math.floor(performance.now()-this.start));}
}

export class SyntheticClock {
  constructor(){this.ms=0;}
  advance(ms){if(!Number.isInteger(ms)||ms<0)throw new Error('CLOCK');this.ms+=ms;return this.ms;}
  now(){return this.ms;}
}

export class EventLog {
  constructor({sessionId,participantAnonId,clock}={}) {
    if (HUMAN_COLLECTION_ENABLED !== false) throw new Error('HUMAN_COLLECTION_MUST_BE_DISABLED');
    if (!sessionId || !participantAnonId || !clock) throw new Error('EVENT_LOG_INIT');
    this.sessionId=sessionId; this.participantAnonId=participantAnonId; this.clock=clock; this.events=[];
  }
  emit(eventType,payload={},identity={}) {
    const e={
      eventSchemaVersion:EVENT_SCHEMA_VERSION,protocolVersion:PROTOCOL_VERSION,presentationVersion:PRESENTATION_VERSION,
      orderPlanVersion:ORDER_PLAN_VERSION,mechanicBaseline:MECHANIC_BASELINE,
      calibrationManifestFingerprint:CALIBRATION_MANIFEST_FINGERPRINT,
      participantAnonId:this.participantAnonId,sessionId:this.sessionId,
      attemptId:identity.attemptId??null,puzzleResearchId:identity.puzzleResearchId??null,
      researchEquivalenceIdV1:identity.researchEquivalenceIdV1??null,puzzleFingerprint:identity.puzzleFingerprint??null,
      eventIndex:this.events.length,sessionElapsedMs:this.clock.now(),eventType,payload
    };
    const errors=validateEventEnvelope(e); if(errors.length) throw new Error('EVENT_ENVELOPE:'+errors.join(','));
    this.events.push(e); return e;
  }
}

export function reconstructAttempt(events, shortest) {
  if (!Number.isInteger(shortest)||shortest<1) throw new Error('SHORTEST');
  const types=new Set(['PUZZLE_PRESENTED','INPUT_ENABLED','INPUT_DISABLED','ENDPOINT_SELECTED','ACTION_SUBMITTED','ACTION_ACCEPTED','ACTION_REJECTED','PUZZLE_RESTARTED','VISIBILITY_PAUSED','VISIBILITY_RESUMED','PUZZLE_SOLVED','PUZZLE_ABANDONED','SESSION_ENDED']);
  if(!Array.isArray(events)||events.length<3)throw new Error('EVENTS');
  const x=events.map((e,i)=>({eventIndex:e.eventIndex,sessionElapsedMs:e.sessionElapsedMs,eventType:e.eventType,payload:e.payload||{}}));
  if(x.at(-1).eventType==='SESSION_ENDED'){
    let visible=true; for(const e of x.slice(0,-1)){if(e.eventType==='VISIBILITY_PAUSED')visible=false; if(e.eventType==='VISIBILITY_RESUMED')visible=true;}
    if(!visible){const t=x.at(-1);x.pop();x.push({eventIndex:x.length,sessionElapsedMs:t.sessionElapsedMs,eventType:'VISIBILITY_RESUMED',payload:{syntheticProtocolClosure:true}});x.push({...t,eventIndex:x.length});}
  }
  let visible=true,input=false,started=false,firstInput=null,last=x[0].sessionElapsedMs,terminal=null,terminalMs=null,pending=null,accepted=0,rejected=0,restarts=0,active=0,paused=0,firstAction=null;
  for(let i=0;i<x.length;i++){
    const e=x[i]; if(!types.has(e.eventType)||e.eventIndex!==i)throw new Error('EVENT_SEQUENCE'); if(i&&e.sessionElapsedMs<x[i-1].sessionElapsedMs)throw new Error('TIME');
    if(i){const d=e.sessionElapsedMs-last;if(started&&!visible)paused+=d;if(started&&visible&&input)active+=d;} last=e.sessionElapsedMs;
    if(terminal)throw new Error('AFTER_TERMINAL');
    switch(e.eventType){
      case 'PUZZLE_PRESENTED': if(i!==0)throw new Error('PRESENTED');break;
      case 'INPUT_ENABLED': if(!visible||input)throw new Error('INPUT_ENABLE');input=true;if(!started){started=true;firstInput=e.sessionElapsedMs;}break;
      case 'INPUT_DISABLED': if(!input)throw new Error('INPUT_DISABLE');input=false;break;
      case 'VISIBILITY_PAUSED': if(!visible)throw new Error('PAUSE');visible=false;break;
      case 'VISIBILITY_RESUMED': if(visible)throw new Error('RESUME');visible=true;break;
      case 'ENDPOINT_SELECTED': if(!started||!input||!visible)throw new Error('SELECT');break;
      case 'ACTION_SUBMITTED': if(!started||!input||!visible||pending)throw new Error('SUBMIT');pending=[e.payload.source,e.payload.destination];break;
      case 'ACTION_ACCEPTED':case 'ACTION_REJECTED': if(!pending||pending[0]!==e.payload.source||pending[1]!==e.payload.destination)throw new Error('RESULT');pending=null;if(e.eventType==='ACTION_ACCEPTED'){if(!e.payload.preStateFingerprint||!e.payload.postStateFingerprint)throw new Error('FP');accepted++;if(firstAction===null)firstAction=active;}else rejected++;break;
      case 'PUZZLE_RESTARTED': if(!started||!input||!visible||pending)throw new Error('RESTART');restarts++;break;
      case 'PUZZLE_SOLVED':case 'PUZZLE_ABANDONED':case 'SESSION_ENDED': if(!started||pending)throw new Error('TERMINAL');terminal=e.eventType==='PUZZLE_SOLVED'?'SOLVED':e.eventType==='PUZZLE_ABANDONED'?'ABANDONED_BY_PARTICIPANT':'SESSION_TERMINATED';terminalMs=e.sessionElapsedMs;break;
    }
  }
  if(!terminal||firstInput===null)throw new Error('NO_TERMINAL');
  const excess=terminal==='SOLVED'?(accepted-shortest):null;if(terminal==='SOLVED'&&excess<0)throw new Error('SHORTER_THAN_SHORTEST');
  return {terminalOutcome:terminal,acceptedMoveCount:accepted,restartCount:restarts,rejectedActionCount:rejected,decisionActiveElapsedMs:active,wallElapsedMs:terminalMs-firstInput,firstActionLatencyMs:firstAction,visibilityPausedMs:paused,solvedExcessMoveCount:excess};
}

export function makeValidationExport({formId,sessionEvents,attempts,participantAnonId,sessionId}) {
  if (HUMAN_COLLECTION_ENABLED !== false) throw new Error('COLLECTION_LOCK');
  return {
    schema:'A3_PRE_HUMAN_TECHNICAL_VALIDATION_EXPORT', version:'0.1.0',
    eligibility:EXPORT_ELIGIBILITY, humanCollectionEnabled:false, runtimeMode:RUNTIME_MODE,
    participantAnonId, sessionId, formId,
    presentationVersion:PRESENTATION_VERSION,
    bundleFingerprint:PILOT_BUNDLE_FINGERPRINT, orderPlanFingerprint:ORDER_PLAN_FINGERPRINT,
    sessionEvents, attempts
  };
}
