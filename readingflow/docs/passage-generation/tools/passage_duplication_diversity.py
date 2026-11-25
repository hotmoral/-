"""Read-only duplication and distribution indicators.

No text/image semantics, plagiarism verdict, automatic rejection, quota or RNG change.
"""
from collections import Counter
from difflib import SequenceMatcher
import re
import unicodedata

def normalize_title(value):
    if not isinstance(value,str):
        raise ValueError("title must be string")
    value=unicodedata.normalize("NFKC",value).casefold()
    return "".join(c for c in value if not c.isspace() and not unicodedata.category(c).startswith("P"))

def normalize_text(value):
    if not isinstance(value,str):
        raise ValueError("text must be string")
    return "".join(unicodedata.normalize("NFKC",value).split())

def _flag(kind,left,right,note,score=None):
    record={"type":kind,"left_id":left,"right_id":right,"disposition":"EDITORIAL_REVIEW_ONLY","note":note}
    if score is not None:record["title_similarity"]=round(score,4)
    return record

def audit_corpus(records,candidate=None,near_threshold=0.82):
    if not isinstance(records,list) or not isinstance(near_threshold,(float,int)) or not 0<near_threshold<1:
        raise ValueError("valid corpus and a 0..1 review threshold required")
    ids=set()
    for row in records:
        if not isinstance(row,dict):
            raise ValueError("record object required")
        key=row.get("passage_id")
        if not isinstance(key,str) or not key.strip() or key in ids:
            raise ValueError("each passage needs a unique ID")
        ids.add(key)
        if not isinstance(row.get("title"),str) or not row["title"].strip():
            raise ValueError("each passage needs a title")
        if not isinstance(row.get("age_group"),str) or not isinstance(row.get("level"),str):
            raise ValueError("age/L required")
    flags=[]
    for i,left in enumerate(records):
        for right in records[i+1:]:
            a,b=normalize_title(left["title"]),normalize_title(right["title"])
            if a==b:
                flags.append(_flag("EXACT_TITLE_REVIEW",left["passage_id"],right["passage_id"],"같거나 거의 동일한 표제; 본문 내용과 목표의 차이 검토"))
            else:
                s=SequenceMatcher(None,a,b).ratio()
                if s>=near_threshold:
                    flags.append(_flag("NEAR_TITLE_REVIEW",left["passage_id"],right["passage_id"],"표제 유사성은 의미 중복의 증거가 아님",s))
            if isinstance(left.get("text"),str) and isinstance(right.get("text"),str):
                if left["text"].strip() and right["text"].strip() and normalize_text(left["text"])==normalize_text(right["text"]):
                    flags.append(_flag("EXACT_TEXT_REVIEW",left["passage_id"],right["passage_id"],"정규화 본문 일치; 버전·의도적 재사용 여부 확인"))
    domain_counts=Counter(row.get("primary_domain") or "UNCLASSIFIED" for row in records)
    age_counts=Counter(row["age_group"] for row in records)
    level_counts=Counter(row["level"] for row in records)
    known_candidate_matches=[]
    if candidate is not None:
        if not isinstance(candidate,dict) or not isinstance(candidate.get("title"),str) or not candidate.get("topic_id"):
            raise ValueError("invalid planned candidate")
        for linked in candidate.get("known_possible_matches",[]):
            if linked not in ids:
                raise ValueError("candidate references passage not in corpus")
            known_candidate_matches.append(_flag("EXPLICIT_KNOWN_TOPIC_OVERLAP",candidate["topic_id"],linked,"기존 주제 후보에 명시한 겹침 가능성; 자동 중복 판정 불가"))
        for row in records:
            if normalize_title(candidate["title"])==normalize_title(row["title"]):
                known_candidate_matches.append(_flag("EXACT_TITLE_REVIEW",candidate["topic_id"],row["passage_id"],"같은 제목; 독해 목표가 다를 수 있음"))
            else:
                s=SequenceMatcher(None,normalize_title(candidate["title"]),normalize_title(row["title"])).ratio()
                if s>=near_threshold:
                    known_candidate_matches.append(_flag("NEAR_TITLE_REVIEW",candidate["topic_id"],row["passage_id"],"제목 유사성: 편집자 확인",s))
    return {
      "status":"STRUCTURAL_INDICATORS_NOT_SEMANTIC_DECISION",
      "corpus_count":len(records),"topic_overlap_review_flags":flags,
      "planned_topic_review_flags":known_candidate_matches,
      "primary_domain_distribution":dict(domain_counts),
      "age_group_distribution":dict(age_counts),
      "level_distribution":dict(level_counts),
      "style_diversity_status":"NOT_MEASURABLE_FROM_METADATA" if not all(
          isinstance(r.get("author_attributes_24"),dict) for r in records
        ) else "SOURCE_ATTRIBUTES_PRESENT_REQUIRES_PROSE_REVIEW",
      "exact_fulltext_checked_pairs":sum(1 for i,r in enumerate(records) for s in records[i+1:]
          if isinstance(r.get("text"),str) and r["text"].strip() and isinstance(s.get("text"),str) and s["text"].strip()),
      "auto_rejected":0,"release_approved":False,
      "note":"Only title/full-text equality and descriptive domain counts are computable. No semantic duplication or true style variety proven."
    }
