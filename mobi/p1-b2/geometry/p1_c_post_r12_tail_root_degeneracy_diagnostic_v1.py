from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

VERSION = "P1_C_POST_R12_TAIL_ROOT_DEGENERACY_DIAGNOSTIC_V1"
DECISION_TOKEN = "POST_R12_TAIL_ROOT_OBSERVATIONAL_DIAGNOSTIC_SELECTED"
CONTRACT_TOKEN = "POST_R12_TAIL_ROOT_DEGENERACY_DIAGNOSTIC_CONTRACT_FROZEN"
PREFLIGHT_TOKEN = "POST_R12_TAIL_ROOT_DEGENERACY_DIAGNOSTIC_PREFLIGHT_PASS"
FREEZE_TOKEN = "POST_R12_TAIL_ROOT_DEGENERACY_DIAGNOSTIC_IMPLEMENTATION_FREEZE"

EXPECTED_R12_SHA256 = "fc4096162607dbf59859749562ec5ab9ea7d0e09551aa7cd3cd1ad05e9f5594c"
EXPECTED_R12_GIT_BLOB_SHA1 = "837f4abe7ff474a527893b099be8087a104f7aaa"
EXPECTED_R12_VERSION = "P1_C_R12_SURFACE_TERMINAL_BIND_ALIAS_V1"
EXPECTED_R11_SHA256 = "af2d8ccafb1878ad96cf6fae60167ae2a33f82480aa76710ce97c8fd95a6ad87"
EXPECTED_SOURCE_SHA256 = "6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5"
EXPECTED_V3125_SHA256 = "839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77"

KNOWN_DEGENERATE_EDGE = ("PELVIS_CTRL", "TAIL_ROOT_CTRL")
TAIL_ROLES = (
    "TAIL_ROOT_CTRL", "TAIL_1_CTRL", "TAIL_2_CTRL",
    "TAIL_3_CTRL", "TAIL_4_CTRL", "TAIL_TIP_CTRL",
)
DOWNSTREAM_TAIL_ROLES = TAIL_ROLES[1:]
WEIGHT_AUDIT_ROLES = ("PELVIS_CTRL",) + TAIL_ROLES
COUNTERFACTUAL_PROBE_NAMES = ("TAIL_ROOT_TO_TAIL_1", "TAIL_PATH_FORWARD")
CLASSIFICATION_PRECEDENCE = (
    "BROADER_ZERO_LENGTH_HIERARCHY_DEGENERACY",
    "COINCIDENT_BRANCH_ROOT_WITH_TAIL_SUPPORT_DEFECT",
    "COINCIDENT_BRANCH_ROOT_WITH_NONVACUOUS_TAIL_SUPPORT",
    "MIXED_OR_UNRESOLVED",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def stable_json(obj) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=True, separators=(",", ": ")) + "\n").encode("utf-8")


def sha256_u64_indices(indices: np.ndarray) -> str:
    arr = np.asarray(indices, dtype="<u8", order="C")
    return hashlib.sha256(arr.tobytes(order="C")).hexdigest()


