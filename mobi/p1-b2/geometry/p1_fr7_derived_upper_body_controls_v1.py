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
import p1_fr5_core_mass_silhouette_v1 as fr5


PROTOTYPE_VERSION = "P1_FR7_DERIVED_UPPER_BODY_CONTROLS_V1_LOCAL_AXIAL_LATERAL"
CONTROL_IDS = ("CRANIUM_CONTROL", "CERVICAL_CONTROL", "THORAX_CONTROL")
# Retain FR5 region IDs for frozen point-to-region influence compatibility.
LAYER_IDS = fr5.LAYER_IDS
MAX_NORMALIZED_CORE_DISPLACEMENT = fr5.MAX_NORMALIZED_CORE_DISPLACEMENT

# Parameters are (axialScale, lateralScale, axialShiftNorm).
# axialShiftNorm is multiplied by half-size. PROFILE is exact identity and is
# bypassed byte-for-byte. The same table applies to every morphology/case/time/
# size/direction record; only continuous canonical view weights blend it.
VIEW_FRAME_PARAMS: Dict[str, Dict[str, Tuple[float, float, float]]] = {
    "CRANIUM_MASS": {
        "PROFILE": (1.00, 1.00, 0.000),
        "THREE_QUARTER": (1.03, 1.10, -0.012),
        "FRONT": (1.05, 1.18, -0.020),
    },
    "CERVICAL_BRIDGE": {
        "PROFILE": (1.00, 1.00, 0.000),
        "THREE_QUARTER": (1.06, 0.96, 0.006),
        "FRONT": (1.10, 0.92, 0.012),
    },
    "THORAX_MASS": {
        "PROFILE": (1.00, 1.00, 0.000),
        "THREE_QUARTER": (1.02, 1.05, 0.002),
        "FRONT": (1.04, 1.10, 0.004),
    },
}

# Frozen by contract: FR7 tests control-frame freedom, not influence-map search.
INFLUENCE_WEIGHTS = fr5.INFLUENCE_WEIGHTS


@dataclass(frozen=True)
class FR7ProbeResult:
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
    prior_fold_corridor_margin: float


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _hash_json(value) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _sub(a: Tuple[float, float], b: Tuple[float, float]) -> Tuple[float, float]:
    return (a[0] - b[0], a[1] - b[1])


def _normalize(vector: Tuple[float, float]) -> Tuple[float, float]:
    length = math.hypot(vector[0], vector[1])
    if length <= 1e-12:
        raise ValueError("degenerate FR7 presentation-control axis")
    return (vector[0] / length, vector[1] / length)


def _dot(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1]


def _control_frames(fixture):
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


def _frame_params(layer_id: str, view_weights: Dict[str, float]) -> Tuple[float, float, float]:
    table = VIEW_FRAME_PARAMS[layer_id]
    axial_scale = sum(float(view_weights.get(view, 0.0)) * table[view][0] for view in table)
    lateral_scale = sum(float(view_weights.get(view, 0.0)) * table[view][1] for view in table)
    axial_shift_norm = sum(float(view_weights.get(view, 0.0)) * table[view][2] for view in table)
    return axial_scale, lateral_scale, axial_shift_norm


def _is_exact_profile(view_weights: Dict[str, float]) -> bool:
    return (
        abs(float(view_weights.get("PROFILE", 0.0)) - 1.0) <= 1e-12
        and abs(float(view_weights.get("THREE_QUARTER", 0.0))) <= 1e-12
        and abs(float(view_weights.get("FRONT", 0.0))) <= 1e-12
    )


def _local_frame_target(
    point: Tuple[float, float],
    seed: Tuple[float, float],
    axis: Tuple[float, float],
    axial_scale: float,
    lateral_scale: float,
    axial_shift: float,
) -> Tuple[float, float]:
    axis = _normalize(axis)
    perpendicular = (-axis[1], axis[0])
    relative = _sub(point, seed)
    axial = _dot(relative, axis)
    lateral = _dot(relative, perpendicular)
    return (
        seed[0] + axis[0] * (axial * axial_scale + axial_shift) + perpendicular[0] * lateral * lateral_scale,
        seed[1] + axis[1] * (axial * axial_scale + axial_shift) + perpendicular[1] * lateral * lateral_scale,
    )


