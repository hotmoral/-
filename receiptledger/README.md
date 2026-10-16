# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, product/domain specifications, validation, CI and debug APK evidence.

## Start here

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `CP36_PERFORMANCE_RELIABILITY_CLOSEOUT.md`
4. `CP36_PERFORMANCE_RELIABILITY_EVIDENCE.md`
5. `CP36_PERFORMANCE_RELIABILITY_PLAN.md`
6. `PERFORMANCE_RELIABILITY_CONSISTENCY_REVIEW.md`
7. `PERFORMANCE_RELIABILITY_VECTORS.md`
8. `CP35_REAL_RECEIPT_EVALUATION_CLOSEOUT.md`
9. `CP35_REAL_RECEIPT_EVALUATION_EVIDENCE.md`
10. `CP34_COMMERCIAL_UI_SHELL_CLOSEOUT.md`
11. `CP33_CAPTURE_REVIEW_UX_V2_CLOSEOUT.md`
12. `CP32_COMMODITY_DETAIL_CLOSEOUT.md`
13. `CP31_PRODUCT_DETAIL_CLOSEOUT.md`
14. `CP30_DESIGN_SYSTEM_FOUNDATION_CLOSEOUT.md`
15. `PRODUCT_REBASELINE_V1_ROADMAP.md`
16. `WORK_UNIT.md`

GitHub is canonical. Verify the current handoff branch HEAD and frozen executable ref separately before relying on old chat context.

## Current boundary

**CP36 — Performance / Reliability — COMPLETE**

- branch `receiptledger/run-v1-performance-reliability-20261016`
- predecessor CP35 handoff `8a8a9ee0bb3bcd7e198f76b436087d54170a469d`
- frozen executable HEAD `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4`
- canonical Actions `38926526457` — SUCCESS
- job `117059359644` — SUCCESS
- artifact ID `12057296715`
- artifact digest `sha256:3e11a5b85f15ad860f4c5a9a81f948d79bb4dd80122fcba6b1f8d2bfffe85756`
- APK SHA-256 `f17ade820165ab40213f17c38b9e720488b7791aa3621b09b3b19cdd4a53c5f7`
- lint `No issues found.`
- version `1.0.34-performance-reliability`, versionCode 35

The planned V1 checkpoint chain CP20 through CP36 is complete.

## Product direction

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Current experience:

`홈 -> 영수증 추가 -> 자동 처리/필요 검토 -> 저장 -> 반복 구매 재사용 -> 검색/카테고리 -> 제품/품목 가격기억 -> 영수증 근거`

## CP36 result

CP36 measured the frozen system before optimizing. The first valid Android baseline found CP29 SQLite discovery dominated by repeated product/link/receipt reads.

Bounded production remediation touched only:

- `SearchBrowseServiceV1.java`;
- `SqliteSearchBrowseSnapshotV1.java`.

No FTS, persistent cache, new index or schema was introduced.

Final canonical measurements:

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
- semantic failures: 0.

Search 10k improved from 17,106 ms to 1,524 ms while preserving CP29 semantics. Dedicated SQLite fast-path semantic and fail-fast parity is 1/1 PASS.

## Explicit known V1 risk

Warm ML Kit OCR on the canonical API 34 x86_64 CI emulator remains above the 1,500 ms decision budget at 4,078 ms median.

This is explicitly accepted for V1 rather than hidden or tuned around. Production OCR is unchanged because cold OCR and memory are within budget, recognizer reuse is already present, the measurement is emulator-based, and real-photo OCR accuracy versus image resolution/merchant variation is not statistically characterized.

Physical-device / real-image OCR profiling may be considered only as separately authorized post-V1 work.

## Frozen domain / architecture

CP21–35 identity/category/commodity/price/evaluation/search/detail/review/UI contracts remain frozen except for the bounded CP36 search read-path optimization described above.

- stable product ID remains identity authority;
- product schema 2;
- receipt schema 1;
- programmatic `Activity + android.widget`;
- no Compose/Material migration;
- no duplicate mutable price truth;
- offline/local OCR posture;
- no broad storage/media/network permissions.

## Evidence limits

CP35's public correctness corpus begins at synthetic `OcrDocument` token/geometry input. CP36's runtime measurements use a GitHub-hosted API 34 x86_64 emulator. Neither constitutes statistical physical-device real-photo OCR certification.

## Next work boundary

**No post-V1 checkpoint is currently authorized.**

Do not start physical-device campaigns, OCR redesign, new features, schema changes, broader optimization or release/signing work until explicitly authorized and bounded by a new checkpoint contract.

## Privacy/security

This repository is public. Never commit signing secrets, credentials, real private receipt photos, real purchase databases/backups, personal identifiers or uncleared assets.

The executable app intentionally does not request CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permissions.

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use other project namespaces or alter repo-wide settings without separate approval.
