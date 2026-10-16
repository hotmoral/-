from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Dict, Iterable, Tuple

from e_v0_profiles import morphology_by_id, orientation_by_id
import p1_c_r2_minimal_volumetric_proxy_v1 as r2


PROTOTYPE_VERSION = "P1_C_R5_BOUNDED_EXPLICIT_ANATOMICAL_CONTROL_SHELL_V1"
EXTERNAL_DOMAINS = ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL")
PERIMETER_IDS = ("DORSAL", "UPPER_L", "LOWER_L", "VENTRAL", "LOWER_R", "UPPER_R")
ROW_IDS = (
    "ROSTRUM",
    "CRANIUM_CHEEK",
    "CRANIAL_BASE",
    "NECK_INSERTION",
    "SHOULDER_CHEST",
    "THORAX_REAR",
    "ABDOMINAL_TUCK",
    "PELVIS_HAUNCH",
    "HAUNCH_REAR",
)
CORE_CONTROL_COUNT = len(ROW_IDS) * len(PERIMETER_IDS)
JUNCTION_CONTROLS_PER_LIMB = 4
JUNCTION_CONTROL_COUNT = 4 * JUNCTION_CONTROLS_PER_LIMB
AUTHORITATIVE_CONTROL_COUNT = CORE_CONTROL_COUNT + JUNCTION_CONTROL_COUNT
CORE_FACE_COUNT = (len(ROW_IDS) - 1) * len(PERIMETER_IDS) + 2
AUTHORITATIVE_FACE_COUNT = CORE_FACE_COUNT + 4

if CORE_CONTROL_COUNT > 72:
    raise RuntimeError("CORE control ceiling exceeded")
if JUNCTION_CONTROL_COUNT > 24 or JUNCTION_CONTROLS_PER_LIMB > 6:
    raise RuntimeError("junction control ceiling exceeded")
if AUTHORITATIVE_CONTROL_COUNT > 96:
    raise RuntimeError("authoritative control ceiling exceeded")
if AUTHORITATIVE_FACE_COUNT > 128:
    raise RuntimeError("authoritative face ceiling exceeded")

# Explicit neutral intrinsic cage. Every perimeter control is authored directly
# in body-local XYZ normalized to size_dp. Values are not generated from an
# ellipse/superellipse/ring equation and are never selected by view, case,
# direction, pose, time, or morphology id.
#
# +X forward, +Y dorsal/up, +Z anatomical left.
CORE_TEMPLATE = {
    "ROSTRUM": (
        (+0.105, +0.035, +0.000),
        (+0.110, +0.022, +0.045),
        (+0.120, -0.020, +0.040),
        (+0.095, -0.055, +0.000),
        (+0.120, -0.020, -0.040),
        (+0.110, +0.022, -0.045),
    ),
    "CRANIUM_CHEEK": (
        (+0.005, +0.108, +0.000),
        (+0.035, +0.070, +0.108),
        (+0.055, -0.020, +0.098),
        (+0.025, -0.078, +0.000),
        (+0.055, -0.020, -0.098),
        (+0.035, +0.070, -0.108),
    ),
    "CRANIAL_BASE": (
        (-0.080, +0.082, +0.000),
        (-0.070, +0.050, +0.090),
        (-0.040, -0.030, +0.072),
        (-0.015, -0.062, +0.000),
        (-0.040, -0.030, -0.072),
        (-0.070, +0.050, -0.090),
    ),
    "NECK_INSERTION": (
        (+0.018, +0.060, +0.000),
        (+0.025, +0.038, +0.057),
        (+0.030, -0.025, +0.050),
        (+0.035, -0.058, +0.000),
        (+0.030, -0.025, -0.050),
        (+0.025, +0.038, -0.057),
    ),
    "SHOULDER_CHEST": (
        (+0.065, +0.138, +0.000),
        (+0.050, +0.082, +0.123),
        (+0.040, -0.060, +0.108),
        (+0.078, -0.145, +0.000),
        (+0.040, -0.060, -0.108),
        (+0.050, +0.082, -0.123),
    ),
    "THORAX_REAR": (
        (+0.025, +0.122, +0.000),
        (+0.012, +0.072, +0.142),
        (-0.005, -0.070, +0.120),
        (+0.018, -0.120, +0.000),
        (-0.005, -0.070, -0.120),
        (+0.012, +0.072, -0.142),
    ),
    "ABDOMINAL_TUCK": (
        (+0.010, +0.090, +0.000),
        (+0.000, +0.052, +0.102),
        (-0.010, -0.008, +0.078),
        (+0.020, -0.052, +0.000),
        (-0.010, -0.008, -0.078),
        (+0.000, +0.052, -0.102),
    ),
    "PELVIS_HAUNCH": (
        (+0.025, +0.118, +0.000),
        (+0.000, +0.076, +0.132),
        (-0.018, -0.060, +0.126),
        (-0.008, -0.108, +0.000),
        (-0.018, -0.060, -0.126),
        (+0.000, +0.076, -0.132),
    ),
    "HAUNCH_REAR": (
        (-0.110, +0.092, +0.000),
        (-0.122, +0.055, +0.116),
        (-0.102, -0.065, +0.108),
        (-0.072, -0.092, +0.000),
        (-0.102, -0.065, -0.108),
        (-0.122, +0.055, -0.116),
    ),
}

