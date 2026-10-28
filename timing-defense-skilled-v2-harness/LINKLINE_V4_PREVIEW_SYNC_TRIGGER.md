# Linkline V4 Preview synchronize trigger

Purpose: generate a pull-request synchronize event after the V4 head is already based on the proven Cloudflare Preview harness ancestry.

- PR: #12
- Scope: DRAFT / DO NOT MERGE hosted-smoke preview only
- Runtime/data bytes: canonical first + final chunks repaired and hash-pinned
- Validation phase: rerun 5/5 chunk SHA + hosted 1300-stage assembly
- Production: unchanged
