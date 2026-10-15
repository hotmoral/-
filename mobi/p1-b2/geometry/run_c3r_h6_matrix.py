from __future__ import annotations

import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from c3_renderer_minimal_v3 import render_fixture as render_fixture_v3
from c3_renderer_view_resolved_v4 import (
    VIEW_REPRESENTATION_VERSION,
    render_fixture as render_fixture_view,
)
from c3_semantic import MORPHOLOGIES, SIZES, build_common_fixture
from run_c3_matrix import _bounds_svg, _shape_svg, canonical_bytes


KEY_T = (0.0, 0.25, 0.50, 0.75, 1.0)
ROWS = ("BASE_V3", "VIEW_V1")


def _step_metrics(items):
    metrics = {
        "maxVisualWidthStepDp": 0.0,
        "maxVisualHeightStepDp": 0.0,
        "maxVisualLeftStepDp": 0.0,
        "maxVisualTopStepDp": 0.0,
    }
    prior = None
    for item in items:
        rect = item["visualBounds"]
        if prior is not None:
            old = prior["visualBounds"]
            metrics["maxVisualWidthStepDp"] = max(
                metrics["maxVisualWidthStepDp"], abs(rect.width - old.width)
            )
            metrics["maxVisualHeightStepDp"] = max(
                metrics["maxVisualHeightStepDp"], abs(rect.height - old.height)
            )
            metrics["maxVisualLeftStepDp"] = max(
                metrics["maxVisualLeftStepDp"], abs(rect.left - old.left)
            )
            metrics["maxVisualTopStepDp"] = max(
                metrics["maxVisualTopStepDp"], abs(rect.top - old.top)
            )
        prior = item
    return metrics


def _partition_area_sum(item):
    return sum(rect.area for rect in item["partitionBounds"].values())


def _front_structure(item):
    by_role = {shape["role"]: shape for shape in item["shapes"]}
    return {
        "visualWidthDp": item["visualBounds"].width,
        "visualHeightDp": item["visualBounds"].height,
        "forequarterRxDp": by_role["forequarter"]["rx"],
        "pelvisRxDp": by_role["pelvis"]["rx"],
        "headRxDp": by_role["head"]["rx"],
        "neckWidthDp": by_role["neck"]["width"],
        "drawOrder": [shape["role"] for shape in item["shapes"]],
        "viewDepthOrder": [
            [shape["role"], shape.get("_viewDepth", 0.0)]
            for shape in item["shapes"]
        ],
    }


def _variant_metrics(items):
    areas = [item["visualBounds"].area for item in items]
    partitions = [_partition_area_sum(item) for item in items]
    return {
        "sampleCount": len(items),
        "maxPartitionGroupCount": max(len(item["partitionBounds"]) for item in items),
        "meanVisualAreaDp2": sum(areas) / len(areas),
        "meanPartitionAabbAreaSumDp2": sum(partitions) / len(partitions),
        **_step_metrics(items),
    }