# Four explicit intrinsic root controls per limb. These form one broad proximal
# fan at the shoulder/haunch before the generated distal limb reaches the
# canonical paw endpoint. Z is authored for anatomical left and mirrored only
# by anatomical side identity, not by screen/view logic.
FORE_ROOT_TEMPLATE = (
    (+0.070, -0.025, +0.100),
    (-0.025, -0.048, +0.112),
    (-0.020, -0.145, +0.064),
    (+0.055, -0.152, +0.058),
)
HIND_ROOT_TEMPLATE = (
    (+0.035, -0.015, +0.112),
    (-0.090, +0.005, +0.124),
    (-0.082, -0.135, +0.070),
    (+0.010, -0.142, +0.066),
)

# These are one global neutral structural mapping, not case tables.
ROW_ORIGIN_RULES = {
    "ROSTRUM": ("HEAD_ROOT", 0.0),
    "CRANIUM_CHEEK": ("HEAD_ROOT", 0.0),
    "CRANIAL_BASE": ("HEAD_ROOT", 0.0),
    "NECK_INSERTION": ("HEAD_FORE", 0.58),
    "SHOULDER_CHEST": ("FOREQUARTER_REF", 0.0),
    "THORAX_REAR": ("BODY_ROOT", 0.0),
    "ABDOMINAL_TUCK": ("BODY_PELVIS", 0.44),
    "PELVIS_HAUNCH": ("PELVIS_REF", 0.0),
    "HAUNCH_REAR": ("PELVIS_REF", 0.0),
}


@dataclass(frozen=True)
class ProjectedControl:
    id: str
    row_id: str
    perimeter_id: str
    intrinsic_xyz: Tuple[float, float, float]
    point: Tuple[float, float]


@dataclass(frozen=True)
class ShellResult:
    version: str
    yaw_rad: float
    signature: str
    controls: Tuple[ProjectedControl, ...]
    junction_controls: Tuple[ProjectedControl, ...]
    core_faces: Tuple[r2.ProjectedPrimitive, ...]
    ears: Tuple[r2.ProjectedPrimitive, ...]
    root_faces: Tuple[r2.ProjectedPrimitive, ...]
    limbs: Tuple[r2.ProjectedPrimitive, ...]
    paws: Tuple[r2.ProjectedPrimitive, ...]
    tail: r2.ProjectedPrimitive
    domain_bounds: Dict[str, Tuple[float, float, float, float]]
    visual_bounds: Tuple[float, float, float, float]
    paw_pin_error: float


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _face_topology():
    faces = []
    for row_index in range(len(ROW_IDS) - 1):
        for perimeter_index in range(len(PERIMETER_IDS)):
            nxt = (perimeter_index + 1) % len(PERIMETER_IDS)
            faces.append((
                (row_index, perimeter_index),
                (row_index, nxt),
                (row_index + 1, nxt),
                (row_index + 1, perimeter_index),
            ))
    faces.append(tuple((0, index) for index in range(len(PERIMETER_IDS))))
    last = len(ROW_IDS) - 1
    faces.append(tuple((last, index) for index in reversed(range(len(PERIMETER_IDS)))))
    return tuple(faces)


