from __future__ import annotations

from math import cos, hypot, sin, sqrt

from model import Rect, Vec2
from c3_semantic import morphology_by_id, orientation_morphology_by_id

GROUPS = ("CORE", "FORE", "HIND", "TAIL")
CORRECTION_H4 = "H4_CORE_ENVELOPE"
CORRECTION_H6 = "H6_TURN_ENVELOPE"
ALLOWED_CORRECTIONS = (CORRECTION_H4, CORRECTION_H6)


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
    raise ValueError(kind)


def union_bounds(shapes):
    result = None
    for shape in shapes:
        bounds = shape_bounds(shape)
        result = bounds if result is None else result.union(bounds)
    if result is None:
        raise ValueError("at least one shape required")
    return result


def partition_bounds(shapes, size_dp):
    pad = max(1.0, size_dp * 0.012)
    result = {}
    for group in GROUPS:
        group_shapes = [shape for shape in shapes if shape["group"] == group]
        if group_shapes:
            result[group] = union_bounds(group_shapes).expand(pad)
    return result


def _projected_half_extent(long_half, lateral_half, yaw):
    return sqrt((long_half * cos(yaw)) ** 2 + (lateral_half * sin(yaw)) ** 2)


def _normalize(vector, fallback=Vec2(1.0, 0.0)):
    length = hypot(vector.x, vector.y)
    if length < 1e-9:
        return fallback
    return Vec2(vector.x / length, vector.y / length)


def _add(point, vector, amount):
    return Vec2(point.x + vector.x * amount, point.y + vector.y * amount)


def _load_bearing_contact(state, owner):
    for contact in state.contacts:
        if contact.owner == owner and contact.load_bearing:
            return contact
    return None


def _generic_limb(root, paw, kind, side_sign, scale, yaw):
    dx = paw.x - root.x
    dy = paw.y - root.y
    lateral_hint = side_sign * sin(yaw) * .075 * scale
    if kind == "FORE":
        elbow = Vec2(root.x + dx * .43 + lateral_hint, root.y + dy * .42)
        wrist = Vec2(root.x + dx * .79 - lateral_hint * .20, root.y + dy * .79)
        return {
            "type": "polyline",
            "role": "forelimb",
            "group": "FORE",
            "points": [root, elbow, wrist, paw],
            "width": .060 * scale,
        }
    stifle = Vec2(root.x + dx * .30 + lateral_hint * 1.15, root.y + dy * .30)
    hock = Vec2(root.x + dx * .66 - lateral_hint, root.y + dy * .69)
    ankle = Vec2(root.x + dx * .86 - lateral_hint * .18, root.y + dy * .87)
    return {
        "type": "polyline",
        "role": "hindlimb",
        "group": "HIND",
        "points": [root, stifle, hock, ankle, paw],
        "width": .070 * scale,
    }


