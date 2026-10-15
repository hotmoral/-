package com.receiptledger.v1.product;

public final class ProductCatalogSchema {
    private ProductCatalogSchema() {}

    public static final String DB_NAME = "receipt-products-v1.db";
    public static final int VERSION = 2;

    public static final String CREATE_PRODUCTS = "CREATE TABLE products (id TEXT PRIMARY KEY NOT NULL,type TEXT NOT NULL,canonical_name TEXT NOT NULL,canonical_key TEXT NOT NULL UNIQUE,created_at_ms INTEGER NOT NULL,record_origin TEXT NOT NULL DEFAULT 'LEGACY_V1')";
    public static final String CREATE_ALIASES = "CREATE TABLE aliases (scope TEXT NOT NULL,merchant_key TEXT NOT NULL,alias_key TEXT NOT NULL,raw_alias TEXT NOT NULL,product_id TEXT NOT NULL,PRIMARY KEY(scope,merchant_key,alias_key),CHECK(scope IN ('GLOBAL','MERCHANT')),CHECK((scope='GLOBAL' AND merchant_key='') OR (scope='MERCHANT' AND merchant_key<>'')),FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)";
    public static final String CREATE_LINKS = "CREATE TABLE item_links (receipt_id TEXT NOT NULL,item_ordinal INTEGER NOT NULL,product_id TEXT NOT NULL,link_source TEXT NOT NULL,PRIMARY KEY(receipt_id,item_ordinal),FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)";
    public static final String CREATE_CATALOG_FIELDS = "CREATE TABLE catalog_fields (product_id TEXT NOT NULL,field_code TEXT NOT NULL,value_text TEXT NOT NULL,value_key TEXT NOT NULL,source TEXT NOT NULL,confidence TEXT NOT NULL,confirmation TEXT NOT NULL,PRIMARY KEY(product_id,field_code),CHECK(field_code IN ('BRAND','PRODUCT_NAME','VARIANT')),FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)";
    public static final String CREATE_PRODUCT_SPECIFICATIONS = "CREATE TABLE product_specifications (product_id TEXT PRIMARY KEY NOT NULL,net_amount TEXT,net_unit TEXT,pack_count INTEGER,inner_amount TEXT,inner_unit TEXT,source TEXT NOT NULL,confidence TEXT NOT NULL,confirmation TEXT NOT NULL,CHECK(pack_count IS NULL OR pack_count>0),CHECK((net_amount IS NULL AND net_unit IS NULL) OR (net_amount IS NOT NULL AND net_unit IS NOT NULL)),CHECK((inner_amount IS NULL AND inner_unit IS NULL) OR (inner_amount IS NOT NULL AND inner_unit IS NOT NULL AND pack_count IS NOT NULL)),FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)";
    public static final String CREATE_CATEGORY_REFS = "CREATE TABLE category_refs (product_id TEXT PRIMARY KEY NOT NULL,category_id TEXT NOT NULL,FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)";
    public static final String CREATE_OBSERVATION_PURCHASE_FORMS = "CREATE TABLE observation_purchase_forms (receipt_id TEXT NOT NULL,item_ordinal INTEGER NOT NULL,quantity_text TEXT NOT NULL,unit_code TEXT NOT NULL,raw_unit_label TEXT NOT NULL,source TEXT NOT NULL,confidence TEXT NOT NULL,confirmation TEXT NOT NULL,PRIMARY KEY(receipt_id,item_ordinal),FOREIGN KEY(receipt_id,item_ordinal) REFERENCES item_links(receipt_id,item_ordinal) ON DELETE CASCADE)";

    public static final String CREATE_LINK_PRODUCT_INDEX = "CREATE INDEX idx_item_links_product ON item_links(product_id)";
    public static final String CREATE_ALIAS_PRODUCT_INDEX = "CREATE INDEX idx_aliases_product ON aliases(product_id)";
    public static final String CREATE_CATALOG_FIELD_LOOKUP_INDEX = "CREATE INDEX idx_catalog_fields_lookup ON catalog_fields(field_code,value_key)";
    public static final String CREATE_CATEGORY_LOOKUP_INDEX = "CREATE INDEX idx_category_refs_category ON category_refs(category_id)";
}
