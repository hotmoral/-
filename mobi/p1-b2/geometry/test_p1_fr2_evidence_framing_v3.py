from __future__ import annotations

import unittest

from e_v0_fixture_adapter import H4, H6N, H7, build_e_fixture
from e_v0_profiles import M0, MORPHOLOGIES
from p1_fr2_layered_view_prototype_v3 import build_probe


CELL_W = 190.0
CELL_H = 125.0
MARGIN = 8.0


def _geometry_points(fixture, probe):
    points = [(x, y) for _, x, y in probe.core_vertices]
    for ear in probe.ear_shapes:
        points.extend(ear)
    for mesh in probe.limb_meshes:
        points.extend(mesh["vertices"])
        paw = fixture.state.anchors[mesh["pawId"]]
        points.extend((
            (paw.x - mesh["pawRadiusX"], paw.y - mesh["pawRadiusY"]),
            (paw.x + mesh["pawRadiusX"], paw.y + mesh["pawRadiusY"]),
        ))
    points.extend(probe.tail_mesh["vertices"])
    return points


class P1FR2EvidenceFramingV3Tests(unittest.TestCase):
    def test_required_samples_fit_normalized_cells_about_body_root(self):
        samples = []
        for morphology in MORPHOLOGIES:
            for t in (0.0, 0.5, 1.0):
                samples.append((morphology, H6N, t, +1))
        for t in (0.0, 0.25, 0.5, 0.75, 1.0):
            samples.append((M0, H4, t, +1))
            samples.append((M0, H7, t, +1))
        for direction in (+1, -1):
            for t in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
                samples.append((M0, H6N, t, direction))

        half_w = CELL_W / 2.0 - MARGIN
        half_h = CELL_H / 2.0 - MARGIN
        for morphology, case_id, t, direction in samples:
            with self.subTest(morphology=morphology.id, case=case_id, t=t, direction=direction):
                fixture = build_e_fixture(morphology, case_id, 80, t, direction)
                probe = build_probe(fixture, direction)
                root = fixture.state.anchors["BODY_ROOT"]
                points = _geometry_points(fixture, probe)
                self.assertLessEqual(max(abs(x - root.x) for x, _ in points), half_w)
                self.assertLessEqual(max(abs(y - root.y) for _, y in points), half_h)


if __name__ == "__main__":
    unittest.main()
