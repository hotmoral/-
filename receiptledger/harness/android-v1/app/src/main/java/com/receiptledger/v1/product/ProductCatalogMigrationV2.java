package com.receiptledger.v1.product;

import android.database.sqlite.SQLiteDatabase;

/** Executes the explicit CP22 product-catalog migration. */
public final class ProductCatalogMigrationV2 {
    private ProductCatalogMigrationV2() {}

    public static void migrate(SQLiteDatabase db, int oldVersion, int newVersion) {
        if (oldVersion != 1 || newVersion != 2) {
            throw new IllegalStateException("Unsupported product catalog migration: " + oldVersion + " -> " + newVersion);
        }
        for (String sql : ProductCatalogMigrationPlanV2.coreStatements()) db.execSQL(sql);
        db.execSQL(ProductCatalogSchema.CREATE_ALIAS_PRODUCT_INDEX);
        db.execSQL(ProductCatalogSchema.CREATE_CATALOG_FIELDS);
        db.execSQL(ProductCatalogSchema.CREATE_PRODUCT_SPECIFICATIONS);
        db.execSQL(ProductCatalogSchema.CREATE_CATEGORY_REFS);
        db.execSQL(ProductCatalogSchema.CREATE_OBSERVATION_PURCHASE_FORMS);
        db.execSQL(ProductCatalogSchema.CREATE_CATALOG_FIELD_LOOKUP_INDEX);
        db.execSQL(ProductCatalogSchema.CREATE_CATEGORY_LOOKUP_INDEX);
    }
}
