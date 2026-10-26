#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import yaml

import admit_t1_contiguous_15_25_b1_dynamic_v0_1 as b1

r = b1.r
EXPECTED_MATERIALIZED_SHA256 = "284426b71fe03e9838ae141d90422d3d0dec55ad55c71466a4a28bc1fc91297c"
WINDOW = list(range(15, 32))
SEED_DEFAULT = "101,211,307,409,503"
CONTINUITY_KEYS = b1.CONTINUITY_KEYS
VARIANTS = (
    {"id": "L16_EARLY18__L21_EARLY25", "lv16BeforeStage": 18, "lv21BeforeStage": 25},
    {"id": "L16_EARLY18__L21_LATE28", "lv16BeforeStage": 18, "lv21BeforeStage": 28},
    {"id": "L16_LATE21__L21_EARLY25", "lv16BeforeStage": 21, "lv21BeforeStage": 25},
    {"id": "L16_LATE21__L21_LATE28", "lv16BeforeStage": 21, "lv21BeforeStage": 28},
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
        row["skillState"]["c1Variant"] = variant["id"]
        row["skillState"]["lv16BeforeStage"] = int(variant["lv16BeforeStage"])
        row["skillState"]["lv21BeforeStage"] = int(variant["lv21BeforeStage"])
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
        "stagesRequested": WINDOW,
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
    by_variant = defaultdict(list)
    by_class = defaultdict(list)
    all_rows = []
    for case in cases:
        by_variant[case["variant"]].append(case)
        by_class[case["class"]].append(case)
        all_rows.extend(case["results"])

    def row_at(case, stage):
        return next((x for x in case["results"] if int(x["stage"]) == stage), None)

    variant_summary = {}
    for variant_id, rows in sorted(by_variant.items()):
        stage_rows = defaultdict(list)
        for case in rows:
            for row in case["results"]:
                stage_rows[int(row["stage"])].append(row)
        stage_summary = {}
        for stage in WINDOW:
            xs = stage_rows.get(stage, [])
            stage_summary[str(stage)] = {
                "reachedCases": len(xs),
                "terminalFailures": sum(x["combatOutcome"] == "FAILED_WALL_DESTROYED" for x in xs),
                "meanWallDamage": avg(x["wallDamage"] for x in xs),
                "meanWallReserve": avg(x["wallReserve"] for x in xs),
                "meanActions": avg(x["rootTimingActionCount"] for x in xs),
                "meanSettledTime": avg(x["stageSettledTime"] for x in xs),
                "meanPeakActive": avg(x["peakActive"] for x in xs),
            }
        variant_summary[variant_id] = {
            "cases": len(rows),
            "completedThrough31": sum(case["stagesExecuted"] == WINDOW for case in rows),
            "terminalStatusCounts": dict(sorted(Counter(case["finalRunState"]["status"] for case in rows).items())),
            "meanFinalBaseHp": avg(case["finalRunState"]["baseHp"] for case in rows),
            "stages": stage_summary,
        }

    class_focus = {}
    for cls, rows in sorted(by_class.items()):
        focus = {}
        for stage in range(25, 32):
            xs = [row_at(case, stage) for case in rows]
            xs = [x for x in xs if x is not None]
            focus[str(stage)] = {
                "reachedCases": len(xs),
                "terminalFailures": sum(x["combatOutcome"] == "FAILED_WALL_DESTROYED" for x in xs),
                "meanWallDamage": avg(x["wallDamage"] for x in xs),
                "meanActions": avg(x["rootTimingActionCount"] for x in xs),
                "meanSettledTime": avg(x["stageSettledTime"] for x in xs),
                "meanPeakActive": avg(x["peakActive"] for x in xs),
            }
        class_focus[cls] = focus

    keyed = {(c["variant"], c["class"], c["seed"]): c for c in cases}
    lv21_deltas = []
    for lv16_before, prefix in ((18, "L16_EARLY18"), (21, "L16_LATE21")):
        early_id = f"{prefix}__L21_EARLY25"
        late_id = f"{prefix}__L21_LATE28"
        for cls in r.CLASSES:
            seeds = sorted({c["seed"] for c in cases if c["class"] == cls})
            for seed in seeds:
                early = keyed.get((early_id, cls, seed))
                late = keyed.get((late_id, cls, seed))
                if not early or not late:
                    continue
                for stage in (25, 26, 27, 28, 29, 31):
                    a, b = row_at(early, stage), row_at(late, stage)
                    if a is None or b is None:
                        continue
                    lv21_deltas.append({
                        "class": cls,
                        "seed": seed,
                        "lv16BeforeStage": lv16_before,
                        "stage": stage,
                        "early25MinusLate28WallDamage": round(float(a["wallDamage"]) - float(b["wallDamage"]), 6),
                        "early25MinusLate28Actions": int(a["rootTimingActionCount"]) - int(b["rootTimingActionCount"]),
                        "early25MinusLate28SettledTime": round(float(a["stageSettledTime"]) - float(b["stageSettledTime"]), 6),
                    })

    bridge_rows = []
    for case in cases:
        s25, s26 = row_at(case, 25), row_at(case, 26)
        s28, s29 = row_at(case, 28), row_at(case, 29)
        if s25 is not None and s26 is not None:
            bridge_rows.append({
                "edge": "25_TO_26",
                "variant": case["variant"],
                "class": case["class"],
                "seed": case["seed"],
                "nextMinusPrevWallDamage": round(float(s26["wallDamage"]) - float(s25["wallDamage"]), 6),
                "nextMinusPrevActions": int(s26["rootTimingActionCount"]) - int(s25["rootTimingActionCount"]),
                "nextMinusPrevSettledTime": round(float(s26["stageSettledTime"]) - float(s25["stageSettledTime"]), 6),
            })
        if s28 is not None and s29 is not None:
            bridge_rows.append({
                "edge": "28_TO_29",
                "variant": case["variant"],
                "class": case["class"],
                "seed": case["seed"],
                "nextMinusPrevWallDamage": round(float(s29["wallDamage"]) - float(s28["wallDamage"]), 6),
                "nextMinusPrevActions": int(s29["rootTimingActionCount"]) - int(s28["rootTimingActionCount"]),
                "nextMinusPrevSettledTime": round(float(s29["stageSettledTime"]) - float(s28["stageSettledTime"]), 6),
            })

    return {
        "variants": variant_summary,
        "classFocusStage25to31": class_focus,
        "lv21EdgeDeltas": lv21_deltas,
        "bridgeDeltas": bridge_rows,
        "overall": {
            "cases": len(cases),
            "completedThrough31": sum(case["stagesExecuted"] == WINDOW for case in cases),
            "stageRows": len(all_rows),
            "terminalFailureRows": sum(x["combatOutcome"] == "FAILED_WALL_DESTROYED" for x in all_rows),
        },
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

    base_path = Path(args.base)
    materialized_path = Path(args.materialized)
    materialized_sha = b1.sha_bytes(materialized_path)
    fidelity_errors = []
    if materialized_sha != EXPECTED_MATERIALIZED_SHA256:
        fidelity_errors.append(
            f"materialized-sha-drift:{materialized_sha}!={EXPECTED_MATERIALIZED_SHA256}"
        )

    base_doc = yaml.safe_load(base_path.read_text(encoding="utf-8"))
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

    admission = {
        "exactMaterializedIdentity": not fidelity_errors,
        "persistentStateContinuity": not continuity_errors,
        "deterministicReplay": not replay_errors,
        "settlementAndCarryInvariants": not invariant_errors,
        "fidelityErrors": fidelity_errors,
        "continuityErrors": continuity_errors,
        "replayErrors": replay_errors,
        "invariantErrors": invariant_errors,
    }
    admission["pass"] = all(
        admission[k]
        for k in (
            "exactMaterializedIdentity",
            "persistentStateContinuity",
            "deterministicReplay",
            "settlementAndCarryInvariants",
        )
    )

    result = {
        "version": "t1-contiguous-15-31-c1-dynamic-admission-v0.1",
        "status": "PASS_DYNAMIC_DIAGNOSTIC_ONLY" if admission["pass"] else "FIDELITY_FAIL_NO_BALANCE_INTERPRETATION",
        "authorityBoundary": {
            "lv16Reach": "Stage18-21 calibration-candidate band; retained as carry-in edge sensitivity at 18 and 21",
            "lv21Reach": "Stage25-28 calibration-candidate band; tested at both band edges 25 and 28",
            "stage15PriorSkillState": "[Lv6,Lv11] inherited from existing Stage18 paired diagnostic context; not EXP freeze",
            "expNumericalFreeze": False,
            "skillNumericalFreeze": False,
            "stage26_28CandidateAdopted": False,
            "productionGameplayChange": False,
            "fullT1ExactRecipeFreeze": False,
        },
        "sourceIdentity": {
            "baseRecipeSha256": b1.sha_bytes(base_path),
            "materializedStage15to31Sha256": materialized_sha,
        },
        "seeds": list(seeds),
        "variants": list(VARIANTS),
        "admission": admission,
        "summary": aggregate(cases) if cases else {},
        "cases": [slim_case(c) for c in cases],
    }
    Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "admission": admission,
        "materializedStage15to31Sha256": materialized_sha,
        "caseCount": len(cases),
        "overall": result.get("summary", {}).get("overall", {}),
    }, indent=2, sort_keys=True))
    raise SystemExit(0 if admission["pass"] else 1)


if __name__ == "__main__":
    main()
