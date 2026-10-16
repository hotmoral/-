from __future__ import annotations

from dataclasses import dataclass
import binascii
import hashlib
import json
import math
from pathlib import Path
import struct
import zlib

from h6n_stepped_turn import LATERAL_HALF_STANCE_BU, PAWS, stance_anchor_b3, stance_target_s, _structural_anchors
from model import Vec2
from orientation_v2 import M0_V2, MorphologyV2, Vec3, project_b3

VERSION = "P1_C_R9_INTRINSIC_CURVE_PIXEL_V1"
CANVAS_W = 80
CANVAS_H = 80
SAMPLE_COUNT = 33
EXTERNAL_DOMAINS = ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL")
CURVE_GROUP_LIMIT = 16
CONTROL_NODE_LIMIT = 64
CURVE_SEGMENT_LIMIT = 48


@dataclass(frozen=True)
class CurveSpec:
    id: str
    domain: str
    kind: str
    nodes: tuple[Vec3, Vec3, Vec3, Vec3]
    radius_start_bu: float = 0.0
    radius_end_bu: float = 0.0


@dataclass(frozen=True)
class Carrier:
    version: str
    curves: tuple[CurveSpec, ...]


@dataclass(frozen=True)
class RenderMetrics:
    yaw_rad: float
    occupied_pixels: int
    component_count: int
    bbox: tuple[int, int, int, int] | None
    centroid: tuple[float, float] | None


def _v(x: float, y: float, z: float) -> Vec3:
    return Vec3(float(x), float(y), float(z))


def _side(sign: float, x: float, y: float, z: float) -> Vec3:
    return _v(x, y, sign * z)


def _paw_terminal_b3(paw: str, morphology: MorphologyV2) -> Vec3:
    stance = stance_anchor_b3(paw, morphology, +1, LATERAL_HALF_STANCE_BU)
    # H6N canonical BODY_ROOT sits 0.88 BU above ground. Using y=-0.88
    # makes project_b3 land exactly on the canonical neutral paw target.
    return Vec3(stance.x, -0.88, stance.z)


