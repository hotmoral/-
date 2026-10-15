package com.receiptledger.v1.product;

public final class ProductCatalogSchema {
 private ProductCatalogSchema(){}public static final String DB_NAME="receipt-products-v1.db";public static final int VERSION=1;
 public static final String CREATE_PRODUCTS="CREATE TABLE products (id TEXT PRIMARY KEY NOT NULL,type TEXT NOT NULL,canonical_name TEXT NOT NULL,canonical_key TEXT NOT NULL UNIQUE,created_at_ms INTEGER NOT NULL)";
 public static final String CREATE_ALIASES="CREATE TABLE aliases (alias_key TEXT PRIMARY KEY NOT NULL,raw_alias TEXT NOT NULL,product_id TEXT NOT NULL,FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)";
 public static final String CREATE_LINKS="CREATE TABLE item_links (receipt_id TEXT NOT NULL,item_ordinal INTEGER NOT NULL,product_id TEXT NOT NULL,link_source TEXT NOT NULL,PRIMARY KEY(receipt_id,item_ordinal),FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)";
 public static final String CREATE_LINK_PRODUCT_INDEX="CREATE INDEX idx_item_links_product ON item_links(product_id)";
}
