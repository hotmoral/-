#!/usr/bin/env python3
"""V4 progressive selector wrapper with balanced N3/N4 length and difficulty mix.

V2 remains authoritative for N5/N6 hard-pair maximization. This wrapper replaces
only N3/N4 selection: onboarding bands are exact, post-onboarding rows are >=4,
and the accepted V3 length distribution is treated as a strong balancing target
rather than an impossible absolute constraint.
"""
from __future__ import annotations

from collections import Counter, defaultdict

import tools.a3_difficulty_selection_plan_v2 as base
import tools.a3_final_candidate_pool_reuse_v2 as reuse
import tools.a3_target_pair_selection_plan_v1 as v1
import tools.a3_target_pair_selection_plan_v3 as pair_v3

SCHEMA = "LINKLINE_A3_DIFFICULTY_REBALANCED_1300_PUBLIC_SELECTION_PLAN_V4"
VERSION = "4.0.0"

LEGACY_LENGTH_TARGETS = {
    3: {3: 6, 4: 9, 5: 5, 6: 8, 7: 5, 8: 3},
    4: {3: 6, 4: 16, 5: 17, 6: 16, 7: 17, 8: 16, 9: 16, 10: 16},
}
# Avoid both trivial post-onboarding rows and the V2 mistake of front-loading
# extreme N3/N4 solutions before N5 is introduced.
LEGACY_HARD_TARGET_DISTANCE = {3: 5, 4: 6}
MAX_LEGACY_LENGTH_DEVIATION = 3


def balanced_candidate_key(
    row: dict,
    length_counts: Counter,
    length_targets: dict[int, int],
    *,
    low_band: bool,
    preferred_hard_distance: int,
):
    length = row["chainLength"]
    target = length_targets[length]
    after = length_counts[length] + 1
    overflow = max(0, after - target)
    ratio = (after * 1_000_000) // target
    if low_band:
        return (overflow, ratio, base.difficulty(row), row["id"])
    return (
        overflow,
        ratio,
        abs(base.distance(row) - preferred_hard_distance),
        base.distance(row),
        base.difficulty(row),
        row["id"],
    )


