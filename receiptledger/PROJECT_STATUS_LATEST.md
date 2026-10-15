# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Handoff boundary

The current implementation boundary is intentionally clean:

- Last completed implementation checkpoint: **V1 Build Hygiene Core**
- Frozen completed implementation commit: `53d03fc219d4b15bf09cebbc368ae6af6a55053a`
- Completed branch: `receiptledger/run-v1-build-hygiene-core-20261015`
- GitHub Actions run: `38755847381` — **SUCCESS**
- Build Hygiene artifact digest: `sha256:903e259ff0f2156cf14b8d5e39a2b3424f54ec97318df4290d31c63046f2ebd2`
- Android lint at the completed boundary: **0 errors / 1 warning**
- The one remaining warning is `OldTargetApi` because the completed baseline still uses compileSdk/targetSdk 35.

Next implementation checkpoint: **V1 Target API 36 Core**.

Branch already reserved for the next checkpoint:
`receiptledger/run-v1-target-api36-core-20261015`

Important: at handoff time, Target API 36 implementation has **not started**. The branch was created from the completed Build Hygiene commit. Handoff/status documentation may advance the branch HEAD after the frozen implementation commit, but those post-boundary commits must be documentation-only until the next GPT explicitly begins Target API 36 Core.

## 2. Completed checkpoint chain

The following ReceiptLedger V1 implementation branches exist and were completed in sequence before the handoff boundary:

1. Foundation
   - branch: `receiptledger/run-v1-foundation-20261015`
   - head: `d105820275a37e1bc3dc53b64b1b360330d4edd2`
   - minimal Android app + public GitHub Actions debug APK foundation

2. Image Intake / Document Core
   - branch: `receiptledger/run-v1-image-document-core-20261015`
   - head: `54675685541c2fd8cf3840db73aecbea64b18684`
   - camera via external camera app + constrained content URI, gallery/document picker, EXIF normalization, sampled decoding, conservative receipt quad detection, perspective transform

3. OCR Core
   - branch: `receiptledger/run-v1-ocr-core-20261015`
   - head: `3f0141a21c4fb70b7e05a4f5bb5fb0ae5fe3d92e`
   - bundled Korean ML Kit OCR, block/line/element model, source-coordinate preservation, offline permission removal

4. Layout Core
   - branch: `receiptledger/run-v1-layout-core-20261015`
   - head: `e075feb983a3179b23108fe9eb6bbea65ee93bcc`
   - re-clusters OCR elements into receipt rows using geometry rather than trusting ML Kit line grouping

5. Structure Core
   - branch: `receiptledger/run-v1-structure-core-20261015`
   - row roles such as HEADER / DATE / ITEM / DISCOUNT / TOTAL / PAYMENT / UNKNOWN, money/date candidates, explicit reasons

6. Item Tuple Core
   - branch: `receiptledger/run-v1-item-tuple-core-20261015`
   - head: `04268aac3c0de9d707972daf6f14ddd6d882b373`
   - item name / quantity / unit price / line amount with printed/inferred provenance and fail-closed arithmetic

7. Validation Core
   - branch: `receiptledger/run-v1-validation-core-20261015`
   - receipt-level arithmetic validation: `sum(item line amounts) + discounts = printed total`; mismatch values are preserved, not auto-corrected

8. Persistence Core
   - branch: `receiptledger/run-v1-persistence-core-20261015`
   - head: `8af6ec20a9e89cb2df3eeb1d7ed14c973afca3cf`
   - app-private SQLite receipt/item/validation persistence with transactional writes

9. Image Archive Core
   - branch: `receiptledger/run-v1-image-archive-core-20261015`
   - head: `fc3c1cf14f6bc9e5caa6b469da99e12d8008c06b`
   - app-private image archive, deterministic receipt-id mapping, orphan reconciliation

10. Receipt Library Core
    - branch: `receiptledger/run-v1-library-core-20261015`
    - head: `15a645148015bcce3530bd46fdb12a9ae580020a`
    - stored receipt list/detail/delete; detail image decoding is sampled and bounded

11. Review / Edit Core
    - branch: `receiptledger/run-v1-review-edit-core-20261015`
    - user review required before save; edits preserve user-edit provenance and trigger revalidation

12. Product Identity Core
    - branch: `receiptledger/run-v1-product-identity-core-20261015`
    - head: `803f8ea467a00e33ba1f11ed3c77750c6946e2a1`
    - STANDARD / NON_STANDARD / UNCLASSIFIED model; exact confirmed alias reuse only; fuzzy auto-merge forbidden

