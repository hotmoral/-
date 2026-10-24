#!/usr/bin/env python3
"""T1 Archer Lv31 continuous-y corridor bridge probe v0.1.

Purpose
-------
The approved P4-D2 Archer Lv31 geometry uses a five-band diagnostic abstraction:
MID_ADJACENT = aim band plus immediate adjacent bands (band radius 1).
T1 representative recipes use continuous normalized y, while the current T1 runner
reuses heavyLineYTol=0.12 for the Lv31 final. This probe does NOT freeze a width.
It tests bounded continuous-y interpretations of the already-approved structural width:

- 0.12: current T1 runner control
- 0.20: reaches adjacent-band centres if five equal bands span [0,1]
- 0.25: interior sensitivity point
- 0.30: reaches the full immediately-adjacent equal-band cell envelope

Only Archer's Lv31 final call is widened. Ordinary/Lv26 arrows remain unchanged.
All monster/class/scalar anchors and lifecycle semantics remain unchanged.

Diagnostic only. No production or campaign numerical freeze.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import run_t1_transition_slice_microsim_settlement_fix_v0_1 as bridge
import t1_transition_microsim_engine_v0_1 as engine
import probe_t1_stage49_50_sustained_split_pressure_v0_1 as sustained

r = bridge.runner
shape = sustained.shape

WIDTHS = [0.12, 0.20, 0.25, 0.30]
STAGES = [46, 47, 48, 49, 50]
OFF = [6, 11, 16, 21, 26]
ON = [6, 11, 16, 21, 26, 31]


def with_archer_final_width(width: float, fn):
    """Patch only the engine module's Archer attack binding during this call.

    The original Archer implementation reads heavyLineYTol only in the Lv31 final
    branch. Non-final Archer arrows use strictLineYTol, so this wrapper preserves
    ordinary/Lv26 geometry while changing only the final corridor.
    """
    original = engine.archer_attack

    def wrapped(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms):
        if not final:
            return original(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms)
        old = runtime["geometry"]["heavyLineYTol"]
        runtime["geometry"]["heavyLineYTol"] = float(width)
        try:
            return original(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms)
        finally:
            runtime["geometry"]["heavyLineYTol"] = old

    engine.archer_attack = wrapped
    try:
        return fn()
    finally:
        engine.archer_attack = original


def slim(case: dict):
    rows = case["results"]
    late = [x for x in rows if x["stage"] in (49, 50)]
    return {
        "stagesExecuted": case["stagesExecuted"],
        "status": case["finalRunState"]["status"],
        "finalBaseHp": round(case["finalRunState"]["baseHp"], 6),
        "totalWallDamage": round(sum(x["wallDamage"] for x in rows), 6),
        "lateWallDamage": round(sum(x["wallDamage"] for x in late), 6),
        "totalSettledSeconds": round(sum(x["stageSettledTime"] for x in rows), 6),
        "lateSettledSeconds": round(sum(x["stageSettledTime"] for x in late), 6),
        "totalRootActions": sum(x["rootTimingActionCount"] for x in rows),
        "lateRootActions": sum(x["rootTimingActionCount"] for x in late),
        "maxPeakActive": max((x["peakActive"] for x in rows), default=0),
        "lateMaxPeakActive": max((x["peakActive"] for x in late), default=0),
        "frontlineBlockSeconds": round(sum(x["frontlineBlockTime"] for x in rows), 6),
        "backlineExposureSeconds": round(sum(x["backlineExposure"] for x in rows), 6),
        "removalThroughputMean": round(sum(x["removalThroughput"] for x in rows) / max(1, len(rows)), 9),
        "stageRows": [
            {
                "stage": x["stage"],
                "wallDamage": x["wallDamage"],
                "wallReserve": x["wallReserve"],
                "settled": x["stageSettledTime"],
                "actions": x["rootTimingActionCount"],
                "peakActive": x["peakActive"],
                "frontlineBlock": x["frontlineBlockTime"],
                "backlineExposure": x["backlineExposure"],
                "removalThroughput": x["removalThroughput"],
            }
            for x in rows
        ],
    }


def run_chain(runtime, by_stage, cls, seed, active, width):
    return with_archer_final_width(
        width,
        lambda: r.execute_chain(runtime, by_stage, cls, seed, STAGES, active),
    )


def recipe_variants(source: dict):
    return {
        "BASE_V02": copy.deepcopy(source),
        "SUSTAIN_650_Q": sustained.candidate(source, "SUSTAIN_650_Q", 650, 20, 22, "QUARTER"),
        "SUSTAIN_500_Q": sustained.candidate(source, "SUSTAIN_500_Q", 500, 24, 28, "QUARTER"),
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

    source = r.load_yaml(args.recipes)
    p3 = r.load_json(args.p3)
    p4 = r.load_json(args.p4d2_base)
    temporal = r.load_json(args.p4d2_temporal)
    seeds = tuple(int(x) for x in args.seeds.split(",") if x.strip())

    geom = temporal["geometryAbstraction"]
    if geom.get("bands") != [-2, -1, 0, 1, 2]:
        raise SystemExit("ARCHER_WIDTH_BRIDGE_AUTHORITY_FAIL_BANDS")
    if int(temporal["lv31TemporalCenters"]["Archer"]["workingBandRadius"]) != 1:
        raise SystemExit("ARCHER_WIDTH_BRIDGE_AUTHORITY_FAIL_RADIUS")

    variants = recipe_variants(source)
    output_variants = {}
    fidelity_errors = []
    non_archer_digests = {}

    for variant_id, recipe_doc in variants.items():
        static_errors = r.static_recipe_gate(recipe_doc)
        if static_errors:
            raise SystemExit(f"{variant_id}:STATIC_GATE_FAIL:{static_errors}")
        runtime = r.build_runtime(recipe_doc, p3, p4, temporal)
        by_stage = {int(x["stage"]): x for x in recipe_doc["recipes"]}
        rows = []

        for width in WIDTHS:
            for seed in seeds:
                off1 = run_chain(runtime, by_stage, "archer", seed, OFF, width)
                off2 = run_chain(runtime, by_stage, "archer", seed, OFF, width)
                on1 = run_chain(runtime, by_stage, "archer", seed, ON, width)
                on2 = run_chain(runtime, by_stage, "archer", seed, ON, width)
                det_off = r.sha256_obj(off1) == r.sha256_obj(off2)
                det_on = r.sha256_obj(on1) == r.sha256_obj(on2)
                if not (det_off and det_on):
                    fidelity_errors.append(f"determinism/{variant_id}/{width}/{seed}")
                if off1["continuityErrors"] or on1["continuityErrors"]:
                    fidelity_errors.append(f"continuity/{variant_id}/{width}/{seed}")
                eoff = off1["results"][0]["entryState"]
                eon = on1["results"][0]["entryState"]
                keys = ("baseHp", "baseMaxHp", "wallDeficit", "combo", "charge", "judgmentRng", "combatProcRng")
                same_entry = all(eoff[k] == eon[k] for k in keys)
                if not same_entry:
                    fidelity_errors.append(f"pair-entry/{variant_id}/{width}/{seed}")
                rows.append({
                    "width": width,
                    "seed": seed,
                    "sameInitialLifecycle": same_entry,
                    "deterministicOFF": det_off,
                    "deterministicON": det_on,
                    "OFF": slim(off1),
                    "ON": slim(on1),
                })

            for cls in ("knight", "rogue", "tank", "mage"):
                case = run_chain(runtime, by_stage, cls, seeds[0], ON, width)
                key = (variant_id, cls)
                digest = r.sha256_obj(case)
                if key not in non_archer_digests:
                    non_archer_digests[key] = digest
                elif non_archer_digests[key] != digest:
                    fidelity_errors.append(f"non-archer-width-coupling/{variant_id}/{cls}/{width}")

        aggregates = []
        control_off_by_seed = {
            row["seed"]: r.sha256_obj(row["OFF"])
            for row in rows if abs(row["width"] - WIDTHS[0]) < 1e-12
        }
        for width in WIDTHS:
            wrows = [x for x in rows if abs(x["width"] - width) < 1e-12]
            off_invariant = all(r.sha256_obj(x["OFF"]) == control_off_by_seed[x["seed"]] for x in wrows)
            if not off_invariant:
                fidelity_errors.append(f"archer-off-width-coupling/{variant_id}/{width}")
            aggregates.append({
                "width": width,
                "cases": len(wrows),
                "offInvariantVsControl": off_invariant,
                "OFF": {
                    "wallPositive": sum(1 for x in wrows if x["OFF"]["totalWallDamage"] > 0),
                    "totalWallDamage": round(sum(x["OFF"]["totalWallDamage"] for x in wrows), 6),
                    "meanSettledSeconds": round(sum(x["OFF"]["totalSettledSeconds"] for x in wrows) / len(wrows), 6),
                    "meanActions": round(sum(x["OFF"]["totalRootActions"] for x in wrows) / len(wrows), 6),
                    "meanRemoval": round(sum(x["OFF"]["removalThroughputMean"] for x in wrows) / len(wrows), 9),
                },
                "ON": {
                    "wallPositive": sum(1 for x in wrows if x["ON"]["totalWallDamage"] > 0),
                    "totalWallDamage": round(sum(x["ON"]["totalWallDamage"] for x in wrows), 6),
                    "meanSettledSeconds": round(sum(x["ON"]["totalSettledSeconds"] for x in wrows) / len(wrows), 6),
                    "meanActions": round(sum(x["ON"]["totalRootActions"] for x in wrows) / len(wrows), 6),
                    "meanRemoval": round(sum(x["ON"]["removalThroughputMean"] for x in wrows) / len(wrows), 9),
                },
            })

        output_variants[variant_id] = {
            "recipeVersion": recipe_doc["version"],
            "stage49Max4s": shape.max_density(next(x for x in recipe_doc["recipes"] if int(x["stage"]) == 49)["spawns"], 4000),
            "stage50Max4s": shape.max_density(next(x for x in recipe_doc["recipes"] if int(x["stage"]) == 50)["spawns"], 4000),
            "aggregates": aggregates,
            "rows": rows,
        }

    out = {
        "version": "t1-archer-lv31-continuous-corridor-bridge-probe-v0.1",
        "status": "DIAGNOSTIC_WIDTH_BRIDGE_NO_NUMERICAL_FREEZE",
        "sourceRecipe": str(args.recipes),
        "sourceRecipeSha256": r.sha256_bytes(Path(args.recipes).read_bytes()),
        "p4d2BandAuthority": {
            "bands": geom["bands"],
            "workingBandRadius": temporal["lv31TemporalCenters"]["Archer"]["workingBandRadius"],
            "structuralMeaning": "MID_ADJACENT = aim band plus immediately adjacent bands",
        },
        "continuousSensitivity": {
            "widths": WIDTHS,
            "control": 0.12,
            "adjacentBandCentreReach": 0.20,
            "fullAdjacentEqualBandCellEnvelope": 0.30,
            "note": "These are diagnostic coordinate bridges, not production collision-width authority.",
        },
        "seeds": list(seeds),
        "fidelityErrors": fidelity_errors,
        "variants": output_variants,
    }
    Path(args.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("variant width offWall onWall offDamage onDamage offSec onSec offActions onActions offRemoval onRemoval")
    for vid, block in output_variants.items():
        for a in block["aggregates"]:
            print(
                vid, a["width"],
                a["OFF"]["wallPositive"], a["ON"]["wallPositive"],
                a["OFF"]["totalWallDamage"], a["ON"]["totalWallDamage"],
                a["OFF"]["meanSettledSeconds"], a["ON"]["meanSettledSeconds"],
                a["OFF"]["meanActions"], a["ON"]["meanActions"],
                a["OFF"]["meanRemoval"], a["ON"]["meanRemoval"],
            )
    if fidelity_errors:
        raise SystemExit("ARCHER_LV31_WIDTH_BRIDGE_FIDELITY_FAIL")


if __name__ == "__main__":
    main()
