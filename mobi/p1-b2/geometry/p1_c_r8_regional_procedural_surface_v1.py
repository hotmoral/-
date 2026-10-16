from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Dict, Iterable, Tuple

from e_v0_profiles import morphology_by_id, orientation_by_id
import p1_c_r2_minimal_volumetric_proxy_v1 as r2
import p1_c_r5_bounded_explicit_anatomical_control_shell_v1 as r5
import p1_c_r8_regional_grammar_v1 as grammar
import p1_c_r8_neutral_m0_params_v1 as neutral


PROTOTYPE_VERSION = "P1_C_R8_REGIONAL_PROCEDURAL_DEFORMABLE_SURFACE_V1"
SOURCE_FAMILY = grammar.SOURCE_FAMILY
SOURCE_PACK_ID = grammar.SOURCE_PACK_ID
EXTERNAL_DOMAINS = grammar.EXTERNAL_DOMAINS
CORRECTION_USE_COUNT = 0
DERIVED_SUBDIVISION_STEPS = 0
SMOOTH_MIN_VERSION = "POLYNOMIAL_SMOOTH_MIN_V1"


@dataclass(frozen=True)
class RasterizedBody:
    width: int
    height: int
    world_bounds: Tuple[float, float, float, float]
    mask: bytes
    contributor: Tuple[str, ...]
    body_bounds: Tuple[float, float, float, float]
    occupied_pixel_count: int


@dataclass(frozen=True)
class RegionalSurfaceResult:
    version: str
    yaw_rad: float
    signature: str
    grammar_signature: str
    parameter_signature: str
    ears: Tuple[r2.ProjectedPrimitive, ...]
    limbs: Tuple[r2.ProjectedPrimitive, ...]
    paws: Tuple[r2.ProjectedPrimitive, ...]
    tail: r2.ProjectedPrimitive
    paw_pin_error: float
    interface_overlap_pass: bool
    interface_overlap: Dict[str, bool]


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def surface_signature() -> str:
    payload = {
        "version": PROTOTYPE_VERSION,
        "sourceFamily": SOURCE_FAMILY,
        "sourcePackId": SOURCE_PACK_ID,
        "grammarSignature": grammar.grammar_signature(),
        "parameterSignature": neutral.parameter_signature(),
        "smoothMinVersion": SMOOTH_MIN_VERSION,
        "samplingRule": grammar.SAMPLING_RULE,
        "stateOwnership": "EXISTING_CANONICAL_SEMANTICS_READ_ONLY",
        "correctionFamily": "NONE",
        "derivedSubdivisionSteps": DERIVED_SUBDIVISION_STEPS,
    }
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _yaw(fixture) -> float:
    return float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _lerp(a: float, b: float, t: float) -> float:
    return a * (1.0 - t) + b * t


