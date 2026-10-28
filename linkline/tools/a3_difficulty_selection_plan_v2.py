#!/usr/bin/env python3
"""Build the public-safe Linkline A3 difficulty-rebalanced 1,300-stage plan.

Product-owner policy encoded here:
- stages 1..5: shortestDistance exactly 1;
- stages 6..8: shortestDistance exactly 2;
- stages 9..11: shortestDistance exactly 3;
- stages 12..1300: shortestDistance >= 4;
- N3/N4 displayed exact target pairs remain single-use;
- N5/N6 use the maximum number of distinct target pairs that have a legal
  >=4-move candidate, then use only the minimum required second uses, cap=2;
- all first uses precede second uses within N5/N6;
- the accepted 1,300-stage N-format schedule remains unchanged.

The output intentionally contains no puzzle geometry, target coordinates,
private isolation membership, or human/self-test data.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
import json
from pathlib import Path

import tools.a3_final_candidate_pool_reuse_v2 as reuse
import tools.a3_target_pair_selection_plan_v1 as v1
import tools.a3_target_pair_selection_plan_v3 as v3

SCHEMA = "LINKLINE_A3_DIFFICULTY_REBALANCED_1300_PUBLIC_SELECTION_PLAN_V2"
VERSION = "2.0.0"
HARD_MIN_DISTANCE = 4
ONBOARDING_BANDS = ((1, 5, 1), (6, 8, 2), (9, 11, 3))

# Soft balancing targets retained from the accepted V3 target-pair campaign.
# They are not allowed to override the product-owner shortest-distance policy.
LENGTH_TARGETS = {
    5: {6: 103, 7: 104, 8: 102, 9: 104, 10: 101},
    6: {8: 78, 9: 78, 10: 79, 11: 79, 12: 79, 13: 79, 14: 79, 15: 79},
}


class DifficultySelectionError(RuntimeError):
    pass


def fp(value) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def distance(row: dict) -> int:
    value = row.get("structural", {}).get("shortestDistance")
    if type(value) is not int or value < 1:
        raise DifficultySelectionError(f"invalid shortestDistance:{row.get('id')}")
    return value


def difficulty(row: dict) -> int:
    return v1.structural_difficulty(row)


def band(value: int) -> int:
    return value if value <= 3 else 4


def queue_rank(row: dict):
    return (distance(row), difficulty(row), row["chainLength"], row["id"])


def hard_quality(row: dict) -> int:
    return distance(row) * 10_000_000 + difficulty(row)


def compact_hist(values) -> dict:
    counts = Counter(values)
    return {str(k): counts[k] for k in sorted(counts)}


def pool_state_count(path: Path) -> int:
    payload = json.loads(path.read_text(encoding="utf-8"))
    value = payload.get("samplingContract", {}).get("stateCount")
    if type(value) is not int or value < 1:
        raise DifficultySelectionError(f"invalid stateCount contract:{path}")
    return value


def onboarding_quotas(labels: list[int]) -> dict[int, Counter]:
    quotas = {3: Counter(), 4: Counter()}
    covered = set()
    for start, end, d in ONBOARDING_BANDS:
        for stage in range(start, end + 1):
            n = labels[stage - 1]
            if n not in quotas:
                raise DifficultySelectionError(
                    f"onboarding stage {stage} unexpectedly uses N{n}"
                )
            quotas[n][d] += 1
            covered.add(stage)
    if covered != set(range(1, 12)):
        raise DifficultySelectionError("onboarding band coverage mismatch")
    return quotas


def feasible_orbit_allocations(required: int, available: dict[int, int], quotas: Counter):
    result = []
    max1 = min(required, available.get(1, 0), quotas[1])
    for a1 in range(max1 + 1):
        max2 = min(required - a1, available.get(2, 0), quotas[2])
        for a2 in range(max2 + 1):
            max3 = min(required - a1 - a2, available.get(3, 0), quotas[3])
            for a3 in range(max3 + 1):
                a4 = required - a1 - a2 - a3
                if a4 <= available.get(4, 0):
                    result.append((a1, a2, a3, a4))
    return result


def allocation_quality(candidates_by_band: dict[int, list[dict]], allocation) -> int:
    a1, a2, a3, a4 = allocation
    score = 0
    for d, count in ((1, a1), (2, a2), (3, a3)):
        rows = sorted(
            candidates_by_band[d],
            key=lambda row: (difficulty(row), row["chainLength"], row["id"]),
        )[:count]
        score -= sum(difficulty(row) for row in rows)
    hard_rows = sorted(
        candidates_by_band[4],
        key=lambda row: (-distance(row), -difficulty(row), row["chainLength"], row["id"]),
    )[:a4]
    score += sum(hard_quality(row) for row in hard_rows)
    return score


def legacy_progressive_selection(rows: list[dict], quotas_by_n: dict[int, Counter]):
    universe = reuse.legacy_universe()
    by_n_orbit = {3: defaultdict(list), 4: defaultdict(list)}
    orbit_targets = {3: {}, 4: {}}

    for row in rows:
        source = row.get("source", {})
        source_index = source.get("sourceUniverseIndex")
        if type(source_index) is not int or not (0 <= source_index < len(universe)):
            raise DifficultySelectionError("invalid legacy source index")
        identifier, n, length, _initial, targets = universe[source_index]
        if identifier != row.get("id") or n != row.get("n") or length != row.get("chainLength"):
            raise DifficultySelectionError(f"legacy provenance mismatch:{row.get('id')}")
        if n not in (3, 4):
            continue
        canonical_targets = tuple(sorted(targets))
        orbit_key = v3.canonical_pair(n, canonical_targets)
        item = dict(row)
        item["_canonicalTargets"] = canonical_targets
        item["_legacySourceIndex"] = source_index
        by_n_orbit[n][orbit_key].append(item)
        orbit_targets[n].setdefault(orbit_key, canonical_targets)

    selected_by_n = {}
    repairs_by_n = {}
    diagnostics = {}

    for n in (3, 4):
        orbit_keys = sorted(by_n_orbit[n])
        orbit_sizes = {
            key: len(v3.pair_orbit(n, orbit_targets[n][key]))
            for key in orbit_keys
        }
        if sum(orbit_sizes.values()) != v1.TARGET_COUNTS[n]:
            raise DifficultySelectionError(f"N{n} exact-pair orbit coverage mismatch")

        target_quota = quotas_by_n[n]
        # DP state tracks only the scarce onboarding bands. Everything else is >=4.
        dp = {(0, 0, 0): (0, [])}
        for key in orbit_keys:
            required = orbit_sizes[key]
            candidates_by_band = defaultdict(list)
            for row in by_n_orbit[n][key]:
                candidates_by_band[band(distance(row))].append(row)
            available = {d: len(candidates_by_band[d]) for d in (1, 2, 3, 4)}
            options = feasible_orbit_allocations(required, available, target_quota)
            if not options:
                raise DifficultySelectionError(f"N{n} orbit has no legal difficulty allocation")
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
                    next_score = score + allocation_quality(candidates_by_band, allocation)
                    previous = new_dp.get(next_state)
                    candidate_path = path + [(key, allocation)]
                    if previous is None or next_score > previous[0]:
                        new_dp[next_state] = (next_score, candidate_path)
            dp = new_dp
            if not dp:
                raise DifficultySelectionError(f"N{n} onboarding allocation DP exhausted")

        target_state = (target_quota[1], target_quota[2], target_quota[3])
        if target_state not in dp:
            raise DifficultySelectionError(
                f"N{n} cannot satisfy onboarding distance quotas:{dict(target_quota)}"
            )
        allocations = dict(dp[target_state][1])

        selected = []
        repairs = []
        used_ids = set()
        for key in orbit_keys:
            allocation = allocations[key]
            candidates_by_band = defaultdict(list)
            for row in by_n_orbit[n][key]:
                candidates_by_band[band(distance(row))].append(row)

            chosen = []
            for d, count in ((1, allocation[0]), (2, allocation[1]), (3, allocation[2])):
                rows_d = sorted(
                    candidates_by_band[d],
                    key=lambda row: (difficulty(row), row["chainLength"], row["id"]),
                )
                chosen.extend(rows_d[:count])
            hard_rows = sorted(
                candidates_by_band[4],
                key=lambda row: (-distance(row), -difficulty(row), row["chainLength"], row["id"]),
            )
            chosen.extend(hard_rows[: allocation[3]])
            if len(chosen) != orbit_sizes[key] or len({row["id"] for row in chosen}) != len(chosen):
                raise DifficultySelectionError(f"N{n} orbit chosen-row mismatch")
            if used_ids & {row["id"] for row in chosen}:
                raise DifficultySelectionError("legacy research identity reused across orbits")
            used_ids.update(row["id"] for row in chosen)

            exact_pairs = list(v3.pair_orbit(n, orbit_targets[n][key]))
            chosen.sort(key=queue_rank)
            if len(exact_pairs) != len(chosen):
                raise DifficultySelectionError("legacy exact-pair assignment mismatch")
            remaining = [row for row in by_n_orbit[n][key] if row["id"] not in used_ids]

            for row, target_pair in zip(chosen, exact_pairs):
                orientation = v3.transform_for_pair(n, row["_canonicalTargets"], target_pair)
                item = {
                    **row,
                    "_orientationTransform": orientation,
                    "_useIndex": 1,
                }
                selected.append(item)

                floor_band = band(distance(row))
                reserve_candidates = [
                    candidate
                    for candidate in remaining
                    if band(distance(candidate)) == floor_band
                ]
                if not reserve_candidates and floor_band == 4:
                    reserve_candidates = [
                        candidate for candidate in remaining if distance(candidate) >= HARD_MIN_DISTANCE
                    ]
                if reserve_candidates:
                    reserve = min(
                        reserve_candidates,
                        key=lambda candidate: (
                            abs(distance(candidate) - distance(row)),
                            abs(difficulty(candidate) - difficulty(row)),
                            candidate["id"],
                        ),
                    )
                    remaining.remove(reserve)
                    repairs.append({
                        "replacementForId": row["id"],
                        "id": reserve["id"],
                        "n": n,
                        "chainLength": reserve["chainLength"],
                        "orientationTransform": v3.transform_for_pair(
                            n, reserve["_canonicalTargets"], target_pair
                        ),
                        "difficulty": difficulty(reserve),
                        "shortestDistance": distance(reserve),
                        "purpose": "ORIENTED_SAME_EXACT_PAIR_DIFFICULTY_PRESERVING_REPLACEMENT",
                    })

        selected.sort(key=queue_rank)
        if len(selected) != v1.TARGET_COUNTS[n]:
            raise DifficultySelectionError(f"N{n} selected count mismatch")
        realized = Counter(distance(row) if distance(row) <= 3 else 4 for row in selected)
        if realized[1] != target_quota[1] or realized[2] != target_quota[2] or realized[3] != target_quota[3]:
            raise DifficultySelectionError(f"N{n} onboarding quota realization mismatch")
        if realized[4] != v1.TARGET_COUNTS[n] - sum(target_quota.values()):
            raise DifficultySelectionError(f"N{n} hard-row count mismatch")

        selected_by_n[n] = selected
        repairs_by_n[n] = repairs
        diagnostics[str(n)] = {
            "selected": len(selected),
            "pairCap": 1,
            "exactPairCount": len(selected),
            "distanceCounts": compact_hist(distance(row) for row in selected),
            "selectedLengthCounts": {
                str(k): v for k, v in sorted(Counter(row["chainLength"] for row in selected).items())
            },
            "repairRows": len(repairs),
        }

    return selected_by_n, repairs_by_n, diagnostics


def expanded_hard_groups(rows: list[dict], n: int, state_count: int, domains):
    groups = v1.group_candidates(rows, n, state_count, domains)
    eligible = {}
    excluded = 0
    for key, candidates in groups.items():
        hard = [row for row in candidates if distance(row) >= HARD_MIN_DISTANCE]
        if hard:
            eligible[key] = hard
        else:
            excluded += 1
    if not eligible:
        raise DifficultySelectionError(f"N{n} has no >=4 target-pair groups")
    return groups, eligible, excluded


def length_choice_key(row: dict, length_counts: Counter, targets: dict[int, int], *, harder: bool):
    length = row["chainLength"]
    target = targets[length]
    after = length_counts[length] + 1
    overflow = max(0, after - target)
    # Integer ratio comparison is represented by a high-resolution deterministic scalar.
    ratio = (after * 1_000_000) // target
    if harder:
        return (overflow, ratio, -distance(row), -difficulty(row), row["id"])
    return (overflow, ratio, distance(row), difficulty(row), row["id"])


def choose_max_unique_hard(groups, n: int, target: int):
    length_targets = LENGTH_TARGETS[n]
    if sum(length_targets.values()) != target:
        raise DifficultySelectionError(f"N{n} length-target sum mismatch")

    eligible = groups
    unique_count = len(eligible)
    if unique_count > target:
        raise DifficultySelectionError(f"N{n} eligible target-pair count exceeds target")
    second_needed = target - unique_count
    groups_with_two = sum(len(candidates) >= 2 for candidates in eligible.values())
    if groups_with_two < second_needed:
        raise DifficultySelectionError(
            f"N{n} hard pair diversity insufficient:{groups_with_two} second-capable < {second_needed}"
        )

    group_tokens = {
        key: v1.pair_group_token(row["id"] for row in candidates)
        for key, candidates in eligible.items()
    }
    length_counts = Counter()
    primary_by_group = {}

    # Scarce pair groups are assigned first so soft length balancing cannot strand them.
    ordered_groups = sorted(
        eligible,
        key=lambda key: (
            len({row["chainLength"] for row in eligible[key]}),
            len(eligible[key]),
            group_tokens[key],
        ),
    )
    for key in ordered_groups:
        candidates = eligible[key]
        chosen = min(
            candidates,
            key=lambda row: length_choice_key(
                row, length_counts, length_targets, harder=False
            ),
        )
        primary_by_group[key] = chosen
        length_counts[chosen["chainLength"]] += 1

    second_by_group = {}
    while len(second_by_group) < second_needed:
        options = []
        for key in ordered_groups:
            if key in second_by_group:
                continue
            primary = primary_by_group[key]
            for row in eligible[key]:
                if row["id"] == primary["id"]:
                    continue
                options.append(
                    (
                        length_choice_key(row, length_counts, length_targets, harder=True),
                        group_tokens[key],
                        key,
                        row,
                    )
                )
        if not options:
            raise DifficultySelectionError(f"N{n} second-use selection exhausted")
        _rank, _token, key, chosen = min(options, key=lambda item: (item[0], item[1]))
        second_by_group[key] = chosen
        length_counts[chosen["chainLength"]] += 1

    primary = []
    secondary = []
    selected_ids = set()
    for key in sorted(ordered_groups, key=lambda k: group_tokens[k]):
        row = primary_by_group[key]
        if row["id"] in selected_ids:
            raise DifficultySelectionError("expanded primary identity duplicate")
        selected_ids.add(row["id"])
        primary.append({**row, "_groupToken": group_tokens[key], "_useIndex": 1})
        if key in second_by_group:
            row2 = second_by_group[key]
            if row2["id"] in selected_ids:
                raise DifficultySelectionError("expanded secondary identity duplicate")
            selected_ids.add(row2["id"])
            secondary.append({**row2, "_groupToken": group_tokens[key], "_useIndex": 2})

    if len(primary) != unique_count or len(primary) + len(secondary) != target:
        raise DifficultySelectionError(f"N{n} selected count mismatch")
    usage = Counter(row["_groupToken"] for row in primary + secondary)
    if max(usage.values(), default=0) > v1.PAIR_CAPS[n]:
        raise DifficultySelectionError(f"N{n} pair cap violation")

    primary.sort(key=queue_rank)
    secondary.sort(key=queue_rank)

    repair = []
    for key in ordered_groups:
        selected_in_group = {primary_by_group[key]["id"]}
        if key in second_by_group:
            selected_in_group.add(second_by_group[key]["id"])
        unused = [row for row in eligible[key] if row["id"] not in selected_in_group]
        unused.sort(key=lambda row: (-distance(row), -difficulty(row), row["id"]))
        for row in unused[:3]:
            repair.append({
                "groupToken": group_tokens[key],
                "id": row["id"],
                "n": n,
                "chainLength": row["chainLength"],
                "difficulty": difficulty(row),
                "shortestDistance": distance(row),
                "purpose": "HARD_SAME_PAIR_REPLACEMENT",
            })

    deviations = {
        str(length): length_counts[length] - target_count
        for length, target_count in sorted(length_targets.items())
    }
    return primary, secondary, repair, {
        "eligibleDistinctPairCount": unique_count,
        "secondUseCount": len(secondary),
        "selectedCount": len(primary) + len(secondary),
        "pairCap": v1.PAIR_CAPS[n],
        "allSelectedRowsAtLeast4Moves": all(distance(row) >= 4 for row in primary + secondary),
        "distanceCounts": compact_hist(distance(row) for row in primary + secondary),
        "selectedLengthCounts": {
            str(k): v for k, v in sorted(length_counts.items())
        },
        "lengthTargetDeviation": deviations,
        "maxAbsLengthTargetDeviation": max((abs(v) for v in deviations.values()), default=0),
        "repairReservoirRows": len(repair),
    }


def public_legacy_row(row: dict) -> dict:
    return {
        "id": row["id"],
        "n": row["n"],
        "chainLength": row["chainLength"],
        "sourceKind": "EXISTING_PUBLIC_REUSE_POOL_D4_ORIENTED_PROGRESSIVE_DIFFICULTY",
        "sourceUniverseIndex": row["_legacySourceIndex"],
        "orientationTransform": row["_orientationTransform"],
        "useIndex": 1,
        "difficulty": difficulty(row),
        "shortestDistance": distance(row),
    }


def public_expanded_row(row: dict) -> dict:
    return {
        "id": row["id"],
        "n": row["n"],
        "chainLength": row["chainLength"],
        "sourceKind": row["source"]["sourceKind"],
        "groupToken": row["_groupToken"],
        "useIndex": row["_useIndex"],
        "difficulty": difficulty(row),
        "shortestDistance": distance(row),
    }


def block_distance_summary(ordered: list[dict], block_size: int = 100):
    result = []
    for start in range(0, len(ordered), block_size):
        values = sorted(row["shortestDistance"] for row in ordered[start : start + block_size])
        result.append({
            "startStage": start + 1,
            "endStage": start + len(values),
            "min": values[0],
            "median": values[len(values) // 2],
            "max": values[-1],
        })
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-pool", type=Path, required=True)
    parser.add_argument("--n5-pool", type=Path, required=True)
    parser.add_argument("--n6-pool", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    labels = v1.schedule_labels()
    quotas = onboarding_quotas(labels)

    legacy_rows, legacy_source = v3.load_legacy_pool(args.legacy_pool)
    legacy_selected, legacy_repairs, legacy_diag = legacy_progressive_selection(
        legacy_rows, quotas
    )

    n5_state_count = pool_state_count(args.n5_pool)
    n6_state_count = pool_state_count(args.n6_pool)
    n5_rows = v1.public_pool_rows(args.n5_pool, 5, n5_state_count)
    n6_rows = v1.public_pool_rows(args.n6_pool, 6, n6_state_count)
    _n5_all, n5_groups, n5_excluded = expanded_hard_groups(
        n5_rows, 5, n5_state_count, v1.N5_DOMAINS
    )
    _n6_all, n6_groups, n6_excluded = expanded_hard_groups(
        n6_rows, 6, n6_state_count, v1.N6_DOMAINS
    )
    n5_primary, n5_secondary, n5_repair, n5_diag = choose_max_unique_hard(
        n5_groups, 5, v1.TARGET_COUNTS[5]
    )
    n6_primary, n6_secondary, n6_repair, n6_diag = choose_max_unique_hard(
        n6_groups, 6, v1.TARGET_COUNTS[6]
    )
    n5_diag["excludedLowOnlyPairGroups"] = n5_excluded
    n6_diag["excludedLowOnlyPairGroups"] = n6_excluded

    queues = {
        3: deque(legacy_selected[3]),
        4: deque(legacy_selected[4]),
        5: deque(n5_primary + n5_secondary),
        6: deque(n6_primary + n6_secondary),
    }
    ordered = []
    for stage, n in enumerate(labels, start=1):
        if not queues[n]:
            raise DifficultySelectionError(f"N{n} queue exhausted at stage {stage}")
        row = queues[n].popleft()
        item = public_legacy_row(row) if n in (3, 4) else public_expanded_row(row)
        item["stage"] = stage
        ordered.append(item)
    if any(queues[n] for n in queues):
        raise DifficultySelectionError("selected queue residue after scheduling")

    ids = [row["id"] for row in ordered]
    if len(ids) != 1300 or len(ids) != len(set(ids)):
        raise DifficultySelectionError("final identity count/uniqueness mismatch")
    n_counts = Counter(row["n"] for row in ordered)
    if n_counts != Counter(v1.TARGET_COUNTS):
        raise DifficultySelectionError(f"final N count mismatch:{n_counts}")

    expected_stage_distance = {}
    for start, end, d in ONBOARDING_BANDS:
        for stage in range(start, end + 1):
            expected_stage_distance[stage] = d
    for row in ordered:
        stage = row["stage"]
        d = row["shortestDistance"]
        if stage in expected_stage_distance:
            if d != expected_stage_distance[stage]:
                raise DifficultySelectionError(
                    f"onboarding distance mismatch stage {stage}:{d} != {expected_stage_distance[stage]}"
                )
        elif d < HARD_MIN_DISTANCE:
            raise DifficultySelectionError(
                f"shortestDistance<{HARD_MIN_DISTANCE} after onboarding at stage {stage}:{d}"
            )

    first_second = {}
    last_primary = {}
    for n in (5, 6):
        primary_stages = [
            row["stage"] for row in ordered if row["n"] == n and row["useIndex"] == 1
        ]
        second_stages = [
            row["stage"] for row in ordered if row["n"] == n and row["useIndex"] == 2
        ]
        last_primary[str(n)] = max(primary_stages)
        first_second[str(n)] = min(second_stages) if second_stages else None
        if second_stages and min(second_stages) <= max(primary_stages):
            raise DifficultySelectionError(
                f"N{n} target-pair second use occurred before distinct-pair phase closed"
            )

    distance_counts = Counter(row["shortestDistance"] for row in ordered)
    if distance_counts[1] != 5 or distance_counts[2] != 3 or distance_counts[3] != 3:
        raise DifficultySelectionError(f"global low-distance count mismatch:{distance_counts}")

    nl_counts = Counter((row["n"], row["chainLength"]) for row in ordered)
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
        "distanceCounts": {str(k): distance_counts[k] for k in sorted(distance_counts)},
        "lowDistancePolicy": {
            "distance1Stages": [1, 2, 3, 4, 5],
            "distance2Stages": [6, 7, 8],
            "distance3Stages": [9, 10, 11],
            "distance2And3Count": 6,
            "distance2And3Share": 6 / 1300,
            "minimumDistanceFromStage12": 4,
        },
        "targetPairPolicy": {
            "pairCaps": {str(n): cap for n, cap in sorted(v1.PAIR_CAPS.items())},
            "n3n4ExactPairSingleUse": True,
            "n5n6DistinctHardPairsMaximized": True,
            "firstSecondUseStage": first_second,
            "lastPrimaryUseStage": last_primary,
        },
        "legacy": legacy_diag,
        "n5": n5_diag,
        "n6": n6_diag,
        "blockDistanceSummary": block_distance_summary(ordered),
        "sequence": {
            "firstN5Stage": next(row["stage"] for row in ordered if row["n"] == 5),
            "firstN6Stage": next(row["stage"] for row in ordered if row["n"] == 6),
            "maxSameNRun": v1.max_run(row["n"] for row in ordered),
            "maxSameLengthRun": v1.max_run(
                (row["n"], row["chainLength"]) for row in ordered
            ),
        },
        "source": {
            "legacyReusePool": legacy_source,
            "n5StateCount": n5_state_count,
            "n6StateCount": n6_state_count,
            "n5PoolIdentityFingerprint": fp(sorted(row["id"] for row in n5_rows)),
            "n6PoolIdentityFingerprint": fp(sorted(row["id"] for row in n6_rows)),
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
    }
    summary["selectionFingerprint"] = fp([
        [row["id"], row.get("orientationTransform"), row.get("useIndex")]
        for row in ordered
    ])
    summary["summaryFingerprint"] = fp(summary)

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
                "N3/N4 replacement preserves displayed exact pair and difficulty band via D4 orientation"
            ),
            "samePairReplacement": (
                "N5/N6 identical groupToken replacement preserves exact target pair and >=4 floor"
            ),
            "pairCaps": {str(n): cap for n, cap in sorted(v1.PAIR_CAPS.items())},
            "distinctPairPhaseBeforeSecondUse": {"5": True, "6": True},
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
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
