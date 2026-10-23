#!/usr/bin/env python3
"""Temporary bounded Stage48 real-monster chronology search.

Purpose:
- preserve physical right-edge spawn and all class/shop/monster coefficients;
- replace the Knight-only ARMORED_DURABLE_PROXY rows with existing real archetypes only;
- vary frontmost screening / relative entry time at the current Stage48 cycle;
- evaluate under canonical STAGE_SETTLED semantics.

Execution-only diagnostic. No candidate adoption, no numerical freeze, no production authority.
"""
from __future__ import annotations

import copy
import json
from collections import defaultdict
from pathlib import Path

import run_p5_identity_aware_stage46_49_integrated_probe_v0_1 as integ
import run_p5_identity_aware_stage46_49_stage_settled_probe_v0_1 as settled

REAL_TYPES = {"BRUTE", "CHARGER", "FLYER", "GRUNT", "RUNNER", "SHIELD", "SIEGER", "SPLITTER", "SUPPORTER"}


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def row(typ, band, reference_offset, spawn_lead):
    assert typ in REAL_TYPES
    return {
        "type": typ,
        "band": int(band),
        "referenceOffset": float(reference_offset),
        "spawnLeadSeconds": float(spawn_lead),
    }


def packet_with(screen_rows, sieger_row):
    # Preserve the current light trailing pressure rows so only the screening/entry structure changes.
    return list(screen_rows) + [sieger_row,
        row("RUNNER", -1, 2.8, 0.0),
        row("CHARGER", 1, 3.4, 0.0),
    ]


def variants(base_direction):
    out = {}

    def add(name, screen_rows, sieger_row):
        d = copy.deepcopy(base_direction)
        s48 = d["stageDirection"]["48"]
        # Keep current Stage48 cycle fixed. This lane isolates chronology/screening first.
        assert abs(float(s48["pressureCycleSecondsCandidate"]) - 4.9) < 1e-9
        s48["diagnosticPacket"] = packet_with(screen_rows, sieger_row)
        s48["note"] = f"TEMP_REAL_MONSTER_CHRONOLOGY_SEARCH:{name}"
        integ.validate_right_edge_contract(d)
        for r in s48["diagnosticPacket"]:
            assert r["type"] in REAL_TYPES
            assert "spawnX" not in r
        out[name] = d

    # Control: direct one-for-one real BRUTE substitution at the failed proxy timing.
    add("BRUTE_PAIR_EQUIV", [
        row("BRUTE", -2, 0.0, 7.0),
        row("BRUTE", 2, 1.0, 5.0),
    ], row("SIEGER", 0, 2.0, 6.0))

    # Two BRUTEs arrive only ~1-1.5s before the SIEGER instead of leaving one escort exposed alone.
    add("BRUTE_PAIR_TIGHT_SCREEN", [
        row("BRUTE", -1, 0.0, 5.5),   # first-cycle spawn ~6.5s
        row("BRUTE", 1, 0.5, 5.5),    # ~7.0s
    ], row("SIEGER", 0, 2.0, 6.0))    # ~8.0s

    # Three real BRUTEs form a short-lived front line; no stat/durability changes.
    add("BRUTE_TRIPLE_TIGHT_SCREEN", [
        row("BRUTE", -1, 0.0, 6.0),   # ~6.0s
        row("BRUTE", 0, 0.3, 5.8),    # ~6.5s
        row("BRUTE", 1, 0.6, 5.6),    # ~7.0s
    ], row("SIEGER", 0, 2.0, 6.0))

    # Layer a durable BRUTE with faster SHIELD bodies close to the SIEGER entry.
    add("BRUTE_SHIELD_LAYER", [
        row("BRUTE", 0, 0.0, 6.0),    # ~6.0s
        row("SHIELD", -1, 0.4, 5.4),  # ~7.0s
        row("SHIELD", 1, 0.7, 5.4),   # ~7.3s
    ], row("SIEGER", 0, 2.0, 6.0))

    # Two BRUTEs plus one late SHIELD: protects the approach without making all screeners high-HP.
    add("BRUTE_PAIR_LATE_SHIELD", [
        row("BRUTE", -1, 0.0, 6.0),   # ~6.0s
        row("BRUTE", 1, 0.4, 5.9),    # ~6.5s
        row("SHIELD", 0, 0.8, 5.6),   # ~7.2s
    ], row("SIEGER", 0, 2.0, 6.0))

    # Timing sensitivity around the two-BRUTE screen: SIEGER reaches the packet sooner.
    add("BRUTE_PAIR_EARLY_SIEGER", [
        row("BRUTE", -1, 0.0, 5.5),
        row("BRUTE", 1, 0.5, 5.5),
    ], row("SIEGER", 0, 1.5, 6.0))    # ~7.5s

    # Timing sensitivity in the opposite direction: more front-line separation.
    add("BRUTE_PAIR_LATE_SIEGER", [
        row("BRUTE", -1, 0.0, 5.5),
        row("BRUTE", 1, 0.5, 5.5),
    ], row("SIEGER", 0, 3.0, 6.0))    # ~9.0s

    return out


