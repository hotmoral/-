#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path

import run_p5_p6_fidelity_bridge_stage46_49_temp_v0_1 as bridge
import run_p6_stage46_47_causal_convergence_temp_v0_1 as causal

OUT = Path("p6_pressure_family_rotation_temp_v0_1.json")
PROFILE = "BALANCED"
ENTRY_CHARGE = 0
STAGES = (46, 47)
SEEDS = tuple(range(1, 6))  # bounded preflight; expand only if family separation is informative

FAMILIES = ("BASELINE_DENSE_ALIGNED", "DURABLE_DISTRIBUTED", "CONTROL_OBJECTIVE")
ACTIVE_FAMILY = "BASELINE_DENSE_ALIGNED"
_ORIGINAL_FIXED = bridge.fixed_stage_cfg

# Diagnostic schedules only. Every mob still spawns at the normal right edge through the inherited kernel.
PACKETS = {
    "DURABLE_DISTRIBUTED": [
        (0.00, "BRUTE", -2),
        (0.70, "SHIELD", 2),
        (1.40, "BRUTE", 0),
        (2.10, "SHIELD", -1),
        (2.80, "GRUNT", 1),
    ],
    "CONTROL_OBJECTIVE": [
        (0.00, "BRUTE", 0),
        (0.65, "CHARGER", -2),
        (1.30, "SHIELD", 2),
        (1.95, "CHARGER", 1),
        (2.60, "SIEGER", -1),
    ],
}

REPEATS = {
    "DURABLE_DISTRIBUTED": {46: (15, 3.80), 47: (17, 3.30)},
    "CONTROL_OBJECTIVE": {46: (18, 3.25), 47: (20, 2.90)},
}


def custom_schedule(family: str, stage_no: int) -> list[tuple[float, str, int]]:
    if family == "BASELINE_DENSE_ALIGNED":
        raise RuntimeError("baseline schedule is inherited, not synthesized")
    count, period = REPEATS[family][stage_no]
    packet = PACKETS[family]
    out = []
    for i in range(int(count)):
        base_t = i * float(period)
        for off, typ, band in packet:
            t = base_t + float(off)
            if t < 60.0:
                out.append((round(t, 6), str(typ), int(band)))
    return sorted(out, key=lambda x: (x[0], x[1], x[2]))


def patched_fixed_stage_cfg(base_temporal, direction, integration, stage_no, cls, duration):
    cfg, baseline = _ORIGINAL_FIXED(base_temporal, direction, integration, stage_no, cls, duration)
    if ACTIVE_FAMILY == "BASELINE_DENSE_ALIGNED":
        return cfg, baseline
    schedule = custom_schedule(ACTIVE_FAMILY, int(stage_no))
    cfg["version"] = f"p6-pressure-family-{ACTIVE_FAMILY.lower()}-stage{stage_no}-temp-v0.1"
    cfg["_p5FixedStageSchedule"] = [list(x) for x in schedule]
    return cfg, schedule


def effective_hp(base: dict, typ: str) -> float:
    a = base["monsterAnchors"][typ]
    hp = float(a["hp"])
    if typ == "SPLITTER":
        ch = a.get("children") or {}
        hp += float(ch.get("count", 0)) * float(ch.get("hp", 0.0))
    return hp


def schedule_budget(base: dict, schedule: list[tuple[float, str, int]]) -> dict:
    counts = Counter(typ for _, typ, _ in schedule)
    hp = sum(effective_hp(base, typ) for _, typ, _ in schedule)
    nominal_wall = sum(float(base["monsterAnchors"][typ]["wall"]) for _, typ, _ in schedule)
    return {
        "bodies": len(schedule),
        "counts": dict(sorted(counts.items())),
        "effectiveHpIncludingSplitterChildren": round(hp, 3),
        "nominalContactWallBudget": round(nominal_wall, 3),
        "note": "SIEGER ranged shots are not included in nominalContactWallBudget.",
    }


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


