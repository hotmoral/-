# ReceiptLedger V1 — CP26 Commodity / Non-standard V2 Closeout

Updated: 2026-10-16 KST
Status: **PASS / COMPLETE**

## 1. Closed boundary

- branch: `receiptledger/run-v1-commodity-nonstandard-v2-20261016`
- predecessor CP25 handoff: `e9bbd3d1b2b5c6e153d6c76b1c02b2a1cd217389`
- frozen implementation HEAD: `a0b4b1246f2e7bc4d41b3376507ae34f44e1e372`
- canonical Actions run: `38829423445` — SUCCESS
- job: `116744485504` — SUCCESS
- artifact ID: `12016292501`
- artifact digest: `sha256:6ad4342d61274530aecc090fbe7caa8f606f3a20c113285e3b18cd86893336bd`
- APK SHA-256: `250d4d00bb93334fede3873c92e85b63d1ccd05ee5d09f9a4c7970fb366b90cb`
- version: `1.0.24-commodity-nonstandard-v2` / versionCode 25

## 2. What CP26 added

CP26 makes heterogeneous NON_STANDARD purchase forms accumulate under an existing commodity stable ID without making those forms falsely comparable.

Added:

- conservative commodity grouping resolver;
- MERCHANT/GLOBAL confirmed alias reuse for commodities;
- exact canonical commodity-name grouping;
- modifier-bearing whole-phrase review suggestions;
- cross-kind STANDARD/NON_STANDARD firewall;
- explicit user-confirmation helper using existing least-authority alias learning;
- purchase-form evidence preservation helper;
- form relation: `EXACT_NORMALIZABLE_QUANTITY / SAME_FORM_ONLY / INCOMPARABLE / MISSING`;
- bounded local grouping/fragmentation/raw-form/repeat-use metrics.

## 3. Product interpretation

Examples such as:

- 감자 1봉
- 감자 1상자
- 감자 5개
- 감자 1kg

can now resolve to the same `감자` commodity identity when the semantic commodity name is exact or confirmed alias knowledge exists.

The observation still retains its own purchase quantity/unit/form. Grouping therefore answers **“같은 품목인가?”**, not **“가격을 같은 기준으로 비교해도 되는가?”**.

## 4. Safety boundaries

- category is not grouping authority;
- purchase form is not commodity identity authority;
- `감자` does not substring-match `감자칩` or `감자전분`;
- modifier forms such as `국산 감자` are review-only until confirmed;
- STANDARD-target aliases return cross-kind REVIEW rather than commodity auto-group;
- strong packaged-product cues review-gate exact-name commodity matching;
- no fuzzy/edit-distance/embedding/phonetic auto-grouping;
- no commodity auto-create or merge;
- no guessed 봉/상자/팩 conversion.

## 5. Form/comparability boundary

CP26 exposes only quantity/form relations for later CP27 use.

- kg/g, L/mL and count can have an exact mathematical quantity basis;
- 봉 vs 봉 or the same raw OTHER label is only `SAME_FORM_ONLY`;
- 봉 vs 상자, 개 vs kg and unsupported forms are incomparable;
- CP26 does not compute unit price, price averages or cheap/expensive labels.

## 6. Local evidence

Canonical metrics:

`fixtures=25 known_commodity=21 auto_groups=18 correct_auto_groups=18 incorrect_auto_groups=0 false_group=0 review_suggestions=2 false_split=1 negative_fixtures=4 raw_form_cases=12 raw_form_preserved=12 repeat_cases=3 repeat_reused=3`

Interpretation:

- automatic grouping correctness: 18/18;
- false grouping: 0;
- safe review suggestions: 2;
- visible false split / fragmentation risk: 1/21 known commodity fixtures = 4.7619%;
- raw purchase-form preservation: 12/12;
- confirmed repeat reuse: 3/3.

The false split is deliberately retained. It must be reduced via confirmation/alias knowledge or better evidence, not unsafe substring/fuzzy grouping.

## 7. Storage / upstream preservation

Unchanged:

- product schema 2;
- receipt schema 1;
- CP21 catalog domain;
- CP23 semantics;
- CP24 identity resolver;
- CP25 category system;
- receipt persistence;
- manifest/permissions;
- receipt-derived price/date/store/validation truth.

No new table or schema migration was required.

## 8. Known limitations

- resolver groups only to existing NON_STANDARD stable IDs;
- subtype/attached-token names such as `알감자` can remain fragmented until confirmed;
- no automatic commodity creation;
- no complete produce ontology;
- form relation is not yet a price-comparison policy;
- synthetic fixtures are not CP35 real-receipt accuracy.

## 9. Next boundary

Next planned checkpoint: **CP27 — Price Intelligence V2**.

CP27 must first define a receipt-traceable canonical comparison price and eligibility rules before computing latest/previous/delta/mean/median/min/max/store/period metrics. It must consume CP26 grouping/form information without turning `SAME_FORM_ONLY` into fake normalized comparability.

CP27 is not authorized by this closeout.

## 10. Stop condition

CP26 implementation, CI/evidence and handoff synchronization are complete. Stop at this boundary.
