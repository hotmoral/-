from __future__ import annotations

from math import pi, sin

from model import BodyPoseState, ContactKind, ContactSite, Phase, Vec2, rect_from_points
from orientation_v2 import MorphologyV2, Vec3, project_b3, yaw_label

FIXTURE_VERSION = "H6N_STEPPED_QUARTER_TURN_V1"
CASE_ID = FIXTURE_VERSION
PAWS = ("FORE_PAW_L", "FORE_PAW_R", "HIND_PAW_L", "HIND_PAW_R")
MIRROR_PAW = {
    "FORE_PAW_L": "FORE_PAW_R",
    "FORE_PAW_R": "FORE_PAW_L",
    "HIND_PAW_L": "HIND_PAW_R",
    "HIND_PAW_R": "HIND_PAW_L",
}
POSITIVE_ORDER = ("HIND_PAW_R", "FORE_PAW_R", "HIND_PAW_L", "FORE_PAW_L")
NEGATIVE_ORDER = tuple(MIRROR_PAW[paw] for paw in POSITIVE_ORDER)
EVENT_COUNT = 4
YAW_PER_EVENT = pi / 8.0
FINAL_YAW_MAGNITUDE = pi / 2.0
LATERAL_HALF_STANCE_BU = 0.22
SWING_CLEARANCE_SCALE = 0.18

_BASE_LONGITUDINAL = {
    "HIND_PAW_L": -0.58,
    "HIND_PAW_R": -0.32,
    "FORE_PAW_L": +0.30,
    "FORE_PAW_R": +0.56,
}


def _validate_direction(direction: int) -> None:
    if direction not in (-1, +1):
        raise ValueError("direction must be -1 or +1")


def _side_sign(paw: str) -> float:
    if paw.endswith("_L"):
        return +1.0
    if paw.endswith("_R"):
        return -1.0
    raise KeyError(paw)


def _smoothstep(u: float) -> float:
    if not 0.0 <= u <= 1.0:
        raise ValueError("u must be [0,1]")
    return u * u * (3.0 - 2.0 * u)


def _lerp(a: float, b: float, t: float) -> float:
    return a * (1.0 - t) + b * t


def event_order(direction: int):
    _validate_direction(direction)
    return POSITIVE_ORDER if direction > 0 else NEGATIVE_ORDER


def stance_anchor_b3(
    paw: str,
    morphology: MorphologyV2,
    direction: int,
    lateral_half_stance_bu: float = LATERAL_HALF_STANCE_BU,
) -> Vec3:
    """Direction-mirrored body-local stance anchor for the H6N V1 fixture.

    The positive direction uses the accepted legacy longitudinal phase as its
    engineering starting stance. The negative direction mirrors the whole phase
    by swapping L/R longitudinal assignments while preserving each paw's actual
    anatomical side sign in Z_B.
    """
    _validate_direction(direction)
    if paw not in PAWS:
        raise KeyError(paw)
    if lateral_half_stance_bu <= 0.0:
        raise ValueError("lateral_half_stance_bu must be positive")

    longitudinal_source = paw if direction > 0 else MIRROR_PAW[paw]
    x_forward = _BASE_LONGITUDINAL[longitudinal_source] * morphology.base.trunk_length
    z_left = _side_sign(paw) * lateral_half_stance_bu * morphology.stance_width_scale
    return Vec3(x_forward, 0.0, z_left)


def stance_target_s(
    paw: str,
    morphology: MorphologyV2,
    size_dp: float,
    direction: int,
    yaw_rad: float,
    lateral_half_stance_bu: float = LATERAL_HALF_STANCE_BU,
) -> Vec2:
    scale = size_dp / 2.0
    root_x = size_dp * 1.45
    ground_y = size_dp * 1.38
    body_root_s = Vec2(root_x, ground_y - 0.88 * scale)
    projected = project_b3(
        stance_anchor_b3(paw, morphology, direction, lateral_half_stance_bu),
        body_root_s,
        scale,
        yaw_rad,
    )
    return Vec2(projected.x, ground_y)


def _targets_after_completed_events(
    morphology: MorphologyV2,
    size_dp: float,
    direction: int,
    completed_events: int,
):
    if not 0 <= completed_events <= EVENT_COUNT:
        raise ValueError("completed_events out of range")

    targets = {
        paw: stance_target_s(paw, morphology, size_dp, direction, 0.0)
        for paw in PAWS
    }
    order = event_order(direction)
    for event_index in range(completed_events):
        paw = order[event_index]
        yaw_end = direction * (event_index + 1) * YAW_PER_EVENT
        targets[paw] = stance_target_s(paw, morphology, size_dp, direction, yaw_end)
    return targets


def _time_state(t: float):
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be [0,1]")

    scaled = t * EVENT_COUNT
    nearest = round(scaled)
    if abs(scaled - nearest) <= 1e-12:
        boundary_index = int(nearest)
        return {
            "boundary": True,
            "completed": boundary_index,
            "event": None,
            "u": None,
        }

    event_index = int(scaled)
    if event_index >= EVENT_COUNT:
        event_index = EVENT_COUNT - 1
    return {
        "boundary": False,
        "completed": event_index,
        "event": event_index,
        "u": scaled - event_index,
    }


