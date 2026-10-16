from __future__ import annotations

import json
import math
from pathlib import Path

from p1_c_r9_intrinsic_curve_pixel_v1 import (
    binary_mask,
    build_neutral_carrier,
    carrier_signature,
    mask_metrics,
    mask_sha256,
    orientation_metrics,
    paw_pin_errors,
    render_mask,
    structural_summary,
    write_png,
    write_strip_png,
)

OUT = Path("r9_stage1_evidence")


def metrics_dict(metrics):
    return {
        "yawRad": metrics.yaw_rad,
        "occupiedPixels": metrics.occupied_pixels,
        "componentCount": metrics.component_count,
        "bbox": list(metrics.bbox) if metrics.bbox is not None else None,
        "centroid": list(metrics.centroid) if metrics.centroid is not None else None,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    carrier = build_neutral_carrier()
    summary = structural_summary(carrier)

    named = [
        ("PROFILE", 0.0, False, False),
        ("THREE_QUARTER", math.pi / 4.0, False, False),
        ("FRONT", math.pi / 2.0, False, False),
        ("EAR_NEUTRAL_3Q", math.pi / 4.0, True, False),
        ("EAR_NEUTRAL_FRONT", math.pi / 2.0, True, False),
        ("DOMAIN_3Q", math.pi / 4.0, False, True),
        ("DOMAIN_FRONT", math.pi / 2.0, False, True),
    ]

    records = []
    for name, yaw, ears_off, domain in named:
        mask = render_mask(carrier, yaw, ear_neutralized=ears_off, domain_values=domain)
        if domain:
            output_mask = mask
            invert = False
        else:
            output_mask = binary_mask(mask)
            invert = True
        write_png(OUT / f"P1CR9_M0_80_{name}.png", output_mask, invert=invert)
        metrics = mask_metrics(binary_mask(mask), yaw)
        records.append({
            "name": name,
            "earNeutralized": ears_off,
            "domainDiagnostic": domain,
            "maskSha256": mask_sha256(mask),
            "metrics": metrics_dict(metrics),
            "pawPinErrorsDp": paw_pin_errors(carrier, yaw),
        })

    orient = orientation_metrics(carrier, steps=13)
    strip_masks = [frame[1] for frame in orient["frames"]]
    write_strip_png(OUT / "P1CR9_M0_80_ORIENTATION_0_TO_90_STRIP.png", strip_masks, invert=True)

    # Rerender exact equality for accepted evidence determinism.
    rerender_hashes = []
    for i in range(13):
        yaw = (math.pi / 2.0) * i / 12.0
        rerender_hashes.append(mask_sha256(binary_mask(render_mask(carrier, yaw))))
    deterministic = rerender_hashes == orient["frameHashes"]

    orientation_summary = {
        "steps": orient["steps"],
        "maxAreaJumpRatio": orient["maxAreaJumpRatio"],
        "maxCentroidStepPx": orient["maxCentroidStepPx"],
        "maxXorUnionRatio": orient["maxXorUnionRatio"],
        "maxComponentCount": orient["maxComponentCount"],
        "minOccupiedPixels": orient["minOccupiedPixels"],
        "frameHashes": orient["frameHashes"],
        "deterministicRerender": deterministic,
    }

    result = {
        "checkpoint": "P1-C-R9",
        "stage": "STAGE_1_NEUTRAL_ORIENTATION_PIXEL_GATE",
        "family": "RF_K_BOUNDED_INTRINSIC_DEFORMABLE_CURVE_CARRIER_WITH_PIXEL_RASTERIZATION",
        "carrier": summary,
        "carrierSignature": carrier_signature(carrier),
        "records": records,
        "orientation": orientation_summary,
        "mechanicalPass": bool(
            deterministic
            and orient["maxAreaJumpRatio"] <= 0.25
            and orient["maxCentroidStepPx"] <= 4.0
            and orient["maxXorUnionRatio"] <= 0.45
            and orient["maxComponentCount"] <= 3
            and orient["minOccupiedPixels"] > 160
            and max(max(r["pawPinErrorsDp"].values()) for r in records) <= 1e-9
        ),
        "notes": [
            "Stage 1 is neutral/orientation only; no motion-shape law is exercised.",
            "Pixel raster is derived from one body-local carrier; no authored view bases are present.",
            "Direct perceptual review remains required even if mechanicalPass=true.",
        ],
    }

    (OUT / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["mechanicalPass"]:
        raise SystemExit("R9 Stage 1 mechanical gate failed")


if __name__ == "__main__":
    main()
