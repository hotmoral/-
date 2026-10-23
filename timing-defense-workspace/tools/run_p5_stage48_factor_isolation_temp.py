#!/usr/bin/env python3
"""TEMP Stage48 factor-isolation probe.

Purpose: determine whether the current Stage48 all-class failure asymmetry comes mainly
from the analysis-only ARMORED_DURABLE_PROXY, packet repetition, proxy count, or whether
existing real escort bodies can preserve a SIEGER role pulse.
No candidate is approved or frozen by this script.
"""
from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ

DURATION = 240.0


def load_inputs():
    base = integ.load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    temporal = integ.load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49 = integ.load("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction = integ.load("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop = integ.load("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    refinement = integ.load("legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json")
    integration = integ.load("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")
    integ.validate_right_edge_contract(direction)
    base = integ.inject_diagnostic_monsters(base, stage49)
    if "ARMORED_DURABLE_PROXY" not in base["monsterAnchors"]:
        base["monsterAnchors"]["ARMORED_DURABLE_PROXY"] = dict(refinement["knightRobustPair"]["anchor"])
    return base, temporal, direction, shop, integration


def install_fixed_schedule_hook():
    glb = integ.SIMULATE.__globals__
    original = glb["build_integrated_schedule"]
    def hooked(cfg):
        if "_p5FixedStageSchedule" in cfg:
            return [tuple(x) for x in cfg["_p5FixedStageSchedule"]]
        return original(cfg)
    glb["build_integrated_schedule"] = hooked


def variant_cfg(temporal, direction, integration, cls, variant):
    cfg = integ.stage_temporal(temporal, direction, integration, 48, cls)
    packet = copy.deepcopy(cfg["integratedSchedule"]["packet"])
    cycle = float(cfg["simulation"]["pressureCycleSeconds"])

    if variant == "REAL_BRUTE_SAME_PACKET":
        for row in packet:
            if row["type"] == "ARMORED_DURABLE_PROXY":
                row["type"] = "BRUTE"
    elif variant == "REAL_SHIELD_SAME_PACKET":
        for row in packet:
            if row["type"] == "ARMORED_DURABLE_PROXY":
                row["type"] = "SHIELD"
    elif variant == "REAL_BRUTE_SHIELD_MIX":
        seen = 0
        for row in packet:
            if row["type"] == "ARMORED_DURABLE_PROXY":
                row["type"] = "BRUTE" if seen == 0 else "SHIELD"
                seen += 1
    elif variant == "REAL_SHIELD_CYCLE_6P5":
        for row in packet:
            if row["type"] == "ARMORED_DURABLE_PROXY":
                row["type"] = "SHIELD"
        cycle = 6.5
    elif variant == "HALF_REPEAT_PROXY":
        cycle *= 2.0
    elif variant == "ONE_PROXY_ROW":
        removed = False
        new_packet = []
        for row in packet:
            if row["type"] == "ARMORED_DURABLE_PROXY" and removed:
                continue
            if row["type"] == "ARMORED_DURABLE_PROXY":
                removed = True
            new_packet.append(row)
        packet = new_packet
    elif variant != "CURRENT":
        raise ValueError(variant)

    authored = copy.deepcopy(cfg)
    authored["simulation"]["pressureCycleSeconds"] = cycle
    authored["integratedSchedule"]["packet"] = packet
    authored["integratedSchedule"]["maxLeadSeconds"] = max(float(x["spawnLeadSeconds"]) for x in packet)
    authored["simulation"]["durationSeconds"] = float(integration["stageWindowSeconds"])
    schedule = integ.build_integrated_schedule(authored)

    run_cfg = copy.deepcopy(authored)
    run_cfg["simulation"]["durationSeconds"] = DURATION
    run_cfg["_p5FixedStageSchedule"] = [list(x) for x in schedule]
    run_cfg.pop("integratedSchedule", None)
    return run_cfg, schedule


def run_one(base, temporal, direction, shop, integration, cls, profile_name, variant, tank_coeff):
    profile = integ.profile_for(shop, cls, profile_name)
    scale = float(integration["shopEffectScale"])
    cfg, schedule = variant_cfg(temporal, direction, integration, cls, variant)
    wall_max = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * scale
    overrides = {"shockwaveCoefficient": float(tank_coeff)} if cls == "Tank" else None
    row = integ.SIMULATE(
        base, cfg, cls, True, (), overrides=overrides,
        shop_profile=profile, effect_scale=scale, start_wall_current=wall_max,
    )
    types = Counter(x[1] for x in schedule)
    return {
        "variant": variant,
        "class": cls,
        "profile": profile_name,
        "tankShockwaveCoefficient": tank_coeff if cls == "Tank" else None,
        "spawnCount": len(schedule),
        "spawnTypes": dict(sorted(types.items())),
        "settledWithin240": row.get("burialTime") is None and int(row.get("endActive", 0)) == 0,
        "burialTime": row.get("burialTime"),
        "startWall": round(wall_max, 3),
        "endWall": row["endWall"],
        "endActive": row["endActive"],
        "kills": row["kills"],
        "maxActive": row["maxActive"],
        "wallHits": row["wallHits"],
        "siegerShots": row["siegerShots"],
        "siegerRepositions": row["siegerRepositions"],
    }


def main():
    base, temporal, direction, shop, integration = load_inputs()
    install_fixed_schedule_hook()
    variants = [
        "CURRENT",
        "REAL_BRUTE_SAME_PACKET",
        "REAL_SHIELD_SAME_PACKET",
        "REAL_BRUTE_SHIELD_MIX",
        "REAL_SHIELD_CYCLE_6P5",
        "HALF_REPEAT_PROXY",
        "ONE_PROXY_ROW",
    ]
    profiles = list(integration["representativeShopProfiles"])
    rows = []
    for variant in variants:
        for profile in profiles:
            for cls in integ.CLASSES:
                coeff = 0.25 if cls == "Tank" else None
                rows.append(run_one(base, temporal, direction, shop, integration, cls, profile, variant, coeff))
    output = {
        "version": "p5-stage48-factor-isolation-temp-v0.2",
        "status": "TEMP_DIAGNOSTIC_NO_CANDIDATE_APPROVAL_NO_PRODUCTION_AUTHORITY",
        "variants": variants,
        "rows": rows,
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    Path("/tmp/p5-stage48-factor.json").write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__":
    main()
