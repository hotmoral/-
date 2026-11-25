"""Stage 5 integrated nonfiction experimental workflow.

Strict scope:
- Forward topic selection -> objective -> source/fact registry -> independent author draw.
- Experimental pre-existing draft attachment, editorial QA, and independent diversity review.
- NEVER generate/approve a publishable passage, verify internet sources, infer prose quality,
  change taxonomy/pools, reroll author attributes, or write files.
"""
from __future__ import annotations
import hashlib
import json
from copy import deepcopy
from pathlib import Path

from author_attribute_sampler import (
    ATTRIBUTE_NAMES, draw_author_attributes, verify_selection, validate_pools)
from passage_goal_contract import validate_goal_plan
from passage_evidence_contract import planning_readiness
from passage_quality_gate import quality_gate
from new_passage_qa_gate import evaluate_new_candidate
from passage_duplication_diversity import audit_corpus
from topic_taxonomy_v2_contract import validate_topic_record_v2, validate_legacy_mapping

ROOT=Path(__file__).resolve().parents[1]
MODE="EXPERIMENT"
VERSION="readingflow.stage5_integrated_experiment.v1"


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_inputs():
    plan=ROOT/"planning"
    operations=ROOT/"operations"
    return {
        "taxonomy":_read(plan/"topic_taxonomy_proposal_v2.json"),
        "topic":_read(plan/"examples"/"topic_condensation_v2.json"),
        "goals":_read(plan/"examples"/"reading_goals_condensation_v1.json"),
        "evidence":_read(plan/"examples"/"facts_condensation_v1.json"),
        "pools":_read(ROOT/"data"/"author_attribute_candidate_pools_proposal_v1.json")["pools"],
        "quality_policy":_read(operations/"quality"/"quality_policy_v1.json"),
        "diversity_policy":_read(operations/"diversity"/"diversity_policy_v1.json"),
        "legacy_catalog":_read(ROOT/"data"/"normalized_passage_catalog_30_v1.json"),
        "legacy_mapping":_read(plan/"topic_catalog_30_provisional_v2.json"),
    }


def _legacy_rows(mapping):
    return [
        {"passage_id":r["passage_id"],"title":r["topic"],
         "primary_domain":r["primary_domain"],
         "age_group":r["source_age_group"],"level":r["source_level"]}
        for r in mapping["records"]
    ]


def _quality_record(policy,*,passage_id,version,topic,fulltext):
    text_hash=(hashlib.sha256(fulltext.encode("utf-8")).hexdigest()
               if fulltext is not None else None)
    return {
        "schema_version":"readingflow.passage_quality_record.v1",
        "passage_id":passage_id,
        "passage_version":version,
        "topic_id":topic["topic_id"],
        "age_group":topic["age_group"],"level":topic["level"],
        "quality_review_status":"NEEDS_HUMAN_REVIEW",
        "release_approved":False,
        "content_hash":text_hash,
        "reviewer":None,
        "source_facts_verified":False,
        "questions_reviewed":False,
        "learner_difficulty_validated":False,
        "category_checks":[{"code":c["code"],"state":"NOT_REVIEWED",
                            "reviewer":None,"evidence_refs":[],
                            "notes":"실제 독립 검수 전"}
                           for c in policy["categories"]],
        "editorial_subchecks_contract":policy.get("editorial_subchecks_contract"),
        "editorial_checks":[{"code":c["code"],"state":"NOT_REVIEWED",
                             "reviewer":None,"evidence_refs":[],
                             "notes":"연령별 형식·발문·사실 표현은 사람 검수 전"}
                            for c in policy.get("editorial_subchecks",[])],
    }


def _check_draft(draft,passage_id,topic):
    if draft is None:
        return None
    if not isinstance(draft,dict):
        raise ValueError("draft must be a mapping")
    if draft.get("passage_id")!=passage_id or draft.get("topic_id")!=topic["topic_id"]:
        raise ValueError("draft passage_id/topic_id mismatch")
    if draft.get("source_tag") not in ("P2_EXISTING_EXPERIMENTAL_DRAFT", "MANUALLY_SUPPLIED_EXPERIMENTAL_DRAFT", "AI_GENERATED_EXPERIMENTAL_DRAFT"):
        raise ValueError("draft provenance is not declared as experimental")
    if not isinstance(draft.get("text"),str) or not draft["text"].strip():
        raise ValueError("draft requires actual nonblank text")
    version=draft.get("passage_version")
    if not isinstance(version,str) or not version.strip():
        raise ValueError("draft version is required")
    if draft.get("release_approved") is not False:
        raise ValueError("experimental draft is not release approved")
    return draft


