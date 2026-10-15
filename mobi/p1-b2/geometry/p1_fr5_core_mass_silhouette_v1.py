from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
import math
from typing import Dict, Tuple

import p1_fr1_mesh_probe as fr1
import p1_fr3_feline_core_topology_v5 as fr3_v5
import p1_fr4_internal_core_scaffold as fr4_base
import p1_fr4_internal_core_scaffold_v3 as fr4_v3


PROTOTYPE_VERSION = "P1_FR5_CORE_MASS_SILHOUETTE_V1_PERP_ONLY"
LAYER_IDS = ("CRANIUM_MASS", "CERVICAL_BRIDGE", "THORAX_MASS")
MAX_NORMALIZED_CORE_DISPLACEMENT = 0.18

# The first FR5 candidate deliberately changes only mass thickness perpendicular
# to existing semantic axes. PROFILE remains exact. 3Q/front modestly widen the
# cranium and upper thorax while narrowing the cervical bridge.
VIEW_SCALES: Dict[str, Dict[str, float]] = {
    "CRANIUM_MASS": {"PROFILE": 1.00, "THREE_QUARTER": 1.08, "FRONT": 1.14},
    "CERVICAL_BRIDGE": {"PROFILE": 1.00, "THREE_QUARTER": 0.94, "FRONT": 0.88},
    "THORAX_MASS": {"PROFILE": 1.00, "THREE_QUARTER": 1.04, "FRONT": 1.08},
}

# Shared point-to-mass influence topology. It is global across morphology, pose,
# size, time and direction. Trunk/haunch C10..C15 remain untouched.
INFLUENCE_WEIGHTS: Dict[str, Tuple[Tuple[str, float], ...]] = {
    "C00_NOSE_TOP": (("CRANIUM_MASS", 1.00),),
    "C01_BRIDGE": (("CRANIUM_MASS", 1.00),),
    "C02_FOREHEAD": (("CRANIUM_MASS", 1.00),),
    "C03_CROWN_FRONT": (("CRANIUM_MASS", 1.00),),
    "C04_CROWN_REAR": (("CRANIUM_MASS", 1.00),),
    "C05_NECK_DORSAL_HEAD": (("CRANIUM_MASS", 0.75), ("CERVICAL_BRIDGE", 0.25)),
    "C06_NECK_DORSAL_BASE": (("CERVICAL_BRIDGE", 1.00),),
    "C07_SHOULDER_FRONT": (("CERVICAL_BRIDGE", 0.65), ("THORAX_MASS", 0.35)),
    "C08_SHOULDER_DORSAL": (("THORAX_MASS", 0.70),),
    "C09_BACK_FRONT": (("THORAX_MASS", 0.30),),
    "C16_BELLY_FRONT": (("THORAX_MASS", 0.30),),
    "C17_STERNUM": (("THORAX_MASS", 0.70),),
    "C18_CHEST_FRONT": (("THORAX_MASS", 0.70), ("CERVICAL_BRIDGE", 0.30)),
    "C19_NECK_VENTRAL_BASE": (("CERVICAL_BRIDGE", 1.00),),
    "C20_THROAT": (("CERVICAL_BRIDGE", 0.50), ("CRANIUM_MASS", 0.50)),
    "C21_JAW_REAR": (("CRANIUM_MASS", 1.00),),
    "C22_MUZZLE_BOTTOM": (("CRANIUM_MASS", 1.00),),
    "C23_NOSE_BOTTOM": (("CRANIUM_MASS", 1.00),),
}


@dataclass(frozen=True)
class FR5ProbeResult:
    control: object
    base: object
    internal_patches: tuple
    integration_signature: str
    patch_self_intersections: int
    patch_outside_vertex_count: int
    max_core_displacement: float
    normalized_max_core_displacement: float
    ear_base_outside_control: int
    ear_base_outside_final: int


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _hash_json(value) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _sub(a: Tuple[float, float], b: Tuple[float, float]) -> Tuple[float, float]:
    return (a[0] - b[0], a[1] - b[1])


