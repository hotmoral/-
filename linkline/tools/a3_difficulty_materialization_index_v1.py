#!/usr/bin/env python3
"""Encode the final128 difficulty selection as compact deterministic source indexes.

Public-safe transport only: no puzzle geometry, target coordinates, isolation data,
or human/self-test data are persisted.
"""
from __future__ import annotations
import argparse, base64, json, struct
from hashlib import sha256
from pathlib import Path
import tools.a3_target_pair_selection_plan_v1 as v1

SCHEMA="LINKLINE_A3_DIFFICULTY_MATERIALIZATION_INDEX_V1"
SELECTION_SCHEMA="LINKLINE_A3_DIFFICULTY_REBALANCED_1300_PUBLIC_SELECTION_PLAN_V4"
SELECTION_FP="ae1af8798d71a1bd7bf487f382f5cb9ec82ba04b469dd67bd325c11a32b8f802"
STATE_COUNTS={5:128,6:128}
RECORD=">BBIB"
PART_SIZE=325

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--plan",type=Path,required=True); ap.add_argument("--output-dir",type=Path,required=True); args=ap.parse_args()
    plan=json.loads(args.plan.read_text(encoding="utf-8"))
    if plan.get("schema")!=SELECTION_SCHEMA or plan.get("selectionFingerprint")!=SELECTION_FP: raise SystemExit("selection contract mismatch")
    rows=plan.get("order",[])
    if len(rows)!=1300: raise SystemExit("selection row count mismatch")
    rank_cache={}; encoded=bytearray()
    for stage,row in enumerate(rows,1):
        if row.get("stage")!=stage: raise SystemExit(f"stage mismatch:{stage}")
        n=int(row["n"]); length=int(row["chainLength"])
        if n in (3,4):
            source_index=row.get("sourceUniverseIndex"); orientation=row.get("orientationTransform")
            if type(source_index) is not int or source_index<0: raise SystemExit(f"bad legacy source index:{stage}")
            if type(orientation) is not int or not 0<=orientation<8: raise SystemExit(f"bad orientation:{stage}")
        else:
            key=(n,length)
            if key not in rank_cache:
                geometry=v1.reconstruct_geometry_index(n,length,STATE_COUNTS[n])
                rank_cache[key]={identifier:rank for rank,identifier in enumerate(sorted(geometry))}
            if row["id"] not in rank_cache[key]: raise SystemExit(f"unreproducible expanded id:{stage}")
            source_index=rank_cache[key][row["id"]]; orientation=255
        encoded.extend(struct.pack(RECORD,n,length,source_index,orientation))
    size=struct.calcsize(RECORD)
    if len(encoded)!=1300*size: raise SystemExit("encoded length mismatch")
    args.output_dir.mkdir(parents=True,exist_ok=True); parts=[]
    for number,start in enumerate(range(1,1301,PART_SIZE),1):
        end=min(1300,start+PART_SIZE-1); raw=bytes(encoded[(start-1)*size:end*size]); name=f"part_{number:02d}_{start:04d}_{end:04d}.b64"
        (args.output_dir/name).write_text(base64.b64encode(raw).decode("ascii")+"\n",encoding="ascii")
        parts.append({"path":name,"startStage":start,"endStage":end,"recordCount":end-start+1,"sha256":sha256(raw).hexdigest()})
    manifest={"schema":SCHEMA,"version":"1.0.0","sourceSelectionFingerprint":SELECTION_FP,"recordStruct":RECORD,"recordSize":size,"recordCount":1300,"expandedStateCounts":{"5":128,"6":128},"expandedIndexMeaning":"rank in sorted deterministic reconstruct_geometry_index IDs for row N/L","legacyIndexMeaning":"sourceUniverseIndex from selected public legacy universe","orientationSentinelExpanded":255,"parts":parts,"privacy":{"containsPuzzleGeometry":False,"containsTargetCoordinates":False,"containsPrivateIsolationIds":False,"containsHumanOrSelfTestData":False}}
    manifest["payloadSha256"]=sha256(bytes(encoded)).hexdigest()
    (args.output_dir/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","recordCount":1300,"payloadSha256":manifest["payloadSha256"]},sort_keys=True))
if __name__=="__main__": main()
