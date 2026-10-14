from __future__ import annotations

from model import BodyPoseState, ContactKind, ContactSite, Morphology, Phase, Rect, Vec2

PAWS = ("FORE_PAW_L", "FORE_PAW_R", "HIND_PAW_L", "HIND_PAW_R")


def _ellipse_rect(cx: float, cy: float, rx: float, ry: float) -> Rect:
    return Rect(cx - rx, cy - ry, cx + rx, cy + ry)


def _points_rect(points, pad: float = 0.0) -> Rect:
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    return Rect(min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)


def _shape_bounds(shape: dict) -> Rect:
    kind = shape["type"]
    if kind == "ellipse":
        return _ellipse_rect(shape["cx"], shape["cy"], shape["rx"], shape["ry"])
    if kind == "line":
        return _points_rect([shape["p0"], shape["p1"]], shape["width"] / 2.0)
    if kind == "polyline":
        return _points_rect(shape["points"], shape["width"] / 2.0)
    if kind == "polygon":
        return _points_rect(shape["points"])
    raise ValueError(kind)


def _union_shapes(shapes) -> Rect:
    result = None
    for shape in shapes:
        bounds = _shape_bounds(shape)
        result = bounds if result is None else result.union(bounds)
    if result is None:
        raise ValueError("at least one shape required")
    return result


def pose_params(case_id: str) -> dict:
    if case_id in ("H4_SIT", "H4_SIT_TO_STAND"):
        return dict(drop=.30, compress=.80, curve=.14, head_lift=.05)
    if case_id == "H5_CROUCH":
        return dict(drop=.40, compress=.84, curve=.06, head_lift=-.04)
    if case_id in ("H6_TURN_MID", "H6_CHANGE_FACING"):
        return dict(drop=.03, compress=.94, curve=.10, head_lift=.02)
    if case_id in ("H7_NARROW_SUPPORT", "H7_NARROW_SHORT_STEP"):
        return dict(drop=.03, compress=.96, curve=.06, head_lift=.02)
    return dict(drop=0.0, compress=1.0, curve=0.0, head_lift=0.0)


def base_paw_offsets(scale: float, morphology: Morphology, narrow=False, sit=False, crouch=False):
    trunk = morphology.trunk_length
    offsets = {
        "HIND_PAW_L": -.58 * scale * trunk,
        "HIND_PAW_R": -.32 * scale * trunk,
        "FORE_PAW_L": .30 * scale * trunk,
        "FORE_PAW_R": .56 * scale * trunk,
    }
    if narrow:
        offsets = {
            "HIND_PAW_L": -.18 * scale,
            "HIND_PAW_R": -.07 * scale,
            "FORE_PAW_L": .08 * scale,
            "FORE_PAW_R": .19 * scale,
        }
    if sit:
        offsets.update({
            "HIND_PAW_L": -.18 * scale,
            "HIND_PAW_R": -.06 * scale,
            "FORE_PAW_L": .31 * scale,
            "FORE_PAW_R": .43 * scale,
        })
    if crouch:
        offsets = {key: value * .72 for key, value in offsets.items()}
    return offsets


def _leg_polyline(root: Vec2, paw: Vec2, kind: str, direction: float, scale: float):
    delta = paw - root
    if kind == "fore":
        elbow = Vec2(root.x + delta.x * .42 - direction * .07 * scale,
                     root.y + delta.y * .40)
        wrist = Vec2(root.x + delta.x * .76 + direction * .025 * scale,
                     root.y + delta.y * .78)
        return [root, elbow, wrist, paw]
    stifle = Vec2(root.x + delta.x * .32 + direction * .16 * scale,
                  root.y + delta.y * .34)
    hock = Vec2(root.x + delta.x * .68 - direction * .14 * scale,
                root.y + delta.y * .70)
    ankle = Vec2(root.x + delta.x * .86 - direction * .03 * scale,
                 root.y + delta.y * .86)
    return [root, stifle, hock, ankle, paw]


