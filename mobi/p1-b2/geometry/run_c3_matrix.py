from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

from c3_renderers import GROUPS, render_fixture
from c3_semantic import CASES, MORPHOLOGIES, SIZES, build_fixture_matrix

VARIANTS = ("RF_B", "RF_C")
KEY_T = (0.0, 0.25, 0.50, 0.75, 1.0)


def _round(value):
    return round(float(value), 9)


def _rect_payload(rect):
    return [_round(rect.left), _round(rect.top), _round(rect.right), _round(rect.bottom)]


def _point_payload(point):
    return [_round(point.x), _round(point.y)]


def _shape_payload(shape):
    result = {
        "type": shape["type"],
        "role": shape["role"],
        "group": shape["group"],
    }
    kind = shape["type"]
    if kind == "ellipse":
        result.update({
            "cx": _round(shape["cx"]),
            "cy": _round(shape["cy"]),
            "rx": _round(shape["rx"]),
            "ry": _round(shape["ry"]),
        })
    elif kind == "line":
        result.update({
            "p0": _point_payload(shape["p0"]),
            "p1": _point_payload(shape["p1"]),
            "width": _round(shape["width"]),
        })
    elif kind == "polyline":
        result.update({
            "points": [_point_payload(point) for point in shape["points"]],
            "width": _round(shape["width"]),
        })
    elif kind == "polygon":
        result["points"] = [_point_payload(point) for point in shape["points"]]
    else:
        raise ValueError(kind)
    return result


def render_payload(rendered):
    return {
        "variant": rendered["variant"],
        "semanticHash": rendered["semanticHash"],
        "caseId": rendered["caseId"],
        "morphologyId": rendered["morphologyId"],
        "sizeDp": rendered["sizeDp"],
        "t": _round(rendered["t"]),
        "visualBounds": _rect_payload(rendered["visualBounds"]),
        "partitionBounds": {
            group: _rect_payload(rect)
            for group, rect in sorted(rendered["partitionBounds"].items())
        },
        "corrections": list(rendered["corrections"]),
        "shapes": [_shape_payload(shape) for shape in rendered["shapes"]],
    }


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _step_metrics(items):
    max_width_step = 0.0
    max_height_step = 0.0
    max_left_step = 0.0
    max_top_step = 0.0
    previous = None
    for rendered in items:
        rect = rendered["visualBounds"]
        if previous is not None:
            prior = previous["visualBounds"]
            max_width_step = max(max_width_step, abs(rect.width - prior.width))
            max_height_step = max(max_height_step, abs(rect.height - prior.height))
            max_left_step = max(max_left_step, abs(rect.left - prior.left))
            max_top_step = max(max_top_step, abs(rect.top - prior.top))
        previous = rendered
    return {
        "maxVisualWidthStepDp": max_width_step,
        "maxVisualHeightStepDp": max_height_step,
        "maxVisualLeftStepDp": max_left_step,
        "maxVisualTopStepDp": max_top_step,
    }


def run_c3_matrix(sample_count=17):
    fixtures = build_fixture_matrix(sample_count=sample_count)
    grouped = defaultdict(lambda: {variant: [] for variant in VARIANTS})
    semantic_payloads = []

    for fixture in fixtures:
        semantic_payloads.append(fixture.payload)
        key = (fixture.case_id, fixture.morphology_id, fixture.size_dp)
        for variant in VARIANTS:
            grouped[key][variant].append(render_fixture(fixture, variant))

    records = []
    for key in sorted(grouped):
        case_id, morphology_id, size_dp = key
        by_variant = grouped[key]
        semantic_mismatch = 0
        for rf_b, rf_c in zip(by_variant["RF_B"], by_variant["RF_C"]):
            if rf_b["semanticHash"] != rf_c["semanticHash"]:
                semantic_mismatch += 1

        variant_records = {}
        for variant in VARIANTS:
            items = by_variant[variant]
            correction_families = sorted({
                correction
                for item in items
                for correction in item["corrections"]
            })
            partition_counts = [len(item["partitionBounds"]) for item in items]
            shape_counts = [len(item["shapes"]) for item in items]
            visual_areas = [item["visualBounds"].area for item in items]
            partition_union_area = []
            for item in items:
                bounds = list(item["partitionBounds"].values())
                partition_union_area.append(sum(rect.area for rect in bounds))
            variant_records[variant] = {
                "sampleCount": len(items),
                "correctionFamilies": correction_families,
                "correctionFamilyCount": len(correction_families),
                "maxPartitionGroupCount": max(partition_counts),
                "minPartitionGroupCount": min(partition_counts),
                "maxShapeCount": max(shape_counts),
                "minShapeCount": min(shape_counts),
                "maxVisualAreaDp2": max(visual_areas),
                "meanVisualAreaDp2": sum(visual_areas) / len(visual_areas),
                "meanPartitionAabbAreaSumDp2": sum(partition_union_area) / len(partition_union_area),
                **_step_metrics(items),
            }

        records.append({
            "schemaVersion": "P1_C3_DISCRIMINATOR_RESULT_V01",
            "caseId": case_id,
            "morphologyId": morphology_id,
            "sizeDp": size_dp,
            "sampleCount": sample_count,
            "semanticHashMismatchCount": semantic_mismatch,
            "variants": variant_records,
        })

    semantic_digest = hashlib.sha256(canonical_bytes(semantic_payloads)).hexdigest()
    result_digest = hashlib.sha256(canonical_bytes(records)).hexdigest()
    summary = {
        "schemaVersion": "P1_C3_DISCRIMINATOR_SUMMARY_V01",
        "records": len(records),
        "sampleCountPerRecord": sample_count,
        "totalSemanticFixtures": len(fixtures),
        "semanticHashMismatchTotal": sum(record["semanticHashMismatchCount"] for record in records),
        "semanticFixtureSha256": semantic_digest,
        "canonicalResultsSha256": result_digest,
        "rfCCorrectionFamilies": sorted({
            correction
            for record in records
            for correction in record["variants"]["RF_C"]["correctionFamilies"]
        }),
        "rfBMaxCorrectionFamilyCount": max(record["variants"]["RF_B"]["correctionFamilyCount"] for record in records),
        "rfCMaxCorrectionFamilyCountPerRecord": max(record["variants"]["RF_C"]["correctionFamilyCount"] for record in records),
        "maxPartitionGroupCount": max(
            record["variants"][variant]["maxPartitionGroupCount"]
            for record in records
            for variant in VARIANTS
        ),
    }
    return records, summary


