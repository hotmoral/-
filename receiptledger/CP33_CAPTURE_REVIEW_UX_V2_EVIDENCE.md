# ReceiptLedger V1 — CP33 Capture / Review UX V2 Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_CAPTURE_REVIEW_UX_V2_01`

## 1. Frozen implementation

- branch: `receiptledger/run-v1-capture-review-ux-v2-20261016`
- predecessor handoff: `1996668e1fec6961eb158c5dd2e6b673fdb46ee0`
- frozen implementation: `34cdac2d3e61081ab2a529173dbef9a2431431e0`
- workflow: `ReceiptLedger V1 Capture Review UX V2`
- run: `38874509796`
- job: `116886197267`
- conclusion: SUCCESS

## 2. Artifact

- artifact ID: `12034453925`
- artifact name: `receiptledger-v1-capture-review-ux-v2-38874509796`
- artifact digest: `sha256:36da341582f3e4083699a31d87eb5366b62e6c99c555d1fcd41dec4b9dd3f912`
- artifact size: 23,189,130 bytes
- debug APK SHA-256: `8f78d9dab92c65bdccd31008f9cd15221f26ef63dbfcfab2741e9a066d2237b0`

## 3. Build identity

Packaged `BUILD_IDENTITY.txt` records:

- `public_commit=34cdac2d3e61081ab2a529173dbef9a2431431e0`
- `predecessor_handoff=1996668e1fec6961eb158c5dd2e6b673fdb46ee0`
- `product_schema=2_UNCHANGED`
- `receipt_schema=1_UNCHANGED`
- `capture_auto_processing=YES`
- `mandatory_full_review=NO`
- `explicit_save_ack=REQUIRED`
- `selective_review=YES`
- `default_one_requires_confirmation=YES`
- `exact_alias_reuse=GLOBAL_CONFIRMED_ONLY`
- `fuzzy_identity=FORBIDDEN`
- `receipt_traceability=PRESERVED`
- `ui_architecture=PROGRAMMATIC_ANDROID_WIDGET_PRESERVED`
- `compose_migration=NONE`
- `material_dependency_added=NO`
- compileSdk/targetSdk `36`
- minSdk `23`
- version `1.0.31-capture-review-ux-v2` / code `32`
- signing `debug_only`

## 4. Canonical metric

`CP33_METRICS capture_review_version=2 auto_confirm_cases=2 review_required_cases=7 user_edit_exit=1 selective_review=1 full_edit=1 raw_ocr_preserved=1 exact_alias_reuse=1 unknown_alias_safe=1 link_failure_isolated=1 auto_processing=1 schema_unchanged=1`

## 5. Packaged test evidence

| Suite | Tests | Failures | Errors | Skipped |
| --- | ---: | ---: | ---: | ---: |
| CP33 CaptureReviewUxV2 | 13 | 0 | 0 | 0 |
| legacy ReceiptReviewEngine | 4 | 0 | 0 | 0 |
| CP32 CommodityDetailV1 | 11 | 0 | 0 | 0 |
| CP31 ProductDetailV1 | 9 | 0 | 0 | 0 |
| CP30 DesignSystemFoundationV1 | 9 | 0 | 0 | 0 |
| CP29 SearchBrowseV1 | 8 | 0 | 0 | 0 |
| CP28 PriceEvaluationV1 | 8 | 0 | 0 | 0 |
| CP27 PriceIntelligenceV2 | 8 | 0 | 0 | 0 |
| CP26 CommodityNonStandardV2 | 8 | 0 | 0 | 0 |

The workflow also requires the current category/identity/semantics/catalog/persistence contract test XMLs to exist after the full unit-test run.

## 6. Lint / build

- Gradle 8.13 / JDK 17
- `:app:testDebugUnitTest` PASS
- `:app:lintDebug` PASS
- `:app:assembleDebug` PASS
- Android lint: exactly `No issues found.`
- APK ZIP integrity check PASS

## 7. Permission evidence

Packaged permissions:

- internal `com.receiptledger.v1.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`

Forbidden permission checks PASS for:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

## 8. Scope/frozen-contract evidence

The workflow compares every CP33 execution against predecessor handoff `1996668e...` and permits only:

- CP33 plan/consistency/golden docs;
- CP33 workflow;
- app version;
- MainActivity capture/review orchestration;
- CP33 additive review helpers;
- ReceiptReviewDialog presentation;
- user-facing strings;
- CP33 tests.

It rejects changes to the frozen catalog/product/semantics/identity/category/commodity/commoditydetail/persistence/price/priceintel/priceeval/search/detail/design/ocr/recovery/item/validation packages and to CP31/32/detail/library and the frozen ReceiptReviewEngine/parser inputs.

Final Git compare from `1996668e...` to `34cdac2d...` contains exactly 12 CP33-allowed files. No other namespace or frozen package changed.

## 9. Behavioral evidence

CP33 unit/contract evidence covers:

- clean exact receipt auto-confirm;
- safe arithmetic-derived values auto-confirm;
- DEFAULT_ONE remains review-required until explicit confirmation;
- confirmation provenance without erasing original DEFAULT_ONE source;
- PARTIAL/UNKNOWN review gates;
- mismatch/incomplete/missing context review gates;
- corrected user edit exits mandatory review when material blockers are gone;
- raw OCR preservation;
- selective risky-item assessment;
- full edit escape path contract;
- exact alias reuse / unknown alias safety / per-item link failure isolation;
- automatic processing entry ordering;
- product/receipt schema unchanged.

## 10. Manual artifact inspection in closeout session

The downloaded canonical artifact was independently unpacked after Actions completion. The closeout session re-read:

- `APK_SHA256.txt`
- `lint-results-debug.txt`
- `BUILD_IDENTITY.txt`
- `CP33_CAPTURE_REVIEW_UX_V2_METRICS.txt`
- `APK_PERMISSIONS.txt`
- packaged test XML suite attributes

The values above match the artifact and Actions logs.

## 11. Non-canonical earlier runs

- `38873199997`: rejected; build/tests succeeded but lint found 27 obsolete UnusedResources warnings.
- `38873592904`: SUCCESS but not canonical; post-green plan/code review found material save-state/accessibility/review-fallback gaps.

Only run `38874509796` at implementation HEAD `34cdac2d...` is canonical.

## 12. Evidence limitations

Not demonstrated by this evidence:

- private real-receipt accuracy;
- emulator/device visual screenshot comparison;
- real-user task completion time;
- full CP34 navigation integration;
- CP35 real-receipt evaluation;
- CP36 scale/performance hardening.
