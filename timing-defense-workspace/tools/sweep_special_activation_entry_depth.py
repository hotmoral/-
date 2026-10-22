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

METRICS = {
    "chargerWindups",
    "chargerCompleted",
    "chargerInterrupted",
    "siegeShots",
    "siegeScreenedShots",
}


def frange(start: float, stop: float, step: float):
    x = start
    while x <= stop + 1e-12:
        yield round(x, 10)
        x += step


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("recipes", type=Path)
    parser.add_argument("kinematic_anchor", type=Path)
    parser.add_argument("combat_anchor", type=Path)
    parser.add_argument("trace_bracket", type=Path)
    parser.add_argument("--recipe", required=True)
    parser.add_argument("--profile", default="TRACE_BRACKET_CENTRAL")
    parser.add_argument("--power-mode", default="CURRENT_AUTHORITY_LV6")
    parser.add_argument("--special-type", required=True)
    parser.add_argument("--metric", choices=sorted(METRICS), required=True)
    parser.add_argument("--relative-special-offset", type=float, default=.10,
                        help="desired total X offset of the special unit relative to the shifted formation base; positive is deeper")
    parser.add_argument("--shift-start", type=float, default=0.0,
                        help="positive value moves the whole formation closer to the wall by this X amount")
    parser.add_argument("--shift-stop", type=float, default=.75)
    parser.add_argument("--shift-step", type=float, default=.05)
    args = parser.parse_args()

    recipe_data = yaml.safe_load(args.recipes.read_text(encoding="utf-8"))
    kin = yaml.safe_load(args.kinematic_anchor.read_text(encoding="utf-8"))
    combat = yaml.safe_load(args.combat_anchor.read_text(encoding="utf-8"))
    traces = yaml.safe_load(args.trace_bracket.read_text(encoding="utf-8"))

    base_recipe = next((r for r in recipe_data["recipes"] if r["id"] == args.recipe), None)
    if base_recipe is None:
        raise SystemExit(f"recipe not found: {args.recipe}")
    trace = traces["profiles"][args.profile]
    power_mode = traces["powerModes"][args.power_mode]
    base_spawn_x = float(kin["world"]["spawnX"])
    formation_offset = float(kin.get("formationXOffsets", {}).get(base_recipe["formation"], {}).get(args.special_type, 0.0))
    recipe_extra_special = args.relative_special_offset - formation_offset

    print(json.dumps({
        "simulation": "SPECIAL_ACTIVATION_ENTRY_DEPTH_SWEEP",
        "recipeId": args.recipe,
        "profile": args.profile,
        "metric": args.metric,
        "specialType": args.special_type,
        "warning": "entry depth is a simulation geometry candidate, not a production coordinate freeze",
    }, ensure_ascii=False))

    first_all = None
    first_three = None
    for shift in frange(args.shift_start, args.shift_stop, args.shift_step):
        recipe = copy.deepcopy(base_recipe)
        recipe["entryBaseX"] = base_spawn_x - shift
        recipe["entryXOffsetByType"] = {args.special_type: recipe_extra_special}
        by_class = {}
        for cls in CLASSES:
            out = simulate(recipe, kin, combat, trace, cls, power_mode)
            by_class[cls] = {
                "metric": out[args.metric],
                "wallDamage": out["wallDamage"],
                "clearMs": out["clearMs"],
                "firstSiegeShotMs": out["firstSiegeShotMs"],
                "chargerInterrupted": out["chargerInterrupted"],
                "chargerCompleted": out["chargerCompleted"],
            }
        active = sum(1 for row in by_class.values() if row["metric"] > 0)
        record = {
            "shiftTowardWall": shift,
            "entryBaseX": recipe["entryBaseX"],
            "activeClassCount": active,
            "byClass": by_class,
        }
        print(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
        if first_three is None and active >= 3:
            first_three = record
        if first_all is None and active == len(CLASSES):
            first_all = record

    print(json.dumps({
        "summary": {
            "firstAtLeastThreeClasses": first_three,
            "firstAllFiveClasses": first_all,
        }
    }, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
