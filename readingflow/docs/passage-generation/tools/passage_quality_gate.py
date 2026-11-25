"""Separate quality-review gate. Checks metadata completeness, not semantic correctness."""
from collections import Counter

STATES={"NOT_REVIEWED","IN_REVIEW","PASS","REVISE","REJECT","NEEDS_HUMAN_REVIEW"}
SUMMARY_STATES={"PASS","REVISE","REJECT","NEEDS_HUMAN_REVIEW"}
RELEASE_FALSE=False
EDITORIAL_STATES={"NOT_REVIEWED","IN_REVIEW","PASS","REVISE","HOLD"}

def validate_quality_policy(policy):
    checks=policy.get("categories")
    if not isinstance(checks,list) or not checks:
        raise ValueError("quality categories required")
    codes=[c.get("code") for c in checks]
    if len(codes)!=len(set(codes)) or any(not isinstance(x,str) or not x for x in codes):
        raise ValueError("duplicate or invalid quality codes")
    if not any(c["code"]=="FACTUAL_ACCURACY" for c in checks):
        raise ValueError("factual accuracy gate required")
    if not any(c["code"]=="READING_OBJECTIVES" for c in checks):
        raise ValueError("reading objective gate required")
    if policy.get("release_approval_separate") is not True:
        raise ValueError("release decision must remain separate")
    sub=policy.get("editorial_subchecks",[])
    if not isinstance(sub,list):raise ValueError("editorial subchecks list required")
    ids=[x.get("code") for x in sub]
    if len(ids)!=len(set(ids)) or any(not isinstance(x,str) or not x for x in ids):
        raise ValueError("duplicate/invalid editorial subcheck codes")
    if any(x.get("parent_category") not in codes or x.get("scope") not in ("PASSAGE","PER_QUESTION") for x in sub):
        raise ValueError("bad editorial subcheck category/scope")
    return {c["code"]:c for c in checks}

def validate_quality_record(record,policy):
    standards=validate_quality_policy(policy)
    for key in ("passage_id","passage_version","topic_id","age_group","level"):
        if not isinstance(record.get(key),str) or not record[key].strip():
            raise ValueError("missing "+key)
    if record.get("quality_review_status") not in SUMMARY_STATES:
        raise ValueError("invalid overall review state")
    if record.get("release_approved") is not False:
        raise ValueError("QA cannot authorize release")
    checks=record.get("category_checks")
    if not isinstance(checks,list) or len(checks)!=len(standards):
        raise ValueError("quality check inventory incomplete")
    ids=[r.get("code") for r in checks]
    if len(set(ids))!=len(ids) or set(ids)!=set(standards):
        raise ValueError("wrong review categories")
    for r in checks:
        if r.get("state") not in STATES:raise ValueError("invalid category state")
        if not isinstance(r.get("evidence_refs"),list):raise ValueError("evidence list")
        if any(not isinstance(ref,str) or not ref.strip() for ref in r["evidence_refs"]):
            raise ValueError("empty evidence ref")
        if r["state"]=="PASS":
            if not isinstance(r.get("reviewer"),str) or not r["reviewer"].strip():
                raise ValueError("PASS requires named reviewer")
            if not r["evidence_refs"]:raise ValueError("PASS requires evidence links")
    # Existing pending examples remain valid; they are not editorial PASS.
    subpolicy=policy.get("editorial_subchecks",[])
    subchecks=record.get("editorial_checks")
    if subchecks is not None:
        if not isinstance(subchecks,list) or len(subchecks)!=len(subpolicy):
            raise ValueError("editorial subcheck inventory incomplete")
        seen=[x.get("code") for x in subchecks]
        if len(set(seen))!=len(seen) or set(seen)!={x["code"] for x in subpolicy}:
            raise ValueError("editorial subcheck codes mismatch")
        specs={x["code"]:x for x in subpolicy}
        for item in subchecks:
            if item.get("state") not in EDITORIAL_STATES:
                raise ValueError("invalid editorial subcheck state")
            if not isinstance(item.get("evidence_refs"),list):
                raise ValueError("editorial subcheck evidence list required")
            if any(not isinstance(x,str) or not x.strip() for x in item["evidence_refs"]):
                raise ValueError("invalid editorial evidence reference")
            if item["state"]=="PASS":
                if not isinstance(item.get("reviewer"),str) or not item["reviewer"].strip() or not item["evidence_refs"]:
                    raise ValueError("editorial PASS requires reviewer and evidence")
                if specs[item["code"]]["scope"]=="PER_QUESTION":
                    included=item.get("reviewed_question_ids")
                    if not isinstance(included,list) or not included or len(set(included))!=len(included):
                        raise ValueError("per-question editorial PASS requires reviewed IDs")
                    if any(not isinstance(q,str) or not q.strip() for q in included):
                        raise ValueError("invalid reviewed question IDs")
    if record["quality_review_status"]=="PASS":
        if subpolicy and subchecks is None:
            raise ValueError("overall PASS requires editorial subchecks")
        if subpolicy and any(x["state"]!="PASS" for x in subchecks):
            raise ValueError("overall PASS blocked by pending editorial subchecks")
        if subpolicy and any(
            set(x.get("reviewed_question_ids",[]))!=set(record.get("question_ids",[]))
            for x in subchecks
            if next(z for z in subpolicy if z["code"]==x["code"])["scope"]=="PER_QUESTION"
        ):
            raise ValueError("overall PASS requires per-question coverage")
        if subpolicy and not record.get("question_ids"):
            raise ValueError("overall PASS requires question IDs")
        if any(r["state"]!="PASS" for r in checks):
            raise ValueError("overall PASS requires all category reviews")
        if not record.get("source_facts_verified") or not record.get("questions_reviewed"):
            raise ValueError("overall PASS cannot skip facts or question review")
        if not isinstance(record.get("reviewer"),str) or not record["reviewer"].strip():
            raise ValueError("overall PASS requires reviewer")
    return True

def quality_gate(record,policy):
    validate_quality_record(record,policy)
    states=Counter(c["state"] for c in record["category_checks"])
    missing=[c["code"] for c in record["category_checks"] if c["state"]!="PASS"]
    unresolved=[c for c in record["category_checks"] if c["state"] in ("NOT_REVIEWED","IN_REVIEW","NEEDS_HUMAN_REVIEW")]
    editorial=record.get("editorial_checks") or []
    return {"structure_valid":True,"summary_status":record["quality_review_status"],
            "editorial_review_pending_codes":[x["code"] for x in editorial if x["state"]!="PASS"],
            "editorial_review_is_human_verified":False,
            "category_states":dict(states),"review_needed_codes":missing,
            "unreviewed_categories":len(unresolved),
            "can_release":False,
            "automatic_fact_validation_performed":False,
            "warning":"Evidence refs and reviewer fields are claims; metadata checking alone does not prove real review or passage quality."}
