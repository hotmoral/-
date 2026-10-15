from __future__ import annotations

import p1_fr3_feline_core_topology_v3 as v3
import run_p1_fr3_feline_core_topology as base


base.PROTOTYPE_VERSION = v3.PROTOTYPE_VERSION
base.build_probe = v3.build_probe
base.result_dict = v3.result_dict
base.limb_crossing_count = v3.limb_crossing_count


if __name__ == "__main__":
    base.main()
