from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Dict, Iterable, Tuple

from e_v0_profiles import morphology_by_id, orientation_by_id
import p1_c_r2_minimal_volumetric_proxy_v1 as r2


PROTOTYPE_VERSION = "P1_C_R4_ANATOMY_AWARE_CONTINUOUS_SURFACE_SHELL_V1"
EXTERNAL_DOMAINS = ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL")
SECTION_FAMILY = "ELLIPTIC_TRANSVERSE_RING_V1"
FRAME_RULE = "NO_TWIST_B3_TRANSVERSE_V1"
SECTION_SAMPLES = 8
COLLAR_SAMPLES = 6
SECTION_IDS = (
    "ROSTRAL_FRONT",
    "CRANIUM_FRONT",
    "CRANIUM_REAR",
    "CERVICAL_INSERTION",
    "SHOULDER_CHEST",
    "THORAX",
    "ABDOMINAL_TUCK",
    "PELVIS",
    "HAUNCH_REAR",
)

# One shared fixed structural table. These values are never selected by
# morphology id, case, time, direction, or named view. Existing anatomical
# radii come from the frozen R2 ratio table; this table only fixes section
# placement/taper and proximal junction proportions needed by the new shell.
SHELL_TABLE = {
    "cranium_front_x_fraction": 0.45,
    "cranium_rear_x_fraction": -0.62,
    "cranium_front_radius_scale": 0.88,
    "cervical_head_to_fore_t": 0.54,
    "shoulder_forward_x_fraction": 0.30,
    "shoulder_radius_scale": 0.90,
    "haunch_rear_x_fraction": -0.55,
    "haunch_radius_scale": 0.78,
    "fore_attachment_lateral_fraction": 0.62,
    "fore_attachment_ventral_fraction": 0.46,
    "hind_attachment_lateral_fraction": 0.66,
    "hind_attachment_ventral_fraction": 0.42,
    "fore_root_radius_scale": 1.45,
    "hind_root_radius_scale": 1.55,
    "proximal_taper": 0.72,
    "mid_blend_to_paw": 0.52,
    "fore_bend_forward": -0.034,
    "hind_bend_forward": 0.046,
    "side_bias": 0.018,
}


@dataclass(frozen=True)
class SectionRing:
    id: str
    center: Tuple[float, float]
    radius_y: float
    radius_z: float
    points: Tuple[Tuple[float, float], ...]


@dataclass(frozen=True)
class ShellResult:
    version: str
    yaw_rad: float
    signature: str
    sections: Tuple[SectionRing, ...]
    core_surface: Tuple[r2.ProjectedPrimitive, ...]
    ears: Tuple[r2.ProjectedPrimitive, ...]
    collars: Tuple[r2.ProjectedPrimitive, ...]
    limbs: Tuple[r2.ProjectedPrimitive, ...]
    paws: Tuple[r2.ProjectedPrimitive, ...]
    tail: r2.ProjectedPrimitive
    domain_bounds: Dict[str, Tuple[float, float, float, float]]
    visual_bounds: Tuple[float, float, float, float]
    paw_pin_error: float


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def shell_signature() -> str:
    payload = {
        "version": PROTOTYPE_VERSION,
        "externalDomains": EXTERNAL_DOMAINS,
        "sectionFamily": SECTION_FAMILY,
        "frameRule": FRAME_RULE,
        "sectionIds": SECTION_IDS,
        "sectionSamples": SECTION_SAMPLES,
        "collarSamples": COLLAR_SAMPLES,
        "r2Ratios": r2.RATIOS,
        "shellTable": SHELL_TABLE,
        "projection": "ORTHOGRAPHIC_BODY_LOCAL_XYZ_CONTINUOUS_YAW",
        "stateOwnership": "EXISTING_CANONICAL_SEMANTICS_READ_ONLY",
        "specialization": "NONE",
        "correctionFamily": "NONE",
    }
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _yaw(fixture) -> float:
    return float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))


def _lerp_point(a, b, t: float) -> Tuple[float, float]:
    return (
        float(a.x) * (1.0 - t) + float(b.x) * t,
        float(a.y) * (1.0 - t) + float(b.y) * t,
    )


def _point_type_like(reference, point: Tuple[float, float]):
    return type(reference)(float(point[0]), float(point[1]))


def _ring_points(center, radius_y: float, radius_z: float, yaw: float, samples: int = SECTION_SAMPLES):
    if samples != SECTION_SAMPLES:
        raise ValueError("section sample count is frozen")
    points = []
    for index in range(samples):
        theta = 2.0 * math.pi * index / samples
        y_up = radius_y * math.sin(theta)
        z_left = radius_z * math.cos(theta)
        points.append(r2._project_offset(center, 0.0, y_up, z_left, yaw))
    return tuple(points)


