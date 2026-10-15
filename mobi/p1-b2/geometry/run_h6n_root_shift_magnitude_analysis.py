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
from run_h6n_root_shift_timing_analysis import (
    PHASE3_ORDER,
    case_shift_interval,
    movement_burden,
)

ONSET_INDEX = 3
S_A_WORST_REPLANT_GUARD = 1.3273
S_A_WORST_STALENESS_GUARD = 0.9420
EPS = 1e-12


def global_o3_interval():
    intervals = []
    for morphology in MORPHOLOGIES:
        for half_stance in HALF_STANCE_VALUES:
            result = case_shift_interval(morphology, half_stance, ONSET_INDEX)
            if not result["feasible"] or result["interval"] is None:
                raise RuntimeError(
                    f"accepted C3Q O3 interval no longer feasible for {morphology.id}/{half_stance}"
                )
            intervals.append(result["interval"])

    lower = max(interval_[0] for interval_ in intervals)
    upper = min(interval_[1] for interval_ in intervals)
    if lower > upper + EPS:
        raise RuntimeError("accepted C3Q O3 global interval became empty")
    return lower, upper


def final_offsets_for_case(morphology, half_stance, final_shift):
    planted = {
        paw: nominal_tangent(paw, morphology, half_stance, 0.0)
        for paw in PAWS
    }
    root_offset = 0.0

    for event_index, paw in enumerate(PHASE3_ORDER):
        yaw_end = (event_index + 1) * YAW_PER_EVENT
        planted[paw] = root_offset + nominal_tangent(
            paw, morphology, half_stance, yaw_end
        )
        if ONSET_INDEX == event_index + 1:
            root_offset = final_shift

    if abs(root_offset - final_shift) > EPS:
        raise RuntimeError("O3 root shift was not applied")

    return {
        paw: planted[paw] - final_shift
        for paw in PAWS
    }


def candidate_case_record(label, shift, morphology, half_stance):
    burden = movement_burden(
        morphology,
        half_stance,
        ONSET_INDEX,
        shift,
    )
    final_offsets = final_offsets_for_case(morphology, half_stance, shift)
    clearances = {
        paw: side_sign(paw) * offset
        for paw, offset in final_offsets.items()
    }
    mismatch = sorted(
        paw for paw, clearance in clearances.items()
        if clearance < -EPS
    )

    if mismatch != burden["finalMismatchPaws"]:
        raise RuntimeError(
            f"clearance/movement-burden mismatch for {label}/{morphology.id}/{half_stance}: "
            f"{mismatch} != {burden['finalMismatchPaws']}"
        )

    return {
        "candidate": label,
        "shiftNormalized": shift,
        "morphologyId": morphology.id,
        "halfStanceBu": half_stance,
        "finalOffsetsNormalized": final_offsets,
        "finalSideClearancesNormalized": clearances,
        "minimumFinalSideClearanceNormalized": min(clearances.values()),
        "meanFinalSideClearanceNormalized": sum(clearances.values()) / len(clearances),
        "finalMismatchPaws": mismatch,
        "finalMismatchCount": len(mismatch),
        "maxReplantDisplacementNormalized": burden["maxReplantDisplacementNormalized"],
        "maxPlantedTargetStalenessNormalized": burden["maxPlantedTargetStalenessNormalized"],
    }


