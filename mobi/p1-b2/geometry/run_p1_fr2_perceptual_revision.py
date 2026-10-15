from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from e_v0_fixture_adapter import H1, H4, H6N, H7, build_e_fixture, iter_invariant_fixtures
from e_v0_profiles import M0, MORPHOLOGIES
from p1_fr1_mesh_probe_v3 import build_probe as build_fr1_probe
from p1_fr2_layered_view_prototype import (
    PROTOTYPE_VERSION,
    build_probe,
    limb_crossing_count,
    result_dict,
)
from run_p1f_perceptual_evidence import generate as generate_frozen_p1f_baseline


RUN_VERSION = "P1_FR2_PERCEPTUAL_REVISION_EVIDENCE_V1"
PRIMARY_SIZE_DP = 80


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _round_value(value):
    if isinstance(value, float):
        return round(value, 10)
    if isinstance(value, list):
        return [_round_value(item) for item in value]
    if isinstance(value, tuple):
        return [_round_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _round_value(item) for key, item in value.items()}
    return value


def run_matrix():
    records = []
    topology = set()
    semantic_mutations = 0
    max_paw_pin_error = 0.0
    self_intersections = 0
    correction_uses = 0
    mesh_domain_counts = set()
    stress_baseline_crossings = 0
    stress_revision_crossings = 0
    stress_records = 0

    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        result = build_probe(fixture, direction)
        record = _round_value(result_dict(result))
        records.append(record)
        topology.add(result.topology_signature)
        if result.semantic_anchor_hash_before != result.semantic_anchor_hash_after:
            semantic_mutations += 1
        max_paw_pin_error = max(max_paw_pin_error, result.paw_pin_error_max)
        self_intersections += result.core_self_intersections
        correction_uses += len(result.correction_families)
        mesh_domain_counts.add(1 + len(result.limb_meshes) + 1)

        if size_dp == PRIMARY_SIZE_DP and case_id in (H6N, H7):
            baseline = build_fr1_probe(fixture, direction)
            stress_baseline_crossings += limb_crossing_count(baseline.limb_meshes)
            stress_revision_crossings += limb_crossing_count(result.limb_meshes)
            stress_records += 1

    records.sort(key=lambda r: (
        r["caseId"], r["morphologyId"], r["sizeDp"], r["direction"], r["t"]
    ))
    record_hash = hashlib.sha256(canonical_bytes(records)).hexdigest()
    structural_pass = (
        len(topology) == 1
        and semantic_mutations == 0
        and max_paw_pin_error <= 1e-9
        and self_intersections == 0
        and correction_uses == 0
        and mesh_domain_counts == {6}
    )
    summary = {
        "version": RUN_VERSION,
        "prototypeVersion": PROTOTYPE_VERSION,
        "recordCount": len(records),
        "topologySignatureCount": len(topology),
        "topologySignatures": sorted(topology),
        "semanticMutationCount": semantic_mutations,
        "maxPawPinError": max_paw_pin_error,
        "coreSelfIntersectionCount": self_intersections,
        "correctionUseCount": correction_uses,
        "meshDomainCounts": sorted(mesh_domain_counts),
        "stressCrossingRecordCount": stress_records,
        "fr1StressLimbCrossingCount": stress_baseline_crossings,
        "fr2StressLimbCrossingCount": stress_revision_crossings,
        "stressLimbCrossingDelta": stress_revision_crossings - stress_baseline_crossings,
        "recordContentSha256": record_hash,
        "structuralPass": structural_pass,
        "perceptualDisposition": "REQUIRES_DIRECT_REVIEW",
    }
    return records, summary


def _points_attr(points):
    return " ".join(f"{x:.4f},{y:.4f}" for x, y in points)


def _mesh_perimeter(mesh):
    vertices = mesh["vertices"]
    left = [vertices[i] for i in range(0, len(vertices), 2)]
    right = [vertices[i] for i in range(1, len(vertices), 2)][::-1]
    return left + right


