from __future__ import annotations

import math
import unittest

from c3_semantic import canonical_bytes
from e_v0_fixture_adapter import H6N, build_e_fixture
from e_v0_profiles import M0
import p1_c_r8_neutral_m0_params_v1 as neutral
import p1_c_r8_regional_grammar_v1 as grammar
import p1_c_r8_regional_procedural_surface_v1 as r8


EXPECTED_GRAMMAR_SIGNATURE = "20f1ace341726b6e0b36c45a19f5d01fb5be75ff0b7d27a6e5758850db1979e5"
EXPECTED_PARAMETER_SIGNATURE = "41f3401026b1993e83835b997a727b6974c374441821d30244d6a79dbc316ecd"


class R8RegionalProceduralSurfaceTests(unittest.TestCase):
    def fixtures(self):
        return tuple(
            build_e_fixture(M0, H6N, 80, t, +1)
            for t in (0.0, 0.5, 1.0)
        )

    def test_01_grammar_signature_and_budget(self):
        self.assertEqual(grammar.grammar_signature(), EXPECTED_GRAMMAR_SIGNATURE)
        self.assertEqual(len(grammar.REGIONS), 8)
        self.assertEqual(grammar.region_parameter_count(), 54)
        self.assertEqual(len(grammar.BLEND_INTERFACES), 7)
        self.assertEqual(grammar.authoritative_scalar_count(), 61)
        self.assertLessEqual(grammar.authoritative_scalar_count(), 64)

    def test_02_parameter_signature_and_semantics(self):
        self.assertEqual(neutral.parameter_signature(), EXPECTED_PARAMETER_SIGNATURE)
        self.assertEqual(neutral.scalar_count(), 61)
        self.assertEqual(tuple(neutral.REGION_PARAMS), tuple(region["id"] for region in grammar.REGIONS))

    def test_03_exactly_six_external_domains(self):
        self.assertEqual(
            r8.EXTERNAL_DOMAINS,
            ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL"),
        )

    def test_04_semantic_payload_is_read_only(self):
        for fixture in self.fixtures():
            before = canonical_bytes(fixture.payload)
            result = r8.build_surface(fixture)
            after = canonical_bytes(fixture.payload)
            self.assertEqual(before, after)
            self.assertTrue(math.isfinite(result.paw_pin_error))

    def test_05_one_surface_signature_across_views(self):
        signatures = {r8.build_surface(fixture).signature for fixture in self.fixtures()}
        self.assertEqual(len(signatures), 1)

    def test_06_interface_overlap_is_present(self):
        for fixture in self.fixtures():
            result = r8.build_surface(fixture)
            self.assertTrue(result.interface_overlap_pass, result.interface_overlap)
            self.assertEqual(set(result.interface_overlap), {item["id"] for item in grammar.BLEND_INTERFACES})

    def test_07_paw_pin_is_exact_within_tolerance(self):
        for fixture in self.fixtures():
            result = r8.build_surface(fixture)
            self.assertLessEqual(result.paw_pin_error, 1e-9)

    def test_08_field_values_are_finite_at_canonical_anchors(self):
        for fixture in self.fixtures():
            for anchor in fixture.state.anchors.values():
                values = r8.raw_fields(fixture, float(anchor.x), float(anchor.y), 0.0)
                self.assertTrue(all(math.isfinite(value) for value in values.values()))
                self.assertTrue(math.isfinite(r8.composed_field_from_raw(values)))

    def test_09_no_view_specific_or_correction_catalogue(self):
        self.assertFalse(grammar.grammar_payload()["viewSpecificParameters"])
        self.assertEqual(grammar.CORRECTION_CATALOGUE, "NONE")
        self.assertEqual(r8.CORRECTION_USE_COUNT, 0)

    def test_10_profile_raster_is_nonempty_and_bounded(self):
        fixture = build_e_fixture(M0, H6N, 80, 0.0, +1)
        raster = r8.rasterize_body(fixture)
        self.assertEqual(raster.width, grammar.SAMPLING_RULE["canvasWidthPx"])
        self.assertEqual(raster.height, grammar.SAMPLING_RULE["canvasHeightPx"])
        self.assertGreater(raster.occupied_pixel_count, 0)
        self.assertEqual(len(raster.mask), raster.width * raster.height)
        min_x, min_y, max_x, max_y = raster.world_bounds
        bx0, by0, bx1, by1 = raster.body_bounds
        self.assertLessEqual(min_x, bx0)
        self.assertLessEqual(min_y, by0)
        self.assertGreaterEqual(max_x, bx1)
        self.assertGreaterEqual(max_y, by1)


if __name__ == "__main__":
    unittest.main()
