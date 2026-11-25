"""Validate expandable v2 taxonomy, its topic examples and a read-only legacy mapping.

Keeps v1 as frozen design example. No auto-generation or semantic truth claim.
"""
from pathlib import Path
from collections import Counter
from passage_planning_contract import AGES, LEVELS, _text, _list

V2="readingflow.topic_domains.proposal.v2"

def validate_taxonomy_v2(data):
    if data.get("schema_version") != V2 or data.get("status")!="PROPOSED_NOT_APPROVED":
        raise ValueError("v2 proposed taxonomy required")
    domains=data.get("domains")
    if not isinstance(domains,list) or not domains:raise ValueError("nonempty domains required")
    names=set();ids=set();per_field={}
    for d in domains:
        for key in ("domain_id","name","scope","primary_selection_rule"):_text(d.get(key),key)
        if d["domain_id"] in ids or d["name"] in names:raise ValueError("duplicate domain")
        ids.add(d["domain_id"]);names.add(d["name"])
        _list(d.get("subfields"),"subfields")
        per_field[d["name"]]=set(d["subfields"])
        if d.get("approval")!="PROPOSED":raise ValueError("unapproved subfields mislabeled")
    for case in data.get("interdisciplinary_boundaries",[]):
        if case.get("primary") not in per_field:raise ValueError("unknown boundary primary")
        if not isinstance(case.get("secondary"),list):raise ValueError("boundary secondary list")
        if any(k not in per_field for k in case["secondary"]):raise ValueError("unknown boundary secondary")
        if case["primary"] in case["secondary"]:raise ValueError("boundary repeats primary")
        _text(case.get("question"),"boundary question")
        _text(case.get("reason"),"boundary reason")
    return per_field

SELECTION_TRACE_STEPS=("PRIMARY_DOMAIN","SUBFIELD","INDIVIDUAL_TOPIC","CORE_QUESTION")

def validate_topic_selection_trace(record):
    # For NEW passage planning only. Legacy retrospective mapping uses separate validator.
    trace=record.get("selection_trace")
    if not isinstance(trace,list) or len(trace)!=len(SELECTION_TRACE_STEPS):
        raise ValueError("must record primary domain > subfield > individual topic > core question")
    expected_values=(record.get("primary_domain"),record.get("subfield"),record.get("topic_focus"),record.get("core_question"))
    for index,(item,step,value) in enumerate(zip(trace,SELECTION_TRACE_STEPS,expected_values)):
        if not isinstance(item,dict) or item.get("step")!=step or item.get("value")!=value:
            raise ValueError("topic selection order or value mismatch at step "+str(index+1))
    if record.get("selection_trace_status")!="ILLUSTRATIVE_ORDER_NOT_AUTOMATED":
        raise ValueError("cannot claim automatic topic selection from planning metadata")
    return True

def validate_topic_record_v2(record,taxonomy):
    field_map=validate_taxonomy_v2(taxonomy)
    for key in ("topic_id","title","primary_domain","subfield","topic_focus","core_question"):
        _text(record.get(key),key)
    if record.get("taxonomy_version")!=V2:raise ValueError("topic version mismatch")
    validate_topic_selection_trace(record)
    if record.get("age_group") not in AGES or record.get("level") not in LEVELS:
        raise ValueError("age group/level")
    if record.get("classification_status") not in ("PROVISIONAL_CLASSIFIED","PROPOSED_NEW_DOMAIN"):
        raise ValueError("invalid classification status")
    if record["primary_domain"] not in field_map:
        if record["classification_status"]!="PROPOSED_NEW_DOMAIN":
            raise ValueError("new domain needs explicit proposal")
    elif record["classification_status"]=="PROPOSED_NEW_DOMAIN":
        raise ValueError("existing primary cannot claim new domain")
    _list(record.get("secondary_domains"),"secondary_domains",empty=True)
    if any(x not in field_map or x==record["primary_domain"] for x in record["secondary_domains"]):
        raise ValueError("invalid secondary domain")
    state=record.get("subfield_classification_status")
    exists=record["primary_domain"] in field_map and record["subfield"] in field_map[record["primary_domain"]]
    if state=="EXISTING_SUBFIELD":
        if not exists:raise ValueError("unknown primary subfield")
    elif state=="PROPOSED_NEW_SUBFIELD":
        if exists:raise ValueError("existing subfield mislabeled new")
        _text(record.get("subfield_proposal_rationale"),"new subfield reason")
    else:raise ValueError("invalid subfield proposal status")
    _list(record.get("core_concepts"),"core_concepts")
    overlap=record.get("overlap_review")
    if not isinstance(overlap,dict) or overlap.get("status") not in ("NOT_SCREENED","NEEDS_SEMANTIC_REVIEW","REVIEWED_SEPARATE"):
        raise ValueError("topic overlap status")
    if not isinstance(overlap.get("possible_matches"),list):raise ValueError("topic overlap list")
    if record.get("release_approved") is not False:raise ValueError("example cannot be approved")
    return True

def validate_legacy_mapping(mapping,source_catalog,taxonomy):
    field_map=validate_taxonomy_v2(taxonomy)
    records=mapping.get("records")
    old=source_catalog.get("records")
    if not isinstance(records,list) or not isinstance(old,list) or len(records)!=len(old):
        raise ValueError("mapping/source cardinality")
    if mapping.get("taxonomy_version")!=V2:raise ValueError("wrong mapping taxonomy version")
    ids=set();counts=Counter();flagged=[]
    for row,src in zip(records,old):
        if row.get("passage_id")!=src.get("passage_id") or row.get("topic")!=src.get("topic"):
            raise ValueError("legacy passage record mismatch")
        if row["passage_id"] in ids:raise ValueError("duplicate passage id")
        ids.add(row["passage_id"])
        if (row["source_age_group"],row["source_level"],row["legacy_domain"])!=(
            src["age_group"],src["level"],src["domain"]):
            raise ValueError("legacy metadata changed")
        primary=row["primary_domain"]
        if primary not in field_map or row["primary_subfield"] not in field_map[primary]:
            raise ValueError("unregistered field/subfield")
        _list(row.get("secondary_domains"),"secondary_domains",empty=True)
        if primary in row["secondary_domains"] or any(x not in field_map for x in row["secondary_domains"]):
            raise ValueError("invalid secondary mapping")
        _text(row.get("classification_reason"),"classification reason")
        if row.get("editorial_review_status") not in ("PROVISIONAL_MAPPED","NEEDS_EDITORIAL_REVIEW"):
            raise ValueError("invalid mapping review status")
        if row.get("release_approved") is not False:raise ValueError("mapping cannot approve release")
        if row["editorial_review_status"]=="NEEDS_EDITORIAL_REVIEW":flagged.append(row["passage_id"])
        counts[primary]+=1
    if mapping.get("total")!=len(records):raise ValueError("mapping total mismatch")
    coverage=[]
    for example in mapping.get("coverage_scenarios",[]):
        _text(example.get("theme"),"coverage theme")
        _list(example.get("examples"),"coverage examples")
        _list(example.get("required_domains"),"coverage domains")
        for domain in example["required_domains"]:
            if domain not in field_map:raise ValueError("uncovered domain name")
        coverage.append(example["theme"])
    return {"mapped":len(ids),"domain_usage":dict(counts),"requires_editorial_review":flagged,
            "domains_without_legacy_pilots":sorted(set(field_map)-set(counts)),
            "coverage_scenarios":len(coverage)}