def _appendage_svg(mesh, fixture, revision: bool):
    fill = "#d2d2d2" if revision else "#dddddd"
    stroke = "#2f2f2f"
    parts = [
        f'<polygon points="{_points_attr(_mesh_perimeter(mesh))}" fill="{fill}" stroke="{stroke}" stroke-width="0.55" stroke-linejoin="round"/>'
    ]
    if revision and mesh.get("pawId"):
        paw = fixture.state.anchors[mesh["pawId"]]
        parts.append(
            f'<ellipse cx="{paw.x:.4f}" cy="{paw.y:.4f}" rx="{mesh["pawRadiusX"]:.4f}" ry="{mesh["pawRadiusY"]:.4f}" fill="{fill}" stroke="{stroke}" stroke-width="0.45"/>'
        )
    return "".join(parts)


def _mesh_group_svg(fixture, probe, x_offset: float, y_offset: float, revision: bool):
    parts = [f'<g transform="translate({x_offset:.4f},{y_offset:.4f})">']
    appendages = list(probe.limb_meshes) + [probe.tail_mesh]
    ordered = sorted(appendages, key=lambda mesh: (mesh.get("viewDepth", 0.0), mesh["id"]))
    far = [mesh for mesh in ordered if mesh.get("viewDepth", 0.0) <= 0.0]
    near = [mesh for mesh in ordered if mesh.get("viewDepth", 0.0) > 0.0]

    for mesh in far:
        parts.append(_appendage_svg(mesh, fixture, revision))

    if revision:
        for ear in probe.ear_shapes:
            parts.append(
                f'<polygon points="{_points_attr(ear)}" fill="#ededed" stroke="#202020" stroke-width="0.55" stroke-linejoin="round"/>'
            )

    core_points = [(x, y) for _, x, y in probe.core_vertices]
    parts.append(
        f'<polygon points="{_points_attr(core_points)}" fill="#ededed" stroke="#181818" stroke-width="0.75" stroke-linejoin="round"/>'
    )

    for mesh in near:
        parts.append(_appendage_svg(mesh, fixture, revision))

    for name in ("FORE_PAW_L", "FORE_PAW_R", "HIND_PAW_L", "HIND_PAW_R"):
        p = fixture.state.anchors[name]
        parts.append(f'<circle cx="{p.x:.4f}" cy="{p.y:.4f}" r="0.95" fill="none" stroke="#777" stroke-width="0.30"/>')
    parts.append("</g>")
    return "".join(parts)


def _comparison_sheet(samples, title: str, cell_w: float = 190.0, cell_h: float = 125.0):
    columns = len(samples)
    left = 68.0
    top = 30.0
    width = left + columns * cell_w
    height = top + 2 * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="17" font-family="sans-serif" font-size="10">{escape(title)}</text>',
        f'<text x="6" y="{top + 16:.4f}" font-family="sans-serif" font-size="8">FR1 V3</text>',
        f'<text x="6" y="{top + cell_h + 16:.4f}" font-family="sans-serif" font-size="8">FR2</text>',
    ]
    for col, (label, fixture, baseline, revision) in enumerate(samples):
        x = left + col * cell_w
        parts.append(f'<text x="{x + 4:.4f}" y="17" font-family="sans-serif" font-size="7">{escape(label)}</text>')
        parts.append(_mesh_group_svg(fixture, baseline, x + cell_w * 0.50, top + cell_h * 0.52, False))
        parts.append(_mesh_group_svg(fixture, revision, x + cell_w * 0.50, top + cell_h * 1.52, True))
    parts.append("</svg>")
    return "\n".join(parts)


