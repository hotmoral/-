from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

from e_v0_fixture_adapter import H4, H6N, H7, build_e_fixture, iter_invariant_fixtures
from e_v0_profiles import M0, MORPHOLOGIES
import p1_fr3_feline_core_topology_v5 as fr3_v5
import p1_fr5_core_mass_silhouette_v1 as fr5
import run_p1_fr4_internal_core_scaffold as fr4_render


RUN_VERSION = "P1_FR5_CORE_MASS_SILHOUETTE_EVIDENCE_V1_PERP_ONLY"
PRIMARY_SIZE_DP = 80
FROZEN_FR3_V5 = fr4_render.FROZEN_FR3_V5
FROZEN_FR4_V3 = {
    "publicRepository": "hotmoral/-",
    "publicHead": "4a53163c51cf7ef8ca7358cc3c7d757d39703388",
    "runId": 38802518626,
    "jobId": 116654937653,
    "artifactId": 12004069076,
    "artifactDigest": "sha256:4c3a281d3f76cff56f9e403363ac760ba9903436895c68cab06bbccae2653194",
    "recordContentSha256": "c278f320547b86a079d37b5961f0586e06a86a50f55a21b9793a670dbfe08727",
    "scaffoldSignature": "cf9f55d3c08b0b2e8bc2e64025ee8248aa9a0ff9c0be037c98f238af113153ba",
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


def _is_exact_profile(probe) -> bool:
    weights = dict(probe.view_weights)
    return (
        abs(float(weights.get("PROFILE", 0.0)) - 1.0) <= 1e-12
        and abs(float(weights.get("THREE_QUARTER", 0.0))) <= 1e-12
        and abs(float(weights.get("FRONT", 0.0))) <= 1e-12
    )


def _core_map(core_vertices):
    return {vertex_id: (float(x), float(y)) for vertex_id, x, y in core_vertices}


def _distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _mass_widths(core_vertices):
    core = _core_map(core_vertices)
    return {
        "cranium": _distance(core["C04_CROWN_REAR"], core["C21_JAW_REAR"]),
        "cervical": _distance(core["C06_NECK_DORSAL_BASE"], core["C19_NECK_VENTRAL_BASE"]),
        "thorax": _distance(core["C08_SHOULDER_DORSAL"], core["C17_STERNUM"]),
    }


def _hierarchy_sample(t: float):
    fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, +1)
    result = fr5.build_probe(fixture, +1)
    return {
        "t": t,
        "viewWeights": dict(result.base.view_weights),
        "control": _mass_widths(result.control.core_vertices),
        "fr5": _mass_widths(result.base.core_vertices),
    }


