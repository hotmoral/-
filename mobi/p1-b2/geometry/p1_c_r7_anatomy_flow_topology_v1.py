from __future__ import annotations

import hashlib
import json


TOPOLOGY_VERSION = "P1_C_R7_ANATOMY_FLOW_TOPOLOGY_V1"
SOURCE_FAMILY = "RF_I_BOUNDED_ANATOMY_FLOW_CONTROL_SURFACE"
SOURCE_PACK_ID = "R6_CONSTRUCTION_PACK_V1"
EXTERNAL_DOMAINS = ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL")
DERIVED_SUBDIVISION_STEPS = 0

DORSAL = (
    "D_MUZZLE", "D_CRANIUM", "D_CRANIAL_BASE", "D_CERVICAL",
    "D_SHOULDER", "D_THORAX", "D_LUMBAR", "D_PELVIS", "D_RUMP",
)
LEFT_DORSOLATERAL = (
    "LU_MUZZLE", "LU_CHEEK", "LU_CRANIAL_BASE", "LU_CERVICAL",
    "LU_SHOULDER", "LU_THORAX", "LU_FLANK", "LU_PELVIS", "LU_HAUNCH",
)
LEFT_VENTROLATERAL = (
    "LL_MUZZLE", "LL_CHEEK", "LL_CRANIAL_BASE", "LL_CERVICAL",
    "LL_CHEST", "LL_THORAX", "LL_ABDOMEN", "LL_TUCK", "LL_PELVIS", "LL_HAUNCH",
)
VENTRAL = (
    "V_MUZZLE", "V_JAW", "V_THROAT", "V_STERNUM",
    "V_ABDOMEN", "V_TUCK", "V_PELVIS", "V_RUMP",
)
RIGHT_DORSOLATERAL = tuple(value.replace("LU_", "RU_") for value in LEFT_DORSOLATERAL)
RIGHT_VENTROLATERAL = tuple(value.replace("LL_", "RL_") for value in LEFT_VENTROLATERAL)
PROXIMAL = (
    "FORE_L_PROX_CRANIAL", "FORE_L_PROX_CAUDAL",
    "FORE_R_PROX_CRANIAL", "FORE_R_PROX_CAUDAL",
    "HIND_L_PROX_CRANIAL", "HIND_L_PROX_CAUDAL",
    "HIND_R_PROX_CRANIAL", "HIND_R_PROX_CAUDAL",
)

VERTEX_IDS = DORSAL + LEFT_DORSOLATERAL + LEFT_VENTROLATERAL + VENTRAL + RIGHT_DORSOLATERAL + RIGHT_VENTROLATERAL + PROXIMAL

