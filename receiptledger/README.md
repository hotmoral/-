# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, validation, CI, and debug APK build material.

## Start here for a new GPT session

Read in this order:

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `README.md`
4. `WORK_UNIT.md`
5. `TARGET_API36_CORE_PLAN.md`

Do not reconstruct state from an old chat transcript before reading those files and verifying GitHub refs.

## Current completed boundary

Latest completed implementation checkpoint:
**V1 Target API 36 Core**

Frozen implementation HEAD:
`56abeee3bb185cea8dd136d972a9660f243ded27`

Canonical Actions run:
`38800790544` — **SUCCESS**

Final evidence:

- artifact digest: `sha256:338da98a240028a3b06056b0d690a8f2ed6b9ea7d348c9e54b53679af5b75efd`
- APK SHA-256: `272cab6d1d0aea274eb5ba02459d974ac97aaf0d045e79c0072ae2a9dd97f79b`
- lint: **0 errors / 0 warnings** (`No issues found.`)
- compileSdk / targetSdk: 36 / 36
- minSdk: 23
- AGP / Gradle / JDK: 8.11.1 / 8.13 / 17

Target API 36 implementation is complete. Later commits on the same branch may synchronize handoff/status documentation only. A new session must compare the branch with the frozen implementation HEAD before assuming any later implementation exists.

**No next implementation checkpoint is assigned. Await explicit user instruction.**

## Current compatibility model

- Android API 23–34 retains the previous framework decor-fitting behavior.
- Android API 35+ forced edge-to-edge is handled by a shared helper using system-bar + display-cutout insets while preserving each screen's base padding.
- `MainActivity`, `LibraryActivity`, `ReceiptDetailActivity`, and `PriceHistoryActivity` all use the helper.
- Predictive-back audit found no custom back interception; standard Activity navigation is retained.

## Public-safety model

This is a public repository. Anything pushed here must be safe to remain public permanently.

Never place here:

- signing keystores or signing passwords
- API keys, access tokens, OAuth secrets, private credentials
- real private receipt photos
- real purchase-history databases or private backups
- personal identifiers
- uncleared private/proprietary assets

Public CI produces debug development APK artifacts only. Release signing requires a separate private path.

## Current application privacy invariants

The packaged app intentionally does not request:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

Camera intake uses an external camera app plus a constrained temporary content URI. Gallery intake uses the system picker. Korean ML Kit OCR is bundled/local.

## Layout

- `harness/`: Android source and bounded public-safe build/test harness
- `fixtures/`: synthetic or explicitly approved public fixtures only
- `tools/`: deterministic verification scripts
- `workflows/`: ReceiptLedger-local workflow support files
- `.github/workflows/receiptledger-*.yml`: actual ReceiptLedger GitHub Actions workflows
- `output/`: generated public reports/build metadata; not canonical by itself
- `*_CORE_PLAN.md`: checkpoint design/acceptance/closeout contracts
- `PROJECT_STATUS_LATEST.md`: current exact status and completed checkpoint chain
- `SESSION_HANDOFF.md`: restart contract for the next GPT session

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not read from, modify, depend on, cache from, or consume artifacts/output from `mobi/*`, `einstein/*`, `linkline/*`, or other project namespaces.

Do not alter repository-wide settings, rulesets, Actions permissions, shared secrets/variables, or global artifact retention without separate user approval.

Project-prefixed workflow, concurrency, cache, artifact, and output identities remain mandatory.