def _make_ring(id_: str, center, radius_y: float, radius_z: float, yaw: float) -> SectionRing:
    if radius_y <= 0.0 or radius_z <= 0.0:
        raise ValueError((id_, radius_y, radius_z))
    return SectionRing(
        id=id_,
        center=(float(center.x), float(center.y)),
        radius_y=float(radius_y),
        radius_z=float(radius_z),
        points=_ring_points(center, radius_y, radius_z, yaw),
    )


def _section_rings(fixture) -> Tuple[SectionRing, ...]:
    morphology = morphology_by_id(fixture.morphology_id)
    orient = orientation_by_id(fixture.morphology_id)
    anchors = fixture.state.anchors
    size = float(fixture.size_dp)
    yaw = _yaw(fixture)

    head = anchors["HEAD_ROOT"]
    fore = anchors["FOREQUARTER_REF"]
    body = anchors["BODY_ROOT"]
    pelvis = anchors["PELVIS_REF"]

    cr = r2.RATIOS["cranium"]
    ro = r2.RATIOS["rostral"]
    ce = r2.RATIOS["cervical"]
    th = r2.RATIOS["thorax"]
    ab = r2.RATIOS["abdomen"]
    pe = r2.RATIOS["pelvis"]
    table = SHELL_TABLE

    head_scale = morphology.head_scale
    fore_scale = morphology.forequarter_scale
    pelvis_scale = morphology.pelvis_scale

    rostral = r2._project_offset(
        head,
        ro["front_x"] * size * head_scale,
        -ro["ventral_shift"] * size * head_scale,
        0.0,
        yaw,
    )
    cranium_front = r2._project_offset(
        head,
        cr["rx"] * size * head_scale * table["cranium_front_x_fraction"],
        0.0,
        0.0,
        yaw,
    )
    cranium_rear = r2._project_offset(
        head,
        cr["rx"] * size * head_scale * table["cranium_rear_x_fraction"],
        0.0,
        0.0,
        yaw,
    )
    cervical_xy = _lerp_point(head, fore, table["cervical_head_to_fore_t"])
    cervical = _point_type_like(head, cervical_xy)
    shoulder = r2._project_offset(
        fore,
        th["rx"] * size * fore_scale * table["shoulder_forward_x_fraction"],
        0.0,
        0.0,
        yaw,
    )

    abdomen_xy = (
        (float(fore.x) + 2.0 * float(body.x) + float(pelvis.x)) / 4.0,
        (float(fore.y) + 2.0 * float(body.y) + float(pelvis.y)) / 4.0,
    )
    abdomen = _point_type_like(body, abdomen_xy)
    haunch = r2._project_offset(
        pelvis,
        pe["rx"] * size * pelvis_scale * table["haunch_rear_x_fraction"],
        0.0,
        0.0,
        yaw,
    )

    cervical_y = ce["radius_y"] * size * math.sqrt(head_scale * fore_scale)
    cervical_z = ce["radius_z"] * size * math.sqrt(head_scale * orient.thorax_width_scale)
    thorax_y = th["ry"] * size * morphology.trunk_depth * fore_scale
    thorax_z = th["rz"] * size * orient.thorax_width_scale * fore_scale
    abdomen_y = ab["ry"] * size * morphology.trunk_depth
    abdomen_z = ab["rz"] * size * math.sqrt(orient.thorax_width_scale * orient.pelvis_width_scale)
    pelvis_y = pe["ry"] * size * morphology.trunk_depth * pelvis_scale
    pelvis_z = pe["rz"] * size * orient.pelvis_width_scale * pelvis_scale

    return (
        _make_ring(
            "ROSTRAL_FRONT",
            rostral,
            ro["front_half_y"] * size * head_scale,
            ro["front_half_z"] * size * head_scale,
            yaw,
        ),
        _make_ring(
            "CRANIUM_FRONT",
            cranium_front,
            cr["ry"] * size * head_scale * table["cranium_front_radius_scale"],
            cr["rz"] * size * head_scale * table["cranium_front_radius_scale"],
            yaw,
        ),
        _make_ring(
            "CRANIUM_REAR",
            cranium_rear,
            cr["ry"] * size * head_scale,
            cr["rz"] * size * head_scale,
            yaw,
        ),
        _make_ring("CERVICAL_INSERTION", cervical, cervical_y, cervical_z, yaw),
        _make_ring(
            "SHOULDER_CHEST",
            shoulder,
            thorax_y * table["shoulder_radius_scale"],
            thorax_z * table["shoulder_radius_scale"],
            yaw,
        ),
        _make_ring("THORAX", fore, thorax_y, thorax_z, yaw),
        _make_ring("ABDOMINAL_TUCK", abdomen, abdomen_y, abdomen_z, yaw),
        _make_ring("PELVIS", pelvis, pelvis_y, pelvis_z, yaw),
        _make_ring(
            "HAUNCH_REAR",
            haunch,
            pelvis_y * table["haunch_radius_scale"],
            pelvis_z * table["haunch_radius_scale"],
            yaw,
        ),
    )


