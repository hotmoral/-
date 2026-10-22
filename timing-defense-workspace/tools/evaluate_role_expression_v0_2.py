#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

CLASSES = {"knight", "rogue", "tank", "archer", "mage"}


def load_jsonl(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        if "recipeId" in obj and "classId" in obj:
            rows.append(obj)
    return rows


def expressed(monster: str, row: dict) -> tuple[bool, str]:
    if monster == "GRUNT":
        return True, "baseline-exempt"
    if monster == "RUNNER":
        ok = float(row.get("runnerDistanceAdvancedMax") or 0) > 0
        return ok, "distance-advanced" if ok else "no-speed-expression-observed"
    if monster == "BRUTE":
        frontline = int(row.get("bruteFrontlineMs") or 0)
        hits = int(row.get("bruteHitsReceived") or 0)
        absorbed = float(row.get("bruteDamageAbsorbed") or 0)
        ok = hits > 0 and (frontline > 0 or absorbed > 0)
        return ok, "durable-attention-or-screening" if ok else "no-meaningful-durable-attention"
    if monster == "SHIELD":
        ok = int(row.get("shieldMitigatedHits") or 0) > 0 and float(row.get("shieldPreventedDamage") or 0) > 0
        return ok, "mitigation-observed" if ok else "mitigation-not-observed"
    if monster == "FLYER":
        opportunity = int(row.get("flyerArcherLineOpportunityMs") or 0) + int(row.get("flyerMageSplashOpportunityMs") or 0)
        ok = opportunity > 0 or int(row.get("flyerSkillHits") or 0) > 0
        return ok, "geometry-opportunity" if ok else "no-geometry-opportunity-observed"
    if monster == "CHARGER":
        ok = int(row.get("chargerWindups") or 0) > 0 and int(row.get("chargerWindupVisibleMs") or 0) > 0
        return ok, "visible-windup" if ok else "pre-windup-erasure"
    if monster == "SPLITTER":
        children = int(row.get("splitterChildren") or 0)
        consequence = (
            int(row.get("splitterChildAliveMs") or 0) > 0
            and (
                int(row.get("splitterChildFrontlineMs") or 0) > 0
                or int(row.get("splitterTargetReorders") or 0) > 0
                or int(row.get("splitterPeakActiveDelta") or 0) > 0
            )
        )
        ok = children > 0 and consequence
        return ok, "post-split-state-change" if ok else "split-consequence-not-observed"
    if monster == "SUPPORTER":
        ok = int(row.get("supportAuraTargetCount") or 0) > 0 and int(row.get("supportAuraMs") or 0) > 0
        return ok, "aura-applied" if ok else "aura-identity-erased"
    if monster == "SIEGER":
        ok = int(row.get("siegerOpportunityEntries") or 0) > 0 and int(row.get("siegerWindupVisibleMs") or 0) > 0
        return ok, "first-shot-opportunity" if ok else "pre-opportunity-erasure"
    return False, "unknown-monster"


def load_designations(path: Path | None) -> dict[str, set[str]]:
    if path is None:
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    recipe_cfgs = data.get("roleRecipes") or data.get("criticalRecipes") or {}
    out: dict[str, set[str]] = {}
    for recipe_id, cfg in recipe_cfgs.items():
        roles = cfg.get("designatedRoleMonsters") or []
        out[str(recipe_id)] = {str(x) for x in roles}
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("simulation_jsonl", type=Path)
    p.add_argument("contract_yaml", type=Path)
    p.add_argument("--designation-yaml", type=Path, default=None)
    p.add_argument("--monster", action="append", default=[])
    p.add_argument("--require-all-five", action="store_true")
    args = p.parse_args()

    contract = yaml.safe_load(args.contract_yaml.read_text(encoding="utf-8"))
    known = set(contract.get("monsters", {}).keys())
    wanted = set(args.monster) if args.monster else known
    unknown = sorted(wanted - known)
    if unknown:
        raise SystemExit(f"unknown contract monsters: {unknown}")

    designations = load_designations(args.designation_yaml)
    rows = load_jsonl(args.simulation_jsonl)

    results = []
    for row in rows:
        recipe_id = str(row["recipeId"])
        present = set((row.get("roleMetricsByType") or {}).keys())
        recipe_wanted = wanted & present
        if designations:
            recipe_wanted &= designations.get(recipe_id, set())
        for monster in sorted(recipe_wanted):
            ok, reason = expressed(monster, row)
            results.append({
                "recipeId": recipe_id,
                "profile": row.get("profile"),
                "classId": row["classId"],
                "monster": monster,
                "expressed": ok,
                "reason": reason,
            })

    aggregate = defaultdict(lambda: {"classes": set(), "passClasses": set(), "failRows": []})
    for r in results:
        key = (r["recipeId"], r["profile"], r["monster"])
        aggregate[key]["classes"].add(r["classId"])
        if r["expressed"]:
            aggregate[key]["passClasses"].add(r["classId"])
        else:
            aggregate[key]["failRows"].append(r)

    summaries = []
    overall_pass = True
    for key, state in sorted(aggregate.items()):
        recipe_id, profile, monster = key
        classes = state["classes"]
        pass_classes = state["passClasses"]
        all_five_seen = CLASSES <= classes
        all_five_pass = CLASSES <= pass_classes
        passed = all_five_pass if args.require_all_five else bool(pass_classes)
        overall_pass &= passed
        summaries.append({
            "recipeId": recipe_id,
            "profile": profile,
            "monster": monster,
            "observedClasses": sorted(classes),
            "passClasses": sorted(pass_classes),
            "allFiveObserved": all_five_seen,
            "allFiveExpressionPass": all_five_pass,
            "passed": passed,
            "failRows": state["failRows"],
        })

    print(json.dumps({
        "evaluation": "ROLE_EXPRESSION_V0_2",
        "designationFiltered": bool(designations),
        "requireAllFive": args.require_all_five,
        "overallPass": overall_pass,
        "summaries": summaries,
        "warning": (
            "Nonzero structural gates are admission prechecks only. Exact minimum milliseconds/rates remain OPEN until fitted SKILLED_V2."
        ),
    }, ensure_ascii=False, indent=2))
    return 0 if overall_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
