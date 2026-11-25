"""R6.17: real Stage5 consumes the draw made BEFORE model prose, no second draw."""
import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from passage_stage5_integration import load_inputs, integrate
from new_passage_generation_pipeline import generate_experimental_candidate
import passage_stage5_integration as stage5

HERE=Path(__file__).resolve().parents[1]
TRIAL=HERE/"experiments/r6_17_ci_and_generation"


class PreselectedAuthorSingleDrawTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=json.loads((TRIAL/"trial_inputs_v1.json").read_text(encoding="utf-8"))
        cls.draw=json.loads((TRIAL/"author_draw_v1.json").read_text(encoding="utf-8"))
        cls.draft=json.loads((TRIAL/"model_authored_output_v1.json").read_text(encoding="utf-8"))
        cls.inputs=load_inputs()
        cls.inputs.update(topic=cls.plan["topic"],goals=cls.plan["goals"],evidence=cls.plan["evidence"])

    def test_preselected_draw_used_without_any_new_sampling_in_real_stage5(self):
        seen=[]
        def provider(request):
            seen.append(copy.deepcopy(request))
            return {"source_text":self.draft["source_text"],"questions":copy.deepcopy(self.draft["questions"])}
        with patch.object(stage5,"draw_author_attributes",side_effect=AssertionError("unexpected author reroll")):
            out=generate_experimental_candidate(
                self.inputs,passage_id=self.plan["passage_id"],
                passage_version=self.plan["passage_version"],
                provider=provider,allow_unverified_sources=True,
                author_selection_override=self.draw)
        self.assertEqual(out["status"],"READY_FOR_EDITORIAL_REVIEW")
        self.assertEqual(len(seen),1)
        self.assertEqual(out["stage5"]["author_selection"],self.draw)
        self.assertEqual(seen[0]["author_attributes_24"],self.draw["author_attributes_24"])
        qa=out["new_passage_qa"]
        self.assertEqual(len(qa["checks"]),17)
        self.assertEqual(qa["errors"],[])
        self.assertEqual(qa["warnings"],[])
        self.assertFalse(out["can_publish"])
        self.assertFalse(out["release_approved"])
        self.assertFalse(out["author_attributes_24_are_style_verified"])
        self.assertEqual(out["stage5"]["legacy_baseline_count"],30)

    def test_source_hold_with_preselected_draw_has_no_sampling_or_provider(self):
        def provider(_):
            raise AssertionError("provider must not be invoked while sources pending")
        with patch.object(stage5,"draw_author_attributes",side_effect=AssertionError("unexpected author reroll")):
            result=generate_experimental_candidate(
                self.inputs,passage_id=self.plan["passage_id"],
                passage_version=self.plan["passage_version"],
                provider=provider,author_selection_override=self.draw)
        self.assertEqual(result["status"],"HOLD_SOURCE_VERIFICATION")
        self.assertFalse(result["provider_called"])
        self.assertFalse(result["can_publish"])

    def test_override_and_seed_are_mutually_exclusive(self):
        with self.assertRaises(ValueError):
            generate_experimental_candidate(
                self.inputs,passage_id=self.plan["passage_id"],
                provider=lambda x:x,seed=101,
                author_selection_override=self.draw,allow_unverified_sources=True)

    def test_incorrect_preselected_attribute_is_rejected_without_provider_call(self):
        corrupt=copy.deepcopy(self.draw)
        key=next(iter(corrupt["author_attributes_24"]))
        corrupt["author_attributes_24"][key]="NOT_IN_APPROVED_POOL"
        with self.assertRaises(ValueError):
            generate_experimental_candidate(
                self.inputs,passage_id=self.plan["passage_id"],
                provider=lambda _: (_ for _ in ()).throw(AssertionError("provider called")),
                author_selection_override=corrupt,allow_unverified_sources=True)


if __name__=="__main__":
    unittest.main()
