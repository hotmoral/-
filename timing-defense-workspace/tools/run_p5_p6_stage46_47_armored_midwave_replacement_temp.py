#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import run_p5_p6_fidelity_bridge_stage46_49_temp_v0_1 as bridge

OUT = Path("p5_p6_stage46_47_armored_midwave_replacement_temp.json")
ENTRY_CHARGE = 0
VARIANTS = {
    "BASELINE": 0,
    "ARMOR1_PER_STAGE": 1,
    "ARMOR2_PER_STAGE": 2,
}
TARGET_TIMES = {
    1: (30.0,),
    2: (20.0, 40.0),
}

ACTIVE_REPLACEMENTS = 0
REPLACEMENT_LOG = {}
_ORIGINAL_FIXED = bridge.fixed_stage_cfg


def replace_grunts(schedule, stage_no, cls, count):
    rows = [tuple(x) for x in schedule]
    if stage_no not in (46, 47) or count <= 0:
        return rows

    eligible = [i for i, row in enumerate(rows) if str(row[1]) == "GRUNT"]
    chosen = []
    used = set()
    for target in TARGET_TIMES[count]:
        candidates = [i for i in eligible if i not in used]
        if not candidates:
            raise RuntimeError(f"No GRUNT candidate left for Stage{stage_no} {cls} count={count}")
        idx = min(candidates, key=lambda i: (abs(float(rows[i][0]) - target), float(rows[i][0]), i))
        used.add(idx)
        chosen.append(idx)

    out = list(rows)
    details = []
    for idx in sorted(chosen):
        t, old_type, band = out[idx]
        out[idx] = (float(t), "ARMORED_DURABLE_PROXY", int(band))
        details.append({
            "time": round(float(t), 3),
            "band": int(band),
            "replacedType": str(old_type),
        })

    REPLACEMENT_LOG.setdefault(str(count), {}).setdefault(str(stage_no), {})[cls] = details
    return out


def patched_fixed_stage_cfg(base_temporal, direction, integration, stage_no, cls, duration):
    cfg, schedule = _ORIGINAL_FIXED(base_temporal, direction, integration, stage_no, cls, duration)
    replaced = replace_grunts(schedule, stage_no, cls, ACTIVE_REPLACEMENTS)
    cfg["_p5FixedStageSchedule"] = [list(x) for x in replaced]
    return cfg, replaced


def aggregate(rows):
    out = {
        "cases": len(rows),
        "through49": sum(1 for r in rows if r["settledThroughStage49"]),
        "failureStages": dict(sorted(Counter(str(r["failureStage"]) for r in rows if r["failureStage"] is not None).items())),
        "perClass": {},
    }
    for cls in bridge.CLASSES:
        cr = [r for r in rows if r["class"] == cls]
        out["perClass"][cls] = {
            "cases": len(cr),
            "through49": sum(1 for r in cr if r["settledThroughStage49"]),
            "failureStages": dict(sorted(Counter(str(r["failureStage"]) for r in cr if r["failureStage"] is not None).items())),
            "reached48": sum(1 for r in cr if r["reachedStage48"]),
            "finalWalls": [r["finalWall"] for r in cr],
        }
    return out


def main():
    global ACTIVE_REPLACEMENTS

    base, temporal, direction, shop, integration, central = bridge.load_inputs()
    sim_fn = bridge.build_bridge_simulate()
    bridge.fixed_stage_cfg = patched_fixed_stage_cfg

    output = {
        "version": "p5-p6-stage46-47-armored-midwave-replacement-temp-v0.1",
        "status": "DIAGNOSTIC_ONLY_NO_ADOPTION_NO_PRODUCTION_AUTHORITY",
        "basis": {
            "entryCharge": ENTRY_CHARGE,
            "profile": bridge.PROFILE,
            "skilledSeeds": list(bridge.SEEDS),
            "replacementType": "ARMORED_DURABLE_PROXY",
            "replacedOnly": "GRUNT",
            "stageScope": [46, 47],
            "totalMonsterCountChanged": False,
            "stage48And49Changed": False,
            "note": "Existing armored diagnostic anchor is reused unchanged; no new monster or scalar is authored.",
        },
        "variants": {},
    }

    for name, count in VARIANTS.items():
        ACTIVE_REPLACEMENTS = int(count)
        skilled = []
        for seed in bridge.SEEDS:
            for cls in bridge.CLASSES:
                skilled.append(bridge.run_chain(
                    sim_fn, base, temporal, direction, shop, integration, central,
                    cls, "SKILLED_V2_CENTRAL", int(seed), ENTRY_CHARGE,
                ))
        perfect = [
            bridge.run_chain(
                sim_fn, base, temporal, direction, shop, integration, central,
                cls, "ALL_PERFECT", 1, ENTRY_CHARGE,
            )
            for cls in bridge.CLASSES
        ]
        output["variants"][name] = {
            "replacementCountPerStage46And47": int(count),
            "skilled": aggregate(skilled),
            "allPerfect": aggregate(perfect),
        }

    output["replacementLog"] = REPLACEMENT_LOG
    text = json.dumps(output, indent=2, sort_keys=True)
    OUT.write_text(text + "\n", encoding="utf-8")
    print(text)
    print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
