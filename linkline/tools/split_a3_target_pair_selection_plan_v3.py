#!/usr/bin/env python3
"""Split/index the already-public A3 target-pair v3 plan.

Transport/readability transform only. It adds no private data and does not alter
selection semantics.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def clean(value) -> str:
    if value is None:
        return ""
    return str(value).replace("\t", " ").replace("\n", " ")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--chunk-size", type=int, default=50)
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan.get("schema") != "LINKLINE_A3_TARGET_PAIR_1300_PUBLIC_SELECTION_PLAN_V3":
        raise SystemExit("unexpected plan schema")
    order = plan.get("order", [])
    reservoir = plan.get("repairReservoir", [])
    if len(order) != 1300:
        raise SystemExit(f"unexpected order length:{len(order)}")

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "LINKLINE_A3_TARGET_PAIR_1300_PUBLIC_SELECTION_PLAN_V3_CHUNKS",
        "sourceSelectionFingerprint": plan.get("selectionFingerprint"),
        "sourceSummaryFingerprint": plan.get("summaryFingerprint"),
        "orderCount": len(order),
        "repairReservoirCount": len(reservoir),
        "chunkSize": args.chunk_size,
        "orderChunks": [],
        "repairChunks": [],
        "compactSelected": "selected.tsv",
        "compactRepair": "repair.tsv",
        "selectedNibbleDir": "selected_nibble",
        "repairIdNibbleDir": "repair_id_nibble",
    }

    for start in range(0, len(order), args.chunk_size):
        rows = order[start:start + args.chunk_size]
        name = f"order_{start + 1:04d}_{start + len(rows):04d}.json"
        write_json(out / name, rows)
        manifest["orderChunks"].append(name)

    for start in range(0, len(reservoir), args.chunk_size):
        rows = reservoir[start:start + args.chunk_size]
        name = f"repair_{start + 1:04d}_{start + len(rows):04d}.json"
        write_json(out / name, rows)
        manifest["repairChunks"].append(name)

    selected_header = ["stage", "id", "n", "chainLength", "orientationTransform", "useIndex", "groupToken", "difficulty"]
    selected_lines = ["\t".join(selected_header)]
    for row in order:
        selected_lines.append("\t".join(clean(row.get(key)) for key in selected_header))
    (out / "selected.tsv").write_text("\n".join(selected_lines) + "\n", encoding="utf-8")

    repair_header = ["id", "n", "chainLength", "orientationTransform", "groupToken", "purpose", "replacementForId", "difficulty"]
    repair_lines = ["\t".join(repair_header)]
    for row in reservoir:
        repair_lines.append("\t".join(clean(row.get(key)) for key in repair_header))
    (out / "repair.tsv").write_text("\n".join(repair_lines) + "\n", encoding="utf-8")

    selected_nibbles = defaultdict(list)
    for row in order:
        selected_nibbles[row["id"][0]].append(row)
    repair_nibbles = defaultdict(list)
    for row in reservoir:
        repair_nibbles[row["id"][0]].append(row)
    for nibble in "0123456789abcdef":
        write_json(out / "selected_nibble" / f"{nibble}.json", selected_nibbles[nibble])
        write_json(out / "repair_id_nibble" / f"{nibble}.json", repair_nibbles[nibble])

    write_json(out / "manifest.json", manifest)
    print(json.dumps({
        "status": "PASS",
        "orderCount": len(order),
        "repairReservoirCount": len(reservoir),
        "orderChunkCount": len(manifest["orderChunks"]),
        "repairChunkCount": len(manifest["repairChunks"]),
        "selectedNibbleCount": sum(len(v) for v in selected_nibbles.values()),
        "repairNibbleCount": sum(len(v) for v in repair_nibbles.values()),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
