from __future__ import annotations

import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from e_v0_fixture_adapter import H1, H4, H6N, H7, MORPHOLOGIES, build_e_fixture
from e_v0_profiles import M0
from e_v0_renderer_adapter import render_e
from run_c3_matrix import _bounds_svg, _shape_svg
from run_e_v0_structural_matrix import _contact_marker_svg

EVIDENCE_VERSION = "P1_F_PERCEPTUAL_EVIDENCE_V1"
PRIMARY_SIZE_DP = 80
FILMSTRIP_SAMPLES = {
    H4: tuple(i / 8.0 for i in range(9)),
    H6N: tuple(i / 10.0 for i in range(11)),
    H7: tuple(i / 8.0 for i in range(9)),
}


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _frame_svg(fixture, rendered, width, height):
    parts = [
        f'<line x1="0" y1="{height * 0.80:.4f}" x2="{width:.4f}" y2="{height * 0.80:.4f}" stroke="#c4c4c4" stroke-width="0.45"/>'
    ]
    for group, rect in sorted(rendered["partitionBounds"].items()):
        parts.append(_bounds_svg(rect, group))
    for shape in rendered["shapes"]:
        parts.append(_shape_svg(shape))
    parts.append(_contact_marker_svg(fixture))
    return "".join(parts)


def render_filmstrip(morphology, case_id: str, direction: int = +1):
    if case_id not in FILMSTRIP_SAMPLES:
        raise KeyError(case_id)
    if case_id != H6N and direction != +1:
        raise ValueError("only H6N has two perceptual turn directions")

    size_dp = PRIMARY_SIZE_DP
    times = FILMSTRIP_SAMPLES[case_id]
    cell_w = size_dp * 2.25
    cell_h = size_dp * 1.72
    left = 120.0
    top = 28.0
    width = left + len(times) * cell_w
    height = top + cell_h
    title = f"P1-F | {morphology.id} | {case_id} | {size_dp}dp | dir={direction:+d}"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="17" font-family="sans-serif" font-size="10">{escape(title)}</text>',
    ]
    semantic_hashes = []
    for index, t in enumerate(times):
        fixture = build_e_fixture(morphology, case_id, size_dp, t, direction)
        rendered = render_e(fixture)
        semantic_hashes.append(fixture.semantic_hash)
        x0 = left + index * cell_w
        parts.append(f'<text x="{x0 + 2:.4f}" y="17" font-family="sans-serif" font-size="7">t={t:.3f}</text>')
        parts.append(f'<g transform="translate({x0:.4f},{top:.4f})">')
        parts.append(_frame_svg(fixture, rendered, cell_w, cell_h))
        parts.append('</g>')
    parts.append('</svg>')
    return "\n".join(parts), semantic_hashes


def _overview_sample(label: str):
    if label == "neutral":
        return H1, 0.0, +1
    if label == "profile":
        return H6N, 0.0, +1
    if label == "three-quarter":
        return H6N, 0.4, +1
    if label == "front":
        return H6N, 1.0, +1
    raise KeyError(label)


def render_morphology_overview_80():
    labels = ("neutral", "profile", "three-quarter", "front")
    size_dp = 80
    cell_w = size_dp * 2.50
    cell_h = size_dp * 1.66
    left = 145.0
    top = 28.0
    width = left + len(labels) * cell_w
    height = top + len(MORPHOLOGIES) * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="6" y="17" font-family="sans-serif" font-size="10">P1-F | 80dp morphology comparison</text>',
    ]
    semantic_hashes = []
    for col, label in enumerate(labels):
        x0 = left + col * cell_w
        parts.append(f'<text x="{x0 + 3:.4f}" y="17" font-family="sans-serif" font-size="8">{escape(label)}</text>')
    for row, morphology in enumerate(MORPHOLOGIES):
        y0 = top + row * cell_h
        parts.append(f'<text x="5" y="{y0 + 13:.4f}" font-family="sans-serif" font-size="7">{escape(morphology.id)}</text>')
        for col, label in enumerate(labels):
            case_id, t, direction = _overview_sample(label)
            fixture = build_e_fixture(morphology, case_id, size_dp, t, direction)
            rendered = render_e(fixture)
            semantic_hashes.append(fixture.semantic_hash)
            x0 = left + col * cell_w
            parts.append(f'<g transform="translate({x0:.4f},{y0:.4f})">')
            parts.append(_frame_svg(fixture, rendered, cell_w, cell_h))
            parts.append('</g>')
    parts.append('</svg>')
    return "\n".join(parts), semantic_hashes