def _smoothstep(t: float) -> float:
    t = _clamp(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _smooth_min(a: float, b: float, k: float) -> float:
    if k <= 1e-12:
        return min(a, b)
    h = max(k - abs(a - b), 0.0) / k
    return min(a, b) - 0.25 * h * h * k


def _super_norm(coords, exponent: float) -> float:
    exponent = max(1.05, float(exponent))
    return sum(abs(float(value)) ** exponent for value in coords) ** (1.0 / exponent)


def _camera_center(anchor, offset_u: float, offset_v: float, size: float, yaw: float, scale_u: float, scale_v: float):
    u = offset_u * size * scale_u
    v = offset_v * size * scale_v
    return (
        float(anchor.x) + u * math.cos(yaw),
        float(anchor.y) - v,
        -u * math.sin(yaw),
    )


def _body_local(point, center, yaw: float):
    dx = float(point[0]) - float(center[0])
    dy = float(point[1]) - float(center[1])
    dz = float(point[2]) - float(center[2])
    u = dx * math.cos(yaw) - dz * math.sin(yaw)
    w = dx * math.sin(yaw) + dz * math.cos(yaw)
    v = -dy
    return u, v, w


def _morph_scales(fixture, region_id: str):
    morphology = morphology_by_id(fixture.morphology_id)
    orient = orientation_by_id(fixture.morphology_id)
    if region_id == "CRANIUM_MUZZLE":
        return morphology.head_scale, morphology.head_scale, morphology.head_scale
    if region_id == "CERVICAL_NECK":
        blend = math.sqrt(morphology.head_scale * morphology.forequarter_scale)
        width = math.sqrt(morphology.head_scale * orient.thorax_width_scale)
        return blend, blend, width
    if region_id == "SHOULDER_CHEST":
        return (
            morphology.forequarter_scale,
            morphology.trunk_depth * morphology.forequarter_scale,
            orient.thorax_width_scale * morphology.forequarter_scale,
        )
    if region_id == "THORAX_FLANK":
        return morphology.trunk_length, morphology.trunk_depth, orient.thorax_width_scale
    if region_id == "ABDOMEN_TUCK":
        width = math.sqrt(orient.thorax_width_scale * orient.pelvis_width_scale)
        return morphology.trunk_length, morphology.trunk_depth, width
    if region_id == "PELVIS_HAUNCH":
        return (
            morphology.pelvis_scale,
            morphology.trunk_depth * morphology.pelvis_scale,
            orient.pelvis_width_scale * morphology.pelvis_scale,
        )
    if region_id == "FORE_PROXIMAL":
        return (
            morphology.fore_limb_length,
            morphology.forequarter_scale * morphology.trunk_depth,
            orient.thorax_width_scale * morphology.forequarter_scale,
        )
    if region_id == "HIND_PROXIMAL":
        return (
            morphology.hind_limb_length,
            morphology.pelvis_scale * morphology.trunk_depth,
            orient.pelvis_width_scale * morphology.pelvis_scale,
        )
    raise KeyError(region_id)


def _head_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["CRANIUM_MUZZLE"]
    size = float(fixture.size_dp)
    yaw = _yaw(fixture)
    su, sv, sw = _morph_scales(fixture, "CRANIUM_MUZZLE")
    center = _camera_center(fixture.state.anchors["HEAD_ROOT"], p["offset_u"], p["offset_v"], size, yaw, su, sv)
    u, v, w = _body_local(point, center, yaw)
    a = (p["front_length"] if u >= 0.0 else p["rear_length"]) * size * su
    b = p["half_height"] * size * sv
    c = p["half_width"] * size * sw
    if u > 0.0:
        t = _smoothstep(u / max(a, 1e-9))
        c *= max(0.42, 1.0 - p["muzzle_taper"] * t)
        b *= max(0.55, 1.0 - 0.28 * p["muzzle_taper"] * t)
    return _super_norm((u / a, v / b, w / c), p["roundness"]) - 1.0


def _shoulder_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["SHOULDER_CHEST"]
    size = float(fixture.size_dp)
    yaw = _yaw(fixture)
    su, sv, sw = _morph_scales(fixture, "SHOULDER_CHEST")
    center = _camera_center(fixture.state.anchors["FOREQUARTER_REF"], p["offset_u"], p["offset_v"], size, yaw, su, sv)
    u, v, w = _body_local(point, center, yaw)
    a = (p["front_length"] if u >= 0.0 else p["rear_length"]) * size * su
    b = p["half_height"] * size * sv
    c = p["half_width"] * size * sw
    if v < 0.0:
        b *= 1.0 + 0.46 * p["ventral_fullness"]
    else:
        b *= max(0.78, 1.0 - 0.10 * p["ventral_fullness"])
    return _super_norm((u / a, v / b, w / c), p["roundness"]) - 1.0


def _thorax_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["THORAX_FLANK"]
    size = float(fixture.size_dp)
    yaw = _yaw(fixture)
    su, sv, sw = _morph_scales(fixture, "THORAX_FLANK")
    center = _camera_center(fixture.state.anchors["BODY_ROOT"], p["offset_u"], p["offset_v"], size, yaw, su, sv)
    u, v, w = _body_local(point, center, yaw)
    a = p["half_length"] * size * su
    b = p["half_height"] * size * sv
    c = p["half_width"] * size * sw
    exponent = p["roundness"] + (1.8 * p["dorsal_flatten"] if v > 0.0 else 0.0)
    return _super_norm((u / a, v / b, w / c), exponent) - 1.0


def _pelvis_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["PELVIS_HAUNCH"]
    size = float(fixture.size_dp)
    yaw = _yaw(fixture)
    su, sv, sw = _morph_scales(fixture, "PELVIS_HAUNCH")
    center = _camera_center(fixture.state.anchors["PELVIS_REF"], p["offset_u"], p["offset_v"], size, yaw, su, sv)
    u, v, w = _body_local(point, center, yaw)
    a = (p["front_length"] if u >= 0.0 else p["rear_length"]) * size * su
    b = p["half_height"] * size * sv
    c = p["half_width"] * size * sw
    if u < 0.0:
        t = _smoothstep((-u) / max(a, 1e-9))
        c *= 1.0 + 0.52 * p["haunch_fullness"] * t
        b *= 1.0 + 0.30 * p["haunch_fullness"] * t
    return _super_norm((u / a, v / b, w / c), p["roundness"]) - 1.0


def _segment_frame(a, b):
    ax, ay, az = a
    bx, by, bz = b
    tx, ty, tz = bx - ax, by - ay, bz - az
    length = math.sqrt(tx * tx + ty * ty + tz * tz)
    if length <= 1e-12:
        return (1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 1.0), 0.0
    tx, ty, tz = tx / length, ty / length, tz / length
    dorsal = (0.0, -1.0, 0.0)
    wx = ty * dorsal[2] - tz * dorsal[1]
    wy = tz * dorsal[0] - tx * dorsal[2]
    wz = tx * dorsal[1] - ty * dorsal[0]
    wlen = math.sqrt(wx * wx + wy * wy + wz * wz)
    if wlen <= 1e-9:
        wx, wy, wz = 0.0, 0.0, 1.0
    else:
        wx, wy, wz = wx / wlen, wy / wlen, wz / wlen
    vx = wy * tz - wz * ty
    vy = wz * tx - wx * tz
    vz = wx * ty - wy * tx
    vlen = math.sqrt(vx * vx + vy * vy + vz * vz)
    if vlen <= 1e-12:
        vx, vy, vz = 0.0, -1.0, 0.0
    else:
        vx, vy, vz = vx / vlen, vy / vlen, vz / vlen
    return (tx, ty, tz), (vx, vy, vz), (wx, wy, wz), length


def _segment_field(point, a, b, start_rv: float, start_rw: float, end_rv: float, end_rw: float, exponent: float, sag_screen_y: float = 0.0):
    tangent, vaxis, waxis, length = _segment_frame(a, b)
    if length <= 1e-12:
        return 1e9
    px, py, pz = point
    ax, ay, az = a
    rx, ry, rz = px - ax, py - ay, pz - az
    along = rx * tangent[0] + ry * tangent[1] + rz * tangent[2]
    t_raw = along / length
    t = _clamp(t_raw, 0.0, 1.0)
    cx = _lerp(a[0], b[0], t)
    cy = _lerp(a[1], b[1], t) + sag_screen_y * (4.0 * t * (1.0 - t))
    cz = _lerp(a[2], b[2], t)
    qx, qy, qz = px - cx, py - cy, pz - cz
    vcoord = qx * vaxis[0] + qy * vaxis[1] + qz * vaxis[2]
    wcoord = qx * waxis[0] + qy * waxis[1] + qz * waxis[2]
    axial = 0.0
    if t_raw < 0.0:
        axial = -t_raw * length
    elif t_raw > 1.0:
        axial = (t_raw - 1.0) * length
    rv = _lerp(start_rv, end_rv, t)
    rw = _lerp(start_rw, end_rw, t)
    cap = math.sqrt(max(rv * rw, 1e-12))
    return _super_norm((vcoord / max(rv, 1e-9), wcoord / max(rw, 1e-9), axial / max(cap, 1e-9)), exponent) - 1.0


def _neck_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["CERVICAL_NECK"]
    size = float(fixture.size_dp)
    _, sv, sw = _morph_scales(fixture, "CERVICAL_NECK")
    head = fixture.state.anchors["HEAD_ROOT"]
    fore = fixture.state.anchors["FOREQUARTER_REF"]
    a = (float(head.x), float(head.y), 0.0)
    b = (float(fore.x), float(fore.y), 0.0)
    return _segment_field(
        point, a, b,
        p["start_radius_v"] * size * sv,
        p["start_radius_w"] * size * sw,
        p["end_radius_v"] * size * sv,
        p["end_radius_w"] * size * sw,
        p["roundness"],
        sag_screen_y=p["sag_bias"] * size,
    )


def _quadratic_bezier(a: float, m: float, b: float, t: float) -> float:
    return (1.0 - t) * (1.0 - t) * a + 2.0 * (1.0 - t) * t * m + t * t * b


def _waist_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["ABDOMEN_TUCK"]
    size = float(fixture.size_dp)
    _, sv, sw = _morph_scales(fixture, "ABDOMEN_TUCK")
    body = fixture.state.anchors["BODY_ROOT"]
    pelvis = fixture.state.anchors["PELVIS_REF"]
    a = (float(body.x), float(body.y), 0.0)
    b = (float(pelvis.x), float(pelvis.y), 0.0)
    tangent, vaxis, waxis, length = _segment_frame(a, b)
    if length <= 1e-12:
        return 1e9
    px, py, pz = point
    rx, ry, rz = px - a[0], py - a[1], pz - a[2]
    along = rx * tangent[0] + ry * tangent[1] + rz * tangent[2]
    t_raw = along / length
    t = _clamp(t_raw, 0.0, 1.0)
    cx = _lerp(a[0], b[0], t)
    cy = _lerp(a[1], b[1], t) - p["ventral_lift"] * size * sv * (4.0 * t * (1.0 - t))
    cz = 0.0
    qx, qy, qz = px - cx, py - cy, pz - cz
    vcoord = qx * vaxis[0] + qy * vaxis[1] + qz * vaxis[2]
    wcoord = qx * waxis[0] + qy * waxis[1] + qz * waxis[2]
    axial = 0.0
    if t_raw < 0.0:
        axial = -t_raw * length
    elif t_raw > 1.0:
        axial = (t_raw - 1.0) * length
    rv = _quadratic_bezier(
        p["start_radius_v"] * size * sv,
        p["mid_radius_v"] * size * sv,
        p["end_radius_v"] * size * sv,
        t,
    )
    rw = _quadratic_bezier(
        p["start_radius_w"] * size * sw,
        p["mid_radius_w"] * size * sw,
        p["end_radius_w"] * size * sw,
        t,
    )
    cap = math.sqrt(max(rv * rw, 1e-12))
    return _super_norm((vcoord / max(rv, 1e-9), wcoord / max(rw, 1e-9), axial / max(cap, 1e-9)), 2.0) - 1.0


def _proximal_segment(fixture, hind: bool, side: float):
    region_id = "HIND_PROXIMAL" if hind else "FORE_PROXIMAL"
    p = neutral.REGION_PARAMS[region_id]
    size = float(fixture.size_dp)
    yaw = _yaw(fixture)
    anchors = fixture.state.anchors
    owner = anchors["PELVIS_REF" if hind else "FOREQUARTER_REF"]
    side_letter = "L" if side > 0.0 else "R"
    paw = anchors[f"{'HIND' if hind else 'FORE'}_PAW_{side_letter}"]
    _, _, sw = _morph_scales(fixture, region_id)
    root_lateral = side * p["root_radius_w"] * size * sw * 0.42
    end_lateral = side * p["root_radius_w"] * size * sw * 0.62
    a = (
        float(owner.x) + root_lateral * math.sin(yaw),
        float(owner.y),
        root_lateral * math.cos(yaw),
    )
    frac = p["length_fraction"]
    b = (
        float(owner.x) + frac * (float(paw.x) - float(owner.x)) + end_lateral * math.sin(yaw),
        float(owner.y) + frac * (float(paw.y) - float(owner.y)),
        end_lateral * math.cos(yaw),
    )
    return a, b


def _proximal_field(fixture, point, hind: bool, side: float) -> float:
    region_id = "HIND_PROXIMAL" if hind else "FORE_PROXIMAL"
    p = neutral.REGION_PARAMS[region_id]
    size = float(fixture.size_dp)
    _, sv, sw = _morph_scales(fixture, region_id)
    a, b = _proximal_segment(fixture, hind, side)
    return _segment_field(
        point,
        a,
        b,
        p["root_radius_v"] * size * sv,
        p["root_radius_w"] * size * sw,
        p["root_radius_v"] * size * sv * p["end_scale"],
        p["root_radius_w"] * size * sw * p["end_scale"],
        p["roundness"],
    )


def raw_fields(fixture, screen_x: float, screen_y: float, depth: float):
    point = (float(screen_x), float(screen_y), float(depth))
    return {
        "CRANIUM_MUZZLE": _head_field(fixture, point),
        "CERVICAL_NECK": _neck_field(fixture, point),
        "SHOULDER_CHEST": _shoulder_field(fixture, point),
        "THORAX_FLANK": _thorax_field(fixture, point),
        "ABDOMEN_TUCK": _waist_field(fixture, point),
        "PELVIS_HAUNCH": _pelvis_field(fixture, point),
        "FORE_L_PROXIMAL": _proximal_field(fixture, point, False, +1.0),
        "FORE_R_PROXIMAL": _proximal_field(fixture, point, False, -1.0),
        "HIND_L_PROXIMAL": _proximal_field(fixture, point, True, +1.0),
        "HIND_R_PROXIMAL": _proximal_field(fixture, point, True, -1.0),
    }


def composed_field_from_raw(values: Dict[str, float]) -> float:
    b = neutral.BLEND_PARAMS
    value = _smooth_min(values["CRANIUM_MUZZLE"], values["CERVICAL_NECK"], b["blend_head_neck"])
    value = _smooth_min(value, values["SHOULDER_CHEST"], b["blend_neck_shoulder"])
    value = _smooth_min(value, values["THORAX_FLANK"], b["blend_shoulder_thorax"])
    value = _smooth_min(value, values["ABDOMEN_TUCK"], b["blend_thorax_abdomen"])
    value = _smooth_min(value, values["PELVIS_HAUNCH"], b["blend_abdomen_pelvis"])
    value = _smooth_min(value, values["FORE_L_PROXIMAL"], b["blend_shoulder_fore"])
    value = _smooth_min(value, values["FORE_R_PROXIMAL"], b["blend_shoulder_fore"])
    value = _smooth_min(value, values["HIND_L_PROXIMAL"], b["blend_pelvis_hind"])
    value = _smooth_min(value, values["HIND_R_PROXIMAL"], b["blend_pelvis_hind"])
    return value


def field_value(fixture, screen_x: float, screen_y: float, depth: float) -> float:
    return composed_field_from_raw(raw_fields(fixture, screen_x, screen_y, depth))


def winning_region(values: Dict[str, float]) -> str:
    return min(values, key=lambda key: (values[key], key))


def _body_world_bounds(fixture):
    anchors = fixture.state.anchors
    points = [(float(point.x), float(point.y)) for point in anchors.values()]
    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)
    pad = grammar.SAMPLING_RULE["screenPaddingDpFactor"] * float(fixture.size_dp)
    min_x -= pad
    max_x += pad
    min_y -= pad
    max_y += pad
    width = max_x - min_x
    height = max_y - min_y
    aspect = grammar.SAMPLING_RULE["canvasWidthPx"] / grammar.SAMPLING_RULE["canvasHeightPx"]
    current = width / max(height, 1e-9)
    if current < aspect:
        target = height * aspect
        extra = 0.5 * (target - width)
        min_x -= extra
        max_x += extra
    elif current > aspect:
        target = width / aspect
        extra = 0.5 * (target - height)
        min_y -= extra
        max_y += extra
    return min_x, min_y, max_x, max_y


