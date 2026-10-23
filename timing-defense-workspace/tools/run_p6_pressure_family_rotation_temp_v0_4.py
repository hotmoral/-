#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path

import run_p6_pressure_family_rotation_temp_v0_1 as p

OUT = Path("p6_pressure_family_rotation_temp_v0_4.json")

# Baseline already has 20-seed authority from P6-S1. Expand only the two informative
# alternate families to avoid paying again for a closed baseline.
p.SEEDS = tuple(range(1, 21))
p.FAMILIES = (
    "DURABLE_DISTRIBUTED",
    "CHARGER_CONTROL_SCREENED",
)
p.PACKETS["CHARGER_CONTROL_SCREENED"] = [
    (0.00, "BRUTE", 0),
    (0.70, "SHIELD", -2),
    (1.40, "BRUTE", 2),
    (2.10, "CHARGER", -1),
    (2.80, "CHARGER", 1),
]
p.REPEATS["CHARGER_CONTROL_SCREENED"] = {
    46: (16, 3.55),
    47: (18, 3.15),
}
p.OUT = Path("_p6_pressure_family_rotation_temp_v0_4_inherited.json")

with contextlib.redirect_stdout(io.StringIO()):
    p.main()

obj = json.loads(p.OUT.read_text(encoding="utf-8"))
obj["version"] = "p6-pressure-family-rotation-temp-v0.4-full20"
obj["status"] = "DIAGNOSTIC_20SEED_PRESSURE_FAMILY_ROTATION_NO_CONTENT_ADOPTION_NO_NUMERICAL_FREEZE_NO_PRODUCTION_AUTHORITY"
obj["basis"]["baselineReference"] = (
    "Use P6-S1 BALANCED 20-seed baseline rather than rerunning it: Archer19 Mage19 Rogue9 Knight7 Tank2 through47."
)
obj["basis"]["controlFamilyRevision"] = (
    "Screened CHARGER family only; no SIEGER. Normal-right-edge entry and current class/monster/player-power semantics preserved."
)
text = json.dumps(obj, indent=2, sort_keys=True)
OUT.write_text(text + "\n", encoding="utf-8")

agg = obj["aggregate"]
compact = {
    "rankOrders": agg["rankOrders"],
    "classes": {
        family: {
            cls: {
                "through47": agg["families"][family][cls]["through47"],
                "cases": agg["families"][family][cls]["cases"],
                "allPerfect": f'{agg["families"][family][cls]["allPerfectThrough47"]}/{agg["families"][family][cls]["allPerfectCases"]}',
                "finalWallMedian": agg["families"][family][cls]["finalWall"]["median"],
                "judgmentsMean": agg["families"][family][cls]["totalJudgments"]["mean"],
                "pxpRateMean": agg["families"][family][cls]["totalPxpRate"]["mean"],
                "s46WallLossMean": agg["families"][family][cls]["stage46"]["wallLoss"]["mean"],
                "s46MaxActiveMean": agg["families"][family][cls]["stage46"]["maxActive"]["mean"],
                "s46PushMean": agg["families"][family][cls]["stage46"]["pushDistance"]["mean"],
                "s46ChargerInterruptMean": agg["families"][family][cls]["stage46"]["chargerInterrupts"]["mean"],
            }
            for cls in p.bridge.CLASSES
        }
        for family in p.FAMILIES
    },
}
print("P6_PRESSURE_FULL20=" + json.dumps(compact, sort_keys=True))
print("P6_PRESSURE_BUDGETS_FULL20=" + json.dumps(obj["budgets"], sort_keys=True))
print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())
