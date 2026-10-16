from __future__ import annotations

from dataclasses import dataclass
import binascii
import json
import math
from pathlib import Path
import struct
import zlib

VERSION = "P1_C_ADULT_WALK_DENSITY_EXPERIMENT_V1"
CANVAS_W = 96
CANVAS_H = 96
CYCLE_SECONDS = 1.08
STANCE_SECONDS = 0.80
SWING_SECONDS = 0.28
STANCE_FRACTION = STANCE_SECONDS / CYCLE_SECONDS
DIRECTION_COUNTS = (12, 16, 24, 36)
FRAME_COUNTS = (12, 16, 24, 32)
LIMBS = ("RH", "RF", "LH", "LF")
FOOTFALL_OFFSETS = {"RH": 0.00, "RF": 0.25, "LH": 0.50, "LF": 0.75}


@dataclass(frozen=True)
class P3:
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class P2:
    x: float
    y: float


@dataclass(frozen=True)
class LimbPose:
    paw: P3
    joint: P3
    root: P3
    stance: bool


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _smoothstep(u: float) -> float:
    u = _clamp(u, 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)


def _cyclic_phase_distance(a: float, b: float) -> float:
    d = abs((a - b) % 1.0)
    return min(d, 1.0 - d)


def nearest_phase(phase: float, frame_count: int) -> float:
    k = int(math.floor((phase % 1.0) * frame_count + 0.5)) % frame_count
    return k / frame_count


def nearest_yaw(yaw: float, direction_count: int) -> float:
    tau = 2.0 * math.pi
    step = tau / direction_count
    k = int(math.floor((yaw % tau) / step + 0.5)) % direction_count
    return k * step


def angular_error_deg(yaw: float, quantized_yaw: float) -> float:
    d = abs((yaw - quantized_yaw + math.pi) % (2.0 * math.pi) - math.pi)
    return math.degrees(d)


def limb_cycle(limb: str, phase: float) -> tuple[float, bool, float]:
    """Return longitudinal paw offset, stance state and vertical lift in body units."""
    local = (phase - FOOTFALL_OFFSETS[limb]) % 1.0
    stride = 0.46 if limb[1] == "H" else 0.43
    if local < STANCE_FRACTION:
        u = local / STANCE_FRACTION
        x = stride * (0.5 - u)
        return x, True, 0.0
    u = (local - STANCE_FRACTION) / (1.0 - STANCE_FRACTION)
    e = _smoothstep(u)
    x = stride * (-0.5 + e)
    lift = (0.20 if limb[1] == "H" else 0.17) * math.sin(math.pi * u)
    return x, False, lift


def support_state(phase: float) -> tuple[str, ...]:
    return tuple(limb for limb in LIMBS if limb_cycle(limb, phase)[1])


def _limb_pose(limb: str, phase: float) -> LimbPose:
    is_hind = limb[1] == "H"
    is_left = limb[0] == "L"
    z = 0.16 if is_left else -0.16
    if is_hind:
        root = P3(-0.34, 0.68, z)
        paw_base = -0.34
        upper = 0.39
        lower = 0.43
        bend = -1.0
    else:
        root = P3(0.34, 0.72, z)
        paw_base = 0.34
        upper = 0.37
        lower = 0.39
        bend = 1.0

    stride_x, stance, lift = limb_cycle(limb, phase)
    paw = P3(paw_base + stride_x, 0.02 + lift, z)

    dx = paw.x - root.x
    dy = paw.y - root.y
    dist = max(0.05, math.hypot(dx, dy))
    max_reach = upper + lower - 1e-4
    if dist > max_reach:
        s = max_reach / dist
        dx *= s
        dy *= s
        dist = max_reach
    a = (upper * upper - lower * lower + dist * dist) / (2.0 * dist)
    h2 = max(0.0, upper * upper - a * a)
    h = math.sqrt(h2)
    ux, uy = dx / dist, dy / dist
    bx = root.x + a * ux
    by = root.y + a * uy
    px, py = -uy, ux
    joint = P3(bx + bend * h * px, by + bend * h * py, z)
    return LimbPose(paw=paw, joint=joint, root=root, stance=stance)


