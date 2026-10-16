from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

from c3_semantic import canonical_bytes
from e_v0_fixture_adapter import H1, H4, H5, H6N, H7, build_e_fixture, iter_invariant_fixtures
from e_v0_profiles import M0, MORPHOLOGIES, morphology_by_id
import p1_c_r2_minimal_volumetric_proxy_v1 as r2


RUN_VERSION = "P1_C_R2_MINIMAL_VOLUMETRIC_PROXY_EVIDENCE_V1"
PRIMARY_SIZE_DP = 80


def _domain_points(result, domain: str):
    points = []
    for primitive in result.core_primitives + result.ears + result.limbs + result.paws + (result.tail,):
        if primitive.domain == domain:
            points.extend(primitive.points)
    return points


def _bounds_contains(rect, point, eps=1e-9):
    return rect[0] - eps <= point[0] <= rect[2] + eps and rect[1] - eps <= point[1] <= rect[3] + eps


def _primitive_width(primitive):
    xs = [p[0] for p in primitive.points]
    return max(xs) - min(xs)


def _front_mass_ratios():
    fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, 1.0, +1)
    result = r2.build_proxy(fixture)
    by_id = {p.id: p for p in result.core_primitives}
    cranium = _primitive_width(by_id["CRANIUM_VOLUME"])
    cervical = _primitive_width(by_id["CERVICAL_VOLUME"])
    thorax = _primitive_width(by_id["THORAX_VOLUME"])
    return {
        "craniumWidthDp": cranium,
        "cervicalWidthDp": cervical,
        "thoraxWidthDp": thorax,
        "craniumToCervicalWidthRatio": cranium / cervical if cervical else float("inf"),
        "thoraxToCervicalWidthRatio": thorax / cervical if cervical else float("inf"),
        "thoraxToCraniumWidthRatio": thorax / cranium if cranium else float("inf"),
    }


def run_matrix():
    records = []
    semantic_mutations = 0
    nonfinite = 0
    bounds_mismatches = 0
    max_paw_pin = 0.0
    signatures = set()
    domain_counts = set()
    correction_uses = 0
    h4_records = 0
    max_normalized_visual_width = 0.0
    max_normalized_visual_height = 0.0
    h6n_sequences = {}

    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        before = canonical_bytes(fixture.payload)
        result = r2.build_proxy(fixture)
        after = canonical_bytes(fixture.payload)
        if before != after:
            semantic_mutations += 1
        payload = r2.result_dict(fixture, result)
        payload["direction"] = int(direction)
        records.append(payload)
        signatures.add(result.signature)
        domain_counts.add(len(result.domain_bounds))
        max_paw_pin = max(max_paw_pin, result.paw_pin_error)
        correction_uses += int(payload["correctionUseCount"])
        if case_id == H4:
            h4_records += 1
        if not payload["finite"]:
            nonfinite += 1
        for domain, rect in result.domain_bounds.items():
            for point in _domain_points(result, domain):
                if not _bounds_contains(rect, point):
                    bounds_mismatches += 1
                    break
        width = result.visual_bounds[2] - result.visual_bounds[0]
        height = result.visual_bounds[3] - result.visual_bounds[1]
        max_normalized_visual_width = max(max_normalized_visual_width, width / float(size_dp))
        max_normalized_visual_height = max(max_normalized_visual_height, height / float(size_dp))
        if case_id == H6N:
            key = (morphology.id, int(size_dp), int(direction))
            h6n_sequences.setdefault(key, []).append((float(fixture.t), width, height))

    max_width_step = 0.0
    max_height_step = 0.0
    for (morphology_id, size_dp, direction), sequence in h6n_sequences.items():
        sequence.sort()
        for (_, w0, h0), (_, w1, h1) in zip(sequence, sequence[1:]):
            max_width_step = max(max_width_step, abs(w1 - w0) / float(size_dp))
            max_height_step = max(max_height_step, abs(h1 - h0) / float(size_dp))

    record_content_sha = hashlib.sha256(canonical_bytes(records)).hexdigest()
    summary = {
        "version": RUN_VERSION,
        "prototypeVersion": r2.PROTOTYPE_VERSION,
        "recordCount": len(records),
        "semanticMutationCount": semantic_mutations,
        "nonfiniteRecordCount": nonfinite,
        "domainBoundsMismatchCount": bounds_mismatches,
        "maxPawPinError": max_paw_pin,
        "proxySignatureCount": len(signatures),
        "externalDomainCounts": sorted(domain_counts),
        "correctionUseCount": correction_uses,
        "nativeH4RecordCount": h4_records,
        "maxNormalizedVisualWidth": max_normalized_visual_width,
        "maxNormalizedVisualHeight": max_normalized_visual_height,
        "maxNormalizedH6NWidthStep": max_width_step,
        "maxNormalizedH6NHeightStep": max_height_step,
        "frontMassRatiosM0_80dp": _front_mass_ratios(),
        "recordContentSha256": record_content_sha,
    }
    summary["mechanicalPass"] = bool(
        summary["recordCount"] == 1770
        and semantic_mutations == 0
        and nonfinite == 0
        and bounds_mismatches == 0
        and max_paw_pin <= 1e-9
        and len(signatures) == 1
        and domain_counts == {6}
        and correction_uses == 0
        and max_width_step <= 0.10
        and max_height_step <= 0.10
    )
    return records, summary


