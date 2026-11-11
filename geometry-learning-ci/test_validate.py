"""No proprietary geometry project source or fixtures in these tests."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import verify

EXAMPLE = json.loads((Path(__file__).with_name("synthetic_fixture.json")).read_text(encoding="utf-8"))


class PublicSyntheticTransferContract(unittest.TestCase):
    def test_valid_example(self):
        self.assertEqual(verify(EXAMPLE)["status"], "PASS_PUBLIC_SYNTHETIC_RULES_ONLY")

    def test_cannot_satisfy_stable_with_duplicate_stimulus(self):
        x = copy.deepcopy(EXAMPLE)
        x["domains"]["S1"]["planned"][0]["stimulus"] = "topo1"
        with self.assertRaises(ValueError):
            verify(x)

    def test_no_core_stage_promotion(self):
        x = copy.deepcopy(EXAMPLE)
        x["domains"]["S1"]["planned"][0]["stageUpdateEligible"] = True
        with self.assertRaises(ValueError):
            verify(x)

    def test_insufficient_representation_families_fails(self):
        x = copy.deepcopy(EXAMPLE)
        for row in x["domains"]["S1"]["planned"]:
            row["representation"] = "dots"
        with self.assertRaises(ValueError):
            verify(x)

    def test_heldout_must_not_match_training(self):
        x = copy.deepcopy(EXAMPLE)
        x["domains"]["S1"]["heldout"][0]["stimulus"] = "topo2"
        with self.assertRaises(ValueError):
            verify(x)

    def test_missing_heldout_fails(self):
        x = copy.deepcopy(EXAMPLE)
        x["domains"]["S2"]["heldout"] = []
        with self.assertRaises(ValueError):
            verify(x)

    def test_insufficient_training_pool_fails(self):
        x = copy.deepcopy(EXAMPLE)
        x["domains"]["S2"]["planned"] = []
        with self.assertRaises(ValueError):
            verify(x)

    def test_unexpected_public_payload_fails(self):
        x = copy.deepcopy(EXAMPLE)
        x["domains"]["S1"]["planned"][0]["privateNote"] = "sensitive"
        with self.assertRaises(ValueError):
            verify(x)


if __name__ == "__main__":
    unittest.main()
