#!/usr/bin/env python3
"""Timing Defense P5 all-class fixed-rank Stage49 shop-combat probe v0.1.

Cross-class-authoritative families in this lane:
- ATK
- FORTIFICATION
- DEFENSE

Deliberately deferred:
- KNOCKBACK: current P4 diagnostic kernel does not model ordinary push symmetrically across all five classes.
- CRIT / CRIT DAMAGE: attack-template crit policy is effect-specific.

Uses the recovered Tank Lv11 Iron Wall rule on SIEGER shots.
No production value/content is frozen.
"""
from __future__ import annotations

import argparse
import copy
import inspect
import json
from pathlib import Path

import run_p4d2_stage46_temporal_pressure_probe_v0_1 as stage46
import run_p4d2_stage48_49_dynamic_grammar_probe_v0_2 as v02

CLASSES = ["Knight", "Rogue", "Tank", "Archer", "Mage"]
PRIMARY_LANE = {
    "Knight": "COMMON_1P125_NO_BANK",
    "Rogue": "ROGUE_RECOVERY_DELTA_78MS_NO_BANK",
    "Tank": "COMMON_1P125_NO_BANK",
    "Archer": "COMMON_1P125_NO_BANK",
    "Mage": "COMMON_1P125_NO_BANK",
}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def inject_diagnostic_monsters(base, fixture):
    out = copy.deepcopy(base)
    for typ, anchor in fixture.get("diagnosticMonsterAnchors", {}).items():
        out["monsterAnchors"][typ] = dict(anchor)
    return out


def build_shop_simulate():
    src = inspect.getsource(stage46.simulate)

    old_sig = 'def simulate(base, temporal, cls, has_lv31=True, missed_heavy_indices=(), overrides=None):\n'
    new_sig = 'def simulate(base, temporal, cls, has_lv31=True, missed_heavy_indices=(), overrides=None, shop_profile=None, effect_scale=0.0):\n'
    if src.count(old_sig) != 1:
        raise RuntimeError("Stage46 simulate signature changed; P5 all-class shop patch must be reviewed")
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
        '    shop_generic_def = min(0.60, float(shop_profile.get("def",0)) * 0.025 * effect_scale)\n\n'
    )
    if src.count(old_cand) != 1:
        raise RuntimeError("Stage46 candidate block changed; P5 all-class shop patch must be reviewed")
    src = src.replace(old_cand, new_cand, 1)

    old_wall_max = '    wall_max = float(sim["wallHp"])\n'
    new_wall_max = '    wall_max = float(sim["wallHp"]) + shop_fort_flat\n'
    if src.count(old_wall_max) != 1:
        raise RuntimeError("Stage46 wall max line changed")
    src = src.replace(old_wall_max, new_wall_max, 1)

    old_actual = '    actual = min(m.hp, float(raw) * (1.0 if armor_ignore else m.armor))\n'
    new_actual = '    actual = min(m.hp, float(raw) * (1.0 + shop_atk_pct) * (1.0 if armor_ignore else m.armor))\n'
    if src.count(old_actual) != 1:
        raise RuntimeError("Stage46 hit raw-power line changed")
    src = src.replace(old_actual, new_actual, 1)

    old_sieger = '                    incoming = 75.0\n'
    new_sieger = '                    incoming = 75.0 * (1.0 - shop_generic_def) * (0.90 if cls == "Tank" else 1.0)\n'
    if src.count(old_sieger) != 1:
        raise RuntimeError("Expected exactly one SIEGER incoming line")
    src = src.replace(old_sieger, new_sieger, 1)

    old_wall = '                incoming = m.wall * (0.90 if cls == "Tank" else 1.0)\n'
    new_wall = '                incoming = m.wall * (1.0 - shop_generic_def) * (0.90 if cls == "Tank" else 1.0)\n'
    if src.count(old_wall) != 1:
        raise RuntimeError("Expected exactly one ordinary wall incoming line")
    src = src.replace(old_wall, new_wall, 1)

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
        '    }'
    )
    if src.count(old_stats_tail) != 1:
        raise RuntimeError("Stage46 stats shape changed")
    src = src.replace(old_stats_tail, new_stats_tail, 1)

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
        raise RuntimeError("Stage46 Heavy block changed")
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
        raise RuntimeError("Stage46 Lv16 guard block changed")
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
        sieger_absorb + '                    if stats["shield"] <= 1e-9:\n                        stats["shieldSource"] = None\n',
        1,
    )
    src = src.replace(
        wall_absorb,
        wall_absorb + '                if stats["shield"] <= 1e-9:\n                    stats["shieldSource"] = None\n',
        1,
    )

    old_pop = (
        '    stats.pop("shield", None)\n'
        '    stats.pop("shieldUntil", None)\n'
        '    stats.pop("aftershockZones", None)\n'
    )
    new_pop = (
        '    stats.pop("shield", None)\n'
        '    stats.pop("shieldUntil", None)\n'
        '    stats.pop("shieldSource", None)\n'
        '    stats.pop("aftershockZones", None)\n'
    )
    if src.count(old_pop) != 1:
        raise RuntimeError("Stage46 cleanup block changed")
    src = src.replace(old_pop, new_pop, 1)

    ns = dict(vars(stage46))
    exec(src, ns)
    return ns["simulate"]