FACE_TOPOLOGY = _face_topology()


def shell_signature() -> str:
    payload = {
        "version": PROTOTYPE_VERSION,
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
        "projection": "ORTHOGRAPHIC_BODY_LOCAL_XYZ_CONTINUOUS_YAW",
        "stateOwnership": "EXISTING_CANONICAL_SEMANTICS_READ_ONLY",
        "specialization": "NONE",
        "correctionFamily": "NONE",
        "derivedSubdivisionSteps": 0,
    }
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _yaw(fixture) -> float:
    return float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))


def _point_type_like(reference, x: float, y: float):
    return type(reference)(float(x), float(y))


def _lerp_anchor(a, b, t: float):
    return _point_type_like(a, float(a.x) * (1.0 - t) + float(b.x) * t, float(a.y) * (1.0 - t) + float(b.y) * t)


def _origin_for_row(fixture, row_id: str):
    anchors = fixture.state.anchors
    rule, t = ROW_ORIGIN_RULES[row_id]
    if rule == "HEAD_FORE":
        return _lerp_anchor(anchors["HEAD_ROOT"], anchors["FOREQUARTER_REF"], t)
    if rule == "BODY_PELVIS":
        return _lerp_anchor(anchors["BODY_ROOT"], anchors["PELVIS_REF"], t)
    return anchors[rule]


def _axis_scales(fixture, row_id: str):
    morphology = morphology_by_id(fixture.morphology_id)
    orient = orientation_by_id(fixture.morphology_id)
    if row_id in ("ROSTRUM", "CRANIUM_CHEEK", "CRANIAL_BASE"):
        return morphology.head_scale, morphology.head_scale, morphology.head_scale
    if row_id == "NECK_INSERTION":
        blend = math.sqrt(morphology.head_scale * morphology.forequarter_scale)
        width = math.sqrt(morphology.head_scale * orient.thorax_width_scale)
        return blend, blend, width
    if row_id == "SHOULDER_CHEST":
        return morphology.forequarter_scale, morphology.trunk_depth * morphology.forequarter_scale, orient.thorax_width_scale * morphology.forequarter_scale
    if row_id == "THORAX_REAR":
        return morphology.trunk_length, morphology.trunk_depth, orient.thorax_width_scale
    if row_id == "ABDOMINAL_TUCK":
        width = math.sqrt(orient.thorax_width_scale * orient.pelvis_width_scale)
        return morphology.trunk_length, morphology.trunk_depth, width
    return morphology.pelvis_scale, morphology.trunk_depth * morphology.pelvis_scale, orient.pelvis_width_scale * morphology.pelvis_scale


def _project_intrinsic(origin, xyz, size: float, yaw: float, scales=(1.0, 1.0, 1.0)):
    sx, sy, sz = scales
    return r2._project_offset(origin, xyz[0] * size * sx, xyz[1] * size * sy, xyz[2] * size * sz, yaw)


def _build_core_controls(fixture):
    size = float(fixture.size_dp)
    yaw = _yaw(fixture)
    controls = []
    for row_id in ROW_IDS:
        origin = _origin_for_row(fixture, row_id)
        scales = _axis_scales(fixture, row_id)
        template = CORE_TEMPLATE[row_id]
        if len(template) != len(PERIMETER_IDS):
            raise ValueError("explicit control topology drift")
        for perimeter_id, xyz in zip(PERIMETER_IDS, template):
            point = _project_intrinsic(origin, xyz, size, yaw, scales)
            controls.append(ProjectedControl(
                id=f"CORE_{row_id}_{perimeter_id}",
                row_id=row_id,
                perimeter_id=perimeter_id,
                intrinsic_xyz=tuple(float(v) for v in xyz),
                point=(float(point[0]), float(point[1])),
            ))
    if len(controls) != CORE_CONTROL_COUNT:
        raise ValueError("CORE control count drift")
    return tuple(controls)


