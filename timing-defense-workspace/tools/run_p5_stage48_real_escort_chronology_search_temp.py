#!/usr/bin/env python3
"""TEMP Stage48 one-pulse real-body screening threshold probe.

Question only:
With current class/shop/monster numbers unchanged, how many existing BRUTEs are required in a
favorable multi-band screen for one right-edge SIEGER to reach windup/shot uptime?

This is a feasibility threshold, not a Stage48 candidate and not an authoring recommendation.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ

DURATION = 120.0
COARSE_PROFILES = ("BALANCED", "DEFENSE_HEAVY")
BRUTE_COUNTS = (2, 4, 6, 8)
BRUTE_BANDS = (-2, -1, 0, 1, -2, -1, 0, 1)
BRUTE_START = 8.0
BRUTE_STAGGER = 0.15
SIEGER_TIME = 13.0
SIEGER_BAND = 2


def load_inputs():
    base = integ.load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    temporal = integ.load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49 = integ.load("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction = integ.load("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop = integ.load("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    integration = integ.load("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")
    integ.validate_right_edge_contract(direction)
    base = integ.inject_diagnostic_monsters(base, stage49)
    return base, temporal, direction, shop, integration


def install_schedule_hook():
    glb = integ.SIMULATE.__globals__
    original = glb["build_integrated_schedule"]
    def hooked(cfg):
        if "_p5FixedStageSchedule" in cfg:
            return [tuple(x) for x in cfg["_p5FixedStageSchedule"]]
        return original(cfg)
    glb["build_integrated_schedule"] = hooked


def build_schedule(n):
    out = [
        (round(BRUTE_START + i * BRUTE_STAGGER, 6), "BRUTE", int(BRUTE_BANDS[i]))
        for i in range(n)
    ]
    out.append((SIEGER_TIME, "SIEGER", SIEGER_BAND))
    return sorted(out, key=lambda x: (x[0], x[1], x[2]))


def stage_cfg(temporal, direction, cls, schedule):
    cfg = copy.deepcopy(temporal)
    cfg["version"] = "p5-stage48-real-body-screen-threshold-temp"
    cfg["simulation"]["durationSeconds"] = DURATION
    cfg["simulation"]["spawnX"] = float(direction["globalRules"]["normalRightEdgeSpawnX"])
    cfg["simulation"]["rootAttackIntervalSeconds"] = 1.047 if cls == "Rogue" else 1.125
    cfg["_p5FixedStageSchedule"] = [list(x) for x in schedule]
    cfg.pop("integratedSchedule", None)
    return cfg


def run_case(base, temporal, direction, shop, integration, n, profile_name, cls):
    schedule = build_schedule(n)
    profile = integ.profile_for(shop, cls, profile_name)
    scale = float(integration["shopEffectScale"])
    wall_max = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * scale
    overrides = {"shockwaveCoefficient": 0.25} if cls == "Tank" else None
    row = integ.SIMULATE(
        base, stage_cfg(temporal, direction, cls, schedule), cls, True, (),
        overrides=overrides, shop_profile=profile, effect_scale=scale, start_wall_current=wall_max,
    )
    return {
        "bruteCount": n, "profile": profile_name, "class": cls,
        "endWall": row["endWall"], "wallRatio": round(float(row["endWall"]) / wall_max, 6),
        "burialTime": row.get("burialTime"), "endActive": row["endActive"], "kills": row["kills"],
        "wallHits": row["wallHits"], "siegerWindups": row["siegerWindups"],
        "siegerShots": row["siegerShots"], "siegerRepositions": row["siegerRepositions"],
    }


def main():
    base, temporal, direction, shop, integration = load_inputs()
    install_schedule_hook()
    rows = []
    for n in BRUTE_COUNTS:
        for profile in COARSE_PROFILES:
            for cls in integ.CLASSES:
                rows.append(run_case(base, temporal, direction, shop, integration, n, profile, cls))
    threshold = {}
    for cls in integ.CLASSES:
        threshold[cls] = {}
        for profile in COARSE_PROFILES:
            rr = [r for r in rows if r["class"] == cls and r["profile"] == profile]
            wind = [r["bruteCount"] for r in rr if r["siegerWindups"] > 0]
            shot = [r["bruteCount"] for r in rr if r["siegerShots"] > 0]
            threshold[cls][profile] = {
                "firstWindupBruteCount": min(wind) if wind else None,
                "firstShotBruteCount": min(shot) if shot else None,
                "rows": [{"bruteCount": r["bruteCount"], "windups": r["siegerWindups"], "shots": r["siegerShots"], "wallHits": r["wallHits"], "endWall": r["endWall"]} for r in rr],
            }
    output = {
        "version": "p5-stage48-real-body-screen-threshold-temp-v0.4",
        "status": "TEMP_FEASIBILITY_THRESHOLD_NO_CANDIDATE_ADOPTION_NO_PRODUCTION_AUTHORITY",
        "normalRightEdgeSpawnX": direction["globalRules"]["normalRightEdgeSpawnX"],
        "midFieldPopInAllowed": direction["globalRules"]["midFieldPopInAllowed"],
        "setup": {
            "bruteCounts": list(BRUTE_COUNTS), "bruteStart": BRUTE_START, "bruteStagger": BRUTE_STAGGER,
            "siegerTime": SIEGER_TIME, "siegerBand": SIEGER_BAND,
            "note": "favorable spread-screen feasibility test; not Stage48 authoring",
        },
        "threshold": threshold, "rows": rows,
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    Path("/tmp/p5-stage48-chronology-search.json").write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__":
    main()
