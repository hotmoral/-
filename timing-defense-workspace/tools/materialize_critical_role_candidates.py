#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("base_recipes", type=Path)
    p.add_argument("kinematic_anchor", type=Path)
    p.add_argument("candidate_overlay", type=Path)
    args = p.parse_args()

    base = yaml.safe_load(args.base_recipes.read_text(encoding="utf-8"))
    kin = yaml.safe_load(args.kinematic_anchor.read_text(encoding="utf-8"))
    overlay = yaml.safe_load(args.candidate_overlay.read_text(encoding="utf-8"))

    by_id = {str(r["id"]): copy.deepcopy(r) for r in base.get("recipes", [])}
    common_spawn_x = float(kin["world"]["spawnX"])
    formation_offsets = kin.get("formationXOffsets", {})
    recipe_cfgs = overlay.get("roleRecipes") or overlay.get("criticalRecipes") or {}

    out = {
        "version": "model-a-role-expression-materialized-v0.2",
        "status": "BOUNDED_DIAGNOSTIC_CANDIDATES_NOT_PRODUCTION_AUTHORING",
        "sourceBaseVersion": base.get("version"),
        "sourceOverlayVersion": overlay.get("version"),
        "recipes": [],
    }

    for recipe_id, cfg in recipe_cfgs.items():
        if recipe_id not in by_id:
            raise SystemExit(f"base recipe not found: {recipe_id}")
        r = copy.deepcopy(by_id[recipe_id])
        r["designatedRoleMonsters"] = list(cfg.get("designatedRoleMonsters") or [])

        if "entryShiftTowardWall" in cfg:
            r["entryBaseX"] = common_spawn_x - float(cfg["entryShiftTowardWall"])

        relative = cfg.get("relativeSpecialOffsets") or {}
        if relative:
            current_formation = formation_offsets.get(r.get("formation"), {})
            extras = dict(r.get("entryXOffsetByType") or {})
            for typ, desired_total in relative.items():
                extras[str(typ)] = float(desired_total) - float(current_formation.get(str(typ), 0.0))
            r["entryXOffsetByType"] = extras

        overrides = cfg.get("spawnTimeOverridesMs") or []
        if overrides:
            counters = defaultdict(int)
            override_map = {
                (str(x["occurrenceType"]), int(x["occurrenceIndex"])): int(x["tMs"])
                for x in overrides
            }
            new_spawns = []
            for spawn in r.get("spawns", []):
                s = dict(spawn)
                typ = str(s["type"])
                counters[typ] += 1
                key = (typ, counters[typ])
                if key in override_map:
                    s["tMs"] = override_map[key]
                new_spawns.append(s)
            new_spawns.sort(key=lambda x: (int(x["tMs"]), str(x["type"])))
            r["spawns"] = new_spawns

        out["recipes"].append(r)

    yaml.safe_dump(out, sys.stdout, sort_keys=False, allow_unicode=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
