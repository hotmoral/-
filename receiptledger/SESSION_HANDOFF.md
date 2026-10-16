# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct execution state from chat memory before reading current files and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP25_CATEGORY_SYSTEM_CLOSEOUT.md`
4. `receiptledger/CP25_CATEGORY_SYSTEM_EVIDENCE.md`
5. `receiptledger/CP25_CATEGORY_SYSTEM_PLAN.md`
6. `receiptledger/CATEGORY_SYSTEM_CONSISTENCY_REVIEW.md`
7. `receiptledger/CATEGORY_SYSTEM_GOLDEN_VECTORS.md`
8. `receiptledger/CP24_IDENTITY_RESOLVER_V2_CLOSEOUT.md`
9. `receiptledger/CP24_IDENTITY_RESOLVER_V2_EVIDENCE.md`
10. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
11. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
12. `receiptledger/README.md`
13. `receiptledger/WORK_UNIT.md`

## 1. Latest executable checkpoint

**CP25 — Category System — PASS / COMPLETE**

- branch: `receiptledger/run-v1-category-system-20261016`
- predecessor handoff: `4858c6e6b377e09ebbbe77384d9bb94ede4d906d`
- frozen implementation HEAD: `042c3b59063f0e58a273a5f685b25780683fcf36`
- canonical Actions: `38827880730` — SUCCESS
- job: `116739504019` — SUCCESS
- artifact ID: `12015144887`
- artifact digest: `sha256:06e0dcd1d74e3abafd4f39a97363d51b9d53cfb2253c0cf4e742e39f5b257a92`
- APK SHA-256: `69244c65cfb09476f371b9c748d42cbe58a5974c3f49d662be90e603e3622a1f`
- CP25 category tests: 8/8 PASS
- CP24 identity tests: 8/8 PASS
- CP23 semantics tests: 7/7 PASS
- CP21 catalog tests: 15/15 PASS
- CP22 persistence tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- versionName `1.0.23-category-system`, versionCode 24

Later closeout/status commits must remain documentation-only; do not move the executable evidence boundary.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 제품/품목 검색·카테고리 탐색 -> 과거 가격과 현재 가격 판단`

The receipt remains evidence/input. Product/commodity history and price judgment are the destination.

## 3. CP25 category contract

Category is browse/classification metadata over an already-resolved stable catalog ID.

Taxonomy:

- 28 stable nodes;
- roots: FOOD / 식품, HOUSEHOLD / 생활;
- common dairy/noodle/frozen/produce/grain/snack/beverage/seasoning/cleaning/paper/personal-care leaves;
- no forced OTHER bucket.

Decision states:

- `REUSE_PERSISTED`
- `AUTO_ASSIGNABLE`
- `REVIEW`
- `UNRESOLVED`

Strong unique local rules can be auto-assignable. Generic/conflicting evidence is review-gated. Unsupported evidence remains unresolved.

## 4. Persistence/correction contract

CP22 already contains `category_refs(product_id,category_id)`, so CP25 adds no schema migration.

Effective assignment is persisted on the existing stable catalog ID. Correction changes only CategoryRef and must preserve:

- stable ID;
- CatalogKind;
- canonicalName;
- brand/productName/variant/specification fields;
- createdAt/origin;
- aliases/item links.

Persisted category is reused before classifier rules, reducing repeated review.

## 5. Identity firewall

Category MUST NOT:

- prove product/commodity identity;
- alter MERCHANT/GLOBAL alias precedence;
- link/merge/split/create catalog entities;
- repair CP24 false split by itself;
- become a resolver feature without an explicit future amendment.

CP24 `identity/**` is unchanged and was frozen by CI diff guard.

## 6. Canonical local metrics

`fixtures=30 known_category=28 auto_suggestions=24 correct_auto_suggestions=24 incorrect_auto_suggestions=0 review_required=6 unresolved=2 repeat_cases=4 repeat_reused=4 correction_cases=3 correction_reused=3`

- auto suggestions 24/28 known-category fixtures;
- correct auto suggestions 24/24;
- incorrect auto suggestions 0;
- repeat reuse 4/4;
- correction reuse 3/3.

Synthetic/local only; not final real-receipt accuracy.

## 7. Frozen upstream contracts

### CP21
- stable catalog ID = identity authority;
- STANDARD/NON_STANDARD/UNCLASSIFIED semantics;
- grouping != comparability;
- source/confidence/confirmation independent.

### CP22
- product DB schema 2;
- receipt DB schema 1;
- category_refs already available;
- receipt price/date/store/validation authoritative;
- direct SQLite retained.

### CP23
- receipt semantic fields are unconfirmed evidence;
- standalone physical measure ambiguity remains review-gated.

### CP24
- MERCHANT exact alias -> GLOBAL exact alias -> strict unique semantic exact -> review -> unresolved;
- fuzzy similarity not auto-link authority;
- resolver never auto-creates/merges identities;
- category is not identity authority.

## 8. CP25 limitations deliberately retained

- taxonomy is bounded, not exhaustive;
- no user custom categories or tags;
- suggestion provenance/confidence is not separately persisted; only effective assignment is stored;
- category does not establish commodity price comparability;
- category does not eliminate identity fragmentation.

Do not solve these limitations through unrelated scope expansion.

## 9. Preflight process note

An accidental Markdown-only preflight commit `af4640af63d1a3d6faa1355addb8d3b4802205cb` briefly moved the CP24 branch before CP25 branch creation. CP24 was immediately restored with force-with-lease to `4858c6e6...`, and CP25 was branched directly from that exact canonical handoff. The orphan commit contains no app/schema/runtime change and is outside canonical CP24/CP25 history.

## 10. Next planned checkpoint

**CP26 — Commodity / Non-standard V2**

Required concerns before implementation:

1. common commodity identity such as 감자 across heterogeneous purchase forms;
2. preserve original 봉/팩/단/상자/개/kg/g etc. evidence;
3. grouping != comparability remains hard contract;
4. no guessed unit/package conversion;
5. false grouping and false splitting both measured;
6. raw unit/form preservation measured;
7. review burden/repeat reuse measured;
8. category remains metadata only;
9. receipt-derived price truth preserved.

CP26 is planned, not automatically authorized.

## 11. Security/public boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Do not use other project namespaces. Never commit secrets, signing material, private receipts, personal purchase DBs/backups, identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

## 12. Group discipline

For every checkpoint:

- recover canonical state;
- restate essence/non-goals;
- inspect materially relevant consistency risks;
- resolve cheap contradictions before implementation;
- avoid ritual re-audits and unrelated cleanup;
- implement the smallest coherent proof;
- run scoped CI/evidence;
- freeze exact executable refs;
- synchronize handoff/status docs;
- stop before the next unauthorized group.

## 13. Stop condition

**CP25 is complete and handoff-synchronized. Await explicit authorization for CP26.**
