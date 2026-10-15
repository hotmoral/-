from __future__ import annotations

from dataclasses import replace
import hashlib
import json

import p1_fr1_mesh_probe as fr1
import p1_fr3_feline_core_topology_v5 as fr3_v5
import p1_fr4_internal_core_scaffold as fr4_base
import p1_fr4_internal_core_scaffold_v3 as fr4_v3
import p1_fr5_core_mass_silhouette_v1 as v1


PROTOTYPE_VERSION = "P1_FR5_CORE_MASS_SILHOUETTE_V2_FINAL_COEFFICIENT"
LAYER_IDS = v1.LAYER_IDS
MAX_NORMALIZED_CORE_DISPLACEMENT = v1.MAX_NORMALIZED_CORE_DISPLACEMENT
INFLUENCE_WEIGHTS = v1.INFLUENCE_WEIGHTS
FR5ProbeResult = v1.FR5ProbeResult

# Final FR5 coefficient-only candidate. These are the exact values authorized by
# P1_FR5_V1_DIRECT_REVIEW_AND_V2_DECISION.md. No V3 tuning is allowed.
VIEW_SCALES = {
    "CRANIUM_MASS": {"PROFILE": 1.00, "THREE_QUARTER": 1.14, "FRONT": 1.20},
    "CERVICAL_BRIDGE": {"PROFILE": 1.00, "THREE_QUARTER": 0.88, "FRONT": 0.80},
    "THORAX_MASS": {"PROFILE": 1.00, "THREE_QUARTER": 1.08, "FRONT": 1.12},
}


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _hash_json(value) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _layer_scale(layer_id: str, view_weights) -> float:
    scales = VIEW_SCALES[layer_id]
    return sum(float(view_weights.get(view, 0.0)) * scales[view] for view in scales)


def build_integrated_core(fixture, control_core):
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    view_weights = fr3_v5.canonical_view_weights(yaw)
    if v1._is_exact_profile(view_weights):
        return tuple(control_core)
    frames = v1._layer_frames(fixture)
    integrated = []
    for vertex_id, x, y in control_core:
        base = (float(x), float(y))
        dx = 0.0
        dy = 0.0
        influences = INFLUENCE_WEIGHTS.get(vertex_id, ())
        if sum(weight for _, weight in influences) > 1.0 + 1e-12:
            raise RuntimeError((vertex_id, influences))
        for layer_id, influence in influences:
            seed, axis = frames[layer_id]
            target = v1._scaled_perpendicular_target(
                base, seed, axis, _layer_scale(layer_id, view_weights)
            )
            dx += influence * (target[0] - base[0])
            dy += influence * (target[1] - base[1])
        integrated.append((vertex_id, base[0] + dx, base[1] + dy))
    return tuple(integrated)


def integration_signature() -> str:
    payload = {
        "version": PROTOTYPE_VERSION,
        "externalCoreVertexIds": fr3_v5.CORE_VERTEX_IDS,
        "externalCoreBoundaryEdges": fr3_v5.CORE_BOUNDARY_EDGES,
        "layerIds": LAYER_IDS,
        "layerFrames": {
            "CRANIUM_MASS": {"seed": "HEAD_ROOT", "axis": "HEAD_ROOT_TO_FOREQUARTER_REF"},
            "CERVICAL_BRIDGE": {"seed": "MID_HEAD_ROOT_FOREQUARTER_REF", "axis": "HEAD_ROOT_TO_FOREQUARTER_REF"},
            "THORAX_MASS": {"seed": "FOREQUARTER_REF", "axis": "FOREQUARTER_REF_TO_BODY_ROOT"},
        },
        "viewScales": VIEW_SCALES,
        "influenceWeights": INFLUENCE_WEIGHTS,
        "transform": "PERPENDICULAR_COMPONENT_ONLY",
        "profileRule": "EXACT_CONTROL_CORE_BYPASS",
        "externalMeshDomains": ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL"),
        "semanticState": "EXISTING_ANCHORS_DERIVED_READ_ONLY",
        "candidateRule": "FINAL_COEFFICIENT_ONLY_NO_V3",
    }
    return _hash_json(payload)


def build_probe(fixture, direction: int = +1) -> FR5ProbeResult:
    control = fr3_v5.build_probe(fixture, direction)
    final_core = build_integrated_core(fixture, control.core_vertices)
    final_probe = replace(
        control,
        core_vertices=final_core,
        core_self_intersections=fr1.count_self_intersections(final_core),
    )
    patches = fr4_v3.build_internal_patches(fixture, final_core)
    core_polygon = tuple((x, y) for _, x, y in final_core)
    patch_intersections = sum(fr4_base.patch_self_intersections(patch) for patch in patches)
    patch_outside = sum(
        1
        for patch in patches
        for vertex in patch.vertices
        if not fr4_base.point_in_polygon(vertex, core_polygon)
    )
    max_displacement = v1._core_displacement(control.core_vertices, final_core)
    half_size = float(fixture.size_dp) / 2.0
    normalized = max_displacement / half_size if half_size > 0.0 else float("inf")
    return FR5ProbeResult(
        control=control,
        base=final_probe,
        internal_patches=patches,
        integration_signature=integration_signature(),
        patch_self_intersections=patch_intersections,
        patch_outside_vertex_count=patch_outside,
        max_core_displacement=max_displacement,
        normalized_max_core_displacement=normalized,
        ear_base_outside_control=v1.ear_base_outside_count(control.core_vertices, control.ear_shapes),
        ear_base_outside_final=v1.ear_base_outside_count(final_core, final_probe.ear_shapes),
    )


def result_dict(result: FR5ProbeResult) -> dict:
    payload = fr3_v5.result_dict(result.base)
    payload["version"] = PROTOTYPE_VERSION
    payload["integrationSignature"] = result.integration_signature
    payload["patchSelfIntersections"] = result.patch_self_intersections
    payload["patchOutsideVertexCount"] = result.patch_outside_vertex_count
    payload["maxCoreDisplacement"] = result.max_core_displacement
    payload["normalizedMaxCoreDisplacement"] = result.normalized_max_core_displacement
    payload["earBaseOutsideControl"] = result.ear_base_outside_control
    payload["earBaseOutsideFinal"] = result.ear_base_outside_final
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
CORE_SKIN_WEIGHTS = fr3_v5.CORE_SKIN_WEIGHTS
CANONICAL_SHAPES = fr3_v5.CANONICAL_SHAPES
topology_signature = fr3_v5.topology_signature
limb_crossing_count = fr3_v5.limb_crossing_count