def legacy_balanced_progressive_selection(rows: list[dict], quotas_by_n: dict[int, Counter]):
    universe = reuse.legacy_universe()
    by_n_orbit = {3: defaultdict(list), 4: defaultdict(list)}
    orbit_targets = {3: {}, 4: {}}

    for row in rows:
        source_index = row.get("source", {}).get("sourceUniverseIndex")
        if type(source_index) is not int or not (0 <= source_index < len(universe)):
            raise base.DifficultySelectionError("invalid legacy source index")
        identifier, n, length, _initial, targets = universe[source_index]
        if identifier != row.get("id") or n != row.get("n") or length != row.get("chainLength"):
            raise base.DifficultySelectionError(f"legacy provenance mismatch:{row.get('id')}")
        if n not in (3, 4):
            continue
        canonical_targets = tuple(sorted(targets))
        orbit_key = pair_v3.canonical_pair(n, canonical_targets)
        item = dict(row)
        item["_canonicalTargets"] = canonical_targets
        item["_orbitKey"] = orbit_key
        item["_legacySourceIndex"] = source_index
        by_n_orbit[n][orbit_key].append(item)
        orbit_targets[n].setdefault(orbit_key, canonical_targets)

    selected_by_n = {}
    repairs_by_n = {}
    diagnostics = {}

    for n in (3, 4):
        orbit_keys = sorted(by_n_orbit[n])
        orbit_sizes = {
            key: len(pair_v3.pair_orbit(n, orbit_targets[n][key]))
            for key in orbit_keys
        }
        if sum(orbit_sizes.values()) != v1.TARGET_COUNTS[n]:
            raise base.DifficultySelectionError(f"N{n} exact-pair orbit coverage mismatch")

        target_quota = quotas_by_n[n]
        # First solve only the hard product-owner onboarding counts at orbit level.
        dp = {(0, 0, 0): (0, [])}
        band_cache = {}
        for key in orbit_keys:
            required = orbit_sizes[key]
            candidates_by_band = defaultdict(list)
            for row in by_n_orbit[n][key]:
                candidates_by_band[base.band(base.distance(row))].append(row)
            band_cache[key] = candidates_by_band
            available = {d: len(candidates_by_band[d]) for d in (1, 2, 3, 4)}
            options = base.feasible_orbit_allocations(required, available, target_quota)
            if not options:
                raise base.DifficultySelectionError(f"N{n} orbit has no legal allocation")
            new_dp = {}
            for state, (score, path) in dp.items():
                for allocation in options:
                    a1, a2, a3, a4 = allocation
                    next_state = (state[0] + a1, state[1] + a2, state[2] + a3)
                    if (
                        next_state[0] > target_quota[1]
                        or next_state[1] > target_quota[2]
                        or next_state[2] > target_quota[3]
                    ):
                        continue
                    # Favor allocations with more candidate slack; exact candidate
                    # choice and length balancing happen in the next pass.
                    slack = (
                        len(candidates_by_band[1]) - a1
                        + len(candidates_by_band[2]) - a2
                        + len(candidates_by_band[3]) - a3
                        + len(candidates_by_band[4]) - a4
                    )
                    next_score = score + slack
                    candidate_path = path + [(key, allocation)]
                    previous = new_dp.get(next_state)
                    if previous is None or next_score > previous[0]:
                        new_dp[next_state] = (next_score, candidate_path)
            dp = new_dp
            if not dp:
                raise base.DifficultySelectionError(f"N{n} onboarding allocation DP exhausted")

        target_state = (target_quota[1], target_quota[2], target_quota[3])
        if target_state not in dp:
            raise base.DifficultySelectionError(f"N{n} onboarding quotas infeasible")
        allocations = dict(dp[target_state][1])

        length_targets = LEGACY_LENGTH_TARGETS[n]
        length_counts = Counter()
        selected_by_orbit = {}
        used_ids = set()
        # Pick scarcer orbits first, but balance chain lengths globally.
        pick_order = sorted(
            orbit_keys,
            key=lambda key: (
                len({row["chainLength"] for row in by_n_orbit[n][key]}),
                len(by_n_orbit[n][key]),
                key,
            ),
        )
        for key in pick_order:
            allocation = allocations[key]
            candidates_by_band = band_cache[key]
            chosen = []
            for d, count in ((1, allocation[0]), (2, allocation[1]), (3, allocation[2]), (4, allocation[3])):
                available = [
                    row
                    for row in candidates_by_band[d]
                    if row["id"] not in used_ids
                ]
                for _ in range(count):
                    if not available:
                        raise base.DifficultySelectionError(
                            f"N{n} orbit candidate shortage in band {d}"
                        )
                    row = min(
                        available,
                        key=lambda candidate: balanced_candidate_key(
                            candidate,
                            length_counts,
                            length_targets,
                            low_band=(d <= 3),
                            preferred_hard_distance=LEGACY_HARD_TARGET_DISTANCE[n],
                        ),
                    )
                    available.remove(row)
                    chosen.append(row)
                    used_ids.add(row["id"])
                    length_counts[row["chainLength"]] += 1
            if len(chosen) != orbit_sizes[key]:
                raise base.DifficultySelectionError("legacy balanced orbit count mismatch")
            selected_by_orbit[key] = chosen

        selected = []
        repairs = []
        for key in orbit_keys:
            chosen = sorted(selected_by_orbit[key], key=base.queue_rank)
            exact_pairs = list(pair_v3.pair_orbit(n, orbit_targets[n][key]))
            if len(chosen) != len(exact_pairs):
                raise base.DifficultySelectionError("legacy target-pair assignment mismatch")
            remaining = [
                row for row in by_n_orbit[n][key]
                if row["id"] not in {candidate["id"] for candidate in chosen}
            ]
            for row, target_pair in zip(chosen, exact_pairs):
                orientation = pair_v3.transform_for_pair(
                    n, row["_canonicalTargets"], target_pair
                )
                selected.append({
                    **row,
                    "_orientationTransform": orientation,
                    "_useIndex": 1,
                })

                row_band = base.band(base.distance(row))
                reserve_candidates = [
                    candidate
                    for candidate in remaining
                    if base.band(base.distance(candidate)) == row_band
                    and candidate["chainLength"] == row["chainLength"]
                ]
                if not reserve_candidates:
                    reserve_candidates = [
                        candidate
                        for candidate in remaining
                        if base.band(base.distance(candidate)) == row_band
                    ]
                if not reserve_candidates and row_band == 4:
                    reserve_candidates = [
                        candidate
                        for candidate in remaining
                        if base.distance(candidate) >= base.HARD_MIN_DISTANCE
                    ]
                if reserve_candidates:
                    reserve = min(
                        reserve_candidates,
                        key=lambda candidate: (
                            candidate["chainLength"] != row["chainLength"],
                            abs(base.distance(candidate) - base.distance(row)),
                            abs(base.difficulty(candidate) - base.difficulty(row)),
                            candidate["id"],
                        ),
                    )
                    remaining.remove(reserve)
                    repairs.append({
                        "replacementForId": row["id"],
                        "id": reserve["id"],
                        "n": n,
                        "chainLength": reserve["chainLength"],
                        "orientationTransform": pair_v3.transform_for_pair(
                            n, reserve["_canonicalTargets"], target_pair
                        ),
                        "difficulty": base.difficulty(reserve),
                        "shortestDistance": base.distance(reserve),
                        "purpose": "ORIENTED_SAME_EXACT_PAIR_DIFFICULTY_PRESERVING_REPLACEMENT",
                    })

        selected.sort(key=base.queue_rank)
        if len(selected) != v1.TARGET_COUNTS[n]:
            raise base.DifficultySelectionError(f"N{n} selected count mismatch")
        realized = Counter(
            base.distance(row) if base.distance(row) <= 3 else 4
            for row in selected
        )
        if (
            realized[1] != target_quota[1]
            or realized[2] != target_quota[2]
            or realized[3] != target_quota[3]
        ):
            raise base.DifficultySelectionError(f"N{n} onboarding quota mismatch")

        deviations = {
            str(length): length_counts[length] - target
            for length, target in sorted(length_targets.items())
        }
        max_deviation = max((abs(value) for value in deviations.values()), default=0)
        if max_deviation > MAX_LEGACY_LENGTH_DEVIATION:
            raise base.DifficultySelectionError(
                f"N{n} length-mix deviation too large:{deviations}"
            )

        selected_by_n[n] = selected
        repairs_by_n[n] = repairs
        diagnostics[str(n)] = {
            "selected": len(selected),
            "pairCap": 1,
            "exactPairCount": len(selected),
            "distanceCounts": base.compact_hist(base.distance(row) for row in selected),
            "selectedLengthCounts": {
                str(k): v for k, v in sorted(length_counts.items())
            },
            "acceptedLengthTargets": {
                str(k): v for k, v in sorted(length_targets.items())
            },
            "lengthTargetDeviation": deviations,
            "maxAbsLengthTargetDeviation": max_deviation,
            "hardPreferredDistance": LEGACY_HARD_TARGET_DISTANCE[n],
            "repairRows": len(repairs),
        }

    return selected_by_n, repairs_by_n, diagnostics


def main():
    base.SCHEMA = SCHEMA
    base.VERSION = VERSION
    base.legacy_progressive_selection = legacy_balanced_progressive_selection
    base.main()


if __name__ == "__main__":
    main()
