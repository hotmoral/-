#!/usr/bin/env python3
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JAVA = ROOT / "harness/android-v1/app/src/main/java/com/receiptledger/v1"
SCHEMA = JAVA / "product/ProductCatalogSchema.java"
PLAN = JAVA / "product/ProductCatalogMigrationPlanV2.java"
RECEIPT_SCHEMA = JAVA / "persistence/ReceiptSchema.java"


def constant(path: Path, name: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"public static final String\s+" + re.escape(name) + r"\s*=\s*\"([^\"]*)\";", text)
    if not match:
        raise AssertionError(f"missing Java SQL constant {name} in {path}")
    return match.group(1).replace(r"\\", "\\").replace(r'\"', '"')


def int_constant(path: Path, name: str) -> int:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"public static final int\s+" + re.escape(name) + r"\s*=\s*(\d+)\s*;", text)
    if not match:
        raise AssertionError(f"missing Java int constant {name}")
    return int(match.group(1))


V1_PRODUCTS = "CREATE TABLE products (id TEXT PRIMARY KEY NOT NULL,type TEXT NOT NULL,canonical_name TEXT NOT NULL,canonical_key TEXT NOT NULL UNIQUE,created_at_ms INTEGER NOT NULL)"
V1_ALIASES = "CREATE TABLE aliases (alias_key TEXT PRIMARY KEY NOT NULL,raw_alias TEXT NOT NULL,product_id TEXT NOT NULL,FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)"
V1_LINKS = "CREATE TABLE item_links (receipt_id TEXT NOT NULL,item_ordinal INTEGER NOT NULL,product_id TEXT NOT NULL,link_source TEXT NOT NULL,PRIMARY KEY(receipt_id,item_ordinal),FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)"
V1_LINK_INDEX = "CREATE INDEX idx_item_links_product ON item_links(product_id)"

MIGRATION_NAMES = [
    "ADD_RECORD_ORIGIN",
    "RENAME_OLD_ALIASES",
    "CREATE_ALIASES_V2_TEMP",
    "COPY_ALIASES_AS_GLOBAL",
    "DROP_OLD_ALIASES",
    "RENAME_ALIASES_V2",
]
NEW_SCHEMA_NAMES = [
    "CREATE_ALIAS_PRODUCT_INDEX",
    "CREATE_CATALOG_FIELDS",
    "CREATE_PRODUCT_SPECIFICATIONS",
    "CREATE_CATEGORY_REFS",
    "CREATE_OBSERVATION_PURCHASE_FORMS",
    "CREATE_CATALOG_FIELD_LOOKUP_INDEX",
    "CREATE_CATEGORY_LOOKUP_INDEX",
]
FRESH_NAMES = [
    "CREATE_PRODUCTS",
    "CREATE_ALIASES",
    "CREATE_LINKS",
    "CREATE_CATALOG_FIELDS",
    "CREATE_PRODUCT_SPECIFICATIONS",
    "CREATE_CATEGORY_REFS",
    "CREATE_OBSERVATION_PURCHASE_FORMS",
    "CREATE_LINK_PRODUCT_INDEX",
    "CREATE_ALIAS_PRODUCT_INDEX",
    "CREATE_CATALOG_FIELD_LOOKUP_INDEX",
    "CREATE_CATEGORY_LOOKUP_INDEX",
]

assert int_constant(SCHEMA, "VERSION") == 2
assert int_constant(RECEIPT_SCHEMA, "VERSION") == 1
assert constant(SCHEMA, "DB_NAME") == "receipt-products-v1.db"

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys=ON")
for sql in (V1_PRODUCTS, V1_ALIASES, V1_LINKS, V1_LINK_INDEX):
    conn.execute(sql)

products = [
    ("p-standard", "STANDARD", "서울우유 나100% 1L", "서울우유 나100% 1L", 100),
    ("p-commodity", "NON_STANDARD", "감자", "감자", 200),
]
aliases = [
    ("서울우유1000", "서울우유1000", "p-standard"),
    ("감자", "감자", "p-commodity"),
]
links = [
    ("r-1", 0, "p-standard", "USER_CONFIRMED"),
    ("r-2", 3, "p-commodity", "EXACT_ALIAS"),
]
conn.executemany("INSERT INTO products VALUES (?,?,?,?,?)", products)
conn.executemany("INSERT INTO aliases VALUES (?,?,?)", aliases)
conn.executemany("INSERT INTO item_links VALUES (?,?,?,?)", links)
conn.commit()

for name in MIGRATION_NAMES:
    conn.execute(constant(PLAN, name))
for name in NEW_SCHEMA_NAMES:
    conn.execute(constant(SCHEMA, name))
conn.commit()

migrated_products = conn.execute(
    "SELECT id,type,canonical_name,canonical_key,created_at_ms,record_origin FROM products ORDER BY id"
).fetchall()
expected_products = sorted([row + ("LEGACY_V1",) for row in products])
assert migrated_products == expected_products, (migrated_products, expected_products)

