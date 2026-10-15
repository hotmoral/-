import unittest

from c3_renderer_minimal_v3 import render_fixture as render_fixture_v3
from c3_renderer_view_resolved_v4 import (
    VIEW_REPRESENTATION_VERSION,
    render_fixture as render_fixture_view,
)
from c3_semantic import MORPHOLOGIES, SIZES, build_common_fixture
from run_c3_matrix import canonical_bytes
from run_c3r_h6_matrix import run_matrix


class P1C3RH6ViewResolvedTests(unittest.TestCase):
    def test_non_h6_paths_are_exact_v3_geometry(self):
        for case_id in ("H4_SIT_TO_STAND", "H7_NARROW_SHORT_STEP"):
            for morphology in MORPHOLOGIES:
                for size_dp in SIZES:
                    for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                        fixture = build_common_fixture(morphology, case_id, size_dp, t)
                        for variant in ("RF_B", "RF_C"):
                            old = render_fixture_v3(fixture, variant)
                            new = render_fixture_view(fixture, variant)
                            self.assertEqual(new["semanticHash"], fixture.semantic_hash)
                            self.assertEqual(old["shapes"], new["shapes"])
                            self.assertEqual(old["visualBounds"], new["visualBounds"])
                            self.assertEqual(old["partitionBounds"], new["partitionBounds"])
                            self.assertEqual(old["corrections"], new["corrections"])
                            self.assertEqual(
                                new["viewRepresentationVersion"],
                                VIEW_REPRESENTATION_VERSION,
                            )

    def test_h6_semantics_and_rf_variants_remain_identical(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                    fixture = build_common_fixture(
                        morphology, "H6_CHANGE_FACING_2P5D", size_dp, t
                    )
                    rf_b = render_fixture_view(fixture, "RF_B")
                    rf_c = render_fixture_view(fixture, "RF_C")
                    self.assertEqual(rf_b["semanticHash"], fixture.semantic_hash)
                    self.assertEqual(rf_c["semanticHash"], fixture.semantic_hash)
                    self.assertEqual(rf_b["shapes"], rf_c["shapes"])
                    self.assertEqual(rf_b["visualBounds"], rf_c["visualBounds"])
                    self.assertEqual(rf_b["partitionBounds"], rf_c["partitionBounds"])
                    self.assertEqual(rf_b["corrections"], tuple())
                    self.assertEqual(rf_c["corrections"], tuple())

    def test_h6_shapes_are_sorted_far_to_near_deterministically(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                    fixture = build_common_fixture(
                        morphology, "H6_CHANGE_FACING_2P5D", size_dp, t
                    )
                    rendered = render_fixture_view(fixture, "RF_B")
                    keys = [
                        (
                            shape.get("_viewDepth", 0.0),
                            shape.get("_orderBias", 0.0),
                            shape["role"],
                        )
                        for shape in rendered["shapes"]
                    ]
                    self.assertEqual(keys, sorted(keys))

    def test_profile_side_order_reverses_without_identity_swap(self):
        morphology = MORPHOLOGIES[1]
        size_dp = 80

        start = render_fixture_view(
            build_common_fixture(
                morphology, "H6_CHANGE_FACING_2P5D", size_dp, 0.0
            ),
            "RF_B",
        )
        end = render_fixture_view(
            build_common_fixture(
                morphology, "H6_CHANGE_FACING_2P5D", size_dp, 1.0
            ),
            "RF_B",
        )

        start_roles = [shape["role"] for shape in start["shapes"]]
        end_roles = [shape["role"] for shape in end["shapes"]]

        self.assertIn("forelimb_L", start_roles)
        self.assertIn("forelimb_R", start_roles)
        self.assertIn("forelimb_L", end_roles)
        self.assertIn("forelimb_R", end_roles)
        self.assertLess(
            start_roles.index("forelimb_L"), start_roles.index("forelimb_R")
        )
        self.assertLess(
            end_roles.index("forelimb_R"), end_roles.index("forelimb_L")
        )

    def test_front_view_orders_forestructure_in_front_of_hindstructure(self):
        for morphology in MORPHOLOGIES:
            fixture = build_common_fixture(
                morphology, "H6_CHANGE_FACING_2P5D", 80, 0.5
            )
            rendered = render_fixture_view(fixture, "RF_B")
            roles = [shape["role"] for shape in rendered["shapes"]]
            self.assertLess(roles.index("hindlimb_L"), roles.index("forelimb_L"))
            self.assertLess(roles.index("hindlimb_R"), roles.index("forelimb_R"))
            self.assertLess(roles.index("pelvis"), roles.index("forequarter"))
            self.assertLess(roles.index("forequarter"), roles.index("head"))

    def test_front_body_mass_is_wider_than_v3_control(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                fixture = build_common_fixture(
                    morphology, "H6_CHANGE_FACING_2P5D", size_dp, 0.5
                )
                old = render_fixture_v3(fixture, "RF_B")
                new = render_fixture_view(fixture, "RF_B")
                old_fore = next(
                    shape for shape in old["shapes"] if shape["role"] == "forequarter"
                )
                new_fore = next(
                    shape for shape in new["shapes"] if shape["role"] == "forequarter"
                )
                old_pelvis = next(
                    shape for shape in old["shapes"] if shape["role"] == "pelvis"
                )
                new_pelvis = next(
                    shape for shape in new["shapes"] if shape["role"] == "pelvis"
                )
                self.assertGreater(new_fore["rx"], 1.15 * old_fore["rx"])
                self.assertGreater(new_pelvis["rx"], 1.15 * old_pelvis["rx"])

    def test_targeted_matrix_is_deterministic_and_bounded(self):
        first_records, first_summary = run_matrix(sample_count=17)
        second_records, second_summary = run_matrix(sample_count=17)
        self.assertEqual(canonical_bytes(first_records), canonical_bytes(second_records))
        self.assertEqual(canonical_bytes(first_summary), canonical_bytes(second_summary))
        self.assertEqual(first_summary["records"], 6)
        self.assertEqual(first_summary["sampleCountPerRecord"], 17)
        self.assertEqual(first_summary["semanticHashMismatchTotal"], 0)
        self.assertLessEqual(first_summary["maxPartitionGroupCount"], 4)
        self.assertEqual(
            first_summary["viewRepresentationVersion"], VIEW_REPRESENTATION_VERSION
        )


if __name__ == "__main__":
    unittest.main()
