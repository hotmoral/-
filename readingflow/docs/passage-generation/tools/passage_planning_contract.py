"""Topic record validation only. No topic generator, author selection, or approval."""
AGES=("초등 저학년","초등 고학년","중·고등학생","성인","고령층")
LEVELS=tuple(f"L{i}" for i in range(1,7))
SELECTION_MODES=("USER_SPECIFIED","CURATED_PROPOSAL","EXPERIMENT_FIXED")

def _text(value,key):
    if not isinstance(value,str) or not value.strip(): raise ValueError(key)

def _list(value,key,empty=False):
    if not isinstance(value,list) or (not empty and not value):raise ValueError(key)
    for item in value:_text(item,key)
    if len(set(value))!=len(value):raise ValueError("duplicate "+key)

def validate_taxonomy(taxonomy):
    if taxonomy.get("status")!="PROPOSED_NOT_APPROVED":raise ValueError("unapproved taxonomy")
    ds=taxonomy.get("domains")
    if not isinstance(ds,list) or len(ds)!=18:raise ValueError("expected 18 seed domains")
    ids,names=set(),set()
    for d in ds:
        _text(d.get("domain_id"),"domain id")
        _text(d.get("name"),"domain name")
        _list(d.get("subfields"),"subfields")
        ids.add(d["domain_id"]);names.add(d["name"])
    if len(ids)!=18 or len(names)!=18:raise ValueError("duplicate domains")
    return names

def validate_topic_record(record,taxonomy):
    allowed=validate_taxonomy(taxonomy)
    for k in ("topic_id","title","primary_domain","subfield","core_question"):_text(record.get(k),k)
    if record.get("age_group") not in AGES or record.get("level") not in LEVELS:raise ValueError("age/level")
    if record.get("selection_mode") not in SELECTION_MODES:raise ValueError("auto selection not implemented")
    st=record.get("classification_status")
    if st not in ("PROVISIONAL_CLASSIFIED","PROPOSED_NEW_DOMAIN"):raise ValueError("classification status")
    if (record["primary_domain"] not in allowed)!=(st=="PROPOSED_NEW_DOMAIN"):
        raise ValueError("new domain requires proposal")
    _list(record.get("secondary_domains"),"secondary_domains",True)
    if record["primary_domain"] in record["secondary_domains"]:raise ValueError("primary duplicated")
    if any(x not in allowed for x in record["secondary_domains"]):raise ValueError("unreviewed secondary domain")
    _list(record.get("core_concepts"),"core_concepts")
    review=record.get("overlap_review")
    if not isinstance(review,dict) or review.get("status") not in ("NOT_SCREENED","NEEDS_SEMANTIC_REVIEW","REVIEWED_SEPARATE"):
        raise ValueError("overlap review state")
    if not isinstance(review.get("possible_matches"),list):raise ValueError("matches list")
    for m in review["possible_matches"]:
        _text(m.get("passage_id"),"match id");_text(m.get("title"),"match title")
    if record.get("release_approved") is not False:raise ValueError("cannot approve example")
    return True
