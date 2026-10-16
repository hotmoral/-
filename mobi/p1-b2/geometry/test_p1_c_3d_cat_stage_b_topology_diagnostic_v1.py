import unittest, importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("diag", HERE/"p1_c_3d_cat_stage_b_topology_diagnostic_v1.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class TopologyTests(unittest.TestCase):
    def test_closed_tetrahedron(self):
        r=m.topology_metrics(4,[(0,2,1),(0,1,3),(1,2,3),(2,0,3)])
        self.assertTrue(r['closedTwoManifoldByIndexTopology'])
        self.assertEqual(r['boundaryEdgeCount'],0)
        self.assertEqual(r['nonManifoldEdgeCount'],0)
        self.assertEqual(r['orientationMismatchEdgeCount'],0)
        self.assertEqual(r['eulerCharacteristic'],2)
        self.assertEqual(r['genusIfConnectedClosedOrientable'],0)
    def test_open_quad_detected(self):
        r=m.topology_metrics(4,[(0,1,2),(0,2,3)])
        self.assertFalse(r['closedTwoManifoldByIndexTopology'])
        self.assertEqual(r['boundaryEdgeCount'],4)

if __name__=='__main__': unittest.main()
