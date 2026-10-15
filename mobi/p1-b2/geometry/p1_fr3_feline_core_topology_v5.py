from __future__ import annotations

import p1_fr3_feline_core_topology_v2 as v2
import p1_fr3_feline_core_topology_v4 as v4


PROTOTYPE_VERSION = "P1_FR3_FELINE_CORE_TOPOLOGY_V5_FULL_MATRIX_SAFE"

# Full 1,770-record V4 diagnostics found exactly nine folds, all H5 crouch,
# all the same local PROFILE pair:
#   C19_NECK_VENTRAL_BASE -> C20_THROAT
#   C21_JAW_REAR          -> C22_MUZZLE_BOTTOM
# V5 reverts only the two authored insertion points C20/C22 to their exact V2
# subdivision-safe locations. No other V4 change is altered.
PROFILE_SHAPE = list(v4.PROFILE_SHAPE)
PROFILE_SHAPE[20] = v2.CANONICAL_SHAPES["PROFILE"][20]
PROFILE_SHAPE[22] = v2.CANONICAL_SHAPES["PROFILE"][22]
PROFILE_SHAPE = tuple(PROFILE_SHAPE)

THREE_QUARTER_SHAPE = v4.THREE_QUARTER_SHAPE
FRONT_SHAPE = v4.FRONT_SHAPE
CANONICAL_SHAPES = {
    "PROFILE": PROFILE_SHAPE,
    "THREE_QUARTER": THREE_QUARTER_SHAPE,
    "FRONT": FRONT_SHAPE,
}

v4.v3.v2.v1.PROTOTYPE_VERSION = PROTOTYPE_VERSION
v4.v3.v2.v1.PROFILE_SHAPE = PROFILE_SHAPE
v4.v3.v2.v1.THREE_QUARTER_SHAPE = THREE_QUARTER_SHAPE
v4.v3.v2.v1.FRONT_SHAPE = FRONT_SHAPE
v4.v3.v2.v1.CANONICAL_SHAPES = CANONICAL_SHAPES

CORE_VERTEX_IDS = v4.CORE_VERTEX_IDS
CORE_BOUNDARY_EDGES = v4.CORE_BOUNDARY_EDGES
CORE_SKIN_WEIGHTS = v4.CORE_SKIN_WEIGHTS
CANONICAL_ANCHOR_REFS = v4.CANONICAL_ANCHOR_REFS
canonical_view_weights = v4.canonical_view_weights
_shape_blend = v4.v3.v2.v1._shape_blend
build_core_vertices = v4.build_core_vertices
topology_signature = v4.topology_signature
build_probe = v4.build_probe
result_dict = v4.result_dict
build_ear_shapes = v4.build_ear_shapes
build_limb_meshes = v4.build_limb_meshes
build_tail_mesh = v4.build_tail_mesh
limb_crossing_count = v4.limb_crossing_count
FR2ProbeResult = v4.FR2ProbeResult
