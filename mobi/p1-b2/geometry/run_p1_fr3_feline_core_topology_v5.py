from __future__ import annotations

import p1_fr3_feline_core_topology_v5 as v5
import run_p1_fr3_feline_core_topology as base


base.PROTOTYPE_VERSION = v5.PROTOTYPE_VERSION
base.build_probe = v5.build_probe
base.result_dict = v5.result_dict
base.limb_crossing_count = v5.limb_crossing_count


if __name__ == "__main__":
    base.main()
