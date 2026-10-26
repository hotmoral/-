#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import yaml

import admit_t1_contiguous_15_33_d1_dynamic_v0_1 as d1

r = d1.r
CONTINUITY_KEYS = d1.CONTINUITY_KEYS
EXPECTED_MATERIALIZED_SHA256 = "292b81f6d5258d3dfaec2f69abd8d817259b4a7c6955d9f986b570e73db207fd"
WINDOW = list(range(15, 38))
SEED_DEFAULT = "101,211,307,409,503"
VARIANTS = tuple(
    {
        "id": f"L16_{lv16}__L21_{lv21}__L26_{lv26}",
        "lv16BeforeStage": 18 if lv16 == "E18" else 21,
        "lv21BeforeStage": 25 if lv21 == "E25" else 28,
        "lv26BeforeStage": {"E32": 32, "M34": 34, "L36": 36}[lv26],
    }
    for lv16 in ("E18", "L21")
    for lv21 in ("E25", "L28")
    for lv26 in ("E32", "M34", "L36")
)


def avg(values):
    vals = [float(x) for x in values]
    return round(statistics.fmean(vals), 6) if vals else None


def active_for(stage: int, variant: dict) -> list[int]:
    active = {6, 11}
    if stage >= int(variant["lv16BeforeStage"]):
        active.add(16)
    if stage >= int(variant["lv21BeforeStage"]):
        active.add(21)
    if stage >= int(variant["lv26BeforeStage"]):
        active.add(26)
    return sorted(active)


def execute_case(runtime, by_stage: dict[int, dict], cls: str, seed: int, variant: dict):
    run = r.new_run(runtime, cls, seed, 11, [6, 11])
    results = []
    continuity_errors = []
    previous_exit = None
    for stage in WINDOW:
        if run["status"] == "FAILED":
            break
        active = active_for(stage, variant)
        run["activeMilestones"] = active
        run["level"] = max(active or [1])
        row = r.simulate_stage(run, by_stage[stage], runtime)
        row["skillState"]["e1Variant"] = variant["id"]
        row["skillState"]["lv16BeforeStage"] = int(variant["lv16BeforeStage"])
        row["skillState"]["lv21BeforeStage"] = int(variant["lv21BeforeStage"])
        row["skillState"]["lv26BeforeStage"] = int(variant["lv26BeforeStage"])
        if previous_exit is not None:
            for key in CONTINUITY_KEYS:
                if row["entryState"][key] != previous_exit[key]:
                    continuity_errors.append(
                        f"{variant['id']}/{cls}/seed{seed}/stage{stage}:{key}:"
                        f"{row['entryState'][key]}!={previous_exit[key]}"
                    )
        previous_exit = row["exitState"]
        results.append(row)
    return {
        "variant": variant["id"],
        "class": cls,
        "seed": seed,
        "stagesExecuted": [int(x["stage"]) for x in results],
        "continuityErrors": continuity_errors,
        "results": results,
        "finalRunState": {
            "status": run["status"],
            "baseHp": run["baseHp"],
            "baseMaxHp": run["baseMaxHp"],
            "combo": run["combo"],
            "charge": run["charge"],
            "judgmentRng": run["judgmentRng"],
            "combatProcRng": run["combatProcRng"],
            "comboPeak": run["comboPeak"],
            "n3Triggers": run["n3Triggers"],
        },
    }


def slim_case(case: dict) -> dict:
    return {
        "variant": case["variant"],
        "class": case["class"],
        "seed": case["seed"],
        "stagesExecuted": case["stagesExecuted"],
        "continuityErrors": case["continuityErrors"],
        "finalRunState": case["finalRunState"],
        "stageRows": [
            {
                "stage": int(x["stage"]),
                "outcome": x["combatOutcome"],
                "wallDamage": x["wallDamage"],
                "wallReserve": x["wallReserve"],
                "actions": x["rootTimingActionCount"],
                "settledTime": x["stageSettledTime"],
                "peakActive": x["peakActive"],
                "activeMilestones": x["skillState"]["activeMilestones"],
                "noEnemyCarry": x["invariants"]["noEnemyCarry"],
                "noTransientLeakage": x["invariants"]["noTransientLeakage"],
                "stageSettledInvariant": x["invariants"]["stageSettled"],
            }
            for x in case["results"]
        ],
    }


