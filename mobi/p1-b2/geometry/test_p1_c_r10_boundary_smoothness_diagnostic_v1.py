import importlib.util
import math
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "diag", HERE / "p1_c_r10_boundary_smoothness_diagnostic_v1.py"
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class BoundarySmoothnessTests(unittest.TestCase):
    def test_refinement_target_is_contract_value(self):
        self.assertEqual(m.REFINEMENT_TARGET_VERTICES, 1088)
        self.assertAlmostEqual(math.sqrt(1560 * 780), 1103.0865786510142)

    def test_planar_quad_dihedral_zero(self):
        points = np.array(
            [[0,0,0],[1,0,0],[1,1,0],[0,1,0]], dtype=np.float64
        )
        faces = np.array([[0,1,2],[0,2,3]], dtype=np.int32)
        r = m.dihedral_metrics(points, faces)
        self.assertEqual(r['twoFaceEdgeCount'], 1)
        self.assertAlmostEqual(r['angleDegP50'], 0.0, places=12)
        self.assertAlmostEqual(r['angleDegMax'], 0.0, places=12)

    def test_tetrahedron_has_positive_dihedral(self):
        points = np.array(
            [[0,0,0],[1,0,0],[0,1,0],[0,0,1]], dtype=np.float64
        )
        faces = np.array(
            [(0,2,1),(0,1,3),(1,2,3),(2,0,3)], dtype=np.int32
        )
        r = m.dihedral_metrics(points, faces)
        self.assertEqual(r['twoFaceEdgeCount'], 6)
        self.assertGreater(r['angleDegP50'], 0.0)
        self.assertGreater(r['fractionAbove30_0Deg'], 0.0)


if __name__ == '__main__':
    unittest.main()