SIMULATE = build_shop_simulate()


def lane_fixture(stage49, cls):
    lane = PRIMARY_LANE[cls]
    return v02.lane_fixture(stage49, cls, lane)[0], lane


def slim(row):
    keys = [
        "endWall", "endActive", "maxActive", "kills", "burialTime", "wallHits",
        "pxpCount", "heavyMissCount", "noTargetDrops", "siegerShots", "siegerRepositions",
        "shopAtkPct", "shopFortFlat", "shopGenericDef",
    ]
    return {k: row.get(k) for k in keys}


def profile_for(fixture, cls, name):
    if name == "ROLE_AWARE":
        source = fixture["roleAwareProfilesAtCenterSpendEnvelope"][cls]
    else:
        source = fixture["shopProfilesAtCenterSpendEnvelope"][name]
    return {"atk": int(source["atk"]), "fort": int(source["fort"]), "def": int(source["def"])}


def first_by_grammar(stage49, row):
    timeline = v02.annotate_timeline(stage49, row["heavyTimeline"])
    return v02.choose_first_heavy_by_grammar(timeline)


def run_case(base, stage49, fixture, cls, profile_name, scale, detailed=False):
    f, lane = lane_fixture(stage49, cls)
    profile = profile_for(fixture, cls, profile_name)
    success = SIMULATE(base, f, cls, True, (), shop_profile=profile, effect_scale=scale)
    first = first_by_grammar(f, success)

    one = {}
    two = {}
    for grammar in f["pressurePatternLabels"]:
        start = int(first[grammar])
        one[grammar] = slim(SIMULATE(base, f, cls, True, (start,), shop_profile=profile, effect_scale=scale))
        two[grammar] = slim(SIMULATE(base, f, cls, True, (start, start + 1), shop_profile=profile, effect_scale=scale))

    all_missed = SIMULATE(base, f, cls, True, tuple(range(1, 100)), shop_profile=profile, effect_scale=scale)

    out = {
        "class": cls,
        "profile": profile_name,
        "cadenceLane": lane,
        "effectScale": scale,
        "appliedRanks": profile,
        "startingWall": float(f["simulation"]["wallHp"]) + profile["fort"] * 100.0 * scale,
        "allSuccess": slim(success),
        "oneMissByStartGrammar": one,
        "twoConsecutiveMissByStartGrammar": two,
        "allFinalsMissed": slim(all_missed),
    }

    if detailed:
        sweep = {}
        max_n = int(fixture["detailedSweep"]["maxConsecutiveMisses"])
        for grammar in f["pressurePatternLabels"]:
            start = int(first[grammar])
            rows = []
            for n in range(1, max_n + 1):
                rr = SIMULATE(base, f, cls, True, tuple(range(start, start + n)), shop_profile=profile, effect_scale=scale)
                rows.append({"consecutiveMisses": n, **slim(rr)})
                if rr["burialTime"] is not None:
                    break
            sweep[grammar] = {"startHeavyIndex": start, "rows": rows}
        out["consecutiveMissSweep"] = sweep
    return out


