from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from math import hypot
from pathlib import Path
from xml.sax.saxutils import escape

from c3_renderers import shape_bounds
from e_v0_fixture_adapter import (
    CASES,
    H1,
    H4,
    H5,
    H6N,
    H7,
    MORPHOLOGIES,
    SIZES,
    build_e_fixture,
    directions_for_case,
    invariant_times,
    scorecard_times,
)
from e_v0_profiles import I1_COMPACT, I2_LANKY, validate_probe_bounds
from e_v0_renderer_adapter import render_e
from run_c3_matrix import _bounds_svg, _shape_svg, canonical_bytes, render_payload

SCHEMA_VERSION = "P1_E_V0_STRUCTURAL_RESULT_V01"
SUMMARY_VERSION = "P1_E_V0_STRUCTURAL_SUMMARY_V01"
PAWS = ("FORE_PAW_L", "FORE_PAW_R", "HIND_PAW_L", "HIND_PAW_R")

BODY_MASS_ROLES = {
    "forequarter",
    "trunk_mass",
    "pelvis",
    "spine_bridge",
    "waist_bridge",
    "semantic_haunch_support_mass",
    "h4_authored_haunch",
    "h4_authored_waist",
    "h4_authored_chest",
    "h4_authored_back_bridge",
}


def _rects_intersect(a, b, eps=1e-9):
    return not (
        a.right < b.left - eps
        or b.right < a.left - eps
        or a.bottom < b.top - eps
        or b.bottom < a.top - eps
    )


def core_mass_connected(rendered):
    masses = [
        shape
        for shape in rendered["shapes"]
        if shape.get("group") == "CORE" and shape.get("role") in BODY_MASS_ROLES
    ]
    if not masses:
        return False
    rects = [shape_bounds(shape) for shape in masses]
    seen = {0}
    frontier = [0]
    while frontier:
        left = frontier.pop()
        for right in range(len(rects)):
            if right in seen:
                continue
            if _rects_intersect(rects[left], rects[right]):
                seen.add(right)
                frontier.append(right)
    return len(seen) == len(rects)


def paw_center_error(rendered, fixture):
    by_role = defaultdict(list)
    for shape in rendered["shapes"]:
        role = shape.get("role")
        if role in PAWS and shape.get("type") == "ellipse":
            by_role[role].append(shape)

    errors = []
    for paw in PAWS:
        shapes = by_role[paw]
        if len(shapes) != 1:
            raise RuntimeError(f"expected exactly one visible paw envelope for {paw}, got {len(shapes)}")
        shape = shapes[0]
        anchor = fixture.state.anchors[paw]
        errors.append(hypot(shape["cx"] - anchor.x, shape["cy"] - anchor.y))
    return max(errors)


def _partition_area(rendered):
    return sum(rect.area for rect in rendered["partitionBounds"].values())


def _shape_group_counts(rendered):
    counts = defaultdict(int)
    for shape in rendered["shapes"]:
        counts[shape["group"]] += 1
    return dict(sorted(counts.items()))


def _ear_count(rendered):
    return sum(1 for shape in rendered["shapes"] if str(shape.get("role", "")).startswith("ear"))


def _tail_count(rendered):
    return sum(1 for shape in rendered["shapes"] if shape.get("role") == "tail")


def _geometry_hash(rendered):
    payload = render_payload(rendered)
    payload.pop("semanticHash", None)
    payload.pop("morphologyId", None)
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def _anchor_span(fixture):
    fore = fixture.state.anchors["FOREQUARTER_REF"]
    pelvis = fixture.state.anchors["PELVIS_REF"]
    return hypot(fore.x - pelvis.x, fore.y - pelvis.y)


