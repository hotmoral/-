from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from c3_semantic import canonical_bytes
from e_v0_fixture_adapter import H6N, build_e_fixture
from e_v0_profiles import M0, morphology_by_id
import p1_c_r2_minimal_volumetric_proxy_v1 as r2
import p1_c_r7_anatomy_flow_surface_v1 as r7
import p1_c_r7_anatomy_flow_topology_v1 as topo


RUN_VERSION = "P1_C_R7_ANATOMY_FLOW_STAGE3_EVIDENCE_V1"
PRIMARY_SIZE_DP = 80
VIEW_SAMPLES = (("PROFILE", 0.0), ("THREE_QUARTER", 0.5), ("FRONT", 1.0))


def _bounds(points):
    points = tuple(points)
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return min(xs), min(ys), max(xs), max(ys)


def _result_bounds(result, include_ears=True):
    return _bounds(r7.all_points(result, include_ears=include_ears))


def _points_attr(points, scale, tx, ty):
    return " ".join(f"{tx + scale*x:.4f},{ty + scale*y:.4f}" for x, y in points)


def _domain_primitives(result, domain, include_ears=True):
    return tuple(
        primitive
        for primitive in r7.all_primitives(result, include_ears=include_ears)
        if primitive.domain == domain
    )


def _render_polygon(primitive, scale, tx, ty, fill="#111", stroke="none", stroke_width=0.0):
    return (
        f'<polygon points="{_points_attr(primitive.points, scale, tx, ty)}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.3f}"/>'
    )


def _render_surface(
    fixture,
    cx,
    cy,
    display_scale=1.0,
    include_ears=True,
    flow_debug=False,
    proximal_debug=False,
):
    result = r7.build_surface(fixture)
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

    base_fill = "#d8d8d8" if (flow_debug or proximal_debug) else "#111"

    for domain in ("HIND_R", "HIND_L"):
        for primitive in _domain_primitives(result, domain, include_ears=include_ears):
            if primitive.id.startswith("FLOW_FACE_") or primitive.id.startswith(domain):
                parts.append(_render_polygon(primitive, display_scale, tx, ty, fill=base_fill))

    for primitive in result.faces:
        if primitive.domain == "CORE":
            parts.append(_render_polygon(primitive, display_scale, tx, ty, fill=base_fill))

    if include_ears:
        for primitive in result.ears:
            parts.append(_render_polygon(primitive, display_scale, tx, ty, fill=base_fill))

    for domain in ("FORE_R", "FORE_L"):
        for primitive in _domain_primitives(result, domain, include_ears=include_ears):
            if primitive.id.startswith("FLOW_FACE_") or primitive.id.startswith(domain):
                parts.append(_render_polygon(primitive, display_scale, tx, ty, fill=base_fill))

    if flow_debug or proximal_debug:
        cmap = {control.id: control for control in result.controls}

        if flow_debug:
            for a, b in topo.edge_set():
                pa, pb = cmap[a].point, cmap[b].point
                points = (pa, pb)
                parts.append(
                    f'<polyline points="{_points_attr(points, display_scale, tx, ty)}" '
                    'fill="none" stroke="#999" stroke-width="0.45"/>'
                )
            for path in topo.FLOW_PATHS.values():
                points = tuple(cmap[vertex_id].point for vertex_id in path)
                parts.append(
                    f'<polyline points="{_points_attr(points, display_scale, tx, ty)}" '
                    'fill="none" stroke="#222" stroke-width="0.95" stroke-linejoin="round"/>'
                )
            for control in result.controls:
                x, y = control.point
                parts.append(
                    f'<circle cx="{tx + display_scale*x:.4f}" cy="{ty + display_scale*y:.4f}" '
                    'r="0.55" fill="#444"/>'
                )

        if proximal_debug:
            for boundary in topo.SHARED_BOUNDARIES.values():
                points = tuple(cmap[vertex_id].point for vertex_id in boundary) + (cmap[boundary[0]].point,)
                parts.append(
                    f'<polyline points="{_points_attr(points, display_scale, tx, ty)}" '
                    'fill="none" stroke="#222" stroke-width="1.3" stroke-linejoin="round"/>'
                )
            for vertex_id in topo.PROXIMAL:
                x, y = cmap[vertex_id].point
                parts.append(
                    f'<circle cx="{tx + display_scale*x:.4f}" cy="{ty + display_scale*y:.4f}" '
                    'r="1.05" fill="#222"/>'
                )

    return "\n".join(parts)


def _sheet(title, samples, include_ears=True, true_scale=False, flow_debug=False, proximal_debug=False):
    cell_w = 126.0 if true_scale else 170.0
    cell_h = 118.0 if true_scale else 150.0
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
            _render_surface(
                fixture,
                x0 + cell_w * 0.50,
                y0 + cell_h * 0.60,
                display_scale=1.0 if true_scale else 1.28,
                include_ears=include_ears,
                flow_debug=flow_debug,
                proximal_debug=proximal_debug,
            )
        )
    parts.append("</svg>")
    return "\n".join(parts)


def _stage3_samples():
    return tuple(
        (label, build_e_fixture(M0, H6N, PRIMARY_SIZE_DP, t, +1))
        for label, t in VIEW_SAMPLES
    )


def _shared_boundary_interface_pass():
    edge_domains = defaultdict(set)
    for domain, face in topo.FACES:
        for a, b in zip(face, face[1:] + face[:1]):
            edge_domains[tuple(sorted((a, b)))].add(domain)
    for domain, boundary in topo.SHARED_BOUNDARIES.items():
        for a, b in zip(boundary, boundary[1:] + boundary[:1]):
            if edge_domains[tuple(sorted((a, b)))] != {"CORE", domain}:
                return False
    return True


