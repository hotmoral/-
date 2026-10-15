from __future__ import annotations

from collections import Counter
import json

from e_v0_fixture_adapter import iter_invariant_fixtures
from diagnose_p1_fr3_v3_intersections import crossing_pairs
import p1_fr5_core_mass_silhouette_v2 as v2


def main():
    failed_records = []
    pair_counts = Counter()
    morphology_counts = Counter()
    case_counts = Counter()
    size_counts = Counter()
    direction_counts = Counter()
    time_counts = Counter()
    total_intersections = 0

    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        result = v2.build_probe(fixture, direction)
        pairs = crossing_pairs(result.base.core_vertices)
        if not pairs:
            continue
        total_intersections += len(pairs)
        morphology_counts[morphology.id] += 1
        case_counts[case_id] += 1
        size_counts[str(size_dp)] += 1
        direction_counts[str(direction)] += 1
        time_counts[f"{float(fixture.t):.6f}"] += 1
        normalized_pairs = []
        for pair in pairs:
            key = "{}->{} x {}->{}".format(
                pair["edgeA"][0], pair["edgeA"][1],
                pair["edgeB"][0], pair["edgeB"][1],
            )
            pair_counts[key] += 1
            normalized_pairs.append({
                "edgeA": list(pair["edgeA"]),
                "edgeB": list(pair["edgeB"]),
            })
        failed_records.append({
            "caseId": case_id,
            "morphologyId": morphology.id,
            "sizeDp": size_dp,
            "direction": direction,
            "t": float(fixture.t),
            "pairCount": len(pairs),
            "pairs": normalized_pairs,
        })

    payload = {
        "version": "P1_FR5_V2_FINAL_FOLD_DIAGNOSTIC_V1",
        "candidate": v2.PROTOTYPE_VERSION,
        "recordCount": 1770,
        "failedRecordCount": len(failed_records),
        "totalIntersectionCount": total_intersections,
        "edgePairCounts": dict(sorted(pair_counts.items())),
        "morphologyCounts": dict(sorted(morphology_counts.items())),
        "caseCounts": dict(sorted(case_counts.items())),
        "sizeCounts": dict(sorted(size_counts.items())),
        "directionCounts": dict(sorted(direction_counts.items())),
        "timeCounts": dict(sorted(time_counts.items())),
        "failedRecords": failed_records,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
