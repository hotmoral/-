from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from e_v0_fixture_adapter import H1, H4, H6N, build_e_fixture, iter_invariant_fixtures
from e_v0_profiles import M0, MORPHOLOGIES
from p1_fr1_mesh_probe_v3 import PROBE_VERSION, build_probe, result_dict


RUN_VERSION = "P1_FR1_FEASIBILITY_MATRIX_V1"


def canonical_bytes(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _round_record(record: dict) -> dict:
    def walk(value):
        if isinstance(value, float):
            return round(value, 10)
        if isinstance(value, list):
            return [walk(item) for item in value]
        if isinstance(value, tuple):
            return [walk(item) for item in value]
        if isinstance(value, dict):
            return {key: walk(item) for key, item in value.items()}
        return value
    return walk(record)


def run_matrix():
    records = []
    topology = set()
    semantic_mutations = 0
    max_paw_pin_error = 0.0
    self_intersections = 0
    correction_uses = 0
    mesh_domain_counts = set()

    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        result = build_probe(fixture, direction)
        record = _round_record(result_dict(result))
        records.append(record)
        topology.add(result.topology_signature)
        if result.semantic_anchor_hash_before != result.semantic_anchor_hash_after:
            semantic_mutations += 1
        max_paw_pin_error = max(max_paw_pin_error, result.paw_pin_error_max)
        self_intersections += result.core_self_intersections
        correction_uses += len(result.correction_families)
        mesh_domain_counts.add(1 + len(result.limb_meshes) + 1)

    records.sort(key=lambda r: (
        r["caseId"], r["morphologyId"], r["sizeDp"], r["direction"], r["t"]
    ))
    record_hash = hashlib.sha256(canonical_bytes(records)).hexdigest()
    summary = {
        "version": RUN_VERSION,
        "probeVersion": PROBE_VERSION,
        "recordCount": len(records),
        "topologySignatureCount": len(topology),
        "topologySignatures": sorted(topology),
        "semanticMutationCount": semantic_mutations,
        "maxPawPinError": max_paw_pin_error,
        "coreSelfIntersectionCount": self_intersections,
        "correctionUseCount": correction_uses,
        "meshDomainCounts": sorted(mesh_domain_counts),
        "recordContentSha256": record_hash,
    }
    summary["pass"] = (
        len(topology) == 1
        and semantic_mutations == 0
        and max_paw_pin_error <= 1e-9
        and self_intersections == 0
        and correction_uses == 0
        and mesh_domain_counts == {6}
    )
    return records, summary


def _points_attr(points):
    return " ".join(f"{x:.4f},{y:.4f}" for x, y in points)


def _mesh_group_svg(fixture, probe, x_offset: float, y_offset: float):
    items = [f'<g transform="translate({x_offset:.4f},{y_offset:.4f})">']
    core_points = [(x, y) for _, x, y in probe.core_vertices]
    items.append(
        f'<polygon points="{_points_attr(core_points)}" fill="#ececec" stroke="#111" stroke-width="0.7"/>'
    )
    ordered = sorted(
        list(probe.limb_meshes) + [probe.tail_mesh],
        key=lambda mesh: (mesh.get("viewDepth", 0.0), mesh["id"]),
    )
    for mesh in ordered:
        vertices = mesh["vertices"]
        left = [vertices[i] for i in range(0, len(vertices), 2)]
        right = [vertices[i] for i in range(1, len(vertices), 2)][::-1]
        perimeter = left + right
        items.append(
            f'<polygon points="{_points_attr(perimeter)}" fill="#d8d8d8" stroke="#333" stroke-width="0.45"/>'
        )
    for name in ("BODY_ROOT", "FOREQUARTER_REF", "PELVIS_REF", "HEAD_ROOT"):
        p = fixture.state.anchors[name]
        items.append(f'<circle cx="{p.x:.4f}" cy="{p.y:.4f}" r="1.15" fill="none" stroke="#777" stroke-width="0.35"/>')
    for name in ("FORE_PAW_L", "FORE_PAW_R", "HIND_PAW_L", "HIND_PAW_R"):
        p = fixture.state.anchors[name]
        items.append(f'<circle cx="{p.x:.4f}" cy="{p.y:.4f}" r="1.35" fill="none" stroke="#111" stroke-width="0.45"/>')
    items.append("</g>")
    return "".join(items)


def _svg_sheet(entries, title: str, columns: int, cell_w: float = 210.0, cell_h: float = 150.0):
    rows = (len(entries) + columns - 1) // columns
    width = columns * cell_w
    height = 28.0 + rows * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="17" font-family="sans-serif" font-size="10">{escape(title)}</text>',
    ]
    for index, (label, fixture, probe) in enumerate(entries):
        row, col = divmod(index, columns)
        x = col * cell_w
        y = 28.0 + row * cell_h
        parts.append(f'<text x="{x + 5:.4f}" y="{y + 11:.4f}" font-family="sans-serif" font-size="7">{escape(label)}</text>')
        parts.append(_mesh_group_svg(fixture, probe, x + cell_w * 0.45, y + cell_h * 0.50))
    parts.append("</svg>")
    return "\n".join(parts)


def generate_debug_svgs(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    files = []

    morph_entries = []
    for morphology in MORPHOLOGIES:
        fixture = build_e_fixture(morphology, H1, 80, 0.0, +1)
        probe = build_probe(fixture, +1)
        morph_entries.append((morphology.id, fixture, probe))
    svg = _svg_sheet(morph_entries, "P1-FR1 | shared topology | H1 80dp morphology", columns=5)
    path = output_dir / "P1FR1_MORPHOLOGY_H1_80dp.svg"
    path.write_text(svg, encoding="utf-8")
    files.append(path)

    turn_entries = []
    for direction in (+1, -1):
        for t in (0.0, 0.25, 0.50, 0.75, 1.0):
            fixture = build_e_fixture(M0, H6N, 80, t, direction)
            probe = build_probe(fixture, direction)
            turn_entries.append((f"dir={direction:+d} t={t:.2f}", fixture, probe))
    svg = _svg_sheet(turn_entries, "P1-FR1 | M0 H6N canonical view-shape interpolation", columns=5)
    path = output_dir / "P1FR1_M0_H6N_VIEW_INTERPOLATION.svg"
    path.write_text(svg, encoding="utf-8")
    files.append(path)

    h4_entries = []
    for t in (0.0, 0.25, 0.50, 0.75, 1.0):
        fixture = build_e_fixture(M0, H4, 80, t, +1)
        probe = build_probe(fixture, +1)
        h4_entries.append((f"t={t:.2f}", fixture, probe))
    svg = _svg_sheet(h4_entries, "P1-FR1 | M0 H4 pose-driven core mesh", columns=5)
    path = output_dir / "P1FR1_M0_H4_POSE_DEFORMATION.svg"
    path.write_text(svg, encoding="utf-8")
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
    debug_dir = out / "debug"
    svg_files = generate_debug_svgs(debug_dir)
    manifest = {
        "version": RUN_VERSION,
        "summary": summary,
        "debugSvgs": [
            {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in sorted(svg_files)
        ],
    }
    manifest["manifestContentSha256"] = hashlib.sha256(canonical_bytes(manifest)).hexdigest()
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    if not summary["pass"]:
        raise SystemExit("P1-FR1 feasibility matrix failed")


if __name__ == "__main__":
    main()
