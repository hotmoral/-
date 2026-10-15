from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from e_v0_fixture_adapter import H4, H6N, H7, build_e_fixture, iter_invariant_fixtures
from e_v0_profiles import M0, MORPHOLOGIES
import p1_fr3_feline_core_topology_v5 as fr3_v5
import p1_fr4_internal_core_scaffold as fr4
import run_p1_fr2_perceptual_revision as render_base
from run_p1f_perceptual_evidence import generate as generate_frozen_p1f_baseline


RUN_VERSION = "P1_FR4_INTERNAL_CORE_SCAFFOLD_EVIDENCE_V1_NORMALIZED"
PRIMARY_SIZE_DP = 80

FROZEN_FR3_V5 = {
    "publicRepository": "hotmoral/-",
    "publicHead": "bde2b46385850ae089c457f9df852babbbe0fd49",
    "runId": 38763065590,
    "jobId": 116519117134,
    "artifactId": 11986607417,
    "artifactDigest": "sha256:8837ef6d6ee058dbb10e53dd262c29d7a6e72c4ca61d97124182cf2032ffaec0",
    "recordContentSha256": "eb39d3656dc825595bc1ba293e4b6bab6d5ed4eafc61ff69678edaaa80fe3e91",
}


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
    external_topology = set()
    scaffold_signatures = set()
    patch_id_orders = set()
    patch_vertex_count_sets = set()
    semantic_mutations = 0
    max_paw_pin_error = 0.0
    external_self_intersections = 0
    patch_self_intersections = 0
    patch_outside_vertices = 0
    correction_uses = 0
    mesh_domain_counts = set()
    external_core_mismatches = 0
    appendage_mismatches = 0
    stress_fr3_crossings = 0
    stress_fr4_crossings = 0
    stress_records = 0

    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        result = fr4.build_probe(fixture, direction)
        base = result.base
        control = fr3_v5.build_probe(fixture, direction)
        record = _round_value(fr4.result_dict(result))
        records.append(record)

        external_topology.add(base.topology_signature)
        scaffold_signatures.add(result.scaffold_signature)
        patch_id_orders.add(tuple(patch.id for patch in result.internal_patches))
        patch_vertex_count_sets.add(tuple(len(patch.vertices) for patch in result.internal_patches))

        if base.semantic_anchor_hash_before != base.semantic_anchor_hash_after:
            semantic_mutations += 1
        max_paw_pin_error = max(max_paw_pin_error, base.paw_pin_error_max)
        external_self_intersections += base.core_self_intersections
        patch_self_intersections += result.patch_self_intersections
        patch_outside_vertices += result.patch_outside_vertex_count
        correction_uses += len(base.correction_families)
        mesh_domain_counts.add(1 + len(base.limb_meshes) + 1)

        if base.core_vertices != control.core_vertices:
            external_core_mismatches += 1
        if (
            base.ear_shapes != control.ear_shapes
            or base.limb_meshes != control.limb_meshes
            or base.tail_mesh != control.tail_mesh
        ):
            appendage_mismatches += 1

        if size_dp == PRIMARY_SIZE_DP and case_id in (H6N, H7):
            stress_fr3_crossings += fr3_v5.limb_crossing_count(control.limb_meshes)
            stress_fr4_crossings += fr3_v5.limb_crossing_count(base.limb_meshes)
            stress_records += 1

    records.sort(key=lambda r: (
        r["caseId"], r["morphologyId"], r["sizeDp"], r["direction"], r["t"]
    ))
    record_hash = hashlib.sha256(canonical_bytes(records)).hexdigest()
    expected_patch_ids = {fr4.PATCH_IDS}
    expected_vertex_counts = {(8, 6, 8)}
    structural_pass = (
        len(records) == 1770
        and external_topology == {fr3_v5.topology_signature()}
        and len(scaffold_signatures) == 1
        and patch_id_orders == expected_patch_ids
        and patch_vertex_count_sets == expected_vertex_counts
        and semantic_mutations == 0
        and max_paw_pin_error <= 1e-9
        and external_self_intersections == 0
        and patch_self_intersections == 0
        and patch_outside_vertices == 0
        and correction_uses == 0
        and mesh_domain_counts == {6}
        and external_core_mismatches == 0
        and appendage_mismatches == 0
    )
    summary = {
        "version": RUN_VERSION,
        "prototypeVersion": fr4.PROTOTYPE_VERSION,
        "recordCount": len(records),
        "externalTopologySignatureCount": len(external_topology),
        "externalTopologySignatures": sorted(external_topology),
        "scaffoldSignatureCount": len(scaffold_signatures),
        "scaffoldSignatures": sorted(scaffold_signatures),
        "patchIdOrders": [list(value) for value in sorted(patch_id_orders)],
        "patchVertexCountSets": [list(value) for value in sorted(patch_vertex_count_sets)],
        "semanticMutationCount": semantic_mutations,
        "maxPawPinError": max_paw_pin_error,
        "externalCoreSelfIntersectionCount": external_self_intersections,
        "patchSelfIntersectionCount": patch_self_intersections,
        "patchOutsideVertexCount": patch_outside_vertices,
        "correctionUseCount": correction_uses,
        "meshDomainCounts": sorted(mesh_domain_counts),
        "externalCoreMismatchVsFr3V5Count": external_core_mismatches,
        "appendageMismatchVsFr3V5Count": appendage_mismatches,
        "stressCrossingRecordCount": stress_records,
        "fr3V5StressLimbCrossingCount": stress_fr3_crossings,
        "fr4StressLimbCrossingCount": stress_fr4_crossings,
        "stressLimbCrossingDeltaVsFr3V5": stress_fr4_crossings - stress_fr3_crossings,
        "recordContentSha256": record_hash,
        "structuralPass": structural_pass,
        "perceptualDisposition": "REQUIRES_DIRECT_REVIEW",
    }
    return records, summary


