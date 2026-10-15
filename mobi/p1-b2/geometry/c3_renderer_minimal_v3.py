from __future__ import annotations

from c3_renderer_validity_v2 import render_fixture as render_fixture_v2

MINIMAL_CORRECTION_VERSION = "P1_C3_MINIMAL_CORRECTION_V3"


def render_fixture(fixture, variant):
    """Final C3 discriminator renderer with only evidence-justified RF-C correction.

    RF-C is the same bounded articulated base as RF-B plus authored correction only
    where the C3 evidence shows a material structural benefit. The earlier H6
    front-volume experiment did not materially improve transition/bounds continuity,
    so H6 intentionally falls back to the shared RF-B structural renderer while
    retaining the accepted continuous-tail validity adapter.

    Canonical semantic state is never altered.
    """
    if variant not in ("RF_B", "RF_C"):
        raise ValueError(variant)

    if variant == "RF_C" and fixture.case_id == "H6_CHANGE_FACING_2P5D":
        rendered = render_fixture_v2(fixture, "RF_B")
        return {
            **rendered,
            "variant": "RF_C",
            "corrections": tuple(),
            "minimalCorrectionVersion": MINIMAL_CORRECTION_VERSION,
        }

    rendered = render_fixture_v2(fixture, variant)
    return {
        **rendered,
        "minimalCorrectionVersion": MINIMAL_CORRECTION_VERSION,
    }
