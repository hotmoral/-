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
    siege_shot_damage = int(combat["monsters"].get("SIEGER", {}).get("shotWallDamage", 0))

    rows = []
    for shift in frange(args.shift_start, args.shift_stop, args.shift_step):
        recipe = copy.deepcopy(base_recipe)
        recipe["entryBaseX"] = base_spawn_x - shift
        recipe["entryXOffsetByType"] = {args.special_type: extra_special}

        by_class = {}
        for cls in CLASSES:
            out = simulate(recipe, kin, combat, trace, cls, power_mode)
            total_wall = int(out.get("wallDamage") or 0)
            siege_shots = int(out.get("siegeShots") or 0)
            special_wall = siege_shots * siege_shot_damage if args.special_type == "SIEGER" else 0
            contact_wall = max(0, total_wall - special_wall)
            by_class[cls] = {
                "expressionMetric": int(out.get(metric) or 0),
                "wallDamage": total_wall,
                "specialAbilityWallDamage": special_wall,
                "contactWallDamage": contact_wall,
                "clearMs": out.get("clearMs"),
                "chargerInterrupted": int(out.get("chargerInterrupted") or 0),
                "chargerCompleted": int(out.get("chargerCompleted") or 0),
                "siegeShots": siege_shots,
                "firstSiegeShotMs": out.get("firstSiegeShotMs"),
            }

        active = sum(1 for x in by_class.values() if x["expressionMetric"] > 0)
        wall_values = [x["wallDamage"] for x in by_class.values()]
        contact_values = [x["contactWallDamage"] for x in by_class.values()]
        row = {
            "shiftTowardWall": shift,
            "entryBaseX": recipe["entryBaseX"],
            "activeClassCount": active,
            "maxWallDamage": max(wall_values),
            "meanWallDamage": sum(wall_values) / len(wall_values),
            "maxContactWallDamage": max(contact_values),
            "meanContactWallDamage": sum(contact_values) / len(contact_values),
            "byClass": by_class,
        }
        rows.append(row)
        print(json.dumps(row, ensure_ascii=False, separators=(",", ":")))

    windows = contiguous_windows(rows)
    summary = []
    for w in windows:
        best = min(
            w,
            key=lambda r: (
                r["maxContactWallDamage"],
                r["meanContactWallDamage"],
                r["maxWallDamage"],
                r["shiftTowardWall"],
            ),
        )
        zero_contact = [r for r in w if r["maxContactWallDamage"] == 0]
        summary.append({
            "minShift": w[0]["shiftTowardWall"],
            "maxShift": w[-1]["shiftTowardWall"],
            "sampleCount": len(w),
            "zeroContactWallLeakRange": (
                None if not zero_contact else {
                    "minShift": zero_contact[0]["shiftTowardWall"],
                    "maxShift": zero_contact[-1]["shiftTowardWall"],
                    "sampleCount": len(zero_contact),
                }
            ),
            "lowestContactWallPressureSample": {
                "shiftTowardWall": best["shiftTowardWall"],
                "maxContactWallDamage": best["maxContactWallDamage"],
                "meanContactWallDamage": best["meanContactWallDamage"],
                "maxTotalWallDamage": best["maxWallDamage"],
            },
        })

    print(json.dumps({
        "summary": {
            "recipeId": args.recipe,
            "specialType": args.special_type,
            "expressionMetric": metric,
            "allFiveActivationWindows": summary,
            "warning": "windup/actual-shot expression uses an unfitted deterministic trace; special ability wall damage is separated from ordinary contact leak, but production readability thresholds remain open",
        }
    }, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
