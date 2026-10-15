# ReceiptLedger V1 — Product Rebaseline / Master Specification

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PRODUCT_REBASELINE_01`
Branch: `receiptledger/run-v1-product-rebaseline-20261016`

## 0. Purpose

ReceiptLedger is not primarily a receipt archive. Its product purpose is:

> Turn personal receipt purchases into a trustworthy memory of what the user actually paid, so the user can quickly judge whether a current price is cheap, normal, or expensive relative to their own past purchases.

The receipt is an input and evidence source. The primary user-facing objects are repeat-purchase products, non-standard commodities/items, their purchase observations, and price history.

This checkpoint is a planning/rebaseline checkpoint only. It changes no production source, database schema, OCR behavior, or Android runtime behavior.

## 1. Product principles

1. **Price-memory first.** Every major feature must improve reliable recall or comparison of personal purchase prices.
2. **Evidence before automation.** Automatic classification must never silently invent a product identity, quantity, unit, or price when the receipt evidence is ambiguous.
3. **Preserve provenance.** Printed, inferred, user-corrected, and learned values must remain distinguishable.
4. **Fail closed on identity.** A wrong product merge poisons future price history; uncertain identities must remain unresolved or require confirmation.
5. **Repeat use should get easier.** User-confirmed aliases, product identities, categories, and merchant-specific knowledge should reduce future review effort without lowering correctness.
6. **Do not force incomparable data into a fake common unit.** Non-standard goods may be grouped under one commodity while retaining 봉/팩/단/상자/kg/개 etc. exactly as observed.
7. **Derived price history remains traceable to saved receipts.** Do not create an untraceable duplicate truth source for purchase prices.
8. **Commercial UX hides implementation detail.** OCR pass diagnostics and development controls are evidence/debug concerns, not the normal user experience.
9. **Offline/private by default remains a core invariant.** The current no-network/no-broad-media-permission posture is preserved unless separately authorized.
10. **Optimize for the essential loop, not feature breadth.** Do not add unrelated budgeting, banking, cloud, social, coupon, or online-commerce scope unless separately approved.

## 2. Primary user loop

Target V1 user loop:

1. User captures or selects a receipt.
2. ReceiptLedger automatically detects/corrects the document, runs OCR, reconstructs rows, extracts merchant/date/items/quantities/prices, and validates arithmetic.
3. Each purchase line is resolved into one of:
   - a known repeatable packaged product,
   - a known non-standard commodity/item,
   - an unresolved candidate requiring review.
4. The app auto-reuses only sufficiently safe prior knowledge.
5. The user reviews only uncertain or contradictory fields/links.
6. The receipt is saved with source image, structured purchase facts, provenance, validation state, and product/item links.
7. The user later finds a product or commodity by search/category/recent/frequent paths.
8. The app shows historical prices and an evidence-based price judgment.

The desired interaction is eventually closer to:

`영수증 추가 -> 자동 처리 -> "12개 항목 중 2개만 확인" -> 저장`

not a sequence of manual OCR/debug actions.

## 3. Canonical domain model direction

### 3.1 Repeatable packaged product (`STANDARD`)

A STANDARD product is a repeatable manufactured/packaged product for which observations are intended to be directly comparable as the same product/package.

Identity should be decomposable into fields such as:

- brand
- product/family name
- variant/flavor/model when identity-significant
- net quantity
- quantity unit
- pack count / bundle structure
- category
- canonical display name
- merchant/POS aliases

Examples:

- 서울우유 나100% 1L
- 신라면 5입
- 비비고 왕교자 1.05kg

Identity rule: brand/product/variant/specification/bundle differences that can change the commercial SKU must not be casually collapsed.

### 3.2 Non-standard commodity/item (`NON_STANDARD`)

A NON_STANDARD identity groups semantically equivalent loose or variably packaged goods without asserting cross-unit comparability.

Example canonical commodity: `감자`

Possible observations under the same commodity:

- 1봉 / 3,980원
- 1kg / 5,900원
- 5개 / 4,500원
- 1상자 / 18,900원

All belong under `감자`, but their raw sales form must remain visible. Cross-unit normalization is permitted only when the receipt explicitly provides enough quantity/weight information and a later checkpoint defines a safe conversion rule. No guessed conversion.

### 3.3 `UNCLASSIFIED`

UNCLASSIFIED remains a transient unresolved state, not a canonical product identity. It exists when the system lacks enough confidence/evidence to link or create a product/item safely.

### 3.4 Purchase observation

A purchase observation represents one historical purchase fact derived from a saved receipt item plus its receipt context.

Expected logical fields include:

- receipt ID / item ordinal
- resolved product or commodity ID
- raw printed item name
- normalized/parsed semantic fields
- purchase date
- store/merchant
- quantity
- sales unit
- unit price when valid
- line amount
- discount context where applicable
- provenance for each derived field
- validation eligibility

The current architectural invariant remains: observations should be derived from canonical persisted receipt records + links where practical, rather than copied into an independent stale truth table.

## 4. Product identity policy

### 4.1 Preserve the existing safe core

The existing conservative policy remains foundational:

- never overwrite the raw receipt item name;
- exact previously confirmed aliases may auto-link;
- fuzzy similarity must not silently merge products;
- ambiguity/conflict fails closed;
- user confirmation may create reusable identity knowledge.

### 4.2 Extend identity resolution in V2

Future Identity Resolver V2 should separate:

1. raw OCR/POS text normalization;
2. merchant-scoped alias lookup;
3. semantic parsing (brand/product/specification/unit/pack);
4. candidate retrieval;
5. confidence/reason output;
6. deterministic safe auto-link threshold;
7. user confirmation for ambiguous cases;
8. learning from confirmed decisions.

A fuzzy/string/semantic score may be used to **rank suggestions**, but not as sufficient authority for silent product merge unless a later explicitly validated contract defines stronger evidence.

### 4.3 Merchant-scoped aliases

Global exact aliases are useful but insufficient because POS abbreviations can be merchant-specific. Future catalog design should support merchant/store scope or equivalent context so the same short token is not assumed globally unique.

## 5. Category model

Category taxonomy is a new product feature; it was intentionally absent from Product Identity Core.

Requirements:

- hierarchical browse path where useful;
- stable canonical category IDs separate from display labels;
- product/commodity category assignment;
- automatic suggestion for new identities;
- user correction;
- reuse of confirmed category on future observations of the same identity;
- category must not be inferred as a new product identity signal unless its reliability is separately validated.

Initial example hierarchy (illustrative, not frozen taxonomy):

- 식품
  - 유제품
    - 우유
    - 요구르트
    - 치즈
  - 면류
  - 냉동식품
  - 농산물
    - 채소/서류
    - 과일
    - 곡류
- 생활
  - 세제
  - 화장지
  - 위생용품

The exact taxonomy belongs in a dedicated checkpoint; CP20 freezes only the need and governing principles.

## 6. Price intelligence contract

### 6.1 STANDARD products

Desired metrics, subject to later exact statistical contracts:

- latest purchase price
- previous purchase price
- absolute and percentage change vs previous
- recent N-purchase mean
- recent N-purchase median
- period mean/median
- historical minimum / maximum
- same-store history
- all-store history
- observation count and date range

### 6.2 NON_STANDARD commodities

Default behavior:

- show all raw observations together;
- preserve sales unit/form;
- allow filtering by unit/form;
- compare like-with-like when the same unit is present;
- do not claim cross-unit normalized price without explicit quantity/weight evidence and an approved normalization rule.

### 6.3 Price judgment

Future user-facing judgment may use labels such as:

- 매우 저렴
- 평소보다 저렴
- 평소 수준
- 평소보다 비쌈
- 매우 비쌈
- 데이터 부족

But the label must be generated from an explicit, testable statistical policy. It must expose enough context to avoid false precision, e.g. `최근 5회 중앙값보다 6.8% 높음`. Sparse history must yield `데이터 부족`, not a confident label.

### 6.4 Invalid data

Current invariant remains:

- `MISMATCH` / `INCOMPLETE` receipts are excluded from normal comparable price history;
- contradictions are not silently repaired;
- inferred prices remain provenance-marked.

## 7. Search and browse requirements

The product-centric application needs search/browse across:

- brand
- canonical product name
- aliases where safe
- specification
- category
- commodity name
- store/merchant

Primary discovery modes:

- global search
- categories
- recent purchases
- frequent purchases
- recent price changes
- product/commodity detail
- receipt history as supporting evidence

Search must prioritize canonical identity over raw OCR noise while still allowing traceability to source receipts.

## 8. UX / information architecture direction

### 8.1 Home

The future home is product-centric, not an OCR harness. Likely top-level content:

- global product/item search
- add receipt CTA
- frequent/recent products
- recent notable price changes
- categories
- recent receipts

### 8.2 Product detail (`STANDARD`)

Must eventually support:

- canonical product identity/specification
- recent/previous price
- comparison summary
- price trend chart
- min/max/mean/median as approved
- store-aware history
- chronological purchase list
- links back to source receipt records

### 8.3 Commodity detail (`NON_STANDARD`)

Must show mixed raw purchase forms without misleading aggregate claims. Unit/form filters and same-unit comparisons are desirable.

### 8.4 Receipt intake/review

Normal users should not need to manage OCR passes, document transforms, or debug diagnostics. The target is automatic processing with uncertainty-focused review.

Current diagnostic controls/text remain valuable as development evidence until replacement UX is validated; do not delete them prematurely.

## 9. UI technology direction

The validated OCR/domain engine should not be rewritten merely to modernize appearance.

Preferred migration principle:

- preserve tested core/domain logic;
- define a product-centric navigation/information architecture;
- build new commercial screens in a modern UI layer;
- migrate/replace prototype screens incrementally;
- keep debug/evidence surfaces available behind non-primary paths as needed during validation.

The exact View vs Compose implementation decision belongs to a later UI architecture checkpoint. CP20 does not authorize a framework rewrite.

## 10. Persistence direction

Current storage is a proven direct-SQLite implementation with separate receipt and product catalog databases. Do not migrate persistence before the V2 domain schema is frozen.

Future persistence work must cover:

- schema versioning/migration from existing data;
- product specification fields;
- commodity/sales-unit representation;
- categories;
- merchant-scoped aliases or equivalent context;
- indexes for search/history;
- preservation of receipt/product-link traceability;
- migration regression tests;
- no silent identity collapse during migration.

Room may be considered in the persistence-design checkpoint, but CP20 does not mandate it.

## 11. Existing assets: keep / extend / redesign / retire

### KEEP as core invariants

- external-camera intake without app CAMERA permission
- system picker without broad storage/media permission
- EXIF normalization / bounded bitmap decode
- receipt quad detection / perspective correction
- local bundled Korean OCR
- source-coordinate preservation
- geometry-based layout reconstruction
- structure/item extraction with provenance
- arithmetic validation
- bounded OCR recovery / conservative cross-pass merge
- required human review before persistence
- app-private receipt/image storage
- receipt list/detail/delete
- conservative identity linking
- invalid-receipt exclusion from comparable history
- API 36 / lint / permission firewall

### EXTEND

- merchant/store semantics
- product identity
- aliases
- review/edit
- price-history derivation
- receipt/product linking

### REDESIGN significantly

- catalog domain model
- catalog persistence schema
- identity resolver orchestration
- price comparison/statistics
- app navigation/information architecture
- product/category/history presentation

### CREATE NEW

- brand/specification parsing
- category taxonomy/system
- merchant-scoped alias context
- semantic candidate resolver
- commodity/sales-unit model
- search/indexing
- price judgment policy
- product detail / commodity detail
- charts
- commercial design system
- product-centric home
- production-oriented intake/review UX

### RETIRE/HIDE from normal UX only after replacement is validated

- developer-facing OCR pass text
- manual debug-oriented processing controls
- raw validation diagnostics in normal user flow
- prototype product buttons/TextView history surfaces

Do not delete tested internals merely because the final UI hides them.

## 12. Consistency / contradiction review

### Compatible with prior contracts

- STANDARD/NON_STANDARD/UNCLASSIFIED remains semantically useful.
- Existing exact confirmed alias auto-link remains a safe base.
- Price history derived from receipt records remains correct and desirable.
- User review/provenance remains required.
- MISMATCH/INCOMPLETE exclusion remains correct.
- privacy/offline/public-repo firewall remains unaffected.

### Known gaps, not contradictions

- current `CatalogProduct` lacks brand/specification/category fields;
- current alias key is effectively global and lacks merchant context;
- NON_STANDARD currently has no explicit sales-unit model;
- current price history has no charts, category browsing, search, median, period metrics, or price judgment;
- current Main/PriceHistory UI is development/prototype quality.

These are planned extensions/replacements, not evidence that prior checkpoints were wrong.

### Risks to guard against in later checkpoints

1. **Identity poisoning:** over-aggressive fuzzy auto-link corrupts all future history.
2. **Unit deception:** comparing 봉/상자/kg as though directly normalized.
3. **Schema migration loss:** old links/receipts orphaned or silently remapped.
4. **Category leakage:** treating category similarity as product identity proof.
5. **Store alias collision:** global POS abbreviations resolving differently across merchants.
6. **Duplicate truth:** new price tables diverging from canonical receipt data.
7. **UI-first rewrite:** replacing tested domain/OCR code for visual reasons.
8. **Scope creep:** budgeting, banking, cloud sync, online price scraping, loyalty/coupons added before core price-memory loop is complete.
9. **False confidence:** price judgments on insufficient history.
10. **Automation friction inversion:** forcing confirmation for already proven identities, defeating repeat-use efficiency.

## 13. Canonical checkpoint roadmap

The following order is dependency-oriented. A checkpoint may be split if implementation cost is larger than expected, but dependency order should not be skipped casually.

### CP20 — Product Rebaseline / V1 Master Specification
This document set. Planning only.

### CP21 — Catalog Domain V2
Freeze detailed data contracts for Product, Commodity, Specification, SalesUnit, Category, Alias context, PurchaseObservation and compatibility with existing types.

### CP22 — Persistence V2
Implement migration-safe persistence/indexing for the frozen CP21 model. Decide direct SQLite vs Room migration here, not earlier.

### CP23 — Receipt Product Semantics
Parse brand/product/variant/specification/pack/sales-unit candidates from receipt item text while preserving raw source/provenance.

### CP24 — Identity Resolver V2
Merchant-aware aliases, deterministic candidate ranking, safe auto-link contract, ambiguous review, confirmed-decision reuse.

### CP25 — Category System
Taxonomy, persistence, assignment, automatic suggestions, user correction/reuse.

### CP26 — Commodity / Non-standard V2
Explicit raw sales-unit/form handling and one-commodity/multiple-form history.

### CP27 — Price Intelligence V2
Exact statistics and comparable-history rules for STANDARD + like-unit NON_STANDARD views.

### CP28 — Price Evaluation
Explicit data-sufficiency thresholds and user-facing cheap/normal/expensive judgment rules.

### CP29 — Search / Browse
Global search, categories, recents/frequents, filters/sorting/index performance.

### CP30 — Product Detail
Commercial STANDARD price-history/insight screen.

### CP31 — Commodity Detail
Commercial NON_STANDARD mixed-form history screen.

### CP32 — Capture / Review UX V2
Collapse prototype/manual processing into automatic processing + uncertainty-focused review while retaining evidence/debug access.

### CP33 — Design System
Typography, color, spacing, shape, iconography, chart, component and state system.

### CP34 — Commercial UI Shell
Product-centric home/navigation/search/category/receipt/settings integration. Incremental UI migration; no gratuitous domain rewrite.

### CP35 — Real Receipt Evaluation
Use only synthetic/public-safe or explicitly approved sanitized fixtures. Measure end-to-end purchase-registration correctness, not OCR character accuracy alone.

### CP36 — Performance / Reliability
Startup, OCR latency, bitmap memory, large history/search, migration, failure recovery, stability.

### Later release work
Backup/export/restore, private release signing, long-run device use, accessibility/polish, release packaging only after explicit authorization.

## 14. Checkpoint discipline for all future groups

Every future group must:

1. re-read current canonical status/handoff and relevant prior contracts;
2. state the checkpoint essence and explicit non-goals before implementation;
3. inspect upstream/downstream compatibility before changing schemas/contracts;
4. identify contradiction risks from at least domain/data/UX/privacy/performance/test perspectives as relevant;
5. prefer the smallest change that proves the checkpoint goal;
6. preserve evidence and deterministic regression tests;
7. run ReceiptLedger-scoped CI only;
8. close with exact branch/HEAD/run/evidence;
9. synchronize `PROJECT_STATUS_LATEST.md`, `SESSION_HANDOFF.md`, `README.md`, `WORK_UNIT.md`, and the checkpoint plan/master docs as needed;
10. stop before the next checkpoint unless explicitly authorized.

Review should be rigorous but bounded: do not repeat already-proven audits unless a new change can invalidate them.

## 15. CP20 acceptance

CP20 is complete when:

- product purpose is frozen around personal purchase-price memory;
- STANDARD/NON_STANDARD/UNCLASSIFIED semantics are reconciled with current implementation;
- future Product/Commodity/Observation directions are explicit;
- unsafe comparison/identity behaviors are prohibited;
- UX and automation target are explicit;
- existing assets are classified as keep/extend/redesign/create/retire;
- dependency-ordered CP21–CP36 roadmap is documented;
- known risks and non-goals are documented;
- no production code/schema/runtime behavior was changed;
- canonical status/handoff documents are synchronized.

## 16. CP20 non-goals

This checkpoint does **not** implement:

- Product Domain V2 classes/schema
- database migration
- fuzzy identity resolver
- category taxonomy
- commodity conversion
- new statistics
- search
- charts
- Compose migration
- UI redesign
- real-receipt fixtures
- cloud/network features
- release signing/publishing

Those belong to later explicitly authorized groups.
