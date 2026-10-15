from __future__ import annotations

from collections import Counter, defaultdict

from e_v0_fixture_adapter import iter_invariant_fixtures
import p1_fr4_internal_core_scaffold as fr4


def main():
    patch_record_counts = Counter()
    patch_vertex_counts = Counter()
    examples = defaultdict(list)
    any_outside_records = 0

    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        result = fr4.build_probe(fixture, direction)
        core = tuple((x, y) for _, x, y in result.base.core_vertices)
        record_has_outside = False
        for patch in result.internal_patches:
            outside = [
                (index, vertex)
                for index, vertex in enumerate(patch.vertices)
                if not fr4.point_in_polygon(vertex, core)
            ]
            if outside:
                record_has_outside = True
                patch_record_counts[patch.id] += 1
                patch_vertex_counts[patch.id] += len(outside)
                if len(examples[patch.id]) < 6:
                    examples[patch.id].append(
                        (morphology.id, case_id, size_dp, direction, fixture.t, outside)
                    )
        if record_has_outside:
            any_outside_records += 1

    print(f"any_outside_records={any_outside_records}")
    print(f"patch_record_counts={dict(sorted(patch_record_counts.items()))}")
    print(f"patch_vertex_counts={dict(sorted(patch_vertex_counts.items()))}")
    for patch_id in sorted(examples):
        print(f"patch={patch_id}")
        for morphology_id, case_id, size_dp, direction, t, outside in examples[patch_id]:
            print(
                f"  morphology={morphology_id} case={case_id} size={size_dp} "
                f"dir={direction:+d} t={t:.6f} outside={outside}"
            )


if __name__ == "__main__":
    main()
