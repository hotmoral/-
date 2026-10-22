# Timing Defense — SKILLED_V2 Playable Harness Implementation Contract V0.1

Date: 2026-10-22 KST  
Status: **IMPLEMENTATION CONTRACT / NOT YET IMPLEMENTED / NO LIVE DEPLOYMENT AUTHORITY**

Depends on:
- `55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
- `56_SKILLED_V2_TRACE_COLLECTION_PIPELINE_V0_1.md`
- `57_SKILLED_V2_COLLECTION_READINESS_REVIEW_V0_1.md`

---

# 0. Purpose

This contract defines the smallest safe implementation needed to collect observed H0–H5 traces.

It is explicitly **not** a campaign feature.
It must not alter live v0.45 campaign/network/combat behavior.

---

# 1. Isolation boundary

Implementation must live in a dedicated calibration lane/branch or clearly isolated harness surface.

Required properties:
- no production campaign route replacement
- no star/Tier persistence
- no achievement/title mutation
- no shop/coin/EXP persistence
- no public campaign matchmaking integration
- no production balance freeze implied by harness constants
- all output clearly marked calibration data

A future deployment, if any, should use a separate calibration URL/surface or otherwise be unmistakably isolated from the normal game.

---

# 2. Reuse requirement

Where the variable is being measured, the harness must reuse the same authoritative semantics rather than approximate them visually.

At minimum reuse or exactly mirror:
- timing judgment boundaries/meaning
- combo increment/reset semantics
- charge/heavy construction
- P×P classification semantics
- target validity/frontmost semantics when relevant
- Lv6/N3 behavior only when a harness explicitly enables those layers

Any deliberate neutralization must be declared in emitted metadata.

---

# 3. Required harness selector

The playable surface must allow running:

```text
H0 TIMING_BASELINE
H1 SUSTAINED_TEMPO
H2 DURABLE_RHYTHM
H3 TURNOVER_DENSITY
H4 STATEFUL_READ
H5 MIXED_PRESSURE
```

Each run must display which harness/context is active.

It must not present these as campaign stages or grant campaign rewards.

---

# 4. H0 implementation intent

H0 must provide enough uninterrupted valid timing opportunities for combo40 measurement.

Avoid frequent target turnover.
If the target must be replaced:
- emit the turnover state
- mark the affected window
- exclude/segment that region from clean baseline estimation

The harness should not end merely because an ordinary GRUNT HP body is killed before sufficient baseline observations exist.
A harness-only stable/reference-target mechanism is allowed if it preserves the real timing-input semantics and is explicitly labeled as neutralized combat termination.

---

# 5. H1 intent

Use RUNNER-like sustained tempo pressure while keeping:
- geometry complexity low
- stateful mechanics off
- target turnover below H3 levels

The goal is pressure degradation, not target-reacquisition measurement.

---

# 6. H2 intent

Use BRUTE-like durable exposure.

Need enough continuous target time to observe:
- repeated combo behavior
- deliberate heavy attempts
- P×P execution
- cadence drift under long rhythm

---

# 7. H3 intent

Create frequent, intentional authoritative target changes.

Required telemetry:
- exact target reorder time
- no-target windows
- next valid action time
- first post-turnover judgment
- whether combo break is attributable to turnover

Do not add CHARGER/SIEGER telegraph complexity here.

---

# 8. H4 intent

Use a CHARGER stateful-read problem with already-validated role expression.

Required:
- readable windup state
- windup start timestamp
- first relevant response action
- interrupt outcome
- local timing judgments before/during/after response

Do not use a geometry in which CHARGER is routinely killed before windup; that would measure encounter authoring failure rather than player stateful-read skill.

---

# 9. H5 intent

Use at least two already-learned pressure families.

Requirements:
- no new mechanic teaching
- no hidden campaign progression
- enough duration to observe transfer degradation
- state/turnover events emitted when present

H5 is transfer validation, not baseline fitting.

---

# 10. Trace output

Every harness run must emit records compatible with:
- `data/skilled_v2_trace_schema_v0_1.yaml`

Recommended output:
- JSONL export
- one traceId per run
- deterministic ordered records

Required record families:
- SESSION_START
- ACTION
- STATE
- SESSION_END

The implementation should make it possible to retain the raw trace before aggregate transformation.

---

# 11. Anonymous repeated-player grouping

To measure within-player H0→H1..H5 degradation, an anonymous stable player/session grouping mechanism is useful.

Requirements:
- no real name required
- no sensitive personal data required
- anonymous ID may be locally generated
- user may reset the calibration identity

This contract does not authorize any new external tracking/analytics service.

---

# 12. Completion / exclusion UX

Each harness run should end with an explicit status:

```text
COMPLETED_AS_DESIGNED
ABORTED
INVALID_CALIBRATION_RUN
```

If invalid/aborted:
- retain diagnostic raw trace if useful
- populate exclusionReasons
- do not include it silently in the primary fitting dataset

---

# 13. Acceptance tests

Before trace collection begins, verify:

## Global
- campaign stars unchanged
- Tier records unchanged
- achievements/titles unchanged
- campaign EXP/coin unchanged
- JSONL trace passes schema validator

## H0
- >=40 action opportunities can occur in a completed run
- no unintended stateful events

## H3
- target turnover events are actually present
- reacquisition fields populate

## H4
- readable CHARGER state occurs
- state event and response linkage can be reconstructed

## All
- pressureContext matches harness ID
- action seq monotonic
- SESSION_START/END exactly once

---

# 14. Stop conditions

Do not proceed to numeric fitting if:
- one or more harness contexts cannot produce valid traces
- H0 cannot provide combo40 opportunity
- H3 turnover truth is missing
- H4 readable-state truth is missing
- trace records fail semantic validation
- calibration activity mutates campaign progression

---

# 15. Implementation routing

The implementation should be treated as a separate bounded calibration task.

Recommended sequence:

```text
implementation preflight
 -> isolated harness implementation
 -> local/device validation
 -> trace schema validation
 -> small pilot trace collection
 -> data-quality review
 -> broader controlled collection
 -> fitting
```

No live v0.45 production deployment is authorized by this document.

---

# 16. Current state

```text
HARNESS IMPLEMENTATION CONTRACT = READY
HARNESS IMPLEMENTATION = NOT STARTED
OBSERVED H0-H5 DATA = NOT AVAILABLE
NUMERIC SKILLED_V2 FIT = BLOCKED
```
