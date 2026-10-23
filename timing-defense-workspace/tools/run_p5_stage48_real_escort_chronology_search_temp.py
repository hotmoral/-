#!/usr/bin/env python3
"""TEMP SIEGER hit-position telemetry behind a favorable eight-BRUTE screen.

No combat logic is changed. The already-corrected P5 hit function is wrapped only to record
SIEGER pre-hit x/HP, actual damage, post-hit HP, and kill outcome.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ

DURATION = 120.0
PROFILES = ("BALANCED", "DEFENSE_HEAVY")
BRUTE_COUNT = 8
BRUTE_BANDS = (-2, -1, 0, 1, -2, -1, 0, 1)
BRUTE_START = 8.0
BRUTE_STAGGER = 0.15
SIEGER_TIME = 13.0
SIEGER_BAND = 2
SIEGER_EVENTS = []


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


def install_hit_telemetry():
    glb = integ.SIMULATE.__globals__
    original = glb["hit"]
    def traced(mon, cfg, mobs, m, raw, stats, counter, armor_ignore=False):
        pre_hp = float(m.hp) if m is not None else None
        pre_x = float(m.x) if m is not None else None
        typ = m.typ if m is not None else None
        target_id = m.id if m is not None else None
        actual, killed = original(mon, cfg, mobs, m, raw, stats, counter, armor_ignore=armor_ignore)
        if typ == "SIEGER":
            SIEGER_EVENTS.append({
                "targetId": target_id,
                "x": round(pre_x, 6),
                "preHp": round(pre_hp, 6),
                "rawBeforeShopWrapper": round(float(raw), 6),
                "actualDamage": round(float(actual), 6),
                "postHp": round(float(m.hp), 6),
                "killed": bool(killed),
                "armorIgnore": bool(armor_ignore),
            })
        return actual, killed
    glb["hit"] = traced


def build_schedule():
    out = [
        (round(BRUTE_START + i * BRUTE_STAGGER, 6), "BRUTE", int(BRUTE_BANDS[i]))
        for i in range(BRUTE_COUNT)
    ]
    out.append((SIEGER_TIME, "SIEGER", SIEGER_BAND))
    return sorted(out, key=lambda x: (x[0], x[1], x[2]))


def stage_cfg(temporal, direction, cls, schedule):
    cfg = copy.deepcopy(temporal)
    cfg["version"] = "p5-stage48-sieger-hit-position-telemetry-temp"
    cfg["simulation"]["durationSeconds"] = DURATION
    cfg["simulation"]["spawnX"] = float(direction["globalRules"]["normalRightEdgeSpawnX"])
    cfg["simulation"]["rootAttackIntervalSeconds"] = 1.047 if cls == "Rogue" else 1.125
    cfg["_p5FixedStageSchedule"] = [list(x) for x in schedule]
    cfg.pop("integratedSchedule", None)
    return cfg


def run_case(base, temporal, direction, shop, integration, profile_name, cls):
    schedule = build_schedule()
    profile = integ.profile_for(shop, cls, profile_name)
    scale = float(integration["shopEffectScale"])
    wall_max = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * scale
    overrides = {"shockwaveCoefficient": 0.25} if cls == "Tank" else None
    SIEGER_EVENTS.clear()
    row = integ.SIMULATE(
        base, stage_cfg(temporal, direction, cls, schedule), cls, True, (),
        overrides=overrides, shop_profile=profile, effect_scale=scale, start_wall_current=wall_max,
    )
    events = list(SIEGER_EVENTS)
    return {
        "profile": profile_name, "class": cls,
        "siegerWindups": row["siegerWindups"], "siegerShots": row["siegerShots"],
        "wallHits": row["wallHits"], "endWall": row["endWall"],
        "siegerHitCount": len(events),
        "firstHitX": events[0]["x"] if events else None,
        "deathX": next((e["x"] for e in events if e["killed"]), None),
        "events": events,
    }


def main():
    base, temporal, direction, shop, integration = load_inputs()
    install_schedule_hook()
    install_hit_telemetry()
    rows = [run_case(base, temporal, direction, shop, integration, p, c) for p in PROFILES for c in integ.CLASSES]
    output = {
        "version": "p5-stage48-sieger-hit-position-telemetry-temp-v0.5",
        "status": "TEMP_TELEMETRY_NO_LOGIC_CHANGE_NO_CANDIDATE_ADOPTION_NO_PRODUCTION_AUTHORITY",
        "normalRightEdgeSpawnX": direction["globalRules"]["normalRightEdgeSpawnX"],
        "siegeWindupThresholdX": 0.38,
        "setup": {"bruteCount": BRUTE_COUNT, "bruteStart": BRUTE_START, "siegerTime": SIEGER_TIME, "siegerBand": SIEGER_BAND},
        "rows": rows,
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    Path("/tmp/p5-stage48-chronology-search.json").write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__":
    main()