def summarize(rows):
    out = {"families": {}, "rankOrders": {}}
    for family in FAMILIES:
        fr = [r for r in rows if r["family"] == family and r["mode"] == "SKILLED_V2_CENTRAL"]
        fp = [r for r in rows if r["family"] == family and r["mode"] == "ALL_PERFECT"]
        out["families"][family] = {}
        ranking = []
        for cls in bridge.CLASSES:
            cr = [r for r in fr if r["class"] == cls]
            cp = [r for r in fp if r["class"] == cls]
            s46 = [s for r in cr for s in r["stages"] if s["stage"] == 46]
            s47 = [s for r in cr for s in r["stages"] if s["stage"] == 47]
            through = sum(1 for r in cr if r["through47"])
            final_wall = describe([r["finalWall"] for r in cr])
            block = {
                "cases": len(cr),
                "through47": through,
                "failureStages": dict(sorted(Counter(str(r["failureStage"]) for r in cr if r["failureStage"] is not None).items())),
                "allPerfectThrough47": sum(1 for r in cp if r["through47"]),
                "allPerfectCases": len(cp),
                "finalWall": final_wall,
                "totalJudgments": describe([r["totalJudgments"] for r in cr]),
                "totalPxpRate": describe([r["totalPxpRate"] for r in cr]),
                "stage46": {
                    "damage": describe([s["damage"] for s in s46]),
                    "wallLoss": describe([s["wallLoss"] for s in s46]),
                    "maxActive": describe([s["maxActive"] for s in s46]),
                    "pushDistance": describe([s["pushDistance"] for s in s46]),
                    "chargerInterrupts": describe([s["chargerInterrupts"] for s in s46]),
                    "siegerRepositions": describe([s["siegerRepositions"] for s in s46]),
                    "siegerShots": describe([s["siegerShots"] for s in s46]),
                },
                "stage47CasesReached": len(s47),
            }
            out["families"][family][cls] = block
            ranking.append((through, 0.0 if final_wall is None else final_wall["median"], cls))
        # Descriptive ordering only: survival first, median remaining wall as tie-breaker.
        out["rankOrders"][family] = [x[2] for x in sorted(ranking, key=lambda x: (-x[0], -x[1], x[2]))]
    return out


def compact(agg):
    out = {}
    for family in FAMILIES:
        out[family] = {
            cls: {
                "through47": agg["families"][family][cls]["through47"],
                "finalWallMedian": agg["families"][family][cls]["finalWall"]["median"],
                "s46WallLossMean": agg["families"][family][cls]["stage46"]["wallLoss"]["mean"],
                "s46MaxActiveMean": agg["families"][family][cls]["stage46"]["maxActive"]["mean"],
                "s46PushMean": agg["families"][family][cls]["stage46"]["pushDistance"]["mean"],
                "s46ChargerInterruptMean": agg["families"][family][cls]["stage46"]["chargerInterrupts"]["mean"],
                "s46SiegerRepositionMean": agg["families"][family][cls]["stage46"]["siegerRepositions"]["mean"],
            }
            for cls in bridge.CLASSES
        }
    return {"rankOrders": agg["rankOrders"], "classes": out}


def main():
    global ACTIVE_FAMILY
    base, temporal, direction, shop, integration, central = bridge.load_inputs()
    bridge.fixed_stage_cfg = patched_fixed_stage_cfg
    sim_fn = causal.install_push_telemetry(bridge.build_bridge_simulate())

    budgets = {}
    for family in FAMILIES:
        budgets[family] = {}
        for stage_no in STAGES:
            if family == "BASELINE_DENSE_ALIGNED":
                _, schedule = _ORIGINAL_FIXED(temporal, direction, integration, stage_no, "Knight", bridge.DRAIN_SECONDS)
            else:
                schedule = custom_schedule(family, stage_no)
            budgets[family][str(stage_no)] = schedule_budget(base, schedule)

    rows = []
    for family in FAMILIES:
        ACTIVE_FAMILY = family
        for seed in SEEDS:
            for cls in bridge.CLASSES:
                row = causal.run_chain(
                    sim_fn, base, temporal, direction, shop, integration, central,
                    cls, PROFILE, "SKILLED_V2_CENTRAL", int(seed),
                )
                row["family"] = family
                rows.append(row)
        for cls in bridge.CLASSES:
            row = causal.run_chain(
                sim_fn, base, temporal, direction, shop, integration, central,
                cls, PROFILE, "ALL_PERFECT", 1,
            )
            row["family"] = family
            rows.append(row)

    agg = summarize(rows)
    output = {
        "version": "p6-pressure-family-rotation-temp-v0.1-preflight",
        "status": "DIAGNOSTIC_ONLY_NO_CONTENT_ADOPTION_NO_NUMERICAL_FREEZE_NO_PRODUCTION_AUTHORITY",
        "basis": {
            "profile": PROFILE,
            "entryCharge": ENTRY_CHARGE,
            "entryComboBoundary": 0,
            "stages": list(STAGES),
            "skilledSeeds": list(SEEDS),
            "families": list(FAMILIES),
            "normalRightEdgePreserved": True,
            "persistentTimingStatePreserved": True,
            "stageSettledRequired": True,
            "wallStateCarried": True,
            "familyBudgetsAreNormalizationDiagnosticsNotBalanceTargets": True,
            "rankOrderRule": "through47 desc, then median final wall desc; descriptive only",
        },
        "budgets": budgets,
        "aggregate": agg,
        "rows": rows,
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    OUT.write_text(text + "\n", encoding="utf-8")
    print("P6_PRESSURE_PREFLIGHT=" + json.dumps(compact(agg), sort_keys=True))
    print("P6_PRESSURE_BUDGETS=" + json.dumps(budgets, sort_keys=True))
    print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