def _body_points(phase: float) -> dict[str, P3]:
    gait2 = 2.0 * math.pi * phase
    body_bob = 0.018 * math.cos(4.0 * math.pi * phase)
    pitch = 0.020 * math.sin(gait2)
    pelvis_lift = 0.028 * math.sin(gait2 + 0.35)
    shoulder_lift = 0.022 * math.sin(gait2 + math.pi + 0.15)
    return {
        "pelvis": P3(-0.30, 0.78 + body_bob + pelvis_lift, 0.0),
        "abdomen": P3(-0.04, 0.75 + body_bob - 0.012, 0.0),
        "thorax": P3(0.24, 0.82 + body_bob + shoulder_lift, 0.0),
        "neck": P3(0.48, 0.92 + body_bob + 0.5 * pitch, 0.0),
        "head": P3(0.65, 1.03 + body_bob + 0.012 * math.sin(gait2 + 0.6), 0.0),
        "muzzle": P3(0.79, 0.98 + body_bob + 0.010 * math.sin(gait2 + 0.6), 0.0),
        "tail0": P3(-0.49, 0.82 + body_bob, 0.0),
        "tail1": P3(-0.71, 0.93 + body_bob + 0.035 * math.sin(gait2 + 0.7), 0.02 * math.sin(gait2)),
        "tail2": P3(-0.91, 1.10 + body_bob + 0.045 * math.sin(gait2 + 1.2), 0.05 * math.sin(gait2 + 0.4)),
    }


def _project(p: P3, yaw: float) -> tuple[P2, float]:
    c, s = math.cos(yaw), math.sin(yaw)
    sx = p.x * c + p.z * s
    depth = -p.x * s + p.z * c
    scale = 35.0
    return P2(CANVAS_W * 0.50 + sx * scale, 82.0 - p.y * scale), depth


def _new_rgb() -> list[list[list[int]]]:
    return [[[255, 255, 255] for _ in range(CANVAS_W)] for _ in range(CANVAS_H)]


def _set_px(img, x: int, y: int, color: tuple[int, int, int]):
    if 0 <= x < CANVAS_W and 0 <= y < CANVAS_H:
        img[y][x][0], img[y][x][1], img[y][x][2] = color


def _disc(img, cx: float, cy: float, r: float, color):
    x0, x1 = int(math.floor(cx - r)), int(math.ceil(cx + r))
    y0, y1 = int(math.floor(cy - r)), int(math.ceil(cy + r))
    rr = r * r
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2 <= rr:
                _set_px(img, x, y, color)


def _ellipse(img, cx: float, cy: float, rx: float, ry: float, color):
    x0, x1 = int(math.floor(cx - rx)), int(math.ceil(cx + rx))
    y0, y1 = int(math.floor(cy - ry)), int(math.ceil(cy + ry))
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            dx = (x + 0.5 - cx) / max(rx, 1e-6)
            dy = (y + 0.5 - cy) / max(ry, 1e-6)
            if dx * dx + dy * dy <= 1.0:
                _set_px(img, x, y, color)


def _line(img, a: P2, b: P2, width: float, color):
    dx, dy = b.x - a.x, b.y - a.y
    steps = max(1, int(math.ceil(max(abs(dx), abs(dy)) * 1.5)))
    for i in range(steps + 1):
        t = i / steps
        _disc(img, a.x + dx * t, a.y + dy * t, width * 0.5, color)


def _triangle(img, a: P2, b: P2, c: P2, color):
    minx = int(math.floor(min(a.x, b.x, c.x)))
    maxx = int(math.ceil(max(a.x, b.x, c.x)))
    miny = int(math.floor(min(a.y, b.y, c.y)))
    maxy = int(math.ceil(max(a.y, b.y, c.y)))
    def edge(p, q, x, y):
        return (x - p.x) * (q.y - p.y) - (y - p.y) * (q.x - p.x)
    area = edge(a, b, c.x, c.y)
    if abs(area) < 1e-9:
        return
    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            px, py = x + 0.5, y + 0.5
            e1, e2, e3 = edge(a, b, px, py), edge(b, c, px, py), edge(c, a, px, py)
            if (e1 >= 0 and e2 >= 0 and e3 >= 0) or (e1 <= 0 and e2 <= 0 and e3 <= 0):
                _set_px(img, x, y, color)


