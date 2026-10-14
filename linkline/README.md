# Linkline Public Execution Workspace

This directory is the isolated public execution namespace for Linkline.

It is not the Linkline canonical repository and must not become a source of truth.
Only public-safe execution harnesses, fixtures, tools, workflow support files, and generated outputs approved for public exposure may be placed here.

Isolation rules:

- Use only `linkline/*` branches for Linkline public execution work.
- Modify only the `linkline/` namespace plus explicitly approved `.github/workflows/linkline-*.yml` files when a workflow is later authorized.
- Do not modify or reuse `einstein/`, `mobi/`, or any other project's namespace, cache, artifact, output, or workflow data.
- Do not change repository-wide shared settings for Linkline work.
- Do not place secrets, credentials, signing material, private assets, personal data, or unapproved private-source material here.
- Treat anything pushed here, including logs and artifacts, as permanently public.

Reserved structure:

- `harness/` — public execution harness material
- `fixtures/` — public-safe execution fixtures
- `tools/` — public-safe helper tools
- `workflows/` — Linkline-local workflow support scripts/configuration; actual GitHub Actions YAML belongs under `.github/workflows/linkline-*.yml` when authorized
- `output/` — generated public execution reports/output only
