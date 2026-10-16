from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Dict, Iterable, Tuple

from e_v0_profiles import morphology_by_id, orientation_by_id


PROTOTYPE_VERSION = "P1_C_R2_MINIMAL_VOLUMETRIC_FELINE_PROXY_V1"
EXTERNAL_DOMAINS = ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL")
CORE_VOLUME_IDS = (
    "CRANIUM_VOLUME",
    "ROSTRAL_WEDGE",
    "CERVICAL_VOLUME",
    "THORAX_VOLUME",
    "ABDOMEN_BRIDGE_VOLUME",
    "PELVIS_HAUNCH_VOLUME",
)

# One shared ratio table. Values are normalized against 80 dp and are never
# selected by morphology, case, time, direction, or named view.
RATIOS = {
    "cranium": {"rx": 0.1125, "ry": 0.1050, "rz": 0.1125},
    "rostral": {
        "back_x": 0.0150,
        "front_x": 0.1050,
        "back_half_y": 0.0470,
        "front_half_y": 0.0300,
        "back_half_z": 0.0670,
        "front_half_z": 0.0430,
        "ventral_shift": 0.0220,
    },
    "cervical": {"radius_y": 0.0600, "radius_z": 0.0640},
    "thorax": {"rx": 0.1800, "ry": 0.1780, "rz": 0.1450},
    "abdomen": {"ry": 0.1180, "rz": 0.1020},
    "pelvis": {"rx": 0.1550, "ry": 0.1500, "rz": 0.1320},
    "fore_limb": {"radius": 0.0260, "paw_rx": 0.0430, "paw_ry": 0.0240},
    "hind_limb": {"radius": 0.0300, "paw_rx": 0.0470, "paw_ry": 0.0260},
    "ear": {
        "base_y": 0.0740,
        "apex_y": 0.1760,
        "base_half_x": 0.0340,
        "side_z": 0.0670,
        "base_half_z": 0.0320,
    },
    "tail": {"radius": 0.0210, "lift": 0.0550, "lateral": 0.0450},
}


@dataclass(frozen=True)
class ProjectedPrimitive:
    id: str
    kind: str
    domain: str
    points: Tuple[Tuple[float, float], ...]


@dataclass(frozen=True)
class ProxyResult:
    version: str
    yaw_rad: float
    signature: str
    core_primitives: Tuple[ProjectedPrimitive, ...]
    ears: Tuple[ProjectedPrimitive, ...]
    limbs: Tuple[ProjectedPrimitive, ...]
    paws: Tuple[ProjectedPrimitive, ...]
    tail: ProjectedPrimitive
    domain_bounds: Dict[str, Tuple[float, float, float, float]]
    visual_bounds: Tuple[float, float, float, float]
    paw_pin_error: float


def _canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def proxy_signature() -> str:
    payload = {
        "version": PROTOTYPE_VERSION,
        "coreVolumeIds": CORE_VOLUME_IDS,
        "externalDomains": EXTERNAL_DOMAINS,
        "ratios": RATIOS,
        "projection": "ORTHOGRAPHIC_BODY_LOCAL_XYZ_CONTINUOUS_YAW",
        "stateOwnership": "EXISTING_CANONICAL_SEMANTICS_READ_ONLY",
        "specialization": "NONE",
        "h4Correction": "NONE",
    }
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _yaw(fixture) -> float:
    return float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))


def _project_offset(origin, x: float, y: float, z: float, yaw: float) -> Tuple[float, float]:
    # Existing P1 body-local convention: +X forward, +Y dorsal/up,
    # +Z anatomical left. Screen Y grows downward.
    screen_x = x * math.cos(yaw) + z * math.sin(yaw)
    return (float(origin.x) + screen_x, float(origin.y) - y)


def _ellipse(center, rx: float, ry: float, rz: float, yaw: float, samples: int = 28):
    # Orthographic projection of an axis-aligned ellipsoid is an ellipse.
    screen_rx = math.sqrt((rx * math.cos(yaw)) ** 2 + (rz * math.sin(yaw)) ** 2)
    return tuple(
        (
            float(center.x) + screen_rx * math.cos(2.0 * math.pi * i / samples),
            float(center.y) + ry * math.sin(2.0 * math.pi * i / samples),
        )
        for i in range(samples)
    )


def _convex_hull(points: Iterable[Tuple[float, float]]):
    pts = sorted(set((float(x), float(y)) for x, y in points))
    if len(pts) <= 2:
        return tuple(pts)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for point in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 1e-12:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 1e-12:
            upper.pop()
        upper.append(point)
    return tuple(lower[:-1] + upper[:-1])


