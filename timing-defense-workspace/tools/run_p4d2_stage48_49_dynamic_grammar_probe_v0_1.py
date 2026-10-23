#!/usr/bin/env python3
"""Timing Defense P4-D2 Stage48-49 rotating-grammar repeated-miss probe.

This wrapper deliberately reuses the accepted Stage46 temporal combat kernel instead of
forking combat semantics. Only the pressure fixture and miss suites change.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_p4d2_stage46_temporal_pressure_probe_v0_1 import load, simulate, slim

CLASSES = ["Knight", "Rogue", "Tank", "Archer", "Mage"]


def run(base, fixture):
    suites = {"ALL_PXP": []}
    suites.update(fixture["grammarAlignedMissSuites"])

    rows = {}
    for cls in CLASSES:
        rows[cls] = {}
        for name, misses in suites.items():
            rows[cls][name] = slim(
                simulate(base, fixture, cls, True, tuple(misses))
            )

    all_success_survive = all(rows[c]["ALL_PXP"]["burialTime"] is None for c in CLASSES)

    one_miss_names = [n for n in suites if n.startswith("ONE_MISS_")]
    two_miss_names = [n for n in suites if n.startswith("TWO_MISS_")]

    per_class = {}
    for cls in CLASSES:
        one = {n: rows[cls][n] for n in one_miss_names}
        two = {n: rows[cls][n] for n in two_miss_names}
        per_class[cls] = {
            "allPxp": rows[cls]["ALL_PXP"],
            "oneMiss": one,
            "twoMiss": two,
            "oneMissBurialCount": sum(v["burialTime"] is not None for v in one.values()),
            "twoMissBurialCount": sum(v["burialTime"] is not None for v in two.values()),
            "worstOneMissEndWall": min(v["endWall"] for v in one.values()),
            "worstTwoMissEndWall": min(v["endWall"] for v in two.values()),
            "maxOneMissBacklog": max(v["endActive"] for v in one.values()),
            "maxTwoMissBacklog": max(v["endActive"] for v in two.values()),
        }

    # Success monotonicity watch: flag a miss suite if it ends with more wall HP than all-success.
    # This is not automatically a bug because target-order/path effects can exist, but it must be inspected.
    monotonicity = {}
    for cls in CLASSES:
        success_wall = rows[cls]["ALL_PXP"]["endWall"]
        better_when_missed = []
        for name in one_miss_names + two_miss_names:
            if rows[cls][name]["endWall"] > success_wall + 1e-9:
                better_when_missed.append(name)
        monotonicity[cls] = better_when_missed

    return {
        "version": "p4d2-stage48-49-dynamic-grammar-result-v0.1",
        "status": "BOUNDED_DETERMINISTIC_DIAGNOSTIC_NO_NUMERICAL_FREEZE",
        "rng": "NONE",
        "fixtureVersion": fixture["version"],
        "allSuccessSurvive": all_success_survive,
        "perClass": per_class,
        "raw": rows,
        "successMonotonicityWatch": monotonicity,
        "interpretationBoundary": [
            "This result is Stage48-49 mastery-pressure evidence only, not exact campaign authoring.",
            "Grammar/order should be repaired before class coefficients if one class is punished by an arbitrary miss timestamp.",
            "A successful-final-is-worse path is a WATCH requiring authoring/path inspection, not an automatic class nerf.",
            "Final EXP, Stage46 possession threshold, multiplayer scaling, and production numbers remain outside this probe."
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

    base = load(args.base_fixture)
    fixture = load(args.grammar_fixture)
    result = run(base, fixture)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
