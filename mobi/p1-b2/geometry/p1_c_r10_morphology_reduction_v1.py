from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np
import fast_simplification

HERE = Path(__file__).resolve().parent

_spec_render = importlib.util.spec_from_file_location(
    "stage_d", HERE / "p1_c_3d_cat_stage_d_projection_v1.py"
)
stage_d = importlib.util.module_from_spec(_spec_render)
_spec_render.loader.exec_module(stage_d)

VERSION = "P1_C_R10_MORPHOLOGY_REDUCTION_V1"
EXPECTED_SOURCE_SHA256 = "6870facdd3c7784581382af0ede14e5d6fc8f2092ac9ff15cda1f8c3feb315e5"
SOURCE_VERTEX_COUNT = 99642
SOURCE_TRIANGLE_COUNT = 199280
TARGET_VERTICES = [50000, 25000, 12500, 6250, 3125, 1560, 780]
PRIMARY_VIEWS = list(stage_d.VIEWS)
YAW_SWEEP = [i * 2.5 for i in range(37)]
LANES = {
    "A_AGG7": 7.0,
    "B_AGG0": 0.0,
}


def target_faces_for_closed_genus0(target_vertices: int) -> int:
    # For a closed triangulated genus-0 manifold: V - E + F = 2, 3F = 2E => F = 2V - 4.
    if target_vertices < 4:
        raise ValueError("target_vertices must be >= 4")
    return 2 * target_vertices - 4


def topology_metrics(vertex_count: int, triangles: np.ndarray) -> dict:
    edge_counts = Counter()
    directed = Counter()
    used = set()
    degenerate = 0
    adjacency = defaultdict(set)
    for tri in triangles.tolist():
        a, b, c = map(int, tri)
        if len({a, b, c}) < 3:
            degenerate += 1
            continue
        used.update((a, b, c))
        adjacency[a].update((b, c))
        adjacency[b].update((a, c))
        adjacency[c].update((a, b))
        for u, v in ((a, b), (b, c), (c, a)):
            edge_counts[(min(u, v), max(u, v))] += 1
            directed[(u, v)] += 1
    boundary = sum(1 for n in edge_counts.values() if n == 1)
    nonmanifold = sum(1 for n in edge_counts.values() if n > 2)
    orientation_bad = sum(
        1
        for (u, v), n in edge_counts.items()
        if n == 2 and not (directed[(u, v)] == 1 and directed[(v, u)] == 1)
    )
    components = 0
    seen = set()
    for start in sorted(used):
        if start in seen:
            continue
        components += 1
        stack = [start]
        seen.add(start)
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
    e = len(edge_counts)
    f = int(len(triangles))
    chi = int(vertex_count - e + f)
    return {
        "vertexCount": int(vertex_count),
        "triangleCount": f,
        "uniqueEdgeCount": e,
        "connectedComponents": components,
        "boundaryEdgeCount": boundary,
        "nonManifoldEdgeCount": nonmanifold,
        "orientationMismatchEdgeCount": orientation_bad,
        "degenerateIndexTriangleCount": degenerate,
        "eulerCharacteristic": chi,
        "closedOrientedTwoManifold": bool(
            components == 1
            and boundary == 0
            and nonmanifold == 0
            and orientation_bad == 0
            and degenerate == 0
        ),
    }


def geometry_metrics(points: np.ndarray, triangles: np.ndarray) -> dict:
    tri = points[triangles]
    ab = tri[:, 1] - tri[:, 0]
    ac = tri[:, 2] - tri[:, 0]
    cross = np.cross(ab, ac)
    areas = 0.5 * np.linalg.norm(cross, axis=1)
    signed_volume = np.einsum("ij,ij->i", tri[:, 0], np.cross(tri[:, 1], tri[:, 2])).sum() / 6.0

    e01 = np.linalg.norm(tri[:, 1] - tri[:, 0], axis=1)
    e12 = np.linalg.norm(tri[:, 2] - tri[:, 1], axis=1)
    e20 = np.linalg.norm(tri[:, 0] - tri[:, 2], axis=1)
    longest = np.maximum(np.maximum(e01, e12), e20)
    shortest = np.minimum(np.minimum(e01, e12), e20)
    ratio = np.divide(longest, shortest, out=np.full_like(longest, np.inf), where=shortest > 1e-15)
    finite_ratio = ratio[np.isfinite(ratio)]

    return {
        "surfaceArea": float(areas.sum()),
        "signedVolume": float(signed_volume),
        "absVolume": float(abs(signed_volume)),
        "zeroAreaTriangleCount": int(np.count_nonzero(areas <= 1e-15)),
        "edgeRatioP50": float(np.percentile(finite_ratio, 50)) if len(finite_ratio) else None,
        "edgeRatioP95": float(np.percentile(finite_ratio, 95)) if len(finite_ratio) else None,
        "edgeRatioMax": float(np.max(finite_ratio)) if len(finite_ratio) else None,
    }


