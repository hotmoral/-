#!/usr/bin/env python3
"""TEMP diagnostic: distinguish SIEGER never reaching siege from dying during windup."""
from __future__ import annotations

import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_real_monster_frontline_search_temp_v2 as v2


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    base = load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    temporal = load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49 = load("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction = load("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop = load("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    refinement = load("legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json")
    integration = load("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")

    integ.validate_right_edge_contract(direction)
    base = integ.inject_diagnostic_monsters(base, stage49)
    if "ARMORED_DURABLE_PROXY" not in base["monsterAnchors"]:
        base["monsterAnchors"]["ARMORED_DURABLE_PROXY"] = dict(refinement["knightRobustPair"]["anchor"])
    settled.install_fixed_schedule_hook()
    scale = float(integration["shopEffectScale"])
    profiles = list(integration["representativeShopProfiles"])
    starts = v2.pre_stage48_states(base, temporal, direction, shop, integration, profiles, scale)

    output = {"variants": {}}
    for name, d in v2.variants(direction).items():
        rows=[]
        for profile_name in profiles:
            for cls in integ.CLASSES:
                st=starts[(profile_name,cls)]
                row48,_=settled.simulate_stage(
                    base, temporal, d, integration, cls, st["profile"], scale,
                    48, st["startStage48Wall"], 0.25 if cls=="Tank" else None, 120.0,
                )
                rows.append({
                    "class":cls,"profile":profile_name,
                    "windups":int(row48.get("siegerWindups") or 0),
                    "shots":int(row48.get("siegerShots") or 0),
                    "repositions":int(row48.get("siegerRepositions") or 0),
                    "kills":int(row48.get("kills") or 0),
                    "endActive":int(row48.get("endActive") or 0),
                    "wallHits":int(row48.get("wallHits") or 0),
                    "endWall":row48.get("endWall"),
                })
        output["variants"][name]={
            "windupCases":sum(r["windups"]>0 for r in rows),
            "totalWindups":sum(r["windups"] for r in rows),
            "shotCases":sum(r["shots"]>0 for r in rows),
            "totalShots":sum(r["shots"] for r in rows),
            "repositionCases":sum(r["repositions"]>0 for r in rows),
            "totalRepositions":sum(r["repositions"] for r in rows),
            "perClass":{
                cls:{
                    "windupCases":sum(r["windups"]>0 for r in rows if r["class"]==cls),
                    "totalWindups":sum(r["windups"] for r in rows if r["class"]==cls),
                    "shotCases":sum(r["shots"]>0 for r in rows if r["class"]==cls),
                    "totalShots":sum(r["shots"] for r in rows if r["class"]==cls),
                } for cls in integ.CLASSES
            },
            "rows":rows,
        }
    text=json.dumps(output,indent=2,sort_keys=True)
    Path("p5_stage48_sieger_windup_diagnostic_temp.json").write_text(text+"\n",encoding="utf-8")
    print(text)

if __name__=="__main__":
    main()