def aggregate(cases: list[dict]) -> dict:
    def row_at(case, stage):
        return next((x for x in case["results"] if int(x["stage"]) == stage), None)

    all_rows = [row for case in cases for row in case["results"]]
    stage_focus = {}
    for stage in range(33, 38):
        xs = [row_at(case, stage) for case in cases]
        xs = [x for x in xs if x is not None]
        stage_focus[str(stage)] = {
            "reachedCases": len(xs),
            "terminalFailures": sum(x["combatOutcome"] == "FAILED_WALL_DESTROYED" for x in xs),
            "meanWallDamage": avg(x["wallDamage"] for x in xs),
            "meanWallReserve": avg(x["wallReserve"] for x in xs),
            "meanActions": avg(x["rootTimingActionCount"] for x in xs),
            "meanSettledTime": avg(x["stageSettledTime"] for x in xs),
            "meanPeakActive": avg(x["peakActive"] for x in xs),
        }

    by_class = defaultdict(list)
    for case in cases:
        by_class[case["class"]].append(case)
    class_focus = {}
    for cls, rows in sorted(by_class.items()):
        class_focus[cls] = {}
        for stage in range(34, 38):
            xs = [row_at(case, stage) for case in rows]
            xs = [x for x in xs if x is not None]
            class_focus[cls][str(stage)] = {
                "reachedCases": len(xs),
                "terminalFailures": sum(x["combatOutcome"] == "FAILED_WALL_DESTROYED" for x in xs),
                "meanWallDamage": avg(x["wallDamage"] for x in xs),
                "meanActions": avg(x["rootTimingActionCount"] for x in xs),
                "meanSettledTime": avg(x["stageSettledTime"] for x in xs),
                "meanPeakActive": avg(x["peakActive"] for x in xs),
            }

    keyed = {(c["variant"], c["class"], c["seed"]): c for c in cases}
    lv26_deltas = []
    for lv16 in ("E18", "L21"):
        for lv21 in ("E25", "L28"):
            ids = {
                "E32": f"L16_{lv16}__L21_{lv21}__L26_E32",
                "M34": f"L16_{lv16}__L21_{lv21}__L26_M34",
                "L36": f"L16_{lv16}__L21_{lv21}__L26_L36",
            }
            for cls in r.CLASSES:
                for seed in sorted({c["seed"] for c in cases if c["class"] == cls}):
                    late = keyed.get((ids["L36"], cls, seed))
                    if not late:
                        continue
                    for compare_label in ("E32", "M34"):
                        other = keyed.get((ids[compare_label], cls, seed))
                        if not other:
                            continue
                        for stage in range(34, 38):
                            a, b = row_at(other, stage), row_at(late, stage)
                            if a is None or b is None:
                                continue
                            lv26_deltas.append({
                                "comparison": f"{compare_label}_MINUS_L36",
                                "class": cls,
                                "seed": seed,
                                "lv16": lv16,
                                "lv21": lv21,
                                "stage": stage,
                                "wallDamageDelta": round(float(a["wallDamage"]) - float(b["wallDamage"]), 6),
                                "actionsDelta": int(a["rootTimingActionCount"]) - int(b["rootTimingActionCount"]),
                                "settledTimeDelta": round(float(a["stageSettledTime"]) - float(b["stageSettledTime"]), 6),
                            })

    by_variant = defaultdict(list)
    for case in cases:
        by_variant[case["variant"]].append(case)
    variant_summary = {}
    for variant_id, rows in sorted(by_variant.items()):
        variant_summary[variant_id] = {
            "cases": len(rows),
            "completedThrough37": sum(case["stagesExecuted"] == WINDOW for case in rows),
            "terminalStatusCounts": dict(sorted(Counter(case["finalRunState"]["status"] for case in rows).items())),
            "meanFinalBaseHp": avg(case["finalRunState"]["baseHp"] for case in rows),
        }

    return {
        "overall": {
            "cases": len(cases),
            "completedThrough37": sum(case["stagesExecuted"] == WINDOW for case in cases),
            "stageRows": len(all_rows),
            "terminalFailureRows": sum(x["combatOutcome"] == "FAILED_WALL_DESTROYED" for x in all_rows),
        },
        "stage33to37": stage_focus,
        "classFocus34to37": class_focus,
        "variantSummary": variant_summary,
        "lv26PositionDeltas": lv26_deltas,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--materialized", required=True)
    ap.add_argument("--p3-fixture", required=True)
    ap.add_argument("--p4d2-base", required=True)
    ap.add_argument("--p4d2-temporal", required=True)
    ap.add_argument("--seeds", default=SEED_DEFAULT)
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    materialized_path = Path(args.materialized)
    materialized_sha = d1.c1.b1.sha_bytes(materialized_path)
    fidelity_errors = []
    if materialized_sha != EXPECTED_MATERIALIZED_SHA256:
        fidelity_errors.append(f"materialized-sha-drift:{materialized_sha}!={EXPECTED_MATERIALIZED_SHA256}")

    base_doc = yaml.safe_load(Path(args.base).read_text(encoding="utf-8"))
    materialized_doc = yaml.safe_load(materialized_path.read_text(encoding="utf-8"))
    recipes = materialized_doc.get("recipes", [])
    by_stage = {int(x["stage"]): x for x in recipes}
    if sorted(by_stage) != WINDOW:
        fidelity_errors.append(f"materialized-stage-set:{sorted(by_stage)}")

    runtime_doc = dict(base_doc)
    runtime_doc["recipes"] = recipes
    p3 = r.load_json(args.p3_fixture)
    p4base = r.load_json(args.p4d2_base)
    temporal = r.load_json(args.p4d2_temporal)
    runtime = r.build_runtime(runtime_doc, p3, p4base, temporal)

    seeds = tuple(int(x.strip()) for x in args.seeds.split(",") if x.strip())
    cases = []
    replay_errors = []
    continuity_errors = []
    invariant_errors = []

    if not fidelity_errors:
        for variant in VARIANTS:
            for cls in r.CLASSES:
                for seed in seeds:
                    a = execute_case(runtime, by_stage, cls, seed, variant)
                    b = execute_case(runtime, by_stage, cls, seed, variant)
                    if r.sha256_obj(a) != r.sha256_obj(b):
                        replay_errors.append(f"{variant['id']}/{cls}/{seed}")
                    continuity_errors.extend(a["continuityErrors"])
                    for row in a["results"]:
                        inv = row["invariants"]
                        terminal = row["combatOutcome"] == "FAILED_WALL_DESTROYED"
                        if not (inv["stageSettled"] or terminal):
                            invariant_errors.append(f"settle/{variant['id']}/{cls}/{seed}/S{row['stage']}")
                        if inv["stageSettled"] and not inv["noEnemyCarry"]:
                            invariant_errors.append(f"enemy-carry/{variant['id']}/{cls}/{seed}/S{row['stage']}")
                        if inv["stageSettled"] and not inv["noTransientLeakage"]:
                            invariant_errors.append(f"transient/{variant['id']}/{cls}/{seed}/S{row['stage']}")
                    cases.append(a)

    full_completion = bool(cases) and all(case["stagesExecuted"] == WINDOW for case in cases)
    admission = {
        "exactMaterializedIdentity": not fidelity_errors,
        "persistentStateContinuity": not continuity_errors,
        "deterministicReplay": not replay_errors,
        "settlementAndCarryInvariants": not invariant_errors,
        "allCasesCompletedThrough37": full_completion,
        "fidelityErrors": fidelity_errors,
        "continuityErrors": continuity_errors,
        "replayErrors": replay_errors,
        "invariantErrors": invariant_errors,
    }
    admission["pass"] = all(admission[k] for k in (
        "exactMaterializedIdentity", "persistentStateContinuity", "deterministicReplay",
        "settlementAndCarryInvariants", "allCasesCompletedThrough37"
    ))
    result = {
        "version": "t1-contiguous-15-37-e1-dynamic-admission-v0.1",
        "status": "PASS_DYNAMIC_DIAGNOSTIC_ONLY" if admission["pass"] else "DYNAMIC_ADMISSION_FAIL_REVIEW_REQUIRED",
        "authorityBoundary": {
            "lv16Reach": "Stage18-21 calibration-candidate band retained; no exact threshold freeze",
            "lv21Reach": "Stage25-28 calibration-candidate band retained; no exact threshold freeze",
            "lv26Probe": "Lv26 active before Stage32 vs Stage34 vs Stage36 only; does not freeze exact Stage32-36 reach position",
            "productionGameplayChange": False,
            "numericalFreeze": False,
        },
        "materializedSha256": materialized_sha,
        "admission": admission,
        "summary": aggregate(cases) if cases else {},
        "cases": [slim_case(c) for c in cases],
    }
    Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps({"status": result["status"], "admission": admission, "summary": result["summary"]}, indent=2, sort_keys=True))
    raise SystemExit(0 if admission["pass"] else 1)


if __name__ == "__main__":
    main()
