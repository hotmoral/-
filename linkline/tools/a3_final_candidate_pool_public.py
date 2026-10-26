#!/usr/bin/env python3
"""Public-safe deterministic candidate materializer for Linkline A3 final catalog.

This public execution tool deliberately emits no puzzle geometry. It reconstructs
frozen A1 W3 sampling inputs in memory, profiles structural features, and writes
only de-identified research-equivalence IDs plus structural/signature metadata.
Research-isolation filtering remains a private canonical step.
"""
from __future__ import annotations

from collections import Counter, deque
from hashlib import sha256
from itertools import combinations
import argparse
import json
from pathlib import Path

from analysis import a3_structural_features as structural
from reference.m2_state_model import (
    BoardSpecV1,
    ChainSpecV1,
    ChainStateV1,
    GoalSpecV1,
    PuzzleInstanceV1,
    apply_action,
    canonicalize_path,
    legal_actions,
    validate_state,
)
from reference.m3_solver import SearchBudgetV1, SolveStatusV1, solve_puzzle

SCHEMA_VERSION = "1.0.0"
MECHANIC_BASELINE = "a2-v1.0.0"
STATE_CAP = 100_000
A1_SAMPLE_BUDGET = 25_000
SAMPLING_GRAMMAR = "A1_SAMPLING_V1"
CONSTRUCTIVE_REQUESTED = 128
DYNAMIC_REQUESTED = 128
SAMPLER_ATTEMPTS = 4096
CONSTRUCTIVE_NODE_CAP = 2048
GOAL_BASE_STATES = 16

QUOTAS = {
    (3, 3): 18, (3, 4): 38, (3, 5): 44, (3, 6): 26, (3, 7): 33, (3, 8): 1,
    (4, 3): 6, (4, 4): 20, (4, 5): 35, (4, 6): 77, (4, 7): 105,
    (4, 8): 135, (4, 9): 145, (4, 10): 162,
    (5, 6): 60, (5, 7): 60, (5, 8): 40, (5, 9): 50, (5, 10): 50,
    (6, 8): 30, (6, 9): 30, (6, 10): 24, (6, 11): 24, (6, 12): 24,
    (6, 13): 23, (6, 14): 20, (6, 15): 20,
}
TARGET_DOMAINS = tuple(sorted(QUOTAS))

# N3/N4 are deliberately over-materialized so the private isolation/order stage
# can filter research-held identities without another expensive public profile run.
LEGACY_BUFFER_FACTOR = 2.5

REQUIRED_FEATURES = {
    "shortestDistance": "shortestDistance",
    "detourSteps": "shortestMinProximityUpSteps",
    "sideSwitches": "shortestMinRelationalSideSwitches",
    "mandatoryInternalStateCount": "mandatoryInternalStateCount",
    "initialLegalActionCount": "initialLegalActionCount",
    "initialShortestActionCount": "initialShortestActionCount",
}


class MaterializationError(RuntimeError):
    pass