def _points_attr(points, scale, tx, ty):
    return " ".join(f"{tx + scale * x:.4f},{ty + scale * y:.4f}" for x, y in points)


def _result_bounds(result, include_ears=True):
    points = list(r2.all_points(result, include_ears=include_ears))
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def _render_proxy(fixture, cx, cy, display_scale=1.0, include_ears=True):
    result = r2.build_proxy(fixture)
    bounds = _result_bounds(result, include_ears=include_ears)
    bx = (bounds[0] + bounds[2]) * 0.5
    by = (bounds[1] + bounds[3]) * 0.5
    tx = cx - display_scale * bx
    ty = cy - display_scale * by
    parts = []

    # Tail is rendered as the actual derived curved capsule centerline rather
    # than its conservative convex bounds hull.
    morphology = morphology_by_id(fixture.morphology_id)
    tail_points = r2._tail_points(
        fixture.state.anchors["TAIL_ROOT"], float(fixture.size_dp), morphology.tail_length, result.yaw_rad
    )
    tail_radius = float(fixture.size_dp) * r2.RATIOS["tail"]["radius"] * morphology.tail_thickness
    tail_path = " ".join(f"{tx + display_scale*x:.4f},{ty + display_scale*y:.4f}" for x, y in tail_points)
    parts.append(
        f'<polyline points="{tail_path}" fill="none" stroke="#111" stroke-width="{2.0*tail_radius*display_scale:.4f}" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
    )

    # Hind limbs behind the body.
    for primitive in result.limbs + result.paws:
        if primitive.domain.startswith("HIND"):
            parts.append(f'<polygon points="{_points_attr(primitive.points, display_scale, tx, ty)}" fill="#111"/>')

    for primitive in result.core_primitives:
        parts.append(f'<polygon points="{_points_attr(primitive.points, display_scale, tx, ty)}" fill="#111"/>')
    if include_ears:
        for primitive in result.ears:
            parts.append(f'<polygon points="{_points_attr(primitive.points, display_scale, tx, ty)}" fill="#111"/>')

    # Fore limbs after CORE. All acceptance geometry stays monochrome.
    for primitive in result.limbs + result.paws:
        if primitive.domain.startswith("FORE"):
            parts.append(f'<polygon points="{_points_attr(primitive.points, display_scale, tx, ty)}" fill="#111"/>')
    return "\n".join(parts)


def _sheet(title, samples, rows=1, include_ears=True, true_scale=False):
    cell_w = 122.0 if true_scale else 150.0
    cell_h = 112.0 if true_scale else 135.0
    top = 32.0
    cols = int(math.ceil(len(samples) / rows))
    width = cols * cell_w
    height = top + rows * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="15" font-family="sans-serif" font-size="10" fill="#111">{escape(title)}</text>',
    ]
    for index, (label, fixture) in enumerate(samples):
        row = index // cols
        col = index % cols
        x0 = col * cell_w
        y0 = top + row * cell_h
        parts.append(f'<text x="{x0 + 5:.4f}" y="{y0 + 10:.4f}" font-family="sans-serif" font-size="7" fill="#333">{escape(label)}</text>')
        parts.append(_render_proxy(
            fixture,
            x0 + cell_w * 0.50,
            y0 + cell_h * 0.58,
            display_scale=1.0 if true_scale else 1.18,
            include_ears=include_ears,
        ))
    parts.append("</svg>")
    return "\n".join(parts)


