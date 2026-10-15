from __future__ import annotations

import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from c3_renderer_authored_view_basis_v5 import (
    AUTHORED_VIEW_BASIS_VERSION,
    BASIS_NAMES,
    VIEW_BASES,
    render_fixture as render_fixture_basis,
)
from c3_renderer_minimal_v3 import render_fixture as render_fixture_v3
from c3_renderer_view_resolved_v4 import render_fixture as render_fixture_c3r
from c3_semantic import MORPHOLOGIES, SIZES, build_common_fixture
from run_c3_matrix import _bounds_svg, _shape_svg, canonical_bytes


KEY_T = (0.0, 0.25, 0.50, 0.75, 1.0)
ROWS = ("C3_V3", "C3R_VIEW", "C3V_BASIS")


def _step_metrics(items):
    result = {
        "maxVisualWidthStepDp": 0.0,
        "maxVisualHeightStepDp": 0.0,
        "maxVisualLeftStepDp": 0.0,
        "maxVisualTopStepDp": 0.0,
    }
    previous = None
    for item in items:
        rect = item["visualBounds"]
        if previous is not None:
            old = previous["visualBounds"]
            result["maxVisualWidthStepDp"] = max(result["maxVisualWidthStepDp"], abs(rect.width - old.width))
            result["maxVisualHeightStepDp"] = max(result["maxVisualHeightStepDp"], abs(rect.height - old.height))
            result["maxVisualLeftStepDp"] = max(result["maxVisualLeftStepDp"], abs(rect.left - old.left))
            result["maxVisualTopStepDp"] = max(result["maxVisualTopStepDp"], abs(rect.top - old.top))
        previous = item
    return result


def _partition_area_sum(item):
    return sum(rect.area for rect in item["partitionBounds"].values())


def _variant_metrics(items):
    visual_areas = [item["visualBounds"].area for item in items]
    partition_areas = [_partition_area_sum(item) for item in items]
    return {
        "sampleCount": len(items),
        "maxPartitionGroupCount": max(len(item["partitionBounds"]) for item in items),
        "meanVisualAreaDp2": sum(visual_areas) / len(visual_areas),
        "meanPartitionAabbAreaSumDp2": sum(partition_areas) / len(partition_areas),
        **_step_metrics(items),
    }


def _orientation(a, b, c):
    value = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
    if abs(value) < 1e-9:
        return 0
    return 1 if value > 0 else 2


def _on_segment(a, b, c):
    return (
        min(a.x, c.x) - 1e-9 <= b.x <= max(a.x, c.x) + 1e-9
        and min(a.y, c.y) - 1e-9 <= b.y <= max(a.y, c.y) + 1e-9
    )


def _segments_intersect(p1, q1, p2, q2):
    o1 = _orientation(p1, q1, p2)
    o2 = _orientation(p1, q1, q2)
    o3 = _orientation(p2, q2, p1)
    o4 = _orientation(p2, q2, q1)
    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and _on_segment(p1, p2, q1):
        return True
    if o2 == 0 and _on_segment(p1, q2, q1):
        return True
    if o3 == 0 and _on_segment(p2, p1, q2):
        return True
    if o4 == 0 and _on_segment(p2, q1, q2):
        return True
    return False


def _limb_polylines(item):
    result = []
    for shape in item["shapes"]:
        if shape["type"] != "polyline":
            continue
        role = shape.get("role", "")
        if "limb" not in role:
            continue
        result.append((role, shape["points"]))
    return result


def _crossing_count(item):
    limbs = _limb_polylines(item)
    count = 0
    for left_index in range(len(limbs)):
        role_a, points_a = limbs[left_index]
        for right_index in range(left_index + 1, len(limbs)):
            role_b, points_b = limbs[right_index]
            if role_a == role_b:
                continue
            hit = False
            for a0, a1 in zip(points_a, points_a[1:]):
                for b0, b1 in zip(points_b, points_b[1:]):
                    if _segments_intersect(a0, a1, b0, b1):
                        hit = True
                        break
                if hit:
                    break
            if hit:
                count += 1
    return count


def _front_structure(item):
    roles = [shape["role"] for shape in item["shapes"]]
    return {
        "visualBounds": [
            item["visualBounds"].left,
            item["visualBounds"].top,
            item["visualBounds"].right,
            item["visualBounds"].bottom,
        ],
        "limbCrossingPairCount": _crossing_count(item),
        "drawOrder": roles,
        "basisWeights": list(item.get("basisWeights", ())),
    }


