from __future__ import annotations

from collections import Counter, defaultdict

from e_v0_fixture_adapter import iter_invariant_fixtures
import p1_fr4_internal_core_scaffold_v2 as fr4


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
    out = []
    for i in range(n):
        a, b = points[i], points[(i + 1) % n]
        for j in range(i + 1, n):
            if j == i or (j + 1) % n == i or (i + 1) % n == j:
                continue
            if i == 0 and j == n - 1:
                continue
            c, d = points[j], points[(j + 1) % n]
            if _proper_cross(a, b, c, d):
                out.append((i, (i + 1) % n, j, (j + 1) % n, a, b, c, d))
    return out


def main():
    crossing_signatures = Counter()
    patch_cross_records = Counter()
    patch_outside_records = Counter()
    patch_outside_vertices = Counter()
    crossing_examples = defaultdict(list)
    outside_examples = defaultdict(list)
    failed_records = 0
    outside_records = 0

    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        result = fr4.build_probe(fixture, direction)
        core = tuple((x, y) for _, x, y in result.base.core_vertices)
        record_cross = False
        record_outside = False
        for patch in result.internal_patches:
            pairs = crossing_pairs(patch)
            if pairs:
                record_cross = True
                patch_cross_records[patch.id] += 1
            for i0, i1, j0, j1, a, b, c, d in pairs:
                key = (patch.id, i0, i1, j0, j1)
                crossing_signatures[key] += 1
                if len(crossing_examples[key]) < 4:
                    crossing_examples[key].append(
                        (morphology.id, case_id, size_dp, direction, fixture.t, a, b, c, d)
                    )
            outside = [
                (idx, vertex)
                for idx, vertex in enumerate(patch.vertices)
                if not fr4.point_in_polygon(vertex, core)
            ]
            if outside:
                record_outside = True
                patch_outside_records[patch.id] += 1
                patch_outside_vertices[patch.id] += len(outside)
                if len(outside_examples[patch.id]) < 6:
                    outside_examples[patch.id].append(
                        (morphology.id, case_id, size_dp, direction, fixture.t, outside)
                    )
        failed_records += int(record_cross)
        outside_records += int(record_outside)

    print(f"failed_records={failed_records}")
    print(f"patch_cross_records={dict(sorted(patch_cross_records.items()))}")
    print(f"outside_records={outside_records}")
    print(f"patch_outside_records={dict(sorted(patch_outside_records.items()))}")
    print(f"patch_outside_vertices={dict(sorted(patch_outside_vertices.items()))}")
    print("crossing_signatures:")
    for key, count in crossing_signatures.most_common():
        print(f"  {key} count={count}")
        for example in crossing_examples[key]:
            print(f"    example={example}")
    print("outside_examples:")
    for patch_id in sorted(outside_examples):
        print(f"  patch={patch_id}")
        for example in outside_examples[patch_id]:
            print(f"    example={example}")


if __name__ == "__main__":
    main()
