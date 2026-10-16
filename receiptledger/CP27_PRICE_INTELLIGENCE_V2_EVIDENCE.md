# ReceiptLedger V1 — CP27 Price Intelligence V2 Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRICE_INTELLIGENCE_V2_01`
Status: **PASS / COMPLETE**

## 1. Frozen implementation

- branch: `receiptledger/run-v1-price-intelligence-v2-20261016`
- predecessor CP26 handoff: `b5a20233fbe9d64d45e00c46adafadfbe6925f6e`
- frozen implementation HEAD: `4edc37c5e16752ff4a4ebc96d67d8a6abfb8e5b8`
- canonical Actions run: `38831623548` — SUCCESS
- job: `116751473084` — SUCCESS
- artifact ID: `12017014494`
- artifact digest: `sha256:660ead5ea86bae86fbd6cf67643866c17acfa5f144c9b1d06f29d50f71f44dd5`
- artifact expiry: `2026-10-30T00:50:28Z`
- debug APK SHA-256: `8455e4ce23e15c6a113e87ddbd0ddb000e41d9f1849e7f431c9ed5dfbfabe1bc`

## 2. Build identity

Artifact `BUILD_IDENTITY.txt` confirms:

- product schema = 2 UNCHANGED
- receipt schema = 1 UNCHANGED
- legacy price core = UNCHANGED
- comparison price = RECEIPT_TRACEABLE_RATIO
- multi-item unallocated discount = EXCLUDED_FROM_AGGREGATES
- sole-item discount = EXACT_ATTRIBUTION_ALLOWED
- STANDARD basis = EXACT_STABLE_PACKAGE
- commodity strict basis = KG_L_EACH
- commodity like-form = CONTEXTUAL_ONLY
- price judgment = DEFERRED_CP28
- price truth = RECEIPT_DERIVED
- AGP 8.11.1
- Gradle 8.13
- JDK 17
- compileSdk 36
- targetSdk 36
- minSdk 23
- versionName `1.0.25-price-intelligence-v2`
- versionCode 26
- signing = debug only

## 3. Test evidence

Artifact XML results:

- `PriceIntelligenceV2Test`: 8 tests, 0 failures, 0 errors, 0 skipped
- legacy `PriceHistoryServiceTest`: 2 tests, 0 failures, 0 errors, 0 skipped
- `CommodityNonStandardV2Test`: 8 tests, 0 failures, 0 errors, 0 skipped
- `CategorySystemV1Test`: 8 tests, 0 failures, 0 errors, 0 skipped
- `IdentityResolverV2Test`: 8 tests, 0 failures, 0 errors, 0 skipped
- `ReceiptProductSemanticParserTest`: 7 tests, 0 failures, 0 errors, 0 skipped
- `CatalogDomainV2Test`: 15 tests, 0 failures, 0 errors, 0 skipped
- `CatalogPersistenceContractV2Test`: 7 tests, 0 failures, 0 errors, 0 skipped

Android lint: **0 errors / 0 warnings** (`No issues found.`).

`testDebugUnitTest + lintDebug + assembleDebug` completed successfully.

## 4. Canonical CP27 metric

`observations=10 eligible=7 excluded_discount=1 excluded_invalid=1 missing_form=1 standard_cohorts=1 commodity_strict_cohorts=1 commodity_contextual_cohorts=1 scope_checks=2 receipt_traceable_rates=7`

This proves the bounded fixture includes both eligible and explicitly excluded observations, strict and contextual NON_STANDARD cohorts, and deterministic period/store filtering.

These are synthetic/local contract metrics, not CP35 real-receipt accuracy claims.

## 5. Comparison-price contract proven

- STANDARD quantity > 1 derives one-package price from exact line-amount/quantity evidence.
- Exact source numerator/denominator remain stored even for repeating decimals such as `10000 / 3`.
- Persisted unit-price conflicts with line arithmetic are not silently repaired.
- MISMATCH/INCOMPLETE receipts are excluded from aggregates.
- A sole-item receipt discount can be attributed exactly to the only item.
- A multi-item receipt discount without persisted attribution remains visible but is excluded as `UNALLOCATED_RECEIPT_DISCOUNT`.
- No proportional coupon allocation is invented.

## 6. NON_STANDARD comparability contract proven

Strict normalized cohorts:

- kg/g -> price per kg;
- L/mL -> price per L;
- EACH -> price per each.

Contextual cohorts:

- same BAG/PACK/BOX/BUNDLE/OTHER raw form -> like-form cohort only.

Different package forms do not share a cohort. `LIKE_FORM` is not strict normalized commodity price.

## 7. Statistics/scope contract proven

Per cohort:

- latest / previous;
- absolute and percentage delta;
- min / max;
- arithmetic mean / median.

Supported scopes:

- all history;
- inclusive date period;
- exact-normalized store;
- period + store.

No cheap/normal/expensive judgment exists in CP27.

## 8. Frozen upstream contracts confirmed

CI diff guards verified no changes from CP26 handoff to:

- `catalog/**`
- `product/**`
- `semantics/**`
- `identity/**`
- `category/**`
- `commodity/**`
- receipt `persistence/**`
- legacy `price/**`
- `AndroidManifest.xml`

Therefore CP27 introduces no schema migration and does not reinterpret earlier identity/grouping contracts.

## 9. Permission/privacy evidence

APK permission audit passed. The only listed app permission was the Android dynamic-receiver not-exported compatibility permission.

No CAMERA, broad storage/media, INTERNET or ACCESS_NETWORK_STATE permission was packaged. No network price source, private fixture or signing secret was added.

## 10. Evidence conclusion

CP27 satisfies its bounded acceptance contract. Frozen executable/evidence boundary: `4edc37c5e16752ff4a4ebc96d67d8a6abfb8e5b8`.
