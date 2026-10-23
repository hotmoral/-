#!/usr/bin/env python3
"""TEMP bounded Stage48 BRUTE-relay escort chronology search.

Causal question:
The simulator has no physical body-blocking. Escorting works only while another living enemy stays
frontmost. Because BRUTE is slower than SIEGER, a small lead lets SIEGER overtake its own escort.
Can a larger BRUTE lead plus overlapping next-pulse BRUTEs preserve frontmost screening long enough
for real SIEGER role uptime?

No monster/class/shop stat changes. Normal physical spawnX only. No candidate adoption authority.
"""
from __future__ import annotations

import copy
import itertools
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ

AUTHORED_WINDOW = 60.0
DRAIN_CAP = 240.0
COARSE_PROFILES = ("BALANCED", "DEFENSE_HEAVY")
CYCLES = (4.9, 5.3)
SIEGER_GAPS = (4.0, 5.0, 6.0)
SIEGER_BANDS = (0, 2)


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


def make_candidate(cycle, gap, sieger_band):
    # No SUPPORTER here: this probe isolates frontmost relay timing rather than travel acceleration.
    front_bands = (-1, 0) if sieger_band == 2 else (-1, 1)
    rows = [
        ("BRUTE", front_bands[0], 0.0),
        ("BRUTE", front_bands[1], 0.6),
        ("SIEGER", sieger_band, gap),
        ("RUNNER", -2 if sieger_band == 2 else -1, gap + 2.8),
        ("CHARGER", 1, gap + 3.4),
    ]
    return {
        "id": f"DOUBLE_BRUTE_RELAY_C{cycle:.1f}_G{gap:.1f}_SB{sieger_band}",
        "cycle": float(cycle), "siegerGap": float(gap), "siegerBand": int(sieger_band), "rows": rows,
    }


def build_schedule(candidate):
    out = []
    pulse = 0
    ref = 8.0
    while ref < AUTHORED_WINDOW:
        for typ, band, off in candidate["rows"]:
            st = ref + float(off)
            if st < AUTHORED_WINDOW:
                out.append((round(st, 6), typ, int(band)))
        pulse += 1
        ref = 8.0 + pulse * candidate["cycle"]
    return sorted(out, key=lambda x: (x[0], x[1], x[2]))


def stage_cfg(temporal, direction, cls, schedule):
    cfg = copy.deepcopy(temporal)
    cfg["version"] = "p5-stage48-brute-relay-chronology-temp"
    cfg["simulation"]["durationSeconds"] = DRAIN_CAP
    cfg["simulation"]["spawnX"] = float(direction["globalRules"]["normalRightEdgeSpawnX"])
    cfg["simulation"]["rootAttackIntervalSeconds"] = 1.047 if cls == "Rogue" else 1.125
    cfg["_p5FixedStageSchedule"] = [list(x) for x in schedule]
    cfg.pop("integratedSchedule", None)
    return cfg


def run_case(base, temporal, direction, shop, integration, candidate, profile_name, cls):
    schedule = build_schedule(candidate)
    profile = integ.profile_for(shop, cls, profile_name)
    scale = float(integration["shopEffectScale"])
    wall_max = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * scale
    overrides = {"shockwaveCoefficient": 0.25} if cls == "Tank" else None
    row = integ.SIMULATE(
        base, stage_cfg(temporal, direction, cls, schedule), cls, True, (),
        overrides=overrides, shop_profile=profile, effect_scale=scale, start_wall_current=wall_max,
    )
    return {
        "candidate": candidate["id"], "profile": profile_name, "class": cls,
        "startWall": round(wall_max, 3), "endWall": row["endWall"],
        "wallRatio": round(float(row["endWall"]) / wall_max, 6) if wall_max else 0.0,
        "burialTime": row.get("burialTime"),
        "settledBy240": row.get("burialTime") is None and int(row.get("endActive", 0)) == 0,
        "endActive": row["endActive"], "maxActive": row["maxActive"], "kills": row["kills"],
        "wallHits": row["wallHits"], "siegerWindups": row["siegerWindups"],
        "siegerShots": row["siegerShots"], "siegerRepositions": row["siegerRepositions"],
    }


def summarize(candidate, schedule, rows):
    by_class = {}
    for cls in integ.CLASSES:
        cr = [r for r in rows if r["class"] == cls]
        by_class[cls] = {
            "burials": sum(r["burialTime"] is not None for r in cr),
            "settled": sum(r["settledBy240"] for r in cr),
            "minWallRatio": min(r["wallRatio"] for r in cr),
            "totalSiegerWindups": sum(r["siegerWindups"] for r in cr),
            "totalSiegerShots": sum(r["siegerShots"] for r in cr),
            "casesWithSiegerWindup": sum(r["siegerWindups"] > 0 for r in cr),
            "casesWithSiegerShot": sum(r["siegerShots"] > 0 for r in cr),
            "wallHits": sum(r["wallHits"] for r in cr),
        }
    return {
        "id": candidate["id"], "cycle": candidate["cycle"], "siegerGap": candidate["siegerGap"],
        "siegerBand": candidate["siegerBand"], "spawnCount": len(schedule),
        "siegerSpawnCount": sum(t == "SIEGER" for _, t, _ in schedule),
        "burials": sum(r["burialTime"] is not None for r in rows),
        "unsettledBy240": sum((not r["settledBy240"] and r["burialTime"] is None) for r in rows),
        "minWallRatio": min(r["wallRatio"] for r in rows),
        "totalSiegerWindups": sum(r["siegerWindups"] for r in rows),
        "totalSiegerShots": sum(r["siegerShots"] for r in rows),
        "casesWithSiegerWindup": sum(r["siegerWindups"] > 0 for r in rows),
        "casesWithSiegerShot": sum(r["siegerShots"] > 0 for r in rows),
        "totalWallHits": sum(r["wallHits"] for r in rows), "byClass": by_class,
    }


def main():
    base, temporal, direction, shop, integration = load_inputs()
    install_schedule_hook()
    candidates = [make_candidate(c, g, b) for c, g, b in itertools.product(CYCLES, SIEGER_GAPS, SIEGER_BANDS)]
    summaries, all_rows = [], []
    for candidate in candidates:
        schedule = build_schedule(candidate)
        rows = []
        for profile_name in COARSE_PROFILES:
            for cls in integ.CLASSES:
                row = run_case(base, temporal, direction, shop, integration, candidate, profile_name, cls)
                rows.append(row); all_rows.append(row)
        summaries.append(summarize(candidate, schedule, rows))
    summaries.sort(key=lambda s: (
        s["burials"], -s["casesWithSiegerShot"], -s["totalSiegerShots"],
        -s["casesWithSiegerWindup"], -s["totalSiegerWindups"], -s["minWallRatio"], s["spawnCount"]
    ))
    output = {
        "version": "p5-stage48-brute-relay-chronology-search-temp-v0.3",
        "status": "TEMP_BOUNDED_CAUSAL_SEARCH_NO_CANDIDATE_ADOPTION_NO_PRODUCTION_AUTHORITY",
        "profiles": list(COARSE_PROFILES),
        "normalRightEdgeSpawnX": direction["globalRules"]["normalRightEdgeSpawnX"],
        "midFieldPopInAllowed": direction["globalRules"]["midFieldPopInAllowed"],
        "tankWorkingCenterOnly": 0.25,
        "candidates": candidates, "summaries": summaries, "rows": all_rows,
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    Path("/tmp/p5-stage48-chronology-search.json").write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__":
    main()
