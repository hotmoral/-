#!/usr/bin/env python3
from __future__ import annotations

import json
import run_p5_p6_fidelity_bridge_stage46_49_temp_v0_1 as bridge


def summarize_shape(obj, depth=0):
    if depth > 4:
        return type(obj).__name__
    if isinstance(obj, dict):
        return {k: summarize_shape(v, depth + 1) for k, v in obj.items()}
    if isinstance(obj, list):
        return [summarize_shape(obj[0], depth + 1)] if obj else []
    return type(obj).__name__


def main():
    base, temporal, direction, shop, integration, central = bridge.load_inputs()
    sim_fn = bridge.build_bridge_simulate()
    row = bridge.run_chain(
        sim_fn, base, temporal, direction, shop, integration, central,
        "Knight", "SKILLED_V2_CENTRAL", 1, 0,
    )
    print("TOP_KEYS=" + json.dumps(sorted(row.keys())))
    print("SHAPE=" + json.dumps(summarize_shape(row), sort_keys=True))
    print("ROW=" + json.dumps(row, sort_keys=True))


if __name__ == "__main__":
    main()
