#!/usr/bin/env python3
"""Mage-only Stage50 P×P attribution: admitted STAGGER1800 vs rejected CLUSTER-final.

Attribution only. No recipe/scalar/production/adoption change.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import admit_t1_stage49_50_stagger1800_authoring_candidate_dynamic_v0_1 as admit
import probe_t1_stage50_cluster_final_consequence_translation_v0_1 as finalprobe
import probe_t1_stage49_50_pxp_phase_alignment_v0_1 as align
import probe_t1_stage49_50_target_phase_clearance_v0_1 as target
import probe_t1_archer_lv31_continuous_corridor_bridge_v0_1 as widthbridge
import t1_transition_microsim_mage_lv31_fidelity_bridge_v0_1 as magebridge

r = align.r
OFF = align.OFF
ON = align.ON
WIDTH = align.WIDTH
GAP = align.GAP_MS

ORDERS = {
    "ADMITTED_BASE": {
        49: ["DURABLE_SCATTER", "FRONTLINE", "CLUSTER", "LINE"],
        50: ["DURABLE_SCATTER", "FRONTLINE", "CLUSTER", "LINE", "LINE_REPRISE"],
    },
    "CLUSTER_FINAL_REJECTED": {
        49: ["DURABLE_SCATTER", "FRONTLINE", "CLUSTER", "LINE"],
        50: ["DURABLE_SCATTER", "FRONTLINE", "LINE", "LINE_REPRISE", "CLUSTER"],
    },
}
STATE_KEYS = ("baseHp", "baseMaxHp", "wallDeficit", "combo", "charge", "judgmentRng", "combatProcRng")


def build_variants(base: dict, candidate: dict) -> dict[str, dict]:
    admitted = admit.materialize(base, candidate)
    return {
        "ADMITTED_BASE": admitted,
        "CLUSTER_FINAL_REJECTED": finalprobe.build_probe(admitted),
    }


def run_case(runtime: dict, by_stage: dict, seed: int, active: list[int], order: dict) -> dict:
    case = magebridge.with_mage_lv31_fidelity(
        lambda: widthbridge.with_archer_final_width(
            WIDTH,
            lambda: target.execute_with_ledger(runtime, by_stage, "mage", seed, active),
        )
    )
    blocks = {int(x["result"]["stage"]): x for x in case["blocks"]}
    s49 = blocks[49]["result"]
    s50 = blocks[50]["result"]
    continuity = {k: s49["exitState"][k] == s50["entryState"][k] for k in STATE_KEYS}
    opportunities = align.extract_stage(blocks[50], by_stage[50], order[50])
    cluster = [x for x in opportunities if x["actionPhase"] == "CLUSTER"]
    return {
        "status": case["status"],
        "continuityErrors": case["continuityErrors"],
        "continuityEqual": continuity,
        "stage49SettledSeconds": s49["stageSettledTime"],
        "stage50SettledSeconds": s50["stageSettledTime"],
        "stage49ExitState": {k: s49["exitState"][k] for k in STATE_KEYS},
        "stage50EntryState": {k: s50["entryState"][k] for k in STATE_KEYS},
        "stage50RootActions": s50["rootTimingActionCount"],
        "allStage50PxP": opportunities,
        "clusterPxP": cluster,
    }


def summarize_variant(rows: list[dict]) -> dict:
    out = {}
    for side in ("OFF", "ON"):
        selected = [row[side] for row in rows]
        cluster_opps = [o for x in selected for o in x["clusterPxP"]]
        same_origin = [o for o in cluster_opps if o["primaryOriginPhase"] == "CLUSTER"]
        lv31_targets = [o["payload"]["lv31UniqueTargets"] for o in cluster_opps]
        cluster_origin_targets = []
        for o in cluster_opps:
            origin = o["payload"]["targetOriginPhases"].get("CLUSTER", {})
            cluster_origin_targets.append(int(origin.get("uniqueTargets", 0)))
        out[side] = {
            "cases": len(selected),
            "clusterPxPOpportunities": len(cluster_opps),
            "casesWithClusterPxP": sum(1 for x in selected if x["clusterPxP"]),
            "primaryFromCluster": len(same_origin),
            "meanClusterSpawnFractionAtPxP": None if not cluster_opps else round(sum(float(o["activePhaseSpawnFraction"]) for o in cluster_opps) / len(cluster_opps), 6),
            "meanTimeSinceClusterStartMs": None if not cluster_opps else round(sum(int(o["timeSincePhaseStartMs"]) for o in cluster_opps) / len(cluster_opps), 3),
            "meanRootPayloadUniqueTargets": None if not cluster_opps else round(sum(int(o["payload"]["uniqueTargets"]) for o in cluster_opps) / len(cluster_opps), 6),
            "meanClusterOriginUniqueTargets": None if not cluster_opps else round(sum(cluster_origin_targets) / len(cluster_origin_targets), 6),
            "meanLv31UniqueTargets": None if not cluster_opps else round(sum(lv31_targets) / len(lv31_targets), 6),
            "meanLv31Damage": None if not cluster_opps else round(sum(float(o["payload"]["lv31Damage"]) for o in cluster_opps) / len(cluster_opps), 6),
            "meanStage50SettledSeconds": round(sum(float(x["stage50SettledSeconds"]) for x in selected) / len(selected), 6),
            "entryCharges": [x["stage50EntryState"]["charge"] for x in selected],
            "entryCombos": [x["stage50EntryState"]["combo"] for x in selected],
        }
    return out


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
    variants = build_variants(base, candidate)

    out = {
        "version": "t1-mage-stage50-pxp-alignment-current-vs-cluster-final-v0.1",
        "status": "ATTRIBUTION_PASS",
        "candidateSha256": r.sha256_bytes(Path(args.candidate).read_bytes()),
        "baseSha256": r.sha256_bytes(Path(args.base).read_bytes()),
        "seeds": list(seeds),
        "archerWidthBridge": {"yTolerance": WIDTH, "status": "DIAGNOSTIC_ONLY_NOT_FROZEN"},
        "mageLv31FidelityBridge": magebridge.BRIDGE_METADATA,
        "fidelityErrors": [],
        "variants": {},
        "productionGameplayChange": False,
        "authoringAdopted": False,
        "numericalFreeze": False,
    }

    for variant_id, doc in variants.items():
        static_errors = list(r.static_recipe_gate(doc))
        if static_errors:
            out["fidelityErrors"].extend(f"{variant_id}/static/{e}" for e in static_errors)
            continue
        runtime = r.build_runtime(doc, p3, p4, temporal)
        by_stage = {int(x["stage"]): x for x in doc["recipes"]}
        rows = []
        for seed in seeds:
            row = {"seed": seed}
            for side, active in (("OFF", OFF), ("ON", ON)):
                a = run_case(runtime, by_stage, seed, active, ORDERS[variant_id])
                b = run_case(runtime, by_stage, seed, active, ORDERS[variant_id])
                if r.sha256_obj(a) != r.sha256_obj(b):
                    out["fidelityErrors"].append(f"{variant_id}/{side}/{seed}/determinism")
                out["fidelityErrors"].extend(f"{variant_id}/{side}/{seed}/{e}" for e in a["continuityErrors"])
                if not all(a["continuityEqual"].values()):
                    out["fidelityErrors"].append(f"{variant_id}/{side}/{seed}/stage49-50-state-continuity")
                row[side] = a
            rows.append(row)
        out["variants"][variant_id] = {
            "order": ORDERS[variant_id],
            "summary": summarize_variant(rows),
            "rows": rows,
        }

    if out["fidelityErrors"]:
        out["status"] = "ATTRIBUTION_FIDELITY_FAIL"
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for variant_id, block in out["variants"].items():
        print("VARIANT", variant_id, json.dumps(block["summary"], sort_keys=True))
        for row in block["rows"]:
            for side in ("OFF", "ON"):
                x = row[side]
                print(
                    "TRACE", variant_id, row["seed"], side,
                    "entryCharge", x["stage50EntryState"]["charge"],
                    "entryCombo", x["stage50EntryState"]["combo"],
                    "settle", x["stage50SettledSeconds"],
                    "clusterPxP", json.dumps(x["clusterPxP"], sort_keys=True),
                )
    if out["fidelityErrors"]:
        raise SystemExit("T1_MAGE_STAGE50_PXP_ATTRIBUTION_FIDELITY_FAIL")


if __name__ == "__main__":
    main()