FACES = (
    ("CORE", ("D_MUZZLE", "D_CRANIUM", "LU_CHEEK", "LU_MUZZLE")),
    ("CORE", ("D_CRANIUM", "D_CRANIAL_BASE", "LU_CRANIAL_BASE", "LU_CHEEK")),
    ("CORE", ("D_CRANIAL_BASE", "D_CERVICAL", "LU_CERVICAL", "LU_CRANIAL_BASE")),
    ("CORE", ("D_CERVICAL", "D_SHOULDER", "LU_SHOULDER", "LU_CERVICAL")),
    ("CORE", ("D_SHOULDER", "D_THORAX", "LU_THORAX", "LU_SHOULDER")),
    ("CORE", ("D_THORAX", "D_LUMBAR", "LU_FLANK", "LU_THORAX")),
    ("CORE", ("D_LUMBAR", "D_PELVIS", "LU_PELVIS", "LU_FLANK")),
    ("CORE", ("D_PELVIS", "D_RUMP", "LU_HAUNCH", "LU_PELVIS")),
    ("CORE", ("D_MUZZLE", "D_CRANIUM", "RU_CHEEK", "RU_MUZZLE")),
    ("CORE", ("D_CRANIUM", "D_CRANIAL_BASE", "RU_CRANIAL_BASE", "RU_CHEEK")),
    ("CORE", ("D_CRANIAL_BASE", "D_CERVICAL", "RU_CERVICAL", "RU_CRANIAL_BASE")),
    ("CORE", ("D_CERVICAL", "D_SHOULDER", "RU_SHOULDER", "RU_CERVICAL")),
    ("CORE", ("D_SHOULDER", "D_THORAX", "RU_THORAX", "RU_SHOULDER")),
    ("CORE", ("D_THORAX", "D_LUMBAR", "RU_FLANK", "RU_THORAX")),
    ("CORE", ("D_LUMBAR", "D_PELVIS", "RU_PELVIS", "RU_FLANK")),
    ("CORE", ("D_PELVIS", "D_RUMP", "RU_HAUNCH", "RU_PELVIS")),
    ("CORE", ("LU_MUZZLE", "LU_CHEEK", "LL_CHEEK", "LL_MUZZLE")),
    ("CORE", ("LU_CHEEK", "LU_CRANIAL_BASE", "LL_CRANIAL_BASE", "LL_CHEEK")),
    ("CORE", ("LU_CRANIAL_BASE", "LU_CERVICAL", "LL_CERVICAL", "LL_CRANIAL_BASE")),
    ("CORE", ("LU_CERVICAL", "LU_SHOULDER", "LL_CHEST", "LL_CERVICAL")),
    ("CORE", ("LU_THORAX", "LU_FLANK", "LL_ABDOMEN", "LL_THORAX")),
    ("CORE", ("LU_FLANK", "LU_PELVIS", "LL_TUCK", "LL_ABDOMEN")),
    ("CORE", ("LU_PELVIS", "LL_PELVIS", "LL_TUCK")),
    ("CORE", ("RU_MUZZLE", "RU_CHEEK", "RL_CHEEK", "RL_MUZZLE")),
    ("CORE", ("RU_CHEEK", "RU_CRANIAL_BASE", "RL_CRANIAL_BASE", "RL_CHEEK")),
    ("CORE", ("RU_CRANIAL_BASE", "RU_CERVICAL", "RL_CERVICAL", "RL_CRANIAL_BASE")),
    ("CORE", ("RU_CERVICAL", "RU_SHOULDER", "RL_CHEST", "RL_CERVICAL")),
    ("CORE", ("RU_THORAX", "RU_FLANK", "RL_ABDOMEN", "RL_THORAX")),
    ("CORE", ("RU_FLANK", "RU_PELVIS", "RL_TUCK", "RL_ABDOMEN")),
    ("CORE", ("RU_PELVIS", "RL_PELVIS", "RL_TUCK")),
    ("CORE", ("LL_MUZZLE", "LL_CHEEK", "V_JAW", "V_MUZZLE")),
    ("CORE", ("LL_CHEEK", "LL_CRANIAL_BASE", "V_THROAT", "V_JAW")),
    ("CORE", ("LL_CRANIAL_BASE", "LL_CERVICAL", "V_THROAT")),
    ("CORE", ("LL_CERVICAL", "LL_CHEST", "V_STERNUM", "V_THROAT")),
    ("CORE", ("LL_CHEST", "LL_THORAX", "V_ABDOMEN", "V_STERNUM")),
    ("CORE", ("LL_THORAX", "LL_ABDOMEN", "V_ABDOMEN")),
    ("CORE", ("LL_ABDOMEN", "LL_TUCK", "V_TUCK", "V_ABDOMEN")),
    ("CORE", ("LL_TUCK", "LL_PELVIS", "V_PELVIS", "V_TUCK")),
    ("CORE", ("LL_PELVIS", "LL_HAUNCH", "V_RUMP", "V_PELVIS")),
    ("CORE", ("RL_MUZZLE", "RL_CHEEK", "V_JAW", "V_MUZZLE")),
    ("CORE", ("RL_CHEEK", "RL_CRANIAL_BASE", "V_THROAT", "V_JAW")),
    ("CORE", ("RL_CRANIAL_BASE", "RL_CERVICAL", "V_THROAT")),
    ("CORE", ("RL_CERVICAL", "RL_CHEST", "V_STERNUM", "V_THROAT")),
    ("CORE", ("RL_CHEST", "RL_THORAX", "V_ABDOMEN", "V_STERNUM")),
    ("CORE", ("RL_THORAX", "RL_ABDOMEN", "V_ABDOMEN")),
    ("CORE", ("RL_ABDOMEN", "RL_TUCK", "V_TUCK", "V_ABDOMEN")),
    ("CORE", ("RL_TUCK", "RL_PELVIS", "V_PELVIS", "V_TUCK")),
    ("CORE", ("RL_PELVIS", "RL_HAUNCH", "V_RUMP", "V_PELVIS")),
    ("CORE", ("D_MUZZLE", "RU_MUZZLE", "RL_MUZZLE", "V_MUZZLE", "LL_MUZZLE", "LU_MUZZLE")),
    ("CORE", ("D_RUMP", "LU_HAUNCH", "LL_HAUNCH", "V_RUMP", "RL_HAUNCH", "RU_HAUNCH")),
    ("FORE_L", ("LU_SHOULDER", "LU_THORAX", "FORE_L_PROX_CAUDAL", "FORE_L_PROX_CRANIAL")),
    ("FORE_L", ("LU_THORAX", "LL_THORAX", "FORE_L_PROX_CAUDAL")),
    ("FORE_L", ("LL_THORAX", "LL_CHEST", "FORE_L_PROX_CRANIAL", "FORE_L_PROX_CAUDAL")),
    ("FORE_L", ("LL_CHEST", "LU_SHOULDER", "FORE_L_PROX_CRANIAL")),
    ("FORE_R", ("RU_SHOULDER", "RU_THORAX", "FORE_R_PROX_CAUDAL", "FORE_R_PROX_CRANIAL")),
    ("FORE_R", ("RU_THORAX", "RL_THORAX", "FORE_R_PROX_CAUDAL")),
    ("FORE_R", ("RL_THORAX", "RL_CHEST", "FORE_R_PROX_CRANIAL", "FORE_R_PROX_CAUDAL")),
    ("FORE_R", ("RL_CHEST", "RU_SHOULDER", "FORE_R_PROX_CRANIAL")),
    ("HIND_L", ("LU_PELVIS", "LU_HAUNCH", "HIND_L_PROX_CAUDAL", "HIND_L_PROX_CRANIAL")),
    ("HIND_L", ("LU_HAUNCH", "LL_HAUNCH", "HIND_L_PROX_CAUDAL")),
    ("HIND_L", ("LL_HAUNCH", "LL_PELVIS", "HIND_L_PROX_CRANIAL", "HIND_L_PROX_CAUDAL")),
    ("HIND_L", ("LL_PELVIS", "LU_PELVIS", "HIND_L_PROX_CRANIAL")),
    ("HIND_R", ("RU_PELVIS", "RU_HAUNCH", "HIND_R_PROX_CAUDAL", "HIND_R_PROX_CRANIAL")),
    ("HIND_R", ("RU_HAUNCH", "RL_HAUNCH", "HIND_R_PROX_CAUDAL")),
    ("HIND_R", ("RL_HAUNCH", "RL_PELVIS", "HIND_R_PROX_CRANIAL", "HIND_R_PROX_CAUDAL")),
    ("HIND_R", ("RL_PELVIS", "RU_PELVIS", "HIND_R_PROX_CRANIAL")),
)

