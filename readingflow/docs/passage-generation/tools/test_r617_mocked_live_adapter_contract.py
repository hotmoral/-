"""R6.17: test actual Responses adapter contract without network/paid API.

The model output is a chat-authored manuscript read from the experiment JSON.
The mocked HTTP endpoint is strictly a protocol test, not live AI validation.
"""
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from passage_stage5_integration import load_inputs
from new_passage_generation_pipeline import generate_experimental_candidate
from openai_new_passage_adapter import openai_generate_new_passage

ROOT=Path(__file__).resolve().parents[1]
TRIAL=ROOT/"experiments/r6_17_ci_and_generation"


class _Response:
    def __init__(self, body):
        self.body=json.dumps(body,ensure_ascii=False).encode("utf-8")
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self):return self.body


class MockedResponsesAdapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=json.loads((TRIAL/"trial_inputs_v1.json").read_text(encoding="utf-8"))
        cls.author=json.loads((TRIAL/"author_draw_v1.json").read_text(encoding="utf-8"))
        cls.sample=json.loads((TRIAL/"model_authored_output_v1.json").read_text(encoding="utf-8"))
        cls.inputs=load_inputs()
        cls.inputs.update(topic=cls.plan["topic"],goals=cls.plan["goals"],evidence=cls.plan["evidence"])

    def test_missing_auth_or_model_blocks_live_api_request(self):
        req={"mode":"EXPERIMENT_ONLY"}
        with patch.dict(os.environ,{"OPENAI_API_KEY":"","READINGFLOW_PASSAGE_MODEL":""}):
            with self.assertRaisesRegex(RuntimeError,"OPENAI_API_KEY"):
                openai_generate_new_passage(req)
        with patch.dict(os.environ,{"OPENAI_API_KEY":"DUMMY_TEST_ONLY","READINGFLOW_PASSAGE_MODEL":""}):
            with self.assertRaisesRegex(RuntimeError,"READINGFLOW_PASSAGE_MODEL"):
                openai_generate_new_passage(req)

    def test_mocked_responses_json_enters_real_stage5_with_exact_author_draw(self):
        recorded=[]
        answer={"source_text":self.sample["source_text"],"questions":self.sample["questions"]}
        response={"output":[{"type":"message","content":[{"type":"output_text","text":json.dumps(answer,ensure_ascii=False)}]}]}
        def fake_post(request,timeout):
            recorded.append((request,timeout))
            return _Response(response)
        with patch.dict(os.environ,{"OPENAI_API_KEY":"DUMMY_TEST_ONLY","READINGFLOW_PASSAGE_MODEL":"DUMMY_MODEL_ONLY"}):
            with patch("openai_new_passage_adapter.urlopen",side_effect=fake_post):
                result=generate_experimental_candidate(
                    self.inputs,passage_id=self.plan["passage_id"],passage_version=self.plan["passage_version"],
                    provider=openai_generate_new_passage,allow_unverified_sources=True,
                    author_selection_override=self.author)
        self.assertEqual(result["status"],"READY_FOR_EDITORIAL_REVIEW")
        self.assertEqual(result["new_passage_qa"]["errors"],[])
        self.assertEqual(result["new_passage_qa"]["warnings"],[])
        self.assertEqual(len(recorded),1)
        http_req,timeout=recorded[0]
        self.assertEqual(http_req.full_url,"https://api.openai.com/v1/responses")
        self.assertEqual(timeout,120)
        body=json.loads(http_req.data.decode("utf-8"))
        self.assertIs(body["store"],False)
        self.assertEqual(body["text"]["format"],{"type":"json_object"})
        self.assertEqual(body["model"],"DUMMY_MODEL_ONLY")
        request=json.loads(body["input"])
        self.assertEqual(request["author_attributes_24"],self.author["author_attributes_24"])
        self.assertEqual(request["passage_id"],self.plan["passage_id"])
        self.assertEqual(request["mode"],"EXPERIMENT_ONLY")
        self.assertFalse(result["can_publish"])

    def test_provider_requires_explicit_experimental_mode(self):
        with patch.dict(os.environ,{"OPENAI_API_KEY":"DUMMY_TEST_ONLY","READINGFLOW_PASSAGE_MODEL":"DUMMY_MODEL_ONLY"}):
            with self.assertRaises(ValueError):
                openai_generate_new_passage({"mode":"PRODUCTION"})


if __name__=="__main__":unittest.main()