def _surface_faces(sections: Tuple[SectionRing, ...]) -> Tuple[r2.ProjectedPrimitive, ...]:
    if tuple(section.id for section in sections) != SECTION_IDS:
        raise ValueError("section topology drift")
    faces = []
    for section_index, (front, rear) in enumerate(zip(sections, sections[1:])):
        if len(front.points) != SECTION_SAMPLES or len(rear.points) != SECTION_SAMPLES:
            raise ValueError("section sample topology drift")
        for sample_index in range(SECTION_SAMPLES):
            next_index = (sample_index + 1) % SECTION_SAMPLES
            faces.append(
                r2.ProjectedPrimitive(
                    id=f"CORE_FACE_{section_index:02d}_{sample_index:02d}",
                    kind="LOFT_QUAD",
                    domain="CORE",
                    points=(
                        front.points[sample_index],
                        front.points[next_index],
                        rear.points[next_index],
                        rear.points[sample_index],
                    ),
                )
            )
    faces.append(r2.ProjectedPrimitive("CORE_CAP_FRONT", "SECTION_CAP", "CORE", sections[0].points))
    faces.append(r2.ProjectedPrimitive("CORE_CAP_REAR", "SECTION_CAP", "CORE", sections[-1].points))
    return tuple(faces)


def _collar_ring(center, radius_y: float, radius_z: float, yaw: float):
    points = []
    for index in range(COLLAR_SAMPLES):
        theta = 2.0 * math.pi * index / COLLAR_SAMPLES
        points.append(
            r2._project_offset(
                center,
                0.0,
                radius_y * math.sin(theta),
                radius_z * math.cos(theta),
                yaw,
            )
        )
    return tuple(points)


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


def _build_appendages(fixture, yaw: float):
    morphology = morphology_by_id(fixture.morphology_id)
    orient = orientation_by_id(fixture.morphology_id)
    anchors = fixture.state.anchors
    size = float(fixture.size_dp)
    fore = anchors["FOREQUARTER_REF"]
    pelvis = anchors["PELVIS_REF"]

    collars = []
    limbs = []
    paws = []
    paw_pin_error = 0.0

    for domain, owner, side, center, width_scale, limb_scale, hind in (
        ("FORE_L", "FORE", +1.0, fore, orient.thorax_width_scale, morphology.fore_limb_length, False),
        ("FORE_R", "FORE", -1.0, fore, orient.thorax_width_scale, morphology.fore_limb_length, False),
        ("HIND_L", "HIND", +1.0, pelvis, orient.pelvis_width_scale, morphology.hind_limb_length, True),
        ("HIND_R", "HIND", -1.0, pelvis, orient.pelvis_width_scale, morphology.hind_limb_length, True),
    ):
        paw_id = f"{owner}_PAW_{'L' if side > 0 else 'R'}"
        paw = anchors[paw_id]
        ratio = r2.RATIOS["hind_limb" if hind else "fore_limb"]
        body_radius_y = (
            r2.RATIOS["pelvis"]["ry"] * size * morphology.trunk_depth * morphology.pelvis_scale
            if hind
            else r2.RATIOS["thorax"]["ry"] * size * morphology.trunk_depth * morphology.forequarter_scale
        )
        body_radius_z = (
            r2.RATIOS["pelvis"]["rz"] * size * orient.pelvis_width_scale * morphology.pelvis_scale
            if hind
            else r2.RATIOS["thorax"]["rz"] * size * orient.thorax_width_scale * morphology.forequarter_scale
        )
        lateral_fraction = SHELL_TABLE["hind_attachment_lateral_fraction" if hind else "fore_attachment_lateral_fraction"]
        ventral_fraction = SHELL_TABLE["hind_attachment_ventral_fraction" if hind else "fore_attachment_ventral_fraction"]
        attachment = r2._side_attachment(
            center,
            side * body_radius_z * lateral_fraction,
            body_radius_y * ventral_fraction,
            yaw,
        )

        px, py = float(paw.x), float(paw.y)
        ax, ay = attachment
        bend_forward = size * limb_scale * SHELL_TABLE["hind_bend_forward" if hind else "fore_bend_forward"]
        side_bias = side * size * SHELL_TABLE["side_bias"]
        mid = (
            ax * (1.0 - SHELL_TABLE["mid_blend_to_paw"]) + px * SHELL_TABLE["mid_blend_to_paw"]
            + bend_forward * math.cos(yaw)
            + side_bias * math.sin(yaw),
            ay * (1.0 - SHELL_TABLE["mid_blend_to_paw"]) + py * SHELL_TABLE["mid_blend_to_paw"],
        )

        base_radius = size * ratio["radius"]
        root_radius = base_radius * SHELL_TABLE["hind_root_radius_scale" if hind else "fore_root_radius_scale"]
        collar_points = _collar_ring(attachment, root_radius, root_radius, yaw)
        collars.append(r2.ProjectedPrimitive(f"{domain}_COLLAR", "PROXIMAL_COLLAR", domain, collar_points))

        proximal = _tapered_segment(attachment, mid, root_radius, base_radius)
        distal_radius = base_radius * SHELL_TABLE["proximal_taper"]
        distal = r2._capsule(mid, (px, py), distal_radius)
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

    return tuple(collars), tuple(limbs), tuple(paws), paw_pin_error


