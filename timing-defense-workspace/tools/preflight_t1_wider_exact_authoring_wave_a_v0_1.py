#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import yaml


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_yaml(path: str):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def parse_skeleton(path: str) -> dict[int, dict[str, str]]:
    text = Path(path).read_text(encoding="utf-8")
    rows: dict[int, dict[str, str]] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 9:
            continue
        stage = int(cols[0])
        rows[stage] = {
            "band": cols[1],
            "signature": cols[2],
            "formation": cols[3],
            "cadence": cols[4],
            "complexity": cols[5],
            "pressure": cols[6].replace(" ", ""),
            "purpose": cols[7],
            "opportunity": cols[8].replace(" ", ""),
        }
    return rows


def recipe_stages(doc: dict) -> set[int]:
    rows = []
    rows.extend(doc.get("recipes", []) or [])
    rows.extend(doc.get("stageOverrides", []) or [])
    return {int(x["stage"]) for x in rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--skeleton", required=True)
    ap.add_argument("--representative", required=True)
    ap.add_argument("--adopted", required=True)
    ap.add_argument("--json-out", required=True)
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    plan_bytes = Path(args.plan).read_bytes()
    plan = yaml.safe_load(plan_bytes)
    skeleton = parse_skeleton(args.skeleton)
    representative = load_yaml(args.representative)
    adopted = load_yaml(args.adopted)

    targets = [int(x) for x in plan["scope"]["newAuthoringTargetStages"]]
    contexts = [int(x) for x in plan["scope"]["contextOnlyStages"]]
    expected = {int(k): v for k, v in plan["expectedSignatures"].items()}
    rep_stages = recipe_stages(representative)
    adopted_stages = recipe_stages(adopted)

    if len(targets) != len(set(targets)):
        errors.append("duplicate target stage")
    if len(targets) > 13:
        errors.append(f"wave target count {len(targets)} exceeds bounded cap 13")
    if int(plan["scope"]["targetCount"]) != len(targets):
        errors.append("targetCount does not match target list")
    if set(targets) != set(expected):
        errors.append("expectedSignatures keys do not exactly match target stages")
    overlap = set(targets) & rep_stages
    if overlap:
        errors.append(f"new targets overlap already-authored representative stages: {sorted(overlap)}")
    if set(targets) & set(contexts):
        errors.append("target/context overlap")

    required_context = {5, 18, 20, 39, 40, 41, 49, 50}
    missing_context = required_context - set(contexts)
    if missing_context:
        errors.append(f"missing required context anchors: {sorted(missing_context)}")
    missing_context_recipes = required_context - rep_stages
    if missing_context_recipes:
        errors.append(f"required context stages absent from representative recipe base: {sorted(missing_context_recipes)}")
    if not {49, 50}.issubset(adopted_stages):
        errors.append("adopted Stage49-50 candidate does not contain both Stage49 and Stage50")

    canonical_targets = [1, 4, 8, 15, 19, 24, 25, 29, 30, 31, 33, 37, 38]
    if targets != canonical_targets:
        errors.append(f"target ordering drift: {targets}")

    for stage in targets:
        if stage not in skeleton:
            errors.append(f"stage {stage} missing from skeleton table")
            continue
        got = skeleton[stage]
        want = expected[stage]
        for key in ("band", "signature", "formation", "cadence", "complexity"):
            if str(got[key]) != str(want[key]):
                errors.append(f"stage {stage} {key}: skeleton={got[key]!r} plan={want[key]!r}")
        if got["pressure"].replace(" ", "") != str(want["pressure"]).replace(" ", ""):
            errors.append(f"stage {stage} pressure: skeleton={got['pressure']!r} plan={want['pressure']!r}")

    semantic = {
        "stage8FirstMixedGR": skeleton.get(8, {}).get("signature") == "E02 / G+R",
        "stage15BruteTeach": skeleton.get(15, {}).get("signature") == "E03 / B",
        "stage19FirstBRTargetOrderContrast": skeleton.get(19, {}).get("signature") == "E03+E02 / B+R",
        "stage25Lv21BufferC0": skeleton.get(25, {}).get("complexity") == "C0",
        "stage29FirstBoundedF08Synthesis": skeleton.get(29, {}).get("formation") == "F08",
        "stage30CheckpointB": skeleton.get(30, {}).get("band") == "Checkpoint B",
        "stage31SoftWallEntryC1": skeleton.get(31, {}).get("band") == "Pressure / Soft Wall" and skeleton.get(31, {}).get("complexity") == "C1",
        "stage33MageDensitySurface": "M" in skeleton.get(33, {}).get("opportunity", ""),
        "stage37BoundedF08Tempo": skeleton.get(37, {}).get("formation") == "F08",
        "stage38Pre39DurableBridge": skeleton.get(38, {}).get("signature") == "E01+E03 / G+B",
    }
    for name, passed in semantic.items():
        if not passed:
            errors.append(f"semantic guard failed: {name}")

    guards = plan["fixedGuards"]
    must_be_false = [
        "productionGameplayChangeAuthorized",
        "monsterScalarChangeAuthorized",
        "classScalarChangeAuthorized",
        "shopExpPxpChangeAuthorized",
        "fullT1ExactRecipeFreezeAuthorized",
    ]
    for key in must_be_false:
        if guards.get(key) is not False:
            errors.append(f"guard {key} must remain false")

    must_preserve = [
        "preserveStage5", "preserveStage18", "preserveStage20", "preserveStage39",
        "preserveStage40", "preserveStage41", "preserveAdoptedStage49_50",
    ]
    for key in must_preserve:
        if guards.get(key) is not True:
            errors.append(f"guard {key} must remain true")

    slices = plan.get("slices", [])
    slice_targets = [int(s) for block in slices for s in block.get("targetStages", [])]
    if slice_targets != targets:
        errors.append(f"slice target concatenation mismatch: {slice_targets}")

    result = {
        "version": "t1-wider-exact-authoring-wave-a-static-preflight-v0.1",
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "planSha256": sha256_bytes(plan_bytes),
        "skeletonSha256": sha256_bytes(Path(args.skeleton).read_bytes()),
        "representativeSha256": sha256_bytes(Path(args.representative).read_bytes()),
        "adoptedCandidateSha256": sha256_bytes(Path(args.adopted).read_bytes()),
        "targetStages": targets,
        "contextStages": contexts,
        "existingRepresentativeStages": sorted(rep_stages),
        "adoptedCandidateStages": sorted(adopted_stages),
        "semanticGuards": semantic,
        "boundedTargetCount": len(targets),
        "full50FreezeAuthorized": False,
        "productionChangeAuthorized": False,
    }
    Path(args.json_out).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if errors:
        raise SystemExit("T1_WIDER_AUTHORING_WAVE_A_STATIC_PREFLIGHT_FAIL")


if __name__ == "__main__":
    main()
