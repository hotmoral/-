# ReceiptLedger V1 — CP26 Commodity / Non-standard V2 Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_COMMODITY_NONSTANDARD_V2_01`

## 1. Frozen implementation

- branch: `receiptledger/run-v1-commodity-nonstandard-v2-20261016`
- predecessor handoff: `e9bbd3d1b2b5c6e153d6c76b1c02b2a1cd217389`
- frozen implementation HEAD: `a0b4b1246f2e7bc4d41b3376507ae34f44e1e372`
- canonical Actions run: `38829423445` — SUCCESS
- job: `116744485504` — SUCCESS
- artifact ID: `12016292501`
- artifact digest: `sha256:6ad4342d61274530aecc090fbe7caa8f606f3a20c113285e3b18cd86893336bd`
- artifact expiry: `2026-10-30T00:27:46Z`
- debug APK SHA-256: `250d4d00bb93334fede3873c92e85b63d1ccd05ee5d09f9a4c7970fb366b90cb`

## 2. Build identity

Artifact `BUILD_IDENTITY.txt` records:

- product schema = 2 UNCHANGED
- receipt schema = 1 UNCHANGED
- commodity identity = EXISTING_STABLE_ID_ONLY
- grouping equals comparability = FALSE
- guessed unit conversion = FORBIDDEN
- category identity authority = FORBIDDEN
- price truth = RECEIPT_DERIVED
- AGP 8.11.1
- Gradle 8.13
- JDK 17
- compileSdk 36
- targetSdk 36
- minSdk 23
- versionName `1.0.24-commodity-nonstandard-v2`
- versionCode 25
- signing = debug only

## 3. Test evidence

Artifact XML results:

- `CommodityNonStandardV2Test`: 8 tests, 0 failures, 0 errors, 0 skipped
- `CategorySystemV1Test`: 8 tests, 0 failures, 0 errors, 0 skipped
- `IdentityResolverV2Test`: 8 tests, 0 failures, 0 errors, 0 skipped
- `ReceiptProductSemanticParserTest`: 7 tests, 0 failures, 0 errors, 0 skipped
- `CatalogDomainV2Test`: 15 tests, 0 failures, 0 errors, 0 skipped
- `CatalogPersistenceContractV2Test`: 7 tests, 0 failures, 0 errors, 0 skipped

Android lint: **0 errors / 0 warnings** (`No issues found.`).

`testDebugUnitTest + lintDebug + assembleDebug` completed successfully.

## 4. Canonical CP26 metrics

`fixtures=25 known_commodity=21 auto_groups=18 correct_auto_groups=18 incorrect_auto_groups=0 false_group=0 review_suggestions=2 false_split=1 negative_fixtures=4 raw_form_cases=12 raw_form_preserved=12 repeat_cases=3 repeat_reused=3`

Interpretation:

- automatic groups: 18
- correct automatic groups: 18/18
- incorrect automatic groups: 0
- false grouping: 0
- review suggestions: 2
- false split / fragmentation risk: 1/21 known commodity fixtures
- negative fixtures: 4, none auto-grouped
- raw purchase-form preservation: 12/12
- explicit-confirmation repeat reuse: 3/3

Synthetic/local only; these are not final real-receipt accuracy claims.

## 5. Grouping contract proven

Tests prove:

- `감자 1봉 / 1KG / 5개 / 1상자` can share the same existing commodity ID;
- purchase form does not define commodity identity;
- modifier-bearing names such as `국산 감자` remain REVIEW until confirmed;
- `감자칩` and `감자전분` do not produce a `감자` substring candidate;
- exact semantic names with strong packaged-product cues are review-gated;
- confirmed aliases reuse the existing least-authority merchant/global scoping;
- alias targets of STANDARD kind cannot become commodity auto-groups;
- no catalog entity is auto-created or merged.

## 6. Form relation contract proven

- kg/g -> `EXACT_NORMALIZABLE_QUANTITY` with exact base quantities;
- L/mL -> `EXACT_NORMALIZABLE_QUANTITY`;
- same BAG -> `SAME_FORM_ONLY`, not numeric normalized comparison authority;
- same OTHER raw label -> `SAME_FORM_ONLY`;
- BAG vs BOX -> `INCOMPARABLE`;
- EACH vs KILOGRAM -> `INCOMPARABLE`.

No guessed PACKAGE_FORM conversion exists.

## 7. Raw evidence preservation

`persistObservedPurchaseForm` stores the CP23 candidate as a `CatalogField` without upgrading confirmation.

Tests verify preserved:

- quantity;
- `SalesUnitCode`;
- raw unit label;
- source = `PARSED_FROM_RECEIPT`;
- confirmation = `UNCONFIRMED`.

## 8. Frozen upstream contracts confirmed

CI diff guards verified no changes from CP25 handoff to:

- `catalog/**`;
- `product/**`;
- `semantics/**`;
- `identity/**`;
- `category/**`;
- receipt `persistence/**`;
- `AndroidManifest.xml`.

Therefore CP26 adds no schema migration and does not widen CP24 or CP25 authority.

## 9. Permission/privacy evidence

APK permission audit passed. The only listed app permission was the Android dynamic-receiver not-exported compatibility permission.

No CAMERA, broad storage/media, INTERNET or ACCESS_NETWORK_STATE permission was packaged. No network service, private receipt fixture, signing secret or external catalog was added.

## 10. Evidence conclusion

CP26 satisfies its bounded acceptance contract. Frozen executable/evidence boundary: `a0b4b1246f2e7bc4d41b3376507ae34f44e1e372`.
