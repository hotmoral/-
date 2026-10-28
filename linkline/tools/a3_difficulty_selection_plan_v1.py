#!/usr/bin/env python3
"""Build a public-safe 1,300-stage difficulty-rebalanced selection plan.

Policy order:
1. preserve target-pair diversity: N3/N4 exact coordinate pairs are single-use;
   N5/N6 use every available exact pair once before any second use, cap=2;
2. exactly the first five stages use shortestDistance=1, and no later stage may;
3. minimize shortestDistance 2/3 exposure and require their combined share <=1%;
4. among legal candidates prefer larger shortestDistance / structural difficulty;
5. retain the accepted N-format schedule/gates and 1,300 total count.

The public output contains no puzzle geometry or exact pair-coordinate keys.
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

SCHEMA = "LINKLINE_A3_DIFFICULTY_REBALANCED_1300_PUBLIC_SELECTION_PLAN_V1"
VERSION = "1.0.0"
LOW_2_3_CAP = 13  # <= 1% of 1,300, rounded down.


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


def hard_rank(row: dict):
    return (-distance(row), -difficulty(row), -row["chainLength"], row["id"])


def easy_rank(row: dict):
    return (distance(row), difficulty(row), row["chainLength"], row["id"])


def hist(rows) -> dict:
    counts = Counter(distance(row) for row in rows)
    return {str(k): counts[k] for k in sorted(counts)}


def legacy_difficulty_selection(rows: list[dict], early_d1_quota: Counter):
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
        orbit_sizes = {
            key: len(v3.pair_orbit(n, orbit_targets[n][key]))
            for key in by_n_orbit[n]
        }
        if sum(orbit_sizes.values()) != v1.TARGET_COUNTS[n]:
            raise DifficultySelectionError(f"N{n} exact-pair orbit coverage mismatch")

        reserved = defaultdict(list)
        non1_count = {
            key: sum(distance(row) >= 2 for row in candidates)
            for key, candidates in by_n_orbit[n].items()
        }
        easy_options = []
        for key, candidates in by_n_orbit[n].items():
            for row in candidates:
                if distance(row) == 1:
                    easy_options.append((difficulty(row), row["chainLength"], row["id"], key, row))

        needed = int(early_d1_quota[n])
        for _diff, _length, _id, key, row in sorted(easy_options):
            if needed == 0:
                break
            next_reserved = len(reserved[key]) + 1
            required = orbit_sizes[key]
            if next_reserved > required:
                continue
            if non1_count[key] < required - next_reserved:
                continue
            reserved[key].append(row)
            needed -= 1
        if needed:
            raise DifficultySelectionError(f"N{n} cannot reserve required stage-1..5 distance1 rows")

        selected = []
        repairs = []
        for key in sorted(by_n_orbit[n]):
            required = orbit_sizes[key]
            chosen = list(reserved[key])
            chosen_ids = {row["id"] for row in chosen}
            hard_candidates = [
                row for row in by_n_orbit[n][key]
                if row["id"] not in chosen_ids and distance(row) >= 2
            ]
            hard_candidates.sort(key=hard_rank)
            need_hard = required - len(chosen)
            if len(hard_candidates) < need_hard:
                raise DifficultySelectionError(f"N{n} orbit hard supply shortfall")
            chosen.extend(hard_candidates[:need_hard])
            chosen_ids = {row["id"] for row in chosen}

            exact_pairs = list(v3.pair_orbit(n, orbit_targets[n][key]))
            chosen.sort(key=easy_rank)
            if len(chosen) != len(exact_pairs):
                raise DifficultySelectionError("legacy pair/candidate count mismatch")

            remaining = [row for row in by_n_orbit[n][key] if row["id"] not in chosen_ids]
            remaining.sort(key=hard_rank)
            for row, target_pair in zip(chosen, exact_pairs):
                orientation = v3.transform_for_pair(n, row["_canonicalTargets"], target_pair)
                item = {
                    **row,
                    "_orientationTransform": orientation,
                    "_useIndex": 1,
                }
                selected.append(item)

                if remaining:
                    reserve = remaining.pop(0)
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
                        "purpose": "ORIENTED_SAME_EXACT_PAIR_REPLACEMENT",
                    })

        selected.sort(key=easy_rank)
        if len(selected) != v1.TARGET_COUNTS[n]:
            raise DifficultySelectionError(f"N{n} selected count mismatch")
        if len({row["id"] for row in selected}) != len(selected):
            raise DifficultySelectionError(f"N{n} selected identity duplicate")
        if sum(distance(row) == 1 for row in selected) != early_d1_quota[n]:
            raise DifficultySelectionError(f"N{n} distance1 quota mismatch")

        selected_by_n[n] = selected
        repairs_by_n[n] = repairs
        diagnostics[str(n)] = {
            "selected": len(selected),
            "pairCap": 1,
            "exactPairCount": len(selected),
            "distanceCounts": hist(selected),
            "repairRows": len(repairs),
        }

    return selected_by_n, repairs_by_n, diagnostics


def choose_pair_diverse_hard(groups, n: int, target: int):
    pair_count = len(groups)
    if pair_count > target:
        raise DifficultySelectionError(f"N{n} pair count exceeds target")
    if pair_count * v1.PAIR_CAPS[n] < target:
        raise DifficultySelectionError(f"N{n} pair-cap capacity below target")

    ordered_groups = sorted(groups, key=lambda key: v1.fp(["PAIR_ORDER_V1", n, *key[1:]]))
    primary_by_group = {}
    group_tokens = {}
    for key in ordered_groups:
        candidates = groups[key]
        token = v1.pair_group_token(row["id"] for row in candidates)
        group_tokens[key] = token
        primary_by_group[key] = min(candidates, key=hard_rank)

    needed_second = target - pair_count
    second_options = []
    for key in ordered_groups:
        primary = primary_by_group[key]
        alternatives = [row for row in groups[key] if row["id"] != primary["id"]]
        if not alternatives:
            continue
        best = min(alternatives, key=hard_rank)
        second_options.append((hard_rank(best), v1.fp(["SECOND_HARD_V1", group_tokens[key]]), key, best))
    second_options.sort(key=lambda item: (item[0], item[1]))
    if len(second_options) < needed_second:
        raise DifficultySelectionError(f"N{n} second-use capacity shortfall")
    second_by_group = {key: row for _rank, _token, key, row in second_options[:needed_second]}

    primary = []
    secondary = []
    selected_ids = set()
    for key in ordered_groups:
        row = primary_by_group[key]
        selected_ids.add(row["id"])
        primary.append({**row, "_groupToken": group_tokens[key], "_useIndex": 1})
        if key in second_by_group:
            row2 = second_by_group[key]
            if row2["id"] in selected_ids:
                raise DifficultySelectionError("cross-group selected identity duplicate")
            selected_ids.add(row2["id"])
            secondary.append({**row2, "_groupToken": group_tokens[key], "_useIndex": 2})

    if len(primary) + len(secondary) != target:
        raise DifficultySelectionError(f"N{n} selected count mismatch")
    usage = Counter(row["_groupToken"] for row in primary + secondary)
    if max(usage.values(), default=0) > v1.PAIR_CAPS[n]:
        raise DifficultySelectionError(f"N{n} pair cap violation")
    if len(primary) != pair_count:
        raise DifficultySelectionError(f"N{n} unique-pair-first primary mismatch")

    primary.sort(key=easy_rank)
    secondary.sort(key=easy_rank)

    repair = []
    for key in ordered_groups:
        selected_in_group = {primary_by_group[key]["id"]}
        if key in second_by_group:
            selected_in_group.add(second_by_group[key]["id"])
        unused = [row for row in groups[key] if row["id"] not in selected_in_group]
        unused.sort(key=hard_rank)
        for row in unused[:3]:
            repair.append({
                "groupToken": group_tokens[key],
                "id": row["id"],
                "n": n,
                "chainLength": row["chainLength"],
                "difficulty": difficulty(row),
                "shortestDistance": distance(row),
                "purpose": "SAME_PAIR_REPLACEMENT",
            })
        if key not in second_by_group:
            alternatives = [row for row in groups[key] if row["id"] != primary_by_group[key]["id"]]
            if alternatives:
                row = min(alternatives, key=hard_rank)
                repair.append({
                    "groupToken": group_tokens[key],
                    "id": row["id"],
                    "n": n,
                    "chainLength": row["chainLength"],
                    "difficulty": difficulty(row),
                    "shortestDistance": distance(row),
                    "purpose": "SECOND_USE_RESERVE",
                })

    return primary, secondary, repair, {
        "exactPairCount": pair_count,
        "primaryCount": len(primary),
        "secondUseCount": len(secondary),
        "selectedCount": len(primary) + len(secondary),
        "pairCap": v1.PAIR_CAPS[n],
        "uniquePairFirst": True,
        "distanceCounts": hist(primary + secondary),
        "repairReservoirRows": len(repair),
    }


def public_legacy_row(row: dict) -> dict:
    return {
        "id": row["id"],
        "n": row["n"],
        "chainLength": row["chainLength"],
        "sourceKind": "EXISTING_PUBLIC_REUSE_POOL_D4_ORIENTED_DIFFICULTY_REBALANCED",
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-pool", type=Path, required=True)
    parser.add_argument("--n5-pool", type=Path, required=True)
    parser.add_argument("--n6-pool", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    labels = v1.schedule_labels()
    early_d1_quota = Counter(labels[:5])
    if set(early_d1_quota) - {3, 4}:
        raise DifficultySelectionError("first five schedule labels unexpectedly include N5/N6")

    legacy_rows, legacy_source = v3.load_legacy_pool(args.legacy_pool)
    legacy_selected, legacy_repairs, legacy_diag = legacy_difficulty_selection(
        legacy_rows, early_d1_quota
    )

    n5_state_count = json.loads(args.n5_pool.read_text(encoding="utf-8"))["samplingContract"]["stateCount"]
    n6_state_count = json.loads(args.n6_pool.read_text(encoding="utf-8"))["samplingContract"]["stateCount"]
    n5_rows = v1.public_pool_rows(args.n5_pool, 5, n5_state_count)
    n6_rows = v1.public_pool_rows(args.n6_pool, 6, n6_state_count)
    n5_groups = v1.group_candidates(n5_rows, 5, n5_state_count, v1.N5_DOMAINS)
    n6_groups = v1.group_candidates(n6_rows, 6, n6_state_count, v1.N6_DOMAINS)
    n5_primary, n5_secondary, n5_repair, n5_diag = choose_pair_diverse_hard(
        n5_groups, 5, v1.TARGET_COUNTS[5]
    )
    n6_primary, n6_secondary, n6_repair, n6_diag = choose_pair_diverse_hard(
        n6_groups, 6, v1.TARGET_COUNTS[6]
    )

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
        raise DifficultySelectionError("queue residue after schedule materialization")

    ids = [row["id"] for row in ordered]
    if len(ids) != 1300 or len(ids) != len(set(ids)):
        raise DifficultySelectionError("final identity count/uniqueness mismatch")
    n_counts = Counter(row["n"] for row in ordered)
    if n_counts != Counter(v1.TARGET_COUNTS):
        raise DifficultySelectionError(f"final N count mismatch:{n_counts}")

    distance_counts = Counter(row["shortestDistance"] for row in ordered)
    d1_stages = [row["stage"] for row in ordered if row["shortestDistance"] == 1]
    if d1_stages != [1, 2, 3, 4, 5]:
        raise DifficultySelectionError(f"distance1 stage policy failed:{d1_stages}")
    low23 = distance_counts[2] + distance_counts[3]
    if low23 > LOW_2_3_CAP:
        raise DifficultySelectionError(
            f"distance2+3 cap exceeded:{low23}>{LOW_2_3_CAP}; expand hard supply"
        )

    repeat_start = {}
    primary_last = {}
    for n in (5, 6):
        primary_stages = [row["stage"] for row in ordered if row["n"] == n and row["useIndex"] == 1]
        second_stages = [row["stage"] for row in ordered if row["n"] == n and row["useIndex"] == 2]
        primary_last[str(n)] = max(primary_stages)
        repeat_start[str(n)] = min(second_stages) if second_stages else None
        if second_stages and min(second_stages) <= max(primary_stages):
            raise DifficultySelectionError(f"N{n} target-pair repeat occurred before unique-pair phase closed")

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
        "distance1Stages": d1_stages,
        "distance2And3Count": low23,
        "distance2And3Share": low23 / 1300,
        "difficultyPolicy": {
            "distance1OnlyStages1To5": True,
            "distance2And3CombinedCap": LOW_2_3_CAP,
            "distance2And3CombinedShareCap": LOW_2_3_CAP / 1300,
            "hardCandidatePreference": "LEXICOGRAPHIC_SHORTEST_DISTANCE_THEN_STRUCTURAL_DIFFICULTY",
        },
        "targetPairPolicy": {
            "pairCaps": {str(n): cap for n, cap in sorted(v1.PAIR_CAPS.items())},
            "n3n4ExactPairSingleUse": True,
            "n5n6AllAvailablePairsBeforeSecondUse": True,
            "firstSecondUseStage": repeat_start,
            "lastPrimaryUseStage": primary_last,
        },
        "legacy": legacy_diag,
        "n5": n5_diag,
        "n6": n6_diag,
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
            "orientedExactPairReplacement": "N3/N4 replacement preserves displayed exact pair via D4 orientation",
            "samePairReplacement": "N5/N6 identical groupToken replacement preserves exact pair",
            "secondUseReserve": "SECOND_USE_RESERVE may replace a removed second-use row without violating pair cap",
            "pairCaps": {str(n): cap for n, cap in sorted(v1.PAIR_CAPS.items())},
            "uniquePairFirst": {"5": True, "6": True},
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
