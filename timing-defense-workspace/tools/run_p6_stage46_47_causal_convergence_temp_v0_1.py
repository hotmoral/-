#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import run_p5_p6_fidelity_bridge_stage46_49_temp_v0_1 as bridge

OUT = Path("p6_stage46_47_causal_convergence_temp_v0_1.json")
PROFILES = ("BALANCED", "ATTACK_HEAVY", "DEFENSE_HEAVY", "ROLE_AWARE")
ENTRY_CHARGE = 0
STAGES = (46, 47)
SEEDS = tuple(range(1, 21))


def delta_counts(after: dict, before: dict, key: str) -> dict:
    a = Counter(after.get(key) or {})
    b = Counter(before.get(key) or {})
    return {k: int(a[k] - b[k]) for k in sorted(set(a) | set(b)) if a[k] - b[k]}


def install_push_telemetry(sim_fn):
    glb = sim_fn.__globals__
    original = glb["push"]

    def measured_push(m, tier, mul, now, stats):
        if not m or not getattr(m, "alive", False):
            return original(m, tier, mul, now, stats)
        before_x = float(m.x)
        before_ci = int(stats.get("chargerInterrupts", 0))
        before_sr = int(stats.get("siegerRepositions", 0))
        typ = str(getattr(m, "typ", "UNKNOWN"))
        result = original(m, tier, mul, now, stats)
        dx = max(0.0, float(m.x) - before_x)
        if dx > 1e-12:
            stats["p6PushEvents"] = int(stats.get("p6PushEvents", 0)) + 1
            stats["p6PushDistance"] = float(stats.get("p6PushDistance", 0.0)) + dx
            by_type = stats.setdefault("p6PushDistanceByType", {})
            by_type[typ] = float(by_type.get(typ, 0.0)) + dx
        stats["p6InterruptsFromPush"] = int(stats.get("p6InterruptsFromPush", 0)) + max(
            0, int(stats.get("chargerInterrupts", 0)) - before_ci
        )
        stats["p6SiegerRepositionsFromPush"] = int(stats.get("p6SiegerRepositionsFromPush", 0)) + max(
            0, int(stats.get("siegerRepositions", 0)) - before_sr
        )
        return result

    glb["push"] = measured_push
    return sim_fn


def stage_summary(row: dict, result: dict, before: dict, after: dict, start_wall: float) -> dict:
    heavy = int(after["heavyActions"] - before["heavyActions"])
    pxp = int(after["pxpActions"] - before["pxpActions"])
    judgments = int(after["judgmentsConsumed"] - before["judgmentsConsumed"])
    root = int(after["rootActions"] - before["rootActions"])
    return {
        "stage": int(row.get("stage", 0)) if row.get("stage") is not None else None,
        "settled": bool(result["settled"]),
        "burialTime": row.get("burialTime"),
        "duration": float(row.get("durationSimulated") or 0.0),
        "startWall": round(float(start_wall), 3),
        "endWall": round(float(row.get("endWall") or 0.0), 3),
        "wallLoss": round(max(0.0, float(start_wall) - float(row.get("endWall") or 0.0)), 3),
        "wallHits": int(row.get("wallHits") or 0),
        "damage": round(float(row.get("damage") or 0.0), 3),
        "kills": int(row.get("kills") or 0),
        "killsByType": dict(sorted((row.get("killsByType") or {}).items())),
        "maxActive": int(row.get("maxActive") or 0),
        "endActive": int(row.get("endActive") or 0),
        "noTargetDrops": int(row.get("noTargetDrops") or 0),
        "chargerWindups": int(row.get("chargerWindups") or 0),
        "chargerInterrupts": int(row.get("chargerInterrupts") or 0),
        "chargerCharges": int(row.get("chargerCharges") or 0),
        "siegerWindups": int(row.get("siegerWindups") or 0),
        "siegerShots": int(row.get("siegerShots") or 0),
        "siegerRepositions": int(row.get("siegerRepositions") or 0),
        "pushEvents": int(row.get("p6PushEvents") or 0),
        "pushDistance": round(float(row.get("p6PushDistance") or 0.0), 6),
        "pushDistanceByType": {
            k: round(float(v), 6) for k, v in sorted((row.get("p6PushDistanceByType") or {}).items())
        },
        "interruptsFromPush": int(row.get("p6InterruptsFromPush") or 0),
        "siegerRepositionsFromPush": int(row.get("p6SiegerRepositionsFromPush") or 0),
        "judgmentsConsumed": judgments,
        "rootActions": root,
        "heavyActions": heavy,
        "pxpActions": pxp,
        "pxpRate": round(pxp / heavy, 6) if heavy else None,
        "n3Triggers": int(after["n3Triggers"] - before["n3Triggers"]),
        "judgmentCounts": delta_counts(after, before, "judgmentCounts"),
        "heavyTierCounts": delta_counts(after, before, "heavyTierCounts"),
        "damagePerRoot": round(float(row.get("damage") or 0.0) / root, 6) if root else None,
        "killsPerRoot": round(int(row.get("kills") or 0) / root, 6) if root else None,
    }


