#!/usr/bin/env python3
"""Timing Defense P4-D2 Stage48-49 fidelity runner v0.6.

Supersedes v0.5 for Tank wall-incoming fidelity only.

Adds one recovered-contract correction:
- Tank Lv11 Iron Wall is shared-wall incoming damage x0.90, non-stacking;
- therefore it applies to SIEGER wall-shot damage as well as ordinary wall contact.

Preserves v0.5 corrections:
- active Lv31 Absolute Barrier may not be downgraded by weaker Lv16 guard;
- NO_TARGET opportunities do not bank;
- cadence-specific Heavy/PxP timeline mapping;
- Rogue recovered 78ms recovery sensitivity lane.

Diagnostic only. No production value/content freeze.
"""
from __future__ import annotations

import argparse
import inspect
import json
from pathlib import Path

import run_p4d2_stage46_temporal_pressure_probe_v0_1 as stage46
import run_p4d2_stage48_49_dynamic_grammar_probe_v0_2 as v02


def build_fidelity_simulate_v06():
    src = inspect.getsource(stage46.simulate)

    # Recovered Tank Lv11 contract: shared wall incoming x0.90, non-stacking.
    # The historical Stage46 kernel applied this to ordinary wall contact but omitted SIEGER shots.
    old_sieger_incoming = '                    incoming = 75.0\n'
    new_sieger_incoming = '                    incoming = 75.0 * (0.90 if cls == "Tank" else 1.0)\n'
    if src.count(old_sieger_incoming) != 1:
        raise RuntimeError(
            f"Expected exactly one SIEGER incoming line, found {src.count(old_sieger_incoming)}; v0.6 patch must be reviewed"
        )
    src = src.replace(old_sieger_incoming, new_sieger_incoming, 1)

    old_stats_tail = '        "aftershockZones": [],\n    }'
    new_stats_tail = (
        '        "aftershockZones": [],\n'
        '        "shieldSource": None,\n'
        '        "heavyTimeline": [],\n'
        '        "noTargetDrops": 0,\n'
        '    }'
    )
    if old_stats_tail not in src:
        raise RuntimeError("Stage46 simulate() stats shape changed; v0.6 patch must be reviewed")
    src = src.replace(old_stats_tail, new_stats_tail, 1)

    old_attack_guard = '        if now >= next_attack - 1e-9 and nearest(mobs):\n'
    new_attack_guard = (
        '        # P4-D2 fidelity correction: NO_TARGET opportunities do not bank.\n'
        '        if now >= next_attack - 1e-9 and not nearest(mobs):\n'
        '            stats["noTargetDrops"] += 1\n'
        '            next_attack = now + root_interval\n\n'
        '        if now >= next_attack - 1e-9 and nearest(mobs):\n'
    )
    if old_attack_guard not in src:
        raise RuntimeError("Stage46 attack guard changed; v0.6 patch must be reviewed")
    src = src.replace(old_attack_guard, new_attack_guard, 1)

    old_heavy = '            if heavy:\n                heavy_index += 1\n'
    new_heavy = (
        '            if heavy:\n'
        '                heavy_index += 1\n'
        '                stats["heavyTimeline"].append({"index": heavy_index, "time": round(now, 3)})\n'
    )
    if old_heavy not in src:
        raise RuntimeError("Stage46 Heavy block changed; v0.6 patch must be reviewed")
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
    if old_final_barrier not in src:
        raise RuntimeError("Stage46 Lv31 barrier block changed; v0.6 patch must be reviewed")
    src = src.replace(old_final_barrier, new_final_barrier, 1)

    old_lv16_guard = (
        '        if not heavy and tier == "PERFECT":\n'
        '            stats["shield"] = 80.0\n'
        '            stats["shieldUntil"] = now + 3.0\n'
    )
    new_lv16_guard = (
        '        if not heavy and tier == "PERFECT":\n'
        '            if stats["shield"] <= 1e-9 or stats.get("shieldSource") != "LV31":\n'
        '                stats["shield"] = 80.0\n'
        '                stats["shieldUntil"] = now + 3.0\n'
        '                stats["shieldSource"] = "LV16"\n'
    )
    if old_lv16_guard not in src:
        raise RuntimeError("Stage46 Lv16 guard block changed; v0.6 patch must be reviewed")
    src = src.replace(old_lv16_guard, new_lv16_guard, 1)

    old_expiry = (
        '        if stats["shield"] > 0 and now >= stats["shieldUntil"]:\n'
        '            stats["shield"] = 0.0\n'
    )
    new_expiry = (
        '        if stats["shield"] > 0 and now >= stats["shieldUntil"]:\n'
        '            stats["shield"] = 0.0\n'
        '            stats["shieldSource"] = None\n'
    )
    if old_expiry not in src:
        raise RuntimeError("Stage46 shield expiry block changed; v0.6 patch must be reviewed")
    src = src.replace(old_expiry, new_expiry, 1)

    sieger_absorb = '\n                    stats["shield"] -= absorb\n'
    wall_absorb = '\n                stats["shield"] -= absorb\n'
    if src.count(sieger_absorb) != 1:
        raise RuntimeError(f"Expected 1 SIEGER shield absorb line, found {src.count(sieger_absorb)}")
    if src.count(wall_absorb) != 1:
        raise RuntimeError(f"Expected 1 wall-contact shield absorb line, found {src.count(wall_absorb)}")

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

    old_pop_tail = (
        '    stats.pop("shield", None)\n'
        '    stats.pop("shieldUntil", None)\n'
        '    stats.pop("aftershockZones", None)\n'
    )
    new_pop_tail = (
        '    stats.pop("shield", None)\n'
        '    stats.pop("shieldUntil", None)\n'
        '    stats.pop("shieldSource", None)\n'
        '    stats.pop("aftershockZones", None)\n'
    )
    if old_pop_tail not in src:
        raise RuntimeError("Stage46 result cleanup changed; v0.6 patch must be reviewed")
    src = src.replace(old_pop_tail, new_pop_tail, 1)

    ns = dict(vars(stage46))
    exec(src, ns)
    return ns["simulate"]


