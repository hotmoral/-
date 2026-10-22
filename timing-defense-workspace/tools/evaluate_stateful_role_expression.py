#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

STATEFUL = {"CHARGER", "SPLITTER", "SUPPORTER", "SIEGER"}


def row_status(row: dict, monster: str) -> tuple[str, str]:
    if monster == "CHARGER":
        if int(row.get("chargerWindups") or 0) > 0:
            return "PASS", "windup expression observed"
        if int(row.get("chargerErasedBeforeWindup") or 0) > 0:
            return "FAIL", "pre-windup erasure observed"
        return "NOT_APPLICABLE", "no charger observed"

    if monster == "SPLITTER":
        parents = int(row.get("splitterParentsKilled") or 0)
        children = int(row.get("splitterChildren") or 0)
        if parents <= 0:
            return "NOT_APPLICABLE", "no splitter parent death observed"
        if children >= parents * 2:
            return "WATCH", "split occurred; child meaningful-lifetime metrics still missing"
        return "FAIL", "parent death did not create required two-child transform"

    if monster == "SUPPORTER":
        aura = int(row.get("supportAuraMs") or 0)
        if aura > 0:
            return "PASS", "non-self aura interval observed"
        return "FAIL", "supporter present without aura expression"

    if monster == "SIEGER":
        shots = int(row.get("siegeShots") or 0)
        if shots > 0:
            return "PASS_CONSERVATIVE", "actual shot observed; therefore first-shot opportunity existed"
        return "BLOCKED", "zero shot is insufficient to distinguish pre-opportunity erasure from counterplay without new windup/standoff metrics"

    return "NOT_APPLICABLE", "unknown monster"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    parser.add_argument("--input", type=Path, default=None,
                        help="JSONL from simulate_class_aware_layer_a.py; stdin when omitted")
    args = parser.parse_args()

    contract = yaml.safe_load(args.contract.read_text(encoding="utf-8"))
    missing = STATEFUL - set(contract.get("monsters", {}))
    if missing:
        raise SystemExit(f"contract missing stateful monsters: {sorted(missing)}")

    fh = args.input.open("r", encoding="utf-8") if args.input else sys.stdin
    groups = defaultdict(lambda: defaultdict(list))
    try:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if "recipeId" not in row:
                continue
            for monster in STATEFUL:
                status, reason = row_status(row, monster)
                if status != "NOT_APPLICABLE":
                    groups[row["recipeId"]][monster].append((status, row.get("classId"), row.get("profile"), reason))
    finally:
        if args.input:
            fh.close()

    output = {}
    has_fail = False
    for recipe_id, by_monster in sorted(groups.items()):
        output[recipe_id] = {}
        for monster, rows in sorted(by_monster.items()):
            statuses = [r[0] for r in rows]
            if "FAIL" in statuses:
                overall = "FAIL"
                has_fail = True
            elif "BLOCKED" in statuses:
                overall = "BLOCKED"
            elif "WATCH" in statuses:
                overall = "WATCH"
            elif all(s in {"PASS", "PASS_CONSERVATIVE"} for s in statuses):
                overall = "PASS"
            else:
                overall = "MIXED"
            output[recipe_id][monster] = {
                "overall": overall,
                "rows": len(rows),
                "statuses": {s: statuses.count(s) for s in sorted(set(statuses))},
            }

    print(json.dumps({
        "evaluation": "STATEFUL_ROLE_EXPRESSION",
        "note": "SIEGER zero-shot rows remain BLOCKED until standoff/windup opportunity metrics are instrumented",
        "recipes": output,
    }, ensure_ascii=False, indent=2))
    return 1 if has_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
