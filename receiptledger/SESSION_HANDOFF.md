# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Restart contract

GitHub is canonical. Do not reconstruct execution state from old chat before reading current files and verifying refs.

Read in order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP26_COMMODITY_NONSTANDARD_V2_CLOSEOUT.md`
4. `receiptledger/CP26_COMMODITY_NONSTANDARD_V2_EVIDENCE.md`
5. `receiptledger/CP26_COMMODITY_NONSTANDARD_V2_PLAN.md`
6. `receiptledger/COMMODITY_NONSTANDARD_V2_CONSISTENCY_REVIEW.md`
7. `receiptledger/COMMODITY_NONSTANDARD_V2_GOLDEN_VECTORS.md`
8. `receiptledger/CP25_CATEGORY_SYSTEM_CLOSEOUT.md`
9. `receiptledger/CP25_CATEGORY_SYSTEM_EVIDENCE.md`
10. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
11. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
12. `receiptledger/README.md`
13. `receiptledger/WORK_UNIT.md`

## 1. Latest executable checkpoint

**CP26 — Commodity / Non-standard V2 — PASS / COMPLETE**

- branch: `receiptledger/run-v1-commodity-nonstandard-v2-20261016`
- predecessor handoff: `e9bbd3d1b2b5c6e153d6c76b1c02b2a1cd217389`
- frozen implementation HEAD: `a0b4b1246f2e7bc4d41b3376507ae34f44e1e372`
- canonical Actions: `38829423445` — SUCCESS
- job: `116744485504` — SUCCESS
- artifact ID: `12016292501`
- artifact digest: `sha256:6ad4342d61274530aecc090fbe7caa8f606f3a20c113285e3b18cd86893336bd`
- APK SHA-256: `250d4d00bb93334fede3873c92e85b63d1ccd05ee5d09f9a4c7970fb366b90cb`
- CP26 commodity tests: 8/8 PASS
- CP25 category tests: 8/8 PASS
- CP24 identity tests: 8/8 PASS
- CP23 semantics tests: 7/7 PASS
- CP21 catalog tests: 15/15 PASS
- CP22 persistence tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- versionName `1.0.24-commodity-nonstandard-v2`, versionCode 25

Later closeout/status commits must remain documentation-only; do not move the executable evidence boundary.

## 2. Product essence

ReceiptLedger is a personal purchase-price memory and comparison system.

Target experience:

`영수증 추가 -> 자동 처리 -> 필요한 항목만 확인 -> 저장 -> 제품/품목 검색·탐색 -> 과거 가격과 현재 가격 판단`

Receipt remains evidence/input. Product/commodity history and trustworthy price judgment are the destination.

## 3. CP26 grouping contract

Commodity grouping resolves only to an existing `NON_STANDARD_COMMODITY` stable ID.

Authority precedence:

1. confirmed MERCHANT exact alias;
2. confirmed GLOBAL exact alias;
3. unique exact commodity canonical-name match;
4. modifier-bearing safe whole-phrase suggestion -> REVIEW;
5. unresolved.

Hard rules:

- purchase form is not commodity identity authority;
- category is not commodity identity authority;
- lexical substring inside another word is forbidden as a candidate;
- STANDARD-target alias is CROSS_KIND_CONFLICT/REVIEW;
- strong packaged-product cues review-gate semantic commodity matching;
- fuzzy/edit-distance/embedding/phonetic similarity is not automatic grouping authority;
- CP26 never auto-creates, merges or splits catalog rows.

## 4. Confirmation / repeat learning

After explicit user confirmation, commodity aliases reuse CP24 least-authority storage:

- merchant context -> MERCHANT alias by default;
- explicit global decision or no merchant -> GLOBAL alias.

This converts repeated store/POS strings into automatic grouping without widening general lexical matching.

## 5. Purchase-form preservation

CP23 purchase-form evidence is persisted unchanged for the observation:

- quantity;
- standardized SalesUnitCode;
- original raw unit label;
- source/confidence/confirmation.

Grouping confirmation does not upgrade a parsed purchase form to CONFIRMED.

## 6. Grouping vs comparability

CP26 defines only form relations, not price metrics:

- `EXACT_NORMALIZABLE_QUANTITY`: exact base quantity exists within the same physical/count dimension (kg/g, L/mL, count);
- `SAME_FORM_ONLY`: same package/form class such as 봉 vs 봉, or same OTHER raw label;
- `INCOMPARABLE`: different/unsupported dimensions/forms;
- `MISSING`: no purchase-form evidence.

`SAME_FORM_ONLY` is not normalized price authority. CP27 must separately define price comparison eligibility.

## 7. Canonical local metrics

`fixtures=25 known_commodity=21 auto_groups=18 correct_auto_groups=18 incorrect_auto_groups=0 false_group=0 review_suggestions=2 false_split=1 negative_fixtures=4 raw_form_cases=12 raw_form_preserved=12 repeat_cases=3 repeat_reused=3`

- auto-group correctness: 18/18;
- false group: 0;
- safe review suggestions: 2;
- false split / fragmentation risk: 1/21 = 4.7619%;
- raw form preserved: 12/12;
- confirmed repeat reuse: 3/3.

The visible false split is intentionally retained. Do not force it to zero by introducing unsafe substring/fuzzy matching.

These are bounded synthetic metrics, not CP35 end-to-end real/sanitized receipt accuracy.

## 8. Frozen upstream/storage rules

- stable catalog ID remains equality/identity authority;
- product DB `receipt-products-v1.db`, schema 2;
- receipt DB `receiptledger-v1.db`, schema 1;
- CP23 parser evidence remains unconfirmed;
- CP24 STANDARD identity authority unchanged;
- CP25 category authority unchanged and non-identifying;
- price/date/store/validation truth remains receipt-derived;
- no guessed package-form conversion;
- no permission/network/privacy expansion.

## 9. CP26 limitations deliberately retained

- existing commodity IDs only;
- no automatic commodity creation;
- subtype/attached-token forms such as `알감자` can remain fragmented until confirmed;
- no exhaustive commodity ontology;
- no unit-price or history aggregation policy in CP26;
- no UI redesign.

Do not solve these through unrelated scope expansion.

## 10. Next planned implementation checkpoint

**CP27 — Price Intelligence V2**

Required direction:

1. define canonical comparison price for one receipt-derived purchase observation;
2. distinguish line amount, quantity and one package/unit meaning;
3. account only for discounts that can be attributed without guessing;
4. preserve unallocated receipt-level coupon/benefit provenance rather than fake item allocation;
5. exclude invalid/incomplete observations where required;
6. STANDARD comparisons require the correct stable exact-product identity;
7. NON_STANDARD comparisons must respect CP26 form relations and never treat package forms as mathematically normalized;
8. then compute deterministic latest/previous/delta/min/max/mean/median/period/store metrics;
9. remain receipt-traceable and test insufficient/incomparable states.

CP27 is planned, not automatically authorized.

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

**CP26 is complete and handoff-synchronized. Await explicit authorization for CP27.**
