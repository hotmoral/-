from __future__ import annotations

import p1_fr3_feline_core_topology_v2 as v2
import p1_fr3_feline_core_topology_v3 as v3


PROTOTYPE_VERSION = "P1_FR3_FELINE_CORE_TOPOLOGY_V4_PROFILE_DORSAL_SAFE"

# Exact V3 diagnostics localized both retained failures to the same PROFILE
# non-adjacent edge pair:
#   C05_NECK_DORSAL_HEAD -> C06_NECK_DORSAL_BASE
#   C07_SHOULDER_FRONT   -> C08_SHOULDER_DORSAL
# The two failing M2 fixtures produced identical crossing coordinates. V4
# therefore reverts only the two authored PROFILE insertion points C06/C08 to
# their V2 subdivision-safe positions. Every other V3 feline refinement remains.
PROFILE_SHAPE = list(v3.PROFILE_SHAPE)
PROFILE_SHAPE[6] = v2.CANONICAL_SHAPES["PROFILE"][6]
PROFILE_SHAPE[8] = v2.CANONICAL_SHAPES["PROFILE"][8]
PROFILE_SHAPE = tuple(PROFILE_SHAPE)

THREE_QUARTER_SHAPE = v3.THREE_QUARTER_SHAPE
FRONT_SHAPE = v3.FRONT_SHAPE
CANONICAL_SHAPES = {
    "PROFILE": PROFILE_SHAPE,
    "THREE_QUARTER": THREE_QUARTER_SHAPE,
    "FRONT": FRONT_SHAPE,
}

v3.v2.v1.PROTOTYPE_VERSION = PROTOTYPE_VERSION
v3.v2.v1.PROFILE_SHAPE = PROFILE_SHAPE
v3.v2.v1.THREE_QUARTER_SHAPE = THREE_QUARTER_SHAPE
v3.v2.v1.FRONT_SHAPE = FRONT_SHAPE
v3.v2.v1.CANONICAL_SHAPES = CANONICAL_SHAPES

CORE_VERTEX_IDS = v3.CORE_VERTEX_IDS
CORE_BOUNDARY_EDGES = v3.CORE_BOUNDARY_EDGES
CORE_SKIN_WEIGHTS = v3.CORE_SKIN_WEIGHTS
CANONICAL_ANCHOR_REFS = v3.CANONICAL_ANCHOR_REFS
canonical_view_weights = v3.canonical_view_weights
_shape_blend = v3.v2.v1._shape_blend
build_core_vertices = v3.build_core_vertices
topology_signature = v3.topology_signature
build_probe = v3.build_probe
result_dict = v3.result_dict
build_ear_shapes = v3.build_ear_shapes
build_limb_meshes = v3.build_limb_meshes
build_tail_mesh = v3.build_tail_mesh
limb_crossing_count = v3.limb_crossing_count
FR2ProbeResult = v3.FR2ProbeResult
