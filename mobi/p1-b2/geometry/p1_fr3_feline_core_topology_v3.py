from __future__ import annotations

import p1_fr3_feline_core_topology_v2 as v2


PROTOTYPE_VERSION = "P1_FR3_FELINE_CORE_TOPOLOGY_V3_BOUNDED_FELINE_REFINEMENT"

# V2 established that the exact 24-point correspondence, subdivided from FR2 V5,
# is structurally safe. V3 is the first perceptual-authoring use of the added
# degrees of freedom. The refinement is deliberately narrow:
# - muzzle length/return,
# - crown continuity,
# - dorsal neck inset,
# - ventral neck/chest turn,
# - exact-front neck separation.
# Trunk/haunch points C09..C15 remain byte-identical to V2. Skin weights,
# semantic anchors, limbs, tail, ears, morphology semantics and correction
# inventory also remain unchanged.


def _refined(base_shape, edits):
    shape = list(base_shape)
    for index, point in edits.items():
        shape[index] = point
    return tuple(shape)


PROFILE_SHAPE = _refined(v2.CANONICAL_SHAPES["PROFILE"], {
    0: (1.04, -0.16),   # C00 nose top: bounded muzzle shortening
    1: (0.99, -0.29),   # C01 bridge: use added control for gentler bridge
    2: (0.95, -0.40),   # C02 forehead: tiny neighboring adjustment
    4: (0.79, -0.64),   # C04 crown rear: smooth crown continuity
    6: (0.60, -0.48),   # C06 dorsal-neck transition
    8: (0.34, -0.48),   # C08 shoulder transition
    16: (0.20, 0.36),   # C16 front-belly/sternum lead-in
    18: (0.43, 0.29),   # C18 chest-to-neck transition
    20: (0.70, 0.08),   # C20 throat/jaw lead-in
    22: (0.99, 0.01),   # C22 muzzle-bottom return
    23: (1.08, -0.03),  # C23 nose bottom: bounded muzzle shortening
})

THREE_QUARTER_SHAPE = _refined(v2.CANONICAL_SHAPES["THREE_QUARTER"], {
    0: (0.70, -0.18),
    1: (0.67, -0.30),
    2: (0.62, -0.41),
    4: (0.34, -0.64),
    6: (0.11, -0.43),
    8: (-0.12, -0.38),
    16: (0.14, 0.31),
    18: (0.35, 0.18),
    20: (0.49, 0.00),
    22: (0.65, -0.04),
    23: (0.71, -0.08),
})

FRONT_SHAPE = _refined(v2.CANONICAL_SHAPES["FRONT"], {
    0: (0.27, -0.22),
    1: (0.35, -0.34),
    4: (0.24, -0.65),
    6: (-0.12, -0.50),
    7: (-0.24, -0.42),  # small neighboring move; opens left neck inset
    8: (-0.39, -0.34),
    16: (0.38, 0.48),
    18: (0.54, 0.31),
    20: (0.43, 0.04),   # added control: right ventral-neck inset
    21: (0.38, -0.07),  # small neighboring move; keeps inset continuous
    22: (0.34, -0.15),
    23: (0.28, -0.21),
})

CANONICAL_SHAPES = {
    "PROFILE": PROFILE_SHAPE,
    "THREE_QUARTER": THREE_QUARTER_SHAPE,
    "FRONT": FRONT_SHAPE,
}

# Patch only authored view shapes on top of the proven V2 topology/weights.
v2.v1.PROTOTYPE_VERSION = PROTOTYPE_VERSION
v2.v1.PROFILE_SHAPE = PROFILE_SHAPE
v2.v1.THREE_QUARTER_SHAPE = THREE_QUARTER_SHAPE
v2.v1.FRONT_SHAPE = FRONT_SHAPE
v2.v1.CANONICAL_SHAPES = CANONICAL_SHAPES

CORE_VERTEX_IDS = v2.CORE_VERTEX_IDS
CORE_BOUNDARY_EDGES = v2.CORE_BOUNDARY_EDGES
CORE_SKIN_WEIGHTS = v2.CORE_SKIN_WEIGHTS
CANONICAL_ANCHOR_REFS = v2.CANONICAL_ANCHOR_REFS
canonical_view_weights = v2.canonical_view_weights
_shape_blend = v2.v1._shape_blend
build_core_vertices = v2.build_core_vertices
topology_signature = v2.topology_signature
build_probe = v2.build_probe
result_dict = v2.result_dict
build_ear_shapes = v2.build_ear_shapes
build_limb_meshes = v2.build_limb_meshes
build_tail_mesh = v2.build_tail_mesh
limb_crossing_count = v2.limb_crossing_count
FR2ProbeResult = v2.FR2ProbeResult
