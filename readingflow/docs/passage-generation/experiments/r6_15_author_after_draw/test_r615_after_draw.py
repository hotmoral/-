"""R6.15: real pool seeded-draw reproducibility and 17 structural QA.
This test only executes when repository Python and its canonical input files
are available; NO live AI provider and no human semantic approval.
"""
import json
import unittest
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
TOOLS=HERE.parents[1]/"tools"
SIBLING_TRIAL=HERE.parent/"r6_12_door_torque"
sys.path.insert(0,str(TOOLS))
sys.path.insert(0,str(SIBLING_TRIAL))
from run_trial import load_trial
from author_attribute_sampler import draw_author_attributes,verify_selection
from new_passage_qa_gate import evaluate_new_candidate
def read(name):return json.loads((HERE/name).read_text(encoding="utf-8"))

class R615AuthorAfterDraw(unittest.TestCase):
    def test_pools_selection_reproduces_exactly(self):
        inp=load_trial()[2]
        rec=read("author_draw_and_application_v1.json")
        original=draw_author_attributes(rec["passage_id"],inp["pools"],seed=rec["seed"])
        self.assertEqual(original["author_attributes_24"],rec["selection_values"])
        self.assertEqual(original["candidate_pools_sha256"],rec["attribute_candidate_pools_sha256"])
        self.assertEqual(len(rec["selection_values"]),24)
        self.assertEqual(rec["reroll_count"],0)
        self.assertTrue(verify_selection(original,inp["pools"]))
    def test_fresh_candidate_17_structure(self):
        doc=read("experimental_candidate_v1.json")
        baseline=load_trial()[2]
        report=evaluate_new_candidate(doc,author_selection=draw_author_attributes(doc["passage_id"],baseline["pools"],seed=202611232249))
        self.assertEqual(report["decision"],"READY_FOR_EDITORIAL_REVIEW")
        self.assertEqual(len(report["checks"]),17)
        self.assertEqual(report["errors"],[])
        self.assertEqual(report["warnings"],[])
        self.assertFalse(report["human_validated"])
        self.assertFalse(report["can_publish"])
    def test_style_review_is_not_approval(self):
        candidate=read("experimental_candidate_v1.json")
        assessment=read("style_application_ai_review_v1.json")
        self.assertEqual(len(assessment["items"]),24)
        self.assertFalse(assessment["human_reviewed"])
        self.assertFalse(assessment["semantic_style_validated"])
        self.assertTrue(all(not row["example_quote"] or row["example_quote"] in candidate["source_text"] for row in assessment["items"]))
        self.assertEqual({q["correct_option"] for q in candidate["questions"]},{"A","B","D"})
        self.assertFalse(candidate["release_approved"])
        self.assertFalse(candidate["can_publish"])

if __name__=="__main__":unittest.main()
