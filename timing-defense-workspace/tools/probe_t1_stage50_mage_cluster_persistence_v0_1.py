#!/usr/bin/env python3
"""T1 Stage50 Mage cluster-persistence diagnostic v0.1.

The corrected Lv31 package is strong when a real dense group exists at P×P,
but the current Stage50 CLUSTER often collapses to one survivor before the
P×P root arrives. This probe isolates encounter morphology before any scalar
change.

Isolation:
- Stage49 and all non-CLUSTER Stage50 phases use the exact ROT1 order candidate;
- CLUSTER remains the first Stage50 phase, removing prior-phase carryover;
- only the six CLUSTER body types/y placements vary;
- spawn offsets remain [0,120,240,360,480,600] ms;
- monster stats, class coefficients, Lv31 coefficients, action cadence,
  shop/EXP, and production gameplay are unchanged;
- Mage approved-contract fidelity bridge remains active.

Candidates decompose cohesion vs durability:
- CONTROL: current mixed GRUNT/RUNNER/BRUTE cluster;
- GRUNT_COHESION: same-speed light cluster;
- DURABLE_CORE_2: two centered BRUTEs + four GRUNTs;
- DURABLE_CORE_3: three centered BRUTEs + three GRUNTs.

Diagnostic only. No authoring/scalar adoption.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import probe_t1_stage49_50_order_robustness_v0_1 as orderprobe
import probe_t1_stage49_50_target_phase_clearance_v0_1 as target
import probe_t1_stage49_50_pxp_phase_alignment_v0_1 as alignment
import t1_transition_microsim_mage_lv31_fidelity_bridge_v0_1 as magebridge

r = orderprobe.r
ORDER_ID = "ROT1"  # Stage50 starts with CLUSTER; avoids prior Stage50 phase carryover.
OFF = orderprobe.OFF
ON = orderprobe.ON
GAP_MS = orderprobe.GAP_MS

CANDIDATES = {
    "CONTROL": [
        ("GRUNT", 0.42), ("RUNNER", 0.46), ("GRUNT", 0.50),
        ("RUNNER", 0.44), ("BRUTE", 0.48), ("GRUNT", 0.43),
    ],
    "GRUNT_COHESION": [
        ("GRUNT", 0.42), ("GRUNT", 0.46), ("GRUNT", 0.50),
        ("GRUNT", 0.44), ("GRUNT", 0.48), ("GRUNT", 0.43),
    ],
    "DURABLE_CORE_2": [
        ("BRUTE", 0.46), ("GRUNT", 0.44), ("BRUTE", 0.50),
        ("GRUNT", 0.48), ("GRUNT", 0.42), ("GRUNT", 0.46),
    ],
    "DURABLE_CORE_3": [
        ("BRUTE", 0.46), ("GRUNT", 0.44), ("BRUTE", 0.50),
        ("GRUNT", 0.48), ("BRUTE", 0.42), ("GRUNT", 0.46),
    ],
}


def build_candidate(source: dict, cid: str):
    doc, order = orderprobe.build_candidate(source, ORDER_ID)
    by = {int(x["stage"]): x for x in doc["recipes"]}
    recipe = by[50]
    cluster_rows = [x for x in recipe["spawns"] if 0 <= int(x["tMs"]) < GAP_MS]
    if len(cluster_rows) != 6:
        raise r.RunnerFidelityError(f"expected six first-phase cluster rows, got {len(cluster_rows)}")
    for row, (typ, y) in zip(cluster_rows, CANDIDATES[cid]):
        row["type"] = typ
        row["y"] = y
    doc["version"] = f"{doc['version']}+MAGE_CLUSTER_{cid}"
    doc["status"] = "EPHEMERAL_MAGE_CLUSTER_PERSISTENCE_NOT_AUTHORING"
    return doc, order


def execute_case(runtime, by, seed: int, active: list[int], order: dict):
    case = magebridge.with_mage_lv31_fidelity(
        lambda: target.execute_with_ledger(runtime, by, "mage", seed, active)
    )
    stage50 = next(x for x in case["blocks"] if int(x["result"]["stage"]) == 50)
    phase = target.attribute_targets(stage50, by[50], GAP_MS, order[50], runtime)["CLUSTER"]
    opportunities = alignment.extract_stage(stage50, by[50], order[50])
    cluster_pxp = [o for o in opportunities if o["actionPhase"] == "CLUSTER"]
    result = stage50["result"]
    return {
        "continuityErrors": case["continuityErrors"],
        "status": case["status"],
        "cluster": phase,
        "clusterPxP": cluster_pxp,
        "stage50": {
            "settledSeconds": result["stageSettledTime"],
            "wallDamage": result["wallDamage"],
            "wallReserve": result["wallReserve"],
            "peakActive": result["peakActive"],
            "frontlineBlockTime": result["frontlineBlockTime"],
            "backlineExposure": result["backlineExposure"],
        },
    }


def mean(vals):
    return None if not vals else round(sum(vals) / len(vals), 6)


def summarize(rows):
    out = {}
    for side in ("OFF", "ON"):
        cases = [x[side] for x in rows]
        clear = [float(x["cluster"]["clearLatencyFromPhaseStartMs"]) for x in cases if x["cluster"]["clearLatencyFromPhaseStartMs"] is not None]
        pxp = [o for x in cases for o in x["clusterPxP"]]
        out[side] = {
            "cases": len(cases),
            "clusterAllPlayerKilledCases": sum(1 for x in cases if x["cluster"]["allPlayerKilled"]),
            "meanClusterClearLatencyMs": mean(clear),
            "clusterWallResolvedOrUnkilled": sum(int(x["cluster"]["wallResolvedOrUnkilled"]) for x in cases),
            "pxpOpportunities": len(pxp),
            "pxpPrimaryFromCluster": sum(1 for o in pxp if o["primaryOriginPhase"] == "CLUSTER"),
            "meanPxPSpawnFraction": mean([float(o["activePhaseSpawnFraction"]) for o in pxp]),
            "meanPxPPayloadDamage": mean([float(o["payload"]["damage"]) for o in pxp]),
            "meanPxPUniqueTargets": mean([float(o["payload"]["uniqueTargets"]) for o in pxp]),
            "meanLv31Damage": mean([float(o["payload"]["lv31Damage"]) for o in pxp]),
            "meanLv31UniqueTargets": mean([float(o["payload"]["lv31UniqueTargets"]) for o in pxp]),
            "meanStage50SettledSeconds": mean([float(x["stage50"]["settledSeconds"]) for x in cases]),
            "totalStage50WallDamage": round(sum(float(x["stage50"]["wallDamage"]) for x in cases), 6),
            "meanStage50PeakActive": mean([float(x["stage50"]["peakActive"]) for x in cases]),
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

    candidates = {}
    fidelity = []
    for cid in CANDIDATES:
        doc, order = build_candidate(source, cid)
        by = {int(x["stage"]): x for x in doc["recipes"]}
        errors = list(r.static_recipe_gate(doc))
        for stage in source_by:
            if stage not in (49, 50) and by[stage] != source_by[stage]:
                errors.append(f"scope-change-stage{stage}")
        stage_static = {str(s): orderprobe.shape.stage_static(by[s]) for s in (49, 50)}
        if any(v["max4s"] > 8 for v in stage_static.values()):
            errors.append("AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP")
        if errors:
            candidates[cid] = {"staticErrors": errors, "stageStatic": stage_static}
            continue
        runtime = r.build_runtime(doc, p3, p4, temporal)
        rows = []
        for seed in seeds:
            off1 = execute_case(runtime, by, seed, OFF, order)
            off2 = execute_case(runtime, by, seed, OFF, order)
            on1 = execute_case(runtime, by, seed, ON, order)
            on2 = execute_case(runtime, by, seed, ON, order)
            if r.sha256_obj(off1) != r.sha256_obj(off2):
                fidelity.append(f"{cid}/OFF/determinism/{seed}")
            if r.sha256_obj(on1) != r.sha256_obj(on2):
                fidelity.append(f"{cid}/ON/determinism/{seed}")
            fidelity.extend(f"{cid}/OFF/{x}" for x in off1["continuityErrors"])
            fidelity.extend(f"{cid}/ON/{x}" for x in on1["continuityErrors"])
            rows.append({"seed": seed, "OFF": off1, "ON": on1})
        candidates[cid] = {
            "staticErrors": [],
            "stageStatic": stage_static,
            "clusterBodies": CANDIDATES[cid],
            "summary": summarize(rows),
            "rows": rows,
        }

    out = {
        "version": "t1-stage50-mage-cluster-persistence-probe-v0.1",
        "status": "DIAGNOSTIC_ENCOUNTER_MORPHOLOGY_NO_AUTHORING_OR_SCALAR_ADOPTION",
        "sourceRecipe": str(args.recipes),
        "sourceRecipeSha256": r.sha256_bytes(Path(args.recipes).read_bytes()),
        "orderId": ORDER_ID,
        "phaseGapMs": GAP_MS,
        "clusterOffsetsMs": [0, 120, 240, 360, 480, 600],
        "mageLv31FidelityBridge": magebridge.BRIDGE_METADATA,
        "seeds": list(seeds),
        "fidelityErrors": fidelity,
        "candidates": candidates,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for cid, block in candidates.items():
        print("CANDIDATE", cid)
        if block.get("staticErrors"):
            print(" STATIC_REJECT", block["staticErrors"])
            continue
        print(" SUMMARY", json.dumps(block["summary"], sort_keys=True))
        for row in block["rows"]:
            for side in ("OFF", "ON"):
                print(" CASE", cid, row["seed"], side, json.dumps(row[side], sort_keys=True))
    if fidelity:
        raise SystemExit("MAGE_CLUSTER_PERSISTENCE_FIDELITY_FAIL")


if __name__ == "__main__":
    main()
