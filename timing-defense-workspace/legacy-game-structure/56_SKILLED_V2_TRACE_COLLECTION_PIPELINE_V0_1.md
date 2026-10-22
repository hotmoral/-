# Timing Defense — SKILLED_V2 Trace Collection Pipeline V0.1

Date: 2026-10-22 KST  
Status: **DATA-COLLECTION CONTRACT / NO OBSERVED DATA YET / NO FITTED PROFILE**

Depends on:
- `55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
- `24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`

Machine-readable trace schema:
- `data/skilled_v2_trace_schema_v0_1.yaml`

Dataset validator:
- `tools/validate_skilled_v2_trace_dataset.py`

Summary tool:
- `tools/summarize_skilled_v2_trace_dataset.py`

---

# 0. Purpose

The project must not jump from a qualitative statement such as "combo40 is easy when concentrating" directly to invented PERFECT percentages.

The next valid source of player-skill numbers is **observed controlled trace data**.

This pipeline specifies:
- what one trace session contains
- which action/state events are required
- how context is labeled
- which records are excluded from fitting
- which aggregate outputs may be computed before model fitting
- what evidence is still required before a profile may be named `SKILLED_V2_*`

---

# 1. Dataset form

Recommended transport format:
`JSONL`.

Record types:

```text
SESSION_START
ACTION
STATE
SESSION_END
```

Every record must contain:
- `recordType`
- `traceId`
- `harnessVersion`
- `harnessId`

Ordered records for the same `traceId` must be reconstructable by `atMs` and sequence fields.

---

# 2. SESSION_START

Minimum fields:

```yaml
recordType: SESSION_START
traceId: string
harnessVersion: skilled-v2-controlled-harness-v0.1
harnessId: H0|H1|H2|H3|H4|H5
attemptIndex: integer
calibrationFlags: [string]
```

Optional but useful:
- anonymousPlayerId
- classId
- powerMode
- startedAt
- device context
- input surface/version

Privacy rule:
Do not require personally identifying information for player-model fitting.
An anonymous stable ID is enough when repeated-player grouping is needed.

---

# 3. ACTION

Required:

```yaml
recordType: ACTION
traceId: string
harnessVersion: string
harnessId: string
seq: integer
atMs: integer
pressureContext: BASELINE|TEMPO|DURABLE|TURNOVER|STATEFUL|MIXED
judgment: PERFECT|GOOD|NORMAL|MISS|INVALID
comboBefore: integer
comboAfter: integer
comboBreakCause: NONE|TIMING|TARGET_TURNOVER|NO_TARGET|TACTICAL_RESPONSE|INVALID_INPUT|OTHER
chargeBefore: integer
chargeAfter: integer
heavyOpportunity: boolean
heavyAttempted: boolean
heavyCompleted: boolean
ppAttempted: boolean
ppCompleted: boolean
```

Context fields:
- targetId
- targetType
- targetGeneration
- targetChangedSincePriorAction
- noTargetWaitMsBeforeAction
- interActionMs
- reacquireDelayMs

Validation relationships:
- `ppCompleted => ppAttempted`
- `heavyCompleted => heavyAttempted`
- `heavyAttempted => heavyOpportunity` unless an explicit invalid-attempt flag is present
- seq strictly increases within trace
- `comboAfter < comboBefore` should have a non-NONE break cause unless the game authority explicitly resets combo for another recorded reason

---

# 4. STATE

Required:

```yaml
recordType: STATE
traceId: string
harnessVersion: string
harnessId: string
atMs: integer
monsterId: string
monsterType: string
state: WINDUP_START|WINDUP_END|INTERRUPTED|FULL_ACTIVATION|TARGET_REORDER|NO_TARGET_START|NO_TARGET_END|OTHER
```

Optional:
- readableSinceMs
- relatedActionSeq
- targetBefore
- targetAfter

H4 must have stateful-readable evidence.
A trace labeled H4 with no readable state event cannot be used to estimate stateful degradation.

---

# 5. SESSION_END

Required:

```yaml
recordType: SESSION_END
traceId: string
harnessVersion: string
harnessId: string
endedAtMs: integer
completedAsDesigned: boolean
exclusionReasons: [string]
```

If `completedAsDesigned=false`, raw data may be retained for diagnosis but must not silently enter the primary fit.

---

# 6. Dataset validation levels

## L0 — structural
- parseable JSONL
- known record types
- required fields
- H0..H5 known harness IDs
- unique SESSION_START/END per trace
- ordered action seq
- nonnegative timestamps

## L1 — semantic
- pressure context matches harness family
- heavy/P×P logical consistency
- combo-break cause consistency
- H4 contains stateful-read event
- H3 contains target-turnover evidence
- H0 contains enough valid action opportunity to evaluate combo40 when marked as completed

## L2 — fitting admission
Requires actual sample coverage.

Must report:
- trace count
- anonymous player count if available
- per-harness session count
- completed vs excluded traces
- action count
- coverage gaps

L2 does not require an arbitrary universal minimum sample count in V0.1.
The report must expose uncertainty rather than pretending small-N is precise.

---

# 7. Pre-fit summaries allowed

Before fitting a stochastic player model, it is valid to compute descriptive evidence:

Timing by harness:
- judgment counts/shares
- inter-action quantiles

Combo:
- reach10/20/40/60
- longest-combo distribution
- break causes

Heavy/P×P:
- opportunity
- attempt rate
- completion conditional on attempt

Turnover:
- target-change count
- reacquire-delay distribution
- first-post-turnover judgments

Stateful:
- readable-state to response latency
- response success
- judgment change around response window

These are observations, not yet simulator parameter authority.

---

# 8. Pairing H0 with pressure contexts

Where repeated-player data exists, pressure degradation should preferentially use within-player deltas:

```text
H1 - same player's H0
H2 - same player's H0
...
H5 - same player's H0
```

This reduces the risk of treating differences between people as pressure degradation.

When paired H0 is unavailable, mark the estimate as unpaired and increase uncertainty.

---

# 9. Fitting admission gate

A dataset is not automatically a fitted SKILLED_V2 dataset because it passes structural validation.

Before fitting:
- identify exclusions
- verify H0–H5 coverage
- identify player/session grouping
- ensure combo40 opportunity existed in suitable traces
- ensure no single trace dominates action count
- verify H3/H4 contain the intended context events

If data is insufficient, output:
`INSUFFICIENT_OBSERVED_TRACE_COVERAGE`.

Do not fill missing contexts with invented probabilities.

---

# 10. Combo40 evidence handling

The user anchor is qualitative and strong:
combo40 should not be an extraordinary high-mastery-only event.

Observed trace reports must therefore explicitly show:
- number of traces with a real combo40 opportunity
- number reaching combo40
- harness/context where it occurred
- longest combo distribution

If observed CENTRAL-candidate skilled traces routinely reach 40 in clean/stable contexts, the fitted model must preserve that.

If a dataset appears to contradict the anchor, first inspect:
- harness contamination
- insufficient opportunity length
- unfamiliar controls
- sample composition
- instrumentation error

Do not automatically discard the user anchor or force the data to match it.

---

# 11. Anti-manipulation rule for the 60% target

The `<60%` non-T1 full-Tier target is a **game difficulty design goal**, not a player-model fitting target.

Forbidden workflow:

```text
Tier clear too high
 -> lower fitted skilled accuracy
 -> simulation now <60%
