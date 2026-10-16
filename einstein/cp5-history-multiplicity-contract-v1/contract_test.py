#!/usr/bin/env python3
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src" / "HistoryMultiplicityContract.java"
BUILD = ROOT / "build"


def run(*args, check=True):
    p = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and p.returncode != 0:
        raise AssertionError(f"command failed {args}:\n{p.stdout}")
    return p


def main():
    BUILD.mkdir(exist_ok=True)
    run("javac", "-encoding", "UTF-8", "-d", str(BUILD), str(SRC))

    fixture = run("java", "-cp", str(BUILD), "HistoryMultiplicityContract", "fixture")
    shuffled = run("java", "-cp", str(BUILD), "HistoryMultiplicityContract", "shuffled")
    if fixture.stdout != shuffled.stdout:
        raise AssertionError("aggregation changed when synthetic edge/frontier collection order changed")

    actual = json.loads(fixture.stdout)
    expected = {
        "recordType": "SyntheticHistoryMultiplicityContract",
        "contractVersion": "1.0.0",
        "generatedEdgeCount": 9,
        "uniqueArrivalStateCount": 5,
        "distinctStateCount": 6,
        "repeatedArrivalCount": 4,
        "repeatedArrivalBasis": "EDGE_OCCURRENCES_MINUS_UNIQUE_ARRIVAL_STATES",
        "maxInboundHistoryMultiplicity": 3,
        "stateMultiplicityHistogram": {"1": 2, "2": 2, "3": 1},
        "topReconvergedStates": [
            {
                "stateId": "S3",
                "inboundHistoryCount": 3,
                "distinctHistoryCount": 3,
                "minDepth": 2,
                "maxDepth": 3,
                "minCost": 3,
                "maxCost": 8,
            },
            {
                "stateId": "S1",
                "inboundHistoryCount": 2,
                "distinctHistoryCount": 2,
                "minDepth": 1,
                "maxDepth": 1,
                "minCost": 1,
                "maxCost": 3,
            },
            {
                "stateId": "S5",
                "inboundHistoryCount": 2,
                "distinctHistoryCount": 2,
                "minDepth": 3,
                "maxDepth": 3,
                "minCost": 6,
                "maxCost": 7,
            },
        ],
        "crossDepthStates": [{"stateId": "S3", "depths": [2, 3]}],
        "depthBreakdown": [
            {
                "depth": 1,
                "arrivalOccurrences": 3,
                "distinctArrivalStates": 2,
                "globallyNewStates": 2,
                "repeatPressureOccurrences": 1,
            },
            {
                "depth": 2,
                "arrivalOccurrences": 3,
                "distinctArrivalStates": 2,
                "globallyNewStates": 2,
                "repeatPressureOccurrences": 1,
            },
            {
                "depth": 3,
                "arrivalOccurrences": 3,
                "distinctArrivalStates": 2,
                "globallyNewStates": 1,
                "repeatPressureOccurrences": 2,
            },
        ],
        "reconvergedTargetArrivalBySyntheticSkill": {
            "SYNTH_A": 3,
            "SYNTH_B": 2,
            "SYNTH_C": 2,
        },
        "frontier": {
            "historyOccurrenceCount": 4,
            "uniqueStateCount": 3,
            "maxHistoryMultiplicity": 2,
            "stateMultiplicityHistogram": {"1": 2, "2": 1},
            "states": [
                {"stateId": "S5", "historyCount": 2},
                {"stateId": "S3", "historyCount": 1},
                {"stateId": "S4", "historyCount": 1},
            ],
        },
    }
    if actual != expected:
        print("EXPECTED", json.dumps(expected, sort_keys=True, separators=(",", ":")))
        print("ACTUAL  ", json.dumps(actual, sort_keys=True, separators=(",", ":")))
        raise AssertionError("synthetic multiplicity contract mismatch")

    invalid = run(
        "java", "-cp", str(BUILD), "HistoryMultiplicityContract", "invalid-duplicate-history", check=False
    )
    if invalid.returncode == 0 or "duplicate target history: H1" not in invalid.stdout:
        raise AssertionError("duplicate-history negative control did not fail closed")

    # The contract intentionally uses only integer/string/list/map evidence.
    def assert_no_float(value):
        if isinstance(value, float):
            raise AssertionError("float leaked into semantic contract")
        if isinstance(value, dict):
            for k, v in value.items():
                if not isinstance(k, str):
                    raise AssertionError("non-string JSON key")
                assert_no_float(v)
        elif isinstance(value, list):
            for v in value:
                assert_no_float(v)

    assert_no_float(actual)
    print("history multiplicity contract: PASS checks=26")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"history multiplicity contract: FAIL: {exc}", file=sys.stderr)
        raise
