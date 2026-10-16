# ReceiptLedger V1 — CP25 Category System Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_CATEGORY_SYSTEM_01`

## 1. Frozen implementation

- branch: `receiptledger/run-v1-category-system-20261016`
- predecessor CP24 handoff: `4858c6e6b377e09ebbbe77384d9bb94ede4d906d`
- frozen implementation HEAD: `042c3b59063f0e58a273a5f685b25780683fcf36`
- canonical Actions run: `38827880730` — SUCCESS
- job: `116739504019` — SUCCESS
- artifact ID: `12015144887`
- artifact digest: `sha256:06e0dcd1d74e3abafd4f39a97363d51b9d53cfb2253c0cf4e742e39f5b257a92`
- artifact expiry: `2026-10-30T00:12:07Z`
- debug APK SHA-256: `69244c65cfb09476f371b9c748d42cbe58a5974c3f49d662be90e603e3622a1f`

## 2. Build identity

Artifact `BUILD_IDENTITY.txt` records:

- product schema = 2 UNCHANGED
- receipt schema = 1 UNCHANGED
- taxonomy nodes = 28
- category identity authority = FORBIDDEN
- category persistence = EXISTING_CATEGORY_REFS
- forced OTHER = FORBIDDEN
- price truth = RECEIPT_DERIVED
- AGP 8.11.1
- Gradle 8.13
- JDK 17
- compileSdk 36
- targetSdk 36
- minSdk 23
- versionName `1.0.23-category-system`
- versionCode 24
- signing = debug only

## 3. Test evidence

Artifact XML results:

- `CategorySystemV1Test`: 8 tests, 0 failures, 0 errors, 0 skipped
- `IdentityResolverV2Test`: 8 tests, 0 failures, 0 errors, 0 skipped
- `ReceiptProductSemanticParserTest`: 7 tests, 0 failures, 0 errors, 0 skipped
- `CatalogDomainV2Test`: 15 tests, 0 failures, 0 errors, 0 skipped
- `CatalogPersistenceContractV2Test`: 7 tests, 0 failures, 0 errors, 0 skipped

Android lint: **0 errors / 0 warnings** (`No issues found.`).

`testDebugUnitTest + lintDebug + assembleDebug` completed successfully.

## 4. Canonical CP25 local metrics

`fixtures=30 known_category=28 auto_suggestions=24 correct_auto_suggestions=24 incorrect_auto_suggestions=0 review_required=6 unresolved=2 repeat_cases=4 repeat_reused=4 correction_cases=3 correction_reused=3`

Interpretation:

- automatic category suggestions: 24
- correct automatic suggestions: 24/24
- incorrect automatic suggestions: 0
- review-required: 6/30, including 2 unresolved cases
- persisted repeat reuse: 4/4
- corrected-category reuse: 3/3

These are deterministic synthetic local fixtures. They are not CP35 real/sanitized receipt accuracy claims.

## 5. Category contract proven

- taxonomy contains 28 stable acyclic nodes under `FOOD` and `HOUSEHOLD`;
- unsupported evidence remains unresolved instead of being forced into `OTHER`;
- generic/conflicting evidence is review-gated;
- only unique high-confidence rules become `AUTO_ASSIGNABLE`;
- persisted assignment is reused before classifier rules;
- user correction replaces only `CategoryRef` on the same stable catalog ID;
- assignment does not alter alias knowledge or catalog identity fields;
- unknown category IDs are rejected.

## 6. Frozen upstream contracts confirmed

CI scope guards verified no changes from CP24 handoff to:

- `catalog/**`
- `product/**`
- `semantics/**`
- `identity/**`
- receipt `persistence/**`
- `AndroidManifest.xml`

Therefore CP25 does not widen CP24 identity authority and does not introduce a DB migration.

## 7. Permission/privacy evidence

APK permission audit passed. The packaged app did not contain any forbidden ReceiptLedger permission. The only listed app permission was the Android dynamic-receiver not-exported compatibility permission.

No network capability, private fixture, signing secret or external category service was added.

## 8. Preflight branch-hygiene note

Before the CP25 branch was created, a temporary Markdown preflight marker was accidentally committed to the CP24 handoff branch in orphan commit `af4640af63d1a3d6faa1355addb8d3b4802205cb`.

The CP24 branch ref was immediately restored with force-with-lease to `4858c6e6b377e09ebbbe77384d9bb94ede4d906d` before CP25 work began. CP25 was then branched directly from that exact handoff SHA. The accidental commit contained no source/schema/runtime change and is not part of the canonical CP24 or CP25 history.

## 9. Evidence conclusion

CP25 satisfies its bounded acceptance contract. The frozen executable/evidence boundary is `042c3b59063f0e58a273a5f685b25780683fcf36`.
