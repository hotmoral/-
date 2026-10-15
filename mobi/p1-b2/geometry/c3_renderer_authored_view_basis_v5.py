from __future__ import annotations

from math import cos, pi, sin

from model import Vec2
from c3_renderer_minimal_v3 import render_fixture as render_fixture_v3
from c3_renderers import partition_bounds, union_bounds
from c3_semantic import morphology_by_id, orientation_morphology_by_id


AUTHORED_VIEW_BASIS_VERSION = "AUTHORED_STRUCTURAL_VIEW_BASIS_V1"
BASIS_NAMES = ("PROFILE", "THREE_QUARTER", "FRONT")

# Normalized structural concepts, not animation frames or final art.
# One shared set is reused across morphology, size and time.
VIEW_BASES = {
    "PROFILE": {
        "thorax_half": 0.245,
        "pelvis_half": 0.265,
        "waist_half": 0.205,
        "thorax_depth": 0.300,
        "pelvis_depth": 0.320,
        "waist_depth": 0.215,
        "fore_root_spread": 0.070,
        "hind_root_spread": 0.085,
        "fore_corridor": 0.100,
        "hind_corridor": 0.120,
        "neck_width": 0.245,
        "head_half": 0.230,
        "muzzle_half": 0.095,
        "ear_spread": 0.080,
    },
    "THREE_QUARTER": {
        "thorax_half": 0.315,
        "pelvis_half": 0.335,
        "waist_half": 0.245,
        "thorax_depth": 0.315,
        "pelvis_depth": 0.335,
        "waist_depth": 0.220,
        "fore_root_spread": 0.170,
        "hind_root_spread": 0.195,
        "fore_corridor": 0.215,
        "hind_corridor": 0.255,
        "neck_width": 0.205,
        "head_half": 0.245,
        "muzzle_half": 0.120,
        "ear_spread": 0.100,
    },
    "FRONT": {
        "thorax_half": 0.355,
        "pelvis_half": 0.380,
        "waist_half": 0.270,
        "thorax_depth": 0.320,
        "pelvis_depth": 0.345,
        "waist_depth": 0.225,
        "fore_root_spread": 0.235,
        "hind_root_spread": 0.265,
        "fore_corridor": 0.285,
        "hind_corridor": 0.330,
        "neck_width": 0.165,
        "head_half": 0.255,
        "muzzle_half": 0.140,
        "ear_spread": 0.115,
    },
}


def _lerp(a, b, t):
    return a * (1.0 - t) + b * t


def _basis_weights(yaw):
    """Continuous symmetric profile->3/4->front->3/4->profile weights."""
    phase = yaw % pi
    view_angle = phase if phase <= pi / 2.0 else pi - phase
    u = view_angle / (pi / 2.0)
    if u <= 0.5:
        t = u * 2.0
        return {"PROFILE": 1.0 - t, "THREE_QUARTER": t, "FRONT": 0.0}
    t = (u - 0.5) * 2.0
    return {"PROFILE": 0.0, "THREE_QUARTER": 1.0 - t, "FRONT": t}


def _blended_basis(yaw):
    weights = _basis_weights(yaw)
    keys = tuple(VIEW_BASES["PROFILE"].keys())
    return {
        key: sum(VIEW_BASES[name][key] * weights[name] for name in BASIS_NAMES)
        for key in keys
    }, weights


def _view_depth(x_forward, z_left, yaw):
    return x_forward * sin(yaw) - z_left * cos(yaw)


def _with_order(shape, depth, bias=0.0):
    return {
        **shape,
        "_viewDepth": float(depth),
        "_orderBias": float(bias),
    }


def _sorted_shapes(shapes):
    return sorted(
        shapes,
        key=lambda item: (
            item.get("_viewDepth", 0.0),
            item.get("_orderBias", 0.0),
            item.get("role", ""),
        ),
    )


def _side_screen(side_sign, yaw):
    # Accepted B3 local +Z (anatomical left) projects by sin(yaw).
    return side_sign * sin(yaw)


