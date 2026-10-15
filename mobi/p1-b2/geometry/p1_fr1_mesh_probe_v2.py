from __future__ import annotations

from typing import Dict, Tuple

import p1_fr1_mesh_probe as v1
from model import Vec2


PROBE_VERSION = "P1_FR1_LAYERED_VIEW_MESH_FEASIBILITY_V2_SMOOTH_SKINNING"

# V1 assigned each contour vertex to exactly one semantic region. The first
# executable probe falsified that approach: hard region boundaries can fold the
# single visible contour even while semantics remain correct. V2 uses ordinary
# smooth skin weights so neighboring vertices share adjacent anchors.
CORE_SKIN_WEIGHTS = {
    "V00_NOSE_TOP": {"HEAD": 1.00},
    "V01_FOREHEAD": {"HEAD": 1.00},
    "V02_EAR_CROWN_A": {"HEAD": 1.00},
    "V03_CROWN": {"HEAD": 0.92, "FORE": 0.08},
    "V04_NECK_DORSAL": {"HEAD": 0.38, "FORE": 0.62},
    "V05_SHOULDER_DORSAL": {"FORE": 0.82, "BODY": 0.18},
    "V06_BACK_DORSAL": {"FORE": 0.18, "BODY": 0.60, "PELVIS": 0.22},
    "V07_HAUNCH_DORSAL": {"BODY": 0.18, "PELVIS": 0.82},
    "V08_RUMP": {"PELVIS": 1.00},
    "V09_HAUNCH_VENTRAL": {"BODY": 0.08, "PELVIS": 0.92},
    "V10_BELLY_REAR": {"BODY": 0.42, "PELVIS": 0.58},
    "V11_BELLY_FRONT": {"FORE": 0.18, "BODY": 0.70, "PELVIS": 0.12},
    "V12_CHEST": {"FORE": 0.84, "BODY": 0.16},
    "V13_THROAT": {"HEAD": 0.24, "FORE": 0.76},
    "V14_MUZZLE_BOTTOM": {"HEAD": 0.96, "FORE": 0.04},
    "V15_NOSE_BOTTOM": {"HEAD": 1.00},
}

CANONICAL_ANCHOR_REFS = {
    "PROFILE": {
        "HEAD": (1.03, -0.18),
        "FORE": (0.28, -0.04),
        "BODY": (-0.24, 0.03),
        "PELVIS": (-0.78, 0.03),
    },
    "THREE_QUARTER": {
        "HEAD": (0.61, -0.20),
        "FORE": (0.13, -0.03),
        "BODY": (-0.23, 0.10),
        "PELVIS": (-0.58, 0.13),
    },
    "FRONT": {
        "HEAD": (0.00, -0.36),
        "FORE": (0.00, -0.06),
        "BODY": (0.00, 0.15),
        "PELVIS": (0.00, 0.25),
    },
}


def _weighted_actual_anchor(state, skin: Dict[str, float]) -> Vec2:
    mapping = {
        "HEAD": state.anchors["HEAD_ROOT"],
        "FORE": state.anchors["FOREQUARTER_REF"],
        "BODY": state.anchors["BODY_ROOT"],
        "PELVIS": state.anchors["PELVIS_REF"],
    }
    x = sum(mapping[name].x * weight for name, weight in skin.items())
    y = sum(mapping[name].y * weight for name, weight in skin.items())
    return Vec2(x, y)


def _blended_reference_anchor(view_weights: Dict[str, float], skin: Dict[str, float]) -> Tuple[float, float]:
    x = 0.0
    y = 0.0
    for view_name, view_weight in view_weights.items():
        refs = CANONICAL_ANCHOR_REFS[view_name]
        x += view_weight * sum(refs[name][0] * weight for name, weight in skin.items())
        y += view_weight * sum(refs[name][1] * weight for name, weight in skin.items())
    return x, y


def build_core_vertices(fixture):
    state = fixture.state
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    view_weights = v1.canonical_view_weights(yaw)
    shape = v1._shape_blend(view_weights)
    sx, sy = v1._screen_scale(fixture, view_weights)
    mirror = 1.0 if yaw >= 0.0 else -1.0

    vertices = []
    for vertex_id, (shape_x, shape_y) in zip(v1.CORE_VERTEX_IDS, shape):
        skin = CORE_SKIN_WEIGHTS[vertex_id]
        if abs(sum(skin.values()) - 1.0) > 1e-12:
            raise RuntimeError((vertex_id, skin))
        actual = _weighted_actual_anchor(state, skin)
        ref_x, ref_y = _blended_reference_anchor(view_weights, skin)
        local_x = (shape_x - ref_x) * sx * mirror
        local_y = (shape_y - ref_y) * sy
        vertices.append((vertex_id, actual.x + local_x, actual.y + local_y))
    return tuple(vertices)


def build_probe(fixture, direction: int = +1):
    state = fixture.state
    before_hash = v1._hash_json(v1._anchor_payload(state))
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    core = build_core_vertices(fixture)
    limbs = v1.build_limb_meshes(fixture)
    tail = v1.build_tail_mesh(fixture)
    after_hash = v1._hash_json(v1._anchor_payload(state))

    return v1.MeshProbeResult(
        semantic_hash=fixture.semantic_hash,
        morphology_id=fixture.morphology_id,
        case_id=fixture.case_id,
        size_dp=int(fixture.size_dp),
        t=float(fixture.t),
        direction=int(direction),
        yaw_rad=yaw,
        view_weights=tuple(sorted(v1.canonical_view_weights(yaw).items())),
        core_vertices=core,
        limb_meshes=limbs,
        tail_mesh=tail,
        topology_signature=v1.topology_signature(),
        semantic_anchor_hash_before=before_hash,
        semantic_anchor_hash_after=after_hash,
        paw_pin_error_max=max(mesh["pawPinError"] for mesh in limbs),
        core_self_intersections=v1.count_self_intersections(core),
        correction_families=tuple(),
    )


def result_dict(result):
    payload = v1.result_dict(result)
    payload["version"] = PROBE_VERSION
    return payload


# Re-export stable topology/view helpers used by tests and runner.
CORE_VERTEX_IDS = v1.CORE_VERTEX_IDS
canonical_view_weights = v1.canonical_view_weights
topology_signature = v1.topology_signature
