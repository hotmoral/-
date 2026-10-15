from __future__ import annotations

import p1_fr2_layered_view_prototype_v2 as v2
import run_p1_fr2_perceptual_revision as v1_runner


RUN_VERSION = "P1_FR2_PERCEPTUAL_REVISION_EVIDENCE_V2_PROFILE_SAFE"

# Reuse the frozen V1 evidence machinery, but bind its runtime globals to the
# V2 base-shape refinement. This preserves comparison layout and matrix logic.
v1_runner.RUN_VERSION = RUN_VERSION
v1_runner.PROTOTYPE_VERSION = v2.PROTOTYPE_VERSION
v1_runner.build_probe = v2.build_probe
v1_runner.limb_crossing_count = v2.limb_crossing_count
v1_runner.result_dict = v2.result_dict


if __name__ == "__main__":
    v1_runner.main()
