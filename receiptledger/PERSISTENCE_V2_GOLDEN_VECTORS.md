# ReceiptLedger V1 — CP22 Persistence V2 Golden Vectors

Updated: 2026-10-16 KST
Checkpoint: `RL_V1_PERSISTENCE_V2_01`

## PV2-G01 Legacy product preservation

Given V1 products `p-standard` and `p-commodity`, migration preserves exact ID/type/canonical_name/canonical_key/created_at_ms and sets `record_origin=LEGACY_V1`.

## PV2-G02 Legacy aliases become GLOBAL

Given V1 alias `서울우유1000 -> p-standard`, migration yields exactly one alias row with:

- scope GLOBAL
- merchant key empty
- exact old alias key
- exact raw alias
- same product ID.

## PV2-G03 Item links preserved

Given links with USER_CONFIRMED / EXACT_ALIAS sources, all `(receipt_id,item_ordinal,product_id,link_source)` tuples survive unchanged.

## PV2-G04 No semantic guessing

Migrated products have no catalog_fields, product_specifications, category_refs or observation_purchase_forms solely because of migration.

## PV2-G05 Merchant namespace coexistence

The same normalized alias key may coexist under MERCHANT A and MERCHANT B and may target different products without collision.

## PV2-G06 Same-context alias collision rejected

Within one `(scope,merchant_key,alias_key)` namespace, a second product target cannot replace the first silently.

## PV2-G07 STANDARD field persistence shape

BRAND/PRODUCT_NAME/VARIANT rows retain value, normalized lookup key, source, confidence and confirmation independently.

## PV2-G08 Product specification exact decimal storage

`1 L`, `1000 mL`, pack count and inner content are stored as exact decimal text + unit enum, not binary floating point.

## PV2-G09 Commodity purchase-form storage

A linked commodity observation may persist `1 BAG 봉`, `1 KILOGRAM kg`, `5 EACH 개`, or `1 BOX 상자` without any conversion/comparability field.

## PV2-G10 No duplicate price truth

`observation_purchase_forms` contains no unit_price, line_amount, store_name, purchase_date or copied receipt validation columns.

## PV2-G11 Cascade within catalog DB

Removing an item link removes its purchase-form overlay. Removing a product cascades its aliases, semantic fields/spec/category, item links and dependent purchase forms.

## PV2-G12 Fresh V2 schema

A clean install creates the same target table/index structure as a migrated V1 database.

## PV2-G13 Receipt DB untouched

`ReceiptSchema.VERSION` remains 1 and receipt persistence source is unchanged.

## PV2-G14 Unsupported migration fails closed

Any migration path other than explicit 1 -> 2 is rejected.

## PV2-G15 Legacy exact alias compatibility

Current resolver/confirm behavior continues to use GLOBAL context only; merchant-scoped rows cannot be accidentally returned by the legacy global lookup.
