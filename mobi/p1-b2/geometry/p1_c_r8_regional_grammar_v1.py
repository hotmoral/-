from __future__ import annotations

import hashlib
import json


GRAMMAR_VERSION = "P1_C_R8_REGIONAL_GRAMMAR_V1"
SOURCE_FAMILY = "RF_J_BOUNDED_REGIONAL_PROCEDURAL_DEFORMABLE_SURFACE"
SOURCE_PACK_ID = "R6_CONSTRUCTION_PACK_V1"
EXTERNAL_DOMAINS = ("CORE", "FORE_L", "FORE_R", "HIND_L", "HIND_R", "TAIL")
CORRECTION_CATALOGUE = "NONE"

REGIONS = (
    {
        "id": "CRANIUM_MUZZLE",
        "domain": "CORE",
        "basis": "ASYMMETRIC_TAPERED_SUPERELLIPSOID_FIELD_V1",
        "frame": "HEAD_ROOT_BODY_LOCAL_YAW",
        "params": (
            "offset_u", "offset_v", "front_length", "rear_length",
            "half_height", "half_width", "roundness", "muzzle_taper",
        ),
    },
    {
        "id": "CERVICAL_NECK",
        "domain": "CORE",
        "basis": "ANATOMICAL_SEGMENT_TUBE_FIELD_V1",
        "frame": "HEAD_ROOT_TO_FOREQUARTER_REF",
        "params": (
            "start_radius_v", "start_radius_w", "end_radius_v", "end_radius_w",
            "roundness", "sag_bias",
        ),
    },
    {
        "id": "SHOULDER_CHEST",
        "domain": "CORE",
        "basis": "ASYMMETRIC_VENTRAL_SUPERELLIPSOID_FIELD_V1",
        "frame": "FOREQUARTER_REF_BODY_LOCAL_YAW",
        "params": (
            "offset_u", "offset_v", "front_length", "rear_length",
            "half_height", "half_width", "roundness", "ventral_fullness",
        ),
    },
    {
        "id": "THORAX_FLANK",
        "domain": "CORE",
        "basis": "DORSAL_BIASED_SUPERELLIPSOID_FIELD_V1",
        "frame": "BODY_ROOT_BODY_LOCAL_YAW",
        "params": (
            "offset_u", "offset_v", "half_length", "half_height", "half_width",
            "roundness", "dorsal_flatten",
        ),
    },
    {
        "id": "ABDOMEN_TUCK",
        "domain": "CORE",
        "basis": "ANALYTIC_TAPERED_WAIST_FIELD_V1",
        "frame": "BODY_ROOT_TO_PELVIS_REF",
        "params": (
            "start_radius_v", "mid_radius_v", "end_radius_v",
            "start_radius_w", "mid_radius_w", "end_radius_w", "ventral_lift",
        ),
    },
    {
        "id": "PELVIS_HAUNCH",
        "domain": "CORE",
        "basis": "ASYMMETRIC_HAUNCH_SUPERELLIPSOID_FIELD_V1",
        "frame": "PELVIS_REF_BODY_LOCAL_YAW",
        "params": (
            "offset_u", "offset_v", "front_length", "rear_length",
            "half_height", "half_width", "roundness", "haunch_fullness",
        ),
    },
    {
        "id": "FORE_PROXIMAL",
        "domain": "FORE_L/FORE_R",
        "basis": "PAIRED_PROXIMAL_EMERGENCE_FIELD_V1",
        "frame": "FOREQUARTER_REF_TO_CANONICAL_FORE_PAW",
        "params": (
            "length_fraction", "root_radius_v", "root_radius_w", "end_scale", "roundness",
        ),
    },
    {
        "id": "HIND_PROXIMAL",
        "domain": "HIND_L/HIND_R",
        "basis": "PAIRED_PROXIMAL_EMERGENCE_FIELD_V1",
        "frame": "PELVIS_REF_TO_CANONICAL_HIND_PAW",
        "params": (
            "length_fraction", "root_radius_v", "root_radius_w", "end_scale", "roundness",
        ),
    },
)

