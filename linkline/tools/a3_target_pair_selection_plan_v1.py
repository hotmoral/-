#!/usr/bin/env python3
"""Build a public-safe 1,300-ID target-pair selection/order plan.

Inputs:
- the already-public frozen product campaign, used only as the accepted N3/N4
  source; exact bytes are pinned by the canonical product chunk SHA-256 values;
- the approved 96-state N5 acquisition pool;
- the approved 48-state N6 acquisition pool.

Output deliberately contains IDs and non-geometry metadata only. Initial paths,
target coordinates, and exact target-pair coordinate keys are never persisted.
Private canonical isolation is applied later; a bounded repair reservoir is
included so isolated N5/N6 IDs can be replaced without rerunning acquisition.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from hashlib import sha256
import json
from pathlib import Path
from urllib.request import Request, urlopen

import tools.a3_final_candidate_pool_public as base
import tools.a3_target_pair_acquisition_v1 as acquisition

SCHEMA = "LINKLINE_A3_TARGET_PAIR_1300_PUBLIC_SELECTION_PLAN"
VERSION = "1.0.0"
PRODUCT_BASE = "https://linkline-mobile-smoke.sktjsek.workers.dev/data"
EXPECTED_PRODUCT = {
    "catalogFingerprint": "f041497893a1ed9e2cf56fce84f1912a864a45af8060106b7d033bb48d64ccc5",
    "orderFingerprint": "38a91c7d3ad7ed801fe4d4f136314a7f06e878327f317e810dbccad18fead26f",
    "chunks": {
        "campaign-0001-0260.chunk.json": "1daa3c8aa8d65257c4fec2d5b224b050b2e7c75603a5bf5ec25f9746b46651c8",
        "campaign-0261-0520.chunk.json": "ac7ab37884b87176682da514407ee10d817bbbff5a91b8ed98a90a8897efe84".replace("bbbff", "bb84f"),
        "campaign-0521-0780.chunk.json": "bf9156f6ac8c30a267be0cd3747728aa95a175f56547fa700cf4ce45f570223c",
        "campaign-0781-1040.chunk.json": "d69fba56e6245c9b266e5b97ec404e29cd8e1bec493033cf56dfcfd931279923",
        "campaign-1041-1300.chunk.json": "fe1e8a8401a064db497f2c47348b3d11d8a1da298dfa50b9b968c9aee3dbbf2c",
    },
}
TARGET_COUNTS = {3: 36, 4: 120, 5: 514, 6: 630}
PAIR_CAPS = {3: 1, 4: 1, 5: 2, 6: 2}
STATE_COUNTS = {5: 96, 6: 48}
N5_DOMAINS = tuple((5, length) for length in range(6, 11))
N6_DOMAINS = tuple((6, length) for length in range(8, 16))

# 13 x 100-stage curriculum. N5 appears late in block 1; N6 opens only after
# stage 300. N3/N4 taper out rather than disappearing in one abrupt boundary.
BLOCK_QUOTAS = (
    {3: 24, 4: 60, 5: 16, 6: 0},
    {3: 12, 4: 40, 5: 48, 6: 0},
    {3: 0, 4: 20, 5: 80, 6: 0},
    {3: 0, 4: 0, 5: 55, 6: 45},
    {3: 0, 4: 0, 5: 50, 6: 50},
    {3: 0, 4: 0, 5: 45, 6: 55},
    {3: 0, 4: 0, 5: 40, 6: 60},
    {3: 0, 4: 0, 5: 40, 6: 60},
    {3: 0, 4: 0, 5: 35, 6: 65},
    {3: 0, 4: 0, 5: 30, 6: 70},
    {3: 0, 4: 0, 5: 30, 6: 70},
    {3: 0, 4: 0, 5: 25, 6: 75},
    {3: 0, 4: 0, 5: 20, 6: 80},
)


class SelectionError(RuntimeError):
    pass


def fp(value) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "Linkline-A3-Public-Selection/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read()


def fetch_frozen_product_rows():
    manifest_bytes = fetch_bytes(f"{PRODUCT_BASE}/campaign-0001-1300.json")
    manifest = json.loads(manifest_bytes)
    source = manifest.get("source", {})
    if source.get("catalogFingerprint") != EXPECTED_PRODUCT["catalogFingerprint"]:
        raise SelectionError("deployed product catalog fingerprint mismatch")
    if source.get("orderFingerprint") != EXPECTED_PRODUCT["orderFingerprint"]:
        raise SelectionError("deployed product order fingerprint mismatch")
    if manifest.get("launchTotal") != 1300:
        raise SelectionError("deployed product launch total mismatch")

    rows = []
    for chunk in manifest.get("chunks", []):
        name = chunk.get("path")
        expected = EXPECTED_PRODUCT["chunks"].get(name)
        if expected is None or chunk.get("sha256") != expected:
            raise SelectionError(f"unexpected product chunk contract:{name}")
        payload_bytes = fetch_bytes(f"{PRODUCT_BASE}/{name}")
        actual = sha256(payload_bytes).hexdigest()
        if actual != expected:
            raise SelectionError(f"deployed product chunk SHA mismatch:{name}:{actual}")
        payload = json.loads(payload_bytes)
        if payload.get("rowEncoding") != ["n", "length", "initial", "targets"]:
            raise SelectionError(f"unexpected row encoding:{name}")
        for encoded in payload.get("rows", []):
            n, length, initial, targets = encoded
            rows.append(
                {
                    "n": n,
                    "chainLength": length,
                    "initial": initial,
                    "targets": targets,
                    "id": base.identity(n, length, initial, targets),
                    "productPosition": len(rows) + 1,
                }
            )
    if len(rows) != 1300:
        raise SelectionError(f"deployed product row count mismatch:{len(rows)}")
    return rows, {
        "catalogFingerprint": source["catalogFingerprint"],
        "orderFingerprint": source["orderFingerprint"],
        "chunkSha256": EXPECTED_PRODUCT["chunks"],
    }


def exact_pair(n: int, targets) -> tuple[int, int, int]:
    a, b = sorted(int(cell) for cell in targets)
    return n, a, b


def pair_group_token(ids) -> str:
    # Token commits to public candidate IDs, not target coordinates.
    return fp(["PAIR_GROUP_IDS_V1", *sorted(ids)])


def select_legacy_pair_complete(rows):
    result = {}
    coverage = {3: {}, 4: {}}
    for row in rows:
        n = row["n"]
        if n not in (3, 4):
            continue
        key = exact_pair(n, row["targets"])
        coverage[n].setdefault(key, []).append(row)
    for n in (3, 4):
        expected_pairs = n * n * (n * n - 1) // 2
        if len(coverage[n]) != expected_pairs:
            raise SelectionError(
                f"frozen product exact-pair coverage N{n}:{len(coverage[n])}!={expected_pairs}"
            )
        chosen = []
        for key, candidates in sorted(coverage[n].items()):
            chosen.append(min(candidates, key=lambda row: (row["productPosition"], row["id"])))
        if len(chosen) != TARGET_COUNTS[n]:
            raise SelectionError(f"legacy target count mismatch N{n}:{len(chosen)}")
        result[n] = sorted(chosen, key=lambda row: row["productPosition"])
    return result, {
        str(n): {
            "sourceRows": sum(row["n"] == n for row in rows),
            "exactPairCoverage": len(coverage[n]),
            "selected": len(result[n]),
            "pairCap": PAIR_CAPS[n],
        }
        for n in (3, 4)
    }


def reconstruct_geometry_index(n: int, length: int, state_count: int):
    pool, _ = base.sample_domain(n, length)
    states = base.select_states(n, length, pool, count=state_count)
    index = {}
    for state_rank, initial in enumerate(states):
        for span, placement, targets in base.goal_strata(n, length, initial):
            identifier = base.identity(n, length, initial, targets)
            index.setdefault(
                identifier,
                {
                    "targets": tuple(sorted(targets)),
                    "stateRank": state_rank,
                    "goalSpan": span,
                    "goalPlacement": placement,
                },
            )
    return index


def structural_difficulty(row: dict) -> int:
    values = row["structural"]
    return (
        row["chainLength"] * 100
        + values["shortestDistance"] * 12
        + values["detourSteps"] * 45
        + values["sideSwitches"] * 9
        + values["mandatoryInternalStateCount"] * 4
        + max(0, values["initialLegalActionCount"] - values["initialShortestActionCount"]) * 7
    )


def public_pool_rows(path: Path, n: int, expected_state_count: int):
    payload = json.loads(path.read_text(encoding="utf-8"))
    contract = payload.get("samplingContract", {})
    if contract.get("grammar") != base.SAMPLING_GRAMMAR:
        raise SelectionError(f"sampling grammar mismatch:{path}")
    if contract.get("stateCount") != expected_state_count:
        raise SelectionError(f"state count mismatch:{path}")
    rows = [row for row in payload.get("rows", []) if row.get("n") == n]
    if not rows:
        raise SelectionError(f"no N{n} rows:{path}")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise SelectionError(f"duplicate candidate IDs N{n}")
    return rows


def group_candidates(rows: list[dict], n: int, state_count: int, domains):
    geometry = {}
    for dn, length in domains:
        geometry.update(reconstruct_geometry_index(dn, length, state_count))
    groups = defaultdict(list)
    for row in rows:
        item = geometry.get(row["id"])
        if item is None:
            raise SelectionError(f"unreproducible candidate:{row['id']}")
        source = row.get("source", {})
        if source.get("stateCountContract") != state_count:
            raise SelectionError(f"source state-count mismatch:{row['id']}")
        for field in ("stateRank", "goalSpan", "goalPlacement"):
            if source.get(field) != item[field]:
                raise SelectionError(f"source provenance mismatch:{row['id']}:{field}")
        key = exact_pair(n, item["targets"])
        enriched = dict(row)
        enriched["_pair"] = key
        enriched["_difficulty"] = structural_difficulty(row)
        groups[key].append(enriched)
    for key in groups:
        groups[key].sort(key=lambda row: (row["_difficulty"], row["chainLength"], row["id"]))
    return groups


def choose_pair_capped(groups, n: int, target: int):
    # Use every available exact pair once before any second use.
    group_rows = []
    length_counts = Counter()
    primary_by_group = {}
    group_tokens = {}

    ordered_groups = sorted(
        groups,
        key=lambda key: fp(["PAIR_ORDER_V1", n, *key[1:]]),
    )
    for key in ordered_groups:
        candidates = groups[key]
        token = pair_group_token(row["id"] for row in candidates)
        group_tokens[key] = token
        chosen = min(
            candidates,
            key=lambda row: (
                length_counts[row["chainLength"]],
                row["_difficulty"],
                row["id"],
            ),
        )
        primary_by_group[key] = chosen
        length_counts[chosen["chainLength"]] += 1
        group_rows.append((key, chosen, 1))

    if len(group_rows) > target:
        raise SelectionError(f"N{n} unique-pair count exceeds target")
    needed_second = target - len(group_rows)
    if needed_second < 0:
        raise SelectionError("negative second-use requirement")

    second_by_group = {}
    while len(second_by_group) < needed_second:
        options = []
        for key in ordered_groups:
            if key in second_by_group:
                continue
            primary = primary_by_group[key]
            alternatives = [row for row in groups[key] if row["id"] != primary["id"]]
            if not alternatives:
                continue
            secondary = min(
                alternatives,
                key=lambda row: (
                    length_counts[row["chainLength"]],
                    0 if row["chainLength"] != primary["chainLength"] else 1,
                    0 if row["_difficulty"] >= primary["_difficulty"] else 1,
                    abs(row["_difficulty"] - primary["_difficulty"]),
                    row["id"],
                ),
            )
            options.append(
                (
                    length_counts[secondary["chainLength"]],
                    0 if secondary["chainLength"] != primary["chainLength"] else 1,
                    0 if secondary["_difficulty"] >= primary["_difficulty"] else 1,
                    fp(["SECOND_GROUP_ORDER_V1", group_tokens[key]]),
                    key,
                    secondary,
                )
            )
        if not options:
            raise SelectionError(
                f"N{n} second-use capacity exhausted:{len(second_by_group)}/{needed_second}"
            )
        *_rank, key, chosen = min(options)
        second_by_group[key] = chosen
        length_counts[chosen["chainLength"]] += 1

    primary = []
    secondary = []
    selected_ids = set()
    for key in ordered_groups:
        row = primary_by_group[key]
        selected_ids.add(row["id"])
        primary.append(
            {
                **row,
                "_groupToken": group_tokens[key],
                "_useIndex": 1,
            }
        )
        if key in second_by_group:
            row2 = second_by_group[key]
            selected_ids.add(row2["id"])
            secondary.append(
                {
                    **row2,
                    "_groupToken": group_tokens[key],
                    "_useIndex": 2,
                }
            )

    if len(primary) + len(secondary) != target:
        raise SelectionError(f"N{n} selected count mismatch")
    usage = Counter(row["_groupToken"] for row in primary + secondary)
    if max(usage.values(), default=0) > PAIR_CAPS[n]:
        raise SelectionError(f"N{n} pair cap violation")

    # Difficulty progression is applied independently inside the unique-pair and
    # second-use phases. This guarantees no target-pair repeat occurs until all
    # available exact pairs have appeared once.
    primary.sort(key=lambda row: (row["_difficulty"], row["chainLength"], row["id"]))
    secondary.sort(key=lambda row: (row["_difficulty"], row["chainLength"], row["id"]))

    repair = []
    for key in ordered_groups:
        token = group_tokens[key]
        selected_in_group = {
            primary_by_group[key]["id"],
            *([second_by_group[key]["id"]] if key in second_by_group else []),
        }
        unused = [row for row in groups[key] if row["id"] not in selected_in_group]
        for row in unused[:3]:
            repair.append(
                {
                    "groupToken": token,
                    "id": row["id"],
                    "n": n,
                    "chainLength": row["chainLength"],
                    "difficulty": row["_difficulty"],
                    "purpose": "SAME_PAIR_REPLACEMENT",
                }
            )
        if key not in second_by_group and len(groups[key]) >= 2:
            primary_id = primary_by_group[key]["id"]
            candidate = min(
                (row for row in groups[key] if row["id"] != primary_id),
                key=lambda row: (row["_difficulty"], row["id"]),
            )
            repair.append(
                {
                    "groupToken": token,
                    "id": candidate["id"],
                    "n": n,
                    "chainLength": candidate["chainLength"],
                    "difficulty": candidate["_difficulty"],
                    "purpose": "SECOND_USE_RESERVE",
                }
            )

    return primary, secondary, repair, {
        "exactPairCount": len(groups),
        "primaryCount": len(primary),
        "secondUseCount": len(secondary),
        "selectedCount": len(primary) + len(secondary),
        "pairCap": PAIR_CAPS[n],
        "selectedLengthCounts": {
            str(length): count for length, count in sorted(length_counts.items())
        },
        "groupsWithAtLeastTwo": sum(len(rows) >= 2 for rows in groups.values()),
        "maxSourceCandidatesForPair": max((len(rows) for rows in groups.values()), default=0),
        "repairReservoirRows": len(repair),
    }


def balanced_labels(quota: dict[int, int]) -> list[int]:
    size = sum(quota.values())
    used = Counter()
    labels = []
    for position in range(size):
        candidates = [n for n, count in quota.items() if used[n] < count]
        chosen = max(
            candidates,
            key=lambda n: (
                quota[n] * (position + 1) - used[n] * size,
                -n,
            ),
        )
        used[chosen] += 1
        labels.append(chosen)
    if used != Counter(quota):
        raise SelectionError("balanced label quota mismatch")
    return labels


def schedule_labels() -> list[int]:
    labels = []
    # First 60 stages are strictly N3/N4; N5 then enters as a minority signal.
    labels.extend(balanced_labels({3: 18, 4: 42}))
    labels.extend(balanced_labels({3: 6, 4: 18, 5: 16}))
    for block in BLOCK_QUOTAS[1:]:
        labels.extend(balanced_labels({n: count for n, count in block.items() if count}))
    if len(labels) != 1300:
        raise SelectionError(f"schedule length mismatch:{len(labels)}")
    if Counter(labels) != Counter(TARGET_COUNTS):
        raise SelectionError(f"schedule N counts mismatch:{Counter(labels)}")
    if 5 in labels[:60]:
        raise SelectionError("N5 entered before stage 61")
    if 6 in labels[:300]:
        raise SelectionError("N6 entered before stage 301")
    return labels


def max_run(values) -> int:
    best = run = 0
    previous = object()
    for value in values:
        if value == previous:
            run += 1
        else:
            previous = value
            run = 1
        best = max(best, run)
    return best


def public_row(row: dict) -> dict:
    result = {
        "id": row["id"],
        "n": row["n"],
        "chainLength": row["chainLength"],
    }
    if "productPosition" in row:
        result.update(
            {
                "sourceKind": "FROZEN_PRODUCT_ACCEPTED",
                "sourceProductPosition": row["productPosition"],
                "useIndex": 1,
            }
        )
    else:
        result.update(
            {
                "sourceKind": row["source"]["sourceKind"],
                "groupToken": row["_groupToken"],
                "useIndex": row["_useIndex"],
                "difficulty": row["_difficulty"],
            }
        )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n5-pool", type=Path, required=True)
    parser.add_argument("--n6-pool", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    frozen_rows, frozen_source = fetch_frozen_product_rows()
    legacy, legacy_diag = select_legacy_pair_complete(frozen_rows)

    n5_rows = public_pool_rows(args.n5_pool, 5, STATE_COUNTS[5])
    n6_rows = public_pool_rows(args.n6_pool, 6, STATE_COUNTS[6])
    n5_groups = group_candidates(n5_rows, 5, STATE_COUNTS[5], N5_DOMAINS)
    n6_groups = group_candidates(n6_rows, 6, STATE_COUNTS[6], N6_DOMAINS)
    n5_primary, n5_secondary, n5_repair, n5_diag = choose_pair_capped(
        n5_groups, 5, TARGET_COUNTS[5]
    )
    n6_primary, n6_secondary, n6_repair, n6_diag = choose_pair_capped(
        n6_groups, 6, TARGET_COUNTS[6]
    )

    queues = {
        3: deque(legacy[3]),
        4: deque(legacy[4]),
        5: deque(n5_primary + n5_secondary),
        6: deque(n6_primary + n6_secondary),
    }
    labels = schedule_labels()
    ordered = []
    for stage, n in enumerate(labels, start=1):
        if not queues[n]:
            raise SelectionError(f"N{n} queue exhausted at stage {stage}")
        row = queues[n].popleft()
        item = public_row(row)
        item["stage"] = stage
        ordered.append(item)
    if any(queues[n] for n in queues):
        raise SelectionError("selected queue residue after scheduling")

    ids = [row["id"] for row in ordered]
    if len(ids) != len(set(ids)):
        raise SelectionError("selected identity duplicate")
    n_counts = Counter(row["n"] for row in ordered)
    nl_counts = Counter((row["n"], row["chainLength"]) for row in ordered)
    if n_counts != Counter(TARGET_COUNTS):
        raise SelectionError(f"final N count mismatch:{n_counts}")

    repeat_start = {}
    for n in (5, 6):
        stages = [row["stage"] for row in ordered if row["n"] == n and row.get("useIndex") == 2]
        repeat_start[str(n)] = min(stages) if stages else None

    summary = {
        "schema": f"{SCHEMA}_SUMMARY",
        "version": VERSION,
        "status": "PASS",
        "total": len(ordered),
        "nCounts": {str(n): n_counts[n] for n in sorted(n_counts)},
        "nlCounts": {
            f"N{n}L{length}": count for (n, length), count in sorted(nl_counts.items())
        },
        "legacy": legacy_diag,
        "n5": n5_diag,
        "n6": n6_diag,
        "sequence": {
            "firstN5Stage": next(row["stage"] for row in ordered if row["n"] == 5),
            "firstN6Stage": next(row["stage"] for row in ordered if row["n"] == 6),
            "firstRepeatUseStage": repeat_start,
            "maxSameNRun": max_run(row["n"] for row in ordered),
            "maxSameLengthRun": max_run((row["n"], row["chainLength"]) for row in ordered),
            "blockQuotas": [
                {str(n): count for n, count in sorted(block.items())}
                for block in BLOCK_QUOTAS
            ],
        },
        "source": {
            "frozenProduct": frozen_source,
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
        "selectionFingerprint": fp(ids),
    }
    summary["summaryFingerprint"] = fp(summary)

    plan = {
        "schema": SCHEMA,
        "version": VERSION,
        "selectionFingerprint": summary["selectionFingerprint"],
        "summaryFingerprint": summary["summaryFingerprint"],
        "total": len(ordered),
        "order": ordered,
        "repairReservoir": n5_repair + n6_repair,
        "repairContract": {
            "samePairReplacement": "replacement with identical groupToken preserves exact-pair usage",
            "secondUseReserve": "an unused SECOND_USE_RESERVE may replace a removed second-use row for a different group",
            "pairCaps": {"5": 2, "6": 2},
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
