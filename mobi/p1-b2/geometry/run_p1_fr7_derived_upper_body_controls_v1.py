from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from e_v0_fixture_adapter import H4, H6N, H7, build_e_fixture, iter_invariant_fixtures
from e_v0_profiles import M0, MORPHOLOGIES
import p1_fr5_core_mass_silhouette_v1 as fr5
import p1_fr7_derived_upper_body_controls_v1 as fr7
import run_p1_fr4_internal_core_scaffold as fr4_render
import run_p1_fr5_core_mass_silhouette_v1 as fr5_run


RUN_VERSION = "P1_FR7_DERIVED_UPPER_BODY_CONTROLS_EVIDENCE_V1"
PRIMARY_SIZE_DP = 80
FROZEN_FR5_V1 = {
    "publicRepository": "hotmoral/-",
    "publicHead": "e35cece023f3ba730d3492aea57b33022cb66dba",
    "runId": 38810438714,
    "jobId": 116682005960,
    "artifactId": 12008197681,
    "artifactDigest": "sha256:e49a9b31b47b321ab0ee9b548b80e35ba3bcbb6f7478b818875abc07bd8cc205",
    "recordContentSha256": "b1804e5d213710a0f2892c0988adde24d75476dd288b840ea28a72e275815a6b",
}


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def run_matrix():
    original = fr5_run.fr5
    original_version = fr5_run.RUN_VERSION
    try:
        fr5_run.fr5 = fr7
        fr5_run.RUN_VERSION = RUN_VERSION
        records, summary = fr5_run.run_matrix()
    finally:
        fr5_run.fr5 = original
        fr5_run.RUN_VERSION = original_version

    minimum_corridor_margin = min(float(r["priorFoldCorridorMargin"]) for r in records)
    fr5_ear_regression_records = 0
    fr5_corridor_min = float("inf")
    for _case_id, _morphology, _size_dp, direction, fixture in iter_invariant_fixtures():
        current = fr7.build_probe(fixture, direction)
        prior = fr5.build_probe(fixture, direction)
        if current.ear_base_outside_final > prior.ear_base_outside_final:
            fr5_ear_regression_records += 1
        fr5_corridor_min = min(fr5_corridor_min, fr7.prior_fold_corridor_margin(prior.base.core_vertices))

    if "fr5StressLimbCrossingCount" in summary:
        summary["fr7StressLimbCrossingCount"] = summary.pop("fr5StressLimbCrossingCount")
    summary["version"] = RUN_VERSION
    summary["prototypeVersion"] = fr7.PROTOTYPE_VERSION
    summary["minimumPriorFoldCorridorMarginDp"] = minimum_corridor_margin
    summary["fr5V1MinimumPriorFoldCorridorMarginDp"] = fr5_corridor_min
    summary["earAttachmentRegressionRecordCountVsFr5V1"] = fr5_ear_regression_records
    summary["structuralPass"] = bool(
        summary["structuralPass"]
        and minimum_corridor_margin > 1e-9
        and fr5_ear_regression_records == 0
    )
    return records, summary


def _normalized_probe_group(fixture, probe, x: float, y: float):
    root = fixture.state.anchors["BODY_ROOT"]
    return fr4_render.render_base._mesh_group_svg(fixture, probe, x - root.x, y - root.y, True)


def _three_way_sheet(samples, title: str):
    cell_w = 190.0
    cell_h = 125.0
    left = 86.0
    top = 30.0
    width = left + len(samples) * cell_w
    height = top + 3 * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="17" font-family="sans-serif" font-size="10">{escape(title)}</text>',
        f'<text x="6" y="{top + 16:.4f}" font-family="sans-serif" font-size="8">FR3 V5</text>',
        f'<text x="6" y="{top + cell_h + 16:.4f}" font-family="sans-serif" font-size="8">FR5 V1</text>',
        f'<text x="6" y="{top + 2 * cell_h + 16:.4f}" font-family="sans-serif" font-size="8">FR7 V1</text>',
    ]
    for col, (label, fixture, direction) in enumerate(samples):
        control = fr7.build_probe(fixture, direction).control
        prior = fr5.build_probe(fixture, direction).base
        current = fr7.build_probe(fixture, direction).base
        x0 = left + col * cell_w
        parts.append(f'<text x="{x0 + 4:.4f}" y="17" font-family="sans-serif" font-size="7">{escape(label)}</text>')
        parts.append(_normalized_probe_group(fixture, control, x0 + cell_w * 0.50, top + cell_h * 0.52))
        parts.append(_normalized_probe_group(fixture, prior, x0 + cell_w * 0.50, top + cell_h * 1.52))
        parts.append(_normalized_probe_group(fixture, current, x0 + cell_w * 0.50, top + cell_h * 2.52))
    parts.append("</svg>")
    return "\n".join(parts)


