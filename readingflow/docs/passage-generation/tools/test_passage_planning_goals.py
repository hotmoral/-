import json
import unittest
from copy import deepcopy
from pathlib import Path
from passage_goal_contract import validate_goal_types,validate_goal_plan
P=Path(__file__).resolve().parents[1]/"planning"
class ReadingGoalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.goal_types=json.loads((P/"reading_goal_types_v1.json").read_text(encoding="utf8"))
        cls.plan=json.loads((P/"examples"/"reading_goals_condensation_v1.json").read_text(encoding="utf8"))
        cls.topic=json.loads((P/"examples"/"topic_condensation_v1.json").read_text(encoding="utf8"))
    def test_categories_and_no_level_gate(self):
        self.assertTrue(validate_goal_types(self.goal_types))
        self.assertTrue(self.goal_types["constraints"]["any_type_allowed_at_any_level"])
    def test_valid_goals_and_foreign_key(self):
        self.assertTrue(validate_goal_plan(self.plan,self.topic))
        self.assertEqual(len(self.plan["objectives"]),2)
    def test_reject_missing_fact_link(self):
        x=deepcopy(self.plan);x["objectives"][0]["required_fact_ids"]=[]
        with self.assertRaises(ValueError):validate_goal_plan(x,self.topic)
    def test_reject_more_than_three_or_bad_type(self):
        x=deepcopy(self.plan);x["objectives"]*=2
        with self.assertRaises(ValueError):validate_goal_plan(x,self.topic)
        x=deepcopy(self.plan);x["objectives"][0]["operation"]="설득 스타일"
        with self.assertRaises(ValueError):validate_goal_plan(x,self.topic)
    def test_goals_independent_of_author_draw(self):
        self.assertNotIn("author_attributes_24",self.plan)
        self.assertNotIn("서술 목적",self.plan)
    def test_reject_topic_age_mismatch(self):
        x=deepcopy(self.plan);x["level"]="L5"
        with self.assertRaises(ValueError):validate_goal_plan(x,self.topic)
if __name__=="__main__":unittest.main()
