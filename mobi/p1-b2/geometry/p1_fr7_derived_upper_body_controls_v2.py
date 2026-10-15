from __future__ import annotations

import p1_fr7_derived_upper_body_controls_v1 as v1


PROTOTYPE_VERSION = "P1_FR7_DERIVED_UPPER_BODY_CONTROLS_V2_FINAL_COEFFICIENTS"
CONTROL_IDS = v1.CONTROL_IDS
LAYER_IDS = v1.LAYER_IDS
MAX_NORMALIZED_CORE_DISPLACEMENT = v1.MAX_NORMALIZED_CORE_DISPLACEMENT
INFLUENCE_WEIGHTS = v1.INFLUENCE_WEIGHTS
CORE_VERTEX_IDS = v1.CORE_VERTEX_IDS
CORE_BOUNDARY_EDGES = v1.CORE_BOUNDARY_EDGES
CORE_SKIN_WEIGHTS = v1.CORE_SKIN_WEIGHTS
CANONICAL_SHAPES = v1.CANONICAL_SHAPES
topology_signature = v1.topology_signature
limb_crossing_count = v1.limb_crossing_count
prior_fold_corridor_margin = v1.prior_fold_corridor_margin

# Final FR7 coefficient-only candidate. Mechanism, controls, seeds/axes,
# influence topology, PROFILE bypass and all acceptance thresholds remain V1.
# Parameters are (axialScale, lateralScale, axialShiftNorm).
VIEW_FRAME_PARAMS = {
    "CRANIUM_MASS": {
        "PROFILE": (1.00, 1.00, 0.000),
        "THREE_QUARTER": (1.05, 1.14, -0.018),
        "FRONT": (1.08, 1.21, -0.030),
    },
    "CERVICAL_BRIDGE": {
        "PROFILE": (1.00, 1.00, 0.000),
        "THREE_QUARTER": (1.09, 0.94, 0.009),
        "FRONT": (1.15, 0.90, 0.018),
    },
    "THORAX_MASS": {
        "PROFILE": (1.00, 1.00, 0.000),
        "THREE_QUARTER": (1.03, 1.07, 0.003),
        "FRONT": (1.06, 1.12, 0.006),
    },
}


def _call_with_v2(function, *args, **kwargs):
    old_version = v1.PROTOTYPE_VERSION
    old_params = v1.VIEW_FRAME_PARAMS
    try:
        v1.PROTOTYPE_VERSION = PROTOTYPE_VERSION
        v1.VIEW_FRAME_PARAMS = VIEW_FRAME_PARAMS
        return function(*args, **kwargs)
    finally:
        v1.PROTOTYPE_VERSION = old_version
        v1.VIEW_FRAME_PARAMS = old_params


def build_integrated_core(fixture, control_core):
    return _call_with_v2(v1.build_integrated_core, fixture, control_core)


def integration_signature() -> str:
    return _call_with_v2(v1.integration_signature)


def build_probe(fixture, direction: int = +1):
    return _call_with_v2(v1.build_probe, fixture, direction)


def result_dict(result) -> dict:
    return _call_with_v2(v1.result_dict, result)