def run_matrix():
    records = []
    topology_signatures = set()
    integration_signatures = set()
    patch_id_orders = set()
    patch_vertex_count_sets = set()
    semantic_mutations = 0
    max_paw_pin_error = 0.0
    final_core_self_intersections = 0
    patch_self_intersections = 0
    patch_outside_vertices = 0
    correction_uses = 0
    mesh_domain_counts = set()
    appendage_mismatches = 0
    profile_mismatches = 0
    changed_core_records = 0
    max_core_displacement = 0.0
    max_normalized_displacement = 0.0
    ear_base_outside_control = 0
    ear_base_outside_final = 0
    ear_attachment_regression_records = 0
    stress_fr3_crossings = 0
    stress_fr5_crossings = 0
    stress_records = 0

    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        result = fr5.build_probe(fixture, direction)
        probe = result.base
        control = result.control
        records.append(_round_value(fr5.result_dict(result)))
        topology_signatures.add(probe.topology_signature)
        integration_signatures.add(result.integration_signature)
        patch_id_orders.add(tuple(patch.id for patch in result.internal_patches))
        patch_vertex_count_sets.add(tuple(len(patch.vertices) for patch in result.internal_patches))
        if probe.semantic_anchor_hash_before != probe.semantic_anchor_hash_after:
            semantic_mutations += 1
        max_paw_pin_error = max(max_paw_pin_error, probe.paw_pin_error_max)
        final_core_self_intersections += probe.core_self_intersections
        patch_self_intersections += result.patch_self_intersections
        patch_outside_vertices += result.patch_outside_vertex_count
        correction_uses += len(probe.correction_families)
        mesh_domain_counts.add(1 + len(probe.limb_meshes) + 1)
        if (
            probe.ear_shapes != control.ear_shapes
            or probe.limb_meshes != control.limb_meshes
            or probe.tail_mesh != control.tail_mesh
        ):
            appendage_mismatches += 1
        if probe.core_vertices != control.core_vertices:
            changed_core_records += 1
        if _is_exact_profile(probe) and probe.core_vertices != control.core_vertices:
            profile_mismatches += 1
        max_core_displacement = max(max_core_displacement, result.max_core_displacement)
        max_normalized_displacement = max(
            max_normalized_displacement, result.normalized_max_core_displacement
        )
        ear_base_outside_control += result.ear_base_outside_control
        ear_base_outside_final += result.ear_base_outside_final
        if result.ear_base_outside_final > result.ear_base_outside_control:
            ear_attachment_regression_records += 1
        if size_dp == PRIMARY_SIZE_DP and case_id in (H6N, H7):
            stress_fr3_crossings += fr3_v5.limb_crossing_count(control.limb_meshes)
            stress_fr5_crossings += fr3_v5.limb_crossing_count(probe.limb_meshes)
            stress_records += 1

    records.sort(key=lambda r: (
        r["caseId"], r["morphologyId"], r["sizeDp"], r["direction"], r["t"]
    ))
    record_hash = hashlib.sha256(canonical_bytes(records)).hexdigest()
    structural_pass = (
        len(records) == 1770
        and topology_signatures == {fr3_v5.topology_signature()}
        and len(integration_signatures) == 1
        and patch_id_orders == {fr5.LAYER_IDS}
        and patch_vertex_count_sets == {(8, 6, 8)}
        and semantic_mutations == 0
        and max_paw_pin_error <= 1e-9
        and final_core_self_intersections == 0
        and patch_self_intersections == 0
        and patch_outside_vertices == 0
        and correction_uses == 0
        and mesh_domain_counts == {6}
        and appendage_mismatches == 0
        and profile_mismatches == 0
        and changed_core_records > 0
        and max_normalized_displacement <= fr5.MAX_NORMALIZED_CORE_DISPLACEMENT + 1e-12
        and ear_attachment_regression_records == 0
        and stress_fr5_crossings == stress_fr3_crossings
    )
    summary = {
        "version": RUN_VERSION,
        "prototypeVersion": fr5.PROTOTYPE_VERSION,
        "recordCount": len(records),
        "externalTopologySignatureCount": len(topology_signatures),
        "externalTopologySignatures": sorted(topology_signatures),
        "integrationSignatureCount": len(integration_signatures),
        "integrationSignatures": sorted(integration_signatures),
        "patchIdOrders": [list(v) for v in sorted(patch_id_orders)],
        "patchVertexCountSets": [list(v) for v in sorted(patch_vertex_count_sets)],
        "semanticMutationCount": semantic_mutations,
        "maxPawPinError": max_paw_pin_error,
        "finalCoreSelfIntersectionCount": final_core_self_intersections,
        "patchSelfIntersectionCount": patch_self_intersections,
        "patchOutsideVertexCount": patch_outside_vertices,
        "correctionUseCount": correction_uses,
        "meshDomainCounts": sorted(mesh_domain_counts),
        "appendageMismatchVsFr3V5Count": appendage_mismatches,
        "profileCoreMismatchVsFr3V5Count": profile_mismatches,
        "changedCoreRecordCount": changed_core_records,
        "maxCoreDisplacementDp": max_core_displacement,
        "maxNormalizedCoreDisplacement": max_normalized_displacement,
        "maxNormalizedCoreDisplacementLimit": fr5.MAX_NORMALIZED_CORE_DISPLACEMENT,
        "earBaseOutsideControlCount": ear_base_outside_control,
        "earBaseOutsideFinalCount": ear_base_outside_final,
        "earAttachmentRegressionRecordCount": ear_attachment_regression_records,
        "stressCrossingRecordCount": stress_records,
        "fr3V5StressLimbCrossingCount": stress_fr3_crossings,
        "fr5StressLimbCrossingCount": stress_fr5_crossings,
        "stressLimbCrossingDeltaVsFr3V5": stress_fr5_crossings - stress_fr3_crossings,
        "hierarchySamples": {
            "threeQuarter": _hierarchy_sample(0.5),
            "front": _hierarchy_sample(1.0),
        },
        "recordContentSha256": record_hash,
        "structuralPass": structural_pass,
        "perceptualDisposition": "REQUIRES_DIRECT_REVIEW",
    }
    return records, summary


