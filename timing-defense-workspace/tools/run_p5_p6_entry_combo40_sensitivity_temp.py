#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import run_p5_p6_fidelity_bridge_stage46_49_temp_v0_1 as bridge

OUT = Path("p5_p6_entry_combo40_sensitivity_temp.json")
ENTRY_COMBOS = (0, 40)
ENTRY_CHARGE = 0


def main():
    base, temporal, direction, shop, integration, central = bridge.load_inputs()
    sim_fn = bridge.build_bridge_simulate()
    original_new = bridge.new_run_state
    rows = []

    try:
        for entry_combo in ENTRY_COMBOS:
            def with_combo(mode, central_cfg, base_seed, cls, entry_charge, _combo=entry_combo):
                rs = original_new(mode, central_cfg, base_seed, cls, entry_charge)
                rs["combo"] = int(_combo)
                rs["comboPeak"] = int(_combo)
                return rs

            bridge.new_run_state = with_combo
            for seed in bridge.SEEDS:
                for cls in bridge.CLASSES:
                    row = bridge.run_chain(
                        sim_fn, base, temporal, direction, shop, integration, central,
                        cls, "SKILLED_V2_CENTRAL", seed, ENTRY_CHARGE,
                    )
                    row["entryComboSensitivity"] = int(entry_combo)
                    rows.append(row)
    finally:
        bridge.new_run_state = original_new

    aggregate = {}
    for entry_combo in ENTRY_COMBOS:
        rr = [r for r in rows if r["entryComboSensitivity"] == entry_combo]
        per_class = {}
        for cls in bridge.CLASSES:
            cr = [r for r in rr if r["class"] == cls]
            per_class[cls] = {
                "cases": len(cr),
                "through49": sum(1 for r in cr if r["settledThroughStage49"]),
                "failureStages": dict(sorted(Counter(str(r["failureStage"]) for r in cr if r["failureStage"] is not None).items())),
                "reached48": sum(1 for r in cr if r["reachedStage48"]),
                "stage48SiegerShotCases": sum(1 for r in cr if any(s["stage"] == 48 and s["siegerShots"] > 0 for s in r["stages"])),
                "comboPeaks": [r["comboPeak"] for r in cr],
                "n3Triggers": [r["totalN3Triggers"] for r in cr],
            }
        aggregate[str(entry_combo)] = {
            "cases": len(rr),
            "through49": sum(1 for r in rr if r["settledThroughStage49"]),
            "failureStages": dict(sorted(Counter(str(r["failureStage"]) for r in rr if r["failureStage"] is not None).items())),
            "perClass": per_class,
        }

    output = {
        "version": "p5-p6-entry-combo40-sensitivity-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "question": "Can a strong carried Stage46 entry combo plausibly explain the class-skewed skilled failures seen after persistent-state fidelity was restored?",
        "entryCharge": ENTRY_CHARGE,
        "entryCombos": list(ENTRY_COMBOS),
        "combo40Interpretation": "UPPER_BOUND_SENSITIVITY_ONLY_NOT_A_STAGE46_ENTRY_CANDIDATE_OR_DISTRIBUTION",
        "seeds": bridge.SEEDS,
        "rows": rows,
        "aggregate": aggregate,
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    OUT.write_text(text + "\n", encoding="utf-8")
    print(text)
    print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
