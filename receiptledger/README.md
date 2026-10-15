# ReceiptLedger public execution namespace

This directory contains public-safe ReceiptLedger Android/OCR development, validation, product/domain specifications, CI, and debug APK build material.

## Start here for a new GPT session

Read in this order:

1. `PROJECT_STATUS_LATEST.md`
2. `SESSION_HANDOFF.md`
3. `PRODUCT_REBASELINE_V1_MASTER_SPEC.md`
4. `PRODUCT_REBASELINE_V1_CONSISTENCY_REVIEW.md`
5. `PRODUCT_REBASELINE_V1_ROADMAP.md`
6. `README.md`
7. `WORK_UNIT.md`

Do not reconstruct state from an old chat transcript before reading those files and verifying GitHub refs.

## Current completed boundary

Latest completed checkpoint:
**CP20 — Product Rebaseline / V1 Master Specification**

CP20 branch:
`receiptledger/run-v1-product-rebaseline-20261016`

Frozen CP20 specification boundary:
`5d4cd9d0d33536bbda682914af0275e6edb92a33`

CP20 result:
**PASS / COMPLETE — documentation/specification only**

No production source, DB schema, OCR/runtime behavior, permission, or toolchain change was made by CP20.

## Latest executable baseline

The app remains frozen at **V1 Target API 36 Core**:

- implementation HEAD: `56abeee3bb185cea8dd136d972a9660f243ded27`
- canonical Actions run: `38800790544` — SUCCESS
- artifact digest: `sha256:338da98a240028a3b06056b0d690a8f2ed6b9ea7d348c9e54b53679af5b75efd`
- APK SHA-256: `272cab6d1d0aea274eb5ba02459d974ac97aaf0d045e79c0072ae2a9dd97f79b`
- lint: 0 errors / 0 warnings
- compileSdk / targetSdk / minSdk: 36 / 36 / 23
- AGP / Gradle / JDK: 8.11.1 / 8.13 / 17

## Product direction

ReceiptLedger is now explicitly productized as a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

The receipt is input/evidence. Product and commodity history are the main user destination.

Important principles:

- STANDARD = exact repeatable packaged-product identity;
- NON_STANDARD = commodity/item identity that may group mixed sales forms without claiming cross-unit comparability;
- UNCLASSIFIED = unresolved state;
- wrong product merge is worse than unresolved identity;
- no guessed unit conversion;
- confirmed reusable knowledge should reduce future review effort;
- price truth stays traceable to saved receipt records + links;
- price judgment must have explicit testable statistics/data-sufficiency rules;
- commercial UI must not require users to understand OCR internals.

## Roadmap

The product-centric roadmap is documented in `PRODUCT_REBASELINE_V1_ROADMAP.md`.

Next planned checkpoint:
**CP21 — Catalog Domain V2**

CP21 is planned but not automatically authorized. Wait for explicit user instruction before starting it.

## Current privacy/security model

This is a public repository. Anything pushed here must be safe to remain public permanently.

Never place here:

- signing keystores or signing passwords
- API keys, access tokens, OAuth secrets, private credentials
- real private receipt photos
- real purchase-history databases or private backups
- personal identifiers
- uncleared private/proprietary assets

The executable app intentionally does not request:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

Camera intake uses an external camera app plus constrained temporary URI. Gallery intake uses the system picker. Korean ML Kit OCR remains bundled/local.

## Layout

- `harness/`: Android source and bounded public-safe build/test harness
- `fixtures/`: synthetic or explicitly approved public fixtures only
- `tools/`: deterministic verification scripts
- `workflows/`: ReceiptLedger-local workflow support files
- `.github/workflows/receiptledger-*.yml`: ReceiptLedger GitHub Actions workflows
- `output/`: generated public reports/build metadata; not canonical by itself
- `*_CORE_PLAN.md`: earlier executable checkpoint contracts
- `PRODUCT_REBASELINE_V1_*.md`: CP20 product/domain rebaseline
- `CP20_PRODUCT_REBASELINE_*.md`: CP20 decisions/risk/gates/acceptance/evidence
- `PROJECT_STATUS_LATEST.md`: current exact status
- `SESSION_HANDOFF.md`: restart contract

## Namespace isolation

ReceiptLedger work may modify only:

- `receiptledger/**`
- explicitly approved `.github/workflows/receiptledger-*.yml`

Do not read from, modify, depend on, cache from, or consume artifacts/output from other project namespaces.

Do not alter repository visibility, repository-wide Actions permissions, rulesets/branch protection, shared secrets/variables, or global artifact retention without separate user approval.

## Current stop condition

**CP20 is complete. Do not begin CP21 until explicitly authorized.**
