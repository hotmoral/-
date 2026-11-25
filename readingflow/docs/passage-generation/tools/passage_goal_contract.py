"""Validate independent reading-objective plans; no AI evaluation or learner claims."""
from passage_planning_contract import AGES,LEVELS,_text
ALLOWED_OPS=("사실 확인","핵심 파악","비교","인과","통합","추론","근거 평가")

def validate_goal_types(data):
    ds=data.get("type_definitions")
    if not isinstance(ds,list) or [d.get("label") for d in ds]!=list(ALLOWED_OPS):
        raise ValueError("goal type baseline mismatch")
    for d in ds:_text(d.get("operational_definition"),"operation definition")
    return True

def validate_goal_plan(plan,topic,registry=None):
    for field in ("plan_id","topic_id"):
        _text(plan.get(field),field)
    if plan["topic_id"]!=topic["topic_id"]:
        raise ValueError("topic foreign key mismatch")
    if plan.get("age_group")!=topic.get("age_group") or plan.get("level")!=topic.get("level"):
        raise ValueError("age/L mismatch")
    if plan["age_group"] not in AGES or plan["level"] not in LEVELS:
        raise ValueError("age/L invalid")
    goals=plan.get("objectives")
    if not isinstance(goals,list) or not 1<=len(goals)<=3:
        raise ValueError("1..3 objectives required")
    ids=set()
    for g in goals:
        for key in ("objective_id","learner_target","key_question","expected_reasoning"):
            _text(g.get(key),key)
        if g["objective_id"] in ids: raise ValueError("duplicate goal id")
        ids.add(g["objective_id"])
        if g.get("operation") not in ALLOWED_OPS:
            raise ValueError("unknown operation")
        links=g.get("required_fact_ids")
        if not isinstance(links,list) or not links or any(not isinstance(x,str) or not x.strip() for x in links) or len(set(links))!=len(links):
            raise ValueError("missing, invalid or duplicate fact ID")
        if g.get("answer_must_be_supported_in_passage") is not True:
            raise ValueError("answer evidence must be in actual passage")
        if registry is not None:
            ids_in_registry={f["fact_id"] for f in registry.get("facts",[])}
            if any(fid not in ids_in_registry for fid in links):
                raise ValueError("goal refers to unavailable fact")
    if plan.get("release_approved") is not False or plan.get("learner_difficulty_validated") is not False:
        raise ValueError("unvalidated goal plan must not be approved")
    return True
