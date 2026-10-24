#!/usr/bin/env python3
from __future__ import annotations
from t1_transition_microsim_core_v0_1 import *

def knight_attack(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms):
    if has_skill(run, 6):
        raw *= 1.12
    if has_skill(run, 16) and contains_perfect:
        raw *= 1.18
    if has_skill(run, 21) and heavy:
        raw *= 1.20
    knock_base = 1.20 if has_skill(run, 16) and contains_perfect else 1.0

    if final:
        targets = [primary] + forward_line_targets(st, primary, 3, runtime["geometry"]["heavyLineYTol"])
        for idx, target in enumerate(targets):
            apply_damage(
                run,
                st,
                runtime,
                target,
                raw,
                at_ms,
                "CRITICAL",
                "LV31_KNIGHT_FIRST_WAVE",
                knock_mul=knock_base * (1.0 + (0.15 * idx if has_skill(run, 26) else 0.0)),
                parent_action_id=st["actionSeq"],
            )
        center = runtime["lv31Centers"]["Knight"]
        schedule_event(
            st,
            at_ms + round(float(center["secondWaveDelaySeconds"]) * 1000),
            "KNIGHT_LV31_WAVE",
            {
                "raw": raw * float(center["secondWaveCoefficient"]),
                "parentActionId": st["actionSeq"],
            },
        )
        return

    apply_damage(
        run,
        st,
        runtime,
        primary,
        raw,
        at_ms,
        tier,
        "PLAYER_BASE_ATTACK",
        knock_mul=knock_base,
        parent_action_id=st["actionSeq"],
    )

    extra_n = 0
    if has_skill(run, 11):
        extra_n = 2 if heavy else 1
    if has_skill(run, 21) and heavy:
        extra_n = 3
    if extra_n <= 0:
        return

    coeff = 1.0 if has_skill(run, 26) else 0.85
    y_tol = runtime["geometry"]["heavyLineYTol"] if heavy else runtime["geometry"]["strictLineYTol"]
    for idx, target in enumerate(forward_line_targets(st, primary, extra_n, y_tol), start=1):
        step = 1.0 + (0.15 * idx if has_skill(run, 26) else 0.0)
        apply_damage(
            run,
            st,
            runtime,
            target,
            raw * coeff,
            at_ms,
            tier,
            "KNIGHT_PENETRATION",
            knock_mul=knock_base * step,
            parent_action_id=st["actionSeq"],
        )


def rogue_attack(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms):
    if has_skill(run, 11) and proc_roll(run) < 0.06:
        raw *= 1.5
        st["procCrits"] += 1

    if final:
        center = runtime["lv31Centers"]["Rogue"]
        count = int(center["daggers"])
        duration_ms = round(float(center["stormDurationSeconds"]) * 1000)
        coeff = float(center["perDaggerCoefficient"])
        denom = max(1, count - 1)
        for i in range(count):
            schedule_event(
                st,
                at_ms + round(i * duration_ms / denom),
                "ROGUE_LV31_DAGGER",
                {
                    "raw": raw * coeff,
                    "targetId": primary["id"],
                    "effectId": "LV31_ROGUE_DAGGER_STORM",
                    "parentActionId": st["actionSeq"],
                },
            )
        return

    apply_damage(
        run,
        st,
        runtime,
        primary,
        raw,
        at_ms,
        tier,
        "PLAYER_BASE_ATTACK",
        parent_action_id=st["actionSeq"],
    )

    if heavy and has_skill(run, 21):
        for i in range(4):
            schedule_event(
                st,
                at_ms + 55 * (i + 1),
                "ROGUE_FOLLOWUP",
                {
                    "raw": raw * 0.45,
                    "targetId": primary["id"],
                    "effectId": "LV21_ROGUE_BLADE_BARRAGE",
                    "parentActionId": st["actionSeq"],
                },
            )
    elif has_skill(run, 6):
        schedule_event(
            st,
            at_ms + 55,
            "ROGUE_FOLLOWUP",
            {
                "raw": raw * 0.55,
                "targetId": primary["id"],
                "effectId": "LV6_ROGUE_SECOND_HIT",
                "parentActionId": st["actionSeq"],
            },
        )

    if has_skill(run, 26) and contains_perfect:
        secondary = nearest_secondary(st, primary["id"])
        if secondary:
            schedule_event(
                st,
                at_ms + 75,
                "ROGUE_CHAIN",
                {
                    "raw": raw * 0.45,
                    "targetId": secondary["id"],
                    "rootPrimaryId": primary["id"],
                    "parentActionId": st["actionSeq"],
                },
            )


