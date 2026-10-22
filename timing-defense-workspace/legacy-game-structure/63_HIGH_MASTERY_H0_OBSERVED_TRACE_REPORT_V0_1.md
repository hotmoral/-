# Timing Defense — High-Mastery H0 Observed Trace Report V0.1

Date: 2026-10-22 KST  
Status: **OBSERVED H0 TRACE PASS / HIGH_MASTERY_STRESS_CANDIDATE ONLY / NOT SKILLED_V2 FIT**

Depends on:
- `61_HIGH_MASTERY_PLAYER_ANCHOR_AMENDMENT_V0_1.md`
- `55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
- `legacy-game-structure/data/skilled_v2_trace_schema_v0_1.yaml`

## 1. Evidence class

This report records the first real H0 browser/device trace collected from the isolated calibration harness.

The participant explicitly self-classifies above ordinary skilled play. Therefore this trace is classified only as:

`HIGH_MASTERY_STRESS_CANDIDATE`

It must not be used as `SKILLED_V2_CENTRAL`, and it must not be used to raise ordinary skilled difficulty targets by itself.

No raw anonymous ID, device user-agent, or raw trace payload is committed here. Only de-identified aggregate evidence is retained in canonical planning.

## 2. Trace validity

Observed trace structure:

```text
SESSION_START = 1
ACTION        = 80
STATE         = 0
SESSION_END   = 1
TOTAL         = 82 records
```

Harness/context:
- harness: H0 `TIMING_BASELINE`
- pressure context: `BASELINE`
- completedAsDesigned: true
- exclusionReasons: none
- all required schema fields present
- ACTION seq: contiguous 1..80
- ACTION time order: nondecreasing
- one consistent traceId / harnessId / harnessVersion
- semantic implication checks: PASS

Result:
`H0_TRACE_SCHEMA_AND_FLOW = PASS`.

## 3. Timing / judgment observation

Judgments:

```text
PERFECT = 80 / 80 = 100%
GOOD    = 0
NORMAL  = 0
MISS    = 0
INVALID = 0
```

Combo:
- longest combo: 80
- combo breaks: 0
- combo40 reached naturally inside the run
- combo60 reached naturally inside the run

This is direct evidence that combo40 is not an appropriate high-mastery-only threshold for this participant.
It does not establish population-level skilled rates.

## 4. Heavy / P×P observation

Input-axis records:
- X records: 64
- Y records: 16

Completed heavy sequences:
- 16 heavy X→Y pairs
- 16 / 16 heavy sequences completed
- all 16 completed as PERFECT × PERFECT
- completed P×P: 16 / 16 completed heavy sequences

The ACTION schema records heavy opportunity/attempt on both X and Y rows, so raw field counts are larger than the number of completed heavy attacks. Attack-level interpretation must pair the X and Y records.

Result:
`H0_HEAVY_FLOW = PASS`.

## 5. Cadence observation

All-action inter-input intervals, excluding the first action:
- N = 79
- mean ≈ 889.2 ms
- median ≈ 939 ms
- P10 ≈ 665.8 ms
- P25 ≈ 915 ms
- P75 ≈ 958 ms
- P90 ≈ 968.4 ms
- min 617 ms
- max 988 ms

Separated by destination axis:

### X inputs
- N = 63
- mean ≈ 946.4 ms
- median ≈ 949 ms
- range 899–988 ms
- P10 ≈ 921.6 ms
- P90 ≈ 973.2 ms

### Y inputs in heavy sequences
- N = 16
- mean = 664.0 ms
- median = 664 ms
- range 617–711 ms
- P10 ≈ 643.5 ms
- P90 ≈ 678.0 ms

Observed session end time: ≈71.8 s.

These values describe this H0 surface and participant only. They are not yet general player-model coefficients.

## 6. Interpretation boundary

What this evidence supports:
- the deployed H0 surface can produce a complete, coherent real-device trace
- the participant can sustain 80 consecutive PERFECT inputs in H0
- combo40 and combo60 are below this participant's clean-baseline ceiling
- heavy/P×P trace semantics are coherent in this observed run

What this evidence does **not** support:
- `SKILLED_V2_CENTRAL` probability values
- ordinary skilled PERFECT rate
- pressure degradation estimates
- turnover reacquisition estimates
- stateful response-latency estimates
- campaign difficulty tuning

## 7. Next exact boundary

Proceed to H3 `TURNOVER_DENSITY` on the same isolated deployment.

Required H3 evidence:
- `NO_TARGET_START`
- `NO_TARGET_END`
- `TARGET_REORDER`
- first post-turnover ACTION
- target change evidence
- reacquisition timing
- direct inspection of the optional `noTargetWaitMsBeforeAction` field versus the raw STATE-derived interval

Do not fit numeric SKILLED_V2 profiles after H0 alone.
