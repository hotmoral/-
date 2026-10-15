from __future__ import annotations

from math import cos, sin

from e_v0_profiles import morphology_by_id, orientation_by_id
from model import Vec2
import p1_fr2_layered_view_prototype_v3 as v3


PROTOTYPE_VERSION = "P1_FR2_LAYERED_VIEW_PERCEPTUAL_REVISION_V4_VISUAL_REFINEMENT"
base = v3.v2.v1

# Direct V3 perceptual evidence showed four bounded issues:
# 1) profile muzzle reads as an overlong wedge;
# 2) 3Q/front head-neck-chest separation is weak;
# 3) tail is too short/stiff for strong feline identity;
# 4) narrow-support hind routing can form a mechanical loop.
# V4 changes only those base visible-shape/routing properties.

PROFILE_SHAPE = list(v3.PROFILE_SHAPE)
PROFILE_SHAPE[0] = (1.08, -0.15)
PROFILE_SHAPE[1] = (0.96, -0.40)
PROFILE_SHAPE[2] = (0.82, -0.66)
PROFILE_SHAPE[14] = (0.90, 0.08)
PROFILE_SHAPE[15] = (1.14, -0.02)
PROFILE_SHAPE = tuple(PROFILE_SHAPE)

THREE_QUARTER_SHAPE = (
    (0.74, -0.18),
    (0.64, -0.41),
    (0.47, -0.68),
    (0.22, -0.55),
    (0.03, -0.31),   # dorsal neck inset
    (-0.27, -0.43),  # shoulder recovery
    (-0.51, -0.42),
    (-0.69, -0.38),
    (-0.78, -0.05),
    (-0.65, 0.35),
    (-0.36, 0.39),
    (-0.02, 0.28),
    (0.31, 0.35),
    (0.40, 0.02),    # throat inset
    (0.62, 0.02),
    (0.75, -0.08),
)

FRONT_SHAPE = (
    (0.25, -0.22),
    (0.35, -0.43),
    (0.38, -0.66),
    (0.00, -0.58),
    (-0.20, -0.31),  # neck inset
    (-0.48, -0.14),  # left shoulder/chest expansion
    (-0.50, 0.05),
    (-0.46, 0.23),
    (-0.34, 0.42),
    (-0.17, 0.49),
    (0.00, 0.46),
    (0.28, 0.42),
    (0.48, 0.14),    # right chest expansion
    (0.20, -0.30),   # throat/neck inset
    (0.34, -0.08),
    (0.27, -0.18),
)


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


def _feline_limb_centerline(root: Vec2, paw: Vec2, yaw: float, kind: str, size_dp: int):
    delta = paw - root
    half = size_dp / 2.0
    frontness = abs(sin(yaw))
    profile = 1.0 - frontness

    if kind == "FORE":
        p1 = Vec2(root.x + delta.x * 0.32 - profile * half * 0.040,
                  root.y + delta.y * 0.31)
        p2 = Vec2(root.x + delta.x * 0.73 + profile * half * 0.015,
                  root.y + delta.y * 0.74)
    else:
        # Generic geometry-aware bend economy: when the paw sits almost under
        # the hip (the direct V3 H7 failure), reduce the profile zig-zag rather
        # than forcing a fixed knee/hock excursion that loops back on itself.
        horizontal = abs(delta.x) / max(half, 1e-9)
        bend = min(1.0, 0.25 + 1.8 * horizontal)
        p1 = Vec2(root.x + delta.x * 0.30 + profile * half * 0.085 * bend,
                  root.y + delta.y * 0.29)
        p2 = Vec2(root.x + delta.x * 0.68 - profile * half * 0.060 * bend,
                  root.y + delta.y * 0.68)
    return (root, p1, p2, paw)


def _view_depth(x_forward: float, z_left: float, yaw: float) -> float:
    return x_forward * sin(yaw) - z_left * cos(yaw)


