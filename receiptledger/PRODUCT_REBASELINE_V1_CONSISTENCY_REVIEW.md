# ReceiptLedger V1 — Product Rebaseline Consistency Review

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRODUCT_REBASELINE_01`
Companion spec: `PRODUCT_REBASELINE_V1_MASTER_SPEC.md`

## 0. Review objective

This review tests the proposed product rebaseline against the completed ReceiptLedger V1 vertical slice before any V2 implementation begins. The goal is to find cheap-to-fix contradictions now rather than after schema/UI work starts.

Review rule: be rigorous where a new decision can invalidate a prior contract; do not re-audit unrelated proven behavior.

## 1. Executive result

**Result: COMPATIBLE WITH CONTROLLED EXTENSION.**

The rebaseline does not require discarding the existing OCR, receipt, validation, persistence, archive, review, product-identity, or price-history cores. It changes the product center of gravity from receipt processing to personal purchase-price memory and identifies extensions needed to make the existing vertical slice useful as a real product.

No production source/schema/runtime change is authorized by CP20.

## 2. Cross-check matrix

| Existing area | CP20 direction | Result | Required guardrail |
|---|---|---|---|
| Image intake/document correction | Preserve | Compatible | Keep permission/privacy and source-coordinate contracts |
| OCR/layout/structure/item extraction | Preserve + later semantic parsing above it | Compatible | Never overwrite raw OCR/item evidence |
| Arithmetic validation | Preserve | Compatible | Price insights must consume only eligible validated observations |
| Review/edit | Extend toward uncertainty-focused review | Compatible | Preserve user-edit provenance and revalidation |
| Receipt persistence/archive | Preserve | Compatible | Migration must not orphan receipt/image/link identity |
| Merchant/store | Extend for alias context/store comparisons | Compatible | Merchant context must not silently rewrite historical store data |
| STANDARD identity | Enrich with brand/specification/category | Compatible extension | SKU-significant specification differences remain distinct |
| NON_STANDARD identity | Enrich with explicit sales form/unit | Compatible extension | No guessed cross-unit normalization |
| UNCLASSIFIED | Keep as unresolved state | Compatible | Do not persist fake canonical products merely to clear review |
| Exact confirmed aliases | Preserve | Compatible | Future fuzzy/semantic matching may suggest, not silently merge |
| Global alias key | Extend/rework | Gap found | Add merchant/context scoping or collision-safe equivalent |
| Derived price history | Preserve | Compatible | Avoid duplicate independent price truth |
| Current latest/min/max/avg | Extend | Compatible | New statistics require exact eligibility/data sufficiency contracts |
| Prototype MainActivity | Replace incrementally in normal UX | Compatible | Keep debug/evidence path until replacement is proven |
| Prototype PriceHistory UI | Replace | Compatible | Preserve service behavior until Price Intelligence V2 supersedes it |
| API36/privacy firewall | Preserve | Compatible | No network/broad media permission introduced by product work |

## 3. Domain consistency review

### 3.1 STANDARD

Existing meaning: repeatable packaged product whose price history can be compared as the same product.

CP20 meaning: unchanged in essence, but identity becomes structured (brand/product/variant/specification/pack/category).

**Finding:** no semantic contradiction. V2 is a refinement of what “same product” means.

**Risk:** if V2 migration derives structured fields from old canonical names and auto-merges based on imperfect parsing, previously separate products could be collapsed.

**Constraint for CP21/CP22:** structured-field extraction from legacy names must never itself authorize merge. Existing product IDs remain distinct unless an explicit safe migration rule proves equivalence.

### 3.2 NON_STANDARD

Existing meaning: user-defined item identity; retain observations without automatic unit conversion.

CP20 meaning: same identity concept, with explicit raw sales form/unit and mixed-form display.

**Finding:** directly compatible.

**Risk:** later UX might accidentally compute aggregate trend over incomparable forms.

**Constraint:** comparison eligibility must be separate from grouping eligibility.

### 3.3 UNCLASSIFIED

Existing meaning: no product link yet; not persisted as product row.

CP20 meaning: unresolved state pending sufficient evidence/user confirmation.

**Finding:** exact alignment.

## 4. Data-model consistency review

### Current proven boundaries

- Receipt records are canonical purchase evidence.
- Product catalog is separate from receipt DB.
- Item links connect receipt item ordinals to catalog products.
- Price history is derived from receipts + links.

### CP20 impact

Future schema needs brand/specification/category/sales-unit/merchant-scoped alias metadata.

**Finding:** extension is feasible without changing the source-of-truth principle.

### Main migration hazards

1. product IDs accidentally regenerated;
2. aliases collide after scope changes;
3. item links orphaned;
4. old NON_STANDARD entries assigned invented units;
5. inferred structured fields treated as user-confirmed truth;
6. receipt DB and catalog DB migrations become non-atomic and diverge.

**Required CP22 design condition:** define migration phases, rollback/fail-closed behavior, legacy-row mapping, and regression fixtures before schema write code.

## 5. Identity-resolution consistency review

Existing safe behavior allows only confirmed exact normalized alias reuse.

CP20 adds semantic parsing/candidate ranking/merchant context.

**Finding:** candidate ranking is compatible only if authority levels are explicit.

Recommended authority ladder for later formalization:

1. exact confirmed merchant-scoped alias — strongest reusable evidence;
2. exact confirmed global alias where collision-safe;
3. exact structured canonical match with compatible specification;
4. semantic/fuzzy candidate — suggestion only;
5. unresolved.

CP20 does not freeze auto-link thresholds; CP24 must prove them.

## 6. Price-intelligence consistency review

Current service derives eligible observations only from validated receipts and computes STANDARD latest/min/max/average.

CP20 proposes previous-price deltas, medians, period metrics, store-aware metrics and price judgments.

**Finding:** compatible if all metrics share one explicit observation-eligibility layer.

Potential contradiction to avoid:

- one screen using unitPrice;
- another using lineAmount;
- another silently including invalid receipts;
- another applying package-size normalization.

**Constraint for CP27:** define a single canonical `ComparableObservation` contract or equivalent before adding metrics.

## 7. UX consistency review

Current screens expose developer controls and diagnostic text. CP20 proposes product-centric home/search/history and automatic receipt processing.

**Finding:** no domain contradiction; this is an information-architecture replacement.

**Risk:** deleting current controls early would remove useful evidence paths while the new flow is unproven.

**Constraint:** migrate incrementally. Hide/retire prototype surfaces from normal UX only after equivalent functionality/evidence exists.

## 8. Privacy/security consistency review

Product-centric features proposed by CP20 do not inherently require network access, broad photo permission, account data, or cloud services.

**Finding:** existing offline/private posture remains compatible.

**Constraints:**

- category/search/price intelligence should remain local for V1 unless separately approved;
- merchant-scoped aliases are local metadata, not a reason to add network access;
- real personal receipts remain forbidden in the public repository/CI.

## 9. Performance consistency review

Expected future scale grows from a small prototype to potentially thousands of receipts and many thousands of item observations.

New hot paths:

- alias lookup;
- category filtering;
- product search;
- price-history aggregation;
- chart dataset loading;
- migration.

**Finding:** no current performance contradiction, but schema/index choices in CP22 must anticipate search/history scale. Do not prematurely optimize OCR or unrelated subsystems in CP20/CP21.

## 10. Test/evidence consistency review

Current project closes groups with ReceiptLedger-scoped CI and exact evidence.

Future model changes need additional deterministic tests:

- legacy migration fixtures;
- identity collision cases;
- merchant alias separation;
- specification-distinct products;
- NON_STANDARD mixed-unit grouping without false comparison;
- sparse-history price judgment;
- invalid-receipt exclusion across all metrics.

**Finding:** existing discipline is sufficient; new semantic vectors are needed as the domain expands.

## 11. Scope review — what must NOT enter early checkpoints

The following are specifically deferred because they distract from the price-memory core or create premature architecture cost:

- household budgeting/accounting ledger
- bank/card synchronization
- cloud account/sync
- online retail price scraping
- coupon/loyalty integrations
- social sharing
- product-image recognition as identity authority
- barcode/global product database integration
- AI/cloud inference dependency
- forced unit conversion for produce
- release signing/store publishing

These may be reconsidered later only if they directly improve the validated core loop.

## 12. Dependency review of CP21–CP36

### Must remain ordered

- CP21 Domain V2 before CP22 Persistence V2.
- CP22 persistence before production resolvers depend on new stored fields.
- CP23 semantic parsing before CP24 resolver can use those semantics.
- CP27 exact price statistics before CP28 user-facing price judgment.
- CP29 search/browse data access before product-centric shell depends on it.

### Can partially overlap only after contracts freeze

- CP25 Category and CP26 Commodity can be developed independently after CP21/22 if their shared schema is frozen.
- CP30 Product Detail and CP31 Commodity Detail can share visual infrastructure but must retain different comparability semantics.
- CP33 Design System can begin conceptually earlier, but implementation should not block domain correctness and should not force domain rewrites.

### Should remain later

- CP35 real-receipt evaluation after enough end-to-end V2 flow exists to measure meaningful registration correctness.
- CP36 performance/reliability after representative data paths exist, while micro-regressions should still be caught earlier where cheap.

## 13. Decisions frozen by this review

1. Do not rewrite the validated OCR/receipt engine for the product rebaseline.
2. Preserve STANDARD/NON_STANDARD/UNCLASSIFIED, but enrich their data model.
3. Separate grouping eligibility from comparison eligibility for non-standard goods.
4. Preserve receipt-derived price truth.
5. Treat semantic/fuzzy matching as candidate evidence, not silent merge authority by default.
6. Add merchant-context capability to future alias design.
7. Freeze V2 domain before persistence migration.
8. Preserve debug/evidence surfaces until replacement UX proves parity.
9. Keep V1 offline/private unless separately authorized.
10. Evaluate each checkpoint for domain/data/UX/privacy/performance/test impact, but do not re-run irrelevant audits.

## 14. CP20 review conclusion

No blocking contradiction was found between the completed V1 foundation and the product-centric rebaseline.

The correct strategy is **controlled extension with migration safeguards**, not restart/rewrite.

The first implementation-bearing successor remains CP21 — Catalog Domain V2, but CP21 must begin as a contract/specification checkpoint before any persistence or UI code is changed.
