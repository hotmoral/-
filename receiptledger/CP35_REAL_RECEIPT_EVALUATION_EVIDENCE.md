# ReceiptLedger V1 — CP35 Real Receipt Evaluation Evidence

Updated: 2026-10-16 KST
Checkpoint: CP35
Canonical executable HEAD: `6ae9fbcfe0abc17dd9471de243170a9a87272767`

## 1. Canonical CI identity

- workflow: `ReceiptLedger V1 Real Receipt Evaluation`
- run: `38884870134`
- conclusion: SUCCESS
- job: `116920055654`
- artifact ID: `12038973171`
- artifact name: `receiptledger-v1-real-receipt-evaluation-38884870134`
- artifact digest: `sha256:3336486a5807fa971e8385cdd10008f29cb85daf1779ab5fd226008d9ad72258`

## 2. APK identity

- versionName: `1.0.33-real-receipt-evaluation`
- versionCode: 34
- compileSdk: 36
- targetSdk: 36
- minSdk: 23
- signing: debug only
- APK SHA-256: `3e89e7ab1358278889c55410fc49f4b5e4e50f54c8a490aeb473dd58c0cab9cf`
- APK ZIP integrity: PASS

## 3. Scope evidence

Predecessor handoff: `386c1b3d9ef7f3737ffd8b4d0f34fe2e076cab8e`

Executable diff to `6ae9fbcf...`:

- A `.github/workflows/receiptledger-v1-real-receipt-evaluation.yml`
- A `receiptledger/CP35_REAL_RECEIPT_EVALUATION_PLAN.md`
- A `receiptledger/REAL_RECEIPT_EVALUATION_CONSISTENCY_REVIEW.md`
- A `receiptledger/REAL_RECEIPT_EVALUATION_FIXTURES_V1.md`
- M `receiptledger/harness/android-v1/app/build.gradle`
- A `receiptledger/harness/android-v1/app/src/test/java/com/receiptledger/v1/evaluation/RealReceiptEvaluationV1Test.java`

CI explicitly verified no diff under production Java, AndroidManifest or production resources.

## 4. CP35 metric

`CP35_METRICS evaluation_version=1 fixtures=8 receipts=9 items=11 structured_correct=9 auto_confirmed=8 review_required=1 final_safe_registrations=7 exact_alias_reuse=2 conservative_unresolved=1 false_auto_links=0 strict_weight_observations=2 contextual_cohorts=2 discount_exclusions=1 invalid_exclusions=1 detail_trace_rows=7 schema_unchanged=1`

The metrics extractor required every field above to match exactly and required the CP35 JUnit suite to have zero failures/errors.

## 5. Fixture-ground-truth evidence

### STANDARD identity

- new `서울우유1L` had no automatic identity before confirmation;
- explicit confirmation created/linked a STANDARD stable identity;
- later exact `서울우유1L` receipts reused that stable ID through exact-alias authority;
- similar `서울우유900mL` remained UNCLASSIFIED;
- false automatic link count remained zero.

### NON_STANDARD comparability

- `감자 1kg` -> 6,000/kg;
- `감자 500g` -> 6,600/kg;
- both formed one strict `WEIGHT_KG` cohort;
- `감자 1봉` and `감자 1상자` formed separate contextual LIKE_FORM cohorts;
- contextual evaluation remained `CONTEXTUAL_ONLY` with judgment `NONE`.

### Discount safety

Synthetic multi-item receipt:

- milk 3,200;
- ramen 4,990;
- receipt-level coupon -500;
- printed total 7,690.

The linked milk observation was classified `UNALLOCATED_RECEIPT_DISCOUNT` and excluded from the comparable STANDARD_PACKAGE cohort. No guessed item-level discount allocation was produced.

### Invalid receipt safety

Synthetic mismatch:

- item sum 3,500;
- printed total 3,000;
- validation MISMATCH;
- CP33 decision REVIEW_REQUIRED.

A deliberate defense-in-depth link in the test still produced zero eligible price observations and `INVALID_RECEIPT` eligibility.

### Detail provenance

- CP31 Product Detail retained receipt IDs for two eligible milk purchases plus the excluded coupon receipt;
- CP32 Commodity Detail retained four potato receipt IDs across strict/contextual sections;
- total verified detail provenance rows: 7.

## 6. Regression evidence

Artifact XML inspection:

| Suite | Tests | Failures | Errors | Skipped |
|---|---:|---:|---:|---:|
| CP35 RealReceiptEvaluationV1Test | 1 | 0 | 0 | 0 |
| CP34 CommercialUiShellV1Test | 7 | 0 | 0 | 0 |
| CP33 CaptureReviewUxV2Test | 13 | 0 | 0 | 0 |
| CP32 CommodityDetailV1Test | 11 | 0 | 0 | 0 |
| CP31 ProductDetailV1Test | 9 | 0 | 0 | 0 |
| CP29 SearchBrowseV1Test | 8 | 0 | 0 | 0 |

Workflow also required CP28 PriceEvaluation and CP27 PriceIntelligence XMLs to exist and the complete Gradle unit suite finished successfully.

Lint report: `No issues found.`

## 7. Permission evidence

`aapt dump permissions` returned only:

- `com.receiptledger.v1.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`

Forbidden camera/media/storage/network permissions were absent.

## 8. Corpus / OCR boundary limitation

The public artifact contains only synthetic fixture definitions and deterministic test evidence.

It does not contain private real receipts.

The receipt corpus enters at synthetic `OcrDocument` token/geometry input and exercises the production `ReceiptRecognitionPipeline` from layout/structure onward. Consequently this evidence does **not** quantify ML Kit image-to-text accuracy or camera variability.

This distinction is material: CP35 validates correct purchase-registration semantics under controlled realistic receipt structures, not statistical optical-recognition accuracy across real merchants.

## 9. Performance limitation

No startup, OCR latency, memory, large-catalog, large-history, 1k/10k search, migration stress, archive reconciliation or recovery benchmark is claimed here. Those remain CP36.

## 10. Evidence conclusion

Within the declared public-safe corpus and token-boundary limitation, CP35 found:

- no false authoritative identity link;
- no fake commodity normalization;
- no unsupported discount attribution;
- no invalid price contamination;
- correct repeat exact-alias reuse;
- correct receipt provenance through CP31/32.

No production correction was required.
