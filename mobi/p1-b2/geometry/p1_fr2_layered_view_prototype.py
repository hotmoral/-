from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from math import cos, pi, sin
from typing import Dict, List, Sequence, Tuple

from e_v0_profiles import morphology_by_id, orientation_by_id
from model import Vec2
import p1_fr1_mesh_probe as fr1
import p1_fr1_mesh_probe_v2 as fr1_v2


PROTOTYPE_VERSION = "P1_FR2_LAYERED_VIEW_PERCEPTUAL_REVISION_V1"

# FR2 deliberately keeps the FR1 16-vertex CORE correspondence. The revision is
# authored shape quality + base limb routing, not topology proliferation.
CORE_VERTEX_IDS = fr1.CORE_VERTEX_IDS

# Naturalistic structural silhouette bases. These remain neutral engineering
# shapes: no coat, face, eyes, whiskers, fur or pencil texture. The profile
# emphasizes a feline shoulder/back/haunch line and abdominal tuck; 3Q/front
# preserve a separate head-over-chest read instead of compressing into one blob.
PROFILE_SHAPE = (
    (1.18, -0.16),  # nose top
    (1.04, -0.43),  # forehead
    (0.86, -0.68),  # near ear/crown rise
    (0.66, -0.50),  # crown
    (0.46, -0.32),  # neck dorsal
    (0.20, -0.43),  # shoulder dorsal
    (-0.26, -0.47), # back dorsal
    (-0.70, -0.55), # haunch dorsal
    (-0.98, -0.26), # rump
    (-0.88, 0.30),  # haunch ventral
    (-0.52, 0.28),  # belly rear
    (-0.12, 0.16),  # abdominal tuck
    (0.20, 0.31),   # chest
    (0.42, 0.06),   # throat
    (0.84, 0.04),   # muzzle bottom
    (1.15, -0.04),  # nose bottom
)

THREE_QUARTER_SHAPE = (
    (0.82, -0.19),
    (0.68, -0.43),
    (0.48, -0.70),
    (0.22, -0.55),
    (0.00, -0.38),
    (-0.24, -0.43),
    (-0.50, -0.42),
    (-0.68, -0.38),
    (-0.77, -0.06),
    (-0.65, 0.35),
    (-0.36, 0.39),
    (-0.02, 0.28),
    (0.32, 0.36),
    (0.49, 0.08),
    (0.70, 0.03),
    (0.84, -0.08),
)

FRONT_SHAPE = (
    (0.24, -0.25),
    (0.34, -0.47),
    (0.38, -0.68),
    (0.00, -0.57),
    (-0.27, -0.43),
    (-0.42, -0.25),
    (-0.47, -0.02),
    (-0.44, 0.18),
    (-0.36, 0.39),
    (-0.20, 0.48),
    (0.00, 0.43),
    (0.20, 0.48),
    (0.36, 0.39),
    (0.44, 0.08),
    (0.34, -0.08),
    (0.26, -0.18),
)

CANONICAL_SHAPES = {
    "PROFILE": PROFILE_SHAPE,
    "THREE_QUARTER": THREE_QUARTER_SHAPE,
    "FRONT": FRONT_SHAPE,
}


@dataclass(frozen=True)
class FR2ProbeResult:
    semantic_hash: str
    morphology_id: str
    case_id: str
    size_dp: int
    t: float
    direction: int
    yaw_rad: float
    view_weights: Tuple[Tuple[str, float], ...]
    core_vertices: Tuple[Tuple[str, float, float], ...]
    ear_shapes: Tuple[Tuple[Tuple[float, float], ...], ...]
    limb_meshes: Tuple[dict, ...]
    tail_mesh: dict
    topology_signature: str
    semantic_anchor_hash_before: str
    semantic_anchor_hash_after: str
    paw_pin_error_max: float
    core_self_intersections: int
    correction_families: Tuple[str, ...]


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _hash_json(value) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def canonical_view_weights(yaw_rad: float) -> Dict[str, float]:
    return fr1.canonical_view_weights(yaw_rad)


def _shape_blend(weights: Dict[str, float]) -> List[Tuple[float, float]]:
    points = []
    for index in range(len(CORE_VERTEX_IDS)):
        x = sum(CANONICAL_SHAPES[name][index][0] * weight for name, weight in weights.items())
        y = sum(CANONICAL_SHAPES[name][index][1] * weight for name, weight in weights.items())
        points.append((x, y))
    return points