def _points_svg(points):
    return " ".join(f"{point.x:.4f},{point.y:.4f}" for point in points)


def _shape_svg(shape):
    kind = shape["type"]
    role = escape(shape["role"])
    if kind == "ellipse":
        return (
            f'<ellipse data-role="{role}" cx="{shape["cx"]:.4f}" cy="{shape["cy"]:.4f}" '
            f'rx="{shape["rx"]:.4f}" ry="{shape["ry"]:.4f}" fill="black"/>'
        )
    if kind == "line":
        return (
            f'<line data-role="{role}" x1="{shape["p0"].x:.4f}" y1="{shape["p0"].y:.4f}" '
            f'x2="{shape["p1"].x:.4f}" y2="{shape["p1"].y:.4f}" '
            f'stroke="black" stroke-width="{shape["width"]:.4f}" stroke-linecap="round"/>'
        )
    if kind == "polyline":
        return (
            f'<polyline data-role="{role}" points="{_points_svg(shape["points"])}" fill="none" '
            f'stroke="black" stroke-width="{shape["width"]:.4f}" stroke-linecap="round" '
            f'stroke-linejoin="round"/>'
        )
    if kind == "polygon":
        return f'<polygon data-role="{role}" points="{_points_svg(shape["points"])}" fill="black"/>'
    raise ValueError(kind)


def _bounds_svg(rect, group):
    dash = {
        "CORE": "2,2",
        "FORE": "3,2",
        "HIND": "4,2",
        "TAIL": "5,2",
    }[group]
    return (
        f'<rect x="{rect.left:.4f}" y="{rect.top:.4f}" width="{rect.width:.4f}" height="{rect.height:.4f}" '
        f'fill="none" stroke="#999" stroke-width="0.55" stroke-dasharray="{dash}"/>'
    )


def _scorecard_fixture(case_id, morphology, size_dp, t):
    from c3_semantic import build_common_fixture
    return build_common_fixture(morphology, case_id, size_dp, t)


def render_scorecard(case_id, morphology, size_dp):
    cell_w = size_dp * 3.05
    cell_h = size_dp * 1.78
    left_label = 70.0
    top_label = 28.0
    width = left_label + len(KEY_T) * cell_w
    height = top_label + len(VARIANTS) * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="16" font-family="sans-serif" font-size="10">{escape(case_id)} | {escape(morphology.id)} | {size_dp}dp</text>',
    ]
    for col, t in enumerate(KEY_T):
        x = left_label + col * cell_w
        parts.append(f'<text x="{x + 3:.4f}" y="16" font-family="sans-serif" font-size="9">t={t:.2f}</text>')

    for row, variant in enumerate(VARIANTS):
        y0 = top_label + row * cell_h
        parts.append(f'<text x="6" y="{y0 + 15:.4f}" font-family="sans-serif" font-size="10">{variant}</text>')
        for col, t in enumerate(KEY_T):
            fixture = _scorecard_fixture(case_id, morphology, size_dp, t)
            rendered = render_fixture(fixture, variant)
            x0 = left_label + col * cell_w
            parts.append(f'<g transform="translate({x0:.4f},{y0:.4f})">')
            parts.extend(_shape_svg(shape) for shape in rendered["shapes"])
            parts.extend(
                _bounds_svg(rect, group)
                for group, rect in sorted(rendered["partitionBounds"].items())
            )
            parts.append('</g>')
    parts.append('</svg>')
    return "".join(parts)


def write_scorecards(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for case_id in CASES:
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                filename = f"{case_id}_{morphology.id}_{size_dp}dp.svg"
                (output_dir / filename).write_text(
                    render_scorecard(case_id, morphology, size_dp),
                    encoding="utf-8",
                )
                manifest.append(filename)
    (output_dir / "MANIFEST.txt").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir")
    parser.add_argument("--sample-count", type=int, default=17)
    args = parser.parse_args()

    records, summary = run_c3_matrix(sample_count=args.sample_count)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "results.json").write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
        (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
        scorecards = write_scorecards(out / "scorecards")
        print(f"scorecards={len(scorecards)}")