def _revision_morphology_sheet():
    views = (
        ("profile", H6N, 0.0),
        ("3Q", H6N, 0.50),
        ("front", H6N, 1.0),
    )
    cell_w = 190.0
    cell_h = 125.0
    left = 150.0
    top = 30.0
    width = left + len(views) * cell_w
    height = top + len(MORPHOLOGIES) * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="6" y="17" font-family="sans-serif" font-size="10">P1-FR2 | morphology reuse | 80dp</text>',
    ]
    for col, (label, _, _) in enumerate(views):
        parts.append(f'<text x="{left + col * cell_w + 4:.4f}" y="17" font-family="sans-serif" font-size="8">{escape(label)}</text>')
    for row, morphology in enumerate(MORPHOLOGIES):
        y = top + row * cell_h
        parts.append(f'<text x="5" y="{y + 16:.4f}" font-family="sans-serif" font-size="7">{escape(morphology.id)}</text>')
        for col, (_, case_id, t) in enumerate(views):
            fixture = build_e_fixture(morphology, case_id, PRIMARY_SIZE_DP, t, +1)
            probe = build_probe(fixture, +1)
            x = left + col * cell_w
            parts.append(_mesh_group_svg(fixture, probe, x + cell_w * 0.50, y + cell_h * 0.52, True))
    parts.append("</svg>")
    return "\n".join(parts)


def generate_debug_svgs(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    files = []

    view_samples = []
    for label, t in (("profile", 0.0), ("3Q", 0.50), ("front", 1.0)):
        fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, +1)
        view_samples.append((label, fixture, build_fr1_probe(fixture, +1), build_probe(fixture, +1)))
    path = output_dir / "P1FR2_M0_VIEW_COMPARISON_80dp.svg"
    path.write_text(_comparison_sheet(view_samples, "P1-FR2 | M0 canonical view comparison | 80dp"), encoding="utf-8")
    files.append(path)

    h4_samples = []
    for t in (0.0, 0.25, 0.50, 0.75, 1.0):
        fixture = build_e_fixture(M0, H4, PRIMARY_SIZE_DP, t, +1)
        h4_samples.append((f"t={t:.2f}", fixture, build_fr1_probe(fixture, +1), build_probe(fixture, +1)))
    path = output_dir / "P1FR2_M0_H4_COMPARISON_80dp.svg"
    path.write_text(_comparison_sheet(h4_samples, "P1-FR2 | M0 H4 sit-to-stand | 80dp"), encoding="utf-8")
    files.append(path)

    for direction in (+1, -1):
        samples = []
        for t in (0.0, 0.20, 0.40, 0.60, 0.80, 1.0):
            fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, direction)
            samples.append((f"t={t:.2f}", fixture, build_fr1_probe(fixture, direction), build_probe(fixture, direction)))
        path = output_dir / f"P1FR2_M0_H6N_DIR{direction:+d}_COMPARISON_80dp.svg"
        path.write_text(_comparison_sheet(samples, f"P1-FR2 | M0 H6N dir={direction:+d} | 80dp"), encoding="utf-8")
        files.append(path)

    h7_samples = []
    for t in (0.0, 0.25, 0.50, 0.75, 1.0):
        fixture = build_e_fixture(M0, H7, PRIMARY_SIZE_DP, t, +1)
        h7_samples.append((f"t={t:.2f}", fixture, build_fr1_probe(fixture, +1), build_probe(fixture, +1)))
    path = output_dir / "P1FR2_M0_H7_COMPARISON_80dp.svg"
    path.write_text(_comparison_sheet(h7_samples, "P1-FR2 | M0 H7 narrow support | 80dp"), encoding="utf-8")
    files.append(path)

    path = output_dir / "P1FR2_MORPHOLOGY_REUSE_80dp.svg"
    path.write_text(_revision_morphology_sheet(), encoding="utf-8")
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
    baseline_manifest = generate_frozen_p1f_baseline(baseline_dir)
    baseline_manifest_path = baseline_dir / "manifest.json"

    debug_dir = out / "debug"
    svg_files = generate_debug_svgs(debug_dir)
    manifest = {
        "version": RUN_VERSION,
        "summary": summary,
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
        raise SystemExit("P1-FR2 structural invariant lane failed")


if __name__ == "__main__":
    main()
