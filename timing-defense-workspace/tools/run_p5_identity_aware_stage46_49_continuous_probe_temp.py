#!/usr/bin/env python3
"""TEMP diagnostic: replay Stage46->49 as one continuous 240s simulation.

This exists only to test whether the v0.1 synthetic stage-boundary mob discard is material.
No production or numerical authority.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ


def load_default_inputs():
    base = integ.load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    base_temporal = integ.load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49 = integ.load("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction = integ.load("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop = integ.load("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    refinement = integ.load("legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json")
    integration = integ.load("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")
    integ.validate_right_edge_contract(direction)
    base = integ.inject_diagnostic_monsters(base, stage49)
    if "ARMORED_DURABLE_PROXY" not in base["monsterAnchors"]:
        base["monsterAnchors"]["ARMORED_DURABLE_PROXY"] = dict(refinement["knightRobustPair"]["anchor"])
    return base, base_temporal, direction, shop, integration


def absolute_schedule(base_temporal, direction, integration, cls):
    window = float(integration["stageWindowSeconds"])
    out = []
    for i, stage_no in enumerate((46, 47, 48, 49)):
        local_cfg = integ.stage_temporal(base_temporal, direction, integration, stage_no, cls)
        local = integ.build_integrated_schedule(local_cfg)
        offset = i * window
        for st, typ, band in local:
            out.append((offset + float(st), typ, int(band)))
    return sorted(out, key=lambda x: (x[0], x[1], x[2]))


def install_absolute_schedule_hook():
    glb = integ.SIMULATE.__globals__
    original = glb["build_integrated_schedule"]

    def hooked(cfg):
        if "_p5AbsoluteSchedule" in cfg:
            duration = float(cfg["simulation"]["durationSeconds"])
            return [tuple(x) for x in cfg["_p5AbsoluteSchedule"] if float(x[0]) < duration]
        return original(cfg)

    glb["build_integrated_schedule"] = hooked


def continuous_cfg(base_temporal, direction, integration, cls, schedule, duration):
    cfg = copy.deepcopy(base_temporal)
    cfg["version"] = "p5-stage46-49-continuous-backlog-temp"
    cfg["simulation"]["durationSeconds"] = float(duration)
    cfg["simulation"]["spawnX"] = float(direction["globalRules"]["normalRightEdgeSpawnX"])
    cfg["simulation"]["rootAttackIntervalSeconds"] = 1.047 if cls == "Rogue" else 1.125
    cfg["simulation"]["wallHp"] = float(integration["startingBaseWallHp"])
    cfg["_p5AbsoluteSchedule"] = list(schedule)
    cfg.pop("integratedSchedule", None)
    return cfg


def snapshot(base, base_temporal, direction, integration, shop, cls, profile_name, scale, tank_coeff, schedule, duration):
    profile = integ.profile_for(shop, cls, profile_name)
    overrides = None
    if cls == "Tank" and tank_coeff is not None:
        overrides = {"shockwaveCoefficient": float(tank_coeff)}
    row = integ.SIMULATE(
        base,
        continuous_cfg(base_temporal, direction, integration, cls, schedule, duration),
        cls,
        True,
        (),
        overrides=overrides,
        shop_profile=profile,
        effect_scale=float(scale),
        start_wall_current=None,
    )
    return {
        "duration": float(duration),
        "endWall": row["endWall"],
        "endActive": row["endActive"],
        "maxActive": row["maxActive"],
        "kills": row["kills"],
        "wallHits": row["wallHits"],
        "burialTime": row["burialTime"],
        "siegerShots": row["siegerShots"],
        "siegerRepositions": row["siegerRepositions"],
    }


def main():
    base, base_temporal, direction, shop, integration = load_default_inputs()
    install_absolute_schedule_hook()
    scale = float(integration["shopEffectScale"])
    tank_coeffs = [float(x) for x in integration["tankShockwaveDamageSensitivity"]]
    profiles = list(integration["representativeShopProfiles"])
    window = float(integration["stageWindowSeconds"])

    result = {
        "version": "p5-stage46-49-continuous-backlog-temp-v0.1",
        "status": "TEMP_BOUNDARY_FIDELITY_DIAGNOSTIC_NO_PRODUCTION_AUTHORITY",
        "normalRightEdgeSpawnX": direction["globalRules"]["normalRightEdgeSpawnX"],
        "stageWindowSeconds": window,
        "chains": [],
    }

    for profile_name in profiles:
        for cls in integ.CLASSES:
            coeffs = tank_coeffs if cls == "Tank" else [None]
            schedule = absolute_schedule(base_temporal, direction, integration, cls)
            for coeff in coeffs:
                old = integ.run_chain(
                    base, base_temporal, direction, integration, shop,
                    cls, profile_name, scale, tank_coeff=coeff,
                )
                snaps = [
                    snapshot(
                        base, base_temporal, direction, integration, shop,
                        cls, profile_name, scale, coeff, schedule, window * n,
                    )
                    for n in (1, 2, 3, 4)
                ]
                result["chains"].append({
                    "class": cls,
                    "profile": profile_name,
                    "tankShockwaveCoefficient": coeff if cls == "Tank" else None,
                    "resetBoundaryFinalWall": old["finalWall"],
                    "resetBoundaryEndActive": [s["result"]["endActive"] for s in old["stages"]],
                    "continuousSnapshots": snaps,
                    "continuousSurvives240": snaps[-1]["burialTime"] is None,
                    "continuousFinalWall": snaps[-1]["endWall"],
                    "continuousFinalActive": snaps[-1]["endActive"],
                })

    text = json.dumps(result, indent=2, sort_keys=True)
    Path("/tmp/p5-continuous.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
