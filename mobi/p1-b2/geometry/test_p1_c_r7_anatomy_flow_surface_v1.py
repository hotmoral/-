from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import unittest

from c3_semantic import canonical_bytes
from e_v0_fixture_adapter import H6N, build_e_fixture
from e_v0_profiles import M0
import p1_c_r7_anatomy_flow_surface_v1 as r7
import p1_c_r7_anatomy_flow_topology_v1 as topo


class P1CR7AnatomyFlowSurfaceTest(unittest.TestCase):
    def _fixture(self, t):
        return build_e_fixture(M0, H6N, 80, t, +1)

    def test_frozen_topology_identity_and_capacity(self):
        self.assertTrue(topo.validate_topology())
        self.assertEqual(topo.topology_signature(), "626ea4b8b1670c641feff654a458506a64fc7fae8ffd24e3f6fb00695b5bf8a9")
        self.assertEqual(len(topo.VERTEX_IDS), 63)
        self.assertEqual(len(topo.FACES), 66)
        self.assertEqual(len(topo.edge_set()), 127)
        self.assertLessEqual(len(topo.VERTEX_IDS), 96)
        self.assertLessEqual(len(topo.FACES), 128)
        self.assertEqual(topo.DERIVED_SUBDIVISION_STEPS, 0)

    def test_graph_is_not_uniform_station_perimeter_carrier(self):
        self.assertEqual(tuple(map(len, (
            topo.DORSAL,
            topo.LEFT_DORSOLATERAL,
            topo.LEFT_VENTROLATERAL,
            topo.VENTRAL,
            topo.RIGHT_DORSOLATERAL,
            topo.RIGHT_VENTROLATERAL,
        ))), (9, 9, 10, 8, 9, 10))
        source = Path(topo.__file__).read_text(encoding="utf-8")
        for token in ("ROW_IDS", "PERIMETER_IDS", "PROFILE_BASE", "THREE_QUARTER_BASE", "FRONT_BASE"):
            self.assertNotIn(token, source)

    def test_shared_proximal_boundaries_are_core_limb_interfaces(self):
        edge_domains = defaultdict(set)
        for domain, face in topo.FACES:
            for a, b in zip(face, face[1:] + face[:1]):
                edge_domains[tuple(sorted((a, b)))].add(domain)
        for domain, boundary in topo.SHARED_BOUNDARIES.items():
            for a, b in zip(boundary, boundary[1:] + boundary[:1]):
                self.assertEqual(edge_domains[tuple(sorted((a, b)))], {"CORE", domain})

    def test_frozen_coordinate_transcription_and_mirroring(self):
        self.assertEqual(r7.COORDINATES["D_SHOULDER"], (+0.018, +0.130, +0.000))
        self.assertEqual(r7.COORDINATES["LL_TUCK"], (-0.014, -0.006, +0.072))
        self.assertEqual(r7.COORDINATES["FORE_L_PROX_CRANIAL"], (+0.030, -0.152, +0.066))
        self.assertEqual(r7.COORDINATES["HIND_L_PROX_CAUDAL"], (-0.068, -0.132, +0.080))
        for left, right in (
            ("LU_CHEEK", "RU_CHEEK"),
            ("LL_THORAX", "RL_THORAX"),
            ("FORE_L_PROX_CAUDAL", "FORE_R_PROX_CAUDAL"),
            ("HIND_L_PROX_CRANIAL", "HIND_R_PROX_CRANIAL"),
        ):
            lx, ly, lz = r7.COORDINATES[left]
            rx, ry, rz = r7.COORDINATES[right]
            self.assertEqual((lx, ly), (rx, ry))
            self.assertEqual(lz, -rz)

    def test_one_surface_signature_across_neutral_views(self):
        signatures = {r7.build_surface(self._fixture(t)).signature for t in (0.0, 0.5, 1.0)}
        self.assertEqual(signatures, {r7.surface_signature()})

    def test_exact_six_external_domains_and_no_correction(self):
        result = r7.build_surface(self._fixture(0.5))
        payload = r7.result_dict(self._fixture(0.5), result)
        self.assertEqual(tuple(sorted(result.domain_bounds)), tuple(sorted(r7.EXTERNAL_DOMAINS)))
        self.assertEqual(len(result.domain_bounds), 6)
        self.assertEqual(payload["correctionUseCount"], 0)
        self.assertEqual(payload["authoritativeControlCount"], 63)
        self.assertEqual(payload["authoritativeFaceCount"], 66)

    def test_semantic_payload_is_read_only_and_paws_pinned(self):
        for t in (0.0, 0.5, 1.0):
            fixture = self._fixture(t)
            before = canonical_bytes(fixture.payload)
            result = r7.build_surface(fixture)
            after = canonical_bytes(fixture.payload)
            self.assertEqual(before, after)
            self.assertLessEqual(result.paw_pin_error, 1e-9)

    def test_all_geometry_finite_and_bounds_truthful(self):
        for t in (0.0, 0.5, 1.0):
            fixture = self._fixture(t)
            result = r7.build_surface(fixture)
            payload = r7.result_dict(fixture, result)
            self.assertTrue(payload["finite"])
            for domain, rect in result.domain_bounds.items():
                points = [
                    point
                    for primitive in r7.all_primitives(result)
                    if primitive.domain == domain
                    for point in primitive.points
                ]
                self.assertTrue(points)
                for x, y in points:
                    self.assertLessEqual(rect[0] - 1e-9, x)
                    self.assertLessEqual(x, rect[2] + 1e-9)
                    self.assertLessEqual(rect[1] - 1e-9, y)
                    self.assertLessEqual(y, rect[3] + 1e-9)

    def test_source_has_no_view_or_post_evidence_specialization(self):
        source = Path(r7.__file__).read_text(encoding="utf-8")
        for token in (
            "PROFILE_BASE",
            "THREE_QUARTER_BASE",
            "FRONT_BASE",
            "MORPH_TARGET",
            "BLEND_SHAPE",
            "CORRECTION_CATALOG",
        ):
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
