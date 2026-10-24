#!/usr/bin/env python3
from __future__ import annotations
from t1_transition_microsim_core_v0_1 import *
from t1_transition_microsim_skills_v0_1 import *
from t1_transition_microsim_engine_v0_1 import *

def active_for_stage(base_active, stage, lv31_before=None):
    active = set(base_active)
    if lv31_before is not None and stage >= lv31_before:
        active.add(31)
    return sorted(active)


def execute_chain(runtime, recipe_by_stage, cls, base_seed, stages, base_active, lv31_before=None):
    initial_level = 31 if 31 in base_active else max(base_active) if base_active else 1
    run = new_run(runtime, cls, base_seed, initial_level, base_active)
    results = []
    continuity_errors = []
    previous_exit = None

    for stage in stages:
        if run["status"] == "FAILED":
            break
        run["activeMilestones"] = active_for_stage(base_active, stage, lv31_before)
        run["level"] = 31 if 31 in run["activeMilestones"] else max(run["activeMilestones"] or [1])
        result = simulate_stage(run, recipe_by_stage[stage], runtime)
        result["skillState"]["lv31ActivationBeforeStage"] = lv31_before
        if previous_exit is not None:
            entry = result["entryState"]
            for key in (
                "baseHp",
                "baseMaxHp",
                "wallDeficit",
                "combo",
                "charge",
                "judgmentRng",
                "combatProcRng",
            ):
                if entry[key] != previous_exit[key]:
                    continuity_errors.append(
                        f"{cls}/seed{base_seed}/stage{stage}:{key} {entry[key]} != {previous_exit[key]}"
                    )
        previous_exit = result["exitState"]
        results.append(result)

    return {
        "class": cls,
        "seed": base_seed,
        "stagesRequested": list(stages),
        "stagesExecuted": [x["stage"] for x in results],
        "lv31ActivationBeforeStage": lv31_before,
        "results": results,
        "continuityErrors": continuity_errors,
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


def execute_pair(runtime, recipe, cls, base_seed, milestone_level, prior_active):
    baseline = new_run(runtime, cls, base_seed, milestone_level, prior_active)
    invariant_state = {
        k: copy.deepcopy(v)
        for k, v in baseline.items()
        if k not in ("activeMilestones", "level", "ledger")
    }
    variants = {}
    for label, enabled in (("OFF", False), ("ON", True)):
        run = copy.deepcopy(baseline)
        active = set(prior_active)
        if enabled:
            active.add(milestone_level)
        run["activeMilestones"] = sorted(active)
        run["level"] = milestone_level
        result = simulate_stage(run, recipe, runtime)
        result["skillState"]["testedMilestone"] = milestone_level
        result["skillState"]["testedSkillState"] = label
        variants[label] = result
    return {
        "class": cls,
        "seed": base_seed,
        "stage": int(recipe["stage"]),
        "testedMilestone": milestone_level,
        "recipeId": recipe["id"],
        "recipeDigest": sha256_obj(recipe),
        "initialLifecycleStateDigest": sha256_obj(invariant_state),
        "pairIsolation": {
            "sameRecipeDigest": variants["OFF"]["recipeDigest"] == variants["ON"]["recipeDigest"],
            "sameInitialBaseHp": variants["OFF"]["entryState"]["baseHp"]
            == variants["ON"]["entryState"]["baseHp"],
            "sameInitialCombo": variants["OFF"]["entryState"]["combo"]
            == variants["ON"]["entryState"]["combo"],
            "sameInitialCharge": variants["OFF"]["entryState"]["charge"]
            == variants["ON"]["entryState"]["charge"],
            "sameInitialJudgmentRng": variants["OFF"]["entryState"]["judgmentRng"]
            == variants["ON"]["entryState"]["judgmentRng"],
            "sameInitialCombatProcRng": variants["OFF"]["entryState"]["combatProcRng"]
            == variants["ON"]["entryState"]["combatProcRng"],
            "onlyTestedMilestoneDiffers": (
                set(variants["ON"]["skillState"]["activeMilestones"])
                - set(variants["OFF"]["skillState"]["activeMilestones"])
            )
            == {milestone_level},
        },
        "variants": variants,
    }


def digest_case(case):
    return sha256_obj(case)


def replay_check(fn):
    a = fn()
    b = fn()
    return a, digest_case(a) == digest_case(b), digest_case(a), digest_case(b)


def build_cases(recipe_doc, runtime, seeds):
    by_stage = {int(r["stage"]): r for r in recipe_doc["recipes"]}
    output = {
        "A_RUNNER_TEACH_X_LV6": [],
        "B_BRUTE_FIRST_MIX_X_LV16": [],
        "C_STAGE20_23": [],
        "D_STAGE39_45": [],
        "E_STAGE46_50": [],
    }
    replay_failures = []
    pair_failures = []
    lifecycle_failures = []

    for cls in CLASSES:
        for base_seed in seeds:
            for group, stage, milestone_level, prior in (
                ("A_RUNNER_TEACH_X_LV6", 5, 6, []),
                ("B_BRUTE_FIRST_MIX_X_LV16", 18, 16, [6, 11]),
            ):
                case, ok, h1, h2 = replay_check(
                    lambda cls=cls, base_seed=base_seed, stage=stage, milestone_level=milestone_level, prior=prior:
                    execute_pair(runtime, by_stage[stage], cls, base_seed, milestone_level, prior)
                )
                case["deterministicReplay"] = {"pass": ok, "digestA": h1, "digestB": h2}
                output[group].append(case)
                if not ok:
                    replay_failures.append(f"{group}/{cls}/{base_seed}")
                if not all(case["pairIsolation"].values()):
                    pair_failures.append(f"{group}/{cls}/{base_seed}")

            c_case, ok, h1, h2 = replay_check(
                lambda cls=cls, base_seed=base_seed:
                execute_chain(runtime, by_stage, cls, base_seed, [20, 21, 22, 23], [6, 11, 16])
            )
            c_case["deterministicReplay"] = {"pass": ok, "digestA": h1, "digestB": h2}
            output["C_STAGE20_23"].append(c_case)
            if not ok:
                replay_failures.append(f"C/{cls}/{base_seed}")
            if c_case["continuityErrors"]:
                lifecycle_failures.extend(c_case["continuityErrors"])

            for activation in (41, 43, 45):
                d_case, ok, h1, h2 = replay_check(
                    lambda cls=cls, base_seed=base_seed, activation=activation:
                    execute_chain(
                        runtime,
                        by_stage,
                        cls,
                        base_seed,
                        [39, 40, 41, 42, 43, 44, 45],
                        [6, 11, 16, 21, 26],
                        activation,
                    )
                )
                d_case["deterministicReplay"] = {"pass": ok, "digestA": h1, "digestB": h2}
                output["D_STAGE39_45"].append(d_case)
                if not ok:
                    replay_failures.append(f"D{activation}/{cls}/{base_seed}")
                if d_case["continuityErrors"]:
                    lifecycle_failures.extend(d_case["continuityErrors"])

            e_case, ok, h1, h2 = replay_check(
                lambda cls=cls, base_seed=base_seed:
                execute_chain(
                    runtime,
                    by_stage,
                    cls,
                    base_seed,
                    [46, 47, 48, 49, 50],
                    [6, 11, 16, 21, 26, 31],
                )
            )
            e_case["deterministicReplay"] = {"pass": ok, "digestA": h1, "digestB": h2}
            output["E_STAGE46_50"].append(e_case)
            if not ok:
                replay_failures.append(f"E/{cls}/{base_seed}")
            if e_case["continuityErrors"]:
                lifecycle_failures.extend(e_case["continuityErrors"])

    return output, replay_failures, pair_failures, lifecycle_failures


def admission_from_results(groups, replay_failures, pair_failures, lifecycle_failures):
    stage_rows = []
    for group_value in groups.values():
        for case in group_value:
            if "variants" in case:
                stage_rows.extend(case["variants"].values())
            else:
                stage_rows.extend(case["results"])

    stage_settled_or_failed = all(
        row["invariants"]["stageSettled"] or row["combatOutcome"] == "FAILED_WALL_DESTROYED"
        for row in stage_rows
    )
    no_enemy_carry = all(row["invariants"]["noEnemyCarry"] for row in stage_rows)
    no_transient_leakage = all(row["invariants"]["noTransientLeakage"] for row in stage_rows)
    explicit_skill_trace = all(
        "activeMilestones" in row["skillState"] and "class" in row["skillState"] for row in stage_rows
    )

    return {
        "exactRecipeIdentity": True,
        "stageSettledOrTerminalFailure": stage_settled_or_failed,
        "noEnemyCarryAtSettledBoundary": no_enemy_carry,
        "noTransientLeakageAtSettledBoundary": no_transient_leakage,
        "persistentStateContinuity": not lifecycle_failures,
        "deterministicReplay": not replay_failures,
        "pairedIsolation": not pair_failures,
        "explicitSkillStateTrace": explicit_skill_trace,
        "replayFailures": replay_failures,
        "pairFailures": pair_failures,
        "lifecycleFailures": lifecycle_failures,
    }


def summarize(groups):
    out = {}
    for name, cases in groups.items():
        rows = []
        for case in cases:
            if "variants" in case:
                for variant, row in case["variants"].items():
                    rows.append(
                        {
                            "class": case["class"],
                            "seed": case["seed"],
                            "variant": variant,
                            "stage": row["stage"],
                            "outcome": row["combatOutcome"],
                            "wallReserve": row["wallReserve"],
                            "actions": row["rootTimingActionCount"],
                            "settledTime": row["stageSettledTime"],
                        }
                    )
            else:
                for row in case["results"]:
                    rows.append(
                        {
                            "class": case["class"],
                            "seed": case["seed"],
                            "variant": case.get("lv31ActivationBeforeStage"),
                            "stage": row["stage"],
                            "outcome": row["combatOutcome"],
                            "wallReserve": row["wallReserve"],
                            "actions": row["rootTimingActionCount"],
                            "settledTime": row["stageSettledTime"],
                        }
                    )
        out[name] = rows
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--recipes",
        default="legacy-game-structure/data/t1_representative_transition_slice_recipes_v0_1.yaml",
    )
    ap.add_argument(
        "--p3-fixture",
        default="legacy-game-structure/data/p3_ten_stage_fixture_v0_1.json",
    )
    ap.add_argument(
        "--p4d2-base",
        default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json",
    )
    ap.add_argument(
        "--p4d2-temporal",
        default="legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json",
    )
    ap.add_argument("--seeds", default="101,211,307")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--print-full", action="store_true")
    args = ap.parse_args()

    recipe_path = Path(args.recipes)
    recipe_bytes = recipe_path.read_bytes()
    recipe_doc = yaml.safe_load(recipe_bytes.decode("utf-8"))
    static_errors = static_recipe_gate(recipe_doc)
    if static_errors:
        raise RunnerFidelityError("static recipe gate failed: " + "; ".join(static_errors))

    p3_fixture = load_json(args.p3_fixture)
    p4d2_base = load_json(args.p4d2_base)
    p4d2_temporal = load_json(args.p4d2_temporal)
    runtime = build_runtime(recipe_doc, p3_fixture, p4d2_base, p4d2_temporal)
    seeds = tuple(int(x.strip()) for x in args.seeds.split(",") if x.strip())

    groups, replay_failures, pair_failures, lifecycle_failures = build_cases(
        recipe_doc, runtime, seeds
    )
    admission = admission_from_results(
        groups, replay_failures, pair_failures, lifecycle_failures
    )
    admission["pass"] = all(
        bool(v)
        for k, v in admission.items()
        if k
        in {
            "exactRecipeIdentity",
            "stageSettledOrTerminalFailure",
            "noEnemyCarryAtSettledBoundary",
            "noTransientLeakageAtSettledBoundary",
            "persistentStateContinuity",
            "deterministicReplay",
            "pairedIsolation",
            "explicitSkillStateTrace",
        }
    )

    result = {
        "version": "t1-transition-slice-microsim-v0.1",
        "status": (
            "ADMISSION_PASS_DYNAMIC_DIAGNOSTIC_ONLY"
            if admission["pass"]
            else "RUNNER_FIDELITY_FAIL_NO_BALANCE_INTERPRETATION"
        ),
        "authorityBoundary": {
            "sourceSemantics": {
                "lifecycle": "72/76 and P3 persistent kernel semantics",
                "lv6To21": "PLAYER_SKILL_AUTHORITY_REVIEW legacy parity inputs",
                "lv26": "88 user-approved structural semantics with provisional coefficients",
                "lv31": "91 user-approved structural direction with P4D2 provisional centers",
                "n3": "N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21",
            },
            "productionNumericalFreeze": False,
            "fullT1ExactRecipeFreeze": False,
            "classBuffNerfAuthorized": False,
            "shopExpCoupled": False,
            "passiveAttackCoupled": False,
            "startingWallHp": runtime["startingWallHp"],
            "startingWallHpStatus": "P4D2_DIAGNOSTIC_ANCHOR_NOT_PRODUCTION_FREEZE",
            "skillSemantics": "Lv6-21 legacy parity; Lv26 structural approved provisional coefficients; Lv31 P4D2 provisional centers",
        },
        "sourceIdentity": {
            "recipePath": str(recipe_path),
            "recipeSourceSha256": sha256_bytes(recipe_bytes),
            "recipeVersion": recipe_doc["version"],
        },
        "runnerPolicy": {
            "safetyCapMs": SAFETY_CAP_MS,
            "safetyCapBehavior": "RAISE_RUNNER_FIDELITY_ERROR_NEVER_DELETE_ENEMIES_OR_ADVANCE_STAGE",
            "supportedFailureClassifications": [
                "RUNNER_FIDELITY_FAIL",
                "LIFECYCLE_INVARIANT_FAIL",
                "AUTHORING_COLLISION",
                "CLASS_OPPORTUNITY_WEAKNESS",
                "CHRONOLOGY_ORDERING_EFFECT",
                "SCALAR_SENSITIVITY_CANDIDATE",
                "PASS_WITH_WATCH",
            ],
            "metricDefinitions": {
                "frontlineBlockTime": "seconds with BRUTE as current frontmost T1 target",
                "backlineExposure": "seconds with BRUTE frontmost while at least one other enemy remains behind",
                "spawnToFirstContact": "first authored spawn to first wall contact; null if no enemy reaches wall",
                "controlValue": "separate raw control/protection components; not a fairness score",
            },
        },
        "runtime": runtime,
        "seeds": list(seeds),
        "admission": admission,
        "summary": summarize(groups),
        "groups": groups,
    }
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    if args.print_full:
        print(text)
    else:
        print(
            json.dumps(
                {
                    "status": result["status"],
                    "recipeSourceSha256": result["sourceIdentity"]["recipeSourceSha256"],
                    "seeds": result["seeds"],
                    "admission": result["admission"],
                    "jsonOut": args.json_out or None,
                },
                indent=2,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
