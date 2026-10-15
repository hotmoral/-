from __future__ import annotations

import math
from typing import Iterable, Tuple

import p1_fr1_mesh_probe as fr1
import p1_fr3_feline_core_topology_v5 as fr3_v5
import p1_fr4_internal_core_scaffold as v1


PROTOTYPE_VERSION = "P1_FR4_INTERNAL_CORE_SCAFFOLD_V3_SEED_RADIAL"
PATCH_IDS = v1.PATCH_IDS

# Seed safety was verified over the full retained 1,770-record matrix before
# authoring V3: HEAD_ROOT, FOREQUARTER_REF, HEAD_FORE_MID and BODY_ROOT all
# remained inside the FR3 V5 CORE for every record.
#
# V1/V2 showed that boundary-to-boundary chords can leave or fold across the
# near-front CORE even when their endpoints are valid. V3 therefore constructs
# CRANIUM and CERVICAL patches from proven internal seeds. Fixed local angles
# are ray-cast to the first CORE boundary hit, then shortened by fixed fractions.
# This keeps one topology/order for all records and clips intrinsically to CORE.

CRANIUM_ANGLES_DEG = (0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0)
CRANIUM_FRACTIONS = (0.42, 0.55, 0.66, 0.70, 0.70, 0.70, 0.66, 0.55)
CERVICAL_ANGLES_DEG = (0.0, 60.0, 120.0, 180.0, 240.0, 300.0)
CERVICAL_FRACTIONS = (0.62, 0.36, 0.36, 0.62, 0.36, 0.36)


InternalPatch = v1.InternalPatch
FR4ProbeResult = v1.FR4ProbeResult
point_in_polygon = v1.point_in_polygon
patch_self_intersections = v1.patch_self_intersections


def _normalize(vector: Tuple[float, float]) -> Tuple[float, float]:
    length = math.hypot(vector[0], vector[1])
    if length <= 1e-12:
        raise ValueError("degenerate internal scaffold axis")
    return (vector[0] / length, vector[1] / length)


