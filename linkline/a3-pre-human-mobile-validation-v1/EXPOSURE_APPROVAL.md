# Linkline A3 Pre-Human Mobile Validation — Exposure Envelope

Status: APPROVED BY PRODUCT OWNER ON 2026-10-24

Purpose: host the already-accepted collection-disabled web candidate on a normal HTTPS origin for real-mobile technical validation.

Public exposure is intentionally limited to:

- the executable `research/a3/human_pilot_candidate/` web assets needed at runtime;
- the accepted 24-puzzle pilot-only bundle;
- the accepted four-form D1 order plan;
- build/runtime identity metadata and public-bundle manifest needed to verify deployment parity.

Explicitly excluded:

- the 12 reserve-holdout puzzles;
- any real participant/human telemetry;
- private repository history or private canonical commit metadata;
- credentials, tokens, signing material, private keys, personal data, direct identifiers;
- private-only analysis/source that is not needed by the deployed runtime.

Safety lock remains:

- `HUMAN_COLLECTION_ENABLED = false`;
- runtime mode `PRE_HUMAN_VALIDATION`;
- export eligibility `TECHNICAL_VALIDATION_ONLY`;
- no automatic research-data upload;
- this deployment does not authorize recruitment or human research collection.

Everything in this public bundle is treated as permanently public.