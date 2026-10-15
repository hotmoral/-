from __future__ import annotations

import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from c3w_h6n_fixture_adapter import DIRECTIONS, MORPHOLOGIES, SIZES, build_h6n_fixture
from c3w_renderer_adapter import STRATEGIES, VARIANTS, render_h6n
from run_c3_matrix import _bounds_svg, _shape_svg, canonical_bytes, render_payload

KEY_T = (0.0, 0.2, 0.4, 0.6, 0.7, 0.8, 0.9, 1.0)


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
    for index, shape in enumerate(item["shapes"]):
        if shape["type"] != "polyline":
            continue
        role = str(shape.get("role", ""))
        if "limb" not in role:
            continue
        result.append((index, role, shape["points"]))
    return result


def _crossing_count(item):
    """Pairwise limb-polyline intersection diagnostic.

    All limb pairs are included, even when a legacy generic renderer uses the
    same role string for L/R limbs. This is a structural diagnostic only and is
    never treated as a standalone naturalism score.
    """
    limbs = _limb_polylines(item)
    count = 0
    for left_index in range(len(limbs)):
        _, _, points_a = limbs[left_index]
        for right_index in range(left_index + 1, len(limbs)):
            _, _, points_b = limbs[right_index]
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


def _geometry_payload(item):
    payload = render_payload(item)
    payload.pop("variant", None)
    return payload


def _variant_metrics(items, times):
    visual_areas = [item["visualBounds"].area for item in items]
    partition_areas = [_partition_area_sum(item) for item in items]
    crossing_counts = [_crossing_count(item) for item in items]
    max_cross = max(crossing_counts)
    max_cross_index = crossing_counts.index(max_cross)
    correction_families = sorted({
        correction
        for item in items
        for correction in item.get("corrections", ())
    })
    return {
        "sampleCount": len(items),
        "maxPartitionGroupCount": max(len(item["partitionBounds"]) for item in items),
        "minPartitionGroupCount": min(len(item["partitionBounds"]) for item in items),
        "meanVisualAreaDp2": sum(visual_areas) / len(visual_areas),
        "maxVisualAreaDp2": max(visual_areas),
        "meanPartitionAabbAreaSumDp2": sum(partition_areas) / len(partition_areas),
        "maxPartitionAabbAreaSumDp2": max(partition_areas),
        "maxLimbCrossingPairCount": max_cross,
        "maxLimbCrossingAtT": times[max_cross_index],
        "finalFrontLimbCrossingPairCount": crossing_counts[-1],
        "correctionFamilies": correction_families,
        "correctionFamilyCount": len(correction_families),
        **_step_metrics(items),
    }


def _key_crossings(strategy_items, sample_count):
    result = {}
    for t in KEY_T:
        index = int(round(t * (sample_count - 1)))
        result[f"{t:.2f}"] = _crossing_count(strategy_items[index])
    return result