def _core_control_map(controls):
    return {(control.row_id, control.perimeter_id): control for control in controls}


def _build_core_faces(controls):
    cmap = _core_control_map(controls)
    faces = []
    for face_index, refs in enumerate(FACE_TOPOLOGY):
        points = tuple(cmap[(ROW_IDS[row_index], PERIMETER_IDS[perimeter_index])].point for row_index, perimeter_index in refs)
        faces.append(r2.ProjectedPrimitive(
            id=f"CORE_FACE_{face_index:03d}",
            kind="EXPLICIT_CONTROL_FACE",
            domain="CORE",
            points=points,
        ))
    if len(faces) != CORE_FACE_COUNT:
        raise ValueError("CORE face count drift")
    return tuple(faces)


def _root_scales(fixture, hind: bool):
    morphology = morphology_by_id(fixture.morphology_id)
    orient = orientation_by_id(fixture.morphology_id)
    if hind:
        return morphology.pelvis_scale, morphology.trunk_depth * morphology.pelvis_scale, orient.pelvis_width_scale * morphology.pelvis_scale
    return morphology.forequarter_scale, morphology.trunk_depth * morphology.forequarter_scale, orient.thorax_width_scale * morphology.forequarter_scale


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
            point = _project_intrinsic(origin, sided_xyz, size, yaw, scales)
            control = ProjectedControl(
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


def _tapered_segment(a, b, radius_a: float, radius_b: float):
    ax, ay = float(a[0]), float(a[1])
    bx, by = float(b[0]), float(b[1])
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    if length <= 1e-12:
        return r2._capsule(a, b, max(radius_a, radius_b))
    nx, ny = -dy / length, dx / length
    return (
        (ax + nx * radius_a, ay + ny * radius_a),
        (ax - nx * radius_a, ay - ny * radius_a),
        (bx - nx * radius_b, by - ny * radius_b),
        (bx + nx * radius_b, by + ny * radius_b),
    )


def _build_appendages(fixture, root_groups):
    morphology = morphology_by_id(fixture.morphology_id)
    anchors = fixture.state.anchors
    size = float(fixture.size_dp)
    root_faces = []
    limbs = []
    paws = []
    paw_pin_error = 0.0

    for domain, hind, group in root_groups:
        root_faces.append(r2.ProjectedPrimitive(
            id=f"{domain}_ROOT_FACE",
            kind="EXPLICIT_PROXIMAL_ROOT_FACE",
            domain=domain,
            points=tuple(control.point for control in group),
        ))
        owner = "HIND" if hind else "FORE"
        side_letter = "L" if domain.endswith("_L") else "R"
        paw = anchors[f"{owner}_PAW_{side_letter}"]
        px, py = float(paw.x), float(paw.y)
        lower_a = group[2].point
        lower_b = group[3].point
        start = ((lower_a[0] + lower_b[0]) * 0.5, (lower_a[1] + lower_b[1]) * 0.5)
        limb_scale = morphology.hind_limb_length if hind else morphology.fore_limb_length
        ratio = r2.RATIOS["hind_limb" if hind else "fore_limb"]
        base_radius = size * ratio["radius"]
        dx = px - start[0]
        dy = py - start[1]
        mid = (
            start[0] + dx * 0.47 + (0.028 if hind else -0.020) * size * limb_scale,
            start[1] + dy * 0.48,
        )
        proximal = _tapered_segment(start, mid, base_radius * 1.22, base_radius)
        distal = r2._capsule(mid, (px, py), base_radius * 0.82)
        limbs.append(r2.ProjectedPrimitive(f"{domain}_PROXIMAL", "TAPERED_LIMB", domain, proximal))
        limbs.append(r2.ProjectedPrimitive(f"{domain}_DISTAL", "CAPSULE", domain, distal))

        paw_points = r2._ellipse_at(
            paw,
            ratio["paw_rx"] * size * morphology.paw_scale,
            ratio["paw_ry"] * size * morphology.paw_scale,
        )
        paws.append(r2.ProjectedPrimitive(f"{domain}_PAW", "PAW_ELLIPSE", domain, paw_points))
        center_x = sum(point[0] for point in paw_points) / len(paw_points)
        center_y = sum(point[1] for point in paw_points) / len(paw_points)
        paw_pin_error = max(paw_pin_error, math.hypot(center_x - px, center_y - py))

    return tuple(root_faces), tuple(limbs), tuple(paws), paw_pin_error


def _ears(fixture, yaw: float):
    morphology = morphology_by_id(fixture.morphology_id)
    head = fixture.state.anchors["HEAD_ROOT"]
    size = float(fixture.size_dp)
    return tuple(
        r2.ProjectedPrimitive(
            f"EAR_{'L' if side > 0 else 'R'}",
            "TRIANGULAR_EAR",
            "CORE",
            r2._ear(head, side, size, morphology.head_scale, morphology.ear_scale, yaw),
        )
        for side in (+1.0, -1.0)
    )


def _tail(fixture, yaw: float):
    morphology = morphology_by_id(fixture.morphology_id)
    size = float(fixture.size_dp)
    root = fixture.state.anchors["TAIL_ROOT"]
    tail_points = r2._tail_points(root, size, morphology.tail_length, yaw)
    tail_radius = size * r2.RATIOS["tail"]["radius"] * morphology.tail_thickness
    cloud = []
    for a, b in zip(tail_points, tail_points[1:]):
        cloud.extend(r2._capsule(a, b, tail_radius))
    return r2.ProjectedPrimitive("TAIL_CHANNEL", "CURVED_CAPSULE_CHAIN", "TAIL", r2._convex_hull(cloud))


def build_shell(fixture) -> ShellResult:
    yaw = _yaw(fixture)
    controls = _build_core_controls(fixture)
    core_faces = _build_core_faces(controls)
    junction_controls, root_groups = _build_root_controls(fixture)
    root_faces, limbs, paws, paw_pin_error = _build_appendages(fixture, root_groups)
    ears = _ears(fixture, yaw)
    tail = _tail(fixture, yaw)

    by_domain = {domain: [] for domain in EXTERNAL_DOMAINS}
    primitives = core_faces + ears + root_faces + limbs + paws + (tail,)
    for primitive in primitives:
        by_domain[primitive.domain].extend(primitive.points)
    domain_bounds = {domain: r2._bounds(points) for domain, points in by_domain.items()}
    visual_bounds = r2._union_bounds(domain_bounds.values())

    return ShellResult(
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


def all_primitives(result: ShellResult, include_ears: bool = True):
    return result.core_faces + (result.ears if include_ears else ()) + result.root_faces + result.limbs + result.paws + (result.tail,)


def all_points(result: ShellResult, include_ears: bool = True):
    return tuple(point for primitive in all_primitives(result, include_ears=include_ears) for point in primitive.points)


def result_dict(fixture, result: ShellResult) -> dict:
    finite = all(math.isfinite(value) for point in all_points(result) for value in point)
    return {
        "version": result.version,
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
        "derivedSubdivisionSteps": 0,
        "externalDomains": list(EXTERNAL_DOMAINS),
        "externalDomainCount": len(EXTERNAL_DOMAINS),
        "pawPinError": result.paw_pin_error,
        "finite": finite,
        "correctionUseCount": 0,
        "domainBounds": {key: list(value) for key, value in sorted(result.domain_bounds.items())},
        "visualBounds": list(result.visual_bounds),
    }