def rasterize_body(fixture) -> RasterizedBody:
    width = int(grammar.SAMPLING_RULE["canvasWidthPx"])
    height = int(grammar.SAMPLING_RULE["canvasHeightPx"])
    depth_samples = int(grammar.SAMPLING_RULE["depthSamples"])
    bounds = _body_world_bounds(fixture)
    min_x, min_y, max_x, max_y = bounds
    dx = (max_x - min_x) / width
    dy = (max_y - min_y) / height
    depth_half = grammar.SAMPLING_RULE["depthHalfRangeDpFactor"] * float(fixture.size_dp)
    if depth_samples <= 1:
        depth_values = (0.0,)
    else:
        depth_values = tuple(
            -depth_half + (2.0 * depth_half) * index / (depth_samples - 1)
            for index in range(depth_samples)
        )

    mask = bytearray(width * height)
    contributors = [""] * (width * height)
    occupied = 0
    body_points = []

    for py in range(height):
        sy = min_y + (py + 0.5) * dy
        row_offset = py * width
        for px in range(width):
            sx = min_x + (px + 0.5) * dx
            best_field = float("inf")
            best_region = ""
            is_inside = False
            for depth in depth_values:
                values = raw_fields(fixture, sx, sy, depth)
                composed = composed_field_from_raw(values)
                if composed < best_field:
                    best_field = composed
                    best_region = winning_region(values)
                if composed <= 0.0:
                    is_inside = True
            if is_inside:
                idx = row_offset + px
                mask[idx] = 1
                contributors[idx] = best_region
                occupied += 1
                body_points.append((sx, sy))

    if not body_points:
        raise RuntimeError("R8 rasterization produced empty body")

    xs = [point[0] for point in body_points]
    ys = [point[1] for point in body_points]
    body_bounds = (min(xs), min(ys), max(xs), max(ys))
    return RasterizedBody(
        width=width,
        height=height,
        world_bounds=bounds,
        mask=bytes(mask),
        contributor=tuple(contributors),
        body_bounds=body_bounds,
        occupied_pixel_count=occupied,
    )