def integrate(inputs,*,passage_id,seed=None,draft=None,question_bundle=None,author_selection_override=None,mode=MODE):
    """Produce only a structural editorial work record, not a publishable passage.

    When seed is None the source sampler uses system CSPRNG; a supplied nonnegative integer
    enables reproducible *experiments* only. No topic/quality-based conditioning or reroll.
    """
    if mode!="EXPERIMENT":
        raise ValueError("Only EXPERIMENT mode implemented; verified production not available")
    if not isinstance(passage_id,str) or not passage_id.strip():
        raise ValueError("passage_id is required")
    for required in ("taxonomy","topic","goals","evidence","pools",
                     "quality_policy","diversity_policy","legacy_catalog","legacy_mapping"):
        if required not in inputs:
            raise ValueError("missing stage-5 input: "+required)

    taxonomy=inputs["taxonomy"]
    topic=inputs["topic"]
    goals=inputs["goals"]
    evidence=inputs["evidence"]
    validate_topic_record_v2(topic,taxonomy)  # includes required forward-order audit trail
    validate_goal_plan(goals,topic,evidence)
    source_gate=planning_readiness(topic,goals,evidence)

    validate_pools(inputs["pools"])
    if inputs["diversity_policy"].get("no_adjustment_to_author_rng") is not True:
        raise ValueError("diversity policy may not modify independent author sampling")

    legacy_result=validate_legacy_mapping(inputs["legacy_mapping"],
                                           inputs["legacy_catalog"],taxonomy)
    rows=_legacy_rows(inputs["legacy_mapping"])
    declared_overlap=topic["overlap_review"].get("possible_matches",[])
    known_ids=[match["passage_id"] for match in declared_overlap]
    diversity_candidate={
        "topic_id":topic["topic_id"],"title":topic["title"],
        "known_possible_matches":known_ids,
    }
    diversity_report=audit_corpus(rows,diversity_candidate)
    if diversity_report["auto_rejected"]!=0:
        raise ValueError("diversity management must not auto reject content")

    # Forward-selection trace was fully validated before the draw.
    if author_selection_override is not None:
        # Reuse the sole draw made before calling the generator; never sample again.
        if seed is not None:
            raise ValueError("seed and author_selection_override cannot be combined")
        if not isinstance(author_selection_override,dict):
            raise ValueError("author_selection_override must be a mapping")
        selection=deepcopy(author_selection_override)
        if selection.get("passage_id")!=passage_id or selection.get("release_approved") is not False:
            raise ValueError("preselected author attributes must match this passage and be unapproved")
        if set(selection.get("attribute_application_log",{}))!=set(ATTRIBUTE_NAMES):
            raise ValueError("preselected author application log incomplete")
    else:
        selection=draw_author_attributes(passage_id,inputs["pools"],seed=seed)
    if not verify_selection(selection,inputs["pools"]):
        raise ValueError("author draw provenance unexpectedly invalid")
    if set(selection["author_attributes_24"])!=set(ATTRIBUTE_NAMES):
        raise ValueError("24 author attributes required")

    draft=_check_draft(draft,passage_id,topic)
    text=draft["text"] if draft else None
    draft_version=draft["passage_version"] if draft else "pending-draft-v0"
    qa_record=_quality_record(inputs["quality_policy"],passage_id=passage_id,
                              version=draft_version,topic=topic,fulltext=text)
    qa_report=quality_gate(qa_record,inputs["quality_policy"])
    # R6.10 executable 17-item gate. Never promotes editorial PASS.
    candidate={"passage_id":passage_id,"passage_version":draft_version,
               "source_text":text,"age_group":topic["age_group"],
               "level":topic["level"],"questions":None,
               "release_approved":False}
    if question_bundle is not None:
        if not isinstance(question_bundle,dict):
            raise ValueError("question_bundle must be object")
        for field in ("passage_id","passage_version","source_text","age_group","level"):
            if question_bundle.get(field)!=candidate[field]:
                raise ValueError("question_bundle "+field+" mismatches source")
        if question_bundle.get("release_approved") is True:
            raise ValueError("question bundle cannot self-approve")
        candidate["questions"]=question_bundle.get("questions")
    new_passage_qa=evaluate_new_candidate(candidate,author_selection=selection)
    if qa_report["can_release"] or qa_record["release_approved"]:
        raise ValueError("internal QA must never auto approve release")
    if any(x["status"]!="PENDING" for x in selection["attribute_application_log"].values()):
        raise ValueError("unreviewed author choices must remain pending")

    source_blocked=(not source_gate["ready_for_verified_fact_drafting"])
    pending_overlap=topic["overlap_review"]["status"]!="REVIEWED_SEPARATE"
    pending=["SOURCE_EVIDENCE_REVIEW"] if source_blocked else []
    if pending_overlap:pending.append("TOPIC_DUPLICATION_EDITORIAL_REVIEW")
    pending.append("NEW_PASSAGE_17_ITEM_QA")
    pending.extend(["OBJECTIVE_EVIDENCE_EDITORIAL_REVIEW",
                    "PROSE_AND_STYLE_EDITORIAL_REVIEW","QUESTION_GENERATION_AND_REVIEW",
                    "AGE_FORM_AND_QUESTION_LANGUAGE_EDITORIAL_REVIEW",
                    "CLAIM_MODALITY_AND_CAUSATION_EDITORIAL_REVIEW",
                    "AGE_LEVEL_VALIDATION","RIGHTS_AND_RELEASE_APPROVAL"])
    stages=[
        {"step":1,"name":"SELECT_PRIMARY_DOMAIN","state":"SELECTED_AND_TRACE_VALIDATED",
         "value":topic["primary_domain"]},
        {"step":2,"name":"SELECT_SUBFIELD","state":"SELECTED_AND_TRACE_VALIDATED",
         "value":topic["subfield"]},
        {"step":3,"name":"SELECT_INDIVIDUAL_TOPIC","state":"SELECTED_AND_TRACE_VALIDATED",
         "value":topic["topic_focus"]},
        {"step":4,"name":"DEFINE_CORE_QUESTION","state":"DEFINED_AND_TRACE_VALIDATED",
         "value":topic["core_question"]},
        {"step":5,"name":"DEFINE_READING_OBJECTIVES","state":"STRUCTURE_CHECKED_NOT_SEMANTICALLY_VALIDATED",
         "objective_ids":[g["objective_id"] for g in goals["objectives"]]},
        {"step":6,"name":"COLLECT_AND_REVIEW_SOURCE_FACTS",
         "state":"UNVERIFIED_SOURCES_BLOCK_PRODUCTION" if source_blocked else "METADATA_REVIEW_COMPLETE_NOT_TRUTH_CERTIFIED",
         "unresolved_fact_ids":source_gate["fact_review_pending_ids"]},
        {"step":7,"name":"SAMPLE_24_AUTHOR_ATTRIBUTES","state":"DRAWN_WITHOUT_REROLL",
         "method":selection["selection_method"]},
        {"step":8,"name":"DRAFT_NONFICTION","state":(("AI_GENERATED_EXPERIMENTAL_DRAFT" if draft["source_tag"]=="AI_GENERATED_EXPERIMENTAL_DRAFT" else "EXPERIMENTAL_EXISTING_DRAFT_ONLY") if draft else "NOT_STARTED_BLOCKED_FOR_PRODUCTION"),
         "source_tag":draft["source_tag"] if draft else None},
        {"step":9,"name":"QUALITY_REVIEW","state":"PENDING_INDEPENDENT_CONTENT_REVIEW",
         "review_categories":len(inputs["quality_policy"]["categories"])},
        {"step":10,"name":"DUPLICATION_AND_DIVERSITY","state":"STRUCTURAL_FLAGS_ONLY",
         "known_possible_overlap_count":len(known_ids)},
        {"step":11,"name":"PRODUCTION_RELEASE","state":"BLOCKED_NOT_IMPLEMENTED"},
    ]
    return {
        "schema_version":VERSION,
        "mode":mode,
        "experiment_only":True,
        "passage_id":passage_id,
        "topic_id":topic["topic_id"],
        "taxonomy_version":topic["taxonomy_version"],
        "age_group":topic["age_group"],"level":topic["level"],
        "selection_trace":topic["selection_trace"],
        "source_registry_id":evidence["registry_id"],
        "objective_ids":[g["objective_id"] for g in goals["objectives"]],
        "stages":stages,
        "sources_readiness":source_gate,
        "author_selection":selection,
        "draft_provenance":({
            "source_tag":draft["source_tag"],
            "passage_version":draft_version,
            "text_sha256":qa_record["content_hash"],
            "chars_no_whitespace":len("".join(text.split())),
            "text_provided":True,
            "note":"Experimental draft supplied (pre-existing or AI-generated); 24 selected author styles are NOT proved applied."
        } if draft else {"text_provided":False,"passage_version":draft_version}),
        "quality_record":qa_record,
        "quality_report":qa_report,
        "new_passage_qa":new_passage_qa,
        "diversity_report":diversity_report,
        "legacy_baseline_count":legacy_result["mapped"],
        "pending_reviews":pending,
        "can_publish":False,
        "release_approved":False,
        "no_content_or_pool_mutation":True,
        "warning":"Structural pipeline only; unverified sources, educational effectiveness, style implementation and semantic duplication remain unchecked.",
    }


def experimental_example():
    inputs=load_inputs()
    contrasts=_read(ROOT/"experiments"/"author_role_contrasts"/"contrasts.json")
    existing=contrasts["comparisons"][0]["left"]["text"]
    passage_id="RF-STAGE5-EXPERIMENT-CONDENSATION-0001"
    draft={
        "passage_id":passage_id,"topic_id":inputs["topic"]["topic_id"],
        "passage_version":"trial-p2-v1",
        "source_tag":"P2_EXISTING_EXPERIMENTAL_DRAFT",
        "text":existing,"release_approved":False,
    }
    return integrate(inputs,passage_id=passage_id,seed=2026112001,draft=draft)


if __name__=="__main__":
    print(json.dumps(experimental_example(),ensure_ascii=False,indent=2))
