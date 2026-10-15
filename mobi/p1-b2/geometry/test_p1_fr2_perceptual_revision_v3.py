from __future__ import annotations

import unittest

from e_v0_fixture_adapter import H1, H4, H6N, H7, build_e_fixture
from e_v0_profiles import M0, MORPHOLOGIES
import p1_fr1_mesh_probe as fr1
from p1_fr2_layered_view_prototype_v3 import (
    CANONICAL_SHAPES,
    CORE_VERTEX_IDS,
    build_probe,
    limb_crossing_count,
    topology_signature,
)


class P1FR2PerceptualRevisionV3Tests(unittest.TestCase):
    def test_canonical_shapes_share_fr1_correspondence_and_are_simple(self):
        self.assertEqual(len(CORE_VERTEX_IDS), 16)
        for name, shape in CANONICAL_SHAPES.items():
            self.assertEqual(len(shape), len(CORE_VERTEX_IDS), name)
            core = tuple((vertex_id, point[0], point[1]) for vertex_id, point in zip(CORE_VERTEX_IDS, shape))
            self.assertEqual(fr1.count_self_intersections(core), 0, name)

    def test_representative_views_preserve_semantics_and_paw_pinning(self):
        samples = (
            (H1, 0.0, +1),
            (H4, 0.50, +1),
            (H6N, 0.00, +1),
            (H6N, 0.50, +1),
            (H6N, 1.00, +1),
            (H6N, 0.50, -1),
            (H7, 0.50, +1),
        )
        for morphology in MORPHOLOGIES:
            for case_id, t, direction in samples:
                with self.subTest(morphology=morphology.id, case=case_id, t=t, direction=direction):
                    fixture = build_e_fixture(morphology, case_id, 80, t, direction)
                    probe = build_probe(fixture, direction)
                    self.assertEqual(probe.semantic_anchor_hash_before, probe.semantic_anchor_hash_after)
                    self.assertLessEqual(probe.paw_pin_error_max, 1e-9)
                    self.assertEqual(probe.core_self_intersections, 0)
                    self.assertEqual(len(probe.limb_meshes), 4)
                    self.assertEqual(len(probe.ear_shapes), 2)
                    self.assertFalse(probe.correction_families)

    def test_topology_signature_is_shared_across_morphology_and_direction(self):
        signatures = set()
        for morphology in MORPHOLOGIES:
            for direction in (+1, -1):
                fixture = build_e_fixture(morphology, H6N, 80, 0.50, direction)
                signatures.add(build_probe(fixture, direction).topology_signature)
        self.assertEqual(signatures, {topology_signature()})

    def test_stress_crossing_diagnostic_does_not_regress_obviously(self):
        total = 0
        for case_id, times in (
            (H6N, (0.20, 0.40, 0.50, 0.60, 0.80)),
            (H7, (0.25, 0.50, 0.75)),
        ):
            directions = (+1, -1) if case_id == H6N else (+1,)
            for direction in directions:
                for t in times:
                    fixture = build_e_fixture(M0, case_id, 80, t, direction)
                    total += limb_crossing_count(build_probe(fixture, direction).limb_meshes)
        self.assertLessEqual(total, 12)


if __name__ == "__main__":
    unittest.main()
