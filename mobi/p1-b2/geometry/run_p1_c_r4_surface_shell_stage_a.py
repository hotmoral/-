from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

from c3_semantic import canonical_bytes
from e_v0_fixture_adapter import H6N, build_e_fixture
from e_v0_profiles import M0, morphology_by_id
import p1_c_r2_minimal_volumetric_proxy_v1 as r2
import p1_c_r4_anatomy_aware_surface_shell_v1 as r4


RUN_VERSION = "P1_C_R4_SURFACE_SHELL_STAGE_A_EVIDENCE_V1"
PRIMARY_SIZE_DP = 80
VIEW_SAMPLES = (("PROFILE", 0.0), ("THREE_QUARTER", 0.5), ("FRONT", 1.0))


def _bounds(points):
    points = tuple(points)
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return min(xs), min(ys), max(xs), max(ys)


def _result_bounds(result, include_ears=True):
    return _bounds(r4.all_points(result, include_ears=include_ears))


def _points_attr(points, scale, tx, ty):
    return " ".join(f"{tx + scale * x:.4f},{ty + scale * y:.4f}" for x, y in points)


def _domain_primitives(result, domain):
    return tuple(primitive for primitive in r4.all_primitives(result) if primitive.domain == domain)


def _render_primitive(primitive, scale, tx, ty):
    return f'<polygon points="{_points_attr(primitive.points, scale, tx, ty)}" fill="#111"/>'


def _render_shell(fixture, cx, cy, display_scale=1.0, include_ears=True, section_debug=False):
    result = r4.build_shell(fixture)
    bounds = _result_bounds(result, include_ears=include_ears)
    bx = (bounds[0] + bounds[2]) * 0.5
    by = (bounds[1] + bounds[3]) * 0.5
    tx = cx - display_scale * bx
    ty = cy - display_scale * by
    parts = []

    morphology = morphology_by_id(fixture.morphology_id)
    tail_points = r2._tail_points(
        fixture.state.anchors["TAIL_ROOT"],
        float(fixture.size_dp),
        morphology.tail_length,
        result.yaw_rad,
    )
    tail_radius = float(fixture.size_dp) * r2.RATIOS["tail"]["radius"] * morphology.tail_thickness
    tail_path = " ".join(f"{tx + display_scale*x:.4f},{ty + display_scale*y:.4f}" for x, y in tail_points)
    parts.append(
        f'<polyline points="{tail_path}" fill="none" stroke="#111" '
        f'stroke-width="{2.0*tail_radius*display_scale:.4f}" stroke-linecap="round" stroke-linejoin="round"/>'
    )

    # Hind appendages are placed behind the continuous CORE shell.
    for domain in ("HIND_R", "HIND_L"):
        for primitive in _domain_primitives(result, domain):
            parts.append(_render_primitive(primitive, display_scale, tx, ty))

    for primitive in result.core_surface:
        parts.append(_render_primitive(primitive, display_scale, tx, ty))

    if include_ears:
        for primitive in result.ears:
            parts.append(_render_primitive(primitive, display_scale, tx, ty))

    # Fore appendages are placed over CORE; physical L/R identity is unchanged.
    for domain in ("FORE_R", "FORE_L"):
        for primitive in _domain_primitives(result, domain):
            parts.append(_render_primitive(primitive, display_scale, tx, ty))

    if section_debug:
        for ring in result.sections:
            parts.append(
                f'<polygon points="{_points_attr(ring.points, display_scale, tx, ty)}" '
                'fill="none" stroke="#777" stroke-width="0.55"/>'
            )
            parts.append(
                f'<circle cx="{tx + display_scale*ring.center[0]:.4f}" '
                f'cy="{ty + display_scale*ring.center[1]:.4f}" r="0.8" fill="#777"/>'
            )

    return "\n".join(parts)


def _sheet(title, samples, include_ears=True, true_scale=False, section_debug=False):
    cell_w = 126.0 if true_scale else 160.0
    cell_h = 118.0 if true_scale else 145.0
    top = 32.0
    width = len(samples) * cell_w
    height = top + cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="15" font-family="sans-serif" font-size="10" fill="#111">{escape(title)}</text>',
    ]
    for index, (label, fixture) in enumerate(samples):
        x0 = index * cell_w
        y0 = top
        parts.append(
            f'<text x="{x0 + 5:.4f}" y="{y0 + 10:.4f}" font-family="sans-serif" '
            f'font-size="7" fill="#333">{escape(label)}</text>'
        )
        parts.append(
            _render_shell(
                fixture,
                x0 + cell_w * 0.50,
                y0 + cell_h * 0.59,
                display_scale=1.0 if true_scale else 1.24,
                include_ears=include_ears,
                section_debug=section_debug,
            )
        )
    parts.append("</svg>")
    return "\n".join(parts)


