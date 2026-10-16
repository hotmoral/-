# ReceiptLedger V1 — Project Status Latest

Updated: 2026-10-16 KST
Repository: `hotmoral/-`
Public namespace: `receiptledger/`

## 1. Current completed boundary

Latest executable checkpoint: **CP26 — Commodity / Non-standard V2 — PASS / COMPLETE**.

- branch: `receiptledger/run-v1-commodity-nonstandard-v2-20261016`
- predecessor CP25 handoff: `e9bbd3d1b2b5c6e153d6c76b1c02b2a1cd217389`
- frozen CP26 implementation HEAD: `a0b4b1246f2e7bc4d41b3376507ae34f44e1e372`
- canonical Actions run: `38829423445` — SUCCESS
- job: `116744485504` — SUCCESS
- artifact ID: `12016292501`
- artifact digest: `sha256:6ad4342d61274530aecc090fbe7caa8f606f3a20c113285e3b18cd86893336bd`
- debug APK SHA-256: `250d4d00bb93334fede3873c92e85b63d1ccd05ee5d09f9a4c7970fb366b90cb`
- Commodity / Non-standard V2 tests: 8/8 PASS
- Category System tests: 8/8 PASS
- Identity Resolver V2 tests: 8/8 PASS
- Receipt Product Semantics tests: 7/7 PASS
- Catalog Domain V2 tests: 15/15 PASS
- Persistence V2 tests: 7/7 PASS
- lint: 0 errors / 0 warnings
- version: `1.0.24-commodity-nonstandard-v2` / versionCode 25

Any later handoff commit is documentation-only. The executable/evidence boundary remains `a0b4b124...`.

## 2. Product objective

ReceiptLedger is a **personal purchase-price memory and comparison system**.

Primary loop:

`receipt -> trustworthy extraction -> product/commodity identity -> purchase observation -> historical price -> price judgment`

Receipt is evidence/input. Stable product/commodity identity and trustworthy historical price judgment are the destination.

## 3. CP26 result

CP26 makes heterogeneous NON_STANDARD purchase forms accumulate under an existing commodity stable ID without implying invalid price comparability.

Grouping authority:

1. confirmed MERCHANT exact alias;
2. confirmed GLOBAL exact alias;
3. unique exact commodity canonical-name match;
4. modifier-bearing whole-phrase suggestion -> REVIEW;
5. unresolved.

Frozen rules:

- resolve only to existing `NON_STANDARD_COMMODITY` IDs;
- purchase form never proves commodity identity;
- category never proves commodity identity;
- lexical substring inside another word is not a candidate (`감자` != `감자칩` / `감자전분`);
- strong packaged-product cues review-gate semantic commodity grouping;
- STANDARD-target aliases are cross-kind conflicts, not commodity auto-group authority;
- no fuzzy/edit-distance/embedding/phonetic auto-grouping;
- no auto-create, merge or split of catalog entities.

## 4. Purchase-form / comparability boundary

Original `PurchaseForm` evidence remains observation-specific and preserves quantity, standardized unit, raw unit label and provenance/confirmation.

CP26 exposes only a relation for later CP27 use:

- `EXACT_NORMALIZABLE_QUANTITY`: exact physical/count basis such as kg/g, L/mL or count;
- `SAME_FORM_ONLY`: same raw package/form such as 봉 vs 봉; not normalized price authority;
- `INCOMPARABLE`: different/unsupported forms or dimensions;
- `MISSING`: no form evidence.

Thus **grouping != comparability** remains a hard contract. CP26 does not compute unit price or price judgment.

## 5. Storage / upstream boundary

Preserve:

- stable catalog ID = identity/equality authority;
- product schema = 2;
- receipt schema = 1;
- CP21 catalog domain unchanged;
- CP23 semantic evidence unchanged;
- CP24 STANDARD identity resolver unchanged;
- CP25 category system unchanged;
- receipt persistence and price/date/store/validation truth unchanged;
- no guessed package-form conversion.