def render_reference(yaw: float, phase: float) -> list[list[list[int]]]:
    phase %= 1.0
    img = _new_rgb()
    body = _body_points(phase)
    limb_poses = {limb: _limb_pose(limb, phase) for limb in LIMBS}

    projected_limbs = []
    for limb, pose in limb_poses.items():
        root2, d0 = _project(pose.root, yaw)
        joint2, d1 = _project(pose.joint, yaw)
        paw2, d2 = _project(pose.paw, yaw)
        projected_limbs.append((0.5 * (d0 + d2), limb, root2, joint2, paw2, pose.stance))

    projected_limbs.sort(key=lambda row: row[0], reverse=True)
    for depth, limb, root2, joint2, paw2, stance in projected_limbs[:2]:
        color = (120, 120, 120)
        _line(img, root2, joint2, 5.0, color)
        _line(img, joint2, paw2, 4.0, color)
        _ellipse(img, paw2.x + 1.0, paw2.y + 0.5, 3.2, 1.8, color)

    pelvis2, _ = _project(body["pelvis"], yaw)
    abdomen2, _ = _project(body["abdomen"], yaw)
    thorax2, _ = _project(body["thorax"], yaw)
    neck2, _ = _project(body["neck"], yaw)
    head2, _ = _project(body["head"], yaw)
    muzzle2, _ = _project(body["muzzle"], yaw)

    profile = abs(math.cos(yaw))
    front = abs(math.sin(yaw))
    _ellipse(img, pelvis2.x, pelvis2.y, 11.0 * profile + 8.0 * front, 10.2, (35, 35, 35))
    _ellipse(img, abdomen2.x, abdomen2.y + 1.5, 13.0 * profile + 7.5 * front, 8.0, (38, 38, 38))
    _ellipse(img, thorax2.x, thorax2.y, 13.2 * profile + 9.0 * front, 11.0, (28, 28, 28))
    _line(img, thorax2, neck2, 9.0, (28, 28, 28))
    _ellipse(img, head2.x, head2.y, 8.0 * profile + 8.8 * front, 8.4, (20, 20, 20))
    _ellipse(img, muzzle2.x, muzzle2.y + 1.0, 4.8 * profile + 5.4 * front, 4.2, (25, 25, 25))

    # Ears are simple structural cues, not final art.
    ear_left_b = P3(body["head"].x - 0.02, body["head"].y + 0.13, 0.10)
    ear_right_b = P3(body["head"].x - 0.02, body["head"].y + 0.13, -0.10)
    for ear_b in (ear_left_b, ear_right_b):
        base, _ = _project(ear_b, yaw)
        apex_b = P3(ear_b.x - 0.015, ear_b.y + 0.15, ear_b.z)
        apex, _ = _project(apex_b, yaw)
        _triangle(img, P2(base.x - 3.0, base.y + 2.0), P2(base.x + 3.0, base.y + 2.0), apex, (20, 20, 20))

    # Tail.
    tail_pts = [_project(body[k], yaw)[0] for k in ("tail0", "tail1", "tail2")]
    _line(img, tail_pts[0], tail_pts[1], 5.0, (32, 32, 32))
    _line(img, tail_pts[1], tail_pts[2], 4.0, (32, 32, 32))

    for depth, limb, root2, joint2, paw2, stance in projected_limbs[2:]:
        color = (18, 18, 18)
        _line(img, root2, joint2, 5.0, color)
        _line(img, joint2, paw2, 4.0, color)
        _ellipse(img, paw2.x + 1.0, paw2.y + 0.5, 3.2, 1.8, color)

    return img