def _normalized_control_group(fixture, probe, x: float, y: float):
    root = fixture.state.anchors["BODY_ROOT"]
    return fr4_render.render_base._mesh_group_svg(
        fixture, probe, x - root.x, y - root.y, True
    )


def _normalized_fr5_group(fixture, result, x: float, y: float):
    root = fixture.state.anchors["BODY_ROOT"]
    return fr4_render.render_base._mesh_group_svg(
        fixture, result.base, x - root.x, y - root.y, True
    )


def _normalized_fr5_guides(fixture, result, x: float, y: float):
    root = fixture.state.anchors["BODY_ROOT"]
    return fr4_render._fr4_group_svg(fixture, result, x - root.x, y - root.y)


def _comparison_sheet(samples, title: str):
    cell_w = 190.0
    cell_h = 125.0
    left = 82.0
    top = 30.0
    width = left + len(samples) * cell_w
    height = top + 2 * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="17" font-family="sans-serif" font-size="10">{escape(title)}</text>',
        f'<text x="6" y="{top + 16:.4f}" font-family="sans-serif" font-size="8">FR3 V5</text>',
        f'<text x="6" y="{top + cell_h + 16:.4f}" font-family="sans-serif" font-size="8">FR5 V1</text>',
    ]
    for col, (label, fixture, result) in enumerate(samples):
        x0 = left + col * cell_w
        parts.append(f'<text x="{x0 + 4:.4f}" y="17" font-family="sans-serif" font-size="7">{escape(label)}</text>')
        parts.append(_normalized_control_group(
            fixture, result.control, x0 + cell_w * 0.50, top + cell_h * 0.52
        ))
        parts.append(_normalized_fr5_group(
            fixture, result, x0 + cell_w * 0.50, top + cell_h * 1.52
        ))
    parts.append("</svg>")
    return "\n".join(parts)


