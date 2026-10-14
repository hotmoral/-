from __future__ import annotations

from math import cos, pi, sin, sqrt

from model import BodyPoseState, ContactKind, ContactSite, Phase, Rect, Vec2
from orientation_v2 import M0_V2, MorphologyV2, Vec3, project_b3, yaw_label

PAWS = ("FORE_PAW_L", "FORE_PAW_R", "HIND_PAW_L", "HIND_PAW_R")


def _points_rect(points, pad=0.0):
    xs = [point.x for point in points]
    ys = [point.y for point in points]
    return Rect(min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def _shape_bounds(shape):
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


def _union_shapes(shapes):
    result = None
    for shape in shapes:
        bounds = _shape_bounds(shape)
        result = bounds if result is None else result.union(bounds)
    if result is None:
        raise ValueError("at least one shape required")
    return result


def _projected_half_extent(long_half, lateral_half, yaw):
    return sqrt((long_half * cos(yaw)) ** 2 + (lateral_half * sin(yaw)) ** 2)


def _lerp(a, b, t):
    return a * (1.0 - t) + b * t


def _turn_paw_contacts(morphology: MorphologyV2, size_dp: float, t: float):
    scale = size_dp / 2.0
    root_x = size_dp * 1.45
    ground_y = size_dp * 1.38
    trunk = morphology.base.trunk_length
    start_offsets = {
        "HIND_PAW_L": -.58 * scale * trunk,
        "HIND_PAW_R": -.32 * scale * trunk,
        "FORE_PAW_L": .30 * scale * trunk,
        "FORE_PAW_R": .56 * scale * trunk,
    }
    end_offsets = {name: -offset for name, offset in start_offsets.items()}
    paws = {}
    phases = {}

    if t <= .5:
        u = t / .5
        lift = sin(pi * u) * .18 * scale
        for name in PAWS:
            if name.endswith("_L"):
                paws[name] = Vec2(root_x + start_offsets[name], ground_y)
                phases[name] = Phase.CONTACT
            else:
                paws[name] = Vec2(
                    root_x + _lerp(start_offsets[name], end_offsets[name], u),
                    ground_y - lift,
                )
                phases[name] = Phase.CONTACT if t in (0.0, .5) else Phase.SWING
    else:
        u = (t - .5) / .5
        lift = sin(pi * u) * .18 * scale
        for name in PAWS:
            if name.endswith("_R"):
                paws[name] = Vec2(root_x + end_offsets[name], ground_y)
                phases[name] = Phase.CONTACT
            else:
                paws[name] = Vec2(
                    root_x + _lerp(start_offsets[name], end_offsets[name], u),
                    ground_y - lift,
                )
                phases[name] = Phase.CONTACT if t in (.5, 1.0) else Phase.SWING

    return paws, phases


def _limb_shape(root, paw, side_sign, kind, scale, yaw):
    dx = paw.x - root.x
    dy = paw.y - root.y
    lateral_hint = side_sign * sin(yaw) * .09 * scale
    if kind == "fore":
        mid1 = Vec2(root.x + dx * .42 + lateral_hint, root.y + dy * .40)
        mid2 = Vec2(root.x + dx * .78 - lateral_hint * .25, root.y + dy * .78)
        width = .065 * scale
        return {"type": "polyline", "role": "forelimb", "points": [root, mid1, mid2, paw], "width": width}
    stifle = Vec2(root.x + dx * .30 + lateral_hint * 1.25, root.y + dy * .30)
    hock = Vec2(root.x + dx * .66 - lateral_hint, root.y + dy * .70)
    ankle = Vec2(root.x + dx * .86 - lateral_hint * .20, root.y + dy * .87)
    return {"type": "polyline", "role": "hindlimb", "points": [root, stifle, hock, ankle, paw], "width": .075 * scale}


def solve_turn_2p5d(candidate: str, morphology: MorphologyV2, size_dp: float, t: float) -> BodyPoseState:
    if candidate not in {"BM_A", "BM_B", "BM_C"}:
        raise ValueError(candidate)
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be [0,1]")
    morphology.validate()

    base = morphology.base
    scale = size_dp / 2.0
    ground_y = size_dp * 1.38
    body_root_s = Vec2(size_dp * 1.45, ground_y - .88 * scale)
    yaw = pi * t

    trunk_half = .47 * base.trunk_length
    fore_b = Vec3(+trunk_half, 0.02, 0.0)
    pelvis_b = Vec3(-trunk_half, 0.0, 0.0)
    head_b = fore_b + Vec3(.34 * base.head_scale, .18 * base.head_scale, 0.0)
    tail_root_b = pelvis_b + Vec3(-.08, .02, 0.0)

    fore_s = project_b3(fore_b, body_root_s, scale, yaw)
    pelvis_s = project_b3(pelvis_b, body_root_s, scale, yaw)
    head_s = project_b3(head_b, body_root_s, scale, yaw)
    tail_root_s = project_b3(tail_root_b, body_root_s, scale, yaw)

    thorax_half_z = .24 * morphology.thorax_width_scale
    pelvis_half_z = .26 * morphology.pelvis_width_scale
    shapes = []

    if candidate == "BM_A":
        long_half = .62 * base.trunk_length
        lateral_half = .27 * max(morphology.thorax_width_scale, morphology.pelvis_width_scale)
        shapes.append({
            "type": "ellipse",
            "role": "trunk",
            "cx": body_root_s.x,
            "cy": body_root_s.y,
            "rx": scale * _projected_half_extent(long_half, lateral_half, yaw),
            "ry": .32 * scale * base.trunk_depth,
        })
    elif candidate == "BM_B":
        fore_rx = scale * _projected_half_extent(
            .37 * base.forequarter_scale,
            .25 * morphology.thorax_width_scale,
            yaw,
        )
        pelvis_rx = scale * _projected_half_extent(
            .38 * base.pelvis_scale,
            .27 * morphology.pelvis_width_scale,
            yaw,
        )
        shapes.extend([
            {
                "type": "ellipse", "role": "forequarter",
                "cx": fore_s.x, "cy": fore_s.y,
                "rx": fore_rx,
                "ry": .34 * scale * base.trunk_depth * base.forequarter_scale,
            },
            {
                "type": "ellipse", "role": "pelvis",
                "cx": pelvis_s.x, "cy": pelvis_s.y,
                "rx": pelvis_rx,
                "ry": .33 * scale * base.trunk_depth * base.pelvis_scale,
            },
            {
                "type": "line", "role": "spine_bridge",
                "p0": pelvis_s, "p1": fore_s,
                "width": .46 * scale * base.trunk_depth,
            },
        ])
    else:
        extent_x = scale * _projected_half_extent(
            .61 * base.trunk_length,
            .28 * max(morphology.thorax_width_scale, morphology.pelvis_width_scale),
            yaw,
        )
        top = body_root_s.y - .32 * scale * base.trunk_depth
        bottom = body_root_s.y + .30 * scale * base.trunk_depth
        taper = .13 * extent_x
        shapes.append({
            "type": "polygon", "role": "body_envelope",
            "points": [
                Vec2(body_root_s.x - extent_x, body_root_s.y),
                Vec2(body_root_s.x - extent_x + taper, top),
                Vec2(body_root_s.x, top - .02 * scale),
                Vec2(body_root_s.x + extent_x - taper, top),
                Vec2(body_root_s.x + extent_x, body_root_s.y),
                Vec2(body_root_s.x + extent_x - taper, bottom),
                Vec2(body_root_s.x, bottom + .01 * scale),
                Vec2(body_root_s.x - extent_x + taper, bottom),
            ],
        })

    head_long = .255 * base.head_scale
    head_lat = .235 * base.head_scale
    head_rx = scale * _projected_half_extent(head_long, head_lat, yaw)
    head_ry = .23 * scale * base.head_scale
    shapes.append({
        "type": "line", "role": "neck",
        "p0": fore_s, "p1": head_s,
        "width": .30 * scale * base.forequarter_scale,
    })
    shapes.append({
        "type": "ellipse", "role": "head",
        "cx": head_s.x, "cy": head_s.y,
        "rx": head_rx, "ry": head_ry,
    })

    muzzle_b = head_b + Vec3(.16 * base.head_scale, -.03, 0.0)
    muzzle_s = project_b3(muzzle_b, body_root_s, scale, yaw)
    muzzle_rx = scale * _projected_half_extent(.11 * base.head_scale, .12 * base.head_scale, yaw)
    shapes.append({
        "type": "ellipse", "role": "muzzle_silhouette",
        "cx": muzzle_s.x, "cy": muzzle_s.y + .03 * scale,
        "rx": muzzle_rx, "ry": .065 * scale * base.head_scale,
    })

    ear_z = .13 * base.ear_scale
    ear_h = .18 * base.ear_scale
    for side_sign in (+1.0, -1.0):
        base_center = head_b + Vec3(-.03, .17 * base.head_scale, side_sign * ear_z)
        left = project_b3(base_center + Vec3(-.055, 0.0, 0.0), body_root_s, scale, yaw)
        tip = project_b3(base_center + Vec3(0.0, ear_h, 0.0), body_root_s, scale, yaw)
        right = project_b3(base_center + Vec3(.055, 0.0, 0.0), body_root_s, scale, yaw)
        shapes.append({"type": "polygon", "role": "ear", "points": [left, tip, right]})

    tail_local = [
        tail_root_b,
        tail_root_b + Vec3(-.18, .03, 0.00),
        tail_root_b + Vec3(-.40, .08, .06),
        tail_root_b + Vec3(-.58, .24, .18),
        tail_root_b + Vec3(-.62, .44, .26),
    ]
    tail_points = [project_b3(point, body_root_s, scale, yaw) for point in tail_local]
    shapes.append({
        "type": "polyline", "role": "tail",
        "points": tail_points,
        "width": .075 * scale * base.tail_thickness,
    })

    paws, phases = _turn_paw_contacts(morphology, size_dp, t)
    fore_roots = {
        "FORE_PAW_L": project_b3(fore_b + Vec3(0.0, -.06, +thorax_half_z), body_root_s, scale, yaw),
        "FORE_PAW_R": project_b3(fore_b + Vec3(0.0, -.06, -thorax_half_z), body_root_s, scale, yaw),
    }
    hind_roots = {
        "HIND_PAW_L": project_b3(pelvis_b + Vec3(0.0, -.05, +pelvis_half_z), body_root_s, scale, yaw),
        "HIND_PAW_R": project_b3(pelvis_b + Vec3(0.0, -.05, -pelvis_half_z), body_root_s, scale, yaw),
    }

    for name, root in fore_roots.items():
        side_sign = +1.0 if name.endswith("_L") else -1.0
        shapes.append(_limb_shape(root, paws[name], side_sign, "fore", scale, yaw))
    for name, root in hind_roots.items():
        side_sign = +1.0 if name.endswith("_L") else -1.0
        thigh_mid = Vec2((root.x + pelvis_s.x) / 2.0, root.y + .12 * scale)
        shapes.append({
            "type": "ellipse", "role": "hind_thigh",
            "cx": thigh_mid.x, "cy": thigh_mid.y,
            "rx": .13 * scale * base.pelvis_scale,
            "ry": .20 * scale * base.hind_limb_length,
        })
        shapes.append(_limb_shape(root, paws[name], side_sign, "hind", scale, yaw))

    paw_rx = .075 * scale * base.paw_scale
    for name, paw in paws.items():
        shapes.append({
            "type": "ellipse", "role": name,
            "cx": paw.x, "cy": paw.y,
            "rx": paw_rx * 1.15, "ry": paw_rx * .55,
        })

    contacts = []
    support_set = []
    for name in PAWS:
        phase = phases[name]
        load_bearing = phase == Phase.CONTACT
        contact = ContactSite(
            id=f"C_{name}",
            kind=ContactKind.PAW_POINT,
            owner=name,
            phase=phase,
            load_bearing=load_bearing,
            point=paws[name],
            target_point=paws[name] if load_bearing else None,
        )
        contacts.append(contact)
        if load_bearing:
            support_set.append(contact.id)

    visual = _union_shapes(shapes)
    physical = _union_shapes([shape for shape in shapes if shape["role"] not in ("ear", "tail")])
    window = visual.expand(max(1.0, .018 * size_dp))
    resolved = {
        "BODY_ROOT": body_root_s,
        "FOREQUARTER_REF": fore_s,
        "PELVIS_REF": pelvis_s,
        "HEAD_ROOT": head_s,
        "TAIL_ROOT": tail_root_s,
        **paws,
    }
    state = BodyPoseState(
        candidate=candidate,
        morphology_id=morphology.id,
        case_id="H6_CHANGE_FACING_2P5D",
        t=t,
        size_dp=size_dp,
        anchors=resolved,
        contacts=contacts,
        support_set=support_set,
        visual_bounds=visual,
        body_bounds=physical,
        window_bounds=window,
        shapes=shapes,
        notes=[f"bodyYawRad={yaw:.12f}", f"view={yaw_label(yaw)}"],
    )
    return state


if __name__ == "__main__":
    for t in (0.0, .25, .5, .75, 1.0):
        state = solve_turn_2p5d("BM_B", M0_V2, 80, t)
        print(t, state.notes, state.validate())
