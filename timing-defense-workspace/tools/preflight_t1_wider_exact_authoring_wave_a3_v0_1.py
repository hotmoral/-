#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path

import yaml

import run_t1_transition_slice_microsim_settlement_fix_v0_1 as settlement_bridge

r = settlement_bridge.runner

TARGETS = [24, 25, 29, 30, 31]
ALLOWED_MONSTERS = {"GRUNT", "RUNNER", "BRUTE"}
ALLOWED_STAGE_KEYS = {
    "id", "stage", "archetype", "componentArchetypes", "formation",
    "formationSet", "cadence", "complexity", "pressureTags", "entryBaseX", "spawns",
}
ALLOWED_SPAWN_KEYS = {"tMs", "type", "y"}
A1_SHA = "44616732b4cbba8bc52df294d98e0ab485b400d7ec7e9b9bfdd9f3fe32d2910d"
A2_SHA = "2d3bf477e80617c0d26d2c349588caa446195b39c2581df0f11dd29eb1f37f8d"


def max_density(spawns: list[dict], window_ms: int) -> int:
    times = [int(x["tMs"]) for x in spawns]
    if not times:
        return 0
    return max(sum(1 for t in times if start <= t < start + window_ms) for start in times)


def stage_static(stage: dict) -> dict:
    times = [int(x["tMs"]) for x in stage["spawns"]]
    ys = [float(x["y"]) for x in stage["spawns"]]
    return {
        "authored": len(stage["spawns"]),
        "typeCounts": dict(sorted(Counter(str(x["type"]) for x in stage["spawns"]).items())),
        "max4s": max_density(stage["spawns"], 4000),
        "max6s": max_density(stage["spawns"], 6000),
        "firstSpawnMs": min(times),
        "lastSpawnMs": max(times),
        "minY": min(ys),
        "maxY": max(ys),
        "ySpan": max(ys) - min(ys),
        "intervalsMs": [b - a for a, b in zip(times, times[1:])],
    }


def parse_plan_archetype(signature: str) -> str:
    return signature.split("/", 1)[0].strip()


