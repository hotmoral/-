from __future__ import annotations

import unittest

from e_v0_fixture_adapter import H4, H6N, H7, build_e_fixture, iter_invariant_fixtures
from e_v0_profiles import M0, MORPHOLOGIES
import p1_fr3_feline_core_topology_v5 as fr3_v5
import p1_fr5_core_mass_silhouette_v1 as fr5


CELL_W = 190.0
CELL_H = 125.0
MARGIN = 8.0


def _is_exact_profile(probe) -> bool:
    weights = dict(probe.view_weights)
    return (
        abs(float(weights.get("PROFILE", 0.0)) - 1.0) <= 1e-12
        and abs(float(weights.get("THREE_QUARTER", 0.0))) <= 1e-12
        and abs(float(weights.get("FRONT", 0.0))) <= 1e-12
    )


class P1FR5CoreMassSilhouetteV1Tests(unittest.TestCase):
    def test_contract_coefficients_and_influence_topology_are_exact(self):
        self.assertEqual(
            fr5.VIEW_SCALES,
            {
                "CRANIUM_MASS": {"PROFILE": 1.00, "THREE_QUARTER": 1.08, "FRONT": 1.14},
                "CERVICAL_BRIDGE": {"PROFILE": 1.00, "THREE_QUARTER": 0.94, "FRONT": 0.88},
                "THORAX_MASS": {"PROFILE": 1.00, "THREE_QUARTER": 1.04, "FRONT": 1.08},
            },
        )
        self.assertEqual(fr5.LAYER_IDS, ("CRANIUM_MASS", "CERVICAL_BRIDGE", "THORAX_MASS"))
        for vertex_id, influences in fr5.INFLUENCE_WEIGHTS.items():
            self.assertIn(vertex_id, fr3_v5.CORE_VERTEX_IDS)
            self.assertLessEqual(sum(weight for _, weight in influences), 1.0 + 1e-12)
            for layer_id, weight in influences:
                self.assertIn(layer_id, fr5.LAYER_IDS)
                self.assertGreaterEqual(weight, 0.0)
        for vertex_id in ("C10_BACK_REAR", "C11_HAUNCH_DORSAL", "C12_RUMP", "C13_HAUNCH_VENTRAL", "C14_BELLY_REAR", "C15_BELLY_MID"):
            self.assertNotIn(vertex_id, fr5.INFLUENCE_WEIGHTS)

    def test_profile_is_exact_fr3_v5_and_topology_identity_is_preserved(self):
        for morphology in MORPHOLOGIES:
            fixture = build_e_fixture(morphology, H6N, 80, 0.0, +1)
            result = fr5.build_probe(fixture, +1)
            self.assertEqual(result.base.core_vertices, result.control.core_vertices)
            self.assertEqual(result.base.topology_signature, fr3_v5.topology_signature())
            self.assertEqual(tuple(v[0] for v in result.base.core_vertices), fr3_v5.CORE_VERTEX_IDS)
            self.assertEqual(result.integration_signature, fr5.integration_signature())

    def test_representative_samples_preserve_semantics_appendages_and_bounds(self):
        samples = (
            (H4, 0.0, +1), (H4, 0.5, +1), (H4, 1.0, +1),
            (H6N, 0.0, +1), (H6N, 0.25, +1), (H6N, 0.5, +1),
            (H6N, 0.75, +1), (H6N, 1.0, +1),
            (H6N, 0.25, -1), (H6N, 0.5, -1), (H6N, 0.75, -1), (H6N, 1.0, -1),
            (H7, 0.0, +1), (H7, 0.5, +1), (H7, 1.0, +1),
        )
        for morphology in MORPHOLOGIES:
            for case_id, t, direction in samples:
                with self.subTest(morphology=morphology.id, case=case_id, t=t, direction=direction):
                    fixture = build_e_fixture(morphology, case_id, 80, t, direction)
                    result = fr5.build_probe(fixture, direction)
                    probe = result.base
                    control = result.control
                    self.assertEqual(probe.ear_shapes, control.ear_shapes)
                    self.assertEqual(probe.limb_meshes, control.limb_meshes)
                    self.assertEqual(probe.tail_mesh, control.tail_mesh)
                    self.assertEqual(probe.topology_signature, control.topology_signature)
                    self.assertEqual(probe.semantic_anchor_hash_before, probe.semantic_anchor_hash_after)
                    self.assertLessEqual(probe.paw_pin_error_max, 1e-9)
                    self.assertEqual(probe.core_self_intersections, 0)
                    self.assertFalse(probe.correction_families)
                    self.assertEqual(result.patch_self_intersections, 0)
                    self.assertEqual(result.patch_outside_vertex_count, 0)
                    self.assertLessEqual(
                        result.normalized_max_core_displacement,
                        fr5.MAX_NORMALIZED_CORE_DISPLACEMENT + 1e-12,
                    )
                    self.assertLessEqual(
                        result.ear_base_outside_final,
                        result.ear_base_outside_control,
                    )

    def test_full_matrix_preserves_frozen_authority_and_attachment(self):
        count = 0
        signatures = set()
        changed = 0
        exact_profile_count = 0
        for _, _, _, direction, fixture in iter_invariant_fixtures():
            result = fr5.build_probe(fixture, direction)
            probe = result.base
            control = result.control
            count += 1
            signatures.add(result.integration_signature)
            if probe.core_vertices != control.core_vertices:
                changed += 1
            if _is_exact_profile(probe):
                exact_profile_count += 1
                self.assertEqual(probe.core_vertices, control.core_vertices)
            self.assertEqual(tuple(v[0] for v in probe.core_vertices), fr3_v5.CORE_VERTEX_IDS)
            self.assertEqual(probe.topology_signature, fr3_v5.topology_signature())
            self.assertEqual(probe.semantic_anchor_hash_before, probe.semantic_anchor_hash_after)
            self.assertLessEqual(probe.paw_pin_error_max, 1e-9)
            self.assertEqual(probe.core_self_intersections, 0)
            self.assertEqual(probe.ear_shapes, control.ear_shapes)
            self.assertEqual(probe.limb_meshes, control.limb_meshes)
            self.assertEqual(probe.tail_mesh, control.tail_mesh)
            self.assertEqual(result.patch_self_intersections, 0)
            self.assertEqual(result.patch_outside_vertex_count, 0)
            self.assertLessEqual(
                result.normalized_max_core_displacement,
                fr5.MAX_NORMALIZED_CORE_DISPLACEMENT + 1e-12,
            )
            self.assertLessEqual(result.ear_base_outside_final, result.ear_base_outside_control)
        self.assertEqual(count, 1770)
        self.assertEqual(signatures, {fr5.integration_signature()})
        self.assertGreater(changed, 0)
        self.assertGreater(exact_profile_count, 0)

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
            result = fr5.build_probe(fixture, direction)
            root = fixture.state.anchors["BODY_ROOT"]
            points = [(x, y) for _, x, y in result.base.core_vertices]
            for ear in result.base.ear_shapes:
                points.extend(ear)
            for mesh in result.base.limb_meshes:
                points.extend(mesh["vertices"])
            points.extend(result.base.tail_mesh["vertices"])
            self.assertLessEqual(max(abs(x - root.x) for x, _ in points), half_w)
            self.assertLessEqual(max(abs(y - root.y) for _, y in points), half_h)


if __name__ == "__main__":
    unittest.main()