def _stage_a_samples():
    return tuple(
        (label, build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, +1))
        for label, t in VIEW_SAMPLES
    )


def run_stage_a():
    records = []
    semantic_mutations = 0
    signatures = set()
    max_paw_pin = 0.0
    domain_counts = set()
    nonfinite = 0
    bounds_mismatches = 0

    for label, fixture in _stage_a_samples():
        before = canonical_bytes(fixture.payload)
        result = r4.build_shell(fixture)
        after = canonical_bytes(fixture.payload)
        if before != after:
            semantic_mutations += 1
        payload = r4.result_dict(fixture, result)
        payload["reviewLabel"] = label
        records.append(payload)
        signatures.add(result.signature)
        max_paw_pin = max(max_paw_pin, result.paw_pin_error)
        domain_counts.add(len(result.domain_bounds))
        if not payload["finite"]:
            nonfinite += 1
        for domain, rect in result.domain_bounds.items():
            for point in (p for primitive in r4.all_primitives(result) if primitive.domain == domain for p in primitive.points):
                if not (rect[0] - 1e-9 <= point[0] <= rect[2] + 1e-9 and rect[1] - 1e-9 <= point[1] <= rect[3] + 1e-9):
                    bounds_mismatches += 1
                    break

    summary = {
        "version": RUN_VERSION,
        "prototypeVersion": r4.PROTOTYPE_VERSION,
        "recordCount": len(records),
        "semanticMutationCount": semantic_mutations,
        "shellSignatureCount": len(signatures),
        "sectionCount": len(r4.SECTION_IDS),
        "sectionSamples": r4.SECTION_SAMPLES,
        "collarSamples": r4.COLLAR_SAMPLES,
        "externalDomainCounts": sorted(domain_counts),
        "maxPawPinError": max_paw_pin,
        "nonfiniteRecordCount": nonfinite,
        "domainBoundsMismatchCount": bounds_mismatches,
        "correctionUseCount": 0,
    }
    summary["mechanicalPass"] = bool(
        len(records) == 3
        and semantic_mutations == 0
        and len(signatures) == 1
        and len(r4.SECTION_IDS) == 9
        and r4.SECTION_SAMPLES == 8
        and r4.COLLAR_SAMPLES == 6
        and domain_counts == {6}
        and max_paw_pin <= 1e-9
        and nonfinite == 0
        and bounds_mismatches == 0
    )
    summary["recordContentSha256"] = hashlib.sha256(canonical_bytes(records)).hexdigest()
    return records, summary


def generate_stage_a_svgs(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    samples = _stage_a_samples()
    files = []

    path = output_dir / "P1CR4_V1_M0_VIEW_80dp_TRUE_SCALE.svg"
    path.write_text(
        _sheet("P1-C-R4 V1 | M0 profile→front | 80dp true scale", samples, true_scale=True),
        encoding="utf-8",
    )
    files.append(path)

    path = output_dir / "P1CR4_V1_M0_VIEW_80dp_REVIEW.svg"
    path.write_text(
        _sheet("P1-C-R4 V1 | M0 profile→front | 80dp neutral structural review", samples),
        encoding="utf-8",
    )
    files.append(path)

    earless = tuple((label + " EAR-NEUTRAL", fixture) for label, fixture in samples[1:])
    path = output_dir / "P1CR4_V1_M0_EAR_NEUTRALIZED_80dp.svg"
    path.write_text(
        _sheet("P1-C-R4 V1 | diagnostic only | ears hidden, shell unchanged", earless, include_ears=False),
        encoding="utf-8",
    )
    files.append(path)

    path = output_dir / "P1CR4_V1_M0_SECTION_DIAGNOSTIC_80dp.svg"
    path.write_text(
        _sheet("P1-C-R4 V1 | nine fixed section rings | diagnostic overlay", samples, section_debug=True),
        encoding="utf-8",
    )
    files.append(path)

    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    records, summary = run_stage_a()
    (out / "records.json").write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    svgs = generate_stage_a_svgs(out / "debug")
    manifest = {
        "version": RUN_VERSION,
        "prototypeVersion": r4.PROTOTYPE_VERSION,
        "summary": summary,
        "debugSvgs": [
            {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in sorted(svgs)
        ],
    }
    manifest["manifestContentSha256"] = hashlib.sha256(canonical_bytes(manifest)).hexdigest()
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    if not summary["mechanicalPass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