def run_matrix(sample_count=17):
    if sample_count < 5 or sample_count % 2 == 0:
        raise ValueError("sample_count must be odd and >= 5")

    records = []
    semantic_payloads = []
    for morphology in MORPHOLOGIES:
        for size_dp in SIZES:
            v3_items = []
            c3r_items = []
            basis_items = []
            semantic_mismatch = 0

            for index in range(sample_count):
                t = index / (sample_count - 1)
                fixture = build_common_fixture(
                    morphology,
                    "H6_CHANGE_FACING_2P5D",
                    size_dp,
                    t,
                )
                semantic_payloads.append(fixture.payload)
                v3 = render_fixture_v3(fixture, "RF_B")
                c3r = render_fixture_c3r(fixture, "RF_B")
                basis = render_fixture_basis(fixture, "RF_B")
                for item in (v3, c3r, basis):
                    if item["semanticHash"] != fixture.semantic_hash:
                        semantic_mismatch += 1
                v3_items.append(v3)
                c3r_items.append(c3r)
                basis_items.append(basis)

            mid = sample_count // 2
            records.append({
                "schemaVersion": "P1_C3V_H6_RESULT_V01",
                "caseId": "H6_CHANGE_FACING_2P5D",
                "morphologyId": morphology.id,
                "sizeDp": size_dp,
                "sampleCount": sample_count,
                "semanticHashMismatchCount": semantic_mismatch,
                "c3V3": _variant_metrics(v3_items),
                "c3rView": _variant_metrics(c3r_items),
                "c3vBasis": _variant_metrics(basis_items),
                "frontStructure": {
                    "c3V3": _front_structure(v3_items[mid]),
                    "c3rView": _front_structure(c3r_items[mid]),
                    "c3vBasis": _front_structure(basis_items[mid]),
                },
                "profileEndpoints": {
                    "startV3": _front_structure(v3_items[0]),
                    "startBasis": _front_structure(basis_items[0]),
                    "endV3": _front_structure(v3_items[-1]),
                    "endBasis": _front_structure(basis_items[-1]),
                },
            })

    summary = {
        "schemaVersion": "P1_C3V_H6_SUMMARY_V01",
        "authoredViewBasisVersion": AUTHORED_VIEW_BASIS_VERSION,
        "basisNames": list(BASIS_NAMES),
        "basisDefinitionSha256": hashlib.sha256(canonical_bytes(VIEW_BASES)).hexdigest(),
        "records": len(records),
        "sampleCountPerRecord": sample_count,
        "semanticHashMismatchTotal": sum(record["semanticHashMismatchCount"] for record in records),
        "maxPartitionGroupCount": max(record["c3vBasis"]["maxPartitionGroupCount"] for record in records),
        "semanticFixtureSha256": hashlib.sha256(canonical_bytes(semantic_payloads)).hexdigest(),
    }
    summary["canonicalResultsSha256"] = hashlib.sha256(canonical_bytes(records)).hexdigest()
    return records, summary


def _fixture(morphology, size_dp, t):
    return build_common_fixture(morphology, "H6_CHANGE_FACING_2P5D", size_dp, t)


def render_scorecard(morphology, size_dp):
    cell_w = size_dp * 3.05
    cell_h = size_dp * 1.78
    left_label = 88.0
    top_label = 28.0
    width = left_label + len(KEY_T) * cell_w
    height = top_label + len(ROWS) * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="16" font-family="sans-serif" font-size="10">H6 C3V | {escape(morphology.id)} | {size_dp}dp</text>',
    ]
    for col, t in enumerate(KEY_T):
        x = left_label + col * cell_w
        parts.append(f'<text x="{x + 3:.4f}" y="16" font-family="sans-serif" font-size="9">t={t:.2f}</text>')

    for row, label in enumerate(ROWS):
        y0 = top_label + row * cell_h
        parts.append(f'<text x="6" y="{y0 + 15:.4f}" font-family="sans-serif" font-size="8">{label}</text>')
        for col, t in enumerate(KEY_T):
            fixture = _fixture(morphology, size_dp, t)
            if label == "C3_V3":
                rendered = render_fixture_v3(fixture, "RF_B")
            elif label == "C3R_VIEW":
                rendered = render_fixture_c3r(fixture, "RF_B")
            else:
                rendered = render_fixture_basis(fixture, "RF_B")
            x0 = left_label + col * cell_w
            parts.append(f'<g transform="translate({x0:.4f},{y0:.4f})">')
            for group, rect in sorted(rendered["partitionBounds"].items()):
                parts.append(_bounds_svg(rect, group))
            for shape in rendered["shapes"]:
                parts.append(_shape_svg(shape))
            parts.append('</g>')
    parts.append('</svg>')
    return "\n".join(parts)


def write_scorecards(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for morphology in MORPHOLOGIES:
        for size_dp in SIZES:
            path = output_dir / f"H6_C3V_{morphology.id}_{size_dp}dp.svg"
            path.write_text(render_scorecard(morphology, size_dp), encoding="utf-8")
            paths.append(path)
    return paths


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir")
    parser.add_argument("--sample-count", type=int, default=17)
    args = parser.parse_args()

    records, summary = run_matrix(sample_count=args.sample_count)
    print(json.dumps(summary, indent=2, sort_keys=True))

    if args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "results.json").write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
        (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
        scorecards = write_scorecards(out / "scorecards")
        print(f"scorecards={len(scorecards)}")
