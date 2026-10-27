#!/usr/bin/env python3
"""Public-safe geometry/solver validation for the A3 target-pair v3 plan.

The validator reconstructs geometry transiently for the already-public selected
1,300 rows and the already-public repair reservoir, verifies research identity,
reference-solves every candidate, and audits target-pair semantics. It persists
summary counts/fingerprints only: no puzzle geometry, target coordinates, private
isolation IDs, human data, or self-test data are written.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path

import tools.a3_final_candidate_pool_public as base
import tools.a3_final_candidate_pool_reuse_v2 as reuse
import tools.a3_target_pair_selection_plan_v1 as v1
from reference.m2_state_model import (
    BoardSpecV1,
    ChainSpecV1,
    ChainStateV1,
    GoalSpecV1,
    PuzzleInstanceV1,
)
from reference.m3_solver import SolveStatusV1, solve_puzzle

SCHEMA = "LINKLINE_A3_TARGET_PAIR_PUBLIC_CANDIDATE_VALIDATION_V1"
PLAN_SCHEMA = "LINKLINE_A3_TARGET_PAIR_1300_PUBLIC_SELECTION_PLAN_V3"
SELECTION_FP = "1fc7dd15893a113935b0b1b2f5ca636e22669d783e887f90e56203275d3c3131"
SUMMARY_FP = "d1f3c0e5e7f7542bacba4f08843963cfe4d6169f9f3f941ec88f9db0c4c3a3c9"
EXPECTED_SELECTED = 1300
EXPECTED_RESERVOIR = 1961
PAIR_CAPS = {3: 1, 4: 1, 5: 2, 6: 2}


class ValidationError(RuntimeError):
    pass


def fp(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(payload).hexdigest()


def oriented(n: int, values, transform: int):
    return tuple(base.transform_cell(n, int(cell), transform) for cell in values)


def build_legacy_index():
    by_id = {}
    for identifier, n, length, initial, targets in reuse.legacy_universe():
        if n not in (3, 4):
            continue
        item = (int(n), int(length), tuple(initial), tuple(sorted(targets)))
        prior = by_id.get(identifier)
        if prior is not None and prior != item:
            raise ValidationError(f"legacy identity collision:{identifier}")
        by_id[identifier] = item
    return by_id


def build_expanded_domain(n: int, length: int):
    state_count = v1.STATE_COUNTS[n]
    pool, _diag = base.sample_domain(n, length)
    states = base.select_states(n, length, pool, count=state_count)
    geometry = v1.reconstruct_geometry_index(n, length, state_count)
    result = {}
    for identifier, item in geometry.items():
        rank = item["stateRank"]
        if not 0 <= rank < len(states):
            raise ValidationError(f"expanded state rank outside selected states:N{n}L{length}")
        result[identifier] = (
            n,
            length,
            tuple(states[rank]),
            tuple(sorted(item["targets"])),
        )
    return result


def materialize(row: dict, legacy, expanded_cache):
    identifier = row.get("id")
    n = int(row.get("n"))
    length = int(row.get("chainLength"))
    if n in (3, 4):
        item = legacy.get(identifier)
        if item is None:
            raise ValidationError(f"legacy identity not reconstructable:{identifier}")
        if item[0] != n or item[1] != length:
            raise ValidationError(f"legacy N/L provenance mismatch:{identifier}")
        transform = row.get("orientationTransform")
        if type(transform) is not int or not 0 <= transform < 8:
            raise ValidationError(f"legacy orientation missing/invalid:{identifier}")
        initial = oriented(n, item[2], transform)
        targets = tuple(sorted(oriented(n, item[3], transform)))
    elif n in (5, 6):
        key = (n, length)
        if key not in expanded_cache:
            expanded_cache[key] = build_expanded_domain(n, length)
        item = expanded_cache[key].get(identifier)
        if item is None:
            raise ValidationError(f"expanded identity not reconstructable:{identifier}")
        initial = item[2]
        targets = item[3]
    else:
        raise ValidationError(f"unexpected board size:{n}")

    actual = base.identity(n, length, initial, targets)
    if actual != identifier:
        raise ValidationError(f"research identity mismatch:{identifier}")
    return n, length, tuple(initial), tuple(sorted(targets))


def solve_geometry(n: int, length: int, initial, targets):
    instance = PuzzleInstanceV1(
        BoardSpecV1(n),
        ChainSpecV1(length),
        GoalSpecV1(*targets),
        ChainStateV1(tuple(initial)),
    )
    run = solve_puzzle(instance)
    if run.result.status is not SolveStatusV1.SOLVED:
        raise ValidationError(f"reference solver non-SOLVED:N{n}L{length}")
    return run.result.shortest_distance, run.diagnostics.expanded_state_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan.get("schema") != PLAN_SCHEMA:
        raise ValidationError("unexpected plan schema")
    if plan.get("selectionFingerprint") != SELECTION_FP:
        raise ValidationError("selection fingerprint mismatch")
    if plan.get("summaryFingerprint") != SUMMARY_FP:
        raise ValidationError("summary fingerprint mismatch")

    selected = plan.get("order", [])
    reservoir = plan.get("repairReservoir", [])
    if len(selected) != EXPECTED_SELECTED:
        raise ValidationError(f"selected count mismatch:{len(selected)}")
    if len(reservoir) != EXPECTED_RESERVOIR:
        raise ValidationError(f"reservoir count mismatch:{len(reservoir)}")
    for stage, row in enumerate(selected, start=1):
        if row.get("stage") != stage:
            raise ValidationError("selected stage order is not contiguous")

    legacy = build_legacy_index()
    expanded_cache = {}
    selected_pair_by_id = {}
    selected_pair_usage = {n: Counter() for n in PAIR_CAPS}
    group_pairs = defaultdict(set)
    solved = 0
    solver_expanded = 0
    max_shortest = 0
    identity_rows = []

    # Validate selected rows first so direct-replacement checks can reference the
    # exact displayed pair without ever persisting coordinates.
    for index, row in enumerate(selected, start=1):
        n, length, initial, targets = materialize(row, legacy, expanded_cache)
        shortest, expanded = solve_geometry(n, length, initial, targets)
        solved += 1
        solver_expanded += expanded
        max_shortest = max(max_shortest, shortest)
        pair = tuple(sorted(targets))
        selected_pair_by_id[row["id"]] = pair
        selected_pair_usage[n][pair] += 1
        if n in (5, 6):
            token = row.get("groupToken")
            if not token:
                raise ValidationError(f"selected expanded row missing groupToken:{row['id']}")
            group_pairs[(n, token)].add(pair)
        identity_rows.append(["selected", index, row["id"], n, length, shortest])
        if index % 100 == 0:
            print(json.dumps({"phase":"selected","validated":index,"solved":solved}), flush=True)

    direct_repair_checked = 0
    for index, row in enumerate(reservoir, start=1):
        n, length, initial, targets = materialize(row, legacy, expanded_cache)
        shortest, expanded = solve_geometry(n, length, initial, targets)
        solved += 1
        solver_expanded += expanded
        max_shortest = max(max_shortest, shortest)
        pair = tuple(sorted(targets))

        replacement_for = row.get("replacementForId")
        if replacement_for:
            expected = selected_pair_by_id.get(replacement_for)
            if expected is None:
                raise ValidationError(f"replacementForId not in selected set:{replacement_for}")
            if pair != expected:
                raise ValidationError(f"oriented exact-pair replacement mismatch:{row['id']}")
            if row.get("purpose") != "ORIENTED_SAME_EXACT_PAIR_REPLACEMENT":
                raise ValidationError(f"unexpected oriented repair purpose:{row['id']}")
            direct_repair_checked += 1

        if n in (5, 6):
            token = row.get("groupToken")
            if not token:
                raise ValidationError(f"expanded reservoir row missing groupToken:{row['id']}")
            group_pairs[(n, token)].add(pair)
        identity_rows.append(["reserve", index, row["id"], n, length, shortest])
        if index % 100 == 0:
            print(json.dumps({"phase":"reservoir","validated":index,"solved":solved}), flush=True)

    expected_total = EXPECTED_SELECTED + EXPECTED_RESERVOIR
    if solved != expected_total:
        raise ValidationError(f"solver count mismatch:{solved}!={expected_total}")

    pair_audit = {}
    for n, cap in PAIR_CAPS.items():
        usage = selected_pair_usage[n]
        max_use = max(usage.values(), default=0)
        if max_use > cap:
            raise ValidationError(f"selected pair cap exceeded N{n}:{max_use}>{cap}")
        if n == 3 and (len(usage) != 36 or max_use != 1):
            raise ValidationError("N3 exact-pair coverage mismatch")
        if n == 4 and (len(usage) != 120 or max_use != 1):
            raise ValidationError("N4 exact-pair coverage mismatch")
        pair_audit[str(n)] = {
            "uniquePairCount": len(usage),
            "maxPairUse": max_use,
            "pairCap": cap,
        }

    group_pair_violations = sum(1 for values in group_pairs.values() if len(values) != 1)
    if group_pair_violations:
        raise ValidationError(f"groupToken maps to multiple target pairs:{group_pair_violations}")

    expected_direct = 36 + 120
    if direct_repair_checked != expected_direct:
        raise ValidationError(
            f"oriented direct repair coverage mismatch:{direct_repair_checked}!={expected_direct}"
        )

    summary = {
        "schema": SCHEMA,
        "version": "1.0.0",
        "status": "PASS",
        "sourceSelectionFingerprint": SELECTION_FP,
        "sourceSummaryFingerprint": SUMMARY_FP,
        "selectedRowsValidated": EXPECTED_SELECTED,
        "repairReservoirRowsValidated": EXPECTED_RESERVOIR,
        "totalRowsValidated": expected_total,
        "researchIdentityChecksPassed": expected_total,
        "solver": {
            "solved": solved,
            "nonSolved": 0,
            "aggregateExpandedStates": solver_expanded,
            "maxShortestDistance": max_shortest,
        },
        "orientedExactPairReplacementChecks": direct_repair_checked,
        "groupTokenPairConsistency": {
            "groupsChecked": len(group_pairs),
            "violations": group_pair_violations,
        },
        "selectedPairAudit": pair_audit,
        "validationFingerprint": fp(identity_rows),
        "privacy": {
            "containsPuzzleGeometry": False,
            "containsTargetCoordinates": False,
            "containsExactTargetPairCoordinateKeys": False,
            "containsPrivateIsolationIds": False,
            "containsHumanOrSelfTestData": False,
        },
        "boundaries": {
            "privateIsolationApplied": False,
            "privateRepairApplied": False,
            "productionCatalogModified": False,
        },
    }
    summary["summaryFingerprint"] = fp(summary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