def build_integrated_core(fixture, control_core):
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    view_weights = fr3_v5.canonical_view_weights(yaw)
    if _is_exact_profile(view_weights):
        return tuple(control_core)
    frames = _control_frames(fixture)
    half_size = float(fixture.size_dp) / 2.0
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
            axial_scale, lateral_scale, axial_shift_norm = _frame_params(layer_id, view_weights)
            target = _local_frame_target(
                base,
                seed,
                axis,
                axial_scale,
                lateral_scale,
                axial_shift_norm * half_size,
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
        "controls": {
            "CRANIUM_CONTROL": {"seed": "HEAD_ROOT", "axis": "HEAD_ROOT_TO_FOREQUARTER_REF"},
            "CERVICAL_CONTROL": {"seed": "MID_HEAD_ROOT_FOREQUARTER_REF", "axis": "HEAD_ROOT_TO_FOREQUARTER_REF"},
            "THORAX_CONTROL": {"seed": "FOREQUARTER_REF", "axis": "FOREQUARTER_REF_TO_BODY_ROOT"},
        },
        "viewFrameParams": VIEW_FRAME_PARAMS,
        "influenceWeights": INFLUENCE_WEIGHTS,
        "transform": "LOCAL_AXIAL_SCALE_PLUS_LATERAL_SCALE_PLUS_AXIAL_SHIFT",
        "rotation": "NONE",
        "profileRule": "EXACT_CONTROL_CORE_BYPASS",
        "externalMeshDomains": ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL"),
        "semanticState": "EXISTING_ANCHORS_DERIVED_READ_ONLY",
    }
    return _hash_json(payload)


def _core_displacement(control_core, final_core) -> float:
    if tuple(vertex_id for vertex_id, _, _ in control_core) != tuple(vertex_id for vertex_id, _, _ in final_core):
        raise RuntimeError("FR7 changed CORE vertex identity/order")
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


def _orientation(a, b, c) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _segments_intersect(a, b, c, d) -> bool:
    o1 = _orientation(a, b, c)
    o2 = _orientation(a, b, d)
    o3 = _orientation(c, d, a)
    o4 = _orientation(c, d, b)
    return ((o1 > 1e-12 and o2 < -1e-12) or (o1 < -1e-12 and o2 > 1e-12)) and (
        (o3 > 1e-12 and o4 < -1e-12) or (o3 < -1e-12 and o4 > 1e-12)
    )


def _point_segment_distance(p, a, b) -> float:
    vx, vy = b[0] - a[0], b[1] - a[1]
    wx, wy = p[0] - a[0], p[1] - a[1]
    denom = vx * vx + vy * vy
    if denom <= 1e-18:
        return math.hypot(wx, wy)
    t = max(0.0, min(1.0, (wx * vx + wy * vy) / denom))
    q = (a[0] + t * vx, a[1] + t * vy)
    return math.hypot(p[0] - q[0], p[1] - q[1])


def prior_fold_corridor_margin(core_vertices) -> float:
    core = {vertex_id: (float(x), float(y)) for vertex_id, x, y in core_vertices}
    a = core["C18_CHEST_FRONT"]
    b = core["C19_NECK_VENTRAL_BASE"]
    c = core["C20_THROAT"]
    d = core["C21_JAW_REAR"]
    if _segments_intersect(a, b, c, d):
        return 0.0
    return min(
        _point_segment_distance(a, c, d),
        _point_segment_distance(b, c, d),
        _point_segment_distance(c, a, b),
        _point_segment_distance(d, a, b),
    )


def build_probe(fixture, direction: int = +1) -> FR7ProbeResult:
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
    return FR7ProbeResult(
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
        prior_fold_corridor_margin=prior_fold_corridor_margin(final_core),
    )


def result_dict(result: FR7ProbeResult) -> dict:
    payload = fr3_v5.result_dict(result.base)
    payload["version"] = PROTOTYPE_VERSION
    payload["integrationSignature"] = result.integration_signature
    payload["patchSelfIntersections"] = result.patch_self_intersections
    payload["patchOutsideVertexCount"] = result.patch_outside_vertex_count
    payload["maxCoreDisplacement"] = result.max_core_displacement
    payload["normalizedMaxCoreDisplacement"] = result.normalized_max_core_displacement
    payload["earBaseOutsideControl"] = result.ear_base_outside_control
    payload["earBaseOutsideFinal"] = result.ear_base_outside_final
    payload["priorFoldCorridorMargin"] = result.prior_fold_corridor_margin
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
