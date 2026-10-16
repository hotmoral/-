# ReceiptLedger V1 — CP34 Commercial UI Shell Plan

Updated: 2026-10-16 KST
Checkpoint: **CP34 — Commercial UI Shell**
Predecessor handoff: `2a15e14e9897aa9785762faef1568254fbeb5f82`
Frozen predecessor executable: `34cdac2d3e61081ab2a529173dbef9a2431431e0`

## 1. Product goal

Integrate the already-frozen ReceiptLedger capabilities into one coherent normal-user shell centered on personal purchase-price memory.

Primary loop:

`홈 -> 영수증 추가 -> 자동 처리/검토/저장 -> 찾기/카테고리 -> 제품·품목 가격기억 -> 구매 영수증 근거`

## 2. In scope

- new launcher `HomeActivity`;
- obvious primary entry into CP33 `MainActivity` capture flow;
- new `SearchBrowseActivity` consuming the frozen CP29 read-only service;
- recent/frequent/category/search browse modes;
- STANDARD result -> frozen CP31 ProductDetailActivity;
- NON_STANDARD result -> frozen CP32 CommodityDetailActivity;
- receipt-history entry -> LibraryActivity -> ReceiptDetailActivity;
- remove LibraryActivity reliance on legacy PriceHistoryActivity as the primary product browse path;
- Korean normal-user copy and CP30 UiKit/tokens;
- coherent back/primary-navigation behavior without a new navigation framework;
- version/workflow/tests/evidence for CP34.

## 3. Explicit non-goals

CP34 must not:

- change stable identity authority or create/merge/relink products from UI/search relevance;
- change CP27 comparison bases or CP28 thresholds;
- change CP33 review/save semantics;
- mutate product schema 2 or receipt schema 1;
- change OCR/recovery/item/validation algorithms;
- add network/cloud/banking/e-commerce/budgeting scope;
- migrate to Compose/AppCompat/Material;
- add FTS/cache/index performance work reserved for CP36;
- begin CP35 real-receipt evaluation.

## 4. Architecture

Keep `Activity + android.widget`.

- `HomeActivity`: launcher and top-level product shell.
- `MainActivity`: CP33 capture/review flow, unchanged except shell-level copy/navigation only if strictly required.
- `SearchBrowseActivity`: constructs frozen SQLite stores/services and calls `SearchBrowseServiceV1` read-only APIs.
- `LibraryActivity`: receipt-history destination; no legacy price-history browse dependency in primary navigation.
- `CommercialDestinationV1`: pure mapping from ProductType to STANDARD/NON_STANDARD/unsupported destination, so navigation authority is testable without Android UI.
- `CommercialShellFormatterV1`: pure user-facing result/subtitle formatting only; it must not infer identity or price judgments.

## 5. Home composition

Home must foreground product purpose, not database mechanics:

- title/value statement: personal price memory;
- primary CTA: add receipt;
- find products/commodities;
- receipt history;
- small recent-purchase preview sourced from CP29 `recent()` when available;
- empty state that directs first use to receipt add.

No fabricated market-price or savings claims.

## 6. Search/browse composition

Search screen supports:

- text search -> CP29 `search()`;
- recent -> `recent()`;
- frequent -> `frequent()`;
- category roots and bounded taxonomy browse -> `byCategory()`;
- clear text explaining that results are the user's own catalog/history.

Search remains read-only. Result ranking/relevance is never treated as identity evidence.

## 7. Navigation contract

- Home is launcher.
- Add receipt opens MainActivity.
- Find opens SearchBrowseActivity.
- Receipt history opens LibraryActivity.
- ProductType.STANDARD opens ProductDetailActivity with stable product ID.
- ProductType.NON_STANDARD opens CommodityDetailActivity with stable product ID.
- UNCLASSIFIED/unsupported rows are not converted into classified identity by navigation.
- Receipt rows continue opening ReceiptDetailActivity with receipt ID.

## 8. Accessibility/responsive contract

- consume CP30 UiKit and spacing/touch targets;
- vertically scroll long home/search content;
- no hidden primary actions on constrained height;
- text labels accompany meaning; no color-only semantics;
- preserve CP30 content max-width behavior.

## 9. Validation

CP34 unit/contract tests must cover at minimum:

1. launcher/home destination mapping;
2. STANDARD navigation mapping;
3. NON_STANDARD navigation mapping;
4. UNCLASSIFIED unsupported mapping;
5. recent/frequent/category/search mode contract;
6. result formatting contains product identity and purchase context without changing meaning;
7. no schema/version regression except app version bump;
8. frozen CP29–33 regression suites remain green.

Workflow must also enforce:

- public namespace scope;
- frozen domain packages unchanged;
- lint 0 errors / 0 warnings;
- unit tests/build PASS;
- forbidden permissions absent;
- artifact/evidence packaging.

## 10. Acceptance

CP34 closes only when a normal user can launch the app and reach the core capabilities without a development-oriented detour, while every domain decision remains delegated to the already-frozen services.

Stop before CP35 without explicit user authorization.