def run_stage3():
    records = []
    semantic_mutations = 0
    surface_signatures = set()
    topology_signatures = set()
    max_paw_pin = 0.0
    domain_counts = set()
    nonfinite = 0
    bounds_mismatches = 0

    for label, fixture in _stage3_samples():
        before = canonical_bytes(fixture.payload)
        result = r7.build_surface(fixture)
        after = canonical_bytes(fixture.payload)
        if before != after:
            semantic_mutations += 1
        payload = r7.result_dict(fixture, result)
        payload["reviewLabel"] = label
        records.append(payload)
        surface_signatures.add(result.signature)
        topology_signatures.add(payload["topologySignature"])
        max_paw_pin = max(max_paw_pin, result.paw_pin_error)
        domain_counts.add(len(result.domain_bounds))
        if not payload["finite"]:
            nonfinite += 1
        for domain, rect in result.domain_bounds.items():
            domain_points = [
                point
                for primitive in r7.all_primitives(result)
                if primitive.domain == domain
                for point in primitive.points
            ]
            if any(
                not (
                    rect[0] - 1e-9 <= point[0] <= rect[2] + 1e-9
                    and rect[1] - 1e-9 <= point[1] <= rect[3] + 1e-9
                )
                for point in domain_points
            ):
                bounds_mismatches += 1

    interface_pass = _shared_boundary_interface_pass()
    summary = {
        "version": RUN_VERSION,
        "prototypeVersion": r7.PROTOTYPE_VERSION,
        "sourceFamily": r7.SOURCE_FAMILY,
        "sourcePackId": r7.SOURCE_PACK_ID,
        "topologyVersion": topo.TOPOLOGY_VERSION,
        "topologySignature": topo.topology_signature(),
        "recordCount": len(records),
        "semanticMutationCount": semantic_mutations,
        "surfaceSignatureCount": len(surface_signatures),
        "topologySignatureCount": len(topology_signatures),
        "authoritativeControlCount": r7.AUTHORITATIVE_CONTROL_COUNT,
        "authoritativeFaceCount": r7.AUTHORITATIVE_FACE_COUNT,
        "topologyEdgeCount": len(topo.edge_set()),
        "derivedSubdivisionSteps": r7.DERIVED_SUBDIVISION_STEPS,
        "sharedBoundaryInterfacePass": interface_pass,
        "externalDomainCounts": sorted(domain_counts),
        "maxPawPinError": max_paw_pin,
        "nonfiniteRecordCount": nonfinite,
        "domainBoundsMismatchCount": bounds_mismatches,
        "correctionUseCount": r7.CORRECTION_USE_COUNT,
    }
    summary["mechanicalPass"] = bool(
        len(records) == 3
        and semantic_mutations == 0
        and len(surface_signatures) == 1
        and topology_signatures == {topo.FROZEN_TOPOLOGY_SHA256}
        and r7.AUTHORITATIVE_CONTROL_COUNT == 63
        and r7.AUTHORITATIVE_FACE_COUNT == 66
        and len(topo.edge_set()) == 127
        and r7.DERIVED_SUBDIVISION_STEPS == 0
        and interface_pass
        and domain_counts == {6}
        and max_paw_pin <= 1e-9
        and nonfinite == 0
        and bounds_mismatches == 0
        and r7.CORRECTION_USE_COUNT == 0
    )
    summary["recordContentSha256"] = hashlib.sha256(canonical_bytes(records)).hexdigest()
    return records, summary


def generate_stage3_svgs(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    samples = _stage3_samples()
    files = []
    ear_neutral = tuple((label + " EAR-NEUTRAL", fixture) for label, fixture in samples[1:])

    specs = (
        ("P1CR7_V1_M0_VIEW_80dp_TRUE_SCALE.svg", "P1-C-R7 V1 | M0 | 80dp true scale", samples, True, True, False, False),
        ("P1CR7_V1_M0_VIEW_80dp_REVIEW.svg", "P1-C-R7 V1 | M0 | neutral structural review", samples, True, False, False, False),
        ("P1CR7_V1_M0_EAR_NEUTRALIZED_80dp.svg", "P1-C-R7 V1 | diagnostic | ears hidden, surface unchanged", ear_neutral, False, False, False, False),
        ("P1CR7_V1_M0_TOPOLOGY_FLOW_80dp.svg", "P1-C-R7 V1 | frozen anatomy-flow topology diagnostic", samples, True, False, True, False),
        ("P1CR7_V1_M0_PROXIMAL_EMERGENCE_80dp.svg", "P1-C-R7 V1 | shared proximal-boundary diagnostic", samples, True, False, False, True),
    )
    for filename, title, sheet_samples, include_ears, true_scale, flow_debug, proximal_debug in specs:
        path = output_dir / filename
        path.write_text(
            _sheet(
                title,
                sheet_samples,
                include_ears=include_ears,
                true_scale=true_scale,
                flow_debug=flow_debug,
                proximal_debug=proximal_debug,
            ),
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

    records, summary = run_stage3()
    (out / "records.json").write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    svgs = generate_stage3_svgs(out / "debug")
    manifest = {
        "version": RUN_VERSION,
        "prototypeVersion": r7.PROTOTYPE_VERSION,
        "sourcePackId": r7.SOURCE_PACK_ID,
        "topologySignature": topo.topology_signature(),
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
