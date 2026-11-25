"""R6.16: full canonical-input offline end-to-end Stage5 + generator + 17 QA.

Load actual repository JSON files through load_inputs(); use only an injected
synthetic provider (not a paid live model). Verify no approval or mutation.
This is a STRUCTURAL integration test, NOT fact/semantic/learner validation.
"""
import copy
import unittest
from unittest.mock import patch

from passage_stage5_integration import load_inputs, integrate
from new_passage_generation_pipeline import generate_experimental_candidate
from test_new_passage_generation_pipeline import response_for
import passage_stage5_integration as stage5


class CanonicalStage5EndToEnd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = load_inputs()  # repository original input paths, no fixtures
        cls.passage_id = "RF-R616-CANONICAL-E2E-001"

    def test_real_repository_input_inventory_and_11_stage_preflight(self):
        src = self.inputs
        self.assertEqual(len(src["legacy_catalog"]["records"]), 30)
        self.assertEqual(len(src["legacy_mapping"]["records"]), 30)
        self.assertEqual(len(src["taxonomy"]["domains"]), 18)
        self.assertEqual(sum(len(d["subfields"]) for d in src["taxonomy"]["domains"]), 298)
        self.assertEqual(len(src["pools"]), 24)
        self.assertEqual(sum(len(x) for x in src["pools"].values()), 172)
        pre = integrate(src, passage_id=self.passage_id, seed=2026112402)
        self.assertEqual([x["step"] for x in pre["stages"]], list(range(1, 12)))
        self.assertEqual(pre["legacy_baseline_count"], 30)
        self.assertEqual(pre["stages"][6]["state"], "DRAWN_WITHOUT_REROLL")
        self.assertEqual(pre["stages"][7]["state"], "NOT_STARTED_BLOCKED_FOR_PRODUCTION")
        self.assertFalse(pre["sources_readiness"]["ready_for_verified_fact_drafting"])
        self.assertFalse(pre["can_publish"])
        self.assertFalse(pre["release_approved"])

    def test_block_then_explicit_offline_generate_once_and_17_qa(self):
        src = self.inputs
        before = copy.deepcopy(src)
        seen = []
        draws = []
        actual_draw = stage5.draw_author_attributes

        def draw_spy(*args, **kwargs):
            chosen = actual_draw(*args, **kwargs)
            draws.append(copy.deepcopy(chosen))
            return chosen

        def provider(request):
            seen.append(copy.deepcopy(request))
            return response_for(request)

        with patch.object(stage5, "draw_author_attributes", side_effect=draw_spy):
            blocked = generate_experimental_candidate(
                src, passage_id=self.passage_id, provider=provider, seed=2026112402)
            out = generate_experimental_candidate(
                src, passage_id=self.passage_id, provider=provider, seed=2026112402,
                allow_unverified_sources=True)

        self.assertEqual(blocked["status"], "HOLD_SOURCE_VERIFICATION")
        self.assertFalse(blocked["provider_called"])
        self.assertEqual(len(seen), 1)
        self.assertEqual(len(draws), 2, "one independent selection per attempt, never rerolled")
        self.assertEqual(out["status"], "READY_FOR_EDITORIAL_REVIEW")
        self.assertTrue(out["author_drawing_reused"])
        self.assertEqual(out["stage5"]["author_selection"], draws[-1])
        self.assertEqual(seen[0]["author_attributes_24"], draws[-1]["author_attributes_24"])
        self.assertEqual(out["stage5"]["legacy_baseline_count"], 30)
        self.assertEqual(len(out["stage5"]["stages"]), 11)
        self.assertEqual(out["stage5"]["stages"][7]["state"], "AI_GENERATED_EXPERIMENTAL_DRAFT")
        qa = out["new_passage_qa"]
        self.assertEqual(len(qa["checks"]), 17)
        self.assertEqual(qa["errors"], [])
        # The intentionally simplistic legacy test provider has three
        # option-length/absolute-word advisory warnings. Do not hide them.
        self.assertEqual(len(qa["warnings"]), 3)
        self.assertEqual({w["code"] for w in qa["warnings"]}, {"OPTION_SURFACE_CUE"})
        self.assertTrue(all(row["editorial_state"] == "NOT_REVIEWED" for row in qa["checks"]))
        self.assertFalse(qa["semantic_uniqueness_validated"])
        self.assertFalse(qa["human_validated"])
        self.assertFalse(out["author_attributes_24_are_style_verified"])
        self.assertFalse(out["can_publish"])
        self.assertFalse(out["release_approved"])
        self.assertEqual(src, before, "canonical in-memory input data must not mutate")

    def test_bad_correct_answer_revise_with_no_author_reroll(self):
        count = []
        orig_draw = stage5.draw_author_attributes

        def draw_spy(*args, **kwargs):
            count.append(1)
            return orig_draw(*args, **kwargs)

        def bad_provider(request):
            doc = response_for(request)
            doc["questions"][0]["correct_option"] = "A"
            return doc

        with patch.object(stage5, "draw_author_attributes", side_effect=draw_spy):
            out = generate_experimental_candidate(
                self.inputs, passage_id=self.passage_id, seed=2026112402,
                provider=bad_provider, allow_unverified_sources=True)
        self.assertEqual(out["status"], "REVISE")
        self.assertEqual(count, [1])
        self.assertIn("ANSWER_MAPPING_INVALID", {x["code"] for x in out["new_passage_qa"]["errors"]})
        self.assertFalse(out["can_publish"])


if __name__ == "__main__":
    unittest.main()
