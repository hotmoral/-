from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TARGET = HERE / "p1_c_dar1_diagnostic_axis_revision_v1.py"
spec = importlib.util.spec_from_file_location("dar1_under_test", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load DAR1 adapter")
dar1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dar1)


class DAR1DiagnosticAxisRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r12 = dar1.load_r12(HERE)
        cls.r11 = cls.r12.load_r11(HERE)

    def make_controls(self, frozen_tangent: bool = False, extra_degenerate: bool = False, extra_child: bool = False):
        positions = {}
        for i, role in enumerate(self.r11.ROLE_ORDER):
            positions[role] = np.asarray([0.25 + i * 0.13, 0.5 + i * 0.17, 0.75 + i * 0.19], dtype=np.float64)
        positions["TAIL_ROOT_CTRL"] = positions["PELVIS_CTRL"].copy()
        if frozen_tangent:
            positions["TAIL_1_CTRL"] = positions["TAIL_ROOT_CTRL"] + dar1.EXPECTED_TANGENT
        if extra_degenerate:
            positions["TAIL_2_CTRL"] = positions["TAIL_1_CTRL"].copy()

        out = []
        for role in self.r11.ROLE_ORDER:
            parent = self.r11.PARENT[role]
            if extra_child and role == "TAIL_2_CTRL":
                parent = "TAIL_ROOT_CTRL"
            out.append(self.r11.Control(
                role,
                parent,
                self.r11.ROLE_DOMAIN[role],
                tuple(map(float, positions[role])),
                self.r11.PROVENANCE[role],
                "DAR1_TEST",
            ))
        return out

    def test_axis_from_frozen_tangent_matches_contract_identity(self):
        axis = dar1.axis_from_tangent(dar1.EXPECTED_TANGENT)
        self.assertTrue(np.allclose(axis, dar1.EXPECTED_AXIS, rtol=0.0, atol=dar1.IDENTITY_ATOL))
        self.assertAlmostEqual(float(np.linalg.norm(dar1.EXPECTED_TANGENT)), dar1.EXPECTED_TANGENT_NORM, places=15)

    def test_activation_requires_exactly_one_known_degenerate_edge_and_single_direct_child(self):
        controls = self.make_controls(frozen_tangent=True)
        report = dar1.hierarchy_activation_audit(self.r11, dar1.controls_by_role(controls))
        self.assertEqual(report["edgeCount"], 29)
        self.assertEqual(report["degenerateEdgeCount"], 1)
        self.assertEqual(report["degenerateEdges"], [["PELVIS_CTRL", "TAIL_ROOT_CTRL"]])
        self.assertEqual(report["directChildren"], ["TAIL_1_CTRL"])
        self.assertTrue(np.allclose(report["selectedTangentR10"], dar1.EXPECTED_TANGENT, rtol=0.0, atol=dar1.IDENTITY_ATOL))

    def test_non_degenerate_roles_delegate_to_inherited_axis_exactly(self):
        controls = self.make_controls(frozen_tangent=True)
        by = dar1.controls_by_role(controls)
        for role in self.r11.ROLE_ORDER:
            if role == "TAIL_ROOT_CTRL":
                continue
            inherited = self.r11.diagnostic_axis(role, by)
            revised = dar1.diagnostic_axis_dar1(self.r11, self.r11.diagnostic_axis, role, by)
            self.assertTrue(np.array_equal(revised, inherited), role)

    def test_tail_root_only_becomes_defined_and_uses_direct_child_continuation(self):
        controls = self.make_controls(frozen_tangent=True)
        by = dar1.controls_by_role(controls)
        with self.assertRaisesRegex(RuntimeError, "zero diagnostic tangent"):
            self.r11.diagnostic_axis("TAIL_ROOT_CTRL", by)
        revised = dar1.diagnostic_axis_dar1(self.r11, self.r11.diagnostic_axis, "TAIL_ROOT_CTRL", by)
        self.assertTrue(np.allclose(revised, dar1.EXPECTED_AXIS, rtol=0.0, atol=dar1.IDENTITY_ATOL))

    def test_additional_degenerate_edge_stops_instead_of_searching_farther(self):
        controls = self.make_controls(frozen_tangent=True, extra_degenerate=True)
        by = dar1.controls_by_role(controls)
        with self.assertRaisesRegex(RuntimeError, "degenerate edge set drift"):
            dar1.diagnostic_axis_dar1(self.r11, self.r11.diagnostic_axis, "TAIL_ROOT_CTRL", by)

    def test_direct_child_identity_or_count_drift_stops(self):
        controls = self.make_controls(frozen_tangent=True, extra_child=True)
        by = dar1.controls_by_role(controls)
        with self.assertRaisesRegex(RuntimeError, "parent metadata drift|direct-child identity/count drift"):
            dar1.hierarchy_activation_audit(self.r11, by)

    def test_zero_direct_child_continuation_stops_without_second_fallback(self):
        controls = self.make_controls(frozen_tangent=True)
        by = dar1.controls_by_role(controls)
        root = by["TAIL_ROOT_CTRL"]
        tail1 = by["TAIL_1_CTRL"]
        controls2 = []
        for c in controls:
            if c.role == "TAIL_1_CTRL":
                controls2.append(self.r11.Control(
                    c.role, c.parent, c.domain, root.position, c.provenance, c.derivation
                ))
            else:
                controls2.append(c)
        by2 = dar1.controls_by_role(controls2)
        with self.assertRaisesRegex(RuntimeError, "degenerate edge set drift|direct-child continuation tangent is degenerate"):
            dar1.diagnostic_axis_dar1(self.r11, self.r11.diagnostic_axis, "TAIL_ROOT_CTRL", by2)

    def test_axis_isolation_audit_reports_only_tail_root_changed(self):
        controls = self.make_controls(frozen_tangent=True)
        report = dar1.axis_isolation_audit(self.r11, controls)
        self.assertEqual(report["changedDiagnosticAxisRoles"], ["TAIL_ROOT_CTRL"])
        self.assertEqual(report["changedDiagnosticAxisRoleCount"], 1)
        self.assertTrue(report["allNonTailRootAxesExactInherited"])
        self.assertTrue(report["selectedTangentMatchesFrozenIdentity"])
        self.assertTrue(report["selectedAxisMatchesFrozenIdentity"])


if __name__ == "__main__":
    unittest.main()
