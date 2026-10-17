from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TARGET = HERE / "p1_c_fpd2_tail_branch_yaw_v1.py"
spec = importlib.util.spec_from_file_location("fpd2_tail_branch_under_test", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load FPD2 tail-branch evaluator")
fpd2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fpd2)

ROLE_ORDER = (
    "BODY_ROOT_CTRL", "PELVIS_CTRL", "LUMBAR_CTRL", "FOREQUARTER_CTRL", "NECK_BASE_CTRL", "HEAD_CTRL",
    "FORE_L_SCAPULAR_CTRL", "FORE_L_PROXIMAL_CTRL", "FORE_L_MID_CTRL", "FORE_L_DISTAL_CTRL", "FORE_L_PAW_CTRL",
    "FORE_R_SCAPULAR_CTRL", "FORE_R_PROXIMAL_CTRL", "FORE_R_MID_CTRL", "FORE_R_DISTAL_CTRL", "FORE_R_PAW_CTRL",
    "HIND_L_PROXIMAL_CTRL", "HIND_L_MID_CTRL", "HIND_L_DISTAL_CTRL", "HIND_L_PAW_CTRL",
    "HIND_R_PROXIMAL_CTRL", "HIND_R_MID_CTRL", "HIND_R_DISTAL_CTRL", "HIND_R_PAW_CTRL",
    "TAIL_ROOT_CTRL", "TAIL_1_CTRL", "TAIL_2_CTRL", "TAIL_3_CTRL", "TAIL_4_CTRL", "TAIL_TIP_CTRL",
)


