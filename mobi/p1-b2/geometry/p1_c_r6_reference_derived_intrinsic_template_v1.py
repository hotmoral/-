from __future__ import annotations

import hashlib
import json
import math

from e_v0_profiles import morphology_by_id
import p1_c_r2_minimal_volumetric_proxy_v1 as r2
import p1_c_r5_bounded_explicit_anatomical_control_shell_v1 as r5


PROTOTYPE_VERSION = "P1_C_R6_REFERENCE_DERIVED_INTRINSIC_TEMPLATE_V1"
SOURCE_FAMILY = "RF_H_BOUNDED_REFERENCE_DERIVED_INTRINSIC_ANATOMICAL_TEMPLATE"
SOURCE_PACK_ID = "R6_CONSTRUCTION_PACK_V1"
EXTERNAL_DOMAINS = r5.EXTERNAL_DOMAINS
PERIMETER_IDS = r5.PERIMETER_IDS
ROW_IDS = r5.ROW_IDS
CORE_CONTROL_COUNT = r5.CORE_CONTROL_COUNT
JUNCTION_CONTROLS_PER_LIMB = r5.JUNCTION_CONTROLS_PER_LIMB
JUNCTION_CONTROL_COUNT = r5.JUNCTION_CONTROL_COUNT
AUTHORITATIVE_CONTROL_COUNT = r5.AUTHORITATIVE_CONTROL_COUNT
CORE_FACE_COUNT = r5.CORE_FACE_COUNT
AUTHORITATIVE_FACE_COUNT = r5.AUTHORITATIVE_FACE_COUNT
FACE_TOPOLOGY = r5.FACE_TOPOLOGY
DERIVED_SUBDIVISION_STEPS = 0

# Frozen before Stage 2 evaluation in
# P1_C_R6_STAGE1_TEMPLATE_DERIVATION_AND_FREEZE_RECORD.md.
# +X forward, +Y dorsal/up, +Z anatomical left.
CORE_TEMPLATE = {
    "ROSTRUM": (
        (+0.108, +0.030, +0.000),
        (+0.112, +0.016, +0.038),
        (+0.116, -0.018, +0.036),
        (+0.094, -0.046, +0.000),
        (+0.116, -0.018, -0.036),
        (+0.112, +0.016, -0.038),
    ),
    "CRANIUM_CHEEK": (
        (+0.000, +0.100, +0.000),
        (+0.020, +0.064, +0.103),
        (+0.042, -0.018, +0.094),
        (+0.018, -0.066, +0.000),
        (+0.042, -0.018, -0.094),
        (+0.020, +0.064, -0.103),
    ),
    "CRANIAL_BASE": (
        (-0.074, +0.078, +0.000),
        (-0.066, +0.048, +0.082),
        (-0.040, -0.020, +0.064),
        (-0.024, -0.050, +0.000),
        (-0.040, -0.020, -0.064),
        (-0.066, +0.048, -0.082),
    ),
    "NECK_INSERTION": (
        (-0.008, +0.056, +0.000),
        (+0.004, +0.036, +0.054),
        (+0.018, -0.018, +0.048),
        (+0.028, -0.048, +0.000),
        (+0.018, -0.018, -0.048),
        (+0.004, +0.036, -0.054),
    ),
    "SHOULDER_CHEST": (
        (+0.042, +0.126, +0.000),
        (+0.030, +0.078, +0.128),
        (+0.034, -0.056, +0.112),
        (+0.062, -0.136, +0.000),
        (+0.034, -0.056, -0.112),
        (+0.030, +0.078, -0.128),
    ),
    "THORAX_REAR": (
        (-0.006, +0.112, +0.000),
        (-0.018, +0.066, +0.136),
        (-0.024, -0.058, +0.116),
        (-0.004, -0.104, +0.000),
        (-0.024, -0.058, -0.116),
        (-0.018, +0.066, -0.136),
    ),
    "ABDOMINAL_TUCK": (
        (-0.006, +0.078, +0.000),
        (-0.016, +0.046, +0.090),
        (-0.016, -0.004, +0.070),
        (+0.010, -0.030, +0.000),
        (-0.016, -0.004, -0.070),
        (-0.016, +0.046, -0.090),
    ),
    "PELVIS_HAUNCH": (
        (+0.010, +0.116, +0.000),
        (-0.006, +0.072, +0.126),
        (-0.020, -0.052, +0.118),
        (-0.008, -0.092, +0.000),
        (-0.020, -0.052, -0.118),
        (-0.006, +0.072, -0.126),
    ),
    "HAUNCH_REAR": (
        (-0.104, +0.094, +0.000),
        (-0.114, +0.052, +0.108),
        (-0.100, -0.056, +0.100),
        (-0.070, -0.074, +0.000),
        (-0.100, -0.056, -0.100),
        (-0.114, +0.052, -0.108),
    ),
}

