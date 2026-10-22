#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


def max_window_count(times, window_ms):
    times = sorted(int(t) for t in times)
    best = 0
    for start in times:
        count = sum(start <= t < start + window_ms for t in times)
        best = max(best, count)
    return best


def effective_creation_times(spawns):
    """Conservative static stress: each SPLITTER immediately creates 2 children."""
    out = []
    for spawn in spawns:
        t = int(spawn["tMs"])
        out.append(t)
        if spawn["type"] == "SPLITTER":
            out.extend([t, t])
    return out


def analyze(recipes_data, envelope_data):
    errors = []
    warnings = []
    rows = []

    tiers = envelope_data["tiers"]
    guard = recipes_data["staticDensityGuardrails"]
    seen_ids = set()

    for recipe in recipes_data.get("recipes", []):
        rid = recipe["id"]
        if rid in seen_ids:
            errors.append(("DUPLICATE_RECIPE_ID", rid))
        seen_ids.add(rid)

        tier_id = recipe["tier"]
        tier = tiers.get(tier_id)
        if not tier:
            errors.append(("UNKNOWN_TIER", f"{rid}/{tier_id}"))
            continue

        archetype = recipe["archetype"]
        if archetype not in tier["legalArchetypes"]:
            errors.append(("ILLEGAL_ARCHETYPE", f"{rid}/{archetype}"))
        if recipe["formation"] not in tier["formations"]:
            errors.append(("ILLEGAL_FORMATION", f"{rid}/{recipe['formation']}"))
        if recipe["cadence"] not in tier["cadences"]:
            errors.append(("ILLEGAL_CADENCE", f"{rid}/{recipe['cadence']}"))

        spawns = recipe.get("spawns", [])
        if not spawns:
            errors.append(("EMPTY_RECIPE", rid))
            continue

        times = [int(x["tMs"]) for x in spawns]
        if times != sorted(times):
            errors.append(("NON_MONOTONIC_SPAWN_TIME", rid))

        authored = len(spawns)
        effective_times = effective_creation_times(spawns)
        effective = len(effective_times)
        authored4 = max_window_count(times, 4000)
        authored6 = max_window_count(times, 6000)
        effective4 = max_window_count(effective_times, 4000)
        effective6 = max_window_count(effective_times, 6000)
        types = Counter(x["type"] for x in spawns)

        if authored4 > guard["authored4sWatchMax"]:
            errors.append(("AUTHORED_4S_OVER_WATCH", f"{rid}={authored4}"))
        elif authored4 > guard["authored4sNormalMax"]:
            warnings.append(("AUTHORED_4S_WATCH", f"{rid}={authored4}"))

        if effective4 > guard["effective4sWatchMax"]:
            errors.append(("EFFECTIVE_4S_OVER_WATCH", f"{rid}={effective4}"))
        elif effective4 > guard["effective4sNormalMax"]:
            warnings.append(("EFFECTIVE_4S_WATCH", f"{rid}={effective4}"))

        rows.append({
            "id": rid,
            "tier": tier_id,
            "archetype": archetype,
            "authored": authored,
            "effectiveMax": effective,
            "authored4s": authored4,
            "authored6s": authored6,
            "effective4s": effective4,
            "effective6s": effective6,
            "types": dict(types),
        })

    return errors, warnings, rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("recipes", type=Path)
    parser.add_argument("envelope", type=Path)
    args = parser.parse_args()

    recipes_data = yaml.safe_load(args.recipes.read_text(encoding="utf-8"))
    envelope_data = yaml.safe_load(args.envelope.read_text(encoding="utf-8"))
    errors, warnings, rows = analyze(recipes_data, envelope_data)

    print(f"RESULT={'PASS' if not errors else 'FAIL'} errors={len(errors)} warnings={len(warnings)} recipes={len(rows)}")
    for row in rows:
        print(
            f"{row['id']} tier={row['tier']} arch={row['archetype']} "
            f"auth={row['authored']} eff={row['effectiveMax']} "
            f"a4={row['authored4s']} a6={row['authored6s']} "
            f"e4={row['effective4s']} e6={row['effective6s']}"
        )
    for code, msg in errors:
        print(f"ERROR {code}: {msg}")
    for code, msg in warnings:
        print(f"WARN {code}: {msg}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
