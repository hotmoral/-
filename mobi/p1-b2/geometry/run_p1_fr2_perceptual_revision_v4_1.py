from __future__ import annotations

import p1_fr2_layered_view_prototype_v4_1 as v4_1
import run_p1_fr2_perceptual_revision as base_runner


RUN_VERSION = "P1_FR2_PERCEPTUAL_REVISION_EVIDENCE_V4_1_FRONT_SAFE_NORMALIZED"
_original_mesh_group_svg = base_runner._mesh_group_svg


def _normalized_mesh_group_svg(fixture, probe, x_offset: float, y_offset: float, revision: bool):
    body_root = fixture.state.anchors["BODY_ROOT"]
    return _original_mesh_group_svg(
        fixture,
        probe,
        x_offset - body_root.x,
        y_offset - body_root.y,
        revision,
    )


base_runner.RUN_VERSION = RUN_VERSION
base_runner.PROTOTYPE_VERSION = v4_1.PROTOTYPE_VERSION
base_runner.build_probe = v4_1.build_probe
base_runner.limb_crossing_count = v4_1.limb_crossing_count
base_runner.result_dict = v4_1.result_dict
base_runner._mesh_group_svg = _normalized_mesh_group_svg


if __name__ == "__main__":
    base_runner.main()
