#!/usr/bin/env python3
from __future__ import annotations

import argparse
import heapq
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

CLASSES = ["knight", "rogue", "tank", "archer", "mage"]
BASE_DAMAGE = {
    "NORMAL": 100,
    "GOOD": 140,
    "PERFECT": 200,
    "HEAVY": 180,
    "HEAVY+": 230,
    "GREAT": 300,
    "SUPER": 400,
    "CRITICAL": 600,
}
SLOT_Y = 0.30  # solo/player-slot-1 probe


def combo_bonus(combo: int) -> float:
    return .15 if combo >= 30 else .12 if combo >= 20 else .08 if combo >= 10 else .05 if combo >= 5 else 0.0


def strong_tier(x: str, y: str) -> str:
    if x == "PERFECT" and y == "PERFECT":
        return "CRITICAL"
    w = (2 if x == "PERFECT" else 1 if x == "GOOD" else 0) + (2 if y == "PERFECT" else 1 if y == "GOOD" else 0)
    return "SUPER" if w >= 3 else "GREAT" if w == 2 else "HEAVY+" if w == 1 else "HEAVY"


def tier_knock(tier: str) -> float:
    if tier == "CRITICAL":
        return .047
    if tier in ("PERFECT", "SUPER"):
        return .024
    if tier in ("GOOD", "GREAT", "HEAVY+"):
        return .013
    return .006


def milestone_for(combo: int) -> int:
    if combo in (5, 10, 20, 30):
        return combo
    if combo > 30 and combo % 10 == 0:
        return combo
    return 0


def n3_budget(milestone: int) -> int:
    return 210 if milestone >= 30 else 150 if milestone >= 20 else 90 if milestone >= 10 else 60


def n3_weights(cls: str, milestone: int) -> list[float]:
    if cls == "rogue":
        n = 5 if milestone >= 30 else 4 if milestone >= 20 else 3 if milestone >= 10 else 2
        return [1 / n] * n
    if cls == "knight":
        return [.67, .33]
    if cls == "tank":
        return [.60, .20, .20]
    if cls == "archer":
        return [.70, .30]
    return [.55, .15, .15, .15]


def allocate_budget(budget: int, weights: list[float]) -> list[int]:
    exact = [budget * w for w in weights]
    out = [math.floor(x) for x in exact]
    rem = budget - sum(out)
    order = sorted(range(len(weights)), key=lambda i: (-(exact[i] - math.floor(exact[i])), i))
    for k in range(rem):
        out[order[k % len(order)]] += 1
    return out


def judge_stream(perfect_streak: int, break_judge: str):
    i = 0
    while True:
        yield break_judge if i % (perfect_streak + 1) == perfect_streak else "PERFECT"
        i += 1


@dataclass
class Monster:
    id: int
    type: str
    x: float
    y0: float
    spawn_ms: int
    hp: float
    phase: str = "advance"
    phase_at: int = 0
    alive: bool = True
    generation: int = 0
    rearm_until: int = 0
    parent_id: int | None = None


