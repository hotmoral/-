from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import p1_fr4_internal_core_scaffold as v1
import p1_fr3_feline_core_topology_v5 as fr3_v5


PROTOTYPE_VERSION = "P1_FR4_INTERNAL_CORE_SCAFFOLD_V2_CONTAINMENT_SAFE"

PATCH_IDS = v1.PATCH_IDS

# V1 diagnostics showed:
# - all 837 self-crossings / 783 failed records belonged to CRANIUM_MASS;
# - CRANIUM_MASS had 1236 outside vertices across 546 records;
# - CERVICAL_BRIDGE had no crossing, but one repeated exact-front outside
#   vertex in 96 records;
# - THORAX_MASS had neither defect.
# V2 therefore removes the overlapping neck pair from CRANIUM_MASS and reduces
# only the head/cervical inset magnitudes. THORAX_MASS is unchanged.
PATCH_RULES = {
    "CRANIUM_MASS": {
        "pairs": (
            ("C00_NOSE_TOP", "C23_NOSE_BOTTOM"),
            ("C02_FOREHEAD", "C22_MUZZLE_BOTTOM"),
            ("C04_CROWN_REAR", "C21_JAW_REAR"),
        ),
        "inset": 0.34,
        "seam": (2, 3),
    },
    "CERVICAL_BRIDGE": {
        "pairs": v1.PATCH_RULES["CERVICAL_BRIDGE"]["pairs"],
        "inset": 0.30,
        "seam": v1.PATCH_RULES["CERVICAL_BRIDGE"]["seam"],
    },
    "THORAX_MASS": v1.PATCH_RULES["THORAX_MASS"],
}


InternalPatch = v1.InternalPatch
FR4ProbeResult = v1.FR4ProbeResult
point_in_polygon = v1.point_in_polygon
patch_self_intersections = v1.patch_self_intersections


def _build_patch(core: Dict[str, Tuple[float, float]], patch_id: str) -> InternalPatch:
    rule = PATCH_RULES[patch_id]
    upper = []
    lower = []
    for dorsal_id, ventral_id in rule["pairs"]:
        dorsal, ventral = v1._pair_inset(core[dorsal_id], core[ventral_id], float(rule["inset"]))
        upper.append(dorsal)
        lower.append(ventral)
    return InternalPatch(
        id=patch_id,
        vertices=tuple(upper + list(reversed(lower))),
        seam=rule["seam"],
    )


def build_internal_patches(core_vertices):
    core = v1._core_map(core_vertices)
    return tuple(_build_patch(core, patch_id) for patch_id in PATCH_IDS)


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
        "v1DiagnosticBasis": {
            "craniumCrossingFailedRecords": 783,
            "craniumOutsideVertices": 1236,
            "cervicalOutsideVertices": 96,
            "thoraxDefects": 0,
        },
    }
    return v1._hash_json(payload)


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
