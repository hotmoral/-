"""R6.11 generated candidate -> Stage5 -> 17 QA, no reroll/no publish."""
import copy
import unittest
from passage_stage5_integration import load_inputs,integrate
from new_passage_generation_pipeline import generate_experimental_candidate


def response_for(request):
    # Synthetic sample only; NOT a genuine checked or publishable passage.
    t=("차가운 컵 근처의 공기가 식으면 수증기가 작은 물방울로 바뀔 수 있다. "
       "물방울은 컵 안에서 새어 나왔다는 뜻이 아니다. "
       "습도와 표면 온도는 물방울의 양에 영향을 줄 수 있다.")
    qs=[]
    rows=[
        ("물방울의 근원","공기 중 수증기","차가운 컵 근처의 공기가 식으면 수증기가 작은 물방울로 바뀔 수 있다."),
        ("잘못된 원인 구별","컵 안에서 샌 물이 아니다","물방울은 컵 안에서 새어 나왔다는 뜻이 아니다."),
        ("조건 비교","습도와 표면 온도","습도와 표면 온도는 물방울의 양에 영향을 줄 수 있다."),
    ]
    for i,(goal,ans,quote) in enumerate(rows,1):
        qs.append({
            "question_id":request["passage_id"]+"-Q"+str(i),
            "question":"글의 내용에 비추어 설명한 사실 "+str(i)+"은 무엇인가요?",
            "question_goal":goal,"question_type":"사실",
            "source_version":request["passage_version"],"answer":ans,
            "correct_option":"B","evidence":quote,"explanation":"지문 근거에 따른 선택",
            "format":"single_choice",
            "options":[{"id":"A","text":"온도가 높을 때만 언제나 생긴다"},
                       {"id":"B","text":ans},
                       {"id":"C","text":"물방울은 반드시 컵에서 새어 나온다"},
                       {"id":"D","text":"컵의 색에 따라 크기가 달라진다"}],
            "distractor_grounding":[
                {"option_id":k,"evidence":quote,
                 "false_reason":"본문에서 설명된 조건·대상과 일치하지 않는다."}
                for k in ("A","C","D")]
        })
    return {"source_text":t,"questions":qs}


class GeneratedPipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs=load_inputs()
        cls.pid="RF-R611-NEW-EXPERIMENT-001"

    def test_default_unverified_source_blocks_before_calling_provider(self):
        calls=[]
        def forbidden(request):
            calls.append(request)
            raise AssertionError("provider must NOT be called")
        x=generate_experimental_candidate(self.inputs,passage_id=self.pid,
                                          provider=forbidden,seed=33)
        self.assertEqual(x["status"],"HOLD_SOURCE_VERIFICATION")
        self.assertFalse(x["provider_called"])
        self.assertFalse(x["can_publish"])
        self.assertEqual(calls,[])

    def test_explicit_experimental_writing_and_questions_reuse_single_draw(self):
        calls=[]
        def provider(req):
            calls.append(copy.deepcopy(req))
            return response_for(req)
        x=generate_experimental_candidate(self.inputs,passage_id=self.pid,
                 provider=provider,seed=33,allow_unverified_sources=True)
        self.assertEqual(len(calls),1)
        self.assertEqual(x["status"],"READY_FOR_EDITORIAL_REVIEW")
        self.assertTrue(x["author_drawing_reused"])
        self.assertTrue(x["source_validation_pending"])
        self.assertEqual(len(x["candidate"]["questions"]),3)
        self.assertEqual(len(x["new_passage_qa"]["checks"]),17)
        self.assertTrue(all(y["editorial_state"]=="NOT_REVIEWED" for y in x["new_passage_qa"]["checks"]))
        self.assertEqual(x["stage5"]["stages"][7]["state"],"AI_GENERATED_EXPERIMENTAL_DRAFT")
        self.assertEqual(x["stage5"]["author_selection"]["author_attributes_24"],calls[0]["author_attributes_24"])
        self.assertFalse(x["can_publish"])
        self.assertFalse(x["release_approved"])

    def test_no_reselect_based_on_a_question_failure(self):
        calls=[]
        def invalid(req):
            calls.append(req)
            doc=response_for(req)
            doc["questions"][0]["correct_option"]="A"
            return doc
        result=generate_experimental_candidate(self.inputs,passage_id=self.pid,
                      provider=invalid,seed=33,allow_unverified_sources=True)
        self.assertEqual(len(calls),1)
        self.assertEqual(result["status"],"REVISE")
        self.assertEqual(result["stage5"]["author_selection"]["author_attributes_24"],
                         calls[0]["author_attributes_24"])
        self.assertIn("ANSWER_MAPPING_INVALID",[x["code"] for x in result["new_passage_qa"]["errors"]])

    def test_reject_provider_identity_and_approval_tampering(self):
        for mutation in ({"passage_id":"OTHER"},{"release_approved":True},
                         {"age_group":"성인"},{"can_publish":True}):
            def bad(req):
                return dict(response_for(req),**mutation)
            with self.assertRaises(ValueError):
                generate_experimental_candidate(self.inputs,passage_id=self.pid,
                    provider=bad,seed=1,allow_unverified_sources=True)

    def test_presupplied_draw_reuse_and_tampering_guard(self):
        pre=integrate(self.inputs,passage_id=self.pid,seed=11)
        selected=pre["author_selection"]
        x=integrate(self.inputs,passage_id=self.pid,author_selection_override=selected)
        self.assertEqual(x["author_selection"],selected)
        with self.assertRaises(ValueError):
            integrate(self.inputs,passage_id=self.pid,author_selection_override=selected,seed=11)
        wrong=copy.deepcopy(selected)
        wrong["passage_id"]="OTHER"
        with self.assertRaises(ValueError):
            integrate(self.inputs,passage_id=self.pid,author_selection_override=wrong)
        wrong=copy.deepcopy(selected)
        key=next(iter(wrong["author_attributes_24"]))
        wrong["author_attributes_24"][key]="NOT_IN_POOL"
        with self.assertRaises(ValueError):
            integrate(self.inputs,passage_id=self.pid,author_selection_override=wrong)

    def test_provider_request_does_not_claim_verified_facts(self):
        seen=[]
        def gen(req):
            seen.append(copy.deepcopy(req))
            return response_for(req)
        generate_experimental_candidate(self.inputs,passage_id=self.pid,
                provider=gen,seed=9,allow_unverified_sources=True)
        request=seen[0]
        self.assertFalse(request["facts_verified_by_this_pipeline"])
        self.assertEqual(len(request["author_attributes_24"]),24)
        self.assertEqual(len(request["unverified_fact_ids"]),6)
        self.assertEqual(request["required_response"]["questions"][0]["source_version"],
                         request["passage_version"])
        self.assertTrue(request["instructions"]["prior_knowledge_guessability_is_not_quality_criterion"])

if __name__=="__main__":
    unittest.main()
