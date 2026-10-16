from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Dict, Tuple

from e_v0_profiles import morphology_by_id, orientation_by_id
import p1_c_r2_minimal_volumetric_proxy_v1 as r2
import p1_c_r5_bounded_explicit_anatomical_control_shell_v1 as r5
import p1_c_r7_anatomy_flow_topology_v1 as topo


PROTOTYPE_VERSION = "P1_C_R7_ANATOMY_FLOW_CONTROL_SURFACE_V1"
SOURCE_FAMILY = "RF_I_BOUNDED_ANATOMY_FLOW_CONTROL_SURFACE"
SOURCE_PACK_ID = "R6_CONSTRUCTION_PACK_V1"
EXTERNAL_DOMAINS = topo.EXTERNAL_DOMAINS
AUTHORITATIVE_CONTROL_COUNT = len(topo.VERTEX_IDS)
AUTHORITATIVE_FACE_COUNT = len(topo.FACES)
DERIVED_SUBDIVISION_STEPS = topo.DERIVED_SUBDIVISION_STEPS
CORRECTION_USE_COUNT = 0
ORIGIN_RULE_VERSION = "R7_ORIGIN_GROUPS_V1"
SCALING_RULE_VERSION = "R7_REGION_SCALING_V1"

DORSAL_COORDS = {
    "D_MUZZLE": (+0.108, +0.032, +0.000),
    "D_CRANIUM": (+0.000, +0.100, +0.000),
    "D_CRANIAL_BASE": (-0.074, +0.078, +0.000),
    "D_CERVICAL": (-0.010, +0.060, +0.000),
    "D_SHOULDER": (+0.018, +0.130, +0.000),
    "D_THORAX": (-0.005, +0.115, +0.000),
    "D_LUMBAR": (-0.010, +0.088, +0.000),
    "D_PELVIS": (+0.008, +0.118, +0.000),
    "D_RUMP": (-0.108, +0.094, +0.000),
}

LEFT_DORSOLATERAL_COORDS = {
    "LU_MUZZLE": (+0.112, +0.016, +0.038),
    "LU_CHEEK": (+0.018, +0.066, +0.103),
    "LU_CRANIAL_BASE": (-0.064, +0.050, +0.082),
    "LU_CERVICAL": (+0.002, +0.038, +0.055),
    "LU_SHOULDER": (+0.020, +0.082, +0.128),
    "LU_THORAX": (-0.012, +0.070, +0.138),
    "LU_FLANK": (-0.018, +0.052, +0.104),
    "LU_PELVIS": (-0.004, +0.076, +0.130),
    "LU_HAUNCH": (-0.116, +0.054, +0.112),
}

LEFT_VENTROLATERAL_COORDS = {
    "LL_MUZZLE": (+0.116, -0.018, +0.036),
    "LL_CHEEK": (+0.040, -0.020, +0.095),
    "LL_CRANIAL_BASE": (-0.038, -0.018, +0.064),
    "LL_CERVICAL": (+0.016, -0.016, +0.048),
    "LL_CHEST": (+0.032, -0.058, +0.112),
    "LL_THORAX": (-0.020, -0.062, +0.118),
    "LL_ABDOMEN": (-0.020, -0.018, +0.080),
    "LL_TUCK": (-0.014, -0.006, +0.072),
    "LL_PELVIS": (-0.018, -0.052, +0.120),
    "LL_HAUNCH": (-0.102, -0.054, +0.104),
}

VENTRAL_COORDS = {
    "V_MUZZLE": (+0.094, -0.048, +0.000),
    "V_JAW": (+0.014, -0.070, +0.000),
    "V_THROAT": (+0.024, -0.050, +0.000),
    "V_STERNUM": (+0.052, -0.140, +0.000),
    "V_ABDOMEN": (-0.006, -0.104, +0.000),
    "V_TUCK": (+0.008, -0.034, +0.000),
    "V_PELVIS": (-0.006, -0.098, +0.000),
    "V_RUMP": (-0.072, -0.078, +0.000),
}

