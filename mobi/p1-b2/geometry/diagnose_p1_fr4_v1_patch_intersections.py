from __future__ import annotations

from collections import Counter, defaultdict

from e_v0_fixture_adapter import H4, H6N, H7, build_e_fixture, iter_invariant_fixtures
from e_v0_profiles import M0, M1, morphology_by_id
import p1_fr4_internal_core_scaffold as fr4


def _orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _proper_cross(a, b, c, d, eps=1e-9):
    o1 = _orientation(a, b, c)
    o2 = _orientation(a, b, d)
    o3 = _orientation(c, d, a)
    o4 = _orientation(c, d, b)
    return o1 * o2 < -eps and o3 * o4 < -eps


def crossing_pairs(patch):
    points = tuple(patch.vertices)
    n = len(points)
    pairs = []
    for i in range(n):
        a = points[i]
        b = points[(i + 1) % n]
        for j in range(i + 1, n):
            if j == i or (j + 1) % n == i or (i + 1) % n == j:
                continue
            if i == 0 and j == n - 1:
                continue
            c = points[j]
            d = points[(j + 1) % n]
            if _proper_cross(a, b, c, d):
                pairs.append((i, (i + 1) % n, j, (j + 1) % n, a, b, c, d))
    return pairs


def _representative_details():
    samples = (
        (M0, H4, 0.0, +1),
        (M0, H6N, 1.0, +1),
        (M1, H6N, 1.0, +1),
        (M0, H7, 0.5, +1),
    )
    print("=== REPRESENTATIVE_DETAILS ===")
    for morphology, case_id, t, direction in samples:
        fixture = build_e_fixture(morphology, case_id, 80, t, direction)
        result = fr4.build_probe(fixture, direction)
        print(
            f"sample morphology={morphology.id} case={case_id} size=80 "
            f"t={t:.2f} dir={direction:+d} aggregate={result.patch_self_intersections}"
        )
        for patch in result.internal_patches:
            pairs = crossing_pairs(patch)
            print(f"  patch={patch.id} crossings={len(pairs)} vertices={len(patch.vertices)}")
            for i0, i1, j0, j1, a, b, c, d in pairs:
                print(
                    f"    edge=({i0},{i1}) x ({j0},{j1}) "
                    f"a={a} b={b} c={c} d={d}"
                )


def _full_matrix_summary():
    signature_counts = Counter()
    patch_failure_records = Counter()
    case_counts = Counter()
    morphology_counts = Counter()
    size_counts = Counter()
    direction_counts = Counter()
    t_counts = Counter()
    total_failed_records = 0
    total_crossings = 0
    outside_records = 0
    outside_vertices = 0
    examples = defaultdict(list)

    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        result = fr4.build_probe(fixture, direction)
        record_crossings = 0
        for patch in result.internal_patches:
            pairs = crossing_pairs(patch)
            if pairs:
                patch_failure_records[patch.id] += 1
            for i0, i1, j0, j1, a, b, c, d in pairs:
                signature = (patch.id, i0, i1, j0, j1)
                signature_counts[signature] += 1
                record_crossings += 1
                if len(examples[signature]) < 3:
                    examples[signature].append(
                        (morphology.id, case_id, size_dp, direction, fixture.t, a, b, c, d)
                    )
        if record_crossings:
            total_failed_records += 1
            total_crossings += record_crossings
            case_counts[case_id] += 1
            morphology_counts[morphology.id] += 1
            size_counts[size_dp] += 1
            direction_counts[direction] += 1
            t_counts[round(float(fixture.t), 6)] += 1
        if result.patch_outside_vertex_count:
            outside_records += 1
            outside_vertices += result.patch_outside_vertex_count

    print("=== FULL_MATRIX_SUMMARY ===")
    print(f"failed_records={total_failed_records}")
    print(f"total_crossings={total_crossings}")
    print(f"patch_failure_records={dict(sorted(patch_failure_records.items()))}")
    print(f"case_counts={dict(sorted(case_counts.items()))}")
    print(f"morphology_counts={dict(sorted(morphology_counts.items()))}")
    print(f"size_counts={dict(sorted(size_counts.items()))}")
    print(f"direction_counts={dict(sorted(direction_counts.items()))}")
    print(f"t_counts={dict(sorted(t_counts.items()))}")
    print(f"outside_records={outside_records}")
    print(f"outside_vertices={outside_vertices}")
    print("crossing_signatures:")
    for signature, count in signature_counts.most_common():
        print(f"  {signature} count={count}")
        for example in examples[signature]:
            morphology_id, case_id, size_dp, direction, t, a, b, c, d = example
            print(
                f"    example morphology={morphology_id} case={case_id} size={size_dp} "
                f"dir={direction:+d} t={t:.6f} a={a} b={b} c={c} d={d}"
            )


if __name__ == "__main__":
    _representative_details()
    _full_matrix_summary()
