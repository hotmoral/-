#!/usr/bin/env python3
"""Static preflight for the bounded T1 Stage49-50 STAGGER_1800 authoring candidate.

This tool materializes the Stage49/50 overlay on top of the exact v0.2 recipe,
then checks source identity, scope isolation, skeleton metadata preservation,
monster vocabulary, right-edge entry, density, geometry, grammar chronology,
and explicit non-production/non-freeze guards.

No dynamic combat simulation or gameplay adoption occurs here.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import yaml

import run_t1_transition_slice_microsim_settlement_fix_v0_1 as settlement_bridge

r = settlement_bridge.runner

ALLOWED_STAGE_KEYS = {
    "id", "stage", "archetype", "componentArchetypes", "formation",
    "formationSet", "cadence", "complexity", "pressureTags", "entryBaseX",
    "grammarOrder", "spawns",
}
ALLOWED_SPAWN_KEYS = {"tMs", "type", "y"}
ALLOWED_MONSTERS = {"GRUNT", "RUNNER", "BRUTE"}
PHASE_GAP_MS = 5500

EXPECTED_ORDER = {
    49: ["DURABLE_SCATTER", "FRONTLINE", "CLUSTER", "LINE"],
    50: ["DURABLE_SCATTER", "FRONTLINE", "CLUSTER", "LINE", "LINE_REPRISE"],
}
EXPECTED_PHASE_STARTS = {
    49: [0, 5500, 11000, 16500],
    50: [0, 5500, 11000, 16500, 22000],
}
EXPECTED_STAGE49_CLUSTER = [
    {"tMs": 11000, "type": "GRUNT", "y": 0.42},
    {"tMs": 11120, "type": "RUNNER", "y": 0.46},
    {"tMs": 11240, "type": "GRUNT", "y": 0.50},
    {"tMs": 11360, "type": "RUNNER", "y": 0.44},
    {"tMs": 11480, "type": "BRUTE", "y": 0.48},
    {"tMs": 11600, "type": "GRUNT", "y": 0.43},
]
EXPECTED_STAGE50_CLUSTER = [
    {"tMs": 11000, "type": "BRUTE", "y": 0.46},
    {"tMs": 11360, "type": "GRUNT", "y": 0.44},
    {"tMs": 11720, "type": "BRUTE", "y": 0.50},
    {"tMs": 12080, "type": "GRUNT", "y": 0.48},
    {"tMs": 12440, "type": "BRUTE", "y": 0.42},
    {"tMs": 12800, "type": "GRUNT", "y": 0.46},
]


def max_density(spawns: list[dict], window_ms: int) -> int:
    times = [int(x["tMs"]) for x in spawns]
    if not times:
        return 0
    return max(sum(1 for other in times if start <= other < start + window_ms) for start in times)


def stage_static(stage: dict) -> dict:
    ys = [float(x["y"]) for x in stage["spawns"]]
    return {
        "authored": len(stage["spawns"]),
        "max4s": max_density(stage["spawns"], 4000),
        "max6s": max_density(stage["spawns"], 6000),
        "minY": min(ys),
        "maxY": max(ys),
        "ySpread": round(max(ys) - min(ys), 6),
        "lastSpawnMs": max(int(x["tMs"]) for x in stage["spawns"]),
    }


def stage_without_spawns(stage: dict) -> dict:
    return {k: copy.deepcopy(v) for k, v in stage.items() if k != "spawns"}


def materializable_override(raw: dict) -> dict:
    return {k: copy.deepcopy(v) for k, v in raw.items() if k != "grammarOrder"}


def phase_rows(stage: dict, start_ms: int, end_ms: int | None) -> list[dict]:
    return [
        {"tMs": int(row["tMs"]), "type": str(row["type"]), "y": float(row["y"])}
        for row in stage["spawns"]
        if int(row["tMs"]) >= start_ms and (end_ms is None or int(row["tMs"]) < end_ms)
    ]


def check_overlay_shape(candidate: dict, errors: list[str]) -> dict[int, dict]:
    if candidate.get("status") != "DIAGNOSTIC_AUTHORING_CANDIDATE_NO_PRODUCTION_OR_NUMERICAL_FREEZE":
        errors.append("candidate-status-not-explicitly-nonproduction")
    scope = candidate.get("scope", {})
    if scope.get("overriddenStages") != [49, 50]:
        errors.append("scope-overriddenStages-not-49-50-only")
    if scope.get("productionGameplayChange") is not False:
        errors.append("productionGameplayChange-not-false")
    if scope.get("fullT1ExactRecipeFreeze") is not False:
        errors.append("fullT1ExactRecipeFreeze-not-false")
    for flag in ("monsterScalarChange", "classScalarChange", "shopExpChange", "pxpProbabilityChange"):
        if scope.get(flag) is not False:
            errors.append(f"{flag}-not-false")
    if int(scope.get("phaseGapMs", -1)) != PHASE_GAP_MS:
        errors.append("phase-gap-not-5500")
    if scope.get("diagnosticCenter") != "STAGGER_1800_STAGE50_CLUSTER_ONLY":
        errors.append("diagnostic-center-id-mismatch")

    overrides = candidate.get("stageOverrides", [])
    if [int(x.get("stage", -1)) for x in overrides] != [49, 50]:
        errors.append("stageOverrides-not-exactly-49-50")
    by = {int(x["stage"]): x for x in overrides if "stage" in x}
    for stage, raw in by.items():
        extra = set(raw) - ALLOWED_STAGE_KEYS
        if extra:
            errors.append(f"stage{stage}-unexpected-keys:{sorted(extra)}")
        for i, spawn in enumerate(raw.get("spawns", [])):
            extra_spawn = set(spawn) - ALLOWED_SPAWN_KEYS
            if extra_spawn:
                errors.append(f"stage{stage}-spawn{i}-unexpected-keys:{sorted(extra_spawn)}")
            if str(spawn.get("type")) not in ALLOWED_MONSTERS:
                errors.append(f"stage{stage}-spawn{i}-illegal-monster:{spawn.get('type')}")
    return by


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--materialized-out", required=True)
    args = ap.parse_args()

    base_path = Path(args.base)
    candidate_path = Path(args.candidate)
    base = r.load_yaml(base_path)
    candidate = r.load_yaml(candidate_path)

    errors: list[str] = []
    warnings: list[str] = []

    actual_base_sha = r.sha256_bytes(base_path.read_bytes())
    declared_base_sha = str(candidate.get("baseRecipe", {}).get("sha256", ""))
    declared_base_path = str(candidate.get("baseRecipe", {}).get("path", ""))
    if actual_base_sha != declared_base_sha:
        errors.append(f"base-sha-mismatch:{declared_base_sha}!={actual_base_sha}")
    if declared_base_path != "data/t1_representative_transition_slice_recipes_v0_2_pressure_shape_candidate.yaml":
        errors.append("base-path-mismatch")

    override_by = check_overlay_shape(candidate, errors)
    base_by = {int(x["stage"]): x for x in base["recipes"]}

    materialized = copy.deepcopy(base)
    materialized["version"] = "t1-representative-transition-slice-recipes-v0.3-stage49-50-stagger1800-authoring-candidate"
    materialized["status"] = "BOUNDED_STAGE49_50_AUTHORING_CANDIDATE_NO_PRODUCTION_OR_NUMERICAL_FREEZE"
    mat_by = {int(x["stage"]): x for x in materialized["recipes"]}

    for stage in (49, 50):
        if stage not in override_by:
            errors.append(f"missing-stage{stage}-override")
            continue
        mat_by[stage].clear()
        mat_by[stage].update(materializable_override(override_by[stage]))

    # Scope isolation: no recipe object outside Stage49/50 may drift.
    for stage, base_stage in base_by.items():
        if stage not in (49, 50) and mat_by[stage] != base_stage:
            errors.append(f"scope-drift-stage{stage}")
    for stage in (5, 18, 41):
        if mat_by[stage] != base_by[stage]:
            errors.append(f"preserved-stage{stage}-changed")

    # Skeleton/v0.2 metadata is deliberately preserved; only spawns may change.
    for stage in (49, 50):
        if stage_without_spawns(mat_by[stage]) != stage_without_spawns(base_by[stage]):
            errors.append(f"stage{stage}-metadata-drift-from-v02")

    # Canonical complexity/signature guard.
    if mat_by[49].get("complexity") != "C2" or mat_by[50].get("complexity") != "C3":
        errors.append("stage49-50-complexity-drift")
    if mat_by[49].get("formation") != "F08" or mat_by[49].get("cadence") != "CD05":
        errors.append("stage49-skeleton-formation-cadence-drift")
    if mat_by[49].get("pressureTags") != ["RUSH", "BULWARK"]:
        errors.append("stage49-skeleton-pressure-tag-drift")
    if mat_by[50].get("cadence") != "CD03" or mat_by[50].get("pressureTags") != ["BASELINE"]:
        errors.append("stage50-skeleton-cadence-pressure-tag-drift")

    # Right-edge and vocabulary guards.
    for stage in (49, 50):
        if float(mat_by[stage].get("entryBaseX", -1)) != 0.92:
            errors.append(f"stage{stage}-entryBaseX-not-0.92")
        illegal = sorted({str(x["type"]) for x in mat_by[stage]["spawns"]} - ALLOWED_MONSTERS)
        if illegal:
            errors.append(f"stage{stage}-illegal-monsters:{illegal}")

    # Chronology / grammar identity.
    for stage in (49, 50):
        if override_by[stage].get("grammarOrder") != EXPECTED_ORDER[stage]:
            errors.append(f"stage{stage}-grammar-order-mismatch")
        starts = EXPECTED_PHASE_STARTS[stage]
        for i, start in enumerate(starts):
            end = starts[i + 1] if i + 1 < len(starts) else None
            rows = phase_rows(mat_by[stage], start, end)
            if len(rows) != 6:
                errors.append(f"stage{stage}-phase{i}-expected6-got{len(rows)}")

    s49_cluster = phase_rows(mat_by[49], 11000, 16500)
    s50_cluster = phase_rows(mat_by[50], 11000, 16500)
    if s49_cluster != EXPECTED_STAGE49_CLUSTER:
        errors.append("stage49-cluster-not-distinct-burst")
    if s50_cluster != EXPECTED_STAGE50_CLUSTER:
        errors.append("stage50-cluster-not-durable-core3-stagger1800")

    static = {str(stage): stage_static(mat_by[stage]) for stage in (49, 50)}
    if static["49"]["authored"] != 24:
        errors.append("stage49-authored-count-not-24")
    if static["50"]["authored"] != 30:
        errors.append("stage50-authored-count-not-30")
    for stage in (49, 50):
        if static[str(stage)]["max4s"] > 8:
            errors.append(f"stage{stage}-max4s-exceeds-8")
        if static[str(stage)]["minY"] != 0.18 or static[str(stage)]["maxY"] != 0.82:
            errors.append(f"stage{stage}-y-envelope-drift")

    runner_static_errors = list(r.static_recipe_gate(materialized))
    errors.extend(f"runner-static:{e}" for e in runner_static_errors)

    # Materialized artifact is for exact-source inspection only.
    materialized_path = Path(args.materialized_out)
    materialized_path.parent.mkdir(parents=True, exist_ok=True)
    materialized_path.write_text(yaml.safe_dump(materialized, sort_keys=False, allow_unicode=True), encoding="utf-8")

    out = {
        "version": "t1-stage49-50-stagger1800-authoring-static-preflight-v0.1",
        "status": "PASS" if not errors else "FAIL",
        "baseRecipe": str(base_path),
        "baseRecipeSha256": actual_base_sha,
        "candidate": str(candidate_path),
        "candidateSha256": r.sha256_bytes(candidate_path.read_bytes()),
        "materializedSha256": r.sha256_bytes(materialized_path.read_bytes()),
        "scope": {"overriddenStages": [49, 50], "preservedStages": [5, 18, 41]},
        "stageStatic": static,
        "stage49ClusterMode": "DISTINCT_GRAMMAR_BURST_0600",
        "stage50ClusterMode": "DURABLE_CORE_3_STAGGER_1800",
        "phaseGapMs": PHASE_GAP_MS,
        "metadataPreservedFromV02": True,
        "productionGameplayChange": False,
        "numericalFreeze": False,
        "fullT1ExactRecipeFreeze": False,
        "warnings": warnings,
        "errors": errors,
    }
    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(out, indent=2, sort_keys=True))
    if errors:
        raise SystemExit("T1_STAGE49_50_STAGGER1800_STATIC_PREFLIGHT_FAIL")


if __name__ == "__main__":
    main()