def summarize_candidate(label, shift, lower, upper):
    records = [
        candidate_case_record(label, shift, morphology, half_stance)
        for morphology in MORPHOLOGIES
        for half_stance in HALF_STANCE_VALUES
    ]

    worst_replant = max(record["maxReplantDisplacementNormalized"] for record in records)
    mean_replant = sum(record["maxReplantDisplacementNormalized"] for record in records) / len(records)
    worst_staleness = max(record["maxPlantedTargetStalenessNormalized"] for record in records)
    mean_staleness = sum(record["maxPlantedTargetStalenessNormalized"] for record in records) / len(records)
    global_min_clearance = min(record["minimumFinalSideClearanceNormalized"] for record in records)
    mean_case_min_clearance = sum(record["minimumFinalSideClearanceNormalized"] for record in records) / len(records)
    symmetric_margin = min(shift - lower, upper - shift)
    mismatch_cases = sum(record["finalMismatchCount"] > 0 for record in records)

    gate_a = mismatch_cases == 0
    gate_b_replant = worst_replant <= S_A_WORST_REPLANT_GUARD + EPS
    gate_b_staleness = worst_staleness <= S_A_WORST_STALENESS_GUARD + EPS
    gate_b = gate_b_replant and gate_b_staleness

    return {
        "candidate": label,
        "shiftNormalized": shift,
        "rootTranslationCostNormalized": abs(shift),
        "symmetricFeasibilityMarginNormalized": symmetric_margin,
        "globalMinimumFinalSideClearanceNormalized": global_min_clearance,
        "meanCaseMinimumFinalSideClearanceNormalized": mean_case_min_clearance,
        "worstMaxReplantDisplacementNormalized": worst_replant,
        "meanMaxReplantDisplacementNormalized": mean_replant,
        "worstMaxPlantedTargetStalenessNormalized": worst_staleness,
        "meanMaxPlantedTargetStalenessNormalized": mean_staleness,
        "casesWithFinalMismatch": mismatch_cases,
        "gateAFeasible": gate_a,
        "gateBReplantGuard": gate_b_replant,
        "gateBStalenessGuard": gate_b_staleness,
        "gateBSurvives": gate_b,
        "eligibleForSelection": gate_a and gate_b,
        "records": records,
    }


def select_candidate(summaries):
    eligible = [summary for summary in summaries if summary["eligibleForSelection"]]
    if not eligible:
        return {
            "decision": "NO_MAGNITUDE_SELECTED",
            "selectedCandidate": None,
            "selectedShiftNormalized": None,
        }

    # Gate C: maximize worst-case anatomical-side clearance.
    best_clearance = max(
        summary["globalMinimumFinalSideClearanceNormalized"]
        for summary in eligible
    )
    finalists = [
        summary for summary in eligible
        if abs(summary["globalMinimumFinalSideClearanceNormalized"] - best_clearance) <= EPS
    ]

    # Gate D: if robustness ties, select the lower total movement burden.
    finalists.sort(
        key=lambda summary: (
            summary["rootTranslationCostNormalized"],
            summary["worstMaxReplantDisplacementNormalized"],
            summary["worstMaxPlantedTargetStalenessNormalized"],
            summary["candidate"],
        )
    )
    selected = finalists[0]
    decision_by_label = {
        "T-L": "LOWER_BOUND_SELECTED",
        "T-M": "MIDPOINT_SELECTED",
        "T-U": "UPPER_BOUND_SELECTED",
    }
    return {
        "decision": decision_by_label[selected["candidate"]],
        "selectedCandidate": selected["candidate"],
        "selectedShiftNormalized": selected["shiftNormalized"],
    }


def run_analysis():
    lower, upper = global_o3_interval()
    midpoint = (lower + upper) / 2.0

    candidate_values = (
        ("T-L", lower),
        ("T-M", midpoint),
        ("T-U", upper),
    )
    summaries = [
        summarize_candidate(label, shift, lower, upper)
        for label, shift in candidate_values
    ]
    selection = select_candidate(summaries)

    output = {
        "analysisVersion": "P1_C3T_H6N_ROOT_SHIFT_MAGNITUDE_V1",
        "onsetIndex": ONSET_INDEX,
        "phase3Order": list(PHASE3_ORDER),
        "morphologies": [morphology.id for morphology in MORPHOLOGIES],
        "halfStanceBuValues": list(HALF_STANCE_VALUES),
        "globalShiftIntervalNormalized": [lower, upper],
        "globalShiftIntervalWidthNormalized": upper - lower,
        "mandatoryCandidates": [
            {"candidate": label, "shiftNormalized": shift}
            for label, shift in candidate_values
        ],
        "priorDistortionGuard": {
            "source": "C3S_FULL180_SINGLE_CYCLE_REJECTED_COMPARATOR",
            "worstReplantDisplacementNormalized": S_A_WORST_REPLANT_GUARD,
            "worstPlantedTargetStalenessNormalized": S_A_WORST_STALENESS_GUARD,
        },
        "candidateSummary": summaries,
        "selection": selection,
    }
    output["canonicalAnalysisSha256"] = hashlib.sha256(canonical_bytes(output)).hexdigest()
    return output


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2, sort_keys=True))