def render_scale_overview_m0():
    labels = ("neutral", "profile", "three-quarter", "front")
    sizes = (64, 80, 96)
    max_size = max(sizes)
    cell_w = max_size * 2.50
    cell_h = max_size * 1.66
    left = 95.0
    top = 28.0
    width = left + len(labels) * cell_w
    height = top + len(sizes) * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="6" y="17" font-family="sans-serif" font-size="10">P1-F | M0 scale comparison | geometry remains native dp</text>',
    ]
    semantic_hashes = []
    for col, label in enumerate(labels):
        x0 = left + col * cell_w
        parts.append(f'<text x="{x0 + 3:.4f}" y="17" font-family="sans-serif" font-size="8">{escape(label)}</text>')
    for row, size_dp in enumerate(sizes):
        y0 = top + row * cell_h
        parts.append(f'<text x="5" y="{y0 + 13:.4f}" font-family="sans-serif" font-size="8">{size_dp}dp</text>')
        for col, label in enumerate(labels):
            case_id, t, direction = _overview_sample(label)
            fixture = build_e_fixture(M0, case_id, size_dp, t, direction)
            rendered = render_e(fixture)
            semantic_hashes.append(fixture.semantic_hash)
            x0 = left + col * cell_w
            parts.append(f'<g transform="translate({x0:.4f},{y0:.4f})">')
            parts.append(_frame_svg(fixture, rendered, cell_w, cell_h))
            parts.append('</g>')
    parts.append('</svg>')
    return "\n".join(parts), semantic_hashes


def generate(output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    files = []
    frame_count = 0

    for morphology in MORPHOLOGIES:
        for case_id in (H4, H6N, H7):
            directions = (+1, -1) if case_id == H6N else (+1,)
            for direction in directions:
                svg, semantic_hashes = render_filmstrip(morphology, case_id, direction)
                path = out / f"P1F_{morphology.id}_{case_id}_dir{direction:+d}.svg"
                path.write_text(svg, encoding="utf-8")
                digest = hashlib.sha256(svg.encode("utf-8")).hexdigest()
                files.append({
                    "file": path.name,
                    "kind": "filmstrip",
                    "morphologyId": morphology.id,
                    "caseId": case_id,
                    "direction": direction,
                    "frameCount": len(semantic_hashes),
                    "semanticHashes": semantic_hashes,
                    "sha256": digest,
                })
                frame_count += len(semantic_hashes)

    svg, semantic_hashes = render_morphology_overview_80()
    path = out / "P1F_MORPHOLOGY_OVERVIEW_80dp.svg"
    path.write_text(svg, encoding="utf-8")
    files.append({
        "file": path.name,
        "kind": "morphology_overview",
        "frameCount": len(semantic_hashes),
        "semanticHashes": semantic_hashes,
        "sha256": hashlib.sha256(svg.encode("utf-8")).hexdigest(),
    })
    frame_count += len(semantic_hashes)

    svg, semantic_hashes = render_scale_overview_m0()
    path = out / "P1F_SCALE_OVERVIEW_M0.svg"
    path.write_text(svg, encoding="utf-8")
    files.append({
        "file": path.name,
        "kind": "scale_overview",
        "frameCount": len(semantic_hashes),
        "semanticHashes": semantic_hashes,
        "sha256": hashlib.sha256(svg.encode("utf-8")).hexdigest(),
    })
    frame_count += len(semantic_hashes)

    manifest = {
        "version": EVIDENCE_VERSION,
        "primarySizeDp": PRIMARY_SIZE_DP,
        "fileCount": len(files),
        "totalRenderedFrames": frame_count,
        "files": files,
    }
    manifest["manifestContentSha256"] = hashlib.sha256(canonical_bytes(files)).hexdigest()
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(json.dumps(generate(args.output_dir), indent=2, sort_keys=True))