def _normalize(vector: Tuple[float, float]) -> Tuple[float, float]:
    length = math.hypot(vector[0], vector[1])
    if length <= 1e-12:
        raise ValueError("degenerate FR5 mass axis")
    return (vector[0] / length, vector[1] / length)


def _dot(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _scaled_perpendicular_target(
    point: Tuple[float, float],
    seed: Tuple[float, float],
    axis: Tuple[float, float],
    scale: float,
) -> Tuple[float, float]:
    axis = _normalize(axis)
    perpendicular = (-axis[1], axis[0])
    relative = _sub(point, seed)
    axial = _dot(relative, axis)
    lateral = _dot(relative, perpendicular)
    return (
        seed[0] + axis[0] * axial + perpendicular[0] * lateral * scale,
        seed[1] + axis[1] * axial + perpendicular[1] * lateral * scale,
    )


def _layer_frames(fixture):
    anchors = fixture.state.anchors
    head = (float(anchors["HEAD_ROOT"].x), float(anchors["HEAD_ROOT"].y))
    fore = (float(anchors["FOREQUARTER_REF"].x), float(anchors["FOREQUARTER_REF"].y))
    body = (float(anchors["BODY_ROOT"].x), float(anchors["BODY_ROOT"].y))
    head_fore_axis = _normalize(_sub(fore, head))
    fore_body_axis = _normalize(_sub(body, fore))
    cervical = ((head[0] + fore[0]) * 0.5, (head[1] + fore[1]) * 0.5)
    return {
        "CRANIUM_MASS": (head, head_fore_axis),
        "CERVICAL_BRIDGE": (cervical, head_fore_axis),
        "THORAX_MASS": (fore, fore_body_axis),
    }


def _layer_scale(layer_id: str, view_weights: Dict[str, float]) -> float:
    scales = VIEW_SCALES[layer_id]
    return sum(float(view_weights.get(view, 0.0)) * scales[view] for view in scales)


def _is_exact_profile(view_weights: Dict[str, float]) -> bool:
    return (
        abs(float(view_weights.get("PROFILE", 0.0)) - 1.0) <= 1e-12
        and abs(float(view_weights.get("THREE_QUARTER", 0.0))) <= 1e-12
        and abs(float(view_weights.get("FRONT", 0.0))) <= 1e-12
    )


def build_integrated_core(fixture, control_core):
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    view_weights = fr3_v5.canonical_view_weights(yaw)
    # PROFILE exactness is a contractual identity rule, not merely a geometric
    # near-equality. Avoid the axis-decompose/recompose round-trip entirely so
    # PROFILE stays byte-for-byte equal to the FR3 V5 control.
    if _is_exact_profile(view_weights):
        return tuple(control_core)
    frames = _layer_frames(fixture)
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
            target = _scaled_perpendicular_target(
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
    }
    return _hash_json(payload)


def _core_displacement(control_core, final_core) -> float:
    if tuple(vertex_id for vertex_id, _, _ in control_core) != tuple(vertex_id for vertex_id, _, _ in final_core):
        raise RuntimeError("FR5 changed CORE vertex identity/order")
    return max(
        math.hypot(float(fx) - float(cx), float(fy) - float(cy))
        for (_, cx, cy), (_, fx, fy) in zip(control_core, final_core)
    )


def ear_base_outside_count(core_vertices, ear_shapes) -> int:
    polygon = tuple((float(x), float(y)) for _, x, y in core_vertices)
    count = 0
    for ear in ear_shapes:
        for point in (ear[0], ear[2]):
            if not fr4_base.point_in_polygon((float(point[0]), float(point[1])), polygon):
                count += 1
    return count


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
    max_displacement = _core_displacement(control.core_vertices, final_core)
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
        ear_base_outside_control=ear_base_outside_count(control.core_vertices, control.ear_shapes),
        ear_base_outside_final=ear_base_outside_count(final_core, final_probe.ear_shapes),
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
