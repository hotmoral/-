#!/usr/bin/env python3
from __future__ import annotations

import builtins
import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path

import run_p5_p6_fidelity_bridge_stage46_49_temp_v0_1 as bridge
import run_p6_stage46_47_causal_convergence_temp_v0_1 as causal
import run_p6_pressure_family_rotation_temp_v0_1 as pressure

OUT = Path("p6_tank_objective_attribution_temp_v0_2.json")
SEEDS = tuple(range(1, 21))
PROFILE = "BALANCED"
FAMILY = "CHARGER_CONTROL_SCREENED"

pressure.PACKETS[FAMILY] = [
    (0.00, "BRUTE", 0),
    (0.70, "SHIELD", -2),
    (1.40, "BRUTE", 2),
    (2.10, "CHARGER", -1),
    (2.80, "CHARGER", 1),
]
pressure.REPEATS[FAMILY] = {46: (16, 3.55), 47: (18, 3.15)}
pressure.ACTIVE_FAMILY = FAMILY
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


def build_sim(*, correct_aftershock_center: bool, lv31_barrier: bool = True,
              lv16_barrier: bool = True, aftershock_slow: bool = True,
              iron_wall: bool = True):
    original_exec = builtins.exec

    def patched_exec(src, ns, *args, **kwargs):
        if isinstance(src, str) and "def simulate" in src and "shopGenericDef" in src and "shieldSource" in src:
            if correct_aftershock_center:
                ordinary_anchor = (
                    '        hit(mon, cfg, mobs, p, base_damage, stats, counter)\n'
                    '        push(p, tier, 2.0 if heavy else 1.30, now, stats)\n'
                )
                ordinary_repl = (
                    '        _tankImpactX = p.x\n'
                    '        _tankImpactBand = p.band\n'
                    '        hit(mon, cfg, mobs, p, base_damage, stats, counter)\n'
                    '        push(p, tier, 2.0 if heavy else 1.30, now, stats)\n'
                )
                if src.count(ordinary_anchor) != 1:
                    raise RuntimeError("Tank ordinary impact anchor changed")
                src = src.replace(ordinary_anchor, ordinary_repl, 1)
                old_zone = '            stats["aftershockZones"].append((now + 1.5, p.x, p.band))\n'
                new_zone = '            stats["aftershockZones"].append((now + 1.5, _tankImpactX, _tankImpactBand))\n'
                if src.count(old_zone) != 1:
                    raise RuntimeError("Tank ordinary zone anchor changed")
                src = src.replace(old_zone, new_zone, 1)

                final_anchor = '        if final:\n            raw = base_damage * float(cand["shockwaveCoefficient"])\n'
                final_repl = (
                    '        if final:\n'
                    '            _tankFinalImpactX = primary.x if primary else None\n'
                    '            _tankFinalImpactBand = primary.band if primary else None\n'
                    '            raw = base_damage * float(cand["shockwaveCoefficient"])\n'
                )
                if src.count(final_anchor) != 1:
                    raise RuntimeError("Tank final impact anchor changed")
                src = src.replace(final_anchor, final_repl, 1)
                old_final_zone = '                stats["aftershockZones"].append((now + 1.5, primary.x, primary.band))\n'
                new_final_zone = '                stats["aftershockZones"].append((now + 1.5, _tankFinalImpactX, _tankFinalImpactBand))\n'
                if src.count(old_final_zone) != 1:
                    raise RuntimeError("Tank final zone anchor changed")
                src = src.replace(old_final_zone, new_final_zone, 1)

            if not lv31_barrier:
                old = (
                    '            stats["shield"] = float(cand["barrier"])\n'
                    '            stats["shieldUntil"] = now + float(cand["barrierSeconds"])\n'
                    '            stats["shieldSource"] = "LV31"\n'
                )
                new = (
                    '            stats["shield"] = 0.0\n'
                    '            stats["shieldUntil"] = now + float(cand["barrierSeconds"])\n'
                    '            stats["shieldSource"] = None\n'
                )
                if src.count(old) != 1:
                    raise RuntimeError("Lv31 barrier block changed")
                src = src.replace(old, new, 1)

            if not lv16_barrier:
                old = (
                    '                stats["shield"] = 80.0\n'
                    '                stats["shieldUntil"] = now + 3.0\n'
                    '                stats["shieldSource"] = "LV16"\n'
                )
                new = (
                    '                stats["shield"] = 0.0\n'
                    '                stats["shieldUntil"] = now + 3.0\n'
                    '                stats["shieldSource"] = None\n'
                )
                if src.count(old) != 1:
                    raise RuntimeError("Lv16 barrier block changed")
                src = src.replace(old, new, 1)

            if not aftershock_slow:
                old = '                if cls == "Tank" and any(\n'
                new = '                if False and cls == "Tank" and any(\n'
                if src.count(old) != 1:
                    raise RuntimeError("Aftershock slow condition changed")
                src = src.replace(old, new, 1)

            if not iron_wall:
                old = '* (0.90 if cls == "Tank" else 1.0)'
                count = src.count(old)
                if count != 2:
                    raise RuntimeError(f"Iron Wall sites changed: {count}")
                src = src.replace(old, '* 1.0')

        return original_exec(src, ns, *args, **kwargs)

    builtins.exec = patched_exec
    try:
        fn = bridge.build_bridge_simulate()
    finally:
        builtins.exec = original_exec
    return causal.install_push_telemetry(fn)


