#!/usr/bin/env python3
"""T1 Stage49-50 grammar-order robustness probe v0.1.

Purpose
-------
The same late-T1 grammar set showed materially different class/Lv31 response when
only phase order changed. Before choosing an authoring candidate, test whether
intended class-role opportunity survives four cyclic orderings.

Boundaries:
- exact v0.2 source outside Stage49-50;
- same LINE / CLUSTER / FRONTLINE / DURABLE_SCATTER templates;
- legal 5500 ms phase gap; LINE_REPRISE remains the Stage50 closing phase;
- GRUNT/RUNNER/BRUTE only, right-edge spawn, authored max4 <= 8;
- no monster/class/shop/EXP/PxP scalar change;
- Archer Lv31 yTol=0.20 is diagnostic MID_ADJACENT bridge only, not a freeze;
- deterministic Lv31 OFF/ON paired execution.

No authoring adoption or numerical freeze is made by this probe.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import probe_t1_stage49_50_class_rotation_shape_v0_1 as shape
import probe_t1_stage49_50_distinct_grammar_cadence_v0_1 as distinct
import probe_t1_stage49_50_target_phase_clearance_v0_1 as target
import probe_t1_archer_lv31_continuous_corridor_bridge_v0_1 as widthbridge

r = shape.r
WIDTH = 0.20
GAP_MS = 5500
OFF = [6, 11, 16, 21, 26]
ON = [6, 11, 16, 21, 26, 31]
BASE_ORDER = ["LINE", "CLUSTER", "FRONTLINE", "DURABLE_SCATTER"]

ORDERS = {
    f"ROT{i}": BASE_ORDER[i:] + BASE_ORDER[:i]
    for i in range(len(BASE_ORDER))
}

ROLE_TARGETS = {
    "knight": [(49, "FRONTLINE"), (50, "FRONTLINE")],
    "rogue": [(49, "DURABLE_SCATTER"), (50, "DURABLE_SCATTER")],
    "tank": [(49, "FRONTLINE"), (50, "FRONTLINE")],
    "archer": [(49, "LINE"), (50, "LINE"), (50, "LINE_REPRISE")],
    # Stage49 is not a Mage-opportunity signature in the approved T1 skeleton.
    "mage": [(50, "CLUSTER")],
}


def build_candidate(source: dict, order_id: str) -> tuple[dict, dict]:
    doc = copy.deepcopy(source)
    by = {int(x["stage"]): x for x in doc["recipes"]}
    seq = ORDERS[order_id]
    order = {
        49: list(seq),
        50: list(seq) + ["LINE_REPRISE"],
    }
    for stage in (49, 50):
        by[stage]["spawns"] = distinct.build_stage(order[stage], GAP_MS)
        by[stage]["formation"] = "F08" if stage == 49 else "F01"
        by[stage]["formationSet"] = ["F01", "F02", "F03", "F08"]
        by[stage]["cadence"] = "CD05"
        by[stage]["pressureTags"] = ["BASELINE", "FLOOD", "RUSH", "BULWARK"]
    doc["version"] = f"{source['version']}+ORDER_ROBUST_{order_id}"
    doc["status"] = "EPHEMERAL_STAGE49_50_ORDER_ROBUSTNESS_NOT_AUTHORING"
    return doc, order


def role_stats(agg: dict, cls: str, side: str):
    rows = []
    for stage, grammar in ROLE_TARGETS[cls]:
        v = agg[cls][side][str(stage)][grammar]
        rows.append(v)
    unresolved = sum(int(v["wallResolvedOrUnkilled"]) for v in rows)
    killed = sum(int(v["playerKilled"]) for v in rows)
    authored = sum(int(v["authoredTargets"]) for v in rows)
    complete_cases = sum(int(v["allPlayerKilledCases"]) for v in rows)
    latency_weight = 0.0
    latency_cases = 0
    for v in rows:
        n = int(v["allPlayerKilledCases"])
        ms = v["meanClearLatencyMs"]
        if n > 0 and ms is not None:
            latency_weight += float(ms) * n
            latency_cases += n
    mean_latency = None if latency_cases == 0 else round(latency_weight / latency_cases, 3)
    return {
        "authoredTargets": authored,
        "playerKilled": killed,
        "wallResolvedOrUnkilled": unresolved,
        "completeCases": complete_cases,
        "meanClearLatencyMs": mean_latency,
    }


def role_delta(off: dict, on: dict):
    unresolved_improvement = off["wallResolvedOrUnkilled"] - on["wallResolvedOrUnkilled"]
    latency_delta = None
    latency_pct = None
    if off["meanClearLatencyMs"] is not None and on["meanClearLatencyMs"] is not None:
        latency_delta = round(off["meanClearLatencyMs"] - on["meanClearLatencyMs"], 3)
        if abs(off["meanClearLatencyMs"]) > 1e-9:
            latency_pct = round(latency_delta / off["meanClearLatencyMs"], 6)
    if unresolved_improvement > 0:
        direction = "POSITIVE_UNRESOLVED_REDUCTION"
    elif unresolved_improvement < 0:
        direction = "NEGATIVE_UNRESOLVED_INCREASE"
    elif latency_delta is None:
        direction = "NO_COMPLETE_LATENCY_SIGNAL"
    elif latency_delta > 0:
        direction = "POSITIVE_FASTER_CLEAR"
    elif latency_delta < 0:
        direction = "NEGATIVE_SLOWER_CLEAR"
    else:
        direction = "NEUTRAL"
    return {
        "unresolvedImprovement": unresolved_improvement,
        "clearLatencyImprovementMs": latency_delta,
        "clearLatencyImprovementPct": latency_pct,
        "direction": direction,
    }


def execute_target_phase(doc: dict, p3: dict, p4: dict, temporal: dict, seeds, order: dict):
    runtime = r.build_runtime(doc, p3, p4, temporal)
    by = {int(x["stage"]): x for x in doc["recipes"]}
    rows = []
    fidelity = []
    for cls in r.CLASSES:
        for seed in seeds:
            off1 = target.run_side(runtime, by, cls, seed, OFF, GAP_MS, order)
            off2 = target.run_side(runtime, by, cls, seed, OFF, GAP_MS, order)
            on1 = target.run_side(runtime, by, cls, seed, ON, GAP_MS, order)
            on2 = target.run_side(runtime, by, cls, seed, ON, GAP_MS, order)
            if r.sha256_obj(off1) != r.sha256_obj(off2):
                fidelity.append(f"OFF/determinism/{cls}/{seed}")
            if r.sha256_obj(on1) != r.sha256_obj(on2):
                fidelity.append(f"ON/determinism/{cls}/{seed}")
            fidelity.extend(f"OFF/{e}" for e in off1["continuityErrors"])
            fidelity.extend(f"ON/{e}" for e in on1["continuityErrors"])
            rows.append({"class": cls, "seed": seed, "OFF": off1, "ON": on1})
    agg = target.aggregate(rows, order)
    return rows, agg, fidelity


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
    for order_id in ORDERS:
        doc, order = build_candidate(source, order_id)
        by = {int(x["stage"]): x for x in doc["recipes"]}
        static_errors = list(r.static_recipe_gate(doc))
        for stage in source_by:
            if stage not in (49, 50) and by[stage] != source_by[stage]:
                static_errors.append(f"scope-change-stage{stage}")
        stage_static = {str(s): shape.stage_static(by[s]) for s in (49, 50)}
        if any(v["max4s"] > 8 for v in stage_static.values()):
            static_errors.append("AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP")
        if static_errors:
            candidates[order_id] = {"order": order, "staticErrors": static_errors, "stageStatic": stage_static}
            continue

        overall = widthbridge.with_archer_final_width(
            WIDTH,
            lambda doc=doc: shape.execute_candidate(doc, p3, p4, temporal, seeds),
        )
        fidelity.extend(f"{order_id}/overall/{e}" for e in overall["fidelityErrors"])
        phase_rows, phase_agg, phase_fidelity = execute_target_phase(doc, p3, p4, temporal, seeds, order)
        fidelity.extend(f"{order_id}/phase/{e}" for e in phase_fidelity)

        roles = {}
        for cls in r.CLASSES:
            off = role_stats(phase_agg, cls, "OFF")
            on = role_stats(phase_agg, cls, "ON")
            roles[cls] = {"OFF": off, "ON": on, "delta": role_delta(off, on)}
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

        candidates[order_id] = {
            "order": order,
            "staticErrors": [],
            "stageStatic": stage_static,
            "overall": overall,
            "phaseAggregate": phase_agg,
            "phaseRows": phase_rows,
            "roles": roles,
        }

    robustness = {}
    for cls in r.CLASSES:
        dirs = []
        pcts = []
        unresolved = []
        for order_id, block in candidates.items():
            if block.get("staticErrors"):
                continue
            d = block["roles"][cls]["delta"]
            dirs.append({"order": order_id, "direction": d["direction"]})
            if d["clearLatencyImprovementPct"] is not None:
                pcts.append(d["clearLatencyImprovementPct"])
            unresolved.append(d["unresolvedImprovement"])
        robustness[cls] = {
            "directions": dirs,
            "positiveOrders": sum(1 for x in dirs if x["direction"].startswith("POSITIVE")),
            "negativeOrders": sum(1 for x in dirs if x["direction"].startswith("NEGATIVE")),
            "neutralOrNoSignalOrders": sum(1 for x in dirs if not x["direction"].startswith(("POSITIVE", "NEGATIVE"))),
            "latencyImprovementPctRange": None if not pcts else [round(min(pcts), 6), round(max(pcts), 6)],
            "unresolvedImprovementRange": None if not unresolved else [min(unresolved), max(unresolved)],
        }

    out = {
        "version": "t1-stage49-50-order-robustness-probe-v0.1",
        "status": "DIAGNOSTIC_ORDER_ROBUSTNESS_NO_AUTHORING_ADOPTION",
        "sourceRecipe": str(args.recipes),
        "sourceRecipeSha256": r.sha256_bytes(Path(args.recipes).read_bytes()),
        "archerWidthBridge": {"yTolerance": WIDTH, "status": "DIAGNOSTIC_ONLY_NOT_FROZEN"},
        "phaseGapMs": GAP_MS,
        "seeds": list(seeds),
        "baseOrder": BASE_ORDER,
        "orders": ORDERS,
        "roleTargets": {k: [[s, g] for s, g in v] for k, v in ROLE_TARGETS.items()},
        "fidelityErrors": fidelity,
        "candidates": candidates,
        "robustness": robustness,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("order class direction unresolvedDelta latencyPct offWall onWall")
    for order_id, block in candidates.items():
        if block.get("staticErrors"):
            print(order_id, "STATIC_REJECT", block["staticErrors"])
            continue
        for cls in r.CLASSES:
            role = block["roles"][cls]
            boff = block["overall"]["OFF"]["byClass"][cls]
            bon = block["overall"]["ON"]["byClass"][cls]
            print(
                order_id, cls,
                role["delta"]["direction"],
                role["delta"]["unresolvedImprovement"],
                role["delta"]["clearLatencyImprovementPct"],
                boff["totalWallDamage"], bon["totalWallDamage"],
            )
    print("ROBUSTNESS", json.dumps(robustness, sort_keys=True))
    if fidelity:
        raise SystemExit("ORDER_ROBUSTNESS_FIDELITY_FAIL")


if __name__ == "__main__":
    main()
