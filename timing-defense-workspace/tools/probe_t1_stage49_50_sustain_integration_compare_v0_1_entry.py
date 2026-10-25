#!/usr/bin/env python3
"""Output-compatibility entry for sustain integration compare v0.1.

The diagnostic result object uses `meanLateSettledSeconds`; the first reporting
footer referenced the obsolete `meanLateSettled` spelling after all evidence
had already been written. Add a reporting-only alias to the returned summary so
the exact same simulation can complete its green workflow gate.
"""
import probe_t1_stage49_50_sustain_integration_compare_v0_1 as probe

_original_execute_candidate = probe.shape.execute_candidate


def _execute_candidate_with_report_alias(*args, **kwargs):
    result = _original_execute_candidate(*args, **kwargs)
    for side in ("OFF", "ON"):
        for row in result[side]["byClass"].values():
            row["meanLateSettled"] = row["meanLateSettledSeconds"]
    return result


probe.shape.execute_candidate = _execute_candidate_with_report_alias

if __name__ == "__main__":
    probe.main()
