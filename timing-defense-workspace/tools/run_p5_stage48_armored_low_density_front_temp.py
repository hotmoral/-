#!/usr/bin/env python3
"""TEMP P5 Stage48 low-density armored-front diagnostic.

User-directed diagnostic question:
Does sending only 2-3 armored-durable bodies ahead of SIEGER, while reducing temporal and/or
spatial packing density, materially extend SIEGER role time—especially against Archer/Mage—
without changing monster/class/shop numbers?

Diagnostic only. No monster/elite/stage packet/count/timing/value is adopted or frozen.
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


def row(typ, band, t, ref=0.0):
    return {
        "type": typ,
        "band": int(band),
        "referenceOffset": float(ref),
        "spawnLeadSeconds": float(12.0 + ref - t),
    }


def make(direction, name, rows):
    d = copy.deepcopy(direction)
    s48 = d["stageDirection"]["48"]
    s48["pressureCycleSecondsCandidate"] = 999.0
    s48["diagnosticPacket"] = list(rows)
    s48["note"] = f"TEMP_ARMORED_LOW_DENSITY_FRONT:{name}"
    integ.validate_right_edge_contract(d)
    return d


def caller_now():
    f = inspect.currentframe()
    try:
        f = f.f_back
        while f:
            v = f.f_locals.get("now")
            if isinstance(v, (int, float)):
                return round(float(v), 4)
            f = f.f_back
    finally:
        del f
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
    base["monsterAnchors"]["ARMORED_DURABLE_PROXY"] = dict(refinement["knightRobustPair"]["anchor"])
    settled.install_fixed_schedule_hook()

    # Prior best two-body heavy-screen reference.
    baseline2 = [
        row("ARMORED_DURABLE_PROXY", -1, 6.0),
        row("ARMORED_DURABLE_PROXY", 1, 7.0),
        row("SIEGER", 2, 8.0, 2.0),
    ]

    # Isolate SPATIAL density only: preserve t=6/t=7 but move both escorts away from SIEGER's band.
    spatial2 = [
        row("ARMORED_DURABLE_PROXY", -2, 6.0),
        row("ARMORED_DURABLE_PROXY", 0, 7.0),
        row("SIEGER", 2, 8.0, 2.0),
    ]

    # Slightly more front lead, but not so early that escorts are consumed before SIEGER arrives.
    spatial2_moderate_lead = [
        row("ARMORED_DURABLE_PROXY", -2, 5.5),
        row("ARMORED_DURABLE_PROXY", 0, 6.75),
        row("SIEGER", 2, 8.0, 2.0),
    ]

    # Three bodies kept near the SIEGER arrival window, but all outside its immediate band cluster.
    spatial3 = [
        row("ARMORED_DURABLE_PROXY", -2, 5.25),
        row("ARMORED_DURABLE_PROXY", 0, 6.25),
        row("ARMORED_DURABLE_PROXY", -1, 7.25),
        row("SIEGER", 2, 8.0, 2.0),
    ]

    # Previous over-separated temporal variants retained as negative controls.
    temporal2 = [
        row("ARMORED_DURABLE_PROXY", -2, 4.5),
        row("ARMORED_DURABLE_PROXY", 0, 6.5),
        row("SIEGER", 2, 8.0, 2.0),
    ]
    temporal3 = [
        row("ARMORED_DURABLE_PROXY", -2, 2.5),
        row("ARMORED_DURABLE_PROXY", 0, 4.75),
        row("ARMORED_DURABLE_PROXY", -1, 6.75),
        row("SIEGER", 2, 8.0, 2.0),
    ]

    variants = {
        "ARMORED2_BASELINE": make(direction, "ARMORED2_BASELINE", baseline2),
        "ARMORED2_SPATIAL_LOW_DENSITY": make(direction, "ARMORED2_SPATIAL_LOW_DENSITY", spatial2),
        "ARMORED2_SPATIAL_MODERATE_LEAD": make(direction, "ARMORED2_SPATIAL_MODERATE_LEAD", spatial2_moderate_lead),
        "ARMORED3_SPATIAL_LOW_DENSITY": make(direction, "ARMORED3_SPATIAL_LOW_DENSITY", spatial3),
        "ARMORED2_TEMPORAL_OVERSEPARATED": make(direction, "ARMORED2_TEMPORAL_OVERSEPARATED", temporal2),
        "ARMORED3_TEMPORAL_OVERSEPARATED": make(direction, "ARMORED3_TEMPORAL_OVERSEPARATED", temporal3),
    }

    scale = float(integration["shopEffectScale"])
    profile_name = "BALANCED"
    starts = v2.pre_stage48_states(base, temporal, direction, shop, integration, [profile_name], scale)

    glb = integ.SIMULATE.__globals__
    old_hit, old_nearest, old_make = glb["hit"], glb["nearest"], glb["make_mob"]
    trace = None

    def make_wrap(mon, cfg, typ, band, idx):
        m = old_make(mon, cfg, typ, band, idx)
        if trace is not None:
            trace.setdefault("spawn", {})[str(m.id)] = {
                "type": typ, "time": caller_now(), "band": int(band),
            }
            if typ == "SIEGER":
                trace["sieger"] = {
                    "id": str(m.id), "spawnAt": caller_now(),
                    "firstDamageAt": None, "firstPrimaryAt": None,
                    "deathAt": None, "deathX": None,
                }
        return m

    def nearest_wrap(mobs):
        p = old_nearest(mobs)
        if trace is not None and p is not None and getattr(p, "typ", None) == "SIEGER":
            s = trace.get("sieger")
            if s and s["firstPrimaryAt"] is None:
                s["firstPrimaryAt"] = caller_now()
        return p

    def hit_wrap(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=False):
        t = caller_now()
        typ = getattr(target, "typ", None) if target is not None else None
        alive = bool(getattr(target, "alive", False)) if target is not None else False
        before_x = float(getattr(target, "x", 0.0)) if target is not None else None
        mob_id = str(getattr(target, "id", "")) if target is not None else ""

        if typ == "SIEGER" and trace is not None:
            s = trace.get("sieger")
            if s and s["firstDamageAt"] is None:
                s["firstDamageAt"] = t

        res = old_hit(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=armor_ignore)

        if trace is not None and alive and target is not None and not bool(getattr(target, "alive", False)):
            trace.setdefault("deaths", {})[mob_id] = {
                "type": typ, "time": t, "x": round(before_x, 4),
            }
            if typ == "SIEGER":
                s = trace.get("sieger")
                if s and s["deathAt"] is None:
                    s["deathAt"] = t
                    s["deathX"] = round(before_x, 4)
        return res

    glb["hit"], glb["nearest"], glb["make_mob"] = hit_wrap, nearest_wrap, make_wrap

    out = {
        "version": "p5-stage48-armored-low-density-front-temp-v0.2",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "fixed": {
            "spawnX": float(direction["globalRules"]["normalRightEdgeSpawnX"]),
            "siegerThresholdX": 0.38,
            "siegerSpeed": float(base["monsterAnchors"]["SIEGER"]["speed"]),
            "shopProfile": profile_name,
            "shopEffectScale": scale,
            "tankDiagnosticCoefficient": 0.25,
            "monsterStatsChanged": False,
            "classStatsChanged": False,
        },
        "proxyAnchor": base["monsterAnchors"]["ARMORED_DURABLE_PROXY"],
        "rows": [],
        "schedules": {},
    }

    try:
        for name, d in variants.items():
            cfg = integ.stage_temporal(temporal, d, integration, 48, "Knight")
            out["schedules"][name] = [
                {"t": round(t, 3), "type": typ, "band": band}
                for t, typ, band in integ.build_integrated_schedule(cfg)
            ]
            for cls in integ.CLASSES:
                st = starts[(profile_name, cls)]
                trace = {}
                sim, _ = settled.simulate_stage(
                    base, temporal, d, integration, cls, st["profile"], scale,
                    48, st["startStage48Wall"], 0.25 if cls == "Tank" else None, 120.0,
                )
                s = trace.get("sieger") or {}
                sp, fd, fp, de = s.get("spawnAt"), s.get("firstDamageAt"), s.get("firstPrimaryAt"), s.get("deathAt")
                escort_deaths = [
                    x for x in (trace.get("deaths") or {}).values()
                    if x.get("type") == "ARMORED_DURABLE_PROXY"
                ]
                out["rows"].append({
                    "variant": name,
                    "class": cls,
                    "startWall": round(float(st["startStage48Wall"]), 3),
                    "endWall": sim.get("endWall"),
                    "wallLoss": round(float(st["startStage48Wall"]) - float(sim.get("endWall") or 0.0), 3),
                    "burialTime": sim.get("burialTime"),
                    "windups": int(sim.get("siegerWindups") or 0),
                    "shots": int(sim.get("siegerShots") or 0),
                    "repositions": int(sim.get("siegerRepositions") or 0),
                    "firstDamageAfterSpawn": round(fd-sp, 4) if fd is not None and sp is not None else None,
                    "firstPrimaryAfterSpawn": round(fp-sp, 4) if fp is not None and sp is not None else None,
                    "deathAfterSpawn": round(de-sp, 4) if de is not None and sp is not None else None,
                    "deathX": s.get("deathX"),
                    "diedBeforePrimary": bool(de is not None and (fp is None or de < fp - 1e-9)),
                    "escortDeaths": sorted(escort_deaths, key=lambda x: (x.get("time") or -1, x.get("x") or -1)),
                })
                trace = None
    finally:
        glb["hit"], glb["nearest"], glb["make_mob"] = old_hit, old_nearest, old_make

    text = json.dumps(out, indent=2, sort_keys=True)
    Path("p5_stage48_armored_low_density_front_temp.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
