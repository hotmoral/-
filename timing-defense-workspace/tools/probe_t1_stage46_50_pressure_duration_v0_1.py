#!/usr/bin/env python3
"""Timing Defense T1 Stage46-50 pressure-duration sensitivity probe v0.1.

Diagnostic purpose only:
- keep v0.2 monster/class/scalar anchors unchanged;
- preserve exact within-pulse composition and ordering;
- extend Stage46-50 only by repeating the already-authored Stage pulse;
- reject any candidate whose authored 4-second density exceeds the current normal cap;
- compare Lv31 OFF vs ON from identical deterministic lifecycle entry state.

This tool searches for a pressure-duration region. It does not select/freeze production authoring.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import run_t1_transition_slice_microsim_settlement_fix_v0_1 as bridge

r = bridge.runner


def max_density(spawns, window_ms=4000):
    times = [int(x["tMs"]) for x in spawns]
    return max(sum(1 for other in times if start <= other < start + window_ms) for start in times)


def extend_recipe_doc(base_doc, extra_copies: int, shift_ms: int):
    doc = copy.deepcopy(base_doc)
    for recipe in doc["recipes"]:
        stage = int(recipe["stage"])
        if stage < 46 or stage > 50:
            continue
        base_spawns = copy.deepcopy(recipe["spawns"])
        out = copy.deepcopy(base_spawns)
        for copy_index in range(1, extra_copies + 1):
            offset = shift_ms * copy_index
            for spawn in base_spawns:
                row = copy.deepcopy(spawn)
                row["tMs"] = int(row["tMs"]) + offset
                out.append(row)
        out.sort(key=lambda x: (int(x["tMs"]), str(x["type"]), float(x["y"])))
        recipe["spawns"] = out
    doc["version"] = f"{base_doc['version']}+duration-copies{extra_copies}-shift{shift_ms}ms"
    doc["status"] = "EPHEMERAL_PRESSURE_DURATION_SENSITIVITY_NOT_AUTHORING"
    return doc


def slim(case):
    return {
        "stagesExecuted": case["stagesExecuted"],
        "finalStatus": case["finalRunState"]["status"],
        "finalBaseHp": case["finalRunState"]["baseHp"],
        "totalWallDamage": round(sum(x["wallDamage"] for x in case["results"]), 3),
        "totalSettledSeconds": round(sum(x["stageSettledTime"] for x in case["results"]), 3),
        "stageRows": [
            {
                "stage": x["stage"],
                "outcome": x["combatOutcome"],
                "wallDamage": x["wallDamage"],
                "wallReserve": x["wallReserve"],
                "settled": x["stageSettledTime"],
                "actions": x["rootTimingActionCount"],
                "peakActive": x["peakActive"],
            }
            for x in case["results"]
        ],
    }


def execute_candidate(recipe_doc, p3, base, temporal, seeds):
    runtime = r.build_runtime(recipe_doc, p3, base, temporal)
    by_stage = {int(x["stage"]): x for x in recipe_doc["recipes"]}
    stages = [46, 47, 48, 49, 50]
    rows = []
    fidelity_errors = []

    for cls in r.CLASSES:
        for seed in seeds:
            off = r.execute_chain(runtime, by_stage, cls, seed, stages, [6, 11, 16, 21, 26])
            on = r.execute_chain(runtime, by_stage, cls, seed, stages, [6, 11, 16, 21, 26, 31])
            if off["continuityErrors"]:
                fidelity_errors.extend(off["continuityErrors"])
            if on["continuityErrors"]:
                fidelity_errors.extend(on["continuityErrors"])
            if not off["results"] or not on["results"]:
                fidelity_errors.append(f"empty/{cls}/{seed}")
                continue
            eoff = off["results"][0]["entryState"]
            eon = on["results"][0]["entryState"]
            keys = ("baseHp", "baseMaxHp", "wallDeficit", "combo", "charge", "judgmentRng", "combatProcRng")
            same_entry = all(eoff[k] == eon[k] for k in keys)
            if not same_entry:
                fidelity_errors.append(f"pair-entry/{cls}/{seed}")
            rows.append({"class": cls, "seed": seed, "sameInitialLifecycle": same_entry, "OFF": slim(off), "ON": slim(on)})

    def aggregate(label):
        side = [x[label] for x in rows]
        wall_positive = sum(1 for x in side if x["totalWallDamage"] > 0)
        failures = sum(1 for x in side if x["finalStatus"] == "FAILED" or len(x["stagesExecuted"]) < 5)
        return {
            "cases": len(side),
            "wallPositiveCases": wall_positive,
            "failOrIncompleteCases": failures,
            "totalWallDamage": round(sum(x["totalWallDamage"] for x in side), 3),
            "meanWallDamage": round(sum(x["totalWallDamage"] for x in side) / max(1, len(side)), 3),
            "meanFinalBaseHp": round(sum(x["finalBaseHp"] for x in side) / max(1, len(side)), 3),
            "meanSettledSeconds": round(sum(x["totalSettledSeconds"] for x in side) / max(1, len(side)), 3),
        }

    off_agg = aggregate("OFF")
    on_agg = aggregate("ON")
    return {
        "fidelityErrors": fidelity_errors,
        "rows": rows,
        "OFF": off_agg,
        "ON": on_agg,
        "directionalSeparation": {
            "moreOffWallPositiveCases": off_agg["wallPositiveCases"] > on_agg["wallPositiveCases"],
            "moreOffFailures": off_agg["failOrIncompleteCases"] > on_agg["failOrIncompleteCases"],
            "moreOffWallDamage": off_agg["totalWallDamage"] > on_agg["totalWallDamage"],
            "onNotUniversallyFailed": on_agg["failOrIncompleteCases"] < on_agg["cases"],
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recipes", required=True)
    ap.add_argument("--p3", default="legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json")
    ap.add_argument("--p4d2-base", default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    ap.add_argument("--p4d2-temporal", default="legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    ap.add_argument("--seeds", default="101,211,307")
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    base_doc = r.load_yaml(args.recipes)
    p3 = r.load_json(args.p3)
    base = r.load_json(args.p4d2_base)
    temporal = r.load_json(args.p4d2_temporal)
    seeds = tuple(int(x) for x in args.seeds.split(",") if x.strip())
    normal4 = int(base_doc["guards"]["authored4sNormalMax"])

    candidates = []
    rejected = []
    # 6-10s repetition was already proven too dense. Search only wider spacing
    # so the existing 4s cap stays authoritative while duration grows.
    search_grid = [(0, 0)] + [(copies, shift) for copies in (1, 2, 3) for shift in (11000, 12000, 14000, 16000)]

    for copies, shift in search_grid:
        doc = base_doc if copies == 0 else extend_recipe_doc(base_doc, copies, shift)
        stage_density = {}
        illegal = False
        for recipe in doc["recipes"]:
            stage = int(recipe["stage"])
            if 46 <= stage <= 50:
                d4 = max_density(recipe["spawns"], 4000)
                d6 = max_density(recipe["spawns"], 6000)
                stage_density[str(stage)] = {"authored": len(recipe["spawns"]), "max4s": d4, "max6s": d6}
                illegal = illegal or d4 > normal4
        candidate_id = "BASE_V02" if copies == 0 else f"COPY{copies}_SHIFT{shift}"
        if illegal:
            rejected.append({"id": candidate_id, "reason": "AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP", "stageDensity": stage_density})
            continue
        result = execute_candidate(doc, p3, base, temporal, seeds)
        candidates.append({
            "id": candidate_id,
            "extraCopies": copies,
            "shiftMs": shift,
            "stageDensity": stage_density,
            **result,
        })

    output = {
        "version": "t1-stage46-50-pressure-duration-sensitivity-v0.1",
        "status": "DIAGNOSTIC_SEARCH_NO_AUTHORING_SELECTION",
        "sourceRecipe": str(args.recipes),
        "sourceRecipeSha256": r.sha256_bytes(Path(args.recipes).read_bytes()),
        "seeds": list(seeds),
        "normal4sCap": normal4,
        "candidates": candidates,
        "rejected": rejected,
    }
    Path(args.json_out).write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("id offWallCases onWallCases offFail onFail offWallDamage onWallDamage offMeanHp onMeanHp")
    for c in candidates:
        print(
            c["id"],
            c["OFF"]["wallPositiveCases"], c["ON"]["wallPositiveCases"],
            c["OFF"]["failOrIncompleteCases"], c["ON"]["failOrIncompleteCases"],
            c["OFF"]["totalWallDamage"], c["ON"]["totalWallDamage"],
            c["OFF"]["meanFinalBaseHp"], c["ON"]["meanFinalBaseHp"],
        )
    if any(c["fidelityErrors"] for c in candidates):
        raise SystemExit("PRESSURE_DURATION_PROBE_FIDELITY_FAIL")


if __name__ == "__main__":
    main()
