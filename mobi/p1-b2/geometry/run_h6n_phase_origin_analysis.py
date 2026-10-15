from __future__ import annotations

import hashlib
import json
from math import cos, pi, sin

from orientation_v2 import M0_V2, M1_V2, M2_V2

MORPHOLOGIES = (M1_V2, M0_V2, M2_V2)
HALF_STANCE_VALUES = (0.18, 0.22, 0.26)
PAWS = ("FORE_PAW_L", "FORE_PAW_R", "HIND_PAW_L", "HIND_PAW_R")
LEFT_PAWS = ("FORE_PAW_L", "HIND_PAW_L")
RIGHT_PAWS = ("FORE_PAW_R", "HIND_PAW_R")
EVENT_COUNT = 4
YAW_PER_EVENT = pi / 8.0
SAMPLE_COUNT = 33

BASE_CYCLE = ("HIND_PAW_R", "FORE_PAW_R", "HIND_PAW_L", "FORE_PAW_L")
PHASES = tuple(
    BASE_CYCLE[offset:] + BASE_CYCLE[:offset]
    for offset in range(len(BASE_CYCLE))
)

BASE_LONGITUDINAL = {
    "HIND_PAW_L": -0.58,
    "HIND_PAW_R": -0.32,
    "FORE_PAW_L": +0.30,
    "FORE_PAW_R": +0.56,
}


