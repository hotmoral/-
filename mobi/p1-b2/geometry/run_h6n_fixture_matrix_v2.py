from __future__ import annotations

import hashlib
import json
from math import pi

from c3_semantic import canonical_bytes, semantic_payload
from h6n_stepped_turn import LATERAL_HALF_STANCE_BU, MIRROR_PAW, PAWS
from h6n_stepped_turn_v2 import (
    LOGICAL_PHASE_COUNT,
    ROOT_SHIFT_NORMALIZED,
    SHIFT_PHASE_INDEX,
    YAW_PER_EVENT,
    event_order,
    shifted_stance_target_s,
    solve_h6n_stepped_turn_v2,
)
from orientation_v2 import M0_V2, M1_V2, M2_V2

MORPHOLOGIES = (M1_V2, M0_V2, M2_V2)
SIZES = (80, 96)
DIRECTIONS = (+1, -1)
HALF_STANCE_VALUES = (0.18, 0.22, 0.26)
EXPECTED_C3T_GLOBAL_MIN_CLEARANCE = 0.11159424929136375


def _note_value(state, prefix):
    for note in state.notes:
        if note.startswith(prefix):
            return note.split("=", 1)[1]
    raise KeyError(prefix)


def _yaw(state):
    return float(_note_value(state, "bodyYawRad="))


def _root_progress(state):
    return float(_note_value(state, "rootShiftProgress="))


def _semantic_state_payload(state, direction, half_stance):
    payload = semantic_payload(state)
    payload["h6nDirection"] = int(direction)
    payload["h6nHalfStanceBu"] = float(half_stance)
    return payload


def _contact_by_owner(state):
    return {contact.owner: contact for contact in state.contacts}


def _side_sign(paw):
    return +1.0 if paw.endswith("_L") else -1.0


def _final_side_diagnostic(state, direction):
    root_x = state.anchors["BODY_ROOT"].x
    scale = state.size_dp / 2.0
    clearances = {}
    mismatches = []
    for paw in PAWS:
        expected_screen_sign = _side_sign(paw) * direction
        normalized_offset = (state.anchors[paw].x - root_x) / scale
        clearance = normalized_offset * expected_screen_sign
        clearances[paw] = clearance
        if clearance < -1e-12:
            mismatches.append(paw)
    return clearances, sorted(mismatches)


def _replant_displacements(morphology, size_dp, direction, half_stance):
    order = event_order(direction)
    phase_pairs = ((0, 1), (1, 2), (2, 3), (4, 5))
    result = []
    scale = size_dp / 2.0
    for event_index, (start_boundary, end_boundary) in enumerate(phase_pairs):
        start = solve_h6n_stepped_turn_v2(
            morphology,
            size_dp,
            start_boundary / LOGICAL_PHASE_COUNT,
            direction,
            half_stance,
        )
        end = solve_h6n_stepped_turn_v2(
            morphology,
            size_dp,
            end_boundary / LOGICAL_PHASE_COUNT,
            direction,
            half_stance,
        )
        paw = order[event_index]
        result.append(abs(end.anchors[paw].x - start.anchors[paw].x) / scale)
    return result


def run_record(morphology, size_dp, direction, sample_count=41):
    if sample_count < 21 or (sample_count - 1) % LOGICAL_PHASE_COUNT != 0:
        raise ValueError("sample_count must align all five logical-phase boundaries")

    states = [
        solve_h6n_stepped_turn_v2(
            morphology,
            size_dp,
            index / (sample_count - 1),
            direction,
        )
        for index in range(sample_count)
    ]
    errors = [error for state in states for error in state.validate()]
    if errors:
        raise RuntimeError((morphology.id, size_dp, direction, errors))

    payloads = [
        _semantic_state_payload(state, direction, LATERAL_HALF_STANCE_BU)
        for state in states
    ]
    yaws = [_yaw(state) for state in states]
    root_progresses = [_root_progress(state) for state in states]
    support_counts = [len(state.support_set) for state in states]
    scale = size_dp / 2.0

    max_staleness = 0.0
    for state, yaw, root_progress in zip(states, yaws, root_progresses):
        contacts = _contact_by_owner(state)
        for paw in PAWS:
            if not contacts[paw].load_bearing:
                continue
            nominal = shifted_stance_target_s(
                paw,
                morphology,
                size_dp,
                direction,
                yaw,
                root_progress,
            )
            max_staleness = max(
                max_staleness,
                abs(contacts[paw].point.x - nominal.x) / scale,
            )

    shift_start_index = int((sample_count - 1) * SHIFT_PHASE_INDEX / LOGICAL_PHASE_COUNT)
    shift_end_index = int((sample_count - 1) * (SHIFT_PHASE_INDEX + 1) / LOGICAL_PHASE_COUNT)
    shift_states = states[shift_start_index:shift_end_index + 1]
    reference_contacts = _contact_by_owner(shift_states[0])
    max_shift_paw_drift = 0.0
    for state in shift_states:
        contacts = _contact_by_owner(state)
        for paw in PAWS:
            dx = contacts[paw].point.x - reference_contacts[paw].point.x
            dy = contacts[paw].point.y - reference_contacts[paw].point.y
            max_shift_paw_drift = max(max_shift_paw_drift, abs(dx), abs(dy))

    root_xs = [state.anchors["BODY_ROOT"].x for state in states]
    root_shift_normalized = (root_xs[-1] - root_xs[0]) / scale
    replants = _replant_displacements(
        morphology,
        size_dp,
        direction,
        LATERAL_HALF_STANCE_BU,
    )
    final_clearances, final_mismatches = _final_side_diagnostic(states[-1], direction)

    return {
        "morphologyId": morphology.id,
        "sizeDp": int(size_dp),
        "direction": int(direction),
        "sampleCount": sample_count,
        "supportCountMin": min(support_counts),
        "supportCountMax": max(support_counts),
        "finalYawRad": yaws[-1],
        "rootShiftNormalized": root_shift_normalized,
        "rootShiftProgressMin": min(root_progresses),
        "rootShiftProgressMax": max(root_progresses),
        "maxShiftPhasePawDriftDp": max_shift_paw_drift,
        "maxSampleRootDeltaNormalized": max(
            abs(root_xs[index + 1] - root_xs[index]) / scale
            for index in range(len(root_xs) - 1)
        ),
        "replantDisplacementsNormalized": replants,
        "maxReplantDisplacementNormalized": max(replants),
        "maxPlantedTargetStalenessNormalized": max_staleness,
        "finalSideClearancesNormalized": final_clearances,
        "minimumFinalSideClearanceNormalized": min(final_clearances.values()),
        "finalAnatomicalSideMismatchPaws": final_mismatches,
        "finalAnatomicalSideMismatchCount": len(final_mismatches),
        "semanticPayloadSha256": hashlib.sha256(canonical_bytes(payloads)).hexdigest(),
    }


