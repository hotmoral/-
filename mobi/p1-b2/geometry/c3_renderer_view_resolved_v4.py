from __future__ import annotations

from math import cos, sin, sqrt

from model import Vec2
from c3_renderer_minimal_v3 import render_fixture as render_fixture_v3
from c3_renderers import partition_bounds, union_bounds
from c3_semantic import morphology_by_id, orientation_morphology_by_id


VIEW_REPRESENTATION_VERSION = "VIEW_RESOLVED_2P5D_V1"


def _projected_half_extent(long_half, lateral_half, yaw):
    return sqrt((long_half * cos(yaw)) ** 2 + (lateral_half * sin(yaw)) ** 2)


def _view_depth(x_forward, z_left, yaw):
    """Renderer-only near score derived from the accepted B3+yaw rotation.

    Larger values are nearer to the viewer and are drawn later. This is not a
    new physical/environment coordinate and never changes canonical semantics.
    """
    return x_forward * sin(yaw) - z_left * cos(yaw)


def _shape(shape, depth, bias=0.0):
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


def _front_strength(yaw):
    value = sin(yaw)
    return value * value


def _three_quarter_strength(yaw):
    return abs(sin(2.0 * yaw))


def _view_limb(root, paw, kind, side_sign, scale, yaw):
    """Side-preserving limb routing with exact semantic paw endpoints.

    At profile the additional lateral route vanishes. Toward frontal views the
    intermediate joints bow toward their anatomical side so crossing limbs do
    not collapse into one unresolved X. Paw endpoints remain untouched.
    """
    dx = paw.x - root.x
    dy = paw.y - root.y
    front = _front_strength(yaw)
    qtr = _three_quarter_strength(yaw)
    outward = side_sign * sin(yaw) * scale * (0.09 + 0.055 * front + 0.018 * qtr)

    if kind == "FORE":
        elbow = Vec2(
            root.x + dx * 0.40 + outward,
            root.y + dy * 0.40,
        )
        wrist = Vec2(
            root.x + dx * 0.76 + outward * 0.42,
            root.y + dy * 0.77,
        )
        return {
            "type": "polyline",
            "points": [root, elbow, wrist, paw],
            "width": 0.060 * scale,
        }

    stifle = Vec2(
        root.x + dx * 0.29 + outward * 1.18,
        root.y + dy * 0.30,
    )
    hock = Vec2(
        root.x + dx * 0.64 - outward * 0.18,
        root.y + dy * 0.68,
    )
    ankle = Vec2(
        root.x + dx * 0.86 + outward * 0.08,
        root.y + dy * 0.87,
    )
    return {
        "type": "polyline",
        "points": [root, stifle, hock, ankle, paw],
        "width": 0.070 * scale,
    }


