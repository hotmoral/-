#!/usr/bin/env python3
"""Aggregate exact target-pair capacity without emitting target coordinates.

This reads the already-materialized target-pair acquisition pool and reproduces
its deterministic geometry in memory only. Output contains aggregate counts and
capacity margins, never initial paths, target coordinates, or per-pair keys.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path

import tools.a3_final_candidate_pool_public as base
import tools.a3_target_pair_acquisition_v1 as acquisition

POOL = Path("public_output/a3_target_pair_acquisition_v1/candidate_pool.json")
OUTPUT = Path("public_output/a3_target_pair_acquisition_v1/pair_capacity_summary.json")
TARGETS = {5: 514, 6: 630}
PAIR_CAP = {5: 2, 6: 2}


def geometry_by_id(n: int, length: int, state_count: int):
    pool, _ = base.sample_domain(n, length)
    states = base.select_states(n, length, pool, count=state_count)
    result = {}
    for initial in states:
        for _span, _placement, targets in base.goal_strata(n, length, initial):
            identifier = base.identity(n, length, initial, targets)
            result.setdefault(identifier, tuple(sorted(targets)))
    return result


def main():
    payload = json.loads(POOL.read_text(encoding="utf-8"))
    if payload.get("schema") != f"{acquisition.SCHEMA}_POOL":
        raise RuntimeError("unexpected acquisition pool schema")
    if payload.get("version") != acquisition.VERSION:
        raise RuntimeError("unexpected acquisition pool version")
    state_count = payload["samplingContract"]["stateCount"]
    if state_count != acquisition.DEFAULT_STATE_COUNT:
        raise RuntimeError("state-count mismatch")

    rows_by_domain = defaultdict(list)
    for row in payload["rows"]:
        rows_by_domain[(row["n"], row["chainLength"])].append(row)

    pair_counts_by_n = {5: Counter(), 6: Counter()}
    nl_report = {}
    for n, length in acquisition.DOMAINS:
        geometry = geometry_by_id(n, length, state_count)
        pair_counts = Counter()
        rows = rows_by_domain[(n, length)]
        for row in rows:
            targets = geometry.get(row["id"])
            if targets is None:
                raise RuntimeError(f"unreproducible public id:{row['id']}")
            pair_counts[targets] += 1
            pair_counts_by_n[n][targets] += 1
        nl_report[f"N{n}L{length}"] = {
            "rowCount": len(rows),
            "exactPairCount": len(pair_counts),
            "pairsWithAtLeastTwoWithinNL": sum(v >= 2 for v in pair_counts.values()),
            "maxCandidatesForOnePairWithinNL": max(pair_counts.values(), default=0),
        }

    by_n = {}
    for n in (5, 6):
        counts = list(pair_counts_by_n[n].values())
        selectable = sum(min(value, PAIR_CAP[n]) for value in counts)
        by_n[str(n)] = {
            "rowCount": sum(counts),
            "exactPairCount": len(counts),
            "pairsWithAtLeastTwo": sum(value >= 2 for value in counts),
            "maxCandidatesForOnePair": max(counts, default=0),
            "selectableCapacityUnderCap": selectable,
            "provisionalTarget": TARGETS[n],
            "rawMarginOverProvisionalTarget": selectable - TARGETS[n],
        }

    report = {
        "schema": "LINKLINE_A3_TARGET_PAIR_PUBLIC_CAPACITY_SUMMARY",
        "version": "1.0.0",
        "stateCount": state_count,
        "privacy": {
            "containsPuzzleGeometry": False,
            "containsTargetPairKeys": False,
            "containsPrivateIsolationIds": False,
        },
        "byN": by_n,
        "byNL": nl_report,
        "boundary": {
            "privateIsolationApplied": False,
            "finalSelectionPerformed": False,
            "productionCatalogModified": False,
        },
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report["byN"], sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
