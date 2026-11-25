import json
import unittest
from pathlib import Path
from passage_duplication_diversity import audit_corpus

BASE=Path(__file__).resolve().parents[1]
class DuplicationDiversityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        planning=BASE/"planning"
        cls.catalog=json.loads((BASE/"data"/"normalized_passage_catalog_30_v1.json").read_text(encoding="utf-8"))
        cls.mapping=json.loads((planning/"topic_catalog_30_provisional_v2.json").read_text(encoding="utf-8"))
        cls.candidate=json.loads((BASE/"operations"/"diversity"/"examples"/"condensation_candidate.json").read_text(encoding="utf-8"))
        cls.rows=[{"passage_id":x["passage_id"],"title":x["topic"],"age_group":x["source_age_group"],
                   "level":x["source_level"],"primary_domain":x["primary_domain"]} for x in cls.mapping["records"]]
    def test_baseline_30_and_known_overlap_not_auto_rejected(self):
        x=audit_corpus(self.rows,self.candidate)
        self.assertEqual(x["corpus_count"],30)
        self.assertIn("RF-PILOT-UPPER-L2",
          [f["right_id"] for f in x["planned_topic_review_flags"] if f["type"]=="EXPLICIT_KNOWN_TOPIC_OVERLAP"])
        self.assertEqual(x["auto_rejected"],0)
        self.assertFalse(x["release_approved"])
        self.assertEqual(x["style_diversity_status"],"NOT_MEASURABLE_FROM_METADATA")
    def test_same_title_only_review_not_delete(self):
        rows=[{"passage_id":"A","title":"나무의  역할","age_group":"성인","level":"L2","primary_domain":"자연과학"},
              {"passage_id":"B","title":"나무의 역할!","age_group":"성인","level":"L3","primary_domain":"환경·생태"}]
        x=audit_corpus(rows)
        self.assertIn("EXACT_TITLE_REVIEW",[f["type"] for f in x["topic_overlap_review_flags"]])
        self.assertEqual(x["auto_rejected"],0)
    def test_full_text_detects_only_exact_match(self):
        rows=[{"passage_id":"A","title":"한 편","age_group":"성인","level":"L2","primary_domain":"자연과학","text":"새는 날아간다."},
              {"passage_id":"B","title":"두 편","age_group":"성인","level":"L3","primary_domain":"자연과학","text":"새는  날아간다."}]
        x=audit_corpus(rows)
        self.assertIn("EXACT_TEXT_REVIEW",[f["type"] for f in x["topic_overlap_review_flags"]])
        self.assertEqual(x["exact_fulltext_checked_pairs"],1)
        self.assertEqual(x["auto_rejected"],0)
    def test_no_full_text_no_plagiarism_claim(self):
        x=audit_corpus(self.rows)
        self.assertEqual(x["exact_fulltext_checked_pairs"],0)
        self.assertEqual(x["status"],"STRUCTURAL_INDICATORS_NOT_SEMANTIC_DECISION")
    def test_invalid_duplicate_passage_id_fails(self):
        rows=[dict(self.rows[0]),dict(self.rows[0])]
        with self.assertRaises(ValueError):audit_corpus(rows)
    def test_unlisted_known_overlap_fails(self):
        cand=dict(self.candidate,known_possible_matches=["NOT_IN_CATALOG"])
        with self.assertRaises(ValueError):audit_corpus(self.rows,cand)
    def test_distribution_does_not_impose_equality(self):
        x=audit_corpus(self.rows)
        self.assertEqual(sum(x["primary_domain_distribution"].values()),30)
        self.assertNotIn("target_ratio",x)
if __name__=="__main__":unittest.main()
