package com.receiptledger.v1.search;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.CategoryRef;
import com.receiptledger.v1.catalog.PackageMeasure;
import com.receiptledger.v1.catalog.ProductSpecification;
import com.receiptledger.v1.catalog.SalesUnitCode;
import com.receiptledger.v1.persistence.SqliteReceiptStore;
import com.receiptledger.v1.product.CatalogProduct;
import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.product.SqliteProductCatalogStore;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * CP36 read-only SQLite projection for CP29 discovery.
 *
 * <p>No truth is cached or persisted here. Each load reads the existing catalog/receipt tables in bulk,
 * then SearchBrowseServiceV1 applies the unchanged CP29 ranking and filtering rules in memory.</p>
 */
final class SqliteSearchBrowseSnapshotV1 {
    private SqliteSearchBrowseSnapshotV1() {}

    static Snapshot load(SqliteReceiptStore receipts, SqliteProductCatalogStore catalog) {
        if (receipts == null || catalog == null) throw new IllegalArgumentException("stores");

        List<CatalogProduct> products = catalog.listProducts();
        Map<String, ProductBuilder> builders = new LinkedHashMap<>();
        for (CatalogProduct product : products) {
            if (product != null && product.type != ProductType.UNCLASSIFIED) {
                builders.put(product.id, new ProductBuilder(product));
            }
        }
        if (builders.isEmpty()) return new Snapshot(Collections.<ProductRow>emptyList());

        SQLiteDatabase productDb = catalog.getReadableDatabase();
        loadCoreIntegrity(productDb, builders);
        loadStructuredFields(productDb, builders);
        loadSpecifications(productDb, builders);
        loadCategories(productDb, builders);
        validateCatalogShapes(builders);

        Set<String> neededReceiptIds = new HashSet<>();
        try (Cursor c = productDb.query(
                "item_links",
                new String[]{"product_id", "receipt_id", "item_ordinal"},
                null, null, null, null,
                "product_id ASC,receipt_id ASC,item_ordinal ASC")) {
            while (c.moveToNext()) {
                ProductBuilder builder = builders.get(c.getString(0));
                if (builder == null) continue;
                String receiptId = c.getString(1);
                int ordinal = c.getInt(2);
                builder.links.add(new LinkRow(receiptId, ordinal));
                neededReceiptIds.add(receiptId);
            }
        }

        Map<String, ReceiptRow> receiptRows = new HashMap<>();
        Map<String, Map<Integer, String>> itemNames = new HashMap<>();
        if (!neededReceiptIds.isEmpty()) {
            SQLiteDatabase receiptDb = receipts.getReadableDatabase();
            try (Cursor c = receiptDb.query(
                    "receipts",
                    new String[]{"id", "created_at_ms", "purchase_date", "store_name", "source_width", "source_height"},
                    null, null, null, null, null)) {
                while (c.moveToNext()) {
                    String id = c.getString(0);
                    if (!neededReceiptIds.contains(id)) continue;
                    int sourceWidth = c.getInt(4);
                    int sourceHeight = c.getInt(5);
                    if (sourceWidth < 1 || sourceHeight < 1) throw new IllegalArgumentException("source dimensions");
                    receiptRows.put(id, new ReceiptRow(
                            id,
                            c.getLong(1),
                            nullableText(c, 2),
                            nullableText(c, 3)));
                }
            }
            try (Cursor c = receiptDb.query(
                    "receipt_items",
                    new String[]{"receipt_id", "ordinal", "name"},
                    null, null, null, null,
                    "receipt_id ASC,ordinal ASC")) {
                while (c.moveToNext()) {
                    String receiptId = c.getString(0);
                    if (!neededReceiptIds.contains(receiptId)) continue;
                    Map<Integer, String> byOrdinal = itemNames.get(receiptId);
                    if (byOrdinal == null) {
                        byOrdinal = new HashMap<>();
                        itemNames.put(receiptId, byOrdinal);
                    }
                    byOrdinal.put(c.getInt(1), c.getString(2));
                }
            }
        }

        List<ProductRow> rows = new ArrayList<>();
        for (CatalogProduct product : products) {
            ProductBuilder builder = product == null ? null : builders.get(product.id);
            if (builder == null) continue;
            for (LinkRow link : builder.links) {
                ReceiptRow receipt = receiptRows.get(link.receiptId);
                if (receipt == null) continue;
                Map<Integer, String> byOrdinal = itemNames.get(link.receiptId);
                String itemName = byOrdinal == null ? null : byOrdinal.get(link.itemOrdinal);
                builder.purchases.add(new PurchaseRow(
                        receipt.id,
                        itemName,
                        receipt.purchaseDate,
                        receipt.storeName,
                        receipt.createdAtMillis));
            }
            rows.add(builder.build());
        }
        return new Snapshot(Collections.unmodifiableList(rows));
    }

