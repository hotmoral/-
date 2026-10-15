# ReceiptLedger public execution work unit

## Current stage

The original staging-only work unit is complete. ReceiptLedger V1 now has a working public Android vertical slice with OCR, parsing, validation, review/edit, persistence, receipt library, product identity, price history, OCR recovery, cross-pass merge, and build/lint hygiene.

Current completed implementation boundary:

- checkpoint: **V1 Build Hygiene Core**
- frozen implementation HEAD: `53d03fc219d4b15bf09cebbc368ae6af6a55053a`
- Actions run: `38755847381` — SUCCESS
- lint: `0 errors / 1 warning`
- remaining warning: `OldTargetApi`

Next work unit:

**V1 Target API 36 Core**

Reserved branch:
`receiptledger/run-v1-target-api36-core-20261015`

At handoff, implementation of this next work unit has not started. Documentation-only commits may exist on the reserved branch after the frozen Build Hygiene implementation HEAD.

## Required first reads

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `TARGET_API36_CORE_PLAN.md`
4. this file

## Public repository rules

Treat every pushed file, workflow log, cache key, artifact name, generated report, and APK as permanently public.

Never include:

- signing keystores or signing passwords
- API credentials, OAuth secrets, private tokens
- real receipt photos unless explicitly approved as sanitized public fixtures
- personal purchase databases or private backups
- personal identifiers
- private/proprietary assets not cleared for public release

Use synthetic fixtures or data explicitly approved for public exposure.

## Namespace rules

Use only `receiptledger/*` branches for ReceiptLedger work.

Modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use source, fixtures, caches, artifacts, reports, workflow output, or generated data from:

- `mobi/*`
- `einstein/*`
- `linkline/*`
- any other project namespace

Do not modify repository visibility, repository-wide Actions permissions, Allowed Actions policy, rulesets/branch protection, shared repository secrets/variables, or global artifact retention without separate user approval.

Workflow names, jobs, concurrency groups, caches, artifacts, and generated output paths must use a ReceiptLedger-specific prefix. Cache restore keys must never fall back to another project's namespace.

## Build/signing policy

Public jobs produce debug or unsigned APKs only.

Release signing is a separate private concern and must not expose:

- release keystore
- key passwords
- signing passwords
- signing secrets

Any APK generated here must contain no embedded secret or personal data.

## Current privacy firewall

The built APK must not request:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

Camera capture remains delegated to an external camera application using a constrained content URI. Gallery/image selection remains delegated to the system picker. OCR remains bundled/local.

## Next work unit acceptance boundary

Target API 36 Core must be kept narrow:

- migrate compileSdk/targetSdk to 36
- use an API-36-compatible AGP/Gradle/JDK toolchain
- preserve minSdk 23
- add correct system-bar inset handling for Android 16 edge-to-edge behavior
- audit predictive back without unnecessary interception
- preserve all current app/domain contracts
- keep lint at 0 errors and eliminate `OldTargetApi` by real migration, not suppression
- preserve forbidden-permission firewall
- pass tests + lint + assembleDebug + APK integrity + evidence packaging

Do not start unrelated OCR/parser/product/database/UI feature expansion inside this work unit.

On completion, update `PROJECT_STATUS_LATEST.md` and `SESSION_HANDOFF.md` before moving to another group.