def build_neutral_carrier(morphology: MorphologyV2 = M0_V2) -> Carrier:
    """One neutral body-local curve grammar; no authored view bases.

    The carrier has 15 cubic curve groups / 60 body-local control nodes.
    Four paired longitudinal boundary curves describe the trunk, four the head,
    four centerline curves bind to the canonical paw geometry, two tapered ear
    curves are CORE detail, and one tapered tail curve is TAIL.
    """
    morphology.validate()
    base = morphology.base
    tl = base.trunk_length
    hs = base.head_scale
    td = base.trunk_depth
    tw = morphology.thorax_width_scale
    pw = morphology.pelvis_width_scale

    curves: list[CurveSpec] = []

    # CORE trunk: continuous longitudinal boundary curves. These are not authored
    # transverse stations; derived raster strips sample these curves later.
    for suffix, sign in (("L", +1.0), ("R", -1.0)):
        curves.append(CurveSpec(
            f"CORE_DORSAL_{suffix}", "CORE", "BOUNDARY",
            (
                _side(sign, +0.60 * tl, +0.40 * td, 0.27 * tw),
                _side(sign, +0.20 * tl, +0.53 * td, 0.32 * tw),
                _side(sign, -0.34 * tl, +0.44 * td, 0.28 * tw),
                _side(sign, -0.72 * tl, +0.40 * td, 0.33 * pw),
            ),
        ))
        curves.append(CurveSpec(
            f"CORE_VENTRAL_{suffix}", "CORE", "BOUNDARY",
            (
                _side(sign, +0.58 * tl, +0.04 * td, 0.23 * tw),
                _side(sign, +0.18 * tl, -0.10 * td, 0.25 * tw),
                _side(sign, -0.28 * tl, +0.05 * td, 0.17 * tw),
                _side(sign, -0.70 * tl, -0.01 * td, 0.28 * pw),
            ),
        ))

    # CORE head/neck: feline wedge + rounded cranium, still one intrinsic rule.
    for suffix, sign in (("L", +1.0), ("R", -1.0)):
        curves.append(CurveSpec(
            f"HEAD_DORSAL_{suffix}", "CORE", "BOUNDARY",
            (
                _side(sign, +1.04 * hs, +0.63 * hs, 0.10 * hs),
                _side(sign, +0.96 * hs, +0.88 * hs, 0.22 * hs),
                _side(sign, +0.73 * hs, +0.98 * hs, 0.31 * hs),
                _side(sign, +0.51 * hs, +0.55 * hs, 0.23 * hs),
            ),
        ))
        curves.append(CurveSpec(
            f"HEAD_VENTRAL_{suffix}", "CORE", "BOUNDARY",
            (
                _side(sign, +1.05 * hs, +0.52 * hs, 0.10 * hs),
                _side(sign, +0.94 * hs, +0.40 * hs, 0.16 * hs),
                _side(sign, +0.70 * hs, +0.36 * hs, 0.19 * hs),
                _side(sign, +0.50 * hs, +0.39 * hs, 0.22 * hs),
            ),
        ))

    # Four limb centerlines. Their terminal controls are body-local canonical
    # stance anchors, so projection pins them to canonical neutral paw targets.
    limb_defs = (
        ("FORE_L", "FORE_PAW_L", +1.0),
        ("FORE_R", "FORE_PAW_R", -1.0),
        ("HIND_L", "HIND_PAW_L", +1.0),
        ("HIND_R", "HIND_PAW_R", -1.0),
    )
    for domain, paw, sign in limb_defs:
        terminal = _paw_terminal_b3(paw, morphology)
        if domain.startswith("FORE"):
            nodes = (
                _side(sign, +0.48 * tl, +0.18 * td, 0.23 * tw),
                _side(sign, +0.48 * tl, -0.12 * td, 0.25 * tw),
                _side(sign, +0.40 * tl, -0.58 * td, 0.23 * tw),
                terminal,
            )
            r0, r1 = 0.145 * base.forequarter_scale, 0.070 * base.paw_scale
        else:
            nodes = (
                _side(sign, -0.55 * tl, +0.16 * td, 0.28 * pw),
                _side(sign, -0.72 * tl, -0.08 * td, 0.29 * pw),
                _side(sign, -0.48 * tl, -0.56 * td, 0.24 * pw),
                terminal,
            )
            r0, r1 = 0.165 * base.pelvis_scale, 0.075 * base.paw_scale
        curves.append(CurveSpec(domain, domain, "CENTERLINE", nodes, r0, r1))

    # TAIL stays compact enough for the 80px window and curves dorsally instead
    # of extending as a long identity crutch.
    curves.append(CurveSpec(
        "TAIL", "TAIL", "CENTERLINE",
        (
            _v(-0.70 * tl, +0.24 * td, 0.0),
            _v(-0.94 * tl, +0.34 * td, +0.03),
            _v(-1.06 * tl, +0.68 * td, +0.05),
            _v(-0.86 * tl, +0.86 * td, +0.04),
        ),
        0.090 * base.tail_thickness,
        0.035 * base.tail_thickness,
    ))

    # Ears are CORE curves and can be omitted for ear-neutralized diagnostics.
    curves.append(CurveSpec(
        "EAR_L", "CORE", "CENTERLINE",
        (
            _v(+0.80 * hs, +0.90 * hs, +0.18 * hs),
            _v(+0.77 * hs, +1.02 * hs, +0.21 * hs),
            _v(+0.71 * hs, +1.16 * hs, +0.23 * hs),
            _v(+0.66 * hs, +1.23 * hs, +0.24 * hs),
        ),
        0.085 * hs, 0.012 * hs,
    ))
    curves.append(CurveSpec(
        "EAR_R", "CORE", "CENTERLINE",
        (
            _v(+0.80 * hs, +0.90 * hs, -0.18 * hs),
            _v(+0.77 * hs, +1.02 * hs, -0.21 * hs),
            _v(+0.71 * hs, +1.16 * hs, -0.23 * hs),
            _v(+0.66 * hs, +1.23 * hs, -0.24 * hs),
        ),
        0.085 * hs, 0.012 * hs,
    ))

    carrier = Carrier(VERSION, tuple(curves))
    validate_carrier(carrier)
    return carrier


