from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Dict, Iterable, Tuple

import p1_fr1_mesh_probe as fr1
import p1_fr3_feline_core_topology_v5 as fr3_v5


PROTOTYPE_VERSION = "P1_FR4_INTERNAL_CORE_SCAFFOLD_V1_INTERNAL_ONLY"

PATCH_IDS = (
    "CRANIUM_MASS",
    "CERVICAL_BRIDGE",
    "THORAX_MASS",
)

# Each rule pairs a dorsal/outer CORE vertex with its ventral/inner counterpart.
# The generated patch points are symmetric insets along those pair segments.
# This keeps the first FR4 hypothesis subordinate to the frozen FR3 V5 envelope
# and introduces no independent semantic state.
PATCH_RULES = {
    "CRANIUM_MASS": {
        "pairs": (
            ("C00_NOSE_TOP", "C23_NOSE_BOTTOM"),
            ("C02_FOREHEAD", "C22_MUZZLE_BOTTOM"),
            ("C04_CROWN_REAR", "C21_JAW_REAR"),
            ("C05_NECK_DORSAL_HEAD", "C20_THROAT"),
        ),
        "inset": 0.58,
        "seam": (3, 4),
    },
    "CERVICAL_BRIDGE": {
        "pairs": (
            ("C05_NECK_DORSAL_HEAD", "C20_THROAT"),
            ("C06_NECK_DORSAL_BASE", "C19_NECK_VENTRAL_BASE"),
            ("C07_SHOULDER_FRONT", "C18_CHEST_FRONT"),
        ),
        "inset": 0.50,
        "seam": (2, 3),
    },
    "THORAX_MASS": {
        "pairs": (
            ("C07_SHOULDER_FRONT", "C18_CHEST_FRONT"),
            ("C08_SHOULDER_DORSAL", "C17_STERNUM"),
            ("C09_BACK_FRONT", "C16_BELLY_FRONT"),
            ("C10_BACK_REAR", "C15_BELLY_MID"),
        ),
        "inset": 0.56,
        "seam": None,
    },
}


@dataclass(frozen=True)
class InternalPatch:
    id: str
    vertices: Tuple[Tuple[float, float], ...]
    seam: Tuple[int, int] | None


@dataclass(frozen=True)
class FR4ProbeResult:
    base: object
    internal_patches: Tuple[InternalPatch, ...]
    scaffold_signature: str
    patch_self_intersections: int
    patch_outside_vertex_count: int


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _hash_json(value) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _lerp_point(a: Tuple[float, float], b: Tuple[float, float], t: float) -> Tuple[float, float]:
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _pair_inset(
    dorsal: Tuple[float, float],
    ventral: Tuple[float, float],
    inset: float,
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    center = _lerp_point(dorsal, ventral, 0.5)
    return _lerp_point(center, dorsal, inset), _lerp_point(center, ventral, inset)


def _core_map(core_vertices) -> Dict[str, Tuple[float, float]]:
    return {vertex_id: (float(x), float(y)) for vertex_id, x, y in core_vertices}


def _build_patch(core: Dict[str, Tuple[float, float]], patch_id: str) -> InternalPatch:
    rule = PATCH_RULES[patch_id]
    upper = []
    lower = []
    for dorsal_id, ventral_id in rule["pairs"]:
        dorsal, ventral = _pair_inset(core[dorsal_id], core[ventral_id], float(rule["inset"]))
        upper.append(dorsal)
        lower.append(ventral)
    # Cyclic order follows the dorsal chain toward the body, then returns on
    # the ventral chain. The topology is fixed for every fixture.
    vertices = tuple(upper + list(reversed(lower)))
    return InternalPatch(id=patch_id, vertices=vertices, seam=rule["seam"])


def build_internal_patches(core_vertices) -> Tuple[InternalPatch, ...]:
    core = _core_map(core_vertices)
    return tuple(_build_patch(core, patch_id) for patch_id in PATCH_IDS)


def _point_on_segment(p, a, b, eps: float = 1e-9) -> bool:
    cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
    if abs(cross) > eps:
        return False
    return (
        min(a[0], b[0]) - eps <= p[0] <= max(a[0], b[0]) + eps
        and min(a[1], b[1]) - eps <= p[1] <= max(a[1], b[1]) + eps
    )


def point_in_polygon(point, polygon: Iterable[Tuple[float, float]]) -> bool:
    points = tuple(polygon)
    inside = False
    j = len(points) - 1
    for i in range(len(points)):
        a = points[j]
        b = points[i]
        if _point_on_segment(point, a, b):
            return True
        yi, yj = b[1], a[1]
        xi, xj = b[0], a[0]
        crosses = (yi > point[1]) != (yj > point[1])
        if crosses:
            x_at_y = (xj - xi) * (point[1] - yi) / (yj - yi) + xi
            if point[0] < x_at_y:
                inside = not inside
        j = i
    return inside


def patch_self_intersections(patch: InternalPatch) -> int:
    core_like = tuple((f"{patch.id}_{index}", x, y) for index, (x, y) in enumerate(patch.vertices))
    return fr1.count_self_intersections(core_like)


def scaffold_signature() -> str:
    payload = {
        "version": PROTOTYPE_VERSION,
        "patchIds": PATCH_IDS,
        "rules": {
            patch_id: {
                "pairs": PATCH_RULES[patch_id]["pairs"],
                "inset": PATCH_RULES[patch_id]["inset"],
                "vertexCount": 2 * len(PATCH_RULES[patch_id]["pairs"]),
                "seam": PATCH_RULES[patch_id]["seam"],
            }
            for patch_id in PATCH_IDS
        },
        "externalCore": "FR3_V5_24PT_BYTE_EQUIVALENT",
        "externalMeshDomains": ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL"),
        "semanticState": "DERIVED_READ_ONLY",
    }
    return _hash_json(payload)


def build_probe(fixture, direction: int = +1) -> FR4ProbeResult:
    base = fr3_v5.build_probe(fixture, direction)
    patches = build_internal_patches(base.core_vertices)
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
            "seam": list(patch.seam) if patch.seam is not None else None,
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
