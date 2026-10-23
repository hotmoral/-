#!/usr/bin/env python3
"""TEMP: compare current Stage46->49 P5 late-run candidate under all-perfect vs SKILLED_V2_CENTRAL.

Diagnostic only. No design/numeric/production authority.
Keeps the current P3_GRUNT2 Stage48 packet, global SIEGER standoff 0.38,
BALANCED shop, right-edge entry, carried wall deficit, and Stage-settled transition.
Only the timing judgment stream changes.

Important boundedness note:
- this preserves the current P5 late-segment simulator cadence/charge abstraction;
- it does not claim a fitted real-player action cadence;
- SKILLED_V2_CENTRAL changes judgment quality and P×P/Lv31-final frequency only.
"""
from __future__ import annotations

import copy
import hashlib
import inspect
import json
from collections import Counter
from pathlib import Path

import yaml

import run_p4d2_stage46_temporal_pressure_probe_v0_1 as stage46
import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled
import run_p5_stage46_49_moderate_standoff_grunt_screen_temp as moderate
import run_p5_stage48_armored_standoff_hybrid_temp as hybrid
from simulate_class_aware_layer_a import BASE_DAMAGE, strong_tier
from validate_skilled_v2_central_sequence import RNG, choose

SEEDS = [101, 211, 307]
PROFILE = "BALANCED"
DRAIN_SECONDS = 240.0
SCENARIO_ID = "P5_STAGE46_49_P3_GRUNT2_SKILLED_V2"


def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_yaml(path: str):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def fnv_row_seed(base_seed: int, scenario_id: str, cls: str) -> int:
    h = 2166136261
    for byte in f"{base_seed}|{scenario_id}|{cls}".encode("utf-8"):
        h ^= byte
        h = (h * 16777619) & 0xFFFFFFFF
    return h or 0x6D2B79F5


def central_stream(cfg: dict, seed: int):
    model = cfg["model"]
    rng = RNG(seed)
    state = choose(model["initialState"], rng.unit())
    while True:
        s = model["states"][state]
        judgment = choose(s["judgmentDistribution"], rng.unit())
        yield judgment
        state = choose(s["transitionAfterJudgment"], rng.unit())


def build_skilled_integrated_simulate(skilled_ctx: dict):
    """Reuse the exact P5 integrated patch but replace only the root timing judgment block."""
    src = inspect.getsource(stage46.simulate)
    old = '''            attack_no += 1\n            heavy = attack_no % heavy_every == 0\n            if heavy:\n                heavy_index += 1\n            is_miss = heavy and heavy_index in missed_heavy_indices\n            tier = "SUPER" if is_miss else ("CRITICAL" if heavy else "PERFECT")\n            base_damage = 400 if is_miss else (600 if heavy else 200)\n            if heavy and not is_miss:\n                stats["pxpCount"] += 1\n            if is_miss:\n                stats["heavyMissCount"] += 1\n            primary = nearest(mobs)\n            final = has_lv31 and heavy and not is_miss\n'''
    new = '''            attack_no += 1\n            heavy = attack_no % heavy_every == 0\n            if heavy:\n                heavy_index += 1\n            is_miss = False\n            if heavy:\n                _sx = next(_skilled_ctx["stream"])\n                _sy = next(_skilled_ctx["stream"])\n                tier = _strong_tier(_sx, _sy)\n                _skilled_ctx["judgments"].extend((_sx, _sy))\n                _skilled_ctx["heavyTiers"][tier] = _skilled_ctx["heavyTiers"].get(tier, 0) + 1\n            else:\n                _sx = next(_skilled_ctx["stream"])\n                _sy = None\n                tier = _sx\n                _skilled_ctx["judgments"].append(_sx)\n            base_damage = float(_base_damage_map[tier])\n            if heavy and tier == "CRITICAL":\n                stats["pxpCount"] += 1\n            if heavy and tier != "CRITICAL":\n                stats["heavyMissCount"] += 1\n            primary = nearest(mobs)\n            final = has_lv31 and heavy and tier == "CRITICAL"\n'''
    if src.count(old) != 1:
        raise RuntimeError("Stage46 timing block changed; skilled integration review required")
    skilled_src = src.replace(old, new, 1)

    # build_identity_aware_simulate() intentionally patches source obtained through inspect.getsource.
    # Feed it the skilled source while retaining every existing P5 shop/identity patch.
    stage46._skilled_ctx = skilled_ctx
    stage46._strong_tier = strong_tier
    stage46._base_damage_map = BASE_DAMAGE
    original_getsource = integ.inspect.getsource

    def patched_getsource(obj):
        if obj is stage46.simulate:
            return skilled_src
        return original_getsource(obj)

    integ.inspect.getsource = patched_getsource
    try:
        fn = integ.build_identity_aware_simulate()
    finally:
        integ.inspect.getsource = original_getsource
    return hybrid.install_fixed_schedule_hook_on(fn)