def validate_carrier(carrier: Carrier) -> None:
    if carrier.version != VERSION:
        raise ValueError("unexpected carrier version")
    if len(carrier.curves) > CURVE_GROUP_LIMIT:
        raise ValueError("curve group ceiling exceeded")
    node_count = sum(len(c.nodes) for c in carrier.curves)
    if node_count > CONTROL_NODE_LIMIT:
        raise ValueError("control node ceiling exceeded")
    if len(carrier.curves) > CURVE_SEGMENT_LIMIT:
        raise ValueError("curve segment ceiling exceeded")
    domains = {c.domain for c in carrier.curves}
    if domains != set(EXTERNAL_DOMAINS):
        raise ValueError(f"external domains mismatch: {sorted(domains)}")
    ids = [c.id for c in carrier.curves]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate curve id")
    for curve in carrier.curves:
        if len(curve.nodes) != 4:
            raise ValueError(f"{curve.id}: cubic node count must be 4")
        for p in curve.nodes:
            if not all(math.isfinite(v) for v in (p.x, p.y, p.z)):
                raise ValueError(f"{curve.id}: nonfinite control")


def carrier_signature(carrier: Carrier) -> str:
    payload = {
        "version": carrier.version,
        "curves": [
            {
                "id": c.id,
                "domain": c.domain,
                "kind": c.kind,
                "nodes": [[p.x, p.y, p.z] for p in c.nodes],
                "r0": c.radius_start_bu,
                "r1": c.radius_end_bu,
            }
            for c in carrier.curves
        ],
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def cubic_point(nodes: tuple[Vec3, Vec3, Vec3, Vec3], t: float) -> Vec3:
    u = 1.0 - t
    w0 = u * u * u
    w1 = 3.0 * u * u * t
    w2 = 3.0 * u * t * t
    w3 = t * t * t
    return Vec3(
        w0 * nodes[0].x + w1 * nodes[1].x + w2 * nodes[2].x + w3 * nodes[3].x,
        w0 * nodes[0].y + w1 * nodes[1].y + w2 * nodes[2].y + w3 * nodes[3].y,
        w0 * nodes[0].z + w1 * nodes[1].z + w2 * nodes[2].z + w3 * nodes[3].z,
    )


def sample_curve_b3(curve: CurveSpec, count: int = SAMPLE_COUNT) -> list[Vec3]:
    if count < 2:
        raise ValueError("count must be >=2")
    return [cubic_point(curve.nodes, i / (count - 1)) for i in range(count)]


def neutral_semantic_frame(yaw_rad: float, size_dp: float = 80.0, morphology: MorphologyV2 = M0_V2) -> dict[str, Vec2]:
    anchors = dict(_structural_anchors(morphology, size_dp, yaw_rad))
    for paw in PAWS:
        anchors[paw] = stance_target_s(paw, morphology, size_dp, +1, yaw_rad)
    return anchors


def _body_root(size_dp: float) -> Vec2:
    scale = size_dp / 2.0
    ground_y = size_dp * 1.38
    return Vec2(size_dp * 1.45, ground_y - 0.88 * scale)


def project_curve_dp(curve: CurveSpec, yaw_rad: float, size_dp: float = 80.0, count: int = SAMPLE_COUNT) -> list[Vec2]:
    root = _body_root(size_dp)
    scale = size_dp / 2.0
    return [project_b3(p, root, scale, yaw_rad) for p in sample_curve_b3(curve, count)]


def paw_pin_errors(carrier: Carrier, yaw_rad: float, size_dp: float = 80.0, morphology: MorphologyV2 = M0_V2) -> dict[str, float]:
    semantic = neutral_semantic_frame(yaw_rad, size_dp, morphology)
    by_id = {c.id: c for c in carrier.curves}
    out = {}
    mapping = {
        "FORE_L": "FORE_PAW_L",
        "FORE_R": "FORE_PAW_R",
        "HIND_L": "HIND_PAW_L",
        "HIND_R": "HIND_PAW_R",
    }
    for curve_id, paw in mapping.items():
        endpoint = project_b3(by_id[curve_id].nodes[-1], _body_root(size_dp), size_dp / 2.0, yaw_rad)
        target = semantic[paw]
        out[paw] = math.hypot(endpoint.x - target.x, endpoint.y - target.y)
    return out


@dataclass(frozen=True)
class PixelTransform:
    root_s: Vec2
    dp_per_bu: float
    px_per_dp: float
    origin_dp: Vec2
    margin_px: float

    def to_px(self, p: Vec2) -> tuple[float, float]:
        return (
            self.margin_px + (p.x - self.origin_dp.x) * self.px_per_dp,
            self.margin_px + (p.y - self.origin_dp.y) * self.px_per_dp,
        )


def pixel_transform(size_dp: float = 80.0) -> PixelTransform:
    root = _body_root(size_dp)
    scale = size_dp / 2.0
    # Fixed orientation-independent crop: 2.50 BU wide x 2.25 BU tall.
    x_min = root.x - 1.25 * scale
    x_max = root.x + 1.25 * scale
    y_min = root.y - 1.28 * scale
    y_max = root.y + 0.97 * scale
    margin = 3.0
    usable_w = CANVAS_W - 2.0 * margin
    usable_h = CANVAS_H - 2.0 * margin
    px_per_dp = min(usable_w / (x_max - x_min), usable_h / (y_max - y_min))
    return PixelTransform(root, scale, px_per_dp, Vec2(x_min, y_min), margin)


def _blank(value: int = 0) -> list[list[int]]:
    return [[value for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]


def _convex_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    pts = sorted(set((float(x), float(y)) for x, y in points))
    if len(pts) <= 2:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _point_in_poly(x: float, y: float, poly: list[tuple[float, float]]) -> bool:
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)):
            denom = yj - yi
            if abs(denom) < 1e-12:
                denom = 1e-12
            x_cross = (xj - xi) * (y - yi) / denom + xi
            if x < x_cross:
                inside = not inside
        j = i
    return inside