def metadata(stage: dict) -> dict:
    return {
        "archetype": stage.get("archetype"),
        "componentArchetypes": stage.get("componentArchetypes", []),
        "formation": stage.get("formation"),
        "cadence": stage.get("cadence"),
        "complexity": stage.get("complexity"),
        "pressure": ",".join(stage.get("pressureTags", [])),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--a1", required=True)
    ap.add_argument("--a2", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--materialized-out", required=True)
    args = ap.parse_args()

    base_path = Path(args.base)
    plan_path = Path(args.plan)
    a1_path = Path(args.a1)
    a2_path = Path(args.a2)
    candidate_path = Path(args.candidate)

    base = r.load_yaml(base_path)
    plan = r.load_yaml(plan_path)
    a1 = r.load_yaml(a1_path)
    a2 = r.load_yaml(a2_path)
    candidate = r.load_yaml(candidate_path)

    errors: list[str] = []
    warnings: list[str] = []

    actual_base_sha = r.sha256_bytes(base_path.read_bytes())
    actual_plan_sha = r.sha256_bytes(plan_path.read_bytes())
    actual_a1_sha = r.sha256_bytes(a1_path.read_bytes())
    actual_a2_sha = r.sha256_bytes(a2_path.read_bytes())

    if candidate.get("baseRecipe", {}).get("sha256") != actual_base_sha:
        errors.append("base-recipe-sha-mismatch")
    if candidate.get("plan", {}).get("sha256") != actual_plan_sha:
        errors.append("wave-plan-sha-mismatch")
    if candidate.get("plan", {}).get("slice") != "WAVE_A3_LV21_BUFFER_TO_CHECKPOINT_B_SOFTWALL_ENTRY":
        errors.append("slice-id-mismatch")
    if actual_a1_sha != A1_SHA or candidate.get("priorCandidates", {}).get("a1", {}).get("sha256") != actual_a1_sha:
        errors.append("a1-prior-candidate-sha-drift")
    if actual_a2_sha != A2_SHA or candidate.get("priorCandidates", {}).get("a2", {}).get("sha256") != actual_a2_sha:
        errors.append("a2-prior-candidate-sha-drift")

    scope = candidate.get("scope", {})
    if scope.get("addedStages") != TARGETS:
        errors.append("scope-addedStages-not-24-25-29-30-31")
    if scope.get("contextOnlyStages") != []:
        errors.append("scope-contextOnlyStages-must-be-empty")
    if scope.get("allowedMonsters") != ["GRUNT", "RUNNER", "BRUTE"]:
        errors.append("scope-monster-vocabulary-drift")
    for flag in (
        "monsterScalarChange", "classScalarChange", "shopExpPxpChange",
        "productionGameplayChange", "fullT1ExactRecipeFreeze", "candidateAdopted",
    ):
        if scope.get(flag) is not False:
            errors.append(f"scope-{flag}-must-remain-false")
    if float(scope.get("physicalSpawnX", -1)) != 0.92:
        errors.append("physicalSpawnX-not-0.92")
    if scope.get("midfieldPopIn") is not False:
        errors.append("midfield-pop-in-not-false")
    if int(scope.get("authored4sNormalMax", -1)) != 8:
        errors.append("authored4s-cap-not-8")

    additions = candidate.get("stageAdditions", [])
    if [int(x.get("stage", -1)) for x in additions] != TARGETS:
        errors.append("stageAdditions-not-exactly-24-25-29-30-31")
    add_by = {int(x["stage"]): x for x in additions if "stage" in x}

    base_by = {int(x["stage"]): x for x in base.get("recipes", [])}
    a1_by = {int(x["stage"]): x for x in a1.get("stageAdditions", [])}
    a2_by = {int(x["stage"]): x for x in a2.get("stageAdditions", [])}
    prior_stage_set = set(base_by) | set(a1_by) | set(a2_by)
    if set(TARGETS) & prior_stage_set:
        errors.append("a3-target-overlaps-existing-or-prior-candidate-stage")

    expected = {int(k): v for k, v in plan.get("expectedSignatures", {}).items()}
    expected_components = {
        24: ["E01"],
        25: ["E01"],
        29: ["E02", "E03"],
        30: ["E01", "E03"],
        31: ["E03"],
    }

    for stage in TARGETS:
        raw = add_by.get(stage)
        if raw is None:
            continue
        extra = set(raw) - ALLOWED_STAGE_KEYS
        if extra:
            errors.append(f"stage{stage}-unexpected-keys:{sorted(extra)}")
        for i, spawn in enumerate(raw.get("spawns", [])):
            extra_spawn = set(spawn) - ALLOWED_SPAWN_KEYS
            if extra_spawn:
                errors.append(f"stage{stage}-spawn{i}-unexpected-keys:{sorted(extra_spawn)}")
            if str(spawn.get("type")) not in ALLOWED_MONSTERS:
                errors.append(f"stage{stage}-spawn{i}-illegal-monster:{spawn.get('type')}")
            if not (0.0 <= float(spawn.get("y", -1)) <= 1.0):
                errors.append(f"stage{stage}-spawn{i}-y-out-of-range")
        if float(raw.get("entryBaseX", -1)) != 0.92:
            errors.append(f"stage{stage}-entryBaseX-not-0.92")

        want = expected.get(stage, {})
        got = metadata(raw)
        plan_arch = parse_plan_archetype(str(want.get("signature", "")))
        if str(got["archetype"]) != plan_arch.split("+", 1)[0]:
            errors.append(f"stage{stage}-archetype-plan-mismatch:{got['archetype']}!={plan_arch}")
        if got["componentArchetypes"] != expected_components[stage]:
            errors.append(f"stage{stage}-component-archetypes-drift")
        for key in ("formation", "cadence", "complexity"):
            if str(got[key]) != str(want.get(key)):
                errors.append(f"stage{stage}-{key}-plan-mismatch:{got[key]}!={want.get(key)}")
        if got["pressure"].replace(" ", "") != str(want.get("pressure", "")).replace(" ", ""):
            errors.append(f"stage{stage}-pressure-plan-mismatch")

    # Stage24: two readable four-GRUNT cluster bursts, density pressure without new vocabulary.
    s24 = add_by.get(24, {}).get("spawns", [])
    if [x["type"] for x in s24] != ["GRUNT"] * 8:
        errors.append("stage24-not-eight-grunt-density")
    if [int(x["tMs"]) for x in s24] != [0, 150, 300, 450, 2800, 2950, 3100, 3250]:
        errors.append("stage24-burst-chronology-drift")
    if s24 and (max(float(x["y"]) for x in s24) - min(float(x["y"]) for x in s24) > 0.08):
        errors.append("stage24-cluster-y-span-too-wide")

    # Stage25: low-count scatter recovery for Lv21 reward attribution.
    s25 = add_by.get(25, {}).get("spawns", [])
    if [x["type"] for x in s25] != ["GRUNT"] * 4:
        errors.append("stage25-not-four-grunt-recovery")
    if [int(x["tMs"]) for x in s25] != [0, 1800, 3600, 5400]:
        errors.append("stage25-recovery-drip-drift")
    if s25 and (max(float(x["y"]) for x in s25) - min(float(x["y"]) for x in s25) < 0.40):
        errors.append("stage25-scatter-y-span-too-narrow")

    # Stage29: first bounded F08 three-type split-axis synthesis.
    s29 = add_by.get(29, {}).get("spawns", [])
    if Counter(x["type"] for x in s29) != Counter({"GRUNT": 3, "RUNNER": 3, "BRUTE": 3}):
        errors.append("stage29-not-balanced-grunt-runner-brute-synthesis")
    if [int(x["tMs"]) for x in s29] != [0, 450, 900, 2100, 2550, 3000, 4500, 4950, 5400]:
        errors.append("stage29-stagger-chronology-drift")
    y29 = [float(x["y"]) for x in s29]
    if not y29 or min(y29) > 0.32 or max(y29) < 0.68:
        errors.append("stage29-split-axis-separation-missing")
    if any(0.40 < y < 0.60 for y in y29):
        errors.append("stage29-mid-axis-clutter-present")

    # Stage30: lower-complexity two-type checkpoint after Stage29 synthesis.
    s30 = add_by.get(30, {}).get("spawns", [])
    if Counter(x["type"] for x in s30) != Counter({"GRUNT": 5, "BRUTE": 2}):
        errors.append("stage30-checkpoint-type-count-drift")
    if [int(x["tMs"]) for x in s30] != [0, 250, 500, 3300, 3550, 3800, 4050]:
        errors.append("stage30-wave-chronology-drift")
    if any(x["type"] == "RUNNER" for x in s30):
        errors.append("stage30-unintended-runner")

    # Stage31: simple repeated durable-front burst, intensity over complexity.
    s31 = add_by.get(31, {}).get("spawns", [])
    expected31 = ["BRUTE", "GRUNT", "GRUNT", "GRUNT", "BRUTE", "GRUNT", "GRUNT", "GRUNT"]
    if [x["type"] for x in s31] != expected31:
        errors.append("stage31-durable-front-burst-sequence-drift")
    if [int(x["tMs"]) for x in s31] != [0, 200, 400, 600, 3000, 3200, 3400, 3600]:
        errors.append("stage31-burst-chronology-drift")
    if not (s31 and s31[0]["type"] == "BRUTE" and len(s31) >= 5 and s31[4]["type"] == "BRUTE"):
        errors.append("stage31-durable-front-order-drift")

    static = {str(stage): stage_static(add_by[stage]) for stage in TARGETS if stage in add_by}
    for stage, stats in static.items():
        if stats["max4s"] > 8:
            errors.append(f"stage{stage}-max4s-exceeds-8")

    # Cross-stage semantic progression guards.
    if static.get("25", {}).get("authored", 99) >= static.get("24", {}).get("authored", 0):
        errors.append("stage25-not-lower-count-recovery-than-stage24")
    if static.get("25", {}).get("max4s", 99) >= static.get("24", {}).get("max4s", 0):
        errors.append("stage25-not-lower-density-recovery-than-stage24")
    if len({x["type"] for x in s29}) != 3 or len({x["type"] for x in s30}) != 2:
        errors.append("stage29-to-stage30-vocabulary-decompression-failed")
    if static.get("31", {}).get("max4s", 0) < static.get("30", {}).get("max4s", 0):
        errors.append("stage31-softwall-entry-not-intensity-rise-over-stage30")
    if len({float(x["y"]) for x in s31}) > 5:
        errors.append("stage31-geometry-too-complex-for-c1-entry")

    # Base representative recipe remains authoritative and must still satisfy its original fixed-set gate.
    base_static_errors = list(r.static_recipe_gate(base))
    errors.extend(f"base-runner-static:{e}" for e in base_static_errors)

    # Build an accumulated inspection artifact: base + unchanged A1 + unchanged A2 + A3.
    accumulated_additions = (
        copy.deepcopy(a1.get("stageAdditions", []))
        + copy.deepcopy(a2.get("stageAdditions", []))
        + copy.deepcopy(additions)
    )
    stage_ids = [int(x["stage"]) for x in accumulated_additions]
    if len(stage_ids) != len(set(stage_ids)):
        errors.append("wave-a1-a2-a3-duplicate-stage")

    materialized = copy.deepcopy(base)
    materialized["version"] = "t1-representative-transition-slice-recipes-v0.3-wave-a1-a2-a3-candidate"
    materialized["status"] = "BOUNDED_WAVE_A1_A2_A3_CANDIDATE_NO_ADOPTION_NO_PRODUCTION_OR_NUMERICAL_FREEZE"
    materialized["recipes"] = copy.deepcopy(base.get("recipes", [])) + accumulated_additions
    materialized["recipes"] = sorted(materialized["recipes"], key=lambda x: int(x["stage"]))
    mat_by = {int(x["stage"]): x for x in materialized["recipes"]}

    for stage, original in base_by.items():
        if mat_by.get(stage) != original:
            errors.append(f"existing-representative-stage{stage}-drift")
    for stage, original in a1_by.items():
        if mat_by.get(stage) != original:
            errors.append(f"a1-stage{stage}-drift")
    for stage, original in a2_by.items():
        if mat_by.get(stage) != original:
            errors.append(f"a2-stage{stage}-drift")

    materialized_path = Path(args.materialized_out)
    materialized_path.parent.mkdir(parents=True, exist_ok=True)
    materialized_path.write_text(
        yaml.safe_dump(materialized, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )

    result = {
        "version": "t1-wider-exact-authoring-wave-a3-static-preflight-v0.1",
        "status": "PASS" if not errors else "FAIL",
        "baseRecipeSha256": actual_base_sha,
        "wavePlanSha256": actual_plan_sha,
        "a1CandidateSha256": actual_a1_sha,
        "a2CandidateSha256": actual_a2_sha,
        "candidateSha256": r.sha256_bytes(candidate_path.read_bytes()),
        "materializedAccumulatedSha256": r.sha256_bytes(materialized_path.read_bytes()),
        "targetStages": TARGETS,
        "stageStatic": static,
        "existingRepresentativeStagesPreserved": not any(e.startswith("existing-representative-stage") for e in errors),
        "a1Preserved": not any(e.startswith("a1-stage") for e in errors),
        "a2Preserved": not any(e.startswith("a2-stage") for e in errors),
        "progressionGuard": "DENSITY_TO_LV21_BUFFER_TO_SPLIT_SYNTH_TO_CHECKPOINT_TO_DURABLE_SOFTWALL_ENTRY",
        "dynamicExecutionPerformed": False,
        "candidateAdopted": False,
        "productionGameplayChange": False,
        "numericalFreeze": False,
        "fullT1ExactRecipeFreeze": False,
        "warnings": warnings,
        "errors": errors,
    }
    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit("T1_WIDER_AUTHORING_WAVE_A3_STATIC_PREFLIGHT_FAIL")


if __name__ == "__main__":
    main()