def set_no_push(fn):
    glb = fn.__globals__
    original = glb["push"]
    def noop(m, tier, mul, now, stats):
        return None
    glb["push"] = noop
    return original


def run_variant(name, sim_fn, base, temporal, direction, shop, integration, central, *, suppress_push=False):
    restore_push = None
    if suppress_push:
        restore_push = set_no_push(sim_fn)
    rows = []
    try:
        for seed in SEEDS:
            rows.append(causal.run_chain(
                sim_fn, base, temporal, direction, shop, integration, central,
                "Tank", PROFILE, "SKILLED_V2_CENTRAL", int(seed),
            ))
        rows.append(causal.run_chain(
            sim_fn, base, temporal, direction, shop, integration, central,
            "Tank", PROFILE, "ALL_PERFECT", 1,
        ))
    finally:
        if restore_push is not None:
            sim_fn.__globals__["push"] = restore_push
    return {"name": name, "rows": rows}


def aggregate(block):
    skilled = [r for r in block["rows"] if r["mode"] == "SKILLED_V2_CENTRAL"]
    perfect = [r for r in block["rows"] if r["mode"] == "ALL_PERFECT"]
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
            "wallLoss": describe([s["wallLoss"] for s in s46]),
            "maxActive": describe([s["maxActive"] for s in s46]),
            "damage": describe([s["damage"] for s in s46]),
            "pushDistance": describe([s["pushDistance"] for s in s46]),
            "chargerInterrupts": describe([s["chargerInterrupts"] for s in s46]),
            "chargerWindups": describe([s["chargerWindups"] for s in s46]),
            "chargerCharges": describe([s["chargerCharges"] for s in s46]),
        },
    }


def main():
    base, temporal, direction, shop, integration, central = bridge.load_inputs()
    specs = [
        ("SOURCE_CURRENT", dict(correct_aftershock_center=False), False),
        ("FIDELITY_CORRECTED", dict(correct_aftershock_center=True), False),
        ("NO_LV31_BARRIER", dict(correct_aftershock_center=True, lv31_barrier=False), False),
        ("NO_ALL_BARRIERS", dict(correct_aftershock_center=True, lv31_barrier=False, lv16_barrier=False), False),
        ("NO_AFTERSHOCK_SLOW", dict(correct_aftershock_center=True, aftershock_slow=False), False),
        ("NO_IRON_WALL", dict(correct_aftershock_center=True, iron_wall=False), False),
        ("NO_PUSH", dict(correct_aftershock_center=True), True),
    ]
    blocks = []
    for name, kwargs, suppress_push in specs:
        fn = build_sim(**kwargs)
        blocks.append(run_variant(name, fn, base, temporal, direction, shop, integration, central, suppress_push=suppress_push))

    agg = {b["name"]: aggregate(b) for b in blocks}
    full = agg["FIDELITY_CORRECTED"]
    deltas = {}
    for name, row in agg.items():
        if name == "FIDELITY_CORRECTED":
            continue
        deltas[name] = {
            "through47DeltaVsCorrected": row["through47"] - full["through47"],
            "stage46WallLossMeanDeltaVsCorrected": round(row["stage46"]["wallLoss"]["mean"] - full["stage46"]["wallLoss"]["mean"], 6),
            "stage46MaxActiveMeanDeltaVsCorrected": round(row["stage46"]["maxActive"]["mean"] - full["stage46"]["maxActive"]["mean"], 6),
        }

    output = {
        "version": "p6-tank-objective-attribution-temp-v0.2",
        "status": "DIAGNOSTIC_PAIRED_ABLATION_ONLY_NO_NUMERICAL_FREEZE_NO_PRODUCTION_AUTHORITY",
        "basis": {
            "family": FAMILY,
            "profile": PROFILE,
            "seeds": list(SEEDS),
            "shockwaveCoefficient": 0.25,
            "normalRightEdgePreserved": True,
            "approvedAftershockCenter": "authoritative primary Ground Impact location before knockback",
            "sourceCurrentMismatch": "current diagnostic source appends zone after push using post-push p.x",
            "purpose": "Correct source fidelity first, then remove one existing defensive/control component at a time.",
        },
        "aggregate": agg,
        "deltasVsFidelityCorrected": deltas,
        "blocks": blocks,
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    OUT.write_text(text + "\n", encoding="utf-8")
    compact = {
        k: {
            "through47": v["through47"],
            "allPerfect": f'{v["allPerfectThrough47"]}/{v["allPerfectCases"]}',
            "finalWallMedian": v["finalWall"]["median"],
            "judgmentsMean": v["totalJudgments"]["mean"],
            "pxpRateMean": v["totalPxpRate"]["mean"],
            "s46WallLossMean": v["stage46"]["wallLoss"]["mean"],
            "s46MaxActiveMean": v["stage46"]["maxActive"]["mean"],
            "s46PushMean": v["stage46"]["pushDistance"]["mean"],
            "s46InterruptMean": v["stage46"]["chargerInterrupts"]["mean"],
            "s46WindupMean": v["stage46"]["chargerWindups"]["mean"],
            "s46ChargeMean": v["stage46"]["chargerCharges"]["mean"],
        }
        for k, v in agg.items()
    }
    print("P6_TANK_ATTRIBUTION_V02=" + json.dumps(compact, sort_keys=True))
    print("P6_TANK_DELTAS_V02=" + json.dumps(deltas, sort_keys=True))
    print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
