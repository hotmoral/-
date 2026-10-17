from __future__ import annotations

import importlib.util
import math
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TARGET = HERE / "p1_c_fpd1_finite_pose_discriminator_v1.py"
spec = importlib.util.spec_from_file_location("fpd1_under_test", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load FPD1 implementation")
fpd1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fpd1)


class FPD1FinitePoseDiscriminatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dar1 = fpd1.load_dar1(HERE)
        cls.r12 = cls.dar1.load_r12(HERE)
        cls.r11 = cls.r12.load_r11(HERE)
        cls.role_order = tuple(cls.r11.ROLE_ORDER)
        cls.neck = int(cls.r11.ROLE_INDEX["NECK_BASE_CTRL"])
        cls.head = int(cls.r11.ROLE_INDEX["HEAD_CTRL"])
        cls.body = int(cls.r11.ROLE_INDEX["BODY_ROOT_CTRL"])

    def test_frozen_pose_contract_identity(self):
        p = fpd1.validate_pose_contract(self.role_order)
        self.assertEqual(p["poseId"], fpd1.POSE_ID)
        self.assertEqual(p["pivotRole"], "FOREQUARTER_CTRL")
        self.assertEqual(p["selectedRoles"], ["NECK_BASE_CTRL", "HEAD_CTRL"])
        self.assertEqual(p["identityRoleCount"], 28)
        self.assertEqual(p["axisR10"], [0.0, 1.0, 0.0])
        self.assertEqual(p["angleDeg"], 8.0)
        self.assertEqual(p["angleRad"], 0.13962634015954636)

    def test_positive_y_rotation_maps_forward_toward_anatomical_left(self):
        pivot = np.zeros(3, dtype=np.float64)
        forward = np.asarray([[0.0, 0.0, 1.0]], dtype=np.float64)
        q = fpd1.rigid_transform(forward, pivot)[0]
        self.assertGreater(float(q[0]), 0.0)
        self.assertGreater(float(q[2]), 0.0)
        self.assertAlmostEqual(float(np.linalg.norm(q)), 1.0, places=15)

    def test_frozen_reference_positions_match_contract(self):
        pivot = fpd1.EXPECTED_COORDS["FOREQUARTER_CTRL"]
        for role in fpd1.SELECTED_ROLES:
            got = fpd1.rigid_transform(fpd1.EXPECTED_COORDS[role][None, :], pivot)[0]
            self.assertTrue(np.allclose(got, fpd1.EXPECTED_TRANSFORMED_REFERENCE[role], rtol=0.0, atol=fpd1.IDENTITY_ATOL), role)
            disp = float(np.linalg.norm(got - fpd1.EXPECTED_COORDS[role]))
            self.assertTrue(math.isclose(disp, fpd1.EXPECTED_REFERENCE_DISPLACEMENT[role], rel_tol=0.0, abs_tol=fpd1.IDENTITY_ATOL), role)

    def test_zero_selected_weight_is_bit_exact_identity(self):
        v = np.asarray([[0.125, 0.5, 0.75], [-0.25, 0.2, 0.8]], dtype=np.float64)
        idx = np.asarray([[self.body, self.body, self.body, self.body], [self.body, self.body, self.body, self.body]], dtype=np.int64)
        w = np.asarray([[1.0, 0.0, 0.0, 0.0], [0.25, 0.25, 0.25, 0.25]], dtype=np.float64)
        out = fpd1.finite_weighted_evaluate(v, idx, w, self.role_order, np.zeros(3, dtype=np.float64))
        self.assertTrue(np.array_equal(out, v))
        self.assertEqual(out.tobytes(), v.tobytes())

    def test_full_selected_weight_equals_rigid_transform(self):
        v = np.asarray([[0.0, 0.0, 1.0], [0.2, 0.3, 0.7]], dtype=np.float64)
        idx = np.asarray([[self.neck, self.body, self.body, self.body], [self.head, self.body, self.body, self.body]], dtype=np.int64)
        w = np.asarray([[1.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0]], dtype=np.float64)
        pivot = np.asarray([0.1, 0.2, 0.3], dtype=np.float64)
        out = fpd1.finite_weighted_evaluate(v, idx, w, self.role_order, pivot)
        expected = fpd1.rigid_transform(v, pivot)
        self.assertTrue(np.allclose(out, expected, rtol=0.0, atol=1e-15))

    def test_mixed_selected_and_identity_weight_matches_literal_blend(self):
        v = np.asarray([[0.25, 0.4, 0.9]], dtype=np.float64)
        idx = np.asarray([[self.neck, self.body, self.head, self.body]], dtype=np.int64)
        w = np.asarray([[0.2, 0.3, 0.1, 0.4]], dtype=np.float64)
        pivot = np.asarray([0.0, 0.1, 0.2], dtype=np.float64)
        out = fpd1.finite_weighted_evaluate(v, idx, w, self.role_order, pivot)[0]
        rigid = fpd1.rigid_transform(v, pivot)[0]
        literal = (0.2 * rigid) + (0.3 * v[0]) + (0.1 * rigid) + (0.4 * v[0])
        self.assertTrue(np.allclose(out, literal, rtol=0.0, atol=1e-15))

    def test_weight_normalization_drift_stops(self):
        v = np.asarray([[0.0, 0.0, 1.0]], dtype=np.float64)
        idx = np.asarray([[self.neck, self.body, self.body, self.body]], dtype=np.int64)
        w = np.asarray([[0.5, 0.2, 0.2, 0.0]], dtype=np.float64)
        with self.assertRaisesRegex(RuntimeError, "weight normalization drift"):
            fpd1.finite_weighted_evaluate(v, idx, w, self.role_order, np.zeros(3, dtype=np.float64))

    def test_top4_shape_drift_stops(self):
        v = np.asarray([[0.0, 0.0, 1.0]], dtype=np.float64)
        idx = np.asarray([[self.neck, self.body, self.body]], dtype=np.int64)
        w = np.asarray([[1.0, 0.0, 0.0]], dtype=np.float64)
        with self.assertRaisesRegex(RuntimeError, "top-4 array shape drift"):
            fpd1.finite_weighted_evaluate(v, idx, w, self.role_order, np.zeros(3, dtype=np.float64))

    def test_view_contract_is_exactly_9_and_73(self):
        self.assertEqual(fpd1.DIRECT_VIEWS, (-90.0, -67.5, -45.0, -22.5, 0.0, 22.5, 45.0, 67.5, 90.0))
        self.assertEqual(len(fpd1.DIRECT_VIEWS), 9)
        self.assertEqual(len(fpd1.DENSE_VIEWS), 73)
        self.assertEqual(fpd1.DENSE_VIEWS[0], -90.0)
        self.assertEqual(fpd1.DENSE_VIEWS[-1], 90.0)
        self.assertEqual(fpd1.DENSE_VIEWS[36], 0.0)


if __name__ == "__main__":
    unittest.main()