def _view_sheet():
    samples = []
    for label, t in (("profile", 0.0), ("3Q", 0.5), ("front", 1.0)):
        fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, +1)
        samples.append((label, fixture, fr5.build_probe(fixture, +1)))

    cell_w = 190.0
    cell_h = 125.0
    left = 82.0
    top = 30.0
    width = left + len(samples) * cell_w
    height = top + 3 * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="6" y="17" font-family="sans-serif" font-size="10">P1-FR5 | M0 view progression | 80dp | mass-silhouette integration</text>',
        f'<text x="6" y="{top + 16:.4f}" font-family="sans-serif" font-size="8">FR3 V5</text>',
        f'<text x="6" y="{top + cell_h + 16:.4f}" font-family="sans-serif" font-size="8">FR5 silhouette</text>',
        f'<text x="6" y="{top + 2 * cell_h + 16:.4f}" font-family="sans-serif" font-size="8">FR5 guides</text>',
    ]
    for col, (label, fixture, result) in enumerate(samples):
        x0 = left + col * cell_w
        parts.append(f'<text x="{x0 + 4:.4f}" y="17" font-family="sans-serif" font-size="7">{escape(label)}</text>')
        parts.append(_normalized_control_group(
            fixture, result.control, x0 + cell_w * 0.50, top + cell_h * 0.52
        ))
        parts.append(_normalized_fr5_group(
            fixture, result, x0 + cell_w * 0.50, top + cell_h * 1.52
        ))
        parts.append(_normalized_fr5_guides(
            fixture, result, x0 + cell_w * 0.50, top + cell_h * 2.52
        ))
    parts.append("</svg>")
    return "\n".join(parts)


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
        '<text x="6" y="17" font-family="sans-serif" font-size="10">P1-FR5 | shared mass-silhouette rule morphology reuse | 80dp</text>',
    ]
    for col, (label, _) in enumerate(views):
        parts.append(f'<text x="{left + col * cell_w + 4:.4f}" y="17" font-family="sans-serif" font-size="8">{escape(label)}</text>')
    for row, morphology in enumerate(MORPHOLOGIES):
        y0 = top + row * cell_h
        parts.append(f'<text x="5" y="{y0 + 16:.4f}" font-family="sans-serif" font-size="7">{escape(morphology.id)}</text>')
        for col, (_, t) in enumerate(views):
            fixture = build_e_fixture(morphology, H6N, PRIMARY_SIZE_DP, t, +1)
            result = fr5.build_probe(fixture, +1)
            parts.append(_normalized_fr5_group(
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

    path = output_dir / "P1FR5_M0_VIEW_FR3_VS_FR5_80dp.svg"
    path.write_text(_view_sheet(), encoding="utf-8")
    files.append(path)

    h4 = []
    for t in (0.0, 0.25, 0.50, 0.75, 1.0):
        fixture = build_e_fixture(M0, H4, PRIMARY_SIZE_DP, t, +1)
        h4.append((f"t={t:.2f}", fixture, fr5.build_probe(fixture, +1)))
    path = output_dir / "P1FR5_M0_H4_FR3_VS_FR5_80dp.svg"
    path.write_text(_comparison_sheet(h4, "P1-FR5 | M0 H4 sit-to-stand | 80dp"), encoding="utf-8")
    files.append(path)

    for direction in (+1, -1):
        samples = []
        for t in (0.0, 0.20, 0.40, 0.60, 0.80, 1.0):
            fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, direction)
            samples.append((f"t={t:.2f}", fixture, fr5.build_probe(fixture, direction)))
        path = output_dir / f"P1FR5_M0_H6N_DIR{direction:+d}_FR3_VS_FR5_80dp.svg"
        path.write_text(_comparison_sheet(
            samples, f"P1-FR5 | M0 H6N dir={direction:+d} | 80dp"
        ), encoding="utf-8")
        files.append(path)

    h7 = []
    for t in (0.0, 0.25, 0.50, 0.75, 1.0):
        fixture = build_e_fixture(M0, H7, PRIMARY_SIZE_DP, t, +1)
        h7.append((f"t={t:.2f}", fixture, fr5.build_probe(fixture, +1)))
    path = output_dir / "P1FR5_M0_H7_FR3_VS_FR5_80dp.svg"
    path.write_text(_comparison_sheet(h7, "P1-FR5 | M0 H7 narrow support | 80dp"), encoding="utf-8")
    files.append(path)

    path = output_dir / "P1FR5_MORPHOLOGY_REUSE_80dp.svg"
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
        "frozenFr3V5": FROZEN_FR3_V5,
        "frozenFr4V3": FROZEN_FR4_V3,
        "frozenP1FBaselineVersion": baseline_manifest["version"],
        "frozenP1FBaselineManifestSha256": hashlib.sha256(
            baseline_manifest_path.read_bytes()
        ).hexdigest(),
        "debugSvgs": [
            {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in sorted(svg_files)
        ],
    }
    manifest["manifestContentSha256"] = hashlib.sha256(canonical_bytes(manifest)).hexdigest()
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    if not summary["structuralPass"]:
        raise SystemExit("P1-FR5 structural invariant lane failed")


if __name__ == "__main__":
    main()
