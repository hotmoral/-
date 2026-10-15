from __future__ import annotations

import p1_fr2_layered_view_prototype_v2 as v2


PROTOTYPE_VERSION = "P1_FR2_LAYERED_VIEW_PERCEPTUAL_REVISION_V3_DORSAL_SAFE"

# The exact V2 diagnostic localized every repeated PROFILE fold to the same
# non-adjacent edge pair:
#   V03_CROWN -> V04_NECK_DORSAL
#   V05_SHOULDER_DORSAL -> V06_BACK_DORSAL
# V3 therefore changes only those four authored PROFILE points, restoring their
# already-proven FR1 safe envelope. All other FR2 head, haunch, ventral, limb,
# tail and ear revisions are retained. This remains a base-shape refinement;
# topology, semantics and correction inventory do not change.
PROFILE_SHAPE = list(v2.PROFILE_SHAPE)
PROFILE_SHAPE[3] = (0.76, -0.58)   # V03_CROWN
PROFILE_SHAPE[4] = (0.49, -0.40)   # V04_NECK_DORSAL
PROFILE_SHAPE[5] = (0.20, -0.54)   # V05_SHOULDER_DORSAL
PROFILE_SHAPE[6] = (-0.30, -0.50)  # V06_BACK_DORSAL
PROFILE_SHAPE = tuple(PROFILE_SHAPE)

# V2 ultimately delegates its build functions to the V1 implementation module.
# Update that module's authored view-shape globals before any probe executes.
v2.v1.PROTOTYPE_VERSION = PROTOTYPE_VERSION
v2.v1.PROFILE_SHAPE = PROFILE_SHAPE
v2.v1.CANONICAL_SHAPES = dict(v2.v1.CANONICAL_SHAPES)
v2.v1.CANONICAL_SHAPES["PROFILE"] = PROFILE_SHAPE

CORE_VERTEX_IDS = v2.CORE_VERTEX_IDS
CANONICAL_SHAPES = v2.v1.CANONICAL_SHAPES
FR2ProbeResult = v2.FR2ProbeResult
canonical_view_weights = v2.canonical_view_weights
build_core_vertices = v2.build_core_vertices
build_ear_shapes = v2.build_ear_shapes
build_limb_meshes = v2.build_limb_meshes
build_tail_mesh = v2.build_tail_mesh
topology_signature = v2.topology_signature
limb_crossing_count = v2.limb_crossing_count
build_probe = v2.build_probe
result_dict = v2.result_dict
