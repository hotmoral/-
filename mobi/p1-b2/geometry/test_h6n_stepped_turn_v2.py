import math
import unittest

from h6n_stepped_turn import MIRROR_PAW, PAWS, solve_h6n_stepped_turn
from h6n_stepped_turn_v2 import (
    LOGICAL_PHASE_COUNT,
    NEGATIVE_ORDER,
    POSITIVE_ORDER,
    ROOT_SHIFT_NORMALIZED,
    SHIFT_PHASE_INDEX,
    YAW_PER_EVENT,
    _smoothstep,
    event_order,
    root_shift_dp,
    shifted_stance_target_s,
    solve_h6n_stepped_turn_v2,
)
from orientation_v2 import M0_V2, M1_V2, M2_V2

MORPHOLOGIES = (M1_V2, M0_V2, M2_V2)
SIZES = (80, 96)
DIRECTIONS = (+1, -1)
HALF_STANCES = (0.18, 0.22, 0.26)
EXPECTED_C3T_GLOBAL_MIN_CLEARANCE = 0.11159424929136375


def _note_value(state, prefix):
    for note in state.notes:
        if note.startswith(prefix):
            return note.split("=", 1)[1]
    raise KeyError(prefix)


def _yaw(state):
    return float(_note_value(state, "bodyYawRad="))


def _root_progress(state):
    return float(_note_value(state, "rootShiftProgress="))


def _contact_by_owner(state):
    return {contact.owner: contact for contact in state.contacts}


def _assert_point_close(testcase, a, b, places=10):
    testcase.assertAlmostEqual(a.x, b.x, places=places)
    testcase.assertAlmostEqual(a.y, b.y, places=places)


def _side_sign(paw):
    return +1.0 if paw.endswith("_L") else -1.0