FORE_ROOT_TEMPLATE = (
    (+0.050, +0.020, +0.108),
    (-0.045, +0.004, +0.116),
    (-0.032, -0.124, +0.060),
    (+0.044, -0.136, +0.054),
)

HIND_ROOT_TEMPLATE = (
    (+0.028, +0.035, +0.108),
    (-0.090, +0.028, +0.120),
    (-0.080, -0.118, +0.070),
    (+0.012, -0.126, +0.062),
)

ROW_ORIGIN_RULES = {
    "ROSTRUM": ("HEAD_ROOT", 0.0),
    "CRANIUM_CHEEK": ("HEAD_ROOT", 0.0),
    "CRANIAL_BASE": ("HEAD_ROOT", 0.0),
    "NECK_INSERTION": ("HEAD_FORE", 0.50),
    "SHOULDER_CHEST": ("FOREQUARTER_REF", 0.0),
    "THORAX_REAR": ("BODY_ROOT", 0.0),
    "ABDOMINAL_TUCK": ("BODY_PELVIS", 0.42),
    "PELVIS_HAUNCH": ("PELVIS_REF", 0.0),
    "HAUNCH_REAR": ("PELVIS_REF", 0.0),
}

SOURCE_IDS = (
    "R6-S1-INNERSCENE-WALKING-CAT-CC0",
    "R6-S2-WILLIAMS-1875-ATLAS-PD",
    "R6-S3-REIGHARD-JENNINGS-1901-PD",
    "R6-S4-EDINBURGH-CT-CAT-CCBY4",
    "R6-S5-HOLDING-1903-SUPERFICIAL-MUSCLES-PD",
)


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def shell_signature() -> str:
    payload = {
        "version": PROTOTYPE_VERSION,
        "sourceFamily": SOURCE_FAMILY,
        "sourcePackId": SOURCE_PACK_ID,
        "sourceIds": SOURCE_IDS,
        "externalDomains": EXTERNAL_DOMAINS,
        "rowIds": ROW_IDS,
        "perimeterIds": PERIMETER_IDS,
        "coreTemplate": CORE_TEMPLATE,
        "rowOrigins": ROW_ORIGIN_RULES,
        "foreRootTemplate": FORE_ROOT_TEMPLATE,
        "hindRootTemplate": HIND_ROOT_TEMPLATE,
        "faceTopology": FACE_TOPOLOGY,
        "authoritativeControlCount": AUTHORITATIVE_CONTROL_COUNT,
        "authoritativeFaceCount": AUTHORITATIVE_FACE_COUNT,
        "derivedSubdivisionSteps": DERIVED_SUBDIVISION_STEPS,
        "projection": "ORTHOGRAPHIC_BODY_LOCAL_XYZ_CONTINUOUS_YAW",
        "stateOwnership": "EXISTING_CANONICAL_SEMANTICS_READ_ONLY",
        "specialization": "NONE",
        "correctionFamily": "NONE",
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


def _origin_for_row(fixture, row_id: str):
    anchors = fixture.state.anchors
    rule, t = ROW_ORIGIN_RULES[row_id]
    if rule == "HEAD_FORE":
        return _lerp_anchor(anchors["HEAD_ROOT"], anchors["FOREQUARTER_REF"], t)
    if rule == "BODY_PELVIS":
        return _lerp_anchor(anchors["BODY_ROOT"], anchors["PELVIS_REF"], t)
    return anchors[rule]


def _build_core_controls(fixture):
    size = float(fixture.size_dp)
    yaw = _yaw(fixture)
    controls = []
    for row_id in ROW_IDS:
        origin = _origin_for_row(fixture, row_id)
        scales = r5._axis_scales(fixture, row_id)
        template = CORE_TEMPLATE[row_id]
        if len(template) != len(PERIMETER_IDS):
            raise ValueError("reference-derived control topology drift")
        for perimeter_id, xyz in zip(PERIMETER_IDS, template):
            point = r5._project_intrinsic(origin, xyz, size, yaw, scales)
            controls.append(r5.ProjectedControl(
                id=f"CORE_{row_id}_{perimeter_id}",
                row_id=row_id,
                perimeter_id=perimeter_id,
                intrinsic_xyz=tuple(float(v) for v in xyz),
                point=(float(point[0]), float(point[1])),
            ))
    if len(controls) != CORE_CONTROL_COUNT:
        raise ValueError("CORE control count drift")
    return tuple(controls)


def _root_scales(fixture, hind: bool):
    return r5._root_scales(fixture, hind)


def _build_root_controls(fixture):
    anchors = fixture.state.anchors
    size = float(fixture.size_dp)
    yaw = _yaw(fixture)
    controls = []
    root_groups = []
    for domain, owner_key, side, hind in (
        ("FORE_L", "FOREQUARTER_REF", +1.0, False),
        ("FORE_R", "FOREQUARTER_REF", -1.0, False),
        ("HIND_L", "PELVIS_REF", +1.0, True),
        ("HIND_R", "PELVIS_REF", -1.0, True),
    ):
        origin = anchors[owner_key]
        scales = _root_scales(fixture, hind)
        template = HIND_ROOT_TEMPLATE if hind else FORE_ROOT_TEMPLATE
        group = []
        for index, xyz in enumerate(template):
            sided_xyz = (xyz[0], xyz[1], xyz[2] * side)
            point = r5._project_intrinsic(origin, sided_xyz, size, yaw, scales)
            control = r5.ProjectedControl(
                id=f"{domain}_ROOT_{index}",
                row_id=domain,
                perimeter_id=f"ROOT_{index}",
                intrinsic_xyz=tuple(float(v) for v in sided_xyz),
                point=(float(point[0]), float(point[1])),
            )
            controls.append(control)
            group.append(control)
        root_groups.append((domain, hind, tuple(group)))
    if len(controls) != JUNCTION_CONTROL_COUNT:
        raise ValueError("junction control count drift")
    return tuple(controls), tuple(root_groups)


def build_shell(fixture) -> r5.ShellResult:
    yaw = _yaw(fixture)
    controls = _build_core_controls(fixture)
    core_faces = r5._build_core_faces(controls)
    junction_controls, root_groups = _build_root_controls(fixture)
    root_faces, limbs, paws, paw_pin_error = r5._build_appendages(fixture, root_groups)
    ears = r5._ears(fixture, yaw)
    tail = r5._tail(fixture, yaw)

    by_domain = {domain: [] for domain in EXTERNAL_DOMAINS}
    primitives = core_faces + ears + root_faces + limbs + paws + (tail,)
    for primitive in primitives:
        by_domain[primitive.domain].extend(primitive.points)
    domain_bounds = {domain: r2._bounds(points) for domain, points in by_domain.items()}
    visual_bounds = r2._union_bounds(domain_bounds.values())

    return r5.ShellResult(
        version=PROTOTYPE_VERSION,
        yaw_rad=yaw,
        signature=shell_signature(),
        controls=controls,
        junction_controls=junction_controls,
        core_faces=core_faces,
        ears=ears,
        root_faces=root_faces,
        limbs=limbs,
        paws=paws,
        tail=tail,
        domain_bounds=domain_bounds,
        visual_bounds=visual_bounds,
        paw_pin_error=paw_pin_error,
    )


def all_primitives(result, include_ears: bool = True):
    return result.core_faces + (result.ears if include_ears else ()) + result.root_faces + result.limbs + result.paws + (result.tail,)


def all_points(result, include_ears: bool = True):
    return tuple(point for primitive in all_primitives(result, include_ears=include_ears) for point in primitive.points)


def result_dict(fixture, result) -> dict:
    finite = all(math.isfinite(value) for point in all_points(result) for value in point)
    return {
        "version": result.version,
        "sourceFamily": SOURCE_FAMILY,
        "sourcePackId": SOURCE_PACK_ID,
        "sourceIds": list(SOURCE_IDS),
        "caseId": fixture.case_id,
        "morphologyId": fixture.morphology_id,
        "sizeDp": int(fixture.size_dp),
        "t": float(fixture.t),
        "semanticHash": fixture.semantic_hash,
        "yawRad": result.yaw_rad,
        "shellSignature": result.signature,
        "rowIds": list(ROW_IDS),
        "perimeterIds": list(PERIMETER_IDS),
        "coreControlCount": CORE_CONTROL_COUNT,
        "junctionControlCount": JUNCTION_CONTROL_COUNT,
        "authoritativeControlCount": AUTHORITATIVE_CONTROL_COUNT,
        "authoritativeFaceCount": AUTHORITATIVE_FACE_COUNT,
        "derivedSubdivisionSteps": DERIVED_SUBDIVISION_STEPS,
        "externalDomains": list(EXTERNAL_DOMAINS),
        "externalDomainCount": len(EXTERNAL_DOMAINS),
        "pawPinError": result.paw_pin_error,
        "finite": finite,
        "correctionUseCount": 0,
        "domainBounds": {key: list(value) for key, value in sorted(result.domain_bounds.items())},
        "visualBounds": list(result.visual_bounds),
    }
