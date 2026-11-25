"""R6.11 experimental new content generation (explicit live opt-in only).

Example (unverified sources are EXPLICITLY experimental, not publishing):
  python run_new_passage_experiment.py --passage-id RF-NEW-001 \
    --draft-version draft-v1 --live-ai --allow-unverified-sources --output /tmp/new.json
"""
import argparse
import json
from pathlib import Path
from passage_stage5_integration import load_inputs
from new_passage_generation_pipeline import generate_experimental_candidate


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--passage-id",required=True)
    p.add_argument("--draft-version",default="new-draft-v1")
    p.add_argument("--seed",type=int)
    p.add_argument("--output",required=True)
    p.add_argument("--live-ai",action="store_true")
    p.add_argument("--allow-unverified-sources",action="store_true")
    args=p.parse_args()
    output=Path(args.output).resolve()
    if args.live_ai:
        from openai_new_passage_adapter import openai_generate_new_passage
        provider=openai_generate_new_passage
    else:
        def provider(request):
            raise RuntimeError("offline mode: no generator provider called")
    try:
        result=generate_experimental_candidate(
            load_inputs(),passage_id=args.passage_id,seed=args.seed,
            passage_version=args.draft_version,provider=provider,
            allow_unverified_sources=args.allow_unverified_sources,
        )
    except (ValueError,TypeError,RuntimeError,OSError) as exc:
        p.exit(1,"generation failed: "+str(exc)+"\n")
    # Never overwrite existing output; provider input is not a generated passage.
    if output.exists():
        p.error("output already exists; refusing to overwrite")
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"provider_called":result["provider_called"],
                      "can_publish":False,"output":str(output)},ensure_ascii=False))
    raise SystemExit(0 if result["status"]=="READY_FOR_EDITORIAL_REVIEW" else 2)


if __name__=="__main__":
    main()
