"""New-passage 17-item QA: deterministic checks ONLY; never semantic or release PASS.

The 30 original pilot passages are read-only. No model/network calls are made.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "operations/quality/new_passage_question_creation_checklist_v1.json"
IDS = {"G01","G02","G03","G04","G05","G06","Q01","Q02","Q03",
       "Q04","Q05","Q06","Q07","Q08","Q09","V01","V02"}
LETTERS = ("A","B","C","D")
ABSOLUTE = re.compile("언제나|반드시|항상|전혀|무조건|모든|오직|절대|전부|확정")

def load_contract(path=POLICY):
    policy = json.loads(Path(path).read_text(encoding="utf-8"))
    items = policy.get("required")
    if not isinstance(items,list) or len(items)!=17 or {i.get("id") for i in items}!=IDS:
        raise ValueError("17-item QA checklist is incomplete or changed")
    excluded = {i.get("name") for i in policy.get("explicitly_excluded",[])}
    if "BACKGROUND_KNOWLEDGE_BLIND_GUESSABILITY" not in excluded:
        raise ValueError("current user exclusion missing")
    if policy.get("release_approved") is not False:
        raise ValueError("policy cannot approve release")
    return policy

def present(v):
    return isinstance(v,str) and bool(v.strip())

def evaluate_new_candidate(candidate, *, author_selection=None, contract=None):
    """Evaluate ONE new passage; preserve the input, never auto-approve content.

    Input: passage_id, passage_version, source_text, age_group, level (L1..L6),
    questions (3..6). Each question: question_id, question, answer, evidence,
    explanation, question_type, question_goal, source_version, format=single_choice,
    correct_option, options A..D, distractor_grounding (three entries with
    option_id, evidence and false_reason).
    """
    if not isinstance(candidate,dict):
        raise TypeError("candidate must be an object")
    contract = load_contract() if contract is None else contract
    if len(contract.get("required",[]))!=17 or {i.get("id") for i in contract["required"]}!=IDS:
        raise ValueError("unsupported checklist")
    rows = [{"id":i["id"],"name":i["name"],"scope":i["scope"],
             "editorial_state":"NOT_REVIEWED","structural_state":"PENDING"}
            for i in contract["required"]]
    state={r["id"]:r for r in rows}
    errors,warnings,details=[],[],[]
    def finding(check,code,detail,qid=None,advisory=False):
        item={"check_id":check,"code":code,"detail":detail}
        if qid is not None:item["question_id"]=qid
        (warnings if advisory else errors).append(item)
        if not advisory:state[check]["structural_state"]="ISSUE"
        elif state[check]["structural_state"]=="PENDING":
            state[check]["structural_state"]="ADVISORY_ONLY"
    def seen(check):
        if state[check]["structural_state"]=="PENDING":
            state[check]["structural_state"]="STRUCTURE_CHECKED_NOT_SEMANTIC"

    pid=candidate.get("passage_id")
    version=candidate.get("passage_version")
    text=candidate.get("source_text")
    age=candidate.get("age_group")
    level=candidate.get("level")
    questions=candidate.get("questions")
    has_text=present(text)
    has_questions=isinstance(questions,list) and bool(questions)
    if not present(pid):finding("V01","MISSING_PASSAGE_ID","passage_id required")
    if not present(version):finding("V01","MISSING_PASSAGE_VERSION","explicit passage_version required")
    if age not in contract["age_groups"]:finding("G03","INVALID_AGE","unknown age group")
    if level not in contract["levels"] and level not in ["L"+str(v) for v in contract["levels"]]:
        finding("G03","INVALID_LEVEL","expected L1..L6")
    if candidate.get("release_approved") is True:
        finding("V02","SELF_APPROVED","generated candidate cannot authorize release")
    seen("V02")
    sha=hashlib.sha256(text.encode("utf-8")).hexdigest() if has_text else None
    if has_text:
        seen("G03");seen("V01")
        if candidate.get("source_text_sha256") not in (None,sha):
            finding("V01","STALE_SHA","source text hash mismatch")
        if "젖은물" in text or "젖은 물" in text:
            finding("G04","SUSPICIOUS_PHRASE","nonsensical expression requires review",advisory=True)
    elif text is not None:
        finding("G04","BLANK_PASSAGE","source text must not be blank")
    if author_selection is not None:
        attrs=author_selection.get("author_attributes_24") if isinstance(author_selection,dict) else None
        if not isinstance(attrs,dict) or len(attrs)!=24:
            finding("G05","WRONG_AUTHOR_ATTRIBUTE_COUNT","24 attribute draws required")
        else:
            seen("G05") # Presence only: actual author style NOT verified
    if questions is not None and not isinstance(questions,list):
        finding("Q02","MALFORMED_QUESTIONS","questions must be a list")
    if has_questions and not has_text:
        finding("Q02","MISSING_PASSAGE_FOR_QUESTIONS","source required before question checks")
    if has_questions:
        if not 3<=len(questions)<=6:
            finding("Q02","QUESTION_COUNT","requires 3..6 questions")
        seen_ids,seen_stems,seen_goals=set(),set(),set()
        for i,q in enumerate(questions):
            if not isinstance(q,dict):
                finding("Q02","MALFORMED_QUESTION","question must be object",str(i))
                continue
            qid=q.get("question_id")
            tag=qid if present(qid) else "index:"+str(i)
            if not present(qid) or qid in seen_ids:
                finding("Q02","DUPLICATE_QUESTION_ID","unique question_id required",tag)
            elif present(qid):seen_ids.add(qid)
            if q.get("release_approved") is True:
                finding("V02","QUESTION_SELF_APPROVED","question cannot self-approve",tag)
            stem=q.get("question")
            if not all(present(q.get(k)) for k in ("question","question_type","explanation")):
                finding("Q01","STEM_OR_EXPLANATION_MISSING","question, question_type and explanation required",tag)
            else:
                seen("Q01")
                if stem in seen_stems:
                    finding("Q07","REPEATED_STEM","identical questions in one passage",tag)
                seen_stems.add(stem)
                if not stem.rstrip().endswith(("?","？")):
                    finding("Q01","END_OF_STEM_ADVISORY","check natural complete interrogative",tag,True)
            goal=q.get("question_goal")
            if not present(goal):
                finding("Q07","MISSING_QUESTION_GOAL","state specific reading operation",tag)
            else:
                if goal in seen_goals:
                    finding("Q07","GOAL_REPEATED","check substantive question differentiation",tag,True)
                seen_goals.add(goal);seen("Q07")
            if q.get("source_version")!=version:
                finding("V01","STALE_QUESTION_VERSION","question must refer to source passage_version",tag)
            if q.get("format")!="single_choice":
                finding("Q02","INVALID_QUESTION_FORMAT","single_choice required",tag)
            opts=q.get("options")
            mapping={}
            if not isinstance(opts,list) or len(opts)!=4 or any(not isinstance(o,dict) for o in opts):
                finding("Q02","FOUR_OPTIONS_REQUIRED","exactly four option objects required",tag)
            else:
                labels=[o.get("id") for o in opts]
                texts=[o.get("text") for o in opts]
                if labels!=list(LETTERS) or not all(present(t) for t in texts) or len(set(texts))!=4:
                    finding("Q02","OPTION_IDS_TEXT_INVALID","A-D nonblank, unique texts required",tag)
                else:
                    mapping=dict(zip(labels,texts))
                    seen("Q04") # syntax shape only; semantic language not evaluated
            answer_label=q.get("correct_option")
            if answer_label not in LETTERS or mapping.get(answer_label)!=q.get("answer") or not present(q.get("answer")):
                finding("Q02","ANSWER_MAPPING_INVALID","correct label and text mismatch",tag)
            evidence=q.get("evidence")
            literal=has_text and present(evidence) and evidence in text
            if not literal:
                finding("Q02","CORRECT_EVIDENCE_NOT_LITERAL","exact correct evidence must appear in source",tag)
            else:seen("Q02")
            ground=q.get("distractor_grounding")
            wrong=set(LETTERS)-({answer_label} if answer_label in LETTERS else set())
            if not isinstance(ground,list) or len(ground)!=3 or any(not isinstance(g,dict) for g in ground):
                finding("Q03","THREE_GROUNDING_RECORDS_REQUIRED","three wrong-option reason records needed",tag)
            else:
                labels=[g.get("option_id") for g in ground]
                if not all(isinstance(label,str) for label in labels) or set(labels)!=wrong or len(set(labels))!=3:
                    finding("Q03","DISTRACTOR_LABELS_INVALID","one reason for each of three wrong labels",tag)
                else:seen("Q03")
                for g in ground:
                    quote=g.get("evidence")
                    if not has_text or not present(quote) or quote not in text or not present(g.get("false_reason")):
                        finding("Q03","DISTRACTOR_REASON_OR_QUOTE_MISSING","literal evidence and reason required per wrong answer",tag)
            flags=[]
            if len(mapping)==4 and answer_label in mapping:
                ln={letter:len("".join(mapping[letter].split())) for letter in LETTERS}
                smallest=min(ln.values());largest=max(ln.values())
                if ln[answer_label]==smallest and list(ln.values()).count(smallest)==1:
                    flags.append("CORRECT_UNIQUELY_SHORTEST")
                if ln[answer_label]==largest and list(ln.values()).count(largest)==1:
                    flags.append("CORRECT_UNIQUELY_LONGEST")
                if not ABSOLUTE.search(mapping[answer_label]) and sum(bool(ABSOLUTE.search(mapping[v])) for v in LETTERS if v!=answer_label)>=2:
                    flags.append("ABSOLUTE_WRONG_OPTIONS")
                if flags:finding("Q05","OPTION_SURFACE_CUE",", ".join(flags),tag,True)
                seen("Q05");seen("Q06")
            details.append({"question_id":tag,"reading_goal":goal,"correct_option":answer_label,
                            "source_quote_literal":bool(literal),"surface_flags":flags})
    # Intentionally NEVER set editorial PASS from a substring match or metadata.
    decision="REVISE" if errors else ("HOLD" if not has_text or not has_questions
                                     else "READY_FOR_EDITORIAL_REVIEW")
    return {"schema_version":"readingflow.new_passage_17_item_executable_QA.v1",
            "passage_id":pid,"passage_version":version,"source_sha256":sha,
            "decision":decision,"checklist_count":17,"checks":rows,
            "errors":errors,"warnings":warnings,"questions":details,
            "pending_semantic_check_ids":[x["id"] for x in rows],
            "excluded_quality_checks":["BACKGROUND_KNOWLEDGE_BLIND_GUESSABILITY"],
            "semantic_uniqueness_validated":False,
            "human_validated":False,"learner_validated":False,
            "release_approved":False,"can_publish":False,
            "note":"Structural QA only. Korean grammar, factual evidence, semantic answer uniqueness, safety and originality require independent review."}
