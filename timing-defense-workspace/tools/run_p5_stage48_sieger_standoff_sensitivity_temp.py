#!/usr/bin/env python3
"""TEMP P5 Stage48 SIEGER standoff-range sensitivity diagnostic.

Decision-support only. Keep right-edge spawn, monster/class/shop stats, and the tight calculated
real-monster escort chronology fixed. Vary only the provisional SIEGER standoff trigger to learn
whether the unresolved Stage48 role-expression defect is actually a standoff-distance problem.
No value is adopted/frozen and no production authority is implied.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_real_monster_frontline_search_temp_v2 as v2


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def row(typ, band, t, ref=0.0):
    return {
        "type": typ,
        "band": int(band),
        "referenceOffset": float(ref),
        "spawnLeadSeconds": float(12.0 + ref - t),
    }


def tight_direction(direction):
    # Same extreme boundary chronology used only to test whether the standoff axis has causal leverage.
    # SIEGER t=8.0; current SHIELD speed .057 vs SIEGER .045 -> catch time = 4.75*spawn delay.
    catch_targets = [1.0, 3.0, 5.0, 7.0, 9.0, 11.0]
    s_t = 8.0
    screens = [row("BRUTE", -2, 6.0), row("SHIELD", -1, 6.5)]
    for i, target_t in enumerate(catch_targets):
        delay = target_t / 4.75
        screens.append(row("SHIELD", -2 if i % 2 == 0 else -1, s_t + delay, 2.5 + i * 0.2))
    d = copy.deepcopy(direction)
    s48 = d["stageDirection"]["48"]
    s48["pressureCycleSecondsCandidate"] = 999.0
    s48["diagnosticPacket"] = screens + [row("SIEGER", 2, s_t, 2.0)]
    s48["note"] = "TEMP_STANDOFF_SENSITIVITY_ON_TIGHT_HANDOFF_BOUNDARY"
    integ.validate_right_edge_contract(d)
    return d


def build_sim_with_threshold(threshold):
    original_getsource = integ.inspect.getsource

    def patched_getsource(obj):
        src = original_getsource(obj)
        if obj is integ.stage46.simulate:
            old = 'if m.state == "ADVANCE" and m.x <= 0.38:'
            new = f'if m.state == "ADVANCE" and m.x <= {float(threshold):.6f}:'
            if src.count(old) != 1:
                raise RuntimeError("SIEGER threshold source changed; sensitivity patch review required")
            src = src.replace(old, new, 1)
        return src

    integ.inspect.getsource = patched_getsource
    try:
        return integ.build_identity_aware_simulate()
    finally:
        integ.inspect.getsource = original_getsource


def main():
    base = load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    temporal = load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49 = load("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction = load("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop = load("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    integration = load("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")

    integ.validate_right_edge_contract(direction)
    base = integ.inject_diagnostic_monsters(base, stage49)
    settled.install_fixed_schedule_hook()
    d = tight_direction(direction)

    scale = float(integration["shopEffectScale"])
    profile_name = "BALANCED"
    starts = v2.pre_stage48_states(base, temporal, direction, shop, integration, [profile_name], scale)

    thresholds = [0.38, 0.50, 0.60, 0.70, 0.78]
    original_sim = integ.SIMULATE
    out = {
        "version": "p5-stage48-sieger-standoff-sensitivity-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "fixed": {
            "spawnX": float(direction["globalRules"]["normalRightEdgeSpawnX"]),
            "siegerSpeed": float(base["monsterAnchors"]["SIEGER"]["speed"]),
            "windupSeconds": 0.8,
            "chronology": "TIGHT_CALCULATED_HANDOFF_BOUNDARY_1_3_5_7_9_11",
            "shopProfile": profile_name,
            "shopEffectScale": scale,
            "monsterStatsChanged": False,
            "classStatsChanged": False,
        },
        "rows": [],
    }

    try:
        for threshold in thresholds:
            integ.SIMULATE = build_sim_with_threshold(threshold)
            for cls in integ.CLASSES:
                st = starts[(profile_name, cls)]
                sim, _ = settled.simulate_stage(
                    base, temporal, d, integration, cls, st["profile"], scale,
                    48, st["startStage48Wall"], 0.25 if cls == "Tank" else None, 120.0,
                )
                out["rows"].append({
                    "thresholdX": threshold,
                    "straightTravelSeconds": round((0.92 - threshold) / 0.045, 3),
                    "class": cls,
                    "windups": int(sim.get("siegerWindups") or 0),
                    "shots": int(sim.get("siegerShots") or 0),
                    "repositions": int(sim.get("siegerRepositions") or 0),
                    "wallHits": int(sim.get("wallHits") or 0),
                    "endWall": sim.get("endWall"),
                    "endActive": int(sim.get("endActive") or 0),
                    "burialTime": sim.get("burialTime"),
                })
    finally:
        integ.SIMULATE = original_sim

    text = json.dumps(out, indent=2, sort_keys=True)
    Path("p5_stage48_sieger_standoff_sensitivity_temp.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
