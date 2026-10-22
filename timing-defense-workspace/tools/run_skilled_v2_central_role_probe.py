#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter, defaultdict
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

import simulate_class_aware_role_metrics_v0_2 as sim
from validate_skilled_v2_central_sequence import RNG, choose

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "legacy-game-structure" / "data"

DEFAULT_RECIPES = DATA / "model_a_representative_recipes_v0_1.yaml"
DEFAULT_KINEMATICS = DATA / "model_a_kinematic_anchor_v0_1.yaml"
DEFAULT_COMBAT = DATA / "model_a_combat_sensitivity_anchor_v0_1.yaml"
DEFAULT_LEGACY_TRACE = DATA / "model_a_class_action_trace_bracket_v0_1.yaml"
DEFAULT_CENTRAL = DATA / "skilled_v2_central_sequence_candidate_v0_1.yaml"
DEFAULT_OVERLAYS = [
    DATA / "model_a_critical_role_expression_candidates_v0_1.yaml",
    DATA / "model_a_additional10_role_expression_candidates_v0_1.yaml",
]
DEFAULT_SEEDS = [101, 211, 307]


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def overlay_recipes(data: dict) -> dict[str, dict]:
    return data.get("roleRecipes") or data.get("criticalRecipes") or {}


def apply_overlay(recipe: dict, cfg: dict, kin: dict) -> dict:
    r = copy.deepcopy(recipe)
    common_spawn_x = float(kin["world"]["spawnX"])
    formation_offsets = kin.get("formationXOffsets", {})
    r["designatedRoleMonsters"] = list(cfg.get("designatedRoleMonsters") or [])

    if "entryShiftTowardWall" in cfg:
        r["entryBaseX"] = common_spawn_x - float(cfg["entryShiftTowardWall"])

    relative = cfg.get("relativeSpecialOffsets") or {}
    if relative:
        current_formation = formation_offsets.get(r.get("formation"), {})
        extras = dict(r.get("entryXOffsetByType") or {})
        for typ, desired_total in relative.items():
            extras[str(typ)] = float(desired_total) - float(current_formation.get(str(typ), 0.0))
        r["entryXOffsetByType"] = extras

    overrides = cfg.get("spawnTimeOverridesMs") or []
    if overrides:
        counters = defaultdict(int)
        override_map = {
            (str(x["occurrenceType"]), int(x["occurrenceIndex"])): int(x["tMs"])
            for x in overrides
        }
        new_spawns = []
        for spawn in r.get("spawns", []):
            s = dict(spawn)
            typ = str(s["type"])
            counters[typ] += 1
            key = (typ, counters[typ])
            if key in override_map:
                s["tMs"] = override_map[key]
            new_spawns.append(s)
        new_spawns.sort(key=lambda x: (int(x["tMs"]), str(x["type"])))
        r["spawns"] = new_spawns
    return r


def materialize_all20(base: dict, kin: dict, overlays: list[dict]) -> list[dict]:
    by_id = {str(r["id"]): copy.deepcopy(r) for r in base.get("recipes", [])}
    cfg_by_id: dict[str, dict] = {}
    source_by_id: dict[str, str] = {}
    for overlay in overlays:
        version = str(overlay.get("version"))
        for recipe_id, cfg in overlay_recipes(overlay).items():
            recipe_id = str(recipe_id)
            if recipe_id in cfg_by_id:
                raise ValueError(
                    f"recipe {recipe_id} appears in multiple overlays: "
                    f"{source_by_id[recipe_id]} and {version}"
                )
            cfg_by_id[recipe_id] = cfg
            source_by_id[recipe_id] = version

    missing_base = sorted(set(cfg_by_id) - set(by_id))
    if missing_base:
        raise ValueError(f"overlay recipes missing from base: {missing_base}")

    uncovered = sorted(set(by_id) - set(cfg_by_id))
    if uncovered:
        raise ValueError(f"all-20 probe requires overlay coverage for every base recipe: {uncovered}")

    return [apply_overlay(r, cfg_by_id[str(r["id"])], kin) for r in base.get("recipes", [])]


def central_judge_stream(cfg: dict, seed: int, consumed: list[str]):
    model = cfg["model"]
    rng = RNG(seed)
    state = choose(model["initialState"], rng.unit())
    while True:
        s = model["states"][state]
        judgment = choose(s["judgmentDistribution"], rng.unit())
        consumed.append(judgment)
        yield judgment
        state = choose(s["transitionAfterJudgment"], rng.unit())


