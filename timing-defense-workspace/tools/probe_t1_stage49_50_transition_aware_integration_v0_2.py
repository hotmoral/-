#!/usr/bin/env python3
"""T1 Stage49-50 transition-aware integrated diagnostic v0.2.

Refinement over v0.1:
- Stage49 ends on LINE instead of placing CLUSTER after LINE.
- Stage49 and Stage50 now share the same four-grammar learning order:
  DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE
- Stage50 alone adds LINE_REPRISE as the final synthesis close.

Reason: v0.1 isolated a single Archer seed where Lv31 cleared LINE earlier but,
because CLUSTER followed it, changed kill chronology and delayed the subsequent
CLUSTER. This refinement changes only grammar order; no scalar/morphology/rule
is changed relative to the same candidate ID.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import probe_t1_stage49_50_transition_aware_integration_v0_1 as base

ORDER_V02 = {
    49: ["DURABLE_SCATTER", "FRONTLINE", "CLUSTER", "LINE"],
    50: ["DURABLE_SCATTER", "FRONTLINE", "CLUSTER", "LINE", "LINE_REPRISE"],
}


def main():
    base.ORDER = ORDER_V02
    base.main()

    # v0.1 owns the full tested implementation; amend only evidence metadata so
    # the refinement remains explicit and machine-readable.
    if "--json-out" not in sys.argv:
        return
    out_path = Path(sys.argv[sys.argv.index("--json-out") + 1])
    doc = json.loads(out_path.read_text(encoding="utf-8"))
    doc["version"] = "t1-stage49-50-transition-aware-integration-probe-v0.2"
    doc["status"] = "DIAGNOSTIC_ORDER_REFINEMENT_NO_AUTHORING_OR_SCALAR_ADOPTION"
    doc["refinementFromV01"] = {
        "stage49OldOrder": ["DURABLE_SCATTER", "FRONTLINE", "LINE", "CLUSTER"],
        "stage49NewOrder": ORDER_V02[49],
        "stage50OrderUnchanged": ORDER_V02[50],
        "reason": "REMOVE_POST_LINE_CLUSTER_CHRONOLOGY_SIDE_EFFECT_WITHOUT_SCALAR_CHANGE",
    }
    out_path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
