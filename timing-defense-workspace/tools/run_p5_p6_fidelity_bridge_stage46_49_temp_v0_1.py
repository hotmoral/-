#!/usr/bin/env python3
from __future__ import annotations

import builtins
import copy
import hashlib
import inspect
import json
from collections import Counter
from pathlib import Path

import yaml

import run_p3_persistent_kernel_v0_1 as p3
import run_p4d2_stage46_temporal_pressure_probe_v0_1 as stage46
import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ

CLASSES = list(integ.CLASSES)
STAGES = (46, 47, 48, 49)
SEEDS = list(range(1, 21))
ENTRY_CHARGES = (0, 1, 2, 3)
PROFILE = "BALANCED"
DRAIN_SECONDS = 240.0
SCENARIO_ID = "P5P6_FIDELITY_BRIDGE_STAGE46_49_V01"
OUT = Path("p5_p6_fidelity_bridge_stage46_49_temp_v0_1.json")

BRIDGE_CTX = {
    "runState": None,
    "central": None,
}


def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_yaml(path: str):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def make_row(typ: str, band: int, t: float, ref: float = 0.0) -> dict:
    return {
        "type": typ,
        "band": int(band),
        "referenceOffset": float(ref),
        "spawnLeadSeconds": float(12.0 + ref - t),
    }


def candidate_direction(direction: dict) -> dict:
    d = copy.deepcopy(direction)
    s48 = d["stageDirection"]["48"]
    s48["pressureCycleSecondsCandidate"] = 999.0
    s48["diagnosticPacket"] = [
        make_row("ARMORED_DURABLE_PROXY", -2, 5.25),
        make_row("ARMORED_DURABLE_PROXY", 0, 6.25),
        make_row("ARMORED_DURABLE_PROXY", -1, 7.25),
        make_row("GRUNT", 1, 5.85),
        make_row("GRUNT", 0, 6.98),
        make_row("SIEGER", 2, 8.0, 2.0),
    ]
    s48["note"] = "TEMP_P5P6_FIDELITY_FIXED_STAGE48_DIAGNOSTIC_CENTER"
    integ.validate_right_edge_contract(d)
    return d


def derived_seed(base_seed: int, cls: str) -> int:
    return p3.seed(int(base_seed), f"{SCENARIO_ID}|{cls}")


def new_run_state(mode: str, central: dict, base_seed: int, cls: str, entry_charge: int) -> dict:
    row_seed = derived_seed(base_seed, cls)
    rng = p3.RNG(p3.seed(row_seed, "JUDGMENT"))
    state = p3.choose(central["model"]["initialState"], rng.unit())
    return {
        "mode": mode,
        "baseSeed": int(base_seed),
        "derivedSeed": int(row_seed),
        "combo": 0,
        "comboPeak": 0,
        "charge": int(entry_charge),
        "entryCharge": int(entry_charge),
        "judgmentRng": int(rng.state),
        "judgmentState": state,
        "judgmentCounts": {},
        "heavyTierCounts": {},
        "judgmentsConsumed": 0,
        "rootActions": 0,
        "heavyActions": 0,
        "pxpActions": 0,
        "n3Triggers": 0,
    }


def bridge_next_judgment() -> str:
    rs = BRIDGE_CTX["runState"]
    if rs is None:
        raise RuntimeError("bridge runState is not installed")
    if rs["mode"] == "ALL_PERFECT":
        j = "PERFECT"
    elif rs["mode"] == "SKILLED_V2_CENTRAL":
        central = BRIDGE_CTX["central"]
        rng = p3.RNG(int(rs["judgmentRng"]))
        state_cfg = central["model"]["states"][rs["judgmentState"]]
        j = p3.choose(state_cfg["judgmentDistribution"], rng.unit())
        rs["judgmentState"] = p3.choose(state_cfg["transitionAfterJudgment"], rng.unit())
        rs["judgmentRng"] = int(rng.state)
    else:
        raise ValueError(rs["mode"])
    rs["judgmentsConsumed"] += 1
    rs["judgmentCounts"][j] = int(rs["judgmentCounts"].get(j, 0)) + 1
    return j


