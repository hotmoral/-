#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("dataset_jsonl", type=Path)
    p.add_argument("schema_yaml", type=Path)
    args = p.parse_args()

    schema = yaml.safe_load(args.schema_yaml.read_text(encoding="utf-8")) or {}
    record_specs = schema.get("recordTypes") or {}
    allowed = schema.get("allowed") or {}
    context_map = schema.get("harnessContextMap") or {}

    errors: list[str] = []
    warnings: list[str] = []
    records = []

    for line_no, raw in enumerate(args.dataset_jsonl.read_text(encoding="utf-8").splitlines(), start=1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: invalid JSON: {exc}")
            continue
        if not isinstance(row, dict):
            errors.append(f"line {line_no}: record must be an object")
            continue
        row["__line"] = line_no
        records.append(row)

    by_trace: dict[str, list[dict]] = defaultdict(list)
    for row in records:
        line_no = row["__line"]
        typ = row.get("recordType")
        if typ not in record_specs:
            errors.append(f"line {line_no}: unknown recordType {typ!r}")
            continue
        missing = [k for k in record_specs[typ].get("required", []) if k not in row]
        if missing:
            errors.append(f"line {line_no}: {typ} missing required fields {missing}")
        trace_id = row.get("traceId")
        if not isinstance(trace_id, str) or not trace_id:
            errors.append(f"line {line_no}: traceId must be a nonempty string")
            continue
        if row.get("harnessVersion") != schema.get("harnessVersionRequired"):
            errors.append(f"line {line_no}: harnessVersion mismatch")
        hid = row.get("harnessId")
        if hid not in set(allowed.get("harnessIds") or []):
            errors.append(f"line {line_no}: invalid harnessId {hid!r}")
        by_trace[trace_id].append(row)

        if typ == "ACTION":
            if row.get("pressureContext") not in set(allowed.get("pressureContexts") or []):
                errors.append(f"line {line_no}: invalid pressureContext")
            if row.get("judgment") not in set(allowed.get("judgments") or []):
                errors.append(f"line {line_no}: invalid judgment")
            if row.get("comboBreakCause") not in set(allowed.get("comboBreakCauses") or []):
                errors.append(f"line {line_no}: invalid comboBreakCause")
            expected_context = context_map.get(hid)
            if expected_context and row.get("pressureContext") != expected_context:
                errors.append(f"line {line_no}: harness/context mismatch {hid}->{row.get('pressureContext')}, expected {expected_context}")
            if row.get("heavyCompleted") is True and row.get("heavyAttempted") is not True:
                errors.append(f"line {line_no}: heavyCompleted requires heavyAttempted")
            if row.get("heavyAttempted") is True and row.get("heavyOpportunity") is not True:
                errors.append(f"line {line_no}: heavyAttempted requires heavyOpportunity in schema v0.1")
            if row.get("ppCompleted") is True and row.get("ppAttempted") is not True:
                errors.append(f"line {line_no}: ppCompleted requires ppAttempted")
            for key in ("atMs", "seq", "comboBefore", "comboAfter", "chargeBefore", "chargeAfter"):
                if isinstance(row.get(key), bool) or not isinstance(row.get(key), int):
                    errors.append(f"line {line_no}: {key} must be integer")
            if isinstance(row.get("atMs"), int) and row["atMs"] < 0:
                errors.append(f"line {line_no}: atMs must be nonnegative")
            cb, ca = row.get("comboBefore"), row.get("comboAfter")
            if isinstance(cb, int) and isinstance(ca, int) and ca < cb and row.get("comboBreakCause") == "NONE":
                errors.append(f"line {line_no}: combo drop requires non-NONE break cause")

        elif typ == "STATE":
            if row.get("state") not in set(allowed.get("stateValues") or []):
                errors.append(f"line {line_no}: invalid state value")
            if isinstance(row.get("atMs"), bool) or not isinstance(row.get("atMs"), int) or row.get("atMs", -1) < 0:
                errors.append(f"line {line_no}: STATE atMs must be nonnegative integer")

        elif typ == "SESSION_END":
            if isinstance(row.get("endedAtMs"), bool) or not isinstance(row.get("endedAtMs"), int) or row.get("endedAtMs", -1) < 0:
                errors.append(f"line {line_no}: endedAtMs must be nonnegative integer")
            if not isinstance(row.get("completedAsDesigned"), bool):
                errors.append(f"line {line_no}: completedAsDesigned must be boolean")
            if not isinstance(row.get("exclusionReasons"), list):
                errors.append(f"line {line_no}: exclusionReasons must be a list")

    completed_by_harness = defaultdict(int)
    action_count_by_harness = defaultdict(int)
    player_ids = set()

    for trace_id, rows in by_trace.items():
        starts = [r for r in rows if r.get("recordType") == "SESSION_START"]
        ends = [r for r in rows if r.get("recordType") == "SESSION_END"]
        actions = [r for r in rows if r.get("recordType") == "ACTION"]
        states = [r for r in rows if r.get("recordType") == "STATE"]
        if len(starts) != 1:
            errors.append(f"trace {trace_id}: expected exactly one SESSION_START, got {len(starts)}")
        if len(ends) != 1:
            errors.append(f"trace {trace_id}: expected exactly one SESSION_END, got {len(ends)}")
        if not starts:
            continue
        hid = starts[0].get("harnessId")
        pid = starts[0].get("anonymousPlayerId")
        if isinstance(pid, str) and pid:
            player_ids.add(pid)
        for r in rows:
            if r.get("harnessId") != hid:
                errors.append(f"trace {trace_id}: mixed harnessId values")

        seqs = [r.get("seq") for r in actions if isinstance(r.get("seq"), int)]
        if any(b <= a for a, b in zip(seqs, seqs[1:])):
            errors.append(f"trace {trace_id}: ACTION seq must be strictly increasing")
        action_times = [r.get("atMs") for r in actions if isinstance(r.get("atMs"), int)]
        if any(b < a for a, b in zip(action_times, action_times[1:])):
            errors.append(f"trace {trace_id}: ACTION atMs must be nondecreasing in file order")

        completed = len(ends) == 1 and ends[0].get("completedAsDesigned") is True
        if completed:
            completed_by_harness[hid] += 1
            action_count_by_harness[hid] += len(actions)
            if hid == "H0" and len(actions) < 40:
                errors.append(f"trace {trace_id}: completed H0 has fewer than 40 ACTION records; combo40 opportunity missing")
            if hid == "H3":
                turnover = any(r.get("targetChangedSincePriorAction") is True for r in actions) or any(r.get("state") == "TARGET_REORDER" for r in states)
                if not turnover:
                    errors.append(f"trace {trace_id}: completed H3 lacks turnover evidence")
            if hid == "H4":
                stateful = any(r.get("state") in {"WINDUP_START", "INTERRUPTED", "FULL_ACTIVATION"} for r in states)
                if not stateful:
                    errors.append(f"trace {trace_id}: completed H4 lacks readable stateful evidence")

    known_harnesses = list(allowed.get("harnessIds") or [])
    missing_coverage = [h for h in known_harnesses if completed_by_harness[h] == 0]
    if missing_coverage:
        warnings.append(f"INSUFFICIENT_OBSERVED_TRACE_COVERAGE missing completed harnesses: {missing_coverage}")
    if not records:
        warnings.append("dataset contains no records; no fitted profile can be produced")

    print(f"VALIDATION=SKILLED_V2_TRACE_DATASET errors={len(errors)} warnings={len(warnings)} traces={len(by_trace)} players={len(player_ids)}")
    print("COVERAGE " + " ".join(f"{h}={completed_by_harness[h]}" for h in known_harnesses))
    print("ACTIONS " + " ".join(f"{h}={action_count_by_harness[h]}" for h in known_harnesses))
    for x in errors:
        print(f"ERROR {x}")
    for x in warnings:
        print(f"WARN {x}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