FIDELITY_SIMULATE_V06 = build_fidelity_simulate_v06()
v02.FIDELITY_SIMULATE = FIDELITY_SIMULATE_V06


def run_all(base, fixture):
    result = v02.run_all(base, fixture)
    result["version"] = "p4d2-stage48-49-dynamic-grammar-result-v0.6"
    result["status"] = "CADENCE_NO_BANK_TANK_BARRIER_IRON_WALL_FIDELITY_DIAGNOSTIC_NO_NUMERICAL_FREEZE"
    result["sourceKernel"] = "Stage46 simulate + v0.5 fidelity patches + Tank Lv11 Iron Wall on SIEGER"
    result["tankIronWallSemantics"] = {
        "sharedWallIncomingMultiplier": 0.90,
        "multipleTanksStack": False,
        "appliesToOrdinaryWallContact": True,
        "appliesToSiegerWallShot": True,
        "recoveredAuthority": "PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md / Tank Lv11 Iron Wall"
    }
    result["supersession"] = {
        "v05": "exact-admitted historical evidence but Tank SIEGER wall-shot path omitted Lv11 x0.90",
        "v06": "current fidelity candidate for Tank-containing wall-pressure comparisons"
    }
    result["interpretationBoundary"].append(
        "Only Tank scenarios involving SIEGER wall shots require numerical re-evaluation from v0.5; other classes are expected byte-for-semantics unchanged apart from result metadata."
    )
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-fixture", default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    ap.add_argument("--grammar-fixture", default="legacy-game-structure/data/p4d2_stage48_49_dynamic_rotating_grammar_fixture_v0_1.json")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()
    base = stage46.load(args.base_fixture)
    fixture = stage46.load(args.grammar_fixture)
    result = run_all(base, fixture)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
