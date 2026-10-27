#!/usr/bin/env python3
"""Combine public-safe 96-state N5 acquisition shards and measure exact-pair capacity.

The shard generator is the already-approved a3_target_pair_acquisition_v1 runner.
This combiner emits de-identified candidate rows and aggregate capacity only. It
never emits initial paths, target coordinates, or per-pair keys.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import tools.a3_final_candidate_pool_public as base
import tools.a3_target_pair_acquisition_v1 as acquisition

SCHEMA = "LINKLINE_A3_TARGET_PAIR_N5_EXPANSION_PUBLIC_POOL"
VERSION = "1.0.0"
STATE_COUNT = 96
DOMAINS = tuple((5, length) for length in range(6, 11))
TARGET = 514
PAIR_CAP = 2


def fp(value) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def geometry_by_id(n: int, length: int):
    pool, _ = base.sample_domain(n, length)
    states = base.select_states(n, length, pool, count=STATE_COUNT)
    result = {}
    for initial in states:
        for _span, _placement, targets in base.goal_strata(n, length, initial):
            identifier = base.identity(n, length, initial, targets)
            result.setdefault(identifier, tuple(sorted(targets)))
    return result


def combine(input_dir: Path, output_dir: Path):
    paths = sorted(input_dir.rglob("N5L*.candidates.json"))
    if len(paths) != len(DOMAINS):
        raise RuntimeError(f"expected {len(DOMAINS)} N5 shards, got {len(paths)}")

    rows = []
    seen_domains = set()
    domain_summaries = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema") != acquisition.SCHEMA:
            raise RuntimeError(f"unexpected shard schema:{path}")
        if payload.get("version") != acquisition.VERSION:
            raise RuntimeError(f"unexpected shard version:{path}")
        if payload.get("mechanicBaseline") != base.MECHANIC_BASELINE:
            raise RuntimeError(f"mechanic baseline mismatch:{path}")
        contract = payload.get("samplingContract", {})
        if contract.get("stateCount") != STATE_COUNT:
            raise RuntimeError(f"state-count mismatch:{path}")
        domain = payload.get("domain", {})
        key = (domain.get("n"), domain.get("chainLength"))
        if key not in DOMAINS or key in seen_domains:
            raise RuntimeError(f"unexpected/duplicate domain:{key}")
        seen_domains.add(key)
        shard_rows = payload.get("rows")
        if not isinstance(shard_rows, list):
            raise RuntimeError(f"rows missing:{path}")
        rows.extend(shard_rows)
        domain_summaries.append(
            {
                "n": key[0],
                "chainLength": key[1],
                "rowCount": len(shard_rows),
                "identityFingerprint": fp([row["id"] for row in shard_rows]),
            }
        )

    if seen_domains != set(DOMAINS):
        raise RuntimeError("N5 domain closure mismatch")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("cross-domain identity duplicate")
    rows.sort(key=lambda row: (row["chainLength"], row["id"]))

    pair_counts = Counter()
    by_nl = {}
    rows_by_domain = {key: [] for key in DOMAINS}
    for row in rows:
        rows_by_domain[(row["n"], row["chainLength"])].append(row)

    for n, length in DOMAINS:
        geometry = geometry_by_id(n, length)
        local = Counter()
        for row in rows_by_domain[(n, length)]:
            targets = geometry.get(row["id"])
            if targets is None:
                raise RuntimeError(f"unreproducible public id:{row['id']}")
            pair_counts[targets] += 1
            local[targets] += 1
        by_nl[f"N{n}L{length}"] = {
            "rowCount": len(rows_by_domain[(n, length)]),
            "exactPairCount": len(local),
            "pairsWithAtLeastTwoWithinNL": sum(v >= 2 for v in local.values()),
            "maxCandidatesForOnePairWithinNL": max(local.values(), default=0),
        }

    counts = list(pair_counts.values())
    selectable = sum(min(value, PAIR_CAP) for value in counts)
    pair_summary = {
        "rowCount": len(rows),
        "exactPairCount": len(counts),
        "pairsWithAtLeastTwo": sum(value >= 2 for value in counts),
        "maxCandidatesForOnePair": max(counts, default=0),
        "selectableCapacityUnderCap": selectable,
        "provisionalTarget": TARGET,
        "rawMarginOverProvisionalTarget": selectable - TARGET,
    }

    pool = {
        "schema": SCHEMA,
        "version": VERSION,
        "mechanicBaseline": base.MECHANIC_BASELINE,
        "samplingContract": {
            "grammar": base.SAMPLING_GRAMMAR,
            "stateCount": STATE_COUNT,
            "goalSelection": "UNCHANGED_A1_W3_GOAL_STRATA_ONE_PER_BUCKET",
        },
        "privacy": {
            "containsPuzzleGeometry": False,
            "containsTargetPairKeys": False,
            "containsHumanOrSelfTestExport": False,
            "containsIsolationSourceList": False,
            "containsSecrets": False,
            "requiresPrivateCanonicalIsolation": True,
        },
        "domains": sorted(domain_summaries, key=lambda item: item["chainLength"]),
        "rows": rows,
    }
    summary = {
        "schema": f"{SCHEMA}_SUMMARY",
        "version": VERSION,
        "stateCount": STATE_COUNT,
        "identityFingerprint": fp([row["id"] for row in rows]),
        "byN": {"5": pair_summary},
        "byNL": by_nl,
        "boundaries": {
            "privateIsolationApplied": False,
            "finalSelectionPerformed": False,
            "productionCatalogModified": False,
        },
    }
    summary["summaryFingerprint"] = fp(summary)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "candidate_pool.json").write_text(
        json.dumps(pool, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(pair_summary, sort_keys=True), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    combine(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
