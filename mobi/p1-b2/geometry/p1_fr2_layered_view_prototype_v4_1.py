from __future__ import annotations

import p1_fr2_layered_view_prototype_v4 as v4


PROTOTYPE_VERSION = "P1_FR2_LAYERED_VIEW_PERCEPTUAL_REVISION_V4_1_FRONT_SAFE"

# V4 direct regression evidence localized its only representative structural
# failure to the authored exact-FRONT contour: the aggressive right chest ->
# throat inset folded across the head-return chain. V4.1 changes FRONT only.
# It keeps the V4 muzzle, tail and geometry-aware limb routing unchanged while
# restoring a simple ordered contour with a smaller neck inset / chest spread.
FRONT_SHAPE = (
    (0.24, -0.25),
    (0.34, -0.47),
    (0.38, -0.68),
    (0.00, -0.57),
    (-0.22, -0.38),
    (-0.44, -0.22),
    (-0.49, 0.00),
    (-0.46, 0.20),
    (-0.36, 0.40),
    (-0.19, 0.49),
    (0.00, 0.45),
    (0.24, 0.46),
    (0.42, 0.32),
    (0.43, 0.10),
    (0.32, -0.09),
    (0.23, -0.24),
)

v4.base.PROTOTYPE_VERSION = PROTOTYPE_VERSION
v4.base.FRONT_SHAPE = FRONT_SHAPE
v4.base.CANONICAL_SHAPES = dict(v4.base.CANONICAL_SHAPES)
v4.base.CANONICAL_SHAPES["FRONT"] = FRONT_SHAPE

CORE_VERTEX_IDS = v4.CORE_VERTEX_IDS
CANONICAL_SHAPES = v4.base.CANONICAL_SHAPES
FR2ProbeResult = v4.FR2ProbeResult
canonical_view_weights = v4.canonical_view_weights
build_core_vertices = v4.build_core_vertices
build_ear_shapes = v4.build_ear_shapes
build_limb_meshes = v4.build_limb_meshes
build_tail_mesh = v4.build_tail_mesh
topology_signature = v4.topology_signature
limb_crossing_count = v4.limb_crossing_count
build_probe = v4.build_probe
result_dict = v4.result_dict
