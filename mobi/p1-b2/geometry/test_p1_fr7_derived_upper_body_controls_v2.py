from __future__ import annotations

import unittest

from e_v0_fixture_adapter import H6N, build_e_fixture
from e_v0_profiles import M0
import p1_fr7_derived_upper_body_controls_v1 as v1
import p1_fr7_derived_upper_body_controls_v2 as v2
import run_p1_fr7_derived_upper_body_controls_v2 as runner


class FR7DerivedUpperBodyControlsV2Test(unittest.TestCase):
    def test_v2_changes_coefficients_only(self):
        self.assertEqual(v2.CONTROL_IDS, v1.CONTROL_IDS)
        self.assertIs(v2.INFLUENCE_WEIGHTS, v1.INFLUENCE_WEIGHTS)
        self.assertEqual(v2.CORE_VERTEX_IDS, v1.CORE_VERTEX_IDS)
        self.assertEqual(v2.CORE_BOUNDARY_EDGES, v1.CORE_BOUNDARY_EDGES)
        self.assertEqual(v2.MAX_NORMALIZED_CORE_DISPLACEMENT, v1.MAX_NORMALIZED_CORE_DISPLACEMENT)
        self.assertNotEqual(v2.VIEW_FRAME_PARAMS, v1.VIEW_FRAME_PARAMS)

    def test_profile_remains_exact_identity(self):
        for layer_id in v2.LAYER_IDS:
            self.assertEqual(v2.VIEW_FRAME_PARAMS[layer_id]["PROFILE"], (1.0, 1.0, 0.0))
        fixture = build_e_fixture(M0, H6N, 80, 0.0, +1)
        result = v2.build_probe(fixture, +1)
        self.assertEqual(result.base.core_vertices, result.control.core_vertices)

    def test_v2_is_materially_distinct_from_v1_at_front(self):
        fixture = build_e_fixture(M0, H6N, 80, 1.0, +1)
        r1 = v1.build_probe(fixture, +1)
        r2 = v2.build_probe(fixture, +1)
        self.assertNotEqual(r1.base.core_vertices, r2.base.core_vertices)
        self.assertEqual(r1.base.ear_shapes, r2.base.ear_shapes)
        self.assertEqual(r1.base.limb_meshes, r2.base.limb_meshes)
        self.assertEqual(r1.base.tail_mesh, r2.base.tail_mesh)

    def test_v2_signature_is_stable_and_distinct(self):
        self.assertEqual(v2.integration_signature(), v2.integration_signature())
        self.assertNotEqual(v2.integration_signature(), v1.integration_signature())

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
