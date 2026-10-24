#!/usr/bin/env python3
from __future__ import annotations
from t1_transition_microsim_core_v0_1 import *
from t1_transition_microsim_skills_v0_1 import *

def root_action(run, st, runtime, at_ms: int):
    primary = front(st)
    if not primary:
        st["nextActionMs"] = at_ms + 50
        return

    st["actionSeq"] += 1
    st["rootTimingActionCount"] += 1
    heavy = run["charge"] >= 3
    x = judge(run, runtime)
    y = judge(run, runtime) if heavy else None
    milestones = []

    if heavy:
        milestones += update_combo(run, x)
        predicted_combo = run["combo"] + 1 if y == "PERFECT" else 0
        tier = strong_tier(x, y or "NORMAL")
        milestones += update_combo(run, y or "NORMAL")
    else:
        predicted_combo = run["combo"] + 1 if x == "PERFECT" else 0
        tier = x
        milestones += update_combo(run, x)

    raw = float(BASE[tier]) * (1.0 + combo_bonus(predicted_combo))
    contains_perfect = x == "PERFECT" or y == "PERFECT"
    final = heavy and x == y == "PERFECT" and has_skill(run, 31)
    cls = run["classId"]

    st["judgmentTrace"].append(
        {
            "action": st["actionSeq"],
            "atMs": at_ms,
            "heavy": heavy,
            "x": x,
            "y": y,
            "tier": tier,
            "containsPerfect": contains_perfect,
            "comboAfter": run["combo"],
            "chargeBefore": run["charge"],
            "lv31Final": final,
            "primaryTargetId": primary["id"],
            "primaryTargetType": primary["type"],
            "primaryTargetX": round(float(primary["x"]), 6),
            "primaryTargetY": round(float(primary["y"]), 6),
        }
    )

    if cls == "knight":
        knight_attack(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms)
    elif cls == "rogue":
        rogue_attack(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms)
    elif cls == "tank":
        tank_attack(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms)
    elif cls == "archer":
        archer_attack(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms)
    elif cls == "mage":
        mage_attack(run, st, runtime, raw, tier, heavy, contains_perfect, final, primary, at_ms)
    else:
        raise RunnerFidelityError(cls)

    for m in milestones:
        execute_n3(run, st, runtime, m, at_ms, primary)

    run["charge"] = 0 if heavy else min(3, run["charge"] + 1)
    next_delay = int(runtime["actionIntervalMs"])
    if cls == "rogue" and has_skill(run, 16) and contains_perfect:
        next_delay = max(1, next_delay - 78)
    st["nextActionMs"] = at_ms + next_delay


def new_stage(recipe, run):
    times = [int(x["tMs"]) for x in recipe["spawns"]]
    return {
        "stage": int(recipe["stage"]),
        "recipeId": recipe["id"],
        "recipeDigest": sha256_obj(recipe),
        "atMs": 0,
        "spawnIndex": 0,
        "nextMobId": 1,
        "monsters": [],
        "queue": [],
        "queueSeq": 0,
        "nextActionMs": 0,
        "actionSeq": 0,
        "rootTimingActionCount": 0,
        "damage": 0.0,
        "kills": 0,
        "killsByType": {},
        "peakActive": 0,
        "wallDamage": 0.0,
        "wallShield": 0.0,
        "wallShieldUntilMs": 0,
        "wallShieldSource": None,
        "aftershockZones": [],
        "control": {
            "knockbackDistance": 0.0,
            "aftershockSlowDistancePrevented": 0.0,
            "ironWallDamagePrevented": 0.0,
            "shieldAbsorbed": 0.0,
        },
        "frontlineBruteMs": 0,
        "backlineExposureMs": 0,
        "targetReorderCount": 0,
        "lastFrontId": None,
        "firstWallContactMs": None,
        "judgmentTrace": [],
        "procCrits": 0,
        "entry": {
            "baseHp": run["baseHp"],
            "baseMaxHp": run["baseMaxHp"],
            "wallDeficit": run["baseMaxHp"] - run["baseHp"],
            "combo": run["combo"],
            "charge": run["charge"],
            "judgmentRng": run["judgmentRng"],
            "combatProcRng": run["combatProcRng"],
        },
        "authoredSpawnCount": len(recipe["spawns"]),
        "effectiveEntityCount": 0,
        "max4sDensity": max_density(times, 4000),
        "max6sDensity": max_density(times, 6000),
        "firstSpawnMs": min(times) if times else None,
        "settled": False,
    }


