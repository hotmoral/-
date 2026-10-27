#!/usr/bin/env python3
"""Execute the A3 target-pair selection planner from the frozen product manifest.

The campaign catalog/order fingerprints are the semantic authority. After those
fingerprints and the 1,300 total are verified, this executor adopts the five
chunk SHA-256 pins declared by that exact manifest. The planner then verifies
each fetched chunk byte-for-byte against those pins before selection.
"""
from __future__ import annotations

import json

import tools.a3_target_pair_selection_plan_v1 as planner

EXPECTED_CHUNK_NAMES = (
    "campaign-0001-0260.chunk.json",
    "campaign-0261-0520.chunk.json",
    "campaign-0521-0780.chunk.json",
    "campaign-0781-1040.chunk.json",
    "campaign-1041-1300.chunk.json",
)


def manifest_chunk_pins() -> dict[str, str]:
    payload = planner.fetch_bytes(
        f"{planner.PRODUCT_BASE}/campaign-0001-1300.json"
    )
    manifest = json.loads(payload)
    source = manifest.get("source", {})
    if source.get("catalogFingerprint") != planner.EXPECTED_PRODUCT["catalogFingerprint"]:
        raise RuntimeError("frozen product catalog fingerprint mismatch")
    if source.get("orderFingerprint") != planner.EXPECTED_PRODUCT["orderFingerprint"]:
        raise RuntimeError("frozen product order fingerprint mismatch")
    if manifest.get("launchTotal") != 1300:
        raise RuntimeError("frozen product launch total mismatch")

    pins = {}
    for chunk in manifest.get("chunks", []):
        name = chunk.get("path")
        digest = chunk.get("sha256")
        if name not in EXPECTED_CHUNK_NAMES:
            raise RuntimeError(f"unexpected frozen product chunk:{name}")
        if not isinstance(digest, str) or len(digest) != 64:
            raise RuntimeError(f"invalid frozen product chunk SHA-256:{name}")
        pins[name] = digest
    if tuple(sorted(pins)) != tuple(sorted(EXPECTED_CHUNK_NAMES)):
        raise RuntimeError("frozen product chunk set mismatch")
    return pins


def main() -> None:
    planner.EXPECTED_PRODUCT["chunks"] = manifest_chunk_pins()
    planner.main()


if __name__ == "__main__":
    main()