def _tail(fixture, yaw: float):
    morphology = morphology_by_id(fixture.morphology_id)
    size = float(fixture.size_dp)
    root = fixture.state.anchors["TAIL_ROOT"]
    tail_points = r2._tail_points(root, size, morphology.tail_length, yaw)
    tail_radius = size * r2.RATIOS["tail"]["radius"] * morphology.tail_thickness
    tail_cloud = []
    for a, b in zip(tail_points, tail_points[1:]):
        tail_cloud.extend(r2._capsule(a, b, tail_radius))
    return r2.ProjectedPrimitive("TAIL_CHANNEL", "CURVED_CAPSULE_CHAIN", "TAIL", r2._convex_hull(tail_cloud))


def build_shell(fixture) -> ShellResult:
    morphology = morphology_by_id(fixture.morphology_id)
    anchors = fixture.state.anchors
    size = float(fixture.size_dp)
    yaw = _yaw(fixture)

    sections = _section_rings(fixture)
    core_surface = _surface_faces(sections)
    head = anchors["HEAD_ROOT"]
    ears = tuple(
        r2.ProjectedPrimitive(
            f"EAR_{'L' if side > 0 else 'R'}",
            "TRIANGULAR_EAR",
            "CORE",
            r2._ear(head, side, size, morphology.head_scale, morphology.ear_scale, yaw),
        )
        for side in (+1.0, -1.0)
    )
    collars, limbs, paws, paw_pin_error = _build_appendages(fixture, yaw)
    tail = _tail(fixture, yaw)

    by_domain = {domain: [] for domain in EXTERNAL_DOMAINS}
    for primitive in core_surface + ears + collars + limbs + paws + (tail,):
        by_domain[primitive.domain].extend(primitive.points)
    domain_bounds = {domain: r2._bounds(points) for domain, points in by_domain.items()}
    visual_bounds = r2._union_bounds(domain_bounds.values())

    return ShellResult(
        version=PROTOTYPE_VERSION,
        yaw_rad=yaw,
        signature=shell_signature(),
        sections=sections,
        core_surface=core_surface,
        ears=ears,
        collars=collars,
        limbs=limbs,
        paws=paws,
        tail=tail,
        domain_bounds=domain_bounds,
        visual_bounds=visual_bounds,
        paw_pin_error=paw_pin_error,
    )


def all_primitives(result: ShellResult, include_ears: bool = True):
    return result.core_surface + (result.ears if include_ears else ()) + result.collars + result.limbs + result.paws + (result.tail,)


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
        "sectionFamily": SECTION_FAMILY,
        "frameRule": FRAME_RULE,
        "sectionIds": list(SECTION_IDS),
        "sectionCount": len(result.sections),
        "sectionSamples": SECTION_SAMPLES,
        "collarSamples": COLLAR_SAMPLES,
        "externalDomains": list(EXTERNAL_DOMAINS),
        "externalDomainCount": len(EXTERNAL_DOMAINS),
        "pawPinError": result.paw_pin_error,
        "finite": finite,
        "correctionUseCount": 0,
        "domainBounds": {key: list(value) for key, value in sorted(result.domain_bounds.items())},
        "visualBounds": list(result.visual_bounds),
    }