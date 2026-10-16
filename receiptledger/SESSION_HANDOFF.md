# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-17 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct execution state from old chat before reading the current canonical files and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP36_PERFORMANCE_RELIABILITY_CLOSEOUT.md`
4. `receiptledger/CP36_PERFORMANCE_RELIABILITY_EVIDENCE.md`
5. `receiptledger/CP36_PERFORMANCE_RELIABILITY_PLAN.md`
6. `receiptledger/PERFORMANCE_RELIABILITY_CONSISTENCY_REVIEW.md`
7. `receiptledger/PERFORMANCE_RELIABILITY_VECTORS.md`
8. `receiptledger/CP35_REAL_RECEIPT_EVALUATION_CLOSEOUT.md`
9. `receiptledger/CP35_REAL_RECEIPT_EVALUATION_EVIDENCE.md`
10. `receiptledger/CP34_COMMERCIAL_UI_SHELL_CLOSEOUT.md`
11. `receiptledger/CP33_CAPTURE_REVIEW_UX_V2_CLOSEOUT.md`
12. `receiptledger/CP32_COMMODITY_DETAIL_CLOSEOUT.md`
13. `receiptledger/CP31_PRODUCT_DETAIL_CLOSEOUT.md`
14. `receiptledger/CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
15. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
16. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
17. `receiptledger/README.md`
18. `receiptledger/WORK_UNIT.md`

Verify the live handoff branch HEAD and the frozen executable HEAD separately.

## 1. Latest executable checkpoint

**CP36 — Performance / Reliability — PASS / COMPLETE**

- branch: `receiptledger/run-v1-performance-reliability-20261016`
- predecessor CP35 handoff: `8a8a9ee0bb3bcd7e198f76b436087d54170a469d`
- predecessor CP35 frozen executable/evaluation: `6ae9fbcfe0abc17dd9471de243170a9a87272767`
- frozen CP36 executable HEAD: `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`
- canonical Actions: `38926526457` — SUCCESS
- canonical job: `117059359644` — SUCCESS
- artifact ID: `12057296715`
- artifact digest: `sha256:3e11a5b85f15ad860f4c5a9a81f948d79bb4dd80122fcba6b1f8d2bfffe85756`
- APK SHA-256: `f17ade820165ab40213f17c38b9e720488b7791aa3621b09b3b19cdd4a53c5f7`
- versionName `1.0.34-performance-reliability`, versionCode 35
- lint: `No issues found.`

Any later handoff/status synchronization is documentation-only. Do not move the executable/evidence boundary from `78cdd99c...`.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Current user loop:

`홈 -> 영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 반복 구매 재사용 -> 검색/카테고리 -> 제품/품목 상세 -> 내 과거 가격 판단 -> 영수증 근거`

Receipts are input/evidence; trustworthy product/commodity price memory is the product outcome.

## 3. CP36 result

CP36 measured before optimizing. The first valid Android baseline exposed a material CP29 SQLite discovery bottleneck:

- search 1k: 2,385 ms;
- search 10k: 17,106 ms;
- recent 10k: 10,267 ms.

Only this measured bottleneck was remediated. Production changes are limited to:

- modified `SearchBrowseServiceV1.java`;
- added read-only `SqliteSearchBrowseSnapshotV1.java`.

No FTS, persistent cache, new search index, schema or secondary truth was introduced.

Canonical final measurements:

- startup median/max: 516 / 748 ms;
- Home PSS: 42,787 KB;
- search 1k: 189 ms;
- search 10k: 1,524 ms;
- recent 10k: 856 ms;
- price intelligence 1k: 461 ms;
- Product Detail 1k: 459 ms;
- chart 1k: 19 ms;
- OCR cold: 4,448 ms;
- OCR warm median: 4,078 ms;
- migration 1k: 4 ms;
- archive reconciliation: 41 ms;
- reopen cycles: 10;
- semantic failures: 0.

## 4. Search semantics / reliability

The optimized SQLite path remains read-only and preserves CP29 authority boundaries, ranking, filters, match reasons, category behavior and identity non-authority.

A dedicated Android instrumentation parity test compares the optimized SQLite path against an adapter-forced original/generic CP29 path across canonical/compact/structured/specification/observed/store search, store filtering, category browse, recent and frequent ordering.

It also injects corrupt catalog-field evidence and verifies both paths fail fast.

Result: **1/1 PASS**.

## 5. Explicit accepted V1 risk

The only final decision-budget breach is warm ML Kit OCR on the canonical API 34 x86_64 CI emulator:

- final warm median: 4,078 ms;
- budget: 1,500 ms.

This breach is reproducible and explicitly accepted for V1, not hidden. Production OCR remains unchanged because:

- cold OCR is within the 5,000 ms budget;
- OCR memory remains within budget;
- the same recognizer instance is already reused;
- the benchmark is emulator-based, not physical-device certification;
- CP35 did not quantify real-photo OCR accuracy versus image resolution/merchant variation;
- reducing optical work solely to satisfy emulator latency could regress correctness without evidence.

Physical-device / real-image OCR profiling is a post-V1 candidate only if separately authorized.

## 6. Frozen upstream authority

Unchanged:

- stable catalog ID as final identity authority;
- product schema 2 / receipt schema 1;
- CP21–29 domain/search semantics;
- CP27 comparison eligibility and CP28 thresholds;
- CP30 design system;
- CP31/32 detail semantics;
- CP33 capture/review/save/provenance;
- CP34 commercial shell;
- CP35 registration-safety conclusions;
- OCR/recovery/item/validation semantics;
- programmatic `Activity + android.widget` architecture;
- offline/no-network/no-broad-permission posture.

## 7. Regression / privacy evidence

Canonical Run #11 passed:

- public namespace audit;
- bounded CP36 scope guard;
- complete JVM unit regression;
- CP29 and CP31–35 regressions;
- lint 0 errors / 0 warnings;
- APK + AndroidTest build;
- emulator startup/PSS profile;
- Android runtime performance/reliability profile;
- 1→2 migration with 1,000 products;
- archive reconciliation with 2,000 files / 1,000 stale removals;
- repeated reopen cycles;
- SQLite fast-path semantic/fail-fast parity;
- evidence packaging.

Forbidden CAMERA/media/storage/network permissions remain absent. No private receipt, real purchase DB, credential or release signing material was introduced.

## 8. Execution-history caution

Several early CP36 runs failed before valid product measurement because of CI bootstrap/harness issues: sdkmanager pipe handling, AndroidTest API/dependency setup, adb PATH, AVD path resolution and a legacy migration fixture normalization mismatch. Those are not product-performance failures.

Run #9 attempt 2 was accidentally re-run by the assistant while responding to a user stop request. It is retained only as repeatability evidence, not as the canonical run.

Canonical CP36 execution is exclusively:

`78cdd99c... / Actions 38926526457 / job 117059359644`.

## 9. Completed V1 boundary

The authorized V1 chain CP20 through CP36 is complete.

No post-V1 checkpoint is currently authorized. Do not start:

- physical-device campaigns;
- OCR redesign/downsampling;
- new product features;
- schema changes;
- broader optimization;
- release/signing work;

without explicit user authorization and a new bounded checkpoint definition.

## 10. Stop condition

**CP36 is complete and handoff-ready. Planned V1 CP20–CP36 is complete. Await explicit authorization for any post-V1 work.**
