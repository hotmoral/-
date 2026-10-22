#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


def simulate(recipe, kin, combat, raw_dps):
    world = kin["world"]
    move = kin["monsters"]
    stats = combat["monsters"]
    offsets = kin.get("formationXOffsets", {}).get(recipe["formation"], {})
    dt = int(world["timeStepMs"])
    horizon = int(world["horizonMs"])
    spawn_x = float(world["spawnX"])
    wall_x = float(world["wallX"])

    specs = sorted(recipe["spawns"], key=lambda x: int(x["tMs"]))
    monsters = []
    idx = 0
    next_id = 1
    t = 0

    max_active = 0
    max_charger_windups = 0
    supporter_alive_ms = 0
    aura_any_ms = 0
    screened_aura_ms = 0
    siege_shots = 0
    first_siege_shot_ms = None
    wall_damage = 0
    splitter_children = 0
    kills = Counter()
    wall_hits = Counter()

    def type_stats(typ):
        if typ == "SPLITTER_CHILD":
            s = stats["SPLITTER"]
            return {"hp": s["childHp"], "armor": s["childArmor"], "wallDamage": s["childWallDamage"]}
        return stats[typ]

    def speed_for(typ):
        if typ == "SPLITTER_CHILD":
            return float(move["SPLITTER"]["childSpeed"])
        return float(move[typ]["speed"])

    def y_at(m, at):
        if m["type"] != "FLYER":
            return m["y0"]
        age = max(0, at - m["spawnMs"]) / 1000.0
        d = move["FLYER"]
        return m["y0"] + float(d["oscillationAmplitude"]) * math.sin(age * float(d["oscillationOmega"]))

    while t <= horizon:
        while idx < len(specs) and int(specs[idx]["tMs"]) <= t:
            s = specs[idx]
            typ = s["type"]
            st = type_stats(typ)
            monsters.append({
                "id": next_id,
                "type": typ,
                "x": spawn_x + float(offsets.get(typ, 0.0)),
                "y0": float(s["y"]),
                "spawnMs": int(s["tMs"]),
                "phase": "advance",
                "phaseAt": int(s["tMs"]),
                "hp": float(st["hp"]),
                "alive": True,
                "generation": 0,
            })
            next_id += 1
            idx += 1

        alive = [m for m in monsters if m["alive"]]
        max_active = max(max_active, len(alive))
        supporters = [m for m in alive if m["type"] == "SUPPORTER"]

        aura_sources = defaultdict(list)
        for target in alive:
            if target["type"] == "SUPPORTER":
                continue
            for source in supporters:
                dist = math.hypot(target["x"] - source["x"], y_at(target, t) - y_at(source, t))
                if dist <= float(move["SUPPORTER"]["auraRadius"]) + 1e-12:
                    aura_sources[target["id"]].append(source["id"])

        front = min(alive, key=lambda m: (m["x"], m["id"])) if alive else None

        for source in supporters:
            supporter_alive_ms += dt
            targets = [m for m in alive if m["id"] != source["id"] and source["id"] in aura_sources.get(m["id"], [])]
            if targets:
                aura_any_ms += dt
                if front and front["id"] != source["id"]:
                    screened_aura_ms += dt

        for m in alive:
            if m["type"] == "CHARGER":
                d = move["CHARGER"]
                if m["phase"] == "advance" and m["x"] <= float(d["triggerX"]):
                    m["phase"] = "windup"
                    m["phaseAt"] = t
                elif m["phase"] == "windup" and t - m["phaseAt"] >= int(d["windupMs"]):
                    m["phase"] = "charge"
                    m["phaseAt"] = t

            elif m["type"] == "SIEGER":
                d = move["SIEGER"]
                if m["phase"] == "advance" and m["x"] <= float(d["standoffX"]):
                    m["x"] = float(d["standoffX"])
                    m["phase"] = "windup"
                    m["phaseAt"] = t
                elif m["phase"] == "windup" and t - m["phaseAt"] >= int(d["windupMs"]):
                    m["phase"] = "cooldown"
                    m["phaseAt"] = t
                    siege_shots += 1
                    if first_siege_shot_ms is None:
                        first_siege_shot_ms = t
                    wall_damage += int(stats["SIEGER"]["shotWallDamage"])
                elif m["phase"] == "cooldown" and t - m["phaseAt"] >= int(d["repeatMs"] - d["windupMs"]):
                    m["phase"] = "windup"
                    m["phaseAt"] = t

        max_charger_windups = max(
            max_charger_windups,
            sum(1 for m in alive if m["type"] == "CHARGER" and m["phase"] == "windup"),
        )

        if front and front["alive"]:
            st = type_stats(front["type"])
            front["hp"] -= float(raw_dps) * float(st["armor"]) * (dt / 1000.0)
            if front["hp"] <= 0:
                front["alive"] = False
                kills[front["type"]] += 1
                if front["type"] == "SPLITTER" and front.get("generation", 0) == 0:
                    for dy in combat["combatModel"]["childOffsetsY"]:
                        child_st = type_stats("SPLITTER_CHILD")
                        monsters.append({
                            "id": next_id,
                            "type": "SPLITTER_CHILD",
                            "x": front["x"],
                            "y0": front["y0"] + float(dy),
                            "spawnMs": t,
                            "phase": "advance",
                            "phaseAt": t,
                            "hp": float(child_st["hp"]),
                            "alive": True,
                            "generation": 1,
                        })
                        next_id += 1
                        splitter_children += 1

        alive = [m for m in monsters if m["alive"]]
        for m in alive:
            typ = m["type"]
            if typ == "SIEGER" and m["phase"] != "advance":
                continue
            if typ == "CHARGER":
                d = move["CHARGER"]
                speed = 0.0 if m["phase"] == "windup" else float(d["chargeSpeed"] if m["phase"] == "charge" else d["speed"])
            else:
                speed = speed_for(typ)
            if typ != "SUPPORTER" and aura_sources.get(m["id"]):
                speed *= float(move["SUPPORTER"]["auraSpeedMultiplier"])
            m["x"] -= speed * (dt / 1000.0)

        for m in alive:
            if not m["alive"] or m["type"] == "SIEGER":
                continue
            if m["x"] <= wall_x:
                m["alive"] = False
                wall_hits[m["type"]] += 1
                wall_damage += int(type_stats(m["type"])["wallDamage"])

        if idx >= len(specs) and not [m for m in monsters if m["alive"]]:
            break
        t += dt

    return {
        "endMs": t,
        "maxActive": max_active,
        "maxConcurrentChargerWindups": max_charger_windups,
        "supporterAuraSeconds": aura_any_ms / 1000.0,
        "supporterScreenedAuraSeconds": screened_aura_ms / 1000.0,
        "siegeShots": siege_shots,
        "firstSiegeShotMs": first_siege_shot_ms,
        "wallDamage": wall_damage,
        "splitterChildren": splitter_children,
        "kills": dict(kills),
        "wallHits": dict(wall_hits),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("recipes", type=Path)
    parser.add_argument("kinematic_anchor", type=Path)
    parser.add_argument("combat_anchor", type=Path)
    args = parser.parse_args()

    recipes = yaml.safe_load(args.recipes.read_text(encoding="utf-8"))
    kin = yaml.safe_load(args.kinematic_anchor.read_text(encoding="utf-8"))
    combat = yaml.safe_load(args.combat_anchor.read_text(encoding="utf-8"))

    sweep = combat["rawDpsSweep"]
    print(f"SIMULATION=FRONTMOST_DPS_SENSITIVITY recipes={len(recipes.get('recipes', []))} sweep={sweep}")
    for recipe in recipes.get("recipes", []):
        for dps in sweep:
            out = simulate(recipe, kin, combat, dps)
            first = "-" if out["firstSiegeShotMs"] is None else f"{out['firstSiegeShotMs']/1000:.2f}s"
            print(
                f"{recipe['id']} dps={dps} end={out['endMs']/1000:.2f}s maxActive={out['maxActive']} "
                f"windupMax={out['maxConcurrentChargerWindups']} splitChildren={out['splitterChildren']} "
                f"aura={out['supporterAuraSeconds']:.2f}s screenedAura={out['supporterScreenedAuraSeconds']:.2f}s "
                f"siegeShots={out['siegeShots']} firstSiegeShot={first} wallDamage={out['wallDamage']}"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
