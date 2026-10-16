from __future__ import annotations

from pathlib import Path
import unittest

from c3_semantic import canonical_bytes
from e_v0_fixture_adapter import H6N, build_e_fixture
from e_v0_profiles import M0
import p1_c_r6_reference_derived_intrinsic_template_v1 as r6


class P1CR6ReferenceDerivedIntrinsicTemplateTest(unittest.TestCase):
    def _fixture(self, t):
        return build_e_fixture(M0, H6N, 80, t, +1)

    def test_frozen_source_identity_and_capacity(self):
        self.assertEqual(r6.PROTOTYPE_VERSION, "P1_C_R6_REFERENCE_DERIVED_INTRINSIC_TEMPLATE_V1")
        self.assertEqual(r6.SOURCE_PACK_ID, "R6_CONSTRUCTION_PACK_V1")
        self.assertEqual(r6.CORE_CONTROL_COUNT, 54)
        self.assertEqual(r6.JUNCTION_CONTROL_COUNT, 16)
        self.assertEqual(r6.AUTHORITATIVE_CONTROL_COUNT, 70)
        self.assertEqual(r6.CORE_FACE_COUNT, 50)
        self.assertEqual(r6.AUTHORITATIVE_FACE_COUNT, 54)
        self.assertEqual(r6.DERIVED_SUBDIVISION_STEPS, 0)
        self.assertLessEqual(r6.AUTHORITATIVE_CONTROL_COUNT, 96)
        self.assertLessEqual(r6.AUTHORITATIVE_FACE_COUNT, 128)

    def test_frozen_stage1_origin_rules(self):
        self.assertEqual(r6.ROW_ORIGIN_RULES["NECK_INSERTION"], ("HEAD_FORE", 0.50))
        self.assertEqual(r6.ROW_ORIGIN_RULES["ABDOMINAL_TUCK"], ("BODY_PELVIS", 0.42))

    def test_frozen_stage1_coordinate_anchors(self):
        self.assertEqual(r6.CORE_TEMPLATE["ROSTRUM"][0], (+0.108, +0.030, +0.000))
        self.assertEqual(r6.CORE_TEMPLATE["CRANIUM_CHEEK"][1], (+0.020, +0.064, +0.103))
        self.assertEqual(r6.CORE_TEMPLATE["NECK_INSERTION"][3], (+0.028, -0.048, +0.000))
        self.assertEqual(r6.CORE_TEMPLATE["SHOULDER_CHEST"][3], (+0.062, -0.136, +0.000))
        self.assertEqual(r6.CORE_TEMPLATE["ABDOMINAL_TUCK"][3], (+0.010, -0.030, +0.000))
        self.assertEqual(r6.CORE_TEMPLATE["HAUNCH_REAR"][1], (-0.114, +0.052, +0.108))
        self.assertEqual(r6.FORE_ROOT_TEMPLATE[0], (+0.050, +0.020, +0.108))
        self.assertEqual(r6.HIND_ROOT_TEMPLATE[1], (-0.090, +0.028, +0.120))

    def test_one_signature_across_neutral_views(self):
        signatures = {r6.build_shell(self._fixture(t)).signature for t in (0.0, 0.5, 1.0)}
        self.assertEqual(signatures, {r6.shell_signature()})

    def test_exact_six_external_domains_and_no_correction(self):
        fixture = self._fixture(0.5)
        result = r6.build_shell(fixture)
        payload = r6.result_dict(fixture, result)
        self.assertEqual(tuple(sorted(result.domain_bounds)), tuple(sorted(r6.EXTERNAL_DOMAINS)))
        self.assertEqual(len(result.domain_bounds), 6)
        self.assertEqual(payload["correctionUseCount"], 0)
        self.assertEqual(payload["sourcePackId"], "R6_CONSTRUCTION_PACK_V1")

    def test_semantic_payload_is_read_only_and_paws_pinned(self):
        for t in (0.0, 0.5, 1.0):
            fixture = self._fixture(t)
            before = canonical_bytes(fixture.payload)
            result = r6.build_shell(fixture)
            after = canonical_bytes(fixture.payload)
            self.assertEqual(before, after)
            self.assertLessEqual(result.paw_pin_error, 1e-9)

    def test_all_geometry_finite_and_bounds_truthful(self):
        for t in (0.0, 0.5, 1.0):
            fixture = self._fixture(t)
            result = r6.build_shell(fixture)
            self.assertTrue(r6.result_dict(fixture, result)["finite"])
            for domain, rect in result.domain_bounds.items():
                points = [
                    point
                    for primitive in r6.all_primitives(result)
                    if primitive.domain == domain
                    for point in primitive.points
                ]
                self.assertTrue(points)
                for x, y in points:
                    self.assertLessEqual(rect[0] - 1e-9, x)
                    self.assertLessEqual(x, rect[2] + 1e-9)
                    self.assertLessEqual(rect[1] - 1e-9, y)
                    self.assertLessEqual(y, rect[3] + 1e-9)

    def test_source_has_no_runtime_view_bases_or_post_evidence_corrections(self):
        source = Path(r6.__file__).read_text(encoding="utf-8")
        for token in (
            "PROFILE_BASE",
            "THREE_QUARTER_BASE",
            "FRONT_BASE",
            "MORPH_TARGET",
            "BLEND_SHAPE",
            "CORRECTION_CATALOG",
        ):
            self.assertNotIn(token, source)
        self.assertEqual(len(r6.SOURCE_IDS), 5)


if __name__ == "__main__":
    unittest.main()
