#!/usr/bin/env python3
"""T1 Stage49-50 sustained-cluster all-class integration compare v0.1.

Compare only the two Mage-positive Stage50 CLUSTER chronology candidates found
by the isolated sustain probe, under the same transition-aware v0.2 grammar
order and DURABLE_CORE_3 morphology.

Candidates:
- STAGGER_1800 [0,360,720,1080,1440,1800]
- SUSTAIN_3000 [0,600,1200,1800,2400,3000]

Everything else is held constant. This is diagnostic only: no authoring,
production, or numerical freeze.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import probe_t1_stage50_mage_cluster_sustain_v0_1 as sustain
import probe_t1_stage49_50_class_rotation_shape_v0_1 as shape
import probe_t1_stage49_50_order_robustness_v0_1 as orderprobe
import probe_t1_stage49_50_target_phase_clearance_v0_1 as target
import probe_t1_archer_lv31_continuous_corridor_bridge_v0_1 as widthbridge
import t1_transition_microsim_mage_lv31_fidelity_bridge_v0_1 as magebridge

r = sustain.r
ORDER = sustain.ORDER
GAP_MS = sustain.GAP_MS
WIDTH = 0.20
OFF = sustain.OFF
ON = sustain.ON
CANDIDATES = ("STAGGER_1800", "SUSTAIN_3000")


def execute_target_phase(doc, p3, p4, temporal, seeds):
    runtime = r.build_runtime(doc, p3, p4, temporal)
    by = {int(x["stage"]): x for x in doc["recipes"]}
    rows = []
    fidelity = []
    for cls in r.CLASSES:
        for seed in seeds:
            off1 = target.run_side(runtime, by, cls, seed, OFF, GAP_MS, ORDER)
            off2 = target.run_side(runtime, by, cls, seed, OFF, GAP_MS, ORDER)
            on1 = target.run_side(runtime, by, cls, seed, ON, GAP_MS, ORDER)
            on2 = target.run_side(runtime, by, cls, seed, ON, GAP_MS, ORDER)
            if r.sha256_obj(off1) != r.sha256_obj(off2):
                fidelity.append(f"OFF/determinism/{cls}/{seed}")
            if r.sha256_obj(on1) != r.sha256_obj(on2):
                fidelity.append(f"ON/determinism/{cls}/{seed}")
            fidelity.extend(f"OFF/{e}" for e in off1["continuityErrors"])
            fidelity.extend(f"ON/{e}" for e in on1["continuityErrors"])
            rows.append({"class": cls, "seed": seed, "OFF": off1, "ON": on1})
    return rows, target.aggregate(rows, ORDER), fidelity


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
    all_fidelity = []
    for cid in CANDIDATES:
        doc = sustain.build_candidate(source, cid)
        by = {int(x["stage"]): x for x in doc["recipes"]}
        errors = list(r.static_recipe_gate(doc))
        for stage in source_by:
            if stage not in (49, 50) and by[stage] != source_by[stage]:
                errors.append(f"scope-change-stage{stage}")
        stage_static = {str(s): shape.stage_static(by[s]) for s in (49, 50)}
        if any(v["max4s"] > 8 for v in stage_static.values()):
            errors.append("AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP")
        if errors:
            candidates[cid] = {"staticErrors": errors, "stageStatic": stage_static}
            continue

        overall = magebridge.with_mage_lv31_fidelity(
            lambda doc=doc: widthbridge.with_archer_final_width(
                WIDTH,
                lambda: shape.execute_candidate(doc, p3, p4, temporal, seeds),
            )
        )
        all_fidelity.extend(f"{cid}/overall/{e}" for e in overall["fidelityErrors"])

        phase_rows, phase_agg, phase_fidelity = magebridge.with_mage_lv31_fidelity(
            lambda doc=doc: widthbridge.with_archer_final_width(
                WIDTH,
                lambda: execute_target_phase(doc, p3, p4, temporal, seeds),
            )
        )
        all_fidelity.extend(f"{cid}/phase/{e}" for e in phase_fidelity)

        roles = {}
        for cls in r.CLASSES:
            off = orderprobe.role_stats(phase_agg, cls, "OFF")
            on = orderprobe.role_stats(phase_agg, cls, "ON")
            roles[cls] = {"OFF": off, "ON": on, "delta": orderprobe.role_delta(off, on)}
            if cls == "tank":
                boff = overall["OFF"]["byClass"]["tank"]
                bon = overall["ON"]["byClass"]["tank"]
                roles[cls]["objectiveProtection"] = {
                    "offWallDamage": boff["totalWallDamage"],
                    "onWallDamage": bon["totalWallDamage"],
                    "wallDamageReduction": round(boff["totalWallDamage"] - bon["totalWallDamage"], 6),
                    "offControlTotals": boff["controlTotals"],
                    "onControlTotals": bon["controlTotals"],
                }

        candidates[cid] = {
            "staticErrors": [],
            "stageStatic": stage_static,
            "offsetsMs": sustain.OFFSETS[cid],
            "overall": overall,
            "phaseAggregate": phase_agg,
            "roles": roles,
        }

    out = {
        "version": "t1-stage49-50-sustain-integration-compare-v0.1",
        "status": "DIAGNOSTIC_ALL_CLASS_COMPARE_NO_AUTHORING_OR_SCALAR_ADOPTION",
        "sourceRecipe": str(args.recipes),
        "sourceRecipeSha256": r.sha256_bytes(Path(args.recipes).read_bytes()),
        "order": ORDER,
        "phaseGapMs": GAP_MS,
        "clusterMorphology": "DURABLE_CORE_3_FIXED",
        "archerWidthBridge": {"yTolerance": WIDTH, "status": "DIAGNOSTIC_ONLY_NOT_FROZEN"},
        "mageLv31FidelityBridge": magebridge.BRIDGE_METADATA,
        "seeds": list(seeds),
        "fidelityErrors": all_fidelity,
        "candidates": candidates,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("candidate class roleDirection rolePct overallOFF overallON overallPct offWall onWall")
    for cid, block in candidates.items():
        if block.get("staticErrors"):
            print(cid, "STATIC_REJECT", block["staticErrors"])
            continue
        for cls in r.CLASSES:
            role = block["roles"][cls]
            boff = block["overall"]["OFF"]["byClass"][cls]
            bon = block["overall"]["ON"]["byClass"][cls]
            off_s = float(boff["meanLateSettled"])
            on_s = float(bon["meanLateSettled"])
            pct = None if off_s == 0 else round((off_s - on_s) / off_s, 6)
            print(
                cid, cls,
                role["delta"]["direction"],
                role["delta"]["clearLatencyImprovementPct"],
                off_s, on_s, pct,
                boff["totalWallDamage"], bon["totalWallDamage"],
            )
    if all_fidelity:
        raise SystemExit("SUSTAIN_INTEGRATION_COMPARE_FIDELITY_FAIL")


if __name__ == "__main__":
    main()
