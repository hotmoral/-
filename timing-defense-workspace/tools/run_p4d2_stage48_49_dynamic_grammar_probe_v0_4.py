#!/usr/bin/env python3
"""Timing Defense P4-D2 Stage48-49 fidelity runner v0.4.

Supersedes v0.3 before exact replay admission because v0.3 incorrectly assumed
both shield-absorb sites had the same indentation and therefore failed its own
source-patch guard against the live Stage46 kernel.

Adds/keeps structural fidelity corrections:
- an active Lv31 Absolute Barrier shield may not be downgraded by a weaker Lv16 Perfect Guard;
- NO_TARGET opportunities do not bank;
- cadence-specific Heavy/PxP timeline mapping;
- Rogue recovered 78ms recovery sensitivity lane.

This is diagnostic only. It does not freeze production cadence, shield values, or Stage48/49 content.
"""
from __future__ import annotations

import argparse
import inspect
import json
from pathlib import Path

import run_p4d2_stage46_temporal_pressure_probe_v0_1 as stage46
import run_p4d2_stage48_49_dynamic_grammar_probe_v0_2 as v02


def build_fidelity_simulate_v04():
    src = inspect.getsource(stage46.simulate)

    old_stats_tail = '        "aftershockZones": [],\n    }'
    new_stats_tail = (
        '        "aftershockZones": [],\n'
        '        "shieldSource": None,\n'
        '        "heavyTimeline": [],\n'
        '        "noTargetDrops": 0,\n'
        '    }'
    )
    if old_stats_tail not in src:
        raise RuntimeError("Stage46 simulate() stats shape changed; v0.4 patch must be reviewed")
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
        raise RuntimeError("Stage46 attack guard changed; v0.4 patch must be reviewed")
    src = src.replace(old_attack_guard, new_attack_guard, 1)

    old_heavy = '            if heavy:\n                heavy_index += 1\n'
    new_heavy = (
        '            if heavy:\n'
        '                heavy_index += 1\n'
        '                stats["heavyTimeline"].append({"index": heavy_index, "time": round(now, 3)})\n'
    )
    if old_heavy not in src:
        raise RuntimeError("Stage46 Heavy block changed; v0.4 patch must be reviewed")
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
        raise RuntimeError("Stage46 Lv31 barrier block changed; v0.4 patch must be reviewed")
    src = src.replace(old_final_barrier, new_final_barrier, 1)

    old_lv16_guard = (
        '        if not heavy and tier == "PERFECT":\n'
        '            stats["shield"] = 80.0\n'
        '            stats["shieldUntil"] = now + 3.0\n'
    )
    new_lv16_guard = (
        '        if not heavy and tier == "PERFECT":\n'
        '            # Shared non-additive barrier family: a weaker Lv16 guard may not downgrade an active Lv31 barrier.\n'
        '            if stats["shield"] <= 1e-9 or stats.get("shieldSource") != "LV31":\n'
        '                stats["shield"] = 80.0\n'
        '                stats["shieldUntil"] = now + 3.0\n'
        '                stats["shieldSource"] = "LV16"\n'
    )
    if old_lv16_guard not in src:
        raise RuntimeError("Stage46 Lv16 guard block changed; v0.4 patch must be reviewed")
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
        raise RuntimeError("Stage46 shield expiry block changed; v0.4 patch must be reviewed")
    src = src.replace(old_expiry, new_expiry, 1)

    # The two absorb sites intentionally have different indentation in the live Stage46 kernel.
    sieger_absorb = '                    stats["shield"] -= absorb\n'
    wall_absorb = '                stats["shield"] -= absorb\n'
    if src.count(sieger_absorb) != 1:
        raise RuntimeError(f"Expected 1 SIEGER shield absorb site, found {src.count(sieger_absorb)}; v0.4 patch must be reviewed")
    if src.count(wall_absorb) != 1:
        raise RuntimeError(f"Expected 1 wall-contact shield absorb site, found {src.count(wall_absorb)}; v0.4 patch must be reviewed")

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
        raise RuntimeError("Stage46 result cleanup changed; v0.4 patch must be reviewed")
    src = src.replace(old_pop_tail, new_pop_tail, 1)

    ns = dict(vars(stage46))
    exec(src, ns)
    return ns["simulate"]


FIDELITY_SIMULATE_V04 = build_fidelity_simulate_v04()
v02.FIDELITY_SIMULATE = FIDELITY_SIMULATE_V04


def run_all(base, fixture):
    result = v02.run_all(base, fixture)
    result["version"] = "p4d2-stage48-49-dynamic-grammar-result-v0.4"
    result["status"] = "CADENCE_NO_BANK_TANK_BARRIER_FIDELITY_DIAGNOSTIC_NO_NUMERICAL_FREEZE"
    result["sourceKernel"] = "run_p4d2_stage46_temporal_pressure_probe_v0_1.simulate + bounded v0.4 fidelity patches"
    result["tankBarrierSemantics"] = {
        "family": "SHARED_NON_ADDITIVE",
        "lv31BarrierSource": "LV31",
        "lv16GuardSource": "LV16",
        "activeLv31MayBeDowngradedByLv16": False,
        "source": "90_P4D1_LV31_STRUCTURAL_SKILL_CONTRACT_PROPOSAL_V0_1.md T-B, carried forward unless superseded"
    }
    result["runnerCorrection"] = {
        "v03ExactReplayAdmission": "FAIL_SOURCE_PATCH_GUARD",
        "v03Defect": "assumed both shield absorb sites used identical indentation",
        "v04Fix": "patch SIEGER-shot and wall-contact absorb sites independently"
    }
    result["interpretationBoundary"].append(
        "Tank v0.2 miss-severity values that depended on Lv16 overwriting an active Lv31 barrier are superseded by v0.4 fidelity results."
    )
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--base-fixture",
        default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json",
    )
    ap.add_argument(
        "--grammar-fixture",
        default="legacy-game-structure/data/p4d2_stage48_49_dynamic_rotating_grammar_fixture_v0_1.json",
    )
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