13. Price History Core
    - branch: `receiptledger/run-v1-price-history-core-20261015`
    - head: `3a89038e89b2e2773589bde075e84b0234ef45c0`
    - price observations derived from original receipts/product links; invalid receipts excluded; STANDARD gets comparable statistics while NON_STANDARD remains raw observations

14. OCR Quality / Recovery Core
    - branch: `receiptledger/run-v1-ocr-recovery-core-20261015`
    - head: `87116ee52b1738f7c3513672e2cd7a7958701449`
    - original pass first, contrast/adaptive-binary only when weak; maximum 3 real OCR passes; bounded bitmap reuse; quality/structure-aware candidate choice

15. Vertical Integration Core
    - branch: `receiptledger/run-v1-vertical-integration-core-20261015`
    - end-to-end contract from OCR coordinates through layout/structure/item/validation/review/persistence

16. Merchant / Store Core
    - branch: `receiptledger/run-v1-merchant-core-20261015`
    - head: `49d5cd6b1f195b7e31e5f867df53b2a6089196b3`
    - conservative merchant candidate extraction, generic receipt headings rejected, user-editable store name propagated to persistence and price history

17. Conservative Cross-Pass Merge Core
    - branch: `receiptledger/run-v1-cross-pass-merge-core-20261015`
    - head: `3f8c232a2b3db205290b77764545bdd2cb687979`
    - existing OCR passes can supplement spatially missing tokens/rows; merged candidate is derived without increasing OCR pass budget; adopted only when structure/validation score materially improves
    - Actions run `38753359280` — SUCCESS

18. Build Hygiene Core
    - branch: `receiptledger/run-v1-build-hygiene-core-20261015`
    - frozen implementation head: `53d03fc219d4b15bf09cebbc368ae6af6a55053a`
    - Actions run `38755847381` — SUCCESS
    - unit tests + `lintDebug` + `assembleDebug` + permission firewall + artifact packaging all pass
    - lint reduced from 17 errors / 9 warnings to 0 errors / 1 warning
    - API-23-incompatible collection APIs replaced rather than suppressed
    - immediate UI/resource warnings fixed (format strings, package visibility, draw allocation, app icon, hardcoded product button string, unused resources)

## 3. Current application invariants

These must remain preserved unless a future checkpoint explicitly changes them:

- Application ID: `com.receiptledger.v1`
- Minimum SDK: 23
- Current completed baseline compileSdk/targetSdk: 35
- Java: 17
- OCR: bundled Korean Google ML Kit text recognition
- OCR remains local/offline by design.
- APK must not request `INTERNET`, `ACCESS_NETWORK_STATE`, `CAMERA`, broad storage/media permissions, or `MANAGE_EXTERNAL_STORAGE`.
- Camera capture uses an external camera app with a constrained temporary content URI; the app itself does not request CAMERA permission.
- Gallery intake uses the system document/image picker rather than broad storage permission.
- Real receipt photos, real purchase databases, signing material, credentials, API keys, and private backups must never be committed to this public repository.
- Release signing is not performed in the public namespace. Public CI produces debug/unsigned artifacts only.
- Never use, modify, or depend on `mobi/*`, `einstein/*`, `linkline/*`, or any other project namespace.

## 4. Data / correctness invariants

- OCR coordinates are preserved in the normalized source-image coordinate system even when OCR runs on perspective-corrected or scaled/preprocessed images.
- Layout reconstruction operates from OCR element geometry rather than trusting upstream line grouping.
- Arithmetic inference is explicit and provenance-carrying; contradictions are not silently repaired.
- User review is required before recognized data becomes a saved receipt record.
- User edits trigger validation again and are distinguished from printed/inferred values.
- Product aliases are conservative. Exact confirmed alias matches may auto-link; fuzzy string similarity must not auto-merge products.
- Price history is derived from persisted receipt data/product links rather than copied into a second stale price table.
- Receipts with MISMATCH/INCOMPLETE validation are excluded from normal comparable price history.

## 5. Next checkpoint boundary: Target API 36 Core

Do not continue from chat memory alone. Read `SESSION_HANDOFF.md` and `TARGET_API36_CORE_PLAN.md` first.

The next checkpoint is specifically for:

- compileSdk 36
- targetSdk 36
- compatible AGP/Gradle toolchain update
- Android 16 edge-to-edge behavior handling for programmatic View UIs
- predictive-back impact audit
- keeping minSdk 23 compatibility
- retaining lint at 0 errors
- retaining privacy/offline permission firewall
- unit tests + lint + APK build + evidence artifact

Do not bundle unrelated OCR/parser/product/UI feature work into Target API 36 Core.
