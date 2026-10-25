#!/usr/bin/env python3
"""Mage Lv31 fidelity bridge for the T1 transition micro-sim.

This bridge repairs simulator-only drift against the approved P4-D1/P4-D2
Arcane Collapse contract without changing production gameplay or freezing any
new coefficient:

1. Lv31 circle radii inherit the current Lv21 Greater Orb radius on both axes,
   including the recovered Lv11 x1.35 radius modifier, before applying the
   provisional Lv31 radius multiplier.
2. The authoritative root primary receives only the one direct root impact and
   is excluded from all three AoE collapse stages.
3. The final chain excludes every target already hit anywhere in the same
   three-stage Lv31 package, not only targets hit by stage 1.

All existing provisional Lv31 centers (stage coefficient, delays, radius
multiplier, chain coefficient) remain unchanged and unfrozen.
"""
from __future__ import annotations

import t1_transition_microsim_core_v0_1 as core
import t1_transition_microsim_engine_v0_1 as engine


def with_mage_lv31_fidelity(fn):
    """Execute ``fn`` with only Mage Lv31 final-package fidelity corrected."""
    original_attack = engine.mage_attack
    original_process_event = engine.process_event

    def corrected_mage_attack(
        run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms
    ):
        if not final:
            return original_attack(
                run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms
            )

        # Preserve the already-approved Lv21 Heavy scalar continuity used by the
        # existing runner before constructing the replacement Lv31 package.
        if core.has_skill(run, 21) and heavy:
            raw *= 1.20

        px, py = primary["x"], primary["y"]
        center = runtime["lv31Centers"]["Mage"]
        radius_mul = float(center["radiusMultiplier"])

        # Approved Lv31 radius sensitivity is relative to the current Lv21
        # Greater Orb radius. The previous T1 adapter accidentally omitted the
        # Lv11 x1.35 factor on Y only.
        radius_x = runtime["geometry"]["mageBaseRadiusX"] * 1.35 * 1.60 * radius_mul
        radius_y = runtime["geometry"]["mageBaseRadiusY"] * 1.35 * 1.60 * radius_mul

        delays = [round(float(x) * 1000) for x in center["stageDelaysSeconds"]]
        if len(delays) != 3 or delays[0] != 0:
            raise core.RunnerFidelityError(
                f"unexpected Mage Lv31 stage delays: {center['stageDelaysSeconds']}"
            )

        parent_action_id = st["actionSeq"]
        primary_id = primary["id"]

        # One normal direct root impact. The primary is excluded from all AoE
        # stages below, matching the approved crowd-specialist contract.
        core.apply_damage(
            run,
            st,
            runtime,
            primary,
            raw,
            at_ms,
            "CRITICAL",
            "LV31_MAGE_PRIMARY",
            parent_action_id=parent_action_id,
        )

        immediate = core.nearby_targets(
            st,
            px,
            py,
            radius_x,
            radius_y,
            exclude_ids=(primary_id,),
            max_n=None,
        )
        for target in list(immediate):
            core.apply_damage(
                run,
                st,
                runtime,
                target,
                raw * float(center["stageCoefficient"]),
                at_ms,
                "SKILL",
                "LV31_MAGE_BLAST",
                parent_action_id=parent_action_id,
            )

        for i, delay in enumerate(delays[1:], start=1):
            core.schedule_event(
                st,
                at_ms + delay,
                "MAGE_LV31_BLAST",
                {
                    "center": (px, py),
                    "radiusX": radius_x,
                    "radiusY": radius_y,
                    "raw": raw * float(center["stageCoefficient"]),
                    "chainRaw": raw * 0.35,
                    "primaryTargetId": primary_id,
                    "finalStage": i == len(delays) - 1,
                    "parentActionId": parent_action_id,
                    "mageLv31FidelityBridge": "v0.1",
                },
            )

    def corrected_process_event(run, st, runtime, event):
        due_ms, _, kind, p = event
        if kind != "MAGE_LV31_BLAST" or p.get("mageLv31FidelityBridge") != "v0.1":
            return original_process_event(run, st, runtime, event)

        px, py = p["center"]
        primary_id = p["primaryTargetId"]
        targets = core.nearby_targets(
            st,
            px,
            py,
            p["radiusX"],
            p["radiusY"],
            exclude_ids=(primary_id,),
            max_n=None,
        )
        for target in list(targets):
            core.apply_damage(
                run,
                st,
                runtime,
                target,
                p["raw"],
                due_ms,
                "SKILL",
                "LV31_MAGE_BLAST",
                parent_action_id=p["parentActionId"],
            )

        if p.get("finalStage"):
            package_effects = {"LV31_MAGE_PRIMARY", "LV31_MAGE_BLAST"}
            hit_ids = {
                row["targetId"]
                for row in run["ledger"]
                if row.get("stage") == st["stage"]
                and row.get("parentActionId") == p["parentActionId"]
                and row.get("effectId") in package_effects
            }
            chain = [m for m in core.alive(st) if m["id"] not in hit_ids]
            chain.sort(key=lambda m: (m["x"], m["y"], m["id"]))
            for target in chain[:2]:
                core.apply_damage(
                    run,
                    st,
                    runtime,
                    target,
                    p["chainRaw"],
                    due_ms,
                    "SKILL",
                    "LV31_MAGE_CHAIN",
                    parent_action_id=p["parentActionId"],
                )

    engine.mage_attack = corrected_mage_attack
    engine.process_event = corrected_process_event
    try:
        return fn()
    finally:
        engine.mage_attack = original_attack
        engine.process_event = original_process_event


BRIDGE_METADATA = {
    "version": "t1-transition-microsim-mage-lv31-fidelity-bridge-v0.1",
    "productionGameplayChange": False,
    "numericalFreeze": False,
    "corrections": [
        "MAGE_LV31_Y_RADIUS_INHERITS_LV11_AND_LV21_RADIUS",
        "MAGE_LV31_PRIMARY_EXCLUDED_FROM_ALL_AOE_STAGES",
        "MAGE_LV31_FINAL_CHAIN_EXCLUDES_FULL_PACKAGE_HIT_SET",
    ],
}
