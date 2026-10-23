#!/usr/bin/env python3
"""Timing Defense P5 class-identity radar paired probe v0.1.

Purpose:
- reuse the current P5 all-class shop combat kernel;
- test finite packets rather than infinite 60 s survival only;
- measure direct-clear time / unfinished state / backlog for class-identity checks;
- do not freeze any production coefficient or pass threshold.

This is a bounded directional probe. The current P5 kernel still defers
cross-class KNOCK shop semantics and CRIT/CRITDMG policy.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import run_p5_all_class_fixed_rank_shop_stage49_probe_v0_2 as p5

CLASSES = ["Knight", "Rogue", "Tank", "Archer", "Mage"]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def make_temporal(stage49, scenario, duration, cls):
    out = copy.deepcopy(stage49)
    out["version"] = "p5-class-identity-radar-probe-runtime-v0.1"
    out["pressurePatternLabels"] = [scenario["id"]]
    out["pressurePatterns"] = [copy.deepcopy(scenario["rows"])]
    out["simulation"]["durationSeconds"] = float(duration)
    out["simulation"]["pressureCycleSeconds"] = 999.0
    out["simulation"]["spawnX"] = 0.92
    out["simulation"]["wallHp"] = float(scenario.get("wallHp", 2000.0))
    out["simulation"]["firstRootAttackSeconds"] = float(scenario.get("firstRootAttackSeconds", 0.2))
    out["simulation"]["rootAttackIntervalSeconds"] = 1.047 if cls == "Rogue" else 1.125
    out["simulation"]["heavyEveryRootActions"] = 4
    return out


def profile_for(shop_fixture, cls, name):
    return p5.profile_for(shop_fixture, cls, name)


def direct_clear(row, expected_kills):
    return (
        row.get("burialTime") is None
        and int(row.get("wallHits", 0)) == 0
        and int(row.get("kills", 0)) == int(expected_kills)
        and int(row.get("endActive", 0)) == 0
    )


def slim(row):
    keys = [
        "endWall", "endActive", "maxActive", "kills", "damage", "burialTime",
        "wallHits", "pxpCount", "heavyMissCount", "noTargetDrops",
        "siegerShots", "siegerRepositions", "shopAtkPct", "shopFortFlat",
        "shopGenericDef",
    ]
    return {k: row.get(k) for k in keys}


def run_once(base, stage49, shop_fixture, scenario, cls, profile_name, scale, duration):
    temporal = make_temporal(stage49, scenario, duration, cls)
    profile = profile_for(shop_fixture, cls, profile_name)
    return p5.SIMULATE(
        base,
        temporal,
        cls,
        True,
        (),
        shop_profile=profile,
        effect_scale=float(scale),
    )


def find_direct_clear_time(base, stage49, shop_fixture, scenario, cls, profile_name, scale):
    expected = int(scenario["expectedDirectKills"])
    max_offset = max(float(r["offset"]) for r in scenario["rows"])
    lo = max_offset + 0.25
    hi = float(scenario.get("maxClearScanSeconds", 120.0))

    high_row = run_once(base, stage49, shop_fixture, scenario, cls, profile_name, scale, hi)
    if not direct_clear(high_row, expected):
        return None, slim(high_row)

    # Deterministic prefix is identical after all rows have spawned, so the
    # direct-clear predicate is monotone for this finite-packet probe.
    for _ in range(14):
        mid = (lo + hi) / 2.0
        row = run_once(base, stage49, shop_fixture, scenario, cls, profile_name, scale, mid)
        if direct_clear(row, expected):
            hi = mid
            high_row = row
        else:
            lo = mid

    return round(hi, 3), slim(high_row)


def run_case(base, stage49, shop_fixture, scenario, cls, profile_name, scale, horizons):
    clear_time, clear_row = find_direct_clear_time(
        base, stage49, shop_fixture, scenario, cls, profile_name, scale
    )
    snapshots = {}
    for h in horizons:
        row = run_once(base, stage49, shop_fixture, scenario, cls, profile_name, scale, h)
        snapshots[str(h)] = slim(row)
    return {
        "class": cls,
        "profile": profile_name,
        "scenario": scenario["id"],
        "formationTag": scenario.get("formationTag"),
        "alignmentTag": scenario.get("alignmentTag"),
        "densityTag": scenario.get("densityTag"),
        "expectedDirectKills": int(scenario["expectedDirectKills"]),
        "directClearTimeSeconds": clear_time,
        "unfinishedWithinMaxScan": clear_time is None,
        "maxScanSnapshot": clear_row,
        "horizonSnapshots": snapshots,
    }


def ratio(a, b):
    if a is None or b is None or b == 0:
        return None
    return round(float(a) / float(b), 4)


def build_identity_summary(results):
    by_key = {(r["class"], r["profile"], r["scenario"]): r for r in results}

    def ct(cls, profile, scenario):
        row = by_key.get((cls, profile, scenario))
        return None if row is None else row["directClearTimeSeconds"]

    out = {
        "Knight": {
            "balancedAlignedClear": ct("Knight", "BALANCED", "KNIGHT_ALIGNED_FRONT"),
            "balancedDispersedClear": ct("Knight", "BALANCED", "KNIGHT_DISPERSED_FRONT"),
        },
        "Rogue": {
            "balancedDurableClear": ct("Rogue", "BALANCED", "ROGUE_DURABLE_SINGLE"),
            "balancedBroadWaveClear": ct("Rogue", "BALANCED", "ROGUE_BROAD_WAVE"),
        },
        "Tank": {
            "balancedMixedSoloClear": ct("Tank", "BALANCED", "TANK_MIXED_SOLO"),
            "roleAwareMixedSoloClear": ct("Tank", "ROLE_AWARE", "TANK_MIXED_SOLO"),
        },
        "Archer": {
            "balancedAlignedClear": ct("Archer", "BALANCED", "ARCHER_ALIGNED_LINE"),
            "balancedScatterClear": ct("Archer", "BALANCED", "ARCHER_SCATTER"),
            "attackHeavyAlignedClear": ct("Archer", "ATTACK_HEAVY", "ARCHER_ALIGNED_LINE"),
            "attackHeavyScatterClear": ct("Archer", "ATTACK_HEAVY", "ARCHER_SCATTER"),
        },
        "Mage": {
            "balancedClusterClear": ct("Mage", "BALANCED", "MAGE_CLUSTER"),
            "balancedDistributedClear": ct("Mage", "BALANCED", "MAGE_DISTRIBUTED"),
        },
    }

    out["Knight"]["dispersedToAlignedClearRatio"] = ratio(
        out["Knight"]["balancedDispersedClear"], out["Knight"]["balancedAlignedClear"]
    )
    out["Archer"]["balancedScatterToAlignedRatio"] = ratio(
        out["Archer"]["balancedScatterClear"], out["Archer"]["balancedAlignedClear"]
    )
    out["Archer"]["attackHeavyScatterToAlignedRatio"] = ratio(
        out["Archer"]["attackHeavyScatterClear"], out["Archer"]["attackHeavyAlignedClear"]
    )
    out["Mage"]["distributedToClusterClearRatio"] = ratio(
        out["Mage"]["balancedDistributedClear"], out["Mage"]["balancedClusterClear"]
    )

    damage_classes = ["Knight", "Rogue", "Archer", "Mage"]
    damage_times = [ct(c, "BALANCED", "TANK_MIXED_SOLO") for c in damage_classes]
    finite = sorted(x for x in damage_times if x is not None)
    if finite:
        mid = len(finite) // 2
        median = finite[mid] if len(finite) % 2 else (finite[mid - 1] + finite[mid]) / 2.0
    else:
        median = None
    tank_time = out["Tank"]["balancedMixedSoloClear"]
    out["Tank"]["damageClassMedianMixedSoloClear"] = None if median is None else round(median, 3)
    out["Tank"]["tankToDamageClassMedianClearRatio"] = ratio(tank_time, median)

    out["interpretationBoundary"] = {
        "thresholdsFrozen": False,
        "radarValuesAreLiteralCoefficients": False,
        "tankSurvivalEqualsClear": False,
        "use": "Collect first paired distributions before setting numerical identity thresholds.",
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--base-fixture",
        default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json",
    )
    ap.add_argument(
        "--stage49-fixture",
        default="legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json",
    )
    ap.add_argument(
        "--shop-fixture",
        default="legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json",
    )
    ap.add_argument(
        "--identity-fixture",
        default="legacy-game-structure/data/p5_class_identity_radar_probe_fixture_v0_1.json",
    )
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    base = load(args.base_fixture)
    stage49 = load(args.stage49_fixture)
    shop_fixture = load(args.shop_fixture)
    identity = load(args.identity_fixture)
    base = p5.inject_diagnostic_monsters(base, stage49)

    scale = float(identity["shopEffectScale"])
    horizons = [float(x) for x in identity["snapshotHorizonsSeconds"]]
    results = []

    for scenario in identity["scenarios"]:
        for cls in CLASSES:
            profiles = ["BALANCED"]
            profiles += identity.get("extraProfilesByClass", {}).get(cls, [])
            for profile_name in dict.fromkeys(profiles):
                results.append(
                    run_case(
                        base, stage49, shop_fixture, scenario,
                        cls, profile_name, scale, horizons
                    )
                )

    output = {
        "version": "p5-class-identity-radar-probe-result-v0.1",
        "status": "BOUNDED_DIRECTIONAL_IDENTITY_PROBE_NO_NUMERICAL_FREEZE",
        "shopEffectScale": scale,
        "crossClassShopFamilies": ["ATK", "FORTIFICATION", "DEFENSE"],
        "results": results,
        "identitySummary": build_identity_summary(results),
    }

    text = json.dumps(output, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
