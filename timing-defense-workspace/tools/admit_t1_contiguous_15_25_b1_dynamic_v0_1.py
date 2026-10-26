#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

# Reuse the exact admitted transition runner + settlement bridge.  The bridge patches
# runner.simulate_stage so delayed combat events must drain while Stage-local residue
# is cleared at STAGE_SETTLED.
import run_t1_transition_slice_microsim_settlement_fix_v0_1 as settlement_bridge

r = settlement_bridge.runner

EXPECTED_MATERIALIZED_SHA256 = "729553556c8753fc45a3ecd520176dcdaaa4c2b0b68cfc54b4038ec73fee3e9d"
WINDOW = list(range(15, 26))
SEED_DEFAULT = "101,211,307,409,503"
CONTINUITY_KEYS = (
    "baseHp",
    "baseMaxHp",
    "wallDeficit",
    "combo",
    "charge",
    "judgmentRng",
    "combatProcRng",
)
VARIANTS = (
    {"id": "L16_EARLY18__L21_ACTIVE25", "lv16BeforeStage": 18, "lv21ActiveAt25": True},
    {"id": "L16_EARLY18__L21_AFTER25", "lv16BeforeStage": 18, "lv21ActiveAt25": False},
    {"id": "L16_LATE21__L21_ACTIVE25", "lv16BeforeStage": 21, "lv21ActiveAt25": True},
    {"id": "L16_LATE21__L21_AFTER25", "lv16BeforeStage": 21, "lv21ActiveAt25": False},
)


def sha_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def avg(values):
    vals = [float(x) for x in values]
    return round(statistics.fmean(vals), 6) if vals else None


