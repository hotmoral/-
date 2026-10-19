import ast
import json
from pathlib import Path
import unittest

from analysis.a2_cognitive import (
    ANALYZER_VERSION,
    ct1_transition,
    ct2_project_sequence,
    ct3_nonincreasing_proximity,
    ct3_relational_one_side,
    ct4_continuation_observation,
    ct4_footprint_reachable,
    ct5_shortest_dag_summary,
    ct6_solution_space_summary,
    exact_future,
    exact_goal_distance,
    representation_key,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/a2_cognitive_golden_v1.json"


class A2CognitiveAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.cases = {case["id"]: case for case in cls.fixture["cases"]}

    def test_version_and_golden_independence(self):
        self.assertEqual(ANALYZER_VERSION, "1.0.0")
        source = (ROOT / "analysis/a2_cognitive.py").read_text()
        modules = []
        strings = []
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                modules.append(node.module or "")
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                strings.append(node.value)
        self.assertFalse(any(module.startswith("tests") for module in modules))
        self.assertFalse(any("a2_cognitive_golden" in value for value in strings))
        self.assertFalse(any("A2G0" in value for value in strings))

    def test_r1_r2_ct1_collisions_match_frozen_golden(self):
        g1 = self.cases["A2G01"]
        keys = [representation_key("R1", 2, 3, state) for state in g1["states"]]
        self.assertEqual(keys[0], keys[1])
        self.assertEqual(
            [ct1_transition(2, 3, state, g1["action"]) for state in g1["states"]],
            g1["exactResults"],
        )

        g2 = self.cases["A2G02"]
        keys = [representation_key("R2", 4, 9, state) for state in g2["states"]]
        self.assertEqual(keys[0], keys[1])
        self.assertEqual(
            [ct1_transition(4, 9, state, g2["action"]) for state in g2["states"]],
            g2["exactResults"],
        )
        self.assertNotEqual(g2["exactResults"][0]["nextState"], g2["exactResults"][1]["nextState"])

    def test_proximity_descriptor_and_restricted_strategy_match_golden(self):
        g3 = self.cases["A2G03"]
        observed = [
            ct4_continuation_observation(3, 3, g3["initial"], g3["targets"], item["action"])
            for item in g3["alternatives"]
        ]
        self.assertEqual([row["proximity"] for row in observed], [2, 2])
        self.assertEqual(
            [row["exactGoalDistance"] for row in observed],
            [item["exactGoalDistance"] for item in g3["alternatives"]],
        )

        g4 = self.cases["A2G04"]
        restricted = ct3_nonincreasing_proximity(3, 4, g4["initial"], g4["targets"])
        self.assertTrue(restricted["unrestrictedSolutionExists"])
        self.assertEqual(restricted["unrestrictedShortestDistance"], g4["unrestrictedShortestDistance"])
        self.assertTrue(restricted["restrictedComplete"])
        self.assertEqual(restricted["restrictedReachableStateCount"], g4["restrictedReachableStateCount"])
        self.assertEqual(restricted["restrictedSolutionExists"], g4["restrictedSolutionExists"])

    def test_relational_one_side_is_not_persistent_identity(self):
        g5 = self.cases["A2G05"]
        restricted = ct3_relational_one_side(4, 10, g5["initial"], g5["targets"])
        self.assertTrue(restricted["unrestrictedSolutionExists"])
        self.assertEqual(restricted["unrestrictedShortestDistance"], g5["unrestrictedShortestDistance"])
        self.assertTrue(restricted["restrictedComplete"])
        self.assertEqual(restricted["restrictedReachableContextCount"], g5["restrictedReachableContextCount"])
        self.assertEqual(restricted["restrictedSolutionExists"], g5["restrictedSolutionExists"])
        with self.assertRaises(ValueError):
            representation_key("R5", 4, 10, g5["initial"], g5["targets"])

    def test_current_state_sequence_recovery_and_future_space(self):
        g6 = self.cases["A2G06"]
        projection = ct2_project_sequence(3, 3, g6["state"], g6["histories"][1])
        self.assertTrue(projection["complete"])
        self.assertEqual(projection["finalState"], g6["convergedState"])
        future = exact_future(3, 3, g6["convergedState"])
        self.assertEqual([row["action"] for row in future], g6["futureLegalActions"])
        self.assertEqual(future, g6["futureNextStates"])

        g7 = self.cases["A2G07"]
        self.assertEqual(exact_goal_distance(3, 2, g7["initial"], g7["targets"]), g7["initialExactGoalDistance"])
        detour = ct1_transition(3, 2, g7["initial"], g7["detourAction"])
        self.assertTrue(detour["accepted"])
        self.assertEqual(detour["nextState"], g7["detourState"])
        self.assertEqual(exact_goal_distance(3, 2, detour["nextState"], g7["targets"]), g7["detourExactGoalDistance"])
        recovered = ct1_transition(3, 2, detour["nextState"], g7["forcedRecoveryAction"])
        self.assertEqual(recovered["nextState"], g7["recoveredState"])

        g8 = self.cases["A2G08"]
        self.assertEqual(
            [ct4_footprint_reachable(3, 2, state, g8["footprint"], g8["horizon"]) for state in g8["successors"]],
            g8["reachable"],
        )

    def test_ct5_shortest_structure_matches_optimization_only_golden(self):
        g9 = self.cases["A2G09"]
        summary = ct5_shortest_dag_summary(3, 3, g9["initial"], g9["targets"])
        self.assertTrue(summary["complete"])
        self.assertTrue(summary["solvable"])
        self.assertEqual(summary["shortestDistance"], g9["shortestDistance"])
        self.assertEqual(summary["shortestPathCount"], g9["shortestPathCount"])
        self.assertIn(g9["mandatoryInternalState"], summary["mandatoryInternalStates"])
        ct6 = ct6_solution_space_summary(3, 3, g9["initial"], g9["targets"])
        self.assertTrue(ct6["complete"])
        self.assertEqual(ct6["shortestPathCount"], g9["shortestPathCount"])
        self.assertIn(g9["mandatoryInternalState"], ct6["mandatoryInternalStates"])
        observed = [
            ct4_continuation_observation(3, 3, g9["initial"], g9["targets"], item["action"])
            for item in g9["alternatives"]
        ]
        self.assertEqual([row["proximity"] for row in observed], [2, 2])
        self.assertEqual(
            [row["exactGoalDistance"] for row in observed],
            [item["exactGoalDistance"] for item in g9["alternatives"]],
        )
        self.assertEqual(
            [row["onShortestDag"] for row in observed],
            [item["onShortestDag"] for item in g9["alternatives"]],
        )

    def test_fail_closed_guards_and_invalid_sequence(self):
        g4 = self.cases["A2G04"]
        capped = ct3_nonincreasing_proximity(3, 4, g4["initial"], g4["targets"], state_cap=1)
        self.assertFalse(capped["restrictedComplete"])
        self.assertIsNone(capped["restrictedSolutionExists"])

        g5 = self.cases["A2G05"]
        capped = ct3_relational_one_side(4, 10, g5["initial"], g5["targets"], context_cap=1)
        self.assertFalse(capped["restrictedComplete"])
        self.assertIsNone(capped["restrictedSolutionExists"])

        g9 = self.cases["A2G09"]
        self.assertEqual(
            ct5_shortest_dag_summary(3, 3, g9["initial"], g9["targets"], state_cap=1),
            {"complete": False},
        )

        projection = ct2_project_sequence(3, 3, [0, 1, 2], [[0, 3], [0, 4]])
        self.assertFalse(projection["complete"])
        self.assertEqual(projection["invalidStep"], 1)
        self.assertEqual(projection["finalState"], [1, 0, 3])


if __name__ == "__main__":
    unittest.main()
