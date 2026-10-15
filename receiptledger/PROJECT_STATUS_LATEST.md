# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

The latest fully completed implementation checkpoint is **V1 Target API 36 Core**.

- Working/completed branch: `receiptledger/run-v1-target-api36-core-20261015`
- Frozen completed implementation HEAD: `56abeee3bb185cea8dd136d972a9660f243ded27`
- Canonical successful GitHub Actions run: `38800790544` — **SUCCESS**
- Actions artifact ID: `12004666174`
- Actions artifact digest: `sha256:338da98a240028a3b06056b0d690a8f2ed6b9ea7d348c9e54b53679af5b75efd`
- Debug APK SHA-256: `272cab6d1d0aea274eb5ba02459d974ac97aaf0d045e79c0072ae2a9dd97f79b`
- Android lint: **0 errors / 0 warnings** (`No issues found.`)
- `OldTargetApi`: **removed by real API 36 migration; not suppressed**
- Build/test result: unit tests + `lintDebug` + `assembleDebug` + APK/evidence verification all PASS

Current Android build contract:

- AGP: `8.11.1`
- Gradle: `8.13`
- JDK / Java: `17`
- compileSdk: `36`
- targetSdk: `36`
- minSdk: `23`
- versionCode: `19`
- versionName: `1.0.18-target-api36-core`

The frozen implementation HEAD above is the code/evidence boundary. Any later commits on the same branch made only to synchronize handoff/status documentation are **documentation-only** and must not be mistaken for additional implementation.

No subsequent implementation checkpoint has been assigned yet. **Do not start another feature group without explicit user instruction.**

## 2. Completed checkpoint chain

ReceiptLedger V1 has been built incrementally in this order:

1. **Foundation** — minimal Android app + isolated public GitHub Actions debug APK foundation.
2. **Image Intake / Document Core** — external-camera intake, system picker, EXIF normalization, bounded decoding, receipt quad detection, perspective correction.
3. **OCR Core** — bundled Korean ML Kit OCR, block/line/element model, source-coordinate preservation, offline permission removal.
4. **Layout Core** — geometry-based OCR element row reconstruction.
5. **Structure Core** — receipt row roles, money/date candidates, explicit reasoning.
6. **Item Tuple Core** — item name / quantity / unit price / line amount with printed/inferred provenance and fail-closed arithmetic.
7. **Validation Core** — receipt-level arithmetic validation; mismatches are preserved rather than silently repaired.
8. **Persistence Core** — app-private transactional SQLite persistence.
9. **Image Archive Core** — app-private receipt image archive and orphan reconciliation.
10. **Receipt Library Core** — receipt list/detail/delete and bounded detail-image decode.
11. **Review / Edit Core** — user review required before save; user edits preserve provenance and trigger revalidation.
12. **Product Identity Core** — STANDARD / NON_STANDARD / UNCLASSIFIED, exact confirmed alias reuse only, no fuzzy auto-merge.
13. **Price History Core** — price observations derived from persisted receipts/product links; invalid receipts excluded from comparable history.
14. **OCR Quality / Recovery Core** — original pass first, bounded recovery passes, quality/structure-aware candidate choice.
15. **Vertical Integration Core** — integrated OCR → layout → structure → item → validation → review → persistence flow.
16. **Merchant / Store Core** — conservative merchant/store extraction with user-editable store name propagation.
17. **Conservative Cross-Pass Merge Core** — spatially missing tokens/rows may be supplemented from existing passes only when structure/validation materially improves.
18. **Build Hygiene Core** — frozen HEAD `53d03fc219d4b15bf09cebbc368ae6af6a55053a`; Actions `38755847381` SUCCESS; lint reduced to 0 errors / 1 `OldTargetApi` warning.
19. **Target API 36 Core** — frozen HEAD `56abeee3bb185cea8dd136d972a9660f243ded27`; Actions `38800790544` SUCCESS; API 36 toolchain migration, Android 15/16 edge-to-edge inset compatibility, predictive-back audit, lint 0/0, privacy/exported-state/APK evidence PASS.

## 3. Target API 36 compatibility result

Target API 36 Core changed compatibility/tooling only; it did not redesign OCR, parsing, products, persistence, or normal UI behavior.

### Toolchain

- `compileSdk` / `targetSdk` moved from 35 to 36.
- AGP moved from 8.7.3 to 8.11.1.
- CI Gradle moved to 8.13.
- Java 17 and minSdk 23 were preserved.

