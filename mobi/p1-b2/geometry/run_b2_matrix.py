from __future__ import annotations

import json

from model import M0, M1, M2
from motions_v2 import sample_motion
from metrics_v2 import motion_metrics, silhouette_occupancy

CANDIDATES = ("BM_A", "BM_B", "BM_C")
SIZES = (48, 64, 80, 96, 112)
MORPHS = (M0, M1, M2)
MOTION_SAMPLES = {
    "H2_SLOW_WALK": 41,
    "H3_START_WALK_STOP": 61,
    "H4_SIT_TO_STAND": 31,
    "H6_CHANGE_FACING": 41,
    "H7_NARROW_SHORT_STEP": 41,
}


def run_matrix(occupancy_grid=48):
    records = []
    for candidate in CANDIDATES:
        for morphology in MORPHS:
            for size_dp in SIZES:
                for case_id, sample_count in MOTION_SAMPLES.items():
                    states = [
                        sample_motion(candidate, morphology, case_id, size_dp, index / (sample_count - 1))
                        for index in range(sample_count)
                    ]
                    errors = []
                    for state in states:
                        errors.extend(state.validate())
                    metrics = motion_metrics(states)
                    key_indexes = sorted(set((
                        0,
                        (sample_count - 1) // 4,
                        (sample_count - 1) // 2,
                        3 * (sample_count - 1) // 4,
                        sample_count - 1,
                    )))
                    occupancy = [silhouette_occupancy(states[index], occupancy_grid) for index in key_indexes]
                    records.append({
                        "schemaVersion": "P1_B2_RESULT_V01",
                        "candidate": candidate,
                        "morphology": morphology.id,
                        "sizeDp": size_dp,
                        "caseId": case_id,
                        "sampleCount": sample_count,
                        "assertions": {"pass": not errors, "errors": errors},
                        "contactMetrics": {
                            "maxPlantedPawDriftDp": metrics["maxPlantedPawDriftDp"],
                            "meanPlantedPawDriftDp": metrics["meanPlantedPawDriftDp"],
                            "maxSupportTargetErrorDp": metrics["maxSupportTargetErrorDp"],
                            "contactTransitionCount": metrics["contactTransitionCount"],
                            "zeroSupportSampleCount": metrics["zeroSupportSampleCount"],
                        },
                        "windowMetrics": {
                            "maxWindowWidthDp": metrics["maxWindowWidthDp"],
                            "maxWindowHeightDp": metrics["maxWindowHeightDp"],
                            "maxWindowAreaDp2": metrics["maxWindowAreaDp2"],
                            "minWindowFillX": metrics["minWindowFillX"],
                            "minWindowFillY": metrics["minWindowFillY"],
                            "maxTransparentMarginDp": metrics["maxTransparentMarginDp"],
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
    results = run_matrix()
    summary = {
        "records": len(results),
        "failures": sum(1 for result in results if not result["assertions"]["pass"]),
        "maxPlantedPawDriftDp": max(result["contactMetrics"]["maxPlantedPawDriftDp"] for result in results),
        "maxZeroSupport": max(result["contactMetrics"]["zeroSupportSampleCount"] for result in results),
        "minSilhouetteOccupancyRatio": min(result["occupancyMetrics"]["minSilhouetteOccupancyRatio"] for result in results),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
