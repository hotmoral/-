from __future__ import annotations

from math import pi, sin

from h6n_stepped_turn import (
    LATERAL_HALF_STANCE_BU,
    MIRROR_PAW,
    PAWS,
    SWING_CLEARANCE_SCALE,
    YAW_PER_EVENT,
    _structural_anchors as _v1_structural_anchors,
    stance_target_s,
)
from model import BodyPoseState, ContactKind, ContactSite, Phase, Vec2, rect_from_points
from orientation_v2 import MorphologyV2, yaw_label

FIXTURE_VERSION = "H6N_STEPPED_QUARTER_TURN_V2_ROOT_SHIFT"
CASE_ID = FIXTURE_VERSION
POSITIVE_ORDER = ("FORE_PAW_L", "HIND_PAW_R", "FORE_PAW_R", "HIND_PAW_L")
NEGATIVE_ORDER = tuple(MIRROR_PAW[paw] for paw in POSITIVE_ORDER)
EVENT_COUNT = 4
LOGICAL_PHASE_COUNT = 5
SHIFT_PHASE_INDEX = 3
SHIFT_ONSET_COMPLETED_EVENTS = 3
ROOT_SHIFT_NORMALIZED = 0.17629717139304296
FINAL_YAW_MAGNITUDE = pi / 2.0
EPS = 1e-12


def _validate_direction(direction: int) -> None:
    if direction not in (-1, +1):
        raise ValueError("direction must be -1 or +1")


def _smoothstep(u: float) -> float:
    if not 0.0 <= u <= 1.0:
        raise ValueError("u must be [0,1]")
    return u * u * (3.0 - 2.0 * u)


def _lerp(a: float, b: float, t: float) -> float:
    return a * (1.0 - t) + b * t


def event_order(direction: int):
    _validate_direction(direction)
    return POSITIVE_ORDER if direction > 0 else NEGATIVE_ORDER


def root_shift_dp(size_dp: float, progress: float = 1.0) -> float:
    if size_dp <= 0.0:
        raise ValueError("size_dp must be positive")
    if not 0.0 <= progress <= 1.0:
        raise ValueError("progress must be [0,1]")
    return ROOT_SHIFT_NORMALIZED * (size_dp / 2.0) * progress


def shifted_stance_target_s(
    paw: str,
    morphology: MorphologyV2,
    size_dp: float,
    direction: int,
    yaw_rad: float,
    root_shift_progress: float,
    lateral_half_stance_bu: float = LATERAL_HALF_STANCE_BU,
) -> Vec2:
    """Body-relative stance target under the accepted H6N screen-tangent mirror convention.

    The negative turn mirrors paw identity/order and yaw sign. Corresponding mirrored
    paws retain equal screen-space coordinates, so the selected scalar screen-tangent
    BODY_ROOT offset has the same sign for both directions.
    """
    base = stance_target_s(
        paw,
        morphology,
        size_dp,
        direction,
        yaw_rad,
        lateral_half_stance_bu,
    )
    return Vec2(base.x + root_shift_dp(size_dp, root_shift_progress), base.y)


def _targets_after_completed_events(
    morphology: MorphologyV2,
    size_dp: float,
    direction: int,
    completed_events: int,
    lateral_half_stance_bu: float,
):
    if not 0 <= completed_events <= EVENT_COUNT:
        raise ValueError("completed_events out of range")

    targets = {
        paw: shifted_stance_target_s(
            paw,
            morphology,
            size_dp,
            direction,
            0.0,
            0.0,
            lateral_half_stance_bu,
        )
        for paw in PAWS
    }
    order = event_order(direction)

    for event_index in range(min(completed_events, SHIFT_ONSET_COMPLETED_EVENTS)):
        paw = order[event_index]
        yaw_end = direction * (event_index + 1) * YAW_PER_EVENT
        targets[paw] = shifted_stance_target_s(
            paw,
            morphology,
            size_dp,
            direction,
            yaw_end,
            0.0,
            lateral_half_stance_bu,
        )

    if completed_events >= EVENT_COUNT:
        final_paw = order[-1]
        targets[final_paw] = shifted_stance_target_s(
            final_paw,
            morphology,
            size_dp,
            direction,
            direction * FINAL_YAW_MAGNITUDE,
            1.0,
            lateral_half_stance_bu,
        )

    return targets


