#!/usr/bin/env python3
"""Timing Defense P5 identity-aware Stage46->49 integrated probe v0.1.

Purpose:
- keep every authored enemy at the normal right-edge spawn;
- convert spawnLeadSeconds into earlier schedule time with a warmup/reference offset;
- carry current wall HP, max HP, and absolute damage deficit Stage46->49;
- compare Tank Lv31 enemy-damage sensitivities 0.20/0.25/0.30 while preserving control;
- record Rogue Dagger Storm distinct-target telemetry and ordinary one-dagger breakpoints;
- rerun bounded Knight/Archer/Mage identity regressions with the same corrected kernel.

This is planning/harness evidence only. It does not authorize production changes or freeze values.
Cross-class KNOCK and CRIT/CRITDMG remain deferred.
"""
from __future__ import annotations

import argparse
import copy
import inspect
import json
from pathlib import Path

import run_p4d2_stage46_temporal_pressure_probe_v0_1 as stage46

CLASSES = ["Knight", "Rogue", "Tank", "Archer", "Mage"]
ORDINARY_DAGGER_WATCH = ("GRUNT", "RUNNER", "SHIELD")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def inject_diagnostic_monsters(base, fixture):
    out = copy.deepcopy(base)
    for typ, anchor in fixture.get("diagnosticMonsterAnchors", {}).items():
        out["monsterAnchors"][typ] = dict(anchor)
    return out


def profile_for(fixture, cls, name):
    if name == "ROLE_AWARE":
        source = fixture["roleAwareProfilesAtCenterSpendEnvelope"][cls]
    else:
        source = fixture["shopProfilesAtCenterSpendEnvelope"][name]
    return {
        "atk": int(source["atk"]),
        "fort": int(source["fort"]),
        "def": int(source["def"]),
    }


def build_integrated_schedule(cfg):
    """Return (spawn_time, type, band) tuples; make_mob owns physical spawnX."""
    integrated = cfg.get("integratedSchedule")
    if not integrated:
        return stage46.build_schedule(cfg)

    duration = float(cfg["simulation"]["durationSeconds"])
    cycle = float(cfg["simulation"]["pressureCycleSeconds"])
    warmup = float(integrated["referenceWarmupSeconds"])
    packet = integrated["packet"]

    out = []
    reference = warmup
    while reference - float(integrated.get("maxLeadSeconds", 0.0)) < duration:
        for row in packet:
            st = reference + float(row["referenceOffset"]) - float(row["spawnLeadSeconds"])
            if -1e-9 <= st < duration:
                out.append((max(0.0, st), row["type"], int(row["band"])))
        reference += cycle
    return sorted(out, key=lambda x: (x[0], x[1], x[2]))


