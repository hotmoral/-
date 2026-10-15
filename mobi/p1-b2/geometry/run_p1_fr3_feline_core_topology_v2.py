from __future__ import annotations

import p1_fr3_feline_core_topology_v2 as v2
import run_p1_fr3_feline_core_topology as base


base.PROTOTYPE_VERSION = v2.PROTOTYPE_VERSION
base.build_probe = v2.build_probe
base.result_dict = v2.result_dict
base.limb_crossing_count = v2.limb_crossing_count


if __name__ == "__main__":
    base.main()