### Edge-to-edge / insets

The app remains programmatic Android Views. A reusable `SystemBarInsetHelper` is applied to:

- `MainActivity`
- `LibraryActivity`
- `ReceiptDetailActivity`
- `PriceHistoryActivity`

Compatibility contract:

- API 23–34: preserve the prior framework decor-fitting behavior.
- API 35+: account for forced edge-to-edge by applying `systemBars()` + `displayCutout()` insets.
- Existing per-screen base padding is captured and preserved.
- Insets are always computed from the original base padding, so repeated dispatch does not accumulate padding.
- Deprecated `Window.setDecorFitsSystemWindows(...)` is not used in the final implementation.

### Predictive back

Source audit found no custom `onBackPressed`, `OnBackPressedDispatcher`, `OnBackInvokedDispatcher`, back-key interception, or predictive-back opt-out. ReceiptLedger continues to use standard Activity back navigation.

## 4. Current application invariants

- Application ID: `com.receiptledger.v1`
- Minimum SDK: 23
- compileSdk / targetSdk: 36
- Java: 17
- OCR: bundled Korean Google ML Kit text recognition
- OCR remains local/offline by design.
- Camera capture uses an external camera app with a constrained temporary content URI; the app itself does not request CAMERA permission.
- Gallery intake uses the system picker rather than broad storage/media permission.
- Public CI produces debug development APK artifacts only. Release signing is a separate private concern.

The packaged APK must not request:

- `android.permission.CAMERA`
- `android.permission.READ_MEDIA_IMAGES`
- `android.permission.READ_EXTERNAL_STORAGE`
- `android.permission.WRITE_EXTERNAL_STORAGE`
- `android.permission.MANAGE_EXTERNAL_STORAGE`
- `android.permission.INTERNET`
- `android.permission.ACCESS_NETWORK_STATE`

Final packaged permission audit for the frozen Target API 36 build contained none of the forbidden permissions.

## 5. Data / correctness invariants

- OCR coordinates remain in the normalized source-image coordinate system even when recognition runs on corrected/scaled/preprocessed images.
- Layout reconstruction uses OCR element geometry rather than trusting upstream line grouping.
- Arithmetic inference is explicit and provenance-carrying; contradictions are not silently repaired.
- User review is required before recognized data becomes a saved receipt.
- User edits are distinguished from printed/inferred values and trigger revalidation.
- Product aliases remain conservative: exact confirmed aliases may auto-link; fuzzy similarity must not auto-merge products.
- Price history is derived from persisted receipt/product links rather than copied into a stale duplicate price table.
- Receipts with `MISMATCH` / `INCOMPLETE` validation are excluded from normal comparable price history.
- Target API 36 Core made no receipt DB schema or domain-semantics changes.

## 6. Public repository / namespace firewall

ReceiptLedger may modify only:

- `receiptledger/**`
- explicitly ReceiptLedger-prefixed workflows: `.github/workflows/receiptledger-*.yml`

Do not read from, modify, depend on, cache from, or consume artifacts from `mobi/*`, `einstein/*`, `linkline/*`, or any other project namespace.

Never commit/upload signing material, credentials, API keys, real private receipt photos, real purchase databases, private backups, personal identifiers, or uncleared private assets.

Do not alter repository-wide settings, rulesets, Actions permissions, shared secrets/variables, or global retention without explicit user approval.

## 7. CI history note

- Run `38800168937` succeeded on the first API 36 implementation before final edge-to-edge cleanup.
- Run `38800740254` failed during the transitional helper commit because the then-current workflow still required the removed deprecated `setDecorFitsSystemWindows` call. This was a **stale contract failure**, not an app compile/test regression.
- Run `38800790544` is the canonical final run after the workflow contract was updated to the final API 35+ system-bar + display-cutout implementation. It passed every required step and supersedes the transitional run.

## 8. Restart / next-work boundary

For a new session, use GitHub as source of truth and read:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/README.md`
4. `receiptledger/WORK_UNIT.md`
5. `receiptledger/TARGET_API36_CORE_PLAN.md`
6. current Android source/workflow only as required

Then verify the current branch against frozen implementation HEAD `56abeee3bb185cea8dd136d972a9660f243ded27`. Any post-boundary handoff commit should be documentation-only unless the user has explicitly authorized a new checkpoint.

**Current stop condition: Target API 36 Core is complete. Await explicit user direction for the next checkpoint.**
