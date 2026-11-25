"""R6.11 new Korean nonfiction generation interface wired to Stage5 and 17 QA checks.

One provider invocation (opt-in), one independently uniform 24-attribute draw,
no rerolls on quality problems. This module does NOT validate source truth or
copyright, and cannot publish content.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib

from passage_stage5_integration import integrate
from new_passage_qa_gate import present


def create_generation_request(inputs, preflight, *, passage_id, passage_version):
    """Pass planning context to a generator, marking unverified facts honestly."""
    topic, goals, facts = inputs["topic"], inputs["goals"], inputs["evidence"]
    selected = preflight["author_selection"]
    if selected["passage_id"] != passage_id:
        raise ValueError("preflight passage identity mismatch")
    source_map = {s["source_id"]:s for s in facts["sources"]}
    return {
        "request_schema":"readingflow.new_passage_generation_request.v1",
        "mode":"EXPERIMENT_ONLY",
        "passage_id":passage_id,
        "passage_version":passage_version,
        "age_group":topic["age_group"],
        "level":topic["level"],
        "topic":{
            "topic_id":topic["topic_id"], "primary_domain":topic["primary_domain"],
            "subfield":topic["subfield"],"topic_focus":topic["topic_focus"],
            "core_question":topic["core_question"],
        },
        "reading_goals":[{
            "objective_id":g["objective_id"],"operation":g["operation"],
            "learner_target":g["learner_target"],
            "key_question":g["key_question"],
            "expected_reasoning":g["expected_reasoning"],
            "required_fact_ids":list(g["required_fact_ids"]),
        } for g in goals["objectives"]],
        "source_fact_candidates":[{
            "fact_id":fact["fact_id"],"claim":fact["claim"],
            "verification_status":fact["verification_status"],
            "source_references":[{
                "source_id":ref["source_id"],"locator":ref.get("locator"),
                "source_check_status":source_map[ref["source_id"]]["source_check_status"],
            } for ref in fact["source_refs"]],
        } for fact in facts["facts"]],
        "facts_verified_by_this_pipeline":False,
        "unverified_fact_ids":list(preflight["sources_readiness"]["fact_review_pending_ids"]),
        "author_attributes_24":deepcopy(selected["author_attributes_24"]),
        "author_selection_method":selected["selection_method"],
        "author_candidate_pools_sha256":selected["candidate_pools_sha256"],
        "instructions":{
            "genre":"original_Korean_nonfiction_only",
            "age_appropriate_nonfiction":True,
            "plain_writing_ending":"~다/~이다/~한다",
            "word_count":"reference_only_natural_flow_first",
            "question_count_range":[3,6],
            "one_correct_four_choices":True,
            "question_goals_distinct":True,
            "every_distractor_must_be_falsifiable_by_passage":True,
            "each_wrong_option_reason_required":True,
            "literal_quotes_for_correct_and_wrong_reasons":True,
            "avoid_absurd_wrong_choices_and_ungrammatical_combinations":True,
            "check_correct_uniquely_shortest_and_longest":True,
            "safety_over_distractor_attractiveness":True,
            "no_copying_textbook_exam_copyrighted_passages":True,
            "no_invented_sources_or_verified_fact_claims":True,
            "prior_knowledge_guessability_is_not_quality_criterion":True,
            "final_release_approved":False,
        },
        "required_response":{
            "source_text":"new original Korean nonfiction full text",
            "questions":[{
                "question_id":"unique ID", "question":"age-appropriate complete question?",
                "question_type":"reading objective label", "question_goal":"distinct reading task",
                "answer":"exact correct option text", "correct_option":"A|B|C|D",
                "format":"single_choice","source_version":passage_version,
                "evidence":"exact substring of source_text",
                "explanation":"reason relative to passage",
                "options":[{"id":"A","text":"plausible but source-incompatible wrong choice"},
                           {"id":"B","text":"correct answer text"},
                           {"id":"C","text":"different plausible wrong choice"},
                           {"id":"D","text":"third plausible wrong choice"}],
                "distractor_grounding":[
                    {"option_id":"A","evidence":"exact source quote","false_reason":"why A is wrong"},
                    {"option_id":"C","evidence":"exact source quote","false_reason":"why C is wrong"},
                    {"option_id":"D","evidence":"exact source quote","false_reason":"why D is wrong"},
                ],
            }],
        },
        "release_approved":False,
    }


def generate_experimental_candidate(inputs, *, passage_id, provider, passage_version="new-draft-v1",
                                    seed=None, allow_unverified_sources=False,
                                    author_selection_override=None):
    """Return candidate and both QA reports; provider(request)->JSON-like mapping.

    Default source gate blocks the call; allow_unverified_sources explicitly
    permits ONLY an unapproved experimental candidate using proposed facts.
    Optional author_selection_override accepts ONE author draw previously made
    with Stage5 *before prose authorship*. Passing an override means this wrapper
    never samples the author attributes again. seed and override are exclusive.
    """
    if not callable(provider):
        raise TypeError("provider must be callable")
    if not present(passage_id) or not present(passage_version):
        raise ValueError("passage_id and passage_version required")
    if type(allow_unverified_sources) is not bool:
        raise TypeError("allow_unverified_sources must be bool")
    preflight=integrate(inputs,passage_id=passage_id,seed=seed,
                         author_selection_override=author_selection_override)
    readiness=preflight["sources_readiness"]
    pending=not readiness["ready_for_verified_fact_drafting"]
    if pending and not allow_unverified_sources:
        return {
            "schema_version":"readingflow.new_passage_generation_result.v1",
            "status":"HOLD_SOURCE_VERIFICATION",
            "provider_called":False,
            "candidate":None,
            "source_validation_pending":True,
            "blocked_unverified_fact_ids":list(readiness["fact_review_pending_ids"]),
            "preflight":preflight,
            "release_approved":False,"can_publish":False,
        }
    request=create_generation_request(inputs,preflight,passage_id=passage_id,
                                      passage_version=passage_version)
    proposed=provider(deepcopy(request))
    if not isinstance(proposed,dict):
        raise ValueError("provider must return a JSON object")
    # Model/provider output never chooses the immutable identity, approval or fact status.
    if proposed.get("release_approved") is True or proposed.get("can_publish") is True:
        raise ValueError("provider attempted unauthorized publication")
    for protected in ("passage_id","passage_version","age_group","level","topic_id"):
        expected=request["topic"]["topic_id"] if protected=="topic_id" else request.get(protected)
        if protected in proposed and proposed[protected]!=expected:
            raise ValueError("provider tried to change immutable "+protected)
    text=proposed.get("source_text")
    if not present(text):
        raise ValueError("provider response requires nonempty source_text")
    questions=proposed.get("questions")
    # Malformed questions are passed to the 17-item gate as REVISE; no auto-repair.
    candidate={
        "passage_id":passage_id,"passage_version":passage_version,
        "source_text":text,"source_text_sha256":hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "age_group":request["age_group"],"level":request["level"],
        "topic_id":request["topic"]["topic_id"],
        "questions":deepcopy(questions),
        "release_approved":False,
    }
    draft={
        "passage_id":passage_id,
        "topic_id":request["topic"]["topic_id"],
        "passage_version":passage_version,
        "source_tag":"AI_GENERATED_EXPERIMENTAL_DRAFT",
        "text":text,
        "release_approved":False,
    }
    integration=integrate(inputs,passage_id=passage_id,
                          author_selection_override=preflight["author_selection"],
                          draft=draft,question_bundle=candidate)
    if integration["author_selection"]!=preflight["author_selection"]:
        raise ValueError("preselected author draw unexpectedly changed")
    qa=integration["new_passage_qa"]
    return {
        "schema_version":"readingflow.new_passage_generation_result.v1",
        "status":qa["decision"],
        "provider_called":True,
        "provider_response_reviewed_for_safety":False,
        "candidate":candidate,
        "new_passage_qa":qa,
        "stage5":integration,
        "source_validation_pending":pending,
        "unverified_fact_ids":list(readiness["fact_review_pending_ids"]),
        "author_drawing_reused":True,
        "author_attributes_24_are_style_verified":False,
        "human_semantic_review":"NOT_RUN",
        "release_approved":False,
        "can_publish":False,
        "warning":"No factual/semantic/license approval. In unverified-source mode this is explicitly an experimental candidate.",
    }
