# ReceiptLedger — Product / Validation Roadmap

Updated: 2026-10-17 KST

## 1. Completed V1 chain

CP20–CP36 is complete. CP36 closed the measured SQLite search bottleneck while leaving OCR as a physical-device validation risk.

## 2. CP37 — Physical Device / Real-Image OCR Validation — IN PROGRESS

### Phase A — validation instrumentation

Completed and frozen before physical testing.

### Remediation A — false item row / recoverability

Triggered by the first real-device sample where an address/header row was classified as an item and could not be deleted.

Remediation A added:

- narrow pre-date false-item gating;
- explicit `이 항목은 상품이 아님` removal recovery;
- removal provenance.

Physical retest confirmed the triggering address row no longer appeared as an item.

### Review-Coverage Instrumentation — READY_FOR_PHYSICAL_METRIC_CHECK

The Remediation A retest also showed a selective-review evidence gap: initial review selected only 1 of 15 items, while full visual verification resulted in multiple item corrections.

To quantify this without changing review behavior, report schema v2 adds:

- `corrections_outside_review_items`
- `review_scope_miss`

Frozen executable:

- `7dbed4cf73a2963ace7447974e9d972a9776b79f`
- run `38976080450` SUCCESS
- artifact `12078898591`
- APK SHA-256 `29fcd2073d74fee819d53525bf2409db1587a72e72e86af115496843562405b8`
- version `1.0.37-review-coverage-validation` / 38

## 3. Current physical decision path

1. Run one v2 physical metric-check sample.
2. Confirm the new fields are emitted and interpretable.
3. If instrumentation is sound, begin the independent 10-receipt campaign using v2 only.
4. Aggregate correctness/safety/review burden/latency.
5. Only then decide whether review-policy or OCR remediation is justified.

Earlier v1 samples are diagnostic/remediation evidence, not part of the final 10-sample decision corpus.

## 4. Decision priority

1. correctness / false auto-confirm safety;
2. selective-review coverage;
3. save/provenance reliability;
4. review burden;
5. latency.

`false_auto_confirm=1` indicates whole-receipt trust failure.

`review_scope_miss=1` indicates at least one corrected item was outside the initial item review set, even if the receipt as a whole was REVIEW_REQUIRED.

## 5. Frozen authority gates

Still authoritative:

- stable catalog ID final identity authority;
- grouping != comparability;
- CP27/28 price contracts;
- CP29 discovery contract;
- Remediation A structure gate until new evidence justifies change;
- review-policy changes require physical evidence;
- product schema 2 / receipt schema 1;
- offline/no broad permission posture.

## 6. Scope discipline

Do not invent a broader classifier or change OCR/review policy from one sample. The current checkpoint is measurement-only. If the v2 campaign proves a systematic review-scope defect, define the smallest separate remediation boundary with before/after evidence.

## 7. Current stop

**Await one `RL_CP37_SAMPLE version=2 ...` physical report before any further implementation.**
