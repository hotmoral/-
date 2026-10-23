#!/usr/bin/env python3
"""P5 Stage46->49 STAGE_SETTLED fidelity probe.

Canonical semantics used:
- authored spawn window is the existing bounded 60s diagnostic recipe;
- a Stage does not advance while live Stage-owned enemies remain;
- no enemy instance leaks into the next Stage;
- wall current/max/absolute deficit persist;
- fixed late-segment shop snapshot remains diagnostic only.

This is a diagnostic runner only. It has no production or numerical authority.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ

STAGES = (46, 47, 48, 49)
DRAIN_CAP_SECONDS = 240.0
SETTLE_SCAN_ITERS = 16


def load_inputs():
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


def install_fixed_schedule_hook():
    glb = integ.SIMULATE.__globals__
    original = glb["build_integrated_schedule"]

    def hooked(cfg):
        if "_p5FixedStageSchedule" in cfg:
            duration = float(cfg["simulation"]["durationSeconds"])
            return [tuple(x) for x in cfg["_p5FixedStageSchedule"] if float(x[0]) < duration]
        return original(cfg)

    glb["build_integrated_schedule"] = hooked


def fixed_stage_cfg(base_temporal, direction, integration, stage_no, cls, duration):
    authored = integ.stage_temporal(base_temporal, direction, integration, stage_no, cls)
    schedule = integ.build_integrated_schedule(authored)
    cfg = copy.deepcopy(authored)
    cfg["version"] = f"p5-stage{stage_no}-stage-settled-v0.1"
    cfg["simulation"]["durationSeconds"] = float(duration)
    cfg["_p5FixedStageSchedule"] = [list(x) for x in schedule]
    cfg.pop("integratedSchedule", None)
    return cfg, schedule


def simulate_stage(base, base_temporal, direction, integration, cls, profile, scale, stage_no, current, tank_coeff, duration):
    cfg, schedule = fixed_stage_cfg(base_temporal, direction, integration, stage_no, cls, duration)
    overrides = None
    if cls == "Tank" and tank_coeff is not None:
        overrides = {"shockwaveCoefficient": float(tank_coeff)}
    row = integ.SIMULATE(
        base, cfg, cls, True, (),
        overrides=overrides,
        shop_profile=profile,
        effect_scale=float(scale),
        start_wall_current=float(current),
    )
    return row, schedule


def settle_stage(base, base_temporal, direction, integration, cls, profile, scale, stage_no, current, tank_coeff):
    window = float(integration["stageWindowSeconds"])
    cap_row, schedule = simulate_stage(
        base, base_temporal, direction, integration, cls, profile, scale,
        stage_no, current, tank_coeff, DRAIN_CAP_SECONDS,
    )
    if cap_row.get("burialTime") is not None:
        return {
            "settled": False,
            "buried": True,
            "burialTime": cap_row["burialTime"],
            "settleSeconds": None,
            "authoredLastSpawnSeconds": round(max((x[0] for x in schedule), default=0.0), 3),
            "endWall": cap_row["endWall"],
            "endActive": cap_row["endActive"],
            "maxActive": cap_row["maxActive"],
            "kills": cap_row["kills"],
            "wallHits": cap_row["wallHits"],
            "siegerShots": cap_row["siegerShots"],
        }
    if int(cap_row.get("endActive", 0)) != 0:
        return {
            "settled": False,
            "buried": False,
            "burialTime": None,
            "settleSeconds": None,
            "authoredLastSpawnSeconds": round(max((x[0] for x in schedule), default=0.0), 3),
            "endWall": cap_row["endWall"],
            "endActive": cap_row["endActive"],
            "maxActive": cap_row["maxActive"],
            "kills": cap_row["kills"],
            "wallHits": cap_row["wallHits"],
            "siegerShots": cap_row["siegerShots"],
        }

    # Retain exact settle-time visibility because chronology/tail length is an active P5 diagnostic axis.
    lo = window
    lo_row, _ = simulate_stage(
        base, base_temporal, direction, integration, cls, profile, scale,
        stage_no, current, tank_coeff, lo,
    )
    if int(lo_row.get("endActive", 0)) == 0 and lo_row.get("burialTime") is None:
        hi = lo
        settled_row = lo_row
    else:
        hi = DRAIN_CAP_SECONDS
        settled_row = cap_row
        for _ in range(SETTLE_SCAN_ITERS):
            mid = (lo + hi) / 2.0
            row, _ = simulate_stage(
                base, base_temporal, direction, integration, cls, profile, scale,
                stage_no, current, tank_coeff, mid,
            )
            if row.get("burialTime") is None and int(row.get("endActive", 0)) == 0:
                hi = mid
                settled_row = row
            else:
                lo = mid
        settled_row, _ = simulate_stage(
            base, base_temporal, direction, integration, cls, profile, scale,
            stage_no, current, tank_coeff, hi,
        )

    return {
        "settled": True,
        "buried": False,
        "burialTime": None,
        "settleSeconds": round(hi, 3),
        "tailBeyond60Seconds": round(max(0.0, hi - window), 3),
        "authoredLastSpawnSeconds": round(max((x[0] for x in schedule), default=0.0), 3),
        "endWall": settled_row["endWall"],
        "endActive": settled_row["endActive"],
        "maxActive": settled_row["maxActive"],
        "kills": settled_row["kills"],
        "wallHits": settled_row["wallHits"],
        "siegerShots": settled_row["siegerShots"],
    }


def run_chain(base, base_temporal, direction, shop, integration, cls, profile_name, scale, tank_coeff):
    profile = integ.profile_for(shop, cls, profile_name)
    wall_max = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * float(scale)
    current = wall_max
    stages = []
    for stage_no in STAGES:
        start = current
        result = settle_stage(
            base, base_temporal, direction, integration, cls, profile, scale,
            stage_no, current, tank_coeff,
        )
        current = float(result["endWall"])
        stages.append({
            "stage": stage_no,
            "startWall": round(start, 3),
            "maxWall": round(wall_max, 3),
            "startAbsoluteDeficit": round(max(0.0, wall_max - start), 3),
            **result,
            "endAbsoluteDeficit": round(max(0.0, wall_max - current), 3),
        })
        if not result["settled"]:
            break
    return {
        "class": cls,
        "profile": profile_name,
        "tankShockwaveCoefficient": tank_coeff if cls == "Tank" else None,
        "stagesSettled": len([x for x in stages if x["settled"]]),
        "settledThroughStage49": len(stages) == 4 and all(x["settled"] for x in stages),
        "finalWall": round(current, 3),
        "finalAbsoluteDeficit": round(max(0.0, wall_max - current), 3),
        "stages": stages,
    }


def main():
    base, base_temporal, direction, shop, integration = load_inputs()
    install_fixed_schedule_hook()
    scale = float(integration["shopEffectScale"])
    profiles = list(integration["representativeShopProfiles"])
    tank_coeffs = [float(x) for x in integration["tankShockwaveDamageSensitivity"]]
    chains = []
    for profile_name in profiles:
        for cls in integ.CLASSES:
            coeffs = tank_coeffs if cls == "Tank" else [None]
            for coeff in coeffs:
                chains.append(run_chain(
                    base, base_temporal, direction, shop, integration,
                    cls, profile_name, scale, coeff,
                ))
    output = {
        "version": "p5-stage46-49-stage-settled-probe-v0.1",
        "status": "BOUNDED_STAGE_SETTLED_FIDELITY_DIAGNOSTIC_NO_PRODUCTION_AUTHORITY",
        "stageAdvanceContract": "LAST_AUTHORED_SPAWN + ZERO_LIVE_STAGE_ENEMIES before next Stage",
        "normalRightEdgeSpawnX": direction["globalRules"]["normalRightEdgeSpawnX"],
        "authoredSpawnWindowSeconds": float(integration["stageWindowSeconds"]),
        "drainCapSeconds": DRAIN_CAP_SECONDS,
        "chains": chains,
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    print(text)


if __name__ == "__main__":
    main()