LEFT_PROXIMAL_COORDS = {
    "FORE_L_PROX_CRANIAL": (+0.030, -0.152, +0.066),
    "FORE_L_PROX_CAUDAL": (-0.036, -0.146, +0.074),
    "HIND_L_PROX_CRANIAL": (+0.012, -0.142, +0.072),
    "HIND_L_PROX_CAUDAL": (-0.068, -0.132, +0.080),
}


def _mirror_side_key(key: str) -> str:
    if key.startswith("LU_"):
        return key.replace("LU_", "RU_", 1)
    if key.startswith("LL_"):
        return key.replace("LL_", "RL_", 1)
    if key.startswith("FORE_L_"):
        return key.replace("FORE_L_", "FORE_R_", 1)
    if key.startswith("HIND_L_"):
        return key.replace("HIND_L_", "HIND_R_", 1)
    raise KeyError(key)


def _mirrored(mapping):
    return {
        _mirror_side_key(key): (float(x), float(y), -float(z))
        for key, (x, y, z) in mapping.items()
    }


COORDINATES = {
    **DORSAL_COORDS,
    **LEFT_DORSOLATERAL_COORDS,
    **LEFT_VENTROLATERAL_COORDS,
    **VENTRAL_COORDS,
    **LEFT_PROXIMAL_COORDS,
    **_mirrored(LEFT_DORSOLATERAL_COORDS),
    **_mirrored(LEFT_VENTROLATERAL_COORDS),
    **_mirrored(LEFT_PROXIMAL_COORDS),
}

HEAD_GROUP = frozenset({
    "D_MUZZLE", "D_CRANIUM", "D_CRANIAL_BASE",
    "LU_MUZZLE", "LU_CHEEK", "LU_CRANIAL_BASE",
    "LL_MUZZLE", "LL_CHEEK", "LL_CRANIAL_BASE",
    "RU_MUZZLE", "RU_CHEEK", "RU_CRANIAL_BASE",
    "RL_MUZZLE", "RL_CHEEK", "RL_CRANIAL_BASE",
    "V_MUZZLE", "V_JAW",
})
CERVICAL_GROUP = frozenset({
    "D_CERVICAL", "LU_CERVICAL", "LL_CERVICAL", "RU_CERVICAL", "RL_CERVICAL", "V_THROAT",
})
FORE_GROUP = frozenset({
    "D_SHOULDER", "LU_SHOULDER", "LL_CHEST", "RU_SHOULDER", "RL_CHEST", "V_STERNUM",
    "FORE_L_PROX_CRANIAL", "FORE_L_PROX_CAUDAL", "FORE_R_PROX_CRANIAL", "FORE_R_PROX_CAUDAL",
})
THORAX_GROUP = frozenset({
    "D_THORAX", "LU_THORAX", "LL_THORAX", "RU_THORAX", "RL_THORAX", "V_ABDOMEN",
})
MIDBODY_GROUP = frozenset({
    "D_LUMBAR", "LU_FLANK", "LL_ABDOMEN", "LL_TUCK",
    "RU_FLANK", "RL_ABDOMEN", "RL_TUCK", "V_TUCK",
})
PELVIS_GROUP = frozenset({
    "D_PELVIS", "D_RUMP", "LU_PELVIS", "LU_HAUNCH", "LL_PELVIS", "LL_HAUNCH",
    "RU_PELVIS", "RU_HAUNCH", "RL_PELVIS", "RL_HAUNCH", "V_PELVIS", "V_RUMP",
    "HIND_L_PROX_CRANIAL", "HIND_L_PROX_CAUDAL", "HIND_R_PROX_CRANIAL", "HIND_R_PROX_CAUDAL",
})

ORIGIN_GROUPS = {
    "HEAD_ROOT": tuple(sorted(HEAD_GROUP)),
    "HEAD_FORE_050": tuple(sorted(CERVICAL_GROUP)),
    "FOREQUARTER_REF": tuple(sorted(FORE_GROUP)),
    "BODY_ROOT": tuple(sorted(THORAX_GROUP)),
    "BODY_PELVIS_042": tuple(sorted(MIDBODY_GROUP)),
    "PELVIS_REF": tuple(sorted(PELVIS_GROUP)),
}

