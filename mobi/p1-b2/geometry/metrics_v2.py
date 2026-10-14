from __future__ import annotations

from math import hypot

from model import ContactKind, Phase


def motion_metrics(states):
    max_drift = 0.0
    drifts = []
    transition_count = 0
    zero_support = 0
    max_target_error = 0.0
    previous = None

    for state in states:
        if not state.support_set:
            zero_support += 1
        current = {contact.id: contact for contact in state.contacts}
        for contact in state.contacts:
            if contact.load_bearing and contact.target_point is not None:
                max_target_error = max(max_target_error, (contact.point - contact.target_point).length())

        if previous is not None:
            old = {contact.id: contact for contact in previous.contacts}
            for contact_id, contact in current.items():
                prior = old.get(contact_id)
                if prior is None:
                    continue
                if contact.phase != prior.phase:
                    transition_count += 1
                if (
                    contact.kind == ContactKind.PAW_POINT
                    and contact.phase == Phase.CONTACT
                    and prior.phase == Phase.CONTACT
                ):
                    drift = (contact.point - prior.point).length()
                    drifts.append(drift)
                    max_drift = max(max_drift, drift)
        previous = state

    windows = [state.window_bounds for state in states]
    fill_x = [state.visual_bounds.width / state.window_bounds.width for state in states]
    fill_y = [state.visual_bounds.height / state.window_bounds.height for state in states]
    margins = []
    for state in states:
        window = state.window_bounds
        visual = state.visual_bounds
        margins.extend([
            visual.left - window.left,
            window.right - visual.right,
            visual.top - window.top,
            window.bottom - visual.bottom,
        ])

    return {
        "sampleCount": len(states),
        "maxPlantedPawDriftDp": max_drift,
        "meanPlantedPawDriftDp": sum(drifts) / len(drifts) if drifts else 0.0,
        "maxSupportTargetErrorDp": max_target_error,
        "contactTransitionCount": transition_count,
        "zeroSupportSampleCount": zero_support,
        "maxWindowWidthDp": max(window.width for window in windows),
        "maxWindowHeightDp": max(window.height for window in windows),
        "maxWindowAreaDp2": max(window.area for window in windows),
        "minWindowFillX": min(fill_x),
        "minWindowFillY": min(fill_y),
        "maxTransparentMarginDp": max(margins),
    }


def _point_segment_distance(px, py, a, b):
    vx = b.x - a.x
    vy = b.y - a.y
    wx = px - a.x
    wy = py - a.y
    length_sq = vx * vx + vy * vy
    if length_sq == 0.0:
        return hypot(wx, wy)
    u = max(0.0, min(1.0, (wx * vx + wy * vy) / length_sq))
    return hypot(px - (a.x + u * vx), py - (a.y + u * vy))


def _inside_polygon(px, py, points):
    inside = False
    j = len(points) - 1
    for i, point in enumerate(points):
        other = points[j]
        if ((point.y > py) != (other.y > py)) and (
            px < (other.x - point.x) * (py - point.y) / (other.y - point.y + 1e-30) + point.x
        ):
            inside = not inside
        j = i
    return inside


def _point_in_shape(px, py, shape):
    kind = shape["type"]
    if kind == "ellipse":
        rx = shape["rx"]
        ry = shape["ry"]
        return ((px - shape["cx"]) / rx) ** 2 + ((py - shape["cy"]) / ry) ** 2 <= 1.0
    if kind == "line":
        return _point_segment_distance(px, py, shape["p0"], shape["p1"]) <= shape["width"] / 2.0
    if kind == "polyline":
        points = shape["points"]
        return any(
            _point_segment_distance(px, py, a, b) <= shape["width"] / 2.0
            for a, b in zip(points, points[1:])
        )
    if kind == "polygon":
        return _inside_polygon(px, py, shape["points"])
    raise ValueError(kind)


def silhouette_occupancy(state, grid=64):
    """Deterministic development estimator, not production collision rasterization."""
    if grid < 16:
        raise ValueError("grid must be >= 16")
    window = state.window_bounds
    filled = 0
    total = grid * grid
    for iy in range(grid):
        y = window.top + (iy + .5) / grid * window.height
        for ix in range(grid):
            x = window.left + (ix + .5) / grid * window.width
            if any(_point_in_shape(x, y, shape) for shape in state.shapes):
                filled += 1
    ratio = filled / total
    return {
        "grid": grid,
        "silhouetteOccupancyRatio": ratio,
        "blockingSlackAreaDp2": window.area * (1.0 - ratio),
    }
