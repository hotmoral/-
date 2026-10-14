from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional
import copy

from model import SUPPORTED_TARGET, base_world, solved_world, make_evidence, verify, state_identity


@dataclass(frozen=True)
class Case:
    case_id: str
    expected_admissibility: str
    expected_closure: str
    expected_absence: str
    build: Callable[[], tuple[Dict[str, Any], Dict[str, Any]]]


def _base(target: Optional[str] = SUPPORTED_TARGET):
    world = base_world()
    return world, make_evidence(world, target=target)


def _solved(target: Optional[str] = SUPPORTED_TARGET):
    world = solved_world()
    return world, make_evidence(world, target=target)


def _mutate(builder, fn):
    world, evidence = builder()
    world = copy.deepcopy(world)
    evidence = copy.deepcopy(evidence)
    fn(world, evidence)
    return world, evidence


def _case(case_id, a, c, p, builder):
    return Case(case_id, a, c, p, builder)


def cases() -> List[Case]:
    out: List[Case] = []

    # Frozen/adversarial semantic controls (public-safe synthetic realizations).
    out.append(_case("G009_VALID_CLOSURE_ABSENCE", "ADMISSIBLE", "PROVED", "PROVED", _base))

    out.append(_case(
        "G010_OMITTED_OUTGOING_EDGE", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, lambda w, e: e["nodes"]["A"]["outgoing"].pop())
    ))

    out.append(_case(
        "G011_OMITTED_SOLVED_TERMINAL", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_solved, lambda w, e: e["nodes"].pop("S"))
    ))

    out.append(_case(
        "G012_GUARD_MISCLASSIFIED_STALLED", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, lambda w, e: e["nodes"]["G"].__setitem__("classification", "STALLED"))
    ))

    def cycle_injection(w, e):
        edge = copy.deepcopy(e["nodes"]["A"]["outgoing"][0])
        edge["source"] = "B"
        edge["destination"] = "A"
        edge["opportunity"]["id"] = "CYCLE"
        edge["step"]["opportunityId"] = "CYCLE"
        edge["step"]["destination"] = "A"
        e["nodes"]["B"]["outgoing"].append(edge)
    out.append(_case(
        "G013_UNSUPPORTED_CYCLE", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, cycle_injection)
    ))

    out.append(_case(
        "G016_PROFILE_MISMATCH", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, lambda w, e: e["context"].__setitem__("profile", "ABLATED"))
    ))

    out.append(_case(
        "G035_HISTORY_SENSITIVE_LAUNDERING", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, lambda w, e: e.__setitem__("targetPredicate", "HISTORY_REVISIT"))
    ))

    def forged_hash(w, e):
        e["nodes"]["B"]["state"]["payload"] = ["forged"]
        e["nodes"]["B"]["stateHash"] = state_identity(e["nodes"]["B"]["state"])
    out.append(_case(
        "G037_SELF_CONSISTENT_FORGED_HASH", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, forged_hash)
    ))

    def frontier(w, e):
        e["nodes"].pop("B")
        e["frontier"] = ["B"]
    out.append(_case(
        "G047_UNRESOLVED_FRONTIER", "ADMISSIBLE", "INCOMPLETE", "UNKNOWN",
        lambda: _mutate(_base, frontier)
    ))

    # Positive controls that pin closure-vs-absence semantics.
    out.append(_case(
        "P001_CLOSURE_ONLY_NULL_TARGET", "ADMISSIBLE", "PROVED", "NOT_APPLICABLE",
        lambda: _base(target=None)
    ))
    out.append(_case(
        "P002_REACHABLE_SOLVED_REFUTES_ABSENCE", "ADMISSIBLE", "PROVED", "REFUTED",
        _solved
    ))

    # Implementation mutation controls.
    def extra_edge(w, e):
        injected = copy.deepcopy(e["nodes"]["A"]["outgoing"][0])
        injected["opportunity"]["id"] = "EXTRA"
        injected["step"]["opportunityId"] = "EXTRA"
        e["nodes"]["A"]["outgoing"].append(injected)
    out.append(_case(
        "M001_EXTRA_EDGE", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, extra_edge)
    ))

    def reorder(w, e):
        e["nodes"]["A"]["outgoing"] = list(reversed(e["nodes"]["A"]["outgoing"]))
    out.append(_case(
        "M002_REORDERED_COMPLETE_EDGE_MULTISET", "ADMISSIBLE", "PROVED", "PROVED",
        lambda: _mutate(_base, reorder)
    ))

    def parallel_loss(w, e):
        e["nodes"]["A"]["outgoing"] = [
            edge for edge in e["nodes"]["A"]["outgoing"] if edge["opportunity"]["id"] != "E2"
        ]
    out.append(_case(
        "M003_PARALLEL_EDGE_LOSS", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, parallel_loss)
    ))

    def exact_state_tamper(w, e):
        e["nodes"]["B"]["state"]["raw_bits"] = 2
        e["nodes"]["B"]["stateHash"] = state_identity(e["nodes"]["B"]["state"])
    out.append(_case(
        "M004_EXACT_STATE_TAMPER", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, exact_state_tamper)
    ))

    def destination_tamper(w, e):
        e["nodes"]["A"]["outgoing"][0]["destination"] = "G"
        e["nodes"]["A"]["outgoing"][0]["step"]["destination"] = "G"
    out.append(_case(
        "M005_DESTINATION_TAMPER", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, destination_tamper)
    ))

    def opportunity_tamper(w, e):
        e["nodes"]["A"]["outgoing"][0]["opportunity"]["premises"] = ["tampered"]
    out.append(_case(
        "M006_OPPORTUNITY_TAMPER", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, opportunity_tamper)
    ))

    def step_tamper(w, e):
        e["nodes"]["A"]["outgoing"][0]["step"]["skill"] = "FORGED_SKILL"
    out.append(_case(
        "M007_HUMAN_STEP_TAMPER", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, step_tamper)
    ))

    out.append(_case(
        "M008_FALSE_STALLED", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, lambda w, e: e["nodes"]["A"].__setitem__("classification", "STALLED"))
    ))

    out.append(_case(
        "M009_STALE_ROOT", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, lambda w, e: e["context"].__setitem__("root", "B"))
    ))
    out.append(_case(
        "M010_STALE_PROFILE", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, lambda w, e: e["context"].__setitem__("profile", "OLD_FULL"))
    ))
    out.append(_case(
        "M011_STALE_ASSIST", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, lambda w, e: e["context"].__setitem__("assist", "ON"))
    ))
    out.append(_case(
        "M012_STALE_VERSION", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, lambda w, e: e["context"].__setitem__("transitionVersion", "0.9.0"))
    ))

    out.append(_case(
        "M013_TARGET_RESULT_TAMPER", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, lambda w, e: e.__setitem__("producerTargetResult", "REFUTED"))
    ))

    def nondecreasing_rank(w, e):
        # Preserve exact submitted/canonical edge equality while creating a
        # synthetic "legitimate-looking" model whose productive edge violates FD01.
        w["states"]["B"]["raw_bits"] = 6
        e2 = make_evidence(w)
        e.clear()
        e.update(e2)
    out.append(_case(
        "M014_NONDECREASING_RANK_INJECTION", "REJECTED", "UNPROVED", "UNKNOWN",
        lambda: _mutate(_base, nondecreasing_rank)
    ))

    assert len(out) == 25, len(out)
    return out


def run_all() -> List[Dict[str, Any]]:
    results = []
    for case in cases():
        world, evidence = case.build()
        actual = verify(world, evidence)
        passed = (
            actual["admissibility"] == case.expected_admissibility
            and actual["closure"] == case.expected_closure
            and actual["absence"] == case.expected_absence
        )
        results.append({
            "id": case.case_id,
            "expected": {
                "admissibility": case.expected_admissibility,
                "closure": case.expected_closure,
                "absence": case.expected_absence,
            },
            "actual": actual,
            "pass": passed,
        })
    return results
