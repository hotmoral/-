"""Optional live OpenAI Responses adapter, requires explicit opt-in and user env.

No API key or provider output is stored here. No background execution.
"""
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def openai_generate_new_passage(request):
    key=os.environ.get("OPENAI_API_KEY")
    model=os.environ.get("READINGFLOW_PASSAGE_MODEL")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    if not model:
        raise RuntimeError("READINGFLOW_PASSAGE_MODEL must be explicitly set")
    if request.get("mode")!="EXPERIMENT_ONLY":
        raise ValueError("only experimental generation is enabled")
    instruction=(
        "Generate ONE ORIGINAL Korean nonfiction text and 3-6 multiple-choice reading "
        "questions. Work only from the request's topic, reading goals, and proposed facts. "
        "Source facts may be UNVERIFIED: do not claim they were independently confirmed, "
        "do not add fabricated references or assert a quoted source you did not inspect. "
        "Be precise and natural in Korean; use age-group question conventions. "
        "Avoid nonsensical combinations and off-topic or obviously absurd distractors. "
        "For each question, make exactly 4 distinct options A-D and only one correct "
        "relative to the passage. Provide each wrong option's source-text quote and "
        "why it does not answer the question. Every evidence quote must be an EXACT "
        "substring of source_text. Give three distinct reading goals per three questions. "
        "Never alter passage_id, passage_version, age_group, level or author attributes. "
        "Never mark content approved; no publication. "
        "Return ONLY a JSON object with keys source_text and questions following "
        "required_response; do not wrap in markdown."
    )
    payload={
        "model":model,"instructions":instruction,
        "input":json.dumps(request,ensure_ascii=False),
        "text":{"format":{"type":"json_object"}},"store":False,
    }
    try:
        req=Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
            headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},
            method="POST",
        )
        with urlopen(req,timeout=120) as response:
            result=json.load(response)
    except (HTTPError,URLError) as exc:
        raise RuntimeError("new passage generation API call failed") from exc
    fragments=[
        item.get("text","")
        for out in result.get("output",[])
        if out.get("type")=="message"
        for item in out.get("content",[])
        if item.get("type")=="output_text"
    ]
    if not fragments:
        raise ValueError("provider returned no text output")
    doc=json.loads("".join(fragments))
    if not isinstance(doc,dict):
        raise ValueError("generation result must be JSON object")
    return doc