if set(COORDINATES) != set(topo.VERTEX_IDS):
    missing = sorted(set(topo.VERTEX_IDS) - set(COORDINATES))
    extra = sorted(set(COORDINATES) - set(topo.VERTEX_IDS))
    raise RuntimeError(("coordinate/topology vertex mismatch", missing, extra))
if set().union(HEAD_GROUP, CERVICAL_GROUP, FORE_GROUP, THORAX_GROUP, MIDBODY_GROUP, PELVIS_GROUP) != set(topo.VERTEX_IDS):
    raise RuntimeError("origin groups do not cover topology")


@dataclass(frozen=True)
class FlowControl:
    id: str
    intrinsic_xyz: Tuple[float, float, float]
    point: Tuple[float, float]


@dataclass(frozen=True)
class FlowSurfaceResult:
    version: str
    yaw_rad: float
    signature: str
    controls: Tuple[FlowControl, ...]
    faces: Tuple[r2.ProjectedPrimitive, ...]
    ears: Tuple[r2.ProjectedPrimitive, ...]
    limbs: Tuple[r2.ProjectedPrimitive, ...]
    paws: Tuple[r2.ProjectedPrimitive, ...]
    tail: r2.ProjectedPrimitive
    domain_bounds: Dict[str, Tuple[float, float, float, float]]
    visual_bounds: Tuple[float, float, float, float]
    paw_pin_error: float


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def surface_signature() -> str:
    payload = {
        "version": PROTOTYPE_VERSION,
        "sourceFamily": SOURCE_FAMILY,
        "sourcePackId": SOURCE_PACK_ID,
        "topologyVersion": topo.TOPOLOGY_VERSION,
        "topologySignature": topo.topology_signature(),
        "coordinates": {key: list(value) for key, value in sorted(COORDINATES.items())},
        "originGroups": ORIGIN_GROUPS,
        "originRuleVersion": ORIGIN_RULE_VERSION,
        "scalingRuleVersion": SCALING_RULE_VERSION,
        "projection": "ORTHOGRAPHIC_BODY_LOCAL_XYZ_CONTINUOUS_YAW",
        "stateOwnership": "EXISTING_CANONICAL_SEMANTICS_READ_ONLY",
        "correctionFamily": "NONE",
        "derivedSubdivisionSteps": DERIVED_SUBDIVISION_STEPS,
    }
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _yaw(fixture) -> float:
    return float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))


def _point_type_like(reference, x: float, y: float):
    return type(reference)(float(x), float(y))


def _lerp_anchor(a, b, t: float):
    return _point_type_like(
        a,
        float(a.x) * (1.0 - t) + float(b.x) * t,
        float(a.y) * (1.0 - t) + float(b.y) * t,
    )


def _origin_for_vertex(fixture, vertex_id: str):
    anchors = fixture.state.anchors
    if vertex_id in HEAD_GROUP:
        return anchors["HEAD_ROOT"]
    if vertex_id in CERVICAL_GROUP:
        return _lerp_anchor(anchors["HEAD_ROOT"], anchors["FOREQUARTER_REF"], 0.50)
    if vertex_id in FORE_GROUP:
        return anchors["FOREQUARTER_REF"]
    if vertex_id in THORAX_GROUP:
        return anchors["BODY_ROOT"]
    if vertex_id in MIDBODY_GROUP:
        return _lerp_anchor(anchors["BODY_ROOT"], anchors["PELVIS_REF"], 0.42)
    if vertex_id in PELVIS_GROUP:
        return anchors["PELVIS_REF"]
    raise KeyError(vertex_id)


