# ReceiptLedger V1 — CP22 Persistence V2 Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PERSISTENCE_V2_01`
Result: **PASS / COMPLETE**

## Canonical implementation boundary

- branch: `receiptledger/run-v1-persistence-v2-20261016`
- predecessor handoff: `dc62d7adb650ced200fe5058aaf20f23d23fb34c`
- frozen implementation HEAD: `449896c7580fb3412f41c9b58d1ab9412d13d84d`
- canonical Actions run: `38816200340` — SUCCESS
- job: `116701369902` — SUCCESS

## Build identity

- applicationId: `com.receiptledger.v1`
- versionCode: `21`
- versionName: `1.0.20-persistence-v2`
- AGP: `8.11.1`
- Gradle: `8.13`
- JDK / Java: `17`
- compileSdk: `36`
- targetSdk: `36`
- minSdk: `23`
- product catalog schema: `2`
- receipt schema: `1` — unchanged
- persistence engine: direct SQLite / `SQLiteOpenHelper`
- Room migration: deferred
- price truth: receipt-derived

## Migration verification

Host SQLite verifier executes the Java migration SQL constants against a real V1 SQLite fixture.

Result:

- `CP22 SQLite migration verification PASS`
- vectors: `15/15`
- product schema: `2`
- receipt schema: `1`
- legacy products preserved: `2/2`
- legacy aliases migrated to GLOBAL context: `2/2`
- legacy item links preserved: `2/2`

The verifier also proves:

- migration does not drop `products`;
- migration does not drop `item_links`;
- no semantic metadata is invented for legacy rows;
- merchant namespaces can reuse one alias key without collision;
- same-context alias collision is rejected;
- purchase-form persistence contains no copied price/date/store truth;
- catalog-local cascade behavior remains coherent;
- fresh V2 creation reaches the target table/index set;
- receipt schema remains version 1.

## JVM tests

- `CatalogDomainV2Test`: 15 tests, 0 failures, 0 errors, 0 skipped
- `CatalogPersistenceContractV2Test`: 7 tests, 0 failures, 0 errors, 0 skipped
- CP21 + CP22 focused contract tests: **22/22 PASS**
- full Gradle unit-test task: SUCCESS

## Android build / lint

- `:app:testDebugUnitTest`: SUCCESS
- `:app:lintDebug`: SUCCESS
- `:app:assembleDebug`: SUCCESS
- Gradle result: `BUILD SUCCESSFUL`
- lint: **0 errors / 0 warnings** (`No issues found.`)

## APK / public safety evidence

Artifact:

- ID: `12010832560`
- name: `receiptledger-v1-persistence-v2-38816200340`
- size: `23,074,895` bytes
- digest: `sha256:6b27c9e8aa9541346d9a3f5844c12a2f0dacd26841e869bd5b4834d7cb67bea1`
- created: `2026-10-15T22:20:43Z`
- expires: `2026-10-29T22:20:41Z`

Debug APK SHA-256:

`1cddd2f19c70b8ab883a97630c3dbc10e8971d75a3c9e4ec62be72eb69328884`

APK ZIP integrity: PASS / no errors.

Packaged badging:

- package `com.receiptledger.v1`
- versionCode `21`
- versionName `1.0.20-persistence-v2`
- minSdk `23`
- targetSdk `36`
- compileSdk `36`

Packaged permissions contain only the generated internal dynamic-receiver permission:

- `com.receiptledger.v1.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`

Forbidden permissions remain absent:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

## Artifact evidence hashes

- `APK_SHA256.txt`: `4861be9b89aedb60b7f5e4ad16b50300b661e9455e56379e21ffa803ab8a1aa5`
- `BUILD_IDENTITY.txt`: `155001661b6ecbfab9fd1f59da09127a7bfb2ef82668a0eeaf3c63bfda4f6c29`
- `SOURCE_SHA256.txt`: `7ad521532d390f6420f79ea86feb3da03a6ea16405a600459d31d070f0848bc0`
- `APK_PERMISSIONS.txt`: `31bd4f32aa43caaccd42ff74b3bd5e67f8914a9e3396fbba0b23ffa4ce37cb44`
- `CP22_MIGRATION_VERIFICATION.txt`: `2f77c16b794b25fddcc0b41ce9845b36209e795e98a32368e9eb68f90c0baa74`
- `PERSISTENCE_V2_TEST.xml`: `468d757330281171fb0fd2437a0ec9326c547eaa89265c20fd585219fe5d61ce`
- `CP22_DIFF.txt`: `b8ece360946ef799a648ca7d1a823b6ed2948d05e758e3701e37f78ea91e2ed0`

## Non-blocking infrastructure notes

Existing build-platform warnings about future Gradle 9 compatibility, Node action runtime migration, and ML Kit native stripping were observed. None is a CP22 persistence correctness failure; no unrelated infrastructure expansion was performed.