def build_identity_aware_simulate():
    """Patch only simulate-owned lines; apply ATK through a guarded global hit wrapper."""
    src = inspect.getsource(stage46.simulate)
    ctx = {
        "shop_atk_pct": 0.0,
        "cls": None,
        "active_rogue_storm_id": None,
    }

    original_hit = stage46.hit

    def shop_hit(mon, cfg, mobs, m, raw, stats, counter, armor_ignore=False):
        if not m or not m.alive:
            return 0.0, False
        pre_hp = float(m.hp)
        pre_max = float(m.max_hp)
        typ = m.typ
        mob_id = m.id

        actual, killed = original_hit(
            mon,
            cfg,
            mobs,
            m,
            float(raw) * (1.0 + float(ctx["shop_atk_pct"])),
            stats,
            counter,
            armor_ignore=armor_ignore,
        )

        storm_id = ctx.get("active_rogue_storm_id")
        if ctx.get("cls") == "Rogue" and storm_id is not None:
            storm = stats["rogueStormTelemetry"][storm_id]
            storm["targetsHit"].add(mob_id)
            storm["targetTypesHit"].add(typ)
            if killed:
                storm["targetsKilled"].add(mob_id)
                storm["targetTypesKilled"].add(typ)
            if typ in ORDINARY_DAGGER_WATCH and abs(pre_hp - pre_max) <= 1e-9:
                storm["freshOrdinaryEvents"].append(
                    {
                        "type": typ,
                        "targetId": mob_id,
                        "preHp": round(pre_hp, 6),
                        "damage": round(actual, 6),
                        "killed": bool(killed),
                    }
                )
        return actual, killed

    old_sig = (
        "def simulate(base, temporal, cls, has_lv31=True, "
        "missed_heavy_indices=(), overrides=None):\n"
    )
    new_sig = (
        "def simulate(base, temporal, cls, has_lv31=True, "
        "missed_heavy_indices=(), overrides=None, shop_profile=None, "
        "effect_scale=0.0, start_wall_current=None):\n"
    )
    if src.count(old_sig) != 1:
        raise RuntimeError("Stage46 simulate signature changed; integrated patch review required")
    src = src.replace(old_sig, new_sig, 1)

    old_cand = (
        '    cand = center_candidates(base, cfg, cls)\n'
        '    if overrides:\n'
        '        cand.update(overrides)\n\n'
    )
    new_cand = (
        '    cand = center_candidates(base, cfg, cls)\n'
        '    if overrides:\n'
        '        cand.update(overrides)\n'
        '    shop_profile = shop_profile or {"atk":0,"fort":0,"def":0}\n'
        '    effect_scale = float(effect_scale)\n'
        '    shop_atk_pct = float(shop_profile.get("atk",0)) * 0.08 * effect_scale\n'
        '    shop_fort_flat = float(shop_profile.get("fort",0)) * 100.0 * effect_scale\n'
        '    shop_generic_def = min(0.60, float(shop_profile.get("def",0)) * 0.025 * effect_scale)\n'
        '    _p5_ctx["shop_atk_pct"] = shop_atk_pct\n'
        '    _p5_ctx["cls"] = cls\n'
        '    _p5_ctx["active_rogue_storm_id"] = None\n\n'
    )
    if src.count(old_cand) != 1:
        raise RuntimeError("Stage46 candidate block changed; integrated patch review required")
    src = src.replace(old_cand, new_cand, 1)

    old_schedule = '    schedule = build_schedule(cfg)\n'
    new_schedule = '    schedule = build_integrated_schedule(cfg)\n'
    if src.count(old_schedule) != 1:
        raise RuntimeError("Stage46 schedule line changed")
    src = src.replace(old_schedule, new_schedule, 1)

    old_wall = '    wall_max = float(sim["wallHp"])\n'
    new_wall = (
        '    wall_max = (float(sim["wallHp"]) + shop_fort_flat) '
        'if start_wall_current is None else float(start_wall_current)\n'
    )
    if src.count(old_wall) != 1:
        raise RuntimeError("Stage46 starting-wall line changed")
    src = src.replace(old_wall, new_wall, 1)

    old_sieger = '                    incoming = 75.0\n'
    new_sieger = (
        '                    incoming = 75.0 * (1.0 - shop_generic_def) '
        '* (0.90 if cls == "Tank" else 1.0)\n'
    )
    if src.count(old_sieger) != 1:
        raise RuntimeError("Stage46 SIEGER incoming line changed")
    src = src.replace(old_sieger, new_sieger, 1)

    old_contact = '                incoming = m.wall * (0.90 if cls == "Tank" else 1.0)\n'
    new_contact = (
        '                incoming = m.wall * (1.0 - shop_generic_def) '
        '* (0.90 if cls == "Tank" else 1.0)\n'
    )
    if src.count(old_contact) != 1:
        raise RuntimeError("Stage46 wall-contact incoming line changed")
    src = src.replace(old_contact, new_contact, 1)

    old_stats_tail = '        "aftershockZones": [],\n    }'
    new_stats_tail = (
        '        "aftershockZones": [],\n'
        '        "shieldSource": None,\n'
        '        "heavyTimeline": [],\n'
        '        "noTargetDrops": 0,\n'
        '        "shopProfile": dict(shop_profile),\n'
        '        "shopEffectScale": effect_scale,\n'
        '        "shopAtkPct": shop_atk_pct,\n'
        '        "shopFortFlat": shop_fort_flat,\n'
        '        "shopGenericDef": shop_generic_def,\n'
        '        "rogueStormSequence": 0,\n'
        '        "rogueStormTelemetry": {},\n'
        '    }'
    )
    if src.count(old_stats_tail) != 1:
        raise RuntimeError("Stage46 stats block changed")
    src = src.replace(old_stats_tail, new_stats_tail, 1)

    old_rogue_final = (
        '        if final:\n'
        '            n = int(cand["daggers"])\n'
        '            duration_storm = float(cand["stormDurationSeconds"])\n'
        '            raw = 600 * float(cand["perDaggerCoefficient"])\n'
        '            denom = max(1, n - 1)\n'
        '            for k in range(n):\n'
        '                def dagger():\n'
        '                    p = nearest(mobs)\n'
        '                    if p:\n'
        '                        hit(mon, cfg, mobs, p, raw, stats, counter)\n'
        '                schedule_event(now + k * duration_storm / denom, dagger)\n'
        '            return\n'
    )
    new_rogue_final = (
        '        if final:\n'
        '            n = int(cand["daggers"])\n'
        '            duration_storm = float(cand["stormDurationSeconds"])\n'
        '            raw = 600 * float(cand["perDaggerCoefficient"])\n'
        '            stats["rogueStormSequence"] += 1\n'
        '            storm_id = str(stats["rogueStormSequence"])\n'
        '            stats["rogueStormTelemetry"][storm_id] = {\n'
        '                "targetsHit": set(), "targetsKilled": set(),\n'
        '                "targetTypesHit": set(), "targetTypesKilled": set(),\n'
        '                "freshOrdinaryEvents": [],\n'
        '            }\n'
        '            denom = max(1, n - 1)\n'
        '            for k in range(n):\n'
        '                def dagger(storm_id=storm_id):\n'
        '                    p = nearest(mobs)\n'
        '                    if p:\n'
        '                        _p5_ctx["active_rogue_storm_id"] = storm_id\n'
        '                        try:\n'
        '                            hit(mon, cfg, mobs, p, raw, stats, counter)\n'
        '                        finally:\n'
        '                            _p5_ctx["active_rogue_storm_id"] = None\n'
        '                schedule_event(now + k * duration_storm / denom, dagger)\n'
        '            return\n'
    )
    if src.count(old_rogue_final) != 1:
        raise RuntimeError("Stage46 Rogue final block changed")
    src = src.replace(old_rogue_final, new_rogue_final, 1)

    old_attack_guard = '        if now >= next_attack - 1e-9 and nearest(mobs):\n'
    new_attack_guard = (
        '        if now >= next_attack - 1e-9 and not nearest(mobs):\n'
        '            stats["noTargetDrops"] += 1\n'
        '            next_attack = now + root_interval\n\n'
        '        if now >= next_attack - 1e-9 and nearest(mobs):\n'
    )
    if src.count(old_attack_guard) != 1:
        raise RuntimeError("Stage46 attack guard changed")
    src = src.replace(old_attack_guard, new_attack_guard, 1)

    old_heavy = '            if heavy:\n                heavy_index += 1\n'
    new_heavy = (
        '            if heavy:\n'
        '                heavy_index += 1\n'
        '                stats["heavyTimeline"].append({"index": heavy_index, "time": round(now, 3)})\n'
    )
    if src.count(old_heavy) != 1:
        raise RuntimeError("Stage46 heavy block changed")
    src = src.replace(old_heavy, new_heavy, 1)

    old_final_barrier = (
        '            stats["shield"] = float(cand["barrier"])\n'
        '            stats["shieldUntil"] = now + float(cand["barrierSeconds"])\n'
    )
    new_final_barrier = (
        '            stats["shield"] = float(cand["barrier"])\n'
        '            stats["shieldUntil"] = now + float(cand["barrierSeconds"])\n'
        '            stats["shieldSource"] = "LV31"\n'
    )
    if src.count(old_final_barrier) != 1:
        raise RuntimeError("Stage46 Lv31 barrier block changed")
    src = src.replace(old_final_barrier, new_final_barrier, 1)

    old_lv16 = (
        '        if not heavy and tier == "PERFECT":\n'
        '            stats["shield"] = 80.0\n'
        '            stats["shieldUntil"] = now + 3.0\n'
    )
    new_lv16 = (
        '        if not heavy and tier == "PERFECT":\n'
        '            if stats["shield"] <= 1e-9 or stats.get("shieldSource") != "LV31":\n'
        '                stats["shield"] = 80.0\n'
        '                stats["shieldUntil"] = now + 3.0\n'
        '                stats["shieldSource"] = "LV16"\n'
    )
    if src.count(old_lv16) != 1:
        raise RuntimeError("Stage46 Lv16 barrier block changed")
    src = src.replace(old_lv16, new_lv16, 1)

    old_expiry = (
        '        if stats["shield"] > 0 and now >= stats["shieldUntil"]:\n'
        '            stats["shield"] = 0.0\n'
    )
    new_expiry = (
        '        if stats["shield"] > 0 and now >= stats["shieldUntil"]:\n'
        '            stats["shield"] = 0.0\n'
        '            stats["shieldSource"] = None\n'
    )
    if src.count(old_expiry) != 1:
        raise RuntimeError("Stage46 shield expiry block changed")
    src = src.replace(old_expiry, new_expiry, 1)

    sieger_absorb = '\n                    stats["shield"] -= absorb\n'
    wall_absorb = '\n                stats["shield"] -= absorb\n'
    if src.count(sieger_absorb) != 1 or src.count(wall_absorb) != 1:
        raise RuntimeError("Stage46 shield absorb sites changed")
    src = src.replace(
        sieger_absorb,
        sieger_absorb
        + '                    if stats["shield"] <= 1e-9:\n'
        + '                        stats["shieldSource"] = None\n',
        1,
    )
    src = src.replace(
        wall_absorb,
        wall_absorb
        + '                if stats["shield"] <= 1e-9:\n'
        + '                    stats["shieldSource"] = None\n',
        1,
    )

    old_cleanup = (
        '    stats.pop("shield", None)\n'
        '    stats.pop("shieldUntil", None)\n'
        '    stats.pop("aftershockZones", None)\n'
        '    return stats\n'
    )
    new_cleanup = (
        '    for storm in stats["rogueStormTelemetry"].values():\n'
        '        storm["distinctTargetsHit"] = len(storm["targetsHit"])\n'
        '        storm["distinctTargetsKilled"] = len(storm["targetsKilled"])\n'
        '        storm["targetsHit"] = sorted(storm["targetsHit"])\n'
        '        storm["targetsKilled"] = sorted(storm["targetsKilled"])\n'
        '        storm["targetTypesHit"] = sorted(storm["targetTypesHit"])\n'
        '        storm["targetTypesKilled"] = sorted(storm["targetTypesKilled"])\n'
        '    stats.pop("shield", None)\n'
        '    stats.pop("shieldUntil", None)\n'
        '    stats.pop("shieldSource", None)\n'
        '    stats.pop("aftershockZones", None)\n'
        '    return stats\n'
    )
    if src.count(old_cleanup) != 1:
        raise RuntimeError("Stage46 cleanup block changed")
    src = src.replace(old_cleanup, new_cleanup, 1)

    ns = dict(vars(stage46))
    ns["hit"] = shop_hit
    ns["_p5_ctx"] = ctx
    ns["build_integrated_schedule"] = build_integrated_schedule
    exec(src, ns)
    return ns["simulate"]