def mask(img) -> frozenset[int]:
    out = set()
    for y, row in enumerate(img):
        for x, px in enumerate(row):
            if min(px) < 245:
                out.add(y * CANVAS_W + x)
    return frozenset(out)


def disagreement(a: frozenset[int], b: frozenset[int]) -> float:
    union = a | b
    return 0.0 if not union else len(a ^ b) / len(union)


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    idx = (len(xs) - 1) * p
    lo, hi = int(math.floor(idx)), int(math.ceil(idx))
    if lo == hi:
        return xs[lo]
    t = idx - lo
    return xs[lo] * (1.0 - t) + xs[hi] * t


def evaluate_direction_count(direction_count: int) -> dict:
    errors = []
    angular = []
    phases = [k / 8.0 for k in range(8)]
    yaws = [math.radians(k * 5.0) for k in range(72)]
    cache = {}
    for phase in phases:
        for yaw in yaws:
            qyaw = nearest_yaw(yaw, direction_count)
            key_ref = (round(yaw, 12), round(phase, 12))
            key_q = (round(qyaw, 12), round(phase, 12))
            if key_ref not in cache:
                cache[key_ref] = mask(render_reference(yaw, phase))
            if key_q not in cache:
                cache[key_q] = mask(render_reference(qyaw, phase))
            errors.append(disagreement(cache[key_ref], cache[key_q]))
            angular.append(angular_error_deg(yaw, qyaw))

    adjacent = []
    for phase in phases:
        masks = [mask(render_reference(2.0 * math.pi * k / direction_count, phase)) for k in range(direction_count)]
        adjacent.extend(disagreement(masks[k], masks[(k + 1) % direction_count]) for k in range(direction_count))

    return {
        "directionCount": direction_count,
        "assetDirections": direction_count,
        "maxAngularErrorDeg": max(angular),
        "meanMaskDisagreement": sum(errors) / len(errors),
        "p95MaskDisagreement": percentile(errors, 0.95),
        "meanAdjacentDirectionStep": sum(adjacent) / len(adjacent),
        "p95AdjacentDirectionStep": percentile(adjacent, 0.95),
    }


def evaluate_frame_count(frame_count: int) -> dict:
    errors = []
    support_mismatch = 0
    total = 0
    yaws = [math.radians(d) for d in (0, 30, 60, 90, 135, 180)]
    phases = [k / 128.0 for k in range(128)]
    cache = {}
    for yaw in yaws:
        for phase in phases:
            qphase = nearest_phase(phase, frame_count)
            kr = (round(yaw, 12), round(phase, 12))
            kq = (round(yaw, 12), round(qphase, 12))
            if kr not in cache:
                cache[kr] = mask(render_reference(yaw, phase))
            if kq not in cache:
                cache[kq] = mask(render_reference(yaw, qphase))
            errors.append(disagreement(cache[kr], cache[kq]))
            support_mismatch += int(support_state(phase) != support_state(qphase))
            total += 1

    seam_ratios = []
    for yaw in (0.0, math.radians(45), math.radians(90)):
        frames = [mask(render_reference(yaw, k / frame_count)) for k in range(frame_count)]
        steps = [disagreement(frames[k], frames[(k + 1) % frame_count]) for k in range(frame_count)]
        ordinary = steps[:-1]
        denom = percentile(ordinary, 0.5) or 1e-9
        seam_ratios.append(steps[-1] / denom)

    return {
        "frameCount": frame_count,
        "assetFramesPerDirection": frame_count,
        "maxPhaseQuantizationMs": 1000.0 * CYCLE_SECONDS / (2.0 * frame_count),
        "meanMaskDisagreement": sum(errors) / len(errors),
        "p95MaskDisagreement": percentile(errors, 0.95),
        "supportMismatchRate": support_mismatch / total,
        "maxLoopSeamToMedianStepRatio": max(seam_ratios),
    }