BLEND_INTERFACES = (
    {"id": "HEAD_NECK", "a": "CRANIUM_MUZZLE", "b": "CERVICAL_NECK", "operator": "POLYNOMIAL_SMOOTH_MIN_V1", "param": "blend_head_neck"},
    {"id": "NECK_SHOULDER", "a": "CERVICAL_NECK", "b": "SHOULDER_CHEST", "operator": "POLYNOMIAL_SMOOTH_MIN_V1", "param": "blend_neck_shoulder"},
    {"id": "SHOULDER_THORAX", "a": "SHOULDER_CHEST", "b": "THORAX_FLANK", "operator": "POLYNOMIAL_SMOOTH_MIN_V1", "param": "blend_shoulder_thorax"},
    {"id": "THORAX_ABDOMEN", "a": "THORAX_FLANK", "b": "ABDOMEN_TUCK", "operator": "POLYNOMIAL_SMOOTH_MIN_V1", "param": "blend_thorax_abdomen"},
    {"id": "ABDOMEN_PELVIS", "a": "ABDOMEN_TUCK", "b": "PELVIS_HAUNCH", "operator": "POLYNOMIAL_SMOOTH_MIN_V1", "param": "blend_abdomen_pelvis"},
    {"id": "SHOULDER_FORE", "a": "SHOULDER_CHEST", "b": "FORE_PROXIMAL", "operator": "POLYNOMIAL_SMOOTH_MIN_V1", "param": "blend_shoulder_fore"},
    {"id": "PELVIS_HIND", "a": "PELVIS_HAUNCH", "b": "HIND_PROXIMAL", "operator": "POLYNOMIAL_SMOOTH_MIN_V1", "param": "blend_pelvis_hind"},
)

COMPOSITION_ORDER = (
    "CRANIUM_MUZZLE",
    "CERVICAL_NECK",
    "SHOULDER_CHEST",
    "THORAX_FLANK",
    "ABDOMEN_TUCK",
    "PELVIS_HAUNCH",
    "FORE_PROXIMAL",
    "HIND_PROXIMAL",
)

SAMPLING_RULE = {
    "rule": "FIXED_ORTHOGRAPHIC_FIELD_OCCUPANCY_RASTER_V1",
    "canvasWidthPx": 224,
    "canvasHeightPx": 192,
    "depthSamples": 49,
    "screenPaddingDpFactor": 0.46,
    "depthHalfRangeDpFactor": 0.34,
    "viewSource": "canonical H6N M0/80 t in {0.0,0.5,1.0}",
    "structureFill": "UNSHADED_BINARY_WITH_OPTIONAL_REGION_DIAGNOSTIC",
}

CONTINUITY_TARGET = {
    "position": "NO_VISIBLE_GAP",
    "blend": "FIXED_POLYNOMIAL_SMOOTH_MIN",
    "organicBoundary": "G1_OR_C1_EQUIVALENT_WHERE_APPLICABLE",
    "perceptualOverride": "CAT_ID_AND_HEAD_BODY_REMAIN_REQUIRED",
}


def structural_parameter_names():
    names = []
    for region in REGIONS:
        names.extend(f"{region['id']}.{name}" for name in region["params"])
    names.extend(interface["param"] for interface in BLEND_INTERFACES)
    return tuple(names)


def region_parameter_count() -> int:
    return sum(len(region["params"]) for region in REGIONS)


def authoritative_scalar_count() -> int:
    return region_parameter_count() + len(BLEND_INTERFACES)


def grammar_payload():
    return {
        "version": GRAMMAR_VERSION,
        "sourceFamily": SOURCE_FAMILY,
        "sourcePackId": SOURCE_PACK_ID,
        "externalDomains": EXTERNAL_DOMAINS,
        "regions": REGIONS,
        "blends": BLEND_INTERFACES,
        "compositionOrder": COMPOSITION_ORDER,
        "sampling": SAMPLING_RULE,
        "continuity": CONTINUITY_TARGET,
        "wholeBodyOwner": "REGION_GRAMMAR_PLUS_FIXED_BLEND_LAWS",
        "derivedSamplingOwner": False,
        "viewSpecificParameters": False,
        "correctionCatalogue": CORRECTION_CATALOGUE,
    }


def grammar_signature() -> str:
    blob = json.dumps(grammar_payload(), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


if len(REGIONS) > 8:
    raise RuntimeError("R8 region ceiling exceeded")
if region_parameter_count() != 54:
    raise RuntimeError("R8 region scalar count drift")
if len(BLEND_INTERFACES) != 7:
    raise RuntimeError("R8 blend-interface count drift")
if authoritative_scalar_count() != 61:
    raise RuntimeError("R8 authoritative scalar count drift")
if authoritative_scalar_count() > 64:
    raise RuntimeError("R8 authoritative scalar ceiling exceeded")
if len(set(structural_parameter_names())) != authoritative_scalar_count():
    raise RuntimeError("R8 structural parameter names are not unique")
