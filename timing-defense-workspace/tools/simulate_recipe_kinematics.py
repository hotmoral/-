#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


def simulate(recipe, anchor):
    world = anchor["world"]
    meta = anchor["monsters"]
    dt = int(world["timeStepMs"])
    horizon = int(world["horizonMs"])
    spawn_x = float(world["spawnX"])
    wall_x = float(world["wallX"])

    specs = sorted(recipe["spawns"], key=lambda x: int(x["tMs"]))
    monsters = []
    next_id = 1
    spawn_idx = 0
    t = 0

    front_sequence = []
    last_front_id = None
    supporter = defaultdict(lambda: {"aliveMs": 0, "auraAnyMs": 0, "screenedAuraMs": 0})
    wall_arrivals = []
    sieger_first_shot = {}
    max_charger_windups = 0

    def y_at(m, at):
        if m["type"] != "FLYER":
            return m["y0"]
        age = max(0, at - m["spawnMs"]) / 1000.0
        d = meta["FLYER"]
        return m["y0"] + float(d["oscillationAmplitude"]) * math.sin(age * float(d["oscillationOmega"]))

    while t <= horizon:
        while spawn_idx < len(specs) and int(specs[spawn_idx]["tMs"]) <= t:
            s = specs[spawn_idx]
            monsters.append({
                "id": next_id,
                "type": s["type"],
                "x": spawn_x,
                "y0": float(s["y"]),
                "spawnMs": int(s["tMs"]),
                "phase": "advance",
                "phaseAt": int(s["tMs"]),
                "alive": True,
                "shots": 0,
            })
            next_id += 1
            spawn_idx += 1

        alive = [m for m in monsters if m["alive"]]
        supporters = [m for m in alive if m["type"] == "SUPPORTER"]

        aura_sources = defaultdict(list)
        for target in alive:
            if target["type"] == "SUPPORTER":
                continue
            for source in supporters:
                dist = math.hypot(target["x"] - source["x"], y_at(target, t) - y_at(source, t))
                if dist <= float(meta["SUPPORTER"]["auraRadius"]) + 1e-12:
                    aura_sources[target["id"]].append(source["id"])

        front = min(alive, key=lambda m: (m["x"], m["id"])) if alive else None
        if front and front["id"] != last_front_id:
            front_sequence.append({"atMs": t, "id": front["id"], "type": front["type"], "x": front["x"]})
            last_front_id = front["id"]

        for source in supporters:
            row = supporter[source["id"]]
            row["aliveMs"] += dt
            targets = [m for m in alive if m["id"] != source["id"] and source["id"] in aura_sources.get(m["id"], [])]
            if targets:
                row["auraAnyMs"] += dt
                if front and front["id"] != source["id"]:
                    row["screenedAuraMs"] += dt

        for m in alive:
            if m["type"] == "CHARGER":
                d = meta["CHARGER"]
                if m["phase"] == "advance" and m["x"] <= float(d["triggerX"]):
                    m["phase"] = "windup"
                    m["phaseAt"] = t
                elif m["phase"] == "windup" and t - m["phaseAt"] >= int(d["windupMs"]):
                    m["phase"] = "charge"
                    m["phaseAt"] = t

            elif m["type"] == "SIEGER":
                d = meta["SIEGER"]
                if m["phase"] == "advance" and m["x"] <= float(d["standoffX"]):
                    m["x"] = float(d["standoffX"])
                    m["phase"] = "windup"
                    m["phaseAt"] = t
                elif m["phase"] == "windup" and t - m["phaseAt"] >= int(d["windupMs"]):
                    m["phase"] = "cooldown"
                    m["phaseAt"] = t
                    m["shots"] += 1
                    sieger_first_shot.setdefault(m["id"], t)
                elif m["phase"] == "cooldown" and t - m["phaseAt"] >= int(d["repeatMs"] - d["windupMs"]):
                    m["phase"] = "windup"
                    m["phaseAt"] = t

        max_charger_windups = max(
            max_charger_windups,
            sum(1 for m in alive if m["type"] == "CHARGER" and m["phase"] == "windup"),
        )

        sec = dt / 1000.0
        for m in alive:
            typ = m["type"]
            if typ == "SIEGER" and m["phase"] != "advance":
                continue
            if typ == "CHARGER":
                d = meta["CHARGER"]
                speed = 0.0 if m["phase"] == "windup" else float(d["chargeSpeed"] if m["phase"] == "charge" else d["speed"])
            else:
                speed = float(meta[typ]["speed"])
            if typ != "SUPPORTER" and aura_sources.get(m["id"]):
                speed *= float(meta["SUPPORTER"]["auraSpeedMultiplier"])
            m["x"] -= speed * sec

        for m in alive:
            if m["type"] == "SIEGER" or not m["alive"]:
                continue
            if m["x"] <= wall_x:
                m["alive"] = False
                wall_arrivals.append({"atMs": t, "id": m["id"], "type": m["type"]})

        if spawn_idx >= len(specs) and not [m for m in monsters if m["alive"]]:
            break
        t += dt

    def front_at(at_ms):
        current = None
        for row in front_sequence:
            if row["atMs"] <= at_ms:
                current = row
            else:
                break
        return current

    shots = []
    for monster_id, shot_at in sieger_first_shot.items():
        front = front_at(shot_at)
        shots.append({
            "siegeId": monster_id,
            "firstShotAtMs": shot_at,
            "frontTypeAtShot": front["type"] if front else None,
            "screenedAtFirstShot": bool(front and front["id"] != monster_id),
        })

    return {
        "id": recipe["id"],
        "tier": recipe["tier"],
        "archetype": recipe["archetype"],
        "maxConcurrentChargerWindups": max_charger_windups,
        "supporters": dict(supporter),
        "siegers": shots,
        "wallArrivals": wall_arrivals,
        "frontSequence": front_sequence,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("recipes", type=Path)
    parser.add_argument("anchor", type=Path)
    args = parser.parse_args()

    recipe_data = yaml.safe_load(args.recipes.read_text(encoding="utf-8"))
    anchor = yaml.safe_load(args.anchor.read_text(encoding="utf-8"))

    print(f"SIMULATION=KINEMATIC_PRELIGHT recipes={len(recipe_data.get('recipes', []))}")
    for recipe in recipe_data.get("recipes", []):
        out = simulate(recipe, anchor)
        support_parts = []
        for sid, row in out["supporters"].items():
            support_parts.append(
                f"SUP#{sid}:aura={row['auraAnyMs']/1000:.2f}s,screened={row['screenedAuraMs']/1000:.2f}s"
            )
        siege_parts = []
        for row in out["siegers"]:
            siege_parts.append(
                f"SI#{row['siegeId']}:shot={row['firstShotAtMs']/1000:.2f}s,screened={row['screenedAtFirstShot']},front={row['frontTypeAtShot']}"
            )
        print(
            f"{out['id']} chargerWindupMax={out['maxConcurrentChargerWindups']} "
            f"{' '.join(support_parts) if support_parts else '-'} "
            f"{' '.join(siege_parts) if siege_parts else '-'}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
