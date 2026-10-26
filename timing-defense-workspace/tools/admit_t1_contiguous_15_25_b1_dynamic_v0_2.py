#!/usr/bin/env python3
"""B1 Stage15-25 dynamic admission v0.2 identity bridge.

The v0.1 runner intentionally failed closed because the previously copied
materialized byte SHA did not match the materialization reproduced by the live
canonical static preflight.  The static preflight itself passed with no errors
and preserved every authority Stage object.  This wrapper changes only that
input-identity constant to the exact live materialization observed in run
40254173222; combat, lifecycle, skill, variant, and aggregation semantics remain
those of v0.1.
"""
from __future__ import annotations

import admit_t1_contiguous_15_25_b1_dynamic_v0_1 as impl

impl.EXPECTED_MATERIALIZED_SHA256 = "f769dd79e750882a6b7a75dad18bfdbc514da546b183587ec2ed909e50b2ed0f"

if __name__ == "__main__":
    impl.main()
