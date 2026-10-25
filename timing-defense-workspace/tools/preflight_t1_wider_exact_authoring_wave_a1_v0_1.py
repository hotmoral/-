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

TARGETS = [1, 4, 8]
ALLOWED_MONSTERS = {"GRUNT", "RUNNER"}
ALLOWED_STAGE_KEYS = {
    "id", "stage", "archetype", "componentArchetypes", "formation",
    "formationSet", "cadence", "complexity", "pressureTags", "entryBaseX", "spawns",
}
ALLOWED_SPAWN_KEYS = {"tMs", "type", "y"}


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
        "intervalsMs": [b - a for a, b in zip(times, times[1:])],
    }


def metadata(stage: dict) -> dict:
    return {
        "archetype": stage.get("archetype"),
        "formation": stage.get("formation"),
        "cadence": stage.get("cadence"),
        "complexity": stage.get("complexity"),
        "pressure": ",".join(stage.get("pressureTags", [])),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--materialized-out", required=True)
    args = ap.parse_args()

    base_path = Path(args.base)
    plan_path = Path(args.plan)
    candidate_path = Path(args.candidate)
    base = r.load_yaml(base_path)
    plan = r.load_yaml(plan_path)
    candidate = r.load_yaml(candidate_path)

    errors: list[str] = []
    warnings: list[str] = []

    actual_base_sha = r.sha256_bytes(base_path.read_bytes())
    actual_plan_sha = r.sha256_bytes(plan_path.read_bytes())
    if candidate.get("baseRecipe", {}).get("sha256") != actual_base_sha:
        errors.append("base-recipe-sha-mismatch")
    if candidate.get("plan", {}).get("sha256") != actual_plan_sha:
        errors.append("wave-plan-sha-mismatch")
    if candidate.get("plan", {}).get("slice") != "WAVE_A1_ONBOARDING_TO_FIRST_MIX_BRIDGE":
        errors.append("slice-id-mismatch")

    scope = candidate.get("scope", {})
    if scope.get("addedStages") != TARGETS:
        errors.append("scope-addedStages-not-1-4-8")
    if scope.get("contextOnlyStages") != [5]:
        errors.append("scope-context-stage5-missing")
    if scope.get("allowedMonsters") != ["GRUNT", "RUNNER"]:
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
        errors.append("stageAdditions-not-exactly-1-4-8")
    add_by = {int(x["stage"]): x for x in additions if "stage" in x}

    base_by = {int(x["stage"]): x for x in base.get("recipes", [])}
    if set(TARGETS) & set(base_by):
        errors.append("a1-target-overlaps-existing-representative-stage")
    if 5 not in base_by:
        errors.append("stage5-context-anchor-absent-from-base")

    expected_stage5 = [
        {"tMs": 0, "type": "RUNNER", "y": 0.46},
        {"tMs": 1300, "type": "RUNNER", "y": 0.45},
        {"tMs": 2600, "type": "RUNNER", "y": 0.47},
        {"tMs": 3900, "type": "RUNNER", "y": 0.46},
    ]
    if base_by.get(5, {}).get("spawns") != expected_stage5:
        errors.append("stage5-context-anchor-drift")

    expected = {int(k): v for k, v in plan.get("expectedSignatures", {}).items()}
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
        for key in ("archetype", "formation", "cadence", "complexity"):
            if str(got[key]) != str(want.get(key)):
                errors.append(f"stage{stage}-{key}-plan-mismatch:{got[key]}!={want.get(key)}")
        if got["pressure"].replace(" ", "") != str(want.get("pressure", "")).replace(" ", ""):
            errors.append(f"stage{stage}-pressure-plan-mismatch")

    # Candidate-specific pedagogic morphology.
    if [x["type"] for x in add_by.get(1, {}).get("spawns", [])] != ["GRUNT"] * 4:
        errors.append("stage1-not-four-grunt-pure-baseline")
    if [int(x["tMs"]) for x in add_by.get(1, {}).get("spawns", [])] != [0, 1600, 3200, 4800]:
        errors.append("stage1-not-slow-drip-1600")

    if [x["type"] for x in add_by.get(4, {}).get("spawns", [])] != ["GRUNT"] * 6:
        errors.append("stage4-not-six-grunt-pure-baseline")
    if [int(x["tMs"]) for x in add_by.get(4, {}).get("spawns", [])] != [0, 250, 500, 2800, 3050, 3300]:
        errors.append("stage4-not-two-readable-three-unit-waves")

    s8 = add_by.get(8, {}).get("spawns", [])
    if [x["type"] for x in s8] != ["GRUNT", "RUNNER", "GRUNT", "RUNNER", "GRUNT", "RUNNER", "RUNNER"]:
        errors.append("stage8-mix-sequence-drift")
    if [int(x["tMs"]) for x in s8] != [0, 250, 1700, 1950, 3400, 3650, 5100]:
        errors.append("stage8-wave-chronology-drift")
    if not ({"GRUNT", "RUNNER"} <= {str(x["type"]) for x in s8}):
        errors.append("stage8-not-actual-grunt-runner-mix")

    static = {str(stage): stage_static(add_by[stage]) for stage in TARGETS if stage in add_by}
    for stage, stats in static.items():
        if stats["max4s"] > 8:
            errors.append(f"stage{stage}-max4s-exceeds-8")

    # Build an exact inspection artifact while preserving every existing representative recipe object.
    materialized = copy.deepcopy(base)
    materialized["version"] = "t1-representative-transition-slice-recipes-v0.3-wave-a1-candidate"
    materialized["status"] = "BOUNDED_WAVE_A1_CANDIDATE_NO_ADOPTION_NO_PRODUCTION_OR_NUMERICAL_FREEZE"
    materialized["recipes"] = copy.deepcopy(base.get("recipes", [])) + copy.deepcopy(additions)
    materialized["recipes"] = sorted(materialized["recipes"], key=lambda x: int(x["stage"]))
    mat_by = {int(x["stage"]): x for x in materialized["recipes"]}

    for stage, original in base_by.items():
        if mat_by.get(stage) != original:
            errors.append(f"existing-representative-stage{stage}-drift")
    if mat_by.get(5) != base_by.get(5):
        errors.append("stage5-context-anchor-changed-after-materialization")

    runner_static_errors = list(r.static_recipe_gate(materialized))
    errors.extend(f"runner-static:{e}" for e in runner_static_errors)

    materialized_path = Path(args.materialized_out)
    materialized_path.parent.mkdir(parents=True, exist_ok=True)
    materialized_path.write_text(
        yaml.safe_dump(materialized, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )

    result = {
        "version": "t1-wider-exact-authoring-wave-a1-static-preflight-v0.1",
        "status": "PASS" if not errors else "FAIL",
        "baseRecipeSha256": actual_base_sha,
        "wavePlanSha256": actual_plan_sha,
        "candidateSha256": r.sha256_bytes(candidate_path.read_bytes()),
        "materializedSha256": r.sha256_bytes(materialized_path.read_bytes()),
        "targetStages": TARGETS,
        "contextStage5RecipeDigest": r.sha256_obj(base_by[5]) if 5 in base_by else None,
        "stageStatic": static,
        "existingRepresentativeStagesPreserved": not any(
            e.startswith("existing-representative-stage") for e in errors
        ),
        "stage5ContextPreserved": "stage5-context-anchor-changed-after-materialization" not in errors,
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
        raise SystemExit("T1_WIDER_AUTHORING_WAVE_A1_STATIC_PREFLIGHT_FAIL")


if __name__ == "__main__":
    main()
