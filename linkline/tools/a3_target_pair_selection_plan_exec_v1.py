#!/usr/bin/env python3
"""Execute the A3 target-pair selection planner with the exact frozen chunk pin.

The initial planner commit contains a typo in the 0261-0520 SHA literal. This
thin executor corrects only that immutable source pin before entering planner
main(); selection logic and output contracts remain unchanged.
"""
from __future__ import annotations

import tools.a3_target_pair_selection_plan_v1 as planner

CORRECT_0261_0520_SHA256 = (
    "ac7ab37884b87176682da514407ee10d817bb84ff5a91b8ed98a90a8897efe84"
)


def main() -> None:
    planner.EXPECTED_PRODUCT["chunks"][
        "campaign-0261-0520.chunk.json"
    ] = CORRECT_0261_0520_SHA256
    if len(CORRECT_0261_0520_SHA256) != 64:
        raise RuntimeError("frozen chunk SHA-256 pin must be 64 hex characters")
    planner.main()


if __name__ == "__main__":
    main()
