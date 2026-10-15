# ReceiptLedger V1 — CP24 Identity Resolver V2 Evidence

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_IDENTITY_RESOLVER_V2_01`

## 1. Frozen executable boundary

- branch: `receiptledger/run-v1-identity-resolver-v2-20261016`
- predecessor handoff: `d04667a5dd9f257117f59bcde194d5b702fa1337`
- frozen implementation HEAD: `4b556afd4dd52b68cf768e937bb456665ad4c231`
- canonical Actions run: `38824134990` — SUCCESS
- job: `116727478370` — SUCCESS
- artifact ID: `12014915453`
- artifact name: `receiptledger-v1-identity-resolver-v2-38824134990`
- artifact digest: `sha256:4740590ca2c7d7525842aa3ebe6ec7964911d303322ebad77b5701344ce76867`
- artifact expiry: 2026-10-29T23:33:47Z
- debug APK SHA-256: `0656c60110ba7debcb0801ddee048cd2220b959c2119539a79274eebbc05eb6e`

## 2. Build identity

- AGP 8.11.1
- Gradle 8.13
- JDK 17
- compileSdk 36
- targetSdk 36
- minSdk 23
- versionName `1.0.22-identity-resolver-v2`
- versionCode 23
- product schema 2 — unchanged
- receipt schema 1 — unchanged
- signing: debug only
- network permission: absent

## 3. Tests

Artifact XML results:

- `IdentityResolverV2Test`: 8/8 PASS
- `ReceiptProductSemanticParserTest`: 7/7 PASS
- `CatalogDomainV2Test`: 15/15 PASS
- `CatalogPersistenceContractV2Test`: 7/7 PASS
- skipped/failures/errors: 0 for all four suites

Android lint: **0 errors / 0 warnings** (`No issues found.`).

Debug APK assembly and ZIP integrity passed.

## 4. Resolver quality metric

Canonical line:

`CP24_METRICS fixtures=24 known_identity=20 auto_links=14 correct_auto_links=14 incorrect_auto_links=0 false_merge=0 false_split=1 review_required=6 unresolved=4 repeat_cases=4 repeat_reused=4`

Interpretation:

- automatic links: 14;
- correct automatic links: 14/14;
- incorrect automatic links: 0;
- false merge: 0;
- fragmentation-risk / false split: 1/20 known-identity fixtures = 5%;
- review-required: 6;
- unresolved: 4;
- repeat-after-confirmation reuse: 4/4 = 100%.

The one false-split metric is deliberately visible. It is a weak-evidence known-product fixture in which the resolver refuses to fabricate an identity and does not surface the correct product. It is a fragmentation-risk signal, not a reason to broaden automatic merge authority. Later review/knowledge-learning work should reduce this burden safely.

These are deterministic synthetic resolver-fixture metrics, not real-receipt accuracy claims. CP35 remains the end-to-end real/sanitized receipt evaluation checkpoint.

## 5. Authority evidence

Verified resolver order:

1. exact MERCHANT alias;
2. exact GLOBAL alias;
3. unique strict semantic exact;
4. semantic suggestion/review;
5. unresolved.

Verified safeguards:

- a merchant-specific exact alias can override a different GLOBAL mapping for the same raw string;
- dangling confirmed alias -> REVIEW, no silent fallback;
- explicit current brand/variant/non-ambiguous specification contradiction -> REVIEW;
- product-name equality alone cannot auto-link;
- parser HIGH confidence alone cannot auto-link;
- strict semantic auto-link requires unique existing STANDARD identity with confirmed exact product name and confirmed exact specification plus symmetric confirmed brand/variant when present;
- CP23 standalone physical-measure ambiguity remains review-gated;
- duplicate strict semantic candidates -> REVIEW;
- NON_STANDARD semantic grouping is not introduced;
- no auto-create or merge path exists in the resolver;
- fuzzy/edit-distance/embedding/phonetic similarity is not auto-link authority.

## 6. Repeat-use evidence

`IdentityConfirmationV2` uses least-authority alias learning:

- merchant context -> MERCHANT alias by default;
- explicit global decision or no merchant context -> GLOBAL alias.

Golden tests verify that after explicit confirmation, the repeated exact merchant alias auto-links to the same stable ID. Repeat reuse was 4/4 in the bounded metric fixture.

## 7. Public/security evidence

The APK permission dump contains only the package-generated dynamic receiver permission:

- `com.receiptledger.v1.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION`

Forbidden permissions were absent:

- CAMERA
- READ_MEDIA_IMAGES
- READ_EXTERNAL_STORAGE
- WRITE_EXTERNAL_STORAGE
- MANAGE_EXTERNAL_STORAGE
- INTERNET
- ACCESS_NETWORK_STATE

Scope guard also verified no CP24 changes under frozen `catalog/**`, `product/**`, `semantics/**`, receipt `persistence/**`, or AndroidManifest.

## 8. Evidence conclusion

CP24 satisfies its bounded acceptance contract: zero unsafe automatic decisions in the golden set, explicit fragmentation measurement, full repeat-confirmation reuse in the fixture, deterministic review on ambiguity/conflict, unchanged storage/security contracts, complete upstream regression, clean lint, and packaged debug APK evidence.