def load_inputs():
    base = load_json("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    temporal = load_json("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49 = load_json("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction = load_json("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop = load_json("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    refinement = load_json("legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json")
    integration = load_json("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")
    central = load_yaml("legacy-game-structure/data/skilled_v2_central_sequence_candidate_v0_1.yaml")
    integ.validate_right_edge_contract(direction)
    base = integ.inject_diagnostic_monsters(base, stage49)
    base["monsterAnchors"]["ARMORED_DURABLE_PROXY"] = dict(refinement["knightRobustPair"]["anchor"])
    candidate_direction = moderate.candidate_direction(direction)
    return base, temporal, candidate_direction, shop, integration, central


def one_chain(sim_fn, base, temporal, direction, shop, integration, cls, skilled_ctx=None):
    scale = float(integration["shopEffectScale"])
    profile = integ.profile_for(shop, cls, PROFILE)
    wall_max = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * scale
    current = wall_max
    rows = []
    for stage_no in (46, 47, 48, 49):
        cfg, schedule = settled.fixed_stage_cfg(temporal, direction, integration, stage_no, cls, DRAIN_SECONDS)
        before_j = len(skilled_ctx["judgments"]) if skilled_ctx is not None else None
        before_h = dict(skilled_ctx["heavyTiers"]) if skilled_ctx is not None else None
        row = sim_fn(
            base, cfg, cls, True, (),
            overrides={"shockwaveCoefficient": 0.25} if cls == "Tank" else None,
            shop_profile=profile,
            effect_scale=scale,
            start_wall_current=current,
        )
        current = float(row["endWall"])
        stage_j = None
        stage_ht = None
        if skilled_ctx is not None:
            stage_j = skilled_ctx["judgments"][before_j:]
            after_h = skilled_ctx["heavyTiers"]
            keys = set(before_h) | set(after_h)
            stage_ht = {k: int(after_h.get(k, 0) - before_h.get(k, 0)) for k in sorted(keys) if after_h.get(k, 0) - before_h.get(k, 0)}
        rows.append({
            "stage": stage_no,
            "buried": row.get("burialTime") is not None,
            "burialTime": row.get("burialTime"),
            "endActiveAtDrainCap": int(row.get("endActive") or 0),
            "stageSettledByDrainCap": row.get("burialTime") is None and int(row.get("endActive") or 0) == 0,
            "authoredLastSpawn": round(max((float(x[0]) for x in schedule), default=0.0), 3),
            "startWall": round(wall_max if stage_no == 46 else rows[-1]["endWall"], 3),
            "endWall": round(current, 3),
            "siegerShots": int(row.get("siegerShots") or 0),
            "siegerWindups": int(row.get("siegerWindups") or 0),
            "pxpCount": int(row.get("pxpCount") or 0),
            "nonPxpHeavyCount": int(row.get("heavyMissCount") or 0),
            "wallHits": int(row.get("wallHits") or 0),
            "kills": int(row.get("kills") or 0),
            "judgmentCounts": dict(Counter(stage_j)) if stage_j is not None else None,
            "heavyTierCounts": stage_ht,
        })
        if row.get("burialTime") is not None or int(row.get("endActive") or 0) != 0:
            break
    return {
        "class": cls,
        "settledThroughStage49": len(rows) == 4 and all(r["stageSettledByDrainCap"] for r in rows),
        "finalWall": round(current, 3),
        "finalAbsoluteDeficit": round(max(0.0, wall_max - current), 3),
        "stage48Shots": next((r["siegerShots"] for r in rows if r["stage"] == 48), 0),
        "totalSiegerShots": sum(r["siegerShots"] for r in rows),
        "totalPxp": sum(r["pxpCount"] for r in rows),
        "stages": rows,
    }


def main():
    base, temporal, direction, shop, integration, central = load_inputs()
    original_sim = hybrid.install_fixed_schedule_hook_on(integ.SIMULATE)
    skilled_ctx = {"stream": None, "judgments": [], "heavyTiers": {}}
    skilled_sim = build_skilled_integrated_simulate(skilled_ctx)

    out = {
        "version": "p5-stage46-49-skilled-v2-vs-allperfect-grunt-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "comparison": "SAME_P3_GRUNT2_STAGE48_PACKET_SAME_P5_CADENCE_ONLY_JUDGMENT_MODEL_DIFFERS",
        "stage48Candidate": "ARMORED3_SPATIAL_PLUS_GRUNT2_PLUS_SIEGER",
        "globalSiegerStandoff": 0.38,
        "shopProfile": PROFILE,
        "skilledModel": central["version"],
        "skilledSeeds": SEEDS,
        "skilledLimitations": [
            "70/20/10 is a user-approved design prior, not empirical telemetry",
            "current P5 action cadence and stage-local heavy cadence are retained as bounded simulation controls",
            "no baseline MISS/INVALID, turnover penalty, or density judgment penalty is invented",
            "P+P alone triggers CRITICAL/Lv31 final package",
        ],
        "allPerfect": [],
        "skilled": [],
    }

    # Exact same P5 candidate under the previous idealized input model.
    for cls in integ.CLASSES:
        out["allPerfect"].append(one_chain(original_sim, base, temporal, direction, shop, integration, cls))

    # Central skilled: keep one persistent judgment stream across Stage46->49 per class/seed.
    for seed in SEEDS:
        for cls in integ.CLASSES:
            derived = fnv_row_seed(seed, SCENARIO_ID, cls)
            skilled_ctx["stream"] = central_stream(central, derived)
            skilled_ctx["judgments"] = []
            skilled_ctx["heavyTiers"] = {}
            row = one_chain(skilled_sim, base, temporal, direction, shop, integration, cls, skilled_ctx)
            row["baseSeed"] = seed
            row["derivedSeed"] = derived
            row["judgmentCounts"] = dict(Counter(skilled_ctx["judgments"]))
            row["heavyTierCounts"] = dict(sorted(skilled_ctx["heavyTiers"].items()))
            out["skilled"].append(row)

    out["aggregate"] = {
        "allPerfect": {
            "settledThrough49": sum(1 for r in out["allPerfect"] if r["settledThroughStage49"]),
            "cases": len(out["allPerfect"]),
            "stage48ShotsByClass": {r["class"]: r["stage48Shots"] for r in out["allPerfect"]},
            "finalWallByClass": {r["class"]: r["finalWall"] for r in out["allPerfect"]},
            "totalPxpByClass": {r["class"]: r["totalPxp"] for r in out["allPerfect"]},
        },
        "skilled": {
            "settledThrough49": sum(1 for r in out["skilled"] if r["settledThroughStage49"]),
            "cases": len(out["skilled"]),
            "buriedOrUnsettled": sum(1 for r in out["skilled"] if not r["settledThroughStage49"]),
            "perClass": {},
        },
    }
    for cls in integ.CLASSES:
        rows = [r for r in out["skilled"] if r["class"] == cls]
        out["aggregate"]["skilled"]["perClass"][cls] = {
            "settled": sum(1 for r in rows if r["settledThroughStage49"]),
            "cases": len(rows),
            "stage48Shots": [r["stage48Shots"] for r in rows],
            "finalWalls": [r["finalWall"] for r in rows],
            "totalPxp": [r["totalPxp"] for r in rows],
        }

    text = json.dumps(out, indent=2, sort_keys=True)
    p = Path("p5_stage46_49_skilled_v2_vs_allperfect_grunt_temp.json")
    p.write_text(text + "\n", encoding="utf-8")
    print(text)
    print("SHA256=" + hashlib.sha256(p.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
