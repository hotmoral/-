import ast
import json
from pathlib import Path
import unittest

from tests.oracles.a2_cognitive_oracle import fingerprint, golden_payload

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/a2_cognitive_golden_v1.json"


class A2CognitiveGolden(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text())

    def test_fixture_matches_independent_oracle(self):
        actual = golden_payload()
        self.assertEqual(self.fixture, actual)
        self.assertEqual(
            fingerprint(actual),
            "198e1418691e29b8560c0b38270c69c8226034ae439fc6d66d6e02b866772d18",
        )

    def test_case_contract_and_vocabulary(self):
        allowed_status = {
            "EXACT_INFORMATION_SUFFICIENT",
            "EXACT_INFORMATION_INSUFFICIENT",
            "SUFFICIENT_IN_EXHAUSTIVE_DOMAIN",
            "NO_COLLISION_FOUND_IN_DOMAIN",
            "STRATEGY_RESTRICTION_FAILS",
            "STRUCTURALLY_RELEVANT",
            "NOT_REQUIRED_BY_CORE",
            "HUMAN_HYPOTHESIS_ONLY",
            "UNRESOLVED",
        }
        allowed_layers = {"L1", "L2", "L3"}
        allowed_tasks = {f"CT{i}" for i in range(1, 7)}
        ids = []
        for case in self.fixture["cases"]:
            ids.append(case["id"])
            self.assertIn(case["status"], allowed_status)
            self.assertIn(case["evidenceLayer"], allowed_layers)
            self.assertIn(case["task"], allowed_tasks)
            self.assertIn("scope", case)
        self.assertEqual(ids, [f"A2G{i:02d}" for i in range(1, 10)])

    def test_positive_representation_collisions_are_real(self):
        cases = {case["id"]: case for case in self.fixture["cases"]}
        g1 = cases["A2G01"]
        self.assertEqual(g1["reducedRepresentation"]["endpoints"], [0, 3])
        self.assertNotEqual(g1["exactResults"][0], g1["exactResults"][1])

        g2 = cases["A2G02"]
        self.assertEqual(g2["reducedRepresentation"]["endpoints"], [0, 10])
        self.assertEqual(
            sorted(g2["states"][0]),
            g2["reducedRepresentation"]["occupied"],
        )
        self.assertEqual(
            sorted(g2["states"][1]),
            g2["reducedRepresentation"]["occupied"],
        )
        self.assertNotEqual(
            g2["exactResults"][0]["nextState"],
            g2["exactResults"][1]["nextState"],
        )

        g3 = cases["A2G03"]
        self.assertEqual(
            [item["proximity"] for item in g3["alternatives"]],
            [2, 2],
        )
        self.assertEqual(
            [item["exactGoalDistance"] for item in g3["alternatives"]],
            [1, 3],
        )

    def test_strategy_counterexamples_are_exact(self):
        cases = {case["id"]: case for case in self.fixture["cases"]}

        g4 = cases["A2G04"]
        self.assertEqual(g4["unrestrictedShortestDistance"], 4)
        self.assertEqual(g4["restrictedReachableStateCount"], 15)
        self.assertFalse(g4["restrictedSolutionExists"])
        self.assertGreater(
            max(g4["witnessProximitySequence"]),
            g4["witnessProximitySequence"][0],
        )

        g5 = cases["A2G05"]
        self.assertEqual(g5["unrestrictedShortestDistance"], 10)
        self.assertEqual(g5["restrictedReachableContextCount"], 6)
        self.assertFalse(g5["restrictedSolutionExists"])
        self.assertIn(True, g5["switchFlagsAfterFirst"])

    def test_theorem_and_scope_guards(self):
        cases = {case["id"]: case for case in self.fixture["cases"]}
        self.assertEqual(cases["A2G06"]["status"], "NOT_REQUIRED_BY_CORE")
        self.assertEqual(cases["A2G06"]["scope"], "GLOBAL_THEOREM")
        self.assertEqual(cases["A2G07"]["status"], "NOT_REQUIRED_BY_CORE")
        self.assertEqual(cases["A2G07"]["scope"], "GLOBAL_THEOREM")
        self.assertEqual(cases["A2G08"]["reachable"], [False, True])

        g9 = cases["A2G09"]
        self.assertEqual(g9["scope"], "OPTIMIZATION_ONLY")
        self.assertEqual(g9["shortestDistance"], 2)
        self.assertEqual(g9["shortestPathCount"], 2)
        self.assertEqual(
            [item["proximity"] for item in g9["alternatives"]],
            [2, 2],
        )
        self.assertEqual(
            [item["onShortestDag"] for item in g9["alternatives"]],
            [True, False],
        )

    def test_no_production_analyzer_dependency(self):
        source = (ROOT / "tests/oracles/a2_cognitive_oracle.py").read_text()
        modules = []
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                modules.append(node.module or "")
        self.assertFalse(any(module.startswith("analysis") for module in modules))


if __name__ == "__main__":
    unittest.main()
