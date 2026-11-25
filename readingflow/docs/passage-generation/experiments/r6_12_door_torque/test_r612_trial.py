"""R6.12 offline source-hold, QA contract, no-reroll and passage grounding."""
import unittest
from run_trial import run_trial,load_trial
from passage_stage5_integration import integrate
from author_attribute_sampler import ATTRIBUTE_NAMES, verify_selection
import copy

class R612DoorTorqueTests(unittest.TestCase):
    def test_existing_baseline_is_untouched(self):
        plan, sample, inputs=load_trial()
        self.assertEqual(len(inputs["legacy_catalog"]["records"]),30)
        self.assertNotIn(sample["passage_id"],{p["passage_id"] for p in inputs["legacy_catalog"]["records"]})
    def test_trial_pipeline_and_source_block(self):
        result=run_trial()
        self.assertEqual(result["default_source_gate"]["status"],"HOLD_SOURCE_VERIFICATION")
        generated=result["experimental_result"]
        self.assertEqual(generated["status"],"READY_FOR_EDITORIAL_REVIEW")
        self.assertEqual(result["provider_calls"],1)
        self.assertTrue(generated["source_validation_pending"])
        self.assertFalse(generated["can_publish"])
        self.assertFalse(generated["release_approved"])
    def test_genuine_stage5_and_one_draw_reuse(self):
        out=run_trial()
        stage=out["experimental_result"]["stage5"]
        sel=stage["author_selection"]
        _,_,inputs=load_trial()
        self.assertEqual(len(stage["stages"]),11)
        self.assertEqual(stage["legacy_baseline_count"],30)
        self.assertEqual(stage["stages"][7]["state"],"AI_GENERATED_EXPERIMENTAL_DRAFT")
        self.assertEqual(set(sel["author_attributes_24"]),set(ATTRIBUTE_NAMES))
        self.assertTrue(verify_selection(sel,inputs["pools"]))
        self.assertTrue(out["author_selection_transmitted_and_reused"])
        self.assertFalse(out["author_style_in_passage_verified"])

    def test_stage5_override_must_not_redraw(self):
        plan,_,inputs=load_trial()
        preflight=integrate(inputs,passage_id=plan["passage_id"],seed=plan["seed"])
        original=preflight["author_selection"]
        reused=integrate(inputs,passage_id=plan["passage_id"],
                         author_selection_override=original)
        self.assertEqual(reused["author_selection"],original)
        with self.assertRaises(ValueError):
            integrate(inputs,passage_id=plan["passage_id"],seed=plan["seed"],
                      author_selection_override=original)

    def test_old_30_records_not_mutated_by_stage5_run(self):
        plan,_,inputs=load_trial()
        snapshot=copy.deepcopy(inputs)
        run_trial()
        self.assertEqual(inputs,snapshot)

    def test_three_different_questions_and_groundings(self):
        plan, sample, inputs=load_trial()
        source=sample["source_text"]
        self.assertEqual(len(sample["questions"]),3)
        self.assertEqual(len(set(q["question_goal"] for q in sample["questions"])),3)
        for q in sample["questions"]:
            self.assertEqual(q["source_version"],sample["passage_version"])
            self.assertEqual([o["id"] for o in q["options"]],["A","B","C","D"])
            self.assertEqual(q["answer"],next(o["text"] for o in q["options"] if o["id"]==q["correct_option"]))
            self.assertIn(q["evidence"],source)
            self.assertEqual({g["option_id"] for g in q["distractor_grounding"]},set("ABCD")-{q["correct_option"]})
            self.assertTrue(all(g["evidence"] in source and g["false_reason"].strip() for g in q["distractor_grounding"]))
    def test_answer_not_unique_min_or_max_by_length(self):
        _,sample,_=load_trial()
        for q in sample["questions"]:
            chars={o["id"]:len("".join(o["text"].split())) for o in q["options"]}
            vals=list(chars.values())
            c=chars[q["correct_option"]]
            self.assertFalse(c==min(vals) and vals.count(c)==1,q["question_id"]+" shortest")
            self.assertFalse(c==max(vals) and vals.count(c)==1,q["question_id"]+" longest")

    def test_explicit_not_semantic_or_human_pass(self):
        result=run_trial()["experimental_result"]
        report=result["new_passage_qa"]
        self.assertEqual(len(report["checks"]),17)
        self.assertTrue(all(item["editorial_state"]=="NOT_REVIEWED" for item in report["checks"]))
        self.assertFalse(report["human_validated"])
        self.assertFalse(report["semantic_uniqueness_validated"])
        self.assertFalse(report["can_publish"])
        self.assertFalse(result["author_attributes_24_are_style_verified"])
        self.assertEqual(result["human_semantic_review"],"NOT_RUN")

if __name__=="__main__":unittest.main()
