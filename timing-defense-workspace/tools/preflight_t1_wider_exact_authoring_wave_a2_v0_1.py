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

TARGETS = [15, 19]
CONTEXT = [18, 20]
ALLOWED_MONSTERS = {"GRUNT", "RUNNER", "BRUTE"}
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


def parse_plan_archetype(signature: str) -> str:
    # "E03+E02 / B+R" -> "E03+E02"
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
    if candidate.get("plan", {}).get("slice") != "WAVE_A2_BRUTE_TEACH_TO_FIRST_REORDER_BRIDGE":
        errors.append("slice-id-mismatch")

    scope = candidate.get("scope", {})
    if scope.get("addedStages") != TARGETS:
        errors.append("scope-addedStages-not-15-19")
    if scope.get("contextOnlyStages") != CONTEXT:
        errors.append("scope-context-stages-not-18-20")
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
        errors.append("stageAdditions-not-exactly-15-19")
    add_by = {int(x["stage"]): x for x in additions if "stage" in x}

    base_by = {int(x["stage"]): x for x in base.get("recipes", [])}
    if set(TARGETS) & set(base_by):
        errors.append("a2-target-overlaps-existing-representative-stage")
    for stage in CONTEXT:
        if stage not in base_by:
            errors.append(f"context-stage{stage}-absent-from-base")

    # Pin the two context anchors semantically in addition to the base SHA.
    expected_stage18 = [
        {"tMs": 0, "type": "BRUTE", "y": 0.46},
        {"tMs": 250, "type": "GRUNT", "y": 0.43},
        {"tMs": 500, "type": "GRUNT", "y": 0.49},
        {"tMs": 2400, "type": "BRUTE", "y": 0.46},
        {"tMs": 2650, "type": "GRUNT", "y": 0.44},
        {"tMs": 2900, "type": "GRUNT", "y": 0.48},
    ]
    expected_stage20 = [
        {"tMs": 0, "type": "GRUNT", "y": 0.46},
        {"tMs": 250, "type": "GRUNT", "y": 0.44},
        {"tMs": 500, "type": "RUNNER", "y": 0.48},
        {"tMs": 2200, "type": "BRUTE", "y": 0.46},
        {"tMs": 2450, "type": "GRUNT", "y": 0.42},
        {"tMs": 2700, "type": "RUNNER", "y": 0.50},
        {"tMs": 4700, "type": "GRUNT", "y": 0.45},
        {"tMs": 4950, "type": "BRUTE", "y": 0.47},
        {"tMs": 5200, "type": "RUNNER", "y": 0.43},
        {"tMs": 7600, "type": "GRUNT", "y": 0.49},
    ]
    if base_by.get(18, {}).get("spawns") != expected_stage18:
        errors.append("stage18-context-anchor-drift")
    if base_by.get(20, {}).get("spawns") != expected_stage20:
        errors.append("stage20-context-anchor-drift")

    expected = {int(k): v for k, v in plan.get("expectedSignatures", {}).items()}
    expected_components = {15: ["E03"], 19: ["E03", "E02"]}
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

    # Candidate-specific pedagogic morphology.
    s15 = add_by.get(15, {}).get("spawns", [])
    if [x["type"] for x in s15] != ["BRUTE"] * 3:
        errors.append("stage15-not-three-brute-pure-teach")
    if [int(x["tMs"]) for x in s15] != [0, 2200, 4400]:
        errors.append("stage15-not-readable-slow-drip")
    if len({float(x["y"]) for x in s15}) != 1:
        errors.append("stage15-line-light-y-drift")

    s19 = add_by.get(19, {}).get("spawns", [])
    expected_s19_types = ["BRUTE", "RUNNER", "RUNNER", "BRUTE", "RUNNER", "RUNNER"]
    expected_s19_times = [0, 650, 1300, 3000, 3650, 4300]
    if [x["type"] for x in s19] != expected_s19_types:
        errors.append("stage19-brute-runner-stagger-sequence-drift")
    if [int(x["tMs"]) for x in s19] != expected_s19_times:
        errors.append("stage19-stagger-chronology-drift")
    if {str(x["type"]) for x in s19} != {"BRUTE", "RUNNER"}:
        errors.append("stage19-not-exact-brute-runner-mix")
    if any(str(x["type"]) == "GRUNT" for x in s19):
        errors.append("stage19-unintended-grunt-leak")
    # Each packet must start with the durable front before the runners.
    if not (s19 and s19[0]["type"] == "BRUTE" and len(s19) >= 4 and s19[3]["type"] == "BRUTE"):
        errors.append("stage19-durable-front-packet-order-drift")

    static = {str(stage): stage_static(add_by[stage]) for stage in TARGETS if stage in add_by}
    for stage, stats in static.items():
        if stats["max4s"] > 8:
            errors.append(f"stage{stage}-max4s-exceeds-8")

    # Structural progression guards versus the exact context anchors.
    if len(s15) >= len(expected_stage18):
        errors.append("stage15-teach-not-simpler-than-stage18-first-mix")
    if len({x["type"] for x in s15}) != 1:
        errors.append("stage15-teach-has-mixed-vocabulary")
    if len(s19) >= len(expected_stage20):
        errors.append("stage19-reorder-not-bounded-below-stage20-synthesis")
    if len({x["type"] for x in s19}) != 2:
        errors.append("stage19-reorder-vocabulary-not-exactly-two-types")
    if len({x["type"] for x in expected_stage20}) != 3:
        errors.append("stage20-context-no-longer-three-type-synthesis")

    # Base representative recipe must still pass its original fixed-set static gate.
    base_static_errors = list(r.static_recipe_gate(base))
    errors.extend(f"base-runner-static:{e}" for e in base_static_errors)

    # Exact inspection artifact: add only A2 and preserve all existing recipe objects byte-semantically as parsed objects.
    materialized = copy.deepcopy(base)
    materialized["version"] = "t1-representative-transition-slice-recipes-v0.3-wave-a2-candidate"
    materialized["status"] = "BOUNDED_WAVE_A2_CANDIDATE_NO_ADOPTION_NO_PRODUCTION_OR_NUMERICAL_FREEZE"
    materialized["recipes"] = copy.deepcopy(base.get("recipes", [])) + copy.deepcopy(additions)
    materialized["recipes"] = sorted(materialized["recipes"], key=lambda x: int(x["stage"]))
    mat_by = {int(x["stage"]): x for x in materialized["recipes"]}

    for stage, original in base_by.items():
        if mat_by.get(stage) != original:
            errors.append(f"existing-representative-stage{stage}-drift")
    for stage in CONTEXT:
        if mat_by.get(stage) != base_by.get(stage):
            errors.append(f"context-stage{stage}-changed-after-materialization")

    materialized_path = Path(args.materialized_out)
    materialized_path.parent.mkdir(parents=True, exist_ok=True)
    materialized_path.write_text(
        yaml.safe_dump(materialized, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )

    result = {
        "version": "t1-wider-exact-authoring-wave-a2-static-preflight-v0.1",
        "status": "PASS" if not errors else "FAIL",
        "baseRecipeSha256": actual_base_sha,
        "wavePlanSha256": actual_plan_sha,
        "candidateSha256": r.sha256_bytes(candidate_path.read_bytes()),
        "materializedSha256": r.sha256_bytes(materialized_path.read_bytes()),
        "targetStages": TARGETS,
        "contextStages": CONTEXT,
        "contextStage18RecipeDigest": r.sha256_obj(base_by[18]) if 18 in base_by else None,
        "contextStage20RecipeDigest": r.sha256_obj(base_by[20]) if 20 in base_by else None,
        "stageStatic": static,
        "existingRepresentativeStagesPreserved": not any(
            e.startswith("existing-representative-stage") for e in errors
        ),
        "contextAnchorsPreserved": not any(e.startswith("context-stage") and "changed" in e for e in errors),
        "progressionGuard": "PURE_B_TEACH_TO_GB_MIX_TO_BR_STAGGER_TO_GRB_SYNTH",
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
        raise SystemExit("T1_WIDER_AUTHORING_WAVE_A2_STATIC_PREFLIGHT_FAIL")


if __name__ == "__main__":
    main()
