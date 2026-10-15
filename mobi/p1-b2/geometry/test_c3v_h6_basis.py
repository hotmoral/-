import unittest

from c3_renderer_authored_view_basis_v5 import (
    AUTHORED_VIEW_BASIS_VERSION,
    BASIS_NAMES,
    VIEW_BASES,
    render_fixture as render_fixture_basis,
)
from c3_renderer_minimal_v3 import render_fixture as render_fixture_v3
from c3_semantic import MORPHOLOGIES, SIZES, build_common_fixture
from run_c3_matrix import canonical_bytes
from run_c3v_h6_matrix import run_matrix


class P1C3VAuthoredViewBasisTests(unittest.TestCase):
    def test_basis_budget_is_exactly_three_shared_concepts(self):
        self.assertEqual(BASIS_NAMES, ("PROFILE", "THREE_QUARTER", "FRONT"))
        self.assertEqual(tuple(VIEW_BASES.keys()), BASIS_NAMES)
        keys = tuple(VIEW_BASES["PROFILE"].keys())
        self.assertTrue(keys)
        for name in BASIS_NAMES:
            self.assertEqual(tuple(VIEW_BASES[name].keys()), keys)

    def test_non_h6_paths_are_exact_v3_geometry(self):
        for case_id in ("H4_SIT_TO_STAND", "H7_NARROW_SHORT_STEP"):
            for morphology in MORPHOLOGIES:
                for size_dp in SIZES:
                    for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                        fixture = build_common_fixture(morphology, case_id, size_dp, t)
                        for variant in ("RF_B", "RF_C"):
                            old = render_fixture_v3(fixture, variant)
                            new = render_fixture_basis(fixture, variant)
                            self.assertEqual(new["semanticHash"], fixture.semantic_hash)
                            self.assertEqual(old["shapes"], new["shapes"])
                            self.assertEqual(old["visualBounds"], new["visualBounds"])
                            self.assertEqual(old["partitionBounds"], new["partitionBounds"])
                            self.assertEqual(old["corrections"], new["corrections"])
                            self.assertEqual(
                                new["authoredViewBasisVersion"],
                                AUTHORED_VIEW_BASIS_VERSION,
                            )

    def test_h6_semantics_and_rf_variants_remain_identical(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                    fixture = build_common_fixture(
                        morphology, "H6_CHANGE_FACING_2P5D", size_dp, t
                    )
                    rf_b = render_fixture_basis(fixture, "RF_B")
                    rf_c = render_fixture_basis(fixture, "RF_C")
                    self.assertEqual(rf_b["semanticHash"], fixture.semantic_hash)
                    self.assertEqual(rf_c["semanticHash"], fixture.semantic_hash)
                    self.assertEqual(rf_b["shapes"], rf_c["shapes"])
                    self.assertEqual(rf_b["visualBounds"], rf_c["visualBounds"])
                    self.assertEqual(rf_b["partitionBounds"], rf_c["partitionBounds"])
                    self.assertEqual(rf_b["corrections"], tuple())
                    self.assertEqual(rf_c["corrections"], tuple())

    def test_planted_paw_visual_endpoints_equal_canonical_endpoints(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for index in range(17):
                    t = index / 16.0
                    fixture = build_common_fixture(
                        morphology, "H6_CHANGE_FACING_2P5D", size_dp, t
                    )
                    rendered = render_fixture_basis(fixture, "RF_B")
                    by_role = {shape["role"]: shape for shape in rendered["shapes"]}
                    for contact in fixture.state.contacts:
                        if not contact.load_bearing:
                            continue
                        paw = fixture.state.anchors[contact.owner]
                        paw_shape = by_role[contact.owner]
                        self.assertEqual(paw_shape["cx"], paw.x)
                        self.assertEqual(paw_shape["cy"], paw.y)

                        limb_suffix = "L" if contact.owner.endswith("_L") else "R"
                        if contact.owner.startswith("FORE"):
                            limb = by_role[f"basis_forelimb_{limb_suffix}"]
                        else:
                            limb = by_role[f"basis_hindlimb_{limb_suffix}"]
                        self.assertEqual(limb["points"][-1], paw)

    def test_key_yaws_hit_only_the_three_declared_bases(self):
        morphology = MORPHOLOGIES[1]
        for t, expected in (
            (0.0, "PROFILE"),
            (0.25, "THREE_QUARTER"),
            (0.5, "FRONT"),
            (0.75, "THREE_QUARTER"),
            (1.0, "PROFILE"),
        ):
            fixture = build_common_fixture(
                morphology, "H6_CHANGE_FACING_2P5D", 80, t
            )
            rendered = render_fixture_basis(fixture, "RF_B")
            weights = dict(rendered["basisWeights"])
            self.assertAlmostEqual(weights[expected], 1.0, delta=1e-9)
            self.assertAlmostEqual(sum(weights.values()), 1.0, delta=1e-9)
            self.assertEqual(set(weights), set(BASIS_NAMES))

    def test_front_proximal_limb_routes_preserve_anatomical_side_corridors(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                fixture = build_common_fixture(
                    morphology, "H6_CHANGE_FACING_2P5D", size_dp, 0.5
                )
                rendered = render_fixture_basis(fixture, "RF_B")
                body_x = fixture.state.anchors["BODY_ROOT"].x
                by_role = {shape["role"]: shape for shape in rendered["shapes"]}

                # At front, anatomical L projects to +screen-x and R to -screen-x.
                self.assertGreater(by_role["basis_forelimb_L"]["points"][1].x, body_x)
                self.assertLess(by_role["basis_forelimb_R"]["points"][1].x, body_x)
                self.assertGreater(by_role["basis_hindlimb_L"]["points"][1].x, body_x)
                self.assertLess(by_role["basis_hindlimb_R"]["points"][1].x, body_x)

    def test_shapes_are_sorted_far_to_near_deterministically(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                    fixture = build_common_fixture(
                        morphology, "H6_CHANGE_FACING_2P5D", size_dp, t
                    )
                    rendered = render_fixture_basis(fixture, "RF_B")
                    keys = [
                        (
                            shape.get("_viewDepth", 0.0),
                            shape.get("_orderBias", 0.0),
                            shape["role"],
                        )
                        for shape in rendered["shapes"]
                    ]
                    self.assertEqual(keys, sorted(keys))

    def test_targeted_matrix_is_deterministic_semantic_exact_and_bounded(self):
        first_records, first_summary = run_matrix(sample_count=17)
        second_records, second_summary = run_matrix(sample_count=17)
        self.assertEqual(canonical_bytes(first_records), canonical_bytes(second_records))
        self.assertEqual(canonical_bytes(first_summary), canonical_bytes(second_summary))
        self.assertEqual(first_summary["records"], 6)
        self.assertEqual(first_summary["sampleCountPerRecord"], 17)
        self.assertEqual(first_summary["semanticHashMismatchTotal"], 0)
        self.assertLessEqual(first_summary["maxPartitionGroupCount"], 4)
        self.assertEqual(first_summary["basisNames"], list(BASIS_NAMES))
        self.assertEqual(
            first_summary["authoredViewBasisVersion"],
            AUTHORED_VIEW_BASIS_VERSION,
        )


if __name__ == "__main__":
    unittest.main()
