#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

SKILL_ORDER = ["lv6", "lv11", "lv16", "lv21", "lv26", "lv31"]


def midpoint(r):
    return (r[0] + r[1]) / 2.0


def validate(data):
    errors = []
    warnings = []

    def err(code, msg):
        errors.append((code, msg))

    def warn(code, msg):
        warnings.append((code, msg))

    tiers = data.get("tiers", {})
    expected_count = data.get("initialCampaignTierCount")
    if len(tiers) != expected_count:
        err("TIER_COUNT_MISMATCH", f"{len(tiers)} tiers != expected {expected_count}")

    skill = data.get("skillReachWindows", {})
    prev_end = 0
    for lv in SKILL_ORDER:
        r = skill.get(lv)
        if not (isinstance(r, list) and len(r) == 2):
            err("SKILL_WINDOW_MISSING", lv)
            continue
        a, b = r
        if not (1 <= a <= b <= 50):
            err("SKILL_WINDOW_RANGE", f"{lv}={r}")
        if a <= prev_end:
            warn("SKILL_WINDOW_OVERLAP", f"{lv} begins {a} <= previous end {prev_end}")
        prev_end = b

    if skill.get("lv31") != [41, 45]:
        err("LV31_TARGET_MISMATCH", f"lv31={skill.get('lv31')} expected [41,45]")

    late = data.get("lateBand", {})
    required_late = {
        "starGateB": 40,
        "lv31Ascension": [41, 45],
        "postLv31Mastery": [46, 49],
        "tierFinal": 50,
    }
    for key, expected in required_late.items():
        if late.get(key) != expected:
            err("LATE_BAND_MISMATCH", f"{key}={late.get(key)} expected {expected}")

    registry = data.get("monsterRegistry", {})
    current = set(registry.get("currentV1", []))
    if registry.get("lifetimeFixedCount") is not False:
        err("ROSTER_EXTENSIBILITY_CLOSED", "lifetimeFixedCount must be false")

    introduced = []
    prior_available = set()
    for tid in sorted(tiers, key=lambda x: int(x[1:])):
        tier = tiers[tid]
        intro = tier.get("introducedMonsters", [])
        available = set(tier.get("availableMonsters", []))

        for monster in intro:
            if monster in introduced:
                err("MONSTER_DUPLICATE_INTRODUCTION", f"{monster} in {tid}")
            introduced.append(monster)

        if not prior_available.issubset(available):
            err("ROSTER_REGRESSION", f"{tid} drops previously available monsters")
        if not set(introduced).issubset(available):
            err("ROSTER_CUMULATIVE_MISSING", f"{tid} available roster missing introduced monster")
        if not available.issubset(current):
            err("UNKNOWN_MONSTER", f"{tid}: {sorted(available - current)}")
        prior_available = available

        for monster, window in tier.get("introductionWindows", {}).items():
            first_teach = window.get("firstTeach")
            first_mixed = window.get("firstMixed")
            first_high = window.get("firstHighPressure")
            if not all(isinstance(r, list) and len(r) == 2 for r in (first_teach, first_mixed, first_high)):
                err("INTRO_WINDOW_MISSING", f"{tid}/{monster}")
                continue
            if not (first_teach[0] <= first_mixed[0] <= first_high[0]):
                err("INTRO_ORDER", f"{tid}/{monster}: {first_teach},{first_mixed},{first_high}")
            if first_teach[0] >= 40:
                err("FIRST_TEACH_TOO_LATE", f"{tid}/{monster}: {first_teach}")

            # GRUNT is the neutral baseline and does not represent capability-novelty attribution.
            if monster == "GRUNT" or window.get("baselineCollisionExempt"):
                continue

            high_mid = midpoint(first_high)
            for lv, reach_window in skill.items():
                if abs(high_mid - midpoint(reach_window)) <= 2:
                    warn(
                        "POWER_ATTRIBUTION_COLLISION",
                        f"{tid}/{monster} {first_high} near {lv} {reach_window}",
                    )

    if set(introduced) != current:
        warn("V1_ROSTER_NOT_FULLY_INTRODUCED", f"missing={sorted(current - set(introduced))}")

    difficulty = data.get("difficultyGate", {})
    upper_bound = difficulty.get("nonT1FullTierClearUpperBoundExclusive")
    if not isinstance(upper_bound, (int, float)) or not (0 < upper_bound <= 0.60):
        err("DIFFICULTY_GATE_INVALID", f"upperBound={upper_bound}")
    if difficulty.get("profile") != "SKILLED_V2_CENTRAL":
        warn("DIFFICULTY_PROFILE_UNEXPECTED", str(difficulty.get("profile")))

    stars = data.get("metaProgression", {}).get("stars", {})
    expected_stars = {
        "failStages1to19": 0,
        "failStages20to39": 1,
        "failStages40to49": 2,
        "clearStage50": 3,
    }
    if stars != expected_stars:
        err("STAR_CONTRACT_MISMATCH", f"{stars}")

    boss_final = data.get("bossPlaceholders", {}).get("tierFinal", {})
    if boss_final.get("unpreviewedMandatoryMechanicAllowed") is not False:
        err("UNPREVIEWED_FINAL_BOSS_MECHANIC_ALLOWED", "must be false")

    expansion = data.get("futureExpansion", {})
    if expansion.get("futureMonsterAdditionAllowed") is not True:
        err("FUTURE_MONSTER_EXPANSION_DISABLED", "")
    if expansion.get("pressureTaxonomyVersioningAllowed") is not True:
        err("PRESSURE_TAXONOMY_FROZEN", "")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    data = yaml.safe_load(args.path.read_text(encoding="utf-8"))
    errors, warnings = validate(data)

    print(f"RESULT={'PASS' if not errors else 'FAIL'} errors={len(errors)} warnings={len(warnings)}")
    for code, msg in errors:
        print(f"ERROR {code}: {msg}")
    for code, msg in warnings:
        print(f"WARN {code}: {msg}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
