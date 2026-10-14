from __future__ import annotations

from collections import Counter, deque
from hashlib import sha256
import copy
import json
from typing import Any, Dict, List, Optional, Tuple

MODEL_VERSION = "einstein-u4-p05-public-abstract-model-1.0.0"
SUPPORTED_TARGET = "SOLVED_TERMINAL"
DEFAULT_CONTEXT = {
    "root": "A",
    "profile": "FULL",
    "assist": "OFF",
    "opportunityVersion": "1.0.0",
    "transitionVersion": "1.0.0",
    "runtimeVersion": "1.0.0",
    "claim": "PEC2-P05",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return sha256(canonical_json(value).encode("utf-8")).hexdigest()


def rank(state: Dict[str, Any]) -> int:
    return int(state["raw_bits"]) + (int(state["fact_universe"]) - int(state["facts"]))


def state_identity(state: Dict[str, Any]) -> str:
    # Hash is only an index/checksum. Verifier still compares exact state content.
    return digest(state)


def edge_identity(edge: Dict[str, Any]) -> Tuple[str, str, str, str, str, str]:
    return (
        edge["source"],
        edge["destination"],
        edge["opportunity"]["id"],
        canonical_json(edge["opportunity"]["alternatives"]),
        canonical_json(edge["opportunity"]["premises"]),
        canonical_json(edge["step"]),
    )


def expected_classification(world: Dict[str, Any], state_id: str) -> str:
    state = world["states"][state_id]
    if state["guard"]:
        return "GUARD"
    if state["solved"]:
        return "SOLVED"
    if world["outgoing"].get(state_id, []):
        return "EXPAND"
    return "STALLED"


def reachable(world: Dict[str, Any]) -> List[str]:
    seen = set()
    order: List[str] = []
    queue = deque([world["context"]["root"]])
    while queue:
        sid = queue.popleft()
        if sid in seen:
            continue
        if sid not in world["states"]:
            raise ValueError(f"world references unknown state {sid}")
        seen.add(sid)
        order.append(sid)
        cls = expected_classification(world, sid)
        if cls != "EXPAND":
            continue
        for edge in world["outgoing"].get(sid, []):
            queue.append(edge["destination"])
    return order


def make_evidence(world: Dict[str, Any], *, target: Optional[str] = SUPPORTED_TARGET) -> Dict[str, Any]:
    nodes: Dict[str, Any] = {}
    for sid in reachable(world):
        state = copy.deepcopy(world["states"][sid])
        nodes[sid] = {
            "state": state,
            "stateHash": state_identity(state),
            "classification": expected_classification(world, sid),
            "outgoing": copy.deepcopy(world["outgoing"].get(sid, [])),
        }

    independent_target = independent_target_result(world, target)
    return {
        "modelVersion": MODEL_VERSION,
        "context": copy.deepcopy(world["context"]),
        "nodes": nodes,
        "frontier": [],
        "targetPredicate": target,
        "producerTargetResult": independent_target,
    }


def independent_target_result(world: Dict[str, Any], target: Optional[str]) -> str:
    if target is None:
        return "NOT_APPLICABLE"
    if target != SUPPORTED_TARGET:
        return "UNSUPPORTED"
    any_solved = any(world["states"][sid]["solved"] for sid in reachable(world))
    return "REFUTED" if any_solved else "PROVED"


def _reject(reason: str) -> Dict[str, str]:
    return {"admissibility": "REJECTED", "closure": "UNPROVED", "absence": "UNKNOWN", "reason": reason}


def verify(world: Dict[str, Any], evidence: Dict[str, Any]) -> Dict[str, str]:
    if evidence.get("modelVersion") != MODEL_VERSION:
        return _reject("model-version")
    if evidence.get("context") != world["context"]:
        return _reject("context-mismatch")

    target = evidence.get("targetPredicate")
    if target not in (None, SUPPORTED_TARGET):
        return _reject("unsupported-target")

    canonical_reachable = reachable(world)
    canonical_set = set(canonical_reachable)
    nodes = evidence.get("nodes")
    frontier = evidence.get("frontier")
    if not isinstance(nodes, dict) or not isinstance(frontier, list):
        return _reject("malformed-container")
    frontier_set = set(frontier)
    if len(frontier_set) != len(frontier):
        return _reject("duplicate-frontier")
    if not frontier_set.issubset(canonical_set):
        return _reject("foreign-frontier")

    submitted_set = set(nodes)
    if submitted_set - canonical_set:
        return _reject("extra-node")

    missing = canonical_set - submitted_set
    if missing - frontier_set:
        return _reject("omitted-node")

    # Exact state content, checksum, terminal precedence, outgoing edge multiset,
    # and concrete rank decrease are all checked independently.
    for sid in canonical_reachable:
        if sid in frontier_set:
            continue
        node = nodes[sid]
        canonical_state = world["states"][sid]
        if node.get("state") != canonical_state:
            return _reject(f"exact-state:{sid}")
        if node.get("stateHash") != state_identity(node["state"]):
            return _reject(f"state-hash:{sid}")

        expected_cls = expected_classification(world, sid)
        if node.get("classification") != expected_cls:
            return _reject(f"classification:{sid}")

        submitted_edges = node.get("outgoing")
        if not isinstance(submitted_edges, list):
            return _reject(f"malformed-edges:{sid}")
        expected_edges = world["outgoing"].get(sid, [])
        if Counter(map(edge_identity, submitted_edges)) != Counter(map(edge_identity, expected_edges)):
            return _reject(f"edge-multiset:{sid}")

        for edge in submitted_edges:
            if edge.get("source") != sid:
                return _reject(f"edge-source:{sid}")
            dest = edge.get("destination")
            if dest not in world["states"]:
                return _reject(f"edge-destination:{sid}")
            # Full opportunity/step content equality is already bound by edge multiset.
            # Check rank independently to reject unsupported cycle/non-progress.
            if rank(world["states"][dest]) >= rank(canonical_state):
                return _reject(f"nondecreasing-rank:{sid}->{dest}")

    if frontier_set:
        return {
            "admissibility": "ADMISSIBLE",
            "closure": "INCOMPLETE",
            "absence": "UNKNOWN",
            "reason": "unresolved-frontier",
        }

    independent = independent_target_result(world, target)
    if evidence.get("producerTargetResult") != independent:
        return _reject("producer-target-result")

    if target is None:
        return {
            "admissibility": "ADMISSIBLE",
            "closure": "PROVED",
            "absence": "NOT_APPLICABLE",
            "reason": "closure-only",
        }

    return {
        "admissibility": "ADMISSIBLE",
        "closure": "PROVED",
        "absence": independent,
        "reason": "independent-target-scan",
    }


def base_world() -> Dict[str, Any]:
    # Fully synthetic public-safe graph. Two parallel provenance edges A->B are
    # intentional so the harness can detect provenance loss while allowing
    # destination expansion deduplication.
    states = {
        "A": {"raw_bits": 5, "facts": 0, "fact_universe": 10, "guard": False, "solved": False, "payload": ["root"]},
        "B": {"raw_bits": 3, "facts": 1, "fact_universe": 10, "guard": False, "solved": False, "payload": ["stalled"]},
        "G": {"raw_bits": 4, "facts": 1, "fact_universe": 10, "guard": True, "solved": False, "payload": ["guard"]},
    }

    def edge(edge_id: str, dest: str, provenance: str) -> Dict[str, Any]:
        return {
            "source": "A",
            "destination": dest,
            "opportunity": {
                "id": edge_id,
                "alternatives": [f"alt:{edge_id}", f"alt2:{edge_id}"],
                "premises": [f"premise:{provenance}"],
                "consequences": [f"consequence:{edge_id}"],
                "provenance": provenance,
            },
            "step": {
                "skill": "SYNTHETIC_PRODUCTIVE",
                "opportunityId": edge_id,
                "provenance": provenance,
                "destination": dest,
            },
        }

    outgoing = {
        "A": [
            edge("E1", "B", "P1"),
            edge("E2", "B", "P2"),
            edge("E3", "G", "P3"),
        ],
        "B": [],
        "G": [],
    }
    return {"context": copy.deepcopy(DEFAULT_CONTEXT), "states": states, "outgoing": outgoing}


def solved_world() -> Dict[str, Any]:
    world = base_world()
    world["states"] = {
        "A": copy.deepcopy(world["states"]["A"]),
        "S": {"raw_bits": 3, "facts": 1, "fact_universe": 10, "guard": False, "solved": True, "payload": ["solved"]},
    }
    world["outgoing"] = {
        "A": [{
            "source": "A",
            "destination": "S",
            "opportunity": {
                "id": "ES",
                "alternatives": ["alt:ES"],
                "premises": ["premise:ES"],
                "consequences": ["consequence:ES"],
                "provenance": "PS",
            },
            "step": {
                "skill": "SYNTHETIC_PRODUCTIVE",
                "opportunityId": "ES",
                "provenance": "PS",
                "destination": "S",
            },
        }],
        "S": [],
    }
    return world


def clone(value: Any) -> Any:
    return copy.deepcopy(value)
