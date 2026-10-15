from __future__ import annotations

import hashlib
import json

from run_h6n_phase_origin_analysis import (
    HALF_STANCE_VALUES,
    MORPHOLOGIES,
    PAWS,
    YAW_PER_EVENT,
    canonical_bytes,
    nominal_tangent,
    side_sign,
)
from run_h6n_root_shift_timing_analysis import PHASE3_ORDER, movement_burden

SHIFT_LOW = 0.06470292210167919
SHIFT_HIGH = 0.2878914206844067
SHIFT_MID = (SHIFT_LOW + SHIFT_HIGH) / 2.0
CANDIDATES = (
    ("M_LOW", SHIFT_LOW),
    ("M_MID", SHIFT_MID),
    ("M_HIGH", SHIFT_HIGH),
)
ONSET_INDEX = 3


def final_offsets(morphology, half_stance, shift):
    initial = {
        paw: nominal_tangent(paw, morphology, half_stance, 0.0)
        for paw in PAWS
    }
    fixed = dict(initial)

    for event_index, paw in enumerate(PHASE3_ORDER):
        yaw_end = (event_index + 1) * YAW_PER_EVENT
        root_at_replant = 0.0 if event_index < ONSET_INDEX else shift
        fixed[paw] = root_at_replant + nominal_tangent(
            paw, morphology, half_stance, yaw_end
        )

    return {paw: absolute - shift for paw, absolute in fixed.items()}


def analyze_case(candidate_id, shift, morphology, half_stance):
    offsets = final_offsets(morphology, half_stance, shift)
    margins = {
        paw: side_sign(paw) * offset
        for paw, offset in offsets.items()
    }
    burden = movement_burden(
        morphology,
        half_stance,
        ONSET_INDEX,
        shift,
    )
    return {
        "candidateId": candidate_id,
        "shiftNormalized": shift,
        "morphologyId": morphology.id,
        "halfStanceBu": half_stance,
        "finalOffsetsNormalized": offsets,
        "finalSideMarginsNormalized": margins,
        "minimumFinalSideMarginNormalized": min(margins.values()),
        "meanFinalSideMarginNormalized": sum(margins.values()) / len(margins),
        **burden,
    }


def summarize(candidate_id, shift, records):
    rows = [record for record in records if record["candidateId"] == candidate_id]
    return {
        "candidateId": candidate_id,
        "shiftNormalized": shift,
        "cases": len(rows),
        "minimumFinalSideMarginNormalized": min(
            row["minimumFinalSideMarginNormalized"] for row in rows
        ),
        "meanFinalSideMarginNormalized": sum(
            row["meanFinalSideMarginNormalized"] for row in rows
        ) / len(rows),
        "worstMaxReplantDisplacementNormalized": max(
            row["maxReplantDisplacementNormalized"] for row in rows
        ),
        "meanMaxReplantDisplacementNormalized": sum(
            row["maxReplantDisplacementNormalized"] for row in rows
        ) / len(rows),
        "worstMaxPlantedTargetStalenessNormalized": max(
            row["maxPlantedTargetStalenessNormalized"] for row in rows
        ),
        "meanMaxPlantedTargetStalenessNormalized": sum(
            row["maxPlantedTargetStalenessNormalized"] for row in rows
        ) / len(rows),
        "worstFinalMismatchCount": max(row["finalMismatchCount"] for row in rows),
        "casesWithFinalMismatch": sum(row["finalMismatchCount"] > 0 for row in rows),
    }


def run_analysis():
    records = []
    for candidate_id, shift in CANDIDATES:
        for morphology in MORPHOLOGIES:
            for half_stance in HALF_STANCE_VALUES:
                records.append(
                    analyze_case(candidate_id, shift, morphology, half_stance)
                )

    summaries = [
        summarize(candidate_id, shift, records)
        for candidate_id, shift in CANDIDATES
    ]

    output = {
        "analysisVersion": "P1_C3M_H6N_ROOT_SHIFT_MAGNITUDE_V1",
        "phase3Order": list(PHASE3_ORDER),
        "onsetIndex": ONSET_INDEX,
        "sharedFeasibleIntervalNormalized": [SHIFT_LOW, SHIFT_HIGH],
        "candidateShifts": {
            candidate_id: shift for candidate_id, shift in CANDIDATES
        },
        "morphologies": [morphology.id for morphology in MORPHOLOGIES],
        "halfStanceBuValues": list(HALF_STANCE_VALUES),
        "records": records,
        "candidateSummary": summaries,
    }
    output["canonicalAnalysisSha256"] = hashlib.sha256(canonical_bytes(output)).hexdigest()
    return output


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2, sort_keys=True))
