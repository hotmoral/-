#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

JUDGMENTS = ["PERFECT", "GOOD", "NORMAL", "MISS", "INVALID"]
HARNESS_IDS = ["H0", "H1", "H2", "H3", "H4", "H5"]


def quantile(values: list[float], q: float):
    if not values:
        return None
    xs = sorted(values)
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return xs[lo]
    w = pos - lo
    return xs[lo] * (1 - w) + xs[hi] * w


def safe_rate(num: int, den: int):
    return None if den == 0 else num / den


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("dataset_jsonl", type=Path)
    args = p.parse_args()

    records = []
    for raw in args.dataset_jsonl.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        row = json.loads(raw)
        if isinstance(row, dict):
            records.append(row)

    by_trace = defaultdict(list)
    for r in records:
        trace_id = r.get("traceId")
        if trace_id:
            by_trace[str(trace_id)].append(r)

    completed_trace_ids = set()
    excluded_trace_ids = set()
    trace_harness = {}
    trace_player = {}
    for tid, rows in by_trace.items():
        start = next((r for r in rows if r.get("recordType") == "SESSION_START"), None)
        end = next((r for r in rows if r.get("recordType") == "SESSION_END"), None)
        if start:
            trace_harness[tid] = start.get("harnessId")
            trace_player[tid] = start.get("anonymousPlayerId")
        if end and end.get("completedAsDesigned") is True:
            completed_trace_ids.add(tid)
        else:
            excluded_trace_ids.add(tid)

    summary = {
        "summaryType": "DESCRIPTIVE_PRE_FIT_ONLY",
        "fittedProfileProduced": False,
        "traceCount": len(by_trace),
        "completedTraceCount": len(completed_trace_ids),
        "excludedOrIncompleteTraceCount": len(excluded_trace_ids),
        "anonymousPlayerCount": len({p for p in trace_player.values() if isinstance(p, str) and p}),
        "byHarness": {},
        "pairing": {},
        "warnings": [],
    }

    completed_players_by_harness = defaultdict(set)

    for hid in HARNESS_IDS:
        tids = [tid for tid in completed_trace_ids if trace_harness.get(tid) == hid]
        actions = [
            r for tid in tids for r in by_trace[tid]
            if r.get("recordType") == "ACTION"
        ]
        states = [
            r for tid in tids for r in by_trace[tid]
            if r.get("recordType") == "STATE"
        ]
        for tid in tids:
            pid = trace_player.get(tid)
            if isinstance(pid, str) and pid:
                completed_players_by_harness[hid].add(pid)

        judgments = Counter(str(r.get("judgment")) for r in actions if r.get("judgment") is not None)
        valid_judgment_den = sum(judgments[j] for j in JUDGMENTS)
        inter = [float(r["interActionMs"]) for r in actions if isinstance(r.get("interActionMs"), (int, float)) and not isinstance(r.get("interActionMs"), bool)]
        reacq = [float(r["reacquireDelayMs"]) for r in actions if isinstance(r.get("reacquireDelayMs"), (int, float)) and not isinstance(r.get("reacquireDelayMs"), bool)]
        longest_by_trace = {}
        reach = {10: 0, 20: 0, 40: 0, 60: 0}
        for tid in tids:
            trace_actions = [r for r in by_trace[tid] if r.get("recordType") == "ACTION"]
            peak = max([int(r.get("comboBefore") or 0) for r in trace_actions] + [int(r.get("comboAfter") or 0) for r in trace_actions] + [0])
            longest_by_trace[tid] = peak
            for threshold in reach:
                if peak >= threshold:
                    reach[threshold] += 1

        heavy_opp = sum(1 for r in actions if r.get("heavyOpportunity") is True)
        heavy_attempt = sum(1 for r in actions if r.get("heavyAttempted") is True)
        heavy_complete = sum(1 for r in actions if r.get("heavyCompleted") is True)
        pp_attempt = sum(1 for r in actions if r.get("ppAttempted") is True)
        pp_complete = sum(1 for r in actions if r.get("ppCompleted") is True)
        break_causes = Counter(str(r.get("comboBreakCause")) for r in actions if r.get("comboBreakCause") not in (None, "NONE"))
        target_changes = sum(1 for r in actions if r.get("targetChangedSincePriorAction") is True)

        windups = [r for r in states if r.get("state") == "WINDUP_START"]
        response_latencies = []
        action_by_seq = {r.get("seq"): r for r in actions if r.get("seq") is not None}
        for state in states:
            seq = state.get("relatedActionSeq")
            readable = state.get("readableSinceMs")
            action = action_by_seq.get(seq)
            if action and isinstance(readable, int) and isinstance(action.get("atMs"), int):
                response_latencies.append(float(action["atMs"] - readable))

        summary["byHarness"][hid] = {
            "completedTraces": len(tids),
            "actionCount": len(actions),
            "judgmentCounts": {j: judgments[j] for j in JUDGMENTS},
            "judgmentShares": {j: safe_rate(judgments[j], valid_judgment_den) for j in JUDGMENTS},
            "interActionMs": {
                "p25": quantile(inter, .25),
                "p50": quantile(inter, .50),
                "p75": quantile(inter, .75),
                "p90": quantile(inter, .90),
            },
            "comboReachTraceCount": {"10": reach[10], "20": reach[20], "40": reach[40], "60Plus": reach[60]},
            "comboReachTraceRate": {
                "10": safe_rate(reach[10], len(tids)),
                "20": safe_rate(reach[20], len(tids)),
                "40": safe_rate(reach[40], len(tids)),
                "60Plus": safe_rate(reach[60], len(tids)),
            },
            "longestCombo": {
                "p50": quantile(list(longest_by_trace.values()), .50),
                "p90": quantile(list(longest_by_trace.values()), .90),
                "max": max(longest_by_trace.values()) if longest_by_trace else None,
            },
            "comboBreakCauses": dict(break_causes),
            "heavy": {
                "opportunities": heavy_opp,
                "attempts": heavy_attempt,
                "completions": heavy_complete,
                "attemptRateGivenOpportunity": safe_rate(heavy_attempt, heavy_opp),
                "completionRateGivenAttempt": safe_rate(heavy_complete, heavy_attempt),
            },
            "pp": {
                "attempts": pp_attempt,
                "completions": pp_complete,
                "completionRateGivenAttempt": safe_rate(pp_complete, pp_attempt),
            },
            "turnover": {
                "targetChangeCount": target_changes,
                "reacquireDelayMsP50": quantile(reacq, .50),
                "reacquireDelayMsP90": quantile(reacq, .90),
            },
            "stateful": {
                "windupStartCount": len(windups),
                "responseLatencyMsP50": quantile(response_latencies, .50),
                "responseLatencyMsP90": quantile(response_latencies, .90),
            },
        }

    h0_players = completed_players_by_harness["H0"]
    for hid in HARNESS_IDS[1:]:
        paired = h0_players & completed_players_by_harness[hid]
        summary["pairing"][f"H0_{hid}"] = {
            "pairedAnonymousPlayerCount": len(paired),
            "status": "PAIRED_AVAILABLE" if paired else "UNPAIRED_OR_NO_PLAYER_IDS",
        }

    missing = [h for h in HARNESS_IDS if summary["byHarness"][h]["completedTraces"] == 0]
    if missing:
        summary["warnings"].append({
            "classification": "INSUFFICIENT_OBSERVED_TRACE_COVERAGE",
            "missingHarnesses": missing,
        })
    if summary["byHarness"]["H0"]["completedTraces"] > 0 and summary["byHarness"]["H0"]["comboReachTraceRate"]["40"] in (0, 0.0):
        summary["warnings"].append({
            "classification": "COMBO40_NOT_OBSERVED_IN_CURRENT_H0_SAMPLE",
            "note": "inspect opportunity length, familiarity, sample composition and instrumentation before changing the user anchor",
        })

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
