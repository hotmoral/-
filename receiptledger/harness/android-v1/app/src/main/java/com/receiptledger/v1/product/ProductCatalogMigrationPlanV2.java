package com.receiptledger.v1.product;

/** Pure-Java ordered SQL plan for the only CP22-supported migration: catalog schema 1 -> 2. */
public final class ProductCatalogMigrationPlanV2 {
    private ProductCatalogMigrationPlanV2() {}

    public static final String ADD_RECORD_ORIGIN = "ALTER TABLE products ADD COLUMN record_origin TEXT NOT NULL DEFAULT 'LEGACY_V1'";
    public static final String RENAME_OLD_ALIASES = "ALTER TABLE aliases RENAME TO aliases_v1";
    public static final String CREATE_ALIASES_V2_TEMP = "CREATE TABLE aliases_v2 (scope TEXT NOT NULL,merchant_key TEXT NOT NULL,alias_key TEXT NOT NULL,raw_alias TEXT NOT NULL,product_id TEXT NOT NULL,PRIMARY KEY(scope,merchant_key,alias_key),CHECK(scope IN ('GLOBAL','MERCHANT')),CHECK((scope='GLOBAL' AND merchant_key='') OR (scope='MERCHANT' AND merchant_key<>'')),FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)";
    public static final String COPY_ALIASES_AS_GLOBAL = "INSERT INTO aliases_v2(scope,merchant_key,alias_key,raw_alias,product_id) SELECT 'GLOBAL','',alias_key,raw_alias,product_id FROM aliases_v1";
    public static final String DROP_OLD_ALIASES = "DROP TABLE aliases_v1";
    public static final String RENAME_ALIASES_V2 = "ALTER TABLE aliases_v2 RENAME TO aliases";

    public static String[] coreStatements() {
        return new String[] {
                ADD_RECORD_ORIGIN,
                RENAME_OLD_ALIASES,
                CREATE_ALIASES_V2_TEMP,
                COPY_ALIASES_AS_GLOBAL,
                DROP_OLD_ALIASES,
                RENAME_ALIASES_V2
        };
    }
}
