#!/usr/bin/env python3
"""T1 Stage49-50 P×P / grammar phase-alignment diagnostic v0.1.

Purpose
-------
Explain the residual Archer/Mage order sensitivity after known Lv31 adapter
fidelity corrections. This probe changes no recipe, class scalar, monster stat,
shop/EXP rule, or production gameplay.

For the same four cyclic grammar orders used by order-robustness it records:
- every Heavy P×P opportunity in Stage49/50;
- action timestamp and active authored grammar;
- the grammar that originally spawned the authoritative primary target;
- how much of the active phase had spawned by that root action;
- full parent-root payload damage/hits/unique targets by target-origin grammar;
- Lv31-only payload subset for ON cases.

This distinguishes a class-package defect from chronology/frontmost carryover.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

import probe_t1_stage49_50_order_robustness_v0_1 as orderprobe
import probe_t1_stage49_50_target_phase_clearance_v0_1 as target
import probe_t1_archer_lv31_continuous_corridor_bridge_v0_1 as widthbridge
import t1_transition_microsim_mage_lv31_fidelity_bridge_v0_1 as magebridge

r = orderprobe.r
WIDTH = orderprobe.WIDTH
GAP_MS = orderprobe.GAP_MS
OFF = orderprobe.OFF
ON = orderprobe.ON
CLASSES = ("archer", "mage")


def phase_maps(recipe: dict, names: list[str]):
    target_meta = {}
    phase_spawns = {name: [] for name in names}
    phase_starts = {name: i * GAP_MS for i, name in enumerate(names)}
    for idx, spawn in enumerate(recipe["spawns"], start=1):
        at_ms = int(spawn["tMs"])
        phase = target.distinct.phase_for_ms(at_ms, GAP_MS, names)
        tid = f"S{int(recipe['stage'])}_{idx}"
        target_meta[tid] = {
            "phase": phase,
            "spawnMs": at_ms,
            "type": spawn["type"],
            "y": float(spawn["y"]),
        }
        phase_spawns[phase].append(at_ms)
    return target_meta, phase_spawns, phase_starts


def root_payload(ledger: list[dict], action_id: int, target_meta: dict):
    rows = [e for e in ledger if e.get("parentActionId") == action_id]
    by_origin = collections.defaultdict(lambda: {"damage": 0.0, "hits": 0, "targets": set()})
    lv31 = {"damage": 0.0, "hits": 0, "targets": set()}
    effects = collections.Counter()
    for e in rows:
        tid = e["targetId"]
        origin = target_meta.get(tid, {}).get("phase", "NON_AUTHORED_OR_UNKNOWN")
        dmg = float(e["finalDamage"])
        by_origin[origin]["damage"] += dmg
        by_origin[origin]["hits"] += 1
        by_origin[origin]["targets"].add(tid)
        effect = str(e["effectId"])
        effects[effect] += 1
        if effect.startswith("LV31_"):
            lv31["damage"] += dmg
            lv31["hits"] += 1
            lv31["targets"].add(tid)
    return {
        "damage": round(sum(float(e["finalDamage"]) for e in rows), 6),
        "hits": len(rows),
        "uniqueTargets": len({e["targetId"] for e in rows}),
        "lv31Damage": round(lv31["damage"], 6),
        "lv31Hits": lv31["hits"],
        "lv31UniqueTargets": len(lv31["targets"]),
        "effects": dict(sorted(effects.items())),
        "targetOriginPhases": {
            k: {
                "damage": round(v["damage"], 6),
                "hits": v["hits"],
                "uniqueTargets": len(v["targets"]),
            }
            for k, v in sorted(by_origin.items())
        },
    }


def extract_stage(block: dict, recipe: dict, names: list[str]):
    target_meta, phase_spawns, phase_starts = phase_maps(recipe, names)
    opportunities = []
    pxp_seq = 0
    for action in block["result"]["actionTrace"]:
        is_pxp = bool(action.get("heavy") and action.get("x") == "PERFECT" and action.get("y") == "PERFECT")
        if not is_pxp:
            continue
        pxp_seq += 1
        at_ms = int(action["atMs"])
        action_phase = target.distinct.phase_for_ms(at_ms, GAP_MS, names)
        primary_id = action.get("primaryTargetId")
        primary_meta = target_meta.get(primary_id, {})
        authored = phase_spawns[action_phase]
        spawned = sum(1 for t in authored if t <= at_ms)
        opportunities.append({
            "pxpSequence": pxp_seq,
            "actionId": int(action["action"]),
            "atMs": at_ms,
            "actionPhase": action_phase,
            "timeSincePhaseStartMs": at_ms - phase_starts[action_phase],
            "activePhaseSpawned": spawned,
            "activePhaseAuthored": len(authored),
            "activePhaseSpawnFraction": None if not authored else round(spawned / len(authored), 6),
            "primaryTargetId": primary_id,
            "primaryTargetType": action.get("primaryTargetType"),
            "primaryTargetY": action.get("primaryTargetY"),
            "primaryOriginPhase": primary_meta.get("phase", "NON_AUTHORED_OR_UNKNOWN"),
            "primarySpawnMs": primary_meta.get("spawnMs"),
            "lv31Final": bool(action.get("lv31Final")),
            "payload": root_payload(block["ledger"], int(action["action"]), target_meta),
        })
    return opportunities


def run_case(runtime, by_stage, cls: str, seed: int, active: list[int], order: dict):
    case = magebridge.with_mage_lv31_fidelity(
        lambda: widthbridge.with_archer_final_width(
            WIDTH,
            lambda: target.execute_with_ledger(runtime, by_stage, cls, seed, active),
        )
    )
    stages = {}
    for block in case["blocks"]:
        stage = int(block["result"]["stage"])
        if stage in (49, 50):
            stages[str(stage)] = extract_stage(block, by_stage[stage], order[stage])
    return {
        "status": case["status"],
        "baseHp": case["baseHp"],
        "continuityErrors": case["continuityErrors"],
        "stages": stages,
    }


def summarize(rows: list[dict], order: dict):
    out = {}
    target_grammars = {
        "archer": {49: {"LINE"}, 50: {"LINE", "LINE_REPRISE"}},
        "mage": {50: {"CLUSTER"}},
    }
    for cls in CLASSES:
        out[cls] = {}
        for side in ("OFF", "ON"):
            out[cls][side] = {}
            crows = [x for x in rows if x["class"] == cls]
            for stage in (49, 50):
                wanted = target_grammars.get(cls, {}).get(stage, set())
                opps = [
                    o
                    for row in crows
                    for o in row[side]["stages"].get(str(stage), [])
                    if o["actionPhase"] in wanted
                ]
                if not wanted:
                    continue
                out[cls][side][str(stage)] = {
                    "targetGrammars": sorted(wanted),
                    "pxpOpportunities": len(opps),
                    "primaryFromSameGrammar": sum(1 for o in opps if o["primaryOriginPhase"] == o["actionPhase"]),
                    "primaryFromEarlierGrammar": sum(1 for o in opps if o["primaryOriginPhase"] != o["actionPhase"]),
                    "meanActivePhaseSpawnFraction": None if not opps else round(sum(o["activePhaseSpawnFraction"] for o in opps) / len(opps), 6),
                    "meanPayloadDamage": None if not opps else round(sum(o["payload"]["damage"] for o in opps) / len(opps), 6),
                    "meanPayloadUniqueTargets": None if not opps else round(sum(o["payload"]["uniqueTargets"] for o in opps) / len(opps), 6),
                    "meanLv31Damage": None if not opps else round(sum(o["payload"]["lv31Damage"] for o in opps) / len(opps), 6),
                    "meanLv31UniqueTargets": None if not opps else round(sum(o["payload"]["lv31UniqueTargets"] for o in opps) / len(opps), 6),
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

    candidates = {}
    fidelity = []
    for order_id in orderprobe.ORDERS:
        doc, order = orderprobe.build_candidate(source, order_id)
        static_errors = r.static_recipe_gate(doc)
        if static_errors:
            candidates[order_id] = {"order": order, "staticErrors": static_errors}
            continue
        runtime = r.build_runtime(doc, p3, p4, temporal)
        by_stage = {int(x["stage"]): x for x in doc["recipes"]}
        rows = []
        for cls in CLASSES:
            for seed in seeds:
                off1 = run_case(runtime, by_stage, cls, seed, OFF, order)
                off2 = run_case(runtime, by_stage, cls, seed, OFF, order)
                on1 = run_case(runtime, by_stage, cls, seed, ON, order)
                on2 = run_case(runtime, by_stage, cls, seed, ON, order)
                if r.sha256_obj(off1) != r.sha256_obj(off2):
                    fidelity.append(f"{order_id}/OFF/determinism/{cls}/{seed}")
                if r.sha256_obj(on1) != r.sha256_obj(on2):
                    fidelity.append(f"{order_id}/ON/determinism/{cls}/{seed}")
                fidelity.extend(f"{order_id}/OFF/{x}" for x in off1["continuityErrors"])
                fidelity.extend(f"{order_id}/ON/{x}" for x in on1["continuityErrors"])
                rows.append({"class": cls, "seed": seed, "OFF": off1, "ON": on1})
        candidates[order_id] = {
            "order": order,
            "staticErrors": [],
            "summary": summarize(rows, order),
            "rows": rows,
        }

    out = {
        "version": "t1-stage49-50-pxp-phase-alignment-probe-v0.1",
        "status": "DIAGNOSTIC_CHRONOLOGY_ATTRIBUTION_NO_AUTHORING_OR_SCALAR_ADOPTION",
        "sourceRecipe": str(args.recipes),
        "sourceRecipeSha256": r.sha256_bytes(Path(args.recipes).read_bytes()),
        "archerWidthBridge": {"yTolerance": WIDTH, "status": "DIAGNOSTIC_ONLY_NOT_FROZEN"},
        "mageLv31FidelityBridge": magebridge.BRIDGE_METADATA,
        "phaseGapMs": GAP_MS,
        "seeds": list(seeds),
        "fidelityErrors": fidelity,
        "candidates": candidates,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for order_id, block in candidates.items():
        print("ORDER", order_id, json.dumps(block.get("order"), sort_keys=True))
        if block.get("staticErrors"):
            print(" STATIC_REJECT", block["staticErrors"])
            continue
        print(" SUMMARY", json.dumps(block["summary"], sort_keys=True))
        for cls in CLASSES:
            for row in [x for x in block["rows"] if x["class"] == cls]:
                for side in ("OFF", "ON"):
                    for stage in (49, 50):
                        for o in row[side]["stages"].get(str(stage), []):
                            if cls == "mage" and stage == 50 and o["actionPhase"] == "CLUSTER":
                                print(" TRACE", order_id, cls, row["seed"], side, stage, json.dumps(o, sort_keys=True))
                            if cls == "archer" and o["actionPhase"] in ("LINE", "LINE_REPRISE"):
                                print(" TRACE", order_id, cls, row["seed"], side, stage, json.dumps(o, sort_keys=True))
    if fidelity:
        raise SystemExit("PXP_PHASE_ALIGNMENT_FIDELITY_FAIL")


if __name__ == "__main__":
    main()