class FPD2TailBranchYawTests(unittest.TestCase):
    def test_contract_identity_exact(self):
        self.assertEqual(fpd2.VERSION, "P1_C_FPD2_TAIL_BRANCH_YAW_V1")
        self.assertEqual(fpd2.DECISION_TOKEN, "P1_C_POST_FPD1_TAIL_BRANCH_YAW_SELECTED")
        self.assertEqual(fpd2.CONTRACT_TOKEN, "P1_C_FPD2_TAIL_BRANCH_YAW_CONTRACT_FROZEN")
        self.assertEqual(fpd2.PREFLIGHT_TOKEN, "P1_C_FPD2_TAIL_BRANCH_YAW_PREFLIGHT_PASS")
        self.assertEqual(fpd2.POSE_ID, "FPD2_TAIL_ROOT_PIVOT_FULL_TAIL_YAW_RIGHT_8DEG")

    def test_pose_definition_exact(self):
        pose = fpd2.validate_pose_contract(ROLE_ORDER)
        self.assertEqual(pose["pivotRole"], "TAIL_ROOT_CTRL")
        self.assertEqual(pose["selectedRoles"], list(fpd2.SELECTED_ROLES))
        self.assertEqual(pose["identityRoleCount"], 24)
        self.assertEqual(pose["angleDeg"], 8.0)
        self.assertEqual(pose["angleRad"], 0.13962634015954636)
        self.assertEqual(pose["axisR10"], [0.0, 1.0, 0.0])
        self.assertEqual(pose["bodyRootTranslationR10"], [0.0, 0.0, 0.0])
        self.assertFalse(pose["ikApplied"])
        self.assertFalse(pose["rootCompensationApplied"])

    def test_selected_roles_are_exact_full_tail_branch(self):
        self.assertEqual(
            fpd2.SELECTED_ROLES,
            (
                "TAIL_ROOT_CTRL", "TAIL_1_CTRL", "TAIL_2_CTRL",
                "TAIL_3_CTRL", "TAIL_4_CTRL", "TAIL_TIP_CTRL",
            ),
        )
        self.assertEqual(tuple(r for r in ROLE_ORDER if r in fpd2.SELECTED_ROLES), fpd2.SELECTED_ROLES)

    def test_reference_controls_reproduce_frozen_transform(self):
        pivot = fpd2.EXPECTED_COORDS[fpd2.PIVOT_ROLE]
        for role in fpd2.SELECTED_ROLES:
            actual = fpd2.rigid_transform(fpd2.EXPECTED_COORDS[role][None, :], pivot)[0]
            self.assertTrue(np.allclose(actual, fpd2.EXPECTED_TRANSFORMED_REFERENCE[role], rtol=0.0, atol=1e-15), role)
            disp = float(np.linalg.norm(actual - fpd2.EXPECTED_COORDS[role]))
            self.assertAlmostEqual(disp, fpd2.EXPECTED_REFERENCE_DISPLACEMENT[role], places=15)

    def test_tail_root_on_pivot_is_exactly_stationary(self):
        pivot = fpd2.EXPECTED_COORDS[fpd2.PIVOT_ROLE]
        out = fpd2.rigid_transform(pivot[None, :], pivot)[0]
        self.assertTrue(np.array_equal(out, pivot))
        self.assertEqual(float(np.linalg.norm(out - pivot)), 0.0)

    def test_finite_evaluator_preserves_zero_selected_vertices_bit_exact(self):
        v = np.asarray([[0.1, 0.2, 0.3], [-0.4, 0.5, -0.6]], dtype=np.float64)
        indices = np.zeros((2, 4), dtype=np.uint8)
        weights = np.zeros((2, 4), dtype=np.float64)
        indices[:, 0] = 0
        weights[:, 0] = 1.0
        out = fpd2.finite_weighted_evaluate(v, indices, weights, ROLE_ORDER, fpd2.EXPECTED_COORDS[fpd2.PIVOT_ROLE])
        self.assertTrue(np.array_equal(out, v))
        self.assertEqual(out.tobytes(), v.tobytes())

    def test_finite_evaluator_matches_exact_selected_identity_blend(self):
        v = np.asarray([[0.2, 0.4, -0.3]], dtype=np.float64)
        indices = np.zeros((1, 4), dtype=np.uint8)
        weights = np.zeros((1, 4), dtype=np.float64)
        indices[0] = [24, 0, 1, 2]
        weights[0] = [0.25, 0.75, 0.0, 0.0]
        pivot = fpd2.EXPECTED_COORDS[fpd2.PIVOT_ROLE]
        rigid = fpd2.rigid_transform(v, pivot)
        expected = 0.75 * v + 0.25 * rigid
        out = fpd2.finite_weighted_evaluate(v, indices, weights, ROLE_ORDER, pivot)
        self.assertTrue(np.allclose(out, expected, rtol=0.0, atol=1e-15))

    def test_frozen_replay_adapter_identity(self):
        replay = fpd2.load_replay(HERE)
        self.assertEqual(replay.VERSION, fpd2.EXPECTED_REPLAY_VERSION)
        self.assertEqual(replay.CANONICAL_WEIGHTS_BYTES, 112532)
        self.assertEqual(replay.CANONICAL_SERIALIZED_SHA256, fpd2.CANONICAL_SERIALIZED_SHA256)
        self.assertEqual(replay.CANONICAL_INDICES_SHA256, fpd2.CANONICAL_INDICES_SHA256)
        self.assertEqual(replay.CANONICAL_WEIGHT_FLOATS_SHA256, fpd2.CANONICAL_WEIGHT_FLOATS_SHA256)

    def test_view_sets_remain_frozen_and_symmetric(self):
        self.assertEqual(fpd2.DIRECT_VIEWS, (-90.0, -67.5, -45.0, -22.5, 0.0, 22.5, 45.0, 67.5, 90.0))
        self.assertEqual(len(fpd2.DENSE_VIEWS), 73)
        self.assertEqual(fpd2.DENSE_VIEWS[0], -90.0)
        self.assertEqual(fpd2.DENSE_VIEWS[-1], 90.0)
        self.assertIn(0.0, fpd2.DENSE_VIEWS)


if __name__ == "__main__":
    unittest.main()
