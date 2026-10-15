from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from math import cos, pi, sin
from typing import Dict, Iterable, List, Sequence, Tuple

from e_v0_profiles import morphology_by_id, orientation_by_id
from model import Vec2


PROBE_VERSION = "P1_FR1_LAYERED_VIEW_MESH_FEASIBILITY_V1"
CORE_VERTEX_IDS = (
    "V00_NOSE_TOP",
    "V01_FOREHEAD",
    "V02_EAR_CROWN_A",
    "V03_CROWN",
    "V04_NECK_DORSAL",
    "V05_SHOULDER_DORSAL",
    "V06_BACK_DORSAL",
    "V07_HAUNCH_DORSAL",
    "V08_RUMP",
    "V09_HAUNCH_VENTRAL",
    "V10_BELLY_REAR",
    "V11_BELLY_FRONT",
    "V12_CHEST",
    "V13_THROAT",
    "V14_MUZZLE_BOTTOM",
    "V15_NOSE_BOTTOM",
)

# Boundary is a single cyclic contour. Triangulation is intentionally not
# prescribed here: FR1 proves stable contour correspondence/topology, not a
# production tessellator.
CORE_BOUNDARY_EDGES = tuple(
    (CORE_VERTEX_IDS[i], CORE_VERTEX_IDS[(i + 1) % len(CORE_VERTEX_IDS)])
    for i in range(len(CORE_VERTEX_IDS))
)
APPENDAGE_VERTEX_IDS = (
    "A0_ROOT_L", "A0_ROOT_R",
    "A1_JOINT_L", "A1_JOINT_R",
    "A2_DISTAL_L", "A2_DISTAL_R",
    "A3_PAW_L", "A3_PAW_R",
)
APPENDAGE_TRIANGLES = (
    (0, 1, 2), (1, 3, 2),
    (2, 3, 4), (3, 5, 4),
    (4, 5, 6), (5, 7, 6),
)

# Each boundary vertex belongs primarily to a semantic region. This is not a
# new physical state; it is a deformation-weight simplification for the probe.
CORE_REGION = {
    "V00_NOSE_TOP": "HEAD",
    "V01_FOREHEAD": "HEAD",
    "V02_EAR_CROWN_A": "HEAD",
    "V03_CROWN": "HEAD",
    "V04_NECK_DORSAL": "FORE",
    "V05_SHOULDER_DORSAL": "FORE",
    "V06_BACK_DORSAL": "BODY",
    "V07_HAUNCH_DORSAL": "PELVIS",
    "V08_RUMP": "PELVIS",
    "V09_HAUNCH_VENTRAL": "PELVIS",
    "V10_BELLY_REAR": "BODY",
    "V11_BELLY_FRONT": "BODY",
    "V12_CHEST": "FORE",
    "V13_THROAT": "FORE",
    "V14_MUZZLE_BOTTOM": "HEAD",
    "V15_NOSE_BOTTOM": "HEAD",
}

# Normalized canonical silhouette bases. The same cyclic vertex correspondence
# is reused at profile, 3/4 and front. Values are structural debug cages, not
# final art. They deliberately avoid serial ellipse primitives.
PROFILE_SHAPE = (
    (1.42, -0.18), (1.24, -0.50), (1.02, -0.78), (0.76, -0.58),
    (0.49, -0.40), (0.20, -0.54), (-0.30, -0.50), (-0.78, -0.56),
    (-1.08, -0.18), (-0.88, 0.42), (-0.38, 0.36), (0.06, 0.32),
    (0.35, 0.42), (0.56, 0.12), (1.04, 0.10), (1.38, 0.00),
)
THREE_QUARTER_SHAPE = (
    (0.92, -0.24), (0.78, -0.50), (0.55, -0.78), (0.28, -0.63),
    (0.02, -0.46), (-0.28, -0.53), (-0.56, -0.46), (-0.72, -0.34),
    (-0.78, 0.02), (-0.62, 0.45), (-0.30, 0.52), (0.08, 0.50),
    (0.42, 0.40), (0.58, 0.14), (0.78, 0.08), (0.94, -0.04),
)
FRONT_SHAPE = (
    (0.56, -0.28), (0.43, -0.52), (0.23, -0.80), (0.00, -0.64),
    (-0.23, -0.80), (-0.43, -0.52), (-0.56, -0.28), (-0.58, 0.12),
    (-0.44, 0.50), (-0.22, 0.62), (0.00, 0.58), (0.22, 0.62),
    (0.44, 0.50), (0.58, 0.12), (0.62, -0.05), (0.63, -0.18),
)

