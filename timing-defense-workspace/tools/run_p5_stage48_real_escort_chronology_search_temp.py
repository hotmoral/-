#!/usr/bin/env python3
"""TEMP bounded Stage48 dense-overlap / lane-separation search.

Question:
Can existing real monsters, at roughly the current Stage48 density, screen a right-edge SIEGER
long enough for actual role uptime if pulses overlap more and SIEGER is protected from incidental
same-band AOE? No stats are changed and no candidate is adopted by this search.
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
FAMILIES = ("BRUTE_SHIELD", "DOUBLE_BRUTE")
CYCLES = (4.9, 5.7, 6.5)
SIEGER_BANDS = (0, 2)
SIEGER_OFFSET = 2.5


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


def make_candidate(family, cycle, sieger_band):
    if sieger_band == 0:
        front_bands = (-1, 1)
    else:
        # Keep both front bodies at least two bands away from the protected SIEGER when possible,
        # so line/AOE spill from the frontmost target is less likely to erase the role enemy for free.
        front_bands = (-1, 0)
    front_types = ("BRUTE", "SHIELD") if family == "BRUTE_SHIELD" else ("BRUTE", "BRUTE")
    rows = [
        (front_types[0], front_bands[0], 0.0),
        (front_types[1], front_bands[1], 0.6),
        ("SUPPORTER", sieger_band, SIEGER_OFFSET - 0.30),
        ("SIEGER", sieger_band, SIEGER_OFFSET),
        ("RUNNER", -2 if sieger_band == 2 else -1, SIEGER_OFFSET + 2.80),
        ("CHARGER", 1, SIEGER_OFFSET + 3.40),
    ]
    return {
        "id": f"{family}_C{cycle:.1f}_SB{sieger_band}",
        "family": family,
        "cycle": float(cycle),
        "siegerBand": int(sieger_band),
        "rows": rows,
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
        ref = 8.0 + pulse * float(candidate["cycle"])
    return sorted(out, key=lambda x: (x[0], x[1], x[2]))


def stage_cfg(temporal, direction, cls, schedule):
    cfg = copy.deepcopy(temporal)
    cfg["version"] = "p5-stage48-dense-real-escort-chronology-temp"
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
        overrides=overrides, shop_profile=profile, effect_scale=scale,
        start_wall_current=wall_max,
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
            "totalSiegerShots": sum(r["siegerShots"] for r in cr),
            "casesWithSiegerShot": sum(r["siegerShots"] > 0 for r in cr),
            "wallHits": sum(r["wallHits"] for r in cr),
        }
    return {
        "id": candidate["id"], "family": candidate["family"], "cycle": candidate["cycle"],
        "siegerBand": candidate["siegerBand"], "spawnCount": len(schedule),
        "siegerSpawnCount": sum(t == "SIEGER" for _, t, _ in schedule),
        "burials": sum(r["burialTime"] is not None for r in rows),
        "unsettledBy240": sum((not r["settledBy240"] and r["burialTime"] is None) for r in rows),
        "minWallRatio": min(r["wallRatio"] for r in rows),
        "totalSiegerShots": sum(r["siegerShots"] for r in rows),
        "casesWithSiegerShot": sum(r["siegerShots"] > 0 for r in rows),
        "totalWallHits": sum(r["wallHits"] for r in rows), "byClass": by_class,
    }


def main():
    base, temporal, direction, shop, integration = load_inputs()
    install_schedule_hook()
    candidates = [make_candidate(f, c, b) for f, c, b in itertools.product(FAMILIES, CYCLES, SIEGER_BANDS)]
    summaries, all_rows = [], []
    for candidate in candidates:
        schedule = build_schedule(candidate)
        rows = []
        for profile_name in COARSE_PROFILES:
            for cls in integ.CLASSES:
                row = run_case(base, temporal, direction, shop, integration, candidate, profile_name, cls)
                rows.append(row); all_rows.append(row)
        summaries.append(summarize(candidate, schedule, rows))
    summaries.sort(key=lambda s: (s["burials"], -s["casesWithSiegerShot"], -s["totalSiegerShots"], -s["minWallRatio"], s["spawnCount"]))
    output = {
        "version": "p5-stage48-dense-real-escort-chronology-search-temp-v0.2",
        "status": "TEMP_BOUNDED_SEARCH_NO_CANDIDATE_ADOPTION_NO_PRODUCTION_AUTHORITY",
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
