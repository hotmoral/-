#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

import yaml

EXPECTED_SHA256 = {
    "base": "3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf",
    "a2": "2d3bf477e80617c0d26d2c349588caa446195b39c2581df0f11dd29eb1f37f8d",
    "a3": "30860f1ff0911ff121491e62a5fa2ede84b43c6e4ce9bd7ec5f0f8a68d9592e6",
    "a4": "93b9c785ca800ad97ad0149e9931e1d43b58328744dbb5867fdc5b9261dfef36",
    "b1": "b9abc507c5ccdc20bc19c5681ba92cead920326fa9d04c1acf5b2ed90ff91465",
    "c1": "63e40e635b47c54876778a1c64809e961b3929062e3279ea4a805fdf9d8760e4",
}
EXPECTED_GIT_BLOB = {
    "plan": "98c3bbd0acd5f0dcee179eb70c60e6f1568e78b4",
    "a3": "4d3a068a9393d275f7ac2699544b7179a7147bf2",
    "a4": "0c3ea19a5b3ccd7eecd76fe221c795fd8f30d90d",
}
WINDOW = list(range(15, 34))
ALLOWED = {"GRUNT", "RUNNER", "BRUTE"}


def load(path: Path):
    return yaml.safe_load(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


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
    for name in ("plan", "base", "a2", "a3", "a4", "b1", "c1", "candidate"):
        ap.add_argument(f"--{name}", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--materialized-out", required=True)
    args = ap.parse_args()

    paths = {k: Path(getattr(args, k)) for k in ("plan", "base", "a2", "a3", "a4", "b1", "c1", "candidate")}
    docs = {k: load(v) for k, v in paths.items()}
    errors: list[str] = []
    warnings: list[str] = []

    for key, expected in EXPECTED_SHA256.items():
        if sha256(paths[key]) != expected:
            errors.append(f"{key}-sha256-drift")
    for key, expected in EXPECTED_GIT_BLOB.items():
        if git_blob_sha(paths[key]) != expected:
            errors.append(f"{key}-git-blob-drift")

    plan = docs["plan"]
    if plan.get("scope", {}).get("targetStages") != [32]:
        errors.append("plan-target-stage-drift")
    if plan.get("scope", {}).get("leftExactAnchor") != 31 or plan.get("scope", {}).get("rightExactAnchor") != 33:
        errors.append("plan-anchor-drift")
    contract = plan.get("stageContract", {})
    expected_contract = ("E02", ["GRUNT", "RUNNER"], "F04", "CD04", "C2", ["RUSH"])
    got_contract = (contract.get("archetype"), contract.get("monsters"), contract.get("formation"), contract.get("cadence"), contract.get("complexity"), contract.get("pressureTags"))
    if got_contract != expected_contract:
        errors.append("plan-stage32-contract-drift")

    candidate = docs["candidate"]
    if candidate.get("plan", {}).get("gitBlobSha") != EXPECTED_GIT_BLOB["plan"]:
        errors.append("candidate-plan-reference-drift")
    auth = candidate.get("authority", {})
    if auth.get("leftAnchor", {}).get("sha256") != EXPECTED_SHA256["a3"] or auth.get("leftAnchor", {}).get("gitBlobSha") != EXPECTED_GIT_BLOB["a3"]:
        errors.append("candidate-left-anchor-reference-drift")
    if auth.get("rightAnchor", {}).get("sha256") != EXPECTED_SHA256["a4"] or auth.get("rightAnchor", {}).get("gitBlobSha") != EXPECTED_GIT_BLOB["a4"]:
        errors.append("candidate-right-anchor-reference-drift")
    if auth.get("adoptedC1", {}).get("candidate", {}).get("sha256") != EXPECTED_SHA256["c1"]:
        errors.append("candidate-c1-reference-drift")

    scope = candidate.get("scope", {})
    if scope.get("intendedContiguousWindowAfterFutureAdoption") != [15, 33]:
        errors.append("candidate-window-not-15-33")
    if scope.get("addedStages") != [32] or scope.get("canonicalExactWindowBeforeCandidate") != [15, 31]:
        errors.append("candidate-stage-scope-drift")
    if scope.get("rightExactAnchorStages") != [33]:
        errors.append("candidate-right-anchor-stage-drift")
    if scope.get("allowedMonsters") != ["GRUNT", "RUNNER", "BRUTE"]:
        errors.append("monster-vocabulary-drift")
    if float(scope.get("physicalSpawnX", -1)) != 0.92 or scope.get("midfieldPopIn") is not False:
        errors.append("spawn-entry-guard-drift")
    for flag in ("monsterScalarChange", "classScalarChange", "shopExpPxpChange", "productionGameplayChange", "fullT1ExactRecipeFreeze", "candidateAdopted"):
        if scope.get(flag) is not False:
            errors.append(f"scope-{flag}-must-be-false")

    base = by_stage(docs["base"].get("recipes", []))
    a2 = by_stage(docs["a2"].get("stageAdditions", []))
    a3 = by_stage(docs["a3"].get("stageAdditions", []))
    a4 = by_stage(docs["a4"].get("stageAdditions", []))
    b1 = by_stage(docs["b1"].get("stageAdditions", []))
    c1 = by_stage(docs["c1"].get("stageAdditions", []))
    d1 = by_stage(candidate.get("stageAdditions", []))
    if sorted(d1) != [32]:
        errors.append("candidate-stage-set-not-32")

    sources = {
        15: a2.get(15), 16: b1.get(16), 17: b1.get(17), 18: base.get(18), 19: a2.get(19),
        20: base.get(20), 21: base.get(21), 22: base.get(22), 23: base.get(23), 24: a3.get(24),
        25: a3.get(25), 26: c1.get(26), 27: c1.get(27), 28: c1.get(28), 29: a3.get(29),
        30: a3.get(30), 31: a3.get(31), 33: a4.get(33),
    }
    for stage, obj in sources.items():
        if obj is None:
            errors.append(f"missing-authority-stage-{stage}")

    s32_obj = d1.get(32, {})
    got_meta = (
        s32_obj.get("archetype"), s32_obj.get("componentArchetypes"), s32_obj.get("formation"),
        s32_obj.get("formationSet"), s32_obj.get("cadence"), s32_obj.get("complexity"), s32_obj.get("pressureTags"),
    )
    want_meta = ("E02", ["E02"], "F04", ["F04"], "CD04", "C2", ["RUSH"])
    if got_meta != want_meta:
        errors.append("stage32-skeleton-signature-drift")
    if float(s32_obj.get("entryBaseX", -1)) != 0.92:
        errors.append("stage32-entry-x-drift")

    s32 = s32_obj.get("spawns", [])
    times = [int(x.get("tMs", -1)) for x in s32]
    expected_times = [0, 180, 360, 2200, 2380, 2560, 4700, 4880, 5060]
    if times != expected_times:
        errors.append("stage32-cd04-chronology-drift")
    if Counter(str(x.get("type")) for x in s32) != Counter({"RUNNER": 5, "GRUNT": 4}):
        errors.append("stage32-e02-composition-drift")
    if any(str(x.get("type")) not in ALLOWED for x in s32):
        errors.append("stage32-illegal-monster")
    if any(not (0.0 <= float(x.get("y", -1)) <= 1.0) for x in s32):
        errors.append("stage32-y-out-of-range")
    if s32 and max(float(x["y"]) for x in s32) - min(float(x["y"]) for x in s32) < 0.35:
        errors.append("stage32-f04-scatter-too-narrow")
    if max_density(s32, 4000) > 8:
        errors.append("stage32-max4-exceeds-8")
    for start in (0, 3, 6):
        group = times[start:start+3]
        if len(group) != 3 or [group[1]-group[0], group[2]-group[1]] != [180, 180]:
            errors.append(f"stage32-burst-{start//3+1}-internal-cadence-drift")

    s31 = sources.get(31) or {}
    s33 = sources.get(33) or {}
    if (s31.get("complexity"), s31.get("pressureTags")) != ("C1", ["BULWARK"]):
        errors.append("stage31-left-anchor-drift")
    if (s33.get("complexity"), s33.get("pressureTags")) != ("C2", ["BASELINE", "FLOOD"]):
        errors.append("stage33-right-anchor-drift")
    if not (len(s31.get("spawns", [])) < len(s32) < len(s33.get("spawns", []))):
        errors.append("stage31-32-33-count-bridge-not-ordered")
    if max_density(s32, 4000) >= max_density(s33.get("spawns", []), 4000):
        errors.append("stage32-density-collides-with-stage33-flood")

    materialized: dict[int, dict] = {s: copy.deepcopy(o) for s, o in sources.items() if o is not None}
    materialized[32] = copy.deepcopy(s32_obj)
    if sorted(materialized) != WINDOW:
        errors.append(f"materialized-window-incomplete:{sorted(materialized)}")
    for stage, original in sources.items():
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
        "version": "t1-contiguous-15-33-d1-materialized-v0.1",
        "status": "PASS" if not errors else "FAIL",
        "recipes": [materialized[s] for s in sorted(materialized)],
    }
    Path(args.materialized_out).write_text(yaml.safe_dump(out_doc, sort_keys=False))
    materialized_sha = sha256(Path(args.materialized_out))
    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "candidateSha256": sha256(paths["candidate"]),
        "materializedWindowSha256": materialized_sha,
        "windowStages": sorted(materialized),
        "contiguous15to33": sorted(materialized) == WINDOW,
        "authorityPreserved": not any(e.startswith("authority-stage-") for e in errors),
        "referenceIntegrity": "PASS" if not any("reference-drift" in e or "sha256-drift" in e or "git-blob-drift" in e for e in errors) else "FAIL",
        "rotation31to33Preserved": not any(e.startswith("stage31-") or e.startswith("stage33-") for e in errors),
        "stageStatic": stage_stats,
    }
    Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
