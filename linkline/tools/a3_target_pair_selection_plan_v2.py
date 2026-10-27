#!/usr/bin/env python3
"""Build a public-safe 1,300-ID target-pair selection/order plan v2.

V2 fixes the invalid v1 assumption that the currently deployed product already
covers every N3/N4 exact target pair. N3/N4 are instead selected from the
already-public reuse-first A3 candidate pool. N5 uses the approved 96-state
acquisition pool and N6 uses the approved 48-state acquisition pool.

No puzzle geometry, target coordinates, exact coordinate pair keys, private
isolation IDs, human data, or self-test data are written to the output.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import json
from pathlib import Path

import tools.a3_final_candidate_pool_reuse_v2 as reuse
import tools.a3_target_pair_selection_plan_v1 as v1

SCHEMA = "LINKLINE_A3_TARGET_PAIR_1300_PUBLIC_SELECTION_PLAN_V2"
VERSION = "2.0.0"
LEGACY_SCHEMA = "LINKLINE_A3_PUBLIC_FINAL_CANDIDATE_POOL_REUSE_FIRST"
LEGACY_VERSION = "2.0.0"


def load_legacy_pool(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != LEGACY_SCHEMA or payload.get("version") != LEGACY_VERSION:
        raise v1.SelectionError("unexpected legacy reuse-pool contract")
    privacy = payload.get("privacy", {})
    if privacy.get("containsPuzzleGeometry") is not False:
        raise v1.SelectionError("legacy pool privacy contract changed")
    rows = [row for row in payload.get("rows", []) if row.get("n") in (3, 4)]
    ids = [row.get("id") for row in rows]
    if not rows or len(ids) != len(set(ids)):
        raise v1.SelectionError("invalid legacy reuse-pool rows")
    return rows, {
        "schema": payload["schema"],
        "version": payload["version"],
        "identityFingerprint": v1.fp(sorted(ids)),
        "rowCount": len(rows),
    }


def legacy_groups(rows):
    # The reuse-first pool records sourceUniverseIndex. Rebuild the same already-
    # public deterministic universe in memory, verify the provenance index, and
    # keep target coordinates ephemeral.
    universe = reuse.legacy_universe()
    groups = {3: defaultdict(list), 4: defaultdict(list)}
    for row in rows:
        source = row.get("source", {})
        source_index = source.get("sourceUniverseIndex")
        if type(source_index) is not int or not (0 <= source_index < len(universe)):
            raise v1.SelectionError(f"invalid legacy source index:{row.get('id')}")
        identifier, n, length, _initial, targets = universe[source_index]
        if identifier != row.get("id") or n != row.get("n") or length != row.get("chainLength"):
            raise v1.SelectionError(f"legacy provenance mismatch:{row.get('id')}")
        key = v1.exact_pair(n, targets)
        enriched = dict(row)
        enriched["_pair"] = key
        enriched["_difficulty"] = v1.structural_difficulty(row)
        enriched["_legacyReuse"] = True
        enriched["_legacySourceIndex"] = source_index
        groups[n][key].append(enriched)

    diagnostics = {}
    for n in (3, 4):
        expected = v1.TARGET_COUNTS[n]
        if len(groups[n]) != expected:
            raise v1.SelectionError(
                f"legacy reuse-pool exact-pair coverage N{n}:{len(groups[n])}!={expected}"
            )
        for key in groups[n]:
            groups[n][key].sort(
                key=lambda row: (row["_difficulty"], row["chainLength"], row["id"])
            )
        diagnostics[str(n)] = {
            "sourceRows": sum(row["n"] == n for row in rows),
            "exactPairCoverage": len(groups[n]),
            "selectedTarget": expected,
            "pairCap": v1.PAIR_CAPS[n],
            "pairsWithAlternatives": sum(len(items) >= 2 for items in groups[n].values()),
            "maxCandidatesForPair": max((len(items) for items in groups[n].values()), default=0),
        }
    return groups, diagnostics


def public_row(row: dict) -> dict:
    if row.get("_legacyReuse"):
        return {
            "id": row["id"],
            "n": row["n"],
            "chainLength": row["chainLength"],
            "sourceKind": "EXISTING_PUBLIC_REUSE_POOL",
            "sourceUniverseIndex": row["_legacySourceIndex"],
            "groupToken": row["_groupToken"],
            "useIndex": row["_useIndex"],
            "difficulty": row["_difficulty"],
        }
    return v1.public_row(row)


def same_pair_only(repair):
    return [row for row in repair if row.get("purpose") == "SAME_PAIR_REPLACEMENT"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-pool", type=Path, required=True)
    parser.add_argument("--n5-pool", type=Path, required=True)
    parser.add_argument("--n6-pool", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    legacy_rows, legacy_source = load_legacy_pool(args.legacy_pool)
    legacy_group_map, legacy_diag = legacy_groups(legacy_rows)

    n3_primary, n3_secondary, n3_repair_raw, n3_select_diag = v1.choose_pair_capped(
        legacy_group_map[3], 3, v1.TARGET_COUNTS[3]
    )
    n4_primary, n4_secondary, n4_repair_raw, n4_select_diag = v1.choose_pair_capped(
        legacy_group_map[4], 4, v1.TARGET_COUNTS[4]
    )
    if n3_secondary or n4_secondary:
        raise v1.SelectionError("N3/N4 cap=1 unexpectedly required second use")
    n3_repair = same_pair_only(n3_repair_raw)
    n4_repair = same_pair_only(n4_repair_raw)

    n5_rows = v1.public_pool_rows(args.n5_pool, 5, v1.STATE_COUNTS[5])
    n6_rows = v1.public_pool_rows(args.n6_pool, 6, v1.STATE_COUNTS[6])
    n5_groups = v1.group_candidates(n5_rows, 5, v1.STATE_COUNTS[5], v1.N5_DOMAINS)
    n6_groups = v1.group_candidates(n6_rows, 6, v1.STATE_COUNTS[6], v1.N6_DOMAINS)
    n5_primary, n5_secondary, n5_repair, n5_diag = v1.choose_pair_capped(
        n5_groups, 5, v1.TARGET_COUNTS[5]
    )
    n6_primary, n6_secondary, n6_repair, n6_diag = v1.choose_pair_capped(
        n6_groups, 6, v1.TARGET_COUNTS[6]
    )

    queues = {
        3: deque(n3_primary),
        4: deque(n4_primary),
        5: deque(n5_primary + n5_secondary),
        6: deque(n6_primary + n6_secondary),
    }
    ordered = []
    for stage, n in enumerate(v1.schedule_labels(), start=1):
        if not queues[n]:
            raise v1.SelectionError(f"N{n} queue exhausted at stage {stage}")
        item = public_row(queues[n].popleft())
        item["stage"] = stage
        ordered.append(item)
    if any(queues[n] for n in queues):
        raise v1.SelectionError("selected queue residue after scheduling")

    ids = [row["id"] for row in ordered]
    if len(ids) != 1300 or len(ids) != len(set(ids)):
        raise v1.SelectionError("final identity count/uniqueness mismatch")
    n_counts = Counter(row["n"] for row in ordered)
    if n_counts != Counter(v1.TARGET_COUNTS):
        raise v1.SelectionError(f"final N count mismatch:{n_counts}")
    nl_counts = Counter((row["n"], row["chainLength"]) for row in ordered)

    repeat_start = {}
    for n in (5, 6):
        stages = [
            row["stage"] for row in ordered
            if row["n"] == n and row.get("useIndex") == 2
        ]
        repeat_start[str(n)] = min(stages) if stages else None

    summary = {
        "schema": f"{SCHEMA}_SUMMARY",
        "version": VERSION,
        "status": "PASS",
        "total": len(ordered),
        "nCounts": {str(n): n_counts[n] for n in sorted(n_counts)},
        "nlCounts": {
            f"N{n}L{length}": count
            for (n, length), count in sorted(nl_counts.items())
        },
        "legacyCoverage": legacy_diag,
        "n3": n3_select_diag,
        "n4": n4_select_diag,
        "n5": n5_diag,
        "n6": n6_diag,
        "sequence": {
            "firstN5Stage": next(row["stage"] for row in ordered if row["n"] == 5),
            "firstN6Stage": next(row["stage"] for row in ordered if row["n"] == 6),
            "firstRepeatUseStage": repeat_start,
            "maxSameNRun": v1.max_run(row["n"] for row in ordered),
            "maxSameLengthRun": v1.max_run(
                (row["n"], row["chainLength"]) for row in ordered
            ),
        },
        "source": {
            "legacyReusePool": legacy_source,
            "n5PoolIdentityFingerprint": v1.fp(sorted(row["id"] for row in n5_rows)),
            "n6PoolIdentityFingerprint": v1.fp(sorted(row["id"] for row in n6_rows)),
        },
        "privacy": {
            "containsPuzzleGeometry": False,
            "containsTargetCoordinates": False,
            "containsExactTargetPairCoordinateKeys": False,
            "containsPrivateIsolationIds": False,
            "containsHumanOrSelfTestExport": False,
        },
        "boundaries": {
            "privateIsolationApplied": False,
            "privateRepairApplied": False,
            "geometryMaterialized": False,
            "productionCatalogModified": False,
        },
        "selectionFingerprint": v1.fp(ids),
    }
    summary["summaryFingerprint"] = v1.fp(summary)

    plan = {
        "schema": SCHEMA,
        "version": VERSION,
        "selectionFingerprint": summary["selectionFingerprint"],
        "summaryFingerprint": summary["summaryFingerprint"],
        "total": len(ordered),
        "order": ordered,
        "repairReservoir": n3_repair + n4_repair + n5_repair + n6_repair,
        "repairContract": {
            "samePairReplacement": "replacement with identical groupToken preserves exact-pair usage",
            "secondUseReserve": "SECOND_USE_RESERVE applies only where pairCap=2",
            "pairCaps": {str(n): cap for n, cap in sorted(v1.PAIR_CAPS.items())},
            "privateIsolationMustBeZeroAfterRepair": True,
        },
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "selection_plan.json").write_text(
        json.dumps(plan, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
