from __future__ import annotations

import json
import math
from pathlib import Path

from p1_c_adult_walk_density_experiment_v1 import (
    DIRECTION_COUNTS,
    disagreement,
    mask,
    nearest_yaw,
    percentile,
    render_reference,
)

VERSION = "P1_C_ADULT_WALK_DIRECTION_HALFSTEP_DIAGNOSTIC_V1"
PHASES = tuple(k / 8.0 for k in range(8))


def evaluate_direction_halfsteps(direction_count: int) -> dict:
    step = 2.0 * math.pi / direction_count
    halfstep_yaws = tuple((k + 0.5) * step for k in range(direction_count))
    errors = []
    measured_angular_errors = []

    for phase in PHASES:
        for yaw in halfstep_yaws:
            qyaw = nearest_yaw(yaw, direction_count)
            d = abs((yaw - qyaw + math.pi) % (2.0 * math.pi) - math.pi)
            measured_angular_errors.append(math.degrees(d))
            errors.append(
                disagreement(
                    mask(render_reference(yaw, phase)),
                    mask(render_reference(qyaw, phase)),
                )
            )

    return {
        "directionCount": direction_count,
        "directionStepDeg": 360.0 / direction_count,
        "theoreticalMaxAngularErrorDeg": 180.0 / direction_count,
        "measuredHalfstepMaxAngularErrorDeg": max(measured_angular_errors),
        "meanHalfstepMaskDisagreement": sum(errors) / len(errors),
        "p95HalfstepMaskDisagreement": percentile(errors, 0.95),
        "maxHalfstepMaskDisagreement": max(errors),
        "sampleCount": len(errors),
    }


def run() -> dict:
    rows = [evaluate_direction_halfsteps(d) for d in DIRECTION_COUNTS]
    return {
        "version": VERSION,
        "phases": list(PHASES),
        "results": rows,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    result = run()
    (out / "direction_halfstep_summary.json").write_text(
        json.dumps(result, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
