#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

EXPECTED_MESH_SHA = "839968886420707267d0e546c080f1af62c262391bf5e7a13babdbec1be32d77"
EXPECTED_VERTEX_COUNT = 3125
EXPECTED_FACE_COUNT = 6246
PAW_ROLES = (
    "FORE_L_PAW_CTRL",
    "FORE_R_PAW_CTRL",
    "HIND_L_PAW_CTRL",
    "HIND_R_PAW_CTRL",
)
ANCHOR_FOR_ROLE = {
    "FORE_L_PAW_CTRL": "FORE_L_PAW",
    "FORE_R_PAW_CTRL": "FORE_R_PAW",
    "HIND_L_PAW_CTRL": "HIND_L_PAW",
    "HIND_R_PAW_CTRL": "HIND_R_PAW",
}


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("mobi_r11_frozen", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import frozen R11 implementation: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def vec(x):
    return [float(v) for v in np.asarray(x, dtype=np.float64).tolist()]


def f64(x):
    return float(x)


def qstats(values: np.ndarray):
    values = np.asarray(values, dtype=np.float64)
    if len(values) == 0:
        return None
    q = np.quantile(values, [0.0, 0.05, 0.25, 0.50, 0.75, 0.95, 1.0])
    return {
        "min": f64(q[0]),
        "q05": f64(q[1]),
        "q25": f64(q[2]),
        "q50": f64(q[3]),
        "q75": f64(q[4]),
        "q95": f64(q[5]),
        "max": f64(q[6]),
    }


def role_weight(indices, weights, vertex_index: int, role_index: int) -> float:
    slots = np.where(indices[vertex_index] == role_index)[0]
    if len(slots) == 0:
        return 0.0
    return float(weights[vertex_index, int(slots[0])])


def differential_support(r11, vertices, controls, indices, weights, role: str):
    by = {c.role: c for c in controls}
    ridx = r11.ROLE_INDEX[role]
    axis = r11.diagnostic_axis(role, by)
    bind = np.asarray(by[role].position, dtype=np.float64)
    h = r11.body_metrics(vertices)["height"]
    disp = np.zeros(len(vertices), dtype=np.float64)
    for i, vertex in enumerate(vertices):
        slots = np.where(indices[i] == ridx)[0]
        if len(slots) == 0:
            continue
        wt = float(weights[i, int(slots[0])])
        if wt == 0.0:
            continue
        rotated = bind + r11.rodrigues(vertex - bind, axis, r11.JACOBIAN_EPSILON_RAD)
        delta = wt * (rotated - vertex)
        disp[i] = np.linalg.norm(delta) / (r11.JACOBIAN_EPSILON_RAD * h)
    support = np.where(disp > r11.JACOBIAN_DERIVATIVE_THRESHOLD)[0]
    return axis, disp, support


def candidate_table(r11, vertex, domain: str, interface: bool, controls, pitch: float):
    positions = {c.role: np.asarray(c.position, dtype=np.float64) for c in controls}
    sigma = r11.WEIGHT_SIGMA_PITCHES * pitch
    candidates = []
    for role in r11.allowed_roles(domain, interface):
        distance = float(np.linalg.norm(vertex - positions[role]))
        raw = 1.0 / (distance * distance + sigma * sigma)
        candidates.append((-raw, int(r11.ROLE_INDEX[role]), role, raw, distance))
    candidates.sort()
    top = candidates[: r11.MAX_INFLUENCES]
    total = sum(x[3] for x in top)
    out = []
    for rank, item in enumerate(candidates, start=1):
        _neg, ordinal, role, raw, distance = item
        retained = rank <= r11.MAX_INFLUENCES
        out.append(
            {
                "rank": rank,
                "role": role,
                "roleIndex": ordinal,
                "rawScore": float(raw),
                "distanceToControl": float(distance),
                "retained": retained,
                "normalizedWeight": float(raw / total) if retained else 0.0,
            }
        )
    return out


def classify_paw(radius, nearest_surface, local_count, eligible_count, retained_count, differential_within):
    labels = []
    if nearest_surface > radius:
        labels.append("BIND_SURFACE_SEPARATION")
    else:
        if local_count > 0 and eligible_count == 0:
            labels.append("LOCAL_DOMAIN_EXCLUSION")
        elif eligible_count > 0 and retained_count == 0:
            labels.append("TOP4_LOCAL_EVICTION")
        elif retained_count > 0 and differential_within == 0:
            labels.append("DERIVATIVE_THRESHOLD_LOSS")
    if differential_within > 0:
        return ["PASS_LOCAL_SUPPORT"]
    if not labels:
        labels.append("UNRESOLVED_BY_REQUIRED_MEASUREMENTS")
    return labels


def cross_side_classification(paws):
    failed = [role for role in PAW_ROLES if paws[role]["differentialSupportWithinRadiusCount"] == 0]
    s = set(failed)
    if s == {"FORE_L_PAW_CTRL"}:
        label = "LEFT_FORE_SPECIFIC"
    elif s == {"FORE_L_PAW_CTRL", "FORE_R_PAW_CTRL"}:
        label = "FORELIMB_PAIR_SYSTEMATIC"
    elif s == set(PAW_ROLES):
        label = "ALL_PAW_SYSTEMATIC"
    elif len(s) > 1:
        label = "ASYMMETRIC_MULTI_PAW"
    elif len(s) == 0:
        label = "NO_PAW_LOCAL_FAILURE_REPRODUCED"
    else:
        label = "OTHER_SINGLE_PAW_FAILURE"
    return {"classification": label, "failedPawRoles": failed}


def diagnose_paw(r11, vertices, controls, indices, weights, domains, interfaces, pitch, surface_anchors, snapped, transform, role):
    by = {c.role: c for c in controls}
    ridx = int(r11.ROLE_INDEX[role])
    bind = np.asarray(by[role].position, dtype=np.float64)
    radius = float(r11.PAW_SUPPORT_RADIUS_PITCHES * pitch)
    anchor_name = ANCHOR_FOR_ROLE[role]
    surface_anchor = np.asarray(surface_anchors[anchor_name], dtype=np.float64)
    snapped_pos = r11.index_to_world(snapped[anchor_name], transform)

    bind_dist = np.linalg.norm(vertices - bind[None, :], axis=1)
    nearest_idx = int(np.argmin(bind_dist))
    role_domain = r11.ROLE_DOMAIN[role]
    role_domain_idx = np.where(domains == role_domain)[0]
    if len(role_domain_idx) == 0:
        raise RuntimeError(f"no vertices in role domain {role_domain}")
    domain_dist = bind_dist[role_domain_idx]
    nearest_domain_idx = int(role_domain_idx[int(np.argmin(domain_dist))])

    weighted_support = np.array(
        [i for i in range(len(vertices)) if role_weight(indices, weights, i, ridx) > 0.0], dtype=np.int64
    )
    axis, derivative, differential = differential_support(r11, vertices, controls, indices, weights, role)

    weighted_dist = bind_dist[weighted_support] if len(weighted_support) else np.array([], dtype=np.float64)
    differential_dist = bind_dist[differential] if len(differential) else np.array([], dtype=np.float64)
    weighted_within = weighted_support[weighted_dist <= radius] if len(weighted_support) else np.array([], dtype=np.int64)
    differential_within = differential[differential_dist <= radius] if len(differential) else np.array([], dtype=np.int64)

    nearest_supported = None
    if len(weighted_support):
        j = int(weighted_support[int(np.argmin(weighted_dist))])
        nearest_supported = {
            "index": j,
            "positionR10": vec(vertices[j]),
            "domain": str(domains[j]),
            "distanceToBind": float(bind_dist[j]),
            "pawWeight": role_weight(indices, weights, j, ridx),
            "normalizedDerivative": float(derivative[j]),
        }

    local_idx = np.where(bind_dist <= radius)[0]
    local_records = []
    eligible_count = 0
    truncated_count = 0
    retained_count = 0
    ineligible_count = 0
    rank_hist = Counter()
    for i in local_idx.tolist():
        domain = str(domains[i])
        interface = bool(interfaces[i])
        candidates = candidate_table(r11, vertices[i], domain, interface, controls, pitch)
        paw = next((c for c in candidates if c["role"] == role), None)
        eligible = paw is not None
        if not eligible:
            ineligible_count += 1
            rank = None
            retained = False
            raw = None
            final_weight = 0.0
        else:
            eligible_count += 1
            rank = int(paw["rank"])
            rank_hist[str(rank)] += 1
            retained = bool(paw["retained"])
            raw = float(paw["rawScore"])
            final_weight = float(paw["normalizedWeight"])
            if retained:
                retained_count += 1
            else:
                truncated_count += 1
        top4 = [c for c in candidates if c["retained"]]
        local_records.append(
            {
                "vertexIndex": int(i),
                "positionR10": vec(vertices[i]),
                "distanceToBind": float(bind_dist[i]),
                "domain": domain,
                "interface": interface,
                "pawEligible": eligible,
                "pawRawScore": raw,
                "pawRank": rank,
                "pawRetainedTop4": retained,
                "pawFinalWeight": final_weight,
                "pawNormalizedDerivative": float(derivative[i]),
                "top4": top4,
            }
        )

    nearest_surface_distance = float(bind_dist[nearest_idx])
    classification = classify_paw(
        radius,
        nearest_surface_distance,
        len(local_idx),
        eligible_count,
        retained_count,
        len(differential_within),
    )

    return {
        "role": role,
        "roleDomain": role_domain,
        "bindPositionR10": vec(bind),
        "diagnosticAxisR10": vec(axis),
        "surfaceAnchorName": anchor_name,
        "surfaceAnchorPositionR10": vec(surface_anchor),
        "snappedMedialEndpointGrid": list(map(int, snapped[anchor_name])),
        "snappedMedialEndpointPositionR10": vec(snapped_pos),
        "surfaceAnchorToSnappedEndpointDistance": float(np.linalg.norm(surface_anchor - snapped_pos)),
        "bindToSnappedEndpointDistance": float(np.linalg.norm(bind - snapped_pos)),
        "nearestSurface": {
            "index": nearest_idx,
            "positionR10": vec(vertices[nearest_idx]),
            "distanceToBind": nearest_surface_distance,
            "domain": str(domains[nearest_idx]),
        },
        "nearestRoleDomainSurface": {
            "index": nearest_domain_idx,
            "positionR10": vec(vertices[nearest_domain_idx]),
            "distanceToBind": float(bind_dist[nearest_domain_idx]),
            "domain": str(domains[nearest_domain_idx]),
        },
        "localRadius": radius,
        "localVertexCount": int(len(local_idx)),
        "localDomainHistogram": dict(sorted(Counter(str(domains[i]) for i in local_idx).items())),
        "weightedSupportCount": int(len(weighted_support)),
        "weightedSupportDistanceQuantiles": qstats(weighted_dist),
        "weightedSupportWithinRadiusCount": int(len(weighted_within)),
        "differentialSupportCount": int(len(differential)),
        "differentialSupportDistanceQuantiles": qstats(differential_dist),
        "differentialSupportWithinRadiusCount": int(len(differential_within)),
        "nearestWeightedSupport": nearest_supported,
        "localCompetitionAggregate": {
            "localVertexCount": int(len(local_idx)),
            "pawEligibleCount": int(eligible_count),
            "eligibleButTruncatedCount": int(truncated_count),
            "eligibleAndRetainedCount": int(retained_count),
            "ineligibleCount": int(ineligible_count),
            "pawRankHistogram": dict(sorted(rank_hist.items(), key=lambda kv: int(kv[0]))),
        },
        "localVertices": local_records,
        "classification": classification,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_glb", type=Path)
    ap.add_argument("--geometry-dir", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    frozen_path = args.geometry_dir / "p1_c_r11_semantic_scaffold_v1.py"
    r11 = load_module(frozen_path)
    vertices, faces, identity = r11.reproduce_v3125(args.source_glb, args.geometry_dir)
    if len(vertices) != EXPECTED_VERTEX_COUNT or len(faces) != EXPECTED_FACE_COUNT:
        raise RuntimeError("V3125 topology mismatch")
    if identity.get("meshArraySha256") != EXPECTED_MESH_SHA:
        raise RuntimeError(f"V3125 mesh hash mismatch: {identity.get('meshArraySha256')}")

    frame = r11.frame_sign_audit(vertices, args.geometry_dir)
    surface_anchors = r11.derive_surface_anchors(vertices)
    skel, transform, pitch = r11.voxel_skeleton(vertices, faces)
    raw_graph = r11.graph_from_skeleton(skel)
    graph, snapped, nodes, paths = r11.derive_semantic_graph(vertices, raw_graph, transform, pitch)
    controls, path_worlds = r11.make_controls(transform, nodes, paths)
    domains, interfaces, domain_info, polylines = r11.derive_domains(vertices, path_worlds, pitch)
    indices, weights = r11.build_weights(vertices, controls, domains, interfaces, pitch)
    weight_audit = r11.weight_audit(indices, weights, domains, interfaces)

    body = r11.body_metrics(vertices)
    paw_reports = {}
    for role in PAW_ROLES:
        paw_reports[role] = diagnose_paw(
            r11, vertices, controls, indices, weights, domains, interfaces,
            pitch, surface_anchors, snapped, transform, role,
        )

    fl = paw_reports["FORE_L_PAW_CTRL"]
    reproduced = fl["differentialSupportCount"] > 0 and fl["differentialSupportWithinRadiusCount"] == 0
    if not reproduced:
        raise RuntimeError(f"original FORE_L failure not observationally reproduced: {fl['classification']}")

    report = {
        "diagnosticVersion": "R11_POST_FAILURE_DIAGNOSTIC_V1",
        "decisionScope": "OBSERVATIONAL_ONLY_NO_R11_RETUNING",
        "identity": identity,
        "frameAudit": frame,
        "scale": {
            "bodyHeight": float(body["height"]),
            "pitch": float(pitch),
            "pawLocalRadiusPitches": float(r11.PAW_SUPPORT_RADIUS_PITCHES),
            "pawLocalRadius": float(r11.PAW_SUPPORT_RADIUS_PITCHES * pitch),
            "vertexCount": int(len(vertices)),
            "faceCount": int(len(faces)),
        },
        "weightAudit": weight_audit,
        "paws": paw_reports,
        "crossSide": cross_side_classification(paw_reports),
        "originalFailureReproduced": bool(reproduced),
        "r11Stage1StatusRemains": "CLOSED_FAIL_R11_STAGE1_FAIL_FORE_L_PAW_LOCAL_SUPPORT",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True, separators=(",", ": ")) + "\n")
    print(json.dumps({
        "meshArraySha256": identity["meshArraySha256"],
        "pitch": report["scale"]["pitch"],
        "radius": report["scale"]["pawLocalRadius"],
        "crossSide": report["crossSide"],
        "classifications": {r: paw_reports[r]["classification"] for r in PAW_ROLES},
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