def _record_for(case_id, morphology, size_dp, direction, fixture, rendered):
    yaw = float(fixture.payload.get("orientation", {}).get("yawRad", 0.0))
    return {
        "schemaVersion": SCHEMA_VERSION,
        "caseId": case_id,
        "morphologyId": morphology.id,
        "sizeDp": int(size_dp),
        "direction": int(direction),
        "t": round(float(fixture.t), 9),
        "yawRad": round(yaw, 9),
        "semanticHash": fixture.semantic_hash,
        "semanticHashMatch": rendered["semanticHash"] == fixture.semantic_hash,
        "corrections": list(rendered.get("corrections", ())),
        "shapeCount": len(rendered["shapes"]),
        "shapeCountByGroup": _shape_group_counts(rendered),
        "partitionCount": len(rendered["partitionBounds"]),
        "partitionAabbAreaSumDp2": round(_partition_area(rendered), 9),
        "visualAreaDp2": round(rendered["visualBounds"].area, 9),
        "visualWidthDp": round(rendered["visualBounds"].width, 9),
        "visualHeightDp": round(rendered["visualBounds"].height, 9),
        "maxVisiblePawCenterErrorDp": round(paw_center_error(rendered, fixture), 12),
        "coreMassConnected": core_mass_connected(rendered),
        "earPrimitiveCount": _ear_count(rendered),
        "tailPrimitiveCount": _tail_count(rendered),
        "geometrySha256": _geometry_hash(rendered),
        "forePelvisSpanDp": round(_anchor_span(fixture), 9),
        "readabilityAidMode": rendered["readabilityAidMode"],
        "structuralDirection": rendered["structuralDirection"],
    }


def run_matrix():
    probe_check = validate_probe_bounds()
    if not probe_check["pass"]:
        raise RuntimeError(probe_check)

    records = []
    semantic_payloads = []
    for case_id in CASES:
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in directions_for_case(case_id):
                    for t in invariant_times(case_id):
                        fixture = build_e_fixture(morphology, case_id, size_dp, t, direction)
                        rendered = render_e(fixture)
                        semantic_payloads.append({
                            "caseId": case_id,
                            "morphologyId": morphology.id,
                            "sizeDp": size_dp,
                            "direction": direction,
                            "payload": fixture.payload,
                        })
                        records.append(_record_for(
                            case_id, morphology, size_dp, direction, fixture, rendered
                        ))

    group_stats = {}
    for morphology in MORPHOLOGIES:
        for size_dp in SIZES:
            subset = [
                record for record in records
                if record["morphologyId"] == morphology.id and record["sizeDp"] == size_dp
            ]
            group_stats[f"{morphology.id}|{size_dp}"] = {
                "sampleCount": len(subset),
                "meanVisualAreaDp2": round(sum(r["visualAreaDp2"] for r in subset) / len(subset), 9),
                "meanPartitionAabbAreaSumDp2": round(
                    sum(r["partitionAabbAreaSumDp2"] for r in subset) / len(subset), 9
                ),
                "maxPartitionCount": max(r["partitionCount"] for r in subset),
            }

    compact = next(
        record for record in records
        if record["caseId"] == H1 and record["morphologyId"] == I1_COMPACT.id
        and record["sizeDp"] == 80 and record["direction"] == 1
    )
    lanky = next(
        record for record in records
        if record["caseId"] == H1 and record["morphologyId"] == I2_LANKY.id
        and record["sizeDp"] == 80 and record["direction"] == 1
    )

    all_corrections = sorted({
        correction for record in records for correction in record["corrections"]
    })
    non_h4_corrections = sum(
        len(record["corrections"])
        for record in records
        if record["caseId"] != H4
    )

    summary = {
        "schemaVersion": SUMMARY_VERSION,
        "recordCount": len(records),
        "morphologies": [m.id for m in MORPHOLOGIES],
        "sizesDp": list(SIZES),
        "cases": list(CASES),
        "probeBounds": probe_check,
        "semanticHashMismatchTotal": sum(not r["semanticHashMatch"] for r in records),
        "maxVisiblePawCenterErrorDp": max(r["maxVisiblePawCenterErrorDp"] for r in records),
        "maxPartitionCount": max(r["partitionCount"] for r in records),
        "coreDisconnectCount": sum(not r["coreMassConnected"] for r in records),
        "tailPrimitiveMismatchCount": sum(r["tailPrimitiveCount"] != 1 for r in records),
        "minimumEarPrimitiveCount": min(r["earPrimitiveCount"] for r in records),
        "correctionFamilies": all_corrections,
        "nonH4CorrectionUseCount": non_h4_corrections,
        "readabilityAidModes": sorted({r["readabilityAidMode"] for r in records}),
        "groupStats": group_stats,
        "compactVsLankyNeutral80": {
            "geometryHashesDiffer": compact["geometrySha256"] != lanky["geometrySha256"],
            "visualWidthDeltaDp": round(lanky["visualWidthDp"] - compact["visualWidthDp"], 9),
            "visualHeightDeltaDp": round(lanky["visualHeightDp"] - compact["visualHeightDp"], 9),
            "forePelvisSpanDeltaDp": round(lanky["forePelvisSpanDp"] - compact["forePelvisSpanDp"], 9),
        },
        "semanticFixtureSha256": hashlib.sha256(canonical_bytes(semantic_payloads)).hexdigest(),
    }
    summary["canonicalResultsSha256"] = hashlib.sha256(canonical_bytes(records)).hexdigest()
    return records, summary


