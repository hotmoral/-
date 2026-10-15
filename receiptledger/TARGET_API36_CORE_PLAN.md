# ReceiptLedger V1 — Target API 36 Core Plan

Status at handoff: **NOT STARTED**
Reserved branch: `receiptledger/run-v1-target-api36-core-20261015`
Frozen implementation baseline: `53d03fc219d4b15bf09cebbc368ae6af6a55053a`

## 1. Purpose

Remove the final Build Hygiene `OldTargetApi` warning by legitimately migrating the app from Android API 35 to Android 16 / API 36 while preserving the complete existing ReceiptLedger V1 vertical slice and the public privacy boundary.

This is a compatibility/toolchain checkpoint, not a feature-development checkpoint.

## 2. Official compatibility facts verified for planning

- Android API level 36 requires Android Gradle Plugin **8.9.1 or newer** according to the Android Developers AGP compatibility table.
- A conservative stable choice for this checkpoint is **AGP 8.11.1 + Gradle 8.13 + JDK 17**; AGP 8.11 supports API 36 and requires Gradle 8.13.
- Starting 2026-08-31, Google Play new apps and app updates for normal Android mobile apps must target Android 16 / API 36 or higher.
- For apps targeting Android 16 / API 36, edge-to-edge enforcement cannot be opted out on Android 16 devices.
- Predictive back system animations are enabled by default for apps targeting API 36 on Android 16+; existing app code should be audited, but custom back interception must not be added unless behavior actually requires it.

Reference documentation:
- https://developer.android.com/build/releases/about-agp
- https://developer.android.com/build/releases/agp-8-11-0-release-notes
- https://developer.android.com/about/versions/16/behavior-changes-16
- https://developer.android.com/google/play/requirements/target-sdk

## 3. Intended build-tool target

Preferred migration target unless CI evidence requires a different compatible choice:

- AGP: `8.11.1`
- Gradle: `8.13`
- JDK: `17`
- compileSdk: `36`
- targetSdk: `36`
- minSdk: keep `23`

Do not increase minSdk just to simplify compatibility.

## 4. Required implementation work

### A. Toolchain migration

- update root Android Gradle Plugin version
- update CI Gradle provisioning to 8.13
- verify Android platform 36 is available in the GitHub runner; install only in the ReceiptLedger job if required
- update compileSdk and targetSdk to 36
- keep Java 17
- do not introduce unnecessary new dependencies

### B. Edge-to-edge / system bars

The app uses programmatic Android Views rather than Compose. Target API 36 means system-bar overlap must be treated as normal behavior.

Create a small reusable inset helper instead of duplicating ad hoc padding code across Activities.

Required Activities to audit/apply:

- `MainActivity`
- `LibraryActivity`
- `ReceiptDetailActivity`
- `PriceHistoryActivity`

Requirements:

- preserve each screen's existing content padding as base padding
- add status/navigation bar insets on top of base padding
- do not accumulate insets on repeated dispatches
- avoid visual content being hidden under system bars
- preserve scrolling behavior on long receipt/detail screens
- do not redesign the UI beyond what API 36 compatibility requires

### C. Predictive back audit

- search for `onBackPressed`, `OnBackPressedDispatcher`, `OnBackInvokedDispatcher`, custom back key handling, or gesture interception
- if none exists, document that the app relies on standard Activity back navigation and preserve that behavior
- do not disable predictive back merely to silence compatibility concerns

### D. Permission/privacy regression

The final packaged APK must still not request:

- `android.permission.CAMERA`
- `android.permission.READ_MEDIA_IMAGES`
- `android.permission.READ_EXTERNAL_STORAGE`
- `android.permission.WRITE_EXTERNAL_STORAGE`
- `android.permission.MANAGE_EXTERNAL_STORAGE`
- `android.permission.INTERNET`
- `android.permission.ACCESS_NETWORK_STATE`

ML Kit remains bundled/local. Any dependency-added network permissions must continue to be removed at manifest merge.

## 5. Tests / verification

The Target API 36 workflow must require:

1. public namespace audit
2. exact toolchain/version contract checks
3. all existing unit tests
4. new inset helper unit/static contract where feasible
5. `lintDebug`
6. `assembleDebug`
7. APK ZIP integrity
8. packaged permission dump and firewall
9. manifest exported-state checks
10. source SHA-256 evidence
11. APK SHA-256 evidence
12. artifact upload with ReceiptLedger-prefixed identity

Acceptance:

- build succeeds with API 36
- lint reports **0 errors**
- `OldTargetApi` warning is gone
- no new target-API compatibility errors are introduced
- no forbidden permissions are added
- minSdk remains 23
- all existing ReceiptLedger tests remain green

## 6. Scope firewall

Do not implement in this checkpoint:

- new OCR passes or image filters
- parser/structure heuristic expansion
- receipt schema changes
- product fuzzy matching
- new price-history semantics
- release signing
- Play publishing
- real receipt fixtures
- broad UI redesign

If an unrelated defect is discovered, document it for a later checkpoint unless it blocks API 36 migration or causes a verified regression.

## 7. Evidence and closeout

On success, record:

- final branch HEAD
- exact AGP / Gradle / compileSdk / targetSdk / minSdk / JDK
- Actions run ID and conclusion
- lint summary
- APK SHA-256
- Actions artifact digest
- packaged permission result
- edge-to-edge compatibility summary
- predictive-back audit result

Then update `PROJECT_STATUS_LATEST.md` and `SESSION_HANDOFF.md` before beginning any subsequent work group.