def bridge_update_combo(judgment: str) -> list[int]:
    rs = BRIDGE_CTX["runState"]
    if judgment == "PERFECT":
        rs["combo"] += 1
        rs["comboPeak"] = max(int(rs["comboPeak"]), int(rs["combo"]))
        m = p3.mile(int(rs["combo"]))
        return [int(m)] if m else []
    rs["combo"] = 0
    return []


def install_fixed_schedule_hook_on(sim_fn):
    glb = sim_fn.__globals__
    fallback = glb["build_integrated_schedule"]

    def hooked(cfg):
        if "_p5FixedStageSchedule" in cfg:
            duration = float(cfg["simulation"]["durationSeconds"])
            return [tuple(x) for x in cfg["_p5FixedStageSchedule"] if float(x[0]) < duration]
        return fallback(cfg)

    glb["build_integrated_schedule"] = hooked
    return sim_fn


def build_bridge_simulate():
    original_basic_knock = stage46.basic_knock

    def corrected_basic_knock(tier):
        if tier == "HEAVY+":
            return 0.013
        return original_basic_knock(tier)

    stage46.basic_knock = corrected_basic_knock
    stage46._bridge_ctx = BRIDGE_CTX
    stage46._bridge_next_judgment = bridge_next_judgment
    stage46._bridge_update_combo = bridge_update_combo
    stage46._p3 = p3

    src = inspect.getsource(stage46.simulate)
    old_timing = '''            attack_no += 1\n            heavy = attack_no % heavy_every == 0\n            if heavy:\n                heavy_index += 1\n            is_miss = heavy and heavy_index in missed_heavy_indices\n            tier = "SUPER" if is_miss else ("CRITICAL" if heavy else "PERFECT")\n            base_damage = 400 if is_miss else (600 if heavy else 200)\n            if heavy and not is_miss:\n                stats["pxpCount"] += 1\n            if is_miss:\n                stats["heavyMissCount"] += 1\n            primary = nearest(mobs)\n            final = has_lv31 and heavy and not is_miss\n'''
    new_timing = '''            attack_no += 1\n            _rs = _bridge_ctx["runState"]\n            heavy = int(_rs["charge"]) >= 3\n            if heavy:\n                heavy_index += 1\n            is_miss = False\n            milestones = []\n            if heavy:\n                _sx = _bridge_next_judgment()\n                milestones += _bridge_update_combo(_sx)\n                _sy = _bridge_next_judgment()\n                predicted_combo = int(_rs["combo"]) + 1 if _sy == "PERFECT" else 0\n                tier = _p3.strong(_sx, _sy)\n                milestones += _bridge_update_combo(_sy)\n                _rs["heavyActions"] += 1\n                _rs["heavyTierCounts"][tier] = int(_rs["heavyTierCounts"].get(tier, 0)) + 1\n            else:\n                _sx = _bridge_next_judgment()\n                _sy = None\n                predicted_combo = int(_rs["combo"]) + 1 if _sx == "PERFECT" else 0\n                tier = _sx\n                milestones += _bridge_update_combo(_sx)\n            _rs["rootActions"] += 1\n            base_damage = float(_p3.BASE[tier]) * (1.0 + float(_p3.cb(predicted_combo)))\n            if heavy and tier == "CRITICAL":\n                stats["pxpCount"] += 1\n                _rs["pxpActions"] += 1\n            if heavy and tier != "CRITICAL":\n                stats["heavyMissCount"] += 1\n            primary = nearest(mobs)\n            final = has_lv31 and heavy and tier == "CRITICAL"\n'''
    if src.count(old_timing) != 1:
        raise RuntimeError("Stage46 timing block changed; bridge review required")
    modified_src = src.replace(old_timing, new_timing, 1)

    original_getsource = integ.inspect.getsource
    had_exec = "exec" in integ.__dict__
    original_exec = integ.__dict__.get("exec")

    def patched_getsource(obj):
        if obj is stage46.simulate:
            return modified_src
        return original_getsource(obj)

    def bridge_exec(final_src, ns):
        replacements = [
            ('            root = 600 * 1.12 * 1.18 * 1.20\n',
             '            root = base_damage * 1.12 * 1.18 * 1.20\n'),
            ('            raw = 600 * float(cand["perDaggerCoefficient"])\n',
             '            raw = base_damage * float(cand["perDaggerCoefficient"])\n'),
            ('            raw = 600 * float(cand["shockwaveCoefficient"])\n',
             '            raw = base_damage * float(cand["shockwaveCoefficient"])\n'),
            ('            raw = 660 * float(cand["perTargetCoefficient"])\n',
             '            raw = root * float(cand["perTargetCoefficient"])\n'),
        ]
        for old, new in replacements:
            if final_src.count(old) != 1:
                raise RuntimeError(f"final-package combo-basis patch mismatch: {old.strip()}")
            final_src = final_src.replace(old, new, 1)

        old_mage = (
            '        if final:\n'
            '            px, pb = primary.x, primary.band\n'
            '            hit(mon, cfg, mobs, primary, 720, stats, counter)\n'
        )
        new_mage = (
            '        if final:\n'
            '            px, pb = primary.x, primary.band\n'
            '            final_root = base_damage * 1.20\n'
            '            hit(mon, cfg, mobs, primary, final_root, stats, counter)\n'
        )
        if final_src.count(old_mage) != 1:
            raise RuntimeError("Mage final root patch mismatch")
        final_src = final_src.replace(old_mage, new_mage, 1)
        old_stage = '                    hit(mon, cfg, mobs, target, 720 * float(cand["stageCoefficient"]), stats, counter)\n'
        if final_src.count(old_stage) != 1:
            raise RuntimeError("Mage final stage patch mismatch")
        final_src = final_src.replace(old_stage, '                    hit(mon, cfg, mobs, target, final_root * float(cand["stageCoefficient"]), stats, counter)\n', 1)
        old_chain = '                        hit(mon, cfg, mobs, target, 720 * 0.35, stats, counter)\n'
        if final_src.count(old_chain) != 1:
            raise RuntimeError("Mage final chain patch mismatch")
        final_src = final_src.replace(old_chain, '                        hit(mon, cfg, mobs, target, final_root * 0.35, stats, counter)\n', 1)

        n3_code = '''\n    def trigger_bridge_n3(milestone, at):\n        p = nearest(mobs)\n        if not p:\n            return\n        _rs = _bridge_ctx["runState"]\n        _rs["n3Triggers"] += 1\n        parts = _p3.alloc(_p3.budget(int(milestone)), _p3.weights(cls.lower(), int(milestone)))\n        if cls == "Rogue":\n            root_id = p.id\n            for i, raw in enumerate(parts):\n                def n3_dagger(raw=raw, root_id=root_id):\n                    q = next((m for m in mobs if m.alive and m.id == root_id), None) or nearest(mobs)\n                    if q:\n                        hit(mon, cfg, mobs, q, raw, stats, counter)\n                schedule_event(at + i * 0.055, n3_dagger)\n            return\n\n        hit(mon, cfg, mobs, p, parts[0], stats, counter)\n        push(p, "NORMAL", 1.30 if cls == "Tank" else 1.0, at, stats)\n        secondaries = []\n        if cls == "Knight":\n            secondaries = [m for m in corridor_targets(mobs, p, int(geom["knightHeavyBandRadius"]), 4) if m is not p][:1]\n        elif cls == "Tank":\n            secondaries = sorted(\n                [m for m in mobs if m.alive and m is not p and abs(m.x - p.x) <= 0.13 and abs(m.band - p.band) <= 1],\n                key=lambda m: (abs(m.x - p.x), abs(m.band - p.band), m.id),\n            )[:2]\n        elif cls == "Archer":\n            secondaries = [m for m in lane_targets(mobs, p.band, radius=int(geom["archerLv26BandRadius"]), max_n=5) if m is not p][:1]\n        elif cls == "Mage":\n            secondaries = nearby(mobs, p.x, p.band, 0.12, 1, exclude=p, max_n=3)\n        for q, raw in zip(secondaries, parts[1:]):\n            hit(mon, cfg, mobs, q, raw, stats, counter)\n            push(q, "NORMAL", 1.30 if cls == "Tank" else 1.0, at, stats)\n'''
        anchor = '    now = 0.0\n'
        if final_src.count(anchor) != 1:
            raise RuntimeError("N3 insertion anchor changed")
        final_src = final_src.replace(anchor, n3_code + '\n' + anchor, 1)

        old_after_class = (
            '            else:\n'
            '                raise ValueError(cls)\n\n'
            '            next_attack += root_interval\n'
        )
        new_after_class = (
            '            else:\n'
            '                raise ValueError(cls)\n\n'
            '            for _milestone in milestones:\n'
            '                trigger_bridge_n3(_milestone, now)\n'
            '            _rs["charge"] = 0 if heavy else min(3, int(_rs["charge"]) + 1)\n'
            '            next_attack += root_interval\n'
        )
        if final_src.count(old_after_class) != 1:
            raise RuntimeError("post-action persistent-state patch mismatch")
        final_src = final_src.replace(old_after_class, new_after_class, 1)
        builtins.exec(final_src, ns)

    integ.inspect.getsource = patched_getsource
    integ.exec = bridge_exec
    try:
        fn = integ.build_identity_aware_simulate()
    finally:
        integ.inspect.getsource = original_getsource
        if had_exec:
            integ.exec = original_exec
        else:
            del integ.exec
    return install_fixed_schedule_hook_on(fn)


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
    return base, temporal, candidate_direction(direction), shop, integration, central


