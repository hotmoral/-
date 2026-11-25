"""Stage 5 end-to-end structural regression tests (no release/semantics claims)."""
import hashlib
import json
import unittest
from copy import deepcopy
from pathlib import Path
from author_attribute_sampler import ATTRIBUTE_NAMES, verify_selection
from passage_stage5_integration import load_inputs, integrate, experimental_example, ROOT

class Stage5IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs=load_inputs()
        cls.passage_id="RF-STAGE5-EXPERIMENT-CONDENSATION-0001"
        cls.result=experimental_example()

    def test_complete_forward_pipeline_has_all_11_steps(self):
        r=self.result
        self.assertEqual(len(r["stages"]),11)
        self.assertEqual([s["name"] for s in r["stages"][:4]],
                         ["SELECT_PRIMARY_DOMAIN","SELECT_SUBFIELD",
                          "SELECT_INDIVIDUAL_TOPIC","DEFINE_CORE_QUESTION"])
        self.assertEqual([x["step"] for x in r["selection_trace"]],
                         ["PRIMARY_DOMAIN","SUBFIELD","INDIVIDUAL_TOPIC","CORE_QUESTION"])
        self.assertEqual(r["legacy_baseline_count"],30)

    def test_author_24_choices_remain_independent_seeded_without_reroll(self):
        r=self.result
        selection=r["author_selection"]
        self.assertEqual(set(selection["author_attributes_24"]),set(ATTRIBUTE_NAMES))
        self.assertTrue(verify_selection(selection,self.inputs["pools"]))
        self.assertEqual(len(selection["attribute_application_log"]),24)
        self.assertTrue(all(x["status"]=="PENDING"
                            for x in selection["attribute_application_log"].values()))
        second=integrate(deepcopy(self.inputs),passage_id=self.passage_id,seed=2026112001)
        self.assertEqual(selection["author_attributes_24"],
                         second["author_selection"]["author_attributes_24"])
        different=integrate(self.inputs,passage_id=self.passage_id,seed=2026112002)
        self.assertNotEqual(selection["author_attributes_24"],
                            different["author_selection"]["author_attributes_24"])

    def test_unverified_source_blocks_production(self):
        r=self.result
        self.assertFalse(r["sources_readiness"]["ready_for_verified_fact_drafting"])
        self.assertEqual(len(r["sources_readiness"]["fact_review_pending_ids"]),6)
        self.assertIn("SOURCE_EVIDENCE_REVIEW",r["pending_reviews"])
        self.assertFalse(r["can_publish"])
        self.assertFalse(r["release_approved"])

    def test_draft_is_preexisting_and_hash_is_consistent(self):
        r=self.result
        self.assertEqual(r["draft_provenance"]["source_tag"],"P2_EXISTING_EXPERIMENTAL_DRAFT")
        self.assertTrue(r["draft_provenance"]["text_provided"])
        self.assertEqual(r["draft_provenance"]["text_sha256"],r["quality_record"]["content_hash"])
        raw=json.loads((ROOT/"experiments"/"author_role_contrasts"/"contrasts.json").read_text(encoding="utf8"))
        text=raw["comparisons"][0]["left"]["text"]
        self.assertEqual(hashlib.sha256(text.encode("utf8")).hexdigest(),
                         r["draft_provenance"]["text_sha256"])
        self.assertEqual(r["stages"][7]["state"],"EXPERIMENTAL_EXISTING_DRAFT_ONLY")

    def test_quality_and_diversity_are_separate_unapproved_reviews(self):
        r=self.result
        self.assertEqual(len(r["quality_record"]["category_checks"]),8)
        self.assertEqual(len(r["quality_report"]["review_needed_codes"]),8)
        self.assertFalse(r["quality_report"]["can_release"])
        self.assertEqual(r["diversity_report"]["auto_rejected"],0)
        self.assertEqual(r["diversity_report"]["corpus_count"],30)
        self.assertEqual(len([x for x in r["diversity_report"]["planned_topic_review_flags"]
             if x["type"]=="EXPLICIT_KNOWN_TOPIC_OVERLAP"]),1)
        self.assertEqual(r["diversity_report"]["exact_fulltext_checked_pairs"],0)

    def test_reject_reverse_topic_trace(self):
        inputs=deepcopy(self.inputs)
        trace=inputs["topic"]["selection_trace"]
        trace[0],trace[-1]=trace[-1],trace[0]
        with self.assertRaises(ValueError):integrate(inputs,passage_id=self.passage_id,seed=9)

    def test_reject_inconsistent_category_no_silent_reroute(self):
        inputs=deepcopy(self.inputs)
        inputs["topic"]["primary_domain"]="환경·생태"
        with self.assertRaises(ValueError):integrate(inputs,passage_id=self.passage_id,seed=9)

    def test_reject_missing_fact_referenced_by_reading_objective(self):
        inputs=deepcopy(self.inputs)
        inputs["goals"]["objectives"][0]["required_fact_ids"]=["F1","NOT_REAL"]
        with self.assertRaises(ValueError):integrate(inputs,passage_id=self.passage_id,seed=9)

    def test_reject_rogue_source_id(self):
        inputs=deepcopy(self.inputs)
        inputs["evidence"]["facts"][0]["source_refs"][0]["source_id"]="UNKNOWN"
        with self.assertRaises(ValueError):integrate(inputs,passage_id=self.passage_id,seed=9)

    def test_reject_missing_predeclared_known_overlap(self):
        inputs=deepcopy(self.inputs)
        inputs["topic"]["overlap_review"]["possible_matches"]=[{"passage_id":"NOT_IN_30","title":"unknown"}]
        with self.assertRaises(ValueError):integrate(inputs,passage_id=self.passage_id,seed=9)

    def test_reject_author_pool_mutation(self):
        inputs=deepcopy(self.inputs)
        inputs["pools"]["도입"].append(inputs["pools"]["도입"][0])
        with self.assertRaises(ValueError):integrate(inputs,passage_id=self.passage_id,seed=9)

    def test_reject_diversity_pressure_to_change_author_draw(self):
        inputs=deepcopy(self.inputs)
        inputs["diversity_policy"]["no_adjustment_to_author_rng"]=False
        with self.assertRaises(ValueError):integrate(inputs,passage_id=self.passage_id,seed=9)

    def test_production_mode_unavailable_even_if_seeded(self):
        with self.assertRaisesRegex(ValueError,"Only EXPERIMENT"):
            integrate(self.inputs,passage_id=self.passage_id,seed=9,mode="PRODUCTION")

    def test_reject_unapproved_draft_or_mismatched_identity(self):
        draft={"passage_id":self.passage_id,"topic_id":self.inputs["topic"]["topic_id"],
               "text":"실험용 글입니다.","source_tag":"MANUALLY_SUPPLIED_EXPERIMENTAL_DRAFT",
               "passage_version":"trial-v1","release_approved":False}
        x=integrate(self.inputs,passage_id=self.passage_id,seed=9,draft=draft)
        self.assertFalse(x["can_publish"])
        y=dict(draft,release_approved=True)
        with self.assertRaises(ValueError):integrate(self.inputs,passage_id=self.passage_id,seed=9,draft=y)
        y=dict(draft,topic_id="WRONG")
        with self.assertRaises(ValueError):integrate(self.inputs,passage_id=self.passage_id,seed=9,draft=y)

    def test_no_draft_does_not_claim_content(self):
        x=integrate(self.inputs,passage_id=self.passage_id,seed=9)
        self.assertFalse(x["draft_provenance"]["text_provided"])
        self.assertIsNone(x["quality_record"]["content_hash"])
        self.assertEqual(x["stages"][7]["state"],"NOT_STARTED_BLOCKED_FOR_PRODUCTION")
        self.assertEqual(x["stages"][-1]["state"],"BLOCKED_NOT_IMPLEMENTED")

if __name__=="__main__":unittest.main()
