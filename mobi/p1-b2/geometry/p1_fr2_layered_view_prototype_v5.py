from __future__ import annotations

from math import cos, sin

from e_v0_profiles import morphology_by_id
from model import Vec2
import p1_fr2_layered_view_prototype_v4_1 as v4_1


PROTOTYPE_VERSION = "P1_FR2_LAYERED_VIEW_PERCEPTUAL_REVISION_V5_FRONT_READ_FINAL"
base = v4_1.v4.base

# Final bounded FR2 refinement. Direct V4.1 visual review left one systemic
# blocker: exact-front remained too narrow, the structural ear bases floated
# above the head envelope, and an unforeshortened tail read as a horizontal bar.
# V5 changes only those view-realization properties. No semantic state,
# topology, morphology branch, corrective family or final-art treatment is added.
FRONT_SHAPE = (
    (0.30, -0.24),
    (0.42, -0.45),
    (0.46, -0.66),
    (0.00, -0.60),
    (-0.30, -0.44),
    (-0.52, -0.24),
    (-0.60, 0.02),
    (-0.58, 0.24),
    (-0.48, 0.46),
    (-0.25, 0.55),
    (0.00, 0.50),
    (0.28, 0.54),
    (0.50, 0.44),
    (0.58, 0.18),
    (0.45, -0.05),
    (0.31, -0.22),
)


def build_ear_shapes(fixture):
    state = fixture.state
    morphology = morphology_by_id(fixture.morphology_id)
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    half = fixture.size_dp / 2.0
    frontness = abs(sin(yaw))
    head = state.anchors["HEAD_ROOT"]

    spread = half * morphology.ear_scale * (0.07 + 0.16 * frontness)
    # Keep the profile construction unchanged, but lower the FRONT ear bases
    # into the head envelope so they read as attached structural triangles.
    base_y = head.y - half * (0.19 - 0.11 * frontness)
    tip_y = head.y - half * (0.43 + 0.06 * frontness) * morphology.ear_scale
    base_half = half * (0.055 + 0.012 * frontness) * morphology.ear_scale

    near_center = head.x - spread
    far_center = head.x + spread * (0.30 + 0.70 * frontness)
    near_tip_x = near_center - half * 0.018 * (1.0 - frontness)
    far_tip_x = far_center + half * 0.018 * (1.0 - frontness)

    near = (
        (near_center - base_half, base_y),
        (near_tip_x, tip_y),
        (near_center + base_half, base_y),
    )
    far = (
        (far_center - base_half, base_y + half * 0.012 * (1.0 - frontness)),
        (far_tip_x, tip_y + half * 0.035 * (1.0 - frontness)),
        (far_center + base_half, base_y + half * 0.012 * (1.0 - frontness)),
    )
    return (near, far)


def _normalized(v: Vec2) -> Vec2:
    length = v.length()
    if length <= 1e-9:
        return Vec2(0.0, -1.0)
    return Vec2(v.x / length, v.y / length)


def _ribbon(centerline, half_width: float):
    vertices = []
    for index, point in enumerate(centerline):
        if index == 0:
            tangent = centerline[1] - centerline[0]
        elif index == len(centerline) - 1:
            tangent = centerline[-1] - centerline[-2]
        else:
            tangent = centerline[index + 1] - centerline[index - 1]
        normal = _normalized(Vec2(-tangent.y, tangent.x))
        left = point + normal * half_width
        right = point - normal * half_width
        vertices.extend(((left.x, left.y), (right.x, right.y)))
    return tuple(vertices)


def _view_depth(x_forward: float, z_left: float, yaw: float) -> float:
    return x_forward * sin(yaw) - z_left * cos(yaw)


def build_tail_mesh(fixture):
    state = fixture.state
    morphology = morphology_by_id(fixture.morphology_id)
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    half = fixture.size_dp / 2.0
    root = state.anchors["TAIL_ROOT"]
    direction = -1.0 if cos(yaw) >= 0.0 else 1.0
    frontness = abs(sin(yaw))
    length = half * 1.05 * morphology.tail_length
    # A lateral tail axis is strongly foreshortened as the body turns to front.
    # This is view realization only; TAIL_ROOT and semantic orientation are unchanged.
    lateral = 0.24 + 0.76 * (1.0 - frontness)
    p1 = Vec2(root.x + direction * length * 0.30 * lateral,
              root.y - half * (0.03 + 0.04 * frontness))
    p2 = Vec2(root.x + direction * length * 0.64 * lateral,
              root.y - half * (0.18 + 0.04 * frontness))
    p3 = Vec2(root.x + direction * length * lateral,
              root.y - half * (0.30 + 0.04 * frontness))
    centerline = (root, p1, p2, p3)
    ribbon = _ribbon(centerline, half * 0.036 * morphology.tail_thickness)
    return {
        "id": "TAIL_MESH",
        "vertices": ribbon,
        "centerline": tuple((p.x, p.y) for p in centerline),
        "triangles": base.fr1.APPENDAGE_TRIANGLES,
        "viewDepth": _view_depth(-0.55 * morphology.trunk_length, 0.08, yaw),
    }


base.PROTOTYPE_VERSION = PROTOTYPE_VERSION
base.FRONT_SHAPE = FRONT_SHAPE
base.CANONICAL_SHAPES = dict(base.CANONICAL_SHAPES)
base.CANONICAL_SHAPES["FRONT"] = FRONT_SHAPE
base.build_ear_shapes = build_ear_shapes
base.build_tail_mesh = build_tail_mesh

CORE_VERTEX_IDS = base.CORE_VERTEX_IDS
CANONICAL_SHAPES = base.CANONICAL_SHAPES
FR2ProbeResult = base.FR2ProbeResult
canonical_view_weights = base.canonical_view_weights
build_core_vertices = base.build_core_vertices
build_limb_meshes = base.build_limb_meshes
topology_signature = base.topology_signature
limb_crossing_count = base.limb_crossing_count
build_probe = base.build_probe
result_dict = base.result_dict