def _contact_marker_svg(fixture):
    parts = []
    for contact in fixture.state.contacts:
        point = contact.point
        if point is None:
            continue
        if contact.kind.value == "BODY_PATCH":
            extent = contact.tangent_extent_dp or 2.0
            parts.append(
                f'<line x1="{point.x-extent:.4f}" y1="{point.y:.4f}" x2="{point.x+extent:.4f}" y2="{point.y:.4f}" stroke="#555" stroke-width="0.9"/>'
            )
        elif contact.load_bearing:
            parts.append(
                f'<circle cx="{point.x:.4f}" cy="{point.y:.4f}" r="1.35" fill="none" stroke="#555" stroke-width="0.65"/>'
            )
        else:
            r = 1.5
            parts.append(
                f'<line x1="{point.x-r:.4f}" y1="{point.y-r:.4f}" x2="{point.x+r:.4f}" y2="{point.y+r:.4f}" stroke="#777" stroke-width="0.6"/>'
            )
            parts.append(
                f'<line x1="{point.x-r:.4f}" y1="{point.y+r:.4f}" x2="{point.x+r:.4f}" y2="{point.y-r:.4f}" stroke="#777" stroke-width="0.6"/>'
            )
    return "".join(parts)


def _sheet_samples():
    return (
        (H1, 0.0, +1, "neutral"),
        (H4, 0.0, +1, "sit"),
        (H4, 0.5, +1, "rise"),
        (H4, 1.0, +1, "stand"),
        (H5, 0.0, +1, "crouch"),
        (H6N, 0.0, +1, "profile"),
        (H6N, 0.4, +1, "three-quarter"),
        (H6N, 1.0, +1, "front"),
        (H7, 0.0, +1, "narrow-start"),
        (H7, 0.5, +1, "narrow-mid"),
        (H7, 1.0, +1, "narrow-end"),
    )


def render_scorecard(morphology, size_dp):
    samples = _sheet_samples()
    cell_w = size_dp * 2.55
    cell_h = size_dp * 1.78
    columns = 4
    rows = (len(samples) + columns - 1) // columns
    width = columns * cell_w
    height = 30.0 + rows * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="17" font-family="sans-serif" font-size="10">P1-E V0 | {escape(morphology.id)} | {size_dp}dp</text>',
    ]
    for index, (case_id, t, direction, label) in enumerate(samples):
        col = index % columns
        row = index // columns
        x0 = col * cell_w
        y0 = 30.0 + row * cell_h
        fixture = build_e_fixture(morphology, case_id, size_dp, t, direction)
        rendered = render_e(fixture)
        parts.append(f'<g transform="translate({x0:.4f},{y0:.4f})">')
        parts.append(f'<text x="3" y="10" font-family="sans-serif" font-size="7">{escape(label)}</text>')
        ground_y = size_dp * 1.38
        parts.append(
            f'<line x1="0" y1="{ground_y:.4f}" x2="{cell_w-3:.4f}" y2="{ground_y:.4f}" stroke="#bbb" stroke-width="0.45"/>'
        )
        for group, rect in sorted(rendered["partitionBounds"].items()):
            parts.append(_bounds_svg(rect, group))
        for shape in rendered["shapes"]:
            parts.append(_shape_svg(shape))
        parts.append(_contact_marker_svg(fixture))
        parts.append('</g>')
    parts.append('</svg>')
    return "\n".join(parts)


def write_scorecards(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for morphology in MORPHOLOGIES:
        for size_dp in SIZES:
            path = output_dir / f"P1E_V0_{morphology.id}_{size_dp}dp.svg"
            path.write_text(render_scorecard(morphology, size_dp), encoding="utf-8")
            paths.append(path)
    return paths


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    records, summary = run_matrix()
    (out / "results.json").write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    scorecards = write_scorecards(out / "scorecards")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"scorecards={len(scorecards)}")
