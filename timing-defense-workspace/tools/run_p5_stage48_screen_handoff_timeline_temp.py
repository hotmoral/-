#!/usr/bin/env python3
"""TEMP P5 Stage48 screen-handoff timeline diagnostic.

Purpose:
- explain why existing real-monster screens fail to buy enough SIEGER travel time;
- distinguish frontline collapse from class attacks that damage SIEGER before it is frontmost;
- no gameplay/stat/cadence adoption and no production authority.
"""
from __future__ import annotations

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
    if "ARMORED_DURABLE_PROXY" not in base["monsterAnchors"]:
        base["monsterAnchors"]["ARMORED_DURABLE_PROXY"] = dict(refinement["knightRobustPair"]["anchor"])
    settled.install_fixed_schedule_hook()

    scale = float(integration["shopEffectScale"])
    profile_name = "BALANCED"
    starts = v2.pre_stage48_states(base, temporal, direction, shop, integration, [profile_name], scale)

    vv = v2.variants(direction)
    variants = {
        "CURRENT_PROXY_PACKET": direction,
        "BRUTE_PAIR_LONG_LEAD": vv["BRUTE_PAIR_LONG_LEAD"],
        "BRUTE_TRAIN_FOUR": vv["BRUTE_TRAIN_FOUR"],
        "BRUTE_SPLITTER_LAYER": vv["BRUTE_SPLITTER_LAYER"],
    }

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
                "firstDamageAt": None,
                "firstDamageX": None,
                "firstDamageState": None,
                "bodiesAheadAtFirstDamage": None,
                "typesAheadAtFirstDamage": [],
                "firstPrimaryAt": None,
                "firstPrimaryX": None,
                "deathAt": None,
                "deathX": None,
                "deathState": None,
                "hitEvents": 0,
            }
        return mob

    def wrapped_nearest(mobs):
        target = original_nearest(mobs)
        if trace is not None:
            t = caller_now()
            target_id = target.id if target else None
            if target_id != trace["lastPrimaryId"]:
                trace["primaryTransitions"].append({
                    "t": t,
                    "id": target_id,
                    "type": target.typ if target else None,
                    "x": round(float(target.x), 4) if target else None,
                })
                trace["lastPrimaryId"] = target_id
            if target is not None and target.typ == "SIEGER":
                item = trace["siegers"].get(target.id)
                if item is not None and item["firstPrimaryAt"] is None:
                    item["firstPrimaryAt"] = t
                    item["firstPrimaryX"] = round(float(target.x), 4)
        return target

    def wrapped_hit(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=False):
        t = caller_now()
        is_sieger = bool(target is not None and getattr(target, "typ", None) == "SIEGER")
        before_alive = bool(getattr(target, "alive", False)) if target is not None else False
        before_x = float(getattr(target, "x", 0.0)) if target is not None else None
        before_state = str(getattr(target, "state", "")) if target is not None else None
        if is_sieger and trace is not None:
            item = trace["siegers"].setdefault(str(target.id), {
                "id": str(target.id), "spawnAt": None, "spawnX": None,
                "firstDamageAt": None, "firstDamageX": None, "firstDamageState": None,
                "bodiesAheadAtFirstDamage": None, "typesAheadAtFirstDamage": [],
                "firstPrimaryAt": None, "firstPrimaryX": None,
                "deathAt": None, "deathX": None, "deathState": None, "hitEvents": 0,
            })
            item["hitEvents"] += 1
            if item["firstDamageAt"] is None:
                ahead = sorted(
                    [m for m in mobs if m.alive and m is not target and float(m.x) < float(target.x) - 1e-9],
                    key=lambda m: (m.x, m.band, m.id),
                )
                item["firstDamageAt"] = t
                item["firstDamageX"] = round(before_x, 4)
                item["firstDamageState"] = before_state
                item["bodiesAheadAtFirstDamage"] = len(ahead)
                item["typesAheadAtFirstDamage"] = [m.typ for m in ahead[:8]]

        result = original_hit(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=armor_ignore)

        if is_sieger and trace is not None:
            item = trace["siegers"].get(str(target.id))
            after_alive = bool(getattr(target, "alive", False))
            if item is not None and before_alive and not after_alive and item["deathAt"] is None:
                item["deathAt"] = t
                item["deathX"] = round(before_x, 4)
                item["deathState"] = before_state
        return result

    glb["make_mob"] = wrapped_make_mob
    glb["nearest"] = wrapped_nearest
    glb["hit"] = wrapped_hit

    output = {
        "version": "p5-stage48-screen-handoff-timeline-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "physicalSpawnX": float(direction["globalRules"]["normalRightEdgeSpawnX"]),
        "siegeThresholdX": 0.38,
        "siegerSpeedAnchor": float(base["monsterAnchors"]["SIEGER"]["speed"]),
        "derivedStraightTravelSeconds": round(
            (float(direction["globalRules"]["normalRightEdgeSpawnX"]) - 0.38)
            / float(base["monsterAnchors"]["SIEGER"]["speed"]), 4
        ),
        "rows": [],
    }

    try:
        for variant_name, candidate in variants.items():
            for cls in integ.CLASSES:
                st = starts[(profile_name, cls)]
                current_trace = {
                    "lastPrimaryId": None,
                    "primaryTransitions": [],
                    "siegers": {},
                }
                trace = current_trace
                row, _ = settled.simulate_stage(
                    base, temporal, candidate, integration, cls, st["profile"], scale,
                    48, st["startStage48Wall"], 0.25 if cls == "Tank" else None, 120.0,
                )

                siegers = []
                for item in current_trace["siegers"].values():
                    spawn_at = item.get("spawnAt")
                    fd = item.get("firstDamageAt")
                    fp = item.get("firstPrimaryAt")
                    death = item.get("deathAt")
                    item["protectedUntilFirstDamage"] = (
                        round(fd - spawn_at, 4) if fd is not None and spawn_at is not None else None
                    )
                    item["protectedUntilPrimary"] = (
                        round(fp - spawn_at, 4) if fp is not None and spawn_at is not None else None
                    )
                    item["lifeSeconds"] = (
                        round(death - spawn_at, 4) if death is not None and spawn_at is not None else None
                    )
                    item["damagedBeforePrimary"] = bool(
                        fd is not None and (fp is None or fd < fp - 1e-9)
                    )
                    item["diedBeforePrimary"] = bool(
                        death is not None and (fp is None or death < fp - 1e-9)
                    )
                    siegers.append(item)

                valid_fd = [x["protectedUntilFirstDamage"] for x in siegers if x["protectedUntilFirstDamage"] is not None]
                valid_primary = [x["protectedUntilPrimary"] for x in siegers if x["protectedUntilPrimary"] is not None]
                valid_ahead = [x["bodiesAheadAtFirstDamage"] for x in siegers if x["bodiesAheadAtFirstDamage"] is not None]
                output["rows"].append({
                    "variant": variant_name,
                    "class": cls,
                    "siegerCount": len(siegers),
                    "siegerWindups": int(row.get("siegerWindups") or 0),
                    "siegerShots": int(row.get("siegerShots") or 0),
                    "wallHits": int(row.get("wallHits") or 0),
                    "endWall": row.get("endWall"),
                    "damagedBeforePrimaryCount": sum(x["damagedBeforePrimary"] for x in siegers),
                    "diedBeforePrimaryCount": sum(x["diedBeforePrimary"] for x in siegers),
                    "everPrimaryCount": sum(x["firstPrimaryAt"] is not None for x in siegers),
                    "minProtectedUntilFirstDamage": min(valid_fd) if valid_fd else None,
                    "maxProtectedUntilFirstDamage": max(valid_fd) if valid_fd else None,
                    "minProtectedUntilPrimary": min(valid_primary) if valid_primary else None,
                    "maxProtectedUntilPrimary": max(valid_primary) if valid_primary else None,
                    "minBodiesAheadAtFirstDamage": min(valid_ahead) if valid_ahead else None,
                    "maxBodiesAheadAtFirstDamage": max(valid_ahead) if valid_ahead else None,
                    "primaryTransitions": current_trace["primaryTransitions"][:40],
                    "siegers": sorted(siegers, key=lambda x: (x.get("spawnAt") is None, x.get("spawnAt") or 9999, x["id"])),
                })
                trace = None
    finally:
        glb["make_mob"] = original_make_mob
        glb["nearest"] = original_nearest
        glb["hit"] = original_hit

    text = json.dumps(output, indent=2, sort_keys=True)
    Path("p5_stage48_screen_handoff_timeline_temp.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
