from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import zlib

from c3_semantic import canonical_bytes
from e_v0_fixture_adapter import H6N, build_e_fixture
from e_v0_profiles import M0
import p1_c_r8_regional_grammar_v1 as grammar
import p1_c_r8_neutral_m0_params_v1 as neutral
import p1_c_r8_regional_procedural_surface_v1 as r8


RUN_VERSION = "P1_C_R8_REGIONAL_PROCEDURAL_STAGE3_EVIDENCE_V1"
PRIMARY_SIZE_DP = 80
VIEW_SAMPLES = (("PROFILE", 0.0), ("THREE_QUARTER", 0.5), ("FRONT", 1.0))

REGION_COLORS = {
    "CRANIUM_MUZZLE": (71, 85, 105, 255),
    "CERVICAL_NECK": (112, 126, 142, 255),
    "SHOULDER_CHEST": (111, 94, 84, 255),
    "THORAX_FLANK": (133, 119, 102, 255),
    "ABDOMEN_TUCK": (148, 137, 118, 255),
    "PELVIS_HAUNCH": (100, 91, 111, 255),
    "FORE_L_PROXIMAL": (98, 117, 112, 255),
    "FORE_R_PROXIMAL": (98, 117, 112, 255),
    "HIND_L_PROXIMAL": (116, 104, 124, 255),
    "HIND_R_PROXIMAL": (116, 104, 124, 255),
}
BLACK = (18, 18, 18, 255)
MID = (80, 80, 80, 255)
WHITE = (255, 255, 255, 255)


def _png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def write_png(path: Path, width: int, height: int, pixels: bytes):
    if len(pixels) != width * height * 4:
        raise ValueError("RGBA buffer size mismatch")
    raw = bytearray()
    stride = width * 4
    for row in range(height):
        raw.append(0)
        start = row * stride
        raw.extend(pixels[start:start + stride])
    payload = (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + _png_chunk(b"IEND", b"")
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _blank(width: int, height: int):
    return bytearray(WHITE * (width * height))


def _set_pixel(pixels: bytearray, width: int, height: int, x: int, y: int, color):
    if 0 <= x < width and 0 <= y < height:
        idx = (y * width + x) * 4
        pixels[idx:idx + 4] = bytes(color)


def _world_to_pixel(bounds, width, height, point):
    min_x, min_y, max_x, max_y = bounds
    x = (float(point[0]) - min_x) / max(max_x - min_x, 1e-12) * width
    y = (float(point[1]) - min_y) / max(max_y - min_y, 1e-12) * height
    return x, y


def _point_in_polygon(x: float, y: float, points):
    inside = False
    j = len(points) - 1
    for i in range(len(points)):
        xi, yi = points[i]
        xj, yj = points[j]
        intersects = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) if abs(yj - yi) > 1e-12 else 1e-12) + xi
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def _fill_polygon(pixels, width, height, bounds, world_points, color):
    points = tuple(_world_to_pixel(bounds, width, height, point) for point in world_points)
    if len(points) < 3:
        return
    min_x = max(0, int(math.floor(min(x for x, _ in points))) - 1)
    max_x = min(width - 1, int(math.ceil(max(x for x, _ in points))) + 1)
    min_y = max(0, int(math.floor(min(y for _, y in points))) - 1)
    max_y = min(height - 1, int(math.ceil(max(y for _, y in points))) + 1)
    for py in range(min_y, max_y + 1):
        cy = py + 0.5
        for px in range(min_x, max_x + 1):
            if _point_in_polygon(px + 0.5, cy, points):
                _set_pixel(pixels, width, height, px, py, color)


def _fill_body(pixels, raster, diagnostic=False):
    width, height = raster.width, raster.height
    for idx, value in enumerate(raster.mask):
        if not value:
            continue
        y, x = divmod(idx, width)
        color = REGION_COLORS.get(raster.contributor[idx], MID) if diagnostic else BLACK
        _set_pixel(pixels, width, height, x, y, color)


