from __future__ import annotations

import inspect
import math
import unittest

from c3_semantic import canonical_bytes
from e_v0_fixture_adapter import H6N, build_e_fixture
from e_v0_profiles import M0, MORPHOLOGIES
import p1_c_r4_anatomy_aware_surface_shell_v1 as r4
import run_p1_c_r4_surface_shell_stage_a as runner


class R4AnatomyAwareSurfaceShellV1Test(unittest.TestCase):
    def test_frozen_topology_is_inside_r3_ceiling(self):
        self.assertEqual(len(r4.SECTION_IDS), 9)
        self.assertLessEqual(len(r4.SECTION_IDS), 10)
        self.assertEqual(r4.SECTION_SAMPLES, 8)
        self.assertLessEqual(r4.SECTION_SAMPLES, 8)
        self.assertEqual(r4.COLLAR_SAMPLES, 6)
        self.assertLessEqual(r4.COLLAR_SAMPLES, 6)
        self.assertEqual(
            r4.SECTION_IDS,
            (
                "ROSTRAL_FRONT",
                "CRANIUM_FRONT",
                "CRANIUM_REAR",
                "CERVICAL_INSERTION",
                "SHOULDER_CHEST",
                "THORAX",
                "ABDOMINAL_TUCK",
                "PELVIS",
                "HAUNCH_REAR",
            ),
        )
        self.assertEqual(
            r4.EXTERNAL_DOMAINS,
            ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL"),
        )
        self.assertEqual(r4.SECTION_FAMILY, "ELLIPTIC_TRANSVERSE_RING_V1")
        self.assertEqual(r4.FRAME_RULE, "NO_TWIST_B3_TRANSVERSE_V1")

    def test_source_contains_no_geometry_specialization_or_rejected_view_bases(self):
        source = inspect.getsource(r4)
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
            "r2.build_proxy",
            "skin_weight",
            "blendshape",
        )
        for token in forbidden:
            self.assertNotIn(token, source, token)

    def test_signature_is_shared_across_retained_morphologies_and_views(self):
        signatures = set()
        for morphology in MORPHOLOGIES:
            for t in (0.0, 0.5, 1.0):
                result = r4.build_shell(build_e_fixture(morphology, H6N, 80, t, +1))
                signatures.add(result.signature)
        self.assertEqual(signatures, {r4.shell_signature()})
        self.assertEqual(len(r4.shell_signature()), 64)

    def test_primary_views_preserve_semantics_topology_domains_and_paws(self):
        for t in (0.0, 0.5, 1.0):
            fixture = build_e_fixture(M0, H6N, 80, t, +1)
            before = canonical_bytes(fixture.payload)
            result = r4.build_shell(fixture)
            after = canonical_bytes(fixture.payload)
            self.assertEqual(before, after)
            self.assertEqual(tuple(section.id for section in result.sections), r4.SECTION_IDS)
            self.assertTrue(all(len(section.points) == 8 for section in result.sections))
            self.assertEqual(len(result.collars), 4)
            self.assertTrue(all(len(collar.points) == 6 for collar in result.collars))
            self.assertEqual(set(result.domain_bounds), set(r4.EXTERNAL_DOMAINS))
            self.assertLessEqual(result.paw_pin_error, 1e-9)
            self.assertTrue(all(math.isfinite(value) for point in r4.all_points(result) for value in point))
            self.assertEqual(r4.result_dict(fixture, result)["correctionUseCount"], 0)

    def test_front_retains_r2_cross_view_mass_hierarchy(self):
        fixture = build_e_fixture(M0, H6N, 80, 1.0, +1)
        result = r4.build_shell(fixture)
        by_id = {section.id: section for section in result.sections}

        def width(section):
            xs = [point[0] for point in section.points]
            return max(xs) - min(xs)

        cranium = width(by_id["CRANIUM_REAR"])
        cervical = width(by_id["CERVICAL_INSERTION"])
        thorax = width(by_id["THORAX"])
        self.assertAlmostEqual(cranium, 18.0, places=8)
        self.assertAlmostEqual(cervical, 10.24, places=8)
        self.assertAlmostEqual(thorax, 23.2, places=8)
        self.assertGreater(cranium / cervical, 1.40)
        self.assertGreater(thorax / cervical, 1.70)
        self.assertGreater(thorax, cranium)

    def test_projection_changes_continuously_without_authored_view_snap(self):
        widths = []
        heights = []
        for index in range(41):
            fixture = build_e_fixture(M0, H6N, 80, index / 40.0, +1)
            result = r4.build_shell(fixture)
            width = result.visual_bounds[2] - result.visual_bounds[0]
            height = result.visual_bounds[3] - result.visual_bounds[1]
            widths.append(width)
            heights.append(height)
        self.assertLessEqual(max(abs(b - a) for a, b in zip(widths, widths[1:])), 8.0)
        self.assertLessEqual(max(abs(b - a) for a, b in zip(heights, heights[1:])), 8.0)

    def test_stage_a_mechanical_lane(self):
        records, summary = runner.run_stage_a()
        self.assertEqual(len(records), 3)
        self.assertTrue(summary["mechanicalPass"], summary)
        self.assertEqual(summary["semanticMutationCount"], 0)
        self.assertEqual(summary["shellSignatureCount"], 1)
        self.assertEqual(summary["sectionCount"], 9)
        self.assertEqual(summary["sectionSamples"], 8)
        self.assertEqual(summary["collarSamples"], 6)
        self.assertEqual(summary["externalDomainCounts"], [6])
        self.assertLessEqual(summary["maxPawPinError"], 1e-9)
        self.assertEqual(summary["nonfiniteRecordCount"], 0)
        self.assertEqual(summary["domainBoundsMismatchCount"], 0)
        self.assertEqual(summary["correctionUseCount"], 0)


if __name__ == "__main__":
    unittest.main()
