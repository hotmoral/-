#!/usr/bin/env python3
"""TEMP v0.2 wrapper for the P5 SKILLED_V2 vs all-perfect comparison.

Changes from v0.1:
- fixes HEAVY+ knockback compatibility to the authoritative 0.013 tier value;
- expands the deterministic screen to seeds 1..20 because the streak-aware model
  has intentionally large short-window variation;
- adds failure-stage and judgment/heavy-tier aggregates.

Diagnostic only; no adoption/freeze/production authority.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import run_p5_stage46_49_skilled_v2_vs_allperfect_grunt_temp as v1

OUT1 = Path("p5_stage46_49_skilled_v2_vs_allperfect_grunt_temp.json")
OUT2 = Path("p5_stage46_49_skilled_v2_vs_allperfect_grunt_temp_v2.json")


def main():
    # Authoritative tier_knock mapping has HEAVY+ with GOOD/GREAT at 0.013.
    original_basic_knock = v1.stage46.basic_knock

    def corrected_basic_knock(tier):
        if tier == "HEAVY+":
            return 0.013
        return original_basic_knock(tier)

    v1.stage46.basic_knock = corrected_basic_knock
    v1.SEEDS = list(range(1, 21))
    v1.main()

    d = json.loads(OUT1.read_text(encoding="utf-8"))
    d["version"] = "p5-stage46-49-skilled-v2-vs-allperfect-grunt-temp-v0.2"
    d["fidelityFixes"] = [
        "HEAVY+ knockback uses authoritative 0.013 tier value",
        "20 deterministic base seeds used to reduce short-window streak sampling noise",
    ]

    skilled = d["skilled"]
    j = Counter()
    h = Counter()
    failure_stage = Counter()
    reached48 = 0
    reached49 = 0
    for row in skilled:
        j.update(row.get("judgmentCounts") or {})
        h.update(row.get("heavyTierCounts") or {})
        stages = row.get("stages") or []
        if any(s["stage"] == 48 for s in stages):
            reached48 += 1
        if any(s["stage"] == 49 for s in stages):
            reached49 += 1
        if not row.get("settledThroughStage49"):
            failure_stage[str(stages[-1]["stage"] if stages else "NONE")] += 1

    total_j = sum(j.values())
    total_h = sum(h.values())
    agg = d["aggregate"]["skilled"]
    agg["reachedStage48"] = reached48
    agg["reachedStage49"] = reached49
    agg["failureStageCounts"] = dict(sorted(failure_stage.items()))
    agg["judgmentCounts"] = dict(sorted(j.items()))
    agg["judgmentMix"] = {k: round(v / total_j, 6) for k, v in sorted(j.items())} if total_j else {}
    agg["heavyTierCounts"] = dict(sorted(h.items()))
    agg["pxpRateAcrossRealizedHeavy"] = round(h.get("CRITICAL", 0) / total_h, 6) if total_h else None

    for cls, info in agg["perClass"].items():
        rows = [r for r in skilled if r["class"] == cls]
        info["reachedStage48"] = sum(1 for r in rows if any(s["stage"] == 48 for s in r["stages"]))
        info["reachedStage49"] = sum(1 for r in rows if any(s["stage"] == 49 for s in r["stages"]))
        fs = Counter()
        for r in rows:
            if not r["settledThroughStage49"]:
                fs[str(r["stages"][-1]["stage"] if r["stages"] else "NONE")] += 1
        info["failureStageCounts"] = dict(sorted(fs.items()))

    text = json.dumps(d, indent=2, sort_keys=True)
    OUT2.write_text(text + "\n", encoding="utf-8")
    print(text)
    print("SHA256=" + hashlib.sha256(OUT2.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
