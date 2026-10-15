# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct ReceiptLedger execution state from old chat before reading current files and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP24_IDENTITY_RESOLVER_V2_CLOSEOUT.md`
4. `receiptledger/CP24_IDENTITY_RESOLVER_V2_EVIDENCE.md`
5. `receiptledger/CP24_IDENTITY_RESOLVER_V2_PLAN.md`
6. `receiptledger/IDENTITY_RESOLVER_V2_CONSISTENCY_REVIEW.md`
7. `receiptledger/IDENTITY_RESOLVER_V2_GOLDEN_VECTORS.md`
8. `receiptledger/CP23_RECEIPT_PRODUCT_SEMANTICS_CLOSEOUT.md`
9. `receiptledger/CP23_RECEIPT_PRODUCT_SEMANTICS_EVIDENCE.md`
10. `receiptledger/CP22_PERSISTENCE_V2_CLOSEOUT.md`
11. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
12. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
13. `receiptledger/README.md`
14. `receiptledger/WORK_UNIT.md`

## 1. Latest executable checkpoint

**CP24 — Identity Resolver V2 — PASS / COMPLETE**

- branch: `receiptledger/run-v1-identity-resolver-v2-20261016`
- predecessor handoff: `d04667a5dd9f257117f59bcde194d5b702fa1337`
- frozen implementation HEAD: `4b556afd4dd52b68cf768e937bb456665ad4c231`
- canonical Actions: `38824134990` — SUCCESS
- job: `116727478370` — SUCCESS
- artifact ID: `12014915453`
- artifact digest: `sha256:4740590ca2c7d7525842aa3ebe6ec7964911d303322ebad77b5701344ce76867`
- APK SHA-256: `0656c60110ba7debcb0801ddee048cd2220b959c2119539a79274eebbc05eb6e`
- CP24 identity tests: 8/8 PASS
- CP23 semantics tests: 7/7 PASS
- CP21 catalog tests: 15/15 PASS
- CP22 persistence tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- versionName `1.0.22-identity-resolver-v2`, versionCode 23

Later closeout/status commits must remain documentation-only; do not move the executable evidence boundary.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 제품/품목 검색 -> 과거 가격과 현재 가격 판단`

The same purchased product must accumulate under the correct stable identity. Both wrong merging and identity fragmentation undermine price history.

## 3. CP24 resolver contract

Decision states:

- `AUTO_LINK`
- `REVIEW`
- `UNRESOLVED`

Authority precedence:

1. exact MERCHANT alias;
2. exact GLOBAL alias;
3. unique strict semantic exact;
4. semantic suggestion/review;
5. unresolved.

The resolver only points to existing stable catalog IDs. It does not auto-create or merge entities.

## 4. Confirmed alias rules

MERCHANT exact alias is more specific than GLOBAL and is checked first.

A confirmed alias is normally reusable, but a dangling target or strong explicit contradiction in current brand/variant/non-ambiguous specification yields REVIEW instead of silent fallback or automatic linking.

Free lexical product-name differences do not veto an exact alias because abbreviations are a principal reason aliases exist.

## 5. Strict semantic auto-link rules

STANDARD semantic auto-link requires:

- CP23 not review-required and not measure-ambiguous;
- confirmed exact catalog productName;
- confirmed exact catalog specification;
- brand confirmed/present/exact on both sides if either side carries it;
- variant confirmed/present/exact on both sides if either side carries it;
- exactly one strict candidate.

Product-name equality, category, store, HIGH parser confidence, fuzzy similarity or partial semantic resemblance are insufficient by themselves.

Duplicate strict candidates are review-gated; CP24 does not merge them.

## 6. Repeat learning

After an explicit user confirmation:

- merchant context -> remember the raw alias in MERCHANT scope by default;
- explicit global decision or no merchant -> GLOBAL alias.

This is least-authority learning. It is intended to make repeat purchases automatic without poisoning other stores' alias namespaces.

## 7. Canonical local metrics

`fixtures=24 known_identity=20 auto_links=14 correct_auto_links=14 incorrect_auto_links=0 false_merge=0 false_split=1 review_required=6 unresolved=4 repeat_cases=4 repeat_reused=4`

- automatic-link correctness: 14/14;
- false merge: 0;
- incorrect automatic link: 0;
- false split / fragmentation risk: 1/20 = 5%;
- repeat confirmed reuse: 4/4 = 100%.

The one fragmentation-risk case is an intentionally weak known-product fixture where the resolver refuses to guess and fails to surface the correct existing identity. Keep this visible. Do not force it to zero by broadening unsafe auto-link rules.

These are bounded synthetic-fixture metrics. CP35 remains the end-to-end real/sanitized receipt evaluation.

## 8. Frozen upstream/storage rules

- CP21 stable catalog ID remains identity authority;
- product DB `receipt-products-v1.db`, schema 2;
- receipt DB `receiptledger-v1.db`, schema 1;
- CP23 parsed fields remain unconfirmed evidence;
- standalone physical-measure ambiguity remains review-gated;
- category is not identity proof;
- NON_STANDARD semantic grouping remains CP26 work;
- grouping != comparability;
- price/date/store/validation remain receipt-derived;
- no permission/network/privacy expansion.

## 9. Next planned implementation checkpoint

**CP25 — Category System**

Required direction:

- define practical V1 category taxonomy/hierarchy;
- persist stable category identities/assignments;
- assign/suggest categories to already-resolved Product/Commodity identities;
- support user correction and safe repeat reuse;
- measure category suggestion accuracy and review burden locally;
- never use category to prove or override CP24 product identity.

CP25 is planned, not automatically authorized.

## 10. Security/public boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Do not use other project namespaces. Never commit secrets, signing material, private receipts, personal purchase databases/backups, identifiers or uncleared assets.

Forbidden packaged permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

## 11. Group discipline

For every checkpoint:

- recover canonical state;
- restate essence/non-goals;
- inspect only material consistency risks;
- resolve cheap contradictions first;
- avoid unrelated cleanup and speculative scope;
- implement the smallest coherent proof;
- run scoped CI/evidence;
- freeze exact executable refs;
- synchronize handoff/status docs;
- stop before the next unauthorized group.

## 12. Stop condition

**CP24 is complete and handoff synchronization is the final operation of this group. Await explicit authorization for CP25.**
