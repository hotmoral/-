#!/usr/bin/env python3
"""TEMP P5 Stage46->49 STAGE_SETTLED chain for the promising armored/standoff Stage48 pulse.

Purpose:
- preserve the currently promising Stage48 single protected pulse: three spatially separated
  armored-durable diagnostic bodies followed by one SIEGER;
- apply each SIEGER standoff threshold globally across Stage46-49, because standoff is a monster
  property unless a separate stage-specific mechanic is later approved;
- carry wall deficit and require STAGE_SETTLED;
- compare representative shop profiles across all five classes;
- keep Tank at diagnostic center 0.25 only for this encounter-direction check.

No packet, standoff value, monster identity, or balance value is adopted/frozen/production-authorized.
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
        low.row("SIEGER", 2, 8.0, 2.0),
    ]
    s48["note"] = "TEMP_SINGLE_ARMORED3_SPATIAL_PROTECTED_ROLE_PULSE_CHAIN_DIAGNOSTIC"
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
    profiles = list(integration["representativeShopProfiles"])

    thresholds = [0.38, 0.78, 0.82]
    original_sim = integ.SIMULATE
    out = {
        "version": "p5-stage46-49-armored-standoff-chain-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "stage48Candidate": "SINGLE_ARMORED3_SPATIAL_PLUS_SIEGER",
        "tankDiagnosticCoefficient": 0.25,
        "thresholdsGlobalAcrossStage46To49": thresholds,
        "shopProfiles": profiles,
        "rows": [],
    }

    try:
        for threshold in thresholds:
            rebuilt = standoff.build_sim_with_threshold(threshold)
            integ.SIMULATE = hybrid.install_fixed_schedule_hook_on(rebuilt)

            for profile_name in profiles:
                for cls in integ.CLASSES:
                    chain = settled.run_chain(
                        base, temporal, d, shop, integration,
                        cls, profile_name, scale,
                        0.25 if cls == "Tank" else None,
                    )
                    stage_rows = []
                    for sr in chain["stages"]:
                        stage_rows.append({
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
                        "profile": profile_name,
                        "settledThroughStage49": chain["settledThroughStage49"],
                        "stagesSettled": chain["stagesSettled"],
                        "finalWall": chain["finalWall"],
                        "finalAbsoluteDeficit": chain["finalAbsoluteDeficit"],
                        "stages": stage_rows,
                    })
    finally:
        integ.SIMULATE = original_sim

    # compact aggregate for easy comparison
    for threshold in thresholds:
        rows = [r for r in out["rows"] if r["thresholdX"] == threshold]
        out.setdefault("aggregate", {})[str(threshold)] = {
            "caseCount": len(rows),
            "settledThrough49Count": sum(1 for r in rows if r["settledThroughStage49"]),
            "buriedCaseCount": sum(1 for r in rows if any(s["buried"] for s in r["stages"])),
            "minFinalWall": min((r["finalWall"] for r in rows), default=None),
            "maxFinalWall": max((r["finalWall"] for r in rows), default=None),
            "totalSiegerShotsByClass": {
                cls: sum(sum(s["siegerShots"] for s in r["stages"]) for r in rows if r["class"] == cls)
                for cls in integ.CLASSES
            },
            "stage48SiegerShotsByClass": {
                cls: sum(next((s["siegerShots"] for s in r["stages"] if s["stage"] == 48), 0) for r in rows if r["class"] == cls)
                for cls in integ.CLASSES
            },
        }

    text = json.dumps(out, indent=2, sort_keys=True)
    Path("p5_stage46_49_armored_standoff_chain_temp.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