def tank_attack(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms):
    if final:
        center = runtime["lv31Centers"]["Tank"]
        targets = list(alive(st))
        for target in targets:
            apply_damage(
                run,
                st,
                runtime,
                target,
                raw * float(center["shockwaveCoefficient"]),
                at_ms,
                "CRITICAL",
                "LV31_TANK_ABSOLUTE_BARRIER_SHOCKWAVE",
                knock_mul=float(center["knockbackMultiplier"]),
                parent_action_id=st["actionSeq"],
            )
        set_wall_shield(
            st,
            float(center["barrier"]),
            at_ms + round(float(center["barrierSeconds"]) * 1000),
            "LV31",
        )
        return

    knock_mul = 1.0
    if has_skill(run, 6):
        knock_mul = 2.0 if heavy and has_skill(run, 21) else 1.30

    impact_x, impact_y = primary["x"], primary["y"]
    apply_damage(
        run,
        st,
        runtime,
        primary,
        raw,
        at_ms,
        tier,
        "PLAYER_BASE_ATTACK",
        knock_mul=knock_mul,
        parent_action_id=st["actionSeq"],
    )

    if heavy and has_skill(run, 21):
        secondaries = nearby_targets(
            st,
            impact_x,
            impact_y,
            runtime["geometry"]["nearbyX"],
            runtime["geometry"]["nearbyY"],
            exclude_ids=(primary["id"],),
            max_n=None,
        )
        for target in secondaries:
            apply_damage(
                run,
                st,
                runtime,
                target,
                raw,
                at_ms,
                tier,
                "LV21_TANK_GROUND_IMPACT",
                knock_mul=2.0,
                parent_action_id=st["actionSeq"],
            )

    if has_skill(run, 16) and contains_perfect:
        set_wall_shield(st, 80.0, at_ms + 3000, "LV16")

    if heavy and has_skill(run, 26):
        st["aftershockZones"].append(
            {
                "untilMs": at_ms + 1500,
                "x": impact_x,
                "y": impact_y,
                "dx": runtime["geometry"]["nearbyX"],
                "dy": runtime["geometry"]["nearbyY"],
            }
        )


def archer_arrow(
    run,
    st,
    runtime,
    raw,
    tier,
    launch_x,
    launch_y,
    primary,
    at_ms,
    contains_perfect,
    parent_action_id,
    effect_id,
):
    armor_ignore = has_skill(run, 16) and contains_perfect
    apply_damage(
        run,
        st,
        runtime,
        primary,
        raw,
        at_ms,
        tier,
        effect_id,
        armor_ignore=armor_ignore,
        parent_action_id=parent_action_id,
    )
    if not has_skill(run, 6):
        return
    max_extra = 2
    if has_skill(run, 26) and contains_perfect:
        max_extra += 2
    candidates = [
        m
        for m in alive(st)
        if m["id"] != primary["id"]
        and m["x"] >= launch_x - 1e-9
        and abs(m["y"] - launch_y) <= runtime["geometry"]["strictLineYTol"]
    ]
    candidates.sort(key=lambda m: (m["x"], abs(m["y"] - launch_y), m["id"]))
    for target in candidates[:max_extra]:
        coeff = 1.0 if armor_ignore else 0.52
        apply_damage(
            run,
            st,
            runtime,
            target,
            raw * coeff,
            at_ms,
            tier,
            "ARCHER_PENETRATION",
            armor_ignore=armor_ignore,
            parent_action_id=parent_action_id,
        )


def archer_attack(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms):
    if has_skill(run, 11):
        raw *= 1.10
    launch_x, launch_y = primary["x"], primary["y"]

    if final:
        center = runtime["lv31Centers"]["Archer"]
        coeff = float(center["perTargetCoefficient"])
        targets = [
            m
            for m in alive(st)
            if m["x"] >= launch_x - 1e-9
            and abs(m["y"] - launch_y) <= runtime["geometry"]["heavyLineYTol"]
        ]
        targets.sort(key=lambda m: (m["x"], abs(m["y"] - launch_y), m["id"]))
        for target in targets:
            apply_damage(
                run,
                st,
                runtime,
                target,
                raw * coeff,
                at_ms,
                "CRITICAL",
                "LV31_ARCHER_SKY_PIERCING_ARROW",
                armor_ignore=True,
                parent_action_id=st["actionSeq"],
            )
        return

    arrow_coeffs = [1.0, 0.65, 0.65] if heavy and has_skill(run, 21) else [1.0]
    for idx, coeff in enumerate(arrow_coeffs):
        current_primary = target_by_id(st, primary["id"])
        if not current_primary:
            line = [
                m
                for m in alive(st)
                if m["x"] >= launch_x - 0.02
                and abs(m["y"] - launch_y) <= runtime["geometry"]["strictLineYTol"]
            ]
            line.sort(key=lambda m: (m["x"], m["id"]))
            current_primary = line[0] if line else None
        if not current_primary:
            continue
        archer_arrow(
            run,
            st,
            runtime,
            raw * coeff,
            tier if idx == 0 else "SKILL",
            launch_x,
            launch_y,
            current_primary,
            at_ms,
            contains_perfect,
            st["actionSeq"],
            "PLAYER_BASE_ATTACK" if idx == 0 else "LV21_ARCHER_TRIPLE_SHOT",
        )


