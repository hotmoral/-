#!/usr/bin/env python3
"""Timing Defense P4-D2 Stage49 full complementary rotation probe v0.2.

Uses the v0.5 fidelity kernel and a bounded Stage49-like five-grammar rotation.
Adds:
- diagnostic ARMORED_DURABLE_PROXY anchor from the fixture;
- class-primary cadence lane selection (Rogue uses recovered -78ms sensitivity);
- all-finals-missed stress;
- consecutive-miss sweep by grammar start;
- Stage50 wall-reserve continuity reporting.

No production value/content is frozen by this runner.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import run_p4d2_stage46_temporal_pressure_probe_v0_1 as stage46
import run_p4d2_stage48_49_dynamic_grammar_probe_v0_2 as v02
import run_p4d2_stage48_49_dynamic_grammar_probe_v0_5 as v05

CLASSES = ["Knight", "Rogue", "Tank", "Archer", "Mage"]
PRIMARY_LANE = {
    "Knight": "COMMON_1P125_NO_BANK",
    "Rogue": "ROGUE_RECOVERY_DELTA_78MS_NO_BANK",
    "Tank": "COMMON_1P125_NO_BANK",
    "Archer": "COMMON_1P125_NO_BANK",
    "Mage": "COMMON_1P125_NO_BANK",
}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def inject_diagnostic_monsters(base, fixture):
    out = copy.deepcopy(base)
    for typ, anchor in fixture.get("diagnosticMonsterAnchors", {}).items():
        out["monsterAnchors"][typ] = dict(anchor)
    return out


def fixture_for_lane(fixture, cls):
    lane = PRIMARY_LANE[cls]
    f, interval = v02.lane_fixture(fixture, cls, lane)
    return f, lane, interval


def all_missed(base, fixture, cls):
    f, lane, interval = fixture_for_lane(fixture, cls)
    result = v05.FIDELITY_SIMULATE_V05(base, f, cls, True, tuple(range(1, 100)))
    return {
        "cadenceLane": lane,
        "rootIntervalSeconds": round(interval, 6),
        "result": v02.slim(result),
    }


def consecutive_sweep(base, fixture, cls, max_misses=8):
    f, lane, interval = fixture_for_lane(fixture, cls)
    success = v05.FIDELITY_SIMULATE_V05(base, f, cls, True, ())
    timeline = v02.annotate_timeline(f, success["heavyTimeline"])
    first_by_grammar = v02.choose_first_heavy_by_grammar(timeline)
    out = {}
    for grammar in f["pressurePatternLabels"]:
        if grammar not in first_by_grammar:
            out[grammar] = {"status": "NO_ELIGIBLE_HEAVY"}
            continue
        start = int(first_by_grammar[grammar])
        rows = []
        for n in range(1, max_misses + 1):
            misses = tuple(range(start, start + n))
            row = v05.FIDELITY_SIMULATE_V05(base, f, cls, True, misses)
            rows.append({
                "consecutiveMisses": n,
                "endWall": row["endWall"],
                "burialTime": row["burialTime"],
                "endActive": row["endActive"],
                "wallHits": row["wallHits"],
            })
            if row["burialTime"] is not None:
                break
        out[grammar] = {
            "startHeavyIndex": start,
            "cadenceLane": lane,
            "rootIntervalSeconds": round(interval, 6),
            "rows": rows,
        }
    return out


def primary_view(full_result):
    out = {}
    for cls in CLASSES:
        lane = PRIMARY_LANE[cls]
        row = full_result["lanes"][lane][cls]
        out[cls] = {
            "cadenceLane": lane,
            "allSuccess": row["allSuccess"],
            "oneMissByStartGrammar": row["oneMissByStartGrammar"],
            "twoConsecutiveMissByStartGrammar": row["twoConsecutiveMissByStartGrammar"],
            "successMonotonicityWatch": row["successMonotonicityWatch"],
        }
    return out


def run_all(base, fixture):
    base = inject_diagnostic_monsters(base, fixture)
    full = v05.run_all(base, fixture)
    primary = primary_view(full)
    all_miss = {cls: all_missed(base, fixture, cls) for cls in CLASSES}
    sweeps = {cls: consecutive_sweep(base, fixture, cls) for cls in CLASSES}

    all_success_survive = all(primary[c]["allSuccess"]["burialTime"] is None for c in CLASSES)
    all_miss_bury = all(all_miss[c]["result"]["burialTime"] is not None for c in CLASSES)
    max_success_wall_loss = max(2000.0 - primary[c]["allSuccess"]["endWall"] for c in CLASSES)

    return {
        "version": "p4d2-stage49-full-rotation-result-v0.2",
        "status": "BOUNDED_STAGE49_FULL_ROTATION_DIAGNOSTIC_NO_NUMERICAL_FREEZE",
        "rng": "NONE",
        "sourceKernel": "run_p4d2_stage48_49_dynamic_grammar_probe_v0_5",
        "fixtureVersion": fixture["version"],
        "primaryLaneByClass": PRIMARY_LANE,
        "primaryScenarios": primary,
        "allFinalsMissed": all_miss,
        "consecutiveMissSweepMax8": sweeps,
        "stageContinuity": {
            "baseHpPersistsAcrossStages": True,
            "automaticStageHeal": False,
            "maxAllSuccessWallLoss": max_success_wall_loss,
            "exactStage50ReserveFloorFrozen": False,
            "note": "Low surviving Stage49 wall HP is material even without burial because Stage50 inherits the remaining wall state."
        },
        "structuralChecks": {
            "allFiveAllSuccessSurvive": all_success_survive,
            "allFiveAllFinalsMissedBuryWithin60s": all_miss_bury,
            "identicalMistakeBudgetRequired": False,
            "newMonsterApproved": False,
            "productionAuthority": False
        }
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--base-fixture",
        default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json",
    )
    ap.add_argument(
        "--stage49-fixture",
        default="legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json",
    )
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    result = run_all(load(args.base_fixture), load(args.stage49_fixture))
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
