#!/usr/bin/env python3
"""Timing Defense P4-D2 stateful temporal Stage46 pressure stress probe.

Boundaries:
- deterministic / no RNG
- current nine-roster provisional anchors from the committed P4-D2 base fixture
- diagnostic five-band geometry abstraction, not production lanes/collision geometry
- diagnostic 60s stress recipe, not exact Stage46 authoring
- no production numerical freeze
"""
from __future__ import annotations

import argparse
import heapq
import json
from dataclasses import dataclass
from pathlib import Path


def load(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


@dataclass
class Mob:
    id: str
    typ: str
    hp: float
    max_hp: float
    speed: float
    wall: float
    armor: float
    knock: float
    band: int
    x: float
    state: str = "ADVANCE"
    windup_until: float = 0.0
    cooldown_until: float = 0.0
    rearm_until: float = 0.0
    alive: bool = True
    spawned: bool = False


def build_schedule(cfg):
    sim = cfg["simulation"]
    patterns = cfg["pressurePatterns"]
    duration = float(sim["durationSeconds"])
    cycle = float(sim["pressureCycleSeconds"])
    out = []
    c = 0
    t = 0.0
    while t < duration:
        for row in patterns[c % len(patterns)]:
            st = t + float(row["offset"])
            if st < duration:
                out.append((st, row["type"], int(row["band"])))
        c += 1
        t += cycle
    return sorted(out)


def make_mob(mon, cfg, typ, band, idx):
    spawn_x = float(cfg["simulation"]["spawnX"])
    if typ == "SPLITTER_CHILD":
        a = mon["SPLITTER"]["children"]
        return Mob(
            f"{typ}_{idx}", typ, float(a["hp"]), float(a["hp"]),
            float(a["speed"]), float(a["wall"]), float(a["armor"]),
            float(a["knockResist"]), band, spawn_x, spawned=True,
        )
    a = mon[typ]
    return Mob(
        f"{typ}_{idx}", typ, float(a["hp"]), float(a["hp"]),
        float(a["speed"]), float(a["wall"]), float(a["armor"]),
        float(a["knockResist"]), band, spawn_x,
    )


def living(mobs):
    return [m for m in mobs if m.alive]


def nearest(mobs):
    a = living(mobs)
    return min(a, key=lambda m: (m.x, m.band, m.id)) if a else None


def lane_targets(mobs, band, radius=0, min_x=-99.0, max_n=None):
    a = sorted(
        [m for m in mobs if m.alive and abs(m.band - band) <= radius and m.x >= min_x],
        key=lambda m: (m.x, abs(m.band - band), m.id),
    )
    return a if max_n is None else a[:max_n]


def corridor_targets(mobs, primary, band_radius=1, max_n=4):
    return sorted(
        [
            m for m in mobs
            if m.alive and abs(m.band - primary.band) <= band_radius and m.x >= primary.x - 0.001
        ],
        key=lambda m: (m.x, abs(m.band - primary.band), m.id),
    )[:max_n]


def nearby(mobs, px, pband, x_radius, band_radius, exclude=None, max_n=None):
    a = sorted(
        [
            m for m in mobs
            if m.alive and m is not exclude
            and abs(m.x - px) <= x_radius
            and abs(m.band - pband) <= band_radius
        ],
        key=lambda m: (abs(m.x - px), abs(m.band - pband), m.id),
    )
    return a if max_n is None else a[:max_n]


def hit(mon, cfg, mobs, m, raw, stats, counter, armor_ignore=False):
    if not m or not m.alive:
        return 0.0, False
    actual = min(m.hp, float(raw) * (1.0 if armor_ignore else m.armor))
    m.hp -= actual
    stats["damage"] += actual
    killed = m.hp <= 1e-9
    if killed:
        m.hp = 0.0
        m.alive = False
        stats["kills"] += 1
        stats["killsByType"][m.typ] = stats["killsByType"].get(m.typ, 0) + 1
        if m.typ == "SPLITTER":
            stats["splitterParentsKilled"] += 1
            ch = mon["SPLITTER"]["children"]
            for j in range(int(ch["count"])):
                counter[0] += 1
                child = make_mob(mon, cfg, "SPLITTER_CHILD", m.band, counter[0])
                child.x = m.x + (j - 0.5) * 0.002
                mobs.append(child)
                stats["splitterChildrenSpawned"] += 1
    return actual, killed


def basic_knock(tier):
    if tier == "CRITICAL":
        return 0.047
    if tier in ("PERFECT", "SUPER"):
        return 0.024
    if tier in ("GOOD", "GREAT"):
        return 0.013
    return 0.006


def push(m, tier, mul, now, stats):
    if not m or not m.alive:
        return
    dx = basic_knock(tier) * m.knock * float(mul)
    m.x = min(1.08, m.x + dx)

    if m.typ == "CHARGER" and m.state == "WINDUP":
        m.state = "ADVANCE"
        m.windup_until = 0.0
        m.rearm_until = now + 0.900
        stats["chargerInterrupts"] += 1

    if m.typ == "SIEGER" and m.state in ("SIEGE_WINDUP", "SIEGE_COOLDOWN") and m.x > 0.38:
        m.state = "ADVANCE"
        m.windup_until = 0.0
        m.cooldown_until = 0.0
        stats["siegerRepositions"] += 1


def center_candidates(base, temporal, cls):
    c = temporal["lv31TemporalCenters"][cls]
    return dict(c)


def simulate(base, temporal, cls, has_lv31=True, missed_heavy_indices=(), overrides=None):
    mon = base["monsterAnchors"]
    cfg = temporal
    sim = cfg["simulation"]
    geom = cfg["geometryAbstraction"]
    cand = center_candidates(base, cfg, cls)
    if overrides:
        cand.update(overrides)

    duration = float(sim["durationSeconds"])
    dt = float(sim["dtSeconds"])
    wall_max = float(sim["wallHp"])
    schedule = build_schedule(cfg)
    si = 0
    mobs = []
    counter = [0]
    events = []
    event_seq = 0

    stats = {
        "class": cls,
        "hasLv31": has_lv31,
        "missedHeavyIndices": list(missed_heavy_indices),
        "damage": 0.0,
        "kills": 0,
        "killsByType": {},
        "wall": wall_max,
        "shield": 0.0,
        "shieldUntil": 0.0,
        "maxActive": 0,
        "endActive": 0,
        "wallHits": 0,
        "pxpCount": 0,
        "heavyMissCount": 0,
        "burialTime": None,
        "chargerWindups": 0,
        "chargerInterrupts": 0,
        "chargerCharges": 0,
        "siegerWindups": 0,
        "siegerShots": 0,
        "siegerRepositions": 0,
        "splitterParentsKilled": 0,
        "splitterChildrenSpawned": 0,
        "aftershockZones": [],
    }

    def schedule_event(at, fn):
        nonlocal event_seq
        event_seq += 1
        heapq.heappush(events, (at, event_seq, fn))

    def do_knight(now, base_damage, heavy, final, tier, primary):
        mult = 1.12 * 1.18 * (1.20 if heavy else 1.0)
        raw = base_damage * mult
        if final:
            root = 600 * 1.12 * 1.18 * 1.20
            band_radius = int(geom["knightHeavyBandRadius"])

            def wave(coeff):
                p = nearest(mobs)
                if not p:
                    return
                for target in corridor_targets(mobs, p, band_radius, 4):
                    hit(mon, cfg, mobs, target, root * coeff, stats, counter)
                    push(target, "CRITICAL", 1.20, now, stats)

            wave(1.0)
            schedule_event(
                now + float(cand["secondWaveDelaySeconds"]),
                lambda: wave(float(cand["secondWaveCoefficient"])),
            )
            return

        p = primary
        if not p:
            return
        hit(mon, cfg, mobs, p, raw, stats, counter)
        push(p, tier, 1.20, now, stats)
        n_extra = 3 if heavy else 1
        extras = [m for m in corridor_targets(mobs, p, int(geom["knightHeavyBandRadius"]), 4) if m is not p][:n_extra]
        for j, target in enumerate(extras):
            hit(mon, cfg, mobs, target, raw, stats, counter)
            kb = 1.20 * (1 + 0.15 * (j + 1) if heavy else 1.0)
            push(target, tier, kb, now, stats)

    def do_rogue(now, base_damage, heavy, final, primary):
        if final:
            n = int(cand["daggers"])
            duration_storm = float(cand["stormDurationSeconds"])
            raw = 600 * float(cand["perDaggerCoefficient"])
            denom = max(1, n - 1)
            for k in range(n):
                def dagger():
                    p = nearest(mobs)
                    if p:
                        hit(mon, cfg, mobs, p, raw, stats, counter)
                schedule_event(now + k * duration_storm / denom, dagger)
            return

        p = primary
        if not p:
            return
        hit(mon, cfg, mobs, p, base_damage, stats, counter)
        if heavy:
            for _ in range(4):
                q = p if p and p.alive else nearest(mobs)
                if q:
                    hit(mon, cfg, mobs, q, base_damage * 0.45, stats, counter)
        else:
            q = p if p and p.alive else nearest(mobs)
            if q:
                hit(mon, cfg, mobs, q, base_damage * 0.55, stats, counter)

        root_primary = p
        secondaries = sorted(
            [m for m in mobs if m.alive and m is not root_primary],
            key=lambda m: (m.x, m.band, m.id),
        )
        if secondaries:
            hit(mon, cfg, mobs, secondaries[0], base_damage * 0.45, stats, counter)

    def do_tank(now, base_damage, heavy, final, tier, primary):
        if final:
            raw = 600 * float(cand["shockwaveCoefficient"])
            for target in list(living(mobs)):
                hit(mon, cfg, mobs, target, raw, stats, counter)
                push(target, "CRITICAL", float(cand["knockbackMultiplier"]), now, stats)
            stats["shield"] = float(cand["barrier"])
            stats["shieldUntil"] = now + float(cand["barrierSeconds"])
            if primary:
                stats["aftershockZones"].append((now + 1.5, primary.x, primary.band))
            return

        p = primary
        if not p:
            return
        hit(mon, cfg, mobs, p, base_damage, stats, counter)
        push(p, tier, 2.0 if heavy else 1.30, now, stats)
        if heavy:
            for target in [
                m for m in mobs
                if m.alive and m is not p and abs(m.x - p.x) <= 0.16 and abs(m.band - p.band) <= 1
            ]:
                hit(mon, cfg, mobs, target, base_damage, stats, counter)
                push(target, tier, 2.0, now, stats)
            stats["aftershockZones"].append((now + 1.5, p.x, p.band))
        if not heavy and tier == "PERFECT":
            stats["shield"] = 80.0
            stats["shieldUntil"] = now + 3.0

    def do_archer(now, base_damage, heavy, final, primary):
        if not primary:
            return
        root = base_damage * 1.10
        band = primary.band
        if final:
            radius = int(cand["workingBandRadius"])
            raw = 660 * float(cand["perTargetCoefficient"])
            for target in list(lane_targets(mobs, band, radius=radius)):
                hit(mon, cfg, mobs, target, raw, stats, counter, armor_ignore=True)
            return

        coeffs = [1.0, 0.65, 0.65] if heavy else [1.0]
        radius = int(geom["archerLv26BandRadius"])
        for coeff in coeffs:
            for target in list(lane_targets(mobs, band, radius=radius, max_n=5)):
                hit(mon, cfg, mobs, target, root * coeff, stats, counter, armor_ignore=True)

    def do_mage(now, base_damage, heavy, final, primary):
        if not primary:
            return
        if final:
            px, pb = primary.x, primary.band
            hit(mon, cfg, mobs, primary, 720, stats, counter)
            package_hit = {primary.id}
            radius = 0.105 * 1.35 * 1.60 * float(cand["radiusMultiplier"])
            band_radius = int(geom["mageHeavyFinalBandRadius"])

            def blast(stage):
                targets = nearby(mobs, px, pb, radius, band_radius, exclude=primary)
                for target in list(targets):
                    hit(mon, cfg, mobs, target, 720 * float(cand["stageCoefficient"]), stats, counter)
                    package_hit.add(target.id)
                if stage == 3:
                    secondaries = sorted(
                        [m for m in mobs if m.alive and m.id not in package_hit],
                        key=lambda m: (m.x, m.band, m.id),
                    )[:2]
                    for target in secondaries:
                        hit(mon, cfg, mobs, target, 720 * 0.35, stats, counter)

            delays = [float(x) for x in cand["stageDelaysSeconds"]]
            blast(1)
            schedule_event(now + delays[1], lambda: blast(2))
            schedule_event(now + delays[2], lambda: blast(3))
            return

        root = base_damage * (1.20 if heavy else 1.0)
        px, pb = primary.x, primary.band
        hit(mon, cfg, mobs, primary, root, stats, counter)
        radius = 0.105 * 1.35 * (1.60 if heavy else 1.0)
        band_radius = int(geom["mageHeavyFinalBandRadius"] if heavy else geom["mageNormalBandRadius"])
        immediate = nearby(mobs, px, pb, radius, band_radius, exclude=primary, max_n=3)
        hit_ids = {primary.id}
        for target in immediate:
            hit(mon, cfg, mobs, target, root * 0.60, stats, counter)
            hit_ids.add(target.id)

        def resonance():
            for target in nearby(mobs, px, pb, radius, band_radius, exclude=primary, max_n=4):
                hit(mon, cfg, mobs, target, root * 0.55, stats, counter)

        schedule_event(now + 0.18, resonance)
        if len(hit_ids) >= 2:
            secondaries = sorted(
                [m for m in mobs if m.alive and m.id not in hit_ids],
                key=lambda m: (m.x, m.band, m.id),
            )[:2]
            for target in secondaries:
                hit(mon, cfg, mobs, target, root * 0.35, stats, counter)

    now = 0.0
    next_attack = float(sim["firstRootAttackSeconds"])
    root_interval = float(sim["rootAttackIntervalSeconds"])
    heavy_every = int(sim["heavyEveryRootActions"])
    attack_no = 0
    heavy_index = 0

    while now <= duration + 1e-9:
        while si < len(schedule) and schedule[si][0] <= now + 1e-9:
            _, typ, band = schedule[si]
            counter[0] += 1
            mobs.append(make_mob(mon, cfg, typ, band, counter[0]))
            si += 1

        while events and events[0][0] <= now + 1e-9:
            _, _, fn = heapq.heappop(events)
            fn()

        if stats["shield"] > 0 and now >= stats["shieldUntil"]:
            stats["shield"] = 0.0

        if now >= next_attack - 1e-9 and nearest(mobs):
            attack_no += 1
            heavy = attack_no % heavy_every == 0
            if heavy:
                heavy_index += 1
            is_miss = heavy and heavy_index in missed_heavy_indices
            tier = "SUPER" if is_miss else ("CRITICAL" if heavy else "PERFECT")
            base_damage = 400 if is_miss else (600 if heavy else 200)
            if heavy and not is_miss:
                stats["pxpCount"] += 1
            if is_miss:
                stats["heavyMissCount"] += 1
            primary = nearest(mobs)
            final = has_lv31 and heavy and not is_miss

            if cls == "Knight":
                do_knight(now, base_damage, heavy, final, tier, primary)
            elif cls == "Rogue":
                do_rogue(now, base_damage, heavy, final, primary)
            elif cls == "Tank":
                do_tank(now, base_damage, heavy, final, tier, primary)
            elif cls == "Archer":
                do_archer(now, base_damage, heavy, final, primary)
            elif cls == "Mage":
                do_mage(now, base_damage, heavy, final, primary)
            else:
                raise ValueError(cls)

            next_attack += root_interval

        live_now = living(mobs)
        stats["aftershockZones"] = [z for z in stats["aftershockZones"] if z[0] > now]
        supporters = [m for m in live_now if m.typ == "SUPPORTER"]

        for m in list(live_now):
            if m.typ == "CHARGER":
                if m.state == "ADVANCE" and m.x <= 0.62 and now >= m.rearm_until:
                    m.state = "WINDUP"
                    m.windup_until = now + 0.650
                    stats["chargerWindups"] += 1
                elif m.state == "WINDUP" and now >= m.windup_until:
                    m.state = "CHARGE"
                    stats["chargerCharges"] += 1

            if m.typ == "SIEGER":
                if m.state == "ADVANCE" and m.x <= 0.38:
                    m.state = "SIEGE_WINDUP"
                    m.windup_until = now + 0.800
                    stats["siegerWindups"] += 1
                elif m.state == "SIEGE_WINDUP" and now >= m.windup_until:
                    incoming = 75.0
                    absorb = min(stats["shield"], incoming) if now < stats["shieldUntil"] else 0.0
                    stats["shield"] -= absorb
                    stats["wall"] -= incoming - absorb
                    stats["siegerShots"] += 1
                    m.state = "SIEGE_COOLDOWN"
                    m.cooldown_until = now + 2.200
                elif m.state == "SIEGE_COOLDOWN" and now >= m.cooldown_until:
                    m.state = "SIEGE_WINDUP"
                    m.windup_until = now + 0.800
                    stats["siegerWindups"] += 1

            if m.typ == "SIEGER" and m.state in ("SIEGE_WINDUP", "SIEGE_COOLDOWN"):
                speed = 0.0
            elif m.typ == "CHARGER" and m.state == "WINDUP":
                speed = 0.0
            elif m.typ == "CHARGER" and m.state == "CHARGE":
                speed = 0.210
            else:
                speed = m.speed

            if speed > 0:
                if m.typ != "SUPPORTER" and any(
                    s.alive and abs(s.x - m.x) <= 0.18 and abs(s.band - m.band) <= 1
                    for s in supporters
                ):
                    speed *= 1.18

                if cls == "Tank" and any(
                    abs(zx - m.x) <= 0.16 and abs(zb - m.band) <= 1
                    for _, zx, zb in stats["aftershockZones"]
                ):
                    speed *= 0.75

                m.x -= speed * dt

            if m.x <= 0.155 and m.alive:
                incoming = m.wall * (0.90 if cls == "Tank" else 1.0)
                absorb = min(stats["shield"], incoming) if now < stats["shieldUntil"] else 0.0
                stats["shield"] -= absorb
                stats["wall"] -= incoming - absorb
                stats["wallHits"] += 1
                m.alive = False

        active = len(living(mobs))
        stats["maxActive"] = max(stats["maxActive"], active)

        if stats["wall"] <= 0:
            stats["wall"] = 0.0
            stats["burialTime"] = round(now, 3)
            break

        now += dt

    stats["endActive"] = len(living(mobs))
    stats["endWall"] = round(max(0.0, stats["wall"]), 3)
    stats["damage"] = round(stats["damage"], 3)
    stats["durationSimulated"] = round(min(now, duration), 3)
    stats.pop("shield", None)
    stats.pop("shieldUntil", None)
    stats.pop("aftershockZones", None)
    return stats


def slim(row):
    keys = [
        "endWall", "endActive", "maxActive", "kills", "burialTime",
        "wallHits", "pxpCount", "heavyMissCount",
        "chargerWindups", "chargerInterrupts", "chargerCharges",
        "siegerWindups", "siegerShots", "siegerRepositions",
        "splitterParentsKilled", "splitterChildrenSpawned",
    ]
    return {k: row.get(k) for k in keys}


def run_all(base, temporal):
    classes = ["Knight", "Rogue", "Tank", "Archer", "Mage"]
    miss = temporal["simulation"]["missHeavyIndices"]
    main = {}
    for cls in classes:
        main[cls] = {
            "LV26_ALL_PERFECT": slim(simulate(base, temporal, cls, False, ())),
            "LV31_ALL_PXP": slim(simulate(base, temporal, cls, True, ())),
            "LV31_ONE_MISS": slim(simulate(base, temporal, cls, True, tuple(miss["oneMiss"]))),
            "LV31_TWO_CONSECUTIVE_MISS": slim(
                simulate(base, temporal, cls, True, tuple(miss["twoConsecutiveMisses"]))
            ),
        }

    sensitivity = {"Knight": {}, "Rogue": {}, "Tank": {}, "Archer": {}, "Mage": {}}

    for c in (0.75, 1.0, 1.25):
        sensitivity["Knight"][f"secondWave_{c}"] = slim(
            simulate(base, temporal, "Knight", True, (), {"secondWaveCoefficient": c})
        )

    for n in temporal["lv31TemporalCenters"]["Rogue"]["countSensitivity"]:
        sensitivity["Rogue"][f"daggers_{n}"] = slim(
            simulate(base, temporal, "Rogue", True, (), {"daggers": n})
        )

    tank = temporal["lv31TemporalCenters"]["Tank"]
    for d in tank["damageSensitivity"]:
        sensitivity["Tank"][f"damage_{d}_knock_2.5"] = slim(
            simulate(base, temporal, "Tank", True, (), {"shockwaveCoefficient": d, "knockbackMultiplier": 2.5})
        )
    for k in tank["knockbackSensitivity"]:
        sensitivity["Tank"][f"damage_0.75_knock_{k}"] = slim(
            simulate(base, temporal, "Tank", True, (), {"shockwaveCoefficient": 0.75, "knockbackMultiplier": k})
        )

    arch = temporal["lv31TemporalCenters"]["Archer"]
    for width in arch["widthSensitivity"]:
        for c in arch["coefficientSensitivity"]:
            sensitivity["Archer"][f"width_{width}_coeff_{c}"] = slim(
                simulate(base, temporal, "Archer", True, (), {"workingBandRadius": width, "perTargetCoefficient": c})
            )

    mage = temporal["lv31TemporalCenters"]["Mage"]
    for c in mage["stageSensitivity"]:
        sensitivity["Mage"][f"stage_{c}_radius_1.25"] = slim(
            simulate(base, temporal, "Mage", True, (), {"stageCoefficient": c, "radiusMultiplier": 1.25})
        )
    for r in mage["radiusSensitivity"]:
        sensitivity["Mage"][f"stage_0.75_radius_{r}"] = slim(
            simulate(base, temporal, "Mage", True, (), {"stageCoefficient": 0.75, "radiusMultiplier": r})
        )

    all_lv26_buried = all(main[c]["LV26_ALL_PERFECT"]["burialTime"] is not None for c in classes)
    all_lv31_survive = all(main[c]["LV31_ALL_PXP"]["burialTime"] is None for c in classes)

    return {
        "version": "p4d2-stage46-temporal-pressure-result-v0.1",
        "status": "BOUNDED_STATEFUL_STRESS_DIAGNOSTIC_NO_NUMERICAL_FREEZE",
        "rng": "NONE",
        "fixtureVersion": temporal["version"],
        "mainScenarios": main,
        "sensitivity": sensitivity,
        "gateSeparation": {
            "allFiveLv26AllPerfectBuriedWithin60s": all_lv26_buried,
            "allFiveLv31AllPxpSurvive60s": all_lv31_survive,
            "lv26BurialTimesSeconds": {c: main[c]["LV26_ALL_PERFECT"]["burialTime"] for c in classes},
            "lv31EndWall": {c: main[c]["LV31_ALL_PXP"]["endWall"] for c in classes},
            "classification": "CANDIDATE_PRESSURE_ENVELOPE_FOUND" if all_lv26_buried and all_lv31_survive else "REVISE_PRESSURE_ENVELOPE",
        },
        "interpretation": {
            "Rogue": "12 daggers buries in this stress recipe; 16 survives under pressure; 20 largely clears the recipe. 16 remains the useful center.",
            "Archer": "Coefficient increase alone cannot rescue strict-width final in dispersed pressure. A modest wider straight collision corridor is the dominant missing axis; this is a P4-D2 geometry candidate, not a freeze.",
            "Knight": "Second wave 1.00 is a meaningful threshold; 1.25 largely saturates this recipe.",
            "Tank": "0.75 damage center materially reduces backlog; knockback 2.5 remains a reasonable center but role-aligned interrupt probes are still needed.",
            "Mage": "0.75 stage center improves backlog over 0.55 while 1.00 largely saturates; radius/chronology remain active axes.",
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--base-fixture",
        default="legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json",
    )
    ap.add_argument(
        "--temporal-fixture",
        default="legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json",
    )
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()
    base = load(args.base_fixture)
    temporal = load(args.temporal_fixture)
    result = run_all(base, temporal)
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
