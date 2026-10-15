from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from e_v0_fixture_adapter import H4, H6N, H7, build_e_fixture, iter_invariant_fixtures
from e_v0_profiles import M0, MORPHOLOGIES
from p1_fr1_mesh_probe_v3 import build_probe as build_fr1_probe
from p1_fr2_layered_view_prototype_v5 import build_probe as build_fr2_v5_probe
from p1_fr3_feline_core_topology import (
    CORE_VERTEX_IDS,
    PROTOTYPE_VERSION,
    build_probe,
    limb_crossing_count,
    result_dict,
)
import run_p1_fr2_perceptual_revision as render_base
from run_p1f_perceptual_evidence import generate as generate_frozen_p1f_baseline


RUN_VERSION = "P1_FR3_FELINE_CORE_TOPOLOGY_EVIDENCE_V1_24PT_NORMALIZED"
PRIMARY_SIZE_DP = 80

FROZEN_FR2_V5 = {
    "publicRepository": "hotmoral/-",
    "publicHead": "5b0708876a28faed0f6be1f193c2bf976577cbe9",
    "runId": 38757436816,
    "artifactId": 11983124631,
    "artifactDigest": "sha256:53d1ad38e7537edcf3bddc60d7196cf512b646ba6624a7f306699cbec8b8bfaf",
    "recordContentSha256": "34b9d7e012c0f4d0608ab39bf212c61443b22278495f6ff784d9cfeb2e8350b1",
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
    topology = set()
    semantic_mutations = 0
    max_paw_pin_error = 0.0
    self_intersections = 0
    correction_uses = 0
    mesh_domain_counts = set()
    stress_fr2_crossings = 0
    stress_fr3_crossings = 0
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
            fr2_result = build_fr2_v5_probe(fixture, direction)
            stress_fr2_crossings += limb_crossing_count(fr2_result.limb_meshes)
            stress_fr3_crossings += limb_crossing_count(result.limb_meshes)
            stress_records += 1

    records.sort(key=lambda r: (
        r["caseId"], r["morphologyId"], r["sizeDp"], r["direction"], r["t"]
    ))
    record_hash = hashlib.sha256(canonical_bytes(records)).hexdigest()
    structural_pass = (
        len(CORE_VERTEX_IDS) == 24
        and len(topology) == 1
        and semantic_mutations == 0
        and max_paw_pin_error <= 1e-9
        and self_intersections == 0
        and correction_uses == 0
        and mesh_domain_counts == {6}
    )
    summary = {
        "version": RUN_VERSION,
        "prototypeVersion": PROTOTYPE_VERSION,
        "coreVertexCount": len(CORE_VERTEX_IDS),
        "recordCount": len(records),
        "topologySignatureCount": len(topology),
        "topologySignatures": sorted(topology),
        "semanticMutationCount": semantic_mutations,
        "maxPawPinError": max_paw_pin_error,
        "coreSelfIntersectionCount": self_intersections,
        "correctionUseCount": correction_uses,
        "meshDomainCounts": sorted(mesh_domain_counts),
        "stressCrossingRecordCount": stress_records,
        "fr2V5StressLimbCrossingCount": stress_fr2_crossings,
        "fr3StressLimbCrossingCount": stress_fr3_crossings,
        "stressLimbCrossingDeltaVsFr2V5": stress_fr3_crossings - stress_fr2_crossings,
        "recordContentSha256": record_hash,
        "structuralPass": structural_pass,
        "perceptualDisposition": "REQUIRES_DIRECT_REVIEW",
    }
    return records, summary


def _normalized_group(fixture, probe, x: float, y: float, revision: bool):
    root = fixture.state.anchors["BODY_ROOT"]
    return render_base._mesh_group_svg(
        fixture,
        probe,
        x - root.x,
        y - root.y,
        revision,
    )


def _view_triptych_sheet():
    views = (("profile", 0.0), ("3Q", 0.50), ("front", 1.0))
    rows = ("FR1 V3", "FR2 V5", "FR3 24pt")
    cell_w = 190.0
    cell_h = 125.0
    left = 72.0
    top = 30.0
    width = left + len(views) * cell_w
    height = top + len(rows) * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="6" y="17" font-family="sans-serif" font-size="10">P1-FR3 | M0 canonical-view progression | 80dp</text>',
    ]
    for col, (label, _) in enumerate(views):
        parts.append(f'<text x="{left + col * cell_w + 4:.4f}" y="17" font-family="sans-serif" font-size="8">{escape(label)}</text>')
    for row, row_label in enumerate(rows):
        parts.append(f'<text x="6" y="{top + row * cell_h + 16:.4f}" font-family="sans-serif" font-size="8">{escape(row_label)}</text>')
    for col, (_, t) in enumerate(views):
        fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, +1)
        probes = (
            (build_fr1_probe(fixture, +1), False),
            (build_fr2_v5_probe(fixture, +1), True),
            (build_probe(fixture, +1), True),
        )
        for row, (probe, revision) in enumerate(probes):
            x = left + col * cell_w + cell_w * 0.50
            y = top + row * cell_h + cell_h * 0.52
            parts.append(_normalized_group(fixture, probe, x, y, revision))
    parts.append("</svg>")
    return "\n".join(parts)


