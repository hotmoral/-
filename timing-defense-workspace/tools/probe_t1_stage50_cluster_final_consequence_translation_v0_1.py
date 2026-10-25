#!/usr/bin/env python3
"""Bounded Stage50 role-signal -> Stage-consequence chronology probe.

Stage49 remains exactly the admitted STAGGER1800 authoring candidate.
Stage50 keeps all five grammar templates and the same 5500ms phase anchors, but
moves DURABLE_CORE_3/STAGGER1800 CLUSTER to the final phase.

No scalar, metadata, Stage46-49, production, or authoring adoption change.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import admit_t1_stage49_50_stagger1800_authoring_candidate_dynamic_v0_1 as admit
import probe_t1_stage49_50_sustain_integration_compare_v0_1 as compare

r = compare.r
GAP = 5500
BASE_ORDER = {
    49: ["DURABLE_SCATTER", "FRONTLINE", "CLUSTER", "LINE"],
    50: ["DURABLE_SCATTER", "FRONTLINE", "CLUSTER", "LINE", "LINE_REPRISE"],
}
PROBE_ORDER = {
    49: ["DURABLE_SCATTER", "FRONTLINE", "CLUSTER", "LINE"],
    50: ["DURABLE_SCATTER", "FRONTLINE", "LINE", "LINE_REPRISE", "CLUSTER"],
}
BASE_WHOLE_WINDOW_MASTERY_DELTA = {
    "knight": 3.488,
    "rogue": 4.516,
    "tank": 10.912,
    "archer": 0.220,
    "mage": -0.472,
}
BASE_WALL = {"OFF": 1358.0, "ON": 164.0}


def split_templates(stage: dict, order: list[str]) -> dict[str, list[dict]]:
    out = {}
    for i, grammar in enumerate(order):
        start = i * GAP
        end = (i + 1) * GAP if i + 1 < len(order) else None
        rows = []
        for row in stage["spawns"]:
            t = int(row["tMs"])
            if t >= start and (end is None or t < end):
                rows.append({"offsetMs": t - start, "type": row["type"], "y": float(row["y"])})
        out[grammar] = rows
    return out


def build_probe(materialized: dict) -> dict:
    doc = copy.deepcopy(materialized)
    by = {int(x["stage"]): x for x in doc["recipes"]}
    templates = split_templates(by[50], BASE_ORDER[50])
    spawns = []
    for i, grammar in enumerate(PROBE_ORDER[50]):
        start = i * GAP
        for row in templates[grammar]:
            spawns.append({"tMs": start + int(row["offsetMs"]), "type": row["type"], "y": float(row["y"])})
    by[50]["spawns"] = sorted(spawns, key=lambda x: (x["tMs"], x["y"], x["type"]))
    doc["version"] = str(materialized.get("version")) + "+STAGE50_CLUSTER_FINAL_CONSEQUENCE_PROBE"
    doc["status"] = "EPHEMERAL_STAGE50_CLUSTER_FINAL_CONSEQUENCE_DIAGNOSTIC"
    return doc


def whole_window_delta(overall: dict, cls: str) -> float:
    return round(
        float(overall["OFF"]["byClass"][cls]["meanLateSettledSeconds"])
        - float(overall["ON"]["byClass"][cls]["meanLateSettledSeconds"]),
        6,
    )


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

    base = r.load_yaml(args.base)
    candidate = r.load_yaml(args.candidate)
    p3 = r.load_json(args.p3)
    p4 = r.load_json(args.p4d2_base)
    temporal = r.load_json(args.p4d2_temporal)
    seeds = tuple(int(x) for x in args.seeds.split(",") if x.strip())

    admitted = admit.materialize(base, candidate)
    probe = build_probe(admitted)
    admitted_by = {int(x["stage"]): x for x in admitted["recipes"]}
    probe_by = {int(x["stage"]): x for x in probe["recipes"]}

    errors = []
    # Scope isolation: only Stage50 spawns may differ.
    for stage in admitted_by:
        if stage == 50:
            if admit.staticp.stage_without_spawns(probe_by[stage]) != admit.staticp.stage_without_spawns(admitted_by[stage]):
                errors.append("stage50-metadata-drift")
        elif probe_by[stage] != admitted_by[stage]:
            errors.append(f"unexpected-stage-drift:{stage}")

    # Preserve exact grammar bodies; only phase placement changes.
    old_templates = split_templates(admitted_by[50], BASE_ORDER[50])
    new_templates = split_templates(probe_by[50], PROBE_ORDER[50])
    for grammar in BASE_ORDER[50]:
        if old_templates[grammar] != new_templates[grammar]:
            errors.append(f"grammar-template-drift:{grammar}")

    static_errors = list(r.static_recipe_gate(probe))
    errors.extend(f"runner-static:{e}" for e in static_errors)
    stage_static = {str(s): compare.shape.stage_static(probe_by[s]) for s in (49, 50)}
    if stage_static["49"]["max4s"] > 8 or stage_static["50"]["max4s"] > 8:
        errors.append("authored-4s-density-exceeds-8")

    overall = compare.magebridge.with_mage_lv31_fidelity(
        lambda: compare.widthbridge.with_archer_final_width(
            compare.WIDTH,
            lambda: compare.shape.execute_candidate(probe, p3, p4, temporal, seeds),
        )
    )
    fidelity = [f"overall:{e}" for e in overall["fidelityErrors"]]

    phase_rows, phase_agg, phase_fidelity = compare.magebridge.with_mage_lv31_fidelity(
        lambda: compare.widthbridge.with_archer_final_width(
            compare.WIDTH,
            lambda: compare.orderprobe.execute_target_phase(probe, p3, p4, temporal, seeds, PROBE_ORDER),
        )
    )
    fidelity.extend(f"phase:{e}" for e in phase_fidelity)
    errors.extend(f"fidelity:{e}" for e in fidelity)

    roles = {}
    whole = {}
    for cls in r.CLASSES:
        off = compare.orderprobe.role_stats(phase_agg, cls, "OFF")
        on = compare.orderprobe.role_stats(phase_agg, cls, "ON")
        delta = compare.orderprobe.role_delta(off, on)
        roles[cls] = {"OFF": off, "ON": on, "delta": delta}
        probe_delta = whole_window_delta(overall, cls)
        whole[cls] = {
            "baselineMasteryDeltaSeconds": BASE_WHOLE_WINDOW_MASTERY_DELTA[cls],
            "probeMasteryDeltaSeconds": probe_delta,
            "changeVsBaselineSeconds": round(probe_delta - BASE_WHOLE_WINDOW_MASTERY_DELTA[cls], 6),
            "OFFmeanLateSettledSeconds": overall["OFF"]["byClass"][cls]["meanLateSettledSeconds"],
            "ONmeanLateSettledSeconds": overall["ON"]["byClass"][cls]["meanLateSettledSeconds"],
            "OFFbacklineExposureSeconds": overall["OFF"]["byClass"][cls]["meanBacklineExposureSeconds"],
            "ONbacklineExposureSeconds": overall["ON"]["byClass"][cls]["meanBacklineExposureSeconds"],
        }

    out = {
        "version": "t1-stage50-cluster-final-consequence-translation-probe-v0.1",
        "status": "DIAGNOSTIC_EXECUTION_PASS" if not errors else "DIAGNOSTIC_EXECUTION_FAIL",
        "baseCandidateSha256": r.sha256_bytes(Path(args.candidate).read_bytes()),
        "baseOrder": {str(k): v for k, v in BASE_ORDER.items()},
        "probeOrder": {str(k): v for k, v in PROBE_ORDER.items()},
        "phaseAnchorsMs": [0, 5500, 11000, 16500, 22000],
        "stageStatic": stage_static,
        "stage49Unchanged": probe_by[49] == admitted_by[49],
        "stage50MetadataUnchanged": admit.staticp.stage_without_spawns(probe_by[50]) == admit.staticp.stage_without_spawns(admitted_by[50]),
        "grammarTemplatesUnchanged": all(old_templates[g] == new_templates[g] for g in BASE_ORDER[50]),
        "seeds": list(seeds),
        "fidelityErrors": fidelity,
        "roles": roles,
        "wholeWindow": whole,
        "wall": {
            "baseline": BASE_WALL,
            "probe": {"OFF": overall["OFF"]["totalWallDamage"], "ON": overall["ON"]["totalWallDamage"]},
            "classesWithWallPressure": {
                "OFF": overall["OFF"]["classesWithWallPressure"],
                "ON": overall["ON"]["classesWithWallPressure"],
            },
        },
        "failOrIncomplete": {"OFF": overall["OFF"]["failOrIncompleteCases"], "ON": overall["ON"]["failOrIncompleteCases"]},
        "archerWidthBridge": {"yTolerance": compare.WIDTH, "status": "DIAGNOSTIC_ONLY_NOT_FROZEN"},
        "mageLv31FidelityBridge": compare.magebridge.BRIDGE_METADATA,
        "productionGameplayChange": False,
        "authoringAdopted": False,
        "numericalFreeze": False,
        "errors": errors,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    if errors:
        raise SystemExit("T1_STAGE50_CLUSTER_FINAL_CONSEQUENCE_PROBE_FIDELITY_FAIL")


if __name__ == "__main__":
    main()
