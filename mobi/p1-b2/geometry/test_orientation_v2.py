import unittest

from math import pi

from metrics_v2 import motion_metrics, silhouette_occupancy
from model import Vec2
from orientation_v2 import M0_V2, M1_V2, M2_V2, Vec3, project_b3
from turn_2p5d import solve_turn_2p5d


class P1OrientationV2Tests(unittest.TestCase):
    def test_side_profile_hides_lateral_and_front_exposes_it(self):
        root = Vec2(100.0, 100.0)
        left = Vec3(0.0, 0.0, +0.25)
        right = Vec3(0.0, 0.0, -0.25)
        side_left = project_b3(left, root, 40.0, 0.0)
        side_right = project_b3(right, root, 40.0, 0.0)
        front_left = project_b3(left, root, 40.0, pi / 2.0)
        front_right = project_b3(right, root, 40.0, pi / 2.0)
        self.assertAlmostEqual(side_left.x, side_right.x, places=9)
        self.assertGreater(abs(front_left.x - front_right.x), 19.9)

    def test_all_candidates_morphologies_sizes_validate_through_turn(self):
        for candidate in ("BM_A", "BM_B", "BM_C"):
            for morphology in (M0_V2, M1_V2, M2_V2):
                for size_dp in (48, 64, 80, 96, 112):
                    for index in range(41):
                        state = solve_turn_2p5d(candidate, morphology, size_dp, index / 40.0)
                        self.assertEqual(
                            state.validate(),
                            [],
                            (candidate, morphology.id, size_dp, index, state.validate()),
                        )

    def test_turn_never_has_zero_support_and_planted_paws_do_not_drift(self):
        for candidate in ("BM_A", "BM_B", "BM_C"):
            states = [solve_turn_2p5d(candidate, M0_V2, 80, index / 40.0) for index in range(41)]
            metrics = motion_metrics(states)
            self.assertEqual(metrics["zeroSupportSampleCount"], 0, candidate)
            self.assertLess(metrics["maxPlantedPawDriftDp"], 1e-6, candidate)

    def test_opposite_profile_reverses_fore_pelvis_order(self):
        for candidate in ("BM_A", "BM_B", "BM_C"):
            start = solve_turn_2p5d(candidate, M0_V2, 80, 0.0)
            end = solve_turn_2p5d(candidate, M0_V2, 80, 1.0)
            self.assertGreater(start.anchors["FOREQUARTER_REF"].x, start.anchors["PELVIS_REF"].x)
            self.assertLess(end.anchors["FOREQUARTER_REF"].x, end.anchors["PELVIS_REF"].x)

    def test_midturn_body_references_are_continuous(self):
        for candidate in ("BM_A", "BM_B", "BM_C"):
            states = [solve_turn_2p5d(candidate, M0_V2, 80, index / 40.0) for index in range(41)]
            max_jump = 0.0
            body_refs = ("BODY_ROOT", "FOREQUARTER_REF", "PELVIS_REF", "HEAD_ROOT", "TAIL_ROOT")
            for previous, current in zip(states, states[1:]):
                for name in body_refs:
                    max_jump = max(max_jump, (current.anchors[name] - previous.anchors[name]).length())
            self.assertLess(max_jump, 4.0, (candidate, max_jump))

    def test_front_view_does_not_collapse_window_to_line(self):
        for candidate in ("BM_A", "BM_B", "BM_C"):
            side = solve_turn_2p5d(candidate, M0_V2, 80, 0.0)
            front = solve_turn_2p5d(candidate, M0_V2, 80, 0.5)
            self.assertGreater(front.visual_bounds.width, 0.28 * side.visual_bounds.width, candidate)
            occupancy = silhouette_occupancy(front, 48)
            self.assertGreater(occupancy["silhouetteOccupancyRatio"], 0.0)
            self.assertLess(occupancy["silhouetteOccupancyRatio"], 1.0)

    def test_width_stress_profiles_are_separated(self):
        self.assertLess(M1_V2.thorax_width_scale, M2_V2.thorax_width_scale)
        self.assertLess(M1_V2.pelvis_width_scale, M2_V2.pelvis_width_scale)
        self.assertLess(M1_V2.stance_width_scale, M2_V2.stance_width_scale)


if __name__ == "__main__":
    unittest.main()
