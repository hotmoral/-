from __future__ import annotations

import p1_fr3_feline_core_topology_v4 as v4
import run_p1_fr3_feline_core_topology as base


base.PROTOTYPE_VERSION = v4.PROTOTYPE_VERSION
base.build_probe = v4.build_probe
base.result_dict = v4.result_dict
base.limb_crossing_count = v4.limb_crossing_count


if __name__ == "__main__":
    base.main()
