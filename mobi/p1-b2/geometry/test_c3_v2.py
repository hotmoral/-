import math
import unittest

from c3_renderer_validity_v2 import VALIDITY_ADAPTER_VERSION, render_fixture
from c3_semantic import MORPHOLOGIES, SIZES, build_common_fixture
from run_c3_matrix_v2 import canonical_bytes, run_c3_matrix


class P1C3ValidityV2Tests(unittest.TestCase):
    def test_adapter_preserves_semantic_identity(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                    fixture = build_common_fixture(morphology, "H6_CHANGE_FACING_2P5D", size_dp, t)
                    for variant in ("RF_B", "RF_C"):
                        rendered = render_fixture(fixture, variant)
                        self.assertEqual(rendered["semanticHash"], fixture.semantic_hash)
                        self.assertEqual(rendered["validityAdapterVersion"], VALIDITY_ADAPTER_VERSION)

    def test_h6_tail_tip_has_no_front_view_mirror_jump(self):
        sample_count = 33
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for variant in ("RF_B", "RF_C"):
                    previous_tip = None
                    max_step = 0.0
                    for index in range(sample_count):
                        t = index / (sample_count - 1)
                        fixture = build_common_fixture(morphology, "H6_CHANGE_FACING_2P5D", size_dp, t)
                        rendered = render_fixture(fixture, variant)
                        tails = [shape for shape in rendered["shapes"] if shape.get("role") == "tail"]
                        self.assertEqual(len(tails), 1)
                        tip = tails[0]["points"][-1]
                        if previous_tip is not None:
                            step = math.hypot(tip.x - previous_tip.x, tip.y - previous_tip.y)
                            max_step = max(max_step, step)
                        previous_tip = tip
                    # Engineering validity bound for a 33-sample half-turn.
                    # This rejects the v1 sign-flip mirror jump; it is not a
                    # product animation-quality threshold.
                    self.assertLess(
                        max_step,
                        0.12 * size_dp,
                        (morphology.id, size_dp, variant, max_step),
                    )

    def test_matrix_remains_byte_deterministic(self):
        first_records, first_summary = run_c3_matrix(sample_count=9)
        second_records, second_summary = run_c3_matrix(sample_count=9)
        self.assertEqual(canonical_bytes(first_records), canonical_bytes(second_records))
        self.assertEqual(canonical_bytes(first_summary), canonical_bytes(second_summary))
        self.assertEqual(first_summary["semanticHashMismatchTotal"], 0)
        self.assertEqual(first_summary["rfBMaxCorrectionFamilyCount"], 0)
        self.assertEqual(
            first_summary["rfCCorrectionFamilies"],
            ["H4_CORE_ENVELOPE", "H6_TURN_ENVELOPE"],
        )


if __name__ == "__main__":
    unittest.main()