def summarize_variant(rows):
    s48_rows = []
    for r in rows:
        s48 = next((s for s in r["stages"] if s["stage"] == 48), None)
        if s48:
            s48_rows.append((r, s48))

    per_class = {}
    for cls in integ.CLASSES:
        cr = [(r, s) for r, s in s48_rows if r["class"] == cls]
        shots = [int(s.get("siegerShots") or 0) for _, s in cr]
        walls = [float(s.get("endWall") or 0.0) for _, s in cr]
        settles = [float(s.get("settleSeconds") or 0.0) for _, s in cr if s.get("settleSeconds") is not None]
        per_class[cls] = {
            "rows": len(cr),
            "siegerShotCases": sum(v > 0 for v in shots),
            "totalSiegerShots": sum(shots),
            "minStage48EndWall": round(min(walls), 3) if walls else None,
            "maxStage48EndWall": round(max(walls), 3) if walls else None,
            "maxStage48SettleSeconds": round(max(settles), 3) if settles else None,
        }

    burials = []
    for r, s in s48_rows:
        if s.get("buried") or not s.get("settled"):
            burials.append({
                "class": r["class"], "profile": r["profile"],
                "burialTime": s.get("burialTime"), "endWall": s.get("endWall"),
                "endActive": s.get("endActive"),
            })

    shot_cases = [int(s.get("siegerShots") or 0) for _, s in s48_rows]
    return {
        "settledThroughStage49Count": sum(bool(r["settledThroughStage49"]) for r in rows),
        "totalRows": len(rows),
        "stage48BurialsOrUnsettled": burials,
        "stage48SiegerShotCases": sum(v > 0 for v in shot_cases),
        "stage48TotalSiegerShots": sum(shot_cases),
        "stage48MaxSiegerShotsOneRow": max(shot_cases) if shot_cases else 0,
        "perClass": per_class,
    }


def main():
    base = load("legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json")
    base_temporal = load("legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json")
    stage49 = load("legacy-game-structure/data/p4d2_stage49_full_rotation_fixture_v0_1.json")
    direction = load("legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json")
    shop = load("legacy-game-structure/data/p5_all_class_fixed_rank_shop_stage49_fixture_v0_1.json")
    refinement = load("legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json")
    integration = load("legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json")

    integ.validate_right_edge_contract(direction)
    base = integ.inject_diagnostic_monsters(base, stage49)
    if "ARMORED_DURABLE_PROXY" not in base["monsterAnchors"]:
        base["monsterAnchors"]["ARMORED_DURABLE_PROXY"] = dict(refinement["knightRobustPair"]["anchor"])

    settled.install_fixed_schedule_hook()
    scale = float(integration["shopEffectScale"])
    profiles = list(integration["representativeShopProfiles"])

    output = {
        "version": "p5-stage48-real-monster-chronology-search-temp-v0.1",
        "sourceCanonicalHead": "33cac0072964c620383ddb3c71e3d6ac75e71a98",
        "status": "TEMP_BOUNDED_SEARCH_NO_CANDIDATE_ADOPTION_NO_NUMERICAL_FREEZE",
        "physicalSpawnX": direction["globalRules"]["normalRightEdgeSpawnX"],
        "stage48CycleSecondsHeldFixed": direction["stageDirection"]["48"]["pressureCycleSecondsCandidate"],
        "tankCoefficientForCrossClassSearch": 0.25,
        "variants": {},
    }

    for name, d in variants(direction).items():
        rows = []
        for profile in profiles:
            for cls in integ.CLASSES:
                coeff = 0.25 if cls == "Tank" else None
                rows.append(settled.run_chain(
                    base, base_temporal, d, shop, integration,
                    cls, profile, scale, coeff,
                ))
        output["variants"][name] = {
            "stage48Packet": d["stageDirection"]["48"]["diagnosticPacket"],
            "aggregate": summarize_variant(rows),
            "rows": rows,
        }

    text = json.dumps(output, indent=2, sort_keys=True)
    Path("p5_stage48_real_monster_chronology_search_temp.json").write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