def _proximal_exit_2d(fixture, hind: bool, side: float):
    _, b = _proximal_segment(fixture, hind, side)
    return float(b[0]), float(b[1])


def _build_distal_limbs_and_paws(fixture):
    morphology = morphology_by_id(fixture.morphology_id)
    anchors = fixture.state.anchors
    size = float(fixture.size_dp)
    limbs = []
    paws = []
    paw_pin_error = 0.0

    for domain, hind, side in (
        ("FORE_L", False, +1.0),
        ("FORE_R", False, -1.0),
        ("HIND_L", True, +1.0),
        ("HIND_R", True, -1.0),
    ):
        start = _proximal_exit_2d(fixture, hind, side)
        side_letter = "L" if side > 0.0 else "R"
        owner = "HIND" if hind else "FORE"
        paw = anchors[f"{owner}_PAW_{side_letter}"]
        px, py = float(paw.x), float(paw.y)
        ratio = r2.RATIOS["hind_limb" if hind else "fore_limb"]
        base_radius = size * ratio["radius"]
        dx, dy = px - start[0], py - start[1]
        limb_scale = morphology.hind_limb_length if hind else morphology.fore_limb_length
        mid = (
            start[0] + dx * 0.48 + (0.024 if hind else -0.016) * size * limb_scale,
            start[1] + dy * 0.50,
        )
        region_id = "HIND_PROXIMAL" if hind else "FORE_PROXIMAL"
        p = neutral.REGION_PARAMS[region_id]
        _, sv, _ = _morph_scales(fixture, region_id)
        start_radius = p["root_radius_v"] * size * sv * p["end_scale"]
        limbs.append(r2.ProjectedPrimitive(
            f"{domain}_DISTAL_PROXIMAL",
            "TAPERED_LIMB_CONTINUATION",
            domain,
            r5._tapered_segment(start, mid, start_radius, base_radius),
        ))
        limbs.append(r2.ProjectedPrimitive(
            f"{domain}_DISTAL",
            "CAPSULE",
            domain,
            r2._capsule(mid, (px, py), base_radius * 0.82),
        ))
        paw_points = r2._ellipse_at(
            paw,
            ratio["paw_rx"] * size * morphology.paw_scale,
            ratio["paw_ry"] * size * morphology.paw_scale,
        )
        paws.append(r2.ProjectedPrimitive(f"{domain}_PAW", "PAW_ELLIPSE", domain, paw_points))
        center_x = sum(point[0] for point in paw_points) / len(paw_points)
        center_y = sum(point[1] for point in paw_points) / len(paw_points)
        paw_pin_error = max(paw_pin_error, math.hypot(center_x - px, center_y - py))

    return tuple(limbs), tuple(paws), paw_pin_error


