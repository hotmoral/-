from __future__ import annotations

import p1_fr2_layered_view_prototype_v3 as v3
import run_p1_fr2_perceptual_revision as v1_runner


RUN_VERSION = "P1_FR2_PERCEPTUAL_REVISION_EVIDENCE_V3_DORSAL_SAFE"

v1_runner.RUN_VERSION = RUN_VERSION
v1_runner.PROTOTYPE_VERSION = v3.PROTOTYPE_VERSION
v1_runner.build_probe = v3.build_probe
v1_runner.limb_crossing_count = v3.limb_crossing_count
v1_runner.result_dict = v3.result_dict


if __name__ == "__main__":
    v1_runner.main()
