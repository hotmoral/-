import inspect
import json
from pathlib import Path
import unittest

from tests.oracles import a3_structural_feature_oracle as oracle


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "a3_structural_feature_golden_v1.json"
EXPECTED_FINGERPRINT = "9c2f51f76a5e604cc1d8134496eb40208caf88ba7ae1a121467208305318abc0"


class A3StructuralFeatureOracleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.by_id = {case["id"]: case for case in cls.fixture["cases"]}

    def test_fixture_contract_and_fingerprint(self):
        self.assertEqual(self.fixture["schema"], "A3_STRUCTURAL_FEATURE_GOLDEN")
        self.assertEqual(self.fixture["version"], "1.0.0")
        self.assertEqual(self.fixture["featureSchemaVersion"], "0.1")
        self.assertEqual(
            [case["id"] for case in self.fixture["cases"]],
            ["A3G01", "A3G02", "A3G03", "A3G04", "A3G05", "A3G06"],
        )
        self.assertEqual(oracle.normalized_fingerprint(self.fixture), EXPECTED_FINGERPRINT)

    def test_independent_oracle_matches_frozen_fixture(self):
        for case in self.fixture["cases"]:
            with self.subTest(case=case["id"]):
                computed = oracle.case_payload(case)
                self.assertEqual(computed, case)

    def test_orientation_pair_is_identical(self):
        first = self.by_id["A3G02"]
        reversed_case = self.by_id["A3G06"]
        self.assertEqual(first["expected"], reversed_case["expected"])
        self.assertEqual(
            oracle.feature_values(
                first["n"], first["length"], first["initial"], first["targets"]
            ),
            oracle.feature_values(
                reversed_case["n"],
                reversed_case["length"],
                reversed_case["initial"],
                reversed_case["targets"],
            ),
        )

    def test_metric_edge_cases(self):
        detour = self.by_id["A3G03"]["expected"]
        self.assertGreater(detour["shortestMinProximityUpSteps"], 0)
        self.assertGreater(detour["shortestMinProximityUpMagnitude"], 0)

        switching = self.by_id["A3G04"]["expected"]
        self.assertEqual(switching["shortestMinRelationalSideSwitches"], 2)

        no_regret = self.by_id["A3G05"]["expected"]
        self.assertEqual(no_regret["initialPositiveRegretActionCount"], 0)
        self.assertEqual(no_regret["initialMeanRegret"], {"numerator": 0, "denominator": 1})
        self.assertEqual(no_regret["initialMaxRegret"], 0)

    def test_known_a2_structural_relations_are_preserved(self):
        setup = self.by_id["A3G02"]["expected"]
        self.assertEqual(setup["shortestDistance"], 2)
        self.assertEqual(setup["shortestActionSequenceCount"], 2)
        self.assertEqual(setup["mandatoryInternalStateCount"], 1)

        side_switch = self.by_id["A3G04"]["expected"]
        self.assertEqual(side_switch["shortestDistance"], 10)
        self.assertGreater(side_switch["shortestMinRelationalSideSwitches"], 0)

    def test_oracle_has_no_production_a3_dependency(self):
        source = inspect.getsource(oracle)
        self.assertNotIn("analysis.a3_structural_features", source)
        self.assertNotIn("a3_structural_feature_golden_v1", source)
        self.assertEqual(oracle.ORACLE_VERSION, "1.0.0")
        self.assertEqual(oracle.FEATURE_SCHEMA_VERSION, "0.1")


if __name__ == "__main__":
    unittest.main()
