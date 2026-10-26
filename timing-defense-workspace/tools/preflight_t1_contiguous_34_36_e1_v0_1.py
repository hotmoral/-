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
    "materialized15_33": "47f02889b659dcad7988645fcc6e11381de38607657bd7751d7387856dba5466",
    "a4": "93b9c785ca800ad97ad0149e9931e1d43b58328744dbb5867fdc5b9261dfef36",
}
EXPECTED_GIT_BLOB = {
    "plan": "d9bd6fc2ae9d6246791e8409e809cc818387eaf1",
    "a4": "0c3ea19a5b3ccd7eecd76fe221c795fd8f30d90d",
}
TARGETS = [34, 35, 36]
WINDOW = list(range(15, 38))
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
    for name in ("plan", "materialized15_33", "a4", "candidate"):
        ap.add_argument(f"--{name.replace('_', '-')}", dest=name, required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--materialized-out", required=True)
    args = ap.parse_args()

    paths = {k: Path(getattr(args, k)) for k in ("plan", "materialized15_33", "a4", "candidate")}
    docs = {k: load(v) for k, v in paths.items()}
    errors: list[str] = []
    warnings: list[str] = []

    if sha256(paths["materialized15_33"]) != EXPECTED["materialized15_33"]:
        errors.append("materialized15-33-sha256-drift")
    if sha256(paths["a4"]) != EXPECTED["a4"]:
        errors.append("a4-sha256-drift")
    if git_blob_sha(paths["plan"]) != EXPECTED_GIT_BLOB["plan"]:
        errors.append("plan-git-blob-drift")
    if git_blob_sha(paths["a4"]) != EXPECTED_GIT_BLOB["a4"]:
        errors.append("a4-git-blob-drift")

    plan = docs["plan"]
    scope_plan = plan.get("scope", {})
    if scope_plan.get("targetStages") != TARGETS:
        errors.append("plan-target-stage-drift")
    if scope_plan.get("leftExactAnchor") != 33 or scope_plan.get("rightExactAnchor") != 37:
        errors.append("plan-anchor-drift")
    contracts = {int(x["stage"]): x for x in plan.get("stageContracts", [])}
    expected_contracts = {
        34: ("E03+E02", ["GRUNT", "BRUTE", "RUNNER"], "F02", "CD05", "C2", ["BULWARK"]),
        35: ("E01", ["GRUNT"], "F04", "CD05", "C1", ["BASELINE"]),
        36: ("E03", ["GRUNT", "BRUTE"], "F01", "CD03", "C1", ["BULWARK"]),
    }
    for stage, want in expected_contracts.items():
        c = contracts.get(stage, {})
        got = (c.get("archetype"), c.get("monsters"), c.get("formation"), c.get("cadence"), c.get("complexity"), c.get("pressureTags"))
        if got != want:
            errors.append(f"plan-stage{stage}-contract-drift")

    candidate = docs["candidate"]
    if candidate.get("plan", {}).get("gitBlobSha") != EXPECTED_GIT_BLOB["plan"]:
        errors.append("candidate-plan-reference-drift")
    auth = candidate.get("authority", {})
    if auth.get("adoptedD1", {}).get("materializedStage15_33Sha256") != EXPECTED["materialized15_33"]:
        errors.append("candidate-d1-materialized-reference-drift")
    if auth.get("anchors", {}).get("sha256") != EXPECTED["a4"] or auth.get("anchors", {}).get("gitBlobSha") != EXPECTED_GIT_BLOB["a4"]:
        errors.append("candidate-anchor-reference-drift")

    scope = candidate.get("scope", {})
    if scope.get("intendedContiguousWindowAfterFutureAdoption") != [15, 37]:
        errors.append("candidate-window-not-15-37")
    if scope.get("addedStages") != TARGETS or scope.get("canonicalExactWindowBeforeCandidate") != [15, 33]:
        errors.append("candidate-stage-scope-drift")
    if scope.get("rightExactAnchorStages") != [37]:
        errors.append("candidate-right-anchor-stage-drift")
    if scope.get("allowedMonsters") != ["GRUNT", "RUNNER", "BRUTE"]:
        errors.append("monster-vocabulary-drift")
    if float(scope.get("physicalSpawnX", -1)) != 0.92 or scope.get("midfieldPopIn") is not False:
        errors.append("spawn-entry-guard-drift")
    for flag in ("monsterScalarChange", "classScalarChange", "shopExpPxpChange", "productionGameplayChange", "fullT1ExactRecipeFreeze", "candidateAdopted"):
        if scope.get(flag) is not False:
            errors.append(f"scope-{flag}-must-be-false")

    prefix_rows = docs["materialized15_33"].get("recipes", [])
    prefix = by_stage(prefix_rows)
    if sorted(prefix) != list(range(15, 34)):
        errors.append(f"prefix-stage-set-drift:{sorted(prefix)}")
    a4 = by_stage(docs["a4"].get("stageAdditions", []))
    s37_obj = a4.get(37)
    if s37_obj is None:
        errors.append("missing-stage37-anchor")
    additions = by_stage(candidate.get("stageAdditions", []))
    if sorted(additions) != TARGETS:
        errors.append("candidate-stage-set-not-34-36")

    expected_meta = {
        34: ("E03+E02", ["E03", "E02"], "F02", ["F02"], "CD05", "C2", ["BULWARK"]),
        35: ("E01", ["E01"], "F04", ["F04"], "CD05", "C1", ["BASELINE"]),
        36: ("E03", ["E03"], "F01", ["F01"], "CD03", "C1", ["BULWARK"]),
    }
    for stage in TARGETS:
        obj = additions.get(stage, {})
        got = (obj.get("archetype"), obj.get("componentArchetypes"), obj.get("formation"), obj.get("formationSet"), obj.get("cadence"), obj.get("complexity"), obj.get("pressureTags"))
        if got != expected_meta[stage]:
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

    s34 = additions.get(34, {}).get("spawns", [])
    if Counter(str(x.get("type")) for x in s34) != Counter({"RUNNER": 4, "BRUTE": 2, "GRUNT": 2}):
        errors.append("stage34-composition-drift")
    if [int(x.get("tMs", -1)) for x in s34] != [0, 550, 1100, 1650, 3300, 3850, 4400, 4950]:
        errors.append("stage34-cd05-chronology-drift")
    if s34 and max(float(x["y"]) for x in s34) - min(float(x["y"]) for x in s34) > 0.10:
        errors.append("stage34-f02-line-too-wide")

    s35 = additions.get(35, {}).get("spawns", [])
    if Counter(str(x.get("type")) for x in s35) != Counter({"GRUNT": 6}):
        errors.append("stage35-composition-drift")
    if [int(x.get("tMs", -1)) for x in s35] != [0, 900, 1800, 3600, 4500, 5400]:
        errors.append("stage35-cd05-chronology-drift")
    if s35 and max(float(x["y"]) for x in s35) - min(float(x["y"]) for x in s35) < 0.40:
        errors.append("stage35-f04-scatter-too-narrow")
    if len(s35) >= len(s34) or max_density(s35, 4000) >= max_density(s34, 4000):
        errors.append("stage35-not-readable-recovery-from-stage34")

    s36 = additions.get(36, {}).get("spawns", [])
    if Counter(str(x.get("type")) for x in s36) != Counter({"GRUNT": 4, "BRUTE": 3}):
        errors.append("stage36-composition-drift")
    if [int(x.get("tMs", -1)) for x in s36] != [0, 250, 500, 2800, 3050, 3300, 6000]:
        errors.append("stage36-cd03-chronology-drift")
    if s36 and max(float(x["y"]) for x in s36) - min(float(x["y"]) for x in s36) > 0.05:
        errors.append("stage36-f01-line-too-wide")

    s33 = prefix.get(33, {})
    s37 = s37_obj or {}
    if (s33.get("complexity"), s33.get("pressureTags")) != ("C2", ["BASELINE", "FLOOD"]):
        errors.append("stage33-left-anchor-drift")
    if (s37.get("complexity"), s37.get("pressureTags"), s37.get("formation")) != ("C2", ["RUSH"], "F08"):
        errors.append("stage37-right-anchor-drift")
    if max_density(s34, 4000) >= max_density(s33.get("spawns", []), 4000):
        errors.append("stage34-collides-with-stage33-density-peak")
    if len(s36) >= len(s37.get("spawns", [])) or max_density(s36, 4000) >= max_density(s37.get("spawns", []), 4000):
        errors.append("stage36-collides-with-stage37-split-tempo-peak")

    materialized: dict[int, dict] = {s: copy.deepcopy(o) for s, o in prefix.items()}
    for stage, obj in additions.items():
        if stage in materialized:
            errors.append(f"duplicate-stage-{stage}")
        materialized[stage] = copy.deepcopy(obj)
    if s37_obj is not None:
        materialized[37] = copy.deepcopy(s37_obj)
    if sorted(materialized) != WINDOW:
        errors.append(f"materialized-window-incomplete:{sorted(materialized)}")
    for stage, original in prefix.items():
        if materialized.get(stage) != original:
            errors.append(f"authority-stage-{stage}-mutated")
    if s37_obj is not None and materialized.get(37) != s37_obj:
        errors.append("authority-stage-37-mutated")

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
        "version": "t1-contiguous-15-37-e1-materialized-v0.1",
        "status": "PASS" if not errors else "FAIL",
        "recipes": [materialized[s] for s in sorted(materialized)],
    }
    Path(args.materialized_out).write_text(yaml.safe_dump(out_doc, sort_keys=False))
    result = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "candidateSha256": sha256(paths["candidate"]),
        "materializedWindowSha256": sha256(Path(args.materialized_out)),
        "windowStages": sorted(materialized),
        "contiguous15to37": sorted(materialized) == WINDOW,
        "authorityPreserved": not any(e.startswith("authority-stage-") for e in errors),
        "referenceIntegrity": "PASS" if not any("reference-drift" in e or "sha256-drift" in e or "git-blob-drift" in e for e in errors) else "FAIL",
        "rotation33to37Preserved": not any(e.startswith("stage33-") or e.startswith("stage37-") for e in errors),
        "stageStatic": stage_stats,
    }
    Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