def fixed_stage_cfg(base_temporal, direction, integration, stage_no, cls, duration):
    authored = integ.stage_temporal(base_temporal, direction, integration, stage_no, cls)
    schedule = integ.build_integrated_schedule(authored)
    cfg = copy.deepcopy(authored)
    cfg["version"] = f"p5p6-fidelity-stage{stage_no}-temp-v0.1"
    cfg["simulation"]["durationSeconds"] = float(duration)
    cfg["_p5FixedStageSchedule"] = [list(x) for x in schedule]
    cfg.pop("integratedSchedule", None)
    return cfg, schedule


def simulate_stage(sim_fn, base, temporal, direction, integration, cls, profile, scale, stage_no, current_wall, start_state):
    cfg, expected_schedule = fixed_stage_cfg(temporal, direction, integration, stage_no, cls, DRAIN_SECONDS)
    actual_schedule = sim_fn.__globals__["build_integrated_schedule"](cfg)
    if [tuple(x) for x in actual_schedule] != [tuple(x) for x in expected_schedule]:
        raise RuntimeError(f"fixed schedule mismatch Stage{stage_no} {cls}")
    local_state = copy.deepcopy(start_state)
    BRIDGE_CTX["runState"] = local_state
    before = copy.deepcopy(local_state)
    row = sim_fn(
        base,
        cfg,
        cls,
        True,
        (),
        overrides={"shockwaveCoefficient": 0.25} if cls == "Tank" else None,
        shop_profile=profile,
        effect_scale=float(scale),
        start_wall_current=float(current_wall),
    )
    after = copy.deepcopy(BRIDGE_CTX["runState"])
    settled = row.get("burialTime") is None and int(row.get("endActive") or 0) == 0
    return {
        "row": row,
        "settled": bool(settled),
        "schedule": expected_schedule,
        "stateBefore": before,
        "stateAfter": after,
    }


