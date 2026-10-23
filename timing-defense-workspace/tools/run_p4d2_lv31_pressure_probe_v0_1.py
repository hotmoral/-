#!/usr/bin/env python3
"""Timing Defense P4-D2 deterministic Lv31 current-roster pressure-response probe.

Scope:
- bounded diagnostic only
- no RNG
- current nine-roster provisional capability anchors supplied by fixture JSON
- historical/current formula reference used only for package-continuity calculations
- NOT production Stage46 authoring and NOT numerical freeze authority
"""
from __future__ import annotations
import argparse, json, math, statistics
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def mob_instances(fx, snapshot):
    anchors = fx["monsterAnchors"]
    out = []
    seq = 0
    for row in snapshot["mobs"]:
        seq += 1
        a = anchors[row["type"]]
        out.append({
            "id": f'{row["type"]}_{seq}',
            "type": row["type"],
            "x": float(row["x"]),
            "lane": int(row["lane"]),
            "knight": bool(row.get("knight", False)),
            "archer": bool(row.get("archer", False)),
            "mage": bool(row.get("mage", False)),
            "hp": float(a["hp"]),
            "maxHp": float(a["hp"]),
            "speed": float(a["speed"]),
            "wall": float(a["wall"]),
            "knockResist": float(a["knockResist"]),
            "armor": float(a["armor"]),
            "alive": True,
            "spawned": False,
        })
    return out


def alive(mobs):
    return [m for m in mobs if m["alive"]]


def hp_sum(mobs):
    return sum(max(0.0, m["hp"]) for m in mobs if m["alive"])


def wall_budget(mobs):
    return sum(m["wall"] for m in mobs if m["alive"])


def snapshot_metrics(mobs):
    a = alive(mobs)
    return {
        "liveCount": len(a),
        "remainingHp": round(hp_sum(mobs), 3),
        "remainingOneEventWallBudgetProxy": round(wall_budget(mobs), 3),
        "liveTypes": [m["type"] for m in sorted(a, key=lambda z: (z["x"], z["lane"], z["id"]))],
    }


def apply_hit(m, raw, armor_ignore=False):
    if not m["alive"]:
        return 0.0, False
    actual = float(raw) * (1.0 if armor_ignore else m["armor"])
    actual = min(actual, m["hp"])
    m["hp"] -= actual
    killed = m["hp"] <= 1e-9
    if killed:
        m["hp"] = 0.0
        m["alive"] = False
    return actual, killed


def spawn_splitter_children(fx, mobs, parent, geometry_flags):
    child = fx["monsterAnchors"]["SPLITTER"]["children"]
    born = []
    for j in range(int(child["count"])):
        row = {
            "id": f'{parent["id"]}_CHILD_{j + 1}',
            "type": "SPLITTER_CHILD",
            "x": parent["x"] + (j - 0.5) * 0.002,
            "lane": parent["lane"],
            "knight": geometry_flags.get("knight", parent.get("knight", False)),
            "archer": geometry_flags.get("archer", parent.get("archer", False)),
            "mage": geometry_flags.get("mage", parent.get("mage", False)),
            "hp": float(child["hp"]),
            "maxHp": float(child["hp"]),
            "speed": float(child["speed"]),
            "wall": float(child["wall"]),
            "knockResist": float(child["knockResist"]),
            "armor": float(child["armor"]),
            "alive": True,
            "spawned": True,
        }
        mobs.append(row)
        born.append(row["id"])
    return born


def finalize(before, after):
    return {
        "before": before,
        "after": after,
        "populationResetFraction": round(1 - after["liveCount"] / before["liveCount"], 6) if before["liveCount"] else 0,
        "hpResetFraction": round(1 - after["remainingHp"] / before["remainingHp"], 6) if before["remainingHp"] else 0,
        "wallBudgetResetFractionProxy": round(
            1 - after["remainingOneEventWallBudgetProxy"] / before["remainingOneEventWallBudgetProxy"], 6
        ) if before["remainingOneEventWallBudgetProxy"] else 0,
    }


