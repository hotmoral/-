# ReceiptLedger V1 — CP21 Catalog Domain V2 Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_CATALOG_DOMAIN_V2_01`

## 1. Frozen implementation boundary

- branch: `receiptledger/run-v1-catalog-domain-v2-20261016`
- predecessor CP20 handoff HEAD: `3149beb339a2d541a61a694fb1f052556a95c8c1`
- frozen CP21 implementation HEAD: `8596106c370e172161ef00e8d460dc78667bf80d`
- implementation commits over predecessor: exactly 1
- canonical GitHub Actions run: `38808985222` — **SUCCESS**
- workflow job: `116677102660` — **SUCCESS**

The frozen implementation HEAD is the executable/code evidence boundary. Later commits on the same branch may synchronize documentation only and must not be treated as additional CP21 implementation.

## 2. CI/build evidence

Canonical run `38808985222` passed every required step:

- checkout / JDK 17 / Android API 36 / Gradle 8.13 setup
- ReceiptLedger public-tree audit
- CP21 scope and frozen-predecessor contract guard
- full `:app:testDebugUnitTest`
- `:app:lintDebug`
- `:app:assembleDebug`
- APK ZIP integrity
- packaged permission firewall
- evidence packaging
- artifact upload

Gradle result: **BUILD SUCCESSFUL**.

Android lint result:

`No issues found.` = **0 errors / 0 warnings**.

## 3. CP21 deterministic domain tests

`CatalogDomainV2Test`:

- tests: **15**
- failures: **0**
- errors: **0**
- skipped: **0**

Covered contracts include:

- legacy STANDARD preservation without semantic guessing;
- legacy NON_STANDARD -> commodity mapping without invented units;
- UNCLASSIFIED fail-closed behavior;
- stable-ID-only entity equality;
- category non-authority;
- confidence vs confirmation independence;
- merchant alias namespace isolation;
- exact kg/g and L/mL package-measure equivalence;
- pack-count and unknown-vs-explicit distinction;
- rejection of package-form words as exact net-content measures;
- mixed commodity purchase-form preservation;
- native STANDARD product-name requirement;
- purchase-observation evidence/provenance/validation retention.

## 4. Scope evidence

Compare CP20 predecessor `3149beb339a2d541a61a694fb1f052556a95c8c1` -> CP21 implementation `8596106c370e172161ef00e8d460dc78667bf80d`:

- status: ahead
- ahead_by: 1
- behind_by: 0
- changed files: 17

Changes are limited to:

- CP21 workflow;
- CP21 plan/consistency/golden-vector documents;
- app version metadata;
- new pure-Java `com.receiptledger.v1.catalog/**` domain classes;
- new catalog-domain unit test.

Explicitly unchanged:

- legacy `product/**` runtime;
- `persistence/**` runtime;
- `AndroidManifest.xml`;
- OCR/layout/item/validation behavior;
- Activities/navigation/UI;
- existing permission model.

`ProductCatalogSchema.VERSION` remains **1**. CP22 migration has not begun.

## 5. Build identity

- application ID: `com.receiptledger.v1`
- AGP: `8.11.1`
- Gradle: `8.13`
- JDK / Java: `17`
- compileSdk: `36`
- targetSdk: `36`
- minSdk: `23`
- versionCode: `20`
- versionName: `1.0.19-catalog-domain-v2`
- catalog contract: V2 domain
- legacy product schema: V1 unchanged
- persistence migration: NOT STARTED
- Identity Resolver V2: NOT STARTED
- UI change: NONE
- signing: debug only

## 6. APK / artifact evidence

Artifact:

- ID: `12008555521`
- name: `receiptledger-v1-catalog-domain-v2-38808985222`
- size: `23,056,580` bytes
- digest: `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- expiry recorded by Actions: 2026-10-29

Debug APK SHA-256:

`1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`

APK ZIP integrity: PASS.

Packaged permission dump contains only the app-generated dynamic-receiver permission and none of the ReceiptLedger forbidden permissions:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

## 7. Non-blocking infrastructure notices

The CI log also emitted two infrastructure/build-tool notices that are not CP21 domain failures:

1. GitHub-hosted runner warns that some referenced actions target Node.js 20 and are currently forced onto Node.js 24 by the platform.
2. Gradle reports deprecated features that would need attention before a future Gradle 9 migration.

Neither affected CP21 tests, lint, APK build, scope guard or privacy evidence. They are recorded rather than expanded into unrelated CP21 remediation.

## 8. Evidence conclusion

**CP21 Catalog Domain V2 implementation evidence: PASS.**

The domain contract is proven against deterministic tests while the legacy persistence/runtime and privacy boundary remain unchanged.
