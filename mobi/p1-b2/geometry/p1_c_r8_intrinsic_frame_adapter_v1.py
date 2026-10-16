from __future__ import annotations

from functools import lru_cache
import math

from e_v0_profiles import morphology_by_id, orientation_by_id
import p1_c_r8_neutral_m0_params_v1 as neutral
import p1_c_r8_regional_procedural_surface_v1 as base


ADAPTER_VERSION = "P1_C_R8_INTRINSIC_FRAME_ADAPTER_V1"
CORRECTION_CLASS = "PRE_EVIDENCE_INTRINSIC_FRAME_TRANSCRIPTION_ONLY"


@lru_cache(maxsize=None)
def _cached_morph_scales(morphology_id: str, region_id: str):
    morphology = morphology_by_id(morphology_id)
    orient = orientation_by_id(morphology_id)
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


def _morph_scales(fixture, region_id: str):
    return _cached_morph_scales(fixture.morphology_id, region_id)


def _body_local_x_bu(fixture, anchor_name: str) -> float:
    morphology = morphology_by_id(fixture.morphology_id)
    trunk_half = 0.47 * morphology.trunk_length
    if anchor_name == "BODY_ROOT":
        return 0.0
    if anchor_name == "FOREQUARTER_REF":
        return +trunk_half
    if anchor_name == "PELVIS_REF":
        return -trunk_half
    if anchor_name == "HEAD_ROOT":
        return +trunk_half + 0.34 * morphology.head_scale
    if anchor_name == "TAIL_ROOT":
        return -trunk_half - 0.08
    raise KeyError(anchor_name)


def _anchor_depth_dp(fixture, anchor_name: str) -> float:
    yaw = base._yaw(fixture)
    scale = float(fixture.size_dp) / 2.0
    return -_body_local_x_bu(fixture, anchor_name) * scale * math.sin(yaw)


def _camera_center3(anchor, anchor_depth: float, offset_u: float, offset_v: float, size: float, yaw: float, scale_u: float, scale_v: float):
    u = offset_u * size * scale_u
    v = offset_v * size * scale_v
    return (
        float(anchor.x) + u * math.cos(yaw),
        float(anchor.y) - v,
        float(anchor_depth) - u * math.sin(yaw),
    )


@lru_cache(maxsize=None)
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


def _head_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["CRANIUM_MUZZLE"]
    size = float(fixture.size_dp)
    yaw = base._yaw(fixture)
    su, sv, sw = _morph_scales(fixture, "CRANIUM_MUZZLE")
    center = _camera_center3(
        fixture.state.anchors["HEAD_ROOT"],
        _anchor_depth_dp(fixture, "HEAD_ROOT"),
        p["offset_u"], p["offset_v"], size, yaw, su, sv,
    )
    u, v, w = base._body_local(point, center, yaw)
    a = (p["front_length"] if u >= 0.0 else p["rear_length"]) * size * su
    b = p["half_height"] * size * sv
    c = p["half_width"] * size * sw
    if u > 0.0:
        t = base._smoothstep(u / max(a, 1e-9))
        c *= max(0.42, 1.0 - p["muzzle_taper"] * t)
        b *= max(0.55, 1.0 - 0.28 * p["muzzle_taper"] * t)
    return base._super_norm((u / a, v / b, w / c), p["roundness"]) - 1.0


def _shoulder_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["SHOULDER_CHEST"]
    size = float(fixture.size_dp)
    yaw = base._yaw(fixture)
    su, sv, sw = _morph_scales(fixture, "SHOULDER_CHEST")
    center = _camera_center3(
        fixture.state.anchors["FOREQUARTER_REF"],
        _anchor_depth_dp(fixture, "FOREQUARTER_REF"),
        p["offset_u"], p["offset_v"], size, yaw, su, sv,
    )
    u, v, w = base._body_local(point, center, yaw)
    a = (p["front_length"] if u >= 0.0 else p["rear_length"]) * size * su
    b = p["half_height"] * size * sv
    c = p["half_width"] * size * sw
    if v < 0.0:
        b *= 1.0 + 0.46 * p["ventral_fullness"]
    else:
        b *= max(0.78, 1.0 - 0.10 * p["ventral_fullness"])
    return base._super_norm((u / a, v / b, w / c), p["roundness"]) - 1.0


