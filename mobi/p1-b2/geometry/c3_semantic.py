from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from model import M0, M1, M2
from motions_v2 import sample_motion
from orientation_v2 import M0_V2, M1_V2, M2_V2
from turn_2p5d import solve_turn_2p5d

BODY_CANDIDATES = ("BM_A", "BM_B", "BM_C")
MORPHOLOGIES = (M1, M0, M2)
SIZES = (80, 96)
CASES = (
    "H4_SIT_TO_STAND",
    "H6_CHANGE_FACING_2P5D",
    "H7_NARROW_SHORT_STEP",
)

ORIENTATION_MORPH = {
    M0.id: M0_V2,
    M1.id: M1_V2,
    M2.id: M2_V2,
}


@dataclass(frozen=True)
class SemanticFixture:
    case_id: str
    morphology_id: str
    size_dp: int
    t: float
    state: object
    payload: dict
    semantic_hash: str


def _point_payload(point):
    if point is None:
        return None
    return [point.x, point.y]


def _orientation_payload(state):
    yaw = 0.0
    view = "PROFILE_POS"
    for note in state.notes:
        if note.startswith("bodyYawRad="):
            yaw = float(note.split("=", 1)[1])
        elif note.startswith("view="):
            view = note.split("=", 1)[1]
    return {"yawRad": yaw, "view": view}


def semantic_payload(state):
    contacts = []
    for contact in sorted(state.contacts, key=lambda item: item.id):
        contacts.append({
            "id": contact.id,
            "kind": contact.kind.value,
            "owner": contact.owner,
            "phase": contact.phase.value,
            "loadBearing": contact.load_bearing,
            "point": _point_payload(contact.point),
            "targetPoint": _point_payload(contact.target_point),
            "tangentExtentDp": contact.tangent_extent_dp,
            "supportGeometryId": contact.support_geometry_id,
        })
    return {
        "caseId": state.case_id,
        "morphologyId": state.morphology_id,
        "sizeDp": state.size_dp,
        "t": state.t,
        "anchors": {
            name: _point_payload(state.anchors[name])
            for name in sorted(state.anchors)
        },
        "contacts": contacts,
        "supportSet": sorted(state.support_set),
        "orientation": _orientation_payload(state),
    }


def canonical_bytes(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def semantic_hash(payload):
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def _state_for(candidate, morphology, case_id, size_dp, t):
    if case_id == "H6_CHANGE_FACING_2P5D":
        return solve_turn_2p5d(
            candidate,
            ORIENTATION_MORPH[morphology.id],
            size_dp,
            t,
        )
    return sample_motion(candidate, morphology, case_id, size_dp, t)


def build_common_fixture(morphology, case_id, size_dp, t):
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


def build_fixture_matrix(sample_count=17):
    if sample_count < 5:
        raise ValueError("sample_count must be >= 5")
    fixtures = []
    for case_id in CASES:
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for index in range(sample_count):
                    t = index / (sample_count - 1)
                    fixtures.append(build_common_fixture(morphology, case_id, size_dp, t))
    return fixtures


def morphology_by_id(morphology_id):
    for morphology in MORPHOLOGIES:
        if morphology.id == morphology_id:
            return morphology
    raise KeyError(morphology_id)


def orientation_morphology_by_id(morphology_id):
    return ORIENTATION_MORPH[morphology_id]
