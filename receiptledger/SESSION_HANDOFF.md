# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

Do **not** reconstruct ReceiptLedger state from old chat memory. GitHub is the execution source of truth for this public workspace.

Read in this order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/README.md`
4. `receiptledger/WORK_UNIT.md`
5. `receiptledger/TARGET_API36_CORE_PLAN.md`
6. prior `*_CORE_PLAN.md` only when a dependency contract is needed
7. current Android source under `receiptledger/harness/android-v1/`
8. ReceiptLedger workflows under `.github/workflows/receiptledger-*.yml`

Before editing anything, verify exact refs and compare the current handoff branch against the frozen implementation HEAD below.

## 1. Exact completed state

Latest completed checkpoint:
**ReceiptLedger V1 Target API 36 Core**

Branch:
`receiptledger/run-v1-target-api36-core-20261015`

Frozen completed implementation HEAD:
`56abeee3bb185cea8dd136d972a9660f243ded27`

Canonical successful Actions run:
`38800790544` — **SUCCESS**

Artifact:

- ID: `12004666174`
- name: `receiptledger-v1-target-api36-core-38800790544`
- digest: `sha256:338da98a240028a3b06056b0d690a8f2ed6b9ea7d348c9e54b53679af5b75efd`
- debug APK SHA-256: `272cab6d1d0aea274eb5ba02459d974ac97aaf0d045e79c0072ae2a9dd97f79b`

Final Android lint:
`No issues found.` = **0 errors / 0 warnings**

`OldTargetApi` is gone because the app genuinely targets API 36; no lint suppression/baseline was used for that warning.

Post-boundary status/handoff synchronization may advance the branch after the frozen implementation HEAD. Those post-boundary commits must remain documentation-only until the user authorizes a new implementation group.

## 2. Current build/runtime contract

- application ID: `com.receiptledger.v1`
- AGP: `8.11.1`
- Gradle: `8.13`
- JDK / Java: `17`
- compileSdk: `36`
- targetSdk: `36`
- minSdk: `23`
- versionCode: `19`
- versionName: `1.0.18-target-api36-core`
- Korean ML Kit OCR remains bundled/local

Target API 36 Core preserved all existing ReceiptLedger domain/storage behavior.

## 3. What Target API 36 Core changed

### Toolchain / target

- compileSdk 35 → 36
- targetSdk 35 → 36
- AGP 8.7.3 → 8.11.1
- CI Gradle → 8.13
- Java 17 preserved
- minSdk 23 preserved

### Android 15/16 edge-to-edge handling

A shared `SystemBarInsetHelper` now protects the content roots for:

- `MainActivity`
- `LibraryActivity`
- `ReceiptDetailActivity`
- `PriceHistoryActivity`

Final behavior:

- API 23–34 keeps the pre-existing framework decor-fitting path.
- API 35+ uses forced edge-to-edge and adds `WindowInsets.Type.systemBars()` + `WindowInsets.Type.displayCutout()` to each screen's original base padding.
- Original padding is captured once; repeated inset dispatches do not accumulate padding.
- Final code deliberately does **not** call deprecated `Window.setDecorFitsSystemWindows(...)`.
- A pure padding resolver is unit-tested for addition and repeated-dispatch stability.

### Predictive back

Static source audit confirms ReceiptLedger has no custom:

- `onBackPressed`
- `OnBackPressedDispatcher`
- `OnBackInvokedDispatcher`
- `KEYCODE_BACK` interception
- `enableOnBackInvokedCallback` opt-out

Standard Activity back navigation is preserved. No unnecessary predictive-back interception was added.

## 4. Final verification result

Canonical final run `38800790544` passed:

- API 36 SDK availability/provisioning
- Gradle 8.13 / JDK 17 setup
- public namespace audit
- exact toolchain/API/version contract checks
- all existing unit tests + new inset helper tests
- `lintDebug`
- `assembleDebug`
- `OldTargetApi` absence check
- APK ZIP integrity
- packaged permission firewall
- launcher/exported-state audit
- source/APK evidence hashes
- ReceiptLedger-prefixed artifact upload

Packaged exported-state contract remained:

- `MainActivity`: launcher, exported=true
- `LibraryActivity`: exported=false
- `ReceiptDetailActivity`: exported=false
- `PriceHistoryActivity`: exported=false

The final permission dump contained only the app's generated `DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`; none of the ReceiptLedger forbidden permissions were present.

## 5. CI history clarification

There are two earlier Target API 36 workflow records that a future session may notice:

1. `38800168937` — SUCCESS. This validated the initial API 36 implementation before the final deprecated-window-API cleanup.
2. `38800740254` — FAILURE. This is an expected transitional stale-contract failure: the helper commit removed `setDecorFitsSystemWindows`, while the workflow at that instant still required that string. It failed before the final contract update and does **not** represent an unresolved app regression.
3. `38800790544` — SUCCESS. This is the canonical final run after the workflow was updated to the final API 35+ system-bar + display-cutout contract.

Use only `38800790544` as the closeout run for this checkpoint.

## 6. Existing vertical slice that must remain preserved

The app already contains:

- external-camera capture without app CAMERA permission
- system image/document picker without broad storage permission
- EXIF normalization and bounded bitmap decode
- conservative document detection + perspective correction
- bundled Korean ML Kit OCR
- source-coordinate preservation
- geometry-based layout reconstruction
- receipt structure classification
- item tuple extraction with provenance
- arithmetic validation
- bounded OCR recovery and conservative cross-pass merge
- required review/edit before save
- app-private SQLite persistence
- app-private receipt image archive
- receipt library/list/detail/delete
- merchant/store handling
- STANDARD / NON_STANDARD / UNCLASSIFIED product identity
- exact confirmed alias reuse only
- derived price history

Do not casually alter these contracts in a compatibility or maintenance task.

## 7. Security / privacy boundary

This repository is public. Assume every pushed byte, workflow log, and artifact is permanently public.

Never commit/upload:

- release signing keystore/passwords
- API keys, OAuth secrets, tokens, private credentials
- real private receipt photos
- actual personal purchase databases
- private backups
- personal identifiers
- uncleared proprietary/private assets

ReceiptLedger may modify only:

- `receiptledger/**`
- `.github/workflows/receiptledger-*.yml`

Do not read from, modify, depend on, cache from, or consume artifacts/output from `mobi/*`, `einstein/*`, `linkline/*`, or any other project namespace.

Do not change repository-wide settings, rulesets, Actions permissions, shared secrets/variables, or global artifact retention without explicit user approval.

Forbidden packaged permissions remain:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

## 8. Next-task boundary

**No next implementation checkpoint is currently assigned.**

At restart:

1. verify the branch ref;
2. compare it with frozen implementation HEAD `56abeee3bb185cea8dd136d972a9660f243ded27`;
3. confirm any later handoff commit is documentation-only;
4. report current state;
5. wait for explicit user instruction before beginning another implementation group.

Do not automatically extend OCR, parser, product identity, database, UI, publishing, signing, or Play Store scope.
