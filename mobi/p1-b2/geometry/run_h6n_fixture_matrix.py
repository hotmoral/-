from __future__ import annotations

import hashlib
import json
from math import pi

from c3_semantic import canonical_bytes, semantic_payload
from h6n_stepped_turn import (
    EVENT_COUNT,
    MIRROR_PAW,
    PAWS,
    YAW_PER_EVENT,
    event_order,
    solve_h6n_stepped_turn,
    stance_target_s,
)
from orientation_v2 import M0_V2, M1_V2, M2_V2

MORPHOLOGIES = (M1_V2, M0_V2, M2_V2)
SIZES = (80, 96)
DIRECTIONS = (+1, -1)


def _note_value(state, prefix):
    for note in state.notes:
        if note.startswith(prefix):
            return note.split("=", 1)[1]
    raise KeyError(prefix)


def _yaw(state):
    return float(_note_value(state, "bodyYawRad="))


def _contact_by_owner(state):
    return {contact.owner: contact for contact in state.contacts}


def _semantic_state_payload(state, direction):
    payload = semantic_payload(state)
    payload["h6nDirection"] = int(direction)
    return payload


def _semantic_state_hash(state, direction):
    return hashlib.sha256(canonical_bytes(_semantic_state_payload(state, direction))).hexdigest()


def _replant_metrics(morphology, size_dp, direction):
    order = event_order(direction)
    previous = {
        paw: stance_target_s(paw, morphology, size_dp, direction, 0.0)
        for paw in PAWS
    }
    scale = size_dp / 2.0
    displacements = []
    for event_index, paw in enumerate(order):
        yaw_end = direction * (event_index + 1) * YAW_PER_EVENT
        target = stance_target_s(paw, morphology, size_dp, direction, yaw_end)
        displacements.append(abs(target.x - previous[paw].x) / scale)
        previous[paw] = target
    return displacements


def _final_side_diagnostic(state, direction):
    root_x = state.anchors["BODY_ROOT"].x
    scale = state.size_dp / 2.0
    mismatches = []
    magnitudes = []
    for paw in PAWS:
        anatomical_sign = +1.0 if paw.endswith("_L") else -1.0
        expected_screen_sign = anatomical_sign * direction
        offset = state.anchors[paw].x - root_x
        if offset * expected_screen_sign < -1e-12:
            mismatches.append(paw)
            magnitudes.append(abs(offset) / scale)
    return mismatches, magnitudes


def run_record(morphology, size_dp, direction, sample_count=33):
    if sample_count < 17 or (sample_count - 1) % EVENT_COUNT != 0:
        raise ValueError("sample_count must align all four event boundaries")

    states = [
        solve_h6n_stepped_turn(
            morphology=morphology,
            size_dp=size_dp,
            t=index / (sample_count - 1),
            direction=direction,
        )
        for index in range(sample_count)
    ]

    errors = [error for state in states for error in state.validate()]
    if errors:
        raise RuntimeError((morphology.id, size_dp, direction, errors))

    payloads = [_semantic_state_payload(state, direction) for state in states]
    hashes = [_semantic_state_hash(state, direction) for state in states]
    support_counts = [len(state.support_set) for state in states]
    yaws = [_yaw(state) for state in states]
    scale = size_dp / 2.0

    max_staleness = 0.0
    for state, yaw in zip(states, yaws):
        contacts = _contact_by_owner(state)
        for paw in PAWS:
            if not contacts[paw].load_bearing:
                continue
            nominal = stance_target_s(paw, morphology, size_dp, direction, yaw)
            max_staleness = max(
                max_staleness,
                abs(contacts[paw].point.x - nominal.x) / scale,
            )

    replant_displacements = _replant_metrics(morphology, size_dp, direction)
    final_mismatches, final_magnitudes = _final_side_diagnostic(states[-1], direction)

    return {
        "morphologyId": morphology.id,
        "sizeDp": int(size_dp),
        "direction": int(direction),
        "sampleCount": sample_count,
        "semanticHashes": hashes,
        "supportCountMin": min(support_counts),
        "supportCountMax": max(support_counts),
        "finalYawRad": yaws[-1],
        "maxSampleYawDeltaRad": max(
            abs(yaws[index + 1] - yaws[index])
            for index in range(len(yaws) - 1)
        ),
        "replantDisplacementsNormalized": replant_displacements,
        "maxReplantDisplacementNormalized": max(replant_displacements),
        "maxPlantedTargetStalenessNormalized": max_staleness,
        "finalAnatomicalSideMismatchPaws": final_mismatches,
        "finalAnatomicalSideMismatchCount": len(final_mismatches),
        "maxFinalSideViolationNormalized": max(final_magnitudes) if final_magnitudes else 0.0,
        "finalPawPoints": {
            paw: [states[-1].anchors[paw].x, states[-1].anchors[paw].y]
            for paw in PAWS
        },
        "semanticPayloadSha256": hashlib.sha256(canonical_bytes(payloads)).hexdigest(),
    }


def run_matrix(sample_count=33):
    records = []
    for morphology in MORPHOLOGIES:
        for size_dp in SIZES:
            for direction in DIRECTIONS:
                records.append(run_record(morphology, size_dp, direction, sample_count))

    summary = {
        "records": len(records),
        "samplesPerRecord": sample_count,
        "supportCountMin": min(record["supportCountMin"] for record in records),
        "supportCountMax": max(record["supportCountMax"] for record in records),
        "maxReplantDisplacementNormalized": max(
            record["maxReplantDisplacementNormalized"] for record in records
        ),
        "maxPlantedTargetStalenessNormalized": max(
            record["maxPlantedTargetStalenessNormalized"] for record in records
        ),
        "maxFinalAnatomicalSideMismatchCount": max(
            record["finalAnatomicalSideMismatchCount"] for record in records
        ),
        "recordsWithFinalSideMismatch": sum(
            record["finalAnatomicalSideMismatchCount"] > 0 for record in records
        ),
        "maxFinalSideViolationNormalized": max(
            record["maxFinalSideViolationNormalized"] for record in records
        ),
        "expectedFinalYawMagnitude": pi / 2.0,
    }
    summary["canonicalResultsSha256"] = hashlib.sha256(canonical_bytes(records)).hexdigest()
    return records, summary


if __name__ == "__main__":
    records, summary = run_matrix()
    print(json.dumps(summary, indent=2, sort_keys=True))