def _interface_samples(fixture, interface_id: str):
    anchors = fixture.state.anchors
    if interface_id == "HEAD_NECK":
        return ((float(anchors["HEAD_ROOT"].x), float(anchors["HEAD_ROOT"].y), 0.0),
                (float(anchors["FOREQUARTER_REF"].x), float(anchors["FOREQUARTER_REF"].y), 0.0))
    if interface_id == "NECK_SHOULDER":
        return ((float(anchors["HEAD_ROOT"].x), float(anchors["HEAD_ROOT"].y), 0.0),
                (float(anchors["FOREQUARTER_REF"].x), float(anchors["FOREQUARTER_REF"].y), 0.0))
    if interface_id == "SHOULDER_THORAX":
        return ((float(anchors["FOREQUARTER_REF"].x), float(anchors["FOREQUARTER_REF"].y), 0.0),
                (float(anchors["BODY_ROOT"].x), float(anchors["BODY_ROOT"].y), 0.0))
    if interface_id == "THORAX_ABDOMEN":
        return ((float(anchors["BODY_ROOT"].x), float(anchors["BODY_ROOT"].y), 0.0),
                (float(anchors["PELVIS_REF"].x), float(anchors["PELVIS_REF"].y), 0.0))
    if interface_id == "ABDOMEN_PELVIS":
        return ((float(anchors["BODY_ROOT"].x), float(anchors["BODY_ROOT"].y), 0.0),
                (float(anchors["PELVIS_REF"].x), float(anchors["PELVIS_REF"].y), 0.0))
    if interface_id == "SHOULDER_FORE":
        left = _proximal_segment(fixture, False, +1.0)
        right = _proximal_segment(fixture, False, -1.0)
        return (left[0], left[1], right[0], right[1])
    if interface_id == "PELVIS_HIND":
        left = _proximal_segment(fixture, True, +1.0)
        right = _proximal_segment(fixture, True, -1.0)
        return (left[0], left[1], right[0], right[1])
    raise KeyError(interface_id)