def _wedge(head, size: float, head_scale: float, yaw: float):
    r = RATIOS["rostral"]
    scale = size * head_scale
    points = []
    for x, half_y, half_z in (
        (r["back_x"] * scale, r["back_half_y"] * scale, r["back_half_z"] * scale),
        (r["front_x"] * scale, r["front_half_y"] * scale, r["front_half_z"] * scale),
    ):
        for y_sign in (-1.0, 1.0):
            for z_sign in (-1.0, 1.0):
                # negative local Y shifts the muzzle ventrally.
                y = y_sign * half_y - r["ventral_shift"] * scale
                points.append(_project_offset(head, x, y, z_sign * half_z, yaw))
    return _convex_hull(points)


def _capsule(a, b, radius: float, samples: int = 9):
    ax, ay = float(a[0]), float(a[1])
    bx, by = float(b[0]), float(b[1])
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    if length <= 1e-12:
        return tuple(
            (ax + radius * math.cos(2.0 * math.pi * i / (samples * 2)),
             ay + radius * math.sin(2.0 * math.pi * i / (samples * 2)))
            for i in range(samples * 2)
        )
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux
    points = []
    for i in range(samples + 1):
        theta = math.pi / 2.0 + math.pi * i / samples
        points.append((ax + radius * (math.cos(theta) * ux + math.sin(theta) * nx),
                       ay + radius * (math.cos(theta) * uy + math.sin(theta) * ny)))
    for i in range(samples + 1):
        theta = -math.pi / 2.0 + math.pi * i / samples
        points.append((bx + radius * (math.cos(theta) * ux + math.sin(theta) * nx),
                       by + radius * (math.cos(theta) * uy + math.sin(theta) * ny)))
    return _convex_hull(points)


def _bridge_ellipse(a, b, radius_y: float, radius_z: float, yaw: float):
    # The bridge is a projected capsule between already-projected semantic
    # centers. Width includes the genuine lateral radius contribution.
    lateral = abs(radius_z * math.sin(yaw))
    radius = max(radius_y * 0.62, lateral)
    return _capsule((a.x, a.y), (b.x, b.y), radius)


def _bounds(points: Iterable[Tuple[float, float]]):
    pts = tuple(points)
    if not pts:
        raise ValueError("points required")
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def _union_bounds(rects):
    rects = tuple(rects)
    if not rects:
        raise ValueError("rects required")
    return (
        min(r[0] for r in rects),
        min(r[1] for r in rects),
        max(r[2] for r in rects),
        max(r[3] for r in rects),
    )


def _ellipse_at(point, rx: float, ry: float, samples: int = 20):
    return tuple(
        (float(point.x) + rx * math.cos(2.0 * math.pi * i / samples),
         float(point.y) + ry * math.sin(2.0 * math.pi * i / samples))
        for i in range(samples)
    )


def _ear(head, side: float, size: float, head_scale: float, ear_scale: float, yaw: float):
    r = RATIOS["ear"]
    base_y = r["base_y"] * size * head_scale
    apex_y = r["apex_y"] * size * head_scale * ear_scale
    base_half_x = r["base_half_x"] * size * head_scale
    side_z = side * r["side_z"] * size * head_scale
    base_half_z = r["base_half_z"] * size * head_scale
    p0 = _project_offset(head, -base_half_x, base_y, side_z - base_half_z, yaw)
    p1 = _project_offset(head, 0.0, apex_y, side_z, yaw)
    p2 = _project_offset(head, base_half_x, base_y, side_z + base_half_z, yaw)
    return (p0, p1, p2)


def _side_attachment(center, local_z: float, ventral: float, yaw: float):
    return _project_offset(center, 0.0, -ventral, local_z, yaw)


def _limb_chain(attachment, paw, bend_forward: float, side_bias: float, yaw: float):
    ax, ay = attachment
    px, py = float(paw.x), float(paw.y)
    mid = (
        ax * 0.48 + px * 0.52 + bend_forward * math.cos(yaw) + side_bias * math.sin(yaw),
        ay * 0.48 + py * 0.52,
    )
    return attachment, mid, (px, py)


def _limb_polygon(chain, radius: float):
    a, mid, b = chain
    first = _capsule(a, mid, radius)
    second = _capsule(mid, b, radius * 0.86)
    # Keeping two sub-capsules as one convex visual envelope would erase the
    # digitigrade bend, so return a deterministic concatenated boundary cloud
    # and let SVG render the two segment primitives separately via helper data.
    return first, second


