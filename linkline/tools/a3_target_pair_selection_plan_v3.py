#!/usr/bin/env python3
"""Build the public-safe 1,300-ID target-pair selection/order plan v3.

V3 fixes the N3/N4 exact-coordinate accounting bug in v1/v2. Research identity
remains D4-canonical, but product target-pair policy is defined on the actual
board coordinates shown to the player. Therefore one canonical research identity
is selected at most once, while an explicit D4 orientation is assigned at product
materialization time.

N3/N4: every exact board-coordinate target pair is used exactly once.
N5/N6: existing acquisition semantics remain unchanged, with cap=2.

Outputs contain no initial paths, target coordinates, exact pair keys, private
isolation IDs, human data, or self-test data.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import json
from pathlib import Path

import tools.a3_final_candidate_pool_public as base
import tools.a3_final_candidate_pool_reuse_v2 as reuse
import tools.a3_target_pair_selection_plan_v1 as v1

SCHEMA = "LINKLINE_A3_TARGET_PAIR_1300_PUBLIC_SELECTION_PLAN_V3"
VERSION = "3.0.0"
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


def transformed_pair(n: int, targets, transform: int):
    return tuple(sorted(base.transform_cell(n, int(cell), transform) for cell in targets))


def pair_orbit(n: int, targets):
    return tuple(sorted({transformed_pair(n, targets, t) for t in range(8)}))


def canonical_pair(n: int, targets):
    return min(pair_orbit(n, targets))


def transform_for_pair(n: int, canonical_targets, target_pair):
    matches = [t for t in range(8) if transformed_pair(n, canonical_targets, t) == target_pair]
    if not matches:
        raise v1.SelectionError(f"no D4 transform reaches requested N{n} exact pair")
    return min(matches)


def legacy_oriented_selection(rows):
    # Rebuild the same already-public deterministic legacy universe. Its stored
    # geometry is D4-canonical by research identity; keep coordinates ephemeral.
    universe = reuse.legacy_universe()
    by_n_orbit = {3: defaultdict(list), 4: defaultdict(list)}

    for row in rows:
        source = row.get("source", {})
        source_index = source.get("sourceUniverseIndex")
        if type(source_index) is not int or not (0 <= source_index < len(universe)):
            raise v1.SelectionError(f"invalid legacy source index:{row.get('id')}")
        identifier, n, length, _initial, targets = universe[source_index]
        if identifier != row.get("id") or n != row.get("n") or length != row.get("chainLength"):
            raise v1.SelectionError(f"legacy provenance mismatch:{row.get('id')}")
        if n not in (3, 4):
            continue
        canonical_targets = tuple(sorted(targets))
        orbit_key = canonical_pair(n, canonical_targets)
        enriched = dict(row)
        enriched["_canonicalTargets"] = canonical_targets
        enriched["_orbitKey"] = orbit_key
        enriched["_difficulty"] = v1.structural_difficulty(row)
        enriched["_legacySourceIndex"] = source_index
        by_n_orbit[n][orbit_key].append(enriched)

    selections = {}
    repairs = {}
    diagnostics = {}
    for n in (3, 4):
        expected_exact = n * n * (n * n - 1) // 2
        all_exact_pairs = set()
        selected = []
        repair = []
        used_ids = set()
        length_counts = Counter()
        orbit_rows = by_n_orbit[n]
        if not orbit_rows:
            raise v1.SelectionError(f"no N{n} legacy orbits")

        for orbit_key in sorted(orbit_rows):
            candidates = sorted(
                orbit_rows[orbit_key],
                key=lambda row: (row["_difficulty"], row["chainLength"], row["id"]),
            )
            targets = candidates[0]["_canonicalTargets"]
            orbit = pair_orbit(n, targets)
            all_exact_pairs.update(orbit)
            # One distinct research identity per displayed exact pair, plus one
            # exclusive same-orbit repair identity where available.
            if len(candidates) < len(orbit):
                raise v1.SelectionError(
                    f"N{n} orbit identity supply {len(candidates)}<{len(orbit)}"
                )
            remaining = list(candidates)
            for target_pair in orbit:
                chosen = min(
                    remaining,
                    key=lambda row: (
                        length_counts[row["chainLength"]],
                        row["_difficulty"],
                        row["chainLength"],
                        row["id"],
                    ),
                )
                remaining.remove(chosen)
                if chosen["id"] in used_ids:
                    raise v1.SelectionError("legacy research identity reused")
                used_ids.add(chosen["id"])
                length_counts[chosen["chainLength"]] += 1
                orientation = transform_for_pair(n, chosen["_canonicalTargets"], target_pair)
                item = {
                    **chosen,
                    "_orientationTransform": orientation,
                    "_useIndex": 1,
                }
                selected.append(item)

                if remaining:
                    reserve = min(
                        remaining,
                        key=lambda row: (
                            abs(row["_difficulty"] - chosen["_difficulty"]),
                            row["chainLength"],
                            row["id"],
                        ),
                    )
                    remaining.remove(reserve)
                    repair.append({
                        "replacementForId": chosen["id"],
                        "id": reserve["id"],
                        "n": n,
                        "chainLength": reserve["chainLength"],
                        "orientationTransform": transform_for_pair(
                            n, reserve["_canonicalTargets"], target_pair
                        ),
                        "difficulty": reserve["_difficulty"],
                        "purpose": "ORIENTED_SAME_EXACT_PAIR_REPLACEMENT",
                    })

        if len(all_exact_pairs) != expected_exact:
            raise v1.SelectionError(
                f"N{n} D4 orbit expansion exact-pair coverage {len(all_exact_pairs)}!={expected_exact}"
            )
        if len(selected) != v1.TARGET_COUNTS[n]:
            raise v1.SelectionError(
                f"N{n} oriented selection count {len(selected)}!={v1.TARGET_COUNTS[n]}"
            )
        if len({row["id"] for row in selected}) != len(selected):
            raise v1.SelectionError(f"N{n} oriented selected identity duplicate")

        selected.sort(key=lambda row: (row["_difficulty"], row["chainLength"], row["id"]))
        selections[n] = selected
        repairs[n] = repair
        diagnostics[str(n)] = {
            "sourceRows": sum(row["n"] == n for row in rows),
            "canonicalPairOrbitCount": len(orbit_rows),
            "expandedExactPairCount": len(all_exact_pairs),
            "selected": len(selected),
            "pairCap": 1,
            "uniqueSelectedResearchIdentities": len({row["id"] for row in selected}),
            "orientedRepairRows": len(repair),
            "selectedLengthCounts": {
                str(length): count for length, count in sorted(length_counts.items())
            },
        }
    return selections, repairs, diagnostics


def public_legacy_row(row: dict):
    return {
        "id": row["id"],
        "n": row["n"],
        "chainLength": row["chainLength"],
        "sourceKind": "EXISTING_PUBLIC_REUSE_POOL_D4_ORIENTED",
        "sourceUniverseIndex": row["_legacySourceIndex"],
        "orientationTransform": row["_orientationTransform"],
        "useIndex": 1,
        "difficulty": row["_difficulty"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-pool", type=Path, required=True)
    parser.add_argument("--n5-pool", type=Path, required=True)
    parser.add_argument("--n6-pool", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    legacy_rows, legacy_source = load_legacy_pool(args.legacy_pool)
    legacy_selected, legacy_repairs, legacy_diag = legacy_oriented_selection(legacy_rows)

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
        3: deque(legacy_selected[3]),
        4: deque(legacy_selected[4]),
        5: deque(n5_primary + n5_secondary),
        6: deque(n6_primary + n6_secondary),
    }
    ordered = []
    for stage, n in enumerate(v1.schedule_labels(), start=1):
        if not queues[n]:
            raise v1.SelectionError(f"N{n} queue exhausted at stage {stage}")
        row = queues[n].popleft()
        item = public_legacy_row(row) if n in (3, 4) else v1.public_row(row)
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
        "legacyOrientationCoverage": legacy_diag,
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
        "selectionFingerprint": v1.fp([
            [row["id"], row.get("orientationTransform")] for row in ordered
        ]),
    }
    summary["summaryFingerprint"] = v1.fp(summary)

    plan = {
        "schema": SCHEMA,
        "version": VERSION,
        "selectionFingerprint": summary["selectionFingerprint"],
        "summaryFingerprint": summary["summaryFingerprint"],
        "total": len(ordered),
        "order": ordered,
        "repairReservoir": (
            legacy_repairs[3] + legacy_repairs[4] + n5_repair + n6_repair
        ),
        "repairContract": {
            "orientedExactPairReplacement": (
                "N3/N4 replacementForId reserve uses an explicit D4 orientation "
                "that preserves the displayed exact coordinate pair"
            ),
            "samePairReplacement": (
                "N5/N6 replacement with identical groupToken preserves exact-pair usage"
            ),
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
