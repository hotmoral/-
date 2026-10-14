from __future__ import annotations

import json

from footprint_v1 import SCHEMES, analyze_state
from model import M0, M1, M2
from motions_v2 import sample_motion
from orientation_v2 import M0_V2, M1_V2, M2_V2
from turn_2p5d import solve_turn_2p5d

CANDIDATES = ("BM_A", "BM_B", "BM_C")
MORPHOLOGIES = (M0, M1, M2)
SIZES = (48, 64, 80, 96, 112)
MOTION_SAMPLES = {
    "H2_SLOW_WALK": 41,
    "H3_START_WALK_STOP": 61,
    "H4_SIT_TO_STAND": 31,
    "H6_CHANGE_FACING_2P5D": 41,
    "H7_NARROW_SHORT_STEP": 41,
}
ORIENTATION_MORPH = {
    M0.id: M0_V2,
    M1.id: M1_V2,
    M2.id: M2_V2,
}


def sample_state(candidate, morphology, case_id, size_dp, t):
    if case_id == "H6_CHANGE_FACING_2P5D":
        state = solve_turn_2p5d(candidate, ORIENTATION_MORPH[morphology.id], size_dp, t)
        if not any(note.startswith("bodyYawRad=") for note in state.notes):
            raise RuntimeError("H6 must use orientation v0.2 2.5D state")
        return state
    return sample_motion(candidate, morphology, case_id, size_dp, t)


def _mean(values):
    return sum(values) / len(values) if values else 0.0


def _aggregate_scheme(samples, scheme):
    items = [sample["schemes"][scheme] for sample in samples]
    areas = [item["blockingAreaDp2"] for item in items]
    reductions = [item["areaReductionVsF0"] for item in items]
    occupancies = [item["effectiveOccupancy"] for item in items]
    counts = [item["windowCount"] for item in items]
    result = {
        "meanBlockingAreaDp2": _mean(areas),
        "maxBlockingAreaDp2": max(areas),
        "meanAreaReductionVsF0": _mean(reductions),
        "minAreaReductionVsF0": min(reductions),
        "maxAreaReductionVsF0": max(reductions),
        "meanEffectiveOccupancy": _mean(occupancies),
        "minEffectiveOccupancy": min(occupancies),
        "meanWindowCount": _mean(counts),
        "maxWindowCount": max(counts),
    }
    if scheme == "F3_ADAPTIVE_LOWER_BOUND":
        selected = {}
        for item in items:
            key = item["selectedScheme"]
            selected[key] = selected.get(key, 0) + 1
        result["selectedSchemeCounts"] = dict(sorted(selected.items()))
    return result


def run_matrix(occupancy_grid=32):
    records = []
    for candidate in CANDIDATES:
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for case_id, sample_count in MOTION_SAMPLES.items():
                    analyzed = []
                    errors = []
                    for index in range(sample_count):
                        t = index / (sample_count - 1)
                        state = sample_state(candidate, morphology, case_id, size_dp, t)
                        item = analyze_state(state, occupancy_grid=occupancy_grid)
                        analyzed.append(item)
                        errors.extend(item["errors"])

                    records.append({
                        "schemaVersion": "P1_B2_2_FOOTPRINT_RESULT_V01",
                        "candidate": candidate,
                        "morphology": morphology.id,
                        "sizeDp": size_dp,
                        "caseId": case_id,
                        "sampleCount": sample_count,
                        "occupancyGrid": occupancy_grid,
                        "assertions": {
                            "pass": not errors,
                            "errors": sorted(set(errors)),
                        },
                        "schemes": {
                            scheme: _aggregate_scheme(analyzed, scheme)
                            for scheme in SCHEMES
                        },
                    })
    return records


def summarize(records):
    summary = {
        "schemaVersion": "P1_B2_2_FOOTPRINT_SUMMARY_V01",
        "records": len(records),
        "failures": sum(1 for record in records if not record["assertions"]["pass"]),
        "schemes": {},
    }
    for scheme in SCHEMES:
        reductions = [record["schemes"][scheme]["meanAreaReductionVsF0"] for record in records]
        occupancy = [record["schemes"][scheme]["meanEffectiveOccupancy"] for record in records]
        max_counts = [record["schemes"][scheme]["maxWindowCount"] for record in records]
        summary["schemes"][scheme] = {
            "meanOfRecordMeanAreaReductionVsF0": _mean(reductions),
            "minOfRecordMeanAreaReductionVsF0": min(reductions),
            "maxOfRecordMeanAreaReductionVsF0": max(reductions),
            "meanOfRecordMeanEffectiveOccupancy": _mean(occupancy),
            "minOfRecordMeanEffectiveOccupancy": min(occupancy),
            "maxWindowCount": max(max_counts),
        }
    return summary


if __name__ == "__main__":
    records = run_matrix()
    print(json.dumps(summarize(records), indent=2, sort_keys=True))
