#!/usr/bin/env python3
"""TEMP P5 Stage48 SIEGER band-geometry diagnostic.

Keep the BRUTE_TRAIN_FOUR timings/counts, Stage48 cadence, monster/class/shop numerics,
and physical right-edge spawn fixed. Change only diagnostic band assignment to determine
whether SIEGER backline damage is caused materially by corridor/line geometry.
No candidate adoption, numerical freeze, or production authority.
"""
from __future__ import annotations

import copy
import inspect
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_real_monster_frontline_search_temp_v2 as v2


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def caller_now():
    frame = inspect.currentframe()
    try:
        frame = frame.f_back
        while frame is not None:
            value = frame.f_locals.get("now")
            if isinstance(value, (int, float)):
                return round(float(value), 4)
            frame = frame.f_back
    finally:
        del frame
    return None


def remap_train(base_train, name, escort_bands, sieger_band):
    d = copy.deepcopy(base_train)
    packet = d["stageDirection"]["48"]["diagnosticPacket"]
    brute_i = 0
    for row in packet:
        if row["type"] == "BRUTE" and brute_i < 4:
            row["band"] = int(escort_bands[brute_i])
            brute_i += 1
        elif row["type"] == "SIEGER":
            row["band"] = int(sieger_band)
    assert brute_i == 4
    d["stageDirection"]["48"]["note"] = f"TEMP_BAND_GEOMETRY:{name}"
    integ.validate_right_edge_contract(d)
    return d


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

    train = v2.variants(direction)["BRUTE_TRAIN_FOUR"]
    variants = {
        # Original v2 diagnostic geometry.
        "SPREAD_SCREEN_SIEGER_CENTER": remap_train(train, "SPREAD_SCREEN_SIEGER_CENTER", [-1, 1, -1, 1], 0),
        # Deliberate worst-case alignment comparator.
        "ALL_ALIGNED_CENTER": remap_train(train, "ALL_ALIGNED_CENTER", [0, 0, 0, 0], 0),
        # Same timings/counts, but escorts and SIEGER separated beyond Knight/Mage-normal/Archer ordinary band reach.
        "ISOLATED_ESCORT_LEFT_SIEGER_RIGHT": remap_train(train, "ISOLATED_ESCORT_LEFT_SIEGER_RIGHT", [-2, -1, -2, -1], 2),
        # Mirror to detect band-sign artifacts rather than a real separation effect.
        "ISOLATED_ESCORT_RIGHT_SIEGER_LEFT": remap_train(train, "ISOLATED_ESCORT_RIGHT_SIEGER_LEFT", [2, 1, 2, 1], -2),
    }

    scale = float(integration["shopEffectScale"])
    profile_name = "BALANCED"
    starts = v2.pre_stage48_states(base, temporal, direction, shop, integration, [profile_name], scale)

    glb = integ.SIMULATE.__globals__
    original_hit = glb["hit"]
    original_nearest = glb["nearest"]
    original_make_mob = glb["make_mob"]
    trace = None

    def wrapped_make_mob(mon, cfg, typ, band, idx):
        mob = original_make_mob(mon, cfg, typ, band, idx)
        if trace is not None and typ == "SIEGER":
            trace["siegers"][mob.id] = {
                "id": mob.id,
                "spawnAt": caller_now(),
                "spawnX": round(float(mob.x), 4),
                "band": int(mob.band),
                "firstDamageAt": None,
                "firstDamageX": None,
                "bodiesAheadAtFirstDamage": None,
                "typesAheadAtFirstDamage": [],
                "firstPrimaryAt": None,
                "firstPrimaryX": None,
                "deathAt": None,
                "deathX": None,
            }
        return mob

    def wrapped_nearest(mobs):
        target = original_nearest(mobs)
        if trace is not None and target is not None and target.typ == "SIEGER":
            item = trace["siegers"].get(target.id)
            if item is not None and item["firstPrimaryAt"] is None:
                item["firstPrimaryAt"] = caller_now()
                item["firstPrimaryX"] = round(float(target.x), 4)
        return target

    def wrapped_hit(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=False):
        t = caller_now()
        is_sieger = bool(target is not None and getattr(target, "typ", None) == "SIEGER")
        before_alive = bool(getattr(target, "alive", False)) if target is not None else False
        before_x = float(getattr(target, "x", 0.0)) if target is not None else None
        if is_sieger and trace is not None:
            item = trace["siegers"].get(str(target.id))
            if item is not None and item["firstDamageAt"] is None:
                ahead = sorted(
                    [m for m in mobs if m.alive and m is not target and float(m.x) < float(target.x) - 1e-9],
                    key=lambda m: (m.x, m.band, m.id),
                )
                item["firstDamageAt"] = t
                item["firstDamageX"] = round(before_x, 4)
                item["bodiesAheadAtFirstDamage"] = len(ahead)
                item["typesAheadAtFirstDamage"] = [m.typ for m in ahead[:12]]

        result = original_hit(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=armor_ignore)
        if is_sieger and trace is not None:
            item = trace["siegers"].get(str(target.id))
            after_alive = bool(getattr(target, "alive", False))
            if item is not None and before_alive and not after_alive and item["deathAt"] is None:
                item["deathAt"] = t
                item["deathX"] = round(before_x, 4)
        return result

    glb["make_mob"] = wrapped_make_mob
    glb["nearest"] = wrapped_nearest
    glb["hit"] = wrapped_hit

    out = {
        "version": "p5-stage48-band-geometry-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "fixed": {
            "physicalSpawnX": float(direction["globalRules"]["normalRightEdgeSpawnX"]),
            "stage48CycleSeconds": float(direction["stageDirection"]["48"]["pressureCycleSecondsCandidate"]),
            "shopProfile": profile_name,
            "shopEffectScale": scale,
            "tankCoefficient": 0.25,
            "monsterStatsChanged": False,
            "classStatsChanged": False,
            "timingsChangedFromBruteTrainFour": False,
        },
        "rows": [],
    }

    try:
        for variant_name, candidate in variants.items():
            packet = candidate["stageDirection"]["48"]["diagnosticPacket"]
            for cls in integ.CLASSES:
                st = starts[(profile_name, cls)]
                current_trace = {"siegers": {}}
                trace = current_trace
                row, _ = settled.simulate_stage(
                    base, temporal, candidate, integration, cls, st["profile"], scale,
                    48, st["startStage48Wall"], 0.25 if cls == "Tank" else None, 120.0,
                )
                items = list(current_trace["siegers"].values())
                for item in items:
                    spawn_at = item.get("spawnAt")
                    fd = item.get("firstDamageAt")
                    fp = item.get("firstPrimaryAt")
                    death = item.get("deathAt")
                    item["damagedBeforePrimary"] = bool(fd is not None and (fp is None or fd < fp - 1e-9))
                    item["diedBeforePrimary"] = bool(death is not None and (fp is None or death < fp - 1e-9))
                    item["secondsToFirstDamage"] = round(fd - spawn_at, 4) if fd is not None and spawn_at is not None else None
                    item["secondsToPrimary"] = round(fp - spawn_at, 4) if fp is not None and spawn_at is not None else None
                    item["lifeSeconds"] = round(death - spawn_at, 4) if death is not None and spawn_at is not None else None

                death_xs = [x["deathX"] for x in items if x.get("deathX") is not None]
                damage_delays = [x["secondsToFirstDamage"] for x in items if x.get("secondsToFirstDamage") is not None]
                ahead_counts = [x["bodiesAheadAtFirstDamage"] for x in items if x.get("bodiesAheadAtFirstDamage") is not None]
                out["rows"].append({
                    "variant": variant_name,
                    "escortBands": [int(x["band"]) for x in packet if x["type"] == "BRUTE"][:4],
                    "siegerBand": next(int(x["band"]) for x in packet if x["type"] == "SIEGER"),
                    "class": cls,
                    "siegerCount": len(items),
                    "windups": int(row.get("siegerWindups") or 0),
                    "shots": int(row.get("siegerShots") or 0),
                    "wallHits": int(row.get("wallHits") or 0),
                    "endWall": row.get("endWall"),
                    "damagedBeforePrimary": sum(x["damagedBeforePrimary"] for x in items),
                    "diedBeforePrimary": sum(x["diedBeforePrimary"] for x in items),
                    "everPrimary": sum(x["firstPrimaryAt"] is not None for x in items),
                    "minDeathX": min(death_xs) if death_xs else None,
                    "maxDeathX": max(death_xs) if death_xs else None,
                    "minSecondsToFirstDamage": min(damage_delays) if damage_delays else None,
                    "maxSecondsToFirstDamage": max(damage_delays) if damage_delays else None,
                    "minBodiesAheadAtFirstDamage": min(ahead_counts) if ahead_counts else None,
                    "maxBodiesAheadAtFirstDamage": max(ahead_counts) if ahead_counts else None,
                    "siegers": items,
                })
                trace = None
    finally:
        glb["make_mob"] = original_make_mob
        glb["nearest"] = original_nearest
        glb["hit"] = original_hit

    text = json.dumps(out, indent=2, sort_keys=True)
    Path("p5_stage48_band_geometry_temp.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
