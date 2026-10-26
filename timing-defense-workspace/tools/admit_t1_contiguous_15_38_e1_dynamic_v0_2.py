#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import yaml
import admit_t1_contiguous_15_37_e1_dynamic_v0_1 as v1

r = v1.r
CONTINUITY_KEYS = v1.CONTINUITY_KEYS
WINDOW = list(range(15, 39))
VARIANTS = v1.VARIANTS
EXPECTED_MATERIALIZED_SHA256 = "d7dd0c8b5f3593cb0d3cdc6d580c40872dd56ff7c09bd91496f7dcd93bb96d1e"


def avg(values):
    vals = [float(x) for x in values]
    return round(statistics.fmean(vals), 6) if vals else None


def active_for(stage, variant):
    active = {6, 11}
    if stage >= int(variant["lv16BeforeStage"]): active.add(16)
    if stage >= int(variant["lv21BeforeStage"]): active.add(21)
    if stage >= int(variant["lv26BeforeStage"]): active.add(26)
    return sorted(active)


def execute_case(runtime, by_stage, cls, seed, variant):
    run = r.new_run(runtime, cls, seed, 11, [6, 11])
    results, continuity_errors = [], []
    previous_exit = None
    for stage in WINDOW:
        if run["status"] == "FAILED": break
        active = active_for(stage, variant)
        run["activeMilestones"] = active
        run["level"] = max(active or [1])
        row = r.simulate_stage(run, by_stage[stage], runtime)
        row["skillState"]["e1v02Variant"] = variant["id"]
        row["skillState"]["lv16BeforeStage"] = int(variant["lv16BeforeStage"])
        row["skillState"]["lv21BeforeStage"] = int(variant["lv21BeforeStage"])
        row["skillState"]["lv26BeforeStage"] = int(variant["lv26BeforeStage"])
        if previous_exit is not None:
            for key in CONTINUITY_KEYS:
                if row["entryState"][key] != previous_exit[key]:
                    continuity_errors.append(f"{variant['id']}/{cls}/seed{seed}/stage{stage}:{key}")
        previous_exit = row["exitState"]
        results.append(row)
    return {"variant": variant["id"], "class": cls, "seed": seed, "stagesExecuted": [int(x["stage"]) for x in results], "continuityErrors": continuity_errors, "results": results, "finalRunState": {"status": run["status"], "baseHp": run["baseHp"], "baseMaxHp": run["baseMaxHp"], "combo": run["combo"], "charge": run["charge"], "judgmentRng": run["judgmentRng"], "combatProcRng": run["combatProcRng"]}}


def slim_case(case):
    return {"variant": case["variant"], "class": case["class"], "seed": case["seed"], "stagesExecuted": case["stagesExecuted"], "continuityErrors": case["continuityErrors"], "finalRunState": case["finalRunState"], "stageRows": [{"stage": int(x["stage"]), "outcome": x["combatOutcome"], "wallDamage": x["wallDamage"], "actions": x["rootTimingActionCount"], "settledTime": x["stageSettledTime"], "peakActive": x["peakActive"], "activeMilestones": x["skillState"]["activeMilestones"], "noEnemyCarry": x["invariants"]["noEnemyCarry"], "noTransientLeakage": x["invariants"]["noTransientLeakage"], "stageSettledInvariant": x["invariants"]["stageSettled"]} for x in case["results"]]}


