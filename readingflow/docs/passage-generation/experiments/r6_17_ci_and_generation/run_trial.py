"""R6.17 controlled chat-model-authored passage -> real Stage5 -> 17-item QA.

This replays a manuscript authored in a ChatGPT conversation AFTER the
preselected draw. It does not call OpenAI's paid Responses API. Test only.
"""
from __future__ import annotations
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
TOOLS=HERE.parents[1]/"tools"
sys.path.insert(0,str(TOOLS))

import passage_stage5_integration as stage5
from passage_stage5_integration import integrate,load_inputs
from new_passage_generation_pipeline import generate_experimental_candidate,create_generation_request


def load_trial():
    plan=json.loads((HERE/"trial_inputs_v1.json").read_text(encoding="utf-8"))
    selection=json.loads((HERE/"author_draw_v1.json").read_text(encoding="utf-8"))
    candidate=json.loads((HERE/"model_authored_output_v1.json").read_text(encoding="utf-8"))
    inputs=load_inputs()
    inputs.update(topic=plan["topic"],goals=plan["goals"],evidence=plan["evidence"])
    return plan,selection,candidate,inputs


def run_trial():
    plan,selection,candidate,inputs=load_trial()
    fingerprint=json.dumps(inputs,ensure_ascii=False,sort_keys=True)
    assert candidate["passage_id"]==selection["passage_id"]==plan["passage_id"]
    assert candidate["passage_version"]==plan["passage_version"]
    assert hashlib.sha256(candidate["source_text"].encode()).hexdigest()==candidate["source_text_sha256"]
    calls=[]

    def provider(request):
        calls.append(deepcopy(request))
        return {"source_text":candidate["source_text"],"questions":deepcopy(candidate["questions"])}

    # A genuine author's preselection is supplied. Never sample a second time.
    with patch.object(stage5,"draw_author_attributes",side_effect=AssertionError("author reroll forbidden")):
        blocked=generate_experimental_candidate(
            inputs,passage_id=plan["passage_id"],passage_version=plan["passage_version"],
            provider=provider,author_selection_override=selection)
        output=generate_experimental_candidate(
            inputs,passage_id=plan["passage_id"],passage_version=plan["passage_version"],
            provider=provider,allow_unverified_sources=True,
            author_selection_override=selection)
        # Independently rebuild the formal generation request from the same
        # preselection, still without an extra draw.
        preflight=integrate(inputs,passage_id=plan["passage_id"],
                            author_selection_override=selection)
        request=create_generation_request(inputs,preflight,
                    passage_id=plan["passage_id"],passage_version=plan["passage_version"])

    assert blocked["status"]=="HOLD_SOURCE_VERIFICATION"
    assert blocked["provider_called"] is False
    assert len(calls)==1
    assert output["provider_called"] is True
    assert output["status"]=="READY_FOR_EDITORIAL_REVIEW"
    assert output["stage5"]["author_selection"]==selection
    assert request==calls[0]
    assert output["author_drawing_reused"] is True
    assert len(selection["author_attributes_24"])==24
    assert len(output["stage5"]["stages"])==11
    assert output["stage5"]["legacy_baseline_count"]==30
    qa=output["new_passage_qa"]
    assert qa["checklist_count"]==len(qa["checks"])==17
    assert qa["errors"]==[]
    assert qa["warnings"]==[]
    assert len(qa["questions"])==3
    assert all(q["source_quote_literal"] for q in qa["questions"])
    assert all(q["surface_flags"]==[] for q in qa["questions"])
    assert all(c["editorial_state"]=="NOT_REVIEWED" for c in qa["checks"])
    assert not any((output["can_publish"],output["release_approved"],qa["human_validated"],qa["semantic_uniqueness_validated"]))
    assert json.dumps(inputs,ensure_ascii=False,sort_keys=True)==fingerprint
    return {
        "schema_version":"readingflow.r617.live_stage5_offline_model_draft.v1",
        "passage_id":plan["passage_id"],
        "passage_version":plan["passage_version"],
        "text_sha256":candidate["source_text_sha256"],
        "chars_without_whitespace":len("".join(candidate["source_text"].split())),
        "paragraphs":len(candidate["source_text"].split("\n\n")),
        "question_count":len(candidate["questions"]),
        "correct_option_labels":[q["correct_option"] for q in candidate["questions"]],
        "stage5_steps":len(output["stage5"]["stages"]),
        "legacy_passages_untouched":output["stage5"]["legacy_baseline_count"],
        "author_attributes_count":len(selection["author_attributes_24"]),
        "author_selection_reused_exactly":output["stage5"]["author_selection"]==selection,
        "additional_draws":0,
        "source_default_status":blocked["status"],
        "experimental_status":output["status"],
        "provider_calls":len(calls),
        "qa_checks":len(qa["checks"]),"qa_errors":len(qa["errors"]),"qa_warnings":len(qa["warnings"]),
        "structural_evidence_literals":sum(bool(q["source_quote_literal"]) for q in qa["questions"]),
        "human_validated":False,"learner_validated":False,
        "author_style_verified_by_human":False,
        "factual_sources_independently_verified":False,
        "live_openai_api_called":False,
        "model_written_in_chat_after_draw":True,
        "release_approved":False,"can_publish":False,
        "note":"Real Stage5 and 17-item QA; source fact, Korean editorial, meaning, learner and rights validation still pending."
    },request


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--summary-output",type=Path)
    parser.add_argument("--request-output",type=Path)
    args=parser.parse_args()
    summary,request=run_trial()
    for path,obj in ((args.summary_output,summary),(args.request_output,request)):
        if path:
            if path.exists():parser.error(f"output already exists: {path}")
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
