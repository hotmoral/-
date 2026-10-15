from __future__ import annotations

import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from c4_hard_motion_fixture_adapter import (
    CASES,
    H6N,
    MORPHOLOGIES,
    SIZES,
    build_c4_fixture,
    directions_for_case,
    sample_times,
    scorecard_times,
)
from c4_renderer_adapter import CANDIDATE_B, CANDIDATE_C, CANDIDATES, render_c4
from run_c3_matrix import _bounds_svg, _shape_svg, canonical_bytes, render_payload


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


def _limb_crossing_count(item):
    limbs = []
    for shape in item["shapes"]:
        if shape["type"] == "polyline" and "limb" in str(shape.get("role", "")):
            limbs.append(shape["points"])
    count = 0
    for left in range(len(limbs)):
        for right in range(left + 1, len(limbs)):
            hit = False
            for a0, a1 in zip(limbs[left], limbs[left][1:]):
                for b0, b1 in zip(limbs[right], limbs[right][1:]):
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


def _candidate_metrics(items, support_counts, times):
    visual_areas = [item["visualBounds"].area for item in items]
    partition_areas = [_partition_area_sum(item) for item in items]
    correction_families = sorted({
        correction
        for item in items
        for correction in item.get("corrections", ())
    })
    result = {
        "sampleCount": len(items),
        "supportCountMin": min(support_counts),
        "supportCountMax": max(support_counts),
        "correctionFamilies": correction_families,
        "correctionFamilyCount": len(correction_families),
        "maxPartitionGroupCount": max(len(item["partitionBounds"]) for item in items),
        "minPartitionGroupCount": min(len(item["partitionBounds"]) for item in items),
        "meanVisualAreaDp2": sum(visual_areas) / len(visual_areas),
        "maxVisualAreaDp2": max(visual_areas),
        "meanPartitionAabbAreaSumDp2": sum(partition_areas) / len(partition_areas),
        "maxPartitionAabbAreaSumDp2": max(partition_areas),
        **_step_metrics(items),
    }
    if len(items) > 1 and any("limb" in str(shape.get("role", "")) for item in items for shape in item["shapes"]):
        crossings = [_limb_crossing_count(item) for item in items]
        max_cross = max(crossings)
        result["maxLimbCrossingPairCount"] = max_cross
        result["maxLimbCrossingAtT"] = times[crossings.index(max_cross)]
        result["finalLimbCrossingPairCount"] = crossings[-1]
    return result


def run_matrix():
    records = []
    semantic_payloads = []

    for case_id in CASES:
        times = sample_times(case_id)
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in directions_for_case(case_id):
                    by_candidate = {candidate: [] for candidate in CANDIDATES}
                    support_counts = []
                    semantic_mismatch = 0
                    geometry_mismatch = 0

                    for t in times:
                        fixture = build_c4_fixture(morphology, case_id, size_dp, t, direction)
                        semantic_payloads.append({
                            "caseId": case_id,
                            "direction": direction,
                            "payload": fixture.payload,
                        })
                        support_counts.append(len(fixture.state.support_set))
                        rendered = {}
                        for candidate in CANDIDATES:
                            item = render_c4(fixture, candidate)
                            if item["semanticHash"] != fixture.semantic_hash:
                                semantic_mismatch += 1
                            by_candidate[candidate].append(item)
                            rendered[candidate] = item
                        if canonical_bytes(_geometry_payload(rendered[CANDIDATE_B])) != canonical_bytes(
                            _geometry_payload(rendered[CANDIDATE_C])
                        ):
                            geometry_mismatch += 1

                    records.append({
                        "schemaVersion": "P1_C4_HARD_MOTION_RESULT_V01",
                        "caseId": case_id,
                        "morphologyId": morphology.id,
                        "sizeDp": int(size_dp),
                        "direction": int(direction),
                        "sampleCount": len(times),
                        "semanticHashMismatchCount": semantic_mismatch,
                        "candidateGeometryMismatchCount": geometry_mismatch,
                        "candidates": {
                            candidate: _candidate_metrics(by_candidate[candidate], support_counts, times)
                            for candidate in CANDIDATES
                        },
                    })

    correction_families = {
        candidate: sorted({
            correction
            for record in records
            for correction in record["candidates"][candidate]["correctionFamilies"]
        })
        for candidate in CANDIDATES
    }
    geometry_mismatch_by_case = {
        case_id: sum(
            record["candidateGeometryMismatchCount"]
            for record in records
            if record["caseId"] == case_id
        )
        for case_id in CASES
    }
    summary = {
        "schemaVersion": "P1_C4_HARD_MOTION_SUMMARY_V01",
        "records": len(records),
        "cases": list(CASES),
        "semanticHashMismatchTotal": sum(record["semanticHashMismatchCount"] for record in records),
        "correctionFamiliesByCandidate": correction_families,
        "geometryMismatchByCase": geometry_mismatch_by_case,
        "maxPartitionGroupCountByCandidate": {
            candidate: max(
                record["candidates"][candidate]["maxPartitionGroupCount"]
                for record in records
            )
            for candidate in CANDIDATES
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
                f'<line x1="{point.x-extent:.4f}" y1="{point.y:.4f}" x2="{point.x+extent:.4f}" y2="{point.y:.4f}" '
                f'stroke="#444" stroke-width="1.0"/>'
            )
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


def render_scorecard(case_id, morphology, size_dp, direction):
    key_times = scorecard_times(case_id)
    cell_w = size_dp * 3.05
    cell_h = size_dp * 1.82
    left_label = 146.0
    top_label = 30.0
    width = left_label + len(key_times) * cell_w
    height = top_label + len(CANDIDATES) * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="17" font-family="sans-serif" font-size="10">C4 | {escape(case_id)} | {escape(morphology.id)} | {size_dp}dp | dir={direction:+d}</text>',
    ]
    for col, t in enumerate(key_times):
        x = left_label + col * cell_w
        parts.append(f'<text x="{x + 3:.4f}" y="17" font-family="sans-serif" font-size="8">t={t:.2f}</text>')

    for row, candidate in enumerate(CANDIDATES):
        y0 = top_label + row * cell_h
        parts.append(f'<text x="5" y="{y0 + 15:.4f}" font-family="sans-serif" font-size="8">{escape(candidate)}</text>')
        for col, t in enumerate(key_times):
            fixture = build_c4_fixture(morphology, case_id, size_dp, t, direction)
            rendered = render_c4(fixture, candidate)
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
    for case_id in CASES:
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in directions_for_case(case_id):
                    filename = f"C4_{case_id}_{morphology.id}_{size_dp}dp_dir{direction:+d}.svg"
                    path = output_dir / filename
                    path.write_text(
                        render_scorecard(case_id, morphology, size_dp, direction),
                        encoding="utf-8",
                    )
                    paths.append(path)
    return paths


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir")
    args = parser.parse_args()

    records, summary = run_matrix()
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "results.json").write_text(json.dumps(records, indent=2, sort_keys=True), encoding="utf-8")
        (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
        scorecards = write_scorecards(out / "scorecards")
        print(f"scorecards={len(scorecards)}")
