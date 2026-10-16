import importlib.util
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "audit", HERE / "p1_c_post_r10_pose_correspondence_audit_v1.py"
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class PoseCorrespondenceAuditTests(unittest.TestCase):
    def test_choose_body_uses_largest_triangle_primitive(self):
        records = [
            {"triangleCount": 10, "vertexCount": 12, "meshIndex": 0, "primitiveIndex": 0},
            {"triangleCount": 50, "vertexCount": 30, "meshIndex": 2, "primitiveIndex": 0},
            {"triangleCount": 20, "vertexCount": 25, "meshIndex": 1, "primitiveIndex": 0},
        ]
        self.assertIs(m._choose_body(records), records[1])

    def test_similarity_alignment_removes_rigid_scale_difference(self):
        source = np.array(
            [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float64
        )
        target = 2.5 * source + np.array([4.0, -3.0, 7.0])
        aligned, meta = m._similarity_align(source, target)
        self.assertTrue(np.allclose(aligned, target, atol=1e-12))
        self.assertAlmostEqual(meta["scale"], 2.5, places=12)
        self.assertAlmostEqual(meta["rotationDeterminant"], 1.0, places=12)

    def test_compare_pair_accepts_only_exact_index_sequence(self):
        positions = np.array(
            [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float64
        )
        base = {
            "vertexCount": 4,
            "triangleCount": 2,
            "indexCount": 6,
            "indexSha256": "same",
            "positions": positions,
        }
        same = dict(base)
        same["positions"] = positions.copy()
        r = m.compare_pair("a", base, "b", same)
        self.assertEqual(r["classification"], "EXACT_VERTEX_TOPOLOGY_CORRESPONDENCE")
        self.assertTrue(r["directVertexCorrespondenceAccepted"])

        diff = dict(base)
        diff["indexSha256"] = "different"
        r2 = m.compare_pair("a", base, "b", diff)
        self.assertEqual(r2["classification"], "COUNT_MATCH_BUT_CONNECTIVITY_DIFFERS")
        self.assertFalse(r2["directVertexCorrespondenceAccepted"])

    def test_count_mismatch_is_no_direct_correspondence(self):
        p = np.zeros((4, 3), dtype=np.float64)
        a = {
            "vertexCount": 4, "triangleCount": 2, "indexCount": 6,
            "indexSha256": "x", "positions": p,
        }
        b = {
            "vertexCount": 5, "triangleCount": 3, "indexCount": 9,
            "indexSha256": "y", "positions": np.zeros((5, 3), dtype=np.float64),
        }
        r = m.compare_pair("a", a, "b", b)
        self.assertEqual(r["classification"], "NO_DIRECT_CORRESPONDENCE")
        self.assertFalse(r["directVertexCorrespondenceAccepted"])


if __name__ == "__main__":
    unittest.main()
