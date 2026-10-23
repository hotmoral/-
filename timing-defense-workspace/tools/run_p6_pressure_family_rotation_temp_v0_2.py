#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path

import run_p6_pressure_family_rotation_temp_v0_1 as p

OUT = Path("p6_pressure_family_rotation_temp_v0_2.json")

# Keep the informative baseline and durable-distributed family unchanged.
# Refine only the control/objective family so stateful roles have a durable screen,
# fewer concurrent bodies, and repeated SIEGER/CHARGER activation opportunities.
p.FAMILIES = (
    "BASELINE_DENSE_ALIGNED",
    "DURABLE_DISTRIBUTED",
    "CONTROL_OBJECTIVE_SCREENED",
)
p.PACKETS["CONTROL_OBJECTIVE_SCREENED"] = [
    (0.00, "BRUTE", 0),
    (0.70, "SHIELD", -2),
    (1.40, "BRUTE", 2),
    (2.10, "SIEGER", -1),
    (2.80, "CHARGER", 1),
    (3.50, "SIEGER", 0),
]
p.REPEATS["CONTROL_OBJECTIVE_SCREENED"] = {
    46: (12, 4.40),
    47: (14, 3.85),
}

# Write the inherited implementation to a throwaway path, then relabel the result
# so the evidence file truthfully records the refined family definition.
p.OUT = Path("_p6_pressure_family_rotation_temp_v0_2_inherited.json")

with contextlib.redirect_stdout(io.StringIO()):
    p.main()

obj = json.loads(p.OUT.read_text(encoding="utf-8"))
obj["version"] = "p6-pressure-family-rotation-temp-v0.2-preflight"
obj["status"] = "DIAGNOSTIC_ONLY_REFINED_CONTROL_FAMILY_NO_CONTENT_ADOPTION_NO_NUMERICAL_FREEZE_NO_PRODUCTION_AUTHORITY"
obj["basis"]["controlFamilyRevision"] = (
    "v0.2 keeps normal-right-edge entry and current monster stats, reduces concurrent body count, "
    "adds durable screening, and creates repeated CHARGER/SIEGER activation opportunities; it is not production authoring."
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
                "finalWallMedian": agg["families"][family][cls]["finalWall"]["median"],
                "s46WallLossMean": agg["families"][family][cls]["stage46"]["wallLoss"]["mean"],
                "s46PushMean": agg["families"][family][cls]["stage46"]["pushDistance"]["mean"],
                "s46ChargerInterruptMean": agg["families"][family][cls]["stage46"]["chargerInterrupts"]["mean"],
                "s46SiegerRepositionMean": agg["families"][family][cls]["stage46"]["siegerRepositions"]["mean"],
                "s46SiegerShotsMean": agg["families"][family][cls]["stage46"]["siegerShots"]["mean"],
            }
            for cls in p.bridge.CLASSES
        }
        for family in p.FAMILIES
    },
}
print("P6_PRESSURE_PREFLIGHT_V02=" + json.dumps(compact, sort_keys=True))
print("P6_PRESSURE_BUDGETS_V02=" + json.dumps(obj["budgets"], sort_keys=True))
print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())