def build_core_vertices(fixture) -> Tuple[Tuple[str, float, float], ...]:
    state = fixture.state
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    view_weights = canonical_view_weights(yaw)
    shape = _shape_blend(view_weights)
    sx, sy = fr1._screen_scale(fixture, view_weights)

    vertices = []
    for vertex_id, (shape_x, shape_y) in zip(CORE_VERTEX_IDS, shape):
        skin = fr1_v2.CORE_SKIN_WEIGHTS[vertex_id]
        actual = fr1_v2._weighted_actual_anchor(state, skin)
        ref_x, ref_y = fr1_v2._blended_reference_anchor(view_weights, skin)
        local_x = (shape_x - ref_x) * sx
        local_y = (shape_y - ref_y) * sy
        vertices.append((vertex_id, actual.x + local_x, actual.y + local_y))
    return tuple(vertices)


def build_ear_shapes(fixture) -> Tuple[Tuple[Tuple[float, float], ...], ...]:
    """Neutral structural ear pair attached to CORE; not a new mesh domain."""
    state = fixture.state
    morphology = morphology_by_id(fixture.morphology_id)
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    half = fixture.size_dp / 2.0
    frontness = abs(sin(yaw))
    head = state.anchors["HEAD_ROOT"]

    spread = half * morphology.ear_scale * (0.07 + 0.16 * frontness)
    base_y = head.y - half * (0.19 + 0.04 * frontness)
    tip_y = head.y - half * (0.43 + 0.06 * frontness) * morphology.ear_scale
    base_half = half * (0.055 + 0.012 * frontness) * morphology.ear_scale

    # Profile keeps the far ear slightly behind the near one; front separates
    # both symmetrically. This is still renderer-local structural silhouette.
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


def _ribbon(centerline: Sequence[Vec2], half_width: float) -> Tuple[Tuple[float, float], ...]:
    vertices: List[Tuple[float, float]] = []
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


def _feline_limb_centerline(root: Vec2, paw: Vec2, yaw: float, kind: str, size_dp: int) -> Tuple[Vec2, ...]:
    delta = paw - root
    half = size_dp / 2.0
    frontness = abs(sin(yaw))
    profile = 1.0 - frontness

    if kind == "FORE":
        # Mild rearward elbow / near-vertical distal segment in profile. The
        # bend fades toward front so left/right lanes do not create an X.
        p1 = Vec2(root.x + delta.x * 0.32 - profile * half * 0.045,
                  root.y + delta.y * 0.31)
        p2 = Vec2(root.x + delta.x * 0.73 + profile * half * 0.018,
                  root.y + delta.y * 0.74)
    else:
        # Feline hind leg: forward knee then rearward hock in profile. Again the
        # zig-zag collapses toward front to preserve readable side lanes.
        p1 = Vec2(root.x + delta.x * 0.30 + profile * half * 0.090,
                  root.y + delta.y * 0.29)
        p2 = Vec2(root.x + delta.x * 0.68 - profile * half * 0.070,
                  root.y + delta.y * 0.68)
    return (root, p1, p2, paw)


def _view_depth(x_forward: float, z_left: float, yaw: float) -> float:
    return x_forward * sin(yaw) - z_left * cos(yaw)


def build_limb_meshes(fixture) -> Tuple[dict, ...]:
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
            base = state.anchors["FOREQUARTER_REF"]
            root_follow = 0.18 + 0.16 * frontness
            root = Vec2(base.x + (paw.x - base.x) * root_follow,
                        base.y + half * 0.015)
            limb_scale = morphology.fore_limb_length
            x_forward = +0.47 * morphology.trunk_length
            z_left = side_sign * 0.18 * orientation.thorax_width_scale
            width = half * 0.050 * limb_scale
        else:
            base = state.anchors["PELVIS_REF"]
            root_follow = 0.16 + 0.17 * frontness
            root = Vec2(base.x + (paw.x - base.x) * root_follow,
                        base.y + half * 0.030)
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
        pin_error = (end_center - paw).length()
        meshes.append({
            "id": paw_id.replace("_PAW", "_LIMB_MESH"),
            "kind": kind,
            "side": "L" if side_sign > 0 else "R",
            "vertices": ribbon,
            "centerline": tuple((p.x, p.y) for p in centerline),
            "triangles": fr1.APPENDAGE_TRIANGLES,
            "pawId": paw_id,
            "pawPinError": pin_error,
            "pawRadiusX": half * 0.060 * morphology.paw_scale,
            "pawRadiusY": half * 0.038 * morphology.paw_scale,
            "viewDepth": _view_depth(x_forward, z_left, yaw),
        })
    return tuple(meshes)


