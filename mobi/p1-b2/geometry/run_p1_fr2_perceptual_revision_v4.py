from __future__ import annotations

import p1_fr2_layered_view_prototype_v4 as v4
import run_p1_fr2_perceptual_revision as base_runner


RUN_VERSION = "P1_FR2_PERCEPTUAL_REVISION_EVIDENCE_V4_VISUAL_REFINEMENT_NORMALIZED"
_original_mesh_group_svg = base_runner._mesh_group_svg


def _normalized_mesh_group_svg(fixture, probe, x_offset: float, y_offset: float, revision: bool):
    """Use the same BODY_ROOT-centered evidence frame for baseline and V4."""
    body_root = fixture.state.anchors["BODY_ROOT"]
    return _original_mesh_group_svg(
        fixture,
        probe,
        x_offset - body_root.x,
        y_offset - body_root.y,
        revision,
    )


base_runner.RUN_VERSION = RUN_VERSION
base_runner.PROTOTYPE_VERSION = v4.PROTOTYPE_VERSION
base_runner.build_probe = v4.build_probe
base_runner.limb_crossing_count = v4.limb_crossing_count
base_runner.result_dict = v4.result_dict
base_runner._mesh_group_svg = _normalized_mesh_group_svg


if __name__ == "__main__":
    base_runner.main()
