"""R6.14 regression: count actual Stage5 24-author draws on real repository inputs.

Unlike synthetic local R6.14 execution, these tests deliberately load canonical
JSON from the checked-out repository through run_trial.load_trial(). No live AI
request is made. This checks selection transport, NOT prose style realization.
"""
import copy
import unittest
from unittest.mock import patch

from run_trial import load_trial  # adds ../../tools to sys.path
import passage_stage5_integration as stage5
from new_passage_generation_pipeline import generate_experimental_candidate


class R614RealStage5DrawSpyTests(unittest.TestCase):
    def setUp(self):
        self.plan, self.sample, self.inputs = load_trial()
        self.before = copy.deepcopy(self.inputs)

    def _run(self, *, bad_answer=False, allow_unverified_sources=True):
        drawn = []
        submitted = []
        original = stage5.draw_author_attributes

        def track_draw(*args, **kwargs):
            picked = original(*args, **kwargs)
            drawn.append(picked)
            return picked

        def provider(request):
            submitted.append(request)
            payload = {
                "source_text": self.sample["source_text"],
                "questions": copy.deepcopy(self.sample["questions"]),
            }
            if bad_answer:
                # Existing correct content is not changed: deliberately corrupt
                # one label in this isolated test's returned candidate.
                payload["questions"][0]["correct_option"] = "A"
            return payload

        with patch.object(stage5, "draw_author_attributes", side_effect=track_draw):
            out = generate_experimental_candidate(
                self.inputs,
                passage_id=self.plan["passage_id"],
                passage_version=self.plan["passage_version"],
                seed=self.plan["seed"],
                provider=provider,
                allow_unverified_sources=allow_unverified_sources,
            )
        self.assertEqual(len(drawn), 1, "one draw per attempted generation")
        self.assertEqual(self.inputs, self.before, "caller inputs must not mutate")
        self.assertIs(out["release_approved"], False)
        self.assertIs(out["can_publish"], False)
        if submitted:
            self.assertEqual(len(submitted), 1)
            self.assertEqual(
                submitted[0]["author_attributes_24"],
                drawn[0]["author_attributes_24"],
            )
            self.assertEqual(
                out["stage5"]["author_selection"]["author_attributes_24"],
                drawn[0]["author_attributes_24"],
            )
            self.assertTrue(out["author_drawing_reused"])
            self.assertFalse(out["author_attributes_24_are_style_verified"])
        return out, drawn, submitted

    def test_explicit_experiment_single_draw_and_structural_ready(self):
        out, drawn, submitted = self._run()
        self.assertEqual(out["status"], "READY_FOR_EDITORIAL_REVIEW")
        self.assertEqual(len(out["new_passage_qa"]["checks"]), 17)
        self.assertEqual(len(out["new_passage_qa"]["errors"]), 0)
        self.assertTrue(out["source_validation_pending"])
        self.assertTrue(all(
            item["editorial_state"] == "NOT_REVIEWED"
            for item in out["new_passage_qa"]["checks"]
        ))

    def test_invalid_answer_no_reroll_and_revise(self):
        out, drawn, submitted = self._run(bad_answer=True)
        self.assertEqual(out["status"], "REVISE")
        codes = [x["code"] for x in out["new_passage_qa"]["errors"]]
        self.assertIn("ANSWER_MAPPING_INVALID", codes)

    def test_unverified_facts_hold_before_provider(self):
        out, drawn, submitted = self._run(allow_unverified_sources=False)
        self.assertEqual(out["status"], "HOLD_SOURCE_VERIFICATION")
        self.assertEqual(len(submitted), 0)
        self.assertFalse(out["provider_called"])


if __name__ == "__main__":
    unittest.main()
