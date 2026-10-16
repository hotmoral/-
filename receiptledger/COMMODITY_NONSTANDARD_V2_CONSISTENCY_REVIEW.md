# ReceiptLedger V1 — Commodity / Non-standard V2 Consistency Review

Updated: 2026-10-16 KST

## 1. Essential question

Can ReceiptLedger group heterogeneous observations under one commodity without corrupting product identity or implying invalid price comparability?

Decision: **yes, if commodity grouping authority and form comparability are separate contracts.**

## 2. CP21 consistency

CP21 already defines `NON_STANDARD_COMMODITY` as a stable catalog identity without STANDARD brand/product/variant/specification fields.

CP26 therefore must not add product-like SKU fields to commodities. Commodity identity remains the stable catalog ID plus canonical commodity name and confirmed aliases.

## 3. CP22 consistency

CP22 already stores:

- commodity catalog rows in the existing `products` table;
- contextual aliases;
- item links;
- observation purchase forms.

No new table is needed. Duplicate observation storage would create stale-divergence risk and is rejected.

## 4. CP23 consistency

CP23 deliberately treats standalone physical measures such as `감자 1KG` as ambiguous between package specification and purchase form.

For CP26, once resolution is specifically against an existing NON_STANDARD commodity, purchase form can participate as observation evidence, but CP23 source/confidence/confirmation must remain unchanged. CP26 does not rewrite CP23 parse results.

## 5. CP24 consistency

CP24 strict semantic auto-link is STANDARD-only. CP26 adds a separate commodity path rather than widening CP24.

Confirmed MERCHANT/GLOBAL aliases remain reusable identity knowledge, but CP26 validates that alias targets are actually NON_STANDARD. A STANDARD target becomes REVIEW/cross-kind conflict.

Thus CP24 source code and authority contract remain frozen.

## 6. CP25 consistency

Category equality must not group commodities. `FOOD.PRODUCE.VEGETABLE` can contain 감자, 당근, 양파 and many unrelated identities.

CP26 does not read category as grouping authority.

## 7. False grouping risk

High-cost failure: `감자칩` or `감자전분` accidentally entering the `감자` history.

Mitigations:

- exact canonical-name match may auto-group;
- modifier-bearing names use whole-phrase boundaries and are review-only;
- substring matching inside one lexical token is forbidden;
- strong STANDARD cues on an exact semantic name review-gate automatic grouping;
- fuzzy similarity is not authority.

## 8. False splitting risk

Conservative matching can miss `알감자`, store abbreviations or other modifier forms.

Mitigation is not unsafe auto-group broadening. Instead:

- safe modifier suggestions surface likely existing commodities for review;
- explicit confirmation learns contextual alias knowledge;
- repeat use then becomes automatic.

Any residual false split remains an explicit metric.

## 9. Purchase-form correctness

`PurchaseForm` original quantity/unit/raw label must be retained exactly.

No conversion is allowed for BAG/PACK/BOX/BUNDLE/OTHER merely because observations share a commodity.

Exact built-in base conversion is allowed only as a **quantity-basis relation** for dimensions already defined by `SalesUnitCode`:

- g/kg;
- mL/L;
- EACH/count.

This relation is not itself a price statistic or user-facing value judgment.

## 10. Persistence correctness

Explicit commodity grouping confirmation may reuse CP24 least-authority alias learning.

Purchase-form persistence must preserve parsed source/confidence/confirmation and must not silently turn parsed evidence into user-confirmed evidence.

## 11. Security/privacy

CP26 is entirely local/offline. No permission, network, cloud, barcode or public-fixture expansion is required.

## 12. Scope decision

No schema migration, no Room migration, no price-history rewrite and no UI work are justified in CP26.

The smallest coherent proof is:

- commodity resolver;
- explicit confirmation helper;
- form-relation classifier;
- deterministic golden metrics;
- upstream regression and scope guards.
