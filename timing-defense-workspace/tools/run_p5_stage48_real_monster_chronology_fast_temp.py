#!/usr/bin/env python3
"""Fast bounded screen for Stage48 real-monster chronology candidates.

Uses the already validated diagnostic rule: 60s authored spawn window + 60s no-new-spawn drain.
Candidates that do not reach zero live enemies within 120s are rejected/escalated to exact settle-time review.
No production authority, no candidate adoption.
"""
from __future__ import annotations

import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_real_monster_chronology_search_temp as search


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_chain_fast(base, base_temporal, direction, shop, integration, cls, profile_name, scale, tank_coeff):
    profile = integ.profile_for(shop, cls, profile_name)
    wall_max = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * float(scale)
    current = wall_max
    stages = []
    for stage_no in settled.STAGES:
        start = current
        row, schedule = settled.simulate_stage(
            base, base_temporal, direction, integration, cls, profile, scale,
            stage_no, current, tank_coeff, 120.0,
        )
        current = float(row["endWall"])
        settled_ok = row.get("burialTime") is None and int(row.get("endActive", 0)) == 0
        stages.append({
            "stage": stage_no,
            "startWall": round(start, 3),
            "maxWall": round(wall_max, 3),
            "startAbsoluteDeficit": round(max(0.0, wall_max-start), 3),
            "settledWithin120": settled_ok,
            "burialTime": row.get("burialTime"),
            "endWall": row.get("endWall"),
            "endActive": row.get("endActive"),
            "maxActive": row.get("maxActive"),
            "kills": row.get("kills"),
            "wallHits": row.get("wallHits"),
            "siegerShots": row.get("siegerShots"),
            "authoredLastSpawnSeconds": round(max((x[0] for x in schedule), default=0.0), 3),
            "endAbsoluteDeficit": round(max(0.0, wall_max-current), 3),
        })
        if not settled_ok:
            break
    return {
        "class": cls,
        "profile": profile_name,
        "tankShockwaveCoefficient": tank_coeff if cls == "Tank" else None,
        "settledThroughStage49": len(stages)==4 and all(s["settledWithin120"] for s in stages),
        "finalWall": round(current, 3),
        "stages": stages,
    }


def aggregate(rows):
    s48pairs=[]
    for r in rows:
        s=next((x for x in r["stages"] if x["stage"]==48),None)
        if s: s48pairs.append((r,s))
    per_class={}
    for cls in integ.CLASSES:
        cr=[(r,s) for r,s in s48pairs if r["class"]==cls]
        shots=[int(s.get("siegerShots") or 0) for _,s in cr]
        walls=[float(s.get("endWall") or 0) for _,s in cr]
        per_class[cls]={
            "rows":len(cr),
            "siegerShotCases":sum(x>0 for x in shots),
            "totalSiegerShots":sum(shots),
            "minStage48EndWall":round(min(walls),3) if walls else None,
            "maxStage48EndWall":round(max(walls),3) if walls else None,
        }
    failures=[]
    for r in rows:
        if not r["settledThroughStage49"]:
            failures.append({
                "class":r["class"],"profile":r["profile"],
                "stages":[s for s in r["stages"] if not s["settledWithin120"]],
            })
    shots=[int(s.get("siegerShots") or 0) for _,s in s48pairs]
    return {
        "settledThroughStage49Count":sum(bool(r["settledThroughStage49"]) for r in rows),
        "totalRows":len(rows),
        "failures":failures,
        "stage48SiegerShotCases":sum(x>0 for x in shots),
        "stage48TotalSiegerShots":sum(shots),
        "stage48MaxSiegerShotsOneRow":max(shots) if shots else 0,
        "perClass":per_class,
    }


def main():
    base = load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    base_temporal = load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
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
    scale=float(integration["shopEffectScale"])
    profiles=list(integration["representativeShopProfiles"])
    out={
        "version":"p5-stage48-real-monster-chronology-fast-temp-v0.1",
        "sourceCanonicalHead":"33cac0072964c620383ddb3c71e3d6ac75e71a98",
        "spawnWindowSeconds":60.0,
        "drainTailSeconds":60.0,
        "physicalSpawnX":direction["globalRules"]["normalRightEdgeSpawnX"],
        "stage48CycleSecondsHeldFixed":direction["stageDirection"]["48"]["pressureCycleSecondsCandidate"],
        "tankCoefficientForCrossClassSearch":0.25,
        "variants":{},
        "authority":"TEMP_BOUNDED_SCREEN_NO_CANDIDATE_ADOPTION_NO_FREEZE",
    }
    for name,d in search.variants(direction).items():
        rows=[]
        for profile in profiles:
            for cls in integ.CLASSES:
                rows.append(run_chain_fast(
                    base,base_temporal,d,shop,integration,cls,profile,scale,
                    0.25 if cls=="Tank" else None,
                ))
        out["variants"][name]={
            "stage48Packet":d["stageDirection"]["48"]["diagnosticPacket"],
            "aggregate":aggregate(rows),
            "rows":rows,
        }
    text=json.dumps(out,indent=2,sort_keys=True)
    Path("p5_stage48_real_monster_chronology_fast_temp.json").write_text(text+"\n",encoding="utf-8")
    print(text)

if __name__=="__main__":
    main()
