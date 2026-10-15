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
    smoothstep,
)

PHASE3_ORDER = ("FORE_PAW_L", "HIND_PAW_R", "FORE_PAW_R", "HIND_PAW_L")
EVENT_COUNT = 4
SAMPLE_SUBDIVISIONS = 8


def case_shift_interval(morphology, half_stance, onset_index):
    lower = None
    upper = None
    impossible_paws = []

    for event_index, paw in enumerate(PHASE3_ORDER):
        yaw_end = (event_index + 1) * YAW_PER_EVENT
        nominal = nominal_tangent(paw, morphology, half_stance, yaw_end)
        replanted_before_shift = event_index < onset_index

        if replanted_before_shift:
            if side_sign(paw) < 0.0:
                lower = nominal if lower is None else max(lower, nominal)
            else:
                upper = nominal if upper is None else min(upper, nominal)
        else:
            if side_sign(paw) * nominal < -1e-12:
                impossible_paws.append(paw)

    if impossible_paws:
        return {
            "feasible": False,
            "interval": None,
            "impossiblePostShiftPaws": sorted(impossible_paws),
        }

    if lower is None:
        lower = -1.0e9
    if upper is None:
        upper = +1.0e9

    return {
        "feasible": lower <= upper + 1e-12,
        "interval": [lower, upper],
        "impossiblePostShiftPaws": [],
    }


def _targets_at_start(morphology, half_stance):
    return {
        paw: nominal_tangent(paw, morphology, half_stance, 0.0)
        for paw in PAWS
    }


def movement_burden(morphology, half_stance, onset_index, final_shift):
    fixed = _targets_at_start(morphology, half_stance)
    replant_displacements = []
    max_staleness = 0.0
    root_offset = 0.0

    def account_staleness(yaw, current_root, swing_paw=None):
        nonlocal max_staleness
        for paw, planted in fixed.items():
            if paw == swing_paw:
                continue
            nominal_absolute = current_root + nominal_tangent(
                paw, morphology, half_stance, yaw
            )
            max_staleness = max(max_staleness, abs(planted - nominal_absolute))

    if onset_index == 0:
        account_staleness(0.0, 0.0)
        root_offset = final_shift
        account_staleness(0.0, root_offset)

    for event_index, swing_paw in enumerate(PHASE3_ORDER):
        yaw_start = event_index * YAW_PER_EVENT
        yaw_end = (event_index + 1) * YAW_PER_EVENT

        account_staleness(yaw_start, root_offset)

        old_target = fixed[swing_paw]
        new_target = root_offset + nominal_tangent(
            swing_paw, morphology, half_stance, yaw_end
        )
        replant_displacements.append(abs(new_target - old_target))

        for step in range(1, SAMPLE_SUBDIVISIONS):
            local_u = step / SAMPLE_SUBDIVISIONS
            yaw = (event_index + smoothstep(local_u)) * YAW_PER_EVENT
            account_staleness(yaw, root_offset, swing_paw=swing_paw)

        fixed[swing_paw] = new_target
        account_staleness(yaw_end, root_offset)

        if onset_index == event_index + 1:
            root_offset = final_shift
            account_staleness(yaw_end, root_offset)

    final_offsets = {
        paw: planted - final_shift
        for paw, planted in fixed.items()
    }
    mismatch_paws = sorted(
        paw
        for paw, offset in final_offsets.items()
        if side_sign(paw) * offset < -1e-12
    )
    violation = max(
        (abs(final_offsets[paw]) for paw in mismatch_paws),
        default=0.0,
    )

    return {
        "maxReplantDisplacementNormalized": max(replant_displacements),
        "maxPlantedTargetStalenessNormalized": max_staleness,
        "finalMismatchPaws": mismatch_paws,
        "finalMismatchCount": len(mismatch_paws),
        "maxFinalSideViolationNormalized": violation,
    }


def run_analysis():
    records = []
    onset_summaries = []

    for onset_index in range(EVENT_COUNT + 1):
        case_intervals = []
        all_cases_feasible = True

        for morphology in MORPHOLOGIES:
            for half_stance in HALF_STANCE_VALUES:
                result = case_shift_interval(morphology, half_stance, onset_index)
                record = {
                    "onsetIndex": onset_index,
                    "morphologyId": morphology.id,
                    "halfStanceBu": half_stance,
                    **result,
                }
                records.append(record)
                if not result["feasible"]:
                    all_cases_feasible = False
                elif result["interval"] is not None:
                    case_intervals.append(result["interval"])

        global_interval = None
        globally_feasible = False
        burden_summary = None

        if all_cases_feasible and case_intervals:
            global_lower = max(interval[0] for interval in case_intervals)
            global_upper = min(interval[1] for interval in case_intervals)
            globally_feasible = global_lower <= global_upper + 1e-12
            global_interval = [global_lower, global_upper]

            if globally_feasible:
                comparison_shift = global_lower
                burdens = [
                    movement_burden(
                        morphology,
                        half_stance,
                        onset_index,
                        comparison_shift,
                    )
                    for morphology in MORPHOLOGIES
                    for half_stance in HALF_STANCE_VALUES
                ]
                burden_summary = {
                    "comparisonShiftNormalized": comparison_shift,
                    "worstMaxReplantDisplacementNormalized": max(
                        burden["maxReplantDisplacementNormalized"]
                        for burden in burdens
                    ),
                    "meanMaxReplantDisplacementNormalized": sum(
                        burden["maxReplantDisplacementNormalized"]
                        for burden in burdens
                    ) / len(burdens),
                    "worstMaxPlantedTargetStalenessNormalized": max(
                        burden["maxPlantedTargetStalenessNormalized"]
                        for burden in burdens
                    ),
                    "meanMaxPlantedTargetStalenessNormalized": sum(
                        burden["maxPlantedTargetStalenessNormalized"]
                        for burden in burdens
                    ) / len(burdens),
                    "worstFinalMismatchCount": max(
                        burden["finalMismatchCount"] for burden in burdens
                    ),
                    "casesWithFinalMismatch": sum(
                        burden["finalMismatchCount"] > 0 for burden in burdens
                    ),
                }

        onset_summaries.append({
            "onsetIndex": onset_index,
            "globalShiftFeasible": globally_feasible,
            "globalShiftIntervalNormalized": global_interval,
            "burdenAtMinimumFeasibleShift": burden_summary,
        })

    output = {
        "analysisVersion": "P1_C3Q_H6N_ROOT_SHIFT_TIMING_V1",
        "phase3Order": list(PHASE3_ORDER),
        "morphologies": [morphology.id for morphology in MORPHOLOGIES],
        "halfStanceBuValues": list(HALF_STANCE_VALUES),
        "records": records,
        "onsetSummary": onset_summaries,
        "globallyFeasibleOnsets": [
            summary["onsetIndex"]
            for summary in onset_summaries
            if summary["globalShiftFeasible"]
        ],
    }
    output["canonicalAnalysisSha256"] = hashlib.sha256(canonical_bytes(output)).hexdigest()
    return output


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2, sort_keys=True))
