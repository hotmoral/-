package com.receiptledger.v1.product;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.CatalogKind;
import com.receiptledger.v1.catalog.CategoryRef;
import org.junit.Test;

public final class CatalogPersistenceContractV2Test {
    @Test public void catalogDbFilenameIsStableAndVersionAdvancesOnce() {
        assertEquals("receipt-products-v1.db", ProductCatalogSchema.DB_NAME);
        assertEquals(2, ProductCatalogSchema.VERSION);
    }

    @Test public void migrationNeverDropsProductsOrItemLinks() {
        String sql = String.join(";", ProductCatalogMigrationPlanV2.coreStatements()).toUpperCase();
        assertFalse(sql.contains("DROP TABLE PRODUCTS"));
        assertFalse(sql.contains("DROP TABLE ITEM_LINKS"));
        assertTrue(sql.contains("DROP TABLE ALIASES_V1"));
    }

    @Test public void legacyAliasesAreExplicitlyCopiedAsGlobal() {
        String sql = ProductCatalogMigrationPlanV2.COPY_ALIASES_AS_GLOBAL;
        assertTrue(sql.contains("'GLOBAL',''"));
        assertTrue(sql.contains("alias_key,raw_alias,product_id"));
    }

    @Test public void aliasSchemaUsesContextualCompositePrimaryKey() {
        assertTrue(ProductCatalogSchema.CREATE_ALIASES.contains("PRIMARY KEY(scope,merchant_key,alias_key)"));
        assertTrue(ProductCatalogSchema.CREATE_ALIASES.contains("scope='GLOBAL'"));
        assertTrue(ProductCatalogSchema.CREATE_ALIASES.contains("scope='MERCHANT'"));
    }

    @Test public void observationFormSchemaCannotBecomeDuplicatePriceTruth() {
        String schema = ProductCatalogSchema.CREATE_OBSERVATION_PURCHASE_FORMS.toLowerCase();
        assertFalse(schema.contains("unit_price"));
        assertFalse(schema.contains("line_amount"));
        assertFalse(schema.contains("store_name"));
        assertFalse(schema.contains("purchase_date"));
        assertTrue(schema.contains("quantity_text"));
        assertTrue(schema.contains("raw_unit_label"));
    }

    @Test public void legacyOriginCanRehydrateMetadataWithoutChangingIdentityAuthority() {
        CatalogEntryV2 entry = CatalogEntryV2.rehydrate(
                "legacy-id",
                CatalogKind.STANDARD_PRODUCT,
                "기존 제품명",
                CatalogField.parsed("브랜드", CatalogField.Confidence.HIGH),
                CatalogField.parsed("제품", CatalogField.Confidence.MEDIUM),
                CatalogField.absent(),
                CatalogField.absent(),
                new CategoryRef("food"),
                123L,
                CatalogEntryV2.RecordOrigin.LEGACY_V1);
        assertEquals("legacy-id", entry.id);
        assertEquals(CatalogEntryV2.RecordOrigin.LEGACY_V1, entry.recordOrigin);
        assertEquals("브랜드", entry.brand.value);
        assertFalse(entry.brand.isConfirmed());
    }

    @Test public void semanticLookupAndCategoryIndexesAreExplicit() {
        assertTrue(ProductCatalogSchema.CREATE_CATALOG_FIELD_LOOKUP_INDEX.contains("field_code,value_key"));
        assertTrue(ProductCatalogSchema.CREATE_CATEGORY_LOOKUP_INDEX.contains("category_id"));
    }
}
