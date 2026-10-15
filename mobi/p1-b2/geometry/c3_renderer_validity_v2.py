from __future__ import annotations

from math import cos, sin

from model import Vec2
from c3_renderers import partition_bounds, render_fixture as render_fixture_v1, union_bounds
from c3_semantic import morphology_by_id

VALIDITY_ADAPTER_VERSION = "P1_C3_RENDERER_VALIDITY_V2"


def _continuous_tail_shape(fixture, original):
    state = fixture.state
    morphology = morphology_by_id(fixture.morphology_id)
    yaw = fixture.payload["orientation"]["yawRad"]
    scale = state.size_dp / 2.0
    root = state.anchors["TAIL_ROOT"]
    tail_len = .78 * scale * morphology.tail_length

    # Continuous profile-to-front-to-profile projection.
    # The v1 renderer used the sign of cos(yaw), which caused the tail to
    # discontinuously mirror at the front-view crossing. This adapter changes
    # only visual projection; canonical semantic state is untouched.
    backward = -cos(yaw)
    lateral = sin(yaw)

    points = [
        root,
        Vec2(root.x + tail_len * (.22 * backward + .06 * lateral), root.y + .04 * scale),
        Vec2(root.x + tail_len * (.48 * backward + .16 * lateral), root.y - .02 * scale),
        Vec2(root.x + tail_len * (.68 * backward + .28 * lateral), root.y - .18 * scale),
        Vec2(root.x + tail_len * (.72 * backward + .38 * lateral), root.y - .38 * scale),
    ]
    return {
        **original,
        "points": points,
    }


def render_fixture(fixture, variant):
    rendered = render_fixture_v1(fixture, variant)
    shapes = []
    replaced = 0
    for shape in rendered["shapes"]:
        if shape.get("role") == "tail":
            shapes.append(_continuous_tail_shape(fixture, shape))
            replaced += 1
        else:
            shapes.append(shape)
    if replaced != 1:
        raise RuntimeError(f"expected exactly one tail shape, got {replaced}")

    return {
        **rendered,
        "shapes": shapes,
        "visualBounds": union_bounds(shapes),
        "partitionBounds": partition_bounds(shapes, fixture.state.size_dp),
        "validityAdapterVersion": VALIDITY_ADAPTER_VERSION,
    }
