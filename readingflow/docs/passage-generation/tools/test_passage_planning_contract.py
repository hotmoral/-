import json
import unittest
from copy import deepcopy
from pathlib import Path
from passage_planning_contract import validate_taxonomy,validate_topic_record
BASE=Path(__file__).resolve().parents[1]/"planning"

class TopicPlanningContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tax=json.loads((BASE/"topic_taxonomy_proposal_v1.json").read_text(encoding="utf8"))
        cls.rec=json.loads((BASE/"examples"/"topic_condensation_v1.json").read_text(encoding="utf8"))
    def test_domain_seed_count(self):
        self.assertEqual(len(validate_taxonomy(self.tax)),18)
    def test_example_tracks_possible_existing_overlap(self):
        self.assertTrue(validate_topic_record(self.rec,self.tax))
        self.assertEqual(self.rec["overlap_review"]["status"],"NEEDS_SEMANTIC_REVIEW")
    def test_unknown_domain_requires_explicit_proposal(self):
        rec=deepcopy(self.rec);rec["primary_domain"]="신규 융합분야"
        with self.assertRaises(ValueError):validate_topic_record(rec,self.tax)
        rec["classification_status"]="PROPOSED_NEW_DOMAIN"
        self.assertTrue(validate_topic_record(rec,self.tax))
    def test_no_author_or_unimplemented_auto_topic(self):
        self.assertNotIn("author_attributes_24",self.rec)
        rec=deepcopy(self.rec);rec["selection_mode"]="AUTO_SELECTED"
        with self.assertRaises(ValueError):validate_topic_record(rec,self.tax)
    def test_no_duplicate_primary_and_secondary(self):
        rec=deepcopy(self.rec);rec["secondary_domains"]=["자연과학"]
        with self.assertRaises(ValueError):validate_topic_record(rec,self.tax)
if __name__=="__main__":unittest.main()
