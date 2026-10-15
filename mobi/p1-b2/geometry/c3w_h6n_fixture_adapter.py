from __future__ import annotations

from c3_semantic import SemanticFixture, semantic_hash, semantic_payload
from h6n_stepped_turn_v2 import CASE_ID, solve_h6n_stepped_turn_v2
from orientation_v2 import M0_V2, M1_V2, M2_V2

H6N_CASE_ID = CASE_ID
MORPHOLOGIES = (M1_V2, M0_V2, M2_V2)
SIZES = (80, 96)
DIRECTIONS = (+1, -1)


def build_h6n_fixture(morphology, size_dp: int, t: float, direction: int) -> SemanticFixture:
    """Adapt the accepted C3U H6N V2 state to the existing C3 renderer fixture shape.

    Direction remains an external matrix dimension. The canonical semantic payload
    is not extended merely to make record IDs unique.
    """
    state = solve_h6n_stepped_turn_v2(
        morphology=morphology,
        size_dp=size_dp,
        t=t,
        direction=direction,
    )
    errors = state.validate()
    if errors:
        raise RuntimeError((morphology.id, size_dp, t, direction, errors))
    if state.case_id != H6N_CASE_ID:
        raise RuntimeError((state.case_id, H6N_CASE_ID))

    payload = semantic_payload(state)
    return SemanticFixture(
        case_id=state.case_id,
        morphology_id=morphology.id,
        size_dp=int(size_dp),
        t=float(t),
        state=state,
        payload=payload,
        semantic_hash=semantic_hash(payload),
    )


def build_h6n_fixture_matrix(sample_count: int = 41):
    if sample_count < 21 or (sample_count - 1) % 5 != 0:
        raise ValueError("sample_count must align all five H6N logical-phase boundaries")

    fixtures = []
    for morphology in MORPHOLOGIES:
        for size_dp in SIZES:
            for direction in DIRECTIONS:
                for index in range(sample_count):
                    t = index / (sample_count - 1)
                    fixtures.append((direction, build_h6n_fixture(morphology, size_dp, t, direction)))
    return fixtures
