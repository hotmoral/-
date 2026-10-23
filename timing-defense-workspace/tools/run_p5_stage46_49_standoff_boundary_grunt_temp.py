#!/usr/bin/env python3
"""TEMP P5 Stage46->49 boundary screen around the first plausible Mage firing region.

Uses the same Stage48 ARMORED3 + GRUNT2 + SIEGER packet as the moderate screen.
Scans only 0.72/0.74/0.76 globally with BALANCED shop profile and STAGE_SETTLED.
Diagnostic only; no value is adopted/frozen.
"""
from __future__ import annotations
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_sieger_standoff_sensitivity_temp as standoff
import run_p5_stage48_armored_standoff_hybrid_temp as hybrid
import run_p5_stage46_49_moderate_standoff_grunt_screen_temp as moderate


def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))

def main():
    base=load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    temporal=load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49=load("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction=load("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop=load("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    refinement=load("legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json")
    integration=load("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")
    integ.validate_right_edge_contract(direction)
    base=integ.inject_diagnostic_monsters(base,stage49)
    base["monsterAnchors"]["ARMORED_DURABLE_PROXY"]=dict(refinement["knightRobustPair"]["anchor"])
    d=moderate.candidate_direction(direction)
    scale=float(integration["shopEffectScale"]); profile="BALANCED"; thresholds=[0.72,0.74,0.76]
    original=integ.SIMULATE
    out={"version":"p5-stage46-49-standoff-boundary-grunt-temp-v0.1","authority":"TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY","thresholds":thresholds,"rows":[]}
    try:
        for threshold in thresholds:
            integ.SIMULATE=hybrid.install_fixed_schedule_hook_on(standoff.build_sim_with_threshold(threshold))
            for cls in integ.CLASSES:
                chain=settled.run_chain(base,temporal,d,shop,integration,cls,profile,scale,0.25 if cls=="Tank" else None)
                out["rows"].append({
                    "thresholdX":threshold,"class":cls,"settledThroughStage49":chain["settledThroughStage49"],"finalWall":chain["finalWall"],"finalAbsoluteDeficit":chain["finalAbsoluteDeficit"],
                    "stages":[{"stage":s["stage"],"settled":s["settled"],"buried":s["buried"],"burialTime":s.get("burialTime"),"startWall":s["startWall"],"endWall":s["endWall"],"siegerShots":int(s.get("siegerShots") or 0)} for s in chain["stages"]]
                })
    finally:
        integ.SIMULATE=original
    out["aggregate"]={}
    for threshold in thresholds:
        rows=[r for r in out["rows"] if r["thresholdX"]==threshold]
        out["aggregate"][str(threshold)]={
            "settledThrough49Count":sum(1 for r in rows if r["settledThroughStage49"]),
            "buriedCaseCount":sum(1 for r in rows if any(s["buried"] for s in r["stages"])),
            "minFinalWall":min(r["finalWall"] for r in rows),
            "stage48ShotsByClass":{cls:next(next((s["siegerShots"] for s in r["stages"] if s["stage"]==48),0) for r in rows if r["class"]==cls) for cls in integ.CLASSES},
            "totalShotsByClass":{cls:sum(sum(s["siegerShots"] for s in r["stages"]) for r in rows if r["class"]==cls) for cls in integ.CLASSES},
        }
    text=json.dumps(out,indent=2,sort_keys=True); Path("p5_stage46_49_standoff_boundary_grunt_temp.json").write_text(text+"\n",encoding="utf-8"); print(text)

if __name__=="__main__": main()
