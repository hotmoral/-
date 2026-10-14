# EinsteinGame public execution work unit

Purpose: establish an isolated, public-safe GitHub Actions execution workspace for future EinsteinGame machine verification.

Current workspace initialization only. No EinsteinGame production source, private fixture, secret, signing material, artifact, cache, or workflow run is included in this setup commit sequence.

Rules:
- Canonical source remains private `hotmoral/EinsteinGame`.
- Do not include full private repository mirrors or any unapproved source/fixture/data.
- Do not use source, fixtures, caches, artifacts, reports, or workflow output from other project namespaces.
- Do not modify `mobi/*`, `linkline/*`, other project branches, or other projects' `.github/workflows/*` files.
- Do not change repository visibility, repository-wide Actions permissions, Allowed Actions policy, rulesets/branch protection, repository-wide secrets/variables, or global artifact retention for an EinsteinGame work unit without separate user approval.
- Actual Actions workflows must use `.github/workflows/einstein-*.yml` and Einstein-prefixed job/cache/concurrency/artifact identities.
- Cache restore keys must not fall back into another project's cache namespace.
- A public runner must not obtain credentials to clone the private EinsteinGame repository by default; use only an explicitly approved minimum public-safe execution bundle.
- Public results are provisional until reviewed and recorded in the canonical private EinsteinGame repository.
- Branch/run/artifact deletion is cleanup, not secrecy.

Before the first actual Actions execution of each new EinsteinGame work unit, report the exact public branch, public material, workflow purpose, logs/artifacts/cache behavior, and private-material check, then obtain user confirmation if the exposure scope has not already been approved for that unit.
