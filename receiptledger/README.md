# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, validation, CI, and debug APK build material.

## Start here for a new GPT session

Read in this order:

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `TARGET_API36_CORE_PLAN.md`
4. `WORK_UNIT.md`

Do not reconstruct state from an old chat transcript before reading those files and verifying GitHub refs.

## Current handoff boundary

Last completed implementation checkpoint:
**V1 Build Hygiene Core**

Frozen implementation commit:
`53d03fc219d4b15bf09cebbc368ae6af6a55053a`

Verified Actions run:
`38755847381` — SUCCESS

Final completed lint state:
`0 errors / 1 warning`

The only remaining warning is `OldTargetApi` on compileSdk/targetSdk 35.

Reserved next branch:
`receiptledger/run-v1-target-api36-core-20261015`

At the synchronized handoff point, the Target API 36 implementation has **not started**. Post-baseline commits on that branch are handoff/status documentation only until the next session explicitly begins the checkpoint.

## Public-safety model

This is a public repository. Anything pushed here must be safe to remain public permanently.

Never place here:

- signing keystores or signing passwords
- API keys, access tokens, OAuth secrets, private credentials
- real receipt photos unless explicitly approved as sanitized public fixtures
- real purchase-history databases or private backups
- personal identifiers or private assets

Public CI produces debug/unsigned development APK artifacts. Release signing requires a separate private path.

## Current application privacy invariants

The packaged app intentionally does not request:

- CAMERA
- broad storage/media permissions
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
- `*_CORE_PLAN.md`: checkpoint design/acceptance contracts
- `PROJECT_STATUS_LATEST.md`: current exact status and completed checkpoint chain
- `SESSION_HANDOFF.md`: restart contract for the next GPT session

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not read from, modify, depend on, cache from, or consume artifacts/output from `mobi/*`, `einstein/*`, `linkline/*`, or other project namespaces.

Do not alter repository-wide settings, rulesets, Actions permissions, shared secrets/variables, or global retention without separate user approval.

Project-prefixed concurrency, artifact, cache, workflow, and output identities are mandatory.
