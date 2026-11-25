"""QA quality decisions must never auto-certify semantic criteria or release content."""
import json
import unittest
from copy import deepcopy
from pathlib import Path
from passage_quality_gate import validate_quality_record, quality_gate, validate_quality_policy

ROOT=Path(__file__).resolve().parents[1]/"operations"/"quality"
class QualityGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy=json.loads((ROOT/"quality_policy_v1.json").read_text(encoding="utf8"))
        cls.example=json.loads((ROOT/"examples"/"condensation_quality_pending.json").read_text(encoding="utf8"))
    def test_eight_dimensions_and_pending_sample(self):
        self.assertEqual(len(validate_quality_policy(self.policy)),8)
        x=quality_gate(self.example,self.policy)
        self.assertTrue(x["structure_valid"])
        self.assertFalse(x["can_release"])
        self.assertEqual(len(x["review_needed_codes"]),8)
    def test_no_auto_pass_when_pending(self):
        x=deepcopy(self.example);x["quality_review_status"]="PASS"
        with self.assertRaises(ValueError):validate_quality_record(x,self.policy)
    def test_pass_requires_reviewers_and_evidence(self):
        x=deepcopy(self.example);x["category_checks"][0]["state"]="PASS"
        with self.assertRaises(ValueError):validate_quality_record(x,self.policy)
        x["category_checks"][0]["reviewer"]="reviewer";x["category_checks"][0]["evidence_refs"]=["SRC:1"]
        self.assertTrue(validate_quality_record(x,self.policy))
        self.assertFalse(quality_gate(x,self.policy)["can_release"])
    def test_release_flag_is_separate_and_forbidden_here(self):
        x=deepcopy(self.example);x["release_approved"]=True
        with self.assertRaises(ValueError):validate_quality_record(x,self.policy)
    def test_missing_category_detected(self):
        x=deepcopy(self.example);x["category_checks"].pop()
        with self.assertRaises(ValueError):validate_quality_record(x,self.policy)
    def test_duplicate_category_detected(self):
        x=deepcopy(self.example);x["category_checks"][0]["code"]=x["category_checks"][1]["code"]
        with self.assertRaises(ValueError):validate_quality_record(x,self.policy)
    def test_unverified_facts_not_mistaken_for_evidence(self):
        self.assertFalse(self.example["source_facts_verified"])
        self.assertFalse(self.example["learner_difficulty_validated"])
        self.assertFalse(self.example["questions_reviewed"])
if __name__=="__main__":unittest.main()