def _render_h6(fixture, variant):
    if variant not in ("RF_B", "RF_C"):
        raise ValueError(variant)

    # Reuse the accepted v3 semantic identity and continuous-tail validity path.
    # Only the H6 visual structure below is replaced.
    base_rendered = render_fixture_v3(fixture, variant)
    state = fixture.state
    morphology = morphology_by_id(fixture.morphology_id)
    orientation_morph = orientation_morphology_by_id(fixture.morphology_id)
    yaw = fixture.payload["orientation"]["yawRad"]
    scale = state.size_dp / 2.0
    front = _front_strength(yaw)
    qtr = _three_quarter_strength(yaw)

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

    # View-resolved core. Profile dimensions preserve the accepted generic base;
    # frontal lateral dimensions are deliberately wider than the old projection
    # so the body does not collapse into a narrow mechanical column.
    fore_long = 0.34 * morphology.forequarter_scale
    fore_lat = (0.300 + 0.014 * qtr) * orientation_morph.thorax_width_scale
    pelvis_long = 0.37 * morphology.pelvis_scale
    pelvis_lat = (0.320 + 0.014 * qtr) * orientation_morph.pelvis_width_scale

    fore_rx = scale * _projected_half_extent(fore_long, fore_lat, yaw)
    pelvis_rx = scale * _projected_half_extent(pelvis_long, pelvis_lat, yaw)

    center_profile_rx = max(0.20 * scale, abs(fore.x - pelvis.x) * 0.38)
    center_front_rx = (
        0.255
        * scale
        * max(orientation_morph.thorax_width_scale, orientation_morph.pelvis_width_scale)
    )
    center_rx = (
        center_profile_rx * (1.0 - front)
        + center_front_rx * front
        + 0.010 * scale * qtr
    )

    bridge_width = (0.33 - 0.070 * front) * scale * morphology.trunk_depth

    shapes.extend([
        _shape({
            "type": "ellipse",
            "role": "forequarter",
            "group": "CORE",
            "cx": fore.x,
            "cy": fore.y,
            "rx": fore_rx,
            "ry": 0.305 * scale * morphology.trunk_depth * morphology.forequarter_scale,
        }, _view_depth(fore_x, 0.0, yaw), 0.10),
        _shape({
            "type": "ellipse",
            "role": "trunk_mass",
            "group": "CORE",
            "cx": body.x,
            "cy": body.y + 0.025 * scale,
            "rx": center_rx,
            "ry": 0.235 * scale * morphology.trunk_depth,
        }, _view_depth(0.0, 0.0, yaw), 0.00),
        _shape({
            "type": "ellipse",
            "role": "pelvis",
            "group": "CORE",
            "cx": pelvis.x,
            "cy": pelvis.y,
            "rx": pelvis_rx,
            "ry": 0.325 * scale * morphology.trunk_depth * morphology.pelvis_scale,
        }, _view_depth(pelvis_x, 0.0, yaw), -0.10),
        _shape({
            "type": "line",
            "role": "waist_bridge",
            "group": "CORE",
            "p0": pelvis,
            "p1": fore,
            "width": bridge_width,
        }, _view_depth(0.0, 0.0, yaw), -0.05),
    ])

    # Head / neck relation. Frontal neck narrowing keeps the head distinct from
    # the widened forequarter while the muzzle widens structurally toward front.
    head_long = 0.235 * morphology.head_scale
    head_lat = 0.245 * morphology.head_scale
    head_rx = scale * _projected_half_extent(head_long, head_lat, yaw)
    head_ry = 0.215 * scale * morphology.head_scale
    neck_width = (
        (0.25 * (1.0 - front) + 0.175 * front)
        * scale
        * morphology.forequarter_scale
    )

    shapes.append(_shape({
        "type": "line",
        "role": "neck",
        "group": "CORE",
        "p0": fore,
        "p1": head,
        "width": neck_width,
    }, _view_depth((fore_x + head_x) / 2.0, 0.0, yaw), 0.15))
    shapes.append(_shape({
        "type": "ellipse",
        "role": "head",
        "group": "CORE",
        "cx": head.x,
        "cy": head.y,
        "rx": head_rx,
        "ry": head_ry,
    }, _view_depth(head_x, 0.0, yaw), 0.20))

    muzzle_x = head.x + cos(yaw) * 0.15 * scale * morphology.head_scale
    muzzle_rx = (
        (0.092 * (1.0 - front) + 0.135 * front)
        * scale
        * morphology.head_scale
    )
    shapes.append(_shape({
        "type": "ellipse",
        "role": "muzzle_structure",
        "group": "CORE",
        "cx": muzzle_x,
        "cy": head.y + 0.025 * scale,
        "rx": muzzle_rx,
        "ry": 0.058 * scale * morphology.head_scale,
    }, _view_depth(head_x + 0.15 * morphology.head_scale, 0.0, yaw), 0.30))

    ear_spread = 0.088 * scale * morphology.ear_scale * (1.0 + 0.20 * front)
    ear_height = 0.165 * scale * morphology.ear_scale
    ear_base_y = head.y - 0.52 * head_ry
    ear_z = 0.12 * morphology.ear_scale
    for side_name, side_sign in (("L", +1.0), ("R", -1.0)):
        center_x = head.x + side_sign * ear_spread
        shapes.append(_shape({
            "type": "polygon",
            "role": f"ear_{side_name}",
            "group": "CORE",
            "points": [
                Vec2(center_x - 0.45 * ear_spread, ear_base_y),
                Vec2(center_x, ear_base_y - ear_height),
                Vec2(center_x + 0.45 * ear_spread, ear_base_y),
            ],
        }, _view_depth(head_x - 0.03, side_sign * ear_z, yaw), 0.35))

    # Limbs use exact semantic paw endpoints. Only intermediate render joints and
    # ordering change. L/R semantic identity is retained in the role names.
    fore_sep = (
        sin(yaw)
        * (0.18 + 0.025 * front)
        * scale
        * orientation_morph.thorax_width_scale
    )
    hind_sep = (
        sin(yaw)
        * (0.20 + 0.030 * front)
        * scale
        * orientation_morph.pelvis_width_scale
    )

    limb_specs = []
    for name in ("FORE_PAW_L", "FORE_PAW_R"):
        side_sign = +1.0 if name.endswith("_L") else -1.0
        root = Vec2(
            fore.x + side_sign * fore_sep,
            fore.y + 0.02 * scale,
        )
        local_z = side_sign * (0.18 + 0.025 * front) * orientation_morph.thorax_width_scale
        depth = _view_depth(fore_x, local_z, yaw)
        limb_specs.append((name, "FORE", side_sign, root, depth))

    for name in ("HIND_PAW_L", "HIND_PAW_R"):
        side_sign = +1.0 if name.endswith("_L") else -1.0
        root = Vec2(
            pelvis.x + side_sign * hind_sep,
            pelvis.y + 0.04 * scale,
        )
        local_z = side_sign * (0.20 + 0.030 * front) * orientation_morph.pelvis_width_scale
        depth = _view_depth(pelvis_x, local_z, yaw)
        limb_specs.append((name, "HIND", side_sign, root, depth))

    for name, kind, side_sign, root, depth in limb_specs:
        paw = anchors[name]
        side_name = "L" if side_sign > 0.0 else "R"
        limb = _view_limb(root, paw, kind, side_sign, scale, yaw)
        limb.update({
            "role": f"{kind.lower()}limb_{side_name}",
            "group": kind,
        })

        if kind == "HIND":
            stifle = limb["points"][1]
            thigh_center = Vec2(
                root.x * 0.58 + stifle.x * 0.42,
                root.y * 0.58 + stifle.y * 0.42,
            )
            shapes.append(_shape({
                "type": "ellipse",
                "role": f"hind_thigh_{side_name}",
                "group": "HIND",
                "cx": thigh_center.x,
                "cy": thigh_center.y,
                "rx": 0.115 * scale * morphology.pelvis_scale,
                "ry": 0.175 * scale * morphology.hind_limb_length,
            }, depth, -0.02))

        shapes.append(_shape(limb, depth, 0.00))

        paw_rx = 0.070 * scale * morphology.paw_scale
        shapes.append(_shape({
            "type": "ellipse",
            "role": name,
            "group": kind,
            "cx": paw.x,
            "cy": paw.y,
            "rx": paw_rx * 1.15,
            "ry": paw_rx * 0.52,
        }, depth, 0.08))

    # Preserve the accepted continuous tail geometry exactly from v3.
    tail_shapes = [shape for shape in base_rendered["shapes"] if shape.get("role") == "tail"]
    if len(tail_shapes) != 1:
        raise RuntimeError(f"expected one accepted tail shape, got {len(tail_shapes)}")
    tail = dict(tail_shapes[0])
    tail["role"] = "tail"
    tail["group"] = "TAIL"
    shapes.append(_shape(tail, _view_depth(tail_x, 0.08, yaw), -0.20))

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
        "viewRepresentationVersion": VIEW_REPRESENTATION_VERSION,
    }


def render_fixture(fixture, variant):
    if fixture.case_id != "H6_CHANGE_FACING_2P5D":
        rendered = render_fixture_v3(fixture, variant)
        return {
            **rendered,
            "viewRepresentationVersion": VIEW_REPRESENTATION_VERSION,
        }
    return _render_h6(fixture, variant)
