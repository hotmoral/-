#!/usr/bin/env python3
"""Timing Defense P4-D2 Stage48-49 cadence-aware rotating-grammar probe v0.2.

Methodology goals:
- reuse the accepted Stage46 combat/effect kernel rather than reimplementing class formulas;
- remove simulator-only banking of overdue attack opportunities through NO_TARGET periods;
- expose Heavy/PxP timestamps and map them to the active rotating grammar;
- preserve a common 1.125s cadence lane;
- add Rogue legacy-recovery-delta sensitivity: 1.125s - 0.078s = 1.047s;
- select miss suites from the actual cadence-specific Heavy timeline, not hardcoded indices.

This remains a deterministic diagnostic. It does not freeze production cadence or Stage48/49 content.
"""
from __future__ import annotations

import argparse
import copy
import inspect
import json
from pathlib import Path

import run_p4d2_stage46_temporal_pressure_probe_v0_1 as stage46

CLASSES = ["Knight", "Rogue", "Tank", "Archer", "Mage"]
MIN_MISS_HEAVY_INDEX = 4


def build_fidelity_simulate():
    """Patch only timing instrumentation/NO_TARGET clock behavior into the existing kernel."""
    src = inspect.getsource(stage46.simulate)

    old_stats_tail = '        "aftershockZones": [],\n    }'
    new_stats_tail = (
        '        "aftershockZones": [],\n'
        '        "heavyTimeline": [],\n'
        '        "noTargetDrops": 0,\n'
        '    }'
    )
    if old_stats_tail not in src:
        raise RuntimeError("Stage46 simulate() stats shape changed; fidelity patch must be reviewed")
    src = src.replace(old_stats_tail, new_stats_tail, 1)

    old_attack_guard = '        if now >= next_attack - 1e-9 and nearest(mobs):\n'
    new_attack_guard = (
        '        # P4-D2 fidelity correction: NO_TARGET opportunities do not bank.\n'
        '        if now >= next_attack - 1e-9 and not nearest(mobs):\n'
        '            stats["noTargetDrops"] += 1\n'
        '            next_attack = now + root_interval\n\n'
        '        if now >= next_attack - 1e-9 and nearest(mobs):\n'
    )
    if old_attack_guard not in src:
        raise RuntimeError("Stage46 simulate() attack guard changed; fidelity patch must be reviewed")
    src = src.replace(old_attack_guard, new_attack_guard, 1)

    old_heavy = '            if heavy:\n                heavy_index += 1\n'
    new_heavy = (
        '            if heavy:\n'
        '                heavy_index += 1\n'
        '                stats["heavyTimeline"].append({"index": heavy_index, "time": round(now, 3)})\n'
    )
    if old_heavy not in src:
        raise RuntimeError("Stage46 simulate() Heavy block changed; fidelity patch must be reviewed")
    src = src.replace(old_heavy, new_heavy, 1)

    ns = dict(vars(stage46))
    exec(src, ns)
    return ns["simulate"]


FIDELITY_SIMULATE = build_fidelity_simulate()


