import unittest

from footprint_v1 import analyze_state, rect_union_area, role_group
from model import M0, M1, M2, Rect
from run_footprint_matrix import sample_state


class P1B22FootprintTests(unittest.TestCase):
    def test_rect_union_area_exact_for_overlap(self):
        rects = [Rect(0.0, 0.0, 10.0, 10.0), Rect(5.0, 0.0, 15.0, 10.0)]
        self.assertAlmostEqual(rect_union_area(rects), 150.0, places=9)

    def test_role_group_contract(self):
        self.assertEqual(role_group("tail"), "TAIL")
        self.assertEqual(role_group("FORE_PAW_L"), "FORE")
        self.assertEqual(role_group("forelimb"), "FORE")
        self.assertEqual(role_group("HIND_PAW_R"), "HIND")
        self.assertEqual(role_group("hindlimb"), "HIND")
        self.assertEqual(role_group("hind_thigh"), "CORE")
        self.assertEqual(role_group("head"), "CORE")

    def test_partition_never_exceeds_single_window(self):
        for candidate in ("BM_A", "BM_B", "BM_C"):
            for morphology in (M0, M1, M2):
                for size_dp in (48, 80, 112):
                    for case_id in (
                        "H2_SLOW_WALK",
                        "H4_SIT_TO_STAND",
                        "H6_CHANGE_FACING_2P5D",
                        "H7_NARROW_SHORT_STEP",
                    ):
                        for t in (0.0, 0.5, 1.0):
                            state = sample_state(candidate, morphology, case_id, size_dp, t)
                            result = analyze_state(state, occupancy_grid=16)
                            self.assertEqual(result["errors"], [], (candidate, morphology.id, size_dp, case_id, t, result["errors"]))
                            schemes = result["schemes"]
                            f0 = schemes["F0_SINGLE_ALL"]["blockingAreaDp2"]
                            f1 = schemes["F1_CORE_TAIL"]["blockingAreaDp2"]
                            f2 = schemes["F2_CORE_FORE_HIND_TAIL"]["blockingAreaDp2"]
                            f3 = schemes["F3_ADAPTIVE_LOWER_BOUND"]["blockingAreaDp2"]
                            self.assertLessEqual(f1, f0 + 1e-7)
                            self.assertLessEqual(f2, f0 + 1e-7)
                            self.assertLessEqual(f3, min(f1, f2) + 1e-7)

    def test_f0_matches_canonical_window_area(self):
        state = sample_state("BM_A", M0, "H2_SLOW_WALK", 80, 0.25)
        result = analyze_state(state, occupancy_grid=16)
        self.assertAlmostEqual(
            result["schemes"]["F0_SINGLE_ALL"]["blockingAreaDp2"],
            state.window_bounds.area,
            places=9,
        )

    def test_h6_is_2p5d_orientation_source(self):
        state = sample_state("BM_B", M0, "H6_CHANGE_FACING_2P5D", 80, 0.5)
        self.assertEqual(state.case_id, "H6_CHANGE_FACING_2P5D")
        self.assertTrue(any(note.startswith("bodyYawRad=") for note in state.notes))
        self.assertTrue(any(note.startswith("view=") for note in state.notes))

    def test_effective_occupancy_is_bounded(self):
        state = sample_state("BM_C", M2, "H3_START_WALK_STOP", 96, 0.5)
        result = analyze_state(state, occupancy_grid=16)
        for scheme, item in result["schemes"].items():
            self.assertGreaterEqual(item["effectiveOccupancy"], 0.0, scheme)
            self.assertLessEqual(item["effectiveOccupancy"], 1.0, scheme)
            self.assertGreater(item["windowCount"], 0, scheme)


if __name__ == "__main__":
    unittest.main()