def build_tail_mesh(fixture) -> dict:
    state = fixture.state
    morphology = morphology_by_id(fixture.morphology_id)
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    half = fixture.size_dp / 2.0
    root = state.anchors["TAIL_ROOT"]
    direction = -1.0 if cos(yaw) >= 0.0 else 1.0
    length = half * 0.62 * morphology.tail_length
    frontness = abs(sin(yaw))
    p1 = Vec2(root.x + direction * length * 0.32, root.y - half * (0.07 + 0.03 * frontness))
    p2 = Vec2(root.x + direction * length * 0.68, root.y - half * (0.24 + 0.02 * frontness))
    p3 = Vec2(root.x + direction * length, root.y - half * 0.15)
    centerline = (root, p1, p2, p3)
    ribbon = _ribbon(centerline, half * 0.038 * morphology.tail_thickness)
    return {
        "id": "TAIL_MESH",
        "vertices": ribbon,
        "centerline": tuple((p.x, p.y) for p in centerline),
        "triangles": fr1.APPENDAGE_TRIANGLES,
        "viewDepth": _view_depth(-0.55 * morphology.trunk_length, 0.08, yaw),
    }


def topology_signature() -> str:
    return _hash_json({
        "baseTopology": fr1.topology_signature(),
        "coreAccessory": "EAR_PAIR_TRIANGLES_ATTACHED_TO_CORE",
        "meshDomains": ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL"),
    })


def _centerline_from_mesh(mesh: dict) -> Tuple[Vec2, ...]:
    if "centerline" in mesh:
        return tuple(Vec2(float(x), float(y)) for x, y in mesh["centerline"])
    vertices = mesh["vertices"]
    return tuple(
        Vec2(
            (vertices[i][0] + vertices[i + 1][0]) / 2.0,
            (vertices[i][1] + vertices[i + 1][1]) / 2.0,
        )
        for i in range(0, len(vertices), 2)
    )


def limb_crossing_count(meshes: Sequence[dict]) -> int:
    """Diagnostic only: counts strict centerline segment crossings."""
    lines = [(mesh["id"], _centerline_from_mesh(mesh)) for mesh in meshes]
    total = 0
    for i in range(len(lines)):
        _, a_line = lines[i]
        for j in range(i + 1, len(lines)):
            _, b_line = lines[j]
            for ai in range(len(a_line) - 1):
                for bi in range(len(b_line) - 1):
                    if fr1._segments_intersect(a_line[ai], a_line[ai + 1], b_line[bi], b_line[bi + 1]):
                        total += 1
    return total


def build_probe(fixture, direction: int = +1) -> FR2ProbeResult:
    state = fixture.state
    before_hash = fr1._hash_json(fr1._anchor_payload(state))
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    core = build_core_vertices(fixture)
    ears = build_ear_shapes(fixture)
    limbs = build_limb_meshes(fixture)
    tail = build_tail_mesh(fixture)
    after_hash = fr1._hash_json(fr1._anchor_payload(state))

    return FR2ProbeResult(
        semantic_hash=fixture.semantic_hash,
        morphology_id=fixture.morphology_id,
        case_id=fixture.case_id,
        size_dp=int(fixture.size_dp),
        t=float(fixture.t),
        direction=int(direction),
        yaw_rad=yaw,
        view_weights=tuple(sorted(canonical_view_weights(yaw).items())),
        core_vertices=core,
        ear_shapes=ears,
        limb_meshes=limbs,
        tail_mesh=tail,
        topology_signature=topology_signature(),
        semantic_anchor_hash_before=before_hash,
        semantic_anchor_hash_after=after_hash,
        paw_pin_error_max=max(mesh["pawPinError"] for mesh in limbs),
        core_self_intersections=fr1.count_self_intersections(core),
        correction_families=tuple(),
    )


def result_dict(result: FR2ProbeResult) -> dict:
    return {
        "version": PROTOTYPE_VERSION,
        "semanticHash": result.semantic_hash,
        "morphologyId": result.morphology_id,
        "caseId": result.case_id,
        "sizeDp": result.size_dp,
        "t": result.t,
        "direction": result.direction,
        "yawRad": result.yaw_rad,
        "viewWeights": dict(result.view_weights),
        "coreVertices": [[name, x, y] for name, x, y in result.core_vertices],
        "earShapes": [[[x, y] for x, y in shape] for shape in result.ear_shapes],
        "limbMeshes": list(result.limb_meshes),
        "tailMesh": result.tail_mesh,
        "topologySignature": result.topology_signature,
        "semanticAnchorHashBefore": result.semantic_anchor_hash_before,
        "semanticAnchorHashAfter": result.semantic_anchor_hash_after,
        "pawPinErrorMax": result.paw_pin_error_max,
        "coreSelfIntersections": result.core_self_intersections,
        "correctionFamilies": list(result.correction_families),
        "limbCrossingCount": limb_crossing_count(result.limb_meshes),
    }
