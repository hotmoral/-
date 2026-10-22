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


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("recipes", type=Path)
    p.add_argument("kinematic_anchor", type=Path)
    p.add_argument("combat_anchor", type=Path)
    p.add_argument("trace_bracket", type=Path)
    p.add_argument("--recipe", required=True)
    p.add_argument("--profile", default="TRACE_BRACKET_CENTRAL")
    p.add_argument("--power-mode", default="CURRENT_AUTHORITY_LV6")
    p.add_argument("--shift-toward-wall", type=float, required=True)
    p.add_argument("--relative-special-offset", type=float, default=.10)
    p.add_argument("--windup-start-ms", type=int, default=0)
    p.add_argument("--windup-stop-ms", type=int, default=800)
    p.add_argument("--windup-step-ms", type=int, default=50)
    args = p.parse_args()

    recipe_data = yaml.safe_load(args.recipes.read_text(encoding="utf-8"))
    kin = yaml.safe_load(args.kinematic_anchor.read_text(encoding="utf-8"))
    combat = yaml.safe_load(args.combat_anchor.read_text(encoding="utf-8"))
    traces = yaml.safe_load(args.trace_bracket.read_text(encoding="utf-8"))

    recipe = next((copy.deepcopy(r) for r in recipe_data["recipes"] if r["id"] == args.recipe), None)
    if recipe is None:
        raise SystemExit(f"recipe not found: {args.recipe}")

    trace = traces["profiles"][args.profile]
    power_mode = traces["powerModes"][args.power_mode]
    base_spawn_x = float(kin["world"]["spawnX"])
    recipe["entryBaseX"] = base_spawn_x - args.shift_toward_wall
    formation_offset = float(kin.get("formationXOffsets", {}).get(recipe["formation"], {}).get("SIEGER", 0.0))
    recipe["entryXOffsetByType"] = {"SIEGER": args.relative_special_offset - formation_offset}

    original_windup = int(kin["monsters"]["SIEGER"]["windupMs"])
    rows = []
    try:
        for cls in CLASSES:
            class_rows = []
            max_completed_windup = None
            for windup_ms in range(args.windup_start_ms, args.windup_stop_ms + 1, args.windup_step_ms):
                kin["monsters"]["SIEGER"]["windupMs"] = windup_ms
                out = simulate(recipe, kin, combat, trace, cls, power_mode)
                shot_count = int(out.get("siegeShots") or 0)
                if shot_count > 0:
                    max_completed_windup = windup_ms
                class_rows.append({
                    "windupMs": windup_ms,
                    "shotCount": shot_count,
                    "firstShotMs": out.get("firstSiegeShotMs"),
                    "wallDamage": int(out.get("wallDamage") or 0),
                })
            rows.append({
                "classId": cls,
                "maxWindupMsStillCompletingAtLeastOneShot": max_completed_windup,
                "samples": class_rows,
            })
    finally:
        kin["monsters"]["SIEGER"]["windupMs"] = original_windup

    print(json.dumps({
        "probe": "SIEGER_READABILITY_BUDGET_PROXY",
        "recipeId": args.recipe,
        "profile": args.profile,
        "powerMode": args.power_mode,
        "shiftTowardWall": args.shift_toward_wall,
        "authoritativeWindupMs": original_windup,
        "rows": rows,
        "warning": (
            "This is a diagnostic survivable-windup proxy, not a production mechanic change. "
            "A nonzero budget shows that the unit reaches standoff and can remain in its response state for some bounded duration; "
            "exact readable-window acceptance requires fitted SKILLED_V2 and direct state instrumentation later."
        ),
    }, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
