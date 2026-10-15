from __future__ import annotations

import unittest

from e_v0_fixture_adapter import H4, H6N, H7, build_e_fixture, iter_invariant_fixtures
from e_v0_profiles import M0, MORPHOLOGIES
import p1_fr3_feline_core_topology_v5 as fr3_v5
import p1_fr4_internal_core_scaffold as fr4


CELL_W = 190.0
CELL_H = 125.0
MARGIN = 8.0


class P1FR4InternalCoreScaffoldTests(unittest.TestCase):
    def test_exact_three_patch_shared_topology(self):
        self.assertEqual(fr4.PATCH_IDS, ("CRANIUM_MASS", "CERVICAL_BRIDGE", "THORAX_MASS"))
        expected_counts = {"CRANIUM_MASS": 8, "CERVICAL_BRIDGE": 6, "THORAX_MASS": 8}
        fixture = build_e_fixture(M0, H6N, 80, 0.5, +1)
        result = fr4.build_probe(fixture, +1)
        self.assertEqual(tuple(patch.id for patch in result.internal_patches), fr4.PATCH_IDS)
        for patch in result.internal_patches:
            self.assertEqual(len(patch.vertices), expected_counts[patch.id])
            self.assertEqual(fr4.patch_self_intersections(patch), 0, patch.id)
        self.assertEqual(result.scaffold_signature, fr4.scaffold_signature())

    def test_representative_scaffold_is_inside_core_and_preserves_frozen_invariants(self):
        samples = (
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
                    result = fr4.build_probe(fixture, direction)
                    base = result.base
                    control = fr3_v5.build_probe(fixture, direction)
                    self.assertEqual(base.core_vertices, control.core_vertices)
                    self.assertEqual(base.ear_shapes, control.ear_shapes)
                    self.assertEqual(base.limb_meshes, control.limb_meshes)
                    self.assertEqual(base.tail_mesh, control.tail_mesh)
                    self.assertEqual(base.topology_signature, control.topology_signature)
                    self.assertEqual(base.semantic_anchor_hash_before, base.semantic_anchor_hash_after)
                    self.assertLessEqual(base.paw_pin_error_max, 1e-9)
                    self.assertEqual(base.core_self_intersections, 0)
                    self.assertFalse(base.correction_families)
                    self.assertEqual(result.patch_self_intersections, 0)
                    self.assertEqual(result.patch_outside_vertex_count, 0)

    def test_full_matrix_outer_geometry_is_exactly_fr3_v5_and_scaffold_is_valid(self):
        count = 0
        signatures = set()
        for _, _, _, direction, fixture in iter_invariant_fixtures():
            result = fr4.build_probe(fixture, direction)
            control = fr3_v5.build_probe(fixture, direction)
            count += 1
            signatures.add(result.scaffold_signature)
            self.assertEqual(result.base.core_vertices, control.core_vertices)
            self.assertEqual(result.base.ear_shapes, control.ear_shapes)
            self.assertEqual(result.base.limb_meshes, control.limb_meshes)
            self.assertEqual(result.base.tail_mesh, control.tail_mesh)
            self.assertEqual(result.patch_self_intersections, 0)
            self.assertEqual(result.patch_outside_vertex_count, 0)
        self.assertEqual(count, 1770)
        self.assertEqual(signatures, {fr4.scaffold_signature()})

    def test_required_visual_samples_fit_normalized_cells(self):
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
            result = fr4.build_probe(fixture, direction)
            root = fixture.state.anchors["BODY_ROOT"]
            points = [(x, y) for _, x, y in result.base.core_vertices]
            for patch in result.internal_patches:
                points.extend(patch.vertices)
            self.assertLessEqual(max(abs(x - root.x) for x, _ in points), half_w)
            self.assertLessEqual(max(abs(y - root.y) for _, y in points), half_h)


if __name__ == "__main__":
    unittest.main()