class H6NSteppedQuarterTurnV2Tests(unittest.TestCase):
    def test_v1_remains_callable_as_regression_oracle(self):
        state = solve_h6n_stepped_turn(M0_V2, 80, 0.5, +1)
        self.assertEqual(state.validate(), [])
        self.assertEqual(state.case_id, "H6N_STEPPED_QUARTER_TURN_V1")

    def test_phase3_orders_are_exact_anatomical_mirrors(self):
        self.assertEqual(
            POSITIVE_ORDER,
            ("FORE_PAW_L", "HIND_PAW_R", "FORE_PAW_R", "HIND_PAW_L"),
        )
        self.assertEqual(event_order(+1), POSITIVE_ORDER)
        self.assertEqual(event_order(-1), NEGATIVE_ORDER)
        self.assertEqual(
            NEGATIVE_ORDER,
            tuple(MIRROR_PAW[paw] for paw in POSITIVE_ORDER),
        )

    def test_cubic_shift_curve_is_monotonic_and_exact_at_endpoints(self):
        samples = [_smoothstep(i / 100.0) for i in range(101)]
        self.assertEqual(samples[0], 0.0)
        self.assertEqual(samples[-1], 1.0)
        self.assertAlmostEqual(_smoothstep(0.5), 0.5, places=15)
        self.assertTrue(all(b >= a for a, b in zip(samples, samples[1:])))
        self.assertAlmostEqual(root_shift_dp(80, 1.0) / 40.0, ROOT_SHIFT_NORMALIZED, places=12)
        self.assertAlmostEqual(root_shift_dp(96, 1.0) / 48.0, ROOT_SHIFT_NORMALIZED, places=12)

    def test_all_logical_boundaries_are_four_support_states(self):
        expected_yaw_units = (0, 1, 2, 3, 3, 4)
        expected_root_progress = (0, 0, 0, 0, 1, 1)
        for direction in DIRECTIONS:
            for boundary in range(LOGICAL_PHASE_COUNT + 1):
                t = boundary / LOGICAL_PHASE_COUNT
                state = solve_h6n_stepped_turn_v2(M0_V2, 80, t, direction)
                self.assertEqual(state.validate(), [])
                self.assertEqual(len(state.support_set), 4)
                self.assertEqual(
                    sum(contact.load_bearing for contact in state.contacts),
                    4,
                )
                self.assertAlmostEqual(
                    _yaw(state),
                    direction * expected_yaw_units[boundary] * YAW_PER_EVENT,
                    places=10,
                )
                self.assertAlmostEqual(
                    _root_progress(state),
                    expected_root_progress[boundary],
                    places=12,
                )

    def test_swing_phases_have_one_swing_paw_and_three_supports(self):
        phase_to_event = {0: 0, 1: 1, 2: 2, 4: 3}
        for direction in DIRECTIONS:
            order = event_order(direction)
            for phase, event_index in phase_to_event.items():
                t = (phase + 0.5) / LOGICAL_PHASE_COUNT
                state = solve_h6n_stepped_turn_v2(M0_V2, 80, t, direction)
                contacts = _contact_by_owner(state)
                swinging = [paw for paw, contact in contacts.items() if not contact.load_bearing]
                self.assertEqual(swinging, [order[event_index]])
                self.assertEqual(len(state.support_set), 3)

    def test_root_shift_phase_keeps_all_paws_exactly_stationary(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in DIRECTIONS:
                    start = solve_h6n_stepped_turn_v2(
                        morphology,
                        size_dp,
                        SHIFT_PHASE_INDEX / LOGICAL_PHASE_COUNT,
                        direction,
                    )
                    reference = _contact_by_owner(start)
                    states = [
                        solve_h6n_stepped_turn_v2(
                            morphology,
                            size_dp,
                            (SHIFT_PHASE_INDEX + u) / LOGICAL_PHASE_COUNT,
                            direction,
                        )
                        for u in (0.1, 0.25, 0.5, 0.75, 0.9)
                    ]
                    for state in states:
                        self.assertEqual(len(state.support_set), 4)
                        self.assertAlmostEqual(
                            _yaw(state),
                            direction * 3 * YAW_PER_EVENT,
                            places=10,
                        )
                        contacts = _contact_by_owner(state)
                        for paw in PAWS:
                            self.assertTrue(contacts[paw].load_bearing)
                            _assert_point_close(self, contacts[paw].point, reference[paw].point)

    def test_root_moves_monotonically_without_boundary_jump(self):
        for direction in DIRECTIONS:
            samples = [
                solve_h6n_stepped_turn_v2(
                    M0_V2,
                    80,
                    (SHIFT_PHASE_INDEX + i / 100.0) / LOGICAL_PHASE_COUNT,
                    direction,
                )
                for i in range(101)
            ]
            xs = [state.anchors["BODY_ROOT"].x for state in samples]
            self.assertTrue(all(b >= a - 1e-12 for a, b in zip(xs, xs[1:])))
            self.assertAlmostEqual(xs[-1] - xs[0], root_shift_dp(80), places=10)

            eps = 1e-8
            for boundary in (
                SHIFT_PHASE_INDEX / LOGICAL_PHASE_COUNT,
                (SHIFT_PHASE_INDEX + 1) / LOGICAL_PHASE_COUNT,
            ):
                left = solve_h6n_stepped_turn_v2(M0_V2, 80, max(0.0, boundary - eps), direction)
                exact = solve_h6n_stepped_turn_v2(M0_V2, 80, boundary, direction)
                right = solve_h6n_stepped_turn_v2(M0_V2, 80, min(1.0, boundary + eps), direction)
                self.assertLess(abs(left.anchors["BODY_ROOT"].x - exact.anchors["BODY_ROOT"].x), 1e-7)
                self.assertLess(abs(right.anchors["BODY_ROOT"].x - exact.anchors["BODY_ROOT"].x), 1e-7)

    def test_planted_paws_do_not_move_inside_any_swing_phase(self):
        phase_to_event = {0: 0, 1: 1, 2: 2, 4: 3}
        for direction in DIRECTIONS:
            order = event_order(direction)
            for phase, event_index in phase_to_event.items():
                swing_paw = order[event_index]
                states = [
                    solve_h6n_stepped_turn_v2(
                        M0_V2,
                        80,
                        (phase + u) / LOGICAL_PHASE_COUNT,
                        direction,
                    )
                    for u in (0.2, 0.5, 0.8)
                ]
                contacts = [_contact_by_owner(state) for state in states]
                for paw in PAWS:
                    if paw == swing_paw:
                        continue
                    reference = contacts[0][paw].point
                    for contact_map in contacts[1:]:
                        self.assertTrue(contact_map[paw].load_bearing)
                        _assert_point_close(self, contact_map[paw].point, reference)

    def test_final_hind_replant_uses_shifted_body_relative_target(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in DIRECTIONS:
                    state = solve_h6n_stepped_turn_v2(morphology, size_dp, 1.0, direction)
                    final_paw = event_order(direction)[-1]
                    expected = shifted_stance_target_s(
                        final_paw,
                        morphology,
                        size_dp,
                        direction,
                        direction * math.pi / 2.0,
                        1.0,
                    )
                    _assert_point_close(self, state.anchors[final_paw], expected)
                    self.assertAlmostEqual(_yaw(state), direction * math.pi / 2.0, places=10)

    def test_positive_negative_v2_are_exact_screen_coordinate_anatomical_mirrors(self):
        structural = (
            "BODY_ROOT",
            "FOREQUARTER_REF",
            "PELVIS_REF",
            "HEAD_ROOT",
            "TAIL_ROOT",
        )
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for index in range(41):
                    t = index / 40.0
                    positive = solve_h6n_stepped_turn_v2(morphology, size_dp, t, +1)
                    negative = solve_h6n_stepped_turn_v2(morphology, size_dp, t, -1)
                    for anchor in structural:
                        _assert_point_close(self, positive.anchors[anchor], negative.anchors[anchor])

                    pos_contacts = _contact_by_owner(positive)
                    neg_contacts = _contact_by_owner(negative)
                    for positive_paw in PAWS:
                        negative_paw = MIRROR_PAW[positive_paw]
                        _assert_point_close(
                            self,
                            positive.anchors[positive_paw],
                            negative.anchors[negative_paw],
                        )
                        self.assertEqual(
                            pos_contacts[positive_paw].phase,
                            neg_contacts[negative_paw].phase,
                        )
                        self.assertEqual(
                            pos_contacts[positive_paw].load_bearing,
                            neg_contacts[negative_paw].load_bearing,
                        )

    def test_c3t_final_clearance_is_reproduced_across_sensitivity_set(self):
        observed_minima = []
        for morphology in MORPHOLOGIES:
            for half_stance in HALF_STANCES:
                state = solve_h6n_stepped_turn_v2(
                    morphology,
                    80,
                    1.0,
                    +1,
                    lateral_half_stance_bu=half_stance,
                )
                scale = 40.0
                root_x = state.anchors["BODY_ROOT"].x
                clearances = {
                    paw: _side_sign(paw) * ((state.anchors[paw].x - root_x) / scale)
                    for paw in PAWS
                }
                self.assertTrue(all(value >= -1e-12 for value in clearances.values()))
                observed_minima.append(min(clearances.values()))

        self.assertAlmostEqual(
            min(observed_minima),
            EXPECTED_C3T_GLOBAL_MIN_CLEARANCE,
            places=12,
        )

    def test_full_primary_matrix_validates(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in DIRECTIONS:
                    for index in range(41):
                        state = solve_h6n_stepped_turn_v2(
                            morphology,
                            size_dp,
                            index / 40.0,
                            direction,
                        )
                        self.assertEqual(state.validate(), [])


if __name__ == "__main__":
    unittest.main()
