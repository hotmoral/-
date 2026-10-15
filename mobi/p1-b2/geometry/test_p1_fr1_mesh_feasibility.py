from __future__ import annotations

import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from e_v0_fixture_adapter import H1, H4, H6N, build_e_fixture
from e_v0_profiles import M0, MORPHOLOGIES
from p1_fr1_mesh_probe_v3 import (
    CORE_VERTEX_IDS,
    PROBE_VERSION,
    build_probe,
    canonical_view_weights,
    topology_signature,
)
from run_p1_fr1_mesh_feasibility import generate_debug_svgs, run_matrix


class P1FR1MeshFeasibilityTests(unittest.TestCase):
    def test_view_weights_are_bounded_partition_of_unity(self):
        from math import pi

        samples = (-pi / 2, -pi / 4, 0.0, pi / 4, pi / 2)
        expected_dominant = ("FRONT", "THREE_QUARTER", "PROFILE", "THREE_QUARTER", "FRONT")
        for yaw, dominant in zip(samples, expected_dominant):
            weights = canonical_view_weights(yaw)
            self.assertEqual({"PROFILE", "THREE_QUARTER", "FRONT"}, set(weights))
            self.assertAlmostEqual(1.0, sum(weights.values()), places=12)
            self.assertTrue(all(0.0 <= value <= 1.0 for value in weights.values()))
            self.assertAlmostEqual(1.0, weights[dominant], places=12)

    def test_representative_fixtures_preserve_semantics_paws_and_topology(self):
        expected_topology = topology_signature()
        for morphology in MORPHOLOGIES:
            for case_id, t in ((H1, 0.0), (H4, 0.5)):
                fixture = build_e_fixture(morphology, case_id, 80, t, +1)
                result = build_probe(fixture, +1)
                self.assertIn("DIRECTION_CONVENTION", PROBE_VERSION)
                self.assertEqual(expected_topology, result.topology_signature)
                self.assertEqual(result.semantic_anchor_hash_before, result.semantic_anchor_hash_after)
                self.assertLessEqual(result.paw_pin_error_max, 1e-9)
                self.assertEqual(0, result.core_self_intersections)
                self.assertEqual((), result.correction_families)
                self.assertEqual(CORE_VERTEX_IDS, tuple(item[0] for item in result.core_vertices))

    def test_h6n_near_front_depths_preserve_anatomical_identity_under_direction_mirror(self):
        positive = build_probe(build_e_fixture(M0, H6N, 80, 0.75, +1), +1)
        negative = build_probe(build_e_fixture(M0, H6N, 80, 0.75, -1), -1)

        def depths(result, kind):
            return {
                mesh["side"]: mesh["viewDepth"]
                for mesh in result.limb_meshes
                if mesh["kind"] == kind
            }

        for kind in ("FORE", "HIND"):
            pos = depths(positive, kind)
            neg = depths(negative, kind)
            self.assertEqual({"L", "R"}, set(pos))
            self.assertEqual({"L", "R"}, set(neg))
            self.assertGreater(abs(pos["L"] - pos["R"]), 1e-6)
            self.assertGreater(abs(neg["L"] - neg["R"]), 1e-6)
            # Accepted H6N mirror semantics swap the corresponding mirrored paw
            # role while yaw sign reverses view depth. Anatomical IDs themselves
            # remain L/R; no semantic identity swap is performed by the renderer.
            self.assertAlmostEqual(pos["L"], -neg["R"], places=12)
            self.assertAlmostEqual(pos["R"], -neg["L"], places=12)

    def test_exact_front_lateral_depth_tie_is_valid(self):
        for direction in (+1, -1):
            result = build_probe(build_e_fixture(M0, H6N, 80, 1.0, direction), direction)
            for kind in ("FORE", "HIND"):
                values = {
                    mesh["side"]: mesh["viewDepth"]
                    for mesh in result.limb_meshes
                    if mesh["kind"] == kind
                }
                self.assertAlmostEqual(values["L"], values["R"], places=12)

    def test_full_matrix_passes_one_topology_no_mutation_no_self_intersection(self):
        records, summary = run_matrix()
        self.assertTrue(summary["pass"], summary)
        self.assertEqual(1770, summary["recordCount"])
        self.assertEqual(1, summary["topologySignatureCount"])
        self.assertEqual(0, summary["semanticMutationCount"])
        self.assertLessEqual(summary["maxPawPinError"], 1e-9)
        self.assertEqual(0, summary["coreSelfIntersectionCount"])
        self.assertEqual(0, summary["correctionUseCount"])
        self.assertEqual([6], summary["meshDomainCounts"])
        self.assertEqual(1770, len(records))

    def test_debug_svg_generation_is_deterministic_and_xml_valid(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            left = generate_debug_svgs(Path(a))
            right = generate_debug_svgs(Path(b))
            self.assertEqual([p.name for p in left], [p.name for p in right])
            self.assertEqual(3, len(left))
            for lp, rp in zip(left, right):
                self.assertEqual(lp.read_bytes(), rp.read_bytes())
                ET.parse(lp)


if __name__ == "__main__":
    unittest.main()
