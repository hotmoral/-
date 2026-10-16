# ReceiptLedger V1 — CP34 Commercial UI Shell Closeout

Updated: 2026-10-16 KST
Checkpoint: **CP34 — Commercial UI Shell**
Status: **PASS / COMPLETE**

## 1. Canonical execution boundary

- branch: `receiptledger/run-v1-commercial-ui-shell-20261016`
- predecessor CP33 handoff: `2a15e14e9897aa9785762faef1568254fbeb5f82`
- frozen CP34 implementation HEAD: `d9764b1447aefaaf3e3fdc5785c72c7c98e8314e`
- canonical Actions run: `38878681881` — SUCCESS
- canonical job: `116899840083` — SUCCESS
- artifact ID: `12036721843`
- artifact digest: `sha256:61e31f76bcf1e8d4e7dc596807b2aacd6c7774ad8e9fe05f36b09b59d4a95258`
- debug APK SHA-256: `64899bfdd715780ecb864f033896f66e2c89d7186da338f2dd59c7fc2033a2af`
- versionName: `1.0.32-commercial-ui-shell`
- versionCode: `33`
- lint: `No issues found.`

This implementation HEAD is the executable/evidence boundary. Any later handoff synchronization must remain documentation-only.

## 2. Product result

CP34 converts the accumulated ReceiptLedger capabilities into one coherent normal-user shell centered on personal purchase-price memory.

Primary path is now:

`홈 -> 영수증 추가 -> 자동 처리/필요 항목 검토/저장 -> 상품·품목 찾기 -> 가격기억 상세 -> 영수증 근거`

The app no longer launches directly into the development-oriented capture surface.

## 3. Launcher / Home

`HomeActivity` is the packaged MAIN/LAUNCHER activity.

Home provides:

- primary `영수증 추가` action into the frozen CP33 `MainActivity`;
- search/category discovery entry;
- recent-purchase and frequent-purchase shortcuts;
- up to three recent linked price-memory entries from frozen CP29 `recent()`;
- receipt-history entry;
- normal loading, empty and failure states;
- vertically scrollable CP30-compliant composition.

No market-price or savings claim is fabricated.

## 4. Search / Browse

`SearchBrowseActivity` consumes only the frozen CP29 read-only discovery service.

Supported modes:

- text search via `SearchBrowseQueryV1.text()` / `SearchBrowseServiceV1.search()`;
- recent via `recent()`;
- frequent via `frequent()`;
- category navigation from frozen `CategoryTaxonomyV1` and results via `byCategory()`.

Navigation uses the existing stable product ID only:

- STANDARD -> frozen CP31 `ProductDetailActivity`;
- NON_STANDARD -> frozen CP32 `CommodityDetailActivity`;
- unsupported/unclassified -> no identity promotion or relinking.

Search relevance remains discovery-only and never becomes identity evidence.

## 5. Receipt evidence path

`LibraryActivity` is the normal receipt-history destination.

- legacy `PriceHistoryActivity` is no longer the primary browse entry from Library;
- Library exposes `영수증 추가` and `상품·품목 찾기` as coherent shell destinations;
- receipt rows continue to open `ReceiptDetailActivity` by receipt ID;
- full Library content scrolls vertically and follows CP30 max-width behavior;
- receipt-list read failure has an explicit failure state.

CP31/32 purchase rows continue to open the exact underlying receipt, so price-memory detail remains receipt-traceable.

## 6. Frozen authority preserved

CP34 did not change:

- stable catalog-ID identity authority;
- CP21–29 domain/search semantics;
- CP27 comparison eligibility;
- CP28 evaluation thresholds;
- CP30 design-system meaning;
- CP31 STANDARD Product Detail truth;
- CP32 NON_STANDARD Commodity Detail truth;
- CP33 capture/review/save/provenance behavior;
- OCR/recovery/item/validation algorithms;
- product schema 2;
- receipt schema 1;
- direct SQLite truth posture;
- offline/no-network/no-broad-permission posture;
- `Activity + android.widget` architecture.

No Compose/AppCompat/Material migration, FTS/index/cache, cloud, budgeting, banking or e-commerce scope was added.

## 7. Pure shell authority

`CommercialDestinationV1` is a pure type-to-destination mapping:

- STANDARD -> PRODUCT_DETAIL
- NON_STANDARD -> COMMODITY_DETAIL
- UNCLASSIFIED/null -> UNSUPPORTED

`CommercialShellFormatterV1` formats existing fields only. It does not infer identity, comparison basis, price judgment or discount allocation.

## 8. Canonical metric

`CP34_METRICS shell_version=1 launcher_home=1 add_receipt=1 search_browse=1 category_browse=1 standard_detail=1 commodity_detail=1 receipt_history=1 legacy_price_entry_removed=1 schema_unchanged=1`

## 9. Regression evidence

Final canonical run confirms:

- CP34 Commercial UI Shell: 7/7 PASS;
- CP33 Capture / Review UX V2: 13/13 PASS;
- CP32 Commodity Detail: 11/11 PASS;
- CP31 Product Detail: 9/9 PASS;
- CP29 Search / Browse: 8/8 PASS;
- full unit-test task PASS;
- lint 0 errors / 0 warnings;
- debug APK build PASS;
- forbidden CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE permissions absent.

## 10. Meaningful pre-closeout history

CP34 was not closed at the first green-looking point.

1. Run `38877757713` failed compilation because five new layout references used nonexistent `SPACE_5_DP`; scope/frozen guards had already passed. The intended 24dp token was corrected to the existing CP30 `SPACE_6_DP`.
2. Run `38877971396` was green, but post-green review found a constrained-height/large-text accessibility risk in Library plus a receipt-list read failure that could remain stuck in loading state.
3. Final `d9764b...` corrected those issues and canonical run `38878681881` is clean green.

Green CI remains necessary but not sufficient when a cheap material gap is still visible.

## 11. Evidence limitations

CP34 evidence does not claim:

- private real-receipt end-to-end accuracy;
- emulator screenshot-diff coverage;
- physical-device usability validation;
- large-catalog/search performance validation;
- release signing readiness.

Those are not inferred from deterministic CI.

## 12. Next boundary

**CP35 — Real Receipt Evaluation — NOT STARTED**

CP35 should evaluate end-to-end correct purchase registration using public-safe synthetic or explicitly approved sanitized fixtures. The primary metric is correct purchase registration, not OCR character accuracy alone.

Do not begin CP35 without explicit user authorization.