def delta_counts(after: dict, before: dict, key: str) -> dict:
    a = Counter(after.get(key) or {})
    b = Counter(before.get(key) or {})
    return {k: int(a[k] - b[k]) for k in sorted(set(a) | set(b)) if a[k] - b[k]}


def run_chain(sim_fn, base, temporal, direction, shop, integration, central, cls, mode, base_seed, entry_charge):
    BRIDGE_CTX["central"] = central
    state = new_run_state(mode, central, base_seed, cls, entry_charge)
    profile = integ.profile_for(shop, cls, PROFILE)
    scale = float(integration["shopEffectScale"])
    wall_max = float(integration["startingBaseWallHp"]) + float(profile["fort"]) * 100.0 * scale
    current = wall_max
    stages = []

    for stage_no in STAGES:
        start_wall = current
        result = simulate_stage(sim_fn, base, temporal, direction, integration, cls, profile, scale, stage_no, current, state)
        row = result["row"]
        before = result["stateBefore"]
        after = result["stateAfter"]
        current = float(row["endWall"])
        state = after
        stages.append({
            "stage": stage_no,
            "settled": result["settled"],
            "buried": row.get("burialTime") is not None,
            "burialTime": row.get("burialTime"),
            "startWall": round(start_wall, 3),
            "endWall": round(current, 3),
            "endActiveAtDrainCap": int(row.get("endActive") or 0),
            "wallHits": int(row.get("wallHits") or 0),
            "siegerShots": int(row.get("siegerShots") or 0),
            "siegerWindups": int(row.get("siegerWindups") or 0),
            "pxpCount": int(row.get("pxpCount") or 0),
            "comboStart": int(before["combo"]),
            "comboEnd": int(after["combo"]),
            "comboPeakCumulative": int(after["comboPeak"]),
            "chargeStart": int(before["charge"]),
            "chargeEnd": int(after["charge"]),
            "judgmentsConsumed": int(after["judgmentsConsumed"] - before["judgmentsConsumed"]),
            "rootActions": int(after["rootActions"] - before["rootActions"]),
            "heavyActions": int(after["heavyActions"] - before["heavyActions"]),
            "pxpActions": int(after["pxpActions"] - before["pxpActions"]),
            "n3Triggers": int(after["n3Triggers"] - before["n3Triggers"]),
            "judgmentCounts": delta_counts(after, before, "judgmentCounts"),
            "heavyTierCounts": delta_counts(after, before, "heavyTierCounts"),
        })
        if not result["settled"]:
            break

    return {
        "mode": mode,
        "baseSeed": int(base_seed),
        "derivedSeed": int(state["derivedSeed"]),
        "class": cls,
        "entryComboBoundary": 0,
        "entryCharge": int(entry_charge),
        "settledThroughStage49": len(stages) == 4 and all(s["settled"] for s in stages),
        "failureStage": None if len(stages) == 4 and all(s["settled"] for s in stages) else (stages[-1]["stage"] if stages else None),
        "reachedStage48": any(s["stage"] == 48 for s in stages),
        "reachedStage49": any(s["stage"] == 49 for s in stages),
        "finalWall": round(current, 3),
        "finalAbsoluteDeficit": round(max(0.0, wall_max - current), 3),
        "comboPeak": int(state["comboPeak"]),
        "comboEnd": int(state["combo"]),
        "chargeEnd": int(state["charge"]),
        "judgmentCounts": dict(sorted(state["judgmentCounts"].items())),
        "heavyTierCounts": dict(sorted(state["heavyTierCounts"].items())),
        "totalRootActions": int(state["rootActions"]),
        "totalHeavyActions": int(state["heavyActions"]),
        "totalPxpActions": int(state["pxpActions"]),
        "totalN3Triggers": int(state["n3Triggers"]),
        "stages": stages,
    }


