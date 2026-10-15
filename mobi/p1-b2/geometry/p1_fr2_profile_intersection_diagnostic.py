from __future__ import annotations

import json
from typing import Sequence, Tuple

from e_v0_fixture_adapter import H1, H4, H6N, H7, build_e_fixture
from e_v0_profiles import MORPHOLOGIES
from model import Vec2
import p1_fr1_mesh_probe as fr1
from p1_fr1_mesh_probe_v3 import build_probe as build_fr1_probe
from p1_fr2_layered_view_prototype_v2 import build_probe as build_fr2_v2_probe


DIAGNOSTIC_VERSION = "P1_FR2_PROFILE_INTERSECTION_DIAGNOSTIC_V1"


def intersecting_edge_pairs(core_vertices: Sequence[Tuple[str, float, float]]):
    points = [Vec2(x, y) for _, x, y in core_vertices]
    ids = [name for name, _, _ in core_vertices]
    n = len(points)
    pairs = []
    for i in range(n):
        a, b = points[i], points[(i + 1) % n]
        for j in range(i + 1, n):
            if j in (i, (i + 1) % n):
                continue
            if (j + 1) % n in (i, (i + 1) % n):
                continue
            if i == 0 and j == n - 1:
                continue
            c, d = points[j], points[(j + 1) % n]
            if fr1._segments_intersect(a, b, c, d):
                pairs.append({
                    "edgeA": [ids[i], ids[(i + 1) % n]],
                    "edgeB": [ids[j], ids[(j + 1) % n]],
                    "edgeAIndex": i,
                    "edgeBIndex": j,
                    "points": {
                        ids[i]: [a.x, a.y],
                        ids[(i + 1) % n]: [b.x, b.y],
                        ids[j]: [c.x, c.y],
                        ids[(j + 1) % n]: [d.x, d.y],
                    },
                })
    return pairs


def main():
    cases = (
        (H1, 0.0, +1),
        (H4, 0.50, +1),
        (H6N, 0.0, +1),
        (H7, 0.50, +1),
    )
    rows = []
    for morphology in MORPHOLOGIES:
        for case_id, t, direction in cases:
            fixture = build_e_fixture(morphology, case_id, 80, t, direction)
            fr1_probe = build_fr1_probe(fixture, direction)
            fr2_probe = build_fr2_v2_probe(fixture, direction)
            rows.append({
                "morphologyId": morphology.id,
                "caseId": case_id,
                "t": t,
                "direction": direction,
                "fr1Pairs": intersecting_edge_pairs(fr1_probe.core_vertices),
                "fr2V2Pairs": intersecting_edge_pairs(fr2_probe.core_vertices),
                "fr1Count": fr1_probe.core_self_intersections,
                "fr2V2Count": fr2_probe.core_self_intersections,
            })
    payload = {
        "version": DIAGNOSTIC_VERSION,
        "rows": rows,
        "fr2FailingRows": [row for row in rows if row["fr2V2Count"] > 0],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