def mage_attack(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms):
    if has_skill(run, 21) and heavy:
        raw *= 1.20
    px, py = primary["x"], primary["y"]

    if final:
        center = runtime["lv31Centers"]["Mage"]
        radius_x = (
            runtime["geometry"]["mageBaseRadiusX"]
            * 1.35
            * 1.60
            * float(center["radiusMultiplier"])
        )
        radius_y = runtime["geometry"]["mageBaseRadiusY"] * 1.60 * float(center["radiusMultiplier"])
        apply_damage(
            run,
            st,
            runtime,
            primary,
            raw,
            at_ms,
            "CRITICAL",
            "LV31_MAGE_PRIMARY",
            parent_action_id=st["actionSeq"],
        )
        already = {primary["id"]}
        immediate = nearby_targets(st, px, py, radius_x, radius_y, exclude_ids=(primary["id"],), max_n=None)
        for target in immediate:
            apply_damage(
                run,
                st,
                runtime,
                target,
                raw * float(center["stageCoefficient"]),
                at_ms,
                "SKILL",
                "LV31_MAGE_BLAST",
                parent_action_id=st["actionSeq"],
            )
            already.add(target["id"])
        delays = [round(float(x) * 1000) for x in center["stageDelaysSeconds"]]
        for i, delay in enumerate(delays[1:], start=1):
            schedule_event(
                st,
                at_ms + delay,
                "MAGE_LV31_BLAST",
                {
                    "center": (px, py),
                    "radiusX": radius_x,
                    "radiusY": radius_y,
                    "raw": raw * float(center["stageCoefficient"]),
                    "chainRaw": raw * 0.35,
                    "alreadyHitIds": sorted(already),
                    "finalStage": i == len(delays) - 1,
                    "parentActionId": st["actionSeq"],
                },
            )
        return

    apply_damage(
        run,
        st,
        runtime,
        primary,
        raw,
        at_ms,
        tier,
        "PLAYER_BASE_ATTACK",
        parent_action_id=st["actionSeq"],
    )
    root_hit_ids = {primary["id"]}

    if has_skill(run, 6):
        radius_x = runtime["geometry"]["mageBaseRadiusX"]
        radius_y = runtime["geometry"]["mageBaseRadiusY"]
        splash = 0.50
        if has_skill(run, 11):
            radius_x *= 1.35
            radius_y *= 1.35
            splash = 0.60
        if heavy and has_skill(run, 21):
            radius_x *= 1.60
            radius_y *= 1.60

        immediate = nearby_targets(
            st,
            px,
            py,
            radius_x,
            radius_y,
            exclude_ids=(primary["id"],),
            max_n=3,
        )
        for target in immediate:
            apply_damage(
                run,
                st,
                runtime,
                target,
                raw * splash,
                at_ms,
                "SKILL",
                "MAGE_ARCANE_BURST",
                parent_action_id=st["actionSeq"],
            )
            root_hit_ids.add(target["id"])

        if has_skill(run, 16) and contains_perfect:
            schedule_event(
                st,
                at_ms + 180,
                "MAGE_RESONANCE",
                {
                    "center": (px, py),
                    "radiusX": radius_x,
                    "radiusY": radius_y,
                    "raw": raw * 0.55,
                    "excludeId": primary["id"],
                    "parentActionId": st["actionSeq"],
                },
            )

        if has_skill(run, 26) and len(root_hit_ids) >= 2:
            candidates = [m for m in alive(st) if m["id"] not in root_hit_ids]
            candidates.sort(key=lambda m: (m["x"], m["y"], m["id"]))
            for target in candidates[:2]:
                apply_damage(
                    run,
                    st,
                    runtime,
                    target,
                    raw * 0.35,
                    at_ms,
                    "SKILL",
                    "LV26_MAGE_CHAIN_EXPLOSION",
                    parent_action_id=st["actionSeq"],
                )