def aggregate(cases):
    def row_at(case, stage): return next((x for x in case["results"] if int(x["stage"]) == stage), None)
    all_rows = [row for case in cases for row in case["results"]]
    stage_focus = {}
    for stage in range(33, 39):
        xs = [row_at(c, stage) for c in cases]; xs = [x for x in xs if x is not None]
        stage_focus[str(stage)] = {"reachedCases": len(xs), "terminalFailures": sum(x["combatOutcome"] == "FAILED_WALL_DESTROYED" for x in xs), "meanWallDamage": avg(x["wallDamage"] for x in xs), "meanActions": avg(x["rootTimingActionCount"] for x in xs), "meanSettledTime": avg(x["stageSettledTime"] for x in xs), "meanPeakActive": avg(x["peakActive"] for x in xs)}
    by_class = defaultdict(list)
    for c in cases: by_class[c["class"]].append(c)
    class_focus = {}
    for cls, rows in sorted(by_class.items()):
        class_focus[cls] = {}
        for stage in range(34, 39):
            xs = [row_at(c, stage) for c in rows]; xs = [x for x in xs if x is not None]
            class_focus[cls][str(stage)] = {"reachedCases": len(xs), "terminalFailures": sum(x["combatOutcome"] == "FAILED_WALL_DESTROYED" for x in xs), "meanWallDamage": avg(x["wallDamage"] for x in xs), "meanActions": avg(x["rootTimingActionCount"] for x in xs), "meanSettledTime": avg(x["stageSettledTime"] for x in xs), "meanPeakActive": avg(x["peakActive"] for x in xs)}
    by_variant = defaultdict(list)
    for c in cases: by_variant[c["variant"]].append(c)
    variants = {vid: {"cases": len(rows), "completedThrough38": sum(c["stagesExecuted"] == WINDOW for c in rows), "terminalStatusCounts": dict(sorted(Counter(c["finalRunState"]["status"] for c in rows).items())), "meanFinalBaseHp": avg(c["finalRunState"]["baseHp"] for c in rows)} for vid, rows in sorted(by_variant.items())}
    return {"overall": {"cases": len(cases), "completedThrough38": sum(c["stagesExecuted"] == WINDOW for c in cases), "stageRows": len(all_rows), "terminalFailureRows": sum(x["combatOutcome"] == "FAILED_WALL_DESTROYED" for x in all_rows)}, "stage33to38": stage_focus, "classFocus34to38": class_focus, "variantSummary": variants}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True); ap.add_argument("--materialized", required=True)
    ap.add_argument("--p3-fixture", required=True); ap.add_argument("--p4d2-base", required=True); ap.add_argument("--p4d2-temporal", required=True)
    ap.add_argument("--seeds", default="101,211,307,409,503"); ap.add_argument("--json-out", required=True)
    args = ap.parse_args()
    materialized_path = Path(args.materialized)
    materialized_sha = v1.d1.c1.b1.sha_bytes(materialized_path)
    fidelity_errors = []
    if materialized_sha != EXPECTED_MATERIALIZED_SHA256: fidelity_errors.append(f"materialized-sha-drift:{materialized_sha}!={EXPECTED_MATERIALIZED_SHA256}")
    base_doc = yaml.safe_load(Path(args.base).read_text()); mat_doc = yaml.safe_load(materialized_path.read_text())
    recipes = mat_doc.get("recipes", []); by_stage = {int(x["stage"]): x for x in recipes}
    if sorted(by_stage) != WINDOW: fidelity_errors.append(f"materialized-stage-set:{sorted(by_stage)}")
    runtime_doc = dict(base_doc); runtime_doc["recipes"] = recipes
    runtime = r.build_runtime(runtime_doc, r.load_json(args.p3_fixture), r.load_json(args.p4d2_base), r.load_json(args.p4d2_temporal))
    seeds = tuple(int(x.strip()) for x in args.seeds.split(",") if x.strip())
    cases, replay_errors, continuity_errors, invariant_errors = [], [], [], []
    if not fidelity_errors:
        for variant in VARIANTS:
            for cls in r.CLASSES:
                for seed in seeds:
                    a = execute_case(runtime, by_stage, cls, seed, variant); b = execute_case(runtime, by_stage, cls, seed, variant)
                    if r.sha256_obj(a) != r.sha256_obj(b): replay_errors.append(f"{variant['id']}/{cls}/{seed}")
                    continuity_errors.extend(a["continuityErrors"])
                    for row in a["results"]:
                        inv = row["invariants"]; terminal = row["combatOutcome"] == "FAILED_WALL_DESTROYED"
                        if not (inv["stageSettled"] or terminal): invariant_errors.append(f"settle/{variant['id']}/{cls}/{seed}/S{row['stage']}")
                        if inv["stageSettled"] and not inv["noEnemyCarry"]: invariant_errors.append(f"enemy-carry/{variant['id']}/{cls}/{seed}/S{row['stage']}")
                        if inv["stageSettled"] and not inv["noTransientLeakage"]: invariant_errors.append(f"transient/{variant['id']}/{cls}/{seed}/S{row['stage']}")
                    cases.append(a)
    summary = aggregate(cases) if cases else {}
    s34 = summary.get("stage33to38", {}).get("34", {}); s35 = summary.get("stage33to38", {}).get("35", {})
    recovery_supported = bool(s34 and s35 and s35.get("meanActions") < s34.get("meanActions") and s35.get("meanSettledTime") < s34.get("meanSettledTime"))
    full_completion = bool(cases) and all(c["stagesExecuted"] == WINDOW for c in cases)
    admission = {"exactMaterializedIdentity": not fidelity_errors, "persistentStateContinuity": not continuity_errors, "deterministicReplay": not replay_errors, "settlementAndCarryInvariants": not invariant_errors, "allCasesCompletedThrough38": full_completion, "stage35RecoveryIntentSupported": recovery_supported, "fidelityErrors": fidelity_errors, "continuityErrors": continuity_errors, "replayErrors": replay_errors, "invariantErrors": invariant_errors}
    admission["pass"] = all(admission[k] for k in ("exactMaterializedIdentity", "persistentStateContinuity", "deterministicReplay", "settlementAndCarryInvariants", "allCasesCompletedThrough38", "stage35RecoveryIntentSupported"))
    result = {"version": "t1-contiguous-15-38-e1-dynamic-admission-v0.2", "status": "PASS_DYNAMIC_DIAGNOSTIC_ONLY" if admission["pass"] else "DYNAMIC_ADMISSION_FAIL_REVIEW_REQUIRED", "authorityBoundary": {"lv26Probe": "Lv26 active before Stage32 vs Stage34 vs Stage36 only; no exact unlock freeze", "productionGameplayChange": False, "numericalFreeze": False}, "materializedSha256": materialized_sha, "admission": admission, "summary": summary, "cases": [slim_case(c) for c in cases]}
    Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps({"status": result["status"], "admission": admission, "summary": summary}, indent=2, sort_keys=True))
    raise SystemExit(0 if admission["pass"] else 1)


if __name__ == "__main__": main()
