#!/usr/bin/env python3
"""Public-safe capacity diagnostic for Linkline A3 difficulty rebalance.

This reads only already-public candidate pools and the public V3 selection plan.
It emits aggregate shortest-distance counts and pair-diversity-constrained hard
supply capacity. No puzzle geometry, exact pair coordinates, research IDs,
isolation membership, or private evidence are written to output.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path

import tools.a3_final_candidate_pool_reuse_v2 as reuse
import tools.a3_target_pair_selection_plan_v1 as v1
import tools.a3_target_pair_selection_plan_v3 as v3

SCHEMA = "LINKLINE_A3_DIFFICULTY_TARGET_PAIR_CAPACITY_V1"
VERSION = "1.1.0"
THRESHOLDS = tuple(range(2, 9))


def fp(value) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def distance(row: dict) -> int:
    value = row.get("structural", {}).get("shortestDistance")
    if type(value) is not int or value < 1:
        raise v1.SelectionError(f"invalid shortestDistance:{row.get('id')}")
    return value


def compact_hist(values) -> dict:
    counts = Counter(values)
    return {str(k): counts[k] for k in sorted(counts)}


def legacy_orbit_supply(rows: list[dict]):
    universe = reuse.legacy_universe()
    by_n_orbit = {3: defaultdict(list), 4: defaultdict(list)}
    for row in rows:
        source = row.get("source", {})
        source_index = source.get("sourceUniverseIndex")
        if type(source_index) is not int or not (0 <= source_index < len(universe)):
            raise v1.SelectionError("invalid legacy source index")
        identifier, n, length, _initial, targets = universe[source_index]
        if identifier != row.get("id") or n != row.get("n") or length != row.get("chainLength"):
            raise v1.SelectionError("legacy provenance mismatch")
        if n not in (3, 4):
            continue
        orbit = v3.canonical_pair(n, tuple(sorted(targets)))
        by_n_orbit[n][orbit].append(row)

    result = {}
    for n in (3, 4):
        expected = v1.TARGET_COUNTS[n]
        orbit_sizes = {}
        for orbit_key, candidates in by_n_orbit[n].items():
            sample_targets = None
            for source_index in [c["source"]["sourceUniverseIndex"] for c in candidates]:
                _id, _n, _length, _initial, targets = universe[source_index]
                sample_targets = tuple(sorted(targets))
                break
            orbit_sizes[orbit_key] = len(v3.pair_orbit(n, sample_targets))
        if sum(orbit_sizes.values()) != expected:
            raise v1.SelectionError(f"legacy orbit coverage mismatch N{n}")

        threshold_rows = {}
        for threshold in THRESHOLDS:
            hard_capacity = 0
            forced_below = 0
            deficient_orbits = 0
            for orbit_key, candidates in by_n_orbit[n].items():
                required = orbit_sizes[orbit_key]
                hard = sum(distance(row) >= threshold for row in candidates)
                take = min(required, hard)
                hard_capacity += take
                forced_below += required - take
                deficient_orbits += int(hard < required)
            threshold_rows[str(threshold)] = {
                "hardCapacity": hard_capacity,
                "forcedBelowThreshold": forced_below,
                "deficientOrbitCount": deficient_orbits,
            }
        result[str(n)] = {
            "candidateRows": sum(len(v) for v in by_n_orbit[n].values()),
            "orbitCount": len(by_n_orbit[n]),
            "targetCount": expected,
            "rawDistanceCounts": compact_hist(
                distance(row) for candidates in by_n_orbit[n].values() for row in candidates
            ),
            "thresholdCapacity": threshold_rows,
        }
    return result


def expanded_pair_supply(rows: list[dict], n: int, state_count: int, domains):
    groups = v1.group_candidates(rows, n, state_count, domains)
    target = v1.TARGET_COUNTS[n]
    cap = v1.PAIR_CAPS[n]
    pair_count = len(groups)
    if pair_count > target:
        raise v1.SelectionError(f"N{n} unique pair groups exceed target")
    if pair_count * cap < target:
        raise v1.SelectionError(f"N{n} pair-cap supply below target")
    second_use_required = target - pair_count

    threshold_rows = {}
    for threshold in THRESHOLDS:
        hard_counts = {
            key: sum(distance(row) >= threshold for row in candidates)
            for key, candidates in groups.items()
        }
        hard_primary = sum(count >= 1 for count in hard_counts.values())
        hard_second_groups = sum(count >= 2 for count in hard_counts.values())
        hard_second = min(second_use_required, hard_second_groups)
        hard_capacity = hard_primary + hard_second
        threshold_rows[str(threshold)] = {
            "hardCapacity": hard_capacity,
            "forcedBelowThreshold": target - hard_capacity,
            "pairGroupsWithNoHardCandidate": pair_count - hard_primary,
            "pairGroupsWithTwoHardCandidates": hard_second_groups,
            "requiredSecondUses": second_use_required,
            "hardSecondUseCapacity": hard_second,
        }
    return {
        "candidateRows": len(rows),
        "pairGroupCount": pair_count,
        "pairCap": cap,
        "targetCount": target,
        "uniquePairFirst": True,
        "requiredSecondUses": second_use_required,
        "rawDistanceCounts": compact_hist(distance(row) for row in rows),
        "thresholdCapacity": threshold_rows,
    }


def current_selection_distribution(plan: dict, pools: list[list[dict]]):
    by_id = {}
    for rows in pools:
        for row in rows:
            identifier = row.get("id")
            if identifier in by_id:
                if distance(by_id[identifier]) != distance(row):
                    raise v1.SelectionError("same ID has inconsistent distance")
                continue
            by_id[identifier] = row

    values = []
    stages_by_distance = defaultdict(list)
    missing = 0
    for item in plan.get("order", []):
        row = by_id.get(item.get("id"))
        if row is None:
            missing += 1
            continue
        d = distance(row)
        values.append(d)
        stages_by_distance[d].append(item.get("stage"))
    if missing:
        raise v1.SelectionError(f"current selection IDs missing from public pools:{missing}")
    if len(values) != 1300:
        raise v1.SelectionError(f"current selection mapped count:{len(values)}")
    return {
        "distanceCounts": compact_hist(values),
        "distanceAtMost3": sum(v <= 3 for v in values),
        "distanceAtMost2": sum(v <= 2 for v in values),
        "distance1Stages": stages_by_distance.get(1, []),
        "distance2StageSample": stages_by_distance.get(2, [])[:40],
        "distance3StageSample": stages_by_distance.get(3, [])[:40],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-pool", type=Path, required=True)
    parser.add_argument("--n5-pool", type=Path, required=True)
    parser.add_argument("--n6-pool", type=Path, required=True)
    parser.add_argument("--selection-plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    legacy_rows, _legacy_source = v3.load_legacy_pool(args.legacy_pool)
    n5_rows = v1.public_pool_rows(args.n5_pool, 5, v1.STATE_COUNTS[5])
    n6_rows = v1.public_pool_rows(args.n6_pool, 6, v1.STATE_COUNTS[6])
    plan = json.loads(args.selection_plan.read_text(encoding="utf-8"))

    domains = {
        "3_4": legacy_orbit_supply(legacy_rows),
        "5": expanded_pair_supply(n5_rows, 5, v1.STATE_COUNTS[5], v1.N5_DOMAINS),
        "6": expanded_pair_supply(n6_rows, 6, v1.STATE_COUNTS[6], v1.N6_DOMAINS),
    }
    current = current_selection_distribution(plan, [legacy_rows, n5_rows, n6_rows])

    aggregate = {}
    for threshold in THRESHOLDS:
        t = str(threshold)
        hard_capacity = (
            domains["3_4"]["3"]["thresholdCapacity"][t]["hardCapacity"]
            + domains["3_4"]["4"]["thresholdCapacity"][t]["hardCapacity"]
            + domains["5"]["thresholdCapacity"][t]["hardCapacity"]
            + domains["6"]["thresholdCapacity"][t]["hardCapacity"]
        )
        aggregate[t] = {
            "hardCapacity": hard_capacity,
            "forcedBelowThreshold": 1300 - hard_capacity,
        }

    output = {
        "schema": SCHEMA,
        "version": VERSION,
        "status": "PASS",
        "policyContext": {
            "stage1To5MayUseDistance1": True,
            "distance1ForbiddenAfterStage5": True,
            "distance2And3MustBeRare": True,
            "pairCapsRemainHard": {str(n): cap for n, cap in sorted(v1.PAIR_CAPS.items())},
            "allAvailableExactPairsUsedBeforeAnySecondUse": True,
            "pairDiversityPrecedesDifficultyOptimization": True,
        },
        "currentSelection": current,
        "capacity": domains,
        "aggregateThresholdCapacity": aggregate,
        "privacy": {
            "containsPuzzleGeometry": False,
            "containsExactPairCoordinates": False,
            "containsResearchIds": False,
            "containsPrivateIsolation": False,
            "containsHumanOrSelfTestData": False,
        },
    }
    output["summaryFingerprint"] = fp(output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
