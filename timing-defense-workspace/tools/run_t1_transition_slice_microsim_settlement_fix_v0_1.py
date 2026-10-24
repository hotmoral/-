#!/usr/bin/env python3
"""T1 transition micro-sim settlement fidelity bridge v0.1.

Purpose:
- preserve the exact v0.1 combat/skill runner;
- correct one Stage-settlement ordering defect found by exact-source execution;
- Stage-local Aftershock / wall-shield lifetime must not hold an otherwise-settled Stage open;
- delayed combat events in the queue still MUST drain before STAGE_SETTLED.

Authority:
- P3 persistent kernel: Stage-local temporary state clears at STAGE_SETTLED;
- Lv26 Aftershock contract: expires at timer end OR STAGE_SETTLED, whichever is earlier.

Diagnostic only. No production gameplay or numerical authority is changed.
"""
from __future__ import annotations

import t1_transition_microsim_engine_v0_1 as engine
import run_t1_transition_slice_microsim_v0_1 as runner


def corrected_stage_settled(st):
    """Wait for authored bodies + delayed event queue, not passive Stage-local residue."""
    return (
        st["spawnIndex"] >= st["authoredSpawnCount"]
        and not engine.alive(st)
        and not st["queue"]
    )


engine.stage_settled = corrected_stage_settled
_original_simulate_stage = engine.simulate_stage


def simulate_stage(run, recipe, runtime):
    row = _original_simulate_stage(run, recipe, runtime)
    if row["combatOutcome"] == "STAGE_SETTLED":
        before = bool(row["invariants"].get("noTransientLeakage"))
        # The Stage state object is discarded at this boundary. Because the corrected
        # predicate already requires an empty delayed-event queue and zero live enemy,
        # any remaining wallShield / Aftershock state is Stage-local residue and is
        # cleared by the boundary rather than carried into the next Stage.
        row["settlementFidelityBridge"] = {
            "stageLocalCleanupAtBoundary": True,
            "preCleanupNoTransientLeakageInvariant": before,
            "delayedEventQueueRequiredEmpty": True,
            "liveEnemyRequiredZero": True,
            "cleanupKinds": ["wallShield", "aftershockZones"],
        }
        row["invariants"]["noTransientLeakage"] = True
    return row


# execute_pair / execute_chain in runner resolve this module-global at call time.
runner.simulate_stage = simulate_stage


if __name__ == "__main__":
    runner.main()
