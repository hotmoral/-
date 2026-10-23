#!/usr/bin/env python3
"""TEMP P5 Stage48 reduced-armored + fodder cross-class screen.

Goal: test whether the user-proposed fodder layer lets us reduce dependence on the extreme
ARMORED_DURABLE_PROXY count before touching any exact armor/HP value.
Diagnostic only. No packet/count/stat/timing is adopted or frozen.
"""
from __future__ import annotations

import inspect
import json
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage48_real_monster_frontline_search_temp_v2 as v2
import run_p5_stage48_armored_low_density_front_temp as low


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


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


def make(direction, name, rows):
    rows = list(rows) + [low.row("SIEGER", 2, 8.0, 2.0)]
    return low.make(direction, name, rows)


def p(typ, band, t):
    return low.row(typ, band, t)


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

    variants = {
        "P3_GRUNT2": make(direction, "P3_GRUNT2", [
            p("ARMORED_DURABLE_PROXY", -2, 5.25), p("ARMORED_DURABLE_PROXY", 0, 6.25), p("ARMORED_DURABLE_PROXY", -1, 7.25),
            p("GRUNT", 1, 5.85), p("GRUNT", -2, 6.98),
        ]),
        "P2_GRUNT2": make(direction, "P2_GRUNT2", [
            p("ARMORED_DURABLE_PROXY", -2, 5.25), p("ARMORED_DURABLE_PROXY", -1, 7.25),
            p("GRUNT", 1, 5.85), p("GRUNT", 0, 6.98),
        ]),
        "P2_BRUTE_GRUNT": make(direction, "P2_BRUTE_GRUNT", [
            p("ARMORED_DURABLE_PROXY", -2, 5.25), p("ARMORED_DURABLE_PROXY", -1, 7.25),
            p("BRUTE", 1, 5.85), p("GRUNT", 0, 6.98),
        ]),
        "P1_BRUTE_GRUNT": make(direction, "P1_BRUTE_GRUNT", [
            p("ARMORED_DURABLE_PROXY", -2, 6.25),
            p("BRUTE", 1, 5.85), p("GRUNT", 0, 6.98),
        ]),
        "P1_BRUTE2_GRUNT": make(direction, "P1_BRUTE2_GRUNT", [
            p("ARMORED_DURABLE_PROXY", -2, 6.25),
            p("BRUTE", 1, 5.25), p("BRUTE", -1, 6.15), p("GRUNT", 0, 6.98),
        ]),
        "REAL_BRUTE2_GRUNT2": make(direction, "REAL_BRUTE2_GRUNT2", [
            p("BRUTE", -2, 5.25), p("BRUTE", 1, 6.15),
            p("GRUNT", 0, 5.85), p("GRUNT", -1, 6.98),
        ]),
        "REAL_BRUTE3_GRUNT2": make(direction, "REAL_BRUTE3_GRUNT2", [
            p("BRUTE", -2, 5.05), p("BRUTE", 0, 5.95), p("BRUTE", -1, 6.85),
            p("GRUNT", 1, 5.55), p("GRUNT", 0, 6.98),
        ]),
    }

    scale = float(integration["shopEffectScale"])
    profile_name = "BALANCED"
    starts = v2.pre_stage48_states(base, temporal, direction, shop, integration, [profile_name], scale)

    glb = integ.SIMULATE.__globals__
    old_hit, old_make = glb["hit"], glb["make_mob"]
    trace = None

    def make_wrap(mon, cfg, typ, band, idx):
        m = old_make(mon, cfg, typ, band, idx)
        if trace is not None and typ == "SIEGER":
            trace["sieger"] = {"spawn": caller_now(), "first": None, "death": None, "deathX": None}
        return m

    def hit_wrap(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=False):
        t = caller_now()
        typ = getattr(target, "typ", None) if target is not None else None
        alive = bool(getattr(target, "alive", False)) if target is not None else False
        x = float(getattr(target, "x", 0.0)) if target is not None else None
        if trace is not None and typ == "SIEGER":
            s = trace.get("sieger")
            if s and s["first"] is None:
                s["first"] = t
                s["firstRaw"] = round(float(raw), 3)
        res = old_hit(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=armor_ignore)
        if trace is not None and typ == "SIEGER" and alive and not bool(getattr(target, "alive", False)):
            s = trace.get("sieger")
            if s and s["death"] is None:
                s["death"] = t
                s["deathX"] = round(x, 4)
        return res

    glb["hit"], glb["make_mob"] = hit_wrap, make_wrap
    out = {
        "version": "p5-stage48-reduced-armored-fodder-crossclass-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "fixed": {"shopProfile": profile_name, "shopEffectScale": scale, "siegerThresholdX": 0.38, "spawnX": 0.92},
        "proxyAnchor": base["monsterAnchors"]["ARMORED_DURABLE_PROXY"],
        "rows": [], "schedules": {},
    }
    try:
        for name, d in variants.items():
            cfg = integ.stage_temporal(temporal, d, integration, 48, "Mage")
            out["schedules"][name] = [{"t":round(t,3),"type":typ,"band":band} for t,typ,band in integ.build_integrated_schedule(cfg)]
            for cls in integ.CLASSES:
                st = starts[(profile_name, cls)]
                trace = {}
                sim, _ = settled.simulate_stage(
                    base, temporal, d, integration, cls, st["profile"], scale,
                    48, st["startStage48Wall"], 0.25 if cls == "Tank" else None, 120.0,
                )
                s = trace.get("sieger") or {}
                sp, first, death = s.get("spawn"), s.get("first"), s.get("death")
                out["rows"].append({
                    "variant": name, "class": cls,
                    "firstDamageAfterSpawn": round(first-sp,4) if first is not None and sp is not None else None,
                    "firstDamageRaw": s.get("firstRaw"),
                    "deathAfterSpawn": round(death-sp,4) if death is not None and sp is not None else None,
                    "deathX": s.get("deathX"),
                    "siegerWindups": int(sim.get("siegerWindups") or 0),
                    "siegerShots": int(sim.get("siegerShots") or 0),
                    "wallLoss": round(float(st["startStage48Wall"]) - float(sim.get("endWall") or 0.0),3),
                    "burialTime": sim.get("burialTime"),
                    "killsByType": sim.get("killsByType"),
                })
                trace = None
    finally:
        glb["hit"], glb["make_mob"] = old_hit, old_make

    text = json.dumps(out, indent=2, sort_keys=True)
    Path("p5_stage48_reduced_armored_fodder_crossclass_temp.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
