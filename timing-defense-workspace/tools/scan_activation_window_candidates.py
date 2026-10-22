#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

from simulate_class_aware_layer_a import CLASSES, simulate

SUPPORTED = {
    "CHARGER": "chargerWindups",
    "SIEGER": "siegeShots",
}


def frange(start: float, stop: float, step: float):
    x = start
    while x <= stop + 1e-12:
        yield round(x, 10)
        x += step


def contiguous_windows(rows):
    windows = []
    current = []
    for row in rows:
        if row["activeClassCount"] == len(CLASSES):
            current.append(row)
        elif current:
            windows.append(current)
            current = []
    if current:
        windows.append(current)
    return windows


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("recipes", type=Path)
    p.add_argument("kinematic_anchor", type=Path)
    p.add_argument("combat_anchor", type=Path)
    p.add_argument("trace_bracket", type=Path)
    p.add_argument("--recipe", required=True)
    p.add_argument("--special-type", choices=sorted(SUPPORTED), required=True)
    p.add_argument("--profile", default="TRACE_BRACKET_CENTRAL")
    p.add_argument("--power-mode", default="CURRENT_AUTHORITY_LV6")
    p.add_argument("--relative-special-offset", type=float, default=.10)
    p.add_argument("--shift-start", type=float, required=True)
    p.add_argument("--shift-stop", type=float, required=True)
    p.add_argument("--shift-step", type=float, default=.01)
    args = p.parse_args()

    recipe_data = yaml.safe_load(args.recipes.read_text(encoding="utf-8"))
    kin = yaml.safe_load(args.kinematic_anchor.read_text(encoding="utf-8"))
    combat = yaml.safe_load(args.combat_anchor.read_text(encoding="utf-8"))
    traces = yaml.safe_load(args.trace_bracket.read_text(encoding="utf-8"))

    base_recipe = next((r for r in recipe_data["recipes"] if r["id"] == args.recipe), None)
    if base_recipe is None:
        raise SystemExit(f"recipe not found: {args.recipe}")

    trace = traces["profiles"][args.profile]
    power_mode = traces["powerModes"][args.power_mode]
    metric = SUPPORTED[args.special_type]
    base_spawn_x = float(kin["world"]["spawnX"])
    formation_offset = float(kin.get("formationXOffsets", {}).get(base_recipe["formation"], {}).get(args.special_type, 0.0))
    extra_special = args.relative_special_offset - formation_offset

    rows = []
    for shift in frange(args.shift_start, args.shift_stop, args.shift_step):
        recipe = copy.deepcopy(base_recipe)
        recipe["entryBaseX"] = base_spawn_x - shift
        recipe["entryXOffsetByType"] = {args.special_type: extra_special}

        by_class = {}
        for cls in CLASSES:
            out = simulate(recipe, kin, combat, trace, cls, power_mode)
            by_class[cls] = {
                "expressionMetric": out[metric],
                "wallDamage": out["wallDamage"],
                "clearMs": out["clearMs"],
                "chargerInterrupted": out["chargerInterrupted"],
                "chargerCompleted": out["chargerCompleted"],
                "firstSiegeShotMs": out["firstSiegeShotMs"],
            }

        active = sum(1 for x in by_class.values() if (x["expressionMetric"] or 0) > 0)
        wall_values = [int(x["wallDamage"] or 0) for x in by_class.values()]
        row = {
            "shiftTowardWall": shift,
            "entryBaseX": recipe["entryBaseX"],
            "activeClassCount": active,
            "maxWallDamage": max(wall_values),
            "meanWallDamage": sum(wall_values) / len(wall_values),
            "byClass": by_class,
        }
        rows.append(row)
        print(json.dumps(row, ensure_ascii=False, separators=(",", ":")))

    windows = contiguous_windows(rows)
    summary = []
    for w in windows:
        best = min(w, key=lambda r: (r["maxWallDamage"], r["meanWallDamage"], r["shiftTowardWall"]))
        summary.append({
            "minShift": w[0]["shiftTowardWall"],
            "maxShift": w[-1]["shiftTowardWall"],
            "sampleCount": len(w),
            "lowestWallPressureSample": {
                "shiftTowardWall": best["shiftTowardWall"],
                "maxWallDamage": best["maxWallDamage"],
                "meanWallDamage": best["meanWallDamage"],
            },
        })

    print(json.dumps({
        "summary": {
            "recipeId": args.recipe,
            "specialType": args.special_type,
            "expressionMetric": metric,
            "allFiveActivationWindows": summary,
            "warning": "actual-shot/windup visibility is a conservative diagnostic; production readability thresholds remain open",
        }
    }, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
