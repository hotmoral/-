from __future__ import annotations

from c3_semantic import SemanticFixture, canonical_bytes, semantic_hash, semantic_payload
from c3w_h6n_fixture_adapter import build_h6n_fixture
from candidates_v2 import solve_pose
from e_v0_profiles import MORPHOLOGIES, orientation_by_id
from motions_v2 import sample_motion

ADAPTER_VERSION = "P1_E_V0_FIXTURE_ADAPTER_V1"
BODY_CANDIDATES = ("BM_A", "BM_B", "BM_C")
SIZES = (64, 80, 96)
DIRECTIONS = (+1, -1)

H1 = "H1_NEUTRAL_SUPPORT"
H4 = "H4_SIT_TO_STAND"
H5 = "H5_CROUCH"
H6N = "H6N_STEPPED_QUARTER_TURN_V2_ROOT_SHIFT"
H7 = "H7_NARROW_SHORT_STEP"
CASES = (H1, H4, H5, H6N, H7)
STATIC_CASES = (H1, H5)
MOTION_CASES = (H4, H7)


def invariant_times(case_id: str):
    if case_id in STATIC_CASES:
        return (0.0,)
    if case_id == H6N:
        return tuple(index / 40.0 for index in range(41))
    if case_id in MOTION_CASES:
        return tuple(index / 16.0 for index in range(17))
    raise KeyError(case_id)


def scorecard_times(case_id: str):
    if case_id in STATIC_CASES:
        return (0.0,)
    if case_id == H6N:
        return (0.0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0)
    if case_id in MOTION_CASES:
        return (0.0, 0.25, 0.5, 0.75, 1.0)
    raise KeyError(case_id)


def directions_for_case(case_id: str):
    return DIRECTIONS if case_id == H6N else (+1,)


def _state_for(candidate: str, morphology, case_id: str, size_dp: int, t: float):
    if case_id in STATIC_CASES:
        return solve_pose(candidate, morphology, case_id, size_dp, t)
    if case_id in MOTION_CASES:
        return sample_motion(candidate, morphology, case_id, size_dp, t)
    raise KeyError(case_id)


def _common_non_h6n_fixture(morphology, case_id: str, size_dp: int, t: float) -> SemanticFixture:
    states = [
        _state_for(candidate, morphology, case_id, size_dp, t)
        for candidate in BODY_CANDIDATES
    ]
    for state in states:
        errors = state.validate()
        if errors:
            raise RuntimeError((case_id, morphology.id, size_dp, t, state.candidate, errors))

    payloads = [semantic_payload(state) for state in states]
    reference = canonical_bytes(payloads[0])
    for candidate, payload in zip(BODY_CANDIDATES[1:], payloads[1:]):
        if canonical_bytes(payload) != reference:
            raise RuntimeError(
                f"body-candidate semantic divergence: case={case_id} morph={morphology.id} "
                f"size={size_dp} t={t} candidate={candidate}"
            )

    payload = payloads[0]
    return SemanticFixture(
        case_id=case_id,
        morphology_id=morphology.id,
        size_dp=int(size_dp),
        t=float(t),
        state=states[0],
        payload=payload,
        semantic_hash=semantic_hash(payload),
    )


def build_e_fixture(morphology, case_id: str, size_dp: int, t: float, direction: int = +1) -> SemanticFixture:
    if case_id not in CASES:
        raise KeyError(case_id)
    if size_dp not in SIZES:
        raise ValueError(size_dp)
    if morphology not in MORPHOLOGIES:
        raise ValueError(morphology.id)

    if case_id == H6N:
        if direction not in DIRECTIONS:
            raise ValueError(direction)
        return build_h6n_fixture(orientation_by_id(morphology.id), size_dp, t, direction)

    if direction != +1:
        raise ValueError("non-H6N P1-E fixtures use canonical profile direction only")
    return _common_non_h6n_fixture(morphology, case_id, size_dp, t)


def iter_invariant_fixtures():
    for case_id in CASES:
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in directions_for_case(case_id):
                    for t in invariant_times(case_id):
                        yield case_id, morphology, size_dp, direction, build_e_fixture(
                            morphology, case_id, size_dp, t, direction
                        )


def iter_scorecard_fixtures():
    for morphology in MORPHOLOGIES:
        for size_dp in SIZES:
            for case_id in CASES:
                direction = +1
                for t in scorecard_times(case_id):
                    yield case_id, morphology, size_dp, direction, build_e_fixture(
                        morphology, case_id, size_dp, t, direction
                    )
