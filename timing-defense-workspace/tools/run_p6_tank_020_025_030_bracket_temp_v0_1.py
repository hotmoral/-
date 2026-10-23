#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path

import run_p5_p6_fidelity_bridge_stage46_49_temp_v0_1 as bridge
import run_p6_stage46_47_causal_convergence_temp_v0_1 as causal
import run_p6_pressure_family_rotation_temp_v0_1 as pressure
import run_p6_tank_objective_attribution_temp_v0_2 as attrib

OUT = Path("p6_tank_020_025_030_bracket_temp_v0_1.json")
SEEDS = tuple(range(1, 21))
PROFILE = "BALANCED"
COEFFS = (0.20, 0.25, 0.30)
FAMILIES = ("DURABLE_DISTRIBUTED", "CHARGER_CONTROL_SCREENED")

pressure.PACKETS["CHARGER_CONTROL_SCREENED"] = [
    (0.00, "BRUTE", 0),
    (0.70, "SHIELD", -2),
    (1.40, "BRUTE", 2),
    (2.10, "CHARGER", -1),
    (2.80, "CHARGER", 1),
]
pressure.REPEATS["CHARGER_CONTROL_SCREENED"] = {46: (16, 3.55), 47: (18, 3.15)}
bridge.fixed_stage_cfg = pressure.patched_fixed_stage_cfg


def describe(vals):
    xs = [float(v) for v in vals if v is not None]
    if not xs:
        return None
    return {
        "n": len(xs),
        "mean": round(statistics.fmean(xs), 6),
        "median": round(statistics.median(xs), 6),
        "min": round(min(xs), 6),
        "max": round(max(xs), 6),
    }


def simulate_stage_coeff(sim_fn, base, temporal, direction, integration, cls, profile, scale,
                         stage_no, current_wall, start_state, coeff):
    cfg, expected_schedule = bridge.fixed_stage_cfg(
        temporal, direction, integration, stage_no, cls, bridge.DRAIN_SECONDS
    )
    actual_schedule = sim_fn.__globals__["build_integrated_schedule"](cfg)
    if [tuple(x) for x in actual_schedule] != [tuple(x) for x in expected_schedule]:
        raise RuntimeError(f"fixed schedule mismatch Stage{stage_no} {cls}")
    local_state = copy.deepcopy(start_state)
    bridge.BRIDGE_CTX["runState"] = local_state
    before = copy.deepcopy(local_state)
    row = sim_fn(
        base, cfg, cls, True, (),
        overrides={"shockwaveCoefficient": float(coeff)} if cls == "Tank" else None,
        shop_profile=profile,
        effect_scale=float(scale),
        start_wall_current=float(current_wall),
    )
    after = copy.deepcopy(bridge.BRIDGE_CTX["runState"])
    settled = row.get("burialTime") is None and int(row.get("endActive") or 0) == 0
    return {
        "row": row,
        "settled": bool(settled),
        "schedule": expected_schedule,
        "stateBefore": before,
        "stateAfter": after,
    }


def run_chain(sim_fn, base, temporal, direction, shop, integration, central, mode, seed, coeff):
    bridge.BRIDGE_CTX["central"] = central
    state = bridge.new_run_state(mode, central, int(seed), "Tank", causal.ENTRY_CHARGE)
    profile = bridge.integ.profile_for(shop, "Tank", PROFILE)
    scale = float(integration["shopEffectScale"])
    wall_max = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * scale
    current = wall_max
    stages = []
    for stage_no in causal.STAGES:
        start_wall = current
        result = simulate_stage_coeff(
            sim_fn, base, temporal, direction, integration, "Tank", profile, scale,
            stage_no, current, state, coeff,
        )
        row = dict(result["row"])
        row["stage"] = stage_no
        before = result["stateBefore"]
        after = result["stateAfter"]
        stages.append(causal.stage_summary(row, result, before, after, start_wall))
        current = float(row.get("endWall") or 0.0)
        state = after
        if not result["settled"]:
            break
    heavy = int(state["heavyActions"])
    pxp = int(state["pxpActions"])
    return {
        "mode": mode,
        "seed": int(seed),
        "coefficient": float(coeff),
        "through47": len(stages) == 2 and all(s["settled"] for s in stages),
        "failureStage": None if len(stages) == 2 and all(s["settled"] for s in stages) else stages[-1]["stage"],
        "finalWall": round(current, 3),
        "wallMax": round(wall_max, 3),
        "totalJudgments": int(state["judgmentsConsumed"]),
        "totalPxpRate": round(pxp / heavy, 6) if heavy else None,
        "stages": stages,
    }


