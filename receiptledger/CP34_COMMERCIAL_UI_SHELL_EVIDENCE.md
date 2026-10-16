# ReceiptLedger V1 — CP34 Commercial UI Shell Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_COMMERCIAL_UI_SHELL_01`

## 1. Canonical identity

- predecessor handoff: `2a15e14e9897aa9785762faef1568254fbeb5f82`
- frozen executable: `d9764b1447aefaaf3e3fdc5785c72c7c98e8314e`
- branch: `receiptledger/run-v1-commercial-ui-shell-20261016`
- workflow: `ReceiptLedger V1 Commercial UI Shell`
- Actions run: `38878681881`
- job: `116899840083`
- result: SUCCESS

## 2. Artifact

- artifact ID: `12036721843`
- artifact name: `receiptledger-v1-commercial-ui-shell-38878681881`
- artifact digest: `sha256:61e31f76bcf1e8d4e7dc596807b2aacd6c7774ad8e9fe05f36b09b59d4a95258`
- debug APK SHA-256: `64899bfdd715780ecb864f033896f66e2c89d7186da338f2dd59c7fc2033a2af`
- versionName: `1.0.32-commercial-ui-shell`
- versionCode: `33`
- minSdk: 23
- targetSdk: 36
- compileSdk: 36
- signing: debug only

APK ZIP integrity check passed.

## 3. Packaged launcher

APK badging confirms the launchable activity is:

`com.receiptledger.v1.HomeActivity`

The manifest keeps capture/search/detail/history activities internal and exports only the launcher required by the app entry point.

## 4. Permission evidence

Packaged APK permission dump contains only the Android-generated internal dynamic-receiver permission:

`com.receiptledger.v1.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`

The following remain absent:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

Camera acquisition therefore continues through an external camera app/content-URI flow rather than a direct CAMERA permission.

## 5. Build / lint

Canonical run:

- `BUILD SUCCESSFUL`
- `:app:testDebugUnitTest` PASS
- `:app:lintDebug` PASS
- `:app:assembleDebug` PASS
- lint report: `No issues found.`

## 6. CP34 metric

`CP34_METRICS shell_version=1 launcher_home=1 add_receipt=1 search_browse=1 category_browse=1 standard_detail=1 commodity_detail=1 receipt_history=1 legacy_price_entry_removed=1 schema_unchanged=1`

## 7. Packaged regression evidence

Canonical artifact includes zero-failure test XML evidence for:

- CP34 Commercial UI Shell: 7 tests;
- CP33 Capture / Review UX V2: 13 tests;
- CP32 Commodity Detail: 11 tests;
- CP31 Product Detail: 9 tests;
- CP29 Search / Browse: 8 tests.

The workflow also requires the frozen design/price-evaluation/price-intelligence regression result files and executes the full debug unit-test task.

## 8. Scope guard

The canonical workflow diffs from predecessor handoff `2a15e14e...` and permits only the CP34 plan/evidence-contract files, CP34-prefixed workflow, application version/manifest/strings, new Home/Search/shell files, Library integration and CP34 tests.

It explicitly rejects changes to frozen packages including:

- catalog/product/semantics/identity/category;
- commodity/commoditydetail;
- persistence/price/priceintel/priceeval/search/detail/design;
- OCR/recovery/item/validation/review.

It also verifies `MainActivity`, `ProductDetailActivity`, `CommodityDetailActivity`, `PriceHistoryActivity` and `ReceiptDetailActivity` remain unchanged from the predecessor.

## 9. Schema evidence

- ProductCatalogSchema version: 2, unchanged
- ReceiptSchema version: 1, unchanged

No migration was introduced.

## 10. Navigation evidence

Static contract checks and implementation review confirm:

- Home -> CP33 MainActivity for receipt add;
- Home -> SearchBrowseActivity;
- Home -> LibraryActivity;
- Home recent preview -> stable-ID Product/Commodity detail;
- Search -> frozen CP29 text search;
- recent/frequent/category modes -> frozen CP29 APIs;
- STANDARD -> CP31 ProductDetailActivity;
- NON_STANDARD -> CP32 CommodityDetailActivity;
- unsupported/unclassified -> no classification promotion;
- Library receipt rows -> ReceiptDetailActivity;
- legacy PriceHistoryActivity is not a Library primary navigation destination.

CP31/32 purchase-history rows already route to the exact receipt ID, preserving receipt provenance through the commercial shell.

## 11. Post-green review evidence

Run `38877971396` at `fd947ebf...` passed, but was rejected as canonical after manual plan/code review identified:

- Library fixed-header/list-only scrolling risk on constrained height or enlarged text;
- missing explicit Library list-read failure state.

Final `d9764b...` makes the whole Library page vertically scrollable, applies CP30 max-width behavior and provides a deterministic failure state. Full CI was rerun; `38878681881` passed.

## 12. Evidence limitations

No private real-receipt dataset was added to this public repository. No device screenshot comparison, real-user timing study, large-scale 1k/10k search benchmark or release signing evidence is part of CP34.

Those remain future validation/hardening concerns and must not be inferred from this artifact.
