#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import heapq
import json
import math
from pathlib import Path

import yaml

MASK = 0xFFFFFFFF
FNV = 2166136261
PRIME = 16777619
ZERO = 0x6D2B79F5
BASE = {
    "NORMAL": 100,
    "GOOD": 140,
    "PERFECT": 200,
    "HEAVY": 180,
    "HEAVY+": 230,
    "GREAT": 300,
    "SUPER": 400,
    "CRITICAL": 600,
}
CLASSES = ("knight", "rogue", "tank", "archer", "mage")
MILESTONES = (6, 11, 16, 21, 26, 31)
DEFAULT_SEEDS = (101, 211, 307)
T1_TYPES = ("GRUNT", "RUNNER", "BRUTE")
SAFETY_CAP_MS = 180000


class RunnerFidelityError(RuntimeError):
    pass


class RNG:
    def __init__(self, state: int):
        self.state = state & MASK or ZERO

    def unit(self) -> float:
        x = self.state
        x ^= (x << 13) & MASK
        x ^= x >> 17
        x ^= (x << 5) & MASK
        self.state = x & MASK
        return self.state / 4294967296.0


def seed_for(base: int, domain: str) -> int:
    h = FNV
    for b in f"{base}|{domain}".encode("utf-8"):
        h = ((h ^ b) * PRIME) & MASK
    return h or ZERO


def choose(dist: dict[str, float], u: float) -> str:
    acc = 0.0
    last = None
    for key, value in dist.items():
        last = key
        acc += float(value)
        if u < acc:
            return key
    if last is None:
        raise RunnerFidelityError("empty distribution")
    return last


