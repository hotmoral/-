from __future__ import annotations

from c3_renderer_minimal_v3 import render_fixture as render_fixture_v3
from c3_renderer_view_resolved_v4 import _render_h6 as render_view_resolved_h6
from c3_renderers import CORRECTION_H4
from c4_hard_motion_fixture_adapter import H4, H6N

CANDIDATE_B = "VIEW_RESOLVED_RF_B"
CANDIDATE_C = "VIEW_RESOLVED_RF_C_H4"
CANDIDATES = (CANDIDATE_B, CANDIDATE_C)
ADAPTER_VERSION = "P1_C4_HARD_SET_RENDERER_ADAPTER_V1"


def _variant_for_candidate(candidate: str) -> str:
    if candidate == CANDIDATE_B:
        return "RF_B"
    if candidate == CANDIDATE_C:
        return "RF_C"
    raise ValueError(candidate)


def render_c4(fixture, candidate: str):
    variant = _variant_for_candidate(candidate)

    if fixture.case_id == H6N:
        rendered = render_view_resolved_h6(fixture, variant)
    else:
        rendered = render_fixture_v3(fixture, variant)

    if rendered["semanticHash"] != fixture.semantic_hash:
        raise RuntimeError(
            f"semantic hash mismatch candidate={candidate} case={fixture.case_id} "
            f"fixture={fixture.semantic_hash} rendered={rendered['semanticHash']}"
        )

    corrections = tuple(rendered.get("corrections", ()))
    if candidate == CANDIDATE_B and corrections:
        raise RuntimeError(f"C4-B correction budget violated: {corrections}")

    if candidate == CANDIDATE_C:
        if fixture.case_id == H4:
            if corrections != (CORRECTION_H4,):
                raise RuntimeError(f"C4-C H4 correction mismatch: {corrections}")
        elif corrections:
            raise RuntimeError(
                f"C4-C forbids non-H4 correction family: case={fixture.case_id} corrections={corrections}"
            )

    return {
        **rendered,
        "c4Candidate": candidate,
        "c4AdapterVersion": ADAPTER_VERSION,
        "corrections": corrections,
    }
