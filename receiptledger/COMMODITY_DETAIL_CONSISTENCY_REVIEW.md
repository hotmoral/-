# ReceiptLedger V1 — CP32 Commodity Detail Consistency Review

Updated: 2026-10-16 KST
Status: IMPLEMENTATION ALLOWED / READ-ONLY PRESENTATION EXTENSION

## 1. Verdict

CP32 can be implemented without changing identity, persistence, commodity grouping, price intelligence or evaluation policy.

The cheapest safe architecture is a read-only projection over CP26–28 facts plus a new View-based Activity.

## 2. Identity boundary

NON_STANDARD identity remains the stable catalog ID plus canonical commodity name.

`CatalogEntryV2` explicitly forbids STANDARD-only brand/product/variant/spec fields on commodity entries. CP32 must not invent them from receipt text or search similarity.

Category remains browse metadata only and cannot widen identity authority.

## 3. Grouping versus comparability

CP26 allows one commodity such as `감자` to contain heterogeneous forms: kg, g, 개, 봉, 상자, etc.

That grouping does not imply one price basis.

CP27 already partitions safe cohorts:

- WEIGHT_KG;
- VOLUME_L;
- EACH;
- one independent LIKE_FORM cohort per preserved form key.

CP32 must expose this partition rather than flatten it.

## 4. Evaluation safety

`PriceEvaluationServiceV1` evaluates exactly one CP27 cohort.

Strict normalized cohorts can become EVALUATED after sufficient history. LIKE_FORM is hard-gated to `CONTEXTUAL_ONLY`, so no UI-side rule is needed or permitted to suppress/enable judgments.

The UI must not combine cohort medians or create a commodity-wide usual price.

## 5. Latest purchase safety

`PriceIntelligenceV2.observations` is newest-first and includes excluded observations.

Therefore the real latest purchase can be shown as provenance independently of comparison sections.

Risk: replacing a contextual/excluded latest purchase with the newest strict purchase and labeling it `최근 구매` would be misleading.

Mitigation: preserve two concepts:

- latest receipt-linked purchase record;
- latest value within each comparison basis.

## 6. Contextual-form safety

A bag/pack/box/bundle/other form may yield a LIKE_FORM comparison rate using the observed quantity, but CP27 labels it contextual rather than mathematically normalized.

CP32 may show that rate as reference history only. It must not:

- compare it with kg/L/each;
- compare different LIKE_FORM keys;
- attach cheap/expensive tone;
- imply an inferred weight/content.

## 7. Chart safety

Only strict normalized cohorts require charts in CP32.

Each chart gets one cohort and calls the CP30 single-basis grammar guard. It plots receipt observations oldest -> newest and may show usual-price reference/judgment color only when CP28 status is EVALUATED.

No combined commodity chart is allowed.

## 8. Receipt traceability

Every CP27 observation already contains receipt ID, ordinal, date, store, raw item name, PurchaseForm, eligibility and derived comparison rate when eligible.

Thus CP32 needs no new history table. Purchase rows can open the existing Receipt Detail directly.

Excluded observations stay visible as provenance but remain outside cohorts/charts/judgments.

## 9. Visual-risk review

### Risk: basis overload
Mitigation: use plain Korean section titles (`무게 기준`, `부피 기준`, `개수 기준`) and explicit unit labels; show only bases that actually exist.

### Risk: one-card-per-number clutter
Mitigation: keep typography/whitespace primary; cards group semantic sections, not every value.

### Risk: contextual forms look equivalent to strict history
Mitigation: separate heading, INFO presentation, `참고용` wording and no judgment colors/charts.

### Risk: latest raw purchase amount is mistaken for normalized rate
Mitigation: show purchase form and label; normalized strict values always include `/kg`, `/L` or `/개`.

### Risk: no strict history looks broken
Mitigation: intentional INFO state explaining that purchase history exists but safe direct comparison may not yet exist.

## 10. Responsive/accessibility risk review

- compact/medium single-column preserves reading order;
- expanded two-pane only through CP30 policy;
- chart spoken summary includes basis and count;
- history rows >=64dp and do not depend on tiny graph points;
- text+color semantics retained;
- Android SP dimension conversion used in custom drawing.

## 11. Scope isolation

Permitted:

- new Commodity Detail Activity/read model/formatter/chart;
- new strings and manifest entry;
- minimal NON_STANDARD route from Price History;
- version increment;
- CP32 tests/workflow/docs.

Frozen:

- MainActivity/Capture;
- ReceiptDetail behavior;
- ReceiptReviewDialog;
- ProductDetail semantics/UI except regression coverage;
- catalog/product/semantics/identity/category/commodity/persistence/price/priceintel/priceeval/search packages;
- product schema 2 / receipt schema 1;
- permission/network posture.

## 12. Conclusion

No blocking contradiction remains. CP32 implementation is allowed as a NON_STANDARD-only read/presentation layer, provided strict and contextual histories remain visibly and mathematically separate.