#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


def tier_num(tier_id: str) -> int:
    return int(tier_id[1:])


def validate(data):
    errors = []
    warnings = []

    def err(code, msg):
        errors.append((code, msg))

    def warn(code, msg):
        warnings.append((code, msg))

    qualitative = data.get("qualitativeStagePresenceRanges", {})
    allowed_labels = set(qualitative)
    archetypes = data.get("archetypes", {})
    tiers = data.get("tiers", {})
    formation_defs = set(data.get("formationDefinitions", {}))
    cadence_defs = set(data.get("cadenceDefinitions", {}))

    prior_archetypes = set()
    prior_formations = set()
    prior_cadences = set()

    for tier_id in sorted(tiers, key=tier_num):
        tier = tiers[tier_id]
        legal = set(tier.get("legalArchetypes", []))

        if not prior_archetypes.issubset(legal):
            err("ARCHETYPE_REGRESSION", f"{tier_id} drops {sorted(prior_archetypes - legal)}")

        for archetype_id in legal:
            if archetype_id not in archetypes:
                err("UNKNOWN_ARCHETYPE", f"{tier_id}/{archetype_id}")
                continue
            earliest = archetypes[archetype_id]["earliestTier"]
            if tier_num(tier_id) < tier_num(earliest):
                err("ARCHETYPE_TOO_EARLY", f"{archetype_id} in {tier_id}, earliest={earliest}")

        formations = set(tier.get("formations", []))
        if not formations.issubset(formation_defs):
            err("UNKNOWN_FORMATION", f"{tier_id}: {sorted(formations - formation_defs)}")
        if not prior_formations.issubset(formations):
            warn("FORMATION_REGRESSION", f"{tier_id} drops {sorted(prior_formations - formations)}")

        cadences = set(tier.get("cadences", []))
        if not cadences.issubset(cadence_defs):
            err("UNKNOWN_CADENCE", f"{tier_id}: {sorted(cadences - cadence_defs)}")
        if not prior_cadences.issubset(cadences):
            warn("CADENCE_REGRESSION", f"{tier_id} drops {sorted(prior_cadences - cadences)}")

        for pressure, label in tier.get("pressureLabels", {}).items():
            if label not in allowed_labels:
                err("UNKNOWN_PRESSURE_LABEL", f"{tier_id}/{pressure}={label}")

        complexity_ranges = tier.get("dominantComplexityRanges", {})
        min_total = sum(value[0] for value in complexity_ranges.values())
        max_total = sum(value[1] for value in complexity_ranges.values())
        if not (min_total <= 50 <= max_total):
            err("COMPLEXITY_RANGE_INFEASIBLE", f"{tier_id}: min={min_total} max={max_total}")

        # Encounter-archetype complexity and Stage-dominant complexity are distinct.
        # A Stage can become C2/C3 through sequencing/overlap of individually simpler encounters.
        # Therefore do not require every nonzero Stage-complexity bucket to have a legal
        # archetype with the exact same complexity label.

        prior_archetypes = legal
        prior_formations = formations
        prior_cadences = cadences

    if set(tiers.get("T4", {}).get("legalArchetypes", [])) != set(archetypes):
        warn("T4_NOT_FULL_LIBRARY", "T4 does not contain all current archetypes")

    guardrails = data.get("staticGuardrails", {})
    if guardrails.get("lv31AscensionWindow") != [41, 45]:
        err("LV31_ASCENSION_MISMATCH", str(guardrails.get("lv31AscensionWindow")))

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