def mask_iou(a: bytes | bytearray, b: bytes | bytearray) -> tuple[float, int, int]:
    aa = np.frombuffer(bytes(a), dtype=np.uint8) != 0
    bb = np.frombuffer(bytes(b), dtype=np.uint8) != 0
    inter = int(np.count_nonzero(aa & bb))
    union = int(np.count_nonzero(aa | bb))
    diff = int(np.count_nonzero(aa ^ bb))
    return (1.0 if union == 0 else inter / union, diff, union)


def render_mask(points: np.ndarray, triangles: np.ndarray, deg: float) -> bytearray:
    projected = [stage_d.project_point(p, deg) for p in points.tolist()]
    return stage_d.rasterize(projected, [tuple(map(int, t)) for t in triangles.tolist()])


def combine_vertical(grays: list[bytes], w: int, h: int) -> tuple[int, int, bytes]:
    return w, h * len(grays), b"".join(grays)


def render_primary_strip(points: np.ndarray, triangles: np.ndarray, out: Path, stem: str) -> dict:
    masks = []
    grays = []
    reports = []
    for name, deg in PRIMARY_VIEWS:
        mask = render_mask(points, triangles, deg)
        gray = stage_d.mask_to_gray(mask)
        masks.append(mask)
        grays.append(gray)
        m = stage_d.mask_metrics(mask)
        m.update({"name": name, "yawDeg": deg})
        reports.append(m)
    sw, sh, sgray = stage_d.combine_horizontal(grays, stage_d.CANVAS, stage_d.CANVAS)
    native_name = f"{stem}_PRIMARY_96.png"
    enlarged_name = f"{stem}_PRIMARY_96_4X.png"
    (out / native_name).write_bytes(stage_d.png_gray(sw, sh, sgray))
    ew, eh, egray = stage_d.upscale_nearest(sgray, sw, sh, 4)
    (out / enlarged_name).write_bytes(stage_d.png_gray(ew, eh, egray))
    return {
        "masks": masks,
        "reports": reports,
        "nativePng": native_name,
        "enlargedPng": enlarged_name,
        "nativeGray": sgray,
        "nativeSize": [sw, sh],
    }


def build_reference(points: np.ndarray, triangles: np.ndarray) -> dict:
    primary_masks = []
    primary_reports = []
    for name, deg in PRIMARY_VIEWS:
        mask = render_mask(points, triangles, deg)
        primary_masks.append(mask)
        r = stage_d.mask_metrics(mask)
        r.update({"name": name, "yawDeg": deg})
        primary_reports.append(r)

    yaw_masks = [render_mask(points, triangles, deg) for deg in YAW_SWEEP]
    adjacent = []
    for i in range(1, len(yaw_masks)):
        iou, diff, union = mask_iou(yaw_masks[i - 1], yaw_masks[i])
        adjacent.append({
            "fromDeg": YAW_SWEEP[i - 1],
            "toDeg": YAW_SWEEP[i],
            "xorUnion": 0.0 if union == 0 else diff / union,
            "iou": iou,
        })
    return {
        "primaryMasks": primary_masks,
        "primaryReports": primary_reports,
        "yawMasks": yaw_masks,
        "adjacent": adjacent,
        "topology": topology_metrics(len(points), triangles),
        "geometry": geometry_metrics(points, triangles),
    }


def replay_prefix(points: np.ndarray, triangles: np.ndarray, collapses: np.ndarray, prefix_len: int):
    if prefix_len <= 0:
        return points.copy(), triangles.copy()
    p, f, _mapping = fast_simplification.replay_simplification(
        points=points,
        triangles=triangles,
        collapses=collapses[:prefix_len],
    )
    return np.asarray(p, dtype=np.float64), np.asarray(f, dtype=np.int32)


def closest_prefix_for_target(
    points: np.ndarray,
    triangles: np.ndarray,
    collapses: np.ndarray,
    target_vertices: int,
    cache: dict[int, tuple[np.ndarray, np.ndarray]],
):
    source_v = len(points)
    if target_vertices >= source_v:
        return 0, points.copy(), triangles.copy()
    max_prefix = len(collapses)
    if max_prefix == 0:
        return 0, points.copy(), triangles.copy()

    def get(k: int):
        k = max(0, min(max_prefix, int(k)))
        if k not in cache:
            cache[k] = replay_prefix(points, triangles, collapses, k)
        return cache[k]

    guess = max(0, min(max_prefix, source_v - target_vertices))
    best_k = guess
    best_p, best_f = get(guess)
    best_err = abs(len(best_p) - target_vertices)

    lo, hi = 0, max_prefix
    for _ in range(24):
        if lo > hi:
            break
        mid = (lo + hi) // 2
        p, f = get(mid)
        err = abs(len(p) - target_vertices)
        if err < best_err or (err == best_err and len(p) >= target_vertices and len(best_p) < target_vertices):
            best_k, best_p, best_f, best_err = mid, p, f, err
        if len(p) > target_vertices:
            lo = mid + 1
        elif len(p) < target_vertices:
            hi = mid - 1
        else:
            return mid, p, f
    return best_k, best_p, best_f


