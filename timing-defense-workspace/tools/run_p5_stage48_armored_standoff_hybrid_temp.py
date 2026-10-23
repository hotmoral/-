#!/usr/bin/env python3
"""TEMP P5 Stage48 hybrid diagnostic: limited armored front + spatial separation + standoff.

Decision support only. This tests whether combining two individually-insufficient axes can create
actual SIEGER role expression without changing class stats, monster durability, windup, shop,
spawnX, or production. No threshold/packet is adopted or frozen.

Fidelity note:
The threshold-specific SIMULATE function is dynamically rebuilt. STAGE_SETTLED's fixed-schedule
hook therefore must be installed into EACH rebuilt function's globals after rebuild; otherwise
the intended Stage48 integrated packet can silently fall back to the base stress schedule.
"""
from __future__ import annotations

import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_real_monster_frontline_search_temp_v2 as v2
import run_p5_stage48_armored_low_density_front_temp as low
import run_p5_stage48_sieger_standoff_sensitivity_temp as standoff


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def install_fixed_schedule_hook_on(sim_fn):
    """Install the STAGE_SETTLED fixed authored schedule on this exact rebuilt function."""
    glb = sim_fn.__globals__
    fallback = glb["build_integrated_schedule"]

    def hooked(cfg):
        if "_p5FixedStageSchedule" in cfg:
            duration = float(cfg["simulation"]["durationSeconds"])
            return [tuple(x) for x in cfg["_p5FixedStageSchedule"] if float(x[0]) < duration]
        return fallback(cfg)

    glb["build_integrated_schedule"] = hooked
    return sim_fn


def main():
    base = load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    temporal = load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49 = load("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction = load("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop = load("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    refinement = load("legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json")
    integration = load("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")

    integ.validate_right_edge_contract(direction)
    base = integ.inject_diagnostic_monsters(base, stage49)
    base["monsterAnchors"]["ARMORED_DURABLE_PROXY"] = dict(refinement["knightRobustPair"]["anchor"])

    # Needed for the original integrated SIMULATE used by the pre-Stage48 carried-state setup.
    settled.install_fixed_schedule_hook()

    formations = {
        "ARMORED2_SPATIAL": low.make(direction, "HYBRID_ARMORED2_SPATIAL", [
            low.row("ARMORED_DURABLE_PROXY", -2, 6.0),
            low.row("ARMORED_DURABLE_PROXY", 0, 7.0),
            low.row("SIEGER", 2, 8.0, 2.0),
        ]),
        "ARMORED3_SPATIAL": low.make(direction, "HYBRID_ARMORED3_SPATIAL", [
            low.row("ARMORED_DURABLE_PROXY", -2, 5.25),
            low.row("ARMORED_DURABLE_PROXY", 0, 6.25),
            low.row("ARMORED_DURABLE_PROXY", -1, 7.25),
            low.row("SIEGER", 2, 8.0, 2.0),
        ]),
    }

    thresholds = [0.78, 0.82]
    scale = float(integration["shopEffectScale"])
    profile_name = "BALANCED"
    starts = v2.pre_stage48_states(base, temporal, direction, shop, integration, [profile_name], scale)

    out = {
        "version": "p5-stage48-armored-standoff-hybrid-temp-v0.2",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "fidelityFix": "FIXED_SCHEDULE_HOOK_REINSTALLED_ON_EACH_REBUILT_SIMULATE",
        "fixed": {
            "spawnX": float(direction["globalRules"]["normalRightEdgeSpawnX"]),
            "siegerSpeed": float(base["monsterAnchors"]["SIEGER"]["speed"]),
            "windupSeconds": 0.8,
            "shopProfile": profile_name,
            "shopEffectScale": scale,
            "monsterStatsChanged": False,
            "classStatsChanged": False,
        },
        "proxyAnchor": base["monsterAnchors"]["ARMORED_DURABLE_PROXY"],
        "rows": [],
        "schedules": {},
    }

    original_sim = integ.SIMULATE
    try:
        for formation_name, d in formations.items():
            cfg = integ.stage_temporal(temporal, d, integration, 48, "Knight")
            expected_schedule = [
                {"t": round(t, 3), "type": typ, "band": band}
                for t, typ, band in integ.build_integrated_schedule(cfg)
            ]
            out["schedules"][formation_name] = expected_schedule

            for threshold in thresholds:
                rebuilt = standoff.build_sim_with_threshold(threshold)
                integ.SIMULATE = install_fixed_schedule_hook_on(rebuilt)
                for cls in integ.CLASSES:
                    st = starts[(profile_name, cls)]
                    sim, actual_schedule = settled.simulate_stage(
                        base, temporal, d, integration, cls, st["profile"], scale,
                        48, st["startStage48Wall"], 0.25 if cls == "Tank" else None, 120.0,
                    )
                    actual_simple = [
                        {"t": round(float(t), 3), "type": typ, "band": int(band)}
                        for t, typ, band in actual_schedule
                    ]
                    out["rows"].append({
                        "formation": formation_name,
                        "thresholdX": threshold,
                        "straightTravelSeconds": round((0.92-threshold)/0.045, 3),
                        "class": cls,
                        "scheduleMatchesExpected": bool(actual_simple == expected_schedule),
                        "actualSchedule": actual_simple,
                        "windups": int(sim.get("siegerWindups") or 0),
                        "shots": int(sim.get("siegerShots") or 0),
                        "repositions": int(sim.get("siegerRepositions") or 0),
                        "wallHits": int(sim.get("wallHits") or 0),
                        "startWall": round(float(st["startStage48Wall"]), 3),
                        "endWall": sim.get("endWall"),
                        "wallLoss": round(float(st["startStage48Wall"]) - float(sim.get("endWall") or 0.0), 3),
                        "burialTime": sim.get("burialTime"),
                    })
    finally:
        integ.SIMULATE = original_sim

    text = json.dumps(out, indent=2, sort_keys=True)
    Path("p5_stage48_armored_standoff_hybrid_temp.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