def _chest_polygon(center, half_w, half_h):
    # Feline structural chest: broad shoulder zone, tapered sternum/waist edge.
    return [
        Vec2(center.x - half_w * 0.62, center.y - half_h),
        Vec2(center.x + half_w * 0.62, center.y - half_h),
        Vec2(center.x + half_w, center.y - half_h * 0.10),
        Vec2(center.x + half_w * 0.54, center.y + half_h),
        Vec2(center.x - half_w * 0.54, center.y + half_h),
        Vec2(center.x - half_w, center.y - half_h * 0.10),
    ]


def _pelvis_polygon(center, half_w, half_h):
    # Haunch-dominant lower mass, distinct from the chest shield.
    return [
        Vec2(center.x - half_w * 0.72, center.y - half_h),
        Vec2(center.x + half_w * 0.72, center.y - half_h),
        Vec2(center.x + half_w, center.y + half_h * 0.18),
        Vec2(center.x + half_w * 0.68, center.y + half_h),
        Vec2(center.x - half_w * 0.68, center.y + half_h),
        Vec2(center.x - half_w, center.y + half_h * 0.18),
    ]


def _limb_route(root, paw, body_x, side_sign, yaw, corridor, kind, scale):
    """Authored structural route retargeted to the exact semantic paw endpoint.

    The proximal/intermediate points remain in an anatomical side corridor and
    any required cross-body travel is delayed toward the distal/ground region.
    """
    side = _side_screen(side_sign, yaw)
    corridor_x = body_x + side * corridor * scale
    dy = paw.y - root.y

    if kind == "FORE":
        elbow = Vec2(
            _lerp(root.x, corridor_x, 0.72),
            root.y + dy * 0.35,
        )
        wrist = Vec2(
            _lerp(corridor_x, paw.x, 0.46),
            root.y + dy * 0.76,
        )
        return [root, elbow, wrist, paw]

    stifle = Vec2(
        _lerp(root.x, corridor_x, 0.82),
        root.y + dy * 0.29,
    )
    hock = Vec2(
        _lerp(corridor_x, paw.x, 0.26),
        root.y + dy * 0.62,
    )
    ankle = Vec2(
        _lerp(corridor_x, paw.x, 0.78),
        root.y + dy * 0.86,
    )
    return [root, stifle, hock, ankle, paw]


