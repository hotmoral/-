#!/usr/bin/env python3
"""Public-safe deterministic N5/N6 acquisition for A3 target-pair diversity.

This expands only the number of sampled initial states per accepted N/L domain.
It preserves the public A1_SAMPLING_V1 path sampler, target strata, solver budget,
mechanic baseline, structural profiler, and D4 research identity contract.

Outputs deliberately contain no puzzle geometry, private isolation lists, or
human/self-test exports.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import tools.a3_final_candidate_pool_public as base

SCHEMA = "LINKLINE_A3_TARGET_PAIR_ACQUISITION_PUBLIC"
VERSION = "1.0.0"
DEFAULT_STATE_COUNT = 48
DOMAINS = tuple(
    [(5, length) for length in range(6, 11)]
    + [(6, length) for length in range(8, 16)]
)


def fp(value) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def reconstruct_domain(n: int, length: int, state_count: int):
    pool, sample_diag = base.sample_domain(n, length)
    states = base.select_states(n, length, pool, count=state_count)

    status_counts = Counter()
    by_id = {}
    goal_record_count = 0
    for state_rank, initial in enumerate(states):
        for span, placement, targets in base.goal_strata(n, length, initial):
            goal_record_count += 1
            instance = base.PuzzleInstanceV1(
                base.BoardSpecV1(n),
                base.ChainSpecV1(length),
                base.GoalSpecV1(*targets),
                base.ChainStateV1(initial),
            )
            run = base.solve_puzzle(
                instance, base.SearchBudgetV1(base.A1_SAMPLE_BUDGET)
            )
            status = run.result.status.value
            status_counts[status] += 1
            if run.result.status is not base.SolveStatusV1.SOLVED:
                continue

            identifier = base.identity(n, length, initial, targets)
            if identifier not in by_id:
                by_id[identifier] = {
                    "initial": initial,
                    "targets": targets,
                    "distance": run.result.shortest_distance,
                    "stateRank": state_rank,
                    "span": span,
                    "placement": placement,
                }

    rows = []
    exact_failures = 0
    for source_rank, identifier in enumerate(sorted(by_id)):
        item = by_id[identifier]
        values = base.profile_identity(
            n, length, item["initial"], item["targets"]
        )
        if values is None:
            exact_failures += 1
            continue
        if values["shortestDistance"] != item["distance"]:
            raise RuntimeError(
                f"solver/profile distance mismatch N{n}L{length}:{identifier}"
            )
        rows.append(
            base.candidate_row(
                identifier,
                n,
                length,
                values,
                {
                    "sourceKind": "A1_W3_PUBLIC_STATE_EXPANSION_V1",
                    "sourceRank": source_rank,
                    "stateRank": item["stateRank"],
                    "goalSpan": item["span"],
                    "goalPlacement": item["placement"],
                    "stateCountContract": state_count,
                },
            )
        )

    diag = {
        **sample_diag,
        "n": n,
        "chainLength": length,
        "stateCountRequested": state_count,
        "selectedStateCount": len(states),
        "goalRecordCount": goal_record_count,
        "goalStatusCounts": dict(sorted(status_counts.items())),
        "solvedUniqueIdentityCount": len(by_id),
        "exactProfileRows": len(rows),
        "exactProfileFailures": exact_failures,
        "identityFingerprint": fp([row["id"] for row in rows]),
    }
    return rows, diag


def write_shard(n: int, length: int, state_count: int, output_dir: Path):
    if (n, length) not in DOMAINS:
        raise RuntimeError(f"unsupported acquisition domain N{n}L{length}")
    if not 1 <= state_count <= 256:
        raise RuntimeError("state-count must be in [1,256]")

    rows, diag = reconstruct_domain(n, length, state_count)
    stem = f"N{n}L{length}"
    payload = {
        "schema": SCHEMA,
        "version": VERSION,
        "mechanicBaseline": base.MECHANIC_BASELINE,
        "samplingContract": {
            "grammar": base.SAMPLING_GRAMMAR,
            "constructiveRequested": base.CONSTRUCTIVE_REQUESTED,
            "dynamicRequested": base.DYNAMIC_REQUESTED,
            "maxAttempts": base.SAMPLER_ATTEMPTS,
            "constructiveNodeCap": base.CONSTRUCTIVE_NODE_CAP,
            "sampleExpansionBudget": base.A1_SAMPLE_BUDGET,
            "stateCount": state_count,
            "goalSelection": "UNCHANGED_A1_W3_GOAL_STRATA_ONE_PER_BUCKET",
        },
        "privacy": {
            "containsPuzzleGeometry": False,
            "containsHumanOrSelfTestExport": False,
            "containsIsolationSourceList": False,
            "containsSecrets": False,
            "requiresPrivateCanonicalIsolation": True,
        },
        "domain": {"n": n, "chainLength": length},
        "rows": rows,
    }
    summary = {
        "schema": f"{SCHEMA}_SUMMARY",
        "version": VERSION,
        "domain": payload["domain"],
        "samplingContract": payload["samplingContract"],
        "diagnostics": diag,
    }
    summary["summaryFingerprint"] = fp(summary)

    output_dir.mkdir(parents=True, exist_ok=True)
    candidates = output_dir / f"{stem}.candidates.json"
    summary_path = output_dir / f"{stem}.summary.json"
    candidates.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "PASS_SHARD",
                "domain": stem,
                "rows": len(rows),
                "stateCount": state_count,
                "summaryFingerprint": summary["summaryFingerprint"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


def combine(input_dir: Path, output_dir: Path):
    candidate_paths = sorted(input_dir.rglob("N*L*.candidates.json"))
    if len(candidate_paths) != len(DOMAINS):
        raise RuntimeError(
            f"expected {len(DOMAINS)} candidate shards, got {len(candidate_paths)}"
        )

    rows = []
    domains = []
    seen_domains = set()
    state_counts = set()
    for path in candidate_paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema") != SCHEMA or payload.get("version") != VERSION:
            raise RuntimeError(f"unexpected shard schema/version:{path}")
        if payload.get("mechanicBaseline") != base.MECHANIC_BASELINE:
            raise RuntimeError(f"mechanic baseline mismatch:{path}")
        privacy = payload.get("privacy", {})
        if privacy.get("containsPuzzleGeometry") is not False:
            raise RuntimeError(f"geometry exposure contract violation:{path}")
        domain = payload.get("domain", {})
        key = (domain.get("n"), domain.get("chainLength"))
        if key not in DOMAINS or key in seen_domains:
            raise RuntimeError(f"unexpected/duplicate domain:{key}")
        seen_domains.add(key)
        state_counts.add(payload["samplingContract"]["stateCount"])
        shard_rows = payload.get("rows")
        if not isinstance(shard_rows, list):
            raise RuntimeError(f"rows missing:{path}")
        rows.extend(shard_rows)
        domains.append(
            {
                "n": key[0],
                "chainLength": key[1],
                "rowCount": len(shard_rows),
                "identityFingerprint": fp([row["id"] for row in shard_rows]),
            }
        )

    if seen_domains != set(DOMAINS):
        raise RuntimeError("domain closure mismatch")
    if len(state_counts) != 1:
        raise RuntimeError(f"state-count mismatch across shards:{sorted(state_counts)}")

    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("cross-domain identity duplicate")
    rows.sort(key=lambda row: (row["n"], row["chainLength"], row["id"]))

    n_counts = Counter(row["n"] for row in rows)
    nl_counts = Counter((row["n"], row["chainLength"]) for row in rows)
    state_count = next(iter(state_counts))
    pool = {
        "schema": f"{SCHEMA}_POOL",
        "version": VERSION,
        "mechanicBaseline": base.MECHANIC_BASELINE,
        "samplingContract": {
            "grammar": base.SAMPLING_GRAMMAR,
            "stateCount": state_count,
            "goalSelection": "UNCHANGED_A1_W3_GOAL_STRATA_ONE_PER_BUCKET",
        },
        "privacy": {
            "containsPuzzleGeometry": False,
            "containsHumanOrSelfTestExport": False,
            "containsIsolationSourceList": False,
            "containsSecrets": False,
            "requiresPrivateCanonicalIsolation": True,
        },
        "domains": sorted(domains, key=lambda item: (item["n"], item["chainLength"])),
        "rows": rows,
    }
    summary = {
        "schema": f"{SCHEMA}_POOL_SUMMARY",
        "version": VERSION,
        "stateCount": state_count,
        "rowCount": len(rows),
        "nCounts": {str(k): v for k, v in sorted(n_counts.items())},
        "nlCounts": {
            f"N{n}L{length}": count
            for (n, length), count in sorted(nl_counts.items())
        },
        "identityFingerprint": fp(ids),
        "domains": pool["domains"],
        "boundaries": {
            "privateIsolationApplied": False,
            "targetPairCapacityMeasured": False,
            "replacementCatalogSelected": False,
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
    print(
        json.dumps(
            {
                "status": "PASS_COMBINED",
                "rowCount": len(rows),
                "nCounts": summary["nCounts"],
                "summaryFingerprint": summary["summaryFingerprint"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int)
    parser.add_argument("--length", type=int)
    parser.add_argument("--state-count", type=int, default=DEFAULT_STATE_COUNT)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--combine-dir", type=Path)
    args = parser.parse_args()

    if args.combine_dir is not None:
        if args.n is not None or args.length is not None:
            raise RuntimeError("--combine-dir cannot be mixed with --n/--length")
        combine(args.combine_dir, args.output_dir)
        return
    if args.n is None or args.length is None:
        raise RuntimeError("--n and --length are required for shard mode")
    write_shard(args.n, args.length, args.state_count, args.output_dir)


if __name__ == "__main__":
    main()