def _scales_for_vertex(fixture, vertex_id: str):
    morphology = morphology_by_id(fixture.morphology_id)
    orient = orientation_by_id(fixture.morphology_id)
    if vertex_id in HEAD_GROUP:
        return morphology.head_scale, morphology.head_scale, morphology.head_scale
    if vertex_id in CERVICAL_GROUP:
        blend = math.sqrt(morphology.head_scale * morphology.forequarter_scale)
        width = math.sqrt(morphology.head_scale * orient.thorax_width_scale)
        return blend, blend, width
    if vertex_id in FORE_GROUP:
        return (
            morphology.forequarter_scale,
            morphology.trunk_depth * morphology.forequarter_scale,
            orient.thorax_width_scale * morphology.forequarter_scale,
        )
    if vertex_id in THORAX_GROUP:
        return morphology.trunk_length, morphology.trunk_depth, orient.thorax_width_scale
    if vertex_id in MIDBODY_GROUP:
        width = math.sqrt(orient.thorax_width_scale * orient.pelvis_width_scale)
        return morphology.trunk_length, morphology.trunk_depth, width
    if vertex_id in PELVIS_GROUP:
        return (
            morphology.pelvis_scale,
            morphology.trunk_depth * morphology.pelvis_scale,
            orient.pelvis_width_scale * morphology.pelvis_scale,
        )
    raise KeyError(vertex_id)


def _project_control(fixture, vertex_id: str) -> FlowControl:
    origin = _origin_for_vertex(fixture, vertex_id)
    xyz = COORDINATES[vertex_id]
    sx, sy, sz = _scales_for_vertex(fixture, vertex_id)
    size = float(fixture.size_dp)
    point = r2._project_offset(
        origin,
        xyz[0] * size * sx,
        xyz[1] * size * sy,
        xyz[2] * size * sz,
        _yaw(fixture),
    )
    return FlowControl(
        id=vertex_id,
        intrinsic_xyz=tuple(float(value) for value in xyz),
        point=(float(point[0]), float(point[1])),
    )


def _build_controls(fixture):
    controls = tuple(_project_control(fixture, vertex_id) for vertex_id in topo.VERTEX_IDS)
    if len(controls) != AUTHORITATIVE_CONTROL_COUNT:
        raise ValueError("authoritative control count drift")
    return controls


def _control_map(controls):
    return {control.id: control for control in controls}


def _build_faces(controls):
    cmap = _control_map(controls)
    faces = []
    for index, (domain, vertex_ids) in enumerate(topo.FACES):
        faces.append(r2.ProjectedPrimitive(
            id=f"FLOW_FACE_{index:03d}",
            kind="ANATOMY_FLOW_CONTROL_FACE",
            domain=domain,
            points=tuple(cmap[vertex_id].point for vertex_id in vertex_ids),
        ))
    if len(faces) != AUTHORITATIVE_FACE_COUNT:
        raise ValueError("authoritative face count drift")
    return tuple(faces)


