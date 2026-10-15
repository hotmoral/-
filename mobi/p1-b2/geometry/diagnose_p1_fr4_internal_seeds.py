from __future__ import annotations

from collections import Counter

from e_v0_fixture_adapter import iter_invariant_fixtures
import p1_fr3_feline_core_topology_v5 as fr3_v5
import p1_fr4_internal_core_scaffold as geom


def _mid(a, b):
    return ((a.x + b.x) * 0.5, (a.y + b.y) * 0.5)


def main():
    outside = Counter()
    examples = {}
    count = 0
    for case_id, morphology, size_dp, direction, fixture in iter_invariant_fixtures():
        probe = fr3_v5.build_probe(fixture, direction)
        core = tuple((x, y) for _, x, y in probe.core_vertices)
        head = fixture.state.anchors["HEAD_ROOT"]
        fore = fixture.state.anchors["FOREQUARTER_REF"]
        body = fixture.state.anchors["BODY_ROOT"]
        candidates = {
            "HEAD_ROOT": (head.x, head.y),
            "FOREQUARTER_REF": (fore.x, fore.y),
            "HEAD_FORE_MID": _mid(head, fore),
            "BODY_ROOT": (body.x, body.y),
        }
        count += 1
        for name, point in candidates.items():
            if not geom.point_in_polygon(point, core):
                outside[name] += 1
                examples.setdefault(
                    name,
                    (morphology.id, case_id, size_dp, direction, fixture.t, point),
                )
    print(f"record_count={count}")
    print(f"outside_counts={dict(sorted(outside.items()))}")
    print(f"examples={examples}")


if __name__ == "__main__":
    main()