def _cross(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return a[0] * b[1] - a[1] * b[0]


def _sub(a: Tuple[float, float], b: Tuple[float, float]) -> Tuple[float, float]:
    return (a[0] - b[0], a[1] - b[1])


def _first_boundary_distance(
    seed: Tuple[float, float],
    direction: Tuple[float, float],
    polygon: Iterable[Tuple[float, float]],
) -> float:
    points = tuple(polygon)
    best = None
    for index, a in enumerate(points):
        b = points[(index + 1) % len(points)]
        edge = _sub(b, a)
        denom = _cross(direction, edge)
        if abs(denom) <= 1e-12:
            continue
        a_minus_seed = _sub(a, seed)
        t = _cross(a_minus_seed, edge) / denom
        u = _cross(a_minus_seed, direction) / denom
        if t > 1e-9 and -1e-9 <= u <= 1.0 + 1e-9:
            if best is None or t < best:
                best = t
    if best is None:
        raise ValueError("internal scaffold ray did not hit CORE boundary")
    return best


def _local_direction(axis: Tuple[float, float], angle_deg: float) -> Tuple[float, float]:
    angle = math.radians(angle_deg)
    perpendicular = (-axis[1], axis[0])
    direction = (
        axis[0] * math.cos(angle) + perpendicular[0] * math.sin(angle),
        axis[1] * math.cos(angle) + perpendicular[1] * math.sin(angle),
    )
    return _normalize(direction)


def _radial_patch(
    patch_id: str,
    seed: Tuple[float, float],
    axis: Tuple[float, float],
    polygon: Tuple[Tuple[float, float], ...],
    angles_deg: Tuple[float, ...],
    fractions: Tuple[float, ...],
) -> InternalPatch:
    if len(angles_deg) != len(fractions):
        raise ValueError("angle/fraction mismatch")
    vertices = []
    for angle_deg, fraction in zip(angles_deg, fractions):
        direction = _local_direction(axis, angle_deg)
        boundary_distance = _first_boundary_distance(seed, direction, polygon)
        distance = boundary_distance * fraction
        vertices.append((seed[0] + direction[0] * distance, seed[1] + direction[1] * distance))
    return InternalPatch(id=patch_id, vertices=tuple(vertices), seam=None)


def build_internal_patches(fixture, core_vertices) -> Tuple[InternalPatch, ...]:
    polygon = tuple((float(x), float(y)) for _, x, y in core_vertices)
    head = fixture.state.anchors["HEAD_ROOT"]
    fore = fixture.state.anchors["FOREQUARTER_REF"]
    head_seed = (float(head.x), float(head.y))
    fore_point = (float(fore.x), float(fore.y))
    axis = _normalize(_sub(fore_point, head_seed))
    cervical_seed = (
        (head_seed[0] + fore_point[0]) * 0.5,
        (head_seed[1] + fore_point[1]) * 0.5,
    )
    cranium = _radial_patch(
        "CRANIUM_MASS", head_seed, axis, polygon, CRANIUM_ANGLES_DEG, CRANIUM_FRACTIONS
    )
    cervical = _radial_patch(
        "CERVICAL_BRIDGE", cervical_seed, axis, polygon, CERVICAL_ANGLES_DEG, CERVICAL_FRACTIONS
    )
    core_map = v1._core_map(core_vertices)
    thorax = v1._build_patch(core_map, "THORAX_MASS")
    return (cranium, cervical, thorax)


def scaffold_signature() -> str:
    payload = {
        "version": PROTOTYPE_VERSION,
        "patchIds": PATCH_IDS,
        "cranium": {
            "seed": "HEAD_ROOT",
            "axis": "HEAD_ROOT_TO_FOREQUARTER_REF",
            "anglesDeg": CRANIUM_ANGLES_DEG,
            "fractions": CRANIUM_FRACTIONS,
            "vertexCount": len(CRANIUM_ANGLES_DEG),
        },
        "cervical": {
            "seed": "MID_HEAD_ROOT_FOREQUARTER_REF",
            "axis": "HEAD_ROOT_TO_FOREQUARTER_REF",
            "anglesDeg": CERVICAL_ANGLES_DEG,
            "fractions": CERVICAL_FRACTIONS,
            "vertexCount": len(CERVICAL_ANGLES_DEG),
        },
        "thorax": {
            "rule": v1.PATCH_RULES["THORAX_MASS"],
            "vertexCount": 2 * len(v1.PATCH_RULES["THORAX_MASS"]["pairs"]),
        },
        "boundaryClipRule": "FIRST_RAY_HIT_TIMES_FIXED_FRACTION",
        "seedSafetyDiagnostic": "1770_OF_1770_INSIDE",
        "externalCore": "FR3_V5_24PT_BYTE_EQUIVALENT",
        "externalMeshDomains": ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL"),
        "semanticState": "EXISTING_ANCHORS_DERIVED_READ_ONLY",
    }
    return v1._hash_json(payload)


def build_probe(fixture, direction: int = +1) -> FR4ProbeResult:
    base = fr3_v5.build_probe(fixture, direction)
    patches = build_internal_patches(fixture, base.core_vertices)
    core_polygon = tuple((x, y) for _, x, y in base.core_vertices)
    intersections = sum(patch_self_intersections(patch) for patch in patches)
    outside = sum(
        1
        for patch in patches
        for vertex in patch.vertices
        if not point_in_polygon(vertex, core_polygon)
    )
    return FR4ProbeResult(
        base=base,
        internal_patches=patches,
        scaffold_signature=scaffold_signature(),
        patch_self_intersections=intersections,
        patch_outside_vertex_count=outside,
    )


def result_dict(result: FR4ProbeResult) -> dict:
    payload = fr3_v5.result_dict(result.base)
    payload["version"] = PROTOTYPE_VERSION
    payload["scaffoldSignature"] = result.scaffold_signature
    payload["patchSelfIntersections"] = result.patch_self_intersections
    payload["patchOutsideVertexCount"] = result.patch_outside_vertex_count
    payload["internalPatches"] = [
        {
            "id": patch.id,
            "vertices": [list(vertex) for vertex in patch.vertices],
            "seam": None,
        }
        for patch in result.internal_patches
    ]
    return payload


CORE_VERTEX_IDS = fr3_v5.CORE_VERTEX_IDS
CORE_BOUNDARY_EDGES = fr3_v5.CORE_BOUNDARY_EDGES
CANONICAL_SHAPES = fr3_v5.CANONICAL_SHAPES
CORE_SKIN_WEIGHTS = fr3_v5.CORE_SKIN_WEIGHTS
topology_signature = fr3_v5.topology_signature
limb_crossing_count = fr3_v5.limb_crossing_count
