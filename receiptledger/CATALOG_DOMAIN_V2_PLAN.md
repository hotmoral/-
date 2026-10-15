# ReceiptLedger V1 — CP21 Catalog Domain V2

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_CATALOG_DOMAIN_V2_01`
Branch: `receiptledger/run-v1-catalog-domain-v2-20261016`
Depends on: CP20 Product Rebaseline / V1 Master Specification

## 0. Objective

Freeze and implement the storage-independent Catalog Domain V2 contract before any V2 database migration, semantic parser, resolver expansion, category taxonomy, price-statistics expansion, or commercial UI work begins.

The checkpoint exists to make later persistence cheap and safe: meanings are fixed first, storage second.

## 1. Scope

CP21 defines and unit-tests:

- classified catalog kinds and legacy `ProductType` compatibility;
- stable catalog-entity identity rules;
- structured STANDARD product semantic fields;
- NON_STANDARD commodity boundary;
- package specification and exact physical measure semantics;
- raw purchase form / sales-unit representation;
- category references without freezing a taxonomy;
- global vs merchant-scoped alias context;
- field provenance, confidence and confirmation state;
- logical purchase-observation contract;
- legacy V1 catalog adaptation without semantic guessing;
- deterministic golden vectors for the above.

## 2. Explicit non-goals

CP21 MUST NOT:

- change `ProductCatalogSchema.VERSION` or any SQLite schema;
- migrate existing user data;
- modify the legacy `product/**` runtime behavior;
- parse brand/specification from receipt text;
- change exact-alias resolver authority;
- introduce fuzzy/semantic auto-linking;
- freeze category taxonomy;
- define price-comparison statistics or cheap/expensive thresholds;
- redesign Activities/navigation/UI;
- add network access, permissions, cloud, barcode, online catalog, budgeting, or unrelated scope.

Those remain dependency-ordered later checkpoints.

## 3. Catalog kinds and legacy compatibility

Canonical V2 classified kinds:

- `STANDARD_PRODUCT` — repeatable packaged/manufactured commercial identity.
- `NON_STANDARD_COMMODITY` — one semantic commodity/item that may have multiple raw purchase forms.

Legacy mapping is exact and one-way for classified rows:

- legacy `STANDARD` -> `STANDARD_PRODUCT`
- legacy `NON_STANDARD` -> `NON_STANDARD_COMMODITY`
- legacy `UNCLASSIFIED` -> no catalog entity; it remains unresolved and conversion is rejected.

No new V2 catalog row may represent `UNCLASSIFIED`.

## 4. Entity identity rule

The authoritative identity of a catalog entity is its stable catalog ID.

Consequences:

1. Two rows with different IDs are NOT automatically the same product even if every structured field currently matches.
2. Structured brand/name/specification similarity is candidate evidence for CP24, not authority to merge entities in CP21.
3. Category is never part of SKU identity.
4. Store/merchant is never part of SKU identity.
5. A STANDARD observation is directly the same historical product only when linked to the same catalog entity ID under an approved identity-link rule.
6. A NON_STANDARD observation belongs to the same commodity when linked to the same commodity ID; this grouping does not imply that unlike sales forms are price-comparable.

This rule prevents identity poisoning during migration and semantic parsing.

## 5. Catalog entry contract

`CatalogEntryV2` contains:

- stable `id`;
- `CatalogKind`;
- canonical display name + conservative normalized key;
- optional `CategoryRef`;
- creation timestamp;
- record origin: `NATIVE_V2` or `LEGACY_V1`;
- STANDARD-only semantic fields:
  - brand;
  - product/family name;
  - variant/model/flavor when relevant;
  - product specification.

For a native STANDARD entry, product/family name must be present. Brand, variant and specification may remain absent when evidence is incomplete; incompleteness reduces later automation authority rather than inventing values.

A COMMODITY has no STANDARD brand/product/specification fields. Its canonical name is the commodity identity, e.g. `감자`.

A legacy V1 entry is preserved with the same ID, legacy type mapping, canonical name and creation timestamp. CP21 deliberately does NOT parse its canonical name into brand/specification fields.

## 6. Field evidence contract

Structured semantic fields use `CatalogField<T>` with three independent dimensions:

### Source

- `RECEIPT_TEXT`
- `PARSED_FROM_RECEIPT`
- `USER_CONFIRMED`
- `CONFIRMED_KNOWLEDGE`
- `LEGACY_IMPORT`
- `UNKNOWN` only for an absent value

### Confidence

- `UNKNOWN`
- `LOW`
- `MEDIUM`
- `HIGH`

### Confirmation

- `UNCONFIRMED`
- `CONFIRMED`

Important rule: confidence and confirmation are independent. `HIGH` parsed confidence is still not user/knowledge confirmation and may not silently acquire identity authority.

This is intentionally separate from receipt arithmetic `ValueOrigin`; catalog semantics and receipt numeric provenance solve different problems.

## 7. Category reference

CP21 freezes only a stable category reference contract:

- non-empty stable category ID;
- category is descriptive/browse metadata;
- category does not participate in catalog entity equality or product merge authority.

Exact taxonomy, hierarchy, labels, suggestion rules and persistence belong to CP25.

## 8. Alias context

`AliasContext` supports:

- `GLOBAL` — a confirmed alias intentionally reusable without merchant restriction;
- `MERCHANT` — alias meaning is scoped to a normalized/opaque merchant key.

A merchant-scoped context requires a non-empty merchant key. Two identical POS strings under different merchant keys are distinct alias namespaces.

CP21 defines context only. Alias table migration and resolution precedence belong to CP22/CP24.

## 9. Product specification

`ProductSpecification` represents package identity facts, not a guessed purchase conversion.

Fields:

- optional total/net content (`PackageMeasure`);
- optional pack count;
- optional inner-unit content when explicitly known.

Rules:

- quantities are positive exact decimals (`BigDecimal`), never binary floating point;
- supported exact package measures are count, g/kg and mL/L;
- kg<->g and L<->mL canonicalization is exact physical equivalence and may be used for deterministic representation;
- inner-unit content requires an explicit pack count;
- absent means unknown/not represented and is not silently replaced by `1`;
- package-form words such as 봉/박스 are not valid physical net-content measures.

Examples:

- `1 kg` and `1000 g` are exactly the same package measure;
- `1 L` and `1000 mL` are exactly the same package measure;
- `5입` and `10입` are different pack specifications;
- missing pack count is not equal to explicit pack count `1` for inference purposes.

## 10. Sales unit and raw purchase form

`SalesUnitCode` deliberately separates exact physical units from package forms:

- exact count/measure: EACH, GRAM, KILOGRAM, MILLILITER, LITER;
- package forms: BAG, PACK, BOX, BUNDLE;
- OTHER, UNKNOWN.

`PurchaseForm` stores:

- positive exact quantity;
- normalized sales-unit code;
- raw unit label exactly as supplied to the domain object.

Example commodity `감자` may have observations:

- `1 + BAG + "봉"`
- `1 + KILOGRAM + "kg"`
- `5 + EACH + "개"`
- `1 + BOX + "상자"`

All may group under the same commodity ID. CP21 provides no API that claims BAG and BOX are comparable. Cross-unit comparability remains a CP27 concern and guessed conversion remains forbidden.

## 11. Purchase observation logical contract

`PurchaseObservationV2` is an immutable logical projection of one saved receipt item linked to one catalog entry. It does not become a second price truth store in CP21.

It carries:

- receipt ID + item ordinal;
- linked catalog entry ID;
- identity link source;
- raw receipt item name;
- purchase date and store context;
- creation timestamp;
- optional `CatalogField<PurchaseForm>`;
- quantity provenance compatible with current `ValueOrigin`;
- unit price + origin;
- line amount + origin;
- receipt validation status.

No CP21 method computes average, median, normalization, price judgment, or final comparability. Those remain CP27/CP28 responsibilities.

## 12. Legacy V1 compatibility

`LegacyCatalogAdapter` converts an existing `CatalogProduct` into a V2 domain view while preserving:

- exact product ID;
- STANDARD/NON_STANDARD meaning;
- canonical name;
- created timestamp.

It does NOT:

- parse brand from canonical name;
- infer size/pack count;
- assign a category;
- create merchant aliases;
- merge rows with similar names.

This is a critical migration guardrail for CP22.

## 13. Consistency constraints carried forward

- raw receipt item text is never overwritten;
- wrong merge is worse than unresolved;
- category similarity cannot prove identity;
- merchant context cannot rewrite historical store evidence;
- high confidence alone cannot equal confirmation;
- receipt validation/provenance remain intact;
- price truth remains derived from saved receipt records + links;
- NON_STANDARD grouping and price comparability remain separate concepts;
- existing V1 product IDs must survive migration unchanged;
- no public-repo privacy or permission invariant changes.

## 14. Acceptance criteria

CP21 is PASS only if:

1. new catalog domain code is storage-independent pure Java;
2. legacy product runtime/schema files are unchanged;
3. `ProductCatalogSchema.VERSION` remains 1;
4. STANDARD/NON_STANDARD legacy mapping is deterministic and UNCLASSIFIED conversion fails closed;
5. catalog equality is stable-ID based;
6. same semantic fields with different IDs remain distinct entities;
7. legacy adaptation preserves ID/name/type without semantic guessing;
8. global and merchant alias contexts cannot collide accidentally;
9. exact package measure normalization vectors pass;
10. different pack counts remain distinguishable;
11. commodity mixed raw forms remain preservable without fake comparison;
12. confidence vs confirmation distinction is tested;
13. purchase observation retains raw evidence/provenance/validation context;
14. existing complete unit suite still passes;
15. lint is 0 errors / 0 warnings;
16. debug APK builds and forbidden-permission audit remains clean;
17. diff from CP20 contains only CP21-approved domain/test/build/workflow/docs files;
18. canonical status/handoff documents are synchronized after the implementation boundary.

## 15. Downstream gate

After CP21 closes, CP22 may design/implement persistence only against this frozen domain meaning.

CP22 must not reinterpret:

- stable ID equality;
- legacy-row preservation;
- UNCLASSIFIED unresolved semantics;
- category non-authority;
- merchant alias scope;
- unknown != invented default;
- grouping != comparability.

Any change to these semantics requires an explicit canonical amendment before schema migration.