def active_for(stage: int, variant: dict) -> list[int]:
    # Lv6/Lv11 are inherited diagnostic priors from the existing Stage18 paired
    # contract. Lv16/Lv21 are bounded reach-band sensitivity states, not EXP freezes.
    active = {6, 11}
    if stage >= int(variant["lv16BeforeStage"]):
        active.add(16)
    if bool(variant["lv21ActiveAt25"]) and stage >= 25:
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
        row["skillState"]["b1Variant"] = variant["id"]
        row["skillState"]["lv16BeforeStage"] = int(variant["lv16BeforeStage"])
        row["skillState"]["lv21ActiveAt25"] = bool(variant["lv21ActiveAt25"])
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
    all_rows = []
    for case in cases:
        by_variant[case["variant"]].append(case)
        all_rows.extend(case["results"])

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
            }
        variant_summary[variant_id] = {
            "cases": len(rows),
            "completedThrough25": sum(case["stagesExecuted"] == WINDOW for case in rows),
            "terminalStatusCounts": dict(sorted(Counter(case["finalRunState"]["status"] for case in rows).items())),
            "meanFinalBaseHp": avg(case["finalRunState"]["baseHp"] for case in rows),
            "stages": stage_summary,
        }

    # Focused paired deltas.  Comparisons are restricted to matching class+seed and
    # matching the other milestone condition.
    keyed = {(c["variant"], c["class"], c["seed"]): c for c in cases}

    def row_at(case, stage):
        return next((x for x in case["results"] if int(x["stage"]) == stage), None)

    lv16_deltas = []
    for lv21_state in (True, False):
        suffix = "ACTIVE25" if lv21_state else "AFTER25"
        early_id = f"L16_EARLY18__L21_{suffix}"
        late_id = f"L16_LATE21__L21_{suffix}"
        for cls in r.CLASSES:
            seeds = sorted({c["seed"] for c in cases if c["class"] == cls})
            for seed in seeds:
                early = keyed.get((early_id, cls, seed))
                late = keyed.get((late_id, cls, seed))
                if not early or not late:
                    continue
                for stage in (18, 20):
                    a, b = row_at(early, stage), row_at(late, stage)
                    if a is None or b is None:
                        continue
                    lv16_deltas.append({
                        "class": cls,
                        "seed": seed,
                        "lv21Condition": suffix,
                        "stage": stage,
                        "earlyMinusLateWallDamage": round(float(a["wallDamage"]) - float(b["wallDamage"]), 6),
                        "earlyMinusLateActions": int(a["rootTimingActionCount"]) - int(b["rootTimingActionCount"]),
                        "earlyMinusLateSettledTime": round(float(a["stageSettledTime"]) - float(b["stageSettledTime"]), 6),
                    })

    lv21_deltas = []
    for lv16_before, prefix in ((18, "L16_EARLY18"), (21, "L16_LATE21")):
        active_id = f"{prefix}__L21_ACTIVE25"
        off_id = f"{prefix}__L21_AFTER25"
        for cls in r.CLASSES:
            seeds = sorted({c["seed"] for c in cases if c["class"] == cls})
            for seed in seeds:
                on, off = keyed.get((active_id, cls, seed)), keyed.get((off_id, cls, seed))
                if not on or not off:
                    continue
                a, b = row_at(on, 25), row_at(off, 25)
                if a is None or b is None:
                    continue
                lv21_deltas.append({
                    "class": cls,
                    "seed": seed,
                    "lv16BeforeStage": lv16_before,
                    "activeMinusOffWallDamage": round(float(a["wallDamage"]) - float(b["wallDamage"]), 6),
                    "activeMinusOffActions": int(a["rootTimingActionCount"]) - int(b["rootTimingActionCount"]),
                    "activeMinusOffSettledTime": round(float(a["stageSettledTime"]) - float(b["stageSettledTime"]), 6),
                })

    relief_rows = []
    for case in cases:
        s24, s25 = row_at(case, 24), row_at(case, 25)
        if s24 is None or s25 is None:
            continue
        relief_rows.append({
            "variant": case["variant"],
            "class": case["class"],
            "seed": case["seed"],
            "stage25Minus24WallDamage": round(float(s25["wallDamage"]) - float(s24["wallDamage"]), 6),
            "stage25Minus24Actions": int(s25["rootTimingActionCount"]) - int(s24["rootTimingActionCount"]),
            "stage25Minus24SettledTime": round(float(s25["stageSettledTime"]) - float(s24["stageSettledTime"]), 6),
        })

    return {
        "variants": variant_summary,
        "lv16FocusedDeltas": lv16_deltas,
        "lv21Stage25Deltas": lv21_deltas,
        "stage25Vs24ReliefDeltas": relief_rows,
        "overall": {
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
    materialized_sha = sha_bytes(materialized_path)
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
        "version": "t1-contiguous-15-25-b1-dynamic-admission-v0.1",
        "status": "PASS_DYNAMIC_DIAGNOSTIC_ONLY" if admission["pass"] else "FIDELITY_FAIL_NO_BALANCE_INTERPRETATION",
        "authorityBoundary": {
            "lv16Reach": "Stage18-21 calibration-candidate band; tested at band edges 18 and 21",
            "lv21Reach": "Stage25-28 calibration-candidate band; within this Stage15-25 window tested as ACTIVE-at-25 vs AFTER-25",
            "stage15PriorSkillState": "[Lv6,Lv11] inherited from existing Stage18 paired diagnostic context; not EXP freeze",
            "expNumericalFreeze": False,
            "skillNumericalFreeze": False,
            "stage16_17CandidateAdopted": False,
            "productionGameplayChange": False,
            "fullT1ExactRecipeFreeze": False,
        },
        "sourceIdentity": {
            "baseRecipeSha256": sha_bytes(base_path),
            "materializedStage15to25Sha256": materialized_sha,
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
        "materializedStage15to25Sha256": materialized_sha,
        "caseCount": len(cases),
        "overall": result.get("summary", {}).get("overall", {}),
    }, indent=2, sort_keys=True))
    raise SystemExit(0 if admission["pass"] else 1)


if __name__ == "__main__":
    main()
