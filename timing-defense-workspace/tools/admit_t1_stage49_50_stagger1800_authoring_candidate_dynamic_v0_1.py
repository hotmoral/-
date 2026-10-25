#!/usr/bin/env python3
"""Narrow exact dynamic admission for the materialized T1 Stage49-50 STAGGER1800 candidate.

This is not a search. It checks whether the explicit authoring candidate reproduces
already-accepted diagnostic evidence from doc169 while preserving v0.2 Stage46-48
lead-in and the diagnostic-only Archer/Mage fidelity bridges.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import preflight_t1_stage49_50_stagger1800_authoring_candidate_v0_1 as staticp
import probe_t1_stage49_50_sustain_integration_compare_v0_1 as compare

r = compare.r

EXPECTED = {
    "roles": {
        "knight": {"pct": 0.430303, "unresolved": 0},
        "rogue": {"pct": 0.300662, "unresolved": 0},
        "tank": {"pct": 0.273684, "unresolved": 3},
        "archer": {"pct": 0.017241, "unresolved": 0},
        "mage": {"pct": 0.094216, "unresolved": 0},
    },
    "offWallDamage": 1358.0,
    "onWallDamage": 164.0,
    "offMeanFinalBaseHp": 1945.68,
    "onMeanFinalBaseHp": 1993.44,
    "classesWithWallPressureOff": 1,
    "classesWithWallPressureOn": 1,
}


def close(a: float | None, b: float, tol: float = 1e-6) -> bool:
    return a is not None and abs(float(a) - float(b)) <= tol


def materialize(base: dict, candidate: dict) -> dict:
    doc = copy.deepcopy(base)
    doc["version"] = "t1-representative-transition-slice-recipes-v0.3-stage49-50-stagger1800-authoring-candidate"
    doc["status"] = "BOUNDED_STAGE49_50_AUTHORING_CANDIDATE_NO_PRODUCTION_OR_NUMERICAL_FREEZE"
    by = {int(x["stage"]): x for x in doc["recipes"]}
    for raw in candidate["stageOverrides"]:
        stage = int(raw["stage"])
        by[stage].clear()
        by[stage].update(staticp.materializable_override(raw))
    return doc


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--p3", default="legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json")
    ap.add_argument("--p4d2-base", default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    ap.add_argument("--p4d2-temporal", default="legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    ap.add_argument("--seeds", default="101,211,307,409,503")
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    base_path = Path(args.base)
    candidate_path = Path(args.candidate)
    base = r.load_yaml(base_path)
    candidate = r.load_yaml(candidate_path)
    p3 = r.load_json(args.p3)
    p4 = r.load_json(args.p4d2_base)
    temporal = r.load_json(args.p4d2_temporal)
    seeds = tuple(int(x) for x in args.seeds.split(",") if x.strip())

    errors: list[str] = []
    base_sha = r.sha256_bytes(base_path.read_bytes())
    candidate_sha = r.sha256_bytes(candidate_path.read_bytes())
    if base_sha != candidate["baseRecipe"]["sha256"]:
        errors.append("base-sha-mismatch")
    if candidate_sha != "c1bd5f45fb3cbdff6efa45b90f34e20bbc303a94d089564abf62523e15425bc3":
        errors.append("candidate-sha-mismatch-from-static-admission")

    materialized = materialize(base, candidate)
    by = {int(x["stage"]): x for x in materialized["recipes"]}
    base_by = {int(x["stage"]): x for x in base["recipes"]}

    # Stage46-48 are the persistent-state lead-in and must remain exact v0.2.
    for stage in (46, 47, 48):
        if by[stage] != base_by[stage]:
            errors.append(f"stage{stage}-lead-in-drift")

    # Compare explicit authoring spawns to the exact diagnostic generator.
    diagnostic_generated = compare.sustain.build_candidate(base, "STAGGER_1800")
    diag_by = {int(x["stage"]): x for x in diagnostic_generated["recipes"]}
    spawn_equivalence = {}
    for stage in (49, 50):
        same = by[stage]["spawns"] == diag_by[stage]["spawns"]
        spawn_equivalence[str(stage)] = same
        if not same:
            errors.append(f"stage{stage}-spawn-list-differs-from-diagnostic-generator")

    # Static runner gate remains required on the complete materialized recipe.
    errors.extend(f"runner-static:{e}" for e in r.static_recipe_gate(materialized))

    overall = compare.magebridge.with_mage_lv31_fidelity(
        lambda: compare.widthbridge.with_archer_final_width(
            compare.WIDTH,
            lambda: compare.shape.execute_candidate(materialized, p3, p4, temporal, seeds),
        )
    )
    fidelity = [f"overall:{e}" for e in overall["fidelityErrors"]]

    phase_rows, phase_agg, phase_fidelity = compare.magebridge.with_mage_lv31_fidelity(
        lambda: compare.widthbridge.with_archer_final_width(
            compare.WIDTH,
            lambda: compare.execute_target_phase(materialized, p3, p4, temporal, seeds),
        )
    )
    fidelity.extend(f"phase:{e}" for e in phase_fidelity)
    errors.extend(f"fidelity:{e}" for e in fidelity)

    # Paired deterministic lifecycle and completion guards.
    for row in overall["rows"]:
        if not row["sameInitialLifecycle"]:
            errors.append(f"pair-entry-mismatch:{row['class']}:{row['seed']}")
        if not row["deterministicOFF"] or not row["deterministicON"]:
            errors.append(f"determinism-fail:{row['class']}:{row['seed']}")
        for side in ("OFF", "ON"):
            block = row[side]
            if block["finalStatus"] == "FAILED" or len(block["stagesExecuted"]) < 5:
                errors.append(f"failed-or-incomplete:{row['class']}:{row['seed']}:{side}")

    roles = {}
    for cls in r.CLASSES:
        off = compare.orderprobe.role_stats(phase_agg, cls, "OFF")
        on = compare.orderprobe.role_stats(phase_agg, cls, "ON")
        delta = compare.orderprobe.role_delta(off, on)
        roles[cls] = {"OFF": off, "ON": on, "delta": delta}
        expected = EXPECTED["roles"][cls]
        if not close(delta["clearLatencyImprovementPct"], expected["pct"]):
            errors.append(f"role-pct-mismatch:{cls}:{delta['clearLatencyImprovementPct']}!=expected{expected['pct']}")
        if int(delta["unresolvedImprovement"]) != int(expected["unresolved"]):
            errors.append(f"role-unresolved-mismatch:{cls}:{delta['unresolvedImprovement']}!=expected{expected['unresolved']}")
        if not str(delta["direction"]).startswith("POSITIVE"):
            errors.append(f"role-direction-not-positive:{cls}:{delta['direction']}")

    # Exact diagnostic aggregate reproduction.
    if not close(overall["OFF"]["totalWallDamage"], EXPECTED["offWallDamage"]):
        errors.append("off-wall-damage-mismatch")
    if not close(overall["ON"]["totalWallDamage"], EXPECTED["onWallDamage"]):
        errors.append("on-wall-damage-mismatch")
    if not close(overall["OFF"]["meanFinalBaseHp"], EXPECTED["offMeanFinalBaseHp"]):
        errors.append("off-mean-final-base-hp-mismatch")
    if not close(overall["ON"]["meanFinalBaseHp"], EXPECTED["onMeanFinalBaseHp"]):
        errors.append("on-mean-final-base-hp-mismatch")
    if int(overall["OFF"]["classesWithWallPressure"]) != EXPECTED["classesWithWallPressureOff"]:
        errors.append("off-wall-pressure-class-count-mismatch")
    if int(overall["ON"]["classesWithWallPressure"]) != EXPECTED["classesWithWallPressureOn"]:
        errors.append("on-wall-pressure-class-count-mismatch")

    out = {
        "version": "t1-stage49-50-stagger1800-authoring-dynamic-admission-v0.1",
        "status": "PASS" if not errors else "FAIL",
        "scope": "MATERIALIZED_STAGE49_50_CANDIDATE_WITH_V02_STAGE46_48_LEAD_IN",
        "baseRecipe": str(base_path),
        "baseRecipeSha256": base_sha,
        "candidate": str(candidate_path),
        "candidateSha256": candidate_sha,
        "seeds": list(seeds),
        "spawnEquivalentToDiagnosticGenerator": spawn_equivalence,
        "diagnosticCenter": "STAGGER_1800_STAGE50_CLUSTER_ONLY",
        "archerWidthBridge": {"yTolerance": compare.WIDTH, "status": "DIAGNOSTIC_ONLY_NOT_FROZEN"},
        "mageLv31FidelityBridge": compare.magebridge.BRIDGE_METADATA,
        "fidelityErrors": fidelity,
        "roles": roles,
        "overall": {"OFF": overall["OFF"], "ON": overall["ON"]},
        "expectedDoc169": EXPECTED,
        "productionGameplayChange": False,
        "authoringAdopted": False,
        "numericalFreeze": False,
        "fullT1ExactRecipeFreeze": False,
        "errors": errors,
    }
    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    if errors:
        raise SystemExit("T1_STAGE49_50_STAGGER1800_DYNAMIC_ADMISSION_FAIL")


if __name__ == "__main__":
    main()
