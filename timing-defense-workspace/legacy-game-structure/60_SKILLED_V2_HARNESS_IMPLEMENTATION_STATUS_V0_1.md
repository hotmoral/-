# Timing Defense — SKILLED_V2 Harness Implementation Status V0.1

Date: 2026-10-22 KST  
Status: **SOURCE IMPLEMENTED / ISOLATION PASS / BROWSER-DEVICE VALIDATION PENDING / NO DEPLOYMENT AUTHORITY**

Depends on:
- `55_SKILLED_V2_CONTROLLED_HARNESS_AND_FIT_SCHEMA_V0_1.md`
- `56_SKILLED_V2_TRACE_COLLECTION_PIPELINE_V0_1.md`
- `57_SKILLED_V2_COLLECTION_READINESS_REVIEW_V0_1.md`
- `58_SKILLED_V2_PLAYABLE_HARNESS_IMPLEMENTATION_CONTRACT_V0_1.md`
- `59_SKILLED_V2_HARNESS_IMPLEMENTATION_PREFLIGHT_V0_1.md`

---

# 0. Implementation identity

Validated source baseline:
`ea22cc279603394dc4b439b6fdbb0c83aff4299a`

Isolated implementation branch:
`timing-defense-skilled-v2-harness-v01`

Live implementation HEAD at this review:
`7c541e3eb1e51ef9788f943e4603debc5a775e79`

Dedicated project directory:
`timing-defense-skilled-v2-harness/`

Dedicated Worker name:
`timing-defense-skilled-v2-harness`

No public calibration deployment has been authorized or performed.

---

# 1. Isolation verification

Compared with source baseline `ea22cc279...`, the implementation branch adds only the dedicated harness directory.

No existing production v0.45 gameplay file is modified.

Harness contains no production room/WebSocket integration and no persistence route for:
- stars
- Tier records
- achievements/titles
- campaign EXP/coin
- shop state
- multiplayer session state

No external telemetry service is configured.
Raw traces remain local until the player explicitly copies/downloads JSONL.

Result:
`SOURCE_ISOLATION = PASS`.

---

# 2. Implemented surface

Implemented H0–H5 selector:
- H0 TIMING_BASELINE
- H1 SUSTAINED_TEMPO
- H2 DURABLE_RHYTHM
- H3 TURNOVER_DENSITY
- H4 STATEFUL_READ
- H5 MIXED_PRESSURE

Implemented audited timing/input semantics:
- normal one-way sweep 1100ms
- input lock 100ms
- GOOD width .42
- PERFECT width .17
- normalized sweep .06..94
- charge 3 then heavy opportunity
- heavy X -> Y delay 85ms
- normal recovery 390ms
- PERFECT combo continuation
- P×P tracking

H1/H5 deliberately alter context pressure cadence for measurement. Those values are harness context parameters, not production balance.

---

# 3. Trace implementation

Local trace records:
- SESSION_START
- ACTION
- STATE
- SESSION_END

Implemented observations include:
- judgment sequence
- combo before/after and break cause
- charge before/after
- heavy opportunity / attempt / completion
- P×P attempt / completion
- action cadence
- H3 no-target and target reorder STATE evidence
- first post-turnover reacquisition timing
- H4/H5 WINDUP_START and response linkage
- local anonymous calibration identity

Export:
- copy JSONL
- download JSONL

Browser performs a bounded end-of-run semantic check.
Canonical dataset validation remains the authority after export.

---

# 4. Source checks completed

Completed before this status:
- JavaScript syntax check: PASS
- source contract selftest: PASS
- source-baseline isolation comparison: PASS

The selftest asserts:
- H0–H5 exist in code/UI
- H0 exposes >=40 action opportunities
- H3 turnover evidence path exists
- H4 WINDUP evidence path exists
- campaign persistence flag false
- external telemetry flag false
- campaign room/WebSocket/persistence tokens absent
- audited timing constants preserved

This is source validation, not browser/device execution evidence.

---

# 5. Instrumentation WATCH

Schema V0.1 makes `noTargetWaitMsBeforeAction` optional.

The current implementation preserves the authoritative interval in ordered:
- NO_TARGET_START
- NO_TARGET_END
- TARGET_REORDER
- first post-turnover ACTION timestamp

Therefore the true no-target interval is reconstructable from raw records.

However the convenience ACTION field `noTargetWaitMsBeforeAction` may be zero after the target has already returned because the live in-browser state clears the open interval at `NO_TARGET_END`.

Before broad trace collection:
- verify this field in browser smoke,
- then either carry the closed interval into the first post-turnover ACTION or formally derive it in the raw-trace pipeline.

This WATCH does not erase H3 ground truth because ordered STATE timestamps are retained.

---

# 6. Validation still required

Not yet proven by device/browser evidence:
- actual tap/SPACE feel matches intended timing semantics
- H0 can complete with >=40 ACTION records in a real browser session
- H3 produces correct turnover/reacquisition trace under real interaction
- H4 visibly produces windup and links response action correctly
- copy/download JSONL works on target browser/device
- exported sample passes canonical `validate_skilled_v2_trace_dataset.py`
- mobile viewport/touch behavior is usable

No observed skilled-player dataset exists yet.

---

# 7. Current admission

```text
HARNESS_SOURCE_IMPLEMENTATION = PASS_V0_1
SOURCE_ISOLATION = PASS
BROWSER_DEVICE_SMOKE = PENDING
SAMPLE_TRACE_SCHEMA_VALIDATION = PENDING
PUBLIC_CALIBRATION_DEPLOYMENT = NOT_AUTHORIZED
OBSERVED_H0_H5_DATA = MISSING
SKILLED_V2_NUMERIC_FIT = BLOCKED
```

---

# 8. Exact next boundary

Next bounded tranche:
**HARNESS BROWSER/DEVICE VALIDATION + PILOT TRACE READINESS**

Order:
1. run H0 browser smoke and verify >=40 ACTION trace path
2. run H3 and inspect target-turnover/no-target/reacquisition evidence
3. run H4 and inspect WINDUP_START/response linkage
4. fix any trace fidelity defects found
5. export sample JSONL
6. run canonical trace validator
7. verify no campaign/external persistence
8. only after PASS decide whether an isolated calibration deployment is needed for controlled pilot collection
9. collect small pilot traces
10. perform data-quality review before any numeric fit

No production v0.45 deployment or campaign change is authorized by this status.
