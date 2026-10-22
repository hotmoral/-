# Timing Defense — High-Mastery H3 Observed Trace Report V0.1

Updated: 2026-10-22 KST

## Status

**OBSERVED HIGH-MASTERY STRESS EVIDENCE / NOT SKILLED_V2_CENTRAL**

This report records the first completed H3 `TURNOVER_DENSITY` trace from the isolated playable calibration harness.
It must not be used as the ordinary skilled-player central profile.
The observed player is classified only as a `HIGH_MASTERY_STRESS_CANDIDATE` anchor pending broader evidence.

No raw anonymous player identifier or device identifier is stored in this canonical report.

---

## Trace integrity

Observed exported JSONL:

- harness: H3 `TURNOVER_DENSITY`
- completedAsDesigned: true
- exclusionReasons: none
- records: 131
- SESSION_START: 1
- ACTION: 72
- STATE: 57
- SESSION_END: 1
- action sequence: strictly increasing 1..72
- schema/order checks: PASS

STATE composition:

- `NO_TARGET_START`: 19
- `NO_TARGET_END`: 19
- `TARGET_REORDER`: 19

Thus the trace contains 19 complete turnover episodes.

---

## Observed timing/combo result

- PERFECT: 72 / 72
- GOOD: 0
- NORMAL: 0
- MISS: 0
- final combo: 72
- longest combo: 72
- combo breaks: 0
- run duration: ~65.649 s

This is strong evidence that this player remains above the ordinary-skilled calibration center even under repeated target turnover.
It is NOT evidence that ordinary skilled players should be modeled this strongly.

---

## Turnover / reacquisition evidence

All 19 target changes produced a PERFECT first post-turnover action.

Programmed no-target interval:

- min: 320 ms
- median: 321 ms
- max: 321 ms

Effective delay from `TARGET_REORDER` / target availability to first valid post-turnover ACTION:

- min: 409 ms
- P25: 574 ms
- median: 632 ms
- P75: 794 ms
- max: 962 ms
- mean: ~669 ms

Total interval from last pre-turnover ACTION to first post-turnover ACTION:

- min: 729 ms
- median: 953 ms
- max: 1283 ms
- mean: ~990 ms

Interpretation boundary:

- the 632 ms median is an **effective reacquisition-to-action delay in this harness**, not a pure human visual reaction-time constant;
- it includes the choice to wait for a favorable timing sweep after the new target becomes available;
- therefore it can inform high-mastery simulation context but must not be inserted directly as a universal reaction-time parameter.

---

## Heavy / P×P coherence

The trace contains 14 completed Heavy cycles.

- completed Heavy cycles: 14
- completed P×P cycles: 14
- observed completed-cycle P×P rate: 100%

The current action schema records both X and Y legs as Heavy/P×P attempt records, so raw `heavyAttempted` / `ppAttempted` row counts must not be interpreted as cycle counts without pairing the two legs.
For cycle-level summaries, `heavyCompleted` / `ppCompleted` are the authoritative completion markers.

---

## Instrumentation finding — reproduced WATCH

The previously documented convenience-field WATCH was reproduced exactly.

For all 19 first post-turnover ACTION rows:

- raw ordered STATE evidence is intact;
- `reacquireDelayMs` is populated correctly;
- `noTargetWaitMsBeforeAction` is `0`.

Cause:

- the harness clears the open `noTargetSince` marker when the target returns;
- the later ACTION therefore cannot directly read the closed interval.

No ground truth is lost because the authoritative interval is reconstructable from:

`NO_TARGET_START -> NO_TARGET_END -> TARGET_REORDER -> first post-turnover ACTION`.

### Canonical handling decision for current V0.1 collection

Until the convenience field is patched, treat:

- ordered STATE timestamps as authoritative for no-target duration;
- ACTION `reacquireDelayMs` as authoritative for target-available -> first-action delay;
- ACTION `noTargetWaitMsBeforeAction` as **NONAUTHORITATIVE / IGNORE WHEN ZERO AFTER A RECORDED TURNOVER**.

This satisfies the existing collection-pipeline fallback option of formally deriving the interval from raw STATE events.
A code patch remains desirable before broad multi-player collection, but this defect does not invalidate the present H3 trace or block H4 browser smoke.

---

## Calibration consequence

This trace strengthens the separation between:

- ordinary `SKILLED_V2_CONSERVATIVE/CENTRAL/STRONG`, which remain unfitted and require other-player evidence;
- `HIGH_MASTERY_STRESS`, for which this player is a strong candidate anchor.

Do not use this trace to raise the ordinary-skilled campaign difficulty target.
Use it later to test whether monster role-expression and counterplay remain meaningful under unusually consistent play.

---

## Next exact boundary

1. proceed to H4 `STATEFUL_READ` browser/device smoke;
2. verify visible `WINDUP_START` and response linkage;
3. export H4 JSONL;
4. validate interrupt/full-activation sequencing and response latency;
5. only after H4 PASS decide whether the convenience H3 field needs an immediate harness patch before H1/H2/H5 pilot collection.

No production gameplay or balance coefficient is changed by this report.
