import unittest
from author_attribute_sampler import ATTRIBUTE_NAMES, draw_author_attributes, verify_selection


class AuthorSamplerTests(unittest.TestCase):
    def setUp(self):
        self.pools = {name: ["가", "나", "다"] for name in ATTRIBUTE_NAMES}

    def test_24_attributes_and_audit(self):
        result = draw_author_attributes("P1", self.pools)
        self.assertEqual(len(result["author_attributes_24"]), 24)
        self.assertEqual(len(result["attribute_application_log"]), 24)
        self.assertIsNone(result["experimental_seed"])
        self.assertFalse(result["release_approved"])
        self.assertTrue(verify_selection(result, self.pools))

    def test_seeded_reproduction(self):
        a = draw_author_attributes("P1", self.pools, seed=42)
        b = draw_author_attributes("P2", self.pools, seed=42)
        self.assertEqual(a["author_attributes_24"], b["author_attributes_24"])
        self.assertEqual(a["candidate_pools_sha256"], b["candidate_pools_sha256"])

    def test_missing_attribute_rejected(self):
        del self.pools[ATTRIBUTE_NAMES[0]]
        with self.assertRaises(ValueError):
            draw_author_attributes("P1", self.pools)

    def test_duplicate_pool_rejected(self):
        self.pools[ATTRIBUTE_NAMES[0]] = ["가", "가"]
        with self.assertRaises(ValueError):
            draw_author_attributes("P1", self.pools)

    def test_invalid_seed_rejected(self):
        with self.assertRaises(ValueError):
            draw_author_attributes("P1", self.pools, seed="42")

    def test_changed_pool_order_rejected_by_hash(self):
        record = draw_author_attributes("P1", self.pools, seed=5)
        changed = {key: values[:] for key, values in self.pools.items()}
        changed[ATTRIBUTE_NAMES[0]].reverse()
        self.assertFalse(verify_selection(record, changed))

    def test_seed_tampering_rejected(self):
        record = draw_author_attributes("P1", self.pools, seed=5)
        record["experimental_seed"] = 10
        self.assertFalse(verify_selection(record, self.pools))

    def test_tampered_value_rejected(self):
        record = draw_author_attributes("P1", self.pools, seed=5)
        record["author_attributes_24"][ATTRIBUTE_NAMES[0]] = "없는 값"
        self.assertFalse(verify_selection(record, self.pools))


if __name__ == "__main__":
    unittest.main()