def evaluate_candidate(
    points: np.ndarray,
    triangles: np.ndarray,
    reference: dict,
    out: Path,
    stem: str,
) -> dict:
    primary = render_primary_strip(points, triangles, out, stem)
    comparisons = []
    hard_pass = True
    for idx, ((name, deg), cmask, creport, rmask, rreport) in enumerate(
        zip(PRIMARY_VIEWS, primary["masks"], primary["reports"], reference["primaryMasks"], reference["primaryReports"])
    ):
        iou, diff, union = mask_iou(cmask, rmask)
        cb = creport["bbox"]
        rb = rreport["bbox"]
        bbox_delta = [abs(int(cb[i]) - int(rb[i])) for i in range(4)] if cb and rb else [999] * 4
        cc = creport["centroid"]
        rc = rreport["centroid"]
        centroid_delta = math.dist(cc, rc) if cc and rc else 999.0
        view_pass = (
            iou >= 0.975
            and max(bbox_delta) <= 1
            and centroid_delta <= 0.75
            and creport["components8"] == rreport["components8"]
        )
        hard_pass = hard_pass and view_pass
        comparisons.append({
            "name": name,
            "yawDeg": deg,
            "iou": iou,
            "differingPixels": diff,
            "unionPixels": union,
            "differingPixelFractionOfUnion": 0.0 if union == 0 else diff / union,
            "bboxDeltaAbs": bbox_delta,
            "centroidDeltaPx": centroid_delta,
            "componentDelta": creport["components8"] - rreport["components8"],
            "mechanicalViewPass": view_pass,
        })

    yaw_masks = [render_mask(points, triangles, deg) for deg in YAW_SWEEP]
    yaw_comp = []
    max_excess = -1e9
    max_same_view_loss = 0.0
    for i, cmask in enumerate(yaw_masks):
        iou_same, diff_same, union_same = mask_iou(cmask, reference["yawMasks"][i])
        max_same_view_loss = max(max_same_view_loss, 1.0 - iou_same)
        if i == 0:
            continue
        iou_adj, diff_adj, union_adj = mask_iou(yaw_masks[i - 1], cmask)
        cand_xor = 0.0 if union_adj == 0 else diff_adj / union_adj
        ref_xor = reference["adjacent"][i - 1]["xorUnion"]
        excess = cand_xor - ref_xor
        max_excess = max(max_excess, excess)
        yaw_comp.append({
            "fromDeg": YAW_SWEEP[i - 1],
            "toDeg": YAW_SWEEP[i],
            "candidateXorUnion": cand_xor,
            "referenceXorUnion": ref_xor,
            "excessXorUnion": excess,
            "candidateAdjacentIou": iou_adj,
        })

    topo = topology_metrics(len(points), triangles)
    geo = geometry_metrics(points, triangles)
    ref_geo = reference["geometry"]
    topology_pass = topo["closedOrientedTwoManifold"]
    hard_pass = hard_pass and topology_pass

    return {
        "vertexCount": int(len(points)),
        "triangleCount": int(len(triangles)),
        "topology": topo,
        "geometry": geo,
        "surfaceAreaRatioToReference": geo["surfaceArea"] / ref_geo["surfaceArea"],
        "absVolumeRatioToReference": geo["absVolume"] / ref_geo["absVolume"] if ref_geo["absVolume"] else None,
        "primaryComparisons": comparisons,
        "yaw": {
            "stepDeg": 2.5,
            "sampleCount": len(YAW_SWEEP),
            "maxExcessAdjacentXorUnion": max_excess,
            "maxSameViewIouLossVsReference": max_same_view_loss,
            "adjacent": yaw_comp,
        },
        "mechanicalHardPass": bool(hard_pass),
        "primaryNativePng": primary["nativePng"],
        "primaryEnlargedPng": primary["enlargedPng"],
        "_nativeGray": primary["nativeGray"],
        "_nativeSize": primary["nativeSize"],
    }


