from __future__ import annotations

import unittest

from e_v0_fixture_adapter import H6N, build_e_fixture
from e_v0_profiles import M0
import p1_fr3_feline_core_topology_v5 as fr3_v5
import p1_fr5_core_mass_silhouette_v1 as fr5
import p1_fr7_derived_upper_body_controls_v1 as fr7
import run_p1_fr7_derived_upper_body_controls_v1 as runner


class FR7DerivedUpperBodyControlsV1Test(unittest.TestCase):
    def test_control_count_and_identity_are_bounded(self):
        self.assertEqual(
            fr7.CONTROL_IDS,
            ("CRANIUM_CONTROL", "CERVICAL_CONTROL", "THORAX_CONTROL"),
        )
        self.assertEqual(len(fr7.CONTROL_IDS), 3)
        self.assertEqual(fr7.CORE_VERTEX_IDS, fr3_v5.CORE_VERTEX_IDS)
        self.assertEqual(fr7.CORE_BOUNDARY_EDGES, fr3_v5.CORE_BOUNDARY_EDGES)

    def test_influence_topology_is_exactly_frozen_from_fr5(self):
        self.assertIs(fr7.INFLUENCE_WEIGHTS, fr5.INFLUENCE_WEIGHTS)
        self.assertEqual(fr7.INFLUENCE_WEIGHTS, fr5.INFLUENCE_WEIGHTS)

    def test_profile_parameters_are_exact_identity(self):
        for layer_id in fr7.LAYER_IDS:
            self.assertEqual(fr7.VIEW_FRAME_PARAMS[layer_id]["PROFILE"], (1.0, 1.0, 0.0))

    def test_v1_uses_axial_freedom_not_only_fr5_perpendicular_scaling(self):
        non_identity_axial_scale = False
        non_zero_axial_shift = False
        for layer_id in fr7.LAYER_IDS:
            for view in ("THREE_QUARTER", "FRONT"):
                axial_scale, _lateral_scale, axial_shift = fr7.VIEW_FRAME_PARAMS[layer_id][view]
                non_identity_axial_scale |= abs(axial_scale - 1.0) > 1e-12
                non_zero_axial_shift |= abs(axial_shift) > 1e-12
        self.assertTrue(non_identity_axial_scale)
        self.assertTrue(non_zero_axial_shift)

    def test_exact_profile_is_byte_equal_to_fr3_v5(self):
        fixture = build_e_fixture(M0, H6N, 80, 0.0, +1)
        result = fr7.build_probe(fixture, +1)
        self.assertEqual(result.base.core_vertices, result.control.core_vertices)

    def test_front_differs_from_fr5_and_retains_same_appendages(self):
        fixture = build_e_fixture(M0, H6N, 80, 1.0, +1)
        current = fr7.build_probe(fixture, +1)
        prior = fr5.build_probe(fixture, +1)
        self.assertNotEqual(current.base.core_vertices, prior.base.core_vertices)
        self.assertEqual(current.base.ear_shapes, current.control.ear_shapes)
        self.assertEqual(current.base.limb_meshes, current.control.limb_meshes)
        self.assertEqual(current.base.tail_mesh, current.control.tail_mesh)

    def test_integration_signature_is_stable(self):
        self.assertEqual(fr7.integration_signature(), fr7.integration_signature())
        self.assertEqual(len(fr7.integration_signature()), 64)

    def test_full_matrix_structural_lane(self):
        records, summary = runner.run_matrix()
        self.assertEqual(len(records), 1770)
        self.assertTrue(summary["structuralPass"], summary)
        self.assertEqual(summary["semanticMutationCount"], 0)
        self.assertEqual(summary["finalCoreSelfIntersectionCount"], 0)
        self.assertEqual(summary["patchSelfIntersectionCount"], 0)
        self.assertEqual(summary["patchOutsideVertexCount"], 0)
        self.assertEqual(summary["correctionUseCount"], 0)
        self.assertEqual(summary["meshDomainCounts"], [6])
        self.assertEqual(summary["appendageMismatchVsFr3V5Count"], 0)
        self.assertEqual(summary["profileCoreMismatchVsFr3V5Count"], 0)
        self.assertEqual(summary["earAttachmentRegressionRecordCount"], 0)
        self.assertEqual(summary["earAttachmentRegressionRecordCountVsFr5V1"], 0)
        self.assertGreater(summary["minimumPriorFoldCorridorMarginDp"], 0.0)
        self.assertLessEqual(summary["maxNormalizedCoreDisplacement"], 0.18 + 1e-12)
        self.assertEqual(summary["stressLimbCrossingDeltaVsFr3V5"], 0)


if __name__ == "__main__":
    unittest.main()