SIMULATE = build_identity_aware_simulate()


def stage_temporal(base_temporal, direction, integration, stage_no, cls):
    cfg = copy.deepcopy(base_temporal)
    stage_key = str(stage_no)
    rule = direction["stageDirection"][stage_key]
    cfg["version"] = f'p5-identity-aware-stage{stage_key}-runtime-v0.1'
    cfg["simulation"]["durationSeconds"] = float(integration["stageWindowSeconds"])
    cfg["simulation"]["pressureCycleSeconds"] = float(rule["pressureCycleSecondsCandidate"])
    cfg["simulation"]["spawnX"] = float(direction["globalRules"]["normalRightEdgeSpawnX"])
    cfg["simulation"]["rootAttackIntervalSeconds"] = 1.047 if cls == "Rogue" else 1.125

    packet = rule.get("diagnosticPacket")
    if packet:
        max_lead = max(float(r["spawnLeadSeconds"]) for r in packet)
        cfg["integratedSchedule"] = {
            "referenceWarmupSeconds": float(integration["referenceWarmupSeconds"]),
            "maxLeadSeconds": max_lead,
            "packet": copy.deepcopy(packet),
        }
    else:
        cfg.pop("integratedSchedule", None)
    return cfg


def slim_stage(row):
    keys = [
        "endWall", "endActive", "maxActive", "kills", "killsByType", "damage",
        "burialTime", "wallHits", "pxpCount", "heavyMissCount", "noTargetDrops",
        "siegerShots", "siegerRepositions", "shopAtkPct", "shopFortFlat",
        "shopGenericDef", "rogueStormTelemetry",
    ]
    return {k: row.get(k) for k in keys}