def run_chain(sim_fn, base, temporal, direction, shop, integration, central, cls, profile_name, mode, seed):
    bridge.BRIDGE_CTX["central"] = central
    state = bridge.new_run_state(mode, central, int(seed), cls, ENTRY_CHARGE)
    profile = bridge.integ.profile_for(shop, cls, profile_name)
    scale = float(integration["shopEffectScale"])
    wall_max = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * scale
    current = wall_max
    stages = []

    for stage_no in STAGES:
        start_wall = current
        result = bridge.simulate_stage(
            sim_fn, base, temporal, direction, integration,
            cls, profile, scale, stage_no, current, state,
        )
        row = result["row"]
        before = result["stateBefore"]
        after = result["stateAfter"]
        # Raw simulate rows do not carry the stage number.
        row = dict(row)
        row["stage"] = stage_no
        stages.append(stage_summary(row, result, before, after, start_wall))
        current = float(row.get("endWall") or 0.0)
        state = after
        if not result["settled"]:
            break

    heavy = int(state["heavyActions"])
    pxp = int(state["pxpActions"])
    return {
        "mode": mode,
        "seed": int(seed),
        "class": cls,
        "profile": profile_name,
        "shopProfile": profile,
        "entryCharge": ENTRY_CHARGE,
        "through47": len(stages) == 2 and all(s["settled"] for s in stages),
        "failureStage": None if len(stages) == 2 and all(s["settled"] for s in stages) else stages[-1]["stage"],
        "finalWall": round(current, 3),
        "wallMax": round(wall_max, 3),
        "finalDeficit": round(max(0.0, wall_max - current), 3),
        "totalJudgments": int(state["judgmentsConsumed"]),
        "totalRootActions": int(state["rootActions"]),
        "totalHeavyActions": heavy,
        "totalPxpActions": pxp,
        "totalPxpRate": round(pxp / heavy, 6) if heavy else None,
        "totalN3Triggers": int(state["n3Triggers"]),
        "comboPeak": int(state["comboPeak"]),
        "judgmentCounts": dict(sorted(state["judgmentCounts"].items())),
        "heavyTierCounts": dict(sorted(state["heavyTierCounts"].items())),
        "stages": stages,
    }


def describe(values):
    vals = [float(x) for x in values if x is not None]
    if not vals:
        return None
    return {
        "n": len(vals),
        "mean": round(statistics.fmean(vals), 6),
        "median": round(statistics.median(vals), 6),
        "min": round(min(vals), 6),
        "max": round(max(vals), 6),
    }


def pxp_bin(rate):
    if rate is None:
        return "NONE"
    if rate <= 0.40:
        return "LOW_LE_0P40"
    if rate <= 0.65:
        return "MID_0P40_0P65"
    return "HIGH_GT_0P65"


def aggregate(rows):
    result = {"profiles": {}, "pxpBands": {}}
    skilled = [r for r in rows if r["mode"] == "SKILLED_V2_CENTRAL"]
    perfect = [r for r in rows if r["mode"] == "ALL_PERFECT"]

    for profile in PROFILES:
        result["profiles"][profile] = {}
        for cls in bridge.CLASSES:
            cr = [r for r in skilled if r["profile"] == profile and r["class"] == cls]
            pr = [r for r in perfect if r["profile"] == profile and r["class"] == cls]
            fail = Counter(str(r["failureStage"]) for r in cr if r["failureStage"] is not None)
            block = {
                "cases": len(cr),
                "through47": sum(1 for r in cr if r["through47"]),
                "failureStages": dict(sorted(fail.items())),
                "allPerfectThrough47": sum(1 for r in pr if r["through47"]),
                "allPerfectCases": len(pr),
                "finalWall": describe([r["finalWall"] for r in cr]),
                "totalJudgments": describe([r["totalJudgments"] for r in cr]),
                "totalRootActions": describe([r["totalRootActions"] for r in cr]),
                "totalPxpRate": describe([r["totalPxpRate"] for r in cr]),
                "comboPeak": describe([r["comboPeak"] for r in cr]),
                "stages": {},
            }
            for st in STAGES:
                sr = [s for r in cr for s in r["stages"] if s["stage"] == st]
                block["stages"][str(st)] = {
                    "casesReached": len(sr),
                    "settled": sum(1 for s in sr if s["settled"]),
                    "damage": describe([s["damage"] for s in sr]),
                    "kills": describe([s["kills"] for s in sr]),
                    "duration": describe([s["duration"] for s in sr]),
                    "wallLoss": describe([s["wallLoss"] for s in sr]),
                    "wallHits": describe([s["wallHits"] for s in sr]),
                    "maxActive": describe([s["maxActive"] for s in sr]),
                    "endActive": describe([s["endActive"] for s in sr]),
                    "pushDistance": describe([s["pushDistance"] for s in sr]),
                    "pushEvents": describe([s["pushEvents"] for s in sr]),
                    "chargerInterrupts": describe([s["chargerInterrupts"] for s in sr]),
                    "siegerRepositions": describe([s["siegerRepositions"] for s in sr]),
                    "siegerShots": describe([s["siegerShots"] for s in sr]),
                    "judgmentsConsumed": describe([s["judgmentsConsumed"] for s in sr]),
                    "rootActions": describe([s["rootActions"] for s in sr]),
                    "pxpRate": describe([s["pxpRate"] for s in sr]),
                    "damagePerRoot": describe([s["damagePerRoot"] for s in sr]),
                    "killsPerRoot": describe([s["killsPerRoot"] for s in sr]),
                    "noTargetDrops": describe([s["noTargetDrops"] for s in sr]),
                }
            result["profiles"][profile][cls] = block

    for profile in PROFILES:
        result["pxpBands"][profile] = {}
        for cls in bridge.CLASSES:
            bins = defaultdict(list)
            for r in skilled:
                if r["profile"] == profile and r["class"] == cls:
                    bins[pxp_bin(r["totalPxpRate"])].append(r)
            result["pxpBands"][profile][cls] = {
                b: {
                    "cases": len(br),
                    "through47": sum(1 for r in br if r["through47"]),
                    "finalWall": describe([r["finalWall"] for r in br]),
                    "pxpRate": describe([r["totalPxpRate"] for r in br]),
                    "judgments": describe([r["totalJudgments"] for r in br]),
                }
                for b, br in sorted(bins.items())
            }
    return result