migrated_aliases = conn.execute(
    "SELECT scope,merchant_key,alias_key,raw_alias,product_id FROM aliases ORDER BY alias_key"
).fetchall()
expected_aliases = sorted([("GLOBAL", "", a, raw, pid) for a, raw, pid in aliases], key=lambda r: r[2])
assert migrated_aliases == expected_aliases

migrated_links = conn.execute(
    "SELECT receipt_id,item_ordinal,product_id,link_source FROM item_links ORDER BY receipt_id,item_ordinal"
).fetchall()
assert migrated_links == links

for table in ("catalog_fields", "product_specifications", "category_refs", "observation_purchase_forms"):
    assert conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == 0, table

# Merchant namespaces may reuse the same normalized alias key without collision.
conn.execute("INSERT INTO aliases VALUES ('MERCHANT','MARTA','공용','공용','p-standard')")
conn.execute("INSERT INTO aliases VALUES ('MERCHANT','MARTB','공용','공용','p-commodity')")
assert conn.execute("SELECT COUNT(*) FROM aliases WHERE alias_key='공용'").fetchone()[0] == 2
try:
    conn.execute("INSERT INTO aliases VALUES ('MERCHANT','MARTA','공용','다른표기','p-commodity')")
    raise AssertionError("same-context alias collision was not rejected")
except sqlite3.IntegrityError:
    pass

# V2 metadata preserves evidence dimensions and exact decimal text.
conn.execute("INSERT INTO catalog_fields VALUES ('p-standard','BRAND','서울우유','서울우유','PARSED_FROM_RECEIPT','HIGH','UNCONFIRMED')")
conn.execute("INSERT INTO catalog_fields VALUES ('p-standard','PRODUCT_NAME','나100%','나100%','USER_CONFIRMED','HIGH','CONFIRMED')")
conn.execute("INSERT INTO product_specifications VALUES ('p-standard','1','LITER',1,NULL,NULL,'USER_CONFIRMED','HIGH','CONFIRMED')")
conn.execute("INSERT INTO category_refs VALUES ('p-standard','milk')")
conn.execute("INSERT INTO observation_purchase_forms VALUES ('r-1',0,'1','PACK','팩','RECEIPT_TEXT','HIGH','UNCONFIRMED')")
conn.execute("INSERT INTO observation_purchase_forms VALUES ('r-2',3,'1','BAG','봉','RECEIPT_TEXT','MEDIUM','UNCONFIRMED')")
conn.commit()

form_columns = [row[1] for row in conn.execute("PRAGMA table_info(observation_purchase_forms)")]
for forbidden in ("unit_price", "line_amount", "store_name", "purchase_date", "validation_status"):
    assert forbidden not in form_columns, forbidden

index_names = {row[1] for row in conn.execute("PRAGMA index_list(catalog_fields)")}
assert "idx_catalog_fields_lookup" in index_names
category_index_names = {row[1] for row in conn.execute("PRAGMA index_list(category_refs)")}
assert "idx_category_refs_category" in category_index_names

# Cascades stay local and deterministic inside the catalog DB.
conn.execute("DELETE FROM products WHERE id='p-standard'")
conn.commit()
assert conn.execute("SELECT COUNT(*) FROM aliases WHERE product_id='p-standard'").fetchone()[0] == 0
assert conn.execute("SELECT COUNT(*) FROM item_links WHERE product_id='p-standard'").fetchone()[0] == 0
assert conn.execute("SELECT COUNT(*) FROM observation_purchase_forms WHERE receipt_id='r-1' AND item_ordinal=0").fetchone()[0] == 0
assert conn.execute("SELECT COUNT(*) FROM catalog_fields WHERE product_id='p-standard'").fetchone()[0] == 0
assert conn.execute("SELECT COUNT(*) FROM product_specifications WHERE product_id='p-standard'").fetchone()[0] == 0
assert conn.execute("SELECT COUNT(*) FROM category_refs WHERE product_id='p-standard'").fetchone()[0] == 0
assert conn.execute("SELECT COUNT(*) FROM products WHERE id='p-commodity'").fetchone()[0] == 1

# Fresh V2 creation reaches the same table/index target without migration.
fresh = sqlite3.connect(":memory:")
fresh.execute("PRAGMA foreign_keys=ON")
for name in FRESH_NAMES:
    fresh.execute(constant(SCHEMA, name))
fresh_tables = {
    row[0] for row in fresh.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
}
assert fresh_tables == {
    "products", "aliases", "item_links", "catalog_fields", "product_specifications", "category_refs", "observation_purchase_forms"
}

# The migration plan may rebuild aliases, but never core identity/link tables.
plan_sql = ";".join(constant(PLAN, n) for n in MIGRATION_NAMES).upper()
assert "DROP TABLE PRODUCTS" not in plan_sql
assert "DROP TABLE ITEM_LINKS" not in plan_sql

print("CP22 SQLite migration verification PASS")
print("vectors=15")
print("product_schema=2 receipt_schema=1")
print("legacy_products_preserved=2 legacy_aliases_globalized=2 legacy_links_preserved=2")
