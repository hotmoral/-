# ReceiptLedger V1 — CP21 Catalog Domain V2 Consistency Review

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_CATALOG_DOMAIN_V2_01`

## 0. Review objective

Test CP21 against the frozen CP20 product definition and the existing V1 implementation before persistence migration begins. Review only dimensions materially affected by the catalog-domain contract.

## 1. Executive result

**Result: COMPATIBLE / NO BLOCKING CONTRADICTION.**

The safe design is additive: introduce a new storage-independent V2 catalog domain beside the proven legacy product runtime, preserve legacy IDs and semantics, and defer schema migration to CP22.

## 2. Domain review

### STANDARD

CP20 requires exact repeatable packaged-product identity. CP21 represents this as `STANDARD_PRODUCT` and allows structured brand/product/variant/specification metadata without making those fields authoritative entity equality.

Finding: compatible. Stable catalog ID remains authoritative, preventing accidental merge from partial semantics.

### NON_STANDARD

CP20 permits one commodity to group bag/box/kg/each observations without asserting cross-unit comparability. CP21 represents one `NON_STANDARD_COMMODITY` entity plus per-observation `PurchaseForm`.

Finding: compatible. Sales form belongs to observation, not commodity identity.

### UNCLASSIFIED

CP20 says unresolved is not a fake catalog row. CP21 therefore has no V2 catalog kind for UNCLASSIFIED and rejects legacy UNCLASSIFIED conversion.

Finding: exact alignment.

## 3. Identity-poisoning review

Risk: fields such as brand/name/1L could accidentally become equality or migration merge keys.

Mitigation:

- `CatalogEntryV2` entity equality/hash are ID-only;
- structured fields are candidate metadata only;
- category and merchant context are excluded from entity equality;
- legacy adapter preserves rows one-for-one and never parses/merges.

Residual risk is intentionally deferred to CP24 resolver authority rules.

## 4. Legacy/migration review

Existing product DB remains schema version 1. CP21 does not modify it.

Migration-sensitive decisions frozen now:

- preserve every existing catalog product ID;
- preserve canonical names;
- map only legacy classified type;
- do not infer brand/spec/category from canonical names during migration;
- do not collapse separate old IDs even when names/structured candidates look similar;
- UNCLASSIFIED remains absence of catalog identity.

Finding: gives CP22 a deterministic fail-closed migration target.

## 5. Measurement and unit review

Two different concepts are kept separate:

1. product package specification: exact physical/count facts that can identify a packaged SKU;
2. purchase form: how one observation was sold, including package-form labels such as 봉/상자.

Exact physical canonicalization kg<->g and L<->mL is mathematically safe. No conversion between package forms is defined.

Finding: avoids the CP20 unit-deception risk.

## 6. Alias-context review

Current V1 alias keys are global. CP20 found merchant collision risk.

CP21 introduces only alias namespace context (`GLOBAL` or `MERCHANT(key)`) and does not yet alter resolver behavior.

Finding: fixes the semantic gap without prematurely changing production auto-link rules.

## 7. Provenance/automation review

Risk: a high-confidence parser result could be mistaken for confirmed knowledge.

CP21 separates source, confidence and confirmation. A high-confidence parsed value remains `UNCONFIRMED` unless an explicit confirmation mechanism changes the state.

Finding: compatible with existing conservative exact-confirmed-alias philosophy.

## 8. Price-history review

CP21 does not replace current `PriceHistoryService`, change eligibility, or create an observation truth table. `PurchaseObservationV2` is a logical projection contract only.

Finding: current receipt-derived price-truth invariant remains intact.

Potential downstream hazard: CP27 must still define one canonical comparable-observation layer; CP21 intentionally does not duplicate that responsibility.

## 9. Category review

Category is represented only as an optional stable reference. No hierarchy/taxonomy is frozen and category cannot affect identity equality.

Finding: compatible with CP25 ownership and prevents category leakage into product merge authority.

## 10. UX review

No screen or navigation behavior changes in CP21. New domain code is not wired to user flow.

Finding: no premature UI/domain coupling and no loss of existing debug/evidence surfaces.

## 11. Privacy/security review

CP21 requires no new permission, network capability, file access, external catalog, user account, or real receipt fixture.

Workflow must retain the forbidden packaged-permission audit.

Finding: existing offline/private posture is unchanged.

## 12. Performance review

CP21 adds immutable value objects only and no runtime hot-path wiring. No speculative indexing/cache/optimization is introduced.

Finding: correct scope. Index/search performance remains CP22/CP29 work.

## 13. Test/evidence review

Required deterministic vectors cover:

- legacy mapping and ID preservation;
- UNCLASSIFIED rejection;
- stable-ID equality;
- confidence/confirmation independence;
- merchant alias namespace separation;
- exact unit canonicalization;
- pack-count distinction;
- commodity mixed-form preservation;
- observation raw evidence/provenance retention.

Full existing tests + lint + assemble must still pass.

## 14. Contradiction matrix

| Question | Result |
|---|---|
| Changes meaning of existing stored product IDs? | No; preserves ID authority |
| Can structured fields silently merge products? | No |
| Can category prove product identity? | No |
| Can merchant scope rewrite store history? | No |
| Can kg/g or L/mL exact equivalence create fake produce normalization? | No; package measure only, raw purchase form separate |
| Can BAG/BOX be treated as comparable? | No CP21 comparison API exists |
| Does CP21 create duplicate price truth? | No |
| Does CP21 require schema migration now? | No |
| Does CP21 require network/new permissions? | No |
| Does CP21 force UI framework changes? | No |

## 15. Scope audit

Approved changed areas:

- new `com.receiptledger.v1.catalog/**` pure domain classes;
- new catalog-domain unit tests;
- app version metadata;
- CP21-specific workflow;
- CP21/status/handoff documentation.

Forbidden in this group:

- legacy `product/**` edits;
- persistence/schema edits;
- OCR/layout/item/validation behavior edits;
- Activities/UI edits;
- permissions/manifest changes;
- unrelated cleanup.

## 16. Conclusion

CP21 can proceed as an additive domain layer with deterministic tests. The design addresses the cheapest high-impact risks before CP22: identity poisoning, legacy migration collapse, merchant alias collision, fake unit normalization, and confidence/confirmation conflation.
