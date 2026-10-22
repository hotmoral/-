#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

REFERENCE_RAW_HITS = [100, 140, 200, 600]
KNOCK_RESIST = {
    "GRUNT": 0.85,
    "RUNNER": 1.00,
    "BRUTE": 0.38,
    "SHIELD": 0.62,
    "FLYER": 0.90,
}


def hits_to_kill(hp: float, armor_multiplier: float, raw: int) -> int:
    actual = max(1, round(raw * armor_multiplier))
    return math.ceil(hp / actual)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("kinematic_anchor", type=Path)
    p.add_argument("combat_anchor", type=Path)
    args = p.parse_args()

    kin = yaml.safe_load(args.kinematic_anchor.read_text(encoding="utf-8"))
    combat = yaml.safe_load(args.combat_anchor.read_text(encoding="utf-8"))

    world = kin["world"]
    move = kin["monsters"]
    stats = combat["monsters"]
    travel = float(world["spawnX"]) - float(world["wallX"])

    grunt_speed = float(move["GRUNT"]["speed"])
    runner_speed = float(move["RUNNER"]["speed"])
    grunt_t = travel / grunt_speed
    runner_t = travel / runner_speed

    brute_hp = float(stats["BRUTE"]["hp"])
    grunt_hp = float(stats["GRUNT"]["hp"])

    shield_hp = float(stats["SHIELD"]["hp"])
    shield_armor = float(stats["SHIELD"]["armor"])

    flyer = move["FLYER"]

    result = {
        "probe": "PASSIVE_ROLE_CONTRACT_ANCHORS",
        "status": "STRUCTURAL_ANCHOR_ONLY_NOT_ENCOUNTER_ADMISSION",
        "RUNNER": {
            "speedRatioVsGrunt": runner_speed / grunt_speed,
            "travelTimeSecFromCommonSpawn": runner_t,
            "gruntTravelTimeSec": grunt_t,
            "arrivalLeadSecVsGrunt": grunt_t - runner_t,
            "interpretation": "large kinematic separation exists; encounter-level deletion-before-expression still needs direct timing metrics",
        },
        "BRUTE": {
            "hpRatioVsGrunt": brute_hp / grunt_hp,
            "knockResponseRatioVsGrunt": KNOCK_RESIST["BRUTE"] / KNOCK_RESIST["GRUNT"],
            "interpretation": "raw durability and knock resistance are mechanically separated; frontline block/screen time still needs direct instrumentation",
        },
        "SHIELD": {
            "armorDamageMultiplier": shield_armor,
            "preventedFractionPerRawHit": 1.0 - shield_armor,
            "effectiveRawDurability": shield_hp / shield_armor,
            "effectiveRawDurabilityRatioVsGrunt": (shield_hp / shield_armor) / grunt_hp,
            "referenceHitCounts": {
                str(raw): {
                    "shield": hits_to_kill(shield_hp, shield_armor, raw),
                    "grunt": hits_to_kill(grunt_hp, float(stats["GRUNT"]["armor"]), raw),
                }
                for raw in REFERENCE_RAW_HITS
            },
            "interpretation": "mitigation changes hit requirements across representative raw hits; encounter-level decision impact still needs direct instrumentation",
        },
        "FLYER": {
            "speedRatioVsGrunt": float(flyer["speed"]) / grunt_speed,
            "oscillationAmplitudeY": float(flyer["oscillationAmplitude"]),
            "oscillationPeakToPeakY": float(flyer["oscillationAmplitude"]) * 2.0,
            "oscillationOmega": float(flyer["oscillationOmega"]),
            "interpretation": "distinct Y-motion capability exists; actual line/splash/target-order opportunity still requires encounter-level geometry metrics",
        },
        "warning": "This tool validates that passive identities have nontrivial mechanical anchors. It does not replace class-aware role-expression admission metrics.",
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
