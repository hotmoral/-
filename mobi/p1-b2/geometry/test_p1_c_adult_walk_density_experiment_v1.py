from __future__ import annotations

import math
import unittest

from p1_c_adult_walk_density_experiment_v1 import (
    CYCLE_SECONDS,
    DIRECTION_COUNTS,
    FOOTFALL_OFFSETS,
    FRAME_COUNTS,
    LIMBS,
    STANCE_FRACTION,
    angular_error_deg,
    disagreement,
    evaluate_combined,
    evaluate_direction_count,
    evaluate_frame_count,
    limb_cycle,
    mask,
    nearest_phase,
    nearest_yaw,
    render_reference,
    support_state,
)


class AdultWalkDensityExperimentTests(unittest.TestCase):
    def test_lateral_sequence_offsets_are_frozen(self):
        self.assertEqual(LIMBS, ("RH", "RF", "LH", "LF"))
        self.assertEqual([FOOTFALL_OFFSETS[x] for x in LIMBS], [0.0, 0.25, 0.5, 0.75])

    def test_stance_fraction_matches_reference_timing(self):
        self.assertAlmostEqual(STANCE_FRACTION, 0.80 / 1.08, places=12)
        self.assertGreater(STANCE_FRACTION, 0.70)
        self.assertLess(STANCE_FRACTION, 0.80)

    def test_quantizers_wrap(self):
        self.assertAlmostEqual(nearest_phase(0.999, 12), 0.0)
        self.assertAlmostEqual(nearest_yaw(2.0 * math.pi - 1e-4, 12), 0.0)

    def test_direction_max_error_monotone(self):
        rows = [evaluate_direction_count(d) for d in DIRECTION_COUNTS]
        vals = [r["maxAngularErrorDeg"] for r in rows]
        for a, b in zip(vals, vals[1:]):
            self.assertGreaterEqual(a + 1e-9, b)

    def test_frame_time_error_monotone(self):
        rows = [evaluate_frame_count(f) for f in FRAME_COUNTS]
        vals = [r["maxPhaseQuantizationMs"] for r in rows]
        for a, b in zip(vals, vals[1:]):
            self.assertGreater(a, b)

    def test_support_state_has_multiple_support_patterns(self):
        patterns = {support_state(k / 64.0) for k in range(64)}
        self.assertGreaterEqual(len(patterns), 4)
        self.assertTrue(all(len(p) >= 2 for p in patterns))

    def test_render_is_deterministic_and_nonempty(self):
        a = render_reference(math.radians(37.0), 0.317)
        b = render_reference(math.radians(37.0), 0.317)
        ma, mb = mask(a), mask(b)
        self.assertEqual(ma, mb)
        self.assertGreater(len(ma), 100)
        self.assertEqual(disagreement(ma, mb), 0.0)

    def test_combined_asset_count_is_exact(self):
        for d in DIRECTION_COUNTS:
            for f in FRAME_COUNTS:
                row = evaluate_combined(d, f)
                self.assertEqual(row["authoredFrameEquivalent"], d * f)

    def test_limb_cycle_stance_then_swing(self):
        for limb in LIMBS:
            offset = FOOTFALL_OFFSETS[limb]
            _, stance0, lift0 = limb_cycle(limb, offset + 0.01)
            _, stance1, lift1 = limb_cycle(limb, offset + STANCE_FRACTION + 0.05 * (1.0 - STANCE_FRACTION))
            self.assertTrue(stance0)
            self.assertFalse(stance1)
            self.assertEqual(lift0, 0.0)
            self.assertGreater(lift1, 0.0)


if __name__ == "__main__":
    unittest.main()
