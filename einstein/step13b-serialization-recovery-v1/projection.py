#!/usr/bin/env python3
"""Public-safe semantic projection helpers for the Step 13B serialization contract."""
from __future__ import annotations

import copy
import json
from typing import Any, Iterable

I64_MIN = -(1 << 63)
I64_MAX = (1 << 63) - 1


class ContractError(ValueError):
    pass


def _reject_duplicate_pairs(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise ContractError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def loads_strict(text: str) -> Any:
    def reject_constant(token: str) -> Any:
        raise ContractError(f"non-finite JSON number: {token}")

    try:
        return json.loads(text, object_pairs_hook=_reject_duplicate_pairs, parse_constant=reject_constant)
    except ContractError:
        raise
    except (json.JSONDecodeError, ValueError) as exc:
        raise ContractError(str(exc)) from exc


def _require_dict(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(f"{path} must be object")
    return value


def _require_str(value: Any, path: str) -> str:
    if not isinstance(value, str):
        raise ContractError(f"{path} must be string")
    return value


def _require_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ContractError(f"{path} must be integer")
    if value < I64_MIN or value > I64_MAX:
        raise ContractError(f"{path} outside signed 64-bit range")
    return value


def _field(obj: dict[str, Any], key: str, path: str) -> Any:
    if key not in obj:
        raise ContractError(f"missing {path}.{key}")
    return obj[key]


def project_recovery(raw: Any) -> dict[str, Any]:
    root = _require_dict(raw, "$recovery")
    comparator = _require_dict(_field(root, "comparator", "$recovery"), "$recovery.comparator")
    sample = copy.deepcopy(_field(comparator, "sample", "$recovery.comparator"))
    return {
        "classification": _require_str(_field(root, "classification", "$recovery"), "$recovery.classification"),
        "comparator": {
            "baselineIdentity": _require_str(
                _field(comparator, "baselineIdentity", "$recovery.comparator"),
                "$recovery.comparator.baselineIdentity",
            ),
            "sample": sample,
        },
    }


def project_multiplicity(raw: Any) -> dict[str, Any]:
    root = _require_dict(raw, "$multiplicity")
    payload = _require_dict(_field(root, "payload", "$multiplicity"), "$multiplicity.payload")
    aggregate = _require_dict(_field(payload, "aggregate", "$multiplicity.payload"), "$multiplicity.payload.aggregate")
    history = _require_dict(
        _field(payload, "historyMultiplicity", "$multiplicity.payload"),
        "$multiplicity.payload.historyMultiplicity",
    )
    return {
        "payload": {
            "R": _require_str(_field(payload, "R", "$multiplicity.payload"), "$multiplicity.payload.R"),
            "A": _require_str(_field(payload, "A", "$multiplicity.payload"), "$multiplicity.payload.A"),
            "N": _require_str(_field(payload, "N", "$multiplicity.payload"), "$multiplicity.payload.N"),
            "historicalIdentity": _require_str(
                _field(payload, "historicalIdentity", "$multiplicity.payload"),
                "$multiplicity.payload.historicalIdentity",
            ),
            "aggregate": {
                "expandedCount": _require_int(
                    _field(aggregate, "expandedCount", "$multiplicity.payload.aggregate"),
                    "$multiplicity.payload.aggregate.expandedCount",
                ),
                "generatedCount": _require_int(
                    _field(aggregate, "generatedCount", "$multiplicity.payload.aggregate"),
                    "$multiplicity.payload.aggregate.generatedCount",
                ),
                "distinctStateCount": _require_int(
                    _field(aggregate, "distinctStateCount", "$multiplicity.payload.aggregate"),
                    "$multiplicity.payload.aggregate.distinctStateCount",
                ),
                "frontierCount": _require_int(
                    _field(aggregate, "frontierCount", "$multiplicity.payload.aggregate"),
                    "$multiplicity.payload.aggregate.frontierCount",
                ),
                "completeness": _require_str(
                    _field(aggregate, "completeness", "$multiplicity.payload.aggregate"),
                    "$multiplicity.payload.aggregate.completeness",
                ),
                "conclusion": _require_str(
                    _field(aggregate, "conclusion", "$multiplicity.payload.aggregate"),
                    "$multiplicity.payload.aggregate.conclusion",
                ),
            },
            "historyMultiplicity": {
                "arrivalCount": _require_int(
                    _field(history, "arrivalCount", "$multiplicity.payload.historyMultiplicity"),
                    "$multiplicity.payload.historyMultiplicity.arrivalCount",
                ),
                "reconvergedTargetCount": _require_int(
                    _field(history, "reconvergedTargetCount", "$multiplicity.payload.historyMultiplicity"),
                    "$multiplicity.payload.historyMultiplicity.reconvergedTargetCount",
                ),
            },
        }
    }


def assert_integer_safe(value: Any, path: str = "$") -> None:
    if value is None or isinstance(value, str) or isinstance(value, bool):
        return
    if isinstance(value, int):
        if value < I64_MIN or value > I64_MAX:
            raise ContractError(f"{path} outside signed 64-bit range")
        return
    if isinstance(value, float):
        raise ContractError(f"{path} contains float")
    if isinstance(value, list):
        for index, child in enumerate(value):
            assert_integer_safe(child, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ContractError(f"{path} contains non-string object key")
            assert_integer_safe(child, f"{path}.{key}")
        return
    raise ContractError(f"{path} contains unsupported type {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    assert_integer_safe(value)
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")
