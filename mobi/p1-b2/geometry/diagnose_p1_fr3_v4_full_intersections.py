from __future__ import annotations

from collections import Counter

from e_v0_fixture_adapter import iter_invariant_fixtures
import p1_fr3_feline_core_topology_v4 as v4
from diagnose_p1_fr3_v3_intersections import crossing_pairs


def main():
    failures = []
    pair_counts = Counter()
    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        probe = v4.build_probe(fixture, direction)
        if probe.core_self_intersections == 0:
            continue
        pairs = crossing_pairs(probe.core_vertices)
        pair_names = []
        for pair in pairs:
            key = (pair["edgeA"], pair["edgeB"])
            pair_counts[key] += 1
            pair_names.append(key)
        failures.append((
            case_id,
            morphology.id,
            int(size_dp),
            int(direction),
            float(fixture.t),
            int(probe.core_self_intersections),
            tuple(pair_names),
        ))

    print(f"failure_record_count={len(failures)}")
    print(f"intersection_total={sum(item[5] for item in failures)}")
    print("pair_counts:")
    for key, count in sorted(pair_counts.items(), key=lambda item: (-item[1], item[0])):
        print(count, key)
    print("failures:")
    for failure in failures:
        print(failure)


if __name__ == "__main__":
    main()
