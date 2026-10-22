#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

CURRENT_V1 = [
    "GRUNT", "RUNNER", "BRUTE", "SHIELD", "FLYER",
    "CHARGER", "SPLITTER", "SUPPORTER", "SIEGER",
]

REQUIRED_MONSTER_FIELDS = [
    "expressionClass",
    "coreMechanic",
    "minimumRoleExpression",
    "readableCounterplay",
    "requiredMetrics",
]


def validate(data):
    errors = []
    warnings = []

    rules = data.get("globalRules", {})
    if not rules.get("spawnDeleteGuard", {}).get("enabled"):
        errors.append("spawn-delete guard must be enabled")
    if rules.get("numericThresholdsFrozen") is not False:
        warnings.append("numericThresholdsFrozen should remain false until fitted SKILLED_V2 evidence")
    if not rules.get("futureMonsterExtensionRequired"):
        errors.append("future monster extension contract must remain enabled")

    classes = data.get("expressionClasses", {})
    monsters = data.get("monsters", {})

    for monster_id in CURRENT_V1:
        if monster_id not in monsters:
            errors.append(f"missing current V1 monster contract: {monster_id}")

    for monster_id, spec in monsters.items():
        for field in REQUIRED_MONSTER_FIELDS:
            value = spec.get(field)
            if value is None or value == "" or value == []:
                errors.append(f"{monster_id}: missing/empty {field}")
        expression_class = spec.get("expressionClass")
        if expression_class not in classes:
            errors.append(f"{monster_id}: unknown expressionClass {expression_class!r}")
        metrics = spec.get("requiredMetrics", [])
        if len(set(metrics)) != len(metrics):
            errors.append(f"{monster_id}: duplicate requiredMetrics")

        if monster_id == "GRUNT":
            if spec.get("failureClass") is not None:
                warnings.append("GRUNT should remain baseline-exempt with null failureClass")
        else:
            if not spec.get("failureClass"):
                errors.append(f"{monster_id}: non-baseline monster requires failureClass")
            if classes.get(expression_class, {}).get("requiresExpressionGate") is not True:
                errors.append(f"{monster_id}: non-baseline class must require expression gate")

    gate = data.get("validation", {}).get("designatedRoleEncounter", {})
    for key in [
        "requireAllFiveClassesStructuralOpportunity",
        "requireReadableCounterplayWindow",
        "forbidGuaranteedPreExpressionDeletion",
    ]:
        if gate.get(key) is not True:
            errors.append(f"validation.designatedRoleEncounter.{key} must be true")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()

    data = yaml.safe_load(args.contract.read_text(encoding="utf-8"))
    errors, warnings = validate(data)

    for item in warnings:
        print(f"WARN {item}")
    for item in errors:
        print(f"ERROR {item}")

    print(f"RESULT={'PASS' if not errors else 'FAIL'} errors={len(errors)} warnings={len(warnings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
