#!/usr/bin/env python3
"""Encode selected N3/N4 source geometry as deterministic ordinal indexes only.

No coordinates are persisted. This is equivalent in exposure to the existing
sourceUniverseIndex but avoids rebuilding the full research-ID universe privately.
"""
from __future__ import annotations
import argparse, base64, hashlib, json, struct
from itertools import combinations
from pathlib import Path
import tools.a3_final_candidate_pool_public as base
import tools.a3_final_candidate_pool_reuse_v2 as reuse

SCHEMA="LINKLINE_A3_DIFFICULTY_LEGACY_DIRECT_INDEX_V1"
SELECTION_SCHEMA="LINKLINE_A3_DIFFICULTY_REBALANCED_1300_PUBLIC_SELECTION_PLAN_V4"
SELECTION_FP="ae1af8798d71a1bd7bf487f382f5cb9ec82ba04b469dd67bd325c11a32b8f802"
RECORD=">HBBIHB"  # stage,n,length,pathRank,targetPairRank,orientation

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--plan',type=Path,required=True); ap.add_argument('--output-dir',type=Path,required=True); a=ap.parse_args()
    plan=json.loads(a.plan.read_text())
    if plan.get('schema')!=SELECTION_SCHEMA or plan.get('selectionFingerprint')!=SELECTION_FP: raise SystemExit('selection contract mismatch')
    universe=reuse.legacy_universe(); path_cache={}; target_cache={}; raw=bytearray(); count=0
    for row in plan['order']:
        n=int(row['n'])
        if n not in (3,4): continue
        stage=int(row['stage']); length=int(row['chainLength']); si=int(row['sourceUniverseIndex']); ori=int(row['orientationTransform'])
        ident,sn,sl,initial,targets=universe[si]
        if ident!=row['id'] or (sn,sl)!=(n,length): raise SystemExit(f'legacy provenance mismatch:{stage}')
        key=(n,length)
        if key not in path_cache:
            paths=base.enumerate_canonical_paths(n,length); path_cache[key]={p:i for i,p in enumerate(paths)}
        if n not in target_cache:
            target_cache[n]={tuple(p):i for i,p in enumerate(combinations(range(n*n),2))}
        ip=tuple(initial); tp=tuple(sorted(targets))
        if ip not in path_cache[key] or tp not in target_cache[n]: raise SystemExit(f'ordinal reconstruction mismatch:{stage}')
        raw.extend(struct.pack(RECORD,stage,n,length,path_cache[key][ip],target_cache[n][tp],ori)); count+=1
    if count!=156: raise SystemExit(f'legacy count mismatch:{count}')
    a.output_dir.mkdir(parents=True,exist_ok=True)
    (a.output_dir/'legacy_direct.b64').write_text(base64.b64encode(raw).decode()+'\n')
    manifest={'schema':SCHEMA,'version':'1.0.0','sourceSelectionFingerprint':SELECTION_FP,'recordStruct':RECORD,'recordSize':struct.calcsize(RECORD),'recordCount':count,'payloadSha256':hashlib.sha256(raw).hexdigest(),'privacy':{'containsPuzzleGeometry':False,'containsTargetCoordinates':False,'containsPrivateIsolationIds':False,'containsHumanOrSelfTestData':False}}
    (a.output_dir/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','recordCount':count,'payloadSha256':manifest['payloadSha256']},sort_keys=True))
if __name__=='__main__': main()
