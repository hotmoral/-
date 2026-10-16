#!/usr/bin/env python3
import copy
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
BUILD = ROOT / "build"
CLASS = "com.example.einsteingame.authoring.pss.contract.ContractHarness"
checks = 0


def check(value, label):
    global checks
    checks += 1
    if not value:
        raise AssertionError(label)


def assert_no_float(value, path="$"):
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        raise AssertionError(f"float at {path}")
    if isinstance(value, dict):
        for key, child in value.items():
            check(isinstance(key, str), f"non-string key at {path}")
            assert_no_float(child, f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            assert_no_float(child, f"{path}[{index}]")
        return
    raise AssertionError(f"unsupported type at {path}: {type(value).__name__}")


def run(command, expect=0):
    proc = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    check(proc.returncode == expect, f"command exit {proc.returncode} != {expect}: {' '.join(map(str, command))}\n{proc.stdout}")
    return proc.stdout


def java(*args, expect=0):
    return run(["java", "-cp", str(BUILD / "classes"), CLASS, *map(str, args)], expect=expect)


def line_value(output, prefix):
    for line in output.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):]
    raise AssertionError(f"missing {prefix!r} in output:\n{output}")


def compile_java():
    sources = sorted(str(path) for path in SRC.rglob("*.java"))
    check(len(sources) == 2, "unexpected Java source count")
    classes = BUILD / "classes"
    classes.mkdir(parents=True, exist_ok=True)
    run(["javac", "-encoding", "UTF-8", "--release", "17", "-d", str(classes), *sources])


def valid_envelope():
    return {
        "baselineCP5Identity": "synthetic-cp5-identity",
        "baselineCounts": {
            "budgetConsumed": {
                "expandedNodes": 7,
                "generatedEdges": 11,
                "maxDepthReached": 2,
            },
            "expandedNodeCount": 7,
            "generatedEdgeCount": 11,
            "frontierCount": 4,
            "completeness": "BUDGET_EXHAUSTED",
            "conclusion": "UNKNOWN",
        },
        "sample": {
            "request": {"kind": "SYNTHETIC", "ordinal": 1},
            "profile": {"profileId": "SYNTHETIC"},
            "note": "public-contract-✓",
        },
        "longProbe": 2147483648,
    }


def main():
    compile_java()
    envelope = valid_envelope()
    assert_no_float(envelope)
    check("maxDepthReached" not in envelope["baselineCounts"], "top-level depth accidentally present")
    check(envelope["baselineCounts"]["budgetConsumed"]["maxDepthReached"] == 2, "nested depth missing")

    # Python-side guard must reject floats before any Java handoff.
    try:
        assert_no_float({"bad": 1.25})
        raise AssertionError("Python float guard did not reject float")
    except AssertionError as exc:
        check("float at" in str(exc), "wrong Python float-guard failure")

    with tempfile.TemporaryDirectory(prefix="cp5-contract-") as temp_dir:
        temp = Path(temp_dir)
        valid_path = temp / "valid-envelope.json"
        canonical_python = json.dumps(envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        valid_path.write_text(canonical_python, encoding="utf-8")

        # Exact persisted file handoff: Python -> production-equivalent Java parser/writer.
        output = java("validate-envelope", valid_path)
        canonical_java = line_value(output, "CANONICAL=")
        hash_java = line_value(output, "HASH=")
        check(canonical_java == canonical_python, "Python/Java canonical JSON mismatch")
        check(hash_java == hashlib.sha256(canonical_python.encode("utf-8")).hexdigest(), "canonical SHA-256 mismatch")

        # Regression for the first task-local defect: depth in the wrong location must fail.
        wrong_depth = copy.deepcopy(envelope)
        depth = wrong_depth["baselineCounts"]["budgetConsumed"].pop("maxDepthReached")
        wrong_depth["baselineCounts"]["maxDepthReached"] = depth
        wrong_path = temp / "wrong-depth.json"
        wrong_path.write_text(json.dumps(wrong_depth, sort_keys=True, separators=(",", ":")), encoding="utf-8")
        wrong = subprocess.run(
            ["java", "-cp", str(BUILD / "classes"), CLASS, "validate-envelope", str(wrong_path)],
            cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        check(wrong.returncode != 0, "wrong-depth fixture unexpectedly passed")

        # Regression for the second task-local defect: decimal JSON must be rejected.
        decimal_path = temp / "decimal.json"
        decimal_path.write_text('{"baselineElapsedSeconds":10.25}', encoding="utf-8")
        check("REJECT_DECIMAL=PASS" in java("reject-decimal", decimal_path), "decimal JSON not rejected")
        exponent_path = temp / "exponent.json"
        exponent_path.write_text('{"value":1e3}', encoding="utf-8")
        check("REJECT_DECIMAL=PASS" in java("reject-decimal", exponent_path), "exponent JSON not rejected")

        # Writer must reject Java floating numeric types.
        check("REJECT_DOUBLE=PASS" in java("reject-double"), "Double not rejected")
        check("REJECT_FLOAT=PASS" in java("reject-float"), "Float not rejected")

        # Representative post-CP5 checkpoint must remain float-free and round-trip.
        checkpoint_output = java("write-checkpoint")
        checkpoint_json = line_value(checkpoint_output, "CHECKPOINT=")
        checkpoint = json.loads(checkpoint_json)
        assert_no_float(checkpoint)
        check(checkpoint["CP5"]["budgetConsumed"]["maxDepthReached"] == 4, "checkpoint nested depth mismatch")
        check("generatedEdgesPerExpandedNode" not in checkpoint["CP5"], "descriptive ratio leaked into Java semantic payload")
        check("generatedEdgesPerDistinctState" not in checkpoint["CP5"], "descriptive ratio leaked into Java semantic payload")
        checkpoint_hash = line_value(checkpoint_output, "CHECKPOINT_HASH=")
        check(checkpoint_hash == hashlib.sha256(checkpoint_json.encode("utf-8")).hexdigest(), "checkpoint SHA-256 mismatch")

    print(f"PUBLIC CONTRACT PASS checks={checks}")


if __name__ == "__main__":
    main()