    private static void loadCoreIntegrity(SQLiteDatabase db, Map<String, ProductBuilder> builders) {
        try (Cursor c = db.query(
                "products",
                new String[]{"id", "type", "record_origin"},
                null, null, null, null, "canonical_name COLLATE NOCASE ASC")) {
            while (c.moveToNext()) {
                ProductBuilder builder = builders.get(c.getString(0));
                if (builder == null) continue;
                ProductType storedType = ProductType.valueOf(c.getString(1));
                if (storedType != builder.product.type) throw new IllegalStateException("catalog type mismatch");
                builder.recordOrigin = CatalogEntryV2.RecordOrigin.valueOf(c.getString(2));
            }
        }
        for (ProductBuilder builder : builders.values()) {
            if (builder.recordOrigin == null) throw new IllegalStateException("missing catalog core row");
        }
    }

    private static void loadStructuredFields(SQLiteDatabase db, Map<String, ProductBuilder> builders) {
        try (Cursor c = db.query(
                "catalog_fields",
                new String[]{"product_id", "field_code", "value_text", "source", "confidence", "confirmation"},
                null, null, null, null,
                "product_id ASC,field_code ASC")) {
            while (c.moveToNext()) {
                ProductBuilder builder = builders.get(c.getString(0));
                if (builder == null) continue;
                validateEvidence(c, 3, 4, 5);
                String code = c.getString(1);
                String value = c.getString(2);
                if ("BRAND".equals(code)) builder.brand = value;
                else if ("PRODUCT_NAME".equals(code)) builder.productName = value;
                else if ("VARIANT".equals(code)) builder.variant = value;
            }
        }
    }

    private static void loadSpecifications(SQLiteDatabase db, Map<String, ProductBuilder> builders) {
        try (Cursor c = db.query(
                "product_specifications",
                new String[]{
                        "product_id", "net_amount", "net_unit", "pack_count",
                        "inner_amount", "inner_unit", "source", "confidence", "confirmation"},
                null, null, null, null, "product_id ASC")) {
            while (c.moveToNext()) {
                ProductBuilder builder = builders.get(c.getString(0));
                if (builder == null) continue;
                validateEvidence(c, 6, 7, 8);
                builder.specification = new ProductSpecification(
                        readMeasure(c, 1, 2),
                        c.isNull(3) ? null : c.getInt(3),
                        readMeasure(c, 4, 5));
            }
        }
    }

    private static void loadCategories(SQLiteDatabase db, Map<String, ProductBuilder> builders) {
        try (Cursor c = db.query(
                "category_refs",
                new String[]{"product_id", "category_id"},
                null, null, null, null, "product_id ASC")) {
            while (c.moveToNext()) {
                ProductBuilder builder = builders.get(c.getString(0));
                if (builder != null) builder.categoryId = new CategoryRef(c.getString(1)).id;
            }
        }
    }