def evaluate_combined(direction_count: int, frame_count: int) -> dict:
    errors = []
    yaws = [math.radians(k * 10.0 + 2.5) for k in range(36)]
    phases = [(k + 0.37) / 48.0 for k in range(48)]
    cache = {}
    for yaw in yaws:
        for phase in phases:
            qyaw = nearest_yaw(yaw, direction_count)
            qphase = nearest_phase(phase, frame_count)
            kr = (round(yaw, 12), round(phase % 1.0, 12))
            kq = (round(qyaw, 12), round(qphase, 12))
            if kr not in cache:
                cache[kr] = mask(render_reference(yaw, phase))
            if kq not in cache:
                cache[kq] = mask(render_reference(qyaw, qphase))
            errors.append(disagreement(cache[kr], cache[kq]))
    return {
        "directionCount": direction_count,
        "frameCount": frame_count,
        "authoredFrameEquivalent": direction_count * frame_count,
        "meanCombinedDisagreement": sum(errors) / len(errors),
        "p95CombinedDisagreement": percentile(errors, 0.95),
    }


def rgb_bytes(img) -> bytes:
    out = bytearray()
    for row in img:
        for px in row:
            out.extend(px)
    return bytes(out)


def write_png(path: Path, img: list[list[list[int]]]):
    h, w = len(img), len(img[0])
    raw = bytearray()
    for row in img:
        raw.append(0)
        for px in row:
            raw.extend(px)
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    data += chunk(b"IEND", b"")
    path.write_bytes(data)


def make_strip(images: list[list[list[list[int]]]], scale: int = 1) -> list[list[list[int]]]:
    if not images:
        return []
    h, w = len(images[0]), len(images[0][0])
    out = [[[255, 255, 255] for _ in range(w * len(images) * scale)] for _ in range(h * scale)]
    for idx, img in enumerate(images):
        for y in range(h):
            for x in range(w):
                c = img[y][x]
                for yy in range(scale):
                    for xx in range(scale):
                        out[y * scale + yy][(idx * w + x) * scale + xx] = list(c)
    return out


def mechanical_experiment() -> dict:
    directions = [evaluate_direction_count(d) for d in DIRECTION_COUNTS]
    frames = [evaluate_frame_count(f) for f in FRAME_COUNTS]
    combined = [evaluate_combined(d, f) for d in DIRECTION_COUNTS for f in FRAME_COUNTS]
    return {
        "version": VERSION,
        "canvas": [CANVAS_W, CANVAS_H],
        "cycleSeconds": CYCLE_SECONDS,
        "stanceSeconds": STANCE_SECONDS,
        "swingSeconds": SWING_SECONDS,
        "stanceFraction": STANCE_FRACTION,
        "footfallOrder": list(LIMBS),
        "directionResults": directions,
        "frameResults": frames,
        "combinedResults": combined,
    }


def write_visual_evidence(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    phase = 0.125
    for d in DIRECTION_COUNTS:
        imgs = [render_reference(2.0 * math.pi * k / d, phase) for k in range(d)]
        write_png(out_dir / f"directions_D{d}_phase0125.png", make_strip(imgs))

    yaw = 0.0
    for f in FRAME_COUNTS:
        imgs = [render_reference(yaw, k / f) for k in range(f)]
        write_png(out_dir / f"profile_cycle_F{f}.png", make_strip(imgs))

    key_yaws = [math.radians(v) for v in (0, 30, 45, 60, 90)]
    key_phases = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
    key_imgs = [render_reference(y, p) for y in key_yaws for p in key_phases]
    write_png(out_dir / "continuous_reference_keyviews.png", make_strip(key_imgs))


def write_results(out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    result = mechanical_experiment()
    (out_dir / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

    lines = ["directions,frames,authored_frame_equivalent,mean_combined_disagreement,p95_combined_disagreement"]
    for row in result["combinedResults"]:
        lines.append(f"{row['directionCount']},{row['frameCount']},{row['authoredFrameEquivalent']},{row['meanCombinedDisagreement']:.9f},{row['p95CombinedDisagreement']:.9f}")
    (out_dir / "combined_matrix.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")

    write_visual_evidence(out_dir / "visual")
    return result
