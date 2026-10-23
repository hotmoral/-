import inspect
import json
from pathlib import Path
import unittest

from analysis import a3_structural_features as production


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "a3_structural_feature_golden_v1.json"


class A3StructuralFeaturesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.by_id = {case["id"]: case for case in cls.fixture["cases"]}

    def test_version_and_golden_independence(self):
        self.assertEqual(production.ANALYZER_VERSION, "1.0.0")
        self.assertEqual(production.FEATURE_SCHEMA_VERSION, "0.1")
        self.assertEqual(production.MECHANIC_BASELINE, "a2-v1.0.0")

        source = inspect.getsource(production)
        self.assertNotIn("tests.", source)
        self.assertNotIn("a3_structural_feature_golden_v1", source)
        for case_id in self.by_id:
            self.assertNotIn(case_id, source)

    def test_all_golden_feature_values_match(self):
        for case in self.fixture["cases"]:
            with self.subTest(case=case["id"]):
                actual = production.exact_feature_values(
                    case["n"],
                    case["length"],
                    case["initial"],
                    case["targets"],
                )
                self.assertEqual(actual, case["expected"])

    def test_profile_schema_and_exact_statuses(self):
        case = self.by_id["A3G03"]
        profile = production.analyze_structural_features(
            case["n"], case["length"], case["initial"], case["targets"]
        )
        self.assertEqual(profile["mechanicBaseline"], "a2-v1.0.0")
        self.assertEqual(profile["featureSchemaVersion"], "0.1")
        self.assertEqual(profile["analyzerVersion"], "1.0.0")
        self.assertEqual(profile["domainStatus"], "IN_DOMAIN")
        self.assertEqual(list(profile["features"]), list(production.FEATURE_NAMES))
        for name in production.FEATURE_NAMES:
            self.assertEqual(profile["features"][name]["status"], production.EXACT)
            self.assertEqual(profile["features"][name]["value"], case["expected"][name])

    def test_orientation_canonicalization_is_feature_and_identity_stable(self):
        first = self.by_id["A3G02"]
        reverse = self.by_id["A3G06"]
        profile_a = production.analyze_structural_features(
            first["n"], first["length"], first["initial"], first["targets"]
        )
        profile_b = production.analyze_structural_features(
            reverse["n"], reverse["length"], reverse["initial"], reverse["targets"]
        )
        self.assertEqual(profile_a["canonicalInitial"], profile_b["canonicalInitial"])
        self.assertEqual(profile_a["targets"], profile_b["targets"])
        self.assertEqual(profile_a["puzzleFingerprint"], profile_b["puzzleFingerprint"])
        self.assertEqual(profile_a["features"], profile_b["features"])

    def test_cap_fails_closed_only_for_graph_dependent_features(self):
        case = self.by_id["A3G04"]
        profile = production.analyze_structural_features(
            case["n"],
            case["length"],
            case["initial"],
            case["targets"],
            state_cap=2,
        )
        self.assertEqual(profile["domainStatus"], "IN_DOMAIN")

        exact_names = {
            "shortestDistance",
            "initialLegalActionCount",
            "initialShortestActionCount",
            "initialPositiveRegretActionCount",
            "initialMeanRegret",
            "initialMaxRegret",
        }
        incomplete_names = set(production.FEATURE_NAMES) - exact_names
        for name in exact_names:
            self.assertEqual(profile["features"][name]["status"], production.EXACT)
            self.assertEqual(profile["features"][name]["value"], case["expected"][name])
        for name in incomplete_names:
            self.assertEqual(profile["features"][name], {"status": production.INCOMPLETE})

        with self.assertRaises(RuntimeError):
            production.exact_feature_values(
                case["n"],
                case["length"],
                case["initial"],
                case["targets"],
                state_cap=2,
            )

    def test_outside_domain_solved_and_unsolvable(self):
        solved = production.analyze_structural_features(2, 2, [0, 1], [0, 1])
        self.assertEqual(solved["domainStatus"], production.OUTSIDE)
        for row in solved["features"].values():
            self.assertEqual(row["status"], production.OUTSIDE)
            self.assertIsNone(row["value"])

        # Full-board chain, unsolved targets, no empty cell and therefore no move.
        unsolvable = production.analyze_structural_features(
            2, 4, [0, 1, 3, 2], [0, 1]
        )
        self.assertEqual(unsolvable["domainStatus"], production.OUTSIDE)
        for row in unsolvable["features"].values():
            self.assertEqual(row["status"], production.OUTSIDE)
            self.assertIsNone(row["value"])

        with self.assertRaises(ValueError):
            production.exact_feature_values(2, 2, [0, 1], [0, 1])

    def test_regret_identities_and_action_multiplicity(self):
        for case in self.fixture["cases"]:
            values = production.exact_feature_values(
                case["n"], case["length"], case["initial"], case["targets"]
            )
            self.assertEqual(
                values["initialPositiveRegretActionCount"],
                values["initialLegalActionCount"] - values["initialShortestActionCount"],
            )

        all_optimal = production.exact_feature_values(2, 2, [0, 1], [2, 3])
        self.assertEqual(all_optimal["initialShortestActionCount"], 2)
        self.assertEqual(all_optimal["shortestActionSequenceCount"], 2)

    def test_profile_fingerprint_is_deterministic(self):
        case = self.by_id["A3G04"]
        first = production.analyze_structural_features(
            case["n"], case["length"], case["initial"], case["targets"]
        )
        second = production.analyze_structural_features(
            case["n"], case["length"], case["initial"], case["targets"]
        )
        self.assertEqual(first, second)
        self.assertEqual(
            production.normalized_profile_fingerprint(first),
            production.normalized_profile_fingerprint(second),
        )

    def test_invalid_state_cap_is_rejected(self):
        case = self.by_id["A3G01"]
        for invalid in (0, -1, 1.5, True, None):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    production.analyze_structural_features(
                        case["n"],
                        case["length"],
                        case["initial"],
                        case["targets"],
                        state_cap=invalid,
                    )


if __name__ == "__main__":
    unittest.main()
