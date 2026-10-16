from __future__ import annotations

import argparse
import importlib.util
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import fast_simplification

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "r10", HERE / "p1_c_r10_morphology_reduction_v1.py"
)
r10 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r10)

VERSION = "P1_C_R10_BOUNDARY_SMOOTHNESS_DIAGNOSTIC_V1"
REFINEMENT_TARGET_VERTICES = 1088
DIAGNOSTIC_TARGETS = [3125, 1560, 1088, 780]
AGG = 7.0
ANGLE_THRESHOLDS_DEG = [2.5, 5.0, 10.0, 15.0, 20.0, 30.0]


def dihedral_metrics(points: np.ndarray, triangles: np.ndarray) -> dict:
    tri = points[triangles]
    raw_normals = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    lengths = np.linalg.norm(raw_normals, axis=1)
    valid = lengths > 1e-15
    normals = np.zeros_like(raw_normals)
    normals[valid] = raw_normals[valid] / lengths[valid, None]

    edges: dict[tuple[int, int], list[int]] = defaultdict(list)
    for fi, face in enumerate(triangles.tolist()):
        a, b, c = map(int, face)
        for u, v in ((a, b), (b, c), (c, a)):
            edges[(min(u, v), max(u, v))].append(fi)

    angles = []
    weighted_angles = []
    weights = []
    non_two_face = 0
    for (u, v), faces in edges.items():
        if len(faces) != 2:
            non_two_face += 1
            continue
        f0, f1 = faces
        if not valid[f0] or not valid[f1]:
            continue
        dot = float(np.clip(np.dot(normals[f0], normals[f1]), -1.0, 1.0))
        angle = math.degrees(math.acos(dot))
        edge_len = float(np.linalg.norm(points[u] - points[v]))
        angles.append(angle)
        weighted_angles.append(angle)
        weights.append(edge_len)

    arr = np.asarray(angles, dtype=np.float64)
    warr = np.asarray(weighted_angles, dtype=np.float64)
    w = np.asarray(weights, dtype=np.float64)
    if len(arr) == 0:
        raise ValueError("no two-face edges for dihedral measurement")

    def weighted_percentile(values: np.ndarray, weights: np.ndarray, percentile: float) -> float:
        order = np.argsort(values)
        vv = values[order]
        ww = weights[order]
        cumulative = np.cumsum(ww)
        target = percentile / 100.0 * cumulative[-1]
        idx = int(np.searchsorted(cumulative, target, side="left"))
        idx = min(idx, len(vv) - 1)
        return float(vv[idx])

    fractions = {
        f"fractionAbove{str(t).replace('.', '_')}Deg": float(np.mean(arr > t))
        for t in ANGLE_THRESHOLDS_DEG
    }
    weighted_fractions = {
        f"edgeLengthFractionAbove{str(t).replace('.', '_')}Deg": float(
            w[arr > t].sum() / w.sum()
        )
        for t in ANGLE_THRESHOLDS_DEG
    }

    return {
        "twoFaceEdgeCount": int(len(arr)),
        "nonTwoFaceEdgeCount": int(non_two_face),
        "angleDegP50": float(np.percentile(arr, 50)),
        "angleDegP75": float(np.percentile(arr, 75)),
        "angleDegP90": float(np.percentile(arr, 90)),
        "angleDegP95": float(np.percentile(arr, 95)),
        "angleDegP99": float(np.percentile(arr, 99)),
        "angleDegMax": float(np.max(arr)),
        "edgeLengthWeightedAngleDegP50": weighted_percentile(warr, w, 50),
        "edgeLengthWeightedAngleDegP90": weighted_percentile(warr, w, 90),
        "edgeLengthWeightedAngleDegP95": weighted_percentile(warr, w, 95),
        "edgeLengthWeightedAngleDegP99": weighted_percentile(warr, w, 99),
        **fractions,
        **weighted_fractions,
    }


def build_meshes(points: np.ndarray, triangles: np.ndarray):
    lowest_face_target = r10.target_faces_for_closed_genus0(min(DIAGNOSTIC_TARGETS))
    _pmin, _fmin, collapses = fast_simplification.simplify(
        points,
        triangles,
        target_count=lowest_face_target,
        agg=AGG,
        verbose=False,
        return_collapses=True,
        preserve_border=False,
    )
    collapses = np.asarray(collapses, dtype=np.int64)
    cache: dict[int, tuple[np.ndarray, np.ndarray]] = {0: (points.copy(), triangles.copy())}
    meshes = {}
    for target in DIAGNOSTIC_TARGETS:
        prefix, p, f = r10.closest_prefix_for_target(
            points, triangles, collapses, target, cache
        )
        meshes[target] = (prefix, p, f)
    return collapses, meshes


def run(glb: Path, out: Path) -> dict:
    points_list, triangles_list, source_sha = r10.stage_d.load_structural_mesh(glb)
    if source_sha != r10.EXPECTED_SOURCE_SHA256:
        raise ValueError(f"source hash drift: {source_sha}")
    points = np.asarray(points_list, dtype=np.float64)
    triangles = np.asarray(triangles_list, dtype=np.int32)
    out.mkdir(parents=True, exist_ok=True)

    reference = r10.build_reference(points, triangles)
    collapses, meshes = build_meshes(points, triangles)

    ref_dihedral = dihedral_metrics(points, triangles)
    candidates = []
    row_grays = []
    for target in DIAGNOSTIC_TARGETS:
        prefix, p, f = meshes[target]
        ev = r10.evaluate_candidate(
            p, f, reference, out, f"R10_BOUNDARY_V{len(p)}"
        )
        row_grays.append(ev.pop("_nativeGray"))
        ev.pop("_nativeSize", None)
        ev.update({
            "targetVertices": target,
            "collapsePrefixLength": int(prefix),
            "dihedral": dihedral_metrics(p, f),
        })
        candidates.append(ev)

    rw, rh = 5 * r10.stage_d.CANVAS, r10.stage_d.CANVAS
    vw, vh, vgray = r10.combine_vertical(row_grays, rw, rh)
    native_name = "R10_BOUNDARY_3125_1560_1088_780_PRIMARY_96.png"
    enlarged_name = "R10_BOUNDARY_3125_1560_1088_780_PRIMARY_96_4X.png"
    (out / native_name).write_bytes(r10.stage_d.png_gray(vw, vh, vgray))
    ew, eh, egray = r10.stage_d.upscale_nearest(vgray, vw, vh, 4)
    (out / enlarged_name).write_bytes(r10.stage_d.png_gray(ew, eh, egray))

    summary = {
        "version": VERSION,
        "sourceSha256": source_sha,
        "fastSimplificationVersion": getattr(fast_simplification, "__version__", "unknown"),
        "agg": AGG,
        "refinementRule": {
            "broadPassVertices": 1560,
            "broadFailVertices": 780,
            "geometricMean": math.sqrt(1560 * 780),
            "roundingQuantum": 64,
            "frozenRefinementTargetVertices": REFINEMENT_TARGET_VERTICES,
        },
        "collapseCount": int(len(collapses)),
        "referenceDihedral": ref_dihedral,
        "candidates": candidates,
        "boundaryNativePng": native_name,
        "boundaryEnlargedPng": enlarged_name,
    }
    (out / "boundary_smoothness_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("glb", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    print(json.dumps(run(args.glb, args.out), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
