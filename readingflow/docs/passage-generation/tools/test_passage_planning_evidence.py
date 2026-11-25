import json
import unittest
from copy import deepcopy
from pathlib import Path
from passage_evidence_contract import validate_fact_registry,planning_readiness
P=Path(__file__).resolve().parents[1]/"planning"/"examples"
class EvidencePlanningContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def load(name):return json.loads((P/name).read_text(encoding="utf8"))
        cls.topic=load("topic_condensation_v1.json")
        cls.goals=load("reading_goals_condensation_v1.json")
        cls.evidence=load("facts_condensation_v1.json")
    def test_six_facts_and_three_unreviewed_sources(self):
        self.assertTrue(validate_fact_registry(self.evidence,self.topic))
        self.assertEqual(len(self.evidence["facts"]),6)
        self.assertEqual(len(self.evidence["sources"]),3)
    def test_missing_goal_fact_reference_is_rejected(self):
        g=deepcopy(self.goals);g["objectives"][0]["required_fact_ids"].append("NO_SUCH_FACT")
        with self.assertRaises(ValueError):planning_readiness(self.topic,g,self.evidence)
    def test_unknown_source_cannot_supply_fact(self):
        r=deepcopy(self.evidence);r["facts"][0]["source_refs"][0]["source_id"]="UNKNOWN"
        with self.assertRaises(ValueError):validate_fact_registry(r,self.topic)
    def test_pending_sources_block_verified_drafting(self):
        result=planning_readiness(self.topic,self.goals,self.evidence)
        self.assertTrue(result["structurally_valid"])
        self.assertFalse(result["ready_for_verified_fact_drafting"])
        self.assertFalse(result["ready_for_release_pipeline"])
        self.assertIn("FACTS_NOT_VERIFIED",result["unresolved_checks"])
    def test_cannot_claim_fact_review_without_locator_and_reviewer(self):
        r=deepcopy(self.evidence);r["facts"][0]["verification_status"]="REVIEWED_BY_HUMAN"
        with self.assertRaises(ValueError):validate_fact_registry(r,self.topic)
        r["facts"][0]["reviewer"]="reviewer";r["facts"][0]["reviewed_at"]="2026-11-20";r["facts"][0]["source_refs"][0]["locator"]="paragraph 1"
        with self.assertRaises(ValueError):validate_fact_registry(r,self.topic)
    def test_cannot_claim_source_review_without_evidence_of_check(self):
        r=deepcopy(self.evidence);r["sources"][0]["source_check_status"]="REVIEWED_BY_HUMAN"
        with self.assertRaises(ValueError):validate_fact_registry(r,self.topic)
    def test_unapproved_and_no_author_rng_connection(self):
        self.assertFalse(self.evidence["release_approved"])
        self.assertNotIn("author_attributes_24",self.evidence)
if __name__=="__main__":unittest.main()
