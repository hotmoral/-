#!/usr/bin/env python3
"""TEMP P5 Stage48 Mage fodder composition + phase robustness screen.

Follow-up to the first fodder chronology screen. Tests only late-arriving combinations that did not
prematurely shift Mage action phase in the first screen, across small SIEGER timing offsets.
Diagnostic only; no composition/timing/stat is adopted or frozen.
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


def make_packet(direction, name, sieger_t, fodder):
    rows = [
        low.row("ARMORED_DURABLE_PROXY", -2, sieger_t - 2.75),
        low.row("ARMORED_DURABLE_PROXY", 0, sieger_t - 1.75),
        low.row("ARMORED_DURABLE_PROXY", -1, sieger_t - 0.75),
    ]
    fodder_offsets = [-2.15, -1.02, -0.48]
    fodder_bands = [1, -2, 0]
    for i, typ in enumerate(fodder):
        rows.append(low.row(typ, fodder_bands[i], sieger_t + fodder_offsets[i]))
    rows.append(low.row("SIEGER", 2, sieger_t, 2.0))
    return low.make(direction, name, rows)


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

    compositions = {
        "NONE": (),
        "GRUNT2": ("GRUNT", "GRUNT"),
        "GRUNT3": ("GRUNT", "GRUNT", "GRUNT"),
        "GRUNT_RUNNER": ("GRUNT", "RUNNER"),
        "RUNNER_GRUNT": ("RUNNER", "GRUNT"),
        "GRUNT_FLYER": ("GRUNT", "FLYER"),
        "FLYER_GRUNT": ("FLYER", "GRUNT"),
        "GRUNT_BRUTE": ("GRUNT", "BRUTE"),
        "BRUTE_GRUNT": ("BRUTE", "GRUNT"),
        "BRUTE2_CONTROL": ("BRUTE", "BRUTE"),
    }
    sieger_times = [7.70, 8.00, 8.30]

    scale = float(integration["shopEffectScale"])
    profile_name = "BALANCED"
    starts = v2.pre_stage48_states(base, temporal, direction, shop, integration, [profile_name], scale)
    st = starts[(profile_name, "Mage")]

    glb = integ.SIMULATE.__globals__
    old_hit, old_make = glb["hit"], glb["make_mob"]
    trace = None

    def make_wrap(mon, cfg, typ, band, idx):
        m = old_make(mon, cfg, typ, band, idx)
        if trace is not None and typ == "SIEGER":
            trace["sieger"] = {"spawn": caller_now(), "first": None, "death": None, "deathX": None, "hits": []}
        return m

    def hit_wrap(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=False):
        t = caller_now()
        typ = getattr(target, "typ", None) if target is not None else None
        alive = bool(getattr(target, "alive", False)) if target is not None else False
        x = float(getattr(target, "x", 0.0)) if target is not None else None
        if trace is not None and typ == "SIEGER":
            s = trace.get("sieger")
            if s:
                s["hits"].append({"time": t, "raw": round(float(raw), 3), "x": round(x, 4)})
                if s["first"] is None:
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
        "version": "p5-stage48-mage-fodder-phase-screen-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "fixed": {"class": "Mage", "shopProfile": profile_name, "shopEffectScale": scale, "siegerThresholdX": 0.38},
        "rows": [],
    }
    try:
        for cname, fodder in compositions.items():
            for stime in sieger_times:
                d = make_packet(direction, f"{cname}_{stime:.2f}", stime, fodder)
                trace = {}
                sim, schedule = settled.simulate_stage(
                    base, temporal, d, integration, "Mage", st["profile"], scale,
                    48, st["startStage48Wall"], None, 120.0,
                )
                s = trace.get("sieger") or {}
                sp, first, death = s.get("spawn"), s.get("first"), s.get("death")
                out["rows"].append({
                    "composition": cname,
                    "fodder": list(fodder),
                    "siegerTime": stime,
                    "firstDamageAfterSpawn": round(first-sp, 4) if first is not None and sp is not None else None,
                    "firstDamageRaw": s.get("firstRaw"),
                    "deathAfterSpawn": round(death-sp, 4) if death is not None and sp is not None else None,
                    "deathX": s.get("deathX"),
                    "siegerShots": int(sim.get("siegerShots") or 0),
                    "siegerWindups": int(sim.get("siegerWindups") or 0),
                    "wallLoss": round(float(st["startStage48Wall"]) - float(sim.get("endWall") or 0.0), 3),
                    "burialTime": sim.get("burialTime"),
                    "hits": s.get("hits", []),
                    "schedule": [{"t": round(t,3), "type": typ, "band": band} for t,typ,band in schedule],
                })
                trace = None
    finally:
        glb["hit"], glb["make_mob"] = old_hit, old_make

    # Compact robustness summaries.
    summary = {}
    for cname in compositions:
        rs = [r for r in out["rows"] if r["composition"] == cname]
        deaths = [r["deathAfterSpawn"] for r in rs if r["deathAfterSpawn"] is not None]
        firsts = [r["firstDamageAfterSpawn"] for r in rs if r["firstDamageAfterSpawn"] is not None]
        summary[cname] = {
            "minDeathAfterSpawn": min(deaths) if deaths else None,
            "maxDeathAfterSpawn": max(deaths) if deaths else None,
            "minFirstDamageAfterSpawn": min(firsts) if firsts else None,
            "shotCases": sum(1 for r in rs if r["siegerShots"] > 0),
            "maxShots": max((r["siegerShots"] for r in rs), default=0),
        }
    out["summary"] = summary

    text = json.dumps(out, indent=2, sort_keys=True)
    Path("p5_stage48_mage_fodder_phase_screen_temp.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