def knight_probe(fx, snapshot, second_coeff):
    mobs = mob_instances(fx, snapshot)
    before = snapshot_metrics(mobs)
    f = fx["formulaReference"]
    root = f["basePxpDamage"] * f["knightRootMultiplier"]
    damage = 0.0
    kills = []
    wave_details = []
    for wave_index, coeff in enumerate((1.0, float(second_coeff)), start=1):
        eligible = sorted([m for m in alive(mobs) if m["knight"]], key=lambda z: (z["x"], z["lane"], z["id"]))[:4]
        wd = 0.0
        wk = []
        for m in eligible:
            dealt, killed = apply_hit(m, root * coeff)
            wd += dealt
            if killed:
                wk.append(m["id"])
                kills.append(m["id"])
                if m["type"] == "SPLITTER":
                    spawn_splitter_children(fx, mobs, m, {"knight": True, "archer": m["archer"], "mage": m["mage"]})
        damage += wd
        wave_details.append({"wave": wave_index, "coefficient": coeff, "targets": [m["id"] for m in eligible],
                             "damage": round(wd, 3), "kills": wk})
    after = snapshot_metrics(mobs)
    out = finalize(before, after)
    out.update({"rootRaw": round(root, 3), "secondWaveCoefficient": second_coeff,
                "totalDamage": round(damage, 3), "kills": kills, "waves": wave_details})
    return out


def rogue_probe(fx, snapshot, dagger_count):
    mobs = mob_instances(fx, snapshot)
    before = snapshot_metrics(mobs)
    f = fx["formulaReference"]
    raw = f["basePxpDamage"] * fx["lv31Candidates"]["Rogue"]["perDaggerCoefficient"]
    damage = 0.0
    kills = []
    sequence = []
    current = min(alive(mobs), key=lambda z: (z["x"], z["lane"], z["id"]))
    for i in range(int(dagger_count)):
        if current is None or not current["alive"]:
            pool = sorted(alive(mobs), key=lambda z: (z["x"], z["lane"], z["id"]))
            current = pool[0] if pool else None
        if current is None:
            break
        target_id = current["id"]
        dealt, killed = apply_hit(current, raw)
        damage += dealt
        sequence.append({"dagger": i + 1, "target": target_id, "damage": round(dealt, 3), "killed": killed})
        if killed:
            kills.append(target_id)
            if current["type"] == "SPLITTER":
                spawn_splitter_children(fx, mobs, current, {})
            current = None
    after = snapshot_metrics(mobs)
    out = finalize(before, after)
    out.update({"daggerCount": dagger_count, "perDaggerRaw": round(raw, 3),
                "totalDamage": round(damage, 3), "kills": kills, "sequence": sequence})
    return out


def tank_probe(fx, snapshot, damage_coeff, knock_mult):
    mobs = mob_instances(fx, snapshot)
    before = snapshot_metrics(mobs)
    f = fx["formulaReference"]
    raw = f["basePxpDamage"] * float(damage_coeff)
    damage = 0.0
    kills = []
    time_bought = []
    for m in list(alive(mobs)):
        dealt, killed = apply_hit(m, raw)
        damage += dealt
        if killed:
            kills.append(m["id"])
            if m["type"] == "SPLITTER":
                spawn_splitter_children(fx, mobs, m, {})
        else:
            dx = f["criticalKnockDistance"] * float(knock_mult) * m["knockResist"]
            seconds = dx / m["speed"] if m["speed"] > 0 else 0.0
            time_bought.append({"target": m["id"], "type": m["type"], "dx": round(dx, 6),
                                "baseTranslationSecondsBought": round(seconds, 3)})
    after = snapshot_metrics(mobs)
    out = finalize(before, after)
    vals = [x["baseTranslationSecondsBought"] for x in time_bought]
    out.update({
        "shockwaveDamageCoefficient": damage_coeff,
        "knockMultiplier": knock_mult,
        "shockwaveRawPerTarget": round(raw, 3),
        "totalDamage": round(damage, 3),
        "kills": kills,
        "wallShieldCandidate": fx["lv31Candidates"]["Tank"]["wallShield"],
        "wallShieldSecondsCandidate": fx["lv31Candidates"]["Tank"]["shieldSeconds"],
        "controlTimeBaseTranslationOnly": {
            "meanSeconds": round(statistics.mean(vals), 3) if vals else 0,
            "medianSeconds": round(statistics.median(vals), 3) if vals else 0,
            "maxSeconds": round(max(vals), 3) if vals else 0,
            "perSurvivor": time_bought,
        },
        "stateWatch": "CHARGER WINDUP cancellation and SIEGER reposition schedule are not reduced to this time proxy.",
    })
    return out


def archer_probe(fx, snapshot, coeff):
    mobs = mob_instances(fx, snapshot)
    before = snapshot_metrics(mobs)
    f = fx["formulaReference"]
    root = f["basePxpDamage"] * f["archerRootMultiplier"]
    raw = root * float(coeff)
    damage = 0.0
    kills = []
    targets = sorted([m for m in alive(mobs) if m["archer"]], key=lambda z: (z["x"], z["lane"], z["id"]))
    for m in targets:
        dealt, killed = apply_hit(m, raw, armor_ignore=True)
        damage += dealt
        if killed:
            kills.append(m["id"])
            if m["type"] == "SPLITTER":
                spawn_splitter_children(fx, mobs, m, {"archer": True})
    after = snapshot_metrics(mobs)
    out = finalize(before, after)
    out.update({"perTargetCoefficient": coeff, "rootRaw": round(root, 3), "rawPerTarget": round(raw, 3),
                "lineDepth": len(targets), "totalDamage": round(damage, 3), "kills": kills,
                "targets": [m["id"] for m in targets]})
    return out


