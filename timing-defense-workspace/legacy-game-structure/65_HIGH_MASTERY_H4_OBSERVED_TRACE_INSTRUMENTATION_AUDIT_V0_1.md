# Timing Defense — High-Mastery H4 Observed Trace Instrumentation Audit V0.1

Date: 2026-10-22 KST
Status: **TRACE VALID / H4 RESPONSE-LATENCY FIT NOT ADMITTED**

## 0. Scope

This report audits the first observed H4 `STATEFUL_READ` trace collected from the isolated SKILLED_V2 harness.

The player is classified only as `HIGH_MASTERY_STRESS_CANDIDATE`. This trace is not evidence for `SKILLED_V2_CENTRAL`.

Raw anonymous identifiers, device strings, and raw trace payload are not committed here. Only aggregate findings are retained.

## 1. Trace integrity

Observed trace structure:

- SESSION_START: 1
- ACTION: 72
- STATE: 27
- SESSION_END: 1
- completedAsDesigned: true
- harness validation: PASS

Judgment outcome:

- PERFECT: 72 / 72
- GOOD: 0
- NORMAL: 0
- MISS: 0
- longest combo: 72

Heavy execution:

- heavy completions: 14
- P×P completions: 14 / 14 completed heavies

## 2. Stateful events

Observed state events:

- WINDUP_START: 6
- INTERRUPTED: 6
- FULL_ACTIVATION: 0
- NO_TARGET_START: 5
- NO_TARGET_END: 5
- TARGET_REORDER: 5

The six recorded tactical response latencies were:

- 965 ms
- 1168 ms
- 951 ms
- 1067 ms
- 880 ms
- 790 ms

Summary:

- min: 790 ms
- median: 958 ms
- mean: 970.2 ms
- max: 1168 ms

## 3. Critical instrumentation finding

The current H4 implementation starts the CHARGER windup immediately after a completed attack. Any subsequent valid attack before the fixed 1200 ms deadline is treated as the tactical response and can interrupt the windup.

In this trace, each recorded tactical response latency was effectively equal to that action's ordinary inter-action interval. The overall H4 inter-action median was approximately 925 ms, while the stateful-response median was approximately 958 ms.

Therefore the current implementation does not isolate:

> telegraph visible -> player notices telegraph -> player intentionally changes action timing

Instead, it largely measures:

> telegraph starts immediately after prior attack -> next normal rhythm attack occurs before 1200 ms

This is a measurement confound.

## 4. Admission decision

This trace is valid evidence for:

- H4 page/runtime stability
- state-event wiring
- WINDUP_START emission
- INTERRUPTED emission
- state/action ordering
- high-mastery timing stability under the current presentation

This trace is **not admitted** for:

- reaction/counterplay latency fitting
- state-reading degradation fitting
- tactical-response combo-break probability
- SKILLED_V2 STATEFUL model fitting

Reason:

`TACTICAL_RESPONSE_NOT_SEPARATED_FROM_BASE_RHYTHM`

## 5. Required harness correction before H4 rerun

The next H4 revision must make telegraph timing sufficiently independent of the ordinary attack rhythm that the player must actually read and respond to the state.

Required properties:

1. WINDUP onset must not always occur immediately after the prior completed attack.
2. Telegraph onset should be phase-offset / jittered relative to the normal sweep cadence.
3. The response deadline must create some trials where simply waiting for the ordinary next ideal timing input is insufficient or meaningfully different from an intentional response.
4. Counterplay must still use the authoritative normal attack input; do not invent a separate response button.
5. The trace must record enough information to compare:
   - telegraph onset
   - expected ordinary next-action timing
   - actual response action timing
   - judgment quality
   - interrupt/full-activation result
6. H4 timing parameters introduced for measurement remain HARNESS_ONLY and must not be promoted to production CHARGER constants.

## 6. Related H3 instrumentation watch

The first observed H3 trace confirmed that raw STATE timestamps preserve turnover truth, but the convenience field `noTargetWaitMsBeforeAction` currently records 0 after target restoration because `noTargetSince` is cleared before the first post-turnover action.

This field should be repaired before broad trace collection. Existing H3 trace remains reconstructable and valid from STATE timestamps.

## 7. Next boundary

Before more H4/H5 stateful collection:

1. repair H3 direct no-target wait instrumentation,
2. revise H4 windup scheduling to deconfound state reading from ordinary rhythm,
3. deploy the isolated harness revision,
4. rerun H4 smoke,
5. admit H4 skill evidence only if reaction latency is behaviorally separable from baseline cadence.

No production gameplay or campaign balance changes are authorized by this audit.
