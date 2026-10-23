#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from copy import deepcopy
from pathlib import Path

CLASSES = ["Knight", "Rogue", "Tank", "Archer", "Mage"]

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def make_mob(row, cfg, proxy):
    typ = row["type"]
    if typ == "ARMORED_DURABLE_PROXY":
        a = {"hp": proxy["hp"], "armorMultiplier": proxy["armorMultiplier"], "knockResist": proxy["knockResist"]}
    else:
        a = cfg["existingMonsterAnchors"][typ]
    return {
        "type": typ, "x": float(row["x"]), "band": int(row["band"]),
        "hp": float(a["hp"]), "maxHp": float(a["hp"]),
        "armor": float(a["armorMultiplier"]), "knock": float(a["knockResist"]),
        "alive": True,
    }

def living(ms):
    return [m for m in ms if m["alive"]]

def nearest(ms):
    a = living(ms)
    return min(a, key=lambda m: (m["x"], m["band"], m["type"])) if a else None

def hit(m, raw, armor_ignore=False):
    if not m or not m["alive"]:
        return 0.0, False
    d = min(m["hp"], float(raw) * (1.0 if armor_ignore else m["armor"]))
    m["hp"] -= d
    if m["hp"] <= 1e-9:
        m["hp"] = 0.0
        m["alive"] = False
    return d, not m["alive"]

def simulate(cfg, scenario, cls, proxy):
    f = cfg["formulas"]
    ms = [make_mob(x, cfg, proxy) for x in scenario["mobs"]]
    damage = kills = durable_kills = 0

    def do_hit(m, raw, armor_ignore=False):
        nonlocal damage, kills, durable_kills
        d, k = hit(m, raw, armor_ignore)
        damage += d
        if k:
            kills += 1
            if m["type"] == "ARMORED_DURABLE_PROXY":
                durable_kills += 1
        return d, k

    if cls == "Knight":
        q = f["Knight"]
        for coeff in q["waves"]:
            p = nearest(ms)
            if not p:
                break
            ts = sorted(
                [m for m in ms if m["alive"] and abs(m["band"] - p["band"]) <= q["corridorBandRadius"] and m["x"] >= p["x"] - 1e-9],
                key=lambda m: (m["x"], abs(m["band"] - p["band"]), m["type"]),
            )[:q["maxTargetsPerWave"]]
            for m in ts:
                do_hit(m, q["root"] * coeff)

    elif cls == "Rogue":
        q = f["Rogue"]
        for _ in range(q["daggers"]):
            p = nearest(ms)
            if not p:
                break
            do_hit(p, q["perDaggerRaw"])

    elif cls == "Tank":
        q = f["Tank"]
        for m in list(living(ms)):
            do_hit(m, q["shockwaveRaw"])
            if m["alive"]:
                m["x"] += q["criticalKnockDistance"] * q["knockbackMultiplier"] * m["knock"]

    elif cls == "Archer":
        q = f["Archer"]
        p = nearest(ms)
        if p:
            ts = [m for m in ms if m["alive"] and abs(m["band"] - p["band"]) <= q["bandRadius"] and m["x"] >= p["x"] - 1e-9]
            for m in ts:
                do_hit(m, q["perTargetRaw"], q["armorIgnore"])

    elif cls == "Mage":
        q = f["Mage"]
        p = nearest(ms)
        if p:
            px, pb = p["x"], p["band"]
            do_hit(p, q["directRaw"])
            package = {id(p)}
            for _ in range(q["stages"]):
                ts = [m for m in ms if m["alive"] and m is not p and abs(m["x"] - px) <= q["xRadius"] and abs(m["band"] - pb) <= q["bandRadius"]]
                for m in list(ts):
                    do_hit(m, q["stageRaw"])
                    package.add(id(m))
            others = sorted(
                [m for m in ms if m["alive"] and id(m) not in package],
                key=lambda m: (m["x"], m["band"], m["type"]),
            )[:q["chainMax"]]
            for m in others:
                do_hit(m, q["chainRaw"])

    total = sum(m["maxHp"] for m in ms)
    remaining = sum(m["hp"] for m in ms if m["alive"])
    alive = [
        {"type": m["type"], "hp": round(m["hp"], 3), "x": round(m["x"], 4), "band": m["band"]}
        for m in ms if m["alive"]
    ]
    return {
        "damage": round(damage, 3),
        "kills": kills,
        "durableKills": durable_kills,
        "remainingHp": round(remaining, 3),
        "resetFraction": round(1.0 - remaining / total, 6),
        "alive": alive,
    }