def _fill_poly(mask: list[list[int]], poly: list[tuple[float, float]], value: int) -> None:
    if len(poly) < 3:
        return
    min_x = max(0, int(math.floor(min(p[0] for p in poly))) - 1)
    max_x = min(CANVAS_W - 1, int(math.ceil(max(p[0] for p in poly))) + 1)
    min_y = max(0, int(math.floor(min(p[1] for p in poly))) - 1)
    max_y = min(CANVAS_H - 1, int(math.ceil(max(p[1] for p in poly))) + 1)
    for py in range(min_y, max_y + 1):
        cy = py + 0.5
        row = mask[py]
        for px in range(min_x, max_x + 1):
            if _point_in_poly(px + 0.5, cy, poly):
                row[px] = value


def _fill_disc(mask: list[list[int]], cx: float, cy: float, radius: float, value: int) -> None:
    if radius <= 0.0:
        return
    min_x = max(0, int(math.floor(cx - radius - 1)))
    max_x = min(CANVAS_W - 1, int(math.ceil(cx + radius + 1)))
    min_y = max(0, int(math.floor(cy - radius - 1)))
    max_y = min(CANVAS_H - 1, int(math.ceil(cy + radius + 1)))
    r2 = radius * radius
    for py in range(min_y, max_y + 1):
        for px in range(min_x, max_x + 1):
            dx = (px + 0.5) - cx
            dy = (py + 0.5) - cy
            if dx * dx + dy * dy <= r2:
                mask[py][px] = value


def _draw_thick_polyline(mask: list[list[int]], points: list[tuple[float, float]], r0: float, r1: float, value: int) -> None:
    if len(points) < 2:
        return
    for i in range(len(points) - 1):
        ax, ay = points[i]
        bx, by = points[i + 1]
        seg_len = math.hypot(bx - ax, by - ay)
        steps = max(2, int(math.ceil(seg_len * 2.0)))
        for j in range(steps + 1):
            u = j / steps
            t = (i + u) / (len(points) - 1)
            radius = r0 * (1.0 - t) + r1 * t
            _fill_disc(mask, ax * (1.0 - u) + bx * u, ay * (1.0 - u) + by * u, radius, value)


def _curve_map(carrier: Carrier) -> dict[str, CurveSpec]:
    return {c.id: c for c in carrier.curves}


def _project_px(carrier: Carrier, yaw_rad: float, size_dp: float = 80.0) -> dict[str, list[tuple[float, float]]]:
    tf = pixel_transform(size_dp)
    return {
        c.id: [tf.to_px(p) for p in project_curve_dp(c, yaw_rad, size_dp)]
        for c in carrier.curves
    }


