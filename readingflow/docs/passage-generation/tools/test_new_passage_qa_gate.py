"""R6.10 structural QA gate, immutability, Stage5 connection regression."""
import copy
import hashlib
import unittest
from new_passage_qa_gate import evaluate_new_candidate,load_contract
from passage_stage5_integration import load_inputs,integrate

def fixture():
    text="물은 흙으로 스며든다. 흙의 틈을 따라 움직인다. 햇빛을 받으면 따뜻해진다."
    qs=[]
    for n,answer,quote in (
        (1,"흙으로 스며든다","물은 흙으로 스며든다."),
        (2,"틈을 따라 움직인다","흙의 틈을 따라 움직인다."),
        (3,"따뜻해진다","햇빛을 받으면 따뜻해진다.")):
        qs.append({
          "question_id":"NEW-Q"+str(n),"question":"글에서 설명한 현상 "+str(n)+"은 무엇인가요?",
          "question_type":"사실","question_goal":"현상 "+str(n),
          "evidence":quote,"answer":answer,"explanation":"지문의 설명을 확인한다.",
          "format":"single_choice","source_version":"draft-v1","correct_option":"B",
          "options":[{"id":"A","text":"크기는 언제나 변한다"},{"id":"B","text":answer},
                     {"id":"C","text":"순서를 반드시 바꾼다"},{"id":"D","text":"대상과 장소가 바뀐다"}],
          "distractor_grounding":[
           {"option_id":x,"evidence":quote,"false_reason":"해당 설명이 원문에 없다."}
           for x in ("A","C","D")]})
    return {"passage_id":"RF-NEW-GATE-TEST","passage_version":"draft-v1",
            "source_text":text,"age_group":"초등 저학년","level":"L2",
            "release_approved":False,"questions":qs}

class NewPassageQATests(unittest.TestCase):
    def test_all_17_structural_readiness_no_semantic_certification(self):
        data=fixture();old=copy.deepcopy(data);r=evaluate_new_candidate(data)
        self.assertEqual(data,old)
        self.assertEqual(r["decision"],"READY_FOR_EDITORIAL_REVIEW")
        self.assertEqual(r["checklist_count"],17)
        self.assertEqual(len(r["checks"]),17)
        self.assertEqual(set(x["editorial_state"] for x in r["checks"]),{"NOT_REVIEWED"})
        self.assertFalse(r["semantic_uniqueness_validated"])
        self.assertFalse(r["release_approved"])
        self.assertFalse(r["can_publish"])
        self.assertEqual(r["source_sha256"],hashlib.sha256(data["source_text"].encode()).hexdigest())
        self.assertIn("BACKGROUND_KNOWLEDGE_BLIND_GUESSABILITY",r["excluded_quality_checks"])
    def test_no_draft_and_no_questions_hold(self):
        data=fixture();data["source_text"]=None;data["questions"]=None
        r=evaluate_new_candidate(data)
        self.assertEqual(r["decision"],"HOLD")
        self.assertEqual(len(r["pending_semantic_check_ids"]),17)
        data["source_text"]=fixture()["source_text"]
        self.assertEqual(evaluate_new_candidate(data)["decision"],"HOLD")
    def test_bad_answer_key_or_version_revise(self):
        data=fixture()
        data["questions"][0]["correct_option"]="A"
        data["questions"][1]["source_version"]="old-draft"
        r=evaluate_new_candidate(data)
        self.assertEqual(r["decision"],"REVISE")
        self.assertIn("ANSWER_MAPPING_INVALID",[x["code"] for x in r["errors"]])
        self.assertIn("STALE_QUESTION_VERSION",[x["code"] for x in r["errors"]])
    def test_missing_distractor_grounding_blocks(self):
        data=fixture();data["questions"][1]["distractor_grounding"][0]["evidence"]="not in source"
        self.assertIn("DISTRACTOR_REASON_OR_QUOTE_MISSING",
                      [x["code"] for x in evaluate_new_candidate(data)["errors"]])
    def test_shortest_absolute_flags_are_not_auto_failure(self):
        r=evaluate_new_candidate(fixture())
        self.assertEqual(r["decision"],"READY_FOR_EDITORIAL_REVIEW")
        self.assertTrue(any(x["code"]=="OPTION_SURFACE_CUE" for x in r["warnings"]))
        self.assertFalse(any("BACKGROUND" in x["code"] for x in r["errors"]))
    def test_wrong_count_stale_sha_and_approval(self):
        data=fixture();data["questions"].pop()
        self.assertIn("QUESTION_COUNT",[x["code"] for x in evaluate_new_candidate(data)["errors"]])
        data=fixture();data["source_text_sha256"]="00"*32
        data["release_approved"]=True
        r=evaluate_new_candidate(data)
        self.assertEqual(r["decision"],"REVISE")
        self.assertIn("STALE_SHA",[x["code"] for x in r["errors"]])
        self.assertIn("SELF_APPROVED",[x["code"] for x in r["errors"]])
        self.assertFalse(r["release_approved"])
    def test_stage5_integrates_pending_and_new_question_bundle(self):
        inputs=load_inputs()
        r=integrate(inputs,passage_id="RF-STAGE5-EXPERIMENT-CONDENSATION-0001",seed=71)
        self.assertEqual(r["new_passage_qa"]["decision"],"HOLD")
        self.assertEqual(len(r["new_passage_qa"]["checks"]),17)
        self.assertIn("NEW_PASSAGE_17_ITEM_QA",r["pending_reviews"])
        data=fixture()
        data["age_group"]=inputs["topic"]["age_group"]
        data["level"]=inputs["topic"]["level"]
        draft={"passage_id":data["passage_id"],"topic_id":inputs["topic"]["topic_id"],
               "source_tag":"MANUALLY_SUPPLIED_EXPERIMENTAL_DRAFT",
               "passage_version":data["passage_version"],"text":data["source_text"],
               "release_approved":False}
        other=integrate(inputs,passage_id=data["passage_id"],draft=draft,seed=71,
                        question_bundle=data)
        self.assertEqual(other["new_passage_qa"]["decision"],"READY_FOR_EDITORIAL_REVIEW")
        self.assertFalse(other["can_publish"])
        invalid=copy.deepcopy(data);invalid["source_text"]="not same"
        with self.assertRaises(ValueError):
            integrate(inputs,passage_id=data["passage_id"],draft=draft,seed=71,
                      question_bundle=invalid)
    def test_policy_has_exact_ids(self):
        self.assertEqual(len(load_contract()["required"]),17)

if __name__=="__main__":
    unittest.main()
