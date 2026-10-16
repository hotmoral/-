# ReceiptLedger V1 — CP28 Price Evaluation Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRICE_EVALUATION_01`

## 1. Frozen implementation

- branch: `receiptledger/run-v1-price-evaluation-20261016`
- predecessor handoff: `c9131d0c6c8e799390ff37a370a1b1c77c38647a`
- frozen implementation HEAD: `dd4f98613677ae998932d77f3e5f89d7bddba107`
- canonical Actions: `38834818192` — SUCCESS
- job: `116761457914` — SUCCESS
- artifact ID: `12018776680`
- artifact digest: `sha256:aa90bff8107f34d1974fd9998ceb543fba33fd8b0d402cc972840f9495b9e4b6`
- artifact expiry: `2026-10-30T01:25:01Z`
- debug APK SHA-256: `692e16f0bd6ad23caba3361d831376620bac09e1505f4780d7147402f9fd48f6`

## 2. Build identity

Artifact `BUILD_IDENTITY.txt` records:

- product schema = 2 UNCHANGED
- receipt schema = 1 UNCHANGED
- Price Intelligence V2 = frozen input
- baseline = latest excluded + recent 5 prior + median
- minimum prior observations = 3
- material threshold = 5% AND 100 minor units
- extreme threshold = 15% AND 500 minor units
- contextual LIKE_FORM judgment = forbidden
- external market price = none
- generative-AI judgment = none
- AGP 8.11.1 / Gradle 8.13 / JDK 17
- compileSdk/targetSdk 36 / minSdk 23
- version `1.0.26-price-evaluation` / versionCode 27
- debug signing only

## 3. Test evidence

Artifact XML results:

- `PriceEvaluationV1Test`: 8 tests, 0 failures, 0 errors, 0 skipped
- `PriceIntelligenceV2Test`: 8/8 PASS
- `PriceHistoryServiceTest`: 2/2 PASS
- `CommodityNonStandardV2Test`: 8/8 PASS
- `CategorySystemV1Test`: 8/8 PASS
- `IdentityResolverV2Test`: 8/8 PASS
- `ReceiptProductSemanticParserTest`: 7/7 PASS
- `CatalogDomainV2Test`: 15/15 PASS
- `CatalogPersistenceContractV2Test`: 7/7 PASS

Android lint: **0 errors / 0 warnings** (`No issues found.`).

`testDebugUnitTest + lintDebug + assembleDebug` completed successfully.

## 4. Canonical CP28 metrics

`cases=12 evaluated=9 insufficient=1 contextual=1 nonpositive=1 typical=2 cheap=2 very_cheap=1 expensive=2 very_expensive=2 latest_excluded=1 recent_five_window=1 deterministic_repeat=1`

The metric gate proves:

- judgment and no-judgment states are both exercised;
- latest purchase is excluded from its own baseline;
- only recent five prior observations are used;
- repeated evaluation is deterministic.

## 5. Policy vectors proven

Tests prove:

- minimum three prior observations;
- latest excluded from baseline;
- an older outlier outside the five-prior window cannot move usual price;
- median baseline calculation;
- percentage + absolute materiality gates both required;
- exact 5% and 15% boundaries deterministic;
- zero/non-positive median suppresses percentage judgment;
- contextual LIKE_FORM never gets cheap/expensive judgment;
- latest-vs-previous and latest-vs-usual are distinct calculations.

## 6. Frozen upstream contract evidence

CI diff guards verified no CP28 changes to:

- `catalog/**`
- `product/**`
- `semantics/**`
- `identity/**`
- `category/**`
- `commodity/**`
- `persistence/**`
- legacy `price/**`
- CP27 `priceintel/**`
- `AndroidManifest.xml`

Therefore CP28 changes no stored-data meaning and cannot widen price eligibility or identity authority.

## 7. Permission/privacy evidence

APK permission audit passed. Only the Android dynamic-receiver not-exported compatibility permission was listed.

No CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permission was packaged. No network service, private receipt fixture, signing secret or external price source was added.

## 8. CI maintenance note

GitHub-hosted runner emitted a non-blocking platform warning that several upstream actions targeting Node.js 20 were forced to Node.js 24. The run remained SUCCESS and this did not affect ReceiptLedger application evidence. Treat it as future workflow-maintenance signal, not an app regression.

## 9. Evidence conclusion

CP28 satisfies its bounded acceptance contract. Frozen executable/evidence boundary: `dd4f98613677ae998932d77f3e5f89d7bddba107`.
