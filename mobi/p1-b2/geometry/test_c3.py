import math
import unittest

from c3_renderers import ALLOWED_CORRECTIONS, GROUPS, render_fixture
from c3_semantic import CASES, MORPHOLOGIES, SIZES, build_common_fixture
from run_c3_matrix import canonical_bytes, run_c3_matrix


class P1C3DiscriminatorTests(unittest.TestCase):
    def test_common_semantics_are_body_candidate_independent(self):
        for case_id in CASES:
            for morphology in MORPHOLOGIES:
                for size_dp in SIZES:
                    for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                        fixture = build_common_fixture(morphology, case_id, size_dp, t)
                        self.assertEqual(fixture.payload["caseId"], case_id)
                        self.assertEqual(fixture.payload["morphologyId"], morphology.id)
                        self.assertEqual(fixture.payload["sizeDp"], size_dp)

    def test_rf_b_and_rf_c_never_change_semantic_identity(self):
        for case_id in CASES:
            for morphology in MORPHOLOGIES:
                for size_dp in SIZES:
                    for t in (0.0, 0.5, 1.0):
                        fixture = build_common_fixture(morphology, case_id, size_dp, t)
                        rf_b = render_fixture(fixture, "RF_B")
                        rf_c = render_fixture(fixture, "RF_C")
                        self.assertEqual(rf_b["semanticHash"], fixture.semantic_hash)
                        self.assertEqual(rf_c["semanticHash"], fixture.semantic_hash)
                        self.assertEqual(rf_b["semanticHash"], rf_c["semanticHash"])

    def test_partition_groups_are_bounded_and_truthful(self):
        for case_id in CASES:
            for morphology in MORPHOLOGIES:
                fixture = build_common_fixture(morphology, case_id, 80, 0.5)
                for variant in ("RF_B", "RF_C"):
                    rendered = render_fixture(fixture, variant)
                    groups = set(rendered["partitionBounds"])
                    self.assertTrue(groups)
                    self.assertTrue(groups.issubset(set(GROUPS)))
                    self.assertLessEqual(len(groups), 4)
                    for rect in rendered["partitionBounds"].values():
                        self.assertGreater(rect.width, 0.0)
                        self.assertGreater(rect.height, 0.0)
                        for value in (rect.left, rect.top, rect.right, rect.bottom):
                            self.assertTrue(math.isfinite(value))

    def test_rf_c_correction_families_are_bounded(self):
        seen = set()
        for case_id in CASES:
            for morphology in MORPHOLOGIES:
                for size_dp in SIZES:
                    fixture = build_common_fixture(morphology, case_id, size_dp, 0.5)
                    rf_b = render_fixture(fixture, "RF_B")
                    rf_c = render_fixture(fixture, "RF_C")
                    self.assertEqual(rf_b["corrections"], ())
                    for correction in rf_c["corrections"]:
                        self.assertIn(correction, ALLOWED_CORRECTIONS)
                        seen.add(correction)
                    if case_id == "H7_NARROW_SHORT_STEP":
                        self.assertEqual(rf_c["corrections"], ())
                    else:
                        self.assertEqual(len(rf_c["corrections"]), 1)
        self.assertEqual(seen, set(ALLOWED_CORRECTIONS))

    def test_visual_bounds_are_finite_positive(self):
        for case_id in CASES:
            for morphology in MORPHOLOGIES:
                for size_dp in SIZES:
                    for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                        fixture = build_common_fixture(morphology, case_id, size_dp, t)
                        for variant in ("RF_B", "RF_C"):
                            rect = render_fixture(fixture, variant)["visualBounds"]
                            self.assertGreater(rect.width, 0.0)
                            self.assertGreater(rect.height, 0.0)
                            for value in (rect.left, rect.top, rect.right, rect.bottom):
                                self.assertTrue(math.isfinite(value))

    def test_full_matrix_is_byte_deterministic(self):
        first_records, first_summary = run_c3_matrix(sample_count=9)
        second_records, second_summary = run_c3_matrix(sample_count=9)
        self.assertEqual(canonical_bytes(first_records), canonical_bytes(second_records))
        self.assertEqual(canonical_bytes(first_summary), canonical_bytes(second_summary))
        self.assertEqual(first_summary["semanticHashMismatchTotal"], 0)
        self.assertEqual(first_summary["rfBMaxCorrectionFamilyCount"], 0)
        self.assertLessEqual(first_summary["rfCMaxCorrectionFamilyCountPerRecord"], 1)
        self.assertEqual(first_summary["maxPartitionGroupCount"], 4)


if __name__ == "__main__":
    unittest.main()