def _rf_b_core(state, morphology, yaw):
    scale = state.size_dp / 2.0
    anchors = state.anchors
    body = anchors["BODY_ROOT"]
    fore = anchors["FOREQUARTER_REF"]
    pelvis = anchors["PELVIS_REF"]
    orientation_morph = orientation_morphology_by_id(morphology.id)

    fore_rx = scale * _projected_half_extent(
        .34 * morphology.forequarter_scale,
        .245 * orientation_morph.thorax_width_scale,
        yaw,
    )
    pelvis_rx = scale * _projected_half_extent(
        .37 * morphology.pelvis_scale,
        .265 * orientation_morph.pelvis_width_scale,
        yaw,
    )
    fore_ry = .305 * scale * morphology.trunk_depth * morphology.forequarter_scale
    pelvis_ry = .325 * scale * morphology.trunk_depth * morphology.pelvis_scale
    center_rx = max(.20 * scale, abs(fore.x - pelvis.x) * .38)
    center_ry = .235 * scale * morphology.trunk_depth
    bridge_width = .33 * scale * morphology.trunk_depth

    shapes = [
        {
            "type": "ellipse",
            "role": "forequarter",
            "group": "CORE",
            "cx": fore.x,
            "cy": fore.y,
            "rx": fore_rx,
            "ry": fore_ry,
        },
        {
            "type": "ellipse",
            "role": "trunk_mass",
            "group": "CORE",
            "cx": body.x,
            "cy": body.y + .025 * scale,
            "rx": center_rx,
            "ry": center_ry,
        },
        {
            "type": "ellipse",
            "role": "pelvis",
            "group": "CORE",
            "cx": pelvis.x,
            "cy": pelvis.y,
            "rx": pelvis_rx,
            "ry": pelvis_ry,
        },
        {
            "type": "line",
            "role": "spine_bridge",
            "group": "CORE",
            "p0": pelvis,
            "p1": fore,
            "width": bridge_width,
        },
    ]

    haunch = _load_bearing_contact(state, "HAUNCH_CONTACT")
    if haunch is not None:
        vertical_span = max(.18 * scale, abs(haunch.point.y - pelvis.y))
        center = Vec2(
            pelvis.x - cos(yaw) * .055 * scale,
            (pelvis.y + haunch.point.y) / 2.0,
        )
        shapes.append({
            "type": "ellipse",
            "role": "semantic_haunch_support_mass",
            "group": "CORE",
            "cx": center.x,
            "cy": center.y,
            "rx": .27 * scale * morphology.pelvis_scale,
            "ry": vertical_span * .62 + .10 * scale,
        })
    return shapes


def _rf_c_h4_core(state, morphology, yaw):
    scale = state.size_dp / 2.0
    fore = state.anchors["FOREQUARTER_REF"]
    pelvis = state.anchors["PELVIS_REF"]
    body = state.anchors["BODY_ROOT"]
    sit_strength = (1.0 - state.t) ** 2
    haunch = _load_bearing_contact(state, "HAUNCH_CONTACT")

    if haunch is not None:
        haunch_y = (pelvis.y + haunch.point.y) / 2.0
    else:
        haunch_y = pelvis.y + sit_strength * .16 * scale

    rear_center = Vec2(
        pelvis.x - cos(yaw) * .055 * scale * sit_strength,
        haunch_y,
    )
    chest_center = Vec2(
        fore.x + cos(yaw) * .02 * scale,
        fore.y + .025 * scale,
    )
    waist_center = Vec2(
        body.x,
        body.y + .06 * scale * sit_strength,
    )

    return [
        {
            "type": "ellipse",
            "role": "h4_authored_haunch",
            "group": "CORE",
            "cx": rear_center.x,
            "cy": rear_center.y,
            "rx": (.31 + .04 * sit_strength) * scale * morphology.pelvis_scale,
            "ry": (.29 + .12 * sit_strength) * scale * morphology.trunk_depth,
        },
        {
            "type": "ellipse",
            "role": "h4_authored_waist",
            "group": "CORE",
            "cx": waist_center.x,
            "cy": waist_center.y,
            "rx": .29 * scale * morphology.trunk_length,
            "ry": (.21 + .03 * sit_strength) * scale * morphology.trunk_depth,
        },
        {
            "type": "ellipse",
            "role": "h4_authored_chest",
            "group": "CORE",
            "cx": chest_center.x,
            "cy": chest_center.y,
            "rx": .29 * scale * morphology.forequarter_scale,
            "ry": .31 * scale * morphology.trunk_depth * morphology.forequarter_scale,
        },
        {
            "type": "line",
            "role": "h4_authored_back_bridge",
            "group": "CORE",
            "p0": rear_center,
            "p1": chest_center,
            "width": .29 * scale * morphology.trunk_depth,
        },
    ]