def compact_for_log(agg):
    out = {}
    for profile in PROFILES:
        out[profile] = {}
        for cls in bridge.CLASSES:
            b = agg["profiles"][profile][cls]
            out[profile][cls] = {
                "through47": b["through47"],
                "cases": b["cases"],
                "fail": b["failureStages"],
                "allPerfect": f'{b["allPerfectThrough47"]}/{b["allPerfectCases"]}',
                "finalWallMedian": None if b["finalWall"] is None else b["finalWall"]["median"],
                "judgmentsMean": None if b["totalJudgments"] is None else b["totalJudgments"]["mean"],
                "pxpRateMean": None if b["totalPxpRate"] is None else b["totalPxpRate"]["mean"],
                "s46DamageMean": b["stages"]["46"]["damage"]["mean"],
                "s46WallLossMean": b["stages"]["46"]["wallLoss"]["mean"],
                "s46PushMean": b["stages"]["46"]["pushDistance"]["mean"],
                "s46MaxActiveMean": b["stages"]["46"]["maxActive"]["mean"],
            }
    return out


def main():
    base, temporal, direction, shop, integration, central = bridge.load_inputs()
    sim_fn = install_push_telemetry(bridge.build_bridge_simulate())
    rows = []

    for profile in PROFILES:
        for seed in SEEDS:
            for cls in bridge.CLASSES:
                rows.append(run_chain(
                    sim_fn, base, temporal, direction, shop, integration, central,
                    cls, profile, "SKILLED_V2_CENTRAL", seed,
                ))
        for cls in bridge.CLASSES:
            rows.append(run_chain(
                sim_fn, base, temporal, direction, shop, integration, central,
                cls, profile, "ALL_PERFECT", 1,
            ))

    agg = aggregate(rows)
    output = {
        "version": "p6-stage46-47-causal-convergence-temp-v0.1",
        "status": "P6_DIAGNOSTIC_ONLY_NO_NUMERICAL_ADOPTION_NO_PRODUCTION_AUTHORITY",
        "scope": {
            "stages": list(STAGES),
            "entryCharge": ENTRY_CHARGE,
            "entryComboBoundary": 0,
            "skilledSeeds": list(SEEDS),
            "profiles": list(PROFILES),
            "shopEffectScale": float(integration["shopEffectScale"]),
            "shopTemporalAcquisitionMode": integration["shopTemporalAcquisitionMode"],
            "judgmentModel": "SKILLED_V2_CENTRAL",
            "allPerfectControlsPerClassProfile": 1,
            "tankShockwaveCoefficientDiagnosticCenter": 0.25,
            "encounterGeometryChanged": False,
            "classSemanticsChanged": False,
            "pushTelemetryOnly": True,
        },
        "aggregate": agg,
        "rows": rows,
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    OUT.write_text(text + "\n", encoding="utf-8")
    print("P6_COMPACT=" + json.dumps(compact_for_log(agg), sort_keys=True))
    print("P6_PXP_BANDS=" + json.dumps(agg["pxpBands"], sort_keys=True))
    print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
