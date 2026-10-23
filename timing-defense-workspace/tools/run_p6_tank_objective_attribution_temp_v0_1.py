#!/usr/bin/env python3
from __future__ import annotations

import builtins
import copy
import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path

import run_p5_p6_fidelity_bridge_stage46_49_temp_v0_1 as bridge
import run_p6_stage46_47_causal_convergence_temp_v0_1 as causal
import run_p6_pressure_family_rotation_temp_v0_1 as pressure

OUT = Path("p6_tank_objective_attribution_temp_v0_1.json")
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

    def instrumented_exec(src, ns, *args, **kwargs):
        if isinstance(src, str) and "def simulate" in src and "shopGenericDef" in src and "shieldSource" in src:
            # Telemetry fields survive cleanup.
            anchor = '        "rogueStormTelemetry": {},\n    }'
            repl = (
                '        "rogueStormTelemetry": {},\n'
                '        "p6ShieldAbsorbTotal": 0.0,\n'
                '        "p6ShieldAbsorbBySource": {},\n'
                '        "p6Lv31BarrierCreates": 0,\n'
                '        "p6Lv16BarrierCreates": 0,\n'
                '        "p6AftershockSlowEnemySeconds": 0.0,\n'
                '        "p6AftershockSlowTicks": 0,\n'
                '    }'
            )
            if src.count(anchor) != 1:
                raise RuntimeError("Tank attribution stats anchor changed")
            src = src.replace(anchor, repl, 1)

            # Approved contract: zone center is primary impact location, not post-push location.
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

            # Barrier creation telemetry / ablations.
            lv31 = (
                '            stats["shield"] = float(cand["barrier"])\n'
                '            stats["shieldUntil"] = now + float(cand["barrierSeconds"])\n'
                '            stats["shieldSource"] = "LV31"\n'
            )
            lv31_new = (
                f'            stats["shield"] = float(cand["barrier"]) if {str(lv31_barrier)} else 0.0\n'
                '            stats["shieldUntil"] = now + float(cand["barrierSeconds"])\n'
                f'            stats["shieldSource"] = "LV31" if {str(lv31_barrier)} else None\n'
                f'            stats["p6Lv31BarrierCreates"] += 1 if {str(lv31_barrier)} else 0\n'
            )
            if src.count(lv31) != 1:
                raise RuntimeError("Lv31 barrier block changed")
            src = src.replace(lv31, lv31_new, 1)

            lv16 = (
                '                stats["shield"] = 80.0\n'
                '                stats["shieldUntil"] = now + 3.0\n'
                '                stats["shieldSource"] = "LV16"\n'
            )
            lv16_new = (
                f'                stats["shield"] = 80.0 if {str(lv16_barrier)} else 0.0\n'
                '                stats["shieldUntil"] = now + 3.0\n'
                f'                stats["shieldSource"] = "LV16" if {str(lv16_barrier)} else None\n'
                f'                stats["p6Lv16BarrierCreates"] += 1 if {str(lv16_barrier)} else 0\n'
            )
            if src.count(lv16) != 1:
                raise RuntimeError("Lv16 barrier block changed")
            src = src.replace(lv16, lv16_new, 1)

            # Attribute actual absorbed incoming damage by current shield source.
            absorb_line = '                    stats["shield"] -= absorb\n'
            absorb_block = (
                '                    _p6ShieldSrc = stats.get("shieldSource") or "UNKNOWN"\n'
                '                    stats["shield"] -= absorb\n'
                '                    if absorb > 0:\n'
                '                        stats["p6ShieldAbsorbTotal"] += absorb\n'
                '                        stats["p6ShieldAbsorbBySource"][_p6ShieldSrc] = stats["p6ShieldAbsorbBySource"].get(_p6ShieldSrc, 0.0) + absorb\n'
            )
            # No SIEGER in this family, but keep both sites instrumentable. Contact site has different indentation.
            if src.count(absorb_line) == 1:
                src = src.replace(absorb_line, absorb_block, 1)
            contact_line = '                stats["shield"] -= absorb\n'
            contact_block = (
                '                _p6ShieldSrc = stats.get("shieldSource") or "UNKNOWN"\n'
                '                stats["shield"] -= absorb\n'
                '                if absorb > 0:\n'
                '                    stats["p6ShieldAbsorbTotal"] += absorb\n'
                '                    stats["p6ShieldAbsorbBySource"][_p6ShieldSrc] = stats["p6ShieldAbsorbBySource"].get(_p6ShieldSrc, 0.0) + absorb\n'
            )
            if src.count(contact_line) != 1:
                raise RuntimeError("Contact shield absorb site changed")
            src = src.replace(contact_line, contact_block, 1)

            slow_block = (
                '                if cls == "Tank" and any(\n'
                '                    abs(zx - m.x) <= 0.16 and abs(zb - m.band) <= 1\n'
                '                    for _, zx, zb in stats["aftershockZones"]\n'
                '                ):\n'
                '                    speed *= 0.75\n'
            )
            slow_new = (
                f'                if {str(aftershock_slow)} and cls == "Tank" and any(\n'
                '                    abs(zx - m.x) <= 0.16 and abs(zb - m.band) <= 1\n'
                '                    for _, zx, zb in stats["aftershockZones"]\n'
                '                ):\n'
                '                    stats["p6AftershockSlowTicks"] += 1\n'
                '                    stats["p6AftershockSlowEnemySeconds"] += dt\n'
                '                    speed *= 0.75\n'
            )
            if src.count(slow_block) != 1:
                raise RuntimeError("Aftershock slow block changed")
            src = src.replace(slow_block, slow_new, 1)

            if not iron_wall:
                iron = '* (0.90 if cls == "Tank" else 1.0)'
                count = src.count(iron)
                if count != 2:
                    raise RuntimeError(f"Iron Wall sites changed: {count}")
                src = src.replace(iron, '* 1.0')

        return original_exec(src, ns, *args, **kwargs)

    builtins.exec = instrumented_exec
    try:
        fn = bridge.build_bridge_simulate()
    finally:
        builtins.exec = original_exec
    return causal.install_push_telemetry(fn)


