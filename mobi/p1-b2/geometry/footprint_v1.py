from __future__ import annotations

from math import isfinite

from metrics_v2 import silhouette_occupancy
from model import Rect

SCHEMES = ("F0_SINGLE_ALL", "F1_CORE_TAIL", "F2_CORE_FORE_HIND_TAIL", "F3_ADAPTIVE_LOWER_BOUND")
GROUPS_F1 = ("CORE", "TAIL")
GROUPS_F2 = ("CORE", "FORE", "HIND", "TAIL")


def _points_rect(points, pad=0.0):
    xs = [point.x for point in points]
    ys = [point.y for point in points]
    return Rect(min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def shape_bounds(shape):
    kind = shape["type"]
    if kind == "ellipse":
        return Rect(
            shape["cx"] - shape["rx"],
            shape["cy"] - shape["ry"],
            shape["cx"] + shape["rx"],
            shape["cy"] + shape["ry"],
        )
    if kind == "line":
        return _points_rect((shape["p0"], shape["p1"]), shape["width"] / 2.0)
    if kind == "polyline":
        return _points_rect(shape["points"], shape["width"] / 2.0)
    if kind == "polygon":
        return _points_rect(shape["points"])
    raise ValueError(f"unsupported shape type: {kind}")


def role_group(role):
    role = str(role or "")
    if role == "tail":
        return "TAIL"
    if role == "forelimb" or role.startswith("FORE_PAW_"):
        return "FORE"
    if role == "hindlimb" or role.startswith("HIND_PAW_"):
        return "HIND"
    return "CORE"


def _union_rect(a, b):
    if a is None:
        return b
    return a.union(b)


def group_bounds(state, scheme):
    if scheme == "F0_SINGLE_ALL":
        return {"ALL": state.window_bounds}
    if scheme not in ("F1_CORE_TAIL", "F2_CORE_FORE_HIND_TAIL"):
        raise ValueError(f"group_bounds does not accept {scheme}")

    pad = max(1.0, 0.018 * state.size_dp)
    raw = {}
    for shape in state.shapes:
        group = role_group(shape.get("role"))
        if scheme == "F1_CORE_TAIL" and group != "TAIL":
            group = "CORE"
        raw[group] = _union_rect(raw.get(group), shape_bounds(shape))

    ordered = GROUPS_F1 if scheme == "F1_CORE_TAIL" else GROUPS_F2
    result = {}
    for group in ordered:
        rect = raw.get(group)
        if rect is not None:
            result[group] = rect.expand(pad)
    return result


def _union_y_length(intervals):
    if not intervals:
        return 0.0
    intervals = sorted(intervals)
    total = 0.0
    start, end = intervals[0]
    for next_start, next_end in intervals[1:]:
        if next_start <= end:
            end = max(end, next_end)
        else:
            total += end - start
            start, end = next_start, next_end
    return total + end - start


def rect_union_area(rects):
    rects = list(rects)
    if not rects:
        return 0.0
    xs = sorted({value for rect in rects for value in (rect.left, rect.right)})
    area = 0.0
    for left, right in zip(xs, xs[1:]):
        width = right - left
        if width <= 0.0:
            continue
        mid = (left + right) / 2.0
        intervals = [
            (rect.top, rect.bottom)
            for rect in rects
            if rect.left <= mid <= rect.right
        ]
        area += width * _union_y_length(intervals)
    return area


def _valid_rect(rect):
    values = (rect.left, rect.top, rect.right, rect.bottom)
    return all(isfinite(value) for value in values) and rect.width > 0.0 and rect.height > 0.0


def analyze_state(state, occupancy_grid=32):
    errors = list(state.validate())
    if occupancy_grid < 16:
        raise ValueError("occupancy_grid must be >= 16")

    partition = {}
    for scheme in ("F0_SINGLE_ALL", "F1_CORE_TAIL", "F2_CORE_FORE_HIND_TAIL"):
        bounds = group_bounds(state, scheme)
        if not bounds:
            errors.append(f"{scheme}:no_rectangles")
        for group, rect in bounds.items():
            if not _valid_rect(rect):
                errors.append(f"{scheme}:invalid_rect:{group}")
        area = rect_union_area(bounds.values())
        partition[scheme] = {
            "rectangles": bounds,
            "blockingAreaDp2": area,
            "windowCount": len(bounds),
        }

    f0_area = state.window_bounds.area
    if abs(partition["F0_SINGLE_ALL"]["blockingAreaDp2"] - f0_area) > 1e-7:
        errors.append("F0_area_mismatch")

    for scheme in ("F1_CORE_TAIL", "F2_CORE_FORE_HIND_TAIL"):
        if partition[scheme]["blockingAreaDp2"] > f0_area + 1e-7:
            errors.append(f"{scheme}:area_exceeds_F0")

    f1 = partition["F1_CORE_TAIL"]
    f2 = partition["F2_CORE_FORE_HIND_TAIL"]
    selected_name = "F1_CORE_TAIL" if f1["blockingAreaDp2"] <= f2["blockingAreaDp2"] else "F2_CORE_FORE_HIND_TAIL"
    selected = partition[selected_name]
    partition["F3_ADAPTIVE_LOWER_BOUND"] = {
        "rectangles": selected["rectangles"],
        "blockingAreaDp2": selected["blockingAreaDp2"],
        "windowCount": selected["windowCount"],
        "selectedScheme": selected_name,
    }
    if partition["F3_ADAPTIVE_LOWER_BOUND"]["blockingAreaDp2"] > min(f1["blockingAreaDp2"], f2["blockingAreaDp2"]) + 1e-7:
        errors.append("F3_not_lower_bound")

    occupancy = silhouette_occupancy(state, grid=occupancy_grid)
    silhouette_area = f0_area * occupancy["silhouetteOccupancyRatio"]

    result = {
        "errors": errors,
        "occupancyGrid": occupancy_grid,
        "estimatedSilhouetteAreaDp2": silhouette_area,
        "f0SilhouetteOccupancyRatio": occupancy["silhouetteOccupancyRatio"],
        "schemes": {},
    }
    for scheme in SCHEMES:
        item = partition[scheme]
        area = item["blockingAreaDp2"]
        reduction = 0.0 if f0_area == 0.0 else max(0.0, min(1.0, 1.0 - area / f0_area))
        effective = 0.0 if area == 0.0 else max(0.0, min(1.0, silhouette_area / area))
        record = {
            "blockingAreaDp2": area,
            "areaReductionVsF0": reduction,
            "effectiveOccupancy": effective,
            "windowCount": item["windowCount"],
        }
        if scheme == "F3_ADAPTIVE_LOWER_BOUND":
            record["selectedScheme"] = item["selectedScheme"]
        result["schemes"][scheme] = record
    return result