def normalized(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def fingerprint(value) -> str:
    return sha256(normalized(value)).hexdigest()


def transform_cell(n: int, cell: int, transform: int) -> int:
    row, col = divmod(cell, n)
    if transform >= 4:
        col = n - 1 - col
        transform -= 4
    for _ in range(transform):
        row, col = col, n - 1 - row
    return row * n + col


def research_serialization(n: int, length: int, initial, targets) -> str:
    variants = []
    for transform in range(8):
        path = canonicalize_path(
            transform_cell(n, cell, transform) for cell in initial
        )
        goal = tuple(sorted(transform_cell(n, cell, transform) for cell in targets))
        payload = ["LL_A3_RESEARCH_EQ", 1, n, length, list(goal), list(path)]
        variants.append(json.dumps(payload, separators=(",", ":")))
    return min(variants)


def identity(n: int, length: int, initial, targets) -> str:
    return sha256(research_serialization(n, length, initial, targets).encode("utf-8")).hexdigest()


def transitions(n: int, length: int, path):
    board = BoardSpecV1(n)
    chain = ChainSpecV1(length)
    state = ChainStateV1(tuple(path))
    validate_state(board, chain, state)
    rows = []
    for action in legal_actions(board, chain, state):
        result = apply_action(board, chain, state, action)
        if not result.accepted:
            raise MaterializationError("M2 enumerated-action rejection")
        rows.append((action, result.next_state.path))
    return rows


def manhattan(n: int, a: int, b: int) -> int:
    return abs(a // n - b // n) + abs(a % n - b % n)


def necessary_targets(n: int, length: int, targets) -> bool:
    distance = manhattan(n, *targets)
    return distance <= length - 1 and distance % 2 == (length - 1) % 2


def boundary(n: int, cell: int) -> bool:
    return cell // n in (0, n - 1) or cell % n in (0, n - 1)


def rank(*values):
    return sha256(normalized([SAMPLING_GRAMMAR, *values])).digest()


class _ConstructiveGuard(Exception):
    pass


def constructive(n: int, length: int, attempt: int, node_cap: int = CONSTRUCTIVE_NODE_CAP):
    board = BoardSpecV1(n)
    nodes = 0

    def extend(path, mask):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap:
            raise _ConstructiveGuard
        if len(path) == length:
            return ChainStateV1(path).path
        candidates = sorted(
            (cell for cell in board.neighbors(path[-1]) if not mask & (1 << cell)),
            key=lambda cell: (rank("constructive", n, length, attempt, path, cell), cell),
        )
        for cell in candidates:
            result = extend(path + (cell,), mask | (1 << cell))
            if result is not None:
                return result
        return None

    try:
        start = min(
            range(n * n),
            key=lambda cell: (rank("constructive-start", n, length, attempt, cell), cell),
        )
        result = extend((start,), 1 << start)
        if result:
            validate_state(BoardSpecV1(n), ChainSpecV1(length), ChainStateV1(result))
        return result, nodes, False
    except _ConstructiveGuard:
        return None, nodes, True


def dynamic_seed(n: int, length: int):
    path = tuple(
        row * n + col
        for row in range(n)
        for col in (range(n) if row % 2 == 0 else range(n - 1, -1, -1))
    )[:length]
    state = ChainStateV1(path)
    validate_state(BoardSpecV1(n), ChainSpecV1(length), state)
    return state.path


def sample_domain(n: int, length: int):
    all_paths = set()
    constructive_paths = set()
    generated = attempts = node_hits = 0
    for attempt in range(SAMPLER_ATTEMPTS):
        attempts += 1
        path, _, hit = constructive(n, length, attempt)
        node_hits += int(hit)
        if path is not None:
            generated += 1
            constructive_paths.add(path)
        if len(constructive_paths) >= CONSTRUCTIVE_REQUESTED:
            break
    all_paths.update(constructive_paths)
    constructive_diag = {
        "requested": CONSTRUCTIVE_REQUESTED,
        "generated": generated,
        "unique": len(constructive_paths),
        "attempts": attempts,
        "nodeCapHits": node_hits,
    }

    dynamic_paths = set()
    dynamic_seen = set()
    path = dynamic_seed(n, length)
    generated = attempts = 0
    for attempt in range(SAMPLER_ATTEMPTS):
        attempts += 1
        steps = 1 + int.from_bytes(rank("dynamic-steps", n, length, attempt)[:2], "big") % 32
        for step in range(steps):
            row = transitions(n, length, path)
            if not row:
                break
            _, path = min(
                row,
                key=lambda item: (
                    rank(
                        "dynamic", n, length, attempt, step, path,
                        [item[0].source_cell, item[0].destination_cell],
                    ),
                    item[1],
                ),
            )
        generated += 1
        dynamic_seen.add(path)
        if path not in all_paths:
            dynamic_paths.add(path)
        if len(dynamic_paths) >= DYNAMIC_REQUESTED:
            break
    all_paths.update(dynamic_paths)
    dynamic_diag = {
        "requested": DYNAMIC_REQUESTED,
        "generated": generated,
        "unique": len(dynamic_paths),
        "withinFamilyUnique": len(dynamic_seen),
        "overlapWithConstructive": len(dynamic_seen & constructive_paths),
        "attempts": attempts,
    }
    pool = tuple(sorted(all_paths))
    return pool, {
        "n": n,
        "chainLength": length,
        "constructive": constructive_diag,
        "dynamic": dynamic_diag,
        "uniqueTotal": len(pool),
        "poolFingerprint": fingerprint(pool),
    }


def select_states(n: int, length: int, pool, count: int = GOAL_BASE_STATES):
    buckets = {}
    for path in pool:
        descriptor = (
            len(transitions(n, length, path)),
            sum(boundary(n, cell) for cell in (path[0], path[-1])),
        )
        buckets.setdefault(descriptor, []).append(path)
    queues = [
        deque(sorted(buckets[key], key=lambda path: (rank("state-selection", n, length, path), path)))
        for key in sorted(buckets)
    ]
    selected = []
    while queues and len(selected) < count:
        next_queues = []
        for queue in queues:
            if len(selected) < count:
                selected.append(queue.popleft())
            if queue:
                next_queues.append(queue)
        queues = next_queues
    return tuple(selected)


def goal_strata(n: int, length: int, path):
    feasible = [
        target for target in combinations(range(n * n), 2)
        if necessary_targets(n, length, target)
    ]
    distances = sorted({manhattan(n, *target) for target in feasible})
    buckets = {}
    for target in feasible:
        distance = manhattan(n, *target)
        span = min(2, distances.index(distance) * 3 // len(distances))
        placement = (
            "boundary-heavy"
            if all(boundary(n, cell) for cell in target)
            else "interior-available"
        )
        buckets.setdefault((span, placement), []).append(target)
    result = []
    for span in range(3):
        for placement in ("boundary-heavy", "interior-available"):
            options = buckets.get((span, placement), [])
            if options:
                target = min(
                    options,
                    key=lambda target: (
                        rank("goal-stratum", n, length, path, span, placement, target),
                        target,
                    ),
                )
                result.append((span, placement, target))
    return result


def exact_values(profile: dict):
    if profile.get("domainStatus") != "IN_DOMAIN":
        return None
    values = {}
    for output_name, feature_name in REQUIRED_FEATURES.items():
        row = profile.get("features", {}).get(feature_name)
        if not isinstance(row, dict) or row.get("status") != structural.EXACT:
            return None
        value = row.get("value")
        if type(value) is not int or value < 0:
            return None
        values[output_name] = value
    return values


def tier(value: int) -> str:
    return "0" if value == 0 else "1" if value == 1 else "2_PLUS"


def signatures(n: int, length: int, values: dict):
    legal = values["initialLegalActionCount"]
    shortest = values["initialShortestActionCount"]
    if shortest == legal:
        first_choice = "ALL_SHORTEST"
    elif shortest == 1:
        first_choice = "UNIQUE_SHORTEST"
    else:
        first_choice = "MULTI_MIXED"
    format_aware = [
        n, length, values["detourSteps"], values["shortestDistance"],
        values["sideSwitches"], legal, shortest,
        values["mandatoryInternalStateCount"],
    ]
    return {
        "formatAwareFamilyV2": format_aware,
        "crossFormatStructuralV2": format_aware[1:],
        "qualitativeReasoningV2": [
            tier(values["detourSteps"]),
            tier(values["sideSwitches"]),
            tier(values["mandatoryInternalStateCount"]),
            first_choice,
        ],
    }


def roles(n: int, length: int):
    if n == 3:
        return ["N3_FOUNDATION", "N3_ESTABLISHED_RELIEF"]
    if n == 4:
        return ["N4_CORE", "N4_ESTABLISHED_MIX"]
    if n == 5:
        return ["N5_FORMAT_ENTRY", "N5_ESTABLISHED"] if length in (6, 7) else ["N5_ESTABLISHED"]
    if n == 6:
        if length in (8, 9):
            return ["N6_LOW_DENSITY_ENTRY", "N6_ESTABLISHED"]
        if length in (14, 15):
            return ["N6_ESTABLISHED", "N6_DENSITY_TAIL"]
        return ["N6_ESTABLISHED"]
    raise MaterializationError("unsupported N")


def candidate_row(identifier: str, n: int, length: int, values: dict, source: dict):
    return {
        "id": identifier,
        "n": n,
        "chainLength": length,
        "structural": values,
        "podm": {
            "modelId": "PODM-1.0.0",
            "supportStatus": "IN_TESTED_NL_DOMAIN" if n in (3, 4) else "OUTSIDE_TESTED_NL_DOMAIN",
            "score": length + 2 * values["detourSteps"] if n in (3, 4) else None,
        },
        "roleEligibility": roles(n, length),
        "signatures": signatures(n, length, values),
        "source": source,
    }


def enumerate_canonical_paths(n: int, length: int):
    board = BoardSpecV1(n)
    found = set()

    def visit(path, used):
        if len(path) == length:
            found.add(canonicalize_path(path))
            return
        for destination in board.neighbors(path[-1]):
            if destination in used:
                continue
            used.add(destination)
            path.append(destination)
            visit(path, used)
            path.pop()
            used.remove(destination)

    for start in range(n * n):
        visit([start], {start})
    return tuple(sorted(found))


def domain_universe(n: int, length: int):
    by_id = {}
    target_pairs = tuple(combinations(range(n * n), 2))
    for path in enumerate_canonical_paths(n, length):
        endpoint_set = frozenset((path[0], path[-1]))
        for target in target_pairs:
            if frozenset(target) == endpoint_set:
                continue
            serialization = research_serialization(n, length, path, target)
            identifier = sha256(serialization.encode("utf-8")).hexdigest()
            if identifier in by_id:
                continue
            _, _, cn, cl, ct, ci = json.loads(serialization)
            by_id[identifier] = (ci, ct)
    return tuple((identifier, *by_id[identifier]) for identifier in sorted(by_id))


def profile_identity(n: int, length: int, initial, targets):
    profile = structural.analyze_structural_features(
        n, length, initial, targets, state_cap=STATE_CAP
    )
    return exact_values(profile)


def materialize_legacy_domain(n: int, length: int, target_count: int):
    universe = domain_universe(n, length)
    rows = []
    attempts = 0
    for source_rank, (identifier, initial, targets) in enumerate(universe):
        attempts += 1
        values = profile_identity(n, length, initial, targets)
        if values is None:
            continue
        rows.append(
            candidate_row(
                identifier,
                n,
                length,
                values,
                {"sourceKind": "PUBLIC_CANONICAL_UNIVERSE", "sourceRank": source_rank},
            )
        )
        if len(rows) >= target_count:
            break
    return rows, {
        "universeCount": len(universe),
        "profileAttempts": attempts,
        "exactRows": len(rows),
        "requestedRows": target_count,
    }


def reconstruct_w3_domain(n: int, length: int):
    pool, sample_diag = sample_domain(n, length)
    states = select_states(n, length, pool)
    status_counts = Counter()
    by_id = {}
    record_count = 0
    for state_rank, initial in enumerate(states):
        for span, placement, targets in goal_strata(n, length, initial):
            record_count += 1
            instance = PuzzleInstanceV1(
                BoardSpecV1(n),
                ChainSpecV1(length),
                GoalSpecV1(*targets),
                ChainStateV1(initial),
            )
            run = solve_puzzle(instance, SearchBudgetV1(A1_SAMPLE_BUDGET))
            status = run.result.status.value
            status_counts[status] += 1
            if run.result.status is not SolveStatusV1.SOLVED:
                continue
            identifier = identity(n, length, initial, targets)
            if identifier not in by_id:
                by_id[identifier] = {
                    "initial": initial,
                    "targets": targets,
                    "distance": run.result.shortest_distance,
                    "stateRank": state_rank,
                    "span": span,
                    "placement": placement,
                }
    source = tuple((identifier, by_id[identifier]) for identifier in sorted(by_id))
    return source, {
        **sample_diag,
        "selectedStateCount": len(states),
        "goalRecordCount": record_count,
        "goalStatusCounts": dict(sorted(status_counts.items())),
        "solvedUniqueIdentityCount": len(source),
        "sourceIdentityFingerprint": fingerprint([identifier for identifier, _ in source]),
    }


def materialize_expanded_domain(n: int, length: int):
    source, diag = reconstruct_w3_domain(n, length)
    rows = []
    exact_failures = 0
    for source_rank, (identifier, item) in enumerate(source):
        values = profile_identity(n, length, item["initial"], item["targets"])
        if values is None:
            exact_failures += 1
            continue
        if values["shortestDistance"] != item["distance"]:
            raise MaterializationError(
                f"A1/A3 distance mismatch N{n}L{length} id={identifier}"
            )
        rows.append(
            candidate_row(
                identifier,
                n,
                length,
                values,
                {
                    "sourceKind": "A1_W3_PUBLIC_RECONSTRUCTION",
                    "sourceRank": source_rank,
                },
            )
        )
    diag["exactProfileRows"] = len(rows)
    diag["exactProfileFailures"] = exact_failures
    return rows, diag


def summarize(rows):
    nl = Counter((row["n"], row["chainLength"]) for row in rows)
    n = Counter(row["n"] for row in rows)
    format_families = {tuple(row["signatures"]["formatAwareFamilyV2"]) for row in rows}
    cross_families = {tuple(row["signatures"]["crossFormatStructuralV2"]) for row in rows}
    qualitative = {tuple(row["signatures"]["qualitativeReasoningV2"]) for row in rows}
    return {
        "rowCount": len(rows),
        "nCounts": {str(key): value for key, value in sorted(n.items())},
        "nlCounts": {f"N{key[0]}L{key[1]}": value for key, value in sorted(nl.items())},
        "formatAwareUniqueFamilyCount": len(format_families),
        "crossFormatUniqueFamilyCount": len(cross_families),
        "qualitativeSignatureCount": len(qualitative),
        "poolFingerprint": fingerprint([
            [
                row["id"], row["n"], row["chainLength"], row["structural"],
                row["podm"], row["roleEligibility"], row["signatures"], row["source"],
            ]
            for row in rows
        ]),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("public_output/a3_final_candidate_pool_v1"))
    args = parser.parse_args()

    if sum(QUOTAS.values()) != 1300:
        raise MaterializationError("frozen quota sum mismatch")

    rows = []
    domain_diags = []
    for n, length in TARGET_DOMAINS:
        if n in (3, 4):
            requested = max(2, int(QUOTAS[(n, length)] * LEGACY_BUFFER_FACTOR + 0.999999))
            domain_rows, diag = materialize_legacy_domain(n, length, requested)
        else:
            domain_rows, diag = materialize_expanded_domain(n, length)
        rows.extend(domain_rows)
        domain_diags.append({"n": n, "chainLength": length, **diag})
        print(json.dumps({
            "domain": f"N{n}L{length}",
            "rows": len(domain_rows),
            "quota": QUOTAS[(n, length)],
        }, sort_keys=True), flush=True)

    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise MaterializationError("cross-domain identity duplicate")
    rows.sort(key=lambda row: (row["n"], row["chainLength"], row["id"]))

    pool = {
        "schema": "LINKLINE_A3_PUBLIC_FINAL_CANDIDATE_POOL",
        "version": SCHEMA_VERSION,
        "mechanicBaseline": MECHANIC_BASELINE,
        "privacy": {
            "containsPuzzleGeometry": False,
            "containsHumanOrSelfTestExport": False,
            "containsPrivateIsolationList": False,
            "requiresPrivateIsolationBeforeFinalSelection": True,
        },
        "frozenQuotaByNL": {f"N{n}L{length}": QUOTAS[(n, length)] for n, length in TARGET_DOMAINS},
        "rows": rows,
    }
    summary = {
        "schema": "LINKLINE_A3_PUBLIC_FINAL_CANDIDATE_POOL_SUMMARY",
        "version": SCHEMA_VERSION,
        "samplingContract": {
            "grammar": SAMPLING_GRAMMAR,
            "constructiveRequested": CONSTRUCTIVE_REQUESTED,
            "dynamicRequested": DYNAMIC_REQUESTED,
            "maxAttempts": SAMPLER_ATTEMPTS,
            "constructiveNodeCap": CONSTRUCTIVE_NODE_CAP,
            "goalBaseStates": GOAL_BASE_STATES,
            "sampleExpansionBudget": A1_SAMPLE_BUDGET,
        },
        "domains": domain_diags,
        "pool": summarize(rows),
    }
    summary["summaryFingerprint"] = fingerprint(summary)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "candidate_pool.json").write_text(
        json.dumps(pool, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": "PASS",
        "rowCount": summary["pool"]["rowCount"],
        "poolFingerprint": summary["pool"]["poolFingerprint"],
        "summaryFingerprint": summary["summaryFingerprint"],
        "nlCounts": summary["pool"]["nlCounts"],
    }, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