def _morphology_sheet():
    views = (("PROFILE", 0.0), ("3Q", 0.5), ("FRONT", 1.0))
    samples = []
    for morphology in MORPHOLOGIES:
        for label, t in views:
            samples.append((f"{morphology.id} | {label}", build_e_fixture(morphology, H6N, 80, t, +1)))
    return _sheet("P1-C-R2 V1 | shared volumetric morphology reuse | 80dp", samples, rows=len(MORPHOLOGIES))


def generate_debug_svgs(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    files = []

    views = [(label, build_e_fixture(M0, H6N, 80, t, +1)) for label, t in (("PROFILE", 0.0), ("3Q", 0.5), ("FRONT", 1.0))]
    path = output_dir / "P1CR2_V1_M0_VIEW_80dp_TRUE_SCALE.svg"
    path.write_text(_sheet("P1-C-R2 V1 | M0 profile→front | 80dp true scale", views, true_scale=True), encoding="utf-8")
    files.append(path)

    path = output_dir / "P1CR2_V1_M0_VIEW_80dp_REVIEW.svg"
    path.write_text(_sheet("P1-C-R2 V1 | M0 profile→front | 80dp neutral", views), encoding="utf-8")
    files.append(path)

    earless = [(label, build_e_fixture(M0, H6N, 80, t, +1)) for label, t in (("3Q EAR-NEUTRAL", 0.5), ("FRONT EAR-NEUTRAL", 1.0))]
    path = output_dir / "P1CR2_V1_M0_EAR_NEUTRALIZED_80dp.svg"
    path.write_text(_sheet("P1-C-R2 V1 | diagnostic only | ears hidden, body unchanged", earless, include_ears=False), encoding="utf-8")
    files.append(path)

    h4 = [(f"H4 t={t:.2f}", build_e_fixture(M0, H4, 80, t, +1)) for t in (0.0, 0.25, 0.5, 0.75, 1.0)]
    path = output_dir / "P1CR2_V1_M0_H4_NATIVE_80dp.svg"
    path.write_text(_sheet("P1-C-R2 V1 | M0 H4 native / no inherited correction | 80dp", h4), encoding="utf-8")
    files.append(path)

    h5 = [("H5 crouch", build_e_fixture(M0, H5, 80, 0.0, +1))]
    path = output_dir / "P1CR2_V1_M0_H5_80dp.svg"
    path.write_text(_sheet("P1-C-R2 V1 | M0 H5 crouch | 80dp", h5), encoding="utf-8")
    files.append(path)

    for direction in (+1, -1):
        samples = [(f"t={t:.2f}", build_e_fixture(M0, H6N, 80, t, direction)) for t in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)]
        path = output_dir / f"P1CR2_V1_M0_H6N_DIR{direction:+d}_80dp.svg"
        path.write_text(_sheet(f"P1-C-R2 V1 | M0 H6N dir={direction:+d} | 80dp", samples), encoding="utf-8")
        files.append(path)

    h7 = [(f"H7 t={t:.2f}", build_e_fixture(M0, H7, 80, t, +1)) for t in (0.0, 0.25, 0.5, 0.75, 1.0)]
    path = output_dir / "P1CR2_V1_M0_H7_80dp.svg"
    path.write_text(_sheet("P1-C-R2 V1 | M0 H7 narrow support | 80dp", h7), encoding="utf-8")
    files.append(path)

    path = output_dir / "P1CR2_V1_MORPHOLOGY_REUSE_80dp.svg"
    path.write_text(_morphology_sheet(), encoding="utf-8")
    files.append(path)
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    records, summary = run_matrix()
    (out / "records.json").write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    svgs = generate_debug_svgs(out / "debug")
    manifest = {
        "version": RUN_VERSION,
        "prototypeVersion": r2.PROTOTYPE_VERSION,
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
        raise SystemExit("P1-C-R2 V1 mechanical invariant lane failed")


if __name__ == "__main__":
    main()