def rogue_analytic_breakpoints(base, base_temporal, profile, scale):
    dagger_raw = 600.0 * float(
        base_temporal["lv31TemporalCenters"]["Rogue"]["perDaggerCoefficient"]
    )
    atk_pct = float(profile["atk"]) * 0.08 * float(scale)
    result = {}
    for typ in ORDINARY_DAGGER_WATCH:
        a = base["monsterAnchors"][typ]
        damage = dagger_raw * (1.0 + atk_pct) * float(a["armor"])
        result[typ] = {
            "hp": float(a["hp"]),
            "armor": float(a["armor"]),
            "oneDaggerRawBeforeArmor": round(dagger_raw * (1.0 + atk_pct), 6),
            "oneDaggerDamageAtFreshHp": round(min(float(a["hp"]), damage), 6),
            "freshOneDaggerOneShot": bool(damage + 1e-9 >= float(a["hp"])),
        }
    return result


def run_chain(base, base_temporal, direction, integration, shop_fixture, cls, profile_name, scale, tank_coeff=None):
    profile = profile_for(shop_fixture, cls, profile_name)
    fort_flat = float(profile["fort"]) * 100.0 * float(scale)
    base_max = float(integration["startingBaseWallHp"])
    wall_max = base_max + fort_flat
    current = wall_max
    stages = []
    rogue_storms = []

    for stage_no in (46, 47, 48, 49):
        cfg = stage_temporal(base_temporal, direction, integration, stage_no, cls)
        start_deficit = max(0.0, wall_max - current)
        overrides = {}
        if cls == "Tank" and tank_coeff is not None:
            overrides["shockwaveCoefficient"] = float(tank_coeff)

        row = SIMULATE(
            base,
            cfg,
            cls,
            True,
            (),
            overrides=overrides or None,
            shop_profile=profile,
            effect_scale=float(scale),
            start_wall_current=current,
        )
        current = float(row["endWall"])
        end_deficit = max(0.0, wall_max - current)
        stages.append(
            {
                "stage": stage_no,
                "startCurrentWall": round(wall_max - start_deficit, 3),
                "maxWall": round(wall_max, 3),
                "startAbsoluteDeficit": round(start_deficit, 3),
                "endCurrentWall": round(current, 3),
                "endAbsoluteDeficit": round(end_deficit, 3),
                "result": slim_stage(row),
            }
        )
        if cls == "Rogue":
            for storm_id, storm in row.get("rogueStormTelemetry", {}).items():
                rogue_storms.append({"stage": stage_no, "stormId": storm_id, **storm})
        if row.get("burialTime") is not None:
            break

    return {
        "class": cls,
        "profile": profile_name,
        "effectScale": float(scale),
        "tankShockwaveCoefficient": tank_coeff if cls == "Tank" else None,
        "shopRanksUsedAsFixedLateSegmentDiagnostic": profile,
        "shopTemporalAcquisitionMode": integration["shopTemporalAcquisitionMode"],
        "startingMaxWall": round(wall_max, 3),
        "stagesCompleted": len(stages),
        "survivedThroughStage49": len(stages) == 4 and stages[-1]["result"]["burialTime"] is None,
        "finalWall": round(current, 3),
        "finalAbsoluteDeficit": round(max(0.0, wall_max - current), 3),
        "stages": stages,
        "rogueStorms": rogue_storms,
        "rogueOrdinaryOneShotAnalytic": (
            rogue_analytic_breakpoints(base, base_temporal, profile, scale)
            if cls == "Rogue" else None
        ),
    }


