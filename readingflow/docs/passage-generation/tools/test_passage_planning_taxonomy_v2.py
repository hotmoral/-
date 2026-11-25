"""Taxonomy v2: variable subfield counts, domain boundaries, legacy coverage, future expansions."""
import json
import unittest
from copy import deepcopy
from pathlib import Path
from topic_taxonomy_v2_contract import validate_taxonomy_v2,validate_topic_record_v2,validate_legacy_mapping
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"planning"

class TopicTaxonomyV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def read(path):return json.loads(path.read_text(encoding="utf8"))
        cls.tax=read(BASE/"topic_taxonomy_proposal_v2.json")
        cls.legacy=read(ROOT/"data"/"normalized_passage_catalog_30_v1.json")
        cls.mapping=read(BASE/"topic_catalog_30_provisional_v2.json")
        cls.example=read(BASE/"examples"/"topic_condensation_v2.json")

    def test_subfields_variable_and_coverage(self):
        domains=validate_taxonomy_v2(self.tax)
        self.assertEqual(len(domains),18)
        sizes=[len(v) for v in domains.values()]
        self.assertGreater(len(set(sizes)),1)
        self.assertTrue(all(size>4 for size in sizes))
        self.assertEqual(sum(sizes),298)
        self.assertEqual(len(self.tax["interdisciplinary_boundaries"]),14)

    def test_expandable_domain_and_subfield_counts(self):
        t=deepcopy(self.tax)
        t["domains"][0]["subfields"].append("새로 제안된 현상")
        t["domains"].append({"domain_id":"D19","name":"신규 영역","scope":"새 영역 실험",
                            "subfields":["신규 세부 분야"],"primary_selection_rule":"신규 영역 판단","approval":"PROPOSED"})
        self.assertEqual(len(validate_taxonomy_v2(t)),19)

    def test_v2_topic_record_is_subfield_validated(self):
        self.assertTrue(validate_topic_record_v2(self.example,self.tax))
        x=deepcopy(self.example);x["subfield"]="비등록 임시 분야"
        with self.assertRaises(ValueError):validate_topic_record_v2(x,self.tax)
        x["subfield_classification_status"]="PROPOSED_NEW_SUBFIELD"
        x["selection_trace"][1]["value"]=x["subfield"]
        x["subfield_proposal_rationale"]="기존 대기·기상 범주와 구분되는 신규 연구 분야라면 편집 검토"
        self.assertTrue(validate_topic_record_v2(x,self.tax))

    def test_legacy_mapping_30_all_preserved(self):
        result=validate_legacy_mapping(self.mapping,self.legacy,self.tax)
        self.assertEqual(result["mapped"],30)
        self.assertGreater(len(result["requires_editorial_review"]),0)
        self.assertEqual(result["coverage_scenarios"],9)

    def test_taxonomy_not_bound_to_author_rng_or_qa_approval(self):
        self.assertEqual(self.tax["status"],"PROPOSED_NOT_APPROVED")
        self.assertNotIn("author_attributes_24",self.tax)
        self.assertFalse(self.example["release_approved"])
        self.assertTrue(all(not x["release_approved"] for x in self.mapping["records"]))

    def test_forward_selection_order_is_recorded(self):
        self.assertEqual([x["step"] for x in self.example["selection_trace"]],
                         ["PRIMARY_DOMAIN","SUBFIELD","INDIVIDUAL_TOPIC","CORE_QUESTION"])
        self.assertTrue(validate_topic_record_v2(self.example,self.tax))

    def test_reverse_selection_or_silent_domain_change_rejected(self):
        x=deepcopy(self.example)
        x["selection_trace"][0],x["selection_trace"][-1]=x["selection_trace"][-1],x["selection_trace"][0]
        with self.assertRaises(ValueError):validate_topic_record_v2(x,self.tax)
        x=deepcopy(self.example);x["primary_domain"]="환경·생태"
        with self.assertRaises(ValueError):validate_topic_record_v2(x,self.tax)

    def test_duplicate_subfields_rejected(self):
        t=deepcopy(self.tax);t["domains"][0]["subfields"].append(t["domains"][0]["subfields"][0])
        with self.assertRaises(ValueError):validate_taxonomy_v2(t)

    def test_invalid_legacy_topic_id_or_subfield_fails(self):
        m=deepcopy(self.mapping);m["records"][0]["passage_id"]="CORRUPTED"
        with self.assertRaises(ValueError):validate_legacy_mapping(m,self.legacy,self.tax)
        m=deepcopy(self.mapping);m["records"][0]["primary_subfield"]="모르는 세부분야"
        with self.assertRaises(ValueError):validate_legacy_mapping(m,self.legacy,self.tax)

if __name__=="__main__":unittest.main()
