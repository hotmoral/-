from __future__ import annotations

from e_v0_fixture_adapter import H1, H4, build_e_fixture
from e_v0_profiles import morphology_by_id
import p1_fr3_feline_core_topology_v3 as v3


def _orientation(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _proper_cross(a, b, c, d, eps=1e-9):
    o1 = _orientation(a, b, c)
    o2 = _orientation(a, b, d)
    o3 = _orientation(c, d, a)
    o4 = _orientation(c, d, b)
    return o1 * o2 < -eps and o3 * o4 < -eps


def crossing_pairs(core):
    points = [(vertex_id, x, y) for vertex_id, x, y in core]
    n = len(points)
    pairs = []
    for i in range(n):
        a = (points[i][1], points[i][2])
        b = (points[(i + 1) % n][1], points[(i + 1) % n][2])
        for j in range(i + 1, n):
            if j == i or (j + 1) % n == i or (i + 1) % n == j:
                continue
            if i == 0 and j == n - 1:
                continue
            c = (points[j][1], points[j][2])
            d = (points[(j + 1) % n][1], points[(j + 1) % n][2])
            if _proper_cross(a, b, c, d):
                pairs.append({
                    "edgeA": (points[i][0], points[(i + 1) % n][0]),
                    "edgeB": (points[j][0], points[(j + 1) % n][0]),
                    "a": a,
                    "b": b,
                    "c": c,
                    "d": d,
                })
    return pairs


def main():
    m2 = morphology_by_id("M2_ADULT_STRESS_V01")
    samples = ((H1, 0.0), (H4, 1.0))
    for case_id, t in samples:
        fixture = build_e_fixture(m2, case_id, 80, t, +1)
        probe = v3.build_probe(fixture, +1)
        print(f"sample={case_id} t={t:.2f} count={probe.core_self_intersections}")
        for pair in crossing_pairs(probe.core_vertices):
            print(pair)


if __name__ == "__main__":
    main()
