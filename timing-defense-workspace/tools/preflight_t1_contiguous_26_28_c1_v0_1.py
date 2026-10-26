#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

import yaml

EXPECTED = {
    "plan": "3ed5001b7755a5b0f9805d67a40abf78e7309845473253b01142a0fa20370a18",
    "base": "3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf",
    "a2": "2d3bf477e80617c0d26d2c349588caa446195b39c2581df0f11dd29eb1f37f8d",
    "a3": "30860f1ff0911ff121491e62a5fa2ede84b43c6e4ce9bd7ec5f0f8a68d9592e6",
    "b1": "b9abc507c5ccdc20bc19c5681ba92cead920326fa9d04c1acf5b2ed90ff91465",
}
TARGETS = [26, 27, 28]
WINDOW = list(range(15, 32))
ALLOWED = {"GRUNT", "RUNNER", "BRUTE"}


def load(path: Path):
    return yaml.safe_load(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def max_density(spawns: list[dict], window_ms: int) -> int:
    times = [int(x["tMs"]) for x in spawns]
    return max((sum(1 for t in times if s <= t < s + window_ms) for s in times), default=0)


def digest_obj(obj) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def by_stage(rows: list[dict]) -> dict[int, dict]:
    return {int(x["stage"]): x for x in rows}


def main() -> None:
    ap = argparse.ArgumentParser()
    for name in ("plan", "base", "a2", "a3", "b1", "candidate"):
        ap.add_argument(f"--{name}", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--materialized-out", required=True)
    args = ap.parse_args()

    paths = {k: Path(getattr(args, k)) for k in ("plan", "base", "a2", "a3", "b1", "candidate")}
    docs = {k: load(v) for k, v in paths.items()}
    errors: list[str] = []
    warnings: list[str] = []

    for key, expected_sha in EXPECTED.items():
        if sha(paths[key]) != expected_sha:
            errors.append(f"{key}-sha-drift")

    plan = docs["plan"]
    if plan.get("structuralAuthority", {}).get("staticAudit") != "../162_T1_STAGE_SIGNATURE_STATIC_CONSISTENCY_AUDIT_V0_1.md":
        errors.append("plan-static-audit-reference-drift")
    if plan.get("scope", {}).get("targetStages") != TARGETS:
        errors.append("plan-target-stage-drift")
    if plan.get("scope", {}).get("intendedContiguousWindowAfterFutureAdoption") != [15, 31]:
        errors.append("plan-contiguous-window-drift")

    candidate = docs["candidate"]
    if candidate.get("plan", {}).get("sha256") != EXPECTED["plan"]:
        errors.append("candidate-plan-reference-drift")
    auth = candidate.get("authority", {})
    if auth.get("baseRecipe", {}).get("sha256") != EXPECTED["base"]:
        errors.append("candidate-base-reference-drift")
    if auth.get("adoptedWaveA", {}).get("a2", {}).get("sha256") != EXPECTED["a2"]:
        errors.append("candidate-a2-reference-drift")
    if auth.get("adoptedWaveA", {}).get("a3", {}).get("sha256") != EXPECTED["a3"]:
        errors.append("candidate-a3-reference-drift")
    if auth.get("adoptedB1", {}).get("candidate", {}).get("sha256") != EXPECTED["b1"]:
        errors.append("candidate-b1-reference-drift")

    scope = candidate.get("scope", {})
    if scope.get("intendedContiguousWindowAfterFutureAdoption") != [15, 31]:
        errors.append("contiguous-window-not-15-31")
    if scope.get("addedStages") != TARGETS:
        errors.append("added-stages-not-26-28")
    if scope.get("existingExactStages") != [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 29, 30, 31]:
        errors.append("existing-exact-stage-set-drift")
    if scope.get("allowedMonsters") != ["GRUNT", "RUNNER", "BRUTE"]:
        errors.append("monster-vocabulary-drift")
    for flag in ("monsterScalarChange", "classScalarChange", "shopExpPxpChange",
                 "productionGameplayChange", "fullT1ExactRecipeFreeze", "candidateAdopted"):
        if scope.get(flag) is not False:
            errors.append(f"scope-{flag}-must-be-false")
    if float(scope.get("physicalSpawnX", -1)) != 0.92 or scope.get("midfieldPopIn") is not False:
        errors.append("spawn-entry-guard-drift")

    base = by_stage(docs["base"].get("recipes", []))
    a2 = by_stage(docs["a2"].get("stageAdditions", []))
    a3 = by_stage(docs["a3"].get("stageAdditions", []))
    b1 = by_stage(docs["b1"].get("stageAdditions", []))
    additions = by_stage(candidate.get("stageAdditions", []))
    if sorted(additions) != TARGETS:
        errors.append("candidate-stage-set-not-26-28")

    expected_sources = {
        15: a2.get(15),
        16: b1.get(16),
        17: b1.get(17),
        18: base.get(18),
        19: a2.get(19),
        20: base.get(20),
        21: base.get(21),
        22: base.get(22),
        23: base.get(23),
        24: a3.get(24),
        25: a3.get(25),
        29: a3.get(29),
        30: a3.get(30),
        31: a3.get(31),
    }
    for stage, obj in expected_sources.items():
        if obj is None:
            errors.append(f"missing-authority-stage-{stage}")

    expected_meta = {
        26: ("E03", ["E03"], "F01", ["F01"], "CD02", "C1", ["BULWARK"]),
        27: ("E02", ["E02"], "F04", ["F04"], "CD03", "C1", ["RUSH"]),
        28: ("E01", ["E01"], "F03", ["F03"], "CD03", "C1", ["BASELINE", "FLOOD"]),
    }
    for stage in TARGETS:
        obj = additions.get(stage, {})
        want = expected_meta[stage]
        got = (
            obj.get("archetype"),
            obj.get("componentArchetypes"),
            obj.get("formation"),
            obj.get("formationSet"),
            obj.get("cadence"),
            obj.get("complexity"),
            obj.get("pressureTags"),
        )
        if got != want:
            errors.append(f"stage{stage}-skeleton-signature-drift")
        if float(obj.get("entryBaseX", -1)) != 0.92:
            errors.append(f"stage{stage}-entry-x-drift")

        spawns = obj.get("spawns", [])
        times = [int(x.get("tMs", -1)) for x in spawns]
        if times != sorted(times) or len(times) != len(set(times)) or any(t < 0 for t in times):
            errors.append(f"stage{stage}-timestamp-order-invalid")
        if any(str(x.get("type")) not in ALLOWED for x in spawns):
            errors.append(f"stage{stage}-illegal-monster")
        if any(not (0.0 <= float(x.get("y", -1)) <= 1.0) for x in spawns):
            errors.append(f"stage{stage}-y-out-of-range")
        if max_density(spawns, 4000) > 8:
            errors.append(f"stage{stage}-max4-exceeds-8")

    s26 = additions.get(26, {}).get("spawns", [])
    if Counter(str(x.get("type")) for x in s26) != Counter({"GRUNT": 3, "BRUTE": 2}):
        errors.append("stage26-not-e03-medium-composition")
    if [int(x.get("tMs", -1)) for x in s26] != [0, 800, 1600, 2400, 3200]:
        errors.append("stage26-cd02-chronology-drift")
    s26_gaps = [int(s26[i + 1]["tMs"]) - int(s26[i]["tMs"]) for i in range(len(s26) - 1)]
    if s26_gaps and any(not (650 <= gap <= 900) for gap in s26_gaps):
        errors.append("stage26-cd02-gap-out-of-envelope")
    if s26 and max(float(x["y"]) for x in s26) - min(float(x["y"]) for x in s26) > 0.06:
        errors.append("stage26-f01-line-too-wide")

    s27 = additions.get(27, {}).get("spawns", [])
    if Counter(str(x.get("type")) for x in s27) != Counter({"RUNNER": 4, "GRUNT": 3}):
        errors.append("stage27-not-e02-medium-composition")
    if [int(x.get("tMs", -1)) for x in s27] != [0, 250, 500, 2000, 2250, 3750, 4000]:
        errors.append("stage27-cd03-chronology-drift")
    if s27 and max(float(x["y"]) for x in s27) - min(float(x["y"]) for x in s27) < 0.30:
        errors.append("stage27-f04-scatter-too-narrow")

    s28 = additions.get(28, {}).get("spawns", [])
    if Counter(str(x.get("type")) for x in s28) != Counter({"GRUNT": 6}):
        errors.append("stage28-not-e01-medium-composition")
    if [int(x.get("tMs", -1)) for x in s28] != [0, 250, 500, 2000, 2250, 2500]:
        errors.append("stage28-cd03-chronology-drift")
    if s28 and max(float(x["y"]) for x in s28) - min(float(x["y"]) for x in s28) > 0.06:
        errors.append("stage28-f03-cluster-too-wide")

    s24 = expected_sources.get(24, {}).get("spawns", []) if expected_sources.get(24) else []
    if len(s28) >= len(s24):
        errors.append("stage28-not-below-stage24-high-pressure-count")
    if max_density(s28, 4000) >= max_density(s24, 4000):
        errors.append("stage28-not-below-stage24-high-pressure-density")

    s25 = expected_sources.get(25, {}).get("spawns", []) if expected_sources.get(25) else []
    if len(s26) <= len(s25):
        errors.append("stage26-not-step-up-from-stage25-buffer")

    s29_obj = expected_sources.get(29) or {}
    s29 = s29_obj.get("spawns", [])
    if (
        s29_obj.get("complexity") != "C2"
        or s29_obj.get("formation") != "F08"
        or set(s29_obj.get("pressureTags", [])) != {"RUSH", "BULWARK"}
        or len(s29) <= len(s28)
    ):
        errors.append("stage29-synthesis-no-longer-clear-step-up")

    materialized: dict[int, dict] = {}
    for stage, obj in expected_sources.items():
        if obj is not None:
            materialized[stage] = copy.deepcopy(obj)
    for stage, obj in additions.items():
        if stage in materialized:
            errors.append(f"duplicate-stage-{stage}")
        materialized[stage] = copy.deepcopy(obj)

    if sorted(materialized) != WINDOW:
        errors.append(f"materialized-window-incomplete:{sorted(materialized)}")

    for stage, original in expected_sources.items():
        if original is not None and materialized.get(stage) != original:
            errors.append(f"authority-stage-{stage}-mutated")

    stage_stats = {}
    for stage in sorted(materialized):
        spawns = materialized[stage].get("spawns", [])
        stage_stats[str(stage)] = {
            "authored": len(spawns),
            "max4s": max_density(spawns, 4000),
            "max6s": max_density(spawns, 6000),
            "types": dict(sorted(Counter(str(x["type"]) for x in spawns).items())),
            "digest": digest_obj(materialized[stage]),
        }

    out_doc = {
        "version": "t1-contiguous-15-31-c1-materialized-v0.1",
        "status": "PASS" if not errors else "FAIL",
        "recipes": [materialized[s] for s in sorted(materialized)],
    }
    Path(args.materialized_out).write_text(yaml.safe_dump(out_doc, sort_keys=False))
    materialized_sha = sha(Path(args.materialized_out))

    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "candidateSha256": sha(paths["candidate"]),
        "materializedWindowSha256": materialized_sha,
        "windowStages": sorted(materialized),
        "contiguous15to31": sorted(materialized) == WINDOW,
        "authorityPreserved": not any(e.startswith("authority-stage-") for e in errors),
        "referenceIntegrity": "PASS" if "plan-static-audit-reference-drift" not in errors else "FAIL",
        "stageStatic": stage_stats,
    }
    Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