def _thorax_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["THORAX_FLANK"]
    size = float(fixture.size_dp)
    yaw = base._yaw(fixture)
    su, sv, sw = _morph_scales(fixture, "THORAX_FLANK")
    center = _camera_center3(
        fixture.state.anchors["BODY_ROOT"],
        _anchor_depth_dp(fixture, "BODY_ROOT"),
        p["offset_u"], p["offset_v"], size, yaw, su, sv,
    )
    u, v, w = base._body_local(point, center, yaw)
    a = p["half_length"] * size * su
    b = p["half_height"] * size * sv
    c = p["half_width"] * size * sw
    exponent = p["roundness"] + (1.8 * p["dorsal_flatten"] if v > 0.0 else 0.0)
    return base._super_norm((u / a, v / b, w / c), exponent) - 1.0


def _pelvis_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["PELVIS_HAUNCH"]
    size = float(fixture.size_dp)
    yaw = base._yaw(fixture)
    su, sv, sw = _morph_scales(fixture, "PELVIS_HAUNCH")
    center = _camera_center3(
        fixture.state.anchors["PELVIS_REF"],
        _anchor_depth_dp(fixture, "PELVIS_REF"),
        p["offset_u"], p["offset_v"], size, yaw, su, sv,
    )
    u, v, w = base._body_local(point, center, yaw)
    a = (p["front_length"] if u >= 0.0 else p["rear_length"]) * size * su
    b = p["half_height"] * size * sv
    c = p["half_width"] * size * sw
    if u < 0.0:
        t = base._smoothstep((-u) / max(a, 1e-9))
        c *= 1.0 + 0.52 * p["haunch_fullness"] * t
        b *= 1.0 + 0.30 * p["haunch_fullness"] * t
    return base._super_norm((u / a, v / b, w / c), p["roundness"]) - 1.0


def _neck_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["CERVICAL_NECK"]
    size = float(fixture.size_dp)
    _, sv, sw = _morph_scales(fixture, "CERVICAL_NECK")
    head = fixture.state.anchors["HEAD_ROOT"]
    fore = fixture.state.anchors["FOREQUARTER_REF"]
    a = (float(head.x), float(head.y), _anchor_depth_dp(fixture, "HEAD_ROOT"))
    b = (float(fore.x), float(fore.y), _anchor_depth_dp(fixture, "FOREQUARTER_REF"))
    return base._segment_field(
        point, a, b,
        p["start_radius_v"] * size * sv,
        p["start_radius_w"] * size * sw,
        p["end_radius_v"] * size * sv,
        p["end_radius_w"] * size * sw,
        p["roundness"],
        sag_screen_y=p["sag_bias"] * size,
    )


def _waist_field(fixture, point) -> float:
    p = neutral.REGION_PARAMS["ABDOMEN_TUCK"]
    size = float(fixture.size_dp)
    _, sv, sw = _morph_scales(fixture, "ABDOMEN_TUCK")
    body = fixture.state.anchors["BODY_ROOT"]
    pelvis = fixture.state.anchors["PELVIS_REF"]
    a = (float(body.x), float(body.y), _anchor_depth_dp(fixture, "BODY_ROOT"))
    b = (float(pelvis.x), float(pelvis.y), _anchor_depth_dp(fixture, "PELVIS_REF"))
    tangent, vaxis, waxis, length = _segment_frame(a, b)
    if length <= 1e-12:
        return 1e9
    px, py, pz = point
    rx, ry, rz = px - a[0], py - a[1], pz - a[2]
    along = rx * tangent[0] + ry * tangent[1] + rz * tangent[2]
    t_raw = along / length
    t = base._clamp(t_raw, 0.0, 1.0)
    cx = base._lerp(a[0], b[0], t)
    cy = base._lerp(a[1], b[1], t) - p["ventral_lift"] * size * sv * (4.0 * t * (1.0 - t))
    cz = base._lerp(a[2], b[2], t)
    qx, qy, qz = px - cx, py - cy, pz - cz
    vcoord = qx * vaxis[0] + qy * vaxis[1] + qz * vaxis[2]
    wcoord = qx * waxis[0] + qy * waxis[1] + qz * waxis[2]
    axial = 0.0
    if t_raw < 0.0:
        axial = -t_raw * length
    elif t_raw > 1.0:
        axial = (t_raw - 1.0) * length
    rv = base._quadratic_bezier(
        p["start_radius_v"] * size * sv,
        p["mid_radius_v"] * size * sv,
        p["end_radius_v"] * size * sv,
        t,
    )
    rw = base._quadratic_bezier(
        p["start_radius_w"] * size * sw,
        p["mid_radius_w"] * size * sw,
        p["end_radius_w"] * size * sw,
        t,
    )
    cap = math.sqrt(max(rv * rw, 1e-12))
    return base._super_norm((vcoord / max(rv, 1e-9), wcoord / max(rw, 1e-9), axial / max(cap, 1e-9)), 2.0) - 1.0


