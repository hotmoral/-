# ReceiptLedger V1 — CP29 Search / Browse Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_SEARCH_BROWSE_01`
Status: **PASS**

## 1. Canonical refs

- branch: `receiptledger/run-v1-search-browse-20261016`
- predecessor handoff: `36c361d8c5c5845a15ecf77648861cd2ea7a1b40`
- implementation HEAD: `b73fe8653b9e90e83c44cb24aa3e3da9bfed96f1`
- Actions run: `38839041465`
- job: `116774625167`
- artifact ID: `12020980247`
- artifact digest: `sha256:16505e577d84180771fe8e6da8f8d4243cf389aa0892f2446e621933fad4de81`
- artifact expiry: 2026-10-30T02:12:11Z

## 2. Build identity

Artifact `BUILD_IDENTITY.txt` confirms:

- `public_commit=b73fe8653b9e90e83c44cb24aa3e3da9bfed96f1`
- `product_schema=2_UNCHANGED`
- `receipt_schema=1_UNCHANGED`
- `search_mutation=NONE`
- `mutable_search_index=NONE`
- `search_ranking=EXACT_PREFIX_CONTAINS_ALL_TERMS`
- `store_filter=EXACT_NORMALIZED`
- `frequency=UNIQUE_RECEIPT_OCCASIONS`
- `price_change=STRICT_CP28_EVALUATED_NON_TYPICAL_ONLY`
- `fuzzy_identity_authority=NONE`
- AGP 8.11.1
- Gradle 8.13
- JDK 17
- compileSdk 36
- targetSdk 36
- minSdk 23
- versionName `1.0.27-search-browse`
- versionCode 28
- debug signing only

## 3. APK evidence

Debug APK:

`receiptledger-v1-search-browse-debug.apk`

SHA-256:

`e8f0503cd12126461f6eb257a11be2d0ef7bac68cc2857c6b4f523c059830088`

APK ZIP integrity passed.

Packaged permissions contain only the app's dynamic receiver not-exported permission. Forbidden CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE permissions were absent.

## 4. CP29 metric

Canonical metric:

`CP29_METRICS documents=3 exact_hits=1 compact_hits=1 observed_hits=1 category_rows=3 store_rows=1 recent_rows=3 frequent_rows=3 no_result_rows=0 mutation_checks=1 diagnostics_scanned=3`

Interpretation:

- exact canonical search works;
- whitespace-compacted discovery works;
- observed receipt item-name discovery works;
- category descendant browse works;
- exact normalized store filter works;
- recent/frequent views return deterministic rows;
- no-result path is explicitly empty;
- search leaves product/link state unchanged;
- scan diagnostics are present for later CP36 scale testing.

## 5. Test evidence

Artifact XML results:

| Suite | Tests | Failures | Errors | Skipped |
|---|---:|---:|---:|---:|
| CP29 Search / Browse | 8 | 0 | 0 | 0 |
| CP28 Price Evaluation | 8 | 0 | 0 | 0 |
| CP27 Price Intelligence | 8 | 0 | 0 | 0 |
| Legacy Price History | 2 | 0 | 0 | 0 |
| CP26 Commodity / Non-standard | 8 | 0 | 0 | 0 |
| CP25 Category System | 8 | 0 | 0 | 0 |
| CP24 Identity Resolver | 8 | 0 | 0 | 0 |
| CP23 Receipt Product Semantics | 7 | 0 | 0 | 0 |
| CP21 Catalog Domain V2 | 15 | 0 | 0 | 0 |
| CP22 Persistence V2 | 7 | 0 | 0 | 0 |

Android lint report: `No issues found.`

## 6. Scope evidence

CI scope guard froze upstream packages:

- `catalog`
- `product`
- `semantics`
- `identity`
- `category`
- `commodity`
- `persistence`
- legacy `price`
- `priceintel`
- `priceeval`
- AndroidManifest

Only the CP29 search package/test/docs/workflow and build version metadata were permitted.

## 7. Search safety evidence

Golden tests verified:

- canonical/structured/observed search;
- compact whitespace handling;
- category descendant semantics;
- exact-normalized store filtering rather than partial store equality;
- distinct receipt occasions for frequency;
- blank/no-result behavior;
- CP28 status gate for price-change browse;
- separate `WEIGHT_KG` and `EACH` price-change rows for one commodity;
- read-only product/link invariants.

## 8. Evidence qualification

The fixture is synthetic and deterministic. It proves the CP29 contract and regression boundary; it does not claim real-user search recall, typo tolerance, large-catalog latency or market-quality ranking.

Those concerns remain for later real-use/scale validation, especially CP35 and CP36.