def load_r12(geometry_dir: Path):
    path = geometry_dir / "p1_c_r12_surface_terminal_bind_alias_v1.py"
    if not path.is_file():
        raise RuntimeError("frozen R12 adapter missing")
    actual_sha = sha256_file(path)
    actual_blob = git_blob_sha1(path)
    if actual_sha != EXPECTED_R12_SHA256:
        raise RuntimeError(f"R12 adapter SHA drift: {actual_sha}")
    if actual_blob != EXPECTED_R12_GIT_BLOB_SHA1:
        raise RuntimeError(f"R12 adapter blob drift: {actual_blob}")
    spec = importlib.util.spec_from_file_location("mobi_r12_frozen_for_post_r12_diag", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import frozen R12 adapter")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    if getattr(mod, "VERSION", None) != EXPECTED_R12_VERSION:
        raise RuntimeError(f"R12 version drift: {getattr(mod, 'VERSION', None)}")
    if getattr(mod, "EXPECTED_R11_IMPLEMENTATION_SHA256", None) != EXPECTED_R11_SHA256:
        raise RuntimeError("R12 inherited R11 SHA identity drift")
    if getattr(mod, "EXPECTED_V3125_MESH_SHA256", None) != EXPECTED_V3125_SHA256:
        raise RuntimeError("R12 inherited V3125 identity drift")
    return mod


def controls_by_role(controls) -> dict:
    return {c.role: c for c in controls}


def axis_from_tangent(tangent: np.ndarray) -> np.ndarray:
    tangent = np.asarray(tangent, dtype=np.float64)
    n = float(np.linalg.norm(tangent))
    if n <= 1e-15:
        raise RuntimeError("zero diagnostic tangent")
    t = tangent / n
    basis = min(np.eye(3), key=lambda b: abs(float(np.dot(t, b))))
    axis = np.cross(t, basis)
    an = float(np.linalg.norm(axis))
    if an <= 1e-15:
        raise RuntimeError("zero diagnostic axis")
    return axis / an


def role_weight_vector(r11, role: str, indices: np.ndarray, weights: np.ndarray) -> np.ndarray:
    ridx = int(r11.ROLE_INDEX[role])
    return np.where(indices == ridx, weights, 0.0).sum(axis=1)


def hierarchy_edge_audit(r11, controls, pitch: float, body_height: float) -> dict:
    by = controls_by_role(controls)
    edges = []
    for role in r11.ROLE_ORDER:
        parent = by[role].parent
        if parent is None:
            continue
        p0 = np.asarray(by[parent].position, dtype=np.float64)
        p1 = np.asarray(by[role].position, dtype=np.float64)
        vector = p1 - p0
        length = float(np.linalg.norm(vector))
        edges.append({
            "role": role,
            "parent": parent,
            "parentPositionR10": p0.tolist(),
            "controlPositionR10": p1.tolist(),
            "vectorR10": vector.tolist(),
            "lengthR10": length,
            "lengthPitch": float(length / pitch),
            "lengthBodyHeight": float(length / body_height),
            "exactTupleEqual": tuple(by[parent].position) == tuple(by[role].position),
            "diagnosticDegenerateLE1e15": bool(length <= 1e-15),
        })
    if len(edges) != 29:
        raise RuntimeError(f"hierarchy edge count drift: {len(edges)}")
    known = [x for x in edges if (x["parent"], x["role"]) == KNOWN_DEGENERATE_EDGE]
    if len(known) != 1:
        raise RuntimeError("known pelvis->tail-root hierarchy edge missing or duplicated")
    additional = [
        x for x in edges
        if (x["parent"], x["role"]) != KNOWN_DEGENERATE_EDGE
        and x["diagnosticDegenerateLE1e15"]
    ]
    exact_additional = [
        x for x in edges
        if (x["parent"], x["role"]) != KNOWN_DEGENERATE_EDGE
        and x["exactTupleEqual"]
    ]
    return {
        "edgeCount": len(edges),
        "edges": edges,
        "knownPelvisTailRoot": known[0],
        "additionalDiagnosticDegenerateEdgeCount": len(additional),
        "additionalDiagnosticDegenerateEdges": [
            {"parent": x["parent"], "role": x["role"], "lengthR10": x["lengthR10"]}
            for x in additional
        ],
        "additionalExactCoincidentEdgeCount": len(exact_additional),
        "additionalExactCoincidentEdges": [
            {"parent": x["parent"], "role": x["role"]}
            for x in exact_additional
        ],
    }


def _incident_edges(r11, graph, node, transform, pitch: float) -> list[dict]:
    p0 = np.asarray(r11.index_to_world(node, transform), dtype=np.float64)
    out = []
    for neighbor in sorted(graph[node]):
        p1 = np.asarray(r11.index_to_world(neighbor, transform), dtype=np.float64)
        d = float(np.linalg.norm(p1 - p0))
        out.append({
            "neighborGridNode": list(neighbor),
            "neighborWorldR10": p1.tolist(),
            "edgeLengthR10": d,
            "edgeLengthPitch": float(d / pitch),
        })
    return out


def medial_graph_topology_audit(r11, graph, snapped, nodes, paths, transform, pitch: float) -> dict:
    pelvis = nodes["PELVIS"]
    tail_root = nodes["TAIL_ROOT"]
    pelvis_world = np.asarray(r11.index_to_world(pelvis, transform), dtype=np.float64)
    tail_root_world = np.asarray(r11.index_to_world(tail_root, transform), dtype=np.float64)

    tail_to_head = r11.shortest_path(graph, snapped["TAIL_TIP"], nodes["HEAD"], pitch)[0]
    pelvis_to_head = r11.shortest_path(graph, nodes["PELVIS"], nodes["HEAD"], pitch)[0]
    all_paths = dict(paths)
    all_paths["TAIL_TO_HEAD_DIAGNOSTIC"] = tail_to_head
    all_paths["PELVIS_TO_HEAD_DIAGNOSTIC"] = pelvis_to_head

    def membership(node):
        return {name: bool(node in path) for name, path in sorted(all_paths.items())}

    return {
        "pelvis": {
            "gridNode": list(pelvis),
            "worldR10": pelvis_world.tolist(),
            "graphDegree": int(len(graph[pelvis])),
            "incidentEdges": _incident_edges(r11, graph, pelvis, transform, pitch),
            "pathMembership": membership(pelvis),
            "selectionRule": "pair_merge_node(HIND_L,HIND_R,closest_sum_to_hind_endpoints)",
        },
        "tailRoot": {
            "gridNode": list(tail_root),
            "worldR10": tail_root_world.tolist(),
            "graphDegree": int(len(graph[tail_root])),
            "incidentEdges": _incident_edges(r11, graph, tail_root, transform, pitch),
            "pathMembership": membership(tail_root),
            "selectionRule": "first_merge_from_tail(tail_to_head,pelvis_to_head,minimum_tail_graph_distance)",
        },
        "sameExactGraphNode": bool(pelvis == tail_root),
        "sameExactWorldCoordinate": bool(np.array_equal(pelvis_world, tail_root_world)),
    }


def tail_path_spacing_audit(r11, controls, paths, transform, pitch: float, body_height: float) -> dict:
    by = controls_by_role(controls)
    path_nodes = paths["TAIL"]
    world = np.asarray(r11.path_world(path_nodes, transform), dtype=np.float64)
    seg = np.linalg.norm(np.diff(world, axis=0), axis=1)
    arc = float(seg.sum())

    root = np.asarray(by["TAIL_ROOT_CTRL"].position, dtype=np.float64)
    first_distinct_index = None
    for i in range(1, len(world)):
        if float(np.linalg.norm(world[i] - root)) > 0.0:
            first_distinct_index = i
            break
    if first_distinct_index is None:
        raise RuntimeError("tail path has no distinct point after root")
    first = world[first_distinct_index]
    forward = first - root
    forward_distance = float(np.linalg.norm(forward))

    controls_json = {role: list(by[role].position) for role in TAIL_ROLES}
    consecutive = []
    for a, b in zip(TAIL_ROLES[:-1], TAIL_ROLES[1:]):
        pa = np.asarray(by[a].position, dtype=np.float64)
        pb = np.asarray(by[b].position, dtype=np.float64)
        vec = pb - pa
        dist = float(np.linalg.norm(vec))
        consecutive.append({
            "from": a,
            "to": b,
            "vectorR10": vec.tolist(),
            "distanceR10": dist,
            "distancePitch": float(dist / pitch),
            "distanceBodyHeight": float(dist / body_height),
            "exactTupleEqual": tuple(by[a].position) == tuple(by[b].position),
        })

    coincidences = []
    for i, a in enumerate(TAIL_ROLES):
        for b in TAIL_ROLES[i + 1:]:
            if tuple(by[a].position) == tuple(by[b].position):
                coincidences.append([a, b])

    return {
        "graphNodeCount": int(len(path_nodes)),
        "arcLengthR10": arc,
        "arcLengthPitch": float(arc / pitch),
        "arcLengthBodyHeight": float(arc / body_height),
        "firstPathGridNode": list(path_nodes[0]),
        "firstPathWorldR10": world[0].tolist(),
        "firstDistinctPathIndex": int(first_distinct_index),
        "firstDistinctPathGridNode": list(path_nodes[first_distinct_index]),
        "firstDistinctPathWorldR10": first.tolist(),
        "firstNonzeroForwardVectorR10": forward.tolist(),
        "firstNonzeroForwardDistanceR10": forward_distance,
        "firstNonzeroForwardDistancePitch": float(forward_distance / pitch),
        "tailControlsR10": controls_json,
        "consecutiveControlSpacing": consecutive,
        "exactCoordinateCoincidencesAmongTailControls": coincidences,
    }


def role_support_report(r11, role: str, vertices: np.ndarray, controls, indices, weights, domains, interfaces) -> dict:
    by = controls_by_role(controls)
    rv = role_weight_vector(r11, role, indices, weights)
    support = np.flatnonzero(rv > 0.0)
    vals = rv[support]
    bind = np.asarray(by[role].position, dtype=np.float64)
    distances = np.linalg.norm(vertices[support] - bind, axis=1) if len(support) else np.asarray([], dtype=np.float64)
    domain_counts = {d: int(np.count_nonzero(domains[support] == d)) for d in r11.DOMAIN_ORDER}
    expected_domain = str(r11.ROLE_DOMAIN[role])
    support_domains_match_own = bool(
        len(support) > 0 and all(str(domains[i]) == expected_domain for i in support)
    )
    support_weight_eligibility_allowed = bool(
        len(support) > 0
        and all(role in r11.allowed_roles(str(domains[i]), bool(interfaces[i])) for i in support)
    )
    interface_count = int(np.count_nonzero(interfaces[support])) if len(support) else 0
    return {
        "role": role,
        "bindPositionR10": bind.tolist(),
        "expectedRoleDomain": expected_domain,
        "positiveWeightSupportCount": int(len(support)),
        "maxNormalizedWeight": float(vals.max()) if len(vals) else 0.0,
        "sumPositiveWeights": float(vals.sum()) if len(vals) else 0.0,
        "meanPositiveWeight": float(vals.mean()) if len(vals) else 0.0,
        "supportCountByFinalVertexDomain": domain_counts,
        "interfaceSupportCount": interface_count,
        "nonInterfaceSupportCount": int(len(support) - interface_count),
        "distanceToBindR10": {
            "min": float(distances.min()) if len(distances) else None,
            "max": float(distances.max()) if len(distances) else None,
            "mean": float(distances.mean()) if len(distances) else None,
        },
        "supportVertexIndices": [int(x) for x in support.tolist()],
        "supportVertexIndicesSha256LEU64": sha256_u64_indices(support),
        "supportDomainsMatchOwnRoleDomain": support_domains_match_own,
        "supportWeightEligibilityAllowed": support_weight_eligibility_allowed,
    }


def weight_support_audit(r11, vertices, controls, indices, weights, domains, interfaces) -> dict:
    reports = {
        role: role_support_report(r11, role, vertices, controls, indices, weights, domains, interfaces)
        for role in WEIGHT_AUDIT_ROLES
    }
    support_sets = {role: set(reports[role]["supportVertexIndices"]) for role in WEIGHT_AUDIT_ROLES}
    consecutive = {}
    for a, b in zip(TAIL_ROLES[:-1], TAIL_ROLES[1:]):
        consecutive[f"{a}->{b}"] = int(len(support_sets[a] & support_sets[b]))

    p = support_sets["PELVIS_CTRL"]
    t = support_sets["TAIL_ROOT_CTRL"]
    inter = p & t
    union = p | t
    return {
        "roles": reports,
        "consecutiveTailSupportIntersectionCounts": consecutive,
        "pelvisVsTailRoot": {
            "supportIntersectionCount": int(len(inter)),
            "pelvisOnlyCount": int(len(p - t)),
            "tailRootOnlyCount": int(len(t - p)),
            "supportUnionCount": int(len(union)),
            "jaccardOverlap": float(len(inter) / len(union)) if union else None,
            "supportSetsExactlyEqual": bool(p == t),
            "domainRoleGatingProducesDistinctSupport": bool(p != t),
        },
    }


def tail_weighted_arc_audit(r11, indices, weights, tail_info) -> dict:
    tail_frac = np.asarray(tail_info[1], dtype=np.float64)
    centroids = {}
    supports = {}
    role_reports = {}
    for role in TAIL_ROLES:
        rv = role_weight_vector(r11, role, indices, weights)
        support = np.flatnonzero(rv > 0.0)
        supports[role] = set(int(x) for x in support.tolist())
        centroid = float(np.average(tail_frac[support], weights=rv[support])) if len(support) else None
        centroids[role] = centroid
        role_reports[role] = {
            "positiveWeightSupportCount": int(len(support)),
            "weightedTailPathArcCentroid": centroid,
        }

    ordering_pairs = []
    strict_order = True
    for a, b in zip(TAIL_ROLES[:-1], TAIL_ROLES[1:]):
        ca, cb = centroids[a], centroids[b]
        ok = bool(ca is not None and cb is not None and ca < cb)
        ordering_pairs.append({"from": a, "to": b, "strictlyIncreasing": ok})
        strict_order = strict_order and ok

    overlap_pairs = []
    all_overlap = True
    for a, b in zip(TAIL_ROLES[:-1], TAIL_ROLES[1:]):
        n = len(supports[a] & supports[b])
        ok = n > 0
        overlap_pairs.append({"from": a, "to": b, "intersectionCount": int(n), "nonempty": ok})
        all_overlap = all_overlap and ok

    return {
        "controls": role_reports,
        "centroids": centroids,
        "strictRootToTipCentroidOrdering": bool(strict_order),
        "centroidOrderingPairs": ordering_pairs,
        "allAdjacentPositiveSupportOverlap": bool(all_overlap),
        "adjacentSupportOverlapPairs": overlap_pairs,
    }


def differential_probe(r11, role: str, axis: np.ndarray, vertices, controls, indices, weights, domains) -> dict:
    by = controls_by_role(controls)
    ridx = int(r11.ROLE_INDEX[role])
    bind = np.asarray(by[role].position, dtype=np.float64)
    h = float(r11.body_metrics(vertices)["height"])
    disp = np.zeros(len(vertices), dtype=np.float64)
    for i, v in enumerate(vertices):
        slots = np.where(indices[i] == ridx)[0]
        if len(slots) == 0:
            continue
        wt = float(weights[i, int(slots[0])])
        rotated = bind + r11.rodrigues(v - bind, axis, r11.JACOBIAN_EPSILON_RAD)
        d = wt * (rotated - v)
        disp[i] = np.linalg.norm(d) / (r11.JACOBIAN_EPSILON_RAD * h)
    support = np.where(disp > r11.JACOBIAN_DERIVATIVE_THRESHOLD)[0]
    expected_domain = str(r11.ROLE_DOMAIN[role])
    confined = bool(
        len(support) > 0
        and (expected_domain == "CORE" or all(str(domains[i]) == expected_domain for i in support))
    )
    return {
        "role": role,
        "axisR10": np.asarray(axis, dtype=np.float64).tolist(),
        "supportCount": int(len(support)),
        "maxNormalizedDerivative": float(disp[support].max()) if len(support) else 0.0,
        "expectedRoleDomain": expected_domain,
        "supportDomainConfined": confined,
        "supportVertexIndices": [int(x) for x in support.tolist()],
        "supportVertexIndicesSha256LEU64": sha256_u64_indices(support),
        "epsilonRad": float(r11.JACOBIAN_EPSILON_RAD),
        "derivativeThreshold": float(r11.JACOBIAN_DERIVATIVE_THRESHOLD),
    }


def downstream_tail_jacobian_audit(r11, vertices, controls, indices, weights, domains) -> dict:
    by = controls_by_role(controls)
    out = {}
    for role in DOWNSTREAM_TAIL_ROLES:
        parent = by[role].parent
        p = np.asarray(by[role].position, dtype=np.float64)
        pp = np.asarray(by[parent].position, dtype=np.float64)
        tangent = p - pp
        tangent_norm = float(np.linalg.norm(tangent))
        entry = {
            "role": role,
            "parent": parent,
            "parentTangentR10": tangent.tolist(),
            "parentTangentNorm": tangent_norm,
            "diagnosticAxisDefined": False,
            "failure": None,
        }
        try:
            axis = np.asarray(r11.diagnostic_axis(role, by), dtype=np.float64)
            probe = differential_probe(r11, role, axis, vertices, controls, indices, weights, domains)
            entry.update(probe)
            entry["diagnosticAxisDefined"] = True
            entry["passesFrozenDeadAndDomainGate"] = bool(
                probe["supportCount"] > 0 and probe["supportDomainConfined"]
            )
        except RuntimeError as exc:
            entry["failure"] = str(exc)
            entry["passesFrozenDeadAndDomainGate"] = False
        out[role] = entry
    return {
        "controls": out,
        "allDownstreamTailControlsPassFrozenDeadAndDomainGate": bool(
            all(out[r]["passesFrozenDeadAndDomainGate"] for r in DOWNSTREAM_TAIL_ROLES)
        ),
    }


def tail_root_counterfactual_probes(r11, vertices, controls, indices, weights, domains, tail_path_report) -> dict:
    by = controls_by_role(controls)
    root = np.asarray(by["TAIL_ROOT_CTRL"].position, dtype=np.float64)
    tail1 = np.asarray(by["TAIL_1_CTRL"].position, dtype=np.float64)
    first_path = np.asarray(tail_path_report["firstDistinctPathWorldR10"], dtype=np.float64)
    tangents = {
        "TAIL_ROOT_TO_TAIL_1": tail1 - root,
        "TAIL_PATH_FORWARD": first_path - root,
    }
    if tuple(tangents) != COUNTERFACTUAL_PROBE_NAMES:
        raise RuntimeError("counterfactual probe vocabulary/order drift")

    out = {}
    for name in COUNTERFACTUAL_PROBE_NAMES:
        tangent = np.asarray(tangents[name], dtype=np.float64)
        n = float(np.linalg.norm(tangent))
        entry = {
            "probe": name,
            "tangentR10": tangent.tolist(),
            "tangentNorm": n,
            "defined": bool(n > 1e-15),
            "failure": None,
            "nonzeroAllowedDomainDifferentialSupport": False,
        }
        if n <= 1e-15:
            entry["failure"] = "undefined tangent under frozen <=1e-15 criterion"
            out[name] = entry
            continue
        try:
            axis = axis_from_tangent(tangent)
            probe = differential_probe(r11, "TAIL_ROOT_CTRL", axis, vertices, controls, indices, weights, domains)
            entry.update(probe)
            entry["nonzeroAllowedDomainDifferentialSupport"] = bool(
                probe["supportCount"] > 0 and probe["supportDomainConfined"]
            )
        except RuntimeError as exc:
            entry["failure"] = str(exc)
        out[name] = entry
    return {
        "probes": out,
        "probeNamesExact": list(COUNTERFACTUAL_PROBE_NAMES),
        "anyDefinedProbeHasNonzeroAllowedDomainDifferentialSupport": bool(
            any(
                out[n]["defined"] and out[n]["nonzeroAllowedDomainDifferentialSupport"]
                for n in COUNTERFACTUAL_PROBE_NAMES
            )
        ),
        "bothProbesDefined": bool(all(out[n]["defined"] for n in COUNTERFACTUAL_PROBE_NAMES)),
    }


def classify_diagnostic(hierarchy, graph_topology, weights_report, tail_arc, downstream, probes) -> dict:
    if hierarchy["additionalDiagnosticDegenerateEdgeCount"] > 0:
        return {
            "primary": "BROADER_ZERO_LENGTH_HIERARCHY_DEGENERACY",
            "reasons": ["additional hierarchy edge satisfies frozen diagnostic degeneracy criterion"],
            "precedence": list(CLASSIFICATION_PRECEDENCE),
        }

    same_branch = bool(
        graph_topology["sameExactGraphNode"]
        and graph_topology["sameExactWorldCoordinate"]
    )
    tail_root = weights_report["roles"]["TAIL_ROOT_CTRL"]
    tail_root_weight_ok = bool(
        tail_root["positiveWeightSupportCount"] > 0
        and tail_root["supportDomainsMatchOwnRoleDomain"]
        and tail_root["supportWeightEligibilityAllowed"]
    )
    ordered = bool(tail_arc["strictRootToTipCentroidOrdering"])
    overlap = bool(tail_arc["allAdjacentPositiveSupportOverlap"])
    downstream_ok = bool(downstream["allDownstreamTailControlsPassFrozenDeadAndDomainGate"])
    any_probe_ok = bool(probes["anyDefinedProbeHasNonzeroAllowedDomainDifferentialSupport"])
    both_defined = bool(probes["bothProbesDefined"])

    defects = []
    if same_branch:
        if not tail_root_weight_ok:
            defects.append("tail-root frozen final weight support absent or domain-invalid")
        if not ordered:
            defects.append("tail weighted-arc centroid ordering failed")
        if not overlap:
            defects.append("adjacent tail positive-support overlap failed")
        if not downstream_ok:
            defects.append("one or more downstream tail controls failed unchanged parent-axis audit")
        if both_defined and not any_probe_ok:
            defects.append("both predeclared tail-root probes defined but neither showed allowed-domain differential support")
    if same_branch and defects:
        return {
            "primary": "COINCIDENT_BRANCH_ROOT_WITH_TAIL_SUPPORT_DEFECT",
            "reasons": defects,
            "precedence": list(CLASSIFICATION_PRECEDENCE),
        }

    if same_branch and tail_root_weight_ok and ordered and overlap and downstream_ok and any_probe_ok:
        return {
            "primary": "COINCIDENT_BRANCH_ROOT_WITH_NONVACUOUS_TAIL_SUPPORT",
            "reasons": [
                "pelvis and tail root are the same exact medial-graph node and coordinate",
                "no additional hierarchy-edge degeneracy found",
                "tail-root final frozen weight support is positive and domain-confined",
                "tail weighted-arc centroids are strictly ordered root-to-tip",
                "all adjacent tail supports overlap",
                "TAIL_1..TAIL_TIP pass unchanged parent-axis differential/domain gates",
                "at least one predeclared tail-root counterfactual probe shows allowed-domain differential support",
            ],
            "precedence": list(CLASSIFICATION_PRECEDENCE),
            "interpretationCeiling": (
                "Neutral frozen Stage-1 observables show a structurally non-vacuous coincident "
                "tail-root and localize the blocker enough to consider a separate diagnostic-axis "
                "change-control; this is not R12 PASS or finite-angle/natural-tail proof."
            ),
        }

    unresolved = []
    if not same_branch:
        unresolved.append("pelvis/tail-root exact same branch-node condition not confirmed")
    if same_branch and not any_probe_ok and not (both_defined and not any_probe_ok):
        unresolved.append("counterfactual root-probe evidence insufficient under predeclared defect rule")
    if not unresolved:
        unresolved.append("predeclared positive/defect conditions do not uniquely resolve the case")
    return {
        "primary": "MIXED_OR_UNRESOLVED",
        "reasons": unresolved,
        "precedence": list(CLASSIFICATION_PRECEDENCE),
    }


def reconstruct_exact_r12_state(source_glb: Path, geometry_dir: Path) -> dict:
    r12 = load_r12(geometry_dir)
    r11 = r12.load_r11(geometry_dir)
    if sha256_file(source_glb) != EXPECTED_SOURCE_SHA256:
        raise RuntimeError("source SHA drift")
    v, f, identity = r11.reproduce_v3125(source_glb, geometry_dir)
    if str(identity.get("meshArraySha256", "")) != EXPECTED_V3125_SHA256:
        raise RuntimeError("V3125 mesh identity drift")
    frame = r11.frame_sign_audit(v, geometry_dir)
    if frame.get("anatomicalLeftSign") != "+X_R10":
        raise RuntimeError("frame/sign drift")

    skel, transform, pitch = r11.voxel_skeleton(v, f)
    raw_graph = r11.graph_from_skeleton(skel)
    graph, snapped, nodes, paths = r11.derive_semantic_graph(v, raw_graph, transform, pitch)
    r11_controls, path_worlds = r11.make_controls(transform, nodes, paths)
    aliases = r12.derive_surface_terminal_aliases(v, r11)
    r12_controls = r12.replace_paw_bind_controls(r11, r11_controls, aliases)
    delta = r12.delta_audit(r11, r11_controls, r12_controls, path_worlds, aliases)

    domains, interfaces, domain_info, polylines = r11.derive_domains(v, path_worlds, pitch)
    indices, weights = r11.build_weights(v, r12_controls, domains, interfaces, pitch)
    weight_global = r11.weight_audit(indices, weights, domains, interfaces)
    alias_gate = r12.alias_semantic_weight_gate(r11, v, aliases, domains, indices, weights)

    return {
        "r12": r12,
        "r11": r11,
        "vertices": v,
        "faces": f,
        "identity": identity,
        "frame": frame,
        "transform": transform,
        "pitch": float(pitch),
        "rawGraph": raw_graph,
        "graph": graph,
        "snapped": snapped,
        "nodes": nodes,
        "paths": paths,
        "pathWorlds": path_worlds,
        "r11Controls": r11_controls,
        "r12Controls": r12_controls,
        "aliases": aliases,
        "delta": delta,
        "domains": domains,
        "interfaces": interfaces,
        "domainInfo": domain_info,
        "polylines": polylines,
        "indices": indices,
        "weights": weights,
        "weightGlobalAudit": weight_global,
        "aliasGate": alias_gate,
    }


def control_snapshot(r11, controls) -> list[dict]:
    return [{
        "ordinal": int(r11.ROLE_INDEX[c.role] + 1),
        "role": c.role,
        "parent": c.parent,
        "domain": c.domain,
        "positionR10": list(c.position),
        "provenance": c.provenance,
        "derivation": c.derivation,
    } for c in controls]


def run_diagnostic(source_glb: Path, geometry_dir: Path, out_file: Path) -> dict:
    s = reconstruct_exact_r12_state(source_glb, geometry_dir)
    r11 = s["r11"]
    v, f = s["vertices"], s["faces"]
    controls = s["r12Controls"]
    pitch = float(s["pitch"])
    h = float(r11.body_metrics(v)["height"])

    mesh_before = r11.mesh_array_sha256(v, f)
    weight_bytes_before = r11.serialize_weights(s["indices"], s["weights"])
    weight_sha_before = hashlib.sha256(weight_bytes_before).hexdigest()
    controls_before = stable_json(control_snapshot(r11, controls))
    control_sha_before = hashlib.sha256(controls_before).hexdigest()

    hierarchy = hierarchy_edge_audit(r11, controls, pitch, h)
    graph_topology = medial_graph_topology_audit(
        r11, s["graph"], s["snapped"], s["nodes"], s["paths"], s["transform"], pitch
    )
    tail_path = tail_path_spacing_audit(r11, controls, s["paths"], s["transform"], pitch, h)
    support = weight_support_audit(
        r11, v, controls, s["indices"], s["weights"], s["domains"], s["interfaces"]
    )
    tail_arc = tail_weighted_arc_audit(r11, s["indices"], s["weights"], s["domainInfo"]["TAIL"])
    downstream = downstream_tail_jacobian_audit(
        r11, v, controls, s["indices"], s["weights"], s["domains"]
    )
    probes = tail_root_counterfactual_probes(
        r11, v, controls, s["indices"], s["weights"], s["domains"], tail_path
    )
    classification = classify_diagnostic(hierarchy, graph_topology, support, tail_arc, downstream, probes)

    mesh_after = r11.mesh_array_sha256(v, f)
    weight_sha_after = hashlib.sha256(r11.serialize_weights(s["indices"], s["weights"])).hexdigest()
    control_sha_after = hashlib.sha256(stable_json(control_snapshot(r11, controls))).hexdigest()
    mutation_free = bool(
        mesh_before == mesh_after == EXPECTED_V3125_SHA256
        and weight_sha_before == weight_sha_after
        and control_sha_before == control_sha_after
    )
    if not mutation_free:
        raise RuntimeError("diagnostic mutated frozen mesh/control/weight state")

    result = {
        "version": VERSION,
        "decisionToken": DECISION_TOKEN,
        "contractToken": CONTRACT_TOKEN,
        "preflightToken": PREFLIGHT_TOKEN,
        "freezeTokenRequired": FREEZE_TOKEN,
        "classification": classification,
        "identity": {
            "sourceSha256": sha256_file(source_glb),
            "v3125": s["identity"],
            "r11ImplementationSha256": EXPECTED_R11_SHA256,
            "r12AdapterSha256": EXPECTED_R12_SHA256,
            "r12AdapterGitBlobSha1": EXPECTED_R12_GIT_BLOB_SHA1,
            "controlSnapshotSha256": control_sha_before,
            "weightSerializationSha256": weight_sha_before,
            "controlCount": len(controls),
            "roleOrder": list(r11.ROLE_ORDER),
            "frameSign": s["frame"],
            "r12CausalDelta": s["delta"],
            "globalWeightAudit": s["weightGlobalAudit"],
            "aliasSemanticWeightGate": s["aliasGate"],
            "mutationFreeBeforeAfter": mutation_free,
        },
        "controlSnapshot": control_snapshot(r11, controls),
        "hierarchyEdgeAudit": hierarchy,
        "medialGraphTopologyAudit": graph_topology,
        "tailPathAndControlSpacingAudit": tail_path,
        "frozenWeightSupportAudit": support,
        "tailWeightedArcAudit": tail_arc,
        "downstreamTailJacobianAudit": downstream,
        "tailRootCounterfactualProbes": probes,
        "nonGoals": [
            "not R12 Stage-1 rerun",
            "not R12 PASS",
            "not tail-root repair",
            "not production diagnostic-axis selection",
            "not finite pose, IK, gait, animation, or runtime skinning evidence",
        ],
    }
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_bytes(stable_json(result))
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_glb", type=Path)
    ap.add_argument("--geometry-dir", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    result = run_diagnostic(args.source_glb, args.geometry_dir, args.out)
    print(json.dumps(result["classification"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
