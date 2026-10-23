#!/usr/bin/env python3
"""TEMP P5 Stage48 Mage fodder chronology screen.

User-approved exploration axis:
- limited armored/strengthened frontline remains the primary Stage48 search direction;
- test whether ordinary small bodies can redirect/consume Mage follow-up targeting and extend SIEGER life.

Diagnostic only. No monster count, packet, timing, stat, skill rule, standoff distance, or production value is adopted/frozen.
"""
from __future__ import annotations

import copy
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


def packet(direction, name, fodder_type=None, times=()):
    rows = [
        low.row("ARMORED_DURABLE_PROXY", -2, 5.25),
        low.row("ARMORED_DURABLE_PROXY", 0, 6.25),
        low.row("ARMORED_DURABLE_PROXY", -1, 7.25),
    ]
    bands = [1, -2]
    if fodder_type:
        for i, t in enumerate(times):
            rows.append(low.row(fodder_type, bands[i % len(bands)], float(t)))
    rows.append(low.row("SIEGER", 2, 8.0, 2.0))
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

    variants = {
        "ARMORED3_ONLY": packet(direction, "ARMORED3_ONLY"),
    }
    # LATE_PAIR: bodies arrive after/around the penultimate Mage root window; minimizes pre-heavy exposure.
    # EARLY_PAIR: gives speed/durability time to produce real x-separation before the 8.075s heavy-final window.
    for typ in ["GRUNT", "RUNNER", "FLYER", "SHIELD", "SPLITTER", "BRUTE"]:
        variants[f"{typ}_LATE_PAIR"] = packet(direction, f"{typ}_LATE_PAIR", typ, (5.85, 6.98))
        variants[f"{typ}_EARLY_PAIR"] = packet(direction, f"{typ}_EARLY_PAIR", typ, (3.65, 5.85))

    scale = float(integration["shopEffectScale"])
    profile_name = "BALANCED"
    starts = v2.pre_stage48_states(base, temporal, direction, shop, integration, [profile_name], scale)
    st = starts[(profile_name, "Mage")]

    glb = integ.SIMULATE.__globals__
    old_hit, old_make = glb["hit"], glb["make_mob"]
    trace = None

    def make_wrap(mon, cfg, typ, band, idx):
        m = old_make(mon, cfg, typ, band, idx)
        if trace is not None:
            trace.setdefault("spawns", {})[str(m.id)] = {
                "type": typ, "time": caller_now(), "band": int(band),
            }
            if typ == "SIEGER":
                trace["sieger"] = {
                    "id": str(m.id), "spawnAt": caller_now(), "firstDamageAt": None,
                    "firstDamageRaw": None, "deathAt": None, "deathX": None,
                }
        return m

    def hit_wrap(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=False):
        t = caller_now()
        typ = getattr(target, "typ", None) if target is not None else None
        mid = str(getattr(target, "id", "")) if target is not None else ""
        before_alive = bool(getattr(target, "alive", False)) if target is not None else False
        before_x = float(getattr(target, "x", 0.0)) if target is not None else None
        if trace is not None and t is not None and 7.85 <= t <= 8.55:
            trace.setdefault("heavyWindowHits", []).append({
                "time": t, "targetType": typ, "targetId": mid, "raw": round(float(raw), 3),
                "x": round(before_x, 4) if before_x is not None else None,
            })
        if trace is not None and typ == "SIEGER":
            s = trace.get("sieger")
            if s and s["firstDamageAt"] is None:
                s["firstDamageAt"] = t
                s["firstDamageRaw"] = round(float(raw), 3)
        res = old_hit(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=armor_ignore)
        if trace is not None and target is not None and before_alive and not bool(getattr(target, "alive", False)):
            trace.setdefault("deaths", {})[mid] = {
                "type": typ, "time": t, "x": round(before_x, 4) if before_x is not None else None,
            }
            if typ == "SIEGER":
                s = trace.get("sieger")
                if s and s["deathAt"] is None:
                    s["deathAt"] = t
                    s["deathX"] = round(before_x, 4) if before_x is not None else None
        return res

    glb["hit"], glb["make_mob"] = hit_wrap, make_wrap

    out = {
        "version": "p5-stage48-mage-fodder-screen-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "fixed": {
            "class": "Mage", "shopProfile": profile_name, "shopEffectScale": scale,
            "spawnX": float(direction["globalRules"]["normalRightEdgeSpawnX"]),
            "siegerThresholdX": 0.38, "siegerSpawnSeconds": 8.0,
            "mageExpectedHeavyFinalSeconds": 8.075,
            "armoredProxyAnchor": base["monsterAnchors"]["ARMORED_DURABLE_PROXY"],
        },
        "monsterAnchors": {k: base["monsterAnchors"][k] for k in ["GRUNT", "RUNNER", "FLYER", "SHIELD", "SPLITTER", "BRUTE", "SIEGER"]},
        "rows": [], "schedules": {},
    }

    try:
        for name, d in variants.items():
            cfg = integ.stage_temporal(temporal, d, integration, 48, "Mage")
            out["schedules"][name] = [
                {"t": round(t, 3), "type": typ, "band": band}
                for t, typ, band in integ.build_integrated_schedule(cfg)
            ]
            trace = {}
            sim, _ = settled.simulate_stage(
                base, temporal, d, integration, "Mage", st["profile"], scale,
                48, st["startStage48Wall"], None, 120.0,
            )
            s = trace.get("sieger") or {}
            sp, fd, de = s.get("spawnAt"), s.get("firstDamageAt"), s.get("deathAt")
            out["rows"].append({
                "variant": name,
                "startWall": round(float(st["startStage48Wall"]), 3),
                "endWall": sim.get("endWall"),
                "wallLoss": round(float(st["startStage48Wall"]) - float(sim.get("endWall") or 0.0), 3),
                "burialTime": sim.get("burialTime"),
                "siegerWindups": int(sim.get("siegerWindups") or 0),
                "siegerShots": int(sim.get("siegerShots") or 0),
                "siegerFirstDamageAfterSpawn": round(fd-sp, 4) if fd is not None and sp is not None else None,
                "siegerFirstDamageRaw": s.get("firstDamageRaw"),
                "siegerDeathAfterSpawn": round(de-sp, 4) if de is not None and sp is not None else None,
                "siegerDeathX": s.get("deathX"),
                "killsByType": sim.get("killsByType"),
                "heavyWindowHits": trace.get("heavyWindowHits", []),
            })
            trace = None
    finally:
        glb["hit"], glb["make_mob"] = old_hit, old_make

    text = json.dumps(out, indent=2, sort_keys=True)
    Path("p5_stage48_mage_fodder_screen_temp.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