def interface_overlap_checks(fixture):
    interface_region_keys = {
        "HEAD_NECK": (("CRANIUM_MUZZLE",), ("CERVICAL_NECK",)),
        "NECK_SHOULDER": (("CERVICAL_NECK",), ("SHOULDER_CHEST",)),
        "SHOULDER_THORAX": (("SHOULDER_CHEST",), ("THORAX_FLANK",)),
        "THORAX_ABDOMEN": (("THORAX_FLANK",), ("ABDOMEN_TUCK",)),
        "ABDOMEN_PELVIS": (("ABDOMEN_TUCK",), ("PELVIS_HAUNCH",)),
        "SHOULDER_FORE": (("SHOULDER_CHEST",), ("FORE_L_PROXIMAL", "FORE_R_PROXIMAL")),
        "PELVIS_HIND": (("PELVIS_HAUNCH",), ("HIND_L_PROXIMAL", "HIND_R_PROXIMAL")),
    }
    result = {}
    for interface in grammar.BLEND_INTERFACES:
        interface_id = interface["id"]
        samples = _interface_samples(fixture, interface_id)
        left_keys, right_keys = interface_region_keys[interface_id]
        ok = False
        if len(samples) == 2:
            pairs = ((samples[0], samples[1]),)
        else:
            pairs = ((samples[0], samples[1]), (samples[2], samples[3]))
        for a, b in pairs:
            for index in range(17):
                t = index / 16.0
                point = (
                    _lerp(a[0], b[0], t),
                    _lerp(a[1], b[1], t),
                    _lerp(a[2], b[2], t),
                )
                values = raw_fields(fixture, *point)
                left = min(values[key] for key in left_keys)
                right = min(values[key] for key in right_keys)
                if left <= 0.18 and right <= 0.18:
                    ok = True
                    break
            if ok:
                break
        result[interface_id] = ok
    return result


