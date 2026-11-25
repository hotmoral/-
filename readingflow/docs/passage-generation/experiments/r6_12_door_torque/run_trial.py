"""R6.12 -- run a genuine Stage5 -> generator-provider -> 17QA offline pipeline
on the fresh model-authored candidate. The provider supplies a previously generated
draft; it does NOT call the paid live API. No release approval is possible.
"""
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
TOOLS=HERE.parents[1]/"tools"
sys.path.insert(0,str(TOOLS))
from passage_stage5_integration import load_inputs
from author_attribute_sampler import ATTRIBUTE_NAMES, verify_selection
from new_passage_generation_pipeline import generate_experimental_candidate

def load_trial():
    plan=json.loads((HERE/"trial_inputs_v1.json").read_text(encoding="utf-8"))
    sample=json.loads((HERE/"model_authored_output_v1.json").read_text(encoding="utf-8"))
    inputs=load_inputs()
    inputs.update(topic=plan["topic"],goals=plan["goals"],evidence=plan["evidence"])
    return plan,sample,inputs

def run_trial():
    plan,sample,inputs=load_trial()
    # A deterministic snapshot detects accidental mutation of the original planning
    # and legacy records while exercising the actual Stage5 code.
    input_snapshot=json.dumps(inputs,ensure_ascii=False,sort_keys=True)
    calls=[]
    def provider(request):
        calls.append(request)
        if request["passage_id"]!=sample["passage_id"]:
            raise ValueError("provider request passage mismatch")
        return {"source_text":sample["source_text"],"questions":sample["questions"]}
    blocked=generate_experimental_candidate(inputs,passage_id=plan["passage_id"],
                    passage_version=plan["passage_version"],seed=plan["seed"],provider=provider)
    assert blocked["status"]=="HOLD_SOURCE_VERIFICATION" and not blocked["provider_called"] and not calls
    result=generate_experimental_candidate(inputs,passage_id=plan["passage_id"],
                passage_version=plan["passage_version"],seed=plan["seed"],
                provider=provider,allow_unverified_sources=True)
    assert len(calls)==1,"provider should be called exactly once in explicit experimental mode"
    assert result["author_drawing_reused"] is True
    stage=result["stage5"]
    selection=stage["author_selection"]
    assert stage["legacy_baseline_count"]==30
    assert len(stage["stages"])==11
    assert [s["step"] for s in stage["stages"]]==list(range(1,12))
    assert stage["stages"][7]["state"]=="AI_GENERATED_EXPERIMENTAL_DRAFT"
    assert selection["selection_method"]=="python_mt19937_seeded_v1"
    assert selection["experimental_seed"]==plan["seed"]
    assert set(selection["author_attributes_24"])==set(ATTRIBUTE_NAMES)
    assert verify_selection(selection,inputs["pools"])
    assert selection["author_attributes_24"]==calls[0]["author_attributes_24"]
    assert selection["candidate_pools_sha256"]==calls[0]["author_candidate_pools_sha256"]
    assert len(result["new_passage_qa"]["checks"])==17
    assert not result["new_passage_qa"]["errors"]
    assert all(c["editorial_state"]=="NOT_REVIEWED" for c in result["new_passage_qa"]["checks"])
    assert result["author_attributes_24_are_style_verified"] is False
    assert stage["quality_report"]["can_release"] is False
    assert stage["release_approved"] is False
    assert json.dumps(inputs,ensure_ascii=False,sort_keys=True)==input_snapshot
    assert result["release_approved"] is False and result["can_publish"] is False
    assert result["source_validation_pending"] is True
    return {"default_source_gate":{"status":blocked["status"],"provider_called":False},
            "experimental_result":result,"provider_calls":len(calls),
            "stage5_genuine_module_tested_by_this_harness":True,
            "author_selection_transmitted_and_reused":True,
            "author_style_in_passage_verified":False,
            "note":"Offline previously authored draft used as injected provider; live AI not invoked. The script exercises the actual Stage5 module only when run."}

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    output=run_trial()
    doc=json.dumps(output,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        path=args.output.resolve()
        if path.exists(): parser.error("output exists; refusing overwrite")
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(doc,encoding="utf-8")
    print(json.dumps({"default_gate":output["default_source_gate"]["status"],
          "candidate_decision":output["experimental_result"]["status"],
          "qa_errors":len(output["experimental_result"]["new_passage_qa"]["errors"]),
          "qa_warnings":len(output["experimental_result"]["new_passage_qa"]["warnings"]),
          "provider_calls":output["provider_calls"],
          "publish":False},ensure_ascii=False))
