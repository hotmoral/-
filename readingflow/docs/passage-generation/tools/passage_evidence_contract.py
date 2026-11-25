"""Evidence registry contract: provenance structure, NOT fact truth certification."""
from passage_planning_contract import _text
from passage_goal_contract import validate_goal_plan

def validate_fact_registry(registry,topic):
    _text(registry.get("registry_id"),"registry id")
    if registry.get("topic_id")!=topic.get("topic_id"):raise ValueError("topic id mismatch")
    sources=registry.get("sources")
    facts=registry.get("facts")
    if not isinstance(sources,list) or not sources:raise ValueError("source list")
    if not isinstance(facts,list) or not facts:raise ValueError("fact list")
    source_ids=set()
    for source in sources:
        for key in ("source_id","organization","title","url"):_text(source.get(key),key)
        if not source["url"].startswith("https://"):raise ValueError("source URL must use HTTPS")
        if source["source_id"] in source_ids:raise ValueError("duplicate source ID")
        source_ids.add(source["source_id"])
        state=source.get("source_check_status")
        if state not in ("NOT_CHECKED_IN_THIS_STAGE","REVIEWED_BY_HUMAN"):
            raise ValueError("source review state")
        if state=="REVIEWED_BY_HUMAN":
            _text(source.get("checked_at"),"source review timestamp")
            _text(source.get("reviewer"),"source reviewer")
        if source.get("rights_review_status") not in ("NOT_CHECKED","REFERENCES_ONLY","CLEARED_FOR_REUSE"):
            raise ValueError("rights review status")
    fact_ids=set()
    for fact in facts:
        _text(fact.get("fact_id"),"fact id")
        _text(fact.get("claim"),"fact claim")
        if fact["fact_id"] in fact_ids:raise ValueError("duplicate fact ID")
        fact_ids.add(fact["fact_id"])
        refs=fact.get("source_refs")
        if not isinstance(refs,list) or not refs:raise ValueError("fact must have candidate evidence")
        seen=set()
        for ref in refs:
            if ref.get("source_id") not in source_ids:raise ValueError("unknown source ref")
            if ref["source_id"] in seen:raise ValueError("duplicate source ref")
            seen.add(ref["source_id"])
            if ref.get("locator") is not None:_text(ref["locator"],"source locator")
        status=fact.get("verification_status")
        if status not in ("PENDING_EXTERNAL_REVIEW","REVIEWED_BY_HUMAN"):
            raise ValueError("fact verification status")
        if status=="REVIEWED_BY_HUMAN":
            _text(fact.get("reviewer"),"fact reviewer")
            _text(fact.get("reviewed_at"),"fact review date")
            if not any(ref.get("locator") for ref in refs):
                raise ValueError("verified claim needs an exact source locator")
            if not all(s["source_check_status"]=="REVIEWED_BY_HUMAN"
                       for s in sources if s["source_id"] in seen):
                raise ValueError("cannot verify a fact against unchecked source")
    if registry.get("release_approved") is not False:raise ValueError("registry is not release approved")
    return True

def planning_readiness(topic,goals,registry):
    validate_fact_registry(registry,topic)
    validate_goal_plan(goals,topic,registry)
    pending_sources=[s["source_id"] for s in registry["sources"] if s["source_check_status"]!="REVIEWED_BY_HUMAN"]
    pending_facts=[f["fact_id"] for f in registry["facts"] if f["verification_status"]!="REVIEWED_BY_HUMAN"]
    reasons=[]
    if pending_sources:reasons.append("SOURCE_NOT_REVIEWED")
    if pending_facts:reasons.append("FACTS_NOT_VERIFIED")
    if topic["overlap_review"]["status"]!="REVIEWED_SEPARATE":reasons.append("TOPIC_OVERLAP_NOT_RESOLVED")
    return {"structurally_valid":True,"source_review_pending_ids":pending_sources,
            "fact_review_pending_ids":pending_facts,"ready_for_release_pipeline":False,
            "ready_for_verified_fact_drafting":not pending_sources and not pending_facts,
            "unresolved_checks":reasons,
            "note":"Even reviewed metadata does not independently certify claim truth or authorize release."}