def _render_h6(fixture, variant):
    if variant not in ("RF_B", "RF_C"):
        raise ValueError(variant)

    # Accepted v3 is used only as an immutable source for the continuous tail.
    accepted = render_fixture_v3(fixture, variant)
    state = fixture.state
    morphology = morphology_by_id(fixture.morphology_id)
    orient = orientation_morphology_by_id(fixture.morphology_id)
    yaw = fixture.payload["orientation"]["yawRad"]
    scale = state.size_dp / 2.0
    basis, weights = _blended_basis(yaw)

    anchors = state.anchors
    body = anchors["BODY_ROOT"]
    fore = anchors["FOREQUARTER_REF"]
    pelvis = anchors["PELVIS_REF"]
    head = anchors["HEAD_ROOT"]

    trunk_half = 0.47 * morphology.trunk_length
    fore_x = +trunk_half
    pelvis_x = -trunk_half
    head_x = fore_x + 0.34 * morphology.head_scale
    tail_x = pelvis_x - 0.08

    shapes = []

    thorax_half = basis["thorax_half"] * scale * orient.thorax_width_scale
    pelvis_half = basis["pelvis_half"] * scale * orient.pelvis_width_scale
    waist_half = basis["waist_half"] * scale * max(
        orient.thorax_width_scale, orient.pelvis_width_scale
    )
    thorax_h = basis["thorax_depth"] * scale * morphology.trunk_depth * morphology.forequarter_scale
    pelvis_h = basis["pelvis_depth"] * scale * morphology.trunk_depth * morphology.pelvis_scale
    waist_h = basis["waist_depth"] * scale * morphology.trunk_depth

    # Body masses intentionally use different structural topology from the
    # failed all-parametric C3R ellipses: chest and pelvis have authored target
    # organization while the waist stays a deformable bridge mass.
    shapes.append(_with_order({
        "type": "polygon",
        "role": "basis_chest",
        "group": "CORE",
        "points": _chest_polygon(fore, thorax_half, thorax_h),
    }, _view_depth(fore_x, 0.0, yaw), 0.10))

    shapes.append(_with_order({
        "type": "ellipse",
        "role": "basis_waist",
        "group": "CORE",
        "cx": body.x,
        "cy": body.y + 0.035 * scale,
        "rx": waist_half,
        "ry": waist_h,
    }, _view_depth(0.0, 0.0, yaw), 0.00))

    shapes.append(_with_order({
        "type": "polygon",
        "role": "basis_pelvis",
        "group": "CORE",
        "points": _pelvis_polygon(pelvis, pelvis_half, pelvis_h),
    }, _view_depth(pelvis_x, 0.0, yaw), -0.10))

    shapes.append(_with_order({
        "type": "line",
        "role": "basis_spine_bridge",
        "group": "CORE",
        "p0": pelvis,
        "p1": fore,
        "width": (0.25 + 0.04 * weights["PROFILE"]) * scale * morphology.trunk_depth,
    }, _view_depth(0.0, 0.0, yaw), -0.05))

    # Head/neck/chest relation. The head anchor remains canonical; only the
    # visual envelope and neck bridge are basis-conditioned.
    neck_width = basis["neck_width"] * scale * morphology.forequarter_scale
    shapes.append(_with_order({
        "type": "line",
        "role": "basis_neck",
        "group": "CORE",
        "p0": fore,
        "p1": head,
        "width": neck_width,
    }, _view_depth((fore_x + head_x) / 2.0, 0.0, yaw), 0.18))

    head_half = basis["head_half"] * scale * morphology.head_scale
    shapes.append(_with_order({
        "type": "ellipse",
        "role": "basis_head",
        "group": "CORE",
        "cx": head.x,
        "cy": head.y,
        "rx": head_half,
        "ry": 0.215 * scale * morphology.head_scale,
    }, _view_depth(head_x, 0.0, yaw), 0.24))

    muzzle_forward = cos(yaw) * 0.14 * scale * morphology.head_scale
    shapes.append(_with_order({
        "type": "ellipse",
        "role": "basis_muzzle",
        "group": "CORE",
        "cx": head.x + muzzle_forward,
        "cy": head.y + 0.030 * scale,
        "rx": basis["muzzle_half"] * scale * morphology.head_scale,
        "ry": 0.058 * scale * morphology.head_scale,
    }, _view_depth(head_x + 0.14 * morphology.head_scale, 0.0, yaw), 0.30))

    ear_spread = basis["ear_spread"] * scale * morphology.ear_scale
    ear_height = 0.165 * scale * morphology.ear_scale
    ear_y = head.y - 0.50 * (0.215 * scale * morphology.head_scale)
    ear_z = 0.12 * morphology.ear_scale
    for side_name, side_sign in (("L", +1.0), ("R", -1.0)):
        side = _side_screen(side_sign, yaw)
        center_x = head.x + side * ear_spread
        shapes.append(_with_order({
            "type": "polygon",
            "role": f"basis_ear_{side_name}",
            "group": "CORE",
            "points": [
                Vec2(center_x - ear_spread * 0.44, ear_y),
                Vec2(center_x, ear_y - ear_height),
                Vec2(center_x + ear_spread * 0.44, ear_y),
            ],
        }, _view_depth(head_x - 0.03, side_sign * ear_z, yaw), 0.34))

    # Limbs: exact semantic paws, authored structural corridors for proximal and
    # intermediate organization. No sample-specific correction table exists.
    limb_items = []
    for name in ("FORE_PAW_L", "FORE_PAW_R"):
        side_sign = +1.0 if name.endswith("_L") else -1.0
        side = _side_screen(side_sign, yaw)
        root_z = side_sign * basis["fore_root_spread"] * orient.thorax_width_scale
        root = Vec2(
            fore.x + side * basis["fore_root_spread"] * scale * orient.thorax_width_scale,
            fore.y + 0.035 * scale,
        )
        depth = _view_depth(fore_x, root_z, yaw)
        points = _limb_route(
            root,
            anchors[name],
            body.x,
            side_sign,
            yaw,
            basis["fore_corridor"] * orient.thorax_width_scale,
            "FORE",
            scale,
        )
        limb_items.append((name, "FORE", side_sign, depth, points))

    for name in ("HIND_PAW_L", "HIND_PAW_R"):
        side_sign = +1.0 if name.endswith("_L") else -1.0
        side = _side_screen(side_sign, yaw)
        root_z = side_sign * basis["hind_root_spread"] * orient.pelvis_width_scale
        root = Vec2(
            pelvis.x + side * basis["hind_root_spread"] * scale * orient.pelvis_width_scale,
            pelvis.y + 0.055 * scale,
        )
        depth = _view_depth(pelvis_x, root_z, yaw)
        points = _limb_route(
            root,
            anchors[name],
            body.x,
            side_sign,
            yaw,
            basis["hind_corridor"] * orient.pelvis_width_scale,
            "HIND",
            scale,
        )
        limb_items.append((name, "HIND", side_sign, depth, points))

    for name, kind, side_sign, depth, points in limb_items:
        side_name = "L" if side_sign > 0 else "R"
        group = kind
        if kind == "HIND":
            stifle = points[1]
            root = points[0]
            thigh_center = Vec2(
                _lerp(root.x, stifle.x, 0.48),
                _lerp(root.y, stifle.y, 0.48),
            )
            shapes.append(_with_order({
                "type": "ellipse",
                "role": f"basis_hind_thigh_{side_name}",
                "group": "HIND",
                "cx": thigh_center.x,
                "cy": thigh_center.y,
                "rx": 0.105 * scale * morphology.pelvis_scale,
                "ry": 0.165 * scale * morphology.hind_limb_length,
            }, depth, -0.04))

        shapes.append(_with_order({
            "type": "polyline",
            "role": f"basis_{kind.lower()}limb_{side_name}",
            "group": group,
            "points": points,
            "width": (0.058 if kind == "FORE" else 0.067) * scale,
        }, depth, 0.00))

        paw = anchors[name]
        paw_rx = 0.070 * scale * morphology.paw_scale
        shapes.append(_with_order({
            "type": "ellipse",
            "role": name,
            "group": group,
            "cx": paw.x,
            "cy": paw.y,
            "rx": paw_rx * 1.15,
            "ry": paw_rx * 0.52,
        }, depth, 0.10))

    # Preserve the accepted continuous-tail geometry exactly.
    tail_shapes = [shape for shape in accepted["shapes"] if shape.get("role") == "tail"]
    if len(tail_shapes) != 1:
        raise RuntimeError(f"expected one accepted tail shape, got {len(tail_shapes)}")
    tail = dict(tail_shapes[0])
    tail["group"] = "TAIL"
    shapes.append(_with_order(tail, _view_depth(tail_x, 0.08, yaw), -0.20))

    shapes = _sorted_shapes(shapes)
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
        "corrections": tuple(),
        "authoredViewBasisVersion": AUTHORED_VIEW_BASIS_VERSION,
        "basisWeights": tuple((name, weights[name]) for name in BASIS_NAMES),
    }


def render_fixture(fixture, variant):
    if fixture.case_id != "H6_CHANGE_FACING_2P5D":
        rendered = render_fixture_v3(fixture, variant)
        return {
            **rendered,
            "authoredViewBasisVersion": AUTHORED_VIEW_BASIS_VERSION,
        }
    return _render_h6(fixture, variant)