def grammar_for_time(fixture, t):
    cycle = float(fixture["simulation"]["pressureCycleSeconds"])
    labels = fixture["pressurePatternLabels"]
    idx = int(float(t) // cycle)
    return labels[idx % len(labels)], idx


def annotate_timeline(fixture, timeline):
    out = []
    for row in timeline:
        label, cycle_idx = grammar_for_time(fixture, row["time"])
        out.append({
            "heavyIndex": int(row["index"]),
            "time": float(row["time"]),
            "grammar": label,
            "pressureCycleIndex": cycle_idx,
        })
    return out


def lane_fixture(base_fixture, cls, lane):
    f = copy.deepcopy(base_fixture)
    base_interval = float(f["simulation"]["rootAttackIntervalSeconds"])
    if lane == "COMMON_1P125_NO_BANK":
        interval = base_interval
    elif lane == "ROGUE_RECOVERY_DELTA_78MS_NO_BANK":
        if cls != "Rogue":
            raise ValueError("Rogue recovery lane may only be used for Rogue")
        interval = base_interval - 0.078
    else:
        raise ValueError(lane)
    f["simulation"]["rootAttackIntervalSeconds"] = interval
    return f, interval


def slim(row):
    keys = [
        "endWall", "endActive", "maxActive", "kills", "burialTime",
        "wallHits", "pxpCount", "heavyMissCount", "noTargetDrops",
        "chargerWindups", "chargerInterrupts", "chargerCharges",
        "siegerWindups", "siegerShots", "siegerRepositions",
        "splitterParentsKilled", "splitterChildrenSpawned",
    ]
    return {k: row.get(k) for k in keys}


def choose_first_heavy_by_grammar(timeline):
    chosen = {}
    for row in timeline:
        if row["heavyIndex"] < MIN_MISS_HEAVY_INDEX:
            continue
        chosen.setdefault(row["grammar"], row["heavyIndex"])
    return chosen


def actual_miss_timeline(annotated, missed_indices):
    wanted = set(int(x) for x in missed_indices)
    return [x for x in annotated if x["heavyIndex"] in wanted]


def run_lane(base, fixture, cls, lane):
    f, interval = lane_fixture(fixture, cls, lane)
    success_full = FIDELITY_SIMULATE(base, f, cls, True, ())
    success_timeline = annotate_timeline(f, success_full["heavyTimeline"])
    first_by_grammar = choose_first_heavy_by_grammar(success_timeline)

    one = {}
    two = {}
    for grammar in f["pressurePatternLabels"]:
        if grammar not in first_by_grammar:
            one[grammar] = {"status": "NO_ELIGIBLE_HEAVY"}
            two[grammar] = {"status": "NO_ELIGIBLE_HEAVY"}
            continue

        first_idx = int(first_by_grammar[grammar])

        r1 = FIDELITY_SIMULATE(base, f, cls, True, (first_idx,))
        t1 = annotate_timeline(f, r1["heavyTimeline"])
        one[grammar] = {
            "requestedStartGrammar": grammar,
            "requestedMissIndices": [first_idx],
            "actualMissTimeline": actual_miss_timeline(t1, [first_idx]),
            "result": slim(r1),
        }

        pair = [first_idx, first_idx + 1]
        r2 = FIDELITY_SIMULATE(base, f, cls, True, tuple(pair))
        t2 = annotate_timeline(f, r2["heavyTimeline"])
        two[grammar] = {
            "requestedStartGrammar": grammar,
            "requestedMissIndices": pair,
            "actualMissTimeline": actual_miss_timeline(t2, pair),
            "result": slim(r2),
        }

    success_wall = success_full["endWall"]
    monotonicity_watch = []
    for kind, group in (("ONE", one), ("TWO", two)):
        for grammar, row in group.items():
            if "result" in row and row["result"]["endWall"] > success_wall + 1e-9:
                monotonicity_watch.append({
                    "kind": kind,
                    "startGrammar": grammar,
                    "missEndWall": row["result"]["endWall"],
                    "successEndWall": success_wall,
                })

    return {
        "cadenceLane": lane,
        "rootIntervalSeconds": round(interval, 6),
        "productionCadenceFreeze": False,
        "noTargetClock": "NO_TARGET_OPPORTUNITIES_DO_NOT_BANK",
        "allSuccess": slim(success_full),
        "allSuccessHeavyTimeline": success_timeline,
        "firstEligibleHeavyByGrammar": first_by_grammar,
        "oneMissByStartGrammar": one,
        "twoConsecutiveMissByStartGrammar": two,
        "successMonotonicityWatch": monotonicity_watch,
    }


def run_all(base, fixture):
    lanes = {"COMMON_1P125_NO_BANK": {}}
    for cls in CLASSES:
        lanes["COMMON_1P125_NO_BANK"][cls] = run_lane(
            base, fixture, cls, "COMMON_1P125_NO_BANK"
        )

    lanes["ROGUE_RECOVERY_DELTA_78MS_NO_BANK"] = {
        "Rogue": run_lane(base, fixture, "Rogue", "ROGUE_RECOVERY_DELTA_78MS_NO_BANK")
    }

    return {
        "version": "p4d2-stage48-49-dynamic-grammar-result-v0.2",
        "status": "CADENCE_FIDELITY_DIAGNOSTIC_NO_NUMERICAL_FREEZE",
        "rng": "NONE",
        "sourceKernel": "run_p4d2_stage46_temporal_pressure_probe_v0_1.simulate",
        "methodologyAuthority": "legacy-game-structure/99_P4D2_TEMPORAL_CADENCE_FIDELITY_REVIEW_V0_1.md",
        "fixtureVersion": fixture["version"],
        "minMissHeavyIndex": MIN_MISS_HEAVY_INDEX,
        "lanes": lanes,
        "interpretationBoundary": [
            "COMMON_1P125_NO_BANK is continuity/sensitivity, not production cadence authority.",
            "ROGUE_RECOVERY_DELTA_78MS_NO_BANK preserves the recovered legacy recovery delta only; 1.047s is not a production whole-cycle freeze.",
            "Miss opportunities are selected from cadence-specific Heavy timestamps and mapped to active grammar cycles.",
            "NO_TARGET opportunities are not banked into catch-up bursts.",
            "Exact Stage48/49 content, final EXP, multiplayer scaling, and production values remain outside this probe."
        ]
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--base-fixture",
        default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json",
    )
    ap.add_argument(
        "--grammar-fixture",
        default="legacy-game-structure/data/p4d2_stage48_49_dynamic_rotating_grammar_fixture_v0_1.json",
    )
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    base = stage46.load(args.base_fixture)
    fixture = stage46.load(args.grammar_fixture)
    result = run_all(base, fixture)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