def aggregate(rows):
    skilled = [r for r in rows if r["mode"] == "SKILLED_V2_CENTRAL"]
    perfect = [r for r in rows if r["mode"] == "ALL_PERFECT"]
    s46 = [s for r in skilled for s in r["stages"] if s["stage"] == 46]
    return {
        "cases": len(skilled),
        "through47": sum(1 for r in skilled if r["through47"]),
        "failureStages": dict(sorted(Counter(str(r["failureStage"]) for r in skilled if r["failureStage"] is not None).items())),
        "allPerfectThrough47": sum(1 for r in perfect if r["through47"]),
        "allPerfectCases": len(perfect),
        "finalWall": describe([r["finalWall"] for r in skilled]),
        "totalJudgments": describe([r["totalJudgments"] for r in skilled]),
        "totalPxpRate": describe([r["totalPxpRate"] for r in skilled]),
        "stage46": {
            "damage": describe([s["damage"] for s in s46]),
            "wallLoss": describe([s["wallLoss"] for s in s46]),
            "maxActive": describe([s["maxActive"] for s in s46]),
            "pushDistance": describe([s["pushDistance"] for s in s46]),
            "chargerInterrupts": describe([s["chargerInterrupts"] for s in s46]),
        },
    }


def main():
    base, temporal, direction, shop, integration, central = bridge.load_inputs()
    sim_fn = attrib.build_sim(correct_aftershock_center=True)
    result = {}
    raw = []
    for family in FAMILIES:
        pressure.ACTIVE_FAMILY = family
        result[family] = {}
        for coeff in COEFFS:
            rows = [
                run_chain(sim_fn, base, temporal, direction, shop, integration, central,
                          "SKILLED_V2_CENTRAL", seed, coeff)
                for seed in SEEDS
            ]
            rows.append(run_chain(
                sim_fn, base, temporal, direction, shop, integration, central,
                "ALL_PERFECT", 1, coeff,
            ))
            raw.extend({"family": family, **r} for r in rows)
            result[family][f"{coeff:.2f}"] = aggregate(rows)

    output = {
        "version": "p6-tank-020-025-030-bracket-temp-v0.1",
        "status": "AUTHORIZED_EXISTING_DIAGNOSTIC_BRACKET_ONLY_NO_NUMERICAL_FREEZE_NO_PRODUCTION_AUTHORITY",
        "basis": {
            "profile": PROFILE,
            "seeds": list(SEEDS),
            "families": list(FAMILIES),
            "coefficients": list(COEFFS),
            "aftershockCenterFidelityCorrected": True,
            "allOtherTankControlAndDefenseSemanticsPreserved": True,
        },
        "aggregate": result,
        "rows": raw,
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    OUT.write_text(text + "\n", encoding="utf-8")
    compact = {
        family: {
            coeff: {
                "through47": block["through47"],
                "allPerfect": f'{block["allPerfectThrough47"]}/{block["allPerfectCases"]}',
                "finalWallMedian": block["finalWall"]["median"],
                "judgmentsMean": block["totalJudgments"]["mean"],
                "pxpRateMean": block["totalPxpRate"]["mean"],
                "s46DamageMean": block["stage46"]["damage"]["mean"],
                "s46WallLossMean": block["stage46"]["wallLoss"]["mean"],
                "s46MaxActiveMean": block["stage46"]["maxActive"]["mean"],
            }
            for coeff, block in result[family].items()
        }
        for family in FAMILIES
    }
    print("P6_TANK_BRACKET=" + json.dumps(compact, sort_keys=True))
    print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