def build_surface(fixture) -> RegionalSurfaceResult:
    if grammar.grammar_signature() != neutral.GRAMMAR_SIGNATURE:
        raise RuntimeError("R8 grammar/parameter signature mismatch")
    yaw = _yaw(fixture)
    ears = r5._ears(fixture, yaw)
    limbs, paws, paw_pin_error = _build_distal_limbs_and_paws(fixture)
    tail = r5._tail(fixture, yaw)
    overlap = interface_overlap_checks(fixture)
    return RegionalSurfaceResult(
        version=PROTOTYPE_VERSION,
        yaw_rad=yaw,
        signature=surface_signature(),
        grammar_signature=grammar.grammar_signature(),
        parameter_signature=neutral.parameter_signature(),
        ears=ears,
        limbs=limbs,
        paws=paws,
        tail=tail,
        paw_pin_error=paw_pin_error,
        interface_overlap_pass=all(overlap.values()),
        interface_overlap=overlap,
    )


def all_primitives(result: RegionalSurfaceResult, include_ears: bool = True):
    return (result.ears if include_ears else ()) + result.limbs + result.paws + (result.tail,)


def primitive_points(result: RegionalSurfaceResult, include_ears: bool = True):
    return tuple(point for primitive in all_primitives(result, include_ears=include_ears) for point in primitive.points)


