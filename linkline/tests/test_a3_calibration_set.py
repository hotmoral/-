import hashlib
import inspect
import json
from fractions import Fraction
from pathlib import Path
import unittest

from analysis import a3_calibration_set as production
from analysis import a3_structural_features as structural


FIXTURE = Path(__file__).parent / "fixtures" / "a3_calibration_selection_golden_v1.json"


class A3CalibrationSetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_version_and_contract_boundaries(self):
        self.assertEqual(production.C1_VERSION, "0.1.0")
        self.assertEqual(production.C0_CONTRACT_VERSION, "0.1.2")
        self.assertEqual(production.MECHANIC_BASELINE, "a2-v1.0.0")
        self.assertEqual(production.PILOT_TARGET, 24)
        self.assertEqual(production.RESERVE_TARGET, 12)
        self.assertEqual(production.INITIAL_ANALYSIS_BUDGET, 20_000)
        self.assertEqual(production.MAX_ANALYSIS_BUDGET, 50_000)
        source = inspect.getsource(production)
        self.assertNotIn("a3_calibration_selection_golden_v1", source)
        self.assertNotIn("tests.oracles", source)

    def test_d4_golden_and_all_eight_transforms(self):
        case = self.fixture["d4"]
        expected = case["expectedResearchEquivalenceId"]
        self.assertEqual(
            production.research_equivalence_serialization(
                case["n"], case["length"], case["initial"], case["targets"]
            ),
            case["expectedSerialization"],
        )
        for transform in range(8):
            initial = [
                production.transform_cell(case["n"], cell, transform)
                for cell in case["initial"]
            ]
            targets = [
                production.transform_cell(case["n"], cell, transform)
                for cell in case["targets"]
            ]
            self.assertEqual(
                production.research_equivalence_id(
                    case["n"], case["length"], initial, targets
                ),
                expected,
            )

    def test_tiny_candidate_universe_counts_and_order(self):
        one = production.candidate_universe({3: (3,)})
        full_n3 = production.candidate_universe({3: (3, 4, 5, 6, 7, 8)})
        self.assertEqual(len(one), 107)
        self.assertEqual(len(full_n3), 1300)
        ids = [row["researchEquivalenceIdV1"] for row in one]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            production.universe_fingerprint(one),
            production.universe_fingerprint(production.candidate_universe({3: (3,)})),
        )

    def test_distance_bins_and_descriptors_match_independent_golden(self):
        rows = [
            {
                "researchEquivalenceIdV1": identifier,
                "features": {"shortestDistance": distance},
            }
            for identifier, distance in self.fixture["distanceBins"]["rows"]
        ]
        self.assertEqual(
            production.assign_distance_bins(rows),
            self.fixture["distanceBins"]["expected"],
        )
        for row in self.fixture["descriptorCases"]:
            self.assertEqual(
                production.selection_descriptors(row["features"]),
                row["expected"],
            )

    def test_pair_tiers_are_predeclared(self):
        def row(identifier, *, detour=False, switch=False, setup=False, choice="UNIQUE_SHORTEST", mult="UNIQUE", legal=3, shortest=1, distance=5, regret=2, sequences=1):
            positive = 0 if choice == "ALL_SHORTEST" else max(1, legal - shortest)
            return {
                "researchEquivalenceIdV1": identifier,
                "n": 4,
                "length": 8,
                "features": {
                    "shortestDistance": distance,
                    "shortestActionSequenceCount": sequences,
                    "mandatoryInternalStateCount": 1 if setup else 0,
                    "initialLegalActionCount": legal,
                    "initialShortestActionCount": shortest,
                    "initialPositiveRegretActionCount": positive,
                    "initialMeanRegret": {"numerator": regret, "denominator": 1},
                    "initialMaxRegret": regret,
                    "shortestMinProximityUpSteps": 1 if detour else 0,
                    "shortestMinProximityUpMagnitude": 2 if detour else 0,
                    "shortestMinRelationalSideSwitches": 1 if switch else 0,
                },
                "descriptors": {
                    "detourFlag": detour,
                    "sideSwitchFlag": switch,
                    "mandatorySetupFlag": setup,
                    "firstChoiceClass": choice,
                    "positiveRegretFlag": positive > 0,
                    "multiplicityClass": mult,
                },
                "distanceBin": "Q2",
            }

        a = row("a", detour=False, switch=False)
        b = row("b", detour=True, switch=False)
        self.assertEqual(production._tier_ab("MP1", a, b), "A")

        c = row("c", detour=True, switch=True)
        self.assertEqual(production._tier_ab("MP1", a, c), "B")

        d = row("d", detour=True, switch=True, distance=6)
        self.assertIsNone(production._tier_ab("MP1", a, d))
        self.assertEqual(production._tier_c("MP1", a, d), "C")

    def test_small_injected_run_is_deterministic_and_has_no_human_label(self):
        def provider(n, length, initial, targets, *, state_cap):
            payload = json.dumps([n, length, initial, targets], separators=(",", ":"))
            digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            value = int(digest[:12], 16)
            legal = 2 + (value % 3)
            mode = (value >> 3) % 3
            if mode == 0:
                shortest = legal
            elif mode == 1:
                shortest = 1
            else:
                shortest = min(2, legal - 1)
            positive = legal - shortest
            total_regret = positive * 2
            mean = Fraction(total_regret, legal)
            sequences = 1 + ((value >> 6) % 7)
            detour = ((value >> 10) & 1) == 1
            switch = ((value >> 11) & 1) == 1
            mandatory = (value >> 12) % 3
            features = {
                "shortestDistance": 1 + ((value >> 14) % 8),
                "shortestActionSequenceCount": sequences,
                "shortestDagStateCount": 2 + ((value >> 18) % 20),
                "mandatoryInternalStateCount": mandatory,
                "initialLegalActionCount": legal,
                "initialShortestActionCount": shortest,
                "initialPositiveRegretActionCount": positive,
                "initialMeanRegret": {"numerator": mean.numerator, "denominator": mean.denominator},
                "initialMaxRegret": 0 if positive == 0 else 2,
                "shortestMinProximityUpSteps": 1 if detour else 0,
                "shortestMinProximityUpMagnitude": 2 if detour else 0,
                "shortestMinRelationalSideSwitches": 1 if switch else 0,
            }
            return {
                "domainStatus": "IN_DOMAIN",
                "puzzleFingerprint": digest,
                "features": {
                    name: {"status": structural.EXACT, "value": features[name]}
                    for name in structural.FEATURE_NAMES
                },
            }

        kwargs = {
            "max_analysis_budget": 107,
            "state_cap": 50,
            "profile_provider": provider,
            "domain_lengths": {3: (3,)},
        }
        first = production.construct_calibration_set(**kwargs)
        second = production.construct_calibration_set(**kwargs)
        self.assertEqual(first, second)
        self.assertEqual(
            first["manifestFingerprint"],
            production.normalized_manifest_fingerprint(first),
        )
        text = json.dumps(first, sort_keys=True).lower()
        self.assertNotIn("easy", text)
        self.assertNotIn("medium", text)
        self.assertNotIn("hard", text)
        self.assertNotIn("human difficulty", text)
        self.assertLessEqual(len(first["selected"]), 36)

    def test_execution_guards(self):
        with self.assertRaises(ValueError):
            production.construct_calibration_set(max_analysis_budget=50_001)
        with self.assertRaises(ValueError):
            production.construct_calibration_set(max_analysis_budget=0)
        with self.assertRaises(ValueError):
            production.construct_calibration_set(max_analysis_budget=1, state_cap=0)


if __name__ == "__main__":
    unittest.main()
