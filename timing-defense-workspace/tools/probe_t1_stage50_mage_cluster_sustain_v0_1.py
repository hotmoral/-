#!/usr/bin/env python3
"""T1 Stage50 Mage CLUSTER sustain chronology probe v0.1.

Question
--------
Can Stage50 preserve a real Mage Lv31 multi-target opportunity across the
observed persistent-state P×P phase drift without changing any class/monster
scalar or resetting run-local state?

Frozen/isolation boundaries
---------------------------
- use transition-aware v0.2 grammar order exactly;
- use DURABLE_CORE_3 body types/y positions exactly;
- vary only the six Stage50 CLUSTER spawn offsets;
- preserve Stage49 and every non-CLUSTER Stage50 spawn exactly;
- preserve combo/charge/RNG continuity and frontmost targeting;
- Mage Lv31 approved-contract fidelity bridge remains active;
- no production gameplay or numerical freeze.

Candidates
----------
BURST_0600   = [0,120,240,360,480,600]
STAGGER_1800 = [0,360,720,1080,1440,1800]
SUSTAIN_3000 = [0,600,1200,1800,2400,3000]
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import probe_t1_stage49_50_transition_aware_integration_v0_1 as integration
import probe_t1_stage49_50_transition_aware_integration_v0_2 as integration_v02
import probe_t1_stage49_50_target_phase_clearance_v0_1 as target
import probe_t1_stage49_50_pxp_phase_alignment_v0_1 as alignment
import t1_transition_microsim_mage_lv31_fidelity_bridge_v0_1 as magebridge

r = integration.r
ORDER = integration_v02.ORDER_V02
GAP_MS = integration.GAP_MS
OFF = integration.OFF
ON = integration.ON
OFFSETS = {
    "BURST_0600": [0, 120, 240, 360, 480, 600],
    "STAGGER_1800": [0, 360, 720, 1080, 1440, 1800],
    "SUSTAIN_3000": [0, 600, 1200, 1800, 2400, 3000],
}


def build_base(source: dict) -> dict:
    old = integration.ORDER
    try:
        integration.ORDER = ORDER
        return integration.build_candidate(source, "DURABLE_CORE_3")
    finally:
        integration.ORDER = old


def build_candidate(source: dict, cid: str) -> dict:
    doc = build_base(source)
    by = {int(x["stage"]): x for x in doc["recipes"]}
    recipe = by[50]
    cluster_index = ORDER[50].index("CLUSTER")
    phase_start = cluster_index * GAP_MS
    cluster_rows = [
        row for row in recipe["spawns"]
        if target.distinct.phase_for_ms(int(row["tMs"]), GAP_MS, ORDER[50]) == "CLUSTER"
    ]
    cluster_rows.sort(key=lambda row: int(row["tMs"]))
    if len(cluster_rows) != 6:
        raise r.RunnerFidelityError(f"expected six Stage50 CLUSTER rows, got {len(cluster_rows)}")
    # Types/y remain exact DURABLE_CORE_3. Only chronology changes.
    for row, offset in zip(cluster_rows, OFFSETS[cid]):
        row["tMs"] = phase_start + offset
    doc["version"] = f"{doc['version']}+MAGE_CLUSTER_SUSTAIN_{cid}"
    doc["status"] = "EPHEMERAL_MAGE_CLUSTER_SUSTAIN_DIAGNOSTIC_NOT_AUTHORING"
    return doc


def run_side(runtime, by, seed: int, active: list[int]):
    case = magebridge.with_mage_lv31_fidelity(
        lambda: target.execute_with_ledger(runtime, by, "mage", seed, active)
    )
    blocks = {int(x["result"]["stage"]): x for x in case["blocks"]}
    block = blocks[50]
    phase = target.attribute_targets(block, by[50], GAP_MS, ORDER[50], runtime)["CLUSTER"]
    opps = alignment.extract_stage(block, by[50], ORDER[50])
    cluster_pxp = [o for o in opps if o["actionPhase"] == "CLUSTER"]
    result = block["result"]
    return {
        "continuityErrors": case["continuityErrors"],
        "status": case["status"],
        "baseHp": case["baseHp"],
        "cluster": phase,
        "clusterPxP": cluster_pxp,
        "stage50": {
            "entryState": result["entryState"],
            "exitState": result["exitState"],
            "settledSeconds": result["stageSettledTime"],
            "wallDamage": result["wallDamage"],
            "wallReserve": result["wallReserve"],
            "peakActive": result["peakActive"],
            "frontlineBlockTime": result["frontlineBlockTime"],
            "backlineExposure": result["backlineExposure"],
            "rootTimingActionCount": result["rootTimingActionCount"],
        },
    }


def mean(values):
    return None if not values else round(sum(values) / len(values), 6)


def summarize(rows):
    out = {}
    for side in ("OFF", "ON"):
        cases = [row[side] for row in rows]
        pxp = [o for case in cases for o in case["clusterPxP"]]
        clear = [
            float(case["cluster"]["clearLatencyFromPhaseStartMs"])
            for case in cases
            if case["cluster"]["clearLatencyFromPhaseStartMs"] is not None
        ]
        out[side] = {
            "cases": len(cases),
            "clusterAllPlayerKilledCases": sum(1 for case in cases if case["cluster"]["allPlayerKilled"]),
            "clusterWallResolvedOrUnkilled": sum(int(case["cluster"]["wallResolvedOrUnkilled"]) for case in cases),
            "meanClusterClearLatencyMs": mean(clear),
            "pxpOpportunities": len(pxp),
            "pxpPrimaryFromCluster": sum(1 for o in pxp if o["primaryOriginPhase"] == "CLUSTER"),
            "meanPxPTimeSincePhaseStartMs": mean([float(o["timeSincePhaseStartMs"]) for o in pxp]),
            "pxpTimeRangeMs": None if not pxp else [min(o["timeSincePhaseStartMs"] for o in pxp), max(o["timeSincePhaseStartMs"] for o in pxp)],
            "meanActivePhaseSpawnFractionAtPxP": mean([float(o["activePhaseSpawnFraction"]) for o in pxp]),
            "meanPxPPayloadDamage": mean([float(o["payload"]["damage"]) for o in pxp]),
            "meanPxPUniqueTargets": mean([float(o["payload"]["uniqueTargets"]) for o in pxp]),
            "meanLv31Damage": mean([float(o["payload"]["lv31Damage"]) for o in pxp]),
            "meanLv31UniqueTargets": mean([float(o["payload"]["lv31UniqueTargets"]) for o in pxp]),
            "meanStage50SettledSeconds": mean([float(case["stage50"]["settledSeconds"]) for case in cases]),
            "totalStage50WallDamage": round(sum(float(case["stage50"]["wallDamage"]) for case in cases), 6),
            "meanStage50PeakActive": mean([float(case["stage50"]["peakActive"]) for case in cases]),
        }
    off = out["OFF"]["meanClusterClearLatencyMs"]
    on = out["ON"]["meanClusterClearLatencyMs"]
    out["delta"] = {
        "clusterClearImprovementMs": None if off is None or on is None else round(off - on, 6),
        "clusterClearImprovementPct": None if off in (None, 0) or on is None else round((off - on) / off, 6),
        "stage50WallDamageReduction": round(out["OFF"]["totalStage50WallDamage"] - out["ON"]["totalStage50WallDamage"], 6),
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recipes", required=True)
    ap.add_argument("--p3", default="legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json")
    ap.add_argument("--p4d2-base", default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    ap.add_argument("--p4d2-temporal", default="legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    ap.add_argument("--seeds", default="101,211,307,409,503")
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    source = r.load_yaml(args.recipes)
    p3 = r.load_json(args.p3)
    p4 = r.load_json(args.p4d2_base)
    temporal = r.load_json(args.p4d2_temporal)
    seeds = tuple(int(x) for x in args.seeds.split(",") if x.strip())
    source_by = {int(x["stage"]): x for x in source["recipes"]}

    fidelity = []
    candidates = {}
    for cid in OFFSETS:
        doc = build_candidate(source, cid)
        by = {int(x["stage"]): x for x in doc["recipes"]}
        errors = list(r.static_recipe_gate(doc))
        for stage in source_by:
            if stage not in (49, 50) and by[stage] != source_by[stage]:
                errors.append(f"scope-change-stage{stage}")
        # Only Stage50 CLUSTER chronology may differ from transition-aware D3 base.
        base_doc = build_base(source)
        base_by = {int(x["stage"]): x for x in base_doc["recipes"]}
        if by[49] != base_by[49]:
            errors.append("STAGE49_CHANGED")
        stage_static = {str(s): integration.shape.stage_static(by[s]) for s in (49, 50)}
        if any(v["max4s"] > 8 for v in stage_static.values()):
            errors.append("AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP")
        if errors:
            candidates[cid] = {"staticErrors": errors, "stageStatic": stage_static}
            continue
        runtime = r.build_runtime(doc, p3, p4, temporal)
        rows = []
        for seed in seeds:
            off1 = run_side(runtime, by, seed, OFF)
            off2 = run_side(runtime, by, seed, OFF)
            on1 = run_side(runtime, by, seed, ON)
            on2 = run_side(runtime, by, seed, ON)
            if r.sha256_obj(off1) != r.sha256_obj(off2):
                fidelity.append(f"{cid}/OFF/determinism/{seed}")
            if r.sha256_obj(on1) != r.sha256_obj(on2):
                fidelity.append(f"{cid}/ON/determinism/{seed}")
            fidelity.extend(f"{cid}/OFF/{e}" for e in off1["continuityErrors"])
            fidelity.extend(f"{cid}/ON/{e}" for e in on1["continuityErrors"])
            rows.append({"seed": seed, "OFF": off1, "ON": on1})
        candidates[cid] = {
            "staticErrors": [],
            "stageStatic": stage_static,
            "offsetsMs": OFFSETS[cid],
            "summary": summarize(rows),
            "rows": rows,
        }

    out = {
        "version": "t1-stage50-mage-cluster-sustain-probe-v0.1",
        "status": "DIAGNOSTIC_CHRONOLOGY_ONLY_NO_AUTHORING_OR_SCALAR_ADOPTION",
        "sourceRecipe": str(args.recipes),
        "sourceRecipeSha256": r.sha256_bytes(Path(args.recipes).read_bytes()),
        "order": ORDER,
        "phaseGapMs": GAP_MS,
        "clusterMorphology": "DURABLE_CORE_3_FIXED",
        "mageLv31FidelityBridge": magebridge.BRIDGE_METADATA,
        "seeds": list(seeds),
        "fidelityErrors": fidelity,
        "candidates": candidates,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for cid, block in candidates.items():
        print("CANDIDATE", cid, "offsets", block.get("offsetsMs"))
        if block.get("staticErrors"):
            print(" STATIC_REJECT", block["staticErrors"])
            continue
        print(" SUMMARY", json.dumps(block["summary"], sort_keys=True))
        for row in block["rows"]:
            for side in ("OFF", "ON"):
                print(" CASE", cid, row["seed"], side, json.dumps({
                    "cluster": row[side]["cluster"],
                    "clusterPxP": row[side]["clusterPxP"],
                    "stage50": row[side]["stage50"],
                }, sort_keys=True))
    if fidelity:
        raise SystemExit("MAGE_CLUSTER_SUSTAIN_FIDELITY_FAIL")


if __name__ == "__main__":
    main()