def make_finite_temporal(stage49, scenario, duration, cls):
    out = copy.deepcopy(stage49)
    out["version"] = "p5-identity-aware-finite-regression-runtime-v0.1"
    out["pressurePatternLabels"] = [scenario["id"]]
    out["pressurePatterns"] = [copy.deepcopy(scenario["rows"])]
    out["simulation"]["durationSeconds"] = float(duration)
    out["simulation"]["pressureCycleSeconds"] = 999.0
    out["simulation"]["spawnX"] = 0.92
    out["simulation"]["wallHp"] = float(scenario.get("wallHp", 2000.0))
    out["simulation"]["firstRootAttackSeconds"] = float(scenario.get("firstRootAttackSeconds", 0.2))
    out["simulation"]["rootAttackIntervalSeconds"] = 1.047 if cls == "Rogue" else 1.125
    out["simulation"]["heavyEveryRootActions"] = 4
    out.pop("integratedSchedule", None)
    return out


def direct_clear(row, expected_kills):
    return (
        row.get("burialTime") is None
        and int(row.get("wallHits", 0)) == 0
        and int(row.get("kills", 0)) == int(expected_kills)
        and int(row.get("endActive", 0)) == 0
    )


def finite_clear_time(base, stage49, shop_fixture, scenario, cls, profile_name, scale, overrides=None):
    expected = int(scenario["expectedDirectKills"])
    max_offset = max(float(r["offset"]) for r in scenario["rows"])
    lo = max_offset + 0.25
    hi = float(scenario.get("maxClearScanSeconds", 120.0))
    profile = profile_for(shop_fixture, cls, profile_name)

    def once(duration):
        temporal = make_finite_temporal(stage49, scenario, duration, cls)
        return SIMULATE(
            base,
            temporal,
            cls,
            True,
            (),
            overrides=overrides,
            shop_profile=profile,
            effect_scale=float(scale),
        )

    high = once(hi)
    if not direct_clear(high, expected):
        return None
    for _ in range(14):
        mid = (lo + hi) / 2.0
        row = once(mid)
        if direct_clear(row, expected):
            hi = mid
        else:
            lo = mid
    return round(hi, 3)