def _rf_c_h6_core(state, morphology, yaw):
    shapes = _rf_b_core(state, morphology, yaw)
    scale = state.size_dp / 2.0
    body = state.anchors["BODY_ROOT"]
    orientation_morph = orientation_morphology_by_id(morphology.id)
    front_strength = sin(yaw) ** 2
    long_half = .46 * scale * morphology.trunk_length
    lateral_half = .285 * scale * max(
        orientation_morph.thorax_width_scale,
        orientation_morph.pelvis_width_scale,
    )
    projected = _projected_half_extent(long_half, lateral_half, yaw)
    shapes.append({
        "type": "ellipse",
        "role": "h6_authored_front_volume",
        "group": "CORE",
        "cx": body.x,
        "cy": body.y + .025 * scale,
        "rx": projected * (.72 + .10 * front_strength),
        "ry": (.25 + .045 * front_strength) * scale * morphology.trunk_depth,
    })
    return shapes


def _shared_head_neck(state, morphology, yaw):
    scale = state.size_dp / 2.0
    fore = state.anchors["FOREQUARTER_REF"]
    head = state.anchors["HEAD_ROOT"]
    axis = _normalize(head - fore, fallback=Vec2(1.0, 0.0))
    orientation_morph = orientation_morphology_by_id(morphology.id)
    head_rx = scale * _projected_half_extent(
        .235 * morphology.head_scale,
        .215 * orientation_morph.thorax_width_scale,
        yaw,
    )
    head_ry = .215 * scale * morphology.head_scale
    muzzle = _add(head, axis, .15 * scale * morphology.head_scale)

    ear_spread = .088 * scale * morphology.ear_scale
    ear_height = .165 * scale * morphology.ear_scale
    ear_base_y = head.y - .52 * head_ry

    return [
        {
            "type": "line",
            "role": "neck",
            "group": "CORE",
            "p0": fore,
            "p1": head,
            "width": .25 * scale * morphology.forequarter_scale,
        },
        {
            "type": "ellipse",
            "role": "head",
            "group": "CORE",
            "cx": head.x,
            "cy": head.y,
            "rx": head_rx,
            "ry": head_ry,
        },
        {
            "type": "ellipse",
            "role": "muzzle_structure",
            "group": "CORE",
            "cx": muzzle.x,
            "cy": muzzle.y + .025 * scale,
            "rx": .092 * scale * morphology.head_scale,
            "ry": .058 * scale * morphology.head_scale,
        },
        {
            "type": "polygon",
            "role": "ear",
            "group": "CORE",
            "points": [
                Vec2(head.x - ear_spread * 1.10, ear_base_y),
                Vec2(head.x - ear_spread * .55, ear_base_y - ear_height),
                Vec2(head.x - ear_spread * .10, ear_base_y),
            ],
        },
        {
            "type": "polygon",
            "role": "ear",
            "group": "CORE",
            "points": [
                Vec2(head.x + ear_spread * .10, ear_base_y),
                Vec2(head.x + ear_spread * .55, ear_base_y - ear_height),
                Vec2(head.x + ear_spread * 1.10, ear_base_y),
            ],
        },
    ]


