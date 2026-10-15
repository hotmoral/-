from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List, Tuple

from c3_renderers import GROUPS
from c3w_renderer_adapter import (
    STRATEGY_GENERIC,
    STRATEGY_VIEW_RESOLVED,
    render_h6n,
)
from c4_hard_motion_fixture_adapter import H4, H6N, build_c4_fixture_matrix
from c4_renderer_adapter import CANDIDATE_B, CANDIDATE_C, render_c4
from model import Rect, Vec2

COST_PROXY_VERSION = "P1_C5_RUNTIME_COST_PROXY_V1"


@dataclass(frozen=True)
class RenderCost:
    shape_count: int
    point_count: int
    numeric_leaf_count: int
    active_partition_count: int
    partition_filter_shape_visits: int
    bounds_union_shape_visits: int
    total_bounds_shape_visits: int
    view_depth_shape_count: int
    sort_item_count: int
    sort_comparison_upper_proxy: int
    correction_family_count: int
    visual_area: float
    partition_area_sum: float


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _point_count(shape: Dict[str, Any]) -> int:
    count = 0
    for key in ("p0", "p1"):
        if isinstance(shape.get(key), Vec2):
            count += 1
    points = shape.get("points")
    if isinstance(points, (list, tuple)):
        count += sum(1 for value in points if isinstance(value, Vec2))
    return count


def _numeric_leaf_count(value: Any) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, (int, float)):
        return 1
    if isinstance(value, Vec2):
        return 2
    if isinstance(value, Rect):
        return 4
    if isinstance(value, dict):
        return sum(_numeric_leaf_count(item) for item in value.values())
    if isinstance(value, (list, tuple)):
        return sum(_numeric_leaf_count(item) for item in value)
    return 0


def summarize_render(rendered: Dict[str, Any]) -> RenderCost:
    shapes = rendered["shapes"]
    shape_count = len(shapes)
    point_count = sum(_point_count(shape) for shape in shapes)
    view_depth_shape_count = sum(1 for shape in shapes if "_viewDepth" in shape)
    sort_item_count = shape_count if view_depth_shape_count else 0
    sort_upper = (
        int(math.ceil(sort_item_count * math.log2(sort_item_count)))
        if sort_item_count > 1
        else 0
    )

    # Current partition_bounds implementation scans every shape once per semantic
    # group to filter, then union_bounds scans selected shapes. Together with the
    # top-level visual union this is a deterministic structural work proxy.
    partition_filter_shape_visits = len(GROUPS) * shape_count
    bounds_union_shape_visits = shape_count + shape_count
    total_bounds_shape_visits = partition_filter_shape_visits + bounds_union_shape_visits

    partitions = rendered["partitionBounds"]
    return RenderCost(
        shape_count=shape_count,
        point_count=point_count,
        numeric_leaf_count=_numeric_leaf_count(shapes),
        active_partition_count=len(partitions),
        partition_filter_shape_visits=partition_filter_shape_visits,
        bounds_union_shape_visits=bounds_union_shape_visits,
        total_bounds_shape_visits=total_bounds_shape_visits,
        view_depth_shape_count=view_depth_shape_count,
        sort_item_count=sort_item_count,
        sort_comparison_upper_proxy=sort_upper,
        correction_family_count=len(tuple(rendered.get("corrections", ()))),
        visual_area=float(rendered["visualBounds"].area),
        partition_area_sum=float(sum(rect.area for rect in partitions.values())),
    )


def _rect_tuple(rect: Rect) -> Tuple[float, float, float, float]:
    return (float(rect.left), float(rect.top), float(rect.right), float(rect.bottom))


def _changed_partition_count(previous: Dict[str, Rect] | None, current: Dict[str, Rect]) -> int:
    if previous is None:
        return 0
    changed = 0
    for group in GROUPS:
        before = previous.get(group)
        after = current.get(group)
        if before is None and after is None:
            continue
        if before is None or after is None or _rect_tuple(before) != _rect_tuple(after):
            changed += 1
    return changed


def _record_key(case_id: str, morph_id: str, size_dp: int, direction: int, path: str) -> str:
    return f"{path}|{case_id}|{morph_id}|{size_dp}|{direction:+d}"


def _cost_dict(cost: RenderCost) -> Dict[str, Any]:
    return asdict(cost)


