# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-17 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP36 — Performance / Reliability — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-performance-reliability-20261016`
- predecessor CP35 handoff: `8a8a9ee0bb3bcd7e198f76b436087d54170a469d`
- frozen CP36 executable HEAD: `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`
- canonical Actions run: `38926526457` — SUCCESS
- canonical job: `117059359644` — SUCCESS
- artifact ID: `12057296715`
- artifact digest: `sha256:3e11a5b85f15ad860f4c5a9a81f948d79bb4dd80122fcba6b1f8d2bfffe85756`
- debug APK SHA-256: `f17ade820165ab40213f17c38b9e720488b7791aa3621b09b3b19cdd4a53c5f7`
- version: `1.0.34-performance-reliability` / versionCode 35
- lint: 0 errors / 0 warnings (`No issues found.`)

Any later handoff/status synchronization is documentation-only. The executable/evidence boundary remains `78cdd99c...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Current loop:

`홈 -> 영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 반복 구매 재사용 -> 검색/카테고리 -> 제품/품목 가격기억 -> 영수증 근거`

Receipts are input/evidence; trustworthy product/commodity price memory is the product outcome.

## 3. CP36 result

CP36 measured before optimizing. The first complete Android profile found CP29 discovery dominated by repeated SQLite product/link/receipt reads.

Only that measured bottleneck was changed:

- `SearchBrowseServiceV1.java` modified;
- read-only transient `SqliteSearchBrowseSnapshotV1.java` added.

No FTS, persistent cache, new index or schema was added.

Canonical final measurements:

- Home startup median/max: 516 / 748 ms;
- Home PSS: 42,787 KB;
- search 1k: 189 ms;
- search 10k: 1,524 ms;
- recent 10k: 856 ms;
- price 1k: 461 ms;
- detail 1k: 459 ms;
- chart 1k: 19 ms;
- OCR cold: 4,448 ms;
- OCR warm median: 4,078 ms;
- migration 1k: 4 ms;
- archive reconciliation: 41 ms;
- reopen cycles: 10;
- semantic failures: 0.

Search 10k improved from the valid baseline 17,106 ms to 1,524 ms.

## 4. Search semantic preservation

The optimized SQLite path remains read-only and uses the same CP29 ranking/filter/match semantics. Generic/in-memory stores retain the original path.

A dedicated Android parity test compares optimized SQLite output against an adapter-forced original/generic path for canonical, compact, structured, specification, observed-name, store, category, recent and frequent cases. It also verifies equivalent fail-fast handling for corrupt catalog evidence.

Result: **1/1 PASS**.

## 5. Explicit known V1 risk

The only final decision-budget breach is warm ML Kit OCR on the API 34 x86_64 CI emulator:

- final warm median: 4,078 ms;
- decision budget: 1,500 ms.

This was reproducible across valid runs and is explicitly accepted rather than hidden. Production OCR is unchanged because cold OCR and memory are within budget, the recognizer is already reused, the benchmark is emulator-based, and real-photo OCR accuracy versus resolution/merchant variation has not been established. Changing/downsampling OCR solely for this number could trade correctness for latency without evidence.

Physical-device / real-image OCR profiling is a post-V1 validation candidate only if separately authorized.

## 6. Frozen contracts

Unchanged:

- stable catalog ID identity authority;
- CP21–29 domain/search meaning and ranking authority boundary;
- CP27 comparison eligibility;
- CP28 thresholds;
- CP30 design system;
- CP31/32 detail semantics;
- CP33 capture/review/save/provenance;
- CP34 commercial shell;
- CP35 registration-safety conclusions;
- OCR/recovery/item/validation semantics;
- product schema 2 / receipt schema 1;
- programmatic `Activity + android.widget` architecture;
- offline/no-network/no-broad-permission posture.

## 7. Regression / privacy evidence

Canonical Run #11 passed:

- public namespace and bounded-scope guards;
- full JVM unit regression;
- CP29 search regression;
- CP31–35 and price/evaluation regressions;
- lint 0/0;
- APK + AndroidTest build;
- Android startup/memory/runtime profile;
- migration/archive/reopen checks;
- SQLite search parity;
- evidence packaging.

Forbidden CAMERA/media/storage/network permissions remain absent.

## 8. Completed V1 checkpoint chain

CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> CP26 Commodity / Non-standard V2 -> CP27 Price Intelligence V2 -> CP28 Price Evaluation -> CP29 Search / Browse -> CP30 Design System Foundation -> CP31 Product Detail -> CP32 Commodity Detail -> CP33 Capture / Review UX V2 -> CP34 Commercial UI Shell -> CP35 Real Receipt Evaluation -> **CP36 Performance / Reliability**.

The planned V1 roadmap through CP36 is complete.

## 9. Next work boundary

**No post-V1 checkpoint is currently authorized.**

Do not begin a physical-device campaign, OCR redesign, new feature group, schema change or broader optimization without explicit user authorization.

If post-V1 work is authorized, first recover the CP36 frozen executable and current docs-only handoff separately and define a new bounded checkpoint before implementation.

## 10. Canonical restart order

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

GitHub is canonical. Verify live handoff HEAD and frozen executable HEAD separately.

## 11. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase DB/backups, personal identifiers or uncleared assets.

**Current stop condition: planned V1 CP20–CP36 complete. Await explicit authorization for any post-V1 work.**