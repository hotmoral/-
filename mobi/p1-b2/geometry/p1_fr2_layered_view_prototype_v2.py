from __future__ import annotations

import p1_fr2_layered_view_prototype as v1


PROTOTYPE_VERSION = "P1_FR2_LAYERED_VIEW_PERCEPTUAL_REVISION_V2_PROFILE_SAFE"

# V1 pulled the lower front/head-return contour too far inward. That produced
# one repeated PROFILE self-intersection across four morphology probes while
# 3Q/front remained sound. V2 preserves the new feline dorsal/haunch shaping
# but restores the belly-front -> chest -> throat -> muzzle -> nose return to
# the already-proven FR1 safe envelope. This is a base-shape refinement, not a
# corrective and not a topology change.
PROFILE_SHAPE = (
    (1.18, -0.16),
    (1.04, -0.43),
    (0.86, -0.68),
    (0.66, -0.50),
    (0.46, -0.32),
    (0.20, -0.43),
    (-0.26, -0.47),
    (-0.70, -0.55),
    (-0.98, -0.26),
    (-0.88, 0.30),
    (-0.52, 0.28),
    (0.06, 0.32),
    (0.35, 0.42),
    (0.56, 0.12),
    (1.04, 0.10),
    (1.38, 0.00),
)

# Apply the refinement before any of the V1 functions execute. Their global
# lookups then use this V2 authored base while all semantic/deformation logic
# remains byte-identical to V1.
v1.PROTOTYPE_VERSION = PROTOTYPE_VERSION
v1.PROFILE_SHAPE = PROFILE_SHAPE
v1.CANONICAL_SHAPES = dict(v1.CANONICAL_SHAPES)
v1.CANONICAL_SHAPES["PROFILE"] = PROFILE_SHAPE

CORE_VERTEX_IDS = v1.CORE_VERTEX_IDS
CANONICAL_SHAPES = v1.CANONICAL_SHAPES
FR2ProbeResult = v1.FR2ProbeResult
canonical_view_weights = v1.canonical_view_weights
build_core_vertices = v1.build_core_vertices
build_ear_shapes = v1.build_ear_shapes
build_limb_meshes = v1.build_limb_meshes
build_tail_mesh = v1.build_tail_mesh
topology_signature = v1.topology_signature
limb_crossing_count = v1.limb_crossing_count
build_probe = v1.build_probe
result_dict = v1.result_dict
