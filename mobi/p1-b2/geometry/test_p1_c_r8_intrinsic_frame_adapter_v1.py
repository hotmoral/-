from __future__ import annotations

import math
import unittest

from e_v0_fixture_adapter import H6N, build_e_fixture
from e_v0_profiles import M0
import p1_c_r8_intrinsic_frame_adapter_v1 as adapter
from test_p1_c_r8_regional_procedural_surface_v1 import R8RegionalProceduralSurfaceTests


class R8IntrinsicFrameAdapterTests(unittest.TestCase):
    def test_exact_front_abdomen_frame_is_non_degenerate(self):
        fixture = build_e_fixture(M0, H6N, 80, 1.0, +1)
        body = fixture.state.anchors["BODY_ROOT"]
        pelvis = fixture.state.anchors["PELVIS_REF"]
        midpoint = (
            0.5 * (float(body.x) + float(pelvis.x)),
            0.5 * (float(body.y) + float(pelvis.y)),
            0.5 * (
                adapter._anchor_depth_dp(fixture, "BODY_ROOT")
                + adapter._anchor_depth_dp(fixture, "PELVIS_REF")
            ),
        )
        values = adapter.raw_fields(fixture, *midpoint)
        self.assertTrue(math.isfinite(values["ABDOMEN_TUCK"]))
        self.assertLess(values["ABDOMEN_TUCK"], 1e6)

    def test_all_declared_interfaces_overlap_across_neutral_views(self):
        for t in (0.0, 0.5, 1.0):
            fixture = build_e_fixture(M0, H6N, 80, t, +1)
            checks = adapter.interface_overlap_checks(fixture)
            self.assertTrue(all(checks.values()), (t, checks))

    def test_adapter_does_not_add_correction_catalogue_or_domains(self):
        self.assertEqual(adapter.CORRECTION_USE_COUNT, 0)
        self.assertEqual(
            adapter.EXTERNAL_DOMAINS,
            ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL"),
        )


if __name__ == "__main__":
    unittest.main()
