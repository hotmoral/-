# ReceiptLedger public execution work unit

## Current stage

**V1 Target API 36 Core is COMPLETE.**

Frozen implementation boundary:

- branch: `receiptledger/run-v1-target-api36-core-20261015`
- implementation HEAD: `56abeee3bb185cea8dd136d972a9660f243ded27`
- canonical Actions run: `38800790544` — SUCCESS
- artifact digest: `sha256:338da98a240028a3b06056b0d690a8f2ed6b9ea7d348c9e54b53679af5b75efd`
- debug APK SHA-256: `272cab6d1d0aea274eb5ba02459d974ac97aaf0d045e79c0072ae2a9dd97f79b`
- lint: `No issues found.` = 0 errors / 0 warnings

Final build contract:

- AGP 8.11.1
- Gradle 8.13
- JDK/Java 17
- compileSdk 36
- targetSdk 36
- minSdk 23
- versionCode 19
- versionName `1.0.18-target-api36-core`

The Target API 36 group is closed. Post-boundary handoff synchronization may advance this branch with documentation-only commits.

## No next work unit is assigned

Do not automatically start another implementation group.

A future session must first:

1. read `PROJECT_STATUS_LATEST.md` and `SESSION_HANDOFF.md`;
2. verify the current branch ref;
3. compare it with frozen implementation HEAD `56abeee3bb185cea8dd136d972a9660f243ded27`;
4. confirm any post-boundary changes are documentation-only;
5. wait for explicit user direction defining the next checkpoint.

## Completed Target API 36 scope

- compileSdk / targetSdk migrated to 36
- API-36-compatible AGP 8.11.1 + Gradle 8.13 + JDK 17
- minSdk 23 preserved
- API 35+ system-bar + display-cutout inset handling for all four programmatic-View activities
- original base padding preserved; repeated inset dispatch does not accumulate padding
- predictive-back source audit completed; standard Activity back retained
- full existing receipt/OCR/data contracts preserved
- lint 0/0; `OldTargetApi` removed legitimately
- forbidden packaged-permission firewall preserved
- unit tests, lint, assembleDebug, APK integrity, exported-state audit, evidence packaging all PASS

## Public repository rules

Treat every pushed file, workflow log, cache key, artifact name, generated report, and APK as permanently public.

Never include:

- signing keystores or signing passwords
- API credentials, OAuth secrets, private tokens
- real private receipt photos
- personal purchase databases or private backups
- personal identifiers
- private/proprietary assets not cleared for public release

Use synthetic fixtures or data explicitly approved for public exposure.

## Namespace rules

Modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not use source, fixtures, caches, artifacts, reports, workflow output, or generated data from:

- `mobi/*`
- `einstein/*`
- `linkline/*`
- any other project namespace

Do not modify repository visibility, repository-wide Actions permissions, Allowed Actions policy, rulesets/branch protection, shared repository secrets/variables, or global artifact retention without separate user approval.

## Privacy firewall

The built APK must not request:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

Camera capture remains delegated to an external camera application using a constrained content URI. Gallery/image selection remains delegated to the system picker. OCR remains bundled/local.

## CI history note

Run `38800740254` is a superseded transitional failure caused by a stale workflow string contract during removal of deprecated `setDecorFitsSystemWindows`. The final implementation/workflow pair is proven by canonical SUCCESS run `38800790544`.