FLOW_PATHS = {
    "DORSAL_AXIAL": DORSAL,
    "VENTRAL_THORACO_ABDOMINAL": VENTRAL,
    "LEFT_DORSOLATERAL": LEFT_DORSOLATERAL,
    "LEFT_VENTROLATERAL": LEFT_VENTROLATERAL,
    "RIGHT_DORSOLATERAL": RIGHT_DORSOLATERAL,
    "RIGHT_VENTROLATERAL": RIGHT_VENTROLATERAL,
    "FORE_L_EMERGENCE": ("LU_SHOULDER", "FORE_L_PROX_CRANIAL", "FORE_L_PROX_CAUDAL", "LU_THORAX"),
    "FORE_R_EMERGENCE": ("RU_SHOULDER", "FORE_R_PROX_CRANIAL", "FORE_R_PROX_CAUDAL", "RU_THORAX"),
    "HIND_L_EMERGENCE": ("LU_PELVIS", "HIND_L_PROX_CRANIAL", "HIND_L_PROX_CAUDAL", "LU_HAUNCH"),
    "HIND_R_EMERGENCE": ("RU_PELVIS", "HIND_R_PROX_CRANIAL", "HIND_R_PROX_CAUDAL", "RU_HAUNCH"),
}

SHARED_BOUNDARIES = {
    "FORE_L": ("LU_SHOULDER", "LU_THORAX", "LL_THORAX", "LL_CHEST"),
    "FORE_R": ("RU_SHOULDER", "RU_THORAX", "RL_THORAX", "RL_CHEST"),
    "HIND_L": ("LU_PELVIS", "LU_HAUNCH", "LL_HAUNCH", "LL_PELVIS"),
    "HIND_R": ("RU_PELVIS", "RU_HAUNCH", "RL_HAUNCH", "RL_PELVIS"),
}