def solve_pose(
    candidate: str,
    morphology: Morphology,
    case_id: str,
    size_dp: float,
    t: float = 0.0,
    root_dx: float = 0.0,
    paws_override=None,
    paw_phases=None,
    yaw_cos: float = 1.0,
    pose_mix=None,
) -> BodyPoseState:
    morphology.validate()
    if candidate not in {"BM_A", "BM_B", "BM_C"}:
        raise ValueError(candidate)

    scale = size_dp / 2.0
    ground_y = size_dp * 1.38
    root_x = size_dp * 1.45 + root_dx
    pose = pose_params(case_id)
    if pose_mix is not None:
        sit = pose_params("H4_SIT")
        neutral = pose_params("H1_NEUTRAL_SUPPORT")
        pose = {key: sit[key] * (1.0 - pose_mix) + neutral[key] * pose_mix for key in sit}

    projection = max(.30, abs(yaw_cos))
    direction = yaw_cos
    facing_sign = 1 if yaw_cos >= 0.0 else -1
    trunk_half = .47 * scale * morphology.trunk_length * pose["compress"]
    body_y = ground_y - (.88 - pose["drop"]) * scale
    pelvis = Vec2(root_x - trunk_half * direction, body_y + pose["curve"] * .25 * scale)
    fore = Vec2(root_x + trunk_half * direction, body_y - pose["curve"] * .40 * scale)
    body_root = Vec2(root_x, (pelvis.y + fore.y) / 2.0)

    if paws_override is None:
        offsets = base_paw_offsets(
            scale,
            morphology,
            narrow=case_id in ("H7_NARROW_SUPPORT", "H7_NARROW_SHORT_STEP"),
            sit=case_id in ("H4_SIT", "H4_SIT_TO_STAND"),
            crouch=case_id == "H5_CROUCH",
        )
        paws = {key: Vec2(root_x + direction * offset, ground_y) for key, offset in offsets.items()}
    else:
        paws = paws_override

    shapes = []
    if candidate == "BM_A":
        shapes.append({
            "type": "ellipse", "role": "trunk", "cx": root_x, "cy": body_root.y + .02 * scale,
            "rx": .62 * scale * morphology.trunk_length * pose["compress"] * projection + .10 * scale * (1.0 - projection),
            "ry": .32 * scale * morphology.trunk_depth,
        })
    elif candidate == "BM_B":
        pelvis_rx = .38 * scale * morphology.pelvis_scale
        pelvis_ry = .33 * scale * morphology.trunk_depth * morphology.pelvis_scale
        fore_rx = .37 * scale * morphology.forequarter_scale
        fore_ry = .34 * scale * morphology.trunk_depth * morphology.forequarter_scale
        shapes.extend([
            {"type": "ellipse", "role": "pelvis", "cx": pelvis.x, "cy": pelvis.y, "rx": pelvis_rx, "ry": pelvis_ry},
            {"type": "ellipse", "role": "forequarter", "cx": fore.x, "cy": fore.y, "rx": fore_rx, "ry": fore_ry},
            {"type": "line", "role": "spine_bridge", "p0": pelvis, "p1": fore, "width": .48 * scale * morphology.trunk_depth},
        ])
    else:
        extent = .62 * scale * morphology.trunk_length * pose["compress"] * projection + .10 * scale * (1.0 - projection)
        top = min(pelvis.y, fore.y) - .32 * scale * morphology.trunk_depth
        bottom = max(pelvis.y, fore.y) + .30 * scale * morphology.trunk_depth
        slope = .07 * scale * direction
        left = root_x - extent
        right = root_x + extent
        points = [
            Vec2(left, body_root.y + .02 * scale),
            Vec2(left + .18 * extent, top + slope),
            Vec2(root_x, top - .02 * scale),
            Vec2(right - .15 * extent, top - slope),
            Vec2(right, body_root.y - .02 * scale),
            Vec2(right - .18 * extent, bottom - slope * .3),
            Vec2(root_x, bottom - .05 * scale),
            Vec2(left + .16 * extent, bottom + slope * .3),
        ]
        shapes.append({"type": "polygon", "role": "body_envelope", "points": points})

    head_r = .255 * scale * morphology.head_scale
    head = Vec2(
        fore.x + direction * (.33 * scale * morphology.head_scale),
        fore.y - .16 * scale * morphology.head_scale - pose["head_lift"] * scale,
    )
    neck_mid = Vec2((fore.x + head.x) / 2.0, (fore.y + head.y) / 2.0 + .04 * scale)
    shapes.append({"type": "line", "role": "neck", "p0": fore, "p1": neck_mid, "width": .34 * scale * morphology.forequarter_scale})
    shapes.append({"type": "ellipse", "role": "head", "cx": head.x, "cy": head.y, "rx": head_r * (.80 + .20 * projection), "ry": head_r * .90})
    muzzle = Vec2(head.x + direction * head_r * .72, head.y + head_r * .18)
    shapes.append({"type": "ellipse", "role": "muzzle_silhouette", "cx": muzzle.x, "cy": muzzle.y, "rx": head_r * .42 * projection + .03 * scale * (1.0 - projection), "ry": head_r * .28})

    ear_h = .18 * scale * morphology.ear_scale
    ear_w = .105 * scale * morphology.ear_scale
    for side in (-1, 1):
        ear_x = head.x + side * ear_w * .55
        shapes.append({
            "type": "polygon", "role": "ear",
            "points": [
                Vec2(ear_x - ear_w * .45, head.y - head_r * .55),
                Vec2(ear_x, head.y - head_r * .55 - ear_h),
                Vec2(ear_x + ear_w * .45, head.y - head_r * .55),
            ],
        })

    tail_root = Vec2(pelvis.x - direction * .08 * scale, pelvis.y - .04 * scale)
    tail_len = .82 * scale * morphology.tail_length
    if case_id in ("H4_SIT", "H4_SIT_TO_STAND"):
        tail_points = [
            tail_root,
            Vec2(tail_root.x - direction * .35 * tail_len, tail_root.y + .18 * scale),
            Vec2(tail_root.x - direction * .58 * tail_len, ground_y - .18 * scale),
            Vec2(tail_root.x - direction * .72 * tail_len, ground_y - .40 * scale),
        ]
    elif case_id == "H5_CROUCH":
        tail_points = [
            tail_root,
            Vec2(tail_root.x - direction * .35 * tail_len, tail_root.y + .12 * scale),
            Vec2(tail_root.x - direction * .70 * tail_len, tail_root.y + .08 * scale),
            Vec2(tail_root.x - direction * .86 * tail_len, tail_root.y - .10 * scale),
        ]
    else:
        tail_points = [
            tail_root,
            Vec2(tail_root.x - direction * .18 * tail_len, tail_root.y + .06 * scale),
            Vec2(tail_root.x - direction * .42 * tail_len, tail_root.y + .02 * scale),
            Vec2(tail_root.x - direction * .64 * tail_len, tail_root.y - .18 * scale),
            Vec2(tail_root.x - direction * .72 * tail_len, tail_root.y - .42 * scale),
        ]
    shapes.append({"type": "polyline", "role": "tail", "points": tail_points, "width": .085 * scale * morphology.tail_thickness})

    for paw_name in ("FORE_PAW_L", "FORE_PAW_R"):
        points = _leg_polyline(fore, paws[paw_name], "fore", direction, scale * morphology.fore_limb_length)
        points = [Vec2((points[0].x + points[1].x) / 2.0, (points[0].y + points[1].y) / 2.0)] + points[1:]
        shapes.append({"type": "polyline", "role": paw_name, "points": points, "width": .070 * scale})

    shapes.append({
        "type": "ellipse", "role": "hind_thigh",
        "cx": pelvis.x - direction * .03 * scale, "cy": pelvis.y + .14 * scale,
        "rx": .18 * scale * morphology.pelvis_scale,
        "ry": .23 * scale * morphology.hind_limb_length,
    })
    for paw_name in ("HIND_PAW_L", "HIND_PAW_R"):
        points = _leg_polyline(pelvis, paws[paw_name], "hind", direction, scale * morphology.hind_limb_length)
        points = [Vec2((points[0].x + points[1].x) / 2.0, (points[0].y + points[1].y) / 2.0)] + points[1:]
        shapes.append({"type": "polyline", "role": paw_name, "points": points, "width": .080 * scale})

    paw_r = .075 * scale * morphology.paw_scale
    for paw_name, paw in paws.items():
        shapes.append({"type": "ellipse", "role": paw_name, "cx": paw.x, "cy": paw.y, "rx": paw_r * 1.15, "ry": paw_r * .55})

    contacts = []
    support_set = []
    for paw_name in PAWS:
        phase = (paw_phases or {}).get(paw_name, Phase.CONTACT)
        load_bearing = phase == Phase.CONTACT
        contact = ContactSite(
            id=f"C_{paw_name}", kind=ContactKind.PAW_POINT, owner=paw_name,
            phase=phase, load_bearing=load_bearing, point=paws[paw_name],
            target_point=paws[paw_name] if load_bearing else None,
        )
        contacts.append(contact)
        if load_bearing:
            support_set.append(contact.id)

    if case_id in ("H4_SIT", "H4_SIT_TO_STAND") and (pose_mix is None or pose_mix < .45):
        contact = ContactSite(
            id="C_HAUNCH", kind=ContactKind.BODY_PATCH, owner="HAUNCH_CONTACT",
            phase=Phase.CONTACT, load_bearing=True,
            point=Vec2(pelvis.x - direction * .05 * scale, ground_y), tangent_extent_dp=.18 * scale,
        )
        contacts.append(contact)
        support_set.append(contact.id)
    if case_id == "H5_CROUCH":
        contact = ContactSite(
            id="C_TRUNK_REST", kind=ContactKind.BODY_PATCH, owner="TRUNK_REST_CONTACT",
            phase=Phase.CONTACT, load_bearing=True,
            point=Vec2(body_root.x, ground_y), tangent_extent_dp=.24 * scale,
        )
        contacts.append(contact)
        support_set.append(contact.id)

    visual = _union_shapes(shapes)
    physical = _union_shapes([shape for shape in shapes if shape["role"] not in ("ear", "tail")])
    window = visual.expand(max(1.0, .018 * size_dp))
    anchors = {
        "BODY_ROOT": body_root,
        "FOREQUARTER_REF": fore,
        "PELVIS_REF": pelvis,
        "HEAD_ROOT": head,
        "TAIL_ROOT": tail_root,
        **paws,
    }
    return BodyPoseState(
        candidate=candidate,
        morphology_id=morphology.id,
        case_id=case_id,
        t=t,
        size_dp=size_dp,
        anchors=anchors,
        contacts=contacts,
        support_set=support_set,
        visual_bounds=visual,
        body_bounds=physical,
        window_bounds=window,
        shapes=shapes,
    )