def no_push(fn):
    glb = fn.__globals__
    original = glb["push"]
    def noop(m, tier, mul, now, stats):
        return None
    glb["push"] = noop
    return fn, original


def run_variant(name, sim_fn, base, temporal, direction, shop, integration, central, *, suppress_push=False):
    restore = None
    if suppress_push:
        sim_fn, restore = no_push(sim_fn)
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
        if restore is not None:
            sim_fn.__globals__["push"] = restore
    return {"name": name, "rows": rows}


def aggregate(block):
    skilled = [r for r in block["rows"] if r["mode"] == "SKILLED_V2_CENTRAL"]
    perfect = [r for r in block["rows"] if r["mode"] == "ALL_PERFECT"]
    stages46 = [s for r in skilled for s in r["stages"] if s["stage"] == 46]
    def rawsum(key):
        return describe([s.get(key, 0.0) for s in stages46])
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
            "wallLoss": describe([s["wallLoss"] for s in stages46]),
            "maxActive": describe([s["maxActive"] for s in stages46]),
            "damage": describe([s["damage"] for s in stages46]),
            "pushDistance": describe([s["pushDistance"] for s in stages46]),
            "chargerInterrupts": describe([s["chargerInterrupts"] for s in stages46]),
            "shieldAbsorbTotal": rawsum("p6ShieldAbsorbTotal"),
            "lv31BarrierCreates": rawsum("p6Lv31BarrierCreates"),
            "lv16BarrierCreates": rawsum("p6Lv16BarrierCreates"),
            "aftershockSlowEnemySeconds": rawsum("p6AftershockSlowEnemySeconds"),
        },
    }


def main():
    base, temporal, direction, shop, integration, central = bridge.load_inputs()

    specs = [
        ("SOURCE_CURRENT", dict(correct_aftershock_center=False)),
        ("FIDELITY_CORRECTED", dict(correct_aftershock_center=True)),
        ("NO_LV31_BARRIER", dict(correct_aftershock_center=True, lv31_barrier=False)),
        ("NO_ALL_BARRIERS", dict(correct_aftershock_center=True, lv31_barrier=False, lv16_barrier=False)),
        ("NO_AFTERSHOCK_SLOW", dict(correct_aftershock_center=True, aftershock_slow=False)),
        ("NO_IRON_WALL", dict(correct_aftershock_center=True, iron_wall=False)),
    ]

    blocks = []
    for name, kwargs in specs:
        fn = build_sim(**kwargs)
        blocks.append(run_variant(name, fn, base, temporal, direction, shop, integration, central))

    fn = build_sim(correct_aftershock_center=True)
    blocks.append(run_variant("NO_PUSH", fn, base, temporal, direction, shop, integration, central, suppress_push=True))

    agg = {b["name"]: aggregate(b) for b in blocks}
    output = {
        "version": "p6-tank-objective-attribution-temp-v0.1",
        "status": "DIAGNOSTIC_ATTRIBUTION_ONLY_NO_NUMERICAL_FREEZE_NO_PRODUCTION_AUTHORITY",
        "basis": {
            "family": FAMILY,
            "profile": PROFILE,
            "seeds": list(SEEDS),
            "shockwaveCoefficient": 0.25,
            "normalRightEdgePreserved": True,
            "purpose": "First correct Aftershock impact-center fidelity, then attribute existing Tank objective-protection components without changing their numeric values.",
        },
        "aggregate": agg,
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
            "s46ShieldAbsorbMean": v["stage46"]["shieldAbsorbTotal"]["mean"],
            "s46Lv31BarrierCreatesMean": v["stage46"]["lv31BarrierCreates"]["mean"],
            "s46Lv16BarrierCreatesMean": v["stage46"]["lv16BarrierCreates"]["mean"],
            "s46SlowEnemySecondsMean": v["stage46"]["aftershockSlowEnemySeconds"]["mean"],
        }
        for k, v in agg.items()
    }
    print("P6_TANK_ATTRIBUTION=" + json.dumps(compact, sort_keys=True))
    print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
