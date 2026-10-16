from __future__ import annotations

import hashlib
import json

import p1_c_r8_regional_grammar_v1 as grammar


PARAMETER_SET_VERSION = "P1_C_R8_NEUTRAL_M0_PARAMS_V1"
GRAMMAR_SIGNATURE = "20f1ace341726b6e0b36c45a19f5d01fb5be75ff0b7d27a6e5758850db1979e5"
NORMALIZATION = "ALL_LENGTHS_NORMALIZED_BY_SIZE_DP_EXCEPT_ROUNDNESS_TAPER_SCALE_BLEND"

REGION_PARAMS = {
    "CRANIUM_MUZZLE": {
        "offset_u": 0.018,
        "offset_v": 0.006,
        "front_length": 0.126,
        "rear_length": 0.092,
        "half_height": 0.106,
        "half_width": 0.110,
        "roundness": 2.35,
        "muzzle_taper": 0.34,
    },
    "CERVICAL_NECK": {
        "start_radius_v": 0.058,
        "start_radius_w": 0.062,
        "end_radius_v": 0.078,
        "end_radius_w": 0.084,
        "roundness": 2.20,
        "sag_bias": 0.012,
    },
    "SHOULDER_CHEST": {
        "offset_u": -0.020,
        "offset_v": 0.004,
        "front_length": 0.112,
        "rear_length": 0.170,
        "half_height": 0.146,
        "half_width": 0.136,
        "roundness": 2.30,
        "ventral_fullness": 0.22,
    },
    "THORAX_FLANK": {
        "offset_u": -0.010,
        "offset_v": 0.012,
        "half_length": 0.205,
        "half_height": 0.155,
        "half_width": 0.145,
        "roundness": 2.38,
        "dorsal_flatten": 0.16,
    },
    "ABDOMEN_TUCK": {
        "start_radius_v": 0.116,
        "mid_radius_v": 0.074,
        "end_radius_v": 0.108,
        "start_radius_w": 0.114,
        "mid_radius_w": 0.082,
        "end_radius_w": 0.108,
        "ventral_lift": 0.030,
    },
    "PELVIS_HAUNCH": {
        "offset_u": -0.030,
        "offset_v": 0.006,
        "front_length": 0.142,
        "rear_length": 0.172,
        "half_height": 0.146,
        "half_width": 0.136,
        "roundness": 2.28,
        "haunch_fullness": 0.20,
    },
    "FORE_PROXIMAL": {
        "length_fraction": 0.38,
        "root_radius_v": 0.066,
        "root_radius_w": 0.064,
        "end_scale": 0.48,
        "roundness": 2.12,
    },
    "HIND_PROXIMAL": {
        "length_fraction": 0.42,
        "root_radius_v": 0.082,
        "root_radius_w": 0.078,
        "end_scale": 0.50,
        "roundness": 2.16,
    },
}

BLEND_PARAMS = {
    "blend_head_neck": 0.24,
    "blend_neck_shoulder": 0.29,
    "blend_shoulder_thorax": 0.23,
    "blend_thorax_abdomen": 0.27,
    "blend_abdomen_pelvis": 0.26,
    "blend_shoulder_fore": 0.30,
    "blend_pelvis_hind": 0.32,
}


def parameter_payload():
    return {
        "version": PARAMETER_SET_VERSION,
        "grammarSignature": GRAMMAR_SIGNATURE,
        "normalization": NORMALIZATION,
        "regions": REGION_PARAMS,
        "blends": BLEND_PARAMS,
    }


def parameter_signature() -> str:
    blob = json.dumps(parameter_payload(), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def scalar_count() -> int:
    return sum(len(values) for values in REGION_PARAMS.values()) + len(BLEND_PARAMS)


def _validate():
    if grammar.grammar_signature() != GRAMMAR_SIGNATURE:
        raise RuntimeError("R8 grammar signature drift before neutral parameter load")
    expected_region_ids = tuple(region["id"] for region in grammar.REGIONS)
    if tuple(REGION_PARAMS) != expected_region_ids:
        raise RuntimeError("R8 neutral parameter region order/identity drift")
    for region in grammar.REGIONS:
        expected = tuple(region["params"])
        actual = tuple(REGION_PARAMS[region["id"]])
        if actual != expected:
            raise RuntimeError(("R8 neutral parameter semantic drift", region["id"], expected, actual))
    expected_blends = tuple(interface["param"] for interface in grammar.BLEND_INTERFACES)
    if tuple(BLEND_PARAMS) != expected_blends:
        raise RuntimeError("R8 neutral blend parameter semantic drift")
    if scalar_count() != grammar.authoritative_scalar_count():
        raise RuntimeError("R8 neutral scalar count drift")
    if scalar_count() != 61:
        raise RuntimeError("R8 frozen scalar count is not 61")


_validate()
