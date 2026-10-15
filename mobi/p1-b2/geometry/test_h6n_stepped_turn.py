import math
import unittest

from h6n_stepped_turn import (
    EVENT_COUNT,
    MIRROR_PAW,
    NEGATIVE_ORDER,
    PAWS,
    POSITIVE_ORDER,
    YAW_PER_EVENT,
    event_order,
    solve_h6n_stepped_turn,
    stance_target_s,
)
from orientation_v2 import M0_V2, M1_V2, M2_V2
from run_h6n_fixture_matrix import run_matrix


MORPHOLOGIES = (M1_V2, M0_V2, M2_V2)
SIZES = (80, 96)
DIRECTIONS = (+1, -1)


def _note_value(state, prefix):
    for note in state.notes:
        if note.startswith(prefix):
            return note.split("=", 1)[1]
    raise KeyError(prefix)


def _yaw(state):
    return float(_note_value(state, "bodyYawRad="))


def _contact_by_owner(state):
    return {contact.owner: contact for contact in state.contacts}


def _assert_point_close(testcase, a, b, places=10):
    testcase.assertAlmostEqual(a.x, b.x, places=places)
    testcase.assertAlmostEqual(a.y, b.y, places=places)


class H6NSteppedQuarterTurnTests(unittest.TestCase):
    def test_declared_orders_are_anatomical_mirrors(self):
        self.assertEqual(event_order(+1), POSITIVE_ORDER)
        self.assertEqual(event_order(-1), NEGATIVE_ORDER)
        self.assertEqual(
            NEGATIVE_ORDER,
            tuple(MIRROR_PAW[paw] for paw in POSITIVE_ORDER),
        )

    def test_event_boundaries_have_four_supports_and_exact_key_yaw(self):
        for direction in DIRECTIONS:
            for boundary in range(EVENT_COUNT + 1):
                t = boundary / EVENT_COUNT
                state = solve_h6n_stepped_turn(M0_V2, 80, t, direction)
                self.assertEqual(state.validate(), [])
                self.assertEqual(len(state.support_set), 4)
                contacts = _contact_by_owner(state)
                self.assertTrue(all(contact.load_bearing for contact in contacts.values()))
                self.assertAlmostEqual(
                    _yaw(state),
                    direction * boundary * YAW_PER_EVENT,
                    places=10,
                )

    def test_interior_event_has_one_swing_and_three_supports_in_declared_order(self):
        for direction in DIRECTIONS:
            order = event_order(direction)
            for event_index, expected_swing in enumerate(order):
                t = (event_index + 0.5) / EVENT_COUNT
                state = solve_h6n_stepped_turn(M0_V2, 80, t, direction)
                self.assertEqual(state.validate(), [])
                self.assertEqual(len(state.support_set), 3)
                contacts = _contact_by_owner(state)
                swinging = [
                    paw for paw, contact in contacts.items()
                    if not contact.load_bearing
                ]
                self.assertEqual(swinging, [expected_swing])
                self.assertIsNone(contacts[expected_swing].target_point)

    def test_planted_paws_do_not_move_inside_an_event(self):
        for direction in DIRECTIONS:
            order = event_order(direction)
            for event_index, swing_paw in enumerate(order):
                states = [
                    solve_h6n_stepped_turn(
                        M0_V2,
                        80,
                        (event_index + local_u) / EVENT_COUNT,
                        direction,
                    )
                    for local_u in (0.2, 0.5, 0.8)
                ]
                contacts = [_contact_by_owner(state) for state in states]
                for paw in PAWS:
                    if paw == swing_paw:
                        continue
                    reference = contacts[0][paw].point
                    for contact_map in contacts[1:]:
                        _assert_point_close(self, reference, contact_map[paw].point)
                        self.assertTrue(contact_map[paw].load_bearing)

    def test_each_replant_hits_its_body_relative_post_event_target(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in DIRECTIONS:
                    order = event_order(direction)
                    for event_index, moved_paw in enumerate(order):
                        boundary = event_index + 1
                        t = boundary / EVENT_COUNT
                        yaw = direction * boundary * YAW_PER_EVENT
                        state = solve_h6n_stepped_turn(
                            morphology,
                            size_dp,
                            t,
                            direction,
                        )
                        expected = stance_target_s(
                            moved_paw,
                            morphology,
                            size_dp,
                            direction,
                            yaw,
                        )
                        _assert_point_close(self, state.anchors[moved_paw], expected)

    def test_positive_and_negative_fixtures_are_exact_anatomical_mirrors(self):
        structural = (
            "BODY_ROOT",
            "FOREQUARTER_REF",
            "PELVIS_REF",
            "HEAD_ROOT",
            "TAIL_ROOT",
        )
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for index in range(33):
                    t = index / 32.0
                    positive = solve_h6n_stepped_turn(morphology, size_dp, t, +1)
                    negative = solve_h6n_stepped_turn(morphology, size_dp, t, -1)
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

    def test_yaw_is_monotonic_continuous_and_reaches_quarter_turn(self):
        for direction in DIRECTIONS:
            states = [
                solve_h6n_stepped_turn(M0_V2, 80, index / 128.0, direction)
                for index in range(129)
            ]
            yaws = [_yaw(state) for state in states]
            deltas = [yaws[i + 1] - yaws[i] for i in range(len(yaws) - 1)]
            if direction > 0:
                self.assertTrue(all(delta >= -1e-12 for delta in deltas))
            else:
                self.assertTrue(all(delta <= 1e-12 for delta in deltas))
            self.assertLess(max(abs(delta) for delta in deltas), math.pi / 16.0)
            self.assertAlmostEqual(yaws[-1], direction * math.pi / 2.0, places=10)

    def test_full_targeted_matrix_validates_across_morphology_size_direction(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in DIRECTIONS:
                    for index in range(33):
                        state = solve_h6n_stepped_turn(
                            morphology,
                            size_dp,
                            index / 32.0,
                            direction,
                        )
                        self.assertEqual(state.validate(), [])

    def test_matrix_is_byte_deterministic_and_support_bounded(self):
        first_records, first_summary = run_matrix(sample_count=33)
        second_records, second_summary = run_matrix(sample_count=33)
        self.assertEqual(first_records, second_records)
        self.assertEqual(first_summary, second_summary)
        self.assertEqual(first_summary["records"], 12)
        self.assertEqual(first_summary["supportCountMin"], 3)
        self.assertEqual(first_summary["supportCountMax"], 4)


if __name__ == "__main__":
    unittest.main()
