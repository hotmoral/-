# ReceiptLedger — Session Handoff

Updated: 2026-10-17 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct current project state from old chat before reading current documents and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP37_PARTIAL_ROW_PREFILL_REMEDIATION_CLOSEOUT.md`
4. `receiptledger/CP37_PARTIAL_ROW_PREFILL_REMEDIATION_EVIDENCE.md`
5. `receiptledger/CP37_PARTIAL_ROW_PREFILL_REMEDIATION_PLAN.md`
6. `receiptledger/CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_CLOSEOUT.md`
7. `receiptledger/CP37_SELECTIVE_REVIEW_COVERAGE_INSTRUMENTATION_EVIDENCE.md`
8. `receiptledger/CP37_FALSE_ITEM_ROW_REMEDIATION_CLOSEOUT.md`
9. `receiptledger/CP37_PHYSICAL_DEVICE_OCR_VALIDATION_PHASE_A_CLOSEOUT.md`
10. `receiptledger/CP37_PHYSICAL_DEVICE_CAMPAIGN_PROTOCOL.md`
11. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
12. `receiptledger/README.md`
13. `receiptledger/WORK_UNIT.md`

## 1. Current state

V1 CP20–CP36 is complete. CP37 remains open.

Current state: **Remediation C READY_FOR_PHYSICAL_PREFILL_RETEST**.

- branch: `receiptledger/run-post-v1-partial-row-prefill-20261017`
- predecessor handoff: `d4f75d8120e4a9c347b3777c64b511e4f5d224d4`
- frozen executable: `01b22652a45889b6bfaa474131e0c5fa7f19e96e`
- Actions: `38979684033` SUCCESS
- job: `117237351555` SUCCESS
- artifact: `12080029714`
- artifact digest: `sha256:55300e9525851f02232dc03f9a528fcd5b3c9c30ba68e7a30eb0bdb6634d46c2`
- APK SHA-256: `65fe0827f3a9ebfeafbbf783c6c8f82544f8594203008692288ab74ec9eb1e0e`
- version: `1.0.38-partial-row-prefill-validation` / 39
- package: `com.receiptledger.v1.rowrecovery`
- label: `ReceiptLedger 검증 C`
- lint: `No issues found.`

Do not mark CP37 complete.

## 2. Physical findings so far

### False item row

The first real-device sample exposed an address/header row incorrectly treated as an item. Remediation A added a narrow pre-date gate and explicit item removal. Same-receipt retest physically confirmed the triggering false row no longer appeared.

### Selective review scope

Report v2 was added to count corrected item ordinals outside the initial selected review set.

The first v2 physical sample emitted:

- initial items 15;
- initial review items 1;
- corrections outside selected review items 2;
- `review_scope_miss=1`;
- `false_auto_confirm=0`.

The metric path is therefore physically verified, and a real review-scope miss exists.

### Repeated first-item blank fields

The same receipt, across validation builds, repeatedly showed the first item with blank quantity and unit price.

Source inspection identified a bounded solver gap: multiple recognized money values plus no parsed quantity fell to unresolved PARTIAL even when one printed unit-price candidate and printed line amount had an exact integer ratio.

A separate package-suffix OCR character confusion also repeated. No automatic text substitution has been added.

## 3. Remediation C behavior

`ItemTupleSolver` now pre-fills a missing quantity and retains the printed unit price only when:

- no quantity token was parsed;
- one and only one preceding printed money candidate is a valid unit price;
- line amount divides exactly by that unit price;
- inferred quantity is 1..99.

The item remains `PARTIAL` with arithmetic provenance and therefore remains review-required.

Non-integral or ambiguous cases remain unresolved.

## 4. Verification

Canonical metric:

`CP37_PARTIAL_PREFILL_METRICS version=1 item_tuple_tests=4 capture_review_tests=14 report_v2_tests=8 unique_integer_prefill=1 ambiguous_rejected=1 partial_review_preserved=1 report_v2_unchanged=1 schema_unchanged=1`

- ItemTupleSolver: 4/4 PASS
- CaptureReviewUxV2: 14/14 PASS
- DeviceValidationReport v2: 8/8 PASS
- full regression: PASS
- lint: clean
- APK packaging/permission checks: PASS

## 5. Exact next task

This is physical confirmation, not more coding.

1. install `ReceiptLedger 검증 C` side by side;
2. process the same receipt/image again;
3. check that the first item quantity is prefilled;
4. check that the first item unit price is prefilled;
5. confirm that this item is still explicitly included in the review UI;
6. visually inspect all other receipt fields, including items not highlighted;
7. correct all factual/structural errors;
8. save;
9. return only the generated `RL_CP37_SAMPLE version=2 ...` line;
10. separately state whether steps 3–5 passed.

The repeated diagnostic receipt does not count in the final 10 independent receipts.

## 6. Frozen/non-goals

Do not change before physical retest analysis:

- OCR model/options or text substitutions;
- recovery preprocessing/pass order;
- Remediation A structure gate;
- selective-review policy;
- report v2 semantics;
- identity/price/search/schema/permission posture.

## 7. Privacy

Real receipt images and values supplied in chat must not be committed to the public repository. Public evidence uses sanitized metrics and generic defect descriptions only.