def _render(fixture, result, raster, include_ears=True, diagnostic=False):
    width, height = raster.width, raster.height
    pixels = _blank(width, height)
    bounds = raster.world_bounds

    _fill_polygon(pixels, width, height, bounds, result.tail.points, BLACK if not diagnostic else MID)

    for primitive in result.limbs + result.paws:
        if primitive.domain.startswith("HIND"):
            _fill_polygon(pixels, width, height, bounds, primitive.points, BLACK if not diagnostic else MID)

    _fill_body(pixels, raster, diagnostic=diagnostic)

    if include_ears:
        for primitive in result.ears:
            _fill_polygon(pixels, width, height, bounds, primitive.points, BLACK if not diagnostic else REGION_COLORS["CRANIUM_MUZZLE"])

    for primitive in result.limbs + result.paws:
        if primitive.domain.startswith("FORE"):
            _fill_polygon(pixels, width, height, bounds, primitive.points, BLACK if not diagnostic else MID)

    return bytes(pixels)


def _compose_horizontal(images, gap=8):
    if not images:
        raise ValueError("images required")
    heights = {height for _, height, _ in images}
    if len(heights) != 1:
        raise ValueError("equal image heights required")
    height = heights.pop()
    width = sum(w for w, _, _ in images) + gap * (len(images) - 1)
    out = _blank(width, height)
    cursor = 0
    for image_width, _, data in images:
        for y in range(height):
            src_start = y * image_width * 4
            dst_start = (y * width + cursor) * 4
            out[dst_start:dst_start + image_width * 4] = data[src_start:src_start + image_width * 4]
        cursor += image_width + gap
    return width, height, bytes(out)


def _primitive_bounds_mismatch(result, raster):
    min_x, min_y, max_x, max_y = raster.world_bounds
    mismatches = 0
    for primitive in r8.all_primitives(result):
        for x, y in primitive.points:
            if not (min_x - 1e-9 <= x <= max_x + 1e-9 and min_y - 1e-9 <= y <= max_y + 1e-9):
                mismatches += 1
                break
    return mismatches