No schema v3 or new table was needed because CP21/22 already supplied NON_STANDARD commodity rows, aliases and observation purchase-form persistence.

## 6. Local quality evidence

Canonical metric:

`fixtures=25 known_commodity=21 auto_groups=18 correct_auto_groups=18 incorrect_auto_groups=0 false_group=0 review_suggestions=2 false_split=1 negative_fixtures=4 raw_form_cases=12 raw_form_preserved=12 repeat_cases=3 repeat_reused=3`

Thus:

- automatic grouping correctness: 18/18;
- false grouping: 0;
- safe review suggestions: 2;
- visible false split / fragmentation risk: 1/21 = 4.7619%;
- raw purchase-form preservation: 12/12;
- confirmed repeat reuse: 3/3.

The false split remains visible instead of being hidden by unsafe matching expansion. These are deterministic synthetic fixtures, not CP35 real-receipt accuracy claims.

## 7. Known limitations

- groups only to already-existing commodity IDs;
- attached subtype forms such as `알감자` may remain fragmented until confirmed;
- no commodity auto-creation;
- no full commodity ontology;
- CP26 form relation is not yet a price-comparison policy;
- no price statistics or cheap/normal/expensive judgment here.

## 8. Completed checkpoint chain

Foundation -> Image/Document -> OCR -> Layout -> Structure -> Item Tuple -> Validation -> Persistence -> Image Archive -> Receipt Library -> Review/Edit -> Product Identity -> Price History -> OCR Recovery -> Vertical Integration -> Merchant -> Cross-Pass Merge -> Build Hygiene -> Target API36 -> CP20 Product Rebaseline -> CP21 Catalog Domain V2 -> CP22 Persistence V2 -> CP23 Receipt Product Semantics -> CP24 Identity Resolver V2 -> CP25 Category System -> **CP26 Commodity / Non-standard V2**.

## 9. Next planned checkpoint

**CP27 — Price Intelligence V2**.

Before statistics, CP27 must define a canonical, receipt-traceable comparison price and eligibility contract covering:

- line amount vs one purchased unit/package;
- quantity > 1;
- item-specific discounts;
- unallocated receipt-level coupons/discounts;
- provenance and validation state;
- invalid/incomplete observations;
- STANDARD exact-package comparability;
- NON_STANDARD exact-normalizable or like-form subsets without fake conversion;
- deterministic latest/previous/delta/min/max/mean/median/period/store metrics.

**Do not begin CP27 without explicit user authorization.**

## 10. Canonical restart order

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/CP26_COMMODITY_NONSTANDARD_V2_CLOSEOUT.md`
4. `receiptledger/CP26_COMMODITY_NONSTANDARD_V2_EVIDENCE.md`
5. `receiptledger/CP26_COMMODITY_NONSTANDARD_V2_PLAN.md`
6. `receiptledger/COMMODITY_NONSTANDARD_V2_CONSISTENCY_REVIEW.md`
7. `receiptledger/COMMODITY_NONSTANDARD_V2_GOLDEN_VECTORS.md`
8. `receiptledger/CP25_CATEGORY_SYSTEM_CLOSEOUT.md`
9. `receiptledger/CLIENT_REQUIREMENT_ALIGNMENT_AMENDMENT.md`
10. `receiptledger/PRODUCT_REBASELINE_V1_ROADMAP.md`
11. `receiptledger/README.md`
12. `receiptledger/WORK_UNIT.md`

GitHub is canonical. Verify current branch/ref and frozen implementation boundary before future work.

## 11. Public/privacy boundary

Modify only `receiptledger/**` and explicitly ReceiptLedger-prefixed workflows. Never commit secrets, release signing material, private receipts, real purchase DB/backups, personal identifiers or uncleared assets.

Forbidden APK permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless separately authorized.

**Current stop condition: CP26 is complete. Await explicit authorization for CP27.**