def _points_attr(points):
    return " ".join(f"{x:.4f},{y:.4f}" for x, y in points)


def _patch_svg(result):
    by_id = {patch.id: patch for patch in result.internal_patches}
    fills = {
        "THORAX_MASS": "#dfdfdf",
        "CERVICAL_BRIDGE": "#f5f5f5",
        "CRANIUM_MASS": "#d5d5d5",
    }
    parts = []
    for patch_id in ("THORAX_MASS", "CERVICAL_BRIDGE", "CRANIUM_MASS"):
        patch = by_id[patch_id]
        parts.append(
            f'<polygon points="{_points_attr(patch.vertices)}" fill="{fills[patch_id]}" stroke="none"/>'
        )
    for patch_id in ("CERVICAL_BRIDGE", "CRANIUM_MASS"):
        patch = by_id[patch_id]
        if patch.seam is None:
            continue
        a = patch.vertices[patch.seam[0]]
        b = patch.vertices[patch.seam[1]]
        parts.append(
            f'<line x1="{a[0]:.4f}" y1="{a[1]:.4f}" x2="{b[0]:.4f}" y2="{b[1]:.4f}" stroke="#666" stroke-width="0.55" stroke-linecap="round"/>'
        )
    return "".join(parts)


def _fr4_group_svg(fixture, result, x_offset: float, y_offset: float):
    probe = result.base
    parts = [f'<g transform="translate({x_offset:.4f},{y_offset:.4f})">']
    appendages = list(probe.limb_meshes) + [probe.tail_mesh]
    ordered = sorted(appendages, key=lambda mesh: (mesh.get("viewDepth", 0.0), mesh["id"]))
    far = [mesh for mesh in ordered if mesh.get("viewDepth", 0.0) <= 0.0]
    near = [mesh for mesh in ordered if mesh.get("viewDepth", 0.0) > 0.0]

    for mesh in far:
        parts.append(render_base._appendage_svg(mesh, fixture, True))
    for ear in probe.ear_shapes:
        parts.append(
            f'<polygon points="{_points_attr(ear)}" fill="#ededed" stroke="#202020" stroke-width="0.55" stroke-linejoin="round"/>'
        )
    core_points = [(x, y) for _, x, y in probe.core_vertices]
    parts.append(
        f'<polygon points="{_points_attr(core_points)}" fill="#ededed" stroke="#181818" stroke-width="0.75" stroke-linejoin="round"/>'
    )
    parts.append(_patch_svg(result))
    for mesh in near:
        parts.append(render_base._appendage_svg(mesh, fixture, True))
    for name in ("FORE_PAW_L", "FORE_PAW_R", "HIND_PAW_L", "HIND_PAW_R"):
        p = fixture.state.anchors[name]
        parts.append(f'<circle cx="{p.x:.4f}" cy="{p.y:.4f}" r="0.95" fill="none" stroke="#777" stroke-width="0.30"/>')
    parts.append("</g>")
    return "".join(parts)


def _normalized_fr3_group(fixture, probe, x: float, y: float):
    root = fixture.state.anchors["BODY_ROOT"]
    return render_base._mesh_group_svg(fixture, probe, x - root.x, y - root.y, True)


def _normalized_fr4_group(fixture, result, x: float, y: float):
    root = fixture.state.anchors["BODY_ROOT"]
    return _fr4_group_svg(fixture, result, x - root.x, y - root.y)