def run_matrix(sample_count=41):
    if sample_count < 21 or (sample_count - 1) % 5 != 0:
        raise ValueError("sample_count must align all five H6N logical-phase boundaries")

    records = []
    semantic_payloads = []
    times = [index / (sample_count - 1) for index in range(sample_count)]

    for morphology in MORPHOLOGIES:
        for size_dp in SIZES:
            for direction in DIRECTIONS:
                by_strategy = {
                    strategy: {variant: [] for variant in VARIANTS}
                    for strategy in STRATEGIES
                }
                semantic_mismatch = 0
                rf_geometry_mismatch = {strategy: 0 for strategy in STRATEGIES}

                for t in times:
                    fixture = build_h6n_fixture(morphology, size_dp, t, direction)
                    semantic_payloads.append({
                        "direction": direction,
                        "payload": fixture.payload,
                    })
                    for strategy in STRATEGIES:
                        rendered_by_variant = {}
                        for variant in VARIANTS:
                            rendered = render_h6n(fixture, strategy, variant)
                            if rendered["semanticHash"] != fixture.semantic_hash:
                                semantic_mismatch += 1
                            by_strategy[strategy][variant].append(rendered)
                            rendered_by_variant[variant] = rendered
                        if canonical_bytes(_geometry_payload(rendered_by_variant["RF_B"])) != canonical_bytes(
                            _geometry_payload(rendered_by_variant["RF_C"])
                        ):
                            rf_geometry_mismatch[strategy] += 1

                strategy_records = {}
                for strategy in STRATEGIES:
                    rf_b_items = by_strategy[strategy]["RF_B"]
                    rf_c_items = by_strategy[strategy]["RF_C"]
                    strategy_records[strategy] = {
                        "RF_B": _variant_metrics(rf_b_items, times),
                        "RF_C": _variant_metrics(rf_c_items, times),
                        "rfVariantGeometryMismatchCount": rf_geometry_mismatch[strategy],
                        "keyCrossingsRF_B": _key_crossings(rf_b_items, sample_count),
                        "keyCrossingsRF_C": _key_crossings(rf_c_items, sample_count),
                    }

                records.append({
                    "schemaVersion": "P1_C3W_H6N_REPRESENTATION_RESULT_V01",
                    "caseId": by_strategy[STRATEGIES[0]]["RF_B"][0]["caseId"],
                    "morphologyId": morphology.id,
                    "sizeDp": int(size_dp),
                    "direction": int(direction),
                    "sampleCount": sample_count,
                    "semanticHashMismatchCount": semantic_mismatch,
                    "strategies": strategy_records,
                })

    summary = {
        "schemaVersion": "P1_C3W_H6N_REPRESENTATION_SUMMARY_V01",
        "records": len(records),
        "sampleCountPerRecord": sample_count,
        "strategies": list(STRATEGIES),
        "semanticHashMismatchTotal": sum(record["semanticHashMismatchCount"] for record in records),
        "rfVariantGeometryMismatchTotalByStrategy": {
            strategy: sum(
                record["strategies"][strategy]["rfVariantGeometryMismatchCount"]
                for record in records
            )
            for strategy in STRATEGIES
        },
        "maxPartitionGroupCountByStrategy": {
            strategy: max(
                record["strategies"][strategy][variant]["maxPartitionGroupCount"]
                for record in records
                for variant in VARIANTS
            )
            for strategy in STRATEGIES
        },
        "maxLimbCrossingPairCountByStrategy": {
            strategy: max(
                record["strategies"][strategy]["RF_B"]["maxLimbCrossingPairCount"]
                for record in records
            )
            for strategy in STRATEGIES
        },
        "maxCorrectionFamilyCountByStrategy": {
            strategy: max(
                record["strategies"][strategy][variant]["correctionFamilyCount"]
                for record in records
                for variant in VARIANTS
            )
            for strategy in STRATEGIES
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
        if contact.load_bearing:
            parts.append(
                f'<circle cx="{point.x:.4f}" cy="{point.y:.4f}" r="1.4" fill="none" stroke="#555" stroke-width="0.65"/>'
            )
        else:
            r = 1.7
            parts.append(
                f'<line x1="{point.x-r:.4f}" y1="{point.y-r:.4f}" x2="{point.x+r:.4f}" y2="{point.y+r:.4f}" stroke="#777" stroke-width="0.65"/>'
            )
            parts.append(
                f'<line x1="{point.x-r:.4f}" y1="{point.y+r:.4f}" x2="{point.x+r:.4f}" y2="{point.y-r:.4f}" stroke="#777" stroke-width="0.65"/>'
            )
    return "".join(parts)


def render_scorecard(morphology, size_dp, direction):
    cell_w = size_dp * 3.05
    cell_h = size_dp * 1.82
    left_label = 112.0
    top_label = 30.0
    width = left_label + len(KEY_T) * cell_w
    height = top_label + len(STRATEGIES) * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="17" font-family="sans-serif" font-size="10">H6N C3W | {escape(morphology.id)} | {size_dp}dp | dir={direction:+d}</text>',
    ]
    for col, t in enumerate(KEY_T):
        x = left_label + col * cell_w
        parts.append(f'<text x="{x + 3:.4f}" y="17" font-family="sans-serif" font-size="8">t={t:.2f}</text>')

    for row, strategy in enumerate(STRATEGIES):
        y0 = top_label + row * cell_h
        parts.append(f'<text x="5" y="{y0 + 15:.4f}" font-family="sans-serif" font-size="8">{escape(strategy)}</text>')
        for col, t in enumerate(KEY_T):
            fixture = build_h6n_fixture(morphology, size_dp, t, direction)
            rendered = render_h6n(fixture, strategy, "RF_B")
            x0 = left_label + col * cell_w
            parts.append(f'<g transform="translate({x0:.4f},{y0:.4f})">')
            ground_y = size_dp * 1.38
            parts.append(
                f'<line x1="0" y1="{ground_y:.4f}" x2="{size_dp*3.0:.4f}" y2="{ground_y:.4f}" stroke="#bbb" stroke-width="0.45"/>'
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
            for direction in DIRECTIONS:
                path = output_dir / f"H6N_C3W_{morphology.id}_{size_dp}dp_dir{direction:+d}.svg"
                path.write_text(render_scorecard(morphology, size_dp, direction), encoding="utf-8")
                paths.append(path)
    return paths


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir")
    parser.add_argument("--sample-count", type=int, default=41)
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
