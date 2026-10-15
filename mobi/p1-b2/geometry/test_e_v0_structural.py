from __future__ import annotations

import unittest

import c3_semantic
from c3_renderers import CORRECTION_H4
from e_v0_fixture_adapter import H1, H4, H6N, MORPHOLOGIES, SIZES, build_e_fixture
from e_v0_profiles import I1_COMPACT, I2_LANKY, validate_probe_bounds
from e_v0_renderer_adapter import READABILITY_AID_MODE, render_e
from run_e_v0_structural_matrix import run_matrix


class P1EV0StructuralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records, cls.summary = run_matrix()

    def test_probe_values_stay_inside_stress_envelope(self):
        result = validate_probe_bounds()
        self.assertTrue(result["pass"], result)
        self.assertEqual([], result["failures"])

    def test_matrix_dimensions_are_exact(self):
        self.assertEqual(5, len(MORPHOLOGIES))
        self.assertEqual((64, 80, 96), SIZES)
        self.assertIn(I1_COMPACT.id, self.summary["morphologies"])
        self.assertIn(I2_LANKY.id, self.summary["morphologies"])
        # Per morphology×size: H1=1, H4=17, H5=1, H6N=41×2, H7=17 = 118.
        self.assertEqual(5 * 3 * 118, self.summary["recordCount"])

    def test_semantics_paws_partitions_and_core_integrity(self):
        self.assertEqual(0, self.summary["semanticHashMismatchTotal"])
        self.assertLessEqual(self.summary["maxVisiblePawCenterErrorDp"], 1e-9)
        self.assertLessEqual(self.summary["maxPartitionCount"], 4)
        self.assertEqual(0, self.summary["coreDisconnectCount"])
        self.assertEqual(0, self.summary["tailPrimitiveMismatchCount"])
        self.assertGreaterEqual(self.summary["minimumEarPrimitiveCount"], 2)

    def test_correction_inventory_does_not_expand(self):
        self.assertEqual([CORRECTION_H4], self.summary["correctionFamilies"])
        self.assertEqual(0, self.summary["nonH4CorrectionUseCount"])
        for record in self.records:
            if record["caseId"] == H4:
                self.assertEqual([CORRECTION_H4], record["corrections"])
            else:
                self.assertEqual([], record["corrections"])

    def test_no_readability_aid_is_preemptively_activated(self):
        self.assertEqual([READABILITY_AID_MODE], self.summary["readabilityAidModes"])
        self.assertEqual("NONE_BASELINE", READABILITY_AID_MODE)

    def test_compact_and_lanky_instantiate_distinct_equal_scale_geometry(self):
        probe = self.summary["compactVsLankyNeutral80"]
        self.assertTrue(probe["geometryHashesDiffer"])
        self.assertGreater(abs(probe["forePelvisSpanDeltaDp"]), 1e-6)

    def test_registry_extension_is_scoped_and_restored(self):
        morph_registry = c3_semantic.MORPHOLOGIES
        orientation_registry = c3_semantic.ORIENTATION_MORPH
        fixture = build_e_fixture(I1_COMPACT, H1, 80, 0.0, +1)
        rendered = render_e(fixture)
        self.assertEqual(fixture.semantic_hash, rendered["semanticHash"])
        self.assertIs(morph_registry, c3_semantic.MORPHOLOGIES)
        self.assertIs(orientation_registry, c3_semantic.ORIENTATION_MORPH)

    def test_new_probe_can_use_view_resolved_h6n_without_authored_rescue(self):
        fixture = build_e_fixture(I2_LANKY, H6N, 80, 0.4, +1)
        rendered = render_e(fixture)
        self.assertEqual((), rendered["corrections"])
        self.assertEqual(fixture.semantic_hash, rendered["semanticHash"])
        self.assertLessEqual(len(rendered["partitionBounds"]), 4)


if __name__ == "__main__":
    unittest.main()
