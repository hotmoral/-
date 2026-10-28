#!/usr/bin/env python3
"""V3 wrapper for the progressive selector with accepted N3/N4 length mix preserved.

The V2 N5/N6 policy is retained. N3/N4 are selected inside the same D4 target-pair
orbit AND the same chain-length cells used by accepted target-pair V3, preventing
hard-candidate selection from collapsing legacy format diversity.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import json

import tools.a3_difficulty_selection_plan_v2 as base
import tools.a3_final_candidate_pool_reuse_v2 as reuse
import tools.a3_target_pair_selection_plan_v1 as v1
import tools.a3_target_pair_selection_plan_v3 as pair_v3

SCHEMA = "LINKLINE_A3_DIFFICULTY_REBALANCED_1300_PUBLIC_SELECTION_PLAN_V3"
VERSION = "3.0.0"


def legacy_length_preserving_selection(rows: list[dict], quotas_by_n: dict[int, Counter]):
    universe = reuse.legacy_universe()

    # Reconstruct the accepted V3 displayed-pair assignment and its balanced
    # chain-length mix. Geometry remains ephemeral.
    baseline, _baseline_repairs, baseline_diag = pair_v3.legacy_oriented_selection(rows)

    candidate_groups = {3: defaultdict(list), 4: defaultdict(list)}
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
        candidate_groups[n][(orbit_key, length)].append(item)

    selected_by_n = {}
    repairs_by_n = {}
    diagnostics = {}

    for n in (3, 4):
        slot_groups = defaultdict(list)
        for slot in baseline[n]:
            target_pair = pair_v3.transformed_pair(
                n, slot["_canonicalTargets"], slot["_orientationTransform"]
            )
            slot_groups[(slot["_orbitKey"], slot["chainLength"])].append(target_pair)

        target_quota = quotas_by_n[n]
        group_keys = sorted(slot_groups, key=lambda item: (item[1], item[0]))
        dp = {(0, 0, 0): (0, [])}
        group_band_cache = {}

        for group_key in group_keys:
            required = len(slot_groups[group_key])
            candidates_by_band = defaultdict(list)
            for row in candidate_groups[n][group_key]:
                candidates_by_band[base.band(base.distance(row))].append(row)
            group_band_cache[group_key] = candidates_by_band
            available = {d: len(candidates_by_band[d]) for d in (1, 2, 3, 4)}
            options = base.feasible_orbit_allocations(required, available, target_quota)
            if not options:
                raise base.DifficultySelectionError(
                    f"N{n} accepted length/orbit cell has no legal allocation:{group_key[1]}"
                )

            new_dp = {}
            for state, (score, path) in dp.items():
                for allocation in options:
                    a1, a2, a3, _a4 = allocation
                    next_state = (state[0] + a1, state[1] + a2, state[2] + a3)
                    if (
                        next_state[0] > target_quota[1]
                        or next_state[1] > target_quota[2]
                        or next_state[2] > target_quota[3]
                    ):
                        continue
                    next_score = score + base.allocation_quality(
                        candidates_by_band, allocation
                    )
                    previous = new_dp.get(next_state)
                    candidate_path = path + [(group_key, allocation)]
                    if previous is None or next_score > previous[0]:
                        new_dp[next_state] = (next_score, candidate_path)
            dp = new_dp
            if not dp:
                raise base.DifficultySelectionError(
                    f"N{n} accepted length-mix allocation DP exhausted"
                )

        target_state = (target_quota[1], target_quota[2], target_quota[3])
        if target_state not in dp:
            raise base.DifficultySelectionError(
                f"N{n} cannot preserve accepted length mix and onboarding quotas"
            )
        allocations = dict(dp[target_state][1])

        selected = []
        repairs = []
        used_ids = set()
        for group_key in group_keys:
            allocation = allocations[group_key]
            candidates_by_band = group_band_cache[group_key]
            chosen = []
            for d, count in ((1, allocation[0]), (2, allocation[1]), (3, allocation[2])):
                rows_d = sorted(
                    candidates_by_band[d],
                    key=lambda row: (
                        base.difficulty(row), row["chainLength"], row["id"]
                    ),
                )
                chosen.extend(rows_d[:count])
            hard_rows = sorted(
                candidates_by_band[4],
                key=lambda row: (
                    -base.distance(row), -base.difficulty(row), row["id"]
                ),
            )
            chosen.extend(hard_rows[: allocation[3]])

            slots = sorted(slot_groups[group_key])
            if len(chosen) != len(slots):
                raise base.DifficultySelectionError("length-preserving slot count mismatch")
            if len({row["id"] for row in chosen}) != len(chosen):
                raise base.DifficultySelectionError("length-preserving local identity duplicate")
            if used_ids & {row["id"] for row in chosen}:
                raise base.DifficultySelectionError("legacy identity reused across length cells")
            used_ids.update(row["id"] for row in chosen)

            chosen.sort(key=base.queue_rank)
            remaining = [
                row for row in candidate_groups[n][group_key]
                if row["id"] not in {chosen_row["id"] for chosen_row in chosen}
            ]
            for row, target_pair in zip(chosen, slots):
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
                        "purpose": "ORIENTED_SAME_EXACT_PAIR_LENGTH_AND_DIFFICULTY_PRESERVING_REPLACEMENT",
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

        selected_lengths = Counter(row["chainLength"] for row in selected)
        accepted_lengths = Counter(row["chainLength"] for row in baseline[n])
        if selected_lengths != accepted_lengths:
            raise base.DifficultySelectionError(f"N{n} accepted length mix changed")

        selected_by_n[n] = selected
        repairs_by_n[n] = repairs
        diagnostics[str(n)] = {
            "selected": len(selected),
            "pairCap": 1,
            "exactPairCount": len(selected),
            "distanceCounts": base.compact_hist(base.distance(row) for row in selected),
            "selectedLengthCounts": {
                str(k): v for k, v in sorted(selected_lengths.items())
            },
            "acceptedLengthCounts": baseline_diag[str(n)]["selectedLengthCounts"],
            "lengthMixMatchesAcceptedV3": True,
            "repairRows": len(repairs),
        }

    return selected_by_n, repairs_by_n, diagnostics


def main():
    base.SCHEMA = SCHEMA
    base.VERSION = VERSION
    base.legacy_progressive_selection = legacy_length_preserving_selection
    base.main()


if __name__ == "__main__":
    main()