```

Required workflow:

```text
observed traces
 -> fit player model
 -> freeze/bound player model for the calibration pass
 -> simulate Tier
 -> if too easy, tune game content/power/economy
```

This separation is mandatory for trustworthy calibration.

---

# 12. Data quality classifications

- `TRACE_SCHEMA_INVALID`
- `HARNESS_CONTEXT_MISMATCH`
- `INCOMPLETE_TRACE`
- `TURNOVER_EVIDENCE_MISSING`
- `STATEFUL_EVIDENCE_MISSING`
- `COMBO40_OPPORTUNITY_MISSING`
- `HEAVY_LOGIC_INCONSISTENT`
- `PP_LOGIC_INCONSISTENT`
- `SINGLE_TRACE_DOMINANCE`
- `INSUFFICIENT_OBSERVED_TRACE_COVERAGE`
- `PLAYER_GROUP_LEAKAGE_RISK`

---

# 13. Current boundary

Planning/data/tooling can now validate incoming traces and produce descriptive summaries.

What cannot be done honestly yet:
- name numeric `SKILLED_V2_CENTRAL` parameters
- claim combo40 probability
- claim pressure-degradation percentages
- claim the non-T1 <60% Tier gate has been calibrated

The next evidence-producing step is observed H0–H5 trace collection, either through an explicitly authorized playable calibration harness or equivalent controlled telemetry source.
