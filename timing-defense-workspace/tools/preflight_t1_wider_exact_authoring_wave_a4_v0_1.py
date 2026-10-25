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

TARGETS = [33, 37, 38]
CONTEXT = [39, 40]
ALLOWED_MONSTERS = {"GRUNT", "RUNNER", "BRUTE"}
ALLOWED_STAGE_KEYS = {
    "id", "stage", "archetype", "componentArchetypes", "formation",
    "formationSet", "cadence", "complexity", "pressureTags", "entryBaseX", "spawns",
}
ALLOWED_SPAWN_KEYS = {"tMs", "type", "y"}
A1_SHA = "44616732b4cbba8bc52df294d98e0ab485b400d7ec7e9b9bfdd9f3fe32d2910d"
A2_SHA = "2d3bf477e80617c0d26d2c349588caa446195b39c2581df0f11dd29eb1f37f8d"
A3_SHA = "30860f1ff0911ff121491e62a5fa2ede84b43c6e4ce9bd7ec5f0f8a68d9592e6"


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
    ap.add_argument("--a3", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--materialized-out", required=True)
    args = ap.parse_args()

    base_path = Path(args.base)
    plan_path = Path(args.plan)
    a1_path = Path(args.a1)
    a2_path = Path(args.a2)
    a3_path = Path(args.a3)
    candidate_path = Path(args.candidate)

    base = r.load_yaml(base_path)
    plan = r.load_yaml(plan_path)
    a1 = r.load_yaml(a1_path)
    a2 = r.load_yaml(a2_path)
    a3 = r.load_yaml(a3_path)
    candidate = r.load_yaml(candidate_path)

    errors: list[str] = []
    warnings: list[str] = []

    actual_base_sha = r.sha256_bytes(base_path.read_bytes())
    actual_plan_sha = r.sha256_bytes(plan_path.read_bytes())
    actual_a1_sha = r.sha256_bytes(a1_path.read_bytes())
    actual_a2_sha = r.sha256_bytes(a2_path.read_bytes())
    actual_a3_sha = r.sha256_bytes(a3_path.read_bytes())

    if candidate.get("baseRecipe", {}).get("sha256") != actual_base_sha:
        errors.append("base-recipe-sha-mismatch")
    if candidate.get("plan", {}).get("sha256") != actual_plan_sha:
        errors.append("wave-plan-sha-mismatch")
    if candidate.get("plan", {}).get("slice") != "WAVE_A4_PRE_GATE_PRESSURE_BRIDGE":
        errors.append("slice-id-mismatch")

    for key, actual, expected_sha in (
        ("a1", actual_a1_sha, A1_SHA),
        ("a2", actual_a2_sha, A2_SHA),
        ("a3", actual_a3_sha, A3_SHA),
    ):
        if actual != expected_sha:
            errors.append(f"{key}-prior-candidate-sha-drift")
        if candidate.get("priorCandidates", {}).get(key, {}).get("sha256") != actual:
            errors.append(f"{key}-candidate-reference-sha-drift")

    scope = candidate.get("scope", {})
    if scope.get("addedStages") != TARGETS:
        errors.append("scope-addedStages-not-33-37-38")
    if scope.get("contextOnlyStages") != CONTEXT:
        errors.append("scope-context-stages-not-39-40")
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
        errors.append("stageAdditions-not-exactly-33-37-38")
    add_by = {int(x["stage"]): x for x in additions if "stage" in x}

    base_by = {int(x["stage"]): x for x in base.get("recipes", [])}
    a1_by = {int(x["stage"]): x for x in a1.get("stageAdditions", [])}
    a2_by = {int(x["stage"]): x for x in a2.get("stageAdditions", [])}
    a3_by = {int(x["stage"]): x for x in a3.get("stageAdditions", [])}
    prior_stage_set = set(base_by) | set(a1_by) | set(a2_by) | set(a3_by)
    if set(TARGETS) & prior_stage_set:
        errors.append("a4-target-overlaps-existing-or-prior-candidate-stage")
    for stage in CONTEXT:
        if stage not in base_by:
            errors.append(f"context-stage{stage}-absent-from-base")

    expected = {int(k): v for k, v in plan.get("expectedSignatures", {}).items()}
    expected_components = {
        33: ["E01"],
        37: ["E02"],
        38: ["E01", "E03"],
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

    s33 = add_by.get(33, {}).get("spawns", [])
    if [x["type"] for x in s33] != ["GRUNT"] * 12:
        errors.append("stage33-not-twelve-grunt-density")
    if [int(x["tMs"]) for x in s33] != [0, 150, 300, 450, 2200, 2350, 2500, 2650, 5000, 5150, 5300, 5450]:
        errors.append("stage33-density-chronology-drift")
    if s33 and max(float(x["y"]) for x in s33) - min(float(x["y"]) for x in s33) > 0.08:
        errors.append("stage33-cluster-y-span-too-wide")

    s37 = add_by.get(37, {}).get("spawns", [])
    if Counter(x["type"] for x in s37) != Counter({"GRUNT": 4, "RUNNER": 4}):
        errors.append("stage37-not-balanced-grunt-runner-split")
    if [int(x["tMs"]) for x in s37] != [0, 180, 360, 540, 2600, 2780, 2960, 3140]:
        errors.append("stage37-burst-chronology-drift")
    y37 = [float(x["y"]) for x in s37]
    if not y37 or min(y37) > 0.32 or max(y37) < 0.68:
        errors.append("stage37-split-axis-separation-missing")
    if any(0.40 < y < 0.60 for y in y37):
        errors.append("stage37-mid-axis-clutter-present")
    if any(x["type"] == "BRUTE" for x in s37):
        errors.append("stage37-unintended-brute")

    s38 = add_by.get(38, {}).get("spawns", [])
    expected38_types = ["BRUTE", "GRUNT", "GRUNT", "GRUNT", "BRUTE", "GRUNT", "GRUNT", "GRUNT"]
    if [x["type"] for x in s38] != expected38_types:
        errors.append("stage38-durable-bridge-sequence-drift")
    if [int(x["tMs"]) for x in s38] != [0, 250, 500, 750, 3300, 3550, 3800, 4050]:
        errors.append("stage38-wave-chronology-drift")
    if any(x["type"] == "RUNNER" for x in s38):
        errors.append("stage38-unintended-runner")
    if s38 and max(float(x["y"]) for x in s38) - min(float(x["y"]) for x in s38) > 0.08:
        errors.append("stage38-durable-line-y-span-too-wide")

    static = {str(stage): stage_static(add_by[stage]) for stage in TARGETS if stage in add_by}
    for stage, stats in static.items():
        if stats["max4s"] > 8:
            errors.append(f"stage{stage}-max4s-exceeds-8")

    s24 = a3_by.get(24, {}).get("spawns", [])
    s29 = a3_by.get(29, {}).get("spawns", [])
    if len(s33) <= len(s24):
        errors.append("stage33-not-sustained-density-step-over-stage24")
    if static.get("33", {}).get("max4s") != 8:
        errors.append("stage33-density-should-hit-not-exceed-4s-cap")
    if len({x["type"] for x in s37}) >= len({x["type"] for x in s29}):
        errors.append("stage37-not-vocabulary-simpler-than-stage29-f08")
    if len(s37) >= len(s29):
        errors.append("stage37-not-count-bounded-below-stage29-f08")

    expected39 = [
        {"tMs": 0, "type": "BRUTE", "y": 0.38},
        {"tMs": 250, "type": "RUNNER", "y": 0.42},
        {"tMs": 500, "type": "RUNNER", "y": 0.40},
        {"tMs": 1500, "type": "BRUTE", "y": 0.54},
        {"tMs": 1750, "type": "RUNNER", "y": 0.58},
        {"tMs": 2000, "type": "RUNNER", "y": 0.56},
        {"tMs": 3200, "type": "RUNNER", "y": 0.40},
        {"tMs": 3450, "type": "BRUTE", "y": 0.44},
        {"tMs": 4100, "type": "RUNNER", "y": 0.42},
        {"tMs": 5200, "type": "RUNNER", "y": 0.56},
        {"tMs": 5450, "type": "BRUTE", "y": 0.60},
        {"tMs": 5700, "type": "RUNNER", "y": 0.58},
        {"tMs": 7600, "type": "BRUTE", "y": 0.38},
        {"tMs": 7850, "type": "RUNNER", "y": 0.54},
    ]
    expected40 = [
        {"tMs": 0, "type": "GRUNT", "y": 0.46},
        {"tMs": 200, "type": "RUNNER", "y": 0.44},
        {"tMs": 400, "type": "GRUNT", "y": 0.48},
        {"tMs": 1800, "type": "BRUTE", "y": 0.46},
        {"tMs": 2000, "type": "GRUNT", "y": 0.43},
        {"tMs": 2200, "type": "RUNNER", "y": 0.49},
        {"tMs": 4200, "type": "BRUTE", "y": 0.46},
        {"tMs": 4400, "type": "GRUNT", "y": 0.45},
        {"tMs": 4600, "type": "RUNNER", "y": 0.47},
        {"tMs": 7000, "type": "GRUNT", "y": 0.44},
        {"tMs": 7200, "type": "BRUTE", "y": 0.48},
    ]
    if base_by.get(39, {}).get("spawns") != expected39:
        errors.append("stage39-context-anchor-drift")
    if base_by.get(40, {}).get("spawns") != expected40:
        errors.append("stage40-context-anchor-drift")

    s39_static = stage_static(base_by[39]) if 39 in base_by else {}
    if static.get("38", {}).get("authored", 99) >= s39_static.get("authored", 0):
        errors.append("stage38-not-count-bounded-below-stage39-peak")
    if static.get("38", {}).get("max4s", 99) >= s39_static.get("max4s", 0):
        errors.append("stage38-not-density-bounded-below-stage39-peak")
    if len({x["type"] for x in s38}) >= len({x["type"] for x in expected39}):
        errors.append("stage38-not-vocabulary-bounded-below-stage39-peak")

    base_static_errors = list(r.static_recipe_gate(base))
    errors.extend(f"base-runner-static:{e}" for e in base_static_errors)

    accumulated_additions = (
        copy.deepcopy(a1.get("stageAdditions", []))
        + copy.deepcopy(a2.get("stageAdditions", []))
        + copy.deepcopy(a3.get("stageAdditions", []))
        + copy.deepcopy(additions)
    )
    stage_ids = [int(x["stage"]) for x in accumulated_additions]
    if len(stage_ids) != len(set(stage_ids)):
        errors.append("wave-a1-a2-a3-a4-duplicate-stage")

    materialized = copy.deepcopy(base)
    materialized["version"] = "t1-representative-transition-slice-recipes-v0.3-wave-a-complete-static-candidate"
    materialized["status"] = "BOUNDED_WAVE_A_COMPLETE_STATIC_CANDIDATE_NO_ADOPTION_NO_PRODUCTION_OR_NUMERICAL_FREEZE"
    materialized["recipes"] = copy.deepcopy(base.get("recipes", [])) + accumulated_additions
    materialized["recipes"] = sorted(materialized["recipes"], key=lambda x: int(x["stage"]))
    mat_by = {int(x["stage"]): x for x in materialized["recipes"]}

    for stage, original in base_by.items():
        if mat_by.get(stage) != original:
            errors.append(f"existing-representative-stage{stage}-drift")
    for label, prior in (("a1", a1_by), ("a2", a2_by), ("a3", a3_by)):
        for stage, original in prior.items():
            if mat_by.get(stage) != original:
                errors.append(f"{label}-stage{stage}-drift")
    for stage in CONTEXT:
        if mat_by.get(stage) != base_by.get(stage):
            errors.append(f"context-stage{stage}-changed-after-materialization")

    materialized_path = Path(args.materialized_out)
    materialized_path.parent.mkdir(parents=True, exist_ok=True)
    materialized_path.write_text(
        yaml.safe_dump(materialized, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )

    result = {
        "version": "t1-wider-exact-authoring-wave-a4-static-preflight-v0.1",
        "status": "PASS" if not errors else "FAIL",
        "baseRecipeSha256": actual_base_sha,
        "wavePlanSha256": actual_plan_sha,
        "priorCandidateSha256": {"a1": actual_a1_sha, "a2": actual_a2_sha, "a3": actual_a3_sha},
        "candidateSha256": r.sha256_bytes(candidate_path.read_bytes()),
        "materializedAccumulatedSha256": r.sha256_bytes(materialized_path.read_bytes()),
        "targetStages": TARGETS,
        "contextStages": CONTEXT,
        "stageStatic": static,
        "stage39Static": s39_static,
        "stage39RecipeDigest": r.sha256_obj(base_by[39]) if 39 in base_by else None,
        "stage40RecipeDigest": r.sha256_obj(base_by[40]) if 40 in base_by else None,
        "priorCandidatesPreserved": not any(
            e.startswith(("a1-stage", "a2-stage", "a3-stage")) for e in errors
        ),
        "existingRepresentativeStagesPreserved": not any(
            e.startswith("existing-representative-stage") for e in errors
        ),
        "contextAnchorsPreserved": not any(e.startswith("context-stage") for e in errors),
        "fullWaveAStaticMaterialized": not errors,
        "progressionGuard": "MAGE_DENSITY_TO_SPLIT_TEMPO_TO_DURABLE_BRIDGE_TO_STAGE39_PEAK_TO_STAGE40_GATE",
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
        raise SystemExit(1)


if __name__ == "__main__":
    main()
