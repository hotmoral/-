# ReceiptLedger V1 — CP26 Commodity / Non-standard V2 Plan

Updated: 2026-10-16 KST

## 1. Goal

Make NON_STANDARD commodity history useful across heterogeneous purchase forms while preserving original evidence and preventing fake comparability.

Example target:

`감자 1봉 / 감자 1상자 / 감자 5개 / 감자 1kg -> same commodity history`

but not:

`봉 price == kg price` or any guessed conversion.

## 2. Frozen upstream contracts

Preserve without modification:

- stable catalog ID remains identity/equality authority;
- CP24 STANDARD identity authority and alias precedence;
- CP25 category remains metadata only;
- product DB schema 2;
- receipt DB schema 1;
- receipt price/date/store/validation truth;
- CP23 semantic candidates remain parsed/unconfirmed evidence;
- public/offline/no-permission-expansion boundary.

## 3. Existing capabilities reused

No schema migration is required.

CP21/22 already provide:

- `CatalogKind.NON_STANDARD_COMMODITY`;
- `CatalogEntryV2.commodity(...)`;
- `PurchaseForm(quantity, unit, rawUnitLabel)`;
- observation purchase-form persistence;
- GLOBAL/MERCHANT alias persistence.

CP26 therefore adds policy/runtime logic rather than duplicate storage.

## 4. Grouping authority

Commodity grouping resolves only to an **existing NON_STANDARD stable catalog ID**.

Authority order:

1. confirmed MERCHANT exact alias;
2. confirmed GLOBAL exact alias;
3. unique exact commodity canonical-name match;
4. modifier-bearing whole-phrase suggestion -> REVIEW;
5. unresolved.

Rules:

- purchase form never defines commodity identity;
- category never defines commodity identity;
- lexical substring inside another word never creates a candidate (`감자` must not match `감자칩` or `감자전분`);
- STANDARD-target alias is a cross-kind conflict and cannot be commodity auto-group authority;
- strong STANDARD-product cues on an exact semantic name require review rather than commodity auto-group;
- resolver never creates, merges or splits catalog rows.

## 5. Confirmation/repeat-use learning

After explicit user confirmation, remember the raw receipt alias using the existing least-authority rule:

- merchant present -> MERCHANT alias by default;
- explicit global choice or no merchant -> GLOBAL alias.

This should reduce repeat review without broadening string similarity rules.

## 6. Purchase-form preservation

When a receipt supplies purchase-form evidence, persist the CP23 `PurchaseForm` unchanged:

- quantity;
- standardized `SalesUnitCode`;
- original `rawUnitLabel`;
- source/confidence/confirmation.

CP26 must not upgrade parsed evidence to CONFIRMED merely because the commodity identity is known.

## 7. Form/comparability relation

CP26 does not calculate price statistics. It exposes only a form relation for CP27:

- `EXACT_NORMALIZABLE_QUANTITY`: same exact physical/count dimension with exact built-in base conversion (`kg<->g`, `L<->mL`, count);
- `SAME_FORM_ONLY`: same package/form class such as 봉 vs 봉, or identical OTHER raw unit label; usable for filtering/context, not normalized price authority;
- `INCOMPARABLE`: different dimensions/forms or unsupported conversion;
- `MISSING`: purchase-form evidence absent.

This preserves `grouping != comparability`.

## 8. Local acceptance metrics

Synthetic fixtures must report at least:

- known commodity count;
- auto groups / correct / incorrect;
- false grouping;
- review suggestions;
- false split / fragmentation risk;
- negative fixtures;
- raw-form preservation;
- confirmed repeat reuse.

Required gates:

- incorrect auto groups = 0;
- false grouping = 0;
- all raw-form preservation fixtures preserved exactly;
- all confirmed repeat fixtures reused;
- any false split remains visible rather than erased by unsafe rule broadening.

These are local deterministic metrics, not CP35 real-receipt accuracy.

## 9. Scope

Allowed implementation changes:

- new `commodity/**` runtime package;
- new commodity tests;
- CP26 docs;
- ReceiptLedger-specific CP26 CI workflow;
- version metadata.

Do not modify:

- `catalog/**`;
- `product/**` persistence/schema/runtime;
- `semantics/**`;
- `identity/**`;
- `category/**`;
- receipt persistence;
- manifest/permissions;
- existing price-history semantics.

## 10. Non-goals

- no commodity auto-creation;
- no fuzzy/embedding/phonetic grouping;
- no barcode/cloud catalog;
- no guessed 봉/상자/팩 weight or count conversion;
- no price-per-unit calculation;
- no cheap/normal/expensive judgment;
- no UI redesign;
- no custom taxonomy expansion.

## 11. Stop condition

Implementation -> tests/lint/build -> metrics/evidence -> exact refs -> handoff synchronization, then stop. CP27 must not start automatically.