def _structural_anchors(morphology: MorphologyV2, size_dp: float, yaw: float):
    base = morphology.base
    scale = size_dp / 2.0
    ground_y = size_dp * 1.38
    body_root_s = Vec2(size_dp * 1.45, ground_y - 0.88 * scale)

    trunk_half = 0.47 * base.trunk_length
    fore_b = Vec3(+trunk_half, 0.02, 0.0)
    pelvis_b = Vec3(-trunk_half, 0.0, 0.0)
    head_b = fore_b + Vec3(0.34 * base.head_scale, 0.18 * base.head_scale, 0.0)
    tail_root_b = pelvis_b + Vec3(-0.08, 0.02, 0.0)

    return {
        "BODY_ROOT": body_root_s,
        "FOREQUARTER_REF": project_b3(fore_b, body_root_s, scale, yaw),
        "PELVIS_REF": project_b3(pelvis_b, body_root_s, scale, yaw),
        "HEAD_ROOT": project_b3(head_b, body_root_s, scale, yaw),
        "TAIL_ROOT": project_b3(tail_root_b, body_root_s, scale, yaw),
    }


def solve_h6n_stepped_turn(
    morphology: MorphologyV2,
    size_dp: float,
    t: float,
    direction: int,
) -> BodyPoseState:
    """Semantic/contact-only H6N stepped 90-degree turn fixture.

    No renderer-specific geometry is authored here. Planted contacts remain exact
    until release; one paw swings per event; BODY_ROOT remains fixed in V1.
    """
    _validate_direction(direction)
    morphology.validate()
    if size_dp <= 0.0:
        raise ValueError("size_dp must be positive")

    time_state = _time_state(t)
    completed = time_state["completed"]
    targets = _targets_after_completed_events(morphology, size_dp, direction, completed)
    order = event_order(direction)
    scale = size_dp / 2.0

    if time_state["boundary"]:
        yaw = direction * completed * YAW_PER_EVENT
        swing_paw = None
        paw_points = dict(targets)
        phases = {paw: Phase.CONTACT for paw in PAWS}
        local_event_u = None
    else:
        event_index = time_state["event"]
        local_event_u = time_state["u"]
        eased = _smoothstep(local_event_u)
        yaw_start = direction * event_index * YAW_PER_EVENT
        yaw_end = direction * (event_index + 1) * YAW_PER_EVENT
        yaw = _lerp(yaw_start, yaw_end, eased)
        swing_paw = order[event_index]

        start_point = targets[swing_paw]
        end_point = stance_target_s(swing_paw, morphology, size_dp, direction, yaw_end)
        lift = sin(pi * eased) * SWING_CLEARANCE_SCALE * scale
        swing_point = Vec2(
            _lerp(start_point.x, end_point.x, eased),
            _lerp(start_point.y, end_point.y, eased) - lift,
        )

        paw_points = dict(targets)
        paw_points[swing_paw] = swing_point
        phases = {
            paw: (Phase.SWING if paw == swing_paw else Phase.CONTACT)
            for paw in PAWS
        }

    anchors = _structural_anchors(morphology, size_dp, yaw)
    anchors.update(paw_points)

    contacts = []
    support_set = []
    for paw in PAWS:
        phase = phases[paw]
        load_bearing = phase == Phase.CONTACT
        contact = ContactSite(
            id=f"C_{paw}",
            kind=ContactKind.PAW_POINT,
            owner=paw,
            phase=phase,
            load_bearing=load_bearing,
            point=paw_points[paw],
            target_point=paw_points[paw] if load_bearing else None,
        )
        contacts.append(contact)
        if load_bearing:
            support_set.append(contact.id)

    semantic_points = list(anchors.values())
    body_points = [
        anchors["BODY_ROOT"],
        anchors["FOREQUARTER_REF"],
        anchors["PELVIS_REF"],
        anchors["HEAD_ROOT"],
        *[anchors[paw] for paw in PAWS],
    ]
    visual_bounds = rect_from_points(semantic_points, pad=0.12 * scale)
    body_bounds = rect_from_points(body_points, pad=0.08 * scale)
    window_bounds = visual_bounds.expand(max(1.0, 0.018 * size_dp))

    direction_label = "POS" if direction > 0 else "NEG"
    event_label = "BOUNDARY" if time_state["boundary"] else str(time_state["event"])
    swing_label = "NONE" if swing_paw is None else swing_paw
    u_label = "NONE" if local_event_u is None else f"{local_event_u:.12f}"

    return BodyPoseState(
        candidate="H6N_SEMANTIC_V1",
        morphology_id=morphology.id,
        case_id=CASE_ID,
        t=float(t),
        size_dp=float(size_dp),
        anchors=anchors,
        contacts=contacts,
        support_set=support_set,
        visual_bounds=visual_bounds,
        body_bounds=body_bounds,
        window_bounds=window_bounds,
        shapes=[],
        notes=[
            f"fixtureVersion={FIXTURE_VERSION}",
            f"bodyYawRad={yaw:.12f}",
            f"view={yaw_label(yaw)}",
            f"direction={direction_label}",
            f"eventIndex={event_label}",
            f"eventU={u_label}",
            f"swingPaw={swing_label}",
        ],
    )
