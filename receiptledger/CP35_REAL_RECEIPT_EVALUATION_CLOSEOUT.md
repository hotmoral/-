# ReceiptLedger V1 — CP35 Real Receipt Evaluation Closeout

Updated: 2026-10-16 KST
Checkpoint: **CP35 — Real Receipt Evaluation**
Status: **PASS / COMPLETE**

## 1. Frozen execution boundary

- branch: `receiptledger/run-v1-real-receipt-evaluation-20261016`
- predecessor CP34 handoff: `386c1b3d9ef7f3737ffd8b4d0f34fe2e076cab8e`
- predecessor CP34 frozen executable: `d9764b1447aefaaf3e3fdc5785c72c7c98e8314e`
- frozen CP35 executable/evaluation HEAD: `6ae9fbcfe0abc17dd9471de243170a9a87272767`
- canonical Actions run: `38884870134` — SUCCESS
- canonical job: `116920055654` — SUCCESS
- artifact ID: `12038973171`
- artifact digest: `sha256:3336486a5807fa971e8385cdd10008f29cb85daf1779ab5fd226008d9ad72258`
- debug APK SHA-256: `3e89e7ab1358278889c55410fc49f4b5e4e50f54c8a490aeb473dd58c0cab9cf`
- version: `1.0.33-real-receipt-evaluation` / versionCode 34
- lint: `No issues found.`

Any later status/handoff synchronization is documentation-only. The executable/evidence boundary remains `6ae9fbcf...`.

## 2. What CP35 evaluated

CP35 tested the frozen system as a purchase-registration pipeline rather than as isolated OCR components:

`synthetic OcrDocument tokens/geometry -> production ReceiptRecognitionPipeline -> ReceiptRecord -> CP33 review assessment -> exact identity confirmation/reuse -> CP27 price intelligence -> CP28 contextual safety -> CP31/32 detail projections -> exact receipt provenance`

The primary success criterion was **correct purchase registration**, not OCR character accuracy.

## 3. Public-safe corpus

Eight risk classes / nine synthetic receipt instances / eleven item rows were evaluated:

1. new STANDARD product requiring explicit confirmation;
2. confirmed STANDARD exact-alias repeat reuse;
3. similar-but-not-exact STANDARD name remaining unresolved;
4. NON_STANDARD 1kg + 500g strict WEIGHT_KG normalization;
5. NON_STANDARD 봉 + 상자 contextual separation;
6. multi-item receipt-level discount exclusion;
7. arithmetic mismatch forcing review and invalid-price exclusion;
8. CP31/32 detail-to-receipt traceability.

All merchant names, dates, products and prices in the fixture corpus are synthetic/public-safe.

## 4. Evaluation result

Canonical metric:

`CP35_METRICS evaluation_version=1 fixtures=8 receipts=9 items=11 structured_correct=9 auto_confirmed=8 review_required=1 final_safe_registrations=7 exact_alias_reuse=2 conservative_unresolved=1 false_auto_links=0 strict_weight_observations=2 contextual_cohorts=2 discount_exclusions=1 invalid_exclusions=1 detail_trace_rows=7 schema_unchanged=1`

Key outcomes:

- all nine receipt instances produced the expected structure/merchant/date/total/item tuples;
- eight valid receipts were AUTO_CONFIRMED by CP33;
- the deliberate mismatch remained REVIEW_REQUIRED;
- false automatic identity links: **0**;
- the confirmed exact alias was reused on both later matching receipts;
- `서울우유900mL` did not inherit the confirmed `서울우유1L` identity;
- 1kg and 500g potato observations normalized to 6,000/kg and 6,600/kg in one WEIGHT_KG cohort;
- 봉 and 상자 remained separate LIKE_FORM cohorts and CP28 returned CONTEXTUAL_ONLY / NONE;
- an unattributed -500 multi-item coupon excluded the linked milk observation instead of fabricating an item price;
- an invalid/mismatched receipt stayed outside eligible price history even when deliberately linked in the test as a defense-in-depth check;
- seven CP31/32 purchase rows retained exact source receipt IDs.

## 5. Production change result

CP35 remained evaluation-only.

Compared with predecessor handoff `386c1b3d...`, the frozen CP35 execution diff contains only:

- CP35 workflow;
- three CP35 evaluation/specification Markdown files;
- test-only `RealReceiptEvaluationV1Test.java`;
- version bump in `app/build.gradle`.

No production Java, AndroidManifest or production resource file changed.

Frozen product schema 2 and receipt schema 1 remain unchanged.

## 6. Regression result

Canonical packaged evidence includes:

- CP35 evaluation test: 1/1 PASS;
- CP34 Commercial UI Shell: 7/7 PASS;
- CP33 Capture / Review UX V2: 13/13 PASS;
- CP32 Commodity Detail: 11/11 PASS;
- CP31 Product Detail: 9/9 PASS;
- CP29 Search / Browse: 8/8 PASS;
- lint: 0 issues;
- debug APK build: PASS.

The full unit suite executed successfully before artifact packaging.

## 7. Privacy / permissions

Packaged permissions remain limited to the internal dynamic-receiver permission.

Absent as required:

- CAMERA;
- READ_MEDIA_IMAGES;
- READ_EXTERNAL_STORAGE;
- WRITE_EXTERNAL_STORAGE;
- MANAGE_EXTERNAL_STORAGE;
- INTERNET;
- ACCESS_NETWORK_STATE.

No private real receipt, personal identifier, real purchase database or signing secret was added.

## 8. Evidence limitation

The checkpoint name remains the roadmap's **Real Receipt Evaluation**, but the canonical public evidence is deliberately public-safe and synthetic.

Fixtures begin at the `OcrDocument` token/geometry boundary. Therefore CP35 proves the downstream recognition/structure/registration/identity/price/detail contracts for those realistic receipt shapes, but **does not measure**:

- ML Kit image-to-text character recognition accuracy;
- camera/image quality variation;
- merchant/font statistical coverage;
- physical-device usability;
- production-scale latency/memory/reliability.

These limitations are explicit and must not be silently reinterpreted as real-world OCR accuracy evidence.

## 9. Post-green review

The first implementation run was green. It was not accepted merely because CI passed.

Post-green review verified:

- production source remained unchanged;
- purchase-form evidence is saved only after item identity linkage, matching the production persistence contract;
- repeat exact-alias evaluation uses the same `resolveAndLinkExact()` authority used by CP33 post-save reuse;
- CP29 search behavior remains separately regression-covered and does not need to become identity authority inside the CP35 harness;
- no material missing contract justified another implementation revision.

Therefore run `38884870134` is the canonical CP35 run.

## 10. Next boundary

**CP36 — Performance / Reliability — NOT STARTED**

CP36 may benchmark startup/OCR latency and memory, representative large catalog/history workloads, CP29 search scaling, price/detail workloads, migrations, archive reconciliation and recovery. It must not be started without explicit user authorization.