def _shared_limbs(state, morphology, yaw):
    scale = state.size_dp / 2.0
    fore = state.anchors["FOREQUARTER_REF"]
    pelvis = state.anchors["PELVIS_REF"]
    orientation_morph = orientation_morphology_by_id(morphology.id)

    fore_sep = sin(yaw) * .18 * scale * orientation_morph.thorax_width_scale
    hind_sep = sin(yaw) * .20 * scale * orientation_morph.pelvis_width_scale

    roots = {
        "FORE_PAW_L": Vec2(fore.x + fore_sep, fore.y + .02 * scale),
        "FORE_PAW_R": Vec2(fore.x - fore_sep, fore.y + .02 * scale),
        "HIND_PAW_L": Vec2(pelvis.x + hind_sep, pelvis.y + .04 * scale),
        "HIND_PAW_R": Vec2(pelvis.x - hind_sep, pelvis.y + .04 * scale),
    }

    shapes = []
    for name in ("FORE_PAW_L", "FORE_PAW_R"):
        side = 1.0 if name.endswith("_L") else -1.0
        shapes.append(_generic_limb(roots[name], state.anchors[name], "FORE", side, scale, yaw))
    for name in ("HIND_PAW_L", "HIND_PAW_R"):
        side = 1.0 if name.endswith("_L") else -1.0
        thigh_mid = Vec2(
            (roots[name].x + state.anchors[name].x) / 2.0,
            roots[name].y + .12 * scale,
        )
        shapes.append({
            "type": "ellipse",
            "role": "hind_thigh",
            "group": "HIND",
            "cx": thigh_mid.x,
            "cy": thigh_mid.y,
            "rx": .12 * scale * morphology.pelvis_scale,
            "ry": .18 * scale * morphology.hind_limb_length,
        })
        shapes.append(_generic_limb(roots[name], state.anchors[name], "HIND", side, scale, yaw))

    paw_rx = .070 * scale * morphology.paw_scale
    for name in ("FORE_PAW_L", "FORE_PAW_R", "HIND_PAW_L", "HIND_PAW_R"):
        paw = state.anchors[name]
        group = "FORE" if name.startswith("FORE") else "HIND"
        shapes.append({
            "type": "ellipse",
            "role": name,
            "group": group,
            "cx": paw.x,
            "cy": paw.y,
            "rx": paw_rx * 1.15,
            "ry": paw_rx * .52,
        })
    return shapes


def _shared_tail(state, morphology, yaw):
    scale = state.size_dp / 2.0
    root = state.anchors["TAIL_ROOT"]
    tail_len = .78 * scale * morphology.tail_length
    profile_dir = -1.0 if cos(yaw) >= 0.0 else 1.0
    side_bias = sin(yaw)

    points = [
        root,
        Vec2(root.x + profile_dir * .22 * tail_len + side_bias * .05 * scale, root.y + .04 * scale),
        Vec2(root.x + profile_dir * .48 * tail_len + side_bias * .13 * scale, root.y - .02 * scale),
        Vec2(root.x + profile_dir * .68 * tail_len + side_bias * .22 * scale, root.y - .18 * scale),
        Vec2(root.x + profile_dir * .72 * tail_len + side_bias * .30 * scale, root.y - .38 * scale),
    ]
    return [{
        "type": "polyline",
        "role": "tail",
        "group": "TAIL",
        "points": points,
        "width": .075 * scale * morphology.tail_thickness,
    }]


def render_fixture(fixture, variant):
    if variant not in ("RF_B", "RF_C"):
        raise ValueError(variant)

    state = fixture.state
    morphology = morphology_by_id(fixture.morphology_id)
    yaw = fixture.payload["orientation"]["yawRad"]
    corrections = []

    if variant == "RF_C" and fixture.case_id == "H4_SIT_TO_STAND":
        core = _rf_c_h4_core(state, morphology, yaw)
        corrections.append(CORRECTION_H4)
    elif variant == "RF_C" and fixture.case_id == "H6_CHANGE_FACING_2P5D":
        core = _rf_c_h6_core(state, morphology, yaw)
        corrections.append(CORRECTION_H6)
    else:
        core = _rf_b_core(state, morphology, yaw)

    shapes = []
    shapes.extend(core)
    shapes.extend(_shared_head_neck(state, morphology, yaw))
    shapes.extend(_shared_limbs(state, morphology, yaw))
    shapes.extend(_shared_tail(state, morphology, yaw))

    visual = union_bounds(shapes)
    partitions = partition_bounds(shapes, state.size_dp)
    return {
        "variant": variant,
        "semanticHash": fixture.semantic_hash,
        "caseId": fixture.case_id,
        "morphologyId": fixture.morphology_id,
        "sizeDp": fixture.size_dp,
        "t": fixture.t,
        "shapes": shapes,
        "visualBounds": visual,
        "partitionBounds": partitions,
        "corrections": tuple(corrections),
    }