def aggregate(rows: list[dict]) -> dict:
    out = {"byEntryCharge": {}, "skilledOverall": {}, "allPerfect": {}}
    for charge in ENTRY_CHARGES:
        charge_rows = [r for r in rows if r["entryCharge"] == charge]
        block = {}
        for mode in ("ALL_PERFECT", "SKILLED_V2_CENTRAL"):
            mr = [r for r in charge_rows if r["mode"] == mode]
            per_class = {}
            for cls in CLASSES:
                cr = [r for r in mr if r["class"] == cls]
                per_class[cls] = {
                    "cases": len(cr),
                    "through49": sum(1 for r in cr if r["settledThroughStage49"]),
                    "failureStages": dict(sorted(Counter(str(r["failureStage"]) for r in cr if r["failureStage"] is not None).items())),
                    "reached48": sum(1 for r in cr if r["reachedStage48"]),
                    "stage48SiegerShotCases": sum(1 for r in cr if any(s["stage"] == 48 and s["siegerShots"] > 0 for s in r["stages"])),
                    "finalWalls": [r["finalWall"] for r in cr],
                    "comboPeaks": [r["comboPeak"] for r in cr],
                    "n3Triggers": [r["totalN3Triggers"] for r in cr],
                    "pxpActions": [r["totalPxpActions"] for r in cr],
                }
            block[mode] = {
                "cases": len(mr),
                "through49": sum(1 for r in mr if r["settledThroughStage49"]),
                "failureStages": dict(sorted(Counter(str(r["failureStage"]) for r in mr if r["failureStage"] is not None).items())),
                "perClass": per_class,
            }
        out["byEntryCharge"][str(charge)] = block

    skilled = [r for r in rows if r["mode"] == "SKILLED_V2_CENTRAL"]
    j = Counter()
    h = Counter()
    for r in skilled:
        j.update(r["judgmentCounts"])
        h.update(r["heavyTierCounts"])
    tj = sum(j.values())
    th = sum(h.values())
    out["skilledOverall"] = {
        "cases": len(skilled),
        "through49": sum(1 for r in skilled if r["settledThroughStage49"]),
        "judgmentCounts": dict(sorted(j.items())),
        "judgmentMix": {k: round(v / tj, 6) for k, v in sorted(j.items())} if tj else {},
        "heavyTierCounts": dict(sorted(h.items())),
        "pxpRate": round(h.get("CRITICAL", 0) / th, 6) if th else None,
    }
    perfect = [r for r in rows if r["mode"] == "ALL_PERFECT"]
    out["allPerfect"] = {
        "cases": len(perfect),
        "through49": sum(1 for r in perfect if r["settledThroughStage49"]),
    }
    return out