def _fill_boundary_strip(mask: list[list[int]], a: list[tuple[float, float]], b: list[tuple[float, float]], c: list[tuple[float, float]], d: list[tuple[float, float]], value: int) -> None:
    n = min(len(a), len(b), len(c), len(d))
    for i in range(n - 1):
        hull = _convex_hull([a[i], b[i], c[i], d[i], a[i+1], b[i+1], c[i+1], d[i+1]])
        _fill_poly(mask, hull, value)


def _depth_of(curve: CurveSpec, yaw_rad: float) -> float:
    # Orthogonal to project_b3's screen tangent. Larger value is treated as near.
    values = [p.x * math.sin(yaw_rad) - p.z * math.cos(yaw_rad) for p in curve.nodes]
    return sum(values) / len(values)


def render_mask(
    carrier: Carrier,
    yaw_rad: float,
    *,
    size_dp: float = 80.0,
    ear_neutralized: bool = False,
    domain_values: bool = False,
) -> list[list[int]]:
    validate_carrier(carrier)
    projected = _project_px(carrier, yaw_rad, size_dp)
    by_id = _curve_map(carrier)
    tf = pixel_transform(size_dp)
    scale_px_per_bu = tf.dp_per_bu * tf.px_per_dp

    values = {
        "CORE": 48,
        "FORE_L": 92,
        "FORE_R": 122,
        "HIND_L": 158,
        "HIND_R": 188,
        "TAIL": 220,
    }
    def val(domain: str) -> int:
        return values[domain] if domain_values else 255

    mask = _blank(0)

    limb_ids = ("FORE_L", "FORE_R", "HIND_L", "HIND_R")
    far = [cid for cid in limb_ids if _depth_of(by_id[cid], yaw_rad) < 0.0]
    near = [cid for cid in limb_ids if _depth_of(by_id[cid], yaw_rad) >= 0.0]

    def draw_centerline(cid: str) -> None:
        curve = by_id[cid]
        _draw_thick_polyline(
            mask,
            projected[cid],
            curve.radius_start_bu * scale_px_per_bu,
            curve.radius_end_bu * scale_px_per_bu,
            val(curve.domain),
        )

    # Far limbs first.
    for cid in sorted(far):
        draw_centerline(cid)

    # Tail sits behind the core at its root.
    draw_centerline("TAIL")

    # Trunk and head are filled only from sampled continuous boundary curves.
    _fill_boundary_strip(
        mask,
        projected["CORE_DORSAL_L"], projected["CORE_DORSAL_R"],
        projected["CORE_VENTRAL_R"], projected["CORE_VENTRAL_L"],
        val("CORE"),
    )
    _fill_boundary_strip(
        mask,
        projected["HEAD_DORSAL_L"], projected["HEAD_DORSAL_R"],
        projected["HEAD_VENTRAL_R"], projected["HEAD_VENTRAL_L"],
        val("CORE"),
    )

    if not ear_neutralized:
        draw_centerline("EAR_L")
        draw_centerline("EAR_R")

    # Near limbs last to create deterministic depth/occlusion without view assets.
    for cid in sorted(near):
        draw_centerline(cid)

    return mask


def mask_metrics(mask: list[list[int]], yaw_rad: float) -> RenderMetrics:
    points = [(x, y) for y, row in enumerate(mask) for x, v in enumerate(row) if v != 0]
    if not points:
        return RenderMetrics(yaw_rad, 0, 0, None, None)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    bbox = (min(xs), min(ys), max(xs), max(ys))
    centroid = (sum(xs) / len(xs), sum(ys) / len(ys))

    occupied = set(points)
    components = 0
    while occupied:
        components += 1
        stack = [occupied.pop()]
        while stack:
            x, y = stack.pop()
            for nb in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if nb in occupied:
                    occupied.remove(nb)
                    stack.append(nb)
    return RenderMetrics(yaw_rad, len(points), components, bbox, centroid)


def binary_mask(mask: list[list[int]]) -> list[list[int]]:
    return [[255 if v else 0 for v in row] for row in mask]


def mask_bytes(mask: list[list[int]]) -> bytes:
    return bytes(v for row in mask for v in row)


def mask_sha256(mask: list[list[int]]) -> str:
    return hashlib.sha256(mask_bytes(mask)).hexdigest()