def run(cfg):
    center = cfg["workingCenter"]
    scenarios = {}
    for s in cfg["scenarios"]:
        scenarios[s["id"]] = {c: simulate(cfg, s, c, center) for c in CLASSES}

    single = next(s for s in cfg["scenarios"] if s["id"] == "S1_SINGLE_DURABLE")
    sensitivity = []
    for hp in cfg["proxySensitivity"]["hp"]:
        for armor in cfg["proxySensitivity"]["armorMultiplier"]:
            proxy = dict(center)
            proxy["hp"] = hp
            proxy["armorMultiplier"] = armor
            row = {"hp": hp, "armorMultiplier": armor}
            for c in CLASSES:
                r = simulate(cfg, single, c, proxy)
                row[c] = {"kill": r["durableKills"] > 0, "remainingFraction": round(r["remainingHp"] / hp, 6)}
            sensitivity.append(row)

    c = scenarios["S1_SINGLE_DURABLE"]
    findings = {
        "KnightRemainingFraction": round(c["Knight"]["remainingHp"] / center["hp"], 6),
        "RogueKillsSingle": c["Rogue"]["durableKills"] == 1,
        "TankRemainingFraction": round(c["Tank"]["remainingHp"] / center["hp"], 6),
        "ArcherRemainingFraction": round(c["Archer"]["remainingHp"] / center["hp"], 6),
        "MageRemainingFraction": round(c["Mage"]["remainingHp"] / center["hp"], 6),
        "TankProxyPushDistance": round(cfg["formulas"]["Tank"]["criticalKnockDistance"] * cfg["formulas"]["Tank"]["knockbackMultiplier"] * center["knockResist"], 6),
    }
    cluster = scenarios["S2_CLUSTERED_3"]
    dist = scenarios["S3_DISTRIBUTED_3"]
    findings["MageClusterResetFraction"] = cluster["Mage"]["resetFraction"]
    findings["MageDistributedResetFraction"] = dist["Mage"]["resetFraction"]
    findings["ArcherClusterResetFraction"] = cluster["Archer"]["resetFraction"]
    findings["ArcherDistributedResetFraction"] = dist["Archer"]["resetFraction"]

    return {
        "version": "p4d2-armored-durable-proxy-result-v0.1",
        "status": "BOUNDED_DIAGNOSTIC_PROXY_NO_NUMERICAL_FREEZE",
        "fixtureVersion": cfg["version"],
        "workingCenter": center,
        "centerFindings": findings,
        "scenarios": scenarios,
        "singleProxySensitivity": sensitivity,
        "classification": {
            "durableAxisUsefulForTankMagePressure": findings["TankRemainingFraction"] > 0.75 and findings["MageRemainingFraction"] > 0.65,
            "rogueExecutionIdentityPreserved": findings["RogueKillsSingle"],
            "archerArmorIgnoreIdentityPreserved": findings["ArcherRemainingFraction"] < 0.10,
            "tankControlNotHardCountered": findings["TankProxyPushDistance"] > 0.05,
            "mageStillBenefitsFromClustering": findings["MageClusterResetFraction"] > findings["MageDistributedResetFraction"],
            "proxyIsNewMonsterAuthority": False,
        },
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", default="legacy-game-structure/data/p4d2_armored_durable_proxy_fixture_v0_1.json")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()
    result = run(load(args.fixture))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        Path(args.json_out).write_text(text, encoding="utf-8")
    print(text, end="")

if __name__ == "__main__":
    main()
