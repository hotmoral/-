# ReceiptLedger V1 — CP34 Commercial UI Shell Golden Vectors

Updated: 2026-10-16 KST

## GV34-01 Launcher
App launcher resolves to HomeActivity, not the capture harness directly.

## GV34-02 Add receipt
Home primary add action opens MainActivity. CP33 save/review truth is unchanged.

## GV34-03 STANDARD result
A CP29 result with `ProductType.STANDARD` routes by stable product ID to ProductDetailActivity.

## GV34-04 NON_STANDARD result
A CP29 result with `ProductType.NON_STANDARD` routes by stable product ID to CommodityDetailActivity.

## GV34-05 UNCLASSIFIED safety
UNCLASSIFIED/unsupported result never becomes STANDARD/NON_STANDARD because of UI navigation.

## GV34-06 Text search
User text is passed to `SearchBrowseQueryV1.text(..., boundedLimit)` and result ordering is CP29-owned.

## GV34-07 Recent browse
Recent mode consumes `SearchBrowseServiceV1.recent()` only.

## GV34-08 Frequent browse
Frequent mode consumes `SearchBrowseServiceV1.frequent()` only.

## GV34-09 Category browse
Root/child labels come from CategoryTaxonomyV1; result rows come from `byCategory()`. Category does not alter identity.

## GV34-10 Empty catalog
Home/search show a normal empty state and direct the user to add a receipt; no error or fabricated data.

## GV34-11 Receipt history
Home receipt-history action opens LibraryActivity; receipt rows continue to ReceiptDetailActivity by receipt ID.

## GV34-12 Legacy browse removal
LibraryActivity no longer uses PriceHistoryActivity as the primary browse button.

## GV34-13 Price semantics
Shell does not calculate price judgment, average, normalization or discount allocation. CP31/32 remain detailed price authorities.

## GV34-14 Privacy
Packaged APK contains none of CAMERA, READ_MEDIA_IMAGES, READ/WRITE_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE, INTERNET, ACCESS_NETWORK_STATE.

## GV34-15 Schemas
Product schema remains 2 and receipt schema remains 1.

## GV34-16 Architecture
No Compose/AppCompat/Material dependency is introduced; Activity + android.widget and CP30 UiKit remain.

## GV34-17 Accessibility
Home/search long content is vertically scrollable and primary controls use CP30 touch-target components.

## GV34-18 Regression
CP29, CP30, CP31, CP32 and CP33 key suites remain green after shell integration.
