# ReceiptLedger public execution namespace

This directory contains only public-safe, disposable execution material for ReceiptLedger Android/OCR development and validation.

It is not the canonical store for private user data, signing material, credentials, or real receipt data. Anything pushed here must be safe to remain public permanently.

Initial scope:
- Android application scaffolding and build verification
- OCR/image-processing code approved for public exposure
- deterministic parser/geometry/unit-test fixtures using synthetic or explicitly approved data
- GitHub Actions build/test harnesses
- unsigned or debug APK artifacts only unless a separate signing plan is explicitly approved

Never place here:
- signing keystores or signing passwords
- API keys, access tokens, OAuth secrets, private credentials
- real receipt photos, real purchase-history databases, personal data, or private backups
- private assets or third-party material not cleared for public distribution

Layout:
- `harness/`: bounded public-safe Android/build/test harnesses
- `fixtures/`: synthetic or explicitly approved public-safe fixtures only
- `tools/`: deterministic execution and verification scripts
- `workflows/`: ReceiptLedger-local workflow support files; actual GitHub Actions YAML belongs under `.github/workflows/receiptledger-*.yml`
- `output/`: generated public reports and build metadata; never canonical by itself

Isolation rules:
- Use only `receiptledger/*` branches for ReceiptLedger public work.
- Modify only `receiptledger/` plus explicitly approved `.github/workflows/receiptledger-*.yml` files.
- Do not read from, depend on, modify, cache from, or consume artifacts/output from `mobi/*`, `einstein/*`, `linkline/*`, or other project namespaces.
- Do not alter repository-wide settings, rulesets, Actions permissions, shared secrets/variables, or global retention for ReceiptLedger work without separate approval.
- Project-prefixed cache, concurrency, artifact, and workflow identities are mandatory.

Public execution results are provisional until reviewed and accepted for the ReceiptLedger project.
