import unittest

from c3_renderers import CORRECTION_H4
from c3_semantic import canonical_bytes, semantic_payload
from c4_hard_motion_fixture_adapter import (
    CASES,
    H4,
    H6N,
    MORPHOLOGIES,
    SIZES,
    build_c4_fixture,
    directions_for_case,
    scorecard_times,
)
from c4_renderer_adapter import CANDIDATE_B, CANDIDATE_C, CANDIDATES, render_c4
from run_c3_matrix import render_payload
from run_c4_hard_motion_matrix import run_matrix


def _geometry_payload(rendered):
    payload = render_payload(rendered)
    payload.pop("variant", None)
    return payload


class C4HardMotionTests(unittest.TestCase):
    def test_all_scorecard_fixtures_validate_and_preserve_semantic_payload(self):
        for case_id in CASES:
            for morphology in MORPHOLOGIES:
                for size_dp in SIZES:
                    for direction in directions_for_case(case_id):
                        for t in scorecard_times(case_id):
                            fixture = build_c4_fixture(morphology, case_id, size_dp, t, direction)
                            self.assertEqual(fixture.state.validate(), [])
                            self.assertEqual(fixture.payload, semantic_payload(fixture.state))

    def test_candidate_c_uses_exactly_one_h4_correction_and_nowhere_else(self):
        for case_id in CASES:
            for morphology in MORPHOLOGIES:
                for size_dp in SIZES:
                    for direction in directions_for_case(case_id):
                        for t in scorecard_times(case_id):
                            fixture = build_c4_fixture(morphology, case_id, size_dp, t, direction)
                            rendered_b = render_c4(fixture, CANDIDATE_B)
                            rendered_c = render_c4(fixture, CANDIDATE_C)
                            self.assertEqual(tuple(rendered_b["corrections"]), tuple())
                            expected_c = (CORRECTION_H4,) if case_id == H4 else tuple()
                            self.assertEqual(tuple(rendered_c["corrections"]), expected_c)
                            self.assertLessEqual(len(rendered_b["partitionBounds"]), 4)
                            self.assertLessEqual(len(rendered_c["partitionBounds"]), 4)

    def test_candidates_are_geometry_identical_outside_h4(self):
        for case_id in CASES:
            if case_id == H4:
                continue
            for morphology in MORPHOLOGIES:
                for size_dp in SIZES:
                    for direction in directions_for_case(case_id):
                        for t in scorecard_times(case_id):
                            fixture = build_c4_fixture(morphology, case_id, size_dp, t, direction)
                            rf_b = render_c4(fixture, CANDIDATE_B)
                            rf_c = render_c4(fixture, CANDIDATE_C)
                            self.assertEqual(
                                canonical_bytes(_geometry_payload(rf_b)),
                                canonical_bytes(_geometry_payload(rf_c)),
                            )

    def test_h6n_uses_view_resolved_path_without_authored_correction(self):
        for morphology in MORPHOLOGIES:
            for size_dp in SIZES:
                for direction in directions_for_case(H6N):
                    for t in scorecard_times(H6N):
                        fixture = build_c4_fixture(morphology, H6N, size_dp, t, direction)
                        for candidate in CANDIDATES:
                            rendered = render_c4(fixture, candidate)
                            self.assertEqual(
                                rendered.get("viewRepresentationVersion"),
                                "VIEW_RESOLVED_2P5D_V1",
                            )
                            self.assertEqual(tuple(rendered["corrections"]), tuple())

    def test_h4_retained_correction_materially_reduces_height_step(self):
        records, _ = run_matrix()
        h4_records = [record for record in records if record["caseId"] == H4]
        self.assertEqual(len(h4_records), 6)
        for record in h4_records:
            b_step = record["candidates"][CANDIDATE_B]["maxVisualHeightStepDp"]
            c_step = record["candidates"][CANDIDATE_C]["maxVisualHeightStepDp"]
            self.assertGreater(b_step, 0.0)
            self.assertLess(c_step, b_step * 0.40)

    def test_full_matrix_is_byte_deterministic_and_correction_budget_is_sparse(self):
        first_records, first_summary = run_matrix()
        second_records, second_summary = run_matrix()
        self.assertEqual(canonical_bytes(first_records), canonical_bytes(second_records))
        self.assertEqual(canonical_bytes(first_summary), canonical_bytes(second_summary))
        self.assertEqual(first_summary["records"], 48)
        self.assertEqual(first_summary["semanticHashMismatchTotal"], 0)
        self.assertEqual(first_summary["correctionFamiliesByCandidate"][CANDIDATE_B], [])
        self.assertEqual(
            first_summary["correctionFamiliesByCandidate"][CANDIDATE_C],
            [CORRECTION_H4],
        )
        self.assertTrue(
            all(value <= 4 for value in first_summary["maxPartitionGroupCountByCandidate"].values())
        )
        for case_id, mismatch_count in first_summary["geometryMismatchByCase"].items():
            if case_id == H4:
                self.assertGreater(mismatch_count, 0)
            else:
                self.assertEqual(mismatch_count, 0)


if __name__ == "__main__":
    unittest.main()