def canonical_bytes(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def side_sign(paw):
    return +1.0 if paw.endswith("_L") else -1.0


def smoothstep(u):
    return u * u * (3.0 - 2.0 * u)


def nominal_tangent(paw, morphology, half_stance, yaw):
    x_forward = BASE_LONGITUDINAL[paw] * morphology.base.trunk_length
    z_left = side_sign(paw) * half_stance * morphology.stance_width_scale
    return x_forward * cos(yaw) + z_left * sin(yaw)


def targets_after_completed_events(order, morphology, half_stance, completed_events):
    targets = {
        paw: nominal_tangent(paw, morphology, half_stance, 0.0)
        for paw in PAWS
    }
    for event_index in range(completed_events):
        paw = order[event_index]
        yaw_end = (event_index + 1) * YAW_PER_EVENT
        targets[paw] = nominal_tangent(paw, morphology, half_stance, yaw_end)
    return targets


def analyze_case(phase_index, morphology, half_stance):
    order = PHASES[phase_index]
    initial = {
        paw: nominal_tangent(paw, morphology, half_stance, 0.0)
        for paw in PAWS
    }

    replant_displacements = []
    final_targets = dict(initial)
    for event_index, paw in enumerate(order):
        yaw_end = (event_index + 1) * YAW_PER_EVENT
        target = nominal_tangent(paw, morphology, half_stance, yaw_end)
        replant_displacements.append(abs(target - initial[paw]))
        final_targets[paw] = target

    max_staleness = 0.0
    for sample_index in range(SAMPLE_COUNT):
        t = sample_index / (SAMPLE_COUNT - 1)
        scaled = t * EVENT_COUNT
        nearest = round(scaled)
        if abs(scaled - nearest) <= 1e-12:
            completed = int(nearest)
            yaw = completed * YAW_PER_EVENT
            planted = targets_after_completed_events(order, morphology, half_stance, completed)
            swing_paw = None
        else:
            event_index = int(scaled)
            local_u = scaled - event_index
            yaw = (event_index + smoothstep(local_u)) * YAW_PER_EVENT
            planted = targets_after_completed_events(order, morphology, half_stance, event_index)
            swing_paw = order[event_index]

        for paw, planted_tangent in planted.items():
            if paw == swing_paw:
                continue
            nominal = nominal_tangent(paw, morphology, half_stance, yaw)
            max_staleness = max(max_staleness, abs(planted_tangent - nominal))

    mismatches = []
    side_violations = []
    for paw, offset in final_targets.items():
        if side_sign(paw) * offset < -1e-12:
            mismatches.append(paw)
            side_violations.append(abs(offset))

    root_shift_lower = max(final_targets[paw] for paw in RIGHT_PAWS)
    root_shift_upper = min(final_targets[paw] for paw in LEFT_PAWS)
    root_shift_feasible = root_shift_lower <= root_shift_upper + 1e-12

    return {
        "phaseIndex": phase_index,
        "order": list(order),
        "morphologyId": morphology.id,
        "halfStanceBu": half_stance,
        "maxReplantDisplacementNormalized": max(replant_displacements),
        "replantDisplacementsNormalized": replant_displacements,
        "maxPlantedTargetStalenessNormalized": max_staleness,
        "finalTargetsNormalized": final_targets,
        "finalAnatomicalSideMismatchPaws": sorted(mismatches),
        "finalAnatomicalSideMismatchCount": len(mismatches),
        "maxFinalSideViolationNormalized": max(side_violations) if side_violations else 0.0,
        "rootShiftFeasible": root_shift_feasible,
        "rootShiftIntervalNormalized": [root_shift_lower, root_shift_upper],
    }


def phase_summary(phase_index, records):
    phase_records = [record for record in records if record["phaseIndex"] == phase_index]
    global_lower = max(record["rootShiftIntervalNormalized"][0] for record in phase_records)
    global_upper = min(record["rootShiftIntervalNormalized"][1] for record in phase_records)
    return {
        "phaseIndex": phase_index,
        "order": list(PHASES[phase_index]),
        "cases": len(phase_records),
        "worstMaxReplantDisplacementNormalized": max(
            record["maxReplantDisplacementNormalized"] for record in phase_records
        ),
        "meanMaxReplantDisplacementNormalized": sum(
            record["maxReplantDisplacementNormalized"] for record in phase_records
        ) / len(phase_records),
        "worstMaxPlantedTargetStalenessNormalized": max(
            record["maxPlantedTargetStalenessNormalized"] for record in phase_records
        ),
        "meanMaxPlantedTargetStalenessNormalized": sum(
            record["maxPlantedTargetStalenessNormalized"] for record in phase_records
        ) / len(phase_records),
        "worstFinalAnatomicalSideMismatchCount": max(
            record["finalAnatomicalSideMismatchCount"] for record in phase_records
        ),
        "meanFinalAnatomicalSideMismatchCount": sum(
            record["finalAnatomicalSideMismatchCount"] for record in phase_records
        ) / len(phase_records),
        "casesWithFinalSideMismatch": sum(
            record["finalAnatomicalSideMismatchCount"] > 0 for record in phase_records
        ),
        "worstMaxFinalSideViolationNormalized": max(
            record["maxFinalSideViolationNormalized"] for record in phase_records
        ),
        "globalRootShiftIntervalNormalized": [global_lower, global_upper],
        "globalRootShiftFeasible": global_lower <= global_upper + 1e-12,
    }


def run_analysis():
    records = []
    for phase_index in range(len(PHASES)):
        for morphology in MORPHOLOGIES:
            for half_stance in HALF_STANCE_VALUES:
                records.append(analyze_case(phase_index, morphology, half_stance))

    summaries = [phase_summary(phase_index, records) for phase_index in range(len(PHASES))]
    feasible_phases = [
        summary["phaseIndex"]
        for summary in summaries
        if summary["globalRootShiftFeasible"]
    ]
    output = {
        "analysisVersion": "P1_C3P_H6N_PHASE_ORIGIN_V1",
        "sampleCount": SAMPLE_COUNT,
        "morphologies": [morphology.id for morphology in MORPHOLOGIES],
        "halfStanceBuValues": list(HALF_STANCE_VALUES),
        "records": records,
        "phaseSummary": summaries,
        "globallyRootShiftFeasiblePhases": feasible_phases,
    }
    output["canonicalAnalysisSha256"] = hashlib.sha256(canonical_bytes(output)).hexdigest()
    return output


if __name__ == "__main__":
    print(json.dumps(run_analysis(), indent=2, sort_keys=True))
