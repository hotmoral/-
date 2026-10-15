from __future__ import annotations

from contextlib import contextmanager

import c3_semantic
from c3_renderers import CORRECTION_H4
from c4_renderer_adapter import CANDIDATE_C, render_c4
from e_v0_fixture_adapter import H4
from e_v0_profiles import MORPHOLOGIES, ORIENTATION_BY_ID

ADAPTER_VERSION = "P1_E_V0_RENDERER_ADAPTER_V1"
STRUCTURAL_DIRECTION = "NATURALISTIC_STRUCTURAL_ENVELOPE_V0"
READABILITY_AID_MODE = "NONE_BASELINE"


@contextmanager
def _registered_e_profiles():
    """Temporarily extend the frozen C3 lookup registry without editing its source."""
    old_morphologies = c3_semantic.MORPHOLOGIES
    old_orientation = c3_semantic.ORIENTATION_MORPH
    c3_semantic.MORPHOLOGIES = MORPHOLOGIES
    c3_semantic.ORIENTATION_MORPH = dict(ORIENTATION_BY_ID)
    try:
        yield
    finally:
        c3_semantic.MORPHOLOGIES = old_morphologies
        c3_semantic.ORIENTATION_MORPH = old_orientation


def render_e(fixture):
    before_morphologies = c3_semantic.MORPHOLOGIES
    before_orientation = c3_semantic.ORIENTATION_MORPH

    with _registered_e_profiles():
        rendered = render_c4(fixture, CANDIDATE_C)

    if c3_semantic.MORPHOLOGIES is not before_morphologies:
        raise RuntimeError("P1-E morphology registry leaked after render")
    if c3_semantic.ORIENTATION_MORPH is not before_orientation:
        raise RuntimeError("P1-E orientation registry leaked after render")

    if rendered["semanticHash"] != fixture.semantic_hash:
        raise RuntimeError("P1-E semantic hash mismatch")

    corrections = tuple(rendered.get("corrections", ()))
    if fixture.case_id == H4:
        if corrections != (CORRECTION_H4,):
            raise RuntimeError(f"P1-E H4 correction mismatch: {corrections}")
    elif corrections:
        raise RuntimeError(
            f"P1-E forbids non-H4 correction family: case={fixture.case_id} corrections={corrections}"
        )

    return {
        **rendered,
        "eV0AdapterVersion": ADAPTER_VERSION,
        "structuralDirection": STRUCTURAL_DIRECTION,
        "readabilityAidMode": READABILITY_AID_MODE,
        "corrections": corrections,
    }
