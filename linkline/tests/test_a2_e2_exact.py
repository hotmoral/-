import ast
import json
from pathlib import Path
import unittest

from analysis.a2_e2_exact import E2_VERSION, build_e2_summary

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/a2_e2_exact_summary_v1.json"


def projected(summary):
    expected = json.loads(FIXTURE.read_text())
    columns = expected["columns"]
    rows = [[row[column] for column in columns] for row in summary["domains"]]
    return {
        "schemaVersion": summary["schemaVersion"],
        "columns": columns,
        "rows": rows,
        "boundaries": summary["boundaries"],
    }


class A2E2ExactDomains(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.expected = json.loads(FIXTURE.read_text())
        cls.summary = build_e2_summary()

    def test_exact_summary_matches_independent_fixture(self):
        self.assertEqual(projected(self.summary), self.expected)

    def test_domain_is_exactly_n2_n3_all_lengths(self):
        pairs = [(row["N"], row["L"]) for row in self.summary["domains"]]
        self.assertEqual(
            pairs,
            [(2, 2), (2, 3), (2, 4)] + [(3, length) for length in range(2, 10)],
        )
        self.assertEqual(sum(row["canonicalStates"] for row in self.summary["domains"] if row["N"] == 2), 12)
        self.assertEqual(sum(row["canonicalStates"] for row in self.summary["domains"] if row["N"] == 3), 322)

    def test_h2_rejection_identity_is_separate_from_strong_common_accepted_boundary(self):
        h2 = self.summary["boundaries"]["H2"]
        self.assertEqual(
            h2["firstCt1Collision"],
            {"N": 3, "L": 9, "kind": "REJECTED_ACTION_IDENTITY"},
        )
        self.assertFalse(h2["commonAcceptedCollisionInE2"])
        self.assertTrue(
            all(row["r2CommonAcceptedCollisionPairs"] == 0 for row in self.summary["domains"])
        )

    def test_h3s_and_h4_small_domain_boundary(self):
        self.assertEqual(
            self.summary["boundaries"]["H3-S"]["firstRestrictedFailure"],
            {"N": 3, "L": 4},
        )
        self.assertEqual(self.summary["boundaries"]["H3-S"]["e2FailureCount"], 508)
        self.assertEqual(self.summary["boundaries"]["H4"]["restrictedFailuresInE2"], 0)

    def test_h7_h8_and_ct6_are_structural_not_difficulty_scores(self):
        self.assertEqual(
            self.summary["boundaries"]["H7"]["firstBranchPair"],
            {"N": 3, "L": 2, "successorHorizon": 1},
        )
        self.assertEqual(
            self.summary["boundaries"]["H8"]["firstOptimizationInstance"],
            {"N": 3, "L": 2},
        )
        self.assertGreater(
            sum(row["ct6MultipleShortestPathInstances"] for row in self.summary["domains"]),
            0,
        )

    def test_runner_has_no_fixture_or_test_dependency(self):
        source = (ROOT / "analysis/a2_e2_exact.py").read_text()
        tree = ast.parse(source)
        imports = []
        strings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                strings.append(node.value)
        self.assertFalse(any(name.startswith("tests") for name in imports))
        self.assertFalse(any("a2_e2_exact_summary" in value for value in strings))
        self.assertEqual(E2_VERSION, "1.0.0")


if __name__ == "__main__":
    unittest.main()