def _build_distal_limbs_and_paws(fixture, controls):
    cmap = _control_map(controls)
    morphology = morphology_by_id(fixture.morphology_id)
    anchors = fixture.state.anchors
    size = float(fixture.size_dp)
    limbs = []
    paws = []
    paw_pin_error = 0.0

    for domain, hind in (("FORE_L", False), ("FORE_R", False), ("HIND_L", True), ("HIND_R", True)):
        a = cmap[f"{domain}_PROX_CRANIAL"].point
        b = cmap[f"{domain}_PROX_CAUDAL"].point
        start = ((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5)
        owner = "HIND" if hind else "FORE"
        side_letter = "L" if domain.endswith("_L") else "R"
        paw = anchors[f"{owner}_PAW_{side_letter}"]
        px, py = float(paw.x), float(paw.y)
        limb_scale = morphology.hind_limb_length if hind else morphology.fore_limb_length
        ratio = r2.RATIOS["hind_limb" if hind else "fore_limb"]
        base_radius = size * ratio["radius"]
        dx = px - start[0]
        dy = py - start[1]
        mid = (
            start[0] + dx * 0.47 + (0.026 if hind else -0.018) * size * limb_scale,
            start[1] + dy * 0.48,
        )
        limbs.append(r2.ProjectedPrimitive(
            f"{domain}_DISTAL_PROXIMAL",
            "TAPERED_LIMB_CONTINUATION",
            domain,
            r5._tapered_segment(start, mid, base_radius * 1.18, base_radius),
        ))
        limbs.append(r2.ProjectedPrimitive(
            f"{domain}_DISTAL",
            "CAPSULE",
            domain,
            r2._capsule(mid, (px, py), base_radius * 0.82),
        ))
        paw_points = r2._ellipse_at(
            paw,
            ratio["paw_rx"] * size * morphology.paw_scale,
            ratio["paw_ry"] * size * morphology.paw_scale,
        )
        paws.append(r2.ProjectedPrimitive(f"{domain}_PAW", "PAW_ELLIPSE", domain, paw_points))
        center_x = sum(point[0] for point in paw_points) / len(paw_points)
        center_y = sum(point[1] for point in paw_points) / len(paw_points)
        paw_pin_error = max(paw_pin_error, math.hypot(center_x - px, center_y - py))

    return tuple(limbs), tuple(paws), paw_pin_error


def build_surface(fixture) -> FlowSurfaceResult:
    topo.validate_topology()
    controls = _build_controls(fixture)
    faces = _build_faces(controls)
    yaw = _yaw(fixture)
    ears = r5._ears(fixture, yaw)
    limbs, paws, paw_pin_error = _build_distal_limbs_and_paws(fixture, controls)
    tail = r5._tail(fixture, yaw)

    by_domain = {domain: [] for domain in EXTERNAL_DOMAINS}
    primitives = faces + ears + limbs + paws + (tail,)
    for primitive in primitives:
        by_domain[primitive.domain].extend(primitive.points)
    if any(not points for points in by_domain.values()):
        raise ValueError("empty external domain")
    domain_bounds = {domain: r2._bounds(points) for domain, points in by_domain.items()}
    visual_bounds = r2._union_bounds(domain_bounds.values())

    return FlowSurfaceResult(
        version=PROTOTYPE_VERSION,
        yaw_rad=yaw,
        signature=surface_signature(),
        controls=controls,
        faces=faces,
        ears=ears,
        limbs=limbs,
        paws=paws,
        tail=tail,
        domain_bounds=domain_bounds,
        visual_bounds=visual_bounds,
        paw_pin_error=paw_pin_error,
    )


def all_primitives(result: FlowSurfaceResult, include_ears: bool = True):
    return result.faces + (result.ears if include_ears else ()) + result.limbs + result.paws + (result.tail,)


def all_points(result: FlowSurfaceResult, include_ears: bool = True):
    return tuple(point for primitive in all_primitives(result, include_ears=include_ears) for point in primitive.points)


def result_dict(fixture, result: FlowSurfaceResult) -> dict:
    finite = all(math.isfinite(value) for point in all_points(result) for value in point)
    return {
        "version": result.version,
        "sourceFamily": SOURCE_FAMILY,
        "sourcePackId": SOURCE_PACK_ID,
        "topologyVersion": topo.TOPOLOGY_VERSION,
        "topologySignature": topo.topology_signature(),
        "surfaceSignature": result.signature,
        "caseId": fixture.case_id,
        "morphologyId": fixture.morphology_id,
        "sizeDp": int(fixture.size_dp),
        "t": float(fixture.t),
        "semanticHash": fixture.semantic_hash,
        "yawRad": result.yaw_rad,
        "authoritativeControlCount": AUTHORITATIVE_CONTROL_COUNT,
        "authoritativeFaceCount": AUTHORITATIVE_FACE_COUNT,
        "topologyEdgeCount": len(topo.edge_set()),
        "derivedSubdivisionSteps": DERIVED_SUBDIVISION_STEPS,
        "externalDomains": list(EXTERNAL_DOMAINS),
        "externalDomainCount": len(EXTERNAL_DOMAINS),
        "pawPinError": result.paw_pin_error,
        "finite": finite,
        "correctionUseCount": CORRECTION_USE_COUNT,
        "domainBounds": {key: list(value) for key, value in sorted(result.domain_bounds.items())},
        "visualBounds": list(result.visual_bounds),
    }