def _comparison_sheet(samples, title: str):
    cell_w = 190.0
    cell_h = 125.0
    left = 76.0
    top = 30.0
    width = left + len(samples) * cell_w
    height = top + 2 * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="17" font-family="sans-serif" font-size="10">{escape(title)}</text>',
        f'<text x="6" y="{top + 16:.4f}" font-family="sans-serif" font-size="8">FR3 V5</text>',
        f'<text x="6" y="{top + cell_h + 16:.4f}" font-family="sans-serif" font-size="8">FR4 scaffold</text>',
    ]
    for col, (label, fixture, fr3_probe, fr4_result) in enumerate(samples):
        x0 = left + col * cell_w
        parts.append(f'<text x="{x0 + 4:.4f}" y="17" font-family="sans-serif" font-size="7">{escape(label)}</text>')
        parts.append(_normalized_fr3_group(fixture, fr3_probe, x0 + cell_w * 0.50, top + cell_h * 0.52))
        parts.append(_normalized_fr4_group(fixture, fr4_result, x0 + cell_w * 0.50, top + cell_h * 1.52))
    parts.append("</svg>")
    return "\n".join(parts)


def _view_sheet():
    samples = []
    for label, t in (("profile", 0.0), ("3Q", 0.5), ("front", 1.0)):
        fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, +1)
        samples.append((label, fixture, fr3_v5.build_probe(fixture, +1), fr4.build_probe(fixture, +1)))
    return _comparison_sheet(samples, "P1-FR4 | M0 view progression | 80dp | internal-only")


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
        '<text x="6" y="17" font-family="sans-serif" font-size="10">P1-FR4 | shared internal scaffold morphology reuse | 80dp</text>',
    ]
    for col, (label, _) in enumerate(views):
        parts.append(f'<text x="{left + col * cell_w + 4:.4f}" y="17" font-family="sans-serif" font-size="8">{escape(label)}</text>')
    for row, morphology in enumerate(MORPHOLOGIES):
        y0 = top + row * cell_h
        parts.append(f'<text x="5" y="{y0 + 16:.4f}" font-family="sans-serif" font-size="7">{escape(morphology.id)}</text>')
        for col, (_, t) in enumerate(views):
            fixture = build_e_fixture(morphology, H6N, PRIMARY_SIZE_DP, t, +1)
            result = fr4.build_probe(fixture, +1)
            parts.append(_normalized_fr4_group(
                fixture,
                result,
                left + col * cell_w + cell_w * 0.50,
                y0 + cell_h * 0.52,
            ))
    parts.append("</svg>")
    return "\n".join(parts)


def generate_debug_svgs(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    files = []

    path = output_dir / "P1FR4_M0_VIEW_FR3_VS_FR4_80dp.svg"
    path.write_text(_view_sheet(), encoding="utf-8")
    files.append(path)

    h4 = []
    for t in (0.0, 0.25, 0.50, 0.75, 1.0):
        fixture = build_e_fixture(M0, H4, PRIMARY_SIZE_DP, t, +1)
        h4.append((f"t={t:.2f}", fixture, fr3_v5.build_probe(fixture, +1), fr4.build_probe(fixture, +1)))
    path = output_dir / "P1FR4_M0_H4_FR3_VS_FR4_80dp.svg"
    path.write_text(_comparison_sheet(h4, "P1-FR4 | M0 H4 sit-to-stand | 80dp"), encoding="utf-8")
    files.append(path)

    for direction in (+1, -1):
        samples = []
        for t in (0.0, 0.20, 0.40, 0.60, 0.80, 1.0):
            fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, direction)
            samples.append((f"t={t:.2f}", fixture, fr3_v5.build_probe(fixture, direction), fr4.build_probe(fixture, direction)))
        path = output_dir / f"P1FR4_M0_H6N_DIR{direction:+d}_FR3_VS_FR4_80dp.svg"
        path.write_text(_comparison_sheet(samples, f"P1-FR4 | M0 H6N dir={direction:+d} | 80dp"), encoding="utf-8")
        files.append(path)

    h7 = []
    for t in (0.0, 0.25, 0.50, 0.75, 1.0):
        fixture = build_e_fixture(M0, H7, PRIMARY_SIZE_DP, t, +1)
        h7.append((f"t={t:.2f}", fixture, fr3_v5.build_probe(fixture, +1), fr4.build_probe(fixture, +1)))
    path = output_dir / "P1FR4_M0_H7_FR3_VS_FR4_80dp.svg"
    path.write_text(_comparison_sheet(h7, "P1-FR4 | M0 H7 narrow support | 80dp"), encoding="utf-8")
    files.append(path)

    path = output_dir / "P1FR4_MORPHOLOGY_REUSE_80dp.svg"
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
    baseline_manifest = generate_frozen_p1f_baseline(baseline_dir)
    baseline_manifest_path = baseline_dir / "manifest.json"

    debug_dir = out / "debug"
    svg_files = generate_debug_svgs(debug_dir)
    manifest = {
        "version": RUN_VERSION,
        "summary": summary,
        "frozenFr3V5": FROZEN_FR3_V5,
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
        raise SystemExit("P1-FR4 structural invariant lane failed")


if __name__ == "__main__":
    main()