CANONICAL_SHAPES = {
    "PROFILE": PROFILE_SHAPE,
    "THREE_QUARTER": THREE_QUARTER_SHAPE,
    "FRONT": FRONT_SHAPE,
}


@dataclass(frozen=True)
class MeshProbeResult:
    semantic_hash: str
    morphology_id: str
    case_id: str
    size_dp: int
    t: float
    direction: int
    yaw_rad: float
    view_weights: Tuple[Tuple[str, float], ...]
    core_vertices: Tuple[Tuple[str, float, float], ...]
    limb_meshes: Tuple[dict, ...]
    tail_mesh: dict
    topology_signature: str
    semantic_anchor_hash_before: str
    semantic_anchor_hash_after: str
    paw_pin_error_max: float
    core_self_intersections: int
    correction_families: Tuple[str, ...]


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def canonical_view_weights(yaw_rad: float) -> Dict[str, float]:
    """Piecewise-linear canonical shape weights for |yaw| 0..90 degrees."""
    u = _clamp01(abs(yaw_rad) / (pi / 2.0))
    if u <= 0.5:
        q = u / 0.5
        return {"PROFILE": 1.0 - q, "THREE_QUARTER": q, "FRONT": 0.0}
    q = (u - 0.5) / 0.5
    return {"PROFILE": 0.0, "THREE_QUARTER": 1.0 - q, "FRONT": q}


def _shape_blend(weights: Dict[str, float]) -> List[Tuple[float, float]]:
    points = []
    for index in range(len(CORE_VERTEX_IDS)):
        x = sum(CANONICAL_SHAPES[name][index][0] * weight for name, weight in weights.items())
        y = sum(CANONICAL_SHAPES[name][index][1] * weight for name, weight in weights.items())
        points.append((x, y))
    return points


def _anchor_payload(state) -> dict:
    return {
        "anchors": {
            name: [round(point.x, 12), round(point.y, 12)]
            for name, point in sorted(state.anchors.items())
        },
        "contacts": [
            {
                "id": contact.id,
                "point": [round(contact.point.x, 12), round(contact.point.y, 12)],
                "phase": contact.phase.value,
                "loadBearing": bool(contact.load_bearing),
            }
            for contact in sorted(state.contacts, key=lambda item: item.id)
        ],
        "supportSet": sorted(state.support_set),
    }


def _hash_json(value) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _screen_scale(fixture, weights: Dict[str, float]) -> Tuple[float, float]:
    morphology = morphology_by_id(fixture.morphology_id)
    orientation = orientation_by_id(fixture.morphology_id)
    half = fixture.size_dp / 2.0

    profile_x = half * (0.92 + 0.34 * morphology.trunk_length + 0.12 * morphology.head_scale)
    qtr_x = half * (
        0.72
        + 0.18 * morphology.trunk_length
        + 0.11 * max(orientation.thorax_width_scale, orientation.pelvis_width_scale)
    )
    front_x = half * 0.78 * max(orientation.thorax_width_scale, orientation.pelvis_width_scale)

    common_y = half * (
        0.78
        + 0.20 * morphology.trunk_depth
        + 0.08 * morphology.head_scale
        + 0.05 * max(morphology.forequarter_scale, morphology.pelvis_scale)
    )

    sx = (
        weights["PROFILE"] * profile_x
        + weights["THREE_QUARTER"] * qtr_x
        + weights["FRONT"] * front_x
    )
    return sx, common_y


def _region_anchor(state, region: str) -> Vec2:
    if region == "HEAD":
        return state.anchors["HEAD_ROOT"]
    if region == "FORE":
        return state.anchors["FOREQUARTER_REF"]
    if region == "PELVIS":
        return state.anchors["PELVIS_REF"]
    if region == "BODY":
        return state.anchors["BODY_ROOT"]
    raise KeyError(region)


def _reference_region_center(shape: Sequence[Tuple[float, float]], region: str) -> Tuple[float, float]:
    indices = [i for i, vertex_id in enumerate(CORE_VERTEX_IDS) if CORE_REGION[vertex_id] == region]
    return (
        sum(shape[i][0] for i in indices) / len(indices),
        sum(shape[i][1] for i in indices) / len(indices),
    )