def _mirror_error(morphology, size_dp, sample_count):
    maximum = 0.0
    structural = ("BODY_ROOT", "FOREQUARTER_REF", "PELVIS_REF", "HEAD_ROOT", "TAIL_ROOT")
    for index in range(sample_count):
        t = index / (sample_count - 1)
        positive = solve_h6n_stepped_turn_v2(morphology, size_dp, t, +1)
        negative = solve_h6n_stepped_turn_v2(morphology, size_dp, t, -1)
        for anchor in structural:
            maximum = max(
                maximum,
                abs(positive.anchors[anchor].x - negative.anchors[anchor].x),
                abs(positive.anchors[anchor].y - negative.anchors[anchor].y),
            )
        for paw in PAWS:
            mirrored = MIRROR_PAW[paw]
            maximum = max(
                maximum,
                abs(positive.anchors[paw].x - negative.anchors[mirrored].x),
                abs(positive.anchors[paw].y - negative.anchors[mirrored].y),
            )
    return maximum


def run_sensitivity():
    records = []
    for morphology in MORPHOLOGIES:
        for half_stance in HALF_STANCE_VALUES:
            for direction in DIRECTIONS:
                state = solve_h6n_stepped_turn_v2(
                    morphology,
                    80,
                    1.0,
                    direction,
                    half_stance,
                )
                clearances, mismatches = _final_side_diagnostic(state, direction)
                records.append({
                    "morphologyId": morphology.id,
                    "halfStanceBu": half_stance,
                    "direction": direction,
                    "finalSideClearancesNormalized": clearances,
                    "minimumFinalSideClearanceNormalized": min(clearances.values()),
                    "finalMismatchPaws": mismatches,
                    "finalMismatchCount": len(mismatches),
                })

    return records, {
        "records": len(records),
        "globalMinimumFinalSideClearanceNormalized": min(
            record["minimumFinalSideClearanceNormalized"] for record in records
        ),
        "recordsWithFinalMismatch": sum(
            record["finalMismatchCount"] > 0 for record in records
        ),
        "expectedC3TGlobalMinimumFinalSideClearanceNormalized": EXPECTED_C3T_GLOBAL_MIN_CLEARANCE,
    }


def run_matrix(sample_count=41):
    records = [
        run_record(morphology, size_dp, direction, sample_count)
        for morphology in MORPHOLOGIES
        for size_dp in SIZES
        for direction in DIRECTIONS
    ]
    sensitivity_records, sensitivity_summary = run_sensitivity()
    mirror_error = max(
        _mirror_error(morphology, size_dp, sample_count)
        for morphology in MORPHOLOGIES
        for size_dp in SIZES
    )

    summary = {
        "analysisVersion": "P1_C3U_H6N_ROOT_SHIFT_TRAJECTORY_V1",
        "records": len(records),
        "samplesPerRecord": sample_count,
        "supportCountMin": min(record["supportCountMin"] for record in records),
        "supportCountMax": max(record["supportCountMax"] for record in records),
        "rootShiftNormalizedExpected": ROOT_SHIFT_NORMALIZED,
        "maxRootShiftMagnitudeError": max(
            abs(record["rootShiftNormalized"] - ROOT_SHIFT_NORMALIZED)
            for record in records
        ),
        "maxShiftPhasePawDriftDp": max(
            record["maxShiftPhasePawDriftDp"] for record in records
        ),
        "maxMirrorCoordinateErrorDp": mirror_error,
        "maxReplantDisplacementNormalized": max(
            record["maxReplantDisplacementNormalized"] for record in records
        ),
        "maxPlantedTargetStalenessNormalized": max(
            record["maxPlantedTargetStalenessNormalized"] for record in records
        ),
        "recordsWithFinalSideMismatch": sum(
            record["finalAnatomicalSideMismatchCount"] > 0 for record in records
        ),
        "expectedFinalYawMagnitude": pi / 2.0,
        "sensitivity": sensitivity_summary,
    }
    summary["canonicalResultsSha256"] = hashlib.sha256(
        canonical_bytes({
            "records": records,
            "sensitivityRecords": sensitivity_records,
            "summaryWithoutHash": summary,
        })
    ).hexdigest()
    return records, sensitivity_records, summary


if __name__ == "__main__":
    _, _, summary = run_matrix()
    print(json.dumps(summary, indent=2, sort_keys=True))