def archer_continuity(fx):
    f = fx["formulaReference"]
    root = f["basePxpDamage"] * f["archerRootMultiplier"]
    lv26_per_target_coeff = fx["lv31Candidates"]["Archer"]["lv26TripleAggregatePerTarget"]
    max_targets = fx["lv31Candidates"]["Archer"]["lv26MaxTargetsPerArrow"]
    lv26_ceiling_units = lv26_per_target_coeff * max_targets
    rows = []
    for c in fx["lv31Candidates"]["Archer"]["lv31PerTargetCoefficients"]:
        break_even_depth = math.ceil(lv26_ceiling_units / c)
        rows.append({
            "lv31Coefficient": c,
            "durableTargetDamageVsLv26TriplePerTargetRatio": round(c / lv26_per_target_coeff, 6),
            "depthToMatchLv26FiveTargetIdealPackage": break_even_depth,
            "depth5PackageRatio": round((c * 5) / lv26_ceiling_units, 6),
            "depth8PackageRatio": round((c * 8) / lv26_ceiling_units, 6),
            "depth12PackageRatio": round((c * 12) / lv26_ceiling_units, 6),
        })
    return {
        "rootRaw": round(root, 3),
        "lv26TripleAggregateCoefficientPerDurableAlignedTarget": lv26_per_target_coeff,
        "lv26IdealFiveTargetPackageCoefficientUnits": lv26_ceiling_units,
        "lv26IdealFiveTargetRaw": round(root * lv26_ceiling_units, 3),
        "candidates": rows,
        "classificationAt1_00": "REVISE_POWER_MAGNITUDE",
        "workingContinuityCenter": 2.3,
        "reason": "2.30 = 1.00 + 0.65 + 0.65; compresses Lv21 Triple Shot per-target package into one final arrow before unlimited-depth escalation.",
    }


def mage_probe(fx, snapshot, stage_coeff):
    mobs = mob_instances(fx, snapshot)
    before = snapshot_metrics(mobs)
    f = fx["formulaReference"]
    root = f["basePxpDamage"] * f["mageRootMultiplier"]
    primary = min(alive(mobs), key=lambda z: (z["x"], z["lane"], z["id"]))
    damage = 0.0
    kills = []
    package_hit = set()
    chronology = []
    dealt, killed = apply_hit(primary, root)
    damage += dealt
    package_hit.add(primary["id"])
    row = {"event": "direct", "targets": [primary["id"]], "damage": round(dealt, 3), "kills": [], "spawned": []}
    if killed:
        row["kills"].append(primary["id"])
        kills.append(primary["id"])
        if primary["type"] == "SPLITTER":
            row["spawned"] += spawn_splitter_children(fx, mobs, primary, {"mage": primary["mage"]})
    chronology.append(row)
    for s in range(1, 4):
        stage_targets = sorted([m for m in alive(mobs) if m["mage"] and m["id"] != primary["id"]],
                               key=lambda z: (z["x"], z["lane"], z["id"]))
        event = {"event": f"stage{s}", "targets": [], "damage": 0.0, "kills": [], "spawned": []}
        for m in list(stage_targets):
            event["targets"].append(m["id"])
            dealt, killed = apply_hit(m, root * float(stage_coeff))
            event["damage"] += dealt
            damage += dealt
            package_hit.add(m["id"])
            if killed:
                event["kills"].append(m["id"])
                kills.append(m["id"])
                if m["type"] == "SPLITTER":
                    event["spawned"] += spawn_splitter_children(fx, mobs, m, {"mage": True})
        event["damage"] = round(event["damage"], 3)
        chronology.append(event)
    chain_targets = sorted([m for m in alive(mobs) if m["id"] not in package_hit],
                           key=lambda z: (z["x"], z["lane"], z["id"]))[:int(fx["lv31Candidates"]["Mage"]["finalChainMaxTargets"])]
    ce = {"event": "finalChain", "targets": [], "damage": 0.0, "kills": [], "spawned": []}
    for m in chain_targets:
        ce["targets"].append(m["id"])
        dealt, killed = apply_hit(m, root * fx["lv31Candidates"]["Mage"]["finalChainCoefficient"])
        ce["damage"] += dealt
        damage += dealt
        if killed:
            ce["kills"].append(m["id"])
            kills.append(m["id"])
            if m["type"] == "SPLITTER":
                ce["spawned"] += spawn_splitter_children(fx, mobs, m, {})
    ce["damage"] = round(ce["damage"], 3)
    chronology.append(ce)
    after = snapshot_metrics(mobs)
    out = finalize(before, after)
    out.update({"stageCoefficient": stage_coeff, "rootRaw": round(root, 3), "totalDamage": round(damage, 3),
                "kills": kills, "chronology": chronology})
    return out