def _proximal_segment(fixture, hind: bool, side: float):
    region_id = "HIND_PROXIMAL" if hind else "FORE_PROXIMAL"
    p = neutral.REGION_PARAMS[region_id]
    size = float(fixture.size_dp)
    yaw = base._yaw(fixture)
    anchors = fixture.state.anchors
    owner_name = "PELVIS_REF" if hind else "FOREQUARTER_REF"
    owner = anchors[owner_name]
    side_letter = "L" if side > 0.0 else "R"
    paw = anchors[f"{'HIND' if hind else 'FORE'}_PAW_{side_letter}"]
    _, _, sw = _morph_scales(fixture, region_id)
    root_lateral = side * p["root_radius_w"] * size * sw * 0.42
    end_lateral = side * p["root_radius_w"] * size * sw * 0.62
    owner_depth = _anchor_depth_dp(fixture, owner_name)
    a = (
        float(owner.x) + root_lateral * math.sin(yaw),
        float(owner.y),
        owner_depth + root_lateral * math.cos(yaw),
    )
    frac = p["length_fraction"]
    b = (
        float(owner.x) + frac * (float(paw.x) - float(owner.x)) + end_lateral * math.sin(yaw),
        float(owner.y) + frac * (float(paw.y) - float(owner.y)),
        owner_depth * (1.0 - frac) + end_lateral * math.cos(yaw),
    )
    return a, b


def _interface_samples(fixture, interface_id: str):
    anchors = fixture.state.anchors

    def q(name: str):
        point = anchors[name]
        return float(point.x), float(point.y), _anchor_depth_dp(fixture, name)

    if interface_id == "HEAD_NECK":
        return q("HEAD_ROOT"), q("FOREQUARTER_REF")
    if interface_id == "NECK_SHOULDER":
        return q("HEAD_ROOT"), q("FOREQUARTER_REF")
    if interface_id == "SHOULDER_THORAX":
        return q("FOREQUARTER_REF"), q("BODY_ROOT")
    if interface_id == "THORAX_ABDOMEN":
        return q("BODY_ROOT"), q("PELVIS_REF")
    if interface_id == "ABDOMEN_PELVIS":
        return q("BODY_ROOT"), q("PELVIS_REF")
    if interface_id == "SHOULDER_FORE":
        left = _proximal_segment(fixture, False, +1.0)
        right = _proximal_segment(fixture, False, -1.0)
        return left[0], left[1], right[0], right[1]
    if interface_id == "PELVIS_HIND":
        left = _proximal_segment(fixture, True, +1.0)
        right = _proximal_segment(fixture, True, -1.0)
        return left[0], left[1], right[0], right[1]
    raise KeyError(interface_id)


# Install only the pre-evidence transcription/runtime corrections into the frozen base implementation.
base._morph_scales = _morph_scales
base._segment_frame = _segment_frame
base._head_field = _head_field
base._neck_field = _neck_field
base._shoulder_field = _shoulder_field
base._thorax_field = _thorax_field
base._waist_field = _waist_field
base._pelvis_field = _pelvis_field
base._proximal_segment = _proximal_segment
base._interface_samples = _interface_samples


# Re-export the frozen implementation API after installing the adapter.
PROTOTYPE_VERSION = base.PROTOTYPE_VERSION
SOURCE_FAMILY = base.SOURCE_FAMILY
SOURCE_PACK_ID = base.SOURCE_PACK_ID
EXTERNAL_DOMAINS = base.EXTERNAL_DOMAINS
CORRECTION_USE_COUNT = base.CORRECTION_USE_COUNT
DERIVED_SUBDIVISION_STEPS = base.DERIVED_SUBDIVISION_STEPS
RegionalSurfaceResult = base.RegionalSurfaceResult
RasterizedBody = base.RasterizedBody
surface_signature = base.surface_signature
raw_fields = base.raw_fields
composed_field_from_raw = base.composed_field_from_raw
field_value = base.field_value
winning_region = base.winning_region
rasterize_body = base.rasterize_body
interface_overlap_checks = base.interface_overlap_checks
build_surface = base.build_surface
all_primitives = base.all_primitives
primitive_points = base.primitive_points
result_dict = base.result_dict