def simulate(recipe, kin, combat, trace, cls: str, power_mode: dict) -> dict:
    world = kin["world"]
    move = kin["monsters"]
    stats = combat["monsters"]
    formation_offsets = kin.get("formationXOffsets", {}).get(recipe["formation"], {})
    dt = int(world.get("timeStepMs", 10))
    # 55 ms Rogue queue is authoritative; use a divisor of 55 for exact queue sampling.
    if 55 % dt != 0:
        dt = 5
    horizon = int(world.get("horizonMs", 30000))
    spawn_x = float(recipe.get("entryBaseX", world["spawnX"]))
    wall_x = float(world["wallX"])
    recipe_offsets = recipe.get("entryXOffsetByType", {})
    lv6 = bool(power_mode.get("lv6Enabled", False))
    n3_enabled = bool(power_mode.get("n3Enabled", True))

    specs = sorted(recipe["spawns"], key=lambda x: int(x["tMs"]))
    monsters: list[Monster] = []
    idx = 0
    next_id = 1
    qseq = 0
    queue: list[tuple[int, int, str, dict]] = []
    judges = judge_stream(int(trace["perfectStreakJudges"]), str(trace.get("breakJudge", "GOOD")))
    charge = 0
    combo = 0
    combo_peak = 0
    next_action = 0
    last_front_id = None
    windup_seen: set[int] = set()

    metrics = {
        "actions": 0,
        "comboPeak": 0,
        "firstKillMs": None,
        "killOrder": [],
        "frontReorders": 0,
        "wallDamage": 0,
        "peakActive": 0,
        "chargerWindups": 0,
        "chargerCompleted": 0,
        "chargerInterrupted": 0,
        "chargerErasedBeforeWindup": 0,
        "splitterParentsKilled": 0,
        "splitterChildren": 0,
        "splitterChildWallHits": 0,
        "supportAuraMs": 0,
        "supportScreenedAuraMs": 0,
        "siegeShots": 0,
        "siegeScreenedShots": 0,
        "firstSiegeShotMs": None,
        "flyerSkillHits": 0,
        "n3Triggers": 0,
        "lv6SkillHits": 0,
        "damage": 0,
        "clearMs": None,
    }

    def type_stats(typ: str) -> dict:
        if typ == "SPLITTER_CHILD":
            d = stats["SPLITTER"]
            return {"hp": d["childHp"], "armor": d["childArmor"], "wallDamage": d["childWallDamage"]}
        return stats[typ]

    def speed_for(typ: str) -> float:
        if typ == "SPLITTER_CHILD":
            return float(move["SPLITTER"]["childSpeed"])
        return float(move[typ]["speed"])

    def knock_resist(typ: str) -> float:
        if typ == "SPLITTER_CHILD":
            return .82
        return {
            "GRUNT": .85,
            "RUNNER": 1.00,
            "BRUTE": .38,
            "SHIELD": .62,
            "FLYER": .90,
            "CHARGER": .80,
            "SPLITTER": .82,
            "SUPPORTER": .90,
            "SIEGER": .55,
        }[typ]

    def size_for(typ: str) -> float:
        return {
            "GRUNT": 1.00,
            "RUNNER": .70,
            "BRUTE": 1.34,
            "SHIELD": 1.08,
            "FLYER": .78,
            "CHARGER": 1.00,
            "SPLITTER": 1.00,
            "SPLITTER_CHILD": .62,
            "SUPPORTER": 1.00,
            "SIEGER": 1.00,
        }[typ]

    def y_at(m: Monster, at: int) -> float:
        if m.type != "FLYER":
            return m.y0
        age = max(0, at - m.spawn_ms) / 1000.0
        d = move["FLYER"]
        return m.y0 + float(d["oscillationAmplitude"]) * math.sin(age * float(d["oscillationOmega"]))

    def point(m: Monster, at: int) -> dict:
        return {"id": m.id, "type": m.type, "x": m.x, "y": y_at(m, at), "size": size_for(m.type)}

    def alive_list() -> list[Monster]:
        return [m for m in monsters if m.alive]

    def frontmost() -> Monster | None:
        alive = alive_list()
        return min(alive, key=lambda m: (m.x, m.id)) if alive else None

    def schedule(due: int, kind: str, payload: dict):
        nonlocal qseq
        qseq += 1
        heapq.heappush(queue, (due, qseq, kind, payload))

    def kill(m: Monster, at: int):
        nonlocal next_id
        if not m.alive:
            return
        m.alive = False
        metrics["killOrder"].append({"atMs": at, "type": m.type, "id": m.id})
        if metrics["firstKillMs"] is None:
            metrics["firstKillMs"] = at
        if m.type == "CHARGER" and m.id not in windup_seen:
            metrics["chargerErasedBeforeWindup"] += 1
        if m.type == "SPLITTER" and m.generation == 0:
            metrics["splitterParentsKilled"] += 1
            for dy in combat["combatModel"]["childOffsetsY"]:
                d = type_stats("SPLITTER_CHILD")
                monsters.append(Monster(
                    id=next_id,
                    type="SPLITTER_CHILD",
                    x=m.x,
                    y0=m.y0 + float(dy),
                    spawn_ms=at,
                    hp=float(d["hp"]),
                    phase_at=at,
                    generation=1,
                    parent_id=m.id,
                ))
                next_id += 1
                metrics["splitterChildren"] += 1

    def apply_damage(m: Monster | None, raw: float, at: int, tier: str, tank_extra: bool = False):
        if m is None or not m.alive:
            return
        st = type_stats(m.type)
        actual = max(1, round(float(raw) * float(st["armor"])))
        m.hp -= actual
        metrics["damage"] += actual
        push = tier_knock(tier) * knock_resist(m.type)
        if tank_extra:
            push *= 1.30
        m.x = min(.985, m.x + push)
        if m.hp <= 0:
            kill(m, at)
            return
        if m.type == "CHARGER" and m.phase == "windup" and push > 0:
            metrics["chargerInterrupted"] += 1
            m.phase = "advance"
            m.phase_at = at
            m.rearm_until = at + int(move["CHARGER"]["rearmMs"])
        if m.type == "SIEGER" and m.phase in ("windup", "cooldown") and push > 0 and m.x > float(move["SIEGER"]["standoffX"]) + 1e-9:
            m.phase = "advance"
            m.phase_at = at

    def archer_targets(primary: Monster, at: int, max_count: int) -> list[Monster]:
        a = {"x": .105, "y": SLOT_Y}
        p = point(primary, at)
        b = {"x": p["x"], "y": p["y"] - .035 * p["size"]}
        dx, dy = b["x"] - a["x"], b["y"] - a["y"]
        len2 = dx * dx + dy * dy or 1.0
        out = []
        for m in alive_list():
            if m.id == primary.id:
                continue
            q = point(m, at)
            qy = q["y"] - .035 * q["size"]
            t = ((q["x"] - a["x"]) * dx + (qy - a["y"]) * dy) / len2
            if t <= 1.025:
                continue
            px, py = a["x"] + t * dx, a["y"] + t * dy
            dist = math.hypot(q["x"] - px, qy - py)
            if dist <= .042 * q["size"]:
                out.append((t, m.id, m))
        out.sort()
        return [x[2] for x in out[:max_count]]

    def mage_targets(primary: Monster, at: int, dx_max: float, dy_max: float, max_count: int) -> list[Monster]:
        p = point(primary, at)
        out = []
        for m in alive_list():
            if m.id == primary.id:
                continue
            q = point(m, at)
            if abs(q["x"] - p["x"]) < dx_max and abs(q["y"] - p["y"]) < dy_max:
                out.append((math.hypot(q["x"] - p["x"], q["y"] - p["y"]), m.id, m))
        out.sort()
        return [x[2] for x in out[:max_count]]

    def knight_n3_secondary(primary: Monster, at: int) -> Monster | None:
        p = point(primary, at)
        out = []
        for m in alive_list():
            if m.id == primary.id:
                continue
            q = point(m, at)
            if q["x"] >= p["x"] and q["x"] - p["x"] <= .20 and abs(q["y"] - p["y"]) <= .13:
                out.append((q["x"], abs(q["y"] - p["y"]), m.id, m))
        out.sort()
        return out[0][3] if out else None

    def tank_n3_secondaries(primary: Monster, at: int) -> list[Monster]:
        p = point(primary, at)
        out = []
        for m in alive_list():
            if m.id == primary.id:
                continue
            q = point(m, at)
            if abs(q["x"] - p["x"]) <= .13 and abs(q["y"] - p["y"]) <= .16:
                out.append((math.hypot(q["x"] - p["x"], q["y"] - p["y"]), m.id, m))
        out.sort()
        return [x[2] for x in out[:2]]

    def trigger_n3(milestone: int, at: int):
        if not n3_enabled:
            return
        primary = frontmost()
        if primary is None:
            return
        metrics["n3Triggers"] += 1
        parts = allocate_budget(n3_budget(milestone), n3_weights(cls, milestone))
        if cls == "rogue":
            for i, raw in enumerate(parts):
                schedule(at + i * 55, "n3-rogue", {"targetId": primary.id, "raw": raw})
            return
        apply_damage(primary, parts[0], at, "NORMAL", tank_extra=(cls == "tank" and lv6))
        if cls == "knight" and len(parts) > 1:
            q = knight_n3_secondary(primary, at)
            if q:
                apply_damage(q, parts[1], at, "NORMAL")
        elif cls == "tank":
            for q, raw in zip(tank_n3_secondaries(primary, at), parts[1:]):
                apply_damage(q, raw, at, "NORMAL", tank_extra=lv6)
        elif cls == "archer" and len(parts) > 1:
            qs = archer_targets(primary, at, 1)
            if qs:
                apply_damage(qs[0], parts[1], at, "NORMAL")
        elif cls == "mage":
            for q, raw in zip(mage_targets(primary, at, .12, .17, 3), parts[1:]):
                apply_damage(q, raw, at, "NORMAL")

    def update_combo(judge: str) -> list[int]:
        nonlocal combo, combo_peak
        out = []
        if judge == "PERFECT":
            combo += 1
            combo_peak = max(combo_peak, combo)
            m = milestone_for(combo)
            if m:
                out.append(m)
        else:
            combo = 0
        return out

    def do_action(at: int):
        nonlocal charge, next_action
        primary = frontmost()
        if primary is None:
            next_action = at + 50
            return
        metrics["actions"] += 1
        heavy = charge >= 3
        x = next(judges)
        y = next(judges) if heavy else None
        milestones = []
        if heavy:
            milestones += update_combo(x)
            predicted_combo = combo + 1 if y == "PERFECT" else 0
            tier = strong_tier(x, y or "NORMAL")
            milestones += update_combo(y or "NORMAL")
        else:
            predicted_combo = combo + 1 if x == "PERFECT" else 0
            tier = x
            milestones += update_combo(x)

        raw = BASE_DAMAGE[tier] * (1 + combo_bonus(predicted_combo))
        if lv6 and cls == "knight":
            raw *= 1.12
        raw = max(1, round(raw))
        primary_point_id = primary.id
        apply_damage(primary, raw, at, tier, tank_extra=(lv6 and cls == "tank"))

        if lv6:
            # Nonrecursive v0.36 class-skill layer.
            primary_ref = next((m for m in monsters if m.id == primary_point_id), primary)
            if cls == "rogue":
                schedule(at + 55, "lv6-rogue", {"targetId": primary_point_id, "raw": max(1, round(raw * .55))})
            elif cls == "archer":
                for q in archer_targets(primary_ref, at, 2):
                    apply_damage(q, max(1, round(raw * .52)), at, tier)
                    metrics["lv6SkillHits"] += 1
                    if q.type == "FLYER":
                        metrics["flyerSkillHits"] += 1
            elif cls == "mage":
                for q in mage_targets(primary_ref, at, .105, .16, 3):
                    apply_damage(q, max(1, round(raw * .50)), at, "SKILL")
                    metrics["lv6SkillHits"] += 1
                    if q.type == "FLYER":
                        metrics["flyerSkillHits"] += 1

        # v0.39 N3 is triggered after the base action.
        for milestone in milestones:
            trigger_n3(milestone, at)

        charge = 0 if heavy else min(3, charge + 1)
        next_action = at + int(trace["actionIntervalMs"])

    at = 0
    while at <= horizon:
        while idx < len(specs) and int(specs[idx]["tMs"]) <= at:
            spec = specs[idx]
            typ = spec["type"]
            st = type_stats(typ)
            x_offset = float(formation_offsets.get(typ, 0.0)) + float(recipe_offsets.get(typ, 0.0))
            monsters.append(Monster(
                id=next_id,
                type=typ,
                x=spawn_x + x_offset,
                y0=float(spec["y"]),
                spawn_ms=int(spec["tMs"]),
                hp=float(st["hp"]),
                phase_at=int(spec["tMs"]),
            ))
            next_id += 1
            idx += 1

        alive = alive_list()
        metrics["peakActive"] = max(metrics["peakActive"], len(alive))
        supporters = [m for m in alive if m.type == "SUPPORTER"]
        aura_sources = defaultdict(list)
        for target in alive:
            if target.type == "SUPPORTER":
                continue
            for source in supporters:
                if math.hypot(target.x - source.x, y_at(target, at) - y_at(source, at)) <= float(move["SUPPORTER"]["auraRadius"]) + 1e-12:
                    aura_sources[target.id].append(source.id)

        front = frontmost()
        if front and front.id != last_front_id:
            if last_front_id is not None:
                metrics["frontReorders"] += 1
            last_front_id = front.id

        for source in supporters:
            targets = [m for m in alive if m.id != source.id and source.id in aura_sources.get(m.id, [])]
            if targets:
                metrics["supportAuraMs"] += dt
                if front and front.id != source.id:
                    metrics["supportScreenedAuraMs"] += dt

        for m in list(alive):
            if not m.alive:
                continue
            if m.type == "CHARGER":
                d = move["CHARGER"]
                if m.phase == "advance" and m.x <= float(d["triggerX"]) and at >= m.rearm_until:
                    m.phase = "windup"
                    m.phase_at = at
                    windup_seen.add(m.id)
                    metrics["chargerWindups"] += 1
                elif m.phase == "windup" and at - m.phase_at >= int(d["windupMs"]):
                    m.phase = "charge"
                    m.phase_at = at
                    metrics["chargerCompleted"] += 1
            elif m.type == "SIEGER":
                d = move["SIEGER"]
                if m.phase == "advance" and m.x <= float(d["standoffX"]):
                    m.x = float(d["standoffX"])
                    m.phase = "windup"
                    m.phase_at = at
                elif m.phase == "windup" and at - m.phase_at >= int(d["windupMs"]):
                    fr = frontmost()
                    metrics["siegeShots"] += 1
                    if metrics["firstSiegeShotMs"] is None:
                        metrics["firstSiegeShotMs"] = at
                    if fr and fr.id != m.id:
                        metrics["siegeScreenedShots"] += 1
                    metrics["wallDamage"] += int(stats["SIEGER"]["shotWallDamage"])
                    m.phase = "cooldown"
                    m.phase_at = at
                elif m.phase == "cooldown" and at - m.phase_at >= int(d["repeatMs"] - d["windupMs"]):
                    m.phase = "windup"
                    m.phase_at = at

        while queue and queue[0][0] <= at:
            due, _, kind, payload = heapq.heappop(queue)
            target = next((m for m in monsters if m.id == payload["targetId"] and m.alive), None) or frontmost()
            if target is None:
                continue
            if kind == "lv6-rogue":
                apply_damage(target, payload["raw"], due, "SKILL")
                metrics["lv6SkillHits"] += 1
                if target.type == "FLYER":
                    metrics["flyerSkillHits"] += 1
            elif kind == "n3-rogue":
                apply_damage(target, payload["raw"], due, "NORMAL")

        if at >= next_action:
            do_action(at)

        alive = alive_list()
        for m in alive:
            if m.type == "SIEGER" and m.phase != "advance":
                continue
            if m.type == "CHARGER":
                d = move["CHARGER"]
                speed = 0.0 if m.phase == "windup" else float(d["chargeSpeed"] if m.phase == "charge" else d["speed"])
            else:
                speed = speed_for(m.type)
            if m.type != "SUPPORTER" and aura_sources.get(m.id):
                speed *= float(move["SUPPORTER"]["auraSpeedMultiplier"])
            m.x -= speed * (dt / 1000.0)

        for m in list(alive_list()):
            if m.type == "SIEGER":
                continue
            if m.x <= wall_x:
                m.alive = False
                metrics["wallDamage"] += int(type_stats(m.type)["wallDamage"])
                if m.type == "SPLITTER_CHILD":
                    metrics["splitterChildWallHits"] += 1

        if idx >= len(specs) and not alive_list() and not queue:
            metrics["clearMs"] = at
            break
        at += dt

    metrics["comboPeak"] = combo_peak
    metrics["endMs"] = at
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("recipes", type=Path)
    parser.add_argument("kinematic_anchor", type=Path)
    parser.add_argument("combat_anchor", type=Path)
    parser.add_argument("trace_bracket", type=Path)
    parser.add_argument("--recipe", action="append", default=[])
    parser.add_argument("--profile", action="append", default=[])
    parser.add_argument("--power-mode", default="CURRENT_AUTHORITY_LV6")
    args = parser.parse_args()

    recipe_data = yaml.safe_load(args.recipes.read_text(encoding="utf-8"))
    kin = yaml.safe_load(args.kinematic_anchor.read_text(encoding="utf-8"))
    combat = yaml.safe_load(args.combat_anchor.read_text(encoding="utf-8"))
    traces = yaml.safe_load(args.trace_bracket.read_text(encoding="utf-8"))
    power_mode = traces["powerModes"][args.power_mode]

    wanted_recipes = set(args.recipe)
    wanted_profiles = set(args.profile)
    selected_recipes = [r for r in recipe_data["recipes"] if not wanted_recipes or r["id"] in wanted_recipes]
    selected_profiles = [(k, v) for k, v in traces["profiles"].items() if not wanted_profiles or k in wanted_profiles]

    print(json.dumps({
        "simulation": "CLASS_AWARE_LAYER_A",
        "recipeVersion": recipe_data.get("version"),
        "traceVersion": traces.get("version"),
        "powerMode": args.power_mode,
        "warning": "trace profiles are calibration brackets, not fitted SKILLED_V2",
    }, ensure_ascii=False))

    for recipe in selected_recipes:
        for profile_id, trace in selected_profiles:
            for cls in CLASSES:
                out = simulate(recipe, kin, combat, trace, cls, power_mode)
                print(json.dumps({
                    "recipeId": recipe["id"],
                    "tier": recipe["tier"],
                    "archetype": recipe["archetype"],
                    "profile": profile_id,
                    "classId": cls,
                    **out,
                }, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
