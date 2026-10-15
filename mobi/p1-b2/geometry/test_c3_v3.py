import unittest

from c3_renderer_minimal_v3 import MINIMAL_CORRECTION_VERSION, render_fixture
from c3_renderers import CORRECTION_H4
from c3_semantic import MORPHOLOGIES, SIZES, build_common_fixture
from run_c3_matrix_v3 import canonical_bytes, run_c3_matrix


class P1C3MinimalCorrectionV3Tests(unittest.TestCase):
    def test_h6_rf_c_uses_same_base_shapes_as_rf_b(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                    fixture = build_common_fixture(
                        morphology,
                        "H6_CHANGE_FACING_2P5D",
                        size_dp,
                        t,
                    )
                    rf_b = render_fixture(fixture, "RF_B")
                    rf_c = render_fixture(fixture, "RF_C")
                    self.assertEqual(rf_b["semanticHash"], fixture.semantic_hash)
                    self.assertEqual(rf_c["semanticHash"], fixture.semantic_hash)
                    self.assertEqual(rf_b["shapes"], rf_c["shapes"])
                    self.assertEqual(rf_b["visualBounds"], rf_c["visualBounds"])
                    self.assertEqual(rf_b["partitionBounds"], rf_c["partitionBounds"])
                    self.assertEqual(rf_b["corrections"], tuple())
                    self.assertEqual(rf_c["corrections"], tuple())
                    self.assertEqual(rf_c["minimalCorrectionVersion"], MINIMAL_CORRECTION_VERSION)

    def test_h4_single_reusable_correction_materially_reduces_height_step(self):
        sample_count = 17
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                sequences = {}
                for variant in ("RF_B", "RF_C"):
                    rendered = []
                    for index in range(sample_count):
                        t = index / (sample_count - 1)
                        fixture = build_common_fixture(
                            morphology,
                            "H4_SIT_TO_STAND",
                            size_dp,
                            t,
                        )
                        item = render_fixture(fixture, variant)
                        self.assertEqual(item["semanticHash"], fixture.semantic_hash)
                        if variant == "RF_B":
                            self.assertEqual(item["corrections"], tuple())
                        else:
                            self.assertEqual(item["corrections"], (CORRECTION_H4,))
                        rendered.append(item)
                    sequences[variant] = rendered

                def max_height_step(items):
                    heights = [item["visualBounds"].height for item in items]
                    return max(abs(b - a) for a, b in zip(heights, heights[1:]))

                rf_b_step = max_height_step(sequences["RF_B"])
                rf_c_step = max_height_step(sequences["RF_C"])
                # Engineering discriminator, not a product animation threshold:
                # the single H4 correction must show a strong cross-morphology
                # continuity benefit rather than a cosmetic or marginal change.
                self.assertLess(
                    rf_c_step,
                    0.40 * rf_b_step,
                    (morphology.id, size_dp, rf_b_step, rf_c_step),
                )

    def test_full_matrix_is_deterministic_and_h4_only(self):
        first_records, first_summary = run_c3_matrix(sample_count=9)
        second_records, second_summary = run_c3_matrix(sample_count=9)
        self.assertEqual(canonical_bytes(first_records), canonical_bytes(second_records))
        self.assertEqual(canonical_bytes(first_summary), canonical_bytes(second_summary))
        self.assertEqual(first_summary["semanticHashMismatchTotal"], 0)
        self.assertEqual(first_summary["rfBMaxCorrectionFamilyCount"], 0)
        self.assertEqual(first_summary["rfCCorrectionFamilies"], [CORRECTION_H4])
        self.assertEqual(first_summary["rfCMaxCorrectionFamilyCountPerRecord"], 1)


if __name__ == "__main__":
    unittest.main()
