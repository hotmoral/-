# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP25 — Category System — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-category-system-20261016`
- predecessor CP24 handoff: `4858c6e6b377e09ebbbe77384d9bb94ede4d906d`
- frozen CP25 implementation HEAD: `042c3b59063f0e58a273a5f685b25780683fcf36`
- canonical Actions run: `38827880730` — SUCCESS
- job: `116739504019` — SUCCESS
- artifact ID: `12015144887`
- artifact digest: `sha256:06e0dcd1d74e3abafd4f39a97363d51b9d53cfb2253c0cf4e742e39f5b257a92`
- debug APK SHA-256: `69244c65cfb09476f371b9c748d42cbe58a5974c3f49d662be90e603e3622a1f`
- Category System tests: 8/8 PASS
- Identity Resolver V2 tests: 8/8 PASS
- Receipt Product Semantics tests: 7/7 PASS
- Catalog Domain V2 tests: 15/15 PASS
- Persistence V2 tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- version: `1.0.23-category-system` / versionCode 24

Any later handoff commit is documentation-only. The executable/evidence boundary remains `042c3b59...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

Receipt is evidence/input. Stable identity, findability and historical price judgment are the destination.

## 3. CP25 result

CP25 adds category as a browse/classification layer over already-resolved catalog IDs.

Frozen rules:

- taxonomy = 28 stable nodes under `FOOD` and `HOUSEHOLD`;
- category states = `REUSE_PERSISTED`, `AUTO_ASSIGNABLE`, `REVIEW`, `UNRESOLVED`;
- unique high-confidence rules may be auto-assigned downstream;
- generic/conflicting evidence is review-gated;
- unsupported evidence stays unresolved; no forced `OTHER`;
- accepted/corrected category persists through existing `category_refs`;
- persisted category is reused on the same stable catalog ID;
- category is never product/commodity identity authority.

## 4. Storage/identity boundary

Preserve:

- stable catalog ID = identity/equality authority;
- product schema = 2;
- receipt schema = 1;
- CP24 resolver authority unchanged;
- category cannot link, merge, split or create identities;
- category assignment changes only `CategoryRef` on an existing catalog entry;
- price/date/store/validation truth remains receipt-derived;
- grouping != comparability;
- no guessed unit/package conversion.

No schema v3 was needed because CP22 already provisioned `category_refs(product_id, category_id)` and its lookup index.

## 5. Local quality evidence

Canonical metric:

`fixtures=30 known_category=28 auto_suggestions=24 correct_auto_suggestions=24 incorrect_auto_suggestions=0 review_required=6 unresolved=2 repeat_cases=4 repeat_reused=4 correction_cases=3 correction_reused=3`

Thus:

- automatic suggestions: 24;
- correct automatic suggestions: 24/24;
- incorrect automatic suggestions: 0;
- persisted repeat reuse: 4/4;
- corrected-category reuse: 3/3.

These are deterministic synthetic local fixtures, not CP35 real-receipt accuracy claims.

## 6. Known limitations

- bounded taxonomy only;
- no custom categories/tags;
- category suggestion provenance is transient; only effective assignment is persisted;
- category does not repair CP24 false splits;
- category does not define NON_STANDARD grouping/comparability.

## 7. Completed checkpoint chain

Foundation -> Image/Document -> OCR -> Layout -> Structure -> Item Tuple -> Validation -> Persistence -> Image Archive -> Receipt Library -> Review/Edit -> Product Identity -> Price History -> OCR Recovery -> Vertical Integration -> Merchant -> Cross-Pass Merge -> Build Hygiene -> Target API36 -> CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> **CP25 Category System**.

## 8. Next planned checkpoint

**CP26 — Commodity / Non-standard V2**.

Goal: represent and group the same commodity across heterogeneous purchase forms such as 봉/팩/kg/개/상자 while preserving original form/unit and keeping grouping distinct from price comparability.

CP26 must measure false grouping, false splitting, raw-unit/form preservation and review burden. It must not introduce guessed conversion.

**Do not begin CP26 without explicit user authorization.**

## 9. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP25_CATEGORY_SYSTEM_CLOSEOUT.md`
4. `receiptledger/CP25_CATEGORY_SYSTEM_EVIDENCE.md`
5. `receiptledger/CP25_CATEGORY_SYSTEM_PLAN.md`
6. `receiptledger/CATEGORY_SYSTEM_CONSISTENCY_REVIEW.md`
7. `receiptledger/CATEGORY_SYSTEM_GOLDEN_VECTORS.md`
8. `receiptledger/CP24_IDENTITY_RESOLVER_V2_CLOSEOUT.md`
9. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify current branch/ref and frozen implementation boundary before future work.

## 10. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase DB/backups, personal identifiers or uncleared assets.

Forbidden APK permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

**Current stop condition: CP25 is complete. Await explicit authorization for CP26.**
