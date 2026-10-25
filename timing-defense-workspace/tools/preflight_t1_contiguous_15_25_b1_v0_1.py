#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

import yaml

EXPECTED_A = {
    "a1": "44616732b4cbba8bc52df294d98e0ab485b400d7ec7e9b9bfdd9f3fe32d2910d",
    "a2": "2d3bf477e80617c0d26d2c349588caa446195b39c2581df0f11dd29eb1f37f8d",
    "a3": "30860f1ff0911ff121491e62a5fa2ede84b43c6e4ce9bd7ec5f0f8a68d9592e6",
    "a4": "93b9c785ca800ad97ad0149e9931e1d43b58328744dbb5867fdc5b9261dfef36",
}
EXPECTED_BASE = "3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf"
ALLOWED = {"GRUNT", "RUNNER", "BRUTE"}
TARGETS = [16, 17]
WINDOW = list(range(15, 26))


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
    ap.add_argument("--base", required=True)
    ap.add_argument("--a1", required=True)
    ap.add_argument("--a2", required=True)
    ap.add_argument("--a3", required=True)
    ap.add_argument("--a4", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--materialized-out", required=True)
    args = ap.parse_args()

    paths = {k: Path(getattr(args, k)) for k in ("base", "a1", "a2", "a3", "a4", "candidate")}
    docs = {k: load(v) for k, v in paths.items()}
    errors: list[str] = []
    warnings: list[str] = []

    if sha(paths["base"]) != EXPECTED_BASE:
        errors.append("base-sha-drift")
    for k in ("a1", "a2", "a3", "a4"):
        if sha(paths[k]) != EXPECTED_A[k]:
            errors.append(f"{k}-sha-drift")
        ref = docs["candidate"].get("adoptedWaveA", {}).get(k, {}).get("sha256")
        if ref != EXPECTED_A[k]:
            errors.append(f"candidate-{k}-reference-drift")

    scope = docs["candidate"].get("scope", {})
    if scope.get("intendedContiguousWindow") != [15, 25]:
        errors.append("contiguous-window-not-15-25")
    if scope.get("addedStages") != TARGETS:
        errors.append("added-stages-not-16-17")
    if scope.get("existingExactStages") != [15, 18, 19, 20, 21, 22, 23, 24, 25]:
        errors.append("existing-exact-stage-set-drift")
    if scope.get("allowedMonsters") != ["GRUNT", "RUNNER", "BRUTE"]:
        errors.append("monster-vocabulary-drift")
    for flag in ("monsterScalarChange", "classScalarChange", "shopExpPxpChange", "productionGameplayChange", "fullT1ExactRecipeFreeze", "candidateAdopted"):
        if scope.get(flag) is not False:
            errors.append(f"scope-{flag}-must-be-false")
    if float(scope.get("physicalSpawnX", -1)) != 0.92 or scope.get("midfieldPopIn") is not False:
        errors.append("spawn-entry-guard-drift")

    base = by_stage(docs["base"].get("recipes", []))
    a2 = by_stage(docs["a2"].get("stageAdditions", []))
    a3 = by_stage(docs["a3"].get("stageAdditions", []))
    additions = by_stage(docs["candidate"].get("stageAdditions", []))
    if sorted(additions) != TARGETS:
        errors.append("candidate-stage-set-not-16-17")

    expected_sources = {
        15: a2.get(15),
        18: base.get(18),
        19: a2.get(19),
        20: base.get(20),
        21: base.get(21),
        22: base.get(22),
        23: base.get(23),
        24: a3.get(24),
        25: a3.get(25),
    }
    for stage, obj in expected_sources.items():
        if obj is None:
            errors.append(f"missing-authority-stage-{stage}")

    expected_meta = {
        16: ("E03", ["E03"], "F02", "CD02", "C1", ["BULWARK"]),
        17: ("E01", ["E01"], "F01", "CD03", "C1", ["BASELINE"]),
    }
    for stage in TARGETS:
        obj = additions.get(stage, {})
        want = expected_meta[stage]
        got = (obj.get("archetype"), obj.get("componentArchetypes"), obj.get("formation"), obj.get("cadence"), obj.get("complexity"), obj.get("pressureTags"))
        if got != want:
            errors.append(f"stage{stage}-skeleton-signature-drift")
        if float(obj.get("entryBaseX", -1)) != 0.92:
            errors.append(f"stage{stage}-entry-x-drift")
        spawns = obj.get("spawns", [])
        if any(str(x.get("type")) not in ALLOWED for x in spawns):
            errors.append(f"stage{stage}-illegal-monster")
        if any(not (0.0 <= float(x.get("y", -1)) <= 1.0) for x in spawns):
            errors.append(f"stage{stage}-y-out-of-range")
        if max_density(spawns, 4000) > 8:
            errors.append(f"stage{stage}-max4-exceeds-8")

    s16 = additions.get(16, {}).get("spawns", [])
    if [x.get("type") for x in s16] != ["BRUTE"] * 4:
        errors.append("stage16-not-pure-brute4")
    if [int(x.get("tMs", -1)) for x in s16] != [0, 1400, 2800, 4200]:
        errors.append("stage16-drip-chronology-drift")
    if s16 and max(float(x["y"]) for x in s16) - min(float(x["y"]) for x in s16) > 0.05:
        errors.append("stage16-f02-line-too-wide")
    s15 = a2.get(15, {}).get("spawns", [])
    if len(s16) <= len(s15):
        errors.append("stage16-not-step-up-from-stage15-teach")

    s17 = additions.get(17, {}).get("spawns", [])
    if [x.get("type") for x in s17] != ["GRUNT"] * 5:
        errors.append("stage17-not-grunt5-recovery")
    if [int(x.get("tMs", -1)) for x in s17] != [0, 300, 600, 3000, 3300]:
        errors.append("stage17-wave-chronology-drift")
    if any(x.get("type") in {"BRUTE", "RUNNER"} for x in s17):
        errors.append("stage17-new-threat-in-recovery")
    if max_density(s17, 4000) > 5:
        errors.append("stage17-recovery-density-too-high")

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
        "version": "t1-contiguous-15-25-b1-materialized-v0.1",
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
        "contiguous15to25": sorted(materialized) == WINDOW,
        "authorityPreserved": not any(e.startswith("authority-stage-") for e in errors),
        "stageStatic": stage_stats,
    }
    Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