def package_continuity(fx):
    base = fx["formulaReference"]["basePxpDamage"]
    knight_root = base * fx["formulaReference"]["knightRootMultiplier"]
    rogue_lv26_coeff = 1.0 + 4 * 0.45 + 0.45
    rogue_rows = []
    for n in fx["lv31Candidates"]["Rogue"]["daggerCounts"]:
        c = n * fx["lv31Candidates"]["Rogue"]["perDaggerCoefficient"]
        rogue_rows.append({"daggers": n, "lv31CoefficientUnits": round(c, 3),
                           "ratioVsLv26PxpPackage": round(c / rogue_lv26_coeff, 6),
                           "rawNoProcCrit": round(base * c, 3)})
    return {
        "Knight": {
            "rootRaw": round(knight_root, 3),
            "lv26IdealOneWaveFourTargetRaw": round(knight_root * 4, 3),
            "lv31TwoWaveCenterIdealFourTargetEachRaw": round(knight_root * 4 * 2, 3),
            "centerRatioVsLv26IdealOneWave": 2.0,
        },
        "Rogue": {
            "lv26PxpCoefficientUnitsNoProcCrit": rogue_lv26_coeff,
            "lv26PxpRawNoProcCrit": round(base * rogue_lv26_coeff, 3),
            "lv31Candidates": rogue_rows,
        },
        "Archer": archer_continuity(fx),
        "Mage": {
            "rootRaw": round(base * fx["formulaReference"]["mageRootMultiplier"], 3),
            "note": "Density value is fixture-dependent; final chain may be zero when all survivors were already hit.",
        },
    }


def run(fx):
    result = {
        "version": "p4d2-lv31-pressure-probe-result-v0.1",
        "status": "BOUNDED_DETERMINISTIC_DIAGNOSTIC_NO_NUMERICAL_FREEZE",
        "rng": "NONE",
        "fixtureVersion": fx["version"],
        "packageContinuity": package_continuity(fx),
        "snapshots": [],
    }
    for snap in fx["snapshots"]:
        row = {"id": snap["id"], "purpose": snap["purpose"], "initial": snapshot_metrics(mob_instances(fx, snap))}
        row["Knight"] = {str(c): knight_probe(fx, snap, c) for c in fx["lv31Candidates"]["Knight"]["secondWaveCoefficients"]}
        row["Rogue"] = {str(n): rogue_probe(fx, snap, n) for n in fx["lv31Candidates"]["Rogue"]["daggerCounts"]}
        row["Tank"] = {}
        for dc in fx["lv31Candidates"]["Tank"]["shockwaveCoefficients"]:
            row["Tank"][f"d{dc}_k2.5"] = tank_probe(fx, snap, dc, 2.5)
        for km in (2.0, 3.0):
            row["Tank"][f"d0.75_k{km}"] = tank_probe(fx, snap, 0.75, km)
        row["Archer"] = {str(c): archer_probe(fx, snap, c) for c in fx["lv31Candidates"]["Archer"]["lv31PerTargetCoefficients"]}
        row["Mage"] = {str(c): mage_probe(fx, snap, c) for c in fx["lv31Candidates"]["Mage"]["stageCoefficients"]}
        result["snapshots"].append(row)
    result["verdict"] = {
        "Knight": "CENTER_STRONG_CANDIDATE_CONTINUE_STATEFUL_PRESSURE_TEST",
        "Rogue": "16_DAGGER_CENTER_STRONG_CANDIDATE_CONTINUE",
        "Tank": "CONTROL_MAGNITUDE_REQUIRES_STATEFUL_CHARGER_SIEGER_TEST",
        "Archer": "STRUCTURE_PASS_MAGNITUDE_1_00_REVISE; 2_30_CONTINUITY_CENTER_FOR_NEXT_PROBE",
        "Mage": "0_75_CENTER_STRONG_DENSITY_CANDIDATE_CONTINUE_SPLITTER_ORDER_WATCH",
        "overall": "P4D2_CONTINUES_NO_FREEZE",
    }
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()
    fx = load(args.fixture)
    result = run(fx)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