def _tail_points(root, size: float, tail_length_scale: float, yaw: float):
    length = 0.31 * size * tail_length_scale
    lift = RATIOS["tail"]["lift"] * size
    lateral = RATIOS["tail"]["lateral"] * size
    p0 = (float(root.x), float(root.y))
    p1 = _project_offset(root, -0.48 * length, 0.35 * lift, 0.35 * lateral, yaw)
    p2 = _project_offset(root, -0.86 * length, 0.70 * lift, 0.82 * lateral, yaw)
    p3 = _project_offset(root, -1.00 * length, 1.00 * lift, 1.00 * lateral, yaw)
    return p0, p1, p2, p3


def build_proxy(fixture) -> ProxyResult:
    morphology = morphology_by_id(fixture.morphology_id)
    orient = orientation_by_id(fixture.morphology_id)
    anchors = fixture.state.anchors
    size = float(fixture.size_dp)
    yaw = _yaw(fixture)

    head = anchors["HEAD_ROOT"]
    fore = anchors["FOREQUARTER_REF"]
    pelvis = anchors["PELVIS_REF"]
    body = anchors["BODY_ROOT"]
    tail_root = anchors["TAIL_ROOT"]

    cr = RATIOS["cranium"]
    cranium = ProjectedPrimitive(
        "CRANIUM_VOLUME", "ELLIPSOID", "CORE",
        _ellipse(
            head,
            cr["rx"] * size * morphology.head_scale,
            cr["ry"] * size * morphology.head_scale,
            cr["rz"] * size * morphology.head_scale,
            yaw,
        ),
    )
    rostral = ProjectedPrimitive(
        "ROSTRAL_WEDGE", "CAPPED_WEDGE", "CORE",
        _wedge(head, size, morphology.head_scale, yaw),
    )

    ce = RATIOS["cervical"]
    cervical = ProjectedPrimitive(
        "CERVICAL_VOLUME", "CAPSULE_VOLUME", "CORE",
        _bridge_ellipse(
            head, fore,
            ce["radius_y"] * size * math.sqrt(morphology.head_scale * morphology.forequarter_scale),
            ce["radius_z"] * size * math.sqrt(morphology.head_scale * orient.thorax_width_scale),
            yaw,
        ),
    )

    th = RATIOS["thorax"]
    thorax = ProjectedPrimitive(
        "THORAX_VOLUME", "ELLIPSOID", "CORE",
        _ellipse(
            fore,
            th["rx"] * size * morphology.forequarter_scale,
            th["ry"] * size * morphology.trunk_depth * morphology.forequarter_scale,
            th["rz"] * size * orient.thorax_width_scale * morphology.forequarter_scale,
            yaw,
        ),
    )

    abdomen_center = type(body)(
        (float(fore.x) + 2.0 * float(body.x) + float(pelvis.x)) / 4.0,
        (float(fore.y) + 2.0 * float(body.y) + float(pelvis.y)) / 4.0,
    )
    ab = RATIOS["abdomen"]
    abdomen_length = max(0.08 * size, 0.46 * math.hypot(float(pelvis.x) - float(fore.x), float(pelvis.y) - float(fore.y)))
    abdomen = ProjectedPrimitive(
        "ABDOMEN_BRIDGE_VOLUME", "ELLIPSOID", "CORE",
        _ellipse(
            abdomen_center,
            abdomen_length * morphology.trunk_length,
            ab["ry"] * size * morphology.trunk_depth,
            ab["rz"] * size * math.sqrt(orient.thorax_width_scale * orient.pelvis_width_scale),
            yaw,
        ),
    )

    pe = RATIOS["pelvis"]
    pelvis_volume = ProjectedPrimitive(
        "PELVIS_HAUNCH_VOLUME", "ELLIPSOID", "CORE",
        _ellipse(
            pelvis,
            pe["rx"] * size * morphology.pelvis_scale,
            pe["ry"] * size * morphology.trunk_depth * morphology.pelvis_scale,
            pe["rz"] * size * orient.pelvis_width_scale * morphology.pelvis_scale,
            yaw,
        ),
    )
    core_primitives = (cranium, rostral, cervical, thorax, abdomen, pelvis_volume)

    ears = tuple(
        ProjectedPrimitive(
            f"EAR_{'L' if side > 0 else 'R'}", "TRIANGULAR_EAR", "CORE",
            _ear(head, side, size, morphology.head_scale, morphology.ear_scale, yaw),
        )
        for side in (+1.0, -1.0)
    )

    limbs = []
    paws = []
    paw_pin_error = 0.0
    for domain, owner, side, center, width_scale, limb_scale, paw_scale, hind in (
        ("FORE_L", "FORE", +1.0, fore, orient.thorax_width_scale, morphology.fore_limb_length, morphology.paw_scale, False),
        ("FORE_R", "FORE", -1.0, fore, orient.thorax_width_scale, morphology.fore_limb_length, morphology.paw_scale, False),
        ("HIND_L", "HIND", +1.0, pelvis, orient.pelvis_width_scale, morphology.hind_limb_length, morphology.paw_scale, True),
        ("HIND_R", "HIND", -1.0, pelvis, orient.pelvis_width_scale, morphology.hind_limb_length, morphology.paw_scale, True),
    ):
        paw_id = f"{owner}_PAW_{'L' if side > 0 else 'R'}"
        paw = anchors[paw_id]
        local_z = side * size * width_scale * (0.080 if hind else 0.086)
        ventral = size * (0.055 if hind else 0.070)
        attachment = _side_attachment(center, local_z, ventral, yaw)
        bend = size * limb_scale * (0.046 if hind else -0.034)
        side_bias = side * size * 0.018
        chain = _limb_chain(attachment, paw, bend, side_bias, yaw)
        radius = size * RATIOS["hind_limb" if hind else "fore_limb"]["radius"]
        seg_a, seg_b = _limb_polygon(chain, radius)
        limbs.append(ProjectedPrimitive(f"{domain}_PROXIMAL", "CAPSULE", domain, seg_a))
        limbs.append(ProjectedPrimitive(f"{domain}_DISTAL", "CAPSULE", domain, seg_b))
        pr = RATIOS["hind_limb" if hind else "fore_limb"]
        paw_points = _ellipse_at(paw, pr["paw_rx"] * size * paw_scale, pr["paw_ry"] * size * paw_scale)
        paws.append(ProjectedPrimitive(f"{domain}_PAW", "PAW_ELLIPSE", domain, paw_points))
        center_x = sum(p[0] for p in paw_points) / len(paw_points)
        center_y = sum(p[1] for p in paw_points) / len(paw_points)
        paw_pin_error = max(paw_pin_error, math.hypot(center_x - float(paw.x), center_y - float(paw.y)))

    tail_points = _tail_points(tail_root, size, morphology.tail_length, yaw)
    tail_radius = size * RATIOS["tail"]["radius"] * morphology.tail_thickness
    # A single capsule from root to tip would erase the curve. Use the convex
    # envelope only for bounds; evidence renderer draws the centerline segments
    # with this truthful radius.
    tail_cloud = []
    for a, b in zip(tail_points, tail_points[1:]):
        tail_cloud.extend(_capsule(a, b, tail_radius))
    tail = ProjectedPrimitive("TAIL_CHANNEL", "CURVED_CAPSULE_CHAIN", "TAIL", _convex_hull(tail_cloud))

    by_domain = {domain: [] for domain in EXTERNAL_DOMAINS}
    for primitive in core_primitives + ears + tuple(limbs) + tuple(paws) + (tail,):
        by_domain[primitive.domain].extend(primitive.points)
    domain_bounds = {domain: _bounds(points) for domain, points in by_domain.items()}
    visual_bounds = _union_bounds(domain_bounds.values())

    return ProxyResult(
        version=PROTOTYPE_VERSION,
        yaw_rad=yaw,
        signature=proxy_signature(),
        core_primitives=core_primitives,
        ears=ears,
        limbs=tuple(limbs),
        paws=tuple(paws),
        tail=tail,
        domain_bounds=domain_bounds,
        visual_bounds=visual_bounds,
        paw_pin_error=paw_pin_error,
    )


def all_points(result: ProxyResult, include_ears: bool = True):
    primitives = result.core_primitives + (result.ears if include_ears else ()) + result.limbs + result.paws + (result.tail,)
    return tuple(point for primitive in primitives for point in primitive.points)


def result_dict(fixture, result: ProxyResult) -> dict:
    finite = all(math.isfinite(v) for point in all_points(result) for v in point)
    return {
        "version": result.version,
        "caseId": fixture.case_id,
        "morphologyId": fixture.morphology_id,
        "sizeDp": int(fixture.size_dp),
        "t": float(fixture.t),
        "semanticHash": fixture.semantic_hash,
        "yawRad": result.yaw_rad,
        "proxySignature": result.signature,
        "coreVolumeIds": list(CORE_VOLUME_IDS),
        "externalDomains": list(EXTERNAL_DOMAINS),
        "externalDomainCount": len(EXTERNAL_DOMAINS),
        "pawPinError": result.paw_pin_error,
        "finite": finite,
        "correctionUseCount": 0,
        "domainBounds": {key: list(value) for key, value in sorted(result.domain_bounds.items())},
        "visualBounds": list(result.visual_bounds),
    }
