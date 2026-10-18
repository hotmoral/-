#!/usr/bin/env python3
"""Synthetic adversarial contract tests for Step 13B serialization recovery."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import tempfile

from projection import (
    ContractError,
    I64_MAX,
    canonical_bytes,
    loads_strict,
    project_multiplicity,
    project_recovery,
)

ROOT = Path(__file__).resolve().parent
FIX = ROOT / "fixtures"
TESTS = 0


def ok(condition: bool, label: str) -> None:
    global TESTS
    TESTS += 1
    if not condition:
        raise AssertionError(label)
    print(f"PASS {TESTS:02d}: {label}")


def expect_contract_error(fn, label: str) -> None:
    try:
        fn()
    except ContractError:
        ok(True, label)
        return
    raise AssertionError(label + " (no ContractError)")


def has_float(value) -> bool:
    if isinstance(value, float):
        return True
    if isinstance(value, list):
        return any(has_float(v) for v in value)
    if isinstance(value, dict):
        return any(has_float(v) for v in value.values())
    return False


def java_probe(path: Path, expect_success: bool, label: str) -> None:
    result = subprocess.run(
        ["java", "-cp", str(ROOT / "build"), "StrictIntegerJsonProbe", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    ok((result.returncode == 0) == expect_success, label + f" [rc={result.returncode}]")


def write_temp(directory: Path, name: str, text: str) -> Path:
    path = directory / name
    path.write_text(text, encoding="utf-8")
    return path


def main() -> None:
    recovery_text = (FIX / "recovery_raw.json").read_text(encoding="utf-8")
    multiplicity_text = (FIX / "multiplicity_raw.json").read_text(encoding="utf-8")
    recovery_raw = loads_strict(recovery_text)
    multiplicity_raw = loads_strict(multiplicity_text)
    recovery_before = copy.deepcopy(recovery_raw)
    multiplicity_before = copy.deepcopy(multiplicity_raw)

    ok(has_float(recovery_raw), "synthetic Recovery raw fixture contains float timing fields")
    ok(has_float(multiplicity_raw), "synthetic multiplicity raw fixture contains float timing fields")

    recovery_projected = project_recovery(recovery_raw)
    multiplicity_projected = project_multiplicity(multiplicity_raw)
    ok(recovery_raw == recovery_before, "Recovery projection does not mutate source object")
    ok(multiplicity_raw == multiplicity_before, "Multiplicity projection does not mutate source object")
    ok(not has_float(recovery_projected), "Recovery projection is float-free")
    ok(not has_float(multiplicity_projected), "Multiplicity projection is float-free")

    recovery_bytes = canonical_bytes(recovery_projected)
    multiplicity_bytes = canonical_bytes(multiplicity_projected)
    ok(recovery_bytes == (FIX / "recovery_expected_projection.json").read_bytes(), "Recovery canonical bytes match expected projection")
    ok(multiplicity_bytes == (FIX / "multiplicity_expected_projection.json").read_bytes(), "Multiplicity canonical bytes match expected projection")
    ok(recovery_bytes == canonical_bytes(project_recovery(loads_strict(recovery_text))), "Recovery projection is byte-deterministic")
    ok(multiplicity_bytes == canonical_bytes(project_multiplicity(loads_strict(multiplicity_text))), "Multiplicity projection is byte-deterministic")

    recovery_public = recovery_bytes.decode("utf-8")
    multiplicity_public = multiplicity_bytes.decode("utf-8")
    ok("elapsedSeconds" not in recovery_public and "operational" not in recovery_public, "Recovery operational timing fields are not forwarded")
    ok("elapsedSeconds" not in multiplicity_public and '"compile"' not in multiplicity_public and '"execution"' not in multiplicity_public, "Multiplicity operational timing fields are not forwarded")

    expect_contract_error(lambda: loads_strict('{"x":1,"x":2}'), "duplicate JSON keys fail closed")

    bad = copy.deepcopy(recovery_raw)
    del bad["classification"]
    expect_contract_error(lambda: project_recovery(bad), "missing required top-level field fails closed")

    bad = copy.deepcopy(recovery_raw)
    del bad["comparator"]["sample"]
    expect_contract_error(lambda: project_recovery(bad), "missing required nested field fails closed")

    bad = copy.deepcopy(recovery_raw)
    bad["comparator"] = []
    expect_contract_error(lambda: project_recovery(bad), "wrong required object type fails closed")

    bad = copy.deepcopy(multiplicity_raw)
    bad["payload"]["aggregate"]["generatedCount"] = 12.5
    expect_contract_error(lambda: project_multiplicity(bad), "float in required integer field fails closed")

    bad = copy.deepcopy(multiplicity_raw)
    bad["payload"]["aggregate"]["expandedCount"] = True
    expect_contract_error(lambda: project_multiplicity(bad), "boolean cannot masquerade as integer")

    bad = copy.deepcopy(multiplicity_raw)
    bad["payload"]["aggregate"]["generatedCount"] = I64_MAX + 1
    expect_contract_error(lambda: project_multiplicity(bad), "signed 64-bit overflow fails closed in projection")

    bad = copy.deepcopy(recovery_raw)
    bad["comparator"]["sample"]["badFloat"] = 0.25
    projected = project_recovery(bad)
    expect_contract_error(lambda: canonical_bytes(projected), "float hidden inside copied semantic sample fails before serialization")

    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    compile_result = subprocess.run(
        ["javac", "-encoding", "UTF-8", "-d", str(build), str(ROOT / "StrictIntegerJsonProbe.java")],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    ok(compile_result.returncode == 0, "independent Java integer-only probe compiles")

    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        recovery_out = write_temp(tmp, "recovery-projected.json", recovery_bytes.decode("utf-8"))
        multiplicity_out = write_temp(tmp, "multiplicity-projected.json", multiplicity_bytes.decode("utf-8"))
        java_probe(recovery_out, True, "Java probe accepts Recovery projection")
        java_probe(multiplicity_out, True, "Java probe accepts multiplicity projection")

        raw_recovery = write_temp(tmp, "raw-recovery.json", recovery_text)
        raw_multiplicity = write_temp(tmp, "raw-multiplicity.json", multiplicity_text)
        java_probe(raw_recovery, False, "Java probe rejects raw Recovery fixture containing decimals")
        java_probe(raw_multiplicity, False, "Java probe rejects raw multiplicity fixture containing decimals")

        bounds = write_temp(tmp, "bounds.json", '{"min":-9223372036854775808,"max":9223372036854775807}\n')
        java_probe(bounds, True, "Java probe accepts signed 64-bit integer boundaries")
        java_probe(write_temp(tmp, "decimal.json", '{"x":1.5}\n'), False, "Java probe rejects decimal numeric literal")
        java_probe(write_temp(tmp, "exponent.json", '{"x":1e3}\n'), False, "Java probe rejects exponent numeric literal")
        java_probe(write_temp(tmp, "overflow.json", '{"x":9223372036854775808}\n'), False, "Java probe rejects signed 64-bit overflow")
        java_probe(write_temp(tmp, "leading-zero.json", '{"x":01}\n'), False, "Java probe rejects malformed leading-zero integer")

    ok(TESTS >= 29, "contract suite executed at least 29 assertions")
    print(f"PUBLIC_SERIALIZATION_RECOVERY_CONTRACT_PASS tests={TESTS}")


if __name__ == "__main__":
    main()