def scenario_by_id(radar, scenario_id):
    for row in radar["scenarios"]:
        if row["id"] == scenario_id:
            return copy.deepcopy(row)
    raise KeyError(scenario_id)


def refined_knight_scenario(refinement, aligned):
    k = refinement["knightRobustPair"]
    bands = k["alignedBands"] if aligned else k["dispersedBands"]
    rows = [
        {"offset": float(off), "type": k["monster"], "band": int(band)}
        for off, band in zip(k["spawnOffsetsSeconds"], bands)
    ]
    return {
        "id": "KNIGHT_REFINED_ALIGNED" if aligned else "KNIGHT_REFINED_DISPERSED",
        "expectedDirectKills": int(k["monsterCount"]),
        "maxClearScanSeconds": 120.0,
        "rows": rows,
    }


def run_identity_regressions(base, stage49, shop_fixture, radar, refinement, scale, tank_coeffs):
    result = {"Knight": {}, "Archer": {}, "Mage": {}, "Tank": {}}

    ka = refined_knight_scenario(refinement, True)
    kd = refined_knight_scenario(refinement, False)
    for profile in ("BALANCED", "DEFENSE_HEAVY"):
        result["Knight"][profile] = {
            "aligned": finite_clear_time(base, stage49, shop_fixture, ka, "Knight", profile, scale),
            "dispersed": finite_clear_time(base, stage49, shop_fixture, kd, "Knight", profile, scale),
        }

    aa = scenario_by_id(radar, "ARCHER_ALIGNED_LINE")
    asc = scenario_by_id(radar, "ARCHER_SCATTER")
    for profile in ("BALANCED", "ATTACK_HEAVY"):
        result["Archer"][profile] = {
            "aligned": finite_clear_time(base, stage49, shop_fixture, aa, "Archer", profile, scale),
            "scatter": finite_clear_time(base, stage49, shop_fixture, asc, "Archer", profile, scale),
        }

    mc = scenario_by_id(radar, "MAGE_CLUSTER")
    md = scenario_by_id(radar, "MAGE_DISTRIBUTED")
    result["Mage"]["BALANCED"] = {
        "cluster": finite_clear_time(base, stage49, shop_fixture, mc, "Mage", "BALANCED", scale),
        "distributed": finite_clear_time(base, stage49, shop_fixture, md, "Mage", "BALANCED", scale),
    }

    tm = scenario_by_id(radar, "TANK_MIXED_SOLO")
    for coeff in tank_coeffs:
        result["Tank"][str(coeff)] = finite_clear_time(
            base,
            stage49,
            shop_fixture,
            tm,
            "Tank",
            "BALANCED",
            scale,
            overrides={"shockwaveCoefficient": float(coeff)},
        )

    result["directionalReference"] = {
        "Knight": refinement["knightRobustPair"]["directionalReference"],
        "Archer": {
            "balancedAlignedApprox": 3.58,
            "balancedScatterApprox": 8.08,
        },
        "Mage": {
            "balancedClusterApprox": 3.78,
            "balancedDistributedApprox": 8.08,
        },
        "thresholdsFrozen": False,
    }
    return result