def build_core_vertices(fixture) -> Tuple[Tuple[str, float, float], ...]:
    state = fixture.state
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    weights = canonical_view_weights(yaw)
    blended = _shape_blend(weights)
    sx, sy = _screen_scale(fixture, weights)

    # Region-local offsets are evaluated from the same blended shape. The
    # semantic anchors translate each region; the visible mesh never mutates the
    # anchors themselves.
    region_centers = {
        region: _reference_region_center(blended, region)
        for region in ("HEAD", "FORE", "BODY", "PELVIS")
    }

    mirror = 1.0 if yaw >= 0.0 else -1.0
    vertices = []
    for vertex_id, (x, y) in zip(CORE_VERTEX_IDS, blended):
        region = CORE_REGION[vertex_id]
        anchor = _region_anchor(state, region)
        rx, ry = region_centers[region]
        local_x = (x - rx) * sx * mirror
        local_y = (y - ry) * sy
        vertices.append((vertex_id, anchor.x + local_x, anchor.y + local_y))
    return tuple(vertices)


def _segments_intersect(a: Vec2, b: Vec2, c: Vec2, d: Vec2, eps: float = 1e-9) -> bool:
    def orient(p, q, r):
        return (q.x - p.x) * (r.y - p.y) - (q.y - p.y) * (r.x - p.x)

    o1, o2, o3, o4 = orient(a, b, c), orient(a, b, d), orient(c, d, a), orient(c, d, b)
    return (
        ((o1 > eps and o2 < -eps) or (o1 < -eps and o2 > eps))
        and ((o3 > eps and o4 < -eps) or (o3 < -eps and o4 > eps))
    )


def count_self_intersections(core_vertices: Sequence[Tuple[str, float, float]]) -> int:
    points = [Vec2(x, y) for _, x, y in core_vertices]
    n = len(points)
    count = 0
    for i in range(n):
        a, b = points[i], points[(i + 1) % n]
        for j in range(i + 1, n):
            if j in (i, (i + 1) % n):
                continue
            if (j + 1) % n in (i, (i + 1) % n):
                continue
            if i == 0 and j == n - 1:
                continue
            c, d = points[j], points[(j + 1) % n]
            if _segments_intersect(a, b, c, d):
                count += 1
    return count


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


def _limb_centerline(root: Vec2, paw: Vec2, side_sign: float, yaw: float, kind: str, size_dp: int) -> Tuple[Vec2, ...]:
    delta = paw - root
    front = sin(yaw) * sin(yaw)
    outward = side_sign * sin(yaw) * (size_dp / 2.0) * (0.08 + 0.04 * front)
    if kind == "FORE":
        p1 = Vec2(root.x + delta.x * 0.38 + outward, root.y + delta.y * 0.38)
        p2 = Vec2(root.x + delta.x * 0.74 + outward * 0.35, root.y + delta.y * 0.75)
    else:
        p1 = Vec2(root.x + delta.x * 0.30 + outward * 1.15, root.y + delta.y * 0.30)
        p2 = Vec2(root.x + delta.x * 0.66 - outward * 0.12, root.y + delta.y * 0.69)
    return (root, p1, p2, paw)


def _view_depth(x_forward: float, z_left: float, yaw: float) -> float:
    return x_forward * sin(yaw) - z_left * cos(yaw)