def orientation_metrics(carrier: Carrier, steps: int = 13, size_dp: float = 80.0) -> dict:
    if steps < 3:
        raise ValueError("steps must be >=3")
    frames = []
    for i in range(steps):
        yaw = (math.pi / 2.0) * i / (steps - 1)
        mask = binary_mask(render_mask(carrier, yaw, size_dp=size_dp))
        frames.append((yaw, mask, mask_metrics(mask, yaw)))

    max_area_jump = 0.0
    max_centroid_step = 0.0
    max_xor_union = 0.0
    for i in range(len(frames) - 1):
        _, a, ma = frames[i]
        _, b, mb = frames[i+1]
        denom = max(1, ma.occupied_pixels)
        max_area_jump = max(max_area_jump, abs(mb.occupied_pixels - ma.occupied_pixels) / denom)
        if ma.centroid is not None and mb.centroid is not None:
            max_centroid_step = max(max_centroid_step, math.hypot(mb.centroid[0]-ma.centroid[0], mb.centroid[1]-ma.centroid[1]))
        xor = 0
        union = 0
        for y in range(CANVAS_H):
            for x in range(CANVAS_W):
                aa = a[y][x] != 0
                bb = b[y][x] != 0
                xor += int(aa != bb)
                union += int(aa or bb)
        max_xor_union = max(max_xor_union, xor / max(1, union))

    return {
        "steps": steps,
        "maxAreaJumpRatio": max_area_jump,
        "maxCentroidStepPx": max_centroid_step,
        "maxXorUnionRatio": max_xor_union,
        "maxComponentCount": max(frame[2].component_count for frame in frames),
        "minOccupiedPixels": min(frame[2].occupied_pixels for frame in frames),
        "frameHashes": [mask_sha256(frame[1]) for frame in frames],
        "frames": frames,
    }


def _png_chunk(kind: bytes, data: bytes) -> bytes:
    payload = kind + data
    return struct.pack(">I", len(data)) + payload + struct.pack(">I", binascii.crc32(payload) & 0xFFFFFFFF)


def write_png(path: str | Path, mask: list[list[int]], *, invert: bool = True) -> None:
    path = Path(path)
    h = len(mask)
    w = len(mask[0]) if h else 0
    if w <= 0 or h <= 0 or any(len(row) != w for row in mask):
        raise ValueError("invalid mask")
    raw_rows = []
    for row in mask:
        rgb = bytearray()
        for v in row:
            q = 255 - v if invert else v
            rgb.extend((q, q, q))
        raw_rows.append(b"\x00" + bytes(rgb))
    raw = b"".join(raw_rows)
    png = b"\x89PNG\r\n\x1a\n"
    png += _png_chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += _png_chunk(b"IDAT", zlib.compress(raw, 9))
    png += _png_chunk(b"IEND", b"")
    path.write_bytes(png)


def write_strip_png(path: str | Path, masks: list[list[list[int]]], *, invert: bool = True) -> None:
    if not masks:
        raise ValueError("masks required")
    h = len(masks[0])
    w = len(masks[0][0])
    combined = []
    for y in range(h):
        row = []
        for mask in masks:
            if len(mask) != h or len(mask[0]) != w:
                raise ValueError("mask size mismatch")
            row.extend(mask[y])
        combined.append(row)

    path = Path(path)
    width = w * len(masks)
    raw_rows = []
    for row in combined:
        rgb = bytearray()
        for v in row:
            q = 255 - v if invert else v
            rgb.extend((q, q, q))
        raw_rows.append(b"\x00" + bytes(rgb))
    raw = b"".join(raw_rows)
    png = b"\x89PNG\r\n\x1a\n"
    png += _png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, h, 8, 2, 0, 0, 0))
    png += _png_chunk(b"IDAT", zlib.compress(raw, 9))
    png += _png_chunk(b"IEND", b"")
    path.write_bytes(png)


def structural_summary(carrier: Carrier) -> dict:
    return {
        "version": carrier.version,
        "signature": carrier_signature(carrier),
        "curveGroups": len(carrier.curves),
        "controlNodes": sum(len(c.nodes) for c in carrier.curves),
        "curveSegments": len(carrier.curves),
        "domains": sorted({c.domain for c in carrier.curves}),
        "nativeRaster": [CANVAS_W, CANVAS_H],
        "sampleCountPerCurve": SAMPLE_COUNT,
    }
