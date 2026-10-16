from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TARGET = HERE / "p1_c_post_r12_tail_root_degeneracy_diagnostic_v1.py"
spec = importlib.util.spec_from_file_location("post_r12_diag_under_test", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load post-R12 diagnostic")
diag = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = diag
spec.loader.exec_module(diag)


class PostR12TailRootDiagnosticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r12 = diag.load_r12(HERE)
        cls.r11 = cls.r12.load_r11(HERE)

    def synthetic_controls(self, extra_zero_role: str | None = None):
        positions = {}
        for i, role in enumerate(self.r11.ROLE_ORDER):
            positions[role] = np.asarray(
                [float(i + 1), float((i % 5) + 1), float((i % 7) + 1)],
                dtype=np.float64,
            )
        positions["TAIL_ROOT_CTRL"] = positions["PELVIS_CTRL"].copy()
        if extra_zero_role is not None:
            parent = self.r11.PARENT[extra_zero_role]
            positions[extra_zero_role] = positions[parent].copy()
        return [
            self.r11.Control(
                role,
                self.r11.PARENT[role],
                self.r11.ROLE_DOMAIN[role],
                tuple(map(float, positions[role])),
                self.r11.PROVENANCE[role],
                "SYNTHETIC",
            )
            for role in self.r11.ROLE_ORDER
        ]

    def test_axis_from_tangent_matches_frozen_basis_convention(self):
        axis = diag.axis_from_tangent(np.asarray([1.0, 0.0, 0.0]))
        np.testing.assert_array_equal(axis, np.asarray([0.0, 0.0, 1.0]))
        with self.assertRaisesRegex(RuntimeError, "zero diagnostic tangent"):
            diag.axis_from_tangent(np.zeros(3))

    def test_hierarchy_audit_localizes_only_known_zero_edge(self):
        report = diag.hierarchy_edge_audit(
            self.r11, self.synthetic_controls(), 0.01, 1.0
        )
        self.assertEqual(report["edgeCount"], 29)
        self.assertTrue(report["knownPelvisTailRoot"]["exactTupleEqual"])
        self.assertTrue(report["knownPelvisTailRoot"]["diagnosticDegenerateLE1e15"])
        self.assertEqual(report["additionalDiagnosticDegenerateEdgeCount"], 0)

        report2 = diag.hierarchy_edge_audit(
            self.r11, self.synthetic_controls("TAIL_2_CTRL"), 0.01, 1.0
        )
        self.assertEqual(report2["additionalDiagnosticDegenerateEdgeCount"], 1)
        self.assertEqual(
            report2["additionalDiagnosticDegenerateEdges"][0]["role"],
            "TAIL_2_CTRL",
        )

    def test_weight_support_audit_distinguishes_coincident_role_support_sets(self):
        controls = self.synthetic_controls()
        by = {c.role: c for c in controls}
        self.assertEqual(by["PELVIS_CTRL"].position, by["TAIL_ROOT_CTRL"].position)
        vertices = np.asarray([
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [3.0, 0.0, 0.0],
            [4.0, 0.0, 0.0],
            [5.0, 0.0, 0.0],
            [6.0, 0.0, 0.0],
            [7.0, 0.0, 0.0],
        ], dtype=np.float64)
        indices = np.full((7, self.r11.MAX_INFLUENCES), 255, dtype=np.uint8)
        weights = np.zeros((7, self.r11.MAX_INFLUENCES), dtype=np.float64)
        roles = ("PELVIS_CTRL",) + diag.TAIL_ROLES
        for i, role in enumerate(roles):
            indices[i, 0] = self.r11.ROLE_INDEX[role]
            weights[i, 0] = 1.0
        domains = np.asarray(["CORE"] + ["TAIL"] * 6, dtype="U7")
        interfaces = np.zeros(7, dtype=bool)
        report = diag.weight_support_audit(
            self.r11, vertices, controls, indices, weights, domains, interfaces
        )
        self.assertEqual(
            report["roles"]["PELVIS_CTRL"]["positiveWeightSupportCount"], 1
        )
        self.assertEqual(
            report["roles"]["TAIL_ROOT_CTRL"]["positiveWeightSupportCount"], 1
        )
        self.assertTrue(
            report["roles"]["TAIL_ROOT_CTRL"]["supportDomainsMatchOwnRoleDomain"]
        )
        self.assertTrue(
            report["roles"]["TAIL_ROOT_CTRL"]["supportWeightEligibilityAllowed"]
        )
        self.assertTrue(
            report["pelvisVsTailRoot"]["domainRoleGatingProducesDistinctSupport"]
        )
        self.assertEqual(report["pelvisVsTailRoot"]["supportIntersectionCount"], 0)

    def test_tail_weighted_arc_reports_order_and_adjacent_overlap(self):
        n = 7
        indices = np.full((n, self.r11.MAX_INFLUENCES), 255, dtype=np.uint8)
        weights = np.zeros((n, self.r11.MAX_INFLUENCES), dtype=np.float64)
        for i, role in enumerate(diag.TAIL_ROLES):
            ridx = self.r11.ROLE_INDEX[role]
            for vertex in (i, i + 1):
                slot = int(np.count_nonzero(indices[vertex] != 255))
                indices[vertex, slot] = ridx
                weights[vertex, slot] = 1.0
        tail_frac = np.linspace(0.0, 1.0, n)
        report = diag.tail_weighted_arc_audit(
            self.r11, indices, weights, (np.zeros(n), tail_frac)
        )
        self.assertTrue(report["strictRootToTipCentroidOrdering"])
        self.assertTrue(report["allAdjacentPositiveSupportOverlap"])
        self.assertTrue(
            all(x["intersectionCount"] == 1 for x in report["adjacentSupportOverlapPairs"])
        )

    @staticmethod
    def positive_classification_inputs():
        hierarchy = {"additionalDiagnosticDegenerateEdgeCount": 0}
        graph = {"sameExactGraphNode": True, "sameExactWorldCoordinate": True}
        weights = {"roles": {"TAIL_ROOT_CTRL": {
            "positiveWeightSupportCount": 3,
            "supportDomainsMatchOwnRoleDomain": True,
            "supportWeightEligibilityAllowed": True,
        }}}
        arc = {
            "strictRootToTipCentroidOrdering": True,
            "allAdjacentPositiveSupportOverlap": True,
        }
        downstream = {"allDownstreamTailControlsPassFrozenDeadAndDomainGate": True}
        probes = {
            "anyDefinedProbeHasNonzeroAllowedDomainDifferentialSupport": True,
            "bothProbesDefined": True,
        }
        return hierarchy, graph, weights, arc, downstream, probes

    def test_classification_positive_case_is_narrow_nonvacuity_only(self):
        out = diag.classify_diagnostic(*self.positive_classification_inputs())
        self.assertEqual(
            out["primary"],
            "COINCIDENT_BRANCH_ROOT_WITH_NONVACUOUS_TAIL_SUPPORT",
        )
        self.assertIn("not R12 PASS", out["interpretationCeiling"])

    def test_classification_precedence_broader_zero_edge_wins(self):
        args = list(self.positive_classification_inputs())
        args[0] = {"additionalDiagnosticDegenerateEdgeCount": 1}
        args[2]["roles"]["TAIL_ROOT_CTRL"]["positiveWeightSupportCount"] = 0
        out = diag.classify_diagnostic(*args)
        self.assertEqual(
            out["primary"], "BROADER_ZERO_LENGTH_HIERARCHY_DEGENERACY"
        )

    def test_classification_tail_defect_and_unresolved_probe_cases(self):
        args = list(self.positive_classification_inputs())
        args[3] = {
            "strictRootToTipCentroidOrdering": False,
            "allAdjacentPositiveSupportOverlap": True,
        }
        out = diag.classify_diagnostic(*args)
        self.assertEqual(
            out["primary"], "COINCIDENT_BRANCH_ROOT_WITH_TAIL_SUPPORT_DEFECT"
        )

        args = list(self.positive_classification_inputs())
        args[5] = {
            "anyDefinedProbeHasNonzeroAllowedDomainDifferentialSupport": False,
            "bothProbesDefined": False,
        }
        out = diag.classify_diagnostic(*args)
        self.assertEqual(out["primary"], "MIXED_OR_UNRESOLVED")

    def test_contract_vocabulary_is_exact_and_two_probe_only(self):
        self.assertEqual(
            diag.COUNTERFACTUAL_PROBE_NAMES,
            ("TAIL_ROOT_TO_TAIL_1", "TAIL_PATH_FORWARD"),
        )
        self.assertEqual(len(diag.CLASSIFICATION_PRECEDENCE), 4)
        self.assertEqual(
            diag.CLASSIFICATION_PRECEDENCE[0],
            "BROADER_ZERO_LENGTH_HIERARCHY_DEGENERACY",
        )
        self.assertEqual(
            diag.CLASSIFICATION_PRECEDENCE[-1], "MIXED_OR_UNRESOLVED"
        )


if __name__ == "__main__":
    unittest.main()
