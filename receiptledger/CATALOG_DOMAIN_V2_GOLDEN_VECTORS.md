# ReceiptLedger V1 — CP21 Catalog Domain V2 Golden Vectors

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_CATALOG_DOMAIN_V2_01`

These vectors define deterministic domain behavior. They are intentionally storage-independent.

## G01 — legacy STANDARD preservation

Input legacy product:

- id = `p-legacy-1`
- type = `STANDARD`
- canonical name = `서울우유 나100% 1L`

Expected V2:

- same ID
- `STANDARD_PRODUCT`
- same canonical name
- record origin `LEGACY_V1`
- no invented brand/product/specification/category fields

## G02 — legacy NON_STANDARD preservation

Input legacy product `감자` with type `NON_STANDARD`.

Expected V2:

- same ID/name
- `NON_STANDARD_COMMODITY`
- no sales unit invented at catalog level

## G03 — UNCLASSIFIED fail closed

Attempt to map legacy `UNCLASSIFIED` into a V2 catalog kind.

Expected: reject; unresolved is not a catalog entity.

## G04 — stable-ID authority

Two native STANDARD entries have identical canonical/structured fields but IDs `A` and `B`.

Expected: entities are not equal. No semantic auto-merge occurs in CP21.

## G05 — category non-authority

Category changes on the same catalog ID.

Expected: catalog entity identity remains the same stable ID; category is browse metadata.

## G06 — confidence is not confirmation

Field source `PARSED_FROM_RECEIPT`, confidence `HIGH`, confirmation `UNCONFIRMED`.

Expected: `isConfirmed()` is false.

## G07 — merchant alias namespace isolation

Contexts:

- `MERCHANT("STORE-A")`
- `MERCHANT("STORE-B")`
- `GLOBAL`

Expected: all are distinct namespaces. Merchant context rejects empty key.

## G08 — exact package-weight equivalence

- `1 kg`
- `1000 g`

Expected canonical physical measure equivalence.

## G09 — exact package-volume equivalence

- `1 L`
- `1000 mL`

Expected canonical physical measure equivalence.

## G10 — pack-count distinction

Specifications identical except pack count 5 vs 10.

Expected deterministic specification tokens differ.

Missing pack count and explicit pack count 1 also remain distinguishable.

## G11 — mixed commodity purchase forms

Commodity `감자` receives forms:

- `1 BAG / "봉"`
- `1 KILOGRAM / "kg"`
- `5 EACH / "개"`
- `1 BOX / "상자"`

Expected: raw labels and normalized codes are retained independently. No CP21 cross-form comparison result is generated.

## G12 — observation provenance

A purchase observation linked to a catalog ID includes raw printed name, store/date, purchase form evidence, numeric `ValueOrigin`, link source and receipt validation.

Expected: all survive construction unchanged; CP21 performs no average/median/judgment computation.

## G13 — commodity boundary

Native commodity creation does not accept STANDARD brand/product/specification fields through its factory.

Expected: commodity identity is canonical commodity name + stable ID, with per-observation purchase forms.

## G14 — package-form measure rejection

Attempt to create `PackageMeasure(1, BAG)`.

Expected: reject. BAG is a sales form, not an exact physical/count net-content measure.

## G15 — unknown is not default one

Unknown/missing pack count remains absent.

Expected: no automatic substitution with `1`.

These vectors are implemented in `CatalogDomainV2Test` and must remain stable through CP22 unless an explicit canonical amendment changes CP21 semantics.
