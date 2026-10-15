# ReceiptLedger public execution work unit

Purpose: establish an isolated, public-safe GitHub Actions workspace for ReceiptLedger Android/OCR development, build verification, and future APK packaging.

Current stage: structure initialization only. No production app source, real receipt image, personal purchase data, signing material, secret, APK, or workflow run is included in this staging step.

Rules:
- Treat every pushed file, workflow log, cache key, artifact name, and generated report as permanently public.
- Do not include signing keystores, signing passwords, API credentials, private tokens, personal data, real receipt photos, real purchase-history databases, or private backups.
- Use synthetic fixtures or data explicitly approved for public exposure.
- Do not use source, fixtures, caches, artifacts, reports, workflow output, or generated data from `mobi/*`, `einstein/*`, `linkline/*`, or any other project namespace.
- Do not modify other projects' branches or `.github/workflows/*` files.
- Do not modify repository visibility, repository-wide Actions permissions, Allowed Actions policy, rulesets/branch protection, shared repository secrets/variables, or global artifact retention without separate user approval.
- Actual Actions workflows must use `.github/workflows/receiptledger-*.yml`.
- Workflow names, jobs, concurrency groups, caches, artifacts, and generated output paths must use a ReceiptLedger-specific prefix.
- Cache restore keys must never fall back to another project's cache namespace.
- Public build jobs should produce debug or unsigned APKs by default. Release signing requires a separately approved private signing path.
- Any future import of existing ReceiptLedger source must first pass a public-material audit for secrets, personal data, signing material, proprietary/private assets, and accidental receipt samples.
- Any APK generated here is a public build artifact and must contain no embedded secret or personal data.

Before the first real Android source upload or Actions execution, record:
1. exact branch and source baseline,
2. exact public material being exposed,
3. workflow purpose and trigger,
4. permissions, cache behavior, artifact names, and retention,
5. package/application ID strategy,
6. signing mode,
7. private-material scan result,
8. acceptance/stop conditions.

Staging completion criteria:
- ReceiptLedger branch namespace exists.
- ReceiptLedger directory namespace exists.
- README and work-unit rules exist.
- reserved subdirectories exist.
- no ReceiptLedger workflow exists yet.
- no other project namespace is modified.