def result_dict(fixture, result: RegionalSurfaceResult, raster: RasterizedBody | None = None):
    finite = all(math.isfinite(value) for point in primitive_points(result) for value in point)
    payload = {
        "version": result.version,
        "sourceFamily": SOURCE_FAMILY,
        "sourcePackId": SOURCE_PACK_ID,
        "caseId": fixture.case_id,
        "morphologyId": fixture.morphology_id,
        "sizeDp": int(fixture.size_dp),
        "t": float(fixture.t),
        "semanticHash": fixture.semantic_hash,
        "yawRad": result.yaw_rad,
        "surfaceSignature": result.signature,
        "grammarVersion": grammar.GRAMMAR_VERSION,
        "grammarSignature": result.grammar_signature,
        "parameterSetVersion": neutral.PARAMETER_SET_VERSION,
        "parameterSignature": result.parameter_signature,
        "authoritativeRegionFunctionCount": len(grammar.REGIONS),
        "authoritativeRegionScalarCount": grammar.region_parameter_count(),
        "authoritativeBlendInterfaceCount": len(grammar.BLEND_INTERFACES),
        "authoritativeScalarCount": grammar.authoritative_scalar_count(),
        "derivedSubdivisionSteps": DERIVED_SUBDIVISION_STEPS,
        "externalDomains": list(EXTERNAL_DOMAINS),
        "externalDomainCount": len(EXTERNAL_DOMAINS),
        "pawPinError": result.paw_pin_error,
        "finite": finite,
        "correctionUseCount": CORRECTION_USE_COUNT,
        "interfaceOverlapPass": result.interface_overlap_pass,
        "interfaceOverlap": dict(sorted(result.interface_overlap.items())),
    }
    if raster is not None:
        payload.update({
            "rasterWidth": raster.width,
            "rasterHeight": raster.height,
            "occupiedPixelCount": raster.occupied_pixel_count,
            "bodyBounds": list(raster.body_bounds),
            "samplingWorldBounds": list(raster.world_bounds),
        })
    return payload