def _aggregate(samples: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    rows = list(samples)
    if not rows:
        return {"sampleCount": 0}

    integer_fields = (
        "shape_count",
        "point_count",
        "numeric_leaf_count",
        "active_partition_count",
        "partition_filter_shape_visits",
        "bounds_union_shape_visits",
        "total_bounds_shape_visits",
        "view_depth_shape_count",
        "sort_item_count",
        "sort_comparison_upper_proxy",
        "correction_family_count",
        "changed_partition_count",
    )
    float_fields = ("visual_area", "partition_area_sum")

    result: Dict[str, Any] = {"sampleCount": len(rows)}
    for field in integer_fields:
        values = [int(row[field]) for row in rows]
        result[field] = {
            "min": min(values),
            "max": max(values),
            "sum": sum(values),
            "mean": sum(values) / len(values),
        }
    for field in float_fields:
        values = [float(row[field]) for row in rows]
        result[field] = {
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
        }
    return result


def build_cost_report() -> Dict[str, Any]:
    fixtures = build_c4_fixture_matrix()
    sample_rows: List[Dict[str, Any]] = []
    previous_partitions: Dict[str, Dict[str, Rect]] = {}

    for case_id, morph_id, size_dp, direction, fixture in fixtures:
        # Full hard-set candidate replay. Candidate B remains a causal baseline;
        # Candidate C is the surviving sparse-hybrid path.
        for candidate, path in (
            (CANDIDATE_B, "C4_B"),
            (CANDIDATE_C, "C4_C"),
        ):
            rendered = render_c4(fixture, candidate)
            cost = _cost_dict(summarize_render(rendered))
            key = _record_key(case_id, morph_id, size_dp, direction, path)
            changed = _changed_partition_count(previous_partitions.get(key), rendered["partitionBounds"])
            previous_partitions[key] = rendered["partitionBounds"]
            sample_rows.append({
                "path": path,
                "caseId": case_id,
                "morphologyId": morph_id,
                "sizeDp": size_dp,
                "direction": direction,
                "t": fixture.t,
                **cost,
                "changed_partition_count": changed,
            })

        if case_id == H6N:
            for strategy, path in (
                (STRATEGY_GENERIC, "H6N_GENERIC"),
                (STRATEGY_VIEW_RESOLVED, "H6N_VIEW_RESOLVED"),
            ):
                rendered = render_h6n(fixture, strategy, "RF_C")
                cost = _cost_dict(summarize_render(rendered))
                key = _record_key(case_id, morph_id, size_dp, direction, path)
                changed = _changed_partition_count(previous_partitions.get(key), rendered["partitionBounds"])
                previous_partitions[key] = rendered["partitionBounds"]
                sample_rows.append({
                    "path": path,
                    "caseId": case_id,
                    "morphologyId": morph_id,
                    "sizeDp": size_dp,
                    "direction": direction,
                    "t": fixture.t,
                    **cost,
                    "changed_partition_count": changed,
                })

    by_path: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    by_path_case: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in sample_rows:
        by_path[row["path"]].append(row)
        by_path_case[(row["path"], row["caseId"])].append(row)

    aggregates = {path: _aggregate(rows) for path, rows in sorted(by_path.items())}
    case_aggregates = {
        f"{path}|{case_id}": _aggregate(rows)
        for (path, case_id), rows in sorted(by_path_case.items())
    }

    def mean(path: str, field: str) -> float:
        return float(aggregates[path][field]["mean"])

    h6_shape_delta = mean("H6N_VIEW_RESOLVED", "shape_count") - mean("H6N_GENERIC", "shape_count")
    h6_point_delta = mean("H6N_VIEW_RESOLVED", "point_count") - mean("H6N_GENERIC", "point_count")
    h6_bounds_delta = mean("H6N_VIEW_RESOLVED", "total_bounds_shape_visits") - mean("H6N_GENERIC", "total_bounds_shape_visits")
    h6_partition_area_pct = (
        (mean("H6N_VIEW_RESOLVED", "partition_area_sum") / mean("H6N_GENERIC", "partition_area_sum") - 1.0)
        * 100.0
    )

    h4_b = case_aggregates[f"C4_B|{H4}"]
    h4_c = case_aggregates[f"C4_C|{H4}"]

    decision_proxies = {
        "h6n": {
            "meanShapeDeltaViewMinusGeneric": h6_shape_delta,
            "meanPointDeltaViewMinusGeneric": h6_point_delta,
            "meanBoundsShapeVisitDelta": h6_bounds_delta,
            "meanPartitionAreaDeltaPct": h6_partition_area_pct,
            "viewResolvedMeanSortItems": mean("H6N_VIEW_RESOLVED", "sort_item_count"),
            "viewResolvedMeanViewDepthShapes": mean("H6N_VIEW_RESOLVED", "view_depth_shape_count"),
            "genericMeanSortItems": mean("H6N_GENERIC", "sort_item_count"),
            "maxActivePartitionsViewResolved": aggregates["H6N_VIEW_RESOLVED"]["active_partition_count"]["max"],
        },
        "h4": {
            "baselineMeanShapes": h4_b["shape_count"]["mean"],
            "sparseHybridMeanShapes": h4_c["shape_count"]["mean"],
            "baselineMaxShapes": h4_b["shape_count"]["max"],
            "sparseHybridMaxShapes": h4_c["shape_count"]["max"],
            "sparseHybridMaxCorrectionFamiliesPerSample": h4_c["correction_family_count"]["max"],
            "maxActivePartitionsSparseHybrid": h4_c["active_partition_count"]["max"],
        },
        "host": {
            "maximumActiveSemanticPartitionsAcrossReport": max(
                aggregate["active_partition_count"]["max"] for aggregate in aggregates.values()
            ),
            "idleContinuousUpdateRequiredByRepresentation": False,
            "newAndroidWindowMechanismIntroduced": False,
        },
    }

    return {
        "version": COST_PROXY_VERSION,
        "fixtureSampleCount": len(fixtures),
        "renderSampleCount": len(sample_rows),
        "aggregates": aggregates,
        "caseAggregates": case_aggregates,
        "decisionProxies": decision_proxies,
    }