def main():
    base, temporal, direction, shop, integration, central = load_inputs()
    if float(integration["referenceWarmupSeconds"]) != 12.0:
        raise RuntimeError("make_row assumes current 12.0s reference warmup")
    sim_fn = build_bridge_simulate()

    rows = []
    for charge in ENTRY_CHARGES:
        for cls in CLASSES:
            rows.append(run_chain(sim_fn, base, temporal, direction, shop, integration, central, cls, "ALL_PERFECT", 1, charge))
        for seed in SEEDS:
            for cls in CLASSES:
                rows.append(run_chain(sim_fn, base, temporal, direction, shop, integration, central, cls, "SKILLED_V2_CENTRAL", seed, charge))

    output = {
        "version": "p5-p6-fidelity-bridge-stage46-49-temp-v0.1",
        "authority": "TEMP_DIAGNOSTIC_ONLY_NO_ADOPTION_NO_FREEZE_NO_PRODUCTION_AUTHORITY",
        "purpose": "Inject P3 persistent timing/combo/charge/N3 semantics into the current P5 late-run combat/shop/Lv31/STAGE_SETTLED model before numeric tuning.",
        "fixed": {
            "physicalSpawnX": 0.92,
            "stage48DiagnosticCenter": "ARMORED3_SPATIAL_PLUS_GRUNT2_PLUS_SIEGER",
            "globalSiegerStandoff": 0.38,
            "shopProfile": PROFILE,
            "shopEffectScale": float(integration["shopEffectScale"]),
            "stageDrainCapSeconds": DRAIN_SECONDS,
            "entryComboBoundary": 0,
            "entryComboAuthority": "BOUNDARY_ONLY_NOT_FULL_RUN_STAGE46_DISTRIBUTION",
            "entryChargeSensitivity": list(ENTRY_CHARGES),
            "tankShockwaveCoefficient": 0.25,
        },
        "fidelityIncluded": [
            "one persistent SKILLED_V2 judgment RNG/state across Stage46-49",
            "combo persists across Stage46-49 and breaks only on non-PERFECT judgment",
            "charge persists across Stage46-49; Heavy occurs at charge>=3 and consumes two judgments",
            "P+P alone triggers CRITICAL and the Lv31 final package",
            "combo root damage scalar applies to ordinary and Lv31 root outgoing basis",
            "P3 N3 milestones/budgets are generated without recursive combo/charge/EXP",
            "HEAVY+ knockback uses authoritative 0.013 tier value",
            "P5 shop/Lv31/class packages/right-edge/SIEGER/CHARGER/wall carry remain in force",
            "each Stage uses frozen authored schedule then drains to the 240s STAGE_SETTLED cap; enemy instances do not cross stages",
        ],
        "knownBoundary": [
            "Stage46 entry combo is fixed at 0 only as a late-segment boundary; the full Stage1-45 entry distribution is not modeled here.",
            "Stage46 entry charge is not assumed; all four legal charge states are screened.",
            "The current Stage48 armored proxy packet remains diagnostic and is not adopted.",
            "Fixed late-segment shop snapshot remains a diagnostic isolation, not actual purchase history.",
        ],
        "seeds": SEEDS,
        "rows": rows,
        "aggregate": aggregate(rows),
    }
    text = json.dumps(output, indent=2, sort_keys=True)
    OUT.write_text(text + "\n", encoding="utf-8")
    print(text)
    print("SHA256=" + hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