def _fr2_fr3_sheet(samples, title: str):
    cell_w = 190.0
    cell_h = 125.0
    left = 72.0
    top = 30.0
    width = left + len(samples) * cell_w
    height = top + 2 * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="17" font-family="sans-serif" font-size="10">{escape(title)}</text>',
        f'<text x="6" y="{top + 16:.4f}" font-family="sans-serif" font-size="8">FR2 V5</text>',
        f'<text x="6" y="{top + cell_h + 16:.4f}" font-family="sans-serif" font-size="8">FR3 24pt</text>',
    ]
    for col, (label, fixture, fr2_probe, fr3_probe) in enumerate(samples):
        x0 = left + col * cell_w
        parts.append(f'<text x="{x0 + 4:.4f}" y="17" font-family="sans-serif" font-size="7">{escape(label)}</text>')
        parts.append(_normalized_group(fixture, fr2_probe, x0 + cell_w * 0.50, top + cell_h * 0.52, True))
        parts.append(_normalized_group(fixture, fr3_probe, x0 + cell_w * 0.50, top + cell_h * 1.52, True))
    parts.append("</svg>")
    return "\n".join(parts)


def _morphology_sheet():
    views = (("profile", 0.0), ("3Q", 0.50), ("front", 1.0))
    cell_w = 190.0
    cell_h = 125.0
    left = 150.0
    top = 30.0
    width = left + len(views) * cell_w
    height = top + len(MORPHOLOGIES) * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="6" y="17" font-family="sans-serif" font-size="10">P1-FR3 | shared 24pt morphology reuse | 80dp</text>',
    ]
    for col, (label, _) in enumerate(views):
        parts.append(f'<text x="{left + col * cell_w + 4:.4f}" y="17" font-family="sans-serif" font-size="8">{escape(label)}</text>')
    for row, morphology in enumerate(MORPHOLOGIES):
        y0 = top + row * cell_h
        parts.append(f'<text x="5" y="{y0 + 16:.4f}" font-family="sans-serif" font-size="7">{escape(morphology.id)}</text>')
        for col, (_, t) in enumerate(views):
            fixture = build_e_fixture(morphology, H6N, PRIMARY_SIZE_DP, t, +1)
            probe = build_probe(fixture, +1)
            x = left + col * cell_w + cell_w * 0.50
            y = y0 + cell_h * 0.52
            parts.append(_normalized_group(fixture, probe, x, y, True))
    parts.append("</svg>")
    return "\n".join(parts)


def generate_debug_svgs(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    files = []

    path = output_dir / "P1FR3_M0_VIEW_PROGRESSION_80dp.svg"
    path.write_text(_view_triptych_sheet(), encoding="utf-8")
    files.append(path)

    h4 = []
    for t in (0.0, 0.25, 0.50, 0.75, 1.0):
        fixture = build_e_fixture(M0, H4, PRIMARY_SIZE_DP, t, +1)
        h4.append((f"t={t:.2f}", fixture, build_fr2_v5_probe(fixture, +1), build_probe(fixture, +1)))
    path = output_dir / "P1FR3_M0_H4_FR2_VS_FR3_80dp.svg"
    path.write_text(_fr2_fr3_sheet(h4, "P1-FR3 | M0 H4 sit-to-stand | 80dp"), encoding="utf-8")
    files.append(path)

    for direction in (+1, -1):
        samples = []
        for t in (0.0, 0.20, 0.40, 0.60, 0.80, 1.0):
            fixture = build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, direction)
            samples.append((f"t={t:.2f}", fixture, build_fr2_v5_probe(fixture, direction), build_probe(fixture, direction)))
        path = output_dir / f"P1FR3_M0_H6N_DIR{direction:+d}_FR2_VS_FR3_80dp.svg"
        path.write_text(_fr2_fr3_sheet(samples, f"P1-FR3 | M0 H6N dir={direction:+d} | 80dp"), encoding="utf-8")
        files.append(path)

    h7 = []
    for t in (0.0, 0.25, 0.50, 0.75, 1.0):
        fixture = build_e_fixture(M0, H7, PRIMARY_SIZE_DP, t, +1)
        h7.append((f"t={t:.2f}", fixture, build_fr2_v5_probe(fixture, +1), build_probe(fixture, +1)))
    path = output_dir / "P1FR3_M0_H7_FR2_VS_FR3_80dp.svg"
    path.write_text(_fr2_fr3_sheet(h7, "P1-FR3 | M0 H7 narrow support | 80dp"), encoding="utf-8")
    files.append(path)

    path = output_dir / "P1FR3_MORPHOLOGY_REUSE_80dp.svg"
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
        "frozenFr2V5": FROZEN_FR2_V5,
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
        raise SystemExit("P1-FR3 structural invariant lane failed")


if __name__ == "__main__":
    main()
