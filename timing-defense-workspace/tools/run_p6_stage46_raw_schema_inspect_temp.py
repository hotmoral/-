#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import run_p5_p6_fidelity_bridge_stage46_49_temp_v0_1 as bridge


def shape(v, depth=0):
    if depth > 3:
        return type(v).__name__
    if isinstance(v, dict):
        return {k: shape(x, depth + 1) for k, x in v.items()}
    if isinstance(v, list):
        return [shape(v[0], depth + 1)] if v else []
    if isinstance(v, set):
        return "set"
    return type(v).__name__


def json_safe(v):
    if isinstance(v, set):
        return sorted(v)
    if isinstance(v, dict):
        return {k: json_safe(x) for k, x in v.items()}
    if isinstance(v, list):
        return [json_safe(x) for x in v]
    return v


def main():
    base, temporal, direction, shop, integration, central = bridge.load_inputs()
    sim_fn = bridge.build_bridge_simulate()
    bridge.BRIDGE_CTX["central"] = central
    state = bridge.new_run_state("SKILLED_V2_CENTRAL", central, 1, "Tank", 0)
    profile = bridge.integ.profile_for(shop, "Tank", "BALANCED")
    scale = float(integration["shopEffectScale"])
    wall = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * scale
    result = bridge.simulate_stage(
        sim_fn, base, temporal, direction, integration,
        "Tank", profile, scale, 46, wall, copy.deepcopy(state),
    )
    row = result["row"]
    print("RAW_KEYS=" + json.dumps(sorted(row.keys())))
    print("RAW_SHAPE=" + json.dumps(shape(row), sort_keys=True))
    print("RAW_ROW=" + json.dumps(json_safe(row), sort_keys=True))


if __name__ == "__main__":
    main()