def build_limb_meshes(fixture) -> Tuple[dict, ...]:
    state = fixture.state
    morphology = morphology_by_id(fixture.morphology_id)
    orientation = orientation_by_id(fixture.morphology_id)
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    half = fixture.size_dp / 2.0
    front = sin(yaw) * sin(yaw)

    meshes = []
    specs = (
        ("FORE_PAW_L", "FORE", +1.0),
        ("FORE_PAW_R", "FORE", -1.0),
        ("HIND_PAW_L", "HIND", +1.0),
        ("HIND_PAW_R", "HIND", -1.0),
    )
    for paw_id, kind, side_sign in specs:
        if kind == "FORE":
            base = state.anchors["FOREQUARTER_REF"]
            sep = sin(yaw) * half * 0.18 * orientation.thorax_width_scale
            root = Vec2(base.x + side_sign * sep, base.y + 0.02 * half)
            limb_scale = morphology.fore_limb_length
            x_forward = +0.47 * morphology.trunk_length
            z_left = side_sign * (0.18 + 0.025 * front) * orientation.thorax_width_scale
        else:
            base = state.anchors["PELVIS_REF"]
            sep = sin(yaw) * half * 0.20 * orientation.pelvis_width_scale
            root = Vec2(base.x + side_sign * sep, base.y + 0.04 * half)
            limb_scale = morphology.hind_limb_length
            x_forward = -0.47 * morphology.trunk_length
            z_left = side_sign * (0.20 + 0.030 * front) * orientation.pelvis_width_scale

        paw = state.anchors[paw_id]
        centerline = _limb_centerline(root, paw, side_sign, yaw, kind, fixture.size_dp)
        half_width = half * (0.035 if kind == "FORE" else 0.040) * limb_scale
        ribbon = _ribbon(centerline, half_width)
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
            "triangles": APPENDAGE_TRIANGLES,
            "pawId": paw_id,
            "pawPinError": pin_error,
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
    length = half * 0.58 * morphology.tail_length
    p1 = Vec2(root.x + direction * length * 0.38, root.y - half * 0.08)
    p2 = Vec2(root.x + direction * length * 0.72, root.y - half * 0.22)
    p3 = Vec2(root.x + direction * length, root.y - half * 0.14)
    ribbon = _ribbon((root, p1, p2, p3), half * 0.035 * morphology.tail_thickness)
    return {
        "id": "TAIL_MESH",
        "vertices": ribbon,
        "triangles": APPENDAGE_TRIANGLES,
        "viewDepth": _view_depth(-0.55 * morphology.trunk_length, 0.08, yaw),
    }


def topology_signature() -> str:
    return _hash_json({
        "coreVertexIds": CORE_VERTEX_IDS,
        "coreBoundaryEdges": CORE_BOUNDARY_EDGES,
        "appendageVertexIds": APPENDAGE_VERTEX_IDS,
        "appendageTriangles": APPENDAGE_TRIANGLES,
        "meshDomains": ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL"),
    })


def build_probe(fixture, direction: int = +1) -> MeshProbeResult:
    state = fixture.state
    before_payload = _anchor_payload(state)
    before_hash = _hash_json(before_payload)

    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    core = build_core_vertices(fixture)
    limbs = build_limb_meshes(fixture)
    tail = build_tail_mesh(fixture)

    # Re-read authoritative state after all visible-geometry work. This catches
    # accidental mutation even though BodyPoseState is not globally immutable.
    after_payload = _anchor_payload(state)
    after_hash = _hash_json(after_payload)

    return MeshProbeResult(
        semantic_hash=fixture.semantic_hash,
        morphology_id=fixture.morphology_id,
        case_id=fixture.case_id,
        size_dp=int(fixture.size_dp),
        t=float(fixture.t),
        direction=int(direction),
        yaw_rad=yaw,
        view_weights=tuple(sorted(canonical_view_weights(yaw).items())),
        core_vertices=core,
        limb_meshes=limbs,
        tail_mesh=tail,
        topology_signature=topology_signature(),
        semantic_anchor_hash_before=before_hash,
        semantic_anchor_hash_after=after_hash,
        paw_pin_error_max=max(mesh["pawPinError"] for mesh in limbs),
        core_self_intersections=count_self_intersections(core),
        correction_families=tuple(),
    )


def result_dict(result: MeshProbeResult) -> dict:
    return {
        "version": PROBE_VERSION,
        "semanticHash": result.semantic_hash,
        "morphologyId": result.morphology_id,
        "caseId": result.case_id,
        "sizeDp": result.size_dp,
        "t": result.t,
        "direction": result.direction,
        "yawRad": result.yaw_rad,
        "viewWeights": dict(result.view_weights),
        "coreVertices": [list(item) for item in result.core_vertices],
        "limbMeshes": list(result.limb_meshes),
        "tailMesh": result.tail_mesh,
        "topologySignature": result.topology_signature,
        "semanticAnchorHashBefore": result.semantic_anchor_hash_before,
        "semanticAnchorHashAfter": result.semantic_anchor_hash_after,
        "pawPinErrorMax": result.paw_pin_error_max,
        "coreSelfIntersections": result.core_self_intersections,
        "correctionFamilies": list(result.correction_families),
    }