    private static void validateCatalogShapes(Map<String, ProductBuilder> builders) {
        for (ProductBuilder builder : builders.values()) {
            if (builder.product.type == ProductType.NON_STANDARD
                    && (builder.brand != null || builder.productName != null || builder.variant != null
                    || builder.specification != null)) {
                throw new IllegalArgumentException("commodity cannot carry STANDARD product fields");
            }
            if (builder.product.type == ProductType.STANDARD
                    && builder.recordOrigin == CatalogEntryV2.RecordOrigin.NATIVE_V2
                    && builder.productName == null) {
                throw new IllegalArgumentException("native STANDARD product requires productName");
            }
        }
    }

    private static void validateEvidence(Cursor c, int sourceIndex, int confidenceIndex, int confirmationIndex) {
        CatalogField.Source source = CatalogField.Source.valueOf(c.getString(sourceIndex));
        CatalogField.Confidence.valueOf(c.getString(confidenceIndex));
        CatalogField.Confirmation.valueOf(c.getString(confirmationIndex));
        if (source == CatalogField.Source.UNKNOWN) {
            throw new IllegalArgumentException("present field requires a known source");
        }
    }

    private static PackageMeasure readMeasure(Cursor c, int amountIndex, int unitIndex) {
        boolean amountNull = c.isNull(amountIndex);
        boolean unitNull = c.isNull(unitIndex);
        if (amountNull && unitNull) return null;
        if (amountNull || unitNull) throw new IllegalStateException("corrupt package measure");
        return new PackageMeasure(c.getString(amountIndex), SalesUnitCode.valueOf(c.getString(unitIndex)));
    }

    private static String nullableText(Cursor c, int index) {
        return c.isNull(index) ? null : c.getString(index);
    }

    static final class Snapshot {
        final List<ProductRow> products;
        Snapshot(List<ProductRow> products) { this.products = products; }
    }

    static final class ProductRow {
        final CatalogProduct product;
        final String brand;
        final String productName;
        final String variant;
        final ProductSpecification specification;
        final String categoryId;
        final List<PurchaseRow> purchases;

        ProductRow(
                CatalogProduct product,
                String brand,
                String productName,
                String variant,
                ProductSpecification specification,
                String categoryId,
                List<PurchaseRow> purchases) {
            this.product = product;
            this.brand = brand;
            this.productName = productName;
            this.variant = variant;
            this.specification = specification;
            this.categoryId = categoryId;
            this.purchases = purchases;
        }
    }

    static final class PurchaseRow {
        final String receiptId;
        final String itemName;
        final String purchaseDate;
        final String storeName;
        final long createdAtMillis;

        PurchaseRow(String receiptId, String itemName, String purchaseDate, String storeName, long createdAtMillis) {
            this.receiptId = receiptId;
            this.itemName = itemName;
            this.purchaseDate = purchaseDate;
            this.storeName = storeName;
            this.createdAtMillis = createdAtMillis;
        }
    }

    private static final class ProductBuilder {
        final CatalogProduct product;
        final List<LinkRow> links = new ArrayList<>();
        final List<PurchaseRow> purchases = new ArrayList<>();
        String brand;
        String productName;
        String variant;
        ProductSpecification specification;
        String categoryId;
        CatalogEntryV2.RecordOrigin recordOrigin;

        ProductBuilder(CatalogProduct product) { this.product = product; }

        ProductRow build() {
            return new ProductRow(
                    product,
                    brand,
                    productName,
                    variant,
                    specification,
                    categoryId,
                    Collections.unmodifiableList(new ArrayList<>(purchases)));
        }
    }

    private static final class LinkRow {
        final String receiptId;
        final int itemOrdinal;
        LinkRow(String receiptId, int itemOrdinal) {
            this.receiptId = receiptId;
            this.itemOrdinal = itemOrdinal;
        }
    }

    private static final class ReceiptRow {
        final String id;
        final long createdAtMillis;
        final String purchaseDate;
        final String storeName;
        ReceiptRow(String id, long createdAtMillis, String purchaseDate, String storeName) {
            this.id = id;
            this.createdAtMillis = createdAtMillis;
            this.purchaseDate = purchaseDate;
            this.storeName = storeName;
        }
    }
}
