import unittest

from model import M0, M1, M2, Morphology
from motions_v2 import sample_motion
from metrics_v2 import motion_metrics, silhouette_occupancy
from run_b2_matrix import CANDIDATES, SIZES, MOTION_SAMPLES


class P1B2Tests(unittest.TestCase):
    def test_all_motion_states_validate(self):
        for candidate in CANDIDATES:
            for morphology in (M0, M1, M2):
                for size in SIZES:
                    for case_id, sample_count in MOTION_SAMPLES.items():
                        for index in range(sample_count):
                            state = sample_motion(
                                candidate,
                                morphology,
                                case_id,
                                size,
                                index / (sample_count - 1),
                            )
                            self.assertEqual(
                                state.validate(),
                                [],
                                (
                                    candidate,
                                    morphology.id,
                                    size,
                                    case_id,
                                    index,
                                    state.validate(),
                                ),
                            )

    def test_no_zero_support(self):
        for candidate in CANDIDATES:
            for case_id, sample_count in MOTION_SAMPLES.items():
                states = [
                    sample_motion(
                        candidate,
                        M0,
                        case_id,
                        80,
                        index / (sample_count - 1),
                    )
                    for index in range(sample_count)
                ]
                self.assertEqual(
                    motion_metrics(states)["zeroSupportSampleCount"],
                    0,
                    (candidate, case_id),
                )

    def test_planted_paw_world_drift_is_numerical_only(self):
        for candidate in CANDIDATES:
            for case_id in (
                "H2_SLOW_WALK",
                "H3_START_WALK_STOP",
                "H7_NARROW_SHORT_STEP",
            ):
                sample_count = MOTION_SAMPLES[case_id]
                states = [
                    sample_motion(
                        candidate,
                        M0,
                        case_id,
                        80,
                        index / (sample_count - 1),
                    )
                    for index in range(sample_count)
                ]
                self.assertLess(
                    motion_metrics(states)["maxPlantedPawDriftDp"],
                    1e-6,
                    (candidate, case_id),
                )

    def test_turn_anchor_continuity_has_no_midpoint_flip(self):
        for candidate in CANDIDATES:
            sample_count = MOTION_SAMPLES["H6_CHANGE_FACING"]
            states = [
                sample_motion(
                    candidate,
                    M0,
                    "H6_CHANGE_FACING",
                    80,
                    index / (sample_count - 1),
                )
                for index in range(sample_count)
            ]
            max_jump = 0.0
            for previous, current in zip(states, states[1:]):
                for anchor_name in previous.anchors:
                    max_jump = max(
                        max_jump,
                        (current.anchors[anchor_name] - previous.anchors[anchor_name]).length(),
                    )
            self.assertLess(max_jump, 4.0, (candidate, max_jump))

    def test_morphology_interpolation_continuity(self):
        previous = None
        for index in range(21):
            t = index / 20
            morphology = Morphology.blend(M1, M2, t, f"L{index}")
            state = sample_motion("BM_B", morphology, "H2_SLOW_WALK", 80, 0.25)
            if previous is not None:
                self.assertLess(
                    (state.anchors["HEAD_ROOT"] - previous.anchors["HEAD_ROOT"]).length(),
                    4.0,
                )
            previous = state

    def test_occupancy_metric_detects_internal_slack(self):
        state = sample_motion("BM_B", M0, "H2_SLOW_WALK", 80, 0.5)
        occupancy = silhouette_occupancy(state, 48)
        self.assertGreater(occupancy["silhouetteOccupancyRatio"], 0.0)
        self.assertLess(occupancy["silhouetteOccupancyRatio"], 1.0)
        self.assertGreater(occupancy["blockingSlackAreaDp2"], 0.0)


if __name__ == "__main__":
    unittest.main()