def _timeline_state(t: float):
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be [0,1]")

    scaled = t * LOGICAL_PHASE_COUNT
    nearest = round(scaled)
    if abs(scaled - nearest) <= EPS:
        boundary = int(nearest)
        if boundary <= 3:
            return {
                "boundary": True,
                "phase": None,
                "u": None,
                "semantic": "BOUNDARY",
                "completed_events": boundary,
                "event_index": None,
                "root_progress": 0.0,
                "yaw_event_units": float(boundary),
            }
        if boundary == 4:
            return {
                "boundary": True,
                "phase": None,
                "u": None,
                "semantic": "BOUNDARY_POST_SHIFT",
                "completed_events": 3,
                "event_index": None,
                "root_progress": 1.0,
                "yaw_event_units": 3.0,
            }
        if boundary == 5:
            return {
                "boundary": True,
                "phase": None,
                "u": None,
                "semantic": "FINAL_BOUNDARY",
                "completed_events": 4,
                "event_index": None,
                "root_progress": 1.0,
                "yaw_event_units": 4.0,
            }
        raise RuntimeError("unreachable boundary")

    phase = int(scaled)
    local_u = scaled - phase
    eased = _smoothstep(local_u)

    if phase < SHIFT_PHASE_INDEX:
        return {
            "boundary": False,
            "phase": phase,
            "u": local_u,
            "semantic": "PAW_SWING",
            "completed_events": phase,
            "event_index": phase,
            "root_progress": 0.0,
            "yaw_event_units": phase + eased,
        }

    if phase == SHIFT_PHASE_INDEX:
        return {
            "boundary": False,
            "phase": phase,
            "u": local_u,
            "semantic": "ROOT_SHIFT",
            "completed_events": 3,
            "event_index": None,
            "root_progress": eased,
            "yaw_event_units": 3.0,
        }

    if phase == 4:
        return {
            "boundary": False,
            "phase": phase,
            "u": local_u,
            "semantic": "PAW_SWING",
            "completed_events": 3,
            "event_index": 3,
            "root_progress": 1.0,
            "yaw_event_units": 3.0 + eased,
        }

    raise RuntimeError("unreachable phase")


def _shift_structural_anchors(
    morphology: MorphologyV2,
    size_dp: float,
    yaw: float,
    root_progress: float,
):
    anchors = _v1_structural_anchors(morphology, size_dp, yaw)
    dx = root_shift_dp(size_dp, root_progress)
    return {
        name: Vec2(point.x + dx, point.y)
        for name, point in anchors.items()
    }


def solve_h6n_stepped_turn_v2(
    morphology: MorphologyV2,
    size_dp: float,
    t: float,
    direction: int,
    lateral_half_stance_bu: float = LATERAL_HALF_STANCE_BU,
) -> BodyPoseState:
    """Phase-3 H6N 90° semantic fixture with one continuous O3 support shift.

    Root-shift timing/magnitude are accepted C3Q/C3T outputs. Cubic smoothstep is
    used only during the dedicated all-four-contact support phase. This is a
    semantic fixture, not final production animation timing.
    """
    _validate_direction(direction)
    morphology.validate()
    if size_dp <= 0.0:
        raise ValueError("size_dp must be positive")
    if lateral_half_stance_bu <= 0.0:
        raise ValueError("lateral_half_stance_bu must be positive")

    state = _timeline_state(t)
    completed_events = state["completed_events"]
    root_progress = state["root_progress"]
    yaw = direction * state["yaw_event_units"] * YAW_PER_EVENT
    targets = _targets_after_completed_events(
        morphology,
        size_dp,
        direction,
        completed_events,
        lateral_half_stance_bu,
    )
    order = event_order(direction)
    scale = size_dp / 2.0

    if state["boundary"]:
        swing_paw = None
        paw_points = dict(targets)
        phases = {paw: Phase.CONTACT for paw in PAWS}
    elif state["semantic"] == "ROOT_SHIFT":
        swing_paw = None
        paw_points = dict(targets)
        phases = {paw: Phase.CONTACT for paw in PAWS}
    else:
        event_index = state["event_index"]
        local_u = state["u"]
        eased = _smoothstep(local_u)
        swing_paw = order[event_index]
        yaw_end = direction * (event_index + 1) * YAW_PER_EVENT
        end_root_progress = 1.0 if event_index == 3 else 0.0
        start_point = targets[swing_paw]
        end_point = shifted_stance_target_s(
            swing_paw,
            morphology,
            size_dp,
            direction,
            yaw_end,
            end_root_progress,
            lateral_half_stance_bu,
        )
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

    anchors = _shift_structural_anchors(
        morphology,
        size_dp,
        yaw,
        root_progress,
    )
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
    phase_label = "BOUNDARY" if state["phase"] is None else str(state["phase"])
    u_label = "NONE" if state["u"] is None else f"{state['u']:.12f}"
    swing_label = "NONE" if swing_paw is None else swing_paw
    shift_normalized = ROOT_SHIFT_NORMALIZED * root_progress

    return BodyPoseState(
        candidate="H6N_SEMANTIC_V2_ROOT_SHIFT",
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
            f"semanticPhase={state['semantic']}",
            f"phaseIndex={phase_label}",
            f"phaseU={u_label}",
            f"swingPaw={swing_label}",
            f"rootShiftProgress={root_progress:.12f}",
            f"rootShiftNormalized={shift_normalized:.12f}",
            f"rootShiftDp={root_shift_dp(size_dp, root_progress):.12f}",
            "rootShiftMirrorConvention=SAME_SCREEN_TANGENT_UNDER_ANATOMICAL_MIRROR",
        ],
    )
