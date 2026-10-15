from __future__ import annotations

from typing import Dict

import p1_fr1_mesh_probe as fr1
import p1_fr1_mesh_probe_v2 as fr1_v2
import p1_fr2_layered_view_prototype_v5 as fr2_v5
import p1_fr3_feline_core_topology as v1


PROTOTYPE_VERSION = "P1_FR3_FELINE_CORE_TOPOLOGY_V2_SUBDIVISION_SAFE"

# V1 proved the 24-point budget itself is executable, but its newly invented
# base coordinates/skin weights folded. V2 establishes a topology-safe baseline
# by subdividing the already-proven FR2 V5 16-point contour. Every added point
# lies on an existing FR2 edge and its skin weights are the exact linear blend
# of that edge's endpoints. Therefore the denser contour has no new geometric
# freedom yet; it is the control baseline from which bounded feline refinements
# can be made without guessing at correspondence stability.
#
# Entries are (old_vertex_a, old_vertex_b, t), where t=0 preserves an original
# vertex and t=0.5 inserts one midpoint. The eight inserted points are confined
# to head/dorsal-neck and ventral chest/head-return edges.
SUBDIVISION = (
    (0, 1, 0.0),
    (0, 1, 0.5),
    (1, 2, 0.0),
    (2, 3, 0.0),
    (2, 3, 0.5),
    (3, 4, 0.0),
    (3, 4, 0.5),
    (4, 5, 0.0),
    (4, 5, 0.5),
    (5, 6, 0.0),
    (6, 7, 0.0),
    (7, 8, 0.0),
    (8, 9, 0.0),
    (9, 10, 0.0),
    (10, 11, 0.0),
    (11, 12, 0.0),
    (11, 12, 0.5),
    (12, 13, 0.0),
    (12, 13, 0.5),
    (13, 14, 0.0),
    (13, 14, 0.5),
    (14, 15, 0.0),
    (14, 15, 0.5),
    (15, 0, 0.0),
)


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _subdivide_shape(shape):
    return tuple(
        (_lerp(shape[a][0], shape[b][0], t), _lerp(shape[a][1], shape[b][1], t))
        for a, b, t in SUBDIVISION
    )


def _blend_skin(a: Dict[str, float], b: Dict[str, float], t: float) -> Dict[str, float]:
    names = set(a) | set(b)
    blended = {
        name: _lerp(a.get(name, 0.0), b.get(name, 0.0), t)
        for name in names
    }
    return {name: weight for name, weight in blended.items() if abs(weight) > 1e-15}


CANONICAL_SHAPES = {
    name: _subdivide_shape(fr2_v5.CANONICAL_SHAPES[name])
    for name in ("PROFILE", "THREE_QUARTER", "FRONT")
}

OLD_SKIN = fr1_v2.CORE_SKIN_WEIGHTS
OLD_IDS = fr1.CORE_VERTEX_IDS
CORE_SKIN_WEIGHTS = {
    new_id: _blend_skin(OLD_SKIN[OLD_IDS[a]], OLD_SKIN[OLD_IDS[b]], t)
    for new_id, (a, b, t) in zip(v1.CORE_VERTEX_IDS, SUBDIVISION)
}

# Patch only V1's authored 24-point shape/weight tables. All semantic,
# appendage, view interpolation and topology-signature logic stays identical.
v1.PROTOTYPE_VERSION = PROTOTYPE_VERSION
v1.PROFILE_SHAPE = CANONICAL_SHAPES["PROFILE"]
v1.THREE_QUARTER_SHAPE = CANONICAL_SHAPES["THREE_QUARTER"]
v1.FRONT_SHAPE = CANONICAL_SHAPES["FRONT"]
v1.CANONICAL_SHAPES = CANONICAL_SHAPES
v1.CORE_SKIN_WEIGHTS = CORE_SKIN_WEIGHTS

CORE_VERTEX_IDS = v1.CORE_VERTEX_IDS
CORE_BOUNDARY_EDGES = v1.CORE_BOUNDARY_EDGES
CANONICAL_ANCHOR_REFS = v1.CANONICAL_ANCHOR_REFS
canonical_view_weights = v1.canonical_view_weights
_shape_blend = v1._shape_blend
build_core_vertices = v1.build_core_vertices
topology_signature = v1.topology_signature
build_probe = v1.build_probe
result_dict = v1.result_dict
build_ear_shapes = v1.build_ear_shapes
build_limb_meshes = v1.build_limb_meshes
build_tail_mesh = v1.build_tail_mesh
limb_crossing_count = v1.limb_crossing_count
FR2ProbeResult = v1.FR2ProbeResult