def consumption_metrics(consumed: list[str], actions: int) -> dict:
    counts = Counter(consumed)
    idx = 0
    charge = 0
    heavy = 0
    pp = 0
    for _ in range(actions):
        if idx >= len(consumed):
            break
        x = consumed[idx]
        idx += 1
        if charge >= 3:
            if idx >= len(consumed):
                break
            y = consumed[idx]
            idx += 1
            heavy += 1
            if x == "PERFECT" and y == "PERFECT":
                pp += 1
            charge = 0
        else:
            charge = min(3, charge + 1)
    return {
        "judgeEvents": len(consumed),
        "judgeCounts": {
            "PERFECT": int(counts["PERFECT"]),
            "GOOD": int(counts["GOOD"]),
            "NORMAL": int(counts["NORMAL"]),
        },
        "heavyCount": heavy,
        "ppCount": pp,
        "ppRate": (pp / heavy) if heavy else None,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--recipes", type=Path, default=DEFAULT_RECIPES)
    p.add_argument("--kinematic-anchor", type=Path, default=DEFAULT_KINEMATICS)
    p.add_argument("--combat-anchor", type=Path, default=DEFAULT_COMBAT)
    p.add_argument("--legacy-trace", type=Path, default=DEFAULT_LEGACY_TRACE)
    p.add_argument("--central-model", type=Path, default=DEFAULT_CENTRAL)
    p.add_argument("--overlay", type=Path, action="append", default=None)
    p.add_argument("--seed", type=int, action="append", default=None)
    p.add_argument("--action-interval-ms", type=int, default=1100)
    p.add_argument("--power-mode", default="CURRENT_AUTHORITY_LV6")
    p.add_argument("--recipe", action="append", default=[])
    args = p.parse_args()

    if args.action_interval_ms <= 0:
        raise SystemExit("--action-interval-ms must be positive")

    base = load_yaml(args.recipes)
    kin = load_yaml(args.kinematic_anchor)
    combat = load_yaml(args.combat_anchor)
    legacy_trace = load_yaml(args.legacy_trace)
    central = load_yaml(args.central_model)
    overlay_paths = args.overlay or DEFAULT_OVERLAYS
    overlays = [load_yaml(x) for x in overlay_paths]
    recipes = materialize_all20(base, kin, overlays)
    if len(recipes) != 20:
        raise SystemExit(f"expected 20 representative recipes, found {len(recipes)}")

    wanted = set(args.recipe)
    if wanted:
        recipes = [r for r in recipes if str(r["id"]) in wanted]
        missing = sorted(wanted - {str(r["id"]) for r in recipes})
        if missing:
            raise SystemExit(f"unknown recipe ids: {missing}")

    seeds = args.seed or DEFAULT_SEEDS
    if len(set(seeds)) != len(seeds):
        raise SystemExit("duplicate --seed values are not allowed")

    power_modes = legacy_trace.get("powerModes") or {}
    if args.power_mode not in power_modes:
        raise SystemExit(f"unknown power mode: {args.power_mode}")
    power_mode = power_modes[args.power_mode]

    metadata = {
        "simulation": "SKILLED_V2_CENTRAL_ALL20_ROLE_PROBE_V0_1",
        "recipeVersion": base.get("version"),
        "overlayVersions": [o.get("version") for o in overlays],
        "sequenceVersion": central.get("version"),
        "sequenceStatus": central.get("status"),
        "seeds": seeds,
        "powerMode": args.power_mode,
        "actionIntervalMs": args.action_interval_ms,
        "actionIntervalStatus": "BOUNDED_CURRENT_MECHANIC_SIMULATION_CONTROL_NOT_SKILL_FIT",
        "warnings": [
            "70/20/10 is a user-authorized design prior, not empirical population telemetry.",
            "This probe applies no fitted turnover/density judgment penalty.",
            "Production timing-square geometry and line speed are unchanged.",
            "Historical TRACE_BRACKET profiles remain separate comparison probes.",
        ],
    }
    print(json.dumps(metadata, ensure_ascii=False, separators=(",", ":")))

    original_judge_stream = sim.judge_stream
    try:
        for seed in seeds:
            profile_id = f"SKILLED_V2_CENTRAL_CANDIDATE_V0_1_S{seed}"
            for recipe in recipes:
                for cls in sim.CLASSES:
                    consumed: list[str] = []

                    def seeded_stream(_perfect_streak, _break_judge, *, _seed=seed, _consumed=consumed):
                        return central_judge_stream(central, _seed, _consumed)

                    sim.judge_stream = seeded_stream
                    trace_control = {
                        "perfectStreakJudges": 1,
                        "breakJudge": "GOOD",
                        "actionIntervalMs": args.action_interval_ms,
                        "targetReacquireDelayMs": 0,
                    }
                    out = sim.simulate(recipe, kin, combat, trace_control, cls, power_mode)
                    extra = consumption_metrics(consumed, int(out.get("actions") or 0))
                    row = {
                        "recipeId": recipe["id"],
                        "tier": recipe["tier"],
                        "archetype": recipe["archetype"],
                        "profile": profile_id,
                        "sequenceSeed": seed,
                        "sequenceVersion": central.get("version"),
                        "classId": cls,
                        "actionIntervalMs": args.action_interval_ms,
                        **extra,
                        **out,
                    }
                    print(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
    finally:
        sim.judge_stream = original_judge_stream

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
