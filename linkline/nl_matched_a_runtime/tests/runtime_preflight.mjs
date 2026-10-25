import fs from 'node:fs';
import assert from 'node:assert/strict';
import {validateSessionBundle,SyntheticClock,EventLog,reconstructAttempt,validateEventStream} from '../protocol.mjs';

const bundle=JSON.parse(fs.readFileSync(new URL('../data/session_bundle.json',import.meta.url),'utf8'));
assert.deepEqual(await validateSessionBundle(bundle),[]);

const leak=structuredClone(bundle);leak.puzzles[0].features={shortestDistance:4};
assert((await validateSessionBundle(leak)).some(row=>row.startsWith('analysisLeak:')));

const duplicate=structuredClone(bundle);
duplicate.puzzles[1].n=duplicate.puzzles[0].n;
duplicate.puzzles[1].length=duplicate.puzzles[0].length;
duplicate.puzzles[1].initial=[...duplicate.puzzles[0].initial];
assert((await validateSessionBundle(duplicate)).some(row=>row.startsWith('duplicateInitial:')));

const clock=new SyntheticClock();
const log=new EventLog({sessionRunId:'RUN-'+'a'.repeat(32),clock});
const id={attemptId:'A',puzzleResearchId:'P',researchEquivalenceIdV1:'R',puzzleFingerprint:'F'};
log.emit('PUZZLE_PRESENTED',{},id);log.emit('INPUT_ENABLED',{},id);clock.advance(100);
log.emit('ACTION_SUBMITTED',{source:1,destination:2},id);clock.advance(10);
log.emit('ACTION_ACCEPTED',{source:1,destination:2},id);clock.advance(50);log.emit('PUZZLE_SOLVED',{},id);
assert.deepEqual(validateEventStream(log.events),[]);
const observation=reconstructAttempt(log.events);
assert.equal(observation.acceptedMoveCount,1);
assert.equal(observation.decisionActiveElapsedMs,160);
console.log('NL_MATCHED_A_RUNTIME_PREFLIGHT_PASS');