def validate_right_edge_contract(direction):
    expected = float(direction["globalRules"]["normalRightEdgeSpawnX"])
    if expected != 0.92:
        raise RuntimeError(f"normal right-edge spawn changed: {expected}")
    if direction["globalRules"].get("midFieldPopInAllowed", True):
        raise RuntimeError("mid-field pop-in must remain forbidden")
    for stage_no in ("48", "49"):
        for row in direction["stageDirection"][stage_no]["diagnosticPacket"]:
            if "spawnX" in row:
                raise RuntimeError(f"Stage{stage_no} packet must not author row-level spawnX")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--base-fixture",
        default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json",
    )
    ap.add_argument(
        "--base-temporal-fixture",
        default="legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json",
    )
    ap.add_argument(
        "--stage49-fixture",
        default="legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json",
    )
    ap.add_argument(
        "--direction-fixture",
        default="legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json",
    )
    ap.add_argument(
        "--shop-fixture",
        default="legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json",
    )
    ap.add_argument(
        "--radar-fixture",
        default="legacy-game-structure/data/p5_class_identity_radar_probe_fixture_v0_1.json",
    )
    ap.add_argument(
        "--refinement-fixture",
        default="legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json",
    )
    ap.add_argument(
        "--integration-fixture",
        default="legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json",
    )
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    base = load(args.base_fixture)
    base_temporal = load(args.base_temporal_fixture)
    stage49 = load(args.stage49_fixture)
    direction = load(args.direction_fixture)
    shop_fixture = load(args.shop_fixture)
    radar = load(args.radar_fixture)
    refinement = load(args.refinement_fixture)
    integration = load(args.integration_fixture)

    validate_right_edge_contract(direction)
    base = inject_diagnostic_monsters(base, stage49)
    if "ARMORED_DURABLE_PROXY" not in base["monsterAnchors"]:
        base["monsterAnchors"]["ARMORED_DURABLE_PROXY"] = dict(
            refinement["knightRobustPair"]["anchor"]
        )

    scale = float(integration["shopEffectScale"])
    tank_coeffs = [float(x) for x in integration["tankShockwaveDamageSensitivity"]]
    profiles = list(integration["representativeShopProfiles"])

    chains = []
    for profile in profiles:
        for cls in CLASSES:
            coeffs = tank_coeffs if cls == "Tank" else [None]
            for coeff in coeffs:
                chains.append(
                    run_chain(
                        base,
                        base_temporal,
                        direction,
                        integration,
                        shop_fixture,
                        cls,
                        profile,
                        scale,
                        tank_coeff=coeff,
                    )
                )

    identity = run_identity_regressions(
        base,
        stage49,
        shop_fixture,
        radar,
        refinement,
        scale,
        tank_coeffs,
    )

    output = {
        "version": "p5-identity-aware-stage46-49-integrated-result-v0.1",
        "status": "COMMITTED_RUNNER_EXACT_REPLAY_REQUIRED_NO_PRODUCTION_AUTHORITY",
        "rng": "NONE",
        "normalRightEdgeSpawnX": direction["globalRules"]["normalRightEdgeSpawnX"],
        "midFieldPopInAllowed": False,
        "stageWindowSeconds": integration["stageWindowSeconds"],
        "shopTemporalBoundary": integration["shopTemporalBoundary"],
        "crossClassShopFamilies": ["ATK", "FORTIFICATION", "DEFENSE"],
        "tankControlPackageChanged": False,
        "chains": chains,
        "identityRegressions": identity,
        "interpretationBoundary": [
            "Tank 0.20/0.25/0.30 are sensitivity values, not a freeze.",
            "Fixed late-segment shop power isolates identity/chronology and does not model acquisition-time ATK/DEF history.",
            "FORT max/current semantics preserve absolute deficit; this runner carries the resulting deficit between stages.",
            "Every authored enemy physically spawns at normal right edge; spawnLeadSeconds changes schedule time only.",
            "Rogue deterministic retarget remains unchanged.",
            "KNOCK and CRIT/CRITDMG cross-class policy remain deferred.",
            "Stage46-49 cycle/packet coordinates remain authoring diagnostics only.",
            "Production gameplay changes remain unauthorized."
        ]
    }

    text = json.dumps(output, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
