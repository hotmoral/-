from __future__ import annotations

from math import cos, pi, sin

from model import Phase, Vec2
from candidates_v2 import PAWS, base_paw_offsets, solve_pose

OFFSETS = {
    "HIND_PAW_L": 0.0,
    "FORE_PAW_R": 0.25,
    "HIND_PAW_R": 0.50,
    "FORE_PAW_L": 0.75,
}


def gait_paws(morphology, size_dp, q, narrow=False, stride_factor=.68, duty=.68):
    scale = size_dp / 2.0
    root0 = size_dp * 1.45
    step = stride_factor * scale
    root_x = root0 + step * q
    offsets = base_paw_offsets(scale, morphology, narrow=narrow)
    paws = {}
    phases = {}
    for paw_name, phase0 in OFFSETS.items():
        u = (q + phase0) % 1.0
        if u < duty:
            relative_x = offsets[paw_name] + step * duty / 2.0 - step * u
            lift = 0.0
            phases[paw_name] = Phase.CONTACT
        else:
            z = (u - duty) / (1.0 - duty)
            relative_x = offsets[paw_name] - step * duty / 2.0 + step * duty * z
            lift = sin(pi * z) * .25 * scale
            phases[paw_name] = Phase.SWING
        paws[paw_name] = Vec2(root_x + relative_x, size_dp * 1.38 - lift)
    return root_x - root0, paws, phases


def smoothstep(value):
    return value * value * (3.0 - 2.0 * value)


def sample_motion(candidate, morphology, case_id, size_dp, t):
    if not 0.0 <= t <= 1.0:
        raise ValueError("t must be [0,1]")

    if case_id == "H2_SLOW_WALK":
        dx, paws, phases = gait_paws(morphology, size_dp, t)
        return solve_pose(candidate, morphology, case_id, size_dp, t, dx, paws, phases)

    if case_id == "H3_START_WALK_STOP":
        if t < .15:
            q = 0.0
        elif t > .85:
            q = 1.0
        else:
            q = smoothstep((t - .15) / .70)
        dx, paws, phases = gait_paws(morphology, size_dp, q)
        if q in (0.0, 1.0):
            phases = {paw_name: Phase.CONTACT for paw_name in PAWS}
        return solve_pose(candidate, morphology, case_id, size_dp, t, dx, paws, phases)

    if case_id == "H4_SIT_TO_STAND":
        mix = smoothstep(t)
        scale = size_dp / 2.0
        root_x = size_dp * 1.45
        offsets = base_paw_offsets(scale, morphology, sit=True)
        paws = {paw_name: Vec2(root_x + offset, size_dp * 1.38) for paw_name, offset in offsets.items()}
        phases = {paw_name: Phase.CONTACT for paw_name in PAWS}
        return solve_pose(candidate, morphology, case_id, size_dp, t, 0.0, paws, phases, pose_mix=mix)

    if case_id == "H6_CHANGE_FACING":
        yaw = cos(pi * t)
        scale = size_dp / 2.0
        root_x = size_dp * 1.45
        ground_y = size_dp * 1.38
        neutral = base_paw_offsets(scale, morphology)
        paws = {}
        phases = {}
        pivot_paws = ("FORE_PAW_L", "HIND_PAW_L")
        for paw_name, offset in neutral.items():
            if paw_name in pivot_paws:
                paws[paw_name] = Vec2(root_x + offset, ground_y)
                phases[paw_name] = Phase.CONTACT
            else:
                start_x = root_x + offset
                end_x = root_x - offset
                paws[paw_name] = Vec2(
                    start_x * (1.0 - t) + end_x * t,
                    ground_y - sin(pi * t) * .18 * scale,
                )
                phases[paw_name] = Phase.SWING if 0.0 < t < 1.0 else Phase.CONTACT
        return solve_pose(
            candidate,
            morphology,
            case_id,
            size_dp,
            t,
            0.0,
            paws,
            phases,
            yaw_cos=yaw,
        )

    if case_id == "H7_NARROW_SHORT_STEP":
        dx, paws, phases = gait_paws(
            morphology,
            size_dp,
            t,
            narrow=True,
            stride_factor=.30,
            duty=.74,
        )
        return solve_pose(candidate, morphology, case_id, size_dp, t, dx, paws, phases)

    raise ValueError(case_id)
