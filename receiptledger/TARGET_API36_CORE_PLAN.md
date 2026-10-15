# ReceiptLedger V1 — Target API 36 Core Plan

Status: **COMPLETED**
Branch: `receiptledger/run-v1-target-api36-core-20261015`
Frozen completed implementation HEAD: `56abeee3bb185cea8dd136d972a9660f243ded27`
Canonical Actions run: `38800790544` — **SUCCESS**

## 1. Purpose and result

This checkpoint legitimately migrated ReceiptLedger from API 35 to Android API 36 while preserving the existing V1 vertical slice and public privacy boundary.

The prior Build Hygiene `OldTargetApi` warning was removed by real migration, not suppression.

Final build contract:

- AGP: `8.11.1`
- Gradle: `8.13`
- JDK / Java: `17`
- compileSdk: `36`
- targetSdk: `36`
- minSdk: `23`
- versionCode: `19`
- versionName: `1.0.18-target-api36-core`

## 2. Implemented work

### A. Toolchain migration — COMPLETE

- root Android Gradle Plugin moved to 8.11.1
- CI uses Gradle 8.13
- CI verifies/installs Android platform 36 when needed
- compileSdk and targetSdk moved to 36
- Java 17 retained
- minSdk 23 retained
- no unrelated app dependency expansion was introduced

### B. Edge-to-edge / system bars — COMPLETE

ReceiptLedger uses programmatic Android Views. A reusable `SystemBarInsetHelper` was added and applied to:

- `MainActivity`
- `LibraryActivity`
- `ReceiptDetailActivity`
- `PriceHistoryActivity`

Final contract:

- API 23–34: existing framework decor-fitting behavior remains unchanged.
- API 35+: forced edge-to-edge is handled by adding `systemBars()` + `displayCutout()` insets to original screen padding.
- base padding is captured once and reused, preventing cumulative padding on repeated inset dispatch.
- scrolling/detail behavior remains structurally unchanged.
- deprecated `Window.setDecorFitsSystemWindows(...)` was removed from the final implementation.
- helper arithmetic has dedicated unit tests.

No visual redesign was performed beyond compatibility handling.

### C. Predictive back audit — COMPLETE

Source audit found no custom back interception or opt-out:

- no `onBackPressed`
- no `OnBackPressedDispatcher`
- no `OnBackInvokedDispatcher`
- no custom back key handling
- no `enableOnBackInvokedCallback` override

The app therefore continues to rely on standard Activity back navigation. No custom interception was invented merely for API 36.

### D. Permission/privacy regression — PASS

Final packaged APK does not request:

- `android.permission.CAMERA`
- `android.permission.READ_MEDIA_IMAGES`
- `android.permission.READ_EXTERNAL_STORAGE`
- `android.permission.WRITE_EXTERNAL_STORAGE`
- `android.permission.MANAGE_EXTERNAL_STORAGE`
- `android.permission.INTERNET`
- `android.permission.ACCESS_NETWORK_STATE`

Camera remains delegated to an external camera app with a constrained content URI. Gallery intake remains via the system picker. Korean ML Kit OCR remains bundled/local.

## 3. Verification / evidence

Canonical final run:
`38800790544` — **SUCCESS**

Artifact:

- ID: `12004666174`
- name: `receiptledger-v1-target-api36-core-38800790544`
- digest: `sha256:338da98a240028a3b06056b0d690a8f2ed6b9ea7d348c9e54b53679af5b75efd`
- debug APK SHA-256: `272cab6d1d0aea274eb5ba02459d974ac97aaf0d045e79c0072ae2a9dd97f79b`

Verified PASS:

1. public namespace audit
2. exact toolchain/version contract checks
3. existing unit tests
4. inset helper tests
5. `lintDebug`
6. `assembleDebug`
7. lint result `No issues found.` = 0 errors / 0 warnings
8. explicit `OldTargetApi` absence
9. APK ZIP integrity
10. packaged permission firewall
11. launcher/exported-state checks
12. source SHA-256 evidence
13. APK SHA-256 evidence
14. ReceiptLedger-prefixed artifact upload

Packaged activity state remained:

- MainActivity exported=true and launchable
- LibraryActivity exported=false
- ReceiptDetailActivity exported=false
- PriceHistoryActivity exported=false

## 4. CI transition note

- `38800168937` succeeded on the initial API 36 implementation.
- `38800740254` failed only because a helper cleanup commit removed deprecated `setDecorFitsSystemWindows` before the workflow string contract was updated. It is a stale-contract transitional failure, not a production regression.
- `38800790544` is the final canonical SUCCESS after implementation and workflow contract were aligned.

## 5. Scope firewall result

This checkpoint did **not** implement:

- new OCR passes or image filters
- parser/structure heuristic expansion
- receipt schema changes
- product fuzzy matching
- new price-history semantics
- release signing
- Play publishing
- real receipt fixtures
- network services
- general UI redesign

Existing receipt/data behavior remains the prior V1 contract.

## 6. Closeout

Target API 36 Core is complete at frozen implementation HEAD:
`56abeee3bb185cea8dd136d972a9660f243ded27`

Status/handoff documentation may advance the branch after that commit, but such post-boundary commits are documentation-only until another checkpoint is explicitly authorized.

**Stop here. No subsequent work group is assigned by this plan.**