def sha256_obj(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def combo_bonus(combo: int) -> float:
    if combo >= 30:
        return 0.15
    if combo >= 20:
        return 0.12
    if combo >= 10:
        return 0.08
    if combo >= 5:
        return 0.05
    return 0.0


def strong_tier(x: str, y: str) -> str:
    if x == y == "PERFECT":
        return "CRITICAL"
    weight = (2 if x == "PERFECT" else 1 if x == "GOOD" else 0) + (
        2 if y == "PERFECT" else 1 if y == "GOOD" else 0
    )
    if weight >= 3:
        return "SUPER"
    if weight == 2:
        return "GREAT"
    if weight == 1:
        return "HEAVY+"
    return "HEAVY"


def basic_knock(tier: str) -> float:
    if tier == "CRITICAL":
        return 0.047
    if tier in ("PERFECT", "SUPER"):
        return 0.024
    if tier in ("GOOD", "GREAT", "HEAVY+"):
        return 0.013
    return 0.006


def milestone(combo: int) -> int:
    if combo in (5, 10, 20, 30):
        return combo
    if combo > 30 and combo % 10 == 0:
        return combo
    return 0


def n3_budget(m: int) -> int:
    if m >= 30:
        return 210
    if m >= 20:
        return 150
    if m >= 10:
        return 90
    return 60


def n3_weights(cls: str, m: int) -> list[float]:
    if cls == "rogue":
        n = 5 if m >= 30 else 4 if m >= 20 else 3 if m >= 10 else 2
        return [1.0 / n] * n
    return {
        "knight": [0.67, 0.33],
        "tank": [0.60, 0.20, 0.20],
        "archer": [0.70, 0.30],
        "mage": [0.55, 0.15, 0.15, 0.15],
    }[cls]


def allocate_budget(budget: int, weights: list[float]) -> list[int]:
    exact = [budget * x for x in weights]
    out = [math.floor(x) for x in exact]
    remainder = budget - sum(out)
    order = sorted(range(len(weights)), key=lambda i: (-(exact[i] % 1), i))
    for k in range(remainder):
        out[order[k % len(order)]] += 1
    return out


def load_json(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_yaml(path: str | Path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def build_runtime(recipe_doc, p3_fixture, p4d2_base, p4d2_temporal):
    guards = recipe_doc["guards"]
    if recipe_doc.get("tier") != "T1":
        raise RunnerFidelityError("recipe tier is not T1")
    if guards.get("stageBoundary") != "STAGE_SETTLED":
        raise RunnerFidelityError("recipe stage boundary is not STAGE_SETTLED")
    if guards.get("midfieldPopIn") is not False:
        raise RunnerFidelityError("midfield pop-in must remain false")

    allowed = set(guards["allowedMonsters"])
    if allowed != set(T1_TYPES):
        raise RunnerFidelityError(f"unexpected T1 monster set: {sorted(allowed)}")

    monsters = {}
    for typ in T1_TYPES:
        anchor = p4d2_base["monsterAnchors"][typ]
        monsters[typ] = {
            "hp": float(anchor["hp"]),
            "armor": float(anchor["armor"]),
            "wallDamage": float(anchor["wall"]),
            "speed": float(anchor["speed"]),
            "knockResist": float(anchor["knockResist"]),
        }

    return {
        "actionIntervalMs": int(p3_fixture["testControls"]["actionIntervalMs"]),
        "timeStepMs": int(p3_fixture["testControls"]["timeStepMs"]),
        "centralModel": copy.deepcopy(p3_fixture["centralModel"]),
        "spawnX": float(guards["physicalSpawnX"]),
        "wallX": float(p3_fixture["world"]["wallX"]),
        "startingWallHp": float(p4d2_temporal["simulation"]["wallHp"]),
        "monsters": monsters,
        "lv31Centers": copy.deepcopy(p4d2_temporal["lv31TemporalCenters"]),
        "geometry": {
            "strictLineYTol": 0.06,
            "heavyLineYTol": 0.12,
            "nearbyX": 0.16,
            "nearbyY": 0.16,
            "mageBaseRadiusX": 0.105,
            "mageBaseRadiusY": 0.16,
        },
        "provisional": {
            "source": "P3/P4D2 diagnostic anchors; not production numerical authority",
            "passiveAttack": "OFF_NEUTRAL",
            "shop": "OFF_NEUTRAL",
        },
    }


def static_recipe_gate(recipe_doc):
    guards = recipe_doc["guards"]
    allowed_monsters = set(guards["allowedMonsters"])
    allowed_archetypes = set(guards["allowedArchetypes"])
    allowed_formations = set(guards["allowedFormations"])
    allowed_cadences = set(guards["allowedCadences"])
    expected = {5, 18, 20, 21, 22, 23, *range(39, 51)}
    errors = []
    stages = []
    for row in recipe_doc["recipes"]:
        stage = int(row["stage"])
        stages.append(stage)
        if row["archetype"] not in allowed_archetypes:
            errors.append(f"{row['id']}: archetype")
        if row["formation"] not in allowed_formations:
            errors.append(f"{row['id']}: formation")
        if row["cadence"] not in allowed_cadences:
            errors.append(f"{row['id']}: cadence")
        if abs(float(row["entryBaseX"]) - float(guards["physicalSpawnX"])) > 1e-12:
            errors.append(f"{row['id']}: entryBaseX")
        times = [int(s["tMs"]) for s in row["spawns"]]
        if times != sorted(times):
            errors.append(f"{row['id']}: nonmonotone spawn")
        for s in row["spawns"]:
            if s["type"] not in allowed_monsters:
                errors.append(f"{row['id']}: illegal monster {s['type']}")
    if len(stages) != len(set(stages)):
        errors.append("duplicate stage")
    if set(stages) != expected:
        errors.append(f"stage set mismatch got={sorted(stages)}")

    paired = {
        row["id"]: (int(row["stage"]), row["recipe"], int(row["skillMilestone"]), row["variantRule"])
        for row in recipe_doc.get("pairedDiagnostics", [])
    }
    expected_paired = {
        "RUNNER_TEACH_X_LV6": (5, "T1_S05_RUNNER_TEACH", 6, "IDENTICAL_RECIPE_ONLY_SKILL_STATE_DIFFERS"),
        "BRUTE_FIRST_MIX_X_LV16": (18, "T1_S18_BRUTE_FIRST_MIX", 16, "IDENTICAL_RECIPE_ONLY_SKILL_STATE_DIFFERS"),
    }
    if paired != expected_paired:
        errors.append(f"paired diagnostic contract mismatch: {paired}")

    sequential = {row["id"]: row for row in recipe_doc.get("sequentialSlices", [])}
    expected_sequences = {
        "STAGE20_23_GATE_AND_FIRST_HIGH_PRESSURE": [20, 21, 22, 23],
        "STAGE39_45_STAR_GATE_AND_LV31_ASCENSION": [39, 40, 41, 42, 43, 44, 45],
        "STAGE46_50_POST_LV31_MASTERY_AND_FINAL": [46, 47, 48, 49, 50],
    }
    for key, seq in expected_sequences.items():
        row = sequential.get(key)
        if not row or [int(x) for x in row.get("stages", [])] != seq:
            errors.append(f"{key}: sequential stage contract mismatch")
            continue
        if row.get("boundary") != "STAGE_SETTLED":
            errors.append(f"{key}: boundary mismatch")
        if set(row.get("persistentState", [])) != {"wallDeficit", "combo", "charge"}:
            errors.append(f"{key}: persistent state mismatch")
    reach = sequential.get("STAGE39_45_STAR_GATE_AND_LV31_ASCENSION", {}).get("lv31ReachVariants", [])
    if [int(x["activateBeforeStage"]) for x in reach] != [41, 43, 45]:
        errors.append("Lv31 reach variants mismatch")
    if sequential.get("STAGE46_50_POST_LV31_MASTERY_AND_FINAL", {}).get("lv31State") != "ACTIVE":
        errors.append("Stage46-50 Lv31 state mismatch")
    return errors


def max_density(times: list[int], window_ms: int) -> int:
    if not times:
        return 0
    best = 0
    for start in times:
        best = max(best, sum(1 for t in times if start <= t < start + window_ms))
    return best


def new_run(runtime, cls: str, base_seed: int, level: int, active_milestones: list[int]):
    jr = RNG(seed_for(base_seed, "JUDGMENT"))
    initial_state = choose(runtime["centralModel"]["initialState"], jr.unit())
    wall = float(runtime["startingWallHp"])
    return {
        "classId": cls,
        "baseSeed": int(base_seed),
        "level": int(level),
        "activeMilestones": sorted(int(x) for x in active_milestones),
        "baseMaxHp": wall,
        "baseHp": wall,
        "combo": 0,
        "comboPeak": 0,
        "charge": 0,
        "judgmentRng": jr.state,
        "judgmentState": initial_state,
        "combatProcRng": seed_for(base_seed, "COMBAT_PROC"),
        "expEligibleEvents": 0,
        "n3Triggers": 0,
        "ledger": [],
        "status": "ACTIVE",
    }


def has_skill(run, milestone_level: int) -> bool:
    return milestone_level in run["activeMilestones"]


def judge(run, runtime) -> str:
    rng = RNG(run["judgmentRng"])
    state_row = runtime["centralModel"]["states"][run["judgmentState"]]
    judgment = choose(state_row["judgmentDistribution"], rng.unit())
    run["judgmentState"] = choose(state_row["transitionAfterJudgment"], rng.unit())
    run["judgmentRng"] = rng.state
    run["expEligibleEvents"] += 1
    return judgment


def proc_roll(run) -> float:
    rng = RNG(run["combatProcRng"])
    value = rng.unit()
    run["combatProcRng"] = rng.state
    return value


def update_combo(run, judgment: str) -> list[int]:
    if judgment == "PERFECT":
        run["combo"] += 1
        run["comboPeak"] = max(run["comboPeak"], run["combo"])
        m = milestone(run["combo"])
        return [m] if m else []
    run["combo"] = 0
    return []


def alive(st):
    return [m for m in st["monsters"] if m["alive"]]


def front(st):
    living = alive(st)
    return min(living, key=lambda m: (m["x"], m["y"], m["id"])) if living else None


def target_by_id(st, target_id):
    for m in st["monsters"]:
        if m["id"] == target_id and m["alive"]:
            return m
    return None


def forward_line_targets(st, origin, max_n, y_tol):
    rows = [
        m
        for m in alive(st)
        if m["id"] != origin["id"]
        and m["x"] >= origin["x"] - 1e-9
        and abs(m["y"] - origin["y"]) <= y_tol
    ]
    rows.sort(key=lambda m: (m["x"], abs(m["y"] - origin["y"]), m["id"]))
    return rows[:max_n]


def nearby_targets(st, px, py, dx, dy, exclude_ids=(), max_n=None):
    excluded = set(exclude_ids)
    rows = [
        (
            math.hypot((m["x"] - px) / max(dx, 1e-9), (m["y"] - py) / max(dy, 1e-9)),
            m["id"],
            m,
        )
        for m in alive(st)
        if m["id"] not in excluded and abs(m["x"] - px) <= dx and abs(m["y"] - py) <= dy
    ]
    rows.sort(key=lambda x: (x[0], x[1]))
    mobs = [x[2] for x in rows]
    return mobs if max_n is None else mobs[:max_n]


def nearest_secondary(st, primary_id):
    rows = [m for m in alive(st) if m["id"] != primary_id]
    rows.sort(key=lambda m: (m["x"], m["y"], m["id"]))
    return rows[0] if rows else None


def schedule_event(st, due_ms: int, kind: str, payload: dict):
    st["queueSeq"] += 1
    heapq.heappush(st["queue"], (int(due_ms), st["queueSeq"], kind, copy.deepcopy(payload)))


def set_wall_shield(st, amount: float, until_ms: int, source: str):
    if source == "LV16" and st["wallShield"] > 0 and st["wallShieldSource"] == "LV31":
        return
    st["wallShield"] = float(amount)
    st["wallShieldUntilMs"] = int(until_ms)
    st["wallShieldSource"] = source


def apply_damage(
    run,
    st,
    runtime,
    target,
    raw: float,
    at_ms: int,
    tier: str,
    effect_id: str,
    *,
    armor_ignore: bool = False,
    knock_mul: float = 1.0,
    parent_action_id=None,
):
    if not target or not target["alive"]:
        return {"damage": 0.0, "killed": False, "knock": 0.0}
    spec = runtime["monsters"][target["type"]]
    before_x = float(target["x"])
    actual = max(1.0, round(float(raw) * (1.0 if armor_ignore else float(spec["armor"]))))
    actual = min(actual, float(target["hp"]))
    target["hp"] -= actual
    st["damage"] += actual

    dx = basic_knock(tier) * float(spec["knockResist"]) * float(knock_mul)
    if dx > 0:
        target["x"] = min(1.08, float(target["x"]) + dx)
    realized_knock = max(0.0, float(target["x"]) - before_x)
    st["control"]["knockbackDistance"] += realized_knock

    killed = target["hp"] <= 1e-9
    if killed:
        target["hp"] = 0.0
        target["alive"] = False
        st["kills"] += 1
        st["killsByType"][target["type"]] = st["killsByType"].get(target["type"], 0) + 1

    run["ledger"].append(
        {
            "stage": st["stage"],
            "atMs": int(at_ms),
            "actionId": st["actionSeq"],
            "parentActionId": parent_action_id,
            "effectId": effect_id,
            "targetId": target["id"],
            "raw": round(float(raw), 6),
            "finalDamage": round(float(actual), 6),
            "knockDistance": round(float(realized_knock), 9),
        }
    )
    return {"damage": actual, "killed": killed, "knock": realized_knock}


def execute_n3(run, st, runtime, combo_milestone: int, at_ms: int, primary):
    if not primary or not primary["alive"]:
        primary = front(st)
    if not primary:
        return
    run["n3Triggers"] += 1
    parts = allocate_budget(n3_budget(combo_milestone), n3_weights(run["classId"], combo_milestone))
    cls = run["classId"]
    primary_id = primary["id"]

    if cls == "rogue":
        for i, raw in enumerate(parts):
            schedule_event(
                st,
                at_ms + i * 55,
                "N3_ROGUE",
                {"raw": raw, "targetId": primary_id, "rootPrimaryId": primary_id},
            )
        return

    tank_mul = 1.3 if cls == "tank" and has_skill(run, 6) else 1.0
    apply_damage(
        run,
        st,
        runtime,
        primary,
        parts[0],
        at_ms,
        "NORMAL",
        "N3_FIXED_BUDGET",
        knock_mul=tank_mul,
        parent_action_id=st["actionSeq"],
    )

    if cls in ("knight", "archer"):
        secondaries = forward_line_targets(st, primary, 1, runtime["geometry"]["strictLineYTol"])
    elif cls == "tank":
        secondaries = nearby_targets(
            st,
            primary["x"],
            primary["y"],
            0.13,
            0.16,
            exclude_ids=(primary_id,),
            max_n=2,
        )
    else:
        secondaries = nearby_targets(
            st,
            primary["x"],
            primary["y"],
            0.12,
            0.17,
            exclude_ids=(primary_id,),
            max_n=3,
        )
    for target, raw in zip(secondaries, parts[1:]):
        apply_damage(
            run,
            st,
            runtime,
            target,
            raw,
            at_ms,
            "NORMAL",
            "N3_FIXED_BUDGET",
            knock_mul=tank_mul if cls == "tank" else 1.0,
            parent_action_id=st["actionSeq"],
        )


def process_event(run, st, runtime, event):
    due_ms, _, kind, p = event
    if kind in ("ROGUE_FOLLOWUP", "N3_ROGUE", "ROGUE_LV31_DAGGER"):
        target = target_by_id(st, p.get("targetId"))
        if not target:
            target = front(st)
        if target:
            apply_damage(
                run,
                st,
                runtime,
                target,
                p["raw"],
                due_ms,
                "SKILL" if kind != "N3_ROGUE" else "NORMAL",
                p.get("effectId", kind),
                parent_action_id=p.get("parentActionId"),
            )
        return

    if kind == "ROGUE_CHAIN":
        root_primary_id = p["rootPrimaryId"]
        target = target_by_id(st, p["targetId"])
        if not target or target["id"] == root_primary_id:
            target = nearest_secondary(st, root_primary_id)
        if target:
            apply_damage(
                run,
                st,
                runtime,
                target,
                p["raw"],
                due_ms,
                "SKILL",
                "LV26_ROGUE_CHAIN_THROW",
                parent_action_id=p["parentActionId"],
            )
        return

    if kind == "MAGE_RESONANCE":
        px, py = p["center"]
        targets = nearby_targets(
            st,
            px,
            py,
            p["radiusX"],
            p["radiusY"],
            exclude_ids=(p["excludeId"],),
            max_n=4,
        )
        for target in targets:
            apply_damage(
                run,
                st,
                runtime,
                target,
                p["raw"],
                due_ms,
                "SKILL",
                "LV16_MAGE_RESONANCE",
                parent_action_id=p["parentActionId"],
            )
        return

    if kind == "KNIGHT_LV31_WAVE":
        primary = front(st)
        if not primary:
            return
        targets = [primary] + forward_line_targets(
            st,
            primary,
            3,
            runtime["geometry"]["heavyLineYTol"],
        )
        for idx, target in enumerate(targets):
            apply_damage(
                run,
                st,
                runtime,
                target,
                p["raw"],
                due_ms,
                "CRITICAL",
                "LV31_KNIGHT_SECOND_WAVE",
                knock_mul=1.20 * (1.0 + 0.15 * idx),
                parent_action_id=p["parentActionId"],
            )
        return

    if kind == "MAGE_LV31_BLAST":
        px, py = p["center"]
        targets = nearby_targets(
            st,
            px,
            py,
            p["radiusX"],
            p["radiusY"],
            exclude_ids=(),
            max_n=None,
        )
        for target in list(targets):
            apply_damage(
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
            hit_ids = set(p.get("alreadyHitIds", []))
            chain = [m for m in alive(st) if m["id"] not in hit_ids]
            chain.sort(key=lambda m: (m["x"], m["y"], m["id"]))
            for target in chain[:2]:
                apply_damage(
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
        return

    raise RunnerFidelityError(f"unknown queued event {kind}")
