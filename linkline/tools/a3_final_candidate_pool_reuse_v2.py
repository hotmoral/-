#!/usr/bin/env python3
"""Reuse-first public-safe A3 final candidate materializer.

Reconstructs the accepted N3/N4 legacy source shape (4096 deterministic spread
bounded sample + exact N3 union) and the frozen A1 W3 N5/N6 source domains.
No puzzle geometry, human export, self-test export, or isolation-source list is
written. Private canonical isolation is applied after this public computation.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

import tools.a3_final_candidate_pool_public as base

OUT = Path("public_output/a3_final_candidate_pool_v2")
LEGACY_SAMPLE = 4096
LEGACY_DOMAINS = tuple(
    [(3, length) for length in range(3, 9)]
    + [(4, length) for length in range(3, 11)]
)
EXPANDED_DOMAINS = tuple(
    [(5, length) for length in range(6, 11)]
    + [(6, length) for length in range(8, 16)]
)


def fp(value) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def spread(total: int, requested: int):
    count = min(total, requested)
    if count == total:
        return tuple(range(total))
    return tuple((index * total) // count for index in range(count))


def legacy_universe():
    rows = []
    for n, length in LEGACY_DOMAINS:
        for identifier, initial, targets in base.domain_universe(n, length):
            rows.append((identifier, n, length, initial, targets))
        print(json.dumps({"legacyUniverseDomain": f"N{n}L{length}", "accumulated": len(rows)}, sort_keys=True), flush=True)
    rows.sort(key=lambda row: row[0])
    return rows


def materialize_legacy():
    universe = legacy_universe()
    bounded = []
    for source_index in spread(len(universe), LEGACY_SAMPLE):
        identifier, n, length, initial, targets = universe[source_index]
        values = base.profile_identity(n, length, initial, targets)
        if values is None:
            continue
        bounded.append(base.candidate_row(
            identifier, n, length, values,
            {"sourceKind": "LEGACY_BOUNDED_PUBLIC_REPLAY", "sourceUniverseIndex": source_index},
        ))

    exact_n3 = []
    for source_index, (identifier, n, length, initial, targets) in enumerate(universe):
        if n != 3:
            continue
        values = base.profile_identity(n, length, initial, targets)
        if values is None:
            continue
        exact_n3.append(base.candidate_row(
            identifier, n, length, values,
            {"sourceKind": "N3_EXACT_PUBLIC_REPLAY", "sourceUniverseIndex": source_index},
        ))

    by_id = {row["id"]: row for row in bounded}
    for row in exact_n3:
        by_id[row["id"]] = row
    rows = sorted(by_id.values(), key=lambda row: (row["n"], row["chainLength"], row["id"]))
    return rows, {
        "universeCount": len(universe),
        "boundedExactEligibleBeforePrivateIsolation": len(bounded),
        "exactN3BeforePrivateIsolation": len(exact_n3),
        "legacyUnionBeforePrivateIsolation": len(rows),
        "legacyUnionIdentityFingerprintBeforePrivateIsolation": fp([row["id"] for row in rows]),
    }


def materialize_expanded():
    rows = []
    domains = []
    for n, length in EXPANDED_DOMAINS:
        domain_rows, diag = base.materialize_expanded_domain(n, length)
        rows.extend(domain_rows)
        domains.append({"n": n, "chainLength": length, **diag})
        print(json.dumps({"expandedDomain": f"N{n}L{length}", "exactRowsBeforePrivateIsolation": len(domain_rows)}, sort_keys=True), flush=True)
    rows.sort(key=lambda row: (row["n"], row["chainLength"], row["id"]))
    return rows, domains


def summarize(rows):
    n_counts = Counter(row["n"] for row in rows)
    nl_counts = Counter((row["n"], row["chainLength"]) for row in rows)
    format_families = {tuple(row["signatures"]["formatAwareFamilyV2"]) for row in rows}
    cross_families = {tuple(row["signatures"]["crossFormatStructuralV2"]) for row in rows}
    qualitative = {tuple(row["signatures"]["qualitativeReasoningV2"]) for row in rows}
    return {
        "rowCount": len(rows),
        "nCounts": {str(k): v for k, v in sorted(n_counts.items())},
        "nlCounts": {f"N{n}L{length}": v for (n, length), v in sorted(nl_counts.items())},
        "formatAwareUniqueFamilyCount": len(format_families),
        "crossFormatUniqueFamilyCount": len(cross_families),
        "qualitativeSignatureCount": len(qualitative),
        "identityFingerprint": fp([row["id"] for row in rows]),
    }


def main():
    legacy, legacy_diag = materialize_legacy()
    expanded, expanded_diag = materialize_expanded()
    by_id = {}
    for row in legacy + expanded:
        if row["id"] in by_id:
            raise RuntimeError(f"cross-source duplicate:{row['id']}")
        by_id[row["id"]] = row
    rows = sorted(by_id.values(), key=lambda row: (row["n"], row["chainLength"], row["id"]))
    payload = {
        "schema": "LINKLINE_A3_PUBLIC_FINAL_CANDIDATE_POOL_REUSE_FIRST",
        "version": "2.0.0",
        "mechanicBaseline": base.MECHANIC_BASELINE,
        "privacy": {
            "containsPuzzleGeometry": False,
            "containsHumanOrSelfTestExport": False,
            "containsIsolationSourceList": False,
            "requiresPrivateCanonicalIsolation": True,
        },
        "frozenQuotaByNL": {f"N{n}L{length}": q for (n, length), q in sorted(base.QUOTAS.items())},
        "rows": rows,
    }
    summary = {
        "schema": "LINKLINE_A3_PUBLIC_FINAL_CANDIDATE_POOL_REUSE_FIRST_SUMMARY",
        "version": "2.0.0",
        "legacyReplay": legacy_diag,
        "expandedDomains": expanded_diag,
        "poolBeforePrivateIsolation": summarize(rows),
    }
    summary["summaryFingerprint"] = fp(summary)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "candidate_pool.json").write_text(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS_PUBLIC_RECONSTRUCTION", **summary["poolBeforePrivateIsolation"], "summaryFingerprint": summary["summaryFingerprint"]}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
