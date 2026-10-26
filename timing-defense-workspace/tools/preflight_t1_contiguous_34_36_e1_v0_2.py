#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

import yaml

PREFIX_SHA = "47f02889b659dcad7988645fcc6e11381de38607657bd7751d7387856dba5466"
A4_SHA = "93b9c785ca800ad97ad0149e9931e1d43b58328744dbb5867fdc5b9261dfef36"
PLAN_BLOB = "28f2e490c5e5f8c4f35506a9aeb115fc442bab04"
A4_BLOB = "0c3ea19a5b3ccd7eecd76fe221c795fd8f30d90d"
WINDOW = list(range(15, 39))
TARGETS = [34, 35, 36]
ALLOWED = {"GRUNT", "RUNNER", "BRUTE"}
PRESERVED_DIGESTS = {
    34: "3f72e3bce28237d817603143ef647b1514b33b9332e91cbd037f08c35f153aa7",
    36: "39736eede5b872be77fed990b8953230cbd02f42dd4014925a7e3568975bee21",
}


def load(path: Path):
    return yaml.safe_load(path.read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def digest_obj(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def max_density(spawns: list[dict], window_ms: int) -> int:
    times = [int(x["tMs"]) for x in spawns]
    return max((sum(1 for t in times if s <= t < s + window_ms) for s in times), default=0)


def by_stage(rows):
    return {int(x["stage"]): x for x in rows}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--materialized15-33", required=True)
    ap.add_argument("--a4", required=True)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--materialized-out", required=True)
    args = ap.parse_args()
    paths = {k: Path(getattr(args, k)) for k in ("plan", "materialized15_33", "a4", "candidate")}
    docs = {k: load(v) for k, v in paths.items()}
    errors = []
    warnings = []

    if sha256(paths["materialized15_33"]) != PREFIX_SHA: errors.append("prefix-sha256-drift")
    if sha256(paths["a4"]) != A4_SHA: errors.append("a4-sha256-drift")
    if git_blob_sha(paths["plan"]) != PLAN_BLOB: errors.append("plan-git-blob-drift")
    if git_blob_sha(paths["a4"]) != A4_BLOB: errors.append("a4-git-blob-drift")

    plan = docs["plan"]
    ps = plan.get("scope", {})
    if ps.get("targetStages") != TARGETS: errors.append("plan-target-stage-drift")
    if ps.get("leftExactAnchor") != 33 or ps.get("primaryRightExactAnchor") != 37: errors.append("plan-anchor-drift")
    if ps.get("inheritedApprovedExactContinuation") != [38]: errors.append("plan-stage38-continuation-drift")
    if ps.get("intendedContiguousWindowAfterFutureAdoption") != [15, 38]: errors.append("plan-window-drift")

    candidate = docs["candidate"]
    if candidate.get("plan", {}).get("gitBlobSha") != PLAN_BLOB: errors.append("candidate-plan-reference-drift")
    auth = candidate.get("authority", {})
    if auth.get("adoptedD1", {}).get("materializedStage15_33Sha256") != PREFIX_SHA: errors.append("candidate-prefix-reference-drift")
    if auth.get("waveAAnchors", {}).get("sha256") != A4_SHA or auth.get("waveAAnchors", {}).get("gitBlobSha") != A4_BLOB: errors.append("candidate-a4-reference-drift")
    if auth.get("waveAAnchors", {}).get("stages") != [33, 37, 38]: errors.append("candidate-anchor-stage-drift")
    scope = candidate.get("scope", {})
    if scope.get("intendedContiguousWindowAfterFutureAdoption") != [15, 38]: errors.append("candidate-window-drift")
    if scope.get("addedStages") != TARGETS or scope.get("canonicalExactWindowBeforeCandidate") != [15, 33]: errors.append("candidate-stage-scope-drift")
    if scope.get("rightExactAnchorStages") != [37, 38]: errors.append("candidate-right-anchor-drift")
    if scope.get("allowedMonsters") != ["GRUNT", "RUNNER", "BRUTE"]: errors.append("monster-vocabulary-drift")
    if float(scope.get("physicalSpawnX", -1)) != 0.92 or scope.get("midfieldPopIn") is not False: errors.append("spawn-entry-guard-drift")
    for flag in ("monsterScalarChange", "classScalarChange", "shopExpPxpChange", "productionGameplayChange", "fullT1ExactRecipeFreeze", "candidateAdopted"):
        if scope.get(flag) is not False: errors.append(f"scope-{flag}-must-be-false")

    prefix = by_stage(docs["materialized15_33"].get("recipes", []))
    if sorted(prefix) != list(range(15, 34)): errors.append(f"prefix-stage-set-drift:{sorted(prefix)}")
    a4 = by_stage(docs["a4"].get("stageAdditions", []))
    if a4.get(37) is None or a4.get(38) is None: errors.append("missing-wave-a4-right-authority")
    additions = by_stage(candidate.get("stageAdditions", []))
    if sorted(additions) != TARGETS: errors.append("candidate-stage-set-drift")

    expected_meta = {
        34: ("E03+E02", ["E03", "E02"], "F02", ["F02"], "CD05", "C2", ["BULWARK"]),
        35: ("E01", ["E01"], "F04", ["F04"], "CD05", "C1", ["BASELINE"]),
        36: ("E03", ["E03"], "F01", ["F01"], "CD03", "C1", ["BULWARK"]),
    }
    for stage in TARGETS:
        obj = additions.get(stage, {})
        got = (obj.get("archetype"), obj.get("componentArchetypes"), obj.get("formation"), obj.get("formationSet"), obj.get("cadence"), obj.get("complexity"), obj.get("pressureTags"))
        if got != expected_meta[stage]: errors.append(f"stage{stage}-signature-drift")
        if float(obj.get("entryBaseX", -1)) != 0.92: errors.append(f"stage{stage}-entry-x-drift")
        spawns = obj.get("spawns", [])
        times = [int(x.get("tMs", -1)) for x in spawns]
        if times != sorted(times) or len(times) != len(set(times)) or any(t < 0 for t in times): errors.append(f"stage{stage}-timestamp-invalid")
        if any(str(x.get("type")) not in ALLOWED for x in spawns): errors.append(f"stage{stage}-illegal-monster")
        if any(not (0 <= float(x.get("y", -1)) <= 1) for x in spawns): errors.append(f"stage{stage}-y-invalid")
        if max_density(spawns, 4000) > 8: errors.append(f"stage{stage}-max4-exceeds-8")

    if digest_obj(additions.get(34, {})) != PRESERVED_DIGESTS[34]: errors.append("stage34-not-byte-semantic-preserved-from-v01")
    if digest_obj(additions.get(36, {})) != PRESERVED_DIGESTS[36]: errors.append("stage36-not-byte-semantic-preserved-from-v01")

    s34 = additions.get(34, {}).get("spawns", [])
    s35 = additions.get(35, {}).get("spawns", [])
    s36 = additions.get(36, {}).get("spawns", [])
    if Counter(str(x.get("type")) for x in s35) != Counter({"GRUNT": 4}): errors.append("stage35-v02-composition-drift")
    if [int(x.get("tMs", -1)) for x in s35] != [0, 800, 2400, 3200]: errors.append("stage35-v02-chronology-drift")
    if s35 and max(float(x["y"]) for x in s35) - min(float(x["y"]) for x in s35) < 0.40: errors.append("stage35-f04-scatter-too-narrow")
    if len(s35) >= len(s34) or max_density(s35, 4000) >= max_density(s34, 4000): errors.append("stage35-static-recovery-not-lower-than-stage34")

    s33 = prefix.get(33, {})
    s37 = a4.get(37, {})
    s38 = a4.get(38, {})
    if (s33.get("complexity"), s33.get("pressureTags")) != ("C2", ["BASELINE", "FLOOD"]): errors.append("stage33-anchor-drift")
    if (s37.get("complexity"), s37.get("pressureTags"), s37.get("formation")) != ("C2", ["RUSH"], "F08"): errors.append("stage37-anchor-drift")
    if (s38.get("complexity"), s38.get("pressureTags"), s38.get("formation")) != ("C1", ["BULWARK"], "F02"): errors.append("stage38-anchor-drift")
    if max_density(s34, 4000) >= max_density(s33.get("spawns", []), 4000): errors.append("stage34-collides-stage33-density")
    if len(s36) >= len(s37.get("spawns", [])) or max_density(s36, 4000) >= max_density(s37.get("spawns", []), 4000): errors.append("stage36-collides-stage37-tempo")

    materialized = {s: copy.deepcopy(o) for s, o in prefix.items()}
    for stage in TARGETS: materialized[stage] = copy.deepcopy(additions[stage])
    materialized[37] = copy.deepcopy(s37)
    materialized[38] = copy.deepcopy(s38)
    if sorted(materialized) != WINDOW: errors.append(f"materialized-window-incomplete:{sorted(materialized)}")
    for stage, original in prefix.items():
        if materialized.get(stage) != original: errors.append(f"authority-stage-{stage}-mutated")
    if materialized.get(37) != s37: errors.append("authority-stage-37-mutated")
    if materialized.get(38) != s38: errors.append("authority-stage-38-mutated")

    stage_stats = {}
    for stage in sorted(materialized):
        spawns = materialized[stage].get("spawns", [])
        stage_stats[str(stage)] = {"authored": len(spawns), "max4s": max_density(spawns, 4000), "max6s": max_density(spawns, 6000), "types": dict(sorted(Counter(str(x["type"]) for x in spawns).items())), "digest": digest_obj(materialized[stage])}

    out_doc = {"version": "t1-contiguous-15-38-e1-materialized-v0.2", "status": "PASS" if not errors else "FAIL", "recipes": [materialized[s] for s in sorted(materialized)]}
    Path(args.materialized_out).write_text(yaml.safe_dump(out_doc, sort_keys=False))
    result = {
        "status": "PASS" if not errors else "FAIL", "errors": errors, "warnings": warnings,
        "candidateSha256": sha256(paths["candidate"]), "materializedWindowSha256": sha256(Path(args.materialized_out)),
        "windowStages": sorted(materialized), "contiguous15to38": sorted(materialized) == WINDOW,
        "authorityPreserved": not any(e.startswith("authority-stage-") for e in errors),
        "referenceIntegrity": "PASS" if not any("reference-drift" in e or "sha256-drift" in e or "git-blob-drift" in e for e in errors) else "FAIL",
        "stage35RevisionOnly": digest_obj(additions.get(34, {})) == PRESERVED_DIGESTS[34] and digest_obj(additions.get(36, {})) == PRESERVED_DIGESTS[36],
        "stageStatic": stage_stats,
    }
    Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__": main()