def build_limb_meshes(fixture):
    state = fixture.state
    morphology = morphology_by_id(fixture.morphology_id)
    orientation = orientation_by_id(fixture.morphology_id)
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    half = fixture.size_dp / 2.0
    frontness = abs(sin(yaw))
    meshes = []
    specs = (
        ("FORE_PAW_L", "FORE", +1.0),
        ("FORE_PAW_R", "FORE", -1.0),
        ("HIND_PAW_L", "HIND", +1.0),
        ("HIND_PAW_R", "HIND", -1.0),
    )
    for paw_id, kind, side_sign in specs:
        paw = state.anchors[paw_id]
        if kind == "FORE":
            anchor = state.anchors["FOREQUARTER_REF"]
            root_follow = 0.18 + 0.16 * frontness
            root = Vec2(anchor.x + (paw.x - anchor.x) * root_follow,
                        anchor.y + half * 0.015)
            limb_scale = morphology.fore_limb_length
            x_forward = +0.47 * morphology.trunk_length
            z_left = side_sign * 0.18 * orientation.thorax_width_scale
            width = half * 0.050 * limb_scale
        else:
            anchor = state.anchors["PELVIS_REF"]
            root_follow = 0.16 + 0.17 * frontness
            root = Vec2(anchor.x + (paw.x - anchor.x) * root_follow,
                        anchor.y + half * 0.030)
            limb_scale = morphology.hind_limb_length
            x_forward = -0.47 * morphology.trunk_length
            z_left = side_sign * 0.20 * orientation.pelvis_width_scale
            width = half * 0.058 * limb_scale
        centerline = _feline_limb_centerline(root, paw, yaw, kind, fixture.size_dp)
        ribbon = _ribbon(centerline, width)
        end_center = Vec2(
            (ribbon[-2][0] + ribbon[-1][0]) / 2.0,
            (ribbon[-2][1] + ribbon[-1][1]) / 2.0,
        )
        meshes.append({
            "id": paw_id.replace("_PAW", "_LIMB_MESH"),
            "kind": kind,
            "side": "L" if side_sign > 0 else "R",
            "vertices": ribbon,
            "centerline": tuple((p.x, p.y) for p in centerline),
            "triangles": base.fr1.APPENDAGE_TRIANGLES,
            "pawId": paw_id,
            "pawPinError": (end_center - paw).length(),
            "pawRadiusX": half * 0.060 * morphology.paw_scale,
            "pawRadiusY": half * 0.038 * morphology.paw_scale,
            "viewDepth": _view_depth(x_forward, z_left, yaw),
        })
    return tuple(meshes)


def build_tail_mesh(fixture):
    state = fixture.state
    morphology = morphology_by_id(fixture.morphology_id)
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    half = fixture.size_dp / 2.0
    root = state.anchors["TAIL_ROOT"]
    direction = -1.0 if cos(yaw) >= 0.0 else 1.0
    length = half * 1.05 * morphology.tail_length
    frontness = abs(sin(yaw))
    p1 = Vec2(root.x + direction * length * 0.30,
              root.y - half * (0.03 + 0.03 * frontness))
    p2 = Vec2(root.x + direction * length * 0.64,
              root.y - half * (0.18 + 0.02 * frontness))
    p3 = Vec2(root.x + direction * length,
              root.y - half * (0.30 - 0.08 * frontness))
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
base.PROFILE_SHAPE = PROFILE_SHAPE
base.THREE_QUARTER_SHAPE = THREE_QUARTER_SHAPE
base.FRONT_SHAPE = FRONT_SHAPE
base.CANONICAL_SHAPES = {
    "PROFILE": PROFILE_SHAPE,
    "THREE_QUARTER": THREE_QUARTER_SHAPE,
    "FRONT": FRONT_SHAPE,
}
base.build_limb_meshes = build_limb_meshes
base.build_tail_mesh = build_tail_mesh

CORE_VERTEX_IDS = base.CORE_VERTEX_IDS
CANONICAL_SHAPES = base.CANONICAL_SHAPES
FR2ProbeResult = base.FR2ProbeResult
canonical_view_weights = base.canonical_view_weights
build_core_vertices = base.build_core_vertices
build_ear_shapes = base.build_ear_shapes
topology_signature = base.topology_signature
limb_crossing_count = base.limb_crossing_count
build_probe = base.build_probe
result_dict = base.result_dict
