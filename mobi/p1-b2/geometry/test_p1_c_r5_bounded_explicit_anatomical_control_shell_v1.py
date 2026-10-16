from __future__ import annotations

from pathlib import Path
import unittest

from c3_semantic import canonical_bytes
from e_v0_fixture_adapter import H6N, build_e_fixture
from e_v0_profiles import M0
import p1_c_r5_bounded_explicit_anatomical_control_shell_v1 as r5


class P1CR5BoundedExplicitAnatomicalControlShellTest(unittest.TestCase):
    def _fixture(self, t):
        return build_e_fixture(M0, H6N, 80, t, +1)

    def test_frozen_capacity_ceiling(self):
        self.assertEqual(r5.CORE_CONTROL_COUNT, 54)
        self.assertEqual(r5.JUNCTION_CONTROL_COUNT, 16)
        self.assertEqual(r5.AUTHORITATIVE_CONTROL_COUNT, 70)
        self.assertEqual(r5.CORE_FACE_COUNT, 50)
        self.assertEqual(r5.AUTHORITATIVE_FACE_COUNT, 54)
        self.assertLessEqual(r5.CORE_CONTROL_COUNT, 72)
        self.assertLessEqual(r5.JUNCTION_CONTROL_COUNT, 24)
        self.assertLessEqual(r5.AUTHORITATIVE_CONTROL_COUNT, 96)
        self.assertLessEqual(r5.AUTHORITATIVE_FACE_COUNT, 128)

    def test_one_signature_across_neutral_views(self):
        signatures = {r5.build_shell(self._fixture(t)).signature for t in (0.0, 0.5, 1.0)}
        self.assertEqual(len(signatures), 1)
        self.assertEqual(next(iter(signatures)), r5.shell_signature())

    def test_exact_six_external_domains(self):
        result = r5.build_shell(self._fixture(0.5))
        self.assertEqual(tuple(sorted(result.domain_bounds)), tuple(sorted(r5.EXTERNAL_DOMAINS)))
        self.assertEqual(len(result.domain_bounds), 6)

    def test_semantic_payload_is_read_only(self):
        for t in (0.0, 0.5, 1.0):
            fixture = self._fixture(t)
            before = canonical_bytes(fixture.payload)
            r5.build_shell(fixture)
            after = canonical_bytes(fixture.payload)
            self.assertEqual(before, after)

    def test_paws_remain_pinned(self):
        for t in (0.0, 0.5, 1.0):
            result = r5.build_shell(self._fixture(t))
            self.assertLessEqual(result.paw_pin_error, 1e-9)

    def test_all_geometry_finite_and_bounds_truthful(self):
        for t in (0.0, 0.5, 1.0):
            fixture = self._fixture(t)
            result = r5.build_shell(fixture)
            payload = r5.result_dict(fixture, result)
            self.assertTrue(payload["finite"])
            for domain, rect in result.domain_bounds.items():
                points = [
                    p
                    for primitive in r5.all_primitives(result)
                    if primitive.domain == domain
                    for p in primitive.points
                ]
                self.assertTrue(points)
                for x, y in points:
                    self.assertLessEqual(rect[0] - 1e-9, x)
                    self.assertLessEqual(x, rect[2] + 1e-9)
                    self.assertLessEqual(rect[1] - 1e-9, y)
                    self.assertLessEqual(y, rect[3] + 1e-9)

    def test_explicit_cage_is_not_view_authored(self):
        source = Path(r5.__file__).read_text(encoding="utf-8")
        for token in (
            "PROFILE_BASE",
            "THREE_QUARTER_BASE",
            "FRONT_BASE",
            "MORPH_TARGET",
            "BLEND_SHAPE",
            "CORRECTION_CATALOG",
        ):
            self.assertNotIn(token, source)
        self.assertNotIn("M0_NEUTRAL_V01\" :", source)
        self.assertNotIn("H4\" :", source)
        self.assertNotIn("H5\" :", source)
        self.assertNotIn("H6N\" :", source)
        self.assertNotIn("H7\" :", source)

    def test_control_ids_and_face_topology_are_unique(self):
        result = r5.build_shell(self._fixture(0.5))
        ids = [control.id for control in result.controls + result.junction_controls]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(result.controls), r5.CORE_CONTROL_COUNT)
        self.assertEqual(len(result.junction_controls), r5.JUNCTION_CONTROL_COUNT)
        self.assertEqual(len(result.core_faces), r5.CORE_FACE_COUNT)
        self.assertEqual(len(result.root_faces), 4)


if __name__ == "__main__":
    unittest.main()
