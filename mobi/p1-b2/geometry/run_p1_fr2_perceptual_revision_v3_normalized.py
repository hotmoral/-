from __future__ import annotations

import run_p1_fr2_perceptual_revision_v3 as v3_runner


RUN_VERSION = "P1_FR2_PERCEPTUAL_REVISION_EVIDENCE_V3_NORMALIZED"
base = v3_runner.v1_runner
_original_mesh_group_svg = base._mesh_group_svg


def _normalized_mesh_group_svg(fixture, probe, x_offset: float, y_offset: float, revision: bool):
    """Place BODY_ROOT at the requested evidence-cell center.

    The first V3 structural evidence run exposed an evidence-only framing defect:
    raw fixture coordinates were added to the cell translation, so the FR2 row
    could be clipped. Normalizing both baseline and revision by the same
    authoritative BODY_ROOT removes that presentation bias without changing any
    prototype geometry, semantic state, scale, or relative motion.
    """
    body_root = fixture.state.anchors["BODY_ROOT"]
    return _original_mesh_group_svg(
        fixture,
        probe,
        x_offset - body_root.x,
        y_offset - body_root.y,
        revision,
    )


base.RUN_VERSION = RUN_VERSION
base._mesh_group_svg = _normalized_mesh_group_svg


if __name__ == "__main__":
    base.main()
