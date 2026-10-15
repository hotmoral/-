from __future__ import annotations

import unittest

from e_v0_fixture_adapter import H1, H4, H6N, H7, build_e_fixture
from e_v0_profiles import M0, MORPHOLOGIES
import p1_fr1_mesh_probe as fr1
import p1_fr3_feline_core_topology as fr3


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
        points.extend(((paw.x - mesh["pawRadiusX"], paw.y - mesh["pawRadiusY"]),
                       (paw.x + mesh["pawRadiusX"], paw.y + mesh["pawRadiusY"])))
    points.extend(probe.tail_mesh["vertices"])
    return points


class P1FR3FelineCoreTopologyTests(unittest.TestCase):
    def test_exact_24_point_shared_correspondence_and_skin_budget(self):
        self.assertEqual(len(fr3.CORE_VERTEX_IDS), 24)
        self.assertEqual(len(set(fr3.CORE_VERTEX_IDS)), 24)
        self.assertEqual(set(fr3.CANONICAL_SHAPES), {"PROFILE", "THREE_QUARTER", "FRONT"})
        self.assertEqual(set(fr3.CORE_SKIN_WEIGHTS), set(fr3.CORE_VERTEX_IDS))
        allowed_groups = {"HEAD", "FORE", "BODY", "PELVIS"}
        for vertex_id in fr3.CORE_VERTEX_IDS:
            skin = fr3.CORE_SKIN_WEIGHTS[vertex_id]
            self.assertTrue(set(skin).issubset(allowed_groups), vertex_id)
            self.assertAlmostEqual(sum(skin.values()), 1.0, places=12, msg=vertex_id)
        for name, shape in fr3.CANONICAL_SHAPES.items():
            self.assertEqual(len(shape), 24, name)
            core = tuple((vertex_id, p[0], p[1]) for vertex_id, p in zip(fr3.CORE_VERTEX_IDS, shape))
            self.assertEqual(fr1.count_self_intersections(core), 0, name)

    def test_canonical_interpolation_is_simple_at_quarter_steps(self):
        # Test the pure correspondence independently of fixture deformation.
        for yaw_fraction in (0.0, 0.125, 0.25, 0.375, 0.50, 0.625, 0.75, 0.875, 1.0):
            yaw = yaw_fraction * 1.5707963267948966
            weights = fr3.canonical_view_weights(yaw)
            shape = fr3._shape_blend(weights)
            core = tuple((vertex_id, p[0], p[1]) for vertex_id, p in zip(fr3.CORE_VERTEX_IDS, shape))
            self.assertEqual(fr1.count_self_intersections(core), 0, yaw_fraction)

    def test_representative_matrix_preserves_frozen_invariants(self):
        samples = (
            (H1, 0.0, +1),
            (H4, 0.0, +1),
            (H4, 0.5, +1),
            (H4, 1.0, +1),
            (H6N, 0.0, +1),
            (H6N, 0.25, +1),
            (H6N, 0.5, +1),
            (H6N, 0.75, +1),
            (H6N, 1.0, +1),
            (H6N, 0.25, -1),
            (H6N, 0.5, -1),
            (H6N, 0.75, -1),
            (H7, 0.0, +1),
            (H7, 0.5, +1),
            (H7, 1.0, +1),
        )
        for morphology in MORPHOLOGIES:
            for case_id, t, direction in samples:
                with self.subTest(morphology=morphology.id, case=case_id, t=t, direction=direction):
                    fixture = build_e_fixture(morphology, case_id, 80, t, direction)
                    probe = fr3.build_probe(fixture, direction)
                    self.assertEqual(probe.semantic_anchor_hash_before, probe.semantic_anchor_hash_after)
                    self.assertLessEqual(probe.paw_pin_error_max, 1e-9)
                    self.assertEqual(probe.core_self_intersections, 0)
                    self.assertFalse(probe.correction_families)
                    self.assertEqual(len(probe.core_vertices), 24)
                    self.assertEqual(len(probe.limb_meshes), 4)
                    self.assertEqual(len(probe.ear_shapes), 2)

    def test_topology_is_shared_across_all_morphologies_and_directions(self):
        signatures = set()
        for morphology in MORPHOLOGIES:
            for direction in (+1, -1):
                for t in (0.0, 0.5, 1.0):
                    fixture = build_e_fixture(morphology, H6N, 80, t, direction)
                    signatures.add(fr3.build_probe(fixture, direction).topology_signature)
        self.assertEqual(signatures, {fr3.topology_signature()})

    def test_fr2_limb_routing_is_not_regressed(self):
        total = 0
        for case_id, times in ((H6N, (0.2, 0.4, 0.5, 0.6, 0.8)), (H7, (0.25, 0.5, 0.75))):
            directions = (+1, -1) if case_id == H6N else (+1,)
            for direction in directions:
                for t in times:
                    fixture = build_e_fixture(M0, case_id, 80, t, direction)
                    total += fr3.limb_crossing_count(fr3.build_probe(fixture, direction).limb_meshes)
        self.assertLessEqual(total, 12)

    def test_required_samples_fit_normalized_evidence_cells(self):
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
            fixture = build_e_fixture(morphology, case_id, 80, t, direction)
            probe = fr3.build_probe(fixture, direction)
            root = fixture.state.anchors["BODY_ROOT"]
            points = _geometry_points(fixture, probe)
            self.assertLessEqual(max(abs(x - root.x) for x, _ in points), half_w)
            self.assertLessEqual(max(abs(y - root.y) for _, y in points), half_h)


if __name__ == "__main__":
    unittest.main()
