#!/usr/bin/env python3
"""Timing Defense T1 Stage49-50 class-rotation pressure-shape probe v0.1.

Diagnostic purpose only.
- source is the exact v0.2 representative recipe;
- only Stage49-50 geometry/chronology/composition may change in generated ephemeral candidates;
- Stage46-48 remain byte-semantically identical to v0.2 so persistent-state chronology is preserved;
- monster/class/shop/EXP/PxP scalars remain unchanged;
- right-edge entry and authored 4-second density <= 8 are mandatory;
- Lv31 OFF/ON uses identical deterministic lifecycle entry state.

This tool searches candidate shape families. It does not adopt or freeze authoring.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import run_t1_transition_slice_microsim_settlement_fix_v0_1 as bridge

r = bridge.runner

STAGES = [46, 47, 48, 49, 50]
OFF_SKILLS = [6, 11, 16, 21, 26]
ON_SKILLS = [6, 11, 16, 21, 26, 31]


def max_density(spawns, window_ms=4000):
    times = [int(x["tMs"]) for x in spawns]
    if not times:
        return 0
    return max(sum(1 for other in times if start <= other < start + window_ms) for start in times)


def y_pattern(stage: int, mode: str):
    if mode == "DUAL_WIDE":
        return [0.22, 0.78]
    if mode == "TRI_WIDE":
        return [0.18, 0.82, 0.50]
    if mode == "DUAL49_TRI50":
        return [0.22, 0.78] if stage == 49 else [0.18, 0.82, 0.50]
    if mode == "DUAL_MID":
        return [0.28, 0.72]
    raise ValueError(mode)


def remap_stage_geometry(recipe: dict, mode: str):
    stage = int(recipe["stage"])
    pattern = y_pattern(stage, mode)
    brute_i = 0
    non_i = 0
    for spawn in recipe["spawns"]:
        # Distribute durable bodies across axes independently so a single durable lane
        # does not become the only meaningful answer. Non-durable bodies counter-rotate.
        if spawn["type"] == "BRUTE":
            idx = brute_i
            brute_i += 1
        else:
            idx = non_i + 1
            non_i += 1
        spawn["y"] = pattern[idx % len(pattern)]
    recipe["formation"] = "F08"
    recipe["formationSet"] = sorted(set(recipe.get("formationSet", [])) | {"F08"})


def tail_template(stage: int, size: int, mode: str):
    pattern = y_pattern(stage, mode)
    if stage == 49:
        types6 = ["BRUTE", "RUNNER", "GRUNT", "RUNNER", "BRUTE", "RUNNER"]
        types8 = ["BRUTE", "RUNNER", "GRUNT", "RUNNER", "BRUTE", "GRUNT", "RUNNER", "RUNNER"]
    else:
        types6 = ["GRUNT", "RUNNER", "BRUTE", "GRUNT", "RUNNER", "BRUTE"]
        types8 = ["GRUNT", "RUNNER", "BRUTE", "GRUNT", "RUNNER", "BRUTE", "RUNNER", "GRUNT"]
    types = types6 if size == 6 else types8
    if size == 6:
        offsets = [0, 250, 500, 2200, 2450, 2700]
    elif size == 8:
        offsets = [0, 220, 440, 660, 2200, 2420, 2640, 2860]
    else:
        raise ValueError(size)
    out = []
    brute_i = 0
    non_i = 0
    for typ, offset in zip(types, offsets):
        if typ == "BRUTE":
            idx = brute_i
            brute_i += 1
        else:
            idx = non_i + 1
            non_i += 1
        out.append({"tMs": offset, "type": typ, "y": pattern[idx % len(pattern)]})
    return out


def build_candidate(base_doc: dict, *, candidate_id: str, geometry: str, tail_size: int = 0, tail_copies: int = 0, tail_start_ms: int = 14000, tail_gap_ms: int = 14000):
    doc = copy.deepcopy(base_doc)
    by_stage = {int(x["stage"]): x for x in doc["recipes"]}
    for stage in (49, 50):
        remap_stage_geometry(by_stage[stage], geometry)
        if tail_size and tail_copies:
            template = tail_template(stage, tail_size, geometry)
            start0 = tail_start_ms + (1000 if stage == 50 else 0)
            for copy_i in range(tail_copies):
                start = start0 + copy_i * tail_gap_ms
                for row in template:
                    spawn = copy.deepcopy(row)
                    spawn["tMs"] = int(spawn["tMs"]) + start
                    by_stage[stage]["spawns"].append(spawn)
            by_stage[stage]["spawns"].sort(key=lambda x: (int(x["tMs"]), str(x["type"]), float(x["y"])))
    doc["version"] = f"{base_doc['version']}+{candidate_id}"
    doc["status"] = "EPHEMERAL_STAGE49_50_CLASS_ROTATION_SHAPE_DIAGNOSTIC_NOT_AUTHORING"
    return doc


def stage_static(recipe: dict):
    ys = [float(x["y"]) for x in recipe["spawns"]]
    return {
        "authored": len(recipe["spawns"]),
        "max4s": max_density(recipe["spawns"], 4000),
        "max6s": max_density(recipe["spawns"], 6000),
        "minY": min(ys),
        "maxY": max(ys),
        "ySpread": round(max(ys) - min(ys), 3),
    }


def slim(case: dict):
    rows = case["results"]
    late = [x for x in rows if x["stage"] in (49, 50)]
    return {
        "stagesExecuted": case["stagesExecuted"],
        "finalStatus": case["finalRunState"]["status"],
        "finalBaseHp": case["finalRunState"]["baseHp"],
        "totalWallDamage": round(sum(x["wallDamage"] for x in rows), 3),
        "lateWallDamage": round(sum(x["wallDamage"] for x in late), 3),
        "lateSettledSeconds": round(sum(x["stageSettledTime"] for x in late), 3),
        "lateRootActions": sum(x["rootTimingActionCount"] for x in late),
        "latePeakActiveMax": max((x["peakActive"] for x in late), default=0),
        "lateFrontlineBlockSeconds": round(sum(x["frontlineBlockTime"] for x in late), 3),
        "lateBacklineExposureSeconds": round(sum(x["backlineExposure"] for x in late), 3),
        "lateRemovalThroughputMean": round(sum(x["removalThroughput"] for x in late) / max(1, len(late)), 6),
        "lateControl": {
            key: round(sum(x["controlValue"][key] for x in late), 6)
            for key in ("knockbackDistance", "aftershockSlowDistancePrevented", "ironWallDamagePrevented", "shieldAbsorbed")
        },
        "stageRows": [
            {
                "stage": x["stage"],
                "outcome": x["combatOutcome"],
                "wallDamage": x["wallDamage"],
                "wallReserve": x["wallReserve"],
                "settled": x["stageSettledTime"],
                "actions": x["rootTimingActionCount"],
                "peakActive": x["peakActive"],
                "frontlineBlock": x["frontlineBlockTime"],
                "backlineExposure": x["backlineExposure"],
                "removalThroughput": x["removalThroughput"],
                "control": x["controlValue"],
            }
            for x in late
        ],
    }


def execute_candidate(recipe_doc: dict, p3: dict, p4d2_base: dict, temporal: dict, seeds):
    runtime = r.build_runtime(recipe_doc, p3, p4d2_base, temporal)
    by_stage = {int(x["stage"]): x for x in recipe_doc["recipes"]}
    rows = []
    fidelity_errors = []
    for cls in r.CLASSES:
        for seed in seeds:
            off1 = r.execute_chain(runtime, by_stage, cls, seed, STAGES, OFF_SKILLS)
            off2 = r.execute_chain(runtime, by_stage, cls, seed, STAGES, OFF_SKILLS)
            on1 = r.execute_chain(runtime, by_stage, cls, seed, STAGES, ON_SKILLS)
            on2 = r.execute_chain(runtime, by_stage, cls, seed, STAGES, ON_SKILLS)
            det_off = r.sha256_obj(off1) == r.sha256_obj(off2)
            det_on = r.sha256_obj(on1) == r.sha256_obj(on2)
            if not det_off or not det_on:
                fidelity_errors.append(f"determinism/{cls}/{seed}")
            if off1["continuityErrors"]:
                fidelity_errors.extend(off1["continuityErrors"])
            if on1["continuityErrors"]:
                fidelity_errors.extend(on1["continuityErrors"])
            if not off1["results"] or not on1["results"]:
                fidelity_errors.append(f"empty/{cls}/{seed}")
                continue
            eoff = off1["results"][0]["entryState"]
            eon = on1["results"][0]["entryState"]
            keys = ("baseHp", "baseMaxHp", "wallDeficit", "combo", "charge", "judgmentRng", "combatProcRng")
            same_entry = all(eoff[k] == eon[k] for k in keys)
            if not same_entry:
                fidelity_errors.append(f"pair-entry/{cls}/{seed}")
            rows.append({
                "class": cls,
                "seed": seed,
                "sameInitialLifecycle": same_entry,
                "deterministicOFF": det_off,
                "deterministicON": det_on,
                "OFF": slim(off1),
                "ON": slim(on1),
            })

    def aggregate(label: str):
        side = [x[label] for x in rows]
        by_class = {}
        for cls in r.CLASSES:
            crows = [x[label] for x in rows if x["class"] == cls]
            total_damage = sum(x["lateWallDamage"] for x in crows)
            by_class[cls] = {
                "cases": len(crows),
                "wallPositiveCases": sum(1 for x in crows if x["lateWallDamage"] > 0),
                "failOrIncompleteCases": sum(1 for x in crows if x["finalStatus"] == "FAILED" or len(x["stagesExecuted"]) < 5),
                "totalWallDamage": round(total_damage, 3),
                "meanFinalBaseHp": round(sum(x["finalBaseHp"] for x in crows) / max(1, len(crows)), 3),
                "meanLateSettledSeconds": round(sum(x["lateSettledSeconds"] for x in crows) / max(1, len(crows)), 3),
                "meanLatePeakActiveMax": round(sum(x["latePeakActiveMax"] for x in crows) / max(1, len(crows)), 3),
                "meanFrontlineBlockSeconds": round(sum(x["lateFrontlineBlockSeconds"] for x in crows) / max(1, len(crows)), 3),
                "meanBacklineExposureSeconds": round(sum(x["lateBacklineExposureSeconds"] for x in crows) / max(1, len(crows)), 3),
                "meanRemovalThroughput": round(sum(x["lateRemovalThroughputMean"] for x in crows) / max(1, len(crows)), 6),
                "controlTotals": {
                    key: round(sum(x["lateControl"][key] for x in crows), 6)
                    for key in ("knockbackDistance", "aftershockSlowDistancePrevented", "ironWallDamagePrevented", "shieldAbsorbed")
                },
            }
        class_damage = sorted((v["totalWallDamage"], k) for k, v in by_class.items())
        total = sum(v["totalWallDamage"] for v in by_class.values())
        top2 = sum(x[0] for x in class_damage[-2:])
        return {
            "cases": len(side),
            "wallPositiveCases": sum(1 for x in side if x["lateWallDamage"] > 0),
            "failOrIncompleteCases": sum(1 for x in side if x["finalStatus"] == "FAILED" or len(x["stagesExecuted"]) < 5),
            "totalWallDamage": round(total, 3),
            "meanFinalBaseHp": round(sum(x["finalBaseHp"] for x in side) / max(1, len(side)), 3),
            "classesWithWallPressure": sum(1 for v in by_class.values() if v["wallPositiveCases"] > 0),
            "top2DamageShare": None if total <= 0 else round(top2 / total, 6),
            "byClass": by_class,
        }

    return {
        "fidelityErrors": fidelity_errors,
        "rows": rows,
        "OFF": aggregate("OFF"),
        "ON": aggregate("ON"),
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
    p4d2_base = r.load_json(args.p4d2_base)
    temporal = r.load_json(args.p4d2_temporal)
    seeds = tuple(int(x) for x in args.seeds.split(",") if x.strip())
    source_by_stage = {int(x["stage"]): x for x in source["recipes"]}
    cap = int(source["guards"]["authored4sNormalMax"])

    specs = [
        ("BASE_V02", None, 0, 0),
        ("DUAL_WIDE_REMAP", "DUAL_WIDE", 0, 0),
        ("TRI_WIDE_REMAP", "TRI_WIDE", 0, 0),
        ("DUAL49_TRI50_REMAP", "DUAL49_TRI50", 0, 0),
        ("DUAL_WIDE_TAIL6_X1", "DUAL_WIDE", 6, 1),
        ("DUAL_WIDE_TAIL8_X1", "DUAL_WIDE", 8, 1),
        ("DUAL49_TRI50_TAIL6_X1", "DUAL49_TRI50", 6, 1),
        ("DUAL49_TRI50_TAIL8_X1", "DUAL49_TRI50", 8, 1),
        ("DUAL49_TRI50_TAIL6_X2", "DUAL49_TRI50", 6, 2),
        ("TRI_WIDE_TAIL6_X1", "TRI_WIDE", 6, 1),
    ]

    candidates = []
    rejected = []
    for cid, geometry, tail_size, tail_copies in specs:
        if cid == "BASE_V02":
            doc = copy.deepcopy(source)
        else:
            doc = build_candidate(
                source,
                candidate_id=cid,
                geometry=geometry,
                tail_size=tail_size,
                tail_copies=tail_copies,
            )
        by_stage = {int(x["stage"]): x for x in doc["recipes"]}
        static_errors = r.static_recipe_gate(doc)
        # Scope-fidelity gates: nothing outside Stage49-50 may change.
        for stage in source_by_stage:
            if stage not in (49, 50) and by_stage[stage] != source_by_stage[stage]:
                static_errors.append(f"scope-change-stage{stage}")
        stage_info = {str(stage): stage_static(by_stage[stage]) for stage in (49, 50)}
        if any(info["max4s"] > cap for info in stage_info.values()):
            static_errors.append("AUTHORED_4S_DENSITY_EXCEEDS_NORMAL_CAP")
        if any(float(spawn["y"]) < 0 or float(spawn["y"]) > 1 for stage in (49, 50) for spawn in by_stage[stage]["spawns"]):
            static_errors.append("Y_OUT_OF_RANGE")
        if static_errors:
            rejected.append({"id": cid, "staticErrors": static_errors, "stageStatic": stage_info})
            continue
        dynamic = execute_candidate(doc, p3, p4d2_base, temporal, seeds)
        candidates.append({
            "id": cid,
            "geometry": geometry,
            "tailSize": tail_size,
            "tailCopies": tail_copies,
            "stageStatic": stage_info,
            **dynamic,
        })

    output = {
        "version": "t1-stage49-50-class-rotation-shape-probe-v0.1",
        "status": "DIAGNOSTIC_SEARCH_NO_AUTHORING_ADOPTION",
        "sourceRecipe": str(args.recipes),
        "sourceRecipeSha256": r.sha256_bytes(Path(args.recipes).read_bytes()),
        "seeds": list(seeds),
        "stageScope": [49, 50],
        "normal4sCap": cap,
        "candidates": candidates,
        "rejected": rejected,
    }
    Path(args.json_out).write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("id offWall onWall offFail onFail offDamage onDamage offClasses onClasses offTop2 onTop2")
    for c in candidates:
        print(
            c["id"],
            c["OFF"]["wallPositiveCases"], c["ON"]["wallPositiveCases"],
            c["OFF"]["failOrIncompleteCases"], c["ON"]["failOrIncompleteCases"],
            c["OFF"]["totalWallDamage"], c["ON"]["totalWallDamage"],
            c["OFF"]["classesWithWallPressure"], c["ON"]["classesWithWallPressure"],
            c["OFF"]["top2DamageShare"], c["ON"]["top2DamageShare"],
        )
        print("  OFF_BY_CLASS", json.dumps({k:v["totalWallDamage"] for k,v in c["OFF"]["byClass"].items()}, sort_keys=True))
        print("  ON_BY_CLASS ", json.dumps({k:v["totalWallDamage"] for k,v in c["ON"]["byClass"].items()}, sort_keys=True))

    if any(c["fidelityErrors"] for c in candidates):
        raise SystemExit("STAGE49_50_CLASS_ROTATION_PROBE_FIDELITY_FAIL")


if __name__ == "__main__":
    main()
