from __future__ import annotations

import math
import unittest

from p1_c_r9_intrinsic_curve_pixel_v1 import (
    CANVAS_H,
    CANVAS_W,
    CONTROL_NODE_LIMIT,
    CURVE_GROUP_LIMIT,
    CURVE_SEGMENT_LIMIT,
    EXTERNAL_DOMAINS,
    binary_mask,
    build_neutral_carrier,
    carrier_signature,
    mask_bytes,
    mask_metrics,
    neutral_semantic_frame,
    orientation_metrics,
    paw_pin_errors,
    render_mask,
    structural_summary,
)


class R9IntrinsicCurvePixelV1Test(unittest.TestCase):
    def setUp(self):
        self.carrier = build_neutral_carrier()

    def test_01_capacity_and_domains(self):
        summary = structural_summary(self.carrier)
        self.assertLessEqual(summary["curveGroups"], CURVE_GROUP_LIMIT)
        self.assertLessEqual(summary["controlNodes"], CONTROL_NODE_LIMIT)
        self.assertLessEqual(summary["curveSegments"], CURVE_SEGMENT_LIMIT)
        self.assertEqual(set(summary["domains"]), set(EXTERNAL_DOMAINS))
        self.assertEqual(summary["nativeRaster"], [80, 80])

    def test_02_single_signature_independent_of_view(self):
        sig = carrier_signature(self.carrier)
        self.assertEqual(len(sig), 64)
        for yaw in (0.0, math.pi / 8.0, math.pi / 4.0, 3.0 * math.pi / 8.0, math.pi / 2.0):
            render_mask(self.carrier, yaw)
            self.assertEqual(carrier_signature(self.carrier), sig)

    def test_03_exact_paw_binding_profile_3q_front(self):
        for yaw in (0.0, math.pi / 4.0, math.pi / 2.0):
            errors = paw_pin_errors(self.carrier, yaw)
            self.assertEqual(set(errors), {"FORE_PAW_L", "FORE_PAW_R", "HIND_PAW_L", "HIND_PAW_R"})
            self.assertLessEqual(max(errors.values()), 1e-9)

    def test_04_semantic_frame_not_mutated_by_render(self):
        for yaw in (0.0, math.pi / 4.0, math.pi / 2.0):
            before = neutral_semantic_frame(yaw)
            render_mask(self.carrier, yaw)
            after = neutral_semantic_frame(yaw)
            self.assertEqual(before, after)

    def test_05_native_raster_and_determinism(self):
        for yaw in (0.0, math.pi / 4.0, math.pi / 2.0):
            a = render_mask(self.carrier, yaw)
            b = render_mask(self.carrier, yaw)
            self.assertEqual(len(a), CANVAS_H)
            self.assertTrue(all(len(row) == CANVAS_W for row in a))
            self.assertEqual(mask_bytes(a), mask_bytes(b))
            metrics = mask_metrics(binary_mask(a), yaw)
            self.assertGreater(metrics.occupied_pixels, 180)
            self.assertLessEqual(metrics.component_count, 3)

    def test_06_ear_neutralized_is_structural_not_empty(self):
        for yaw in (math.pi / 4.0, math.pi / 2.0):
            full = render_mask(self.carrier, yaw, ear_neutralized=False)
            neutral = render_mask(self.carrier, yaw, ear_neutralized=True)
            self.assertNotEqual(mask_bytes(full), mask_bytes(neutral))
            metrics = mask_metrics(binary_mask(neutral), yaw)
            self.assertGreater(metrics.occupied_pixels, 160)
            self.assertLessEqual(metrics.component_count, 3)

    def test_07_domain_diagnostic_uses_only_declared_values(self):
        allowed = {0, 48, 92, 122, 158, 188, 220}
        for yaw in (0.0, math.pi / 4.0, math.pi / 2.0):
            mask = render_mask(self.carrier, yaw, domain_values=True)
            values = {v for row in mask for v in row}
            self.assertTrue(values.issubset(allowed))
            self.assertIn(48, values)

    def test_08_continuous_orientation_pixel_stability_gate(self):
        result = orientation_metrics(self.carrier, steps=13)
        self.assertEqual(result["steps"], 13)
        self.assertLessEqual(result["maxAreaJumpRatio"], 0.25)
        self.assertLessEqual(result["maxCentroidStepPx"], 4.0)
        self.assertLessEqual(result["maxXorUnionRatio"], 0.45)
        self.assertLessEqual(result["maxComponentCount"], 3)
        self.assertGreater(result["minOccupiedPixels"], 160)
        self.assertEqual(len(set(result["frameHashes"])), 13)

    def test_09_front_and_profile_have_nonzero_two_dimensional_extent(self):
        profile = mask_metrics(binary_mask(render_mask(self.carrier, 0.0)), 0.0)
        front = mask_metrics(binary_mask(render_mask(self.carrier, math.pi / 2.0)), math.pi / 2.0)
        self.assertIsNotNone(profile.bbox)
        self.assertIsNotNone(front.bbox)
        p_width = profile.bbox[2] - profile.bbox[0] + 1
        p_height = profile.bbox[3] - profile.bbox[1] + 1
        f_width = front.bbox[2] - front.bbox[0] + 1
        f_height = front.bbox[3] - front.bbox[1] + 1
        self.assertGreaterEqual(p_width, 35)
        self.assertGreaterEqual(p_height, 35)
        self.assertGreaterEqual(f_width, 12)
        self.assertGreaterEqual(f_height, 35)


if __name__ == "__main__":
    unittest.main(verbosity=2)
