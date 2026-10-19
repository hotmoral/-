#!/usr/bin/env python3
"""Timing Defense pressure-grammar structural calculator.

This script is intentionally NOT a live combat simulator. It validates encounter-grammar
structure and role-opportunity coverage before concrete spawn recipes are authored.
"""

from __future__ import annotations

import itertools
import math
from collections import Counter

CLASSES = ["Knight", "Rogue", "Tank", "Archer", "Mage"]

# Role-response vectors. These are structural coverage coefficients derived from the
# qualitative/targeted v1-v4 findings, not claims about final DPS.
RESP = {
    "S-line":    {"Knight": .90, "Rogue": .55, "Tank": .82, "Archer": 1.35, "Mage": .95},
    "S-cluster": {"Knight": .88, "Rogue": .55, "Tank": .92, "Archer": .85, "Mage": 1.35},
    "S-scatter": {"Knight": 1.05, "Rogue": .62, "Tank": 1.02, "Archer": .98, "Mage": .82},
    "E":         {"Knight": 1.00, "Rogue": 1.40, "Tank": .86, "Archer": .95, "Mage": .72},
    "X-line":    {"Knight": .96, "Rogue": .72, "Tank": 1.05, "Archer": 1.28, "Mage": .82},
    "X-cluster": {"Knight": .96, "Rogue": .72, "Tank": 1.16, "Archer": .88, "Mage": 1.18},
    "X-split":   {"Knight": 1.05, "Rogue": .75, "Tank": 1.30, "Archer": 1.02, "Mage": .90},
}

TIERS = {
    "T1": {
        "complexity": {1: 30, 2: 17, 3: 3},
        "occ": {"S": 25, "E": 24, "X": 24},
        "forms": {"S-line": 8, "S-cluster": 11, "S-scatter": 6,
                  "X-line": 7, "X-cluster": 6, "X-split": 11, "E": 24},
        "name": "Foundations",
    },
    "T2": {
        "complexity": {1: 21, 2: 23, 3: 6},
        "occ": {"S": 24, "E": 37, "X": 24},
        "forms": {"S-line": 7, "S-cluster": 11, "S-scatter": 6,
                  "X-line": 5, "X-cluster": 6, "X-split": 13, "E": 37},
        "name": "Breakers",
    },
    "T3": {
        "complexity": {1: 17, 2: 25, 3: 8},
        "occ": {"S": 40, "E": 19, "X": 32},
        "forms": {"S-line": 22, "S-cluster": 10, "S-scatter": 8,
                  "X-line": 14, "X-cluster": 5, "X-split": 13, "E": 19},
        "name": "Rushline",
    },
    "T4": {
        "complexity": {1: 11, 2: 25, 3: 14},
        "occ": {"S": 32, "E": 28, "X": 43},
        "forms": {"S-line": 8, "S-cluster": 10, "S-scatter": 14,
                  "X-line": 9, "X-cluster": 8, "X-split": 26, "E": 28},
        "name": "Crossfire",
    },
    "T5": {
        "complexity": {1: 23, 2: 19, 3: 8},
        "occ": {"S": 30, "E": 31, "X": 24},
        "forms": {"S-line": 9, "S-cluster": 17, "S-scatter": 4,
                  "X-line": 6, "X-cluster": 6, "X-split": 12, "E": 31},
        "name": "Extremes",
    },
}

# Pressure-budget corrections encode the tier's internal pair/triple dominance.
# They are approximate aggregate multipliers used only to reproduce the v5 structural
# opportunity result; concrete stage authoring stores the exact per-stage shares.
TIER_BUDGET_WEIGHT = {
    "T1": {"S": 1.00, "E": 1.00, "X": 1.00},
    "T2": {"S": .85, "E": 1.30, "X": .90},
    "T3": {"S": 1.20, "E": .65, "X": 1.10},
    "T4": {"S": .90, "E": .80, "X": 1.25},
    "T5": {"S": 1.12, "E": 1.12, "X": .90},
}


def coverage(team, scores):
    if not team:
        return 0.0
    vals = sorted((scores[c] for c in team), reverse=True)
    weights = (1.0, .35, .15)
    return sum(weights[i] * v for i, v in enumerate(vals[:3]))


def shapley(scores):
    n = len(CLASSES)
    out = {c: 0.0 for c in CLASSES}
    denom = math.factorial(n)
    for c in CLASSES:
        others = [x for x in CLASSES if x != c]
        for r in range(len(others) + 1):
            coeff = math.factorial(r) * math.factorial(n-r-1) / denom
            for subset in itertools.combinations(others, r):
                out[c] += coeff * (
                    coverage(subset + (c,), scores) - coverage(subset, scores)
                )
    return out


def family(role_key):
    return role_key[0] if role_key != "E" else "E"


def tier_role_share(tier_key):
    tier = TIERS[tier_key]
    budget = TIER_BUDGET_WEIGHT[tier_key]
    totals = Counter()
    for role_key, count in tier["forms"].items():
        p = family(role_key)
        pressure = count * budget[p]
        sv = shapley(RESP[role_key])
        for cls, value in sv.items():
            totals[cls] += pressure * value
    grand = sum(totals.values())
    return {c: totals[c] / grand for c in CLASSES}


def main():
    complexity_total = Counter()
    all_role = Counter()

    print("Tier complexity and role-coverage shares")
    for key, tier in TIERS.items():
        complexity_total.update(tier["complexity"])
        share = tier_role_share(key)
        print(
            f"{key} {tier['name']}: "
            f"1P={tier['complexity'][1]} 2P={tier['complexity'][2]} 3P={tier['complexity'][3]} | "
            + " ".join(f"{c}={share[c]*100:.1f}%" for c in CLASSES)
        )
        for c in CLASSES:
            all_role[c] += share[c]

    stages = sum(complexity_total.values())
    print("\nPrototype complexity across", stages, "stages")
    for k in (1, 2, 3):
        print(f"{k}P: {complexity_total[k]} ({complexity_total[k]/stages*100:.1f}%)")

    # This simple average treats each 50-stage tier equally.
    print("\nEqual-tier structural opportunity average")
    for c in CLASSES:
        print(f"{c}: {all_role[c]/len(TIERS)*100:.1f}%")


if __name__ == "__main__":
    main()
