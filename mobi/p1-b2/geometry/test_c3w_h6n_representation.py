import unittest

from c3_semantic import canonical_bytes, semantic_payload
from c3w_h6n_fixture_adapter import DIRECTIONS, MORPHOLOGIES, SIZES, H6N_CASE_ID, build_h6n_fixture
from c3w_renderer_adapter import STRATEGIES, VARIANTS, render_h6n
from run_c3_matrix import render_payload
from run_c3w_h6n_representation_matrix import KEY_T, run_matrix


def _geometry_payload(rendered):
    payload = render_payload(rendered)
    payload.pop("variant", None)
    return payload


class C3WH6NRepresentationTests(unittest.TestCase):
    def test_fixture_adapter_preserves_h6n_v2_semantics(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in DIRECTIONS:
                    for t in KEY_T:
                        fixture = build_h6n_fixture(morphology, size_dp, t, direction)
                        self.assertEqual(fixture.case_id, H6N_CASE_ID)
                        self.assertEqual(fixture.state.validate(), [])
                        self.assertEqual(fixture.payload, semantic_payload(fixture.state))

    def test_every_strategy_preserves_semantic_hash_and_has_no_h6n_correction(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in DIRECTIONS:
                    for t in KEY_T:
                        fixture = build_h6n_fixture(morphology, size_dp, t, direction)
                        before = canonical_bytes(semantic_payload(fixture.state))
                        for strategy in STRATEGIES:
                            for variant in VARIANTS:
                                rendered = render_h6n(fixture, strategy, variant)
                                self.assertEqual(rendered["semanticHash"], fixture.semantic_hash)
                                self.assertEqual(tuple(rendered.get("corrections", ())), tuple())
                                self.assertLessEqual(len(rendered["partitionBounds"]), 4)
                                self.assertGreater(len(rendered["shapes"]), 0)
                        after = canonical_bytes(semantic_payload(fixture.state))
                        self.assertEqual(before, after)

    def test_rf_b_and_rf_c_are_geometry_identical_on_h6n_for_each_strategy(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in DIRECTIONS:
                    for t in KEY_T:
                        fixture = build_h6n_fixture(morphology, size_dp, t, direction)
                        for strategy in STRATEGIES:
                            rf_b = render_h6n(fixture, strategy, "RF_B")
                            rf_c = render_h6n(fixture, strategy, "RF_C")
                            self.assertEqual(
                                canonical_bytes(_geometry_payload(rf_b)),
                                canonical_bytes(_geometry_payload(rf_c)),
                            )

    def test_scorecard_key_times_include_shift_boundaries_and_final_front(self):
        self.assertIn(0.6, KEY_T)
        self.assertIn(0.8, KEY_T)
        self.assertEqual(KEY_T[-1], 1.0)
        fixture_pre = build_h6n_fixture(MORPHOLOGIES[1], 80, 0.6, +1)
        fixture_post = build_h6n_fixture(MORPHOLOGIES[1], 80, 0.8, +1)
        fixture_final = build_h6n_fixture(MORPHOLOGIES[1], 80, 1.0, +1)
        self.assertEqual(len(fixture_pre.state.support_set), 4)
        self.assertEqual(len(fixture_post.state.support_set), 4)
        self.assertEqual(len(fixture_final.state.support_set), 4)

    def test_full_c3w_matrix_is_byte_deterministic_and_bounded(self):
        first_records, first_summary = run_matrix(sample_count=41)
        second_records, second_summary = run_matrix(sample_count=41)
        self.assertEqual(canonical_bytes(first_records), canonical_bytes(second_records))
        self.assertEqual(canonical_bytes(first_summary), canonical_bytes(second_summary))
        self.assertEqual(first_summary["records"], 12)
        self.assertEqual(first_summary["sampleCountPerRecord"], 41)
        self.assertEqual(first_summary["semanticHashMismatchTotal"], 0)
        self.assertEqual(
            first_summary["rfVariantGeometryMismatchTotalByStrategy"],
            {strategy: 0 for strategy in STRATEGIES},
        )
        self.assertEqual(
            first_summary["maxCorrectionFamilyCountByStrategy"],
            {strategy: 0 for strategy in STRATEGIES},
        )
        self.assertTrue(
            all(value <= 4 for value in first_summary["maxPartitionGroupCountByStrategy"].values())
        )


if __name__ == "__main__":
    unittest.main()
