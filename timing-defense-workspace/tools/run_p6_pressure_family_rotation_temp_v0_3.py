#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path

import run_p6_pressure_family_rotation_temp_v0_1 as p

OUT = Path("p6_pressure_family_rotation_temp_v0_3.json")

p.FAMILIES = (
    "BASELINE_DENSE_ALIGNED",
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
p.OUT = Path("_p6_pressure_family_rotation_temp_v0_3_inherited.json")

with contextlib.redirect_stdout(io.StringIO()):
    p.main()

obj = json.loads(p.OUT.read_text(encoding="utf-8"))
obj["version"] = "p6-pressure-family-rotation-temp-v0.3-preflight"
obj["status"] = "DIAGNOSTIC_ONLY_CHARGER_CONTROL_ISOLATION_NO_CONTENT_ADOPTION_NO_NUMERICAL_FREEZE_NO_PRODUCTION_AUTHORITY"
obj["basis"]["controlFamilyRevision"] = (
    "v0.3 removes SIEGER entirely and isolates screened CHARGER control value. "
    "Normal-right-edge entry, monster stats, class packages, mastery and shop surface remain unchanged."
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
                "allPerfect": f'{agg["families"][family][cls]["allPerfectThrough47"]}/{agg["families"][family][cls]["allPerfectCases"]}',
                "finalWallMedian": agg["families"][family][cls]["finalWall"]["median"],
                "s46WallLossMean": agg["families"][family][cls]["stage46"]["wallLoss"]["mean"],
                "s46PushMean": agg["families"][family][cls]["stage46"]["pushDistance"]["mean"],
                "s46ChargerInterruptMean": agg["families"][family][cls]["stage46"]["chargerInterrupts"]["mean"],
            }
            for cls in p.bridge.CLASSES
        }
        for family in p.FAMILIES
    },
}
print("P6_PRESSURE_PREFLIGHT_V03=" + json.dumps(compact, sort_keys=True))
print("P6_PRESSURE_BUDGETS_V03=" + json.dumps(obj["budgets"], sort_keys=True))
print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())
