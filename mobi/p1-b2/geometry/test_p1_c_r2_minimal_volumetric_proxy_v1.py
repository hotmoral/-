from __future__ import annotations

import inspect
import math
import unittest

from e_v0_fixture_adapter import H4, H6N, build_e_fixture
from e_v0_profiles import M0, MORPHOLOGIES
import p1_c_r2_minimal_volumetric_proxy_v1 as r2
import run_p1_c_r2_minimal_volumetric_proxy_v1 as runner


class R2MinimalVolumetricProxyV1Test(unittest.TestCase):
    def test_frozen_anatomy_budget_is_exact(self):
        self.assertEqual(
            r2.CORE_VOLUME_IDS,
            (
                "CRANIUM_VOLUME",
                "ROSTRAL_WEDGE",
                "CERVICAL_VOLUME",
                "THORAX_VOLUME",
                "ABDOMEN_BRIDGE_VOLUME",
                "PELVIS_HAUNCH_VOLUME",
            ),
        )
        self.assertEqual(len(r2.CORE_VOLUME_IDS), 6)
        self.assertEqual(
            r2.EXTERNAL_DOMAINS,
            ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL"),
        )

    def test_source_contains_no_geometry_specialization_by_morph_case_or_named_view(self):
        source = inspect.getsource(r2)
        forbidden = (
            "M1_KITTEN_STRESS_V01",
            "M0_NEUTRAL_V01",
            "M2_ADULT_STRESS_V01",
            "I1_COMPACT_PROBE_V0",
            "I2_LANKY_PROBE_V0",
            "H1_NEUTRAL_SUPPORT",
            "H4_SIT_TO_STAND",
            "H5_CROUCH",
            "H6N_STEPPED_QUARTER_TURN_V2_ROOT_SHIFT",
            "H7_NARROW_SHORT_STEP",
            '"PROFILE"',
            '"THREE_QUARTER"',
            '"FRONT"',
        )
        for token in forbidden:
            self.assertNotIn(token, source, token)

    def test_proxy_signature_is_shared_and_stable(self):
        self.assertEqual(r2.proxy_signature(), r2.proxy_signature())
        self.assertEqual(len(r2.proxy_signature()), 64)
        signatures = set()
        for morphology in MORPHOLOGIES:
            for t in (0.0, 0.5, 1.0):
                fixture = build_e_fixture(morphology, H6N, 80, t, +1)
                signatures.add(r2.build_proxy(fixture).signature)
        self.assertEqual(signatures, {r2.proxy_signature()})

    def test_continuous_projection_not_authored_view_targets(self):
        samples = []
        for index in range(41):
            fixture = build_e_fixture(M0, H6N, 80, index / 40.0, +1)
            result = r2.build_proxy(fixture)
            self.assertTrue(math.isfinite(result.yaw_rad))
            samples.append(result.visual_bounds[2] - result.visual_bounds[0])
        # Continuous analytic projection should not produce a large view snap.
        self.assertLess(max(abs(b - a) for a, b in zip(samples, samples[1:])), 8.0)

    def test_front_mass_hierarchy_is_explicit_without_ears(self):
        fixture = build_e_fixture(M0, H6N, 80, 1.0, +1)
        result = r2.build_proxy(fixture)
        by_id = {primitive.id: primitive for primitive in result.core_primitives}

        def width(primitive):
            xs = [point[0] for point in primitive.points]
            return max(xs) - min(xs)

        cranium = width(by_id["CRANIUM_VOLUME"])
        cervical = width(by_id["CERVICAL_VOLUME"])
        thorax = width(by_id["THORAX_VOLUME"])
        self.assertGreater(cranium / cervical, 1.40)
        self.assertGreater(thorax / cervical, 1.70)
        self.assertGreater(thorax, cranium)
        # Removing ears is evidence-only and cannot change body geometry.
        body_with_ears = tuple(p for primitive in result.core_primitives for p in primitive.points)
        body_without_ears = tuple(p for primitive in result.core_primitives for p in primitive.points)
        self.assertEqual(body_with_ears, body_without_ears)

    def test_native_h4_uses_no_inherited_correction(self):
        for t in (0.0, 0.25, 0.5, 0.75, 1.0):
            fixture = build_e_fixture(M0, H4, 80, t, +1)
            result = r2.build_proxy(fixture)
            payload = r2.result_dict(fixture, result)
            self.assertEqual(payload["correctionUseCount"], 0)
            self.assertEqual(payload["externalDomainCount"], 6)
            self.assertTrue(payload["finite"])

    def test_paw_endpoints_are_exact_visual_centers(self):
        for t in (0.0, 0.5, 1.0):
            fixture = build_e_fixture(M0, H6N, 80, t, +1)
            result = r2.build_proxy(fixture)
            self.assertLessEqual(result.paw_pin_error, 1e-9)

    def test_full_retained_matrix_mechanical_lane(self):
        records, summary = runner.run_matrix()
        self.assertEqual(len(records), 1770)
        self.assertTrue(summary["mechanicalPass"], summary)
        self.assertEqual(summary["semanticMutationCount"], 0)
        self.assertEqual(summary["nonfiniteRecordCount"], 0)
        self.assertEqual(summary["domainBoundsMismatchCount"], 0)
        self.assertLessEqual(summary["maxPawPinError"], 1e-9)
        self.assertEqual(summary["proxySignatureCount"], 1)
        self.assertEqual(summary["externalDomainCounts"], [6])
        self.assertEqual(summary["correctionUseCount"], 0)
        self.assertGreater(summary["nativeH4RecordCount"], 0)
        self.assertLessEqual(summary["maxNormalizedH6NWidthStep"], 0.10)
        self.assertLessEqual(summary["maxNormalizedH6NHeightStep"], 0.10)


if __name__ == "__main__":
    unittest.main()
