#!/usr/bin/env python3
"""Timing Defense P5 Stage48 real-monster frontline chronology search v2 (TEMP).

This is a bounded encounter-structure diagnostic only.
- All enemies still physically spawn at the normal right edge.
- Stage48 cycle remains 4.9 s to isolate relative-entry/frontmost-screening chronology.
- No class/shop/monster coefficient is changed.
- Stage46->47 is computed once per class/profile to obtain the real carried Stage48 start wall.
- Each Stage48 candidate gets 60 s authored spawns + up to 60 s no-new-spawn drain.
- No candidate is adopted or frozen by this script.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled

REAL = {"BRUTE", "CHARGER", "FLYER", "GRUNT", "RUNNER", "SHIELD", "SIEGER", "SPLITTER", "SUPPORTER"}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def e(typ, band, ref, lead):
    assert typ in REAL
    return {"type": typ, "band": int(band), "referenceOffset": float(ref), "spawnLeadSeconds": float(lead)}


def make_variant(base_direction, name, screens, sieger, trailing=True):
    d = copy.deepcopy(base_direction)
    s48 = d["stageDirection"]["48"]
    assert abs(float(s48["pressureCycleSecondsCandidate"]) - 4.9) < 1e-9
    packet = list(screens) + [sieger]
    if trailing:
        packet += [e("RUNNER", -1, 2.8, 0.0), e("CHARGER", 1, 3.4, 0.0)]
    s48["diagnosticPacket"] = packet
    s48["note"] = f"TEMP_REAL_MONSTER_FRONTLINE_SEARCH_V2:{name}"
    integ.validate_right_edge_contract(d)
    for x in packet:
        assert x["type"] in REAL and "spawnX" not in x
    return d


def variants(direction):
    out = {}
    add = lambda name, screens, sieger: out.__setitem__(name, make_variant(direction, name, screens, sieger))

    # Earlier front line: BRUTEs are already materially downfield when SIEGER appears.
    add("BRUTE_PAIR_LONG_LEAD", [
        e("BRUTE", -1, 0.0, 10.0),  # first cycle t=2.0
        e("BRUTE",  1, 0.5,  9.5),  # t=3.0
    ], e("SIEGER", 0, 2.0, 6.0))    # t=8.0

    add("BRUTE_TRIPLE_LONG_LEAD", [
        e("BRUTE", -1, 0.0, 10.5),  # t=1.5
        e("BRUTE",  0, 0.4,  9.9),  # t=2.5
        e("BRUTE",  1, 0.8,  9.3),  # t=3.5
    ], e("SIEGER", 0, 2.0, 6.0))

    # A staggered four-body train keeps a frontmost body ahead across more of the SIEGER travel budget.
    add("BRUTE_TRAIN_FOUR", [
        e("BRUTE", -1, 0.0, 11.0),  # t=1.0
        e("BRUTE",  1, 0.5, 10.0),  # t=2.5
        e("BRUTE", -1, 1.0,  9.0),  # t=4.0
        e("BRUTE",  1, 1.5,  8.0),  # t=5.5
    ], e("SIEGER", 0, 2.0, 6.0))    # t=8.0

    # Faster SIEGER entry while two BRUTEs are already well ahead.
    add("BRUTE_PAIR_LONG_LEAD_EARLY_SIEGER", [
        e("BRUTE", -1, 0.0, 10.5),  # t=1.5
        e("BRUTE",  1, 0.5,  9.5),  # t=3.0
    ], e("SIEGER", 0, 1.5, 8.0))    # t=5.5

    # SPLITTER death can leave real child bodies in front without inventing durability.
    add("SPLITTER_PAIR_LONG_LEAD", [
        e("SPLITTER", -1, 0.0, 10.0),
        e("SPLITTER",  1, 0.5,  9.5),
    ], e("SIEGER", 0, 2.0, 6.0))

    add("BRUTE_SPLITTER_LAYER", [
        e("BRUTE",     0, 0.0, 10.5),
        e("SPLITTER", -1, 0.5,  9.5),
        e("SPLITTER",  1, 0.9,  9.0),
    ], e("SIEGER", 0, 2.0, 6.0))

    # SUPPORTER is an existing archetype; here it tests whether a real speed-support layer can create role uptime.
    add("BRUTE_SUPPORTER_LAYER", [
        e("BRUTE",      0, 0.0, 10.0),
        e("SUPPORTER", -1, 0.7,  8.5),
        e("BRUTE",      1, 1.0,  8.5),
    ], e("SIEGER", 0, 2.0, 6.0))

    add("BRUTE_SUPPORTER_EARLY_SIEGER", [
        e("BRUTE",      0, 0.0, 10.5),
        e("SUPPORTER", -1, 0.5,  9.0),
        e("BRUTE",      1, 0.9,  8.8),
    ], e("SIEGER", 0, 1.5, 8.0))

    return out


def pre_stage48_states(base, temporal, direction, shop, integration, profiles, scale):
    states = {}
    for profile_name in profiles:
        for cls in integ.CLASSES:
            profile = integ.profile_for(shop, cls, profile_name)
            wall_max = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * scale
            current = wall_max
            ok = True
            history = []
            for stage_no in (46, 47):
                row, _ = settled.simulate_stage(
                    base, temporal, direction, integration, cls, profile, scale,
                    stage_no, current, 0.25 if cls == "Tank" else None, 120.0,
                )
                stage_ok = row.get("burialTime") is None and int(row.get("endActive", 0)) == 0
                history.append({"stage": stage_no, "endWall": row.get("endWall"), "endActive": row.get("endActive"), "burialTime": row.get("burialTime")})
                current = float(row.get("endWall", 0.0))
                if not stage_ok:
                    ok = False
                    break
            states[(profile_name, cls)] = {
                "ok": ok, "profile": profile, "wallMax": wall_max,
                "startStage48Wall": current, "history": history,
            }
    return states


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
    profiles = list(integration["representativeShopProfiles"])
    starts = pre_stage48_states(base, temporal, direction, shop, integration, profiles, scale)

    payload = {
        "version": "p5-stage48-real-monster-frontline-search-temp-v2",
        "sourceCanonicalHead": "33cac0072964c620383ddb3c71e3d6ac75e71a98",
        "authority": "TEMP_BOUNDED_CHRONOLOGY_SEARCH_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "physicalSpawnX": direction["globalRules"]["normalRightEdgeSpawnX"],
        "stage48CycleSecondsHeldFixed": direction["stageDirection"]["48"]["pressureCycleSecondsCandidate"],
        "tankCoefficientForCrossClassScreen": 0.25,
        "variants": {},
    }

    for name, d in variants(direction).items():
        rows = []
        for profile_name in profiles:
            for cls in integ.CLASSES:
                st = starts[(profile_name, cls)]
                if not st["ok"]:
                    rows.append({"class": cls, "profile": profile_name, "preStage48Failed": True, "history": st["history"]})
                    continue
                row48, schedule = settled.simulate_stage(
                    base, temporal, d, integration, cls, st["profile"], scale,
                    48, st["startStage48Wall"], 0.25 if cls == "Tank" else None, 120.0,
                )
                settled_ok = row48.get("burialTime") is None and int(row48.get("endActive", 0)) == 0
                rows.append({
                    "class": cls, "profile": profile_name, "preStage48Failed": False,
                    "wallMax": round(st["wallMax"], 3),
                    "startStage48Wall": round(st["startStage48Wall"], 3),
                    "startStage48ReserveRatio": round(st["startStage48Wall"] / st["wallMax"], 6),
                    "stage48SettledWithin120": settled_ok,
                    "stage48BurialTime": row48.get("burialTime"),
                    "stage48EndWall": row48.get("endWall"),
                    "stage48EndReserveRatio": round(float(row48.get("endWall", 0.0)) / st["wallMax"], 6),
                    "stage48EndActive": row48.get("endActive"),
                    "stage48MaxActive": row48.get("maxActive"),
                    "stage48Kills": row48.get("kills"),
                    "stage48WallHits": row48.get("wallHits"),
                    "stage48SiegerShots": row48.get("siegerShots"),
                    "authoredLastSpawnSeconds": round(max((x[0] for x in schedule), default=0.0), 3),
                })

        valid = [r for r in rows if not r.get("preStage48Failed")]
        shots = [int(r.get("stage48SiegerShots") or 0) for r in valid]
        settled_count = sum(bool(r.get("stage48SettledWithin120")) for r in valid)
        payload["variants"][name] = {
            "packet": d["stageDirection"]["48"]["diagnosticPacket"],
            "aggregate": {
                "validRows": len(valid),
                "settledRows": settled_count,
                "buriedOrUnsettledRows": [
                    {"class": r["class"], "profile": r["profile"], "burialTime": r.get("stage48BurialTime"), "endActive": r.get("stage48EndActive")}
                    for r in valid if not r.get("stage48SettledWithin120")
                ],
                "siegerShotCases": sum(v > 0 for v in shots),
                "totalSiegerShots": sum(shots),
                "maxSiegerShotsOneRow": max(shots) if shots else 0,
                "minEndReserveRatio": round(min((float(r["stage48EndReserveRatio"]) for r in valid), default=0.0), 6),
                "perClass": {
                    cls: {
                        "shotCases": sum(int(r.get("stage48SiegerShots") or 0) > 0 for r in valid if r["class"] == cls),
                        "totalShots": sum(int(r.get("stage48SiegerShots") or 0) for r in valid if r["class"] == cls),
                        "minEndReserveRatio": round(min((float(r["stage48EndReserveRatio"]) for r in valid if r["class"] == cls), default=0.0), 6),
                        "maxEndReserveRatio": round(max((float(r["stage48EndReserveRatio"]) for r in valid if r["class"] == cls), default=0.0), 6),
                    } for cls in integ.CLASSES
                },
            },
            "rows": rows,
        }

    text = json.dumps(payload, indent=2, sort_keys=True)
    Path("p5_stage48_real_monster_frontline_search_temp_v2.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