FROZEN_TOPOLOGY_SHA256 = "626ea4b8b1670c641feff654a458506a64fc7fae8ffd24e3f6fb00695b5bf8a9"


def edge_set():
    edges = set()
    for _, vertices in FACES:
        for a, b in zip(vertices, vertices[1:] + vertices[:1]):
            edges.add(tuple(sorted((a, b))))
    return tuple(sorted(edges))


def topology_payload():
    return {
        "family": SOURCE_FAMILY,
        "sourcePackId": SOURCE_PACK_ID,
        "externalDomains": list(EXTERNAL_DOMAINS),
        "vertices": list(VERTEX_IDS),
        "faces": [{"domain": domain, "vertices": list(vertices)} for domain, vertices in FACES],
        "flowPaths": {key: list(value) for key, value in FLOW_PATHS.items()},
        "sharedBoundaries": {key: list(value) for key, value in SHARED_BOUNDARIES.items()},
        "derivedSubdivisionSteps": DERIVED_SUBDIVISION_STEPS,
    }


def topology_signature():
    canonical = json.dumps(topology_payload(), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def validate_topology():
    if len(VERTEX_IDS) != len(set(VERTEX_IDS)):
        raise ValueError("duplicate vertex ID")
    if len(VERTEX_IDS) > 96:
        raise ValueError("vertex ceiling exceeded")
    if len(FACES) > 128:
        raise ValueError("face ceiling exceeded")
    if DERIVED_SUBDIVISION_STEPS != 0:
        raise ValueError("Stage 1 frozen subdivision drift")
    vertex_set = set(VERTEX_IDS)
    allowed_domains = set(EXTERNAL_DOMAINS)
    for domain, face in FACES:
        if domain not in allowed_domains:
            raise ValueError(("unknown face domain", domain))
        if len(face) < 3:
            raise ValueError(("degenerate face", face))
        if any(vertex not in vertex_set for vertex in face):
            raise ValueError(("unknown face vertex", face))
    edges = set(edge_set())
    for path_id, path in FLOW_PATHS.items():
        for a, b in zip(path, path[1:]):
            if tuple(sorted((a, b))) not in edges:
                raise ValueError(("flow path is not edge-connected", path_id, a, b))
    for domain, boundary in SHARED_BOUNDARIES.items():
        for a, b in zip(boundary, boundary[1:] + boundary[:1]):
            if tuple(sorted((a, b))) not in edges:
                raise ValueError(("shared boundary edge absent", domain, a, b))
    if topology_signature() != FROZEN_TOPOLOGY_SHA256:
        raise ValueError("frozen topology signature drift")
    return True


validate_topology()