def _view_sheet():
    samples = []
    for label, t in (("profile", 0.0), ("3Q", 0.5), ("front", 1.0)):
        fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, +1)
        samples.append((label, fixture, +1))
    return _three_way_sheet(samples, "P1-FR7 | M0 view progression | 80dp | FR3 vs FR5 vs FR7")


def _morphology_sheet():
    views = (("profile", 0.0), ("3Q", 0.5), ("front", 1.0))
    cell_w = 190.0
    cell_h = 125.0
    left = 150.0
    top = 30.0
    width = left + len(views) * cell_w
    height = top + len(MORPHOLOGIES) * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="6" y="17" font-family="sans-serif" font-size="10">P1-FR7 | shared derived-control morphology reuse | 80dp</text>',
    ]
    for col, (label, _) in enumerate(views):
        parts.append(f'<text x="{left + col * cell_w + 4:.4f}" y="17" font-family="sans-serif" font-size="8">{escape(label)}</text>')
    for row, morphology in enumerate(MORPHOLOGIES):
        y0 = top + row * cell_h
        parts.append(f'<text x="5" y="{y0 + 16:.4f}" font-family="sans-serif" font-size="7">{escape(morphology.id)}</text>')
        for col, (_, t) in enumerate(views):
            fixture = build_e_fixture(morphology, H6N, PRIMARY_SIZE_DP, t, +1)
            current = fr7.build_probe(fixture, +1).base
            parts.append(_normalized_probe_group(
                fixture, current, left + col * cell_w + cell_w * 0.50, y0 + cell_h * 0.52
            ))
    parts.append("</svg>")
    return "\n".join(parts)


def generate_debug_svgs(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    files = []
    path = output_dir / "P1FR7_M0_VIEW_FR3_FR5_FR7_80dp.svg"
    path.write_text(_view_sheet(), encoding="utf-8")
    files.append(path)

    h4 = []
    for t in (0.0, 0.25, 0.50, 0.75, 1.0):
        h4.append((f"t={t:.2f}", build_e_fixture(M0, H4, PRIMARY_SIZE_DP, t, +1), +1))
    path = output_dir / "P1FR7_M0_H4_FR3_FR5_FR7_80dp.svg"
    path.write_text(_three_way_sheet(h4, "P1-FR7 | M0 H4 sit-to-stand | 80dp"), encoding="utf-8")
    files.append(path)

    for direction in (+1, -1):
        samples = []
        for t in (0.0, 0.20, 0.40, 0.60, 0.80, 1.0):
            samples.append((f"t={t:.2f}", build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, direction), direction))
        path = output_dir / f"P1FR7_M0_H6N_DIR{direction:+d}_FR3_FR5_FR7_80dp.svg"
        path.write_text(_three_way_sheet(samples, f"P1-FR7 | M0 H6N dir={direction:+d} | 80dp"), encoding="utf-8")
        files.append(path)

    h7 = []
    for t in (0.0, 0.25, 0.50, 0.75, 1.0):
        h7.append((f"t={t:.2f}", build_e_fixture(M0, H7, PRIMARY_SIZE_DP, t, +1), +1))
    path = output_dir / "P1FR7_M0_H7_FR3_FR5_FR7_80dp.svg"
    path.write_text(_three_way_sheet(h7, "P1-FR7 | M0 H7 narrow support | 80dp"), encoding="utf-8")
    files.append(path)

    path = output_dir / "P1FR7_MORPHOLOGY_REUSE_80dp.svg"
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

    baseline_dir = out / "frozen_p1f_baseline"
    baseline_manifest = fr4_render.generate_frozen_p1f_baseline(baseline_dir)
    baseline_manifest_path = baseline_dir / "manifest.json"
    debug_dir = out / "debug"
    svg_files = generate_debug_svgs(debug_dir)

    manifest = {
        "version": RUN_VERSION,
        "summary": summary,
        "frozenFr5V1": FROZEN_FR5_V1,
        "frozenP1FBaselineVersion": baseline_manifest["version"],
        "frozenP1FBaselineManifestSha256": hashlib.sha256(baseline_manifest_path.read_bytes()).hexdigest(),
        "debugSvgs": [
            {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in sorted(svg_files)
        ],
    }
    manifest["manifestContentSha256"] = hashlib.sha256(canonical_bytes(manifest)).hexdigest()
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    if not summary["structuralPass"]:
        raise SystemExit("P1-FR7 structural invariant lane failed")


if __name__ == "__main__":
    main()