def run_matrix(sample_count=17):
    if sample_count < 5 or sample_count % 2 == 0:
        raise ValueError("sample_count must be odd and >= 5 so t=0.5 is sampled")

    records = []
    semantic_payloads = []
    for morphology in MORPHOLOGIES:
        for size_dp in SIZES:
            baseline = []
            revised = []
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
                old = render_fixture_v3(fixture, "RF_B")
                new = render_fixture_view(fixture, "RF_B")
                if old["semanticHash"] != fixture.semantic_hash:
                    semantic_mismatch += 1
                if new["semanticHash"] != fixture.semantic_hash:
                    semantic_mismatch += 1
                baseline.append(old)
                revised.append(new)

            mid = sample_count // 2
            records.append({
                "schemaVersion": "P1_C3R_H6_RESULT_V01",
                "caseId": "H6_CHANGE_FACING_2P5D",
                "morphologyId": morphology.id,
                "sizeDp": size_dp,
                "sampleCount": sample_count,
                "semanticHashMismatchCount": semantic_mismatch,
                "baselineV3": _variant_metrics(baseline),
                "viewResolvedV1": _variant_metrics(revised),
                "frontStructure": {
                    "baselineVisualWidthDp": baseline[mid]["visualBounds"].width,
                    "revised": _front_structure(revised[mid]),
                },
                "profileEndpoints": {
                    "startBaselineBounds": [
                        baseline[0]["visualBounds"].left,
                        baseline[0]["visualBounds"].top,
                        baseline[0]["visualBounds"].right,
                        baseline[0]["visualBounds"].bottom,
                    ],
                    "startRevisedBounds": [
                        revised[0]["visualBounds"].left,
                        revised[0]["visualBounds"].top,
                        revised[0]["visualBounds"].right,
                        revised[0]["visualBounds"].bottom,
                    ],
                    "endBaselineBounds": [
                        baseline[-1]["visualBounds"].left,
                        baseline[-1]["visualBounds"].top,
                        baseline[-1]["visualBounds"].right,
                        baseline[-1]["visualBounds"].bottom,
                    ],
                    "endRevisedBounds": [
                        revised[-1]["visualBounds"].left,
                        revised[-1]["visualBounds"].top,
                        revised[-1]["visualBounds"].right,
                        revised[-1]["visualBounds"].bottom,
                    ],
                },
            })

    summary = {
        "schemaVersion": "P1_C3R_H6_SUMMARY_V01",
        "viewRepresentationVersion": VIEW_REPRESENTATION_VERSION,
        "records": len(records),
        "sampleCountPerRecord": sample_count,
        "semanticHashMismatchTotal": sum(
            record["semanticHashMismatchCount"] for record in records
        ),
        "maxPartitionGroupCount": max(
            record["viewResolvedV1"]["maxPartitionGroupCount"]
            for record in records
        ),
        "semanticFixtureSha256": hashlib.sha256(
            canonical_bytes(semantic_payloads)
        ).hexdigest(),
    }
    summary["canonicalResultsSha256"] = hashlib.sha256(
        canonical_bytes(records)
    ).hexdigest()
    return records, summary


def _fixture(morphology, size_dp, t):
    return build_common_fixture(
        morphology,
        "H6_CHANGE_FACING_2P5D",
        size_dp,
        t,
    )


def render_scorecard(morphology, size_dp):
    cell_w = size_dp * 3.05
    cell_h = size_dp * 1.78
    left_label = 80.0
    top_label = 28.0
    width = left_label + len(KEY_T) * cell_w
    height = top_label + len(ROWS) * cell_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.4f} {height:.4f}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="6" y="16" font-family="sans-serif" font-size="10">H6 C3R | {escape(morphology.id)} | {size_dp}dp</text>',
    ]
    for col, t in enumerate(KEY_T):
        x = left_label + col * cell_w
        parts.append(
            f'<text x="{x + 3:.4f}" y="16" font-family="sans-serif" font-size="9">t={t:.2f}</text>'
        )

    for row, label in enumerate(ROWS):
        y0 = top_label + row * cell_h
        parts.append(
            f'<text x="6" y="{y0 + 15:.4f}" font-family="sans-serif" font-size="9">{label}</text>'
        )
        for col, t in enumerate(KEY_T):
            fixture = _fixture(morphology, size_dp, t)
            rendered = (
                render_fixture_v3(fixture, "RF_B")
                if label == "BASE_V3"
                else render_fixture_view(fixture, "RF_B")
            )
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
            path = output_dir / f"H6_C3R_{morphology.id}_{size_dp}dp.svg"
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
        (out / "results.json").write_text(
            json.dumps(records, indent=2, sort_keys=True), encoding="utf-8"
        )
        (out / "summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
        )
        scorecards = write_scorecards(out / "scorecards")
        print(f"scorecards={len(scorecards)}")