def run_lane(
    lane_name: str,
    agg: float,
    points: np.ndarray,
    triangles: np.ndarray,
    reference: dict,
    out: Path,
) -> dict:
    lowest_face_target = target_faces_for_closed_genus0(TARGET_VERTICES[-1])
    _pmin, _fmin, collapses = fast_simplification.simplify(
        points,
        triangles,
        target_count=lowest_face_target,
        agg=agg,
        verbose=False,
        return_collapses=True,
        preserve_border=False,
    )
    collapses = np.asarray(collapses, dtype=np.int64)
    reachable_p, reachable_f = replay_prefix(points, triangles, collapses, len(collapses))
    reachable_min_v = len(reachable_p)

    lane_out = out / lane_name
    lane_out.mkdir(parents=True, exist_ok=True)
    cache: dict[int, tuple[np.ndarray, np.ndarray]] = {0: (points.copy(), triangles.copy())}
    tiers = []
    row_grays = []

    # L0 reference row through the same output path.
    ref_eval = evaluate_candidate(points, triangles, reference, lane_out, f"{lane_name}_L0_V{len(points)}")
    row_grays.append(ref_eval.pop("_nativeGray"))
    ref_eval.pop("_nativeSize", None)
    ref_eval.update({
        "tier": "L0",
        "targetVertices": SOURCE_VERTEX_COUNT,
        "collapsePrefixLength": 0,
        "targetReached": True,
        "role": "FULL_REFERENCE",
    })
    tiers.append(ref_eval)

    for idx, target_v in enumerate(TARGET_VERTICES, start=1):
        if target_v < reachable_min_v:
            tiers.append({
                "tier": f"L{idx}",
                "targetVertices": target_v,
                "targetReached": False,
                "reachableMinVertices": int(reachable_min_v),
                "collapsePrefixLength": int(len(collapses)),
                "mechanicalHardPass": False,
                "role": "TARGET_NOT_REACHED",
            })
            continue
        prefix, p, f = closest_prefix_for_target(points, triangles, collapses, target_v, cache)
        ev = evaluate_candidate(p, f, reference, lane_out, f"{lane_name}_L{idx}_V{len(p)}")
        row_grays.append(ev.pop("_nativeGray"))
        ev.pop("_nativeSize", None)
        ev.update({
            "tier": f"L{idx}",
            "targetVertices": target_v,
            "targetReached": True,
            "collapsePrefixLength": int(prefix),
            "role": "BROAD_TIER",
        })
        tiers.append(ev)

    if row_grays:
        rw, rh = 5 * stage_d.CANVAS, stage_d.CANVAS
        vw, vh, vgray = combine_vertical(row_grays, rw, rh)
        native_name = f"{lane_name}_ALL_REACHED_TIERS_96.png"
        enlarged_name = f"{lane_name}_ALL_REACHED_TIERS_96_4X.png"
        (lane_out / native_name).write_bytes(stage_d.png_gray(vw, vh, vgray))
        ew, eh, egray = stage_d.upscale_nearest(vgray, vw, vh, 4)
        (lane_out / enlarged_name).write_bytes(stage_d.png_gray(ew, eh, egray))
    else:
        native_name = enlarged_name = None

    return {
        "lane": lane_name,
        "agg": agg,
        "collapseCount": int(len(collapses)),
        "reachableMinVertices": int(reachable_min_v),
        "reachableMinTriangles": int(len(reachable_f)),
        "allReachedTiersNativePng": native_name,
        "allReachedTiersEnlargedPng": enlarged_name,
        "tiers": tiers,
    }


def run(glb: Path, out: Path) -> dict:
    points_list, triangles_list, source_sha = stage_d.load_structural_mesh(glb)
    if source_sha != EXPECTED_SOURCE_SHA256:
        raise ValueError(f"source hash drift: {source_sha}")
    points = np.asarray(points_list, dtype=np.float64)
    triangles = np.asarray(triangles_list, dtype=np.int32)
    if points.shape != (SOURCE_VERTEX_COUNT, 3):
        raise ValueError(f"source vertex shape drift: {points.shape}")
    if triangles.shape != (SOURCE_TRIANGLE_COUNT, 3):
        raise ValueError(f"source triangle shape drift: {triangles.shape}")
    if not np.all(np.isfinite(points)):
        raise ValueError("source has non-finite points")

    out.mkdir(parents=True, exist_ok=True)
    reference = build_reference(points, triangles)
    lanes = [run_lane(name, agg, points, triangles, reference, out) for name, agg in LANES.items()]

    summary = {
        "version": VERSION,
        "sourceSha256": source_sha,
        "fastSimplificationVersion": getattr(fast_simplification, "__version__", "unknown"),
        "sourceVertexCount": int(len(points)),
        "sourceTriangleCount": int(len(triangles)),
        "targetVertices": TARGET_VERTICES,
        "primaryViews": [{"name": n, "yawDeg": d} for n, d in PRIMARY_VIEWS],
        "yawSweep": {"startDeg": 0.0, "endDeg": 90.0, "stepDeg": 2.5, "count": len(YAW_SWEEP)},
        "referenceTopology": reference["topology"],
        "referenceGeometry": reference["geometry"],
        "lanes": lanes,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("glb", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    summary = run(args.glb, args.out)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
