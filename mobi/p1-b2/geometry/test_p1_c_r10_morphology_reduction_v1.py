import importlib.util
import unittest
from pathlib import Path

import numpy as np
import fast_simplification

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "r10", HERE / "p1_c_r10_morphology_reduction_v1.py"
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class R10ReductionTests(unittest.TestCase):
    def test_closed_genus0_face_relation(self):
        self.assertEqual(m.target_faces_for_closed_genus0(4), 4)
        self.assertEqual(m.target_faces_for_closed_genus0(780), 1556)
        with self.assertRaises(ValueError):
            m.target_faces_for_closed_genus0(3)

    def test_tetrahedron_topology(self):
        faces = np.array(
            [(0, 2, 1), (0, 1, 3), (1, 2, 3), (2, 0, 3)], dtype=np.int32
        )
        r = m.topology_metrics(4, faces)
        self.assertTrue(r["closedOrientedTwoManifold"])
        self.assertEqual(r["connectedComponents"], 1)
        self.assertEqual(r["boundaryEdgeCount"], 0)
        self.assertEqual(r["nonManifoldEdgeCount"], 0)
        self.assertEqual(r["eulerCharacteristic"], 2)

    def test_geometry_metrics_tetrahedron(self):
        points = np.array(
            [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float64
        )
        faces = np.array(
            [(0, 2, 1), (0, 1, 3), (1, 2, 3), (2, 0, 3)], dtype=np.int32
        )
        r = m.geometry_metrics(points, faces)
        self.assertGreater(r["surfaceArea"], 0)
        self.assertAlmostEqual(r["absVolume"], 1.0 / 6.0, places=12)
        self.assertEqual(r["zeroAreaTriangleCount"], 0)

    def test_mask_iou(self):
        a = bytearray([1, 1, 0, 0])
        b = bytearray([1, 0, 1, 0])
        iou, diff, union = m.mask_iou(a, b)
        self.assertEqual(diff, 2)
        self.assertEqual(union, 3)
        self.assertAlmostEqual(iou, 1 / 3)

    def test_fast_simplification_replay_path(self):
        # Closed octahedron: enough triangles to exercise simplify + replay without external files.
        points = np.array(
            [
                [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]
            ],
            dtype=np.float64,
        )
        faces = np.array(
            [
                [0, 2, 4], [2, 1, 4], [1, 3, 4], [3, 0, 4],
                [2, 0, 5], [1, 2, 5], [3, 1, 5], [0, 3, 5],
            ],
            dtype=np.int32,
        )
        p2, f2, collapses = fast_simplification.simplify(
            points, faces, target_count=6, agg=7.0, return_collapses=True
        )
        p3, f3, _ = fast_simplification.replay_simplification(
            points=points, triangles=faces, collapses=collapses
        )
        self.assertEqual(p2.shape, p3.shape)
        self.assertEqual(f2.shape, f3.shape)
        self.assertTrue(np.allclose(p2, p3))
        self.assertTrue(np.array_equal(f2, f3))


if __name__ == "__main__":
    unittest.main()
