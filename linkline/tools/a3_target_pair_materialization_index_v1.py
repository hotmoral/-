#!/usr/bin/env python3
"""Encode the already-public v3 selection as compact deterministic source indexes.

This is a transport-only public-safe artifact. It contains no puzzle geometry,
private isolation data, target coordinates, or human/self-test data.
"""
from __future__ import annotations

import argparse
import base64
from hashlib import sha256
import json
from pathlib import Path
import struct

import tools.a3_target_pair_selection_plan_v1 as v1

SCHEMA = "LINKLINE_A3_TARGET_PAIR_MATERIALIZATION_INDEX_V1"
SELECTION_SCHEMA = "LINKLINE_A3_TARGET_PAIR_1300_PUBLIC_SELECTION_PLAN_V3"
SELECTION_FP = "1fc7dd15893a113935b0b1b2f5ca636e22669d783e887f90e56203275d3c3131"
RECORD = ">BBIB"  # n, chainLength, deterministic source index, orientation(255=N5/N6)
PART_SIZE = 325


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan.get("schema") != SELECTION_SCHEMA:
        raise SystemExit("unexpected selection schema")
    if plan.get("selectionFingerprint") != SELECTION_FP:
        raise SystemExit("selection fingerprint mismatch")
    rows = plan.get("order", [])
    if len(rows) != 1300:
        raise SystemExit("selection row count mismatch")

    rank_cache = {}
    encoded = bytearray()
    for expected_stage, row in enumerate(rows, start=1):
        if row.get("stage") != expected_stage:
            raise SystemExit("non-contiguous stage order")
        n = int(row["n"])
        length = int(row["chainLength"])
        if n in (3, 4):
            source_index = row.get("sourceUniverseIndex")
            orientation = row.get("orientationTransform")
            if type(source_index) is not int or source_index < 0:
                raise SystemExit(f"bad legacy source index at stage {expected_stage}")
            if type(orientation) is not int or not 0 <= orientation < 8:
                raise SystemExit(f"bad legacy orientation at stage {expected_stage}")
        else:
            key = (n, length)
            if key not in rank_cache:
                geometry = v1.reconstruct_geometry_index(
                    n, length, v1.STATE_COUNTS[n]
                )
                rank_cache[key] = {
                    identifier: rank
                    for rank, identifier in enumerate(sorted(geometry))
                }
            try:
                source_index = rank_cache[key][row["id"]]
            except KeyError as exc:
                raise SystemExit(
                    f"unreproducible expanded source at stage {expected_stage}"
                ) from exc
            orientation = 255
        encoded.extend(struct.pack(RECORD, n, length, source_index, orientation))

    record_size = struct.calcsize(RECORD)
    if len(encoded) != 1300 * record_size:
        raise SystemExit("encoded byte count mismatch")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    for part_number, start_stage in enumerate(range(1, 1301, PART_SIZE), start=1):
        end_stage = min(1300, start_stage + PART_SIZE - 1)
        start_byte = (start_stage - 1) * record_size
        end_byte = end_stage * record_size
        raw = bytes(encoded[start_byte:end_byte])
        name = f"part_{part_number:02d}_{start_stage:04d}_{end_stage:04d}.b64"
        (args.output_dir / name).write_text(base64.b64encode(raw).decode("ascii") + "\n", encoding="ascii")
        parts.append({
            "path": name,
            "startStage": start_stage,
            "endStage": end_stage,
            "recordCount": end_stage - start_stage + 1,
            "sha256": sha256(raw).hexdigest(),
        })

    manifest = {
        "schema": SCHEMA,
        "version": "1.0.0",
        "sourceSelectionFingerprint": SELECTION_FP,
        "recordStruct": RECORD,
        "recordSize": record_size,
        "recordCount": 1300,
        "expandedIndexMeaning": "rank in sorted deterministic reconstruct_geometry_index IDs for the row N/L",
        "legacyIndexMeaning": "sourceUniverseIndex from the already-public oriented v3 selection",
        "orientationSentinelExpanded": 255,
        "parts": parts,
        "privacy": {
            "containsPuzzleGeometry": False,
            "containsTargetCoordinates": False,
            "containsPrivateIsolationIds": False,
            "containsHumanOrSelfTestData": False,
        },
    }
    manifest["payloadSha256"] = sha256(bytes(encoded)).hexdigest()
    (args.output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"status":"PASS","recordCount":1300,"payloadSha256":manifest["payloadSha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
