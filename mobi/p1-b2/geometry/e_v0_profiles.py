from __future__ import annotations

from model import M0, M1, M2, Morphology
from orientation_v2 import M0_V2, M1_V2, M2_V2, MorphologyV2

PROFILE_VERSION = "P1_E_V0_MORPHOLOGY_PROBES_V1"

# Engineering-only same-age individuality probes authorized by P1-D/V0.
# They are not breed, sex, age, or biological phenotype standards.
I1_COMPACT = Morphology(
    id="I1_COMPACT_PROBE_V0",
    head_scale=1.03,
    trunk_length=0.92,
    trunk_depth=1.05,
    forequarter_scale=1.04,
    pelvis_scale=1.05,
    fore_limb_length=0.96,
    hind_limb_length=0.96,
    paw_scale=1.02,
    ear_scale=1.00,
    tail_length=0.94,
    tail_thickness=1.04,
)

I2_LANKY = Morphology(
    id="I2_LANKY_PROBE_V0",
    head_scale=0.97,
    trunk_length=1.10,
    trunk_depth=0.95,
    forequarter_scale=0.98,
    pelvis_scale=0.98,
    fore_limb_length=1.08,
    hind_limb_length=1.09,
    paw_scale=1.00,  # tightened by P1-E preflight to remain inside M1↔M2 sampled range
    ear_scale=1.01,
    tail_length=1.10,
    tail_thickness=0.96,
)

I1_COMPACT_V2 = MorphologyV2(
    I1_COMPACT,
    thorax_width_scale=1.04,
    pelvis_width_scale=1.06,
    stance_width_scale=1.02,
)
I2_LANKY_V2 = MorphologyV2(
    I2_LANKY,
    thorax_width_scale=0.97,
    pelvis_width_scale=0.98,
    stance_width_scale=0.96,
)

MORPHOLOGIES = (M1, M0, M2, I1_COMPACT, I2_LANKY)
ORIENTATION_MORPHOLOGIES = (
    M1_V2,
    M0_V2,
    M2_V2,
    I1_COMPACT_V2,
    I2_LANKY_V2,
)

MORPHOLOGY_BY_ID = {m.id: m for m in MORPHOLOGIES}
ORIENTATION_BY_ID = {m.id: m for m in ORIENTATION_MORPHOLOGIES}


def morphology_by_id(morphology_id: str) -> Morphology:
    return MORPHOLOGY_BY_ID[morphology_id]


def orientation_by_id(morphology_id: str) -> MorphologyV2:
    return ORIENTATION_BY_ID[morphology_id]


def _axis_values(morphology: Morphology):
    return {
        key: value
        for key, value in morphology.__dict__.items()
        if key != "id"
    }


def validate_probe_bounds() -> dict:
    """Verify I1/I2 stay within the already stress-tested M1↔M2 axis envelope."""
    lo = {}
    hi = {}
    for key, value in _axis_values(M1).items():
        other = getattr(M2, key)
        lo[key] = min(value, other)
        hi[key] = max(value, other)

    failures = []
    for probe in (I1_COMPACT, I2_LANKY):
        probe.validate()
        for key, value in _axis_values(probe).items():
            if not (lo[key] <= value <= hi[key]):
                failures.append({
                    "probe": probe.id,
                    "axis": key,
                    "value": value,
                    "min": lo[key],
                    "max": hi[key],
                })

    width_ranges = {
        "thorax_width_scale": (
            min(M1_V2.thorax_width_scale, M2_V2.thorax_width_scale),
            max(M1_V2.thorax_width_scale, M2_V2.thorax_width_scale),
        ),
        "pelvis_width_scale": (
            min(M1_V2.pelvis_width_scale, M2_V2.pelvis_width_scale),
            max(M1_V2.pelvis_width_scale, M2_V2.pelvis_width_scale),
        ),
        "stance_width_scale": (
            min(M1_V2.stance_width_scale, M2_V2.stance_width_scale),
            max(M1_V2.stance_width_scale, M2_V2.stance_width_scale),
        ),
    }
    for probe in (I1_COMPACT_V2, I2_LANKY_V2):
        probe.validate()
        for key, (low, high) in width_ranges.items():
            value = getattr(probe, key)
            if not (low <= value <= high):
                failures.append({
                    "probe": probe.id,
                    "axis": key,
                    "value": value,
                    "min": low,
                    "max": high,
                })

    return {
        "version": PROFILE_VERSION,
        "failures": failures,
        "pass": not failures,
    }