def expire_stage_effects(st, at_ms):
    st["aftershockZones"] = [z for z in st["aftershockZones"] if z["untilMs"] > at_ms]
    if st["wallShield"] > 0 and at_ms >= st["wallShieldUntilMs"]:
        st["wallShield"] = 0.0
        st["wallShieldSource"] = None


def apply_wall_contact(run, st, runtime, mob, at_ms):
    incoming = float(runtime["monsters"][mob["type"]]["wallDamage"])
    if run["classId"] == "tank" and has_skill(run, 11):
        prevented = incoming * 0.10
        st["control"]["ironWallDamagePrevented"] += prevented
        incoming *= 0.90
    absorb = min(st["wallShield"], incoming) if st["wallShield"] > 0 else 0.0
    if absorb > 0:
        st["wallShield"] -= absorb
        st["control"]["shieldAbsorbed"] += absorb
        if st["wallShield"] <= 1e-9:
            st["wallShield"] = 0.0
            st["wallShieldSource"] = None
    hp_damage = incoming - absorb
    run["baseHp"] -= hp_damage
    st["wallDamage"] += hp_damage
    mob["alive"] = False
    if st["firstWallContactMs"] is None:
        st["firstWallContactMs"] = at_ms
    if run["baseHp"] <= 0:
        run["baseHp"] = 0.0
        run["status"] = "FAILED"


def move_monsters(run, st, runtime, dt_ms: int, at_ms: int):
    dt_s = dt_ms / 1000.0
    for mob in list(alive(st)):
        speed = float(runtime["monsters"][mob["type"]]["speed"])
        base_distance = speed * dt_s
        actual_distance = base_distance
        if run["classId"] == "tank" and has_skill(run, 26):
            if any(
                abs(mob["x"] - z["x"]) <= z["dx"]
                and abs(mob["y"] - z["y"]) <= z["dy"]
                for z in st["aftershockZones"]
            ):
                actual_distance *= 0.75
                st["control"]["aftershockSlowDistancePrevented"] += base_distance - actual_distance
        mob["x"] -= actual_distance
        if mob["x"] <= runtime["wallX"] and mob["alive"]:
            apply_wall_contact(run, st, runtime, mob, at_ms)


def stage_settled(st):
    return (
        st["spawnIndex"] >= st["authoredSpawnCount"]
        and not alive(st)
        and not st["queue"]
        and not st["aftershockZones"]
        and st["wallShield"] <= 1e-9
    )


