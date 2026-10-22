# SKILLED_V2 Harness — Implementation Status V0.1

Date: 2026-10-22 KST

## State

```text
SOURCE_IMPLEMENTATION = COMPLETE_V0_1
SOURCE_ISOLATION_CHECK = PASS
LOCAL_JS_SYNTAX_CHECK = PASS
LOCAL_SOURCE_SELFTEST = PASS
BROWSER_DEVICE_SMOKE = PENDING
SAMPLE_JSONL_CANONICAL_VALIDATION = PENDING
PUBLIC_CALIBRATION_DEPLOYMENT = NOT_AUTHORIZED
OBSERVED_PLAYER_TRACES = NONE
NUMERIC_SKILLED_V2_FIT = BLOCKED
```

## Branch / baseline

- implementation branch: `timing-defense-skilled-v2-harness-v01`
- source baseline: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production branch modified: **NO**
- distinct Worker name: `timing-defense-skilled-v2-harness`

## Implemented

- H0–H5 selector
- audited timing sweep semantics
- combo and charge/heavy X→Y flow
- P×P tracking
- H3 no-target / target-reorder STATE evidence
- H4/H5 CHARGER-style readable WINDUP state
- local anonymous calibration ID
- browser-local raw JSONL export
- browser-local bounded trace checks
- source selftest
- `/api/health` isolation metadata

## Isolation

The implementation contains no campaign room/WebSocket integration and no star/Tier/achievement/EXP/coin persistence path.
No external telemetry service is configured.

## Instrumentation watch

`noTargetWaitMsBeforeAction` is optional in schema V0.1. The harness preserves authoritative no-target timing via ordered `NO_TARGET_START`, `NO_TARGET_END`, and `TARGET_REORDER` STATE events plus first post-turnover action timing. Therefore the interval is derivable even if the convenience ACTION field is zero in the current V0.1 implementation.

Before broader collection, browser/device smoke should verify this convenience field. If it does not retain the prior no-target interval, either:
1. patch it to carry the closed interval into the first post-turnover ACTION, or
2. formally derive the field from raw ordered STATE records in the collection pipeline.

Raw event order must remain the authority.

## Next gate

Run bounded browser/device smoke for:
- H0: >=40 action records and combo sequence
- H3: turnover + no-target + reacquisition evidence
- H4: WINDUP_START + response linkage
- JSONL copy/download
- canonical dataset validator on exported traces

Do not deploy publicly or fit numeric SKILLED_V2 values until those gates pass.
