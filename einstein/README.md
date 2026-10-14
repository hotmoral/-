# EinsteinGame public execution namespace

This directory contains only public-safe, disposable execution harness material for EinsteinGame validation.

It is not the canonical EinsteinGame repository. The canonical source of truth remains the private `hotmoral/EinsteinGame` repository.

This public namespace must never contain private canonical repository mirrors, credentials, signing material, private assets, personal data, or any source/fixture that has not been explicitly approved for public exposure.

Layout:
- `harness/`: bounded public-safe execution harnesses
- `tools/`: deterministic execution and verification scripts
- `fixtures/`: explicitly approved public-safe fixtures only
- `workflows/`: scripts/config/templates invoked by GitHub Actions; actual workflow YAML belongs under `.github/workflows/einstein-*.yml`
- `output/`: generated public execution reports; never canonical by itself

Isolation rule:
- Do not read, modify, depend on, cache from, or consume artifacts/output from `mobi/*`, `linkline/*`, or any other project namespace.
- Do not modify repository-wide settings for EinsteinGame work without separate user approval.
- Public cleanup is hygiene only; anything published here must be safe to remain public permanently.

Public-run results become authoritative only after review, parity/provenance checks as applicable, and recording in the canonical private EinsteinGame repository.