def simulate_stage(run, recipe, runtime):
    st = new_stage(recipe, run)
    dt = int(runtime["timeStepMs"])
    spawns = recipe["spawns"]

    while st["atMs"] <= SAFETY_CAP_MS:
        at_ms = st["atMs"]

        while st["spawnIndex"] < len(spawns) and int(spawns[st["spawnIndex"]]["tMs"]) <= at_ms:
            spec = spawns[st["spawnIndex"]]
            typ = spec["type"]
            anchor = runtime["monsters"][typ]
            st["monsters"].append(
                {
                    "id": f"S{st['stage']}_{st['nextMobId']}",
                    "type": typ,
                    "x": float(runtime["spawnX"]),
                    "y": float(spec["y"]),
                    "hp": float(anchor["hp"]),
                    "maxHp": float(anchor["hp"]),
                    "alive": True,
                }
            )
            st["nextMobId"] += 1
            st["spawnIndex"] += 1
            st["effectiveEntityCount"] += 1

        st["peakActive"] = max(st["peakActive"], len(alive(st)))

        while st["queue"] and st["queue"][0][0] <= at_ms:
            event = heapq.heappop(st["queue"])
            process_event(run, st, runtime, event)

        expire_stage_effects(st, at_ms)

        if at_ms >= st["nextActionMs"]:
            root_action(run, st, runtime, at_ms)

        current_front = front(st)
        current_front_id = current_front["id"] if current_front else None
        if (
            st["lastFrontId"] is not None
            and current_front_id is not None
            and current_front_id != st["lastFrontId"]
        ):
            st["targetReorderCount"] += 1
        st["lastFrontId"] = current_front_id

        if current_front and current_front["type"] == "BRUTE":
            st["frontlineBruteMs"] += dt
            if any(m["id"] != current_front["id"] for m in alive(st)):
                st["backlineExposureMs"] += dt

        move_monsters(run, st, runtime, dt, at_ms)

        st["peakActive"] = max(st["peakActive"], len(alive(st)))

        if run["status"] == "FAILED":
            break

        if stage_settled(st):
            st["settled"] = True
            break

        st["atMs"] += dt

    if st["atMs"] > SAFETY_CAP_MS:
        raise RunnerFidelityError(
            f"{recipe['id']} exceeded {SAFETY_CAP_MS}ms without STAGE_SETTLED; no timer deletion applied"
        )

    exit_state = {
        "baseHp": run["baseHp"],
        "baseMaxHp": run["baseMaxHp"],
        "wallDeficit": run["baseMaxHp"] - run["baseHp"],
        "combo": run["combo"],
        "charge": run["charge"],
        "judgmentRng": run["judgmentRng"],
        "combatProcRng": run["combatProcRng"],
    }
    wall_contact_delay = None
    if st["firstWallContactMs"] is not None and st["firstSpawnMs"] is not None:
        wall_contact_delay = (st["firstWallContactMs"] - st["firstSpawnMs"]) / 1000.0

    settled_seconds = st["atMs"] / 1000.0
    return {
        "stage": st["stage"],
        "recipeId": st["recipeId"],
        "recipeDigest": st["recipeDigest"],
        "authoredSpawnCount": st["authoredSpawnCount"],
        "effectiveEntityCount": st["effectiveEntityCount"],
        "peakActive": st["peakActive"],
        "max4sDensity": st["max4sDensity"],
        "max6sDensity": st["max6sDensity"],
        "frontlineBlockTime": round(st["frontlineBruteMs"] / 1000.0, 3),
        "targetReorderCount": st["targetReorderCount"],
        "backlineExposure": round(st["backlineExposureMs"] / 1000.0, 3),
        "spawnToFirstContact": None if wall_contact_delay is None else round(wall_contact_delay, 3),
        "damage": round(st["damage"], 3),
        "kills": st["kills"],
        "killsByType": st["killsByType"],
        "removalThroughput": round(st["kills"] / max(settled_seconds, 0.001), 6),
        "controlValue": {
            k: round(v, 6) for k, v in st["control"].items()
        },
        "wallDamage": round(st["wallDamage"], 3),
        "wallReserve": round(run["baseHp"], 3),
        "rootTimingActionCount": st["rootTimingActionCount"],
        "stageSettledTime": round(settled_seconds, 3),
        "procCrits": st["procCrits"],
        "entryState": st["entry"],
        "exitState": exit_state,
        "skillState": {
            "class": run["classId"],
            "level": run["level"],
            "activeMilestones": list(run["activeMilestones"]),
        },
        "actionTraceDigest": sha256_obj(st["judgmentTrace"]),
        "actionTrace": st["judgmentTrace"],
        "combatOutcome": (
            "FAILED_WALL_DESTROYED"
            if run["status"] == "FAILED"
            else "STAGE_SETTLED"
            if st["settled"]
            else "UNSETTLED"
        ),
        "failureClassification": (
            "PASS_WITH_WATCH"
            if run["status"] != "FAILED" and st["settled"]
            else "PASS_WITH_WATCH"
        ),
        "invariants": {
            "stageSettled": bool(st["settled"]),
            "noEnemyCarry": len(alive(st)) == 0 if st["settled"] else run["status"] == "FAILED",
            "noTransientLeakage": (
                not st["queue"] and not st["aftershockZones"] and st["wallShield"] <= 1e-9
            )
            if st["settled"]
            else run["status"] == "FAILED",
        },
    }
