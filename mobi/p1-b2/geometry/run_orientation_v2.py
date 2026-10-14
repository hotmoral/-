from __future__ import annotations

import json

from metrics_v2 import motion_metrics, silhouette_occupancy
from orientation_v2 import M0_V2, M1_V2, M2_V2
from turn_2p5d import solve_turn_2p5d

CANDIDATES = ("BM_A", "BM_B", "BM_C")
MORPHOLOGIES = (M0_V2, M1_V2, M2_V2)
SIZES = (48, 64, 80, 96, 112)
SAMPLE_COUNT = 41
BODY_REFS = ("BODY_ROOT", "FOREQUARTER_REF", "PELVIS_REF", "HEAD_ROOT", "TAIL_ROOT")


def run_orientation_matrix(occupancy_grid=48):
    records = []
    for candidate in CANDIDATES:
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                states = [
                    solve_turn_2p5d(candidate, morphology, size_dp, index / (SAMPLE_COUNT - 1))
                    for index in range(SAMPLE_COUNT)
                ]
                errors = []
                for state in states:
                    errors.extend(state.validate())

                metrics = motion_metrics(states)
                max_body_ref_step = 0.0
                for previous, current in zip(states, states[1:]):
                    for name in BODY_REFS:
                        max_body_ref_step = max(
                            max_body_ref_step,
                            (current.anchors[name] - previous.anchors[name]).length(),
                        )

                key_indexes = (0, 10, 20, 30, 40)
                occupancy = [silhouette_occupancy(states[index], occupancy_grid) for index in key_indexes]
                side_width = states[0].visual_bounds.width
                front_width = states[20].visual_bounds.width

                records.append({
                    "schemaVersion": "P1_ORIENTATION_V02_RESULT_V01",
                    "candidate": candidate,
                    "morphology": morphology.id,
                    "sizeDp": size_dp,
                    "sampleCount": SAMPLE_COUNT,
                    "assertions": {"pass": not errors, "errors": errors},
                    "contactMetrics": {
                        "maxPlantedPawDriftDp": metrics["maxPlantedPawDriftDp"],
                        "zeroSupportSampleCount": metrics["zeroSupportSampleCount"],
                        "contactTransitionCount": metrics["contactTransitionCount"],
                    },
                    "orientationMetrics": {
                        "maxAdjacentBodyReferenceStepDp": max_body_ref_step,
                        "frontToProfileVisualWidthRatio": front_width / side_width,
                    },
                    "windowMetrics": {
                        "maxWindowWidthDp": metrics["maxWindowWidthDp"],
                        "maxWindowHeightDp": metrics["maxWindowHeightDp"],
                        "maxWindowAreaDp2": metrics["maxWindowAreaDp2"],
                    },
                    "occupancyMetrics": {
                        "grid": occupancy_grid,
                        "minSilhouetteOccupancyRatio": min(item["silhouetteOccupancyRatio"] for item in occupancy),
                        "meanSilhouetteOccupancyRatio": sum(item["silhouetteOccupancyRatio"] for item in occupancy) / len(occupancy),
                        "maxBlockingSlackAreaDp2": max(item["blockingSlackAreaDp2"] for item in occupancy),
                    },
                })
    return records


if __name__ == "__main__":
    records = run_orientation_matrix()
    summary = {
        "records": len(records),
        "failures": sum(1 for record in records if not record["assertions"]["pass"]),
        "maxPlantedPawDriftDp": max(record["contactMetrics"]["maxPlantedPawDriftDp"] for record in records),
        "maxZeroSupport": max(record["contactMetrics"]["zeroSupportSampleCount"] for record in records),
        "maxAdjacentBodyReferenceStepDp": max(record["orientationMetrics"]["maxAdjacentBodyReferenceStepDp"] for record in records),
        "minFrontToProfileVisualWidthRatio": min(record["orientationMetrics"]["frontToProfileVisualWidthRatio"] for record in records),
        "minSilhouetteOccupancyRatio": min(record["occupancyMetrics"]["minSilhouetteOccupancyRatio"] for record in records),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
