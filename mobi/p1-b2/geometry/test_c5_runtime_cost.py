from __future__ import annotations

import unittest

from c4_hard_motion_fixture_adapter import H1, H2, H3, H4, H5, H6N, H7
from c5_runtime_cost_proxy import build_cost_report, canonical_json_bytes
from c5_source_cost_audit import build_source_audit


class RuntimeCostProxyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = build_cost_report()

    def test_report_is_byte_deterministic(self):
        first = canonical_json_bytes(self.report)
        second = canonical_json_bytes(build_cost_report())
        self.assertEqual(first, second)

    def test_fixture_and_render_sample_counts_are_fixed(self):
        self.assertEqual(self.report["fixtureSampleCount"], 912)
        self.assertEqual(self.report["renderSampleCount"], 2808)

    def test_partition_group_count_never_exceeds_accepted_bound(self):
        host = self.report["decisionProxies"]["host"]
        self.assertLessEqual(host["maximumActiveSemanticPartitionsAcrossReport"], 4)
        self.assertFalse(host["newAndroidWindowMechanismIntroduced"])
        self.assertFalse(host["idleContinuousUpdateRequiredByRepresentation"])

    def test_h6n_view_resolved_keeps_same_output_shape_scale(self):
        h6n = self.report["decisionProxies"]["h6n"]
        self.assertEqual(h6n["meanShapeDeltaViewMinusGeneric"], 0.0)
        self.assertEqual(h6n["meanPointDeltaViewMinusGeneric"], 0.0)
        self.assertEqual(h6n["meanBoundsShapeVisitDelta"], 0.0)
        self.assertGreater(h6n["viewResolvedMeanSortItems"], 0.0)
        self.assertGreater(h6n["viewResolvedMeanViewDepthShapes"], 0.0)
        self.assertEqual(h6n["genericMeanSortItems"], 0.0)
        self.assertLessEqual(h6n["maxActivePartitionsViewResolved"], 4)

    def test_h4_sparse_correction_does_not_increase_shape_burden(self):
        h4 = self.report["decisionProxies"]["h4"]
        self.assertLessEqual(h4["sparseHybridMeanShapes"], h4["baselineMeanShapes"])
        self.assertLessEqual(h4["sparseHybridMaxShapes"], h4["baselineMaxShapes"])
        self.assertEqual(h4["sparseHybridMaxCorrectionFamiliesPerSample"], 1)
        self.assertLessEqual(h4["maxActivePartitionsSparseHybrid"], 4)

    def test_sparse_hybrid_has_no_non_h4_correction_family(self):
        for case_id in (H1, H2, H3, H5, H6N, H7):
            aggregate = self.report["caseAggregates"][f"C4_C|{case_id}"]
            self.assertEqual(aggregate["correction_family_count"]["max"], 0)
        h4 = self.report["caseAggregates"][f"C4_C|{H4}"]
        self.assertEqual(h4["correction_family_count"]["min"], 1)
        self.assertEqual(h4["correction_family_count"]["max"], 1)

    def test_source_audit_separates_prototype_overhead_from_architecture(self):
        audit = build_source_audit()
        view = audit["viewResolved"]
        partition = audit["partitionBounds"]
        self.assertTrue(view["prototypeFullBasePrerenderForTail"])
        self.assertTrue(view["viewDepthSortPresent"])
        self.assertFalse(view["fullBasePrerenderIsArchitectureRequired"])
        self.assertTrue(partition["currentImplementationFiltersAllShapesPerSemanticGroup"])
        self.assertEqual(partition["semanticGroupCount"], 4)
        self.assertTrue(partition["groupCountIsArchitectureBounded"])


if __name__ == "__main__":
    unittest.main()