def ablation_profile(profile, lane):
    if lane == "NONE":
        return {"atk": 0, "fort": 0, "def": 0}
    if lane == "ATK_ONLY":
        return {"atk": profile["atk"], "fort": 0, "def": 0}
    if lane == "FORT_ONLY":
        return {"atk": 0, "fort": profile["fort"], "def": 0}
    if lane == "DEF_ONLY":
        return {"atk": 0, "fort": 0, "def": profile["def"]}
    if lane == "FORT_DEF":
        return {"atk": 0, "fort": profile["fort"], "def": profile["def"]}
    if lane == "ATK_FORT_DEF":
        return profile
    raise ValueError(lane)


def run_ablation(base, stage49, fixture):
    cfg = fixture["archerMageAblation"]
    out = {}
    for cls in ("Archer", "Mage"):
        f, cadence = lane_fixture(stage49, cls)
        balanced = profile_for(fixture, cls, cfg["profile"])
        out[cls] = {}
        for scale in cfg["effectScales"]:
            lanes = {}
            for name in cfg["lanes"]:
                p = ablation_profile(balanced, name)
                row = SIMULATE(base, f, cls, True, tuple(range(1, 100)), shop_profile=p, effect_scale=float(scale))
                lanes[name] = {
                    "startingWall": float(f["simulation"]["wallHp"]) + p["fort"] * 100.0 * float(scale),
                    "result": slim(row),
                }
            out[cls][str(scale)] = {"cadenceLane": cadence, "lanes": lanes}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-fixture", default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    ap.add_argument("--stage49-fixture", default="legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    ap.add_argument("--shop-fixture", default="legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    stage49 = load(args.stage49_fixture)
    base = inject_diagnostic_monsters(load(args.base_fixture), stage49)
    fixture = load(args.shop_fixture)

    runs = []
    detailed_scale = float(fixture["detailedSweep"]["effectScale"])
    detailed_profiles = set(fixture["detailedSweep"]["profiles"])
    for scale in fixture["effectMagnitudeScaleSensitivity"]:
        for cls in CLASSES:
            for profile in ("ATTACK_HEAVY", "DEFENSE_HEAVY", "BALANCED", "ROLE_AWARE"):
                detailed = float(scale) == detailed_scale and profile in detailed_profiles
                runs.append(run_case(base, stage49, fixture, cls, profile, float(scale), detailed=detailed))

    result = {
        "version": "p5-all-class-fixed-rank-shop-stage49-result-v0.1",
        "status": "DIRECTIONAL_ALL_CLASS_ATK_FORT_DEF_SHOP_COMBAT_NO_PRODUCTION_FREEZE",
        "rng": "NONE",
        "sourceKernel": "Stage46 kernel + v0.5 cadence/barrier fidelity + Tank Iron Wall SIEGER correction + bounded P5 ATK/FORT/DEF patches",
        "fixtureVersion": fixture["version"],
        "crossClassFamiliesApplied": fixture["crossClassAuthoritativeFamiliesThisLane"],
        "deferredFamilies": fixture["deferredFamilies"],
        "runs": runs,
        "archerMageAblation": run_ablation(base, stage49, fixture),
        "interpretationBoundary": [
            "KNOCKBACK is not evaluated cross-class in this result.",
            "CRIT and CRITDMG are not evaluated in this result.",
            "Fortification is fully retained at Stage49 start and therefore defense-favorable.",
            "The 30/40/50 scales are diagnostic legacy-relative sensitivities only.",
            "A 60-second survival must be interpreted with wall reserve, backlog and Stage49->50 continuity, not burial alone.",
            "No hidden per-class shop prices or correction factors are authorized."
        ],
    }

    text = json.dumps(result, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