def _record_content_sha(records):
    return hashlib.sha256(
        b"\n".join(json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8") for record in records)
    ).hexdigest()


def run_stage3(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    debug_dir = output_dir / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)

    records = []
    semantic_mutations = 0
    surface_signatures = set()
    grammar_signatures = set()
    parameter_signatures = set()
    max_paw_pin = 0.0
    nonfinite = 0
    interface_failures = 0
    sampling_bounds_mismatches = 0
    occupied_counts = []
    normal_images = []
    diagnostic_images = []
    ear_images = {}

    for label, t in VIEW_SAMPLES:
        fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, +1)
        before = canonical_bytes(fixture.payload)
        result = r8.build_surface(fixture)
        raster = r8.rasterize_body(fixture)
        after = canonical_bytes(fixture.payload)
        if before != after:
            semantic_mutations += 1

        payload = r8.result_dict(fixture, result, raster)
        payload["reviewLabel"] = label
        records.append(payload)

        surface_signatures.add(result.signature)
        grammar_signatures.add(result.grammar_signature)
        parameter_signatures.add(result.parameter_signature)
        max_paw_pin = max(max_paw_pin, result.paw_pin_error)
        if not payload["finite"]:
            nonfinite += 1
        if not result.interface_overlap_pass:
            interface_failures += 1
        sampling_bounds_mismatches += _primitive_bounds_mismatch(result, raster)
        occupied_counts.append(raster.occupied_pixel_count)

        normal = _render(fixture, result, raster, include_ears=True, diagnostic=False)
        diagnostic = _render(fixture, result, raster, include_ears=False, diagnostic=True)
        normal_images.append((raster.width, raster.height, normal))
        diagnostic_images.append((raster.width, raster.height, diagnostic))

        write_png(debug_dir / f"P1CR8_{label}.png", raster.width, raster.height, normal)
        write_png(debug_dir / f"P1CR8_REGION_{label}.png", raster.width, raster.height, diagnostic)

        if label in ("THREE_QUARTER", "FRONT"):
            ear_neutral = _render(fixture, result, raster, include_ears=False, diagnostic=False)
            ear_images[label] = (raster.width, raster.height, ear_neutral)
            write_png(debug_dir / f"P1CR8_EAR_NEUTRALIZED_{label}.png", raster.width, raster.height, ear_neutral)

    review_w, review_h, review = _compose_horizontal(normal_images)
    write_png(debug_dir / "P1CR8_REVIEW_SHEET.png", review_w, review_h, review)

    diag_w, diag_h, diag = _compose_horizontal(diagnostic_images)
    write_png(debug_dir / "P1CR8_REGION_DIAGNOSTIC_SHEET.png", diag_w, diag_h, diag)

    ear_order = [ear_images["THREE_QUARTER"], ear_images["FRONT"]]
    ear_w, ear_h, ear_sheet = _compose_horizontal(ear_order)
    write_png(debug_dir / "P1CR8_EAR_NEUTRALIZED_SHEET.png", ear_w, ear_h, ear_sheet)

    write_png(
        debug_dir / "P1CR8_PROXIMAL_EMERGENCE_DIAGNOSTIC.png",
        diagnostic_images[1][0],
        diagnostic_images[1][1],
        diagnostic_images[1][2],
    )

    records_path = output_dir / "records.jsonl"
    records_path.write_text(
        "".join(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n" for record in records),
        encoding="utf-8",
    )

    summary = {
        "version": RUN_VERSION,
        "prototypeVersion": r8.PROTOTYPE_VERSION,
        "sourceFamily": r8.SOURCE_FAMILY,
        "sourcePackId": r8.SOURCE_PACK_ID,
        "recordCount": len(records),
        "semanticMutationCount": semantic_mutations,
        "surfaceSignatureCount": len(surface_signatures),
        "grammarSignatureCount": len(grammar_signatures),
        "parameterSignatureCount": len(parameter_signatures),
        "grammarSignature": grammar.grammar_signature(),
        "parameterSignature": neutral.parameter_signature(),
        "authoritativeRegionFunctionCount": len(grammar.REGIONS),
        "authoritativeRegionScalarCount": grammar.region_parameter_count(),
        "authoritativeBlendInterfaceCount": len(grammar.BLEND_INTERFACES),
        "authoritativeScalarCount": grammar.authoritative_scalar_count(),
        "derivedSubdivisionSteps": r8.DERIVED_SUBDIVISION_STEPS,
        "externalDomainCounts": [len(r8.EXTERNAL_DOMAINS)],
        "maxPawPinError": max_paw_pin,
        "nonfiniteRecordCount": nonfinite,
        "interfaceFailureRecordCount": interface_failures,
        "samplingBoundsMismatchCount": sampling_bounds_mismatches,
        "correctionUseCount": r8.CORRECTION_USE_COUNT,
        "occupiedPixelCounts": occupied_counts,
        "recordContentSha256": _record_content_sha(records),
    }
    summary["mechanicalPass"] = all((
        summary["recordCount"] == 3,
        summary["semanticMutationCount"] == 0,
        summary["surfaceSignatureCount"] == 1,
        summary["grammarSignatureCount"] == 1,
        summary["parameterSignatureCount"] == 1,
        summary["authoritativeRegionFunctionCount"] == 8,
        summary["authoritativeRegionScalarCount"] == 54,
        summary["authoritativeBlendInterfaceCount"] == 7,
        summary["authoritativeScalarCount"] == 61,
        summary["externalDomainCounts"] == [6],
        summary["maxPawPinError"] <= 1e-9,
        summary["nonfiniteRecordCount"] == 0,
        summary["interfaceFailureRecordCount"] == 0,
        summary["samplingBoundsMismatchCount"] == 0,
        summary["correctionUseCount"] == 0,
        all(count > 0 for count in summary["occupiedPixelCounts"]),
    ))
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "review_manifest.json").write_text(
        json.dumps(
            {
                "viewOrder": [label for label, _ in VIEW_SAMPLES],
                "reviewSheet": "debug/P1CR8_REVIEW_SHEET.png",
                "earNeutralizedOrder": ["THREE_QUARTER", "FRONT"],
                "earNeutralizedSheet": "debug/P1CR8_EAR_NEUTRALIZED_SHEET.png",
                "regionDiagnosticOrder": [label for label, _ in VIEW_SAMPLES],
                "regionDiagnosticSheet": "debug/P1CR8_REGION_DIAGNOSTIC_SHEET.png",
                "proximalDiagnostic": "debug/P1CR8_PROXIMAL_EMERGENCE_DIAGNOSTIC.png",
                "appearance": "UNSHADED_STRUCTURE_ONLY",
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    summary = run_stage3(Path(args.output_dir))
    print(json.dumps(summary, indent=2, sort_keys=True))
    if not summary["mechanicalPass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
