#!/usr/bin/env python3
"""TEMP P5 Stage46->49 moderate global SIEGER standoff screen.

Purpose:
- use the current clean Stage48 diagnostic packet: 3 spatial ARMORED_DURABLE_PROXY + 2 GRUNT + SIEGER;
- keep every physical spawn at right edge and preserve STAGE_SETTLED / carried wall deficit;
- scan moderate global SIEGER standoff thresholds before considering any exact value;
- BALANCED shop profile only for the first cheap screen across all five classes.

No threshold, packet, monster stat, class stat, or production value is adopted/frozen.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_armored_low_density_front_temp as low
import run_p5_stage48_sieger_standoff_sensitivity_temp as standoff
import run_p5_stage48_armored_standoff_hybrid_temp as hybrid


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def candidate_direction(direction):
    d = copy.deepcopy(direction)
    s48 = d["stageDirection"]["48"]
    s48["pressureCycleSecondsCandidate"] = 999.0
    s48["diagnosticPacket"] = [
        low.row("ARMORED_DURABLE_PROXY", -2, 5.25),
        low.row("ARMORED_DURABLE_PROXY", 0, 6.25),
        low.row("ARMORED_DURABLE_PROXY", -1, 7.25),
        low.row("GRUNT", 1, 5.85),
        low.row("GRUNT", 0, 6.98),
        low.row("SIEGER", 2, 8.0, 2.0),
    ]
    s48["note"] = "TEMP_SINGLE_ARMORED3_GRUNT2_PROTECTED_ROLE_PULSE_MODERATE_STANDOFF_SCREEN"
    integ.validate_right_edge_contract(d)
    return d


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
    base["monsterAnchors"]["ARMORED_DURABLE_PROXY"] = dict(refinement["knightRobustPair"]["anchor"])
    d = candidate_direction(direction)
    scale = float(integration["shopEffectScale"])
    profile_name = "BALANCED"
    thresholds = [0.38, 0.50, 0.55, 0.60, 0.65, 0.70]

    original_sim = integ.SIMULATE
    out = {
        "version": "p5-stage46-49-moderate-standoff-grunt-screen-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "stage48Candidate": "ARMORED3_SPATIAL_PLUS_GRUNT2_PLUS_SIEGER",
        "shopProfile": profile_name,
        "tankDiagnosticCoefficient": 0.25,
        "thresholdsGlobalAcrossStage46To49": thresholds,
        "rows": [],
    }

    try:
        for threshold in thresholds:
            rebuilt = standoff.build_sim_with_threshold(threshold)
            integ.SIMULATE = hybrid.install_fixed_schedule_hook_on(rebuilt)
            for cls in integ.CLASSES:
                chain = settled.run_chain(
                    base, temporal, d, shop, integration,
                    cls, profile_name, scale,
                    0.25 if cls == "Tank" else None,
                )
                stages = []
                for sr in chain["stages"]:
                    stages.append({
                        "stage": sr["stage"],
                        "settled": sr["settled"],
                        "buried": sr["buried"],
                        "startWall": sr["startWall"],
                        "endWall": sr["endWall"],
                        "wallLoss": round(float(sr["startWall"]) - float(sr["endWall"]), 3),
                        "siegerShots": int(sr.get("siegerShots") or 0),
                        "wallHits": int(sr.get("wallHits") or 0),
                        "settleSeconds": sr.get("settleSeconds"),
                        "tailBeyond60Seconds": sr.get("tailBeyond60Seconds"),
                        "burialTime": sr.get("burialTime"),
                    })
                out["rows"].append({
                    "thresholdX": threshold,
                    "class": cls,
                    "settledThroughStage49": chain["settledThroughStage49"],
                    "stagesSettled": chain["stagesSettled"],
                    "finalWall": chain["finalWall"],
                    "finalAbsoluteDeficit": chain["finalAbsoluteDeficit"],
                    "stages": stages,
                })
    finally:
        integ.SIMULATE = original_sim

    aggregate = {}
    for threshold in thresholds:
        rows = [r for r in out["rows"] if r["thresholdX"] == threshold]
        aggregate[str(threshold)] = {
            "caseCount": len(rows),
            "settledThrough49Count": sum(1 for r in rows if r["settledThroughStage49"]),
            "buriedCaseCount": sum(1 for r in rows if any(s["buried"] for s in r["stages"])),
            "minFinalWall": min((r["finalWall"] for r in rows), default=None),
            "stage48ShotsByClass": {
                cls: next((next((s["siegerShots"] for s in r["stages"] if s["stage"] == 48), 0) for r in rows if r["class"] == cls), 0)
                for cls in integ.CLASSES
            },
            "totalShotsByClass": {
                cls: sum(sum(s["siegerShots"] for s in r["stages"]) for r in rows if r["class"] == cls)
                for cls in integ.CLASSES
            },
        }
    out["aggregate"] = aggregate

    text = json.dumps(out, indent=2, sort_keys=True)
    Path("p5_stage46_49_moderate_standoff_grunt_screen_temp.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
