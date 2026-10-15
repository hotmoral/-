package com.receiptledger.v1.product;

import android.content.ContentValues;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.CatalogKind;
import com.receiptledger.v1.catalog.CategoryRef;
import com.receiptledger.v1.catalog.PackageMeasure;
import com.receiptledger.v1.catalog.ProductSpecification;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.catalog.SalesUnitCode;

/** SQLite row codec for CP21 domain values. Price/date/store truth deliberately remains in receipt storage. */
final class CatalogV2Persistence {
    private CatalogV2Persistence() {}

    static void saveCatalog(SQLiteDatabase db, CatalogEntryV2 entry) {
        if (entry == null) throw new IllegalArgumentException("entry");
        CoreRow existing = coreRow(db, entry.id);
        if (existing == null) {
            ContentValues v = new ContentValues();
            v.put("id", entry.id);
            v.put("type", entry.kind.toLegacyType().name());
            v.put("canonical_name", entry.canonicalName);
            v.put("canonical_key", entry.canonicalKey);
            v.put("created_at_ms", entry.createdAtMillis);
            v.put("record_origin", entry.recordOrigin.name());
            db.insertOrThrow("products", null, v);
        } else {
            if (CatalogKind.fromLegacyClassified(existing.type) != entry.kind
                    || !existing.canonicalName.equals(entry.canonicalName)
                    || existing.createdAtMillis != entry.createdAtMillis
                    || existing.recordOrigin != entry.recordOrigin) {
                throw new IllegalStateException("catalog core mutation requires a later explicit contract: " + entry.id);
            }
        }
        saveStringField(db, entry.id, "BRAND", entry.brand);
        saveStringField(db, entry.id, "PRODUCT_NAME", entry.productName);
        saveStringField(db, entry.id, "VARIANT", entry.variant);
        saveSpecification(db, entry.id, entry.specification);
        saveCategory(db, entry.id, entry.category);
    }

    static CatalogEntryV2 readCatalog(SQLiteDatabase db, String id) {
        CoreRow core = coreRow(db, id);
        if (core == null) return null;
        CatalogKind kind = CatalogKind.fromLegacyClassified(core.type);
        return CatalogEntryV2.rehydrate(
                id,
                kind,
                core.canonicalName,
                readStringField(db, id, "BRAND"),
                readStringField(db, id, "PRODUCT_NAME"),
                readStringField(db, id, "VARIANT"),
                readSpecification(db, id),
                readCategory(db, id),
                core.createdAtMillis,
                core.recordOrigin);
    }

    static void saveAlias(SQLiteDatabase db, AliasContext context, String rawAlias, String productId) {
        if (context == null) throw new IllegalArgumentException("context");
        if (coreRow(db, productId) == null) throw new IllegalArgumentException("unknown product: " + productId);
        String aliasKey = ProductNameNormalizer.key(rawAlias);
        if (aliasKey.isEmpty()) throw new IllegalArgumentException("alias");
        String merchantKey = merchantStorageKey(context);
        String existing = aliasProductId(db, context, aliasKey);
        if (existing != null && !existing.equals(productId)) {
            throw new IllegalStateException("alias already belongs to another product in context");
        }
        if (existing != null) return;
        ContentValues v = new ContentValues();
        v.put("scope", context.scope.name());
        v.put("merchant_key", merchantKey);
        v.put("alias_key", aliasKey);
        v.put("raw_alias", rawAlias == null ? "" : rawAlias);
        v.put("product_id", productId);
        db.insertOrThrow("aliases", null, v);
    }

    static String aliasProductId(SQLiteDatabase db, AliasContext context, String rawAliasOrKey) {
        if (context == null) throw new IllegalArgumentException("context");
        String aliasKey = ProductNameNormalizer.key(rawAliasOrKey);
        if (aliasKey.isEmpty()) return null;
        try (Cursor c = db.query(
                "aliases",
                new String[]{"product_id"},
                "scope=? AND merchant_key=? AND alias_key=?",
                new String[]{context.scope.name(), merchantStorageKey(context), aliasKey},
                null, null, null)) {
            return c.moveToFirst() ? c.getString(0) : null;
        }
    }

    static void savePurchaseForm(SQLiteDatabase db, String receiptId, int itemOrdinal, CatalogField<PurchaseForm> field) {
        if (receiptId == null || receiptId.trim().isEmpty()) throw new IllegalArgumentException("receiptId");
        if (itemOrdinal < 0) throw new IllegalArgumentException("itemOrdinal");
        CatalogField<PurchaseForm> safe = field == null ? CatalogField.absent() : field;
        String[] args = new String[]{receiptId, Integer.toString(itemOrdinal)};
        if (!safe.isPresent()) {
            db.delete("observation_purchase_forms", "receipt_id=? AND item_ordinal=?", args);
            return;
        }
        if (!linkExists(db, receiptId, itemOrdinal)) {
            throw new IllegalStateException("purchase form requires existing item link");
        }
        ContentValues v = new ContentValues();
        v.put("receipt_id", receiptId);
        v.put("item_ordinal", itemOrdinal);
        v.put("quantity_text", safe.value.quantity.toPlainString());
        v.put("unit_code", safe.value.unit.name());
        v.put("raw_unit_label", safe.value.rawUnitLabel);
        putEvidence(v, safe);
        db.insertWithOnConflict("observation_purchase_forms", null, v, SQLiteDatabase.CONFLICT_REPLACE);
    }

    static CatalogField<PurchaseForm> readPurchaseForm(SQLiteDatabase db, String receiptId, int itemOrdinal) {
        try (Cursor c = db.query(
                "observation_purchase_forms",
                null,
                "receipt_id=? AND item_ordinal=?",
                new String[]{receiptId, Integer.toString(itemOrdinal)},
                null, null, null)) {
            if (!c.moveToFirst()) return CatalogField.absent();
            PurchaseForm form = new PurchaseForm(
                    text(c, "quantity_text"),
                    SalesUnitCode.valueOf(text(c, "unit_code")),
                    text(c, "raw_unit_label"));
            return CatalogField.of(form, source(c), confirmation(c), confidence(c));
        }
    }

    private static void saveStringField(SQLiteDatabase db, String productId, String code, CatalogField<String> field) {
        CatalogField<String> safe = field == null ? CatalogField.absent() : field;
        if (!safe.isPresent()) {
            db.delete("catalog_fields", "product_id=? AND field_code=?", new String[]{productId, code});
            return;
        }
        ContentValues v = new ContentValues();
        v.put("product_id", productId);
        v.put("field_code", code);
        v.put("value_text", safe.value);
        v.put("value_key", ProductNameNormalizer.key(safe.value));
        putEvidence(v, safe);
        db.insertWithOnConflict("catalog_fields", null, v, SQLiteDatabase.CONFLICT_REPLACE);
    }

    private static CatalogField<String> readStringField(SQLiteDatabase db, String productId, String code) {
        try (Cursor c = db.query(
                "catalog_fields", null,
                "product_id=? AND field_code=?",
                new String[]{productId, code}, null, null, null)) {
            if (!c.moveToFirst()) return CatalogField.absent();
            return CatalogField.of(text(c, "value_text"), source(c), confirmation(c), confidence(c));
        }
    }

    private static void saveSpecification(
            SQLiteDatabase db, String productId, CatalogField<ProductSpecification> field) {
        CatalogField<ProductSpecification> safe = field == null ? CatalogField.absent() : field;
        if (!safe.isPresent()) {
            db.delete("product_specifications", "product_id=?", new String[]{productId});
            return;
        }
        ProductSpecification spec = safe.value;
        ContentValues v = new ContentValues();
        v.put("product_id", productId);
        putMeasure(v, "net_amount", "net_unit", spec.netContent);
        if (spec.packCount == null) v.putNull("pack_count"); else v.put("pack_count", spec.packCount);
        putMeasure(v, "inner_amount", "inner_unit", spec.innerUnitContent);
        putEvidence(v, safe);
        db.insertWithOnConflict("product_specifications", null, v, SQLiteDatabase.CONFLICT_REPLACE);
    }

    private static CatalogField<ProductSpecification> readSpecification(SQLiteDatabase db, String productId) {
        try (Cursor c = db.query("product_specifications", null, "product_id=?", new String[]{productId}, null, null, null)) {
            if (!c.moveToFirst()) return CatalogField.absent();
            ProductSpecification spec = new ProductSpecification(
                    readMeasure(c, "net_amount", "net_unit"),
                    nullableInt(c, "pack_count"),
                    readMeasure(c, "inner_amount", "inner_unit"));
            return CatalogField.of(spec, source(c), confirmation(c), confidence(c));
        }
    }

    private static void saveCategory(SQLiteDatabase db, String productId, CategoryRef category) {
        if (category == null) {
            db.delete("category_refs", "product_id=?", new String[]{productId});
            return;
        }
        ContentValues v = new ContentValues();
        v.put("product_id", productId);
        v.put("category_id", category.id);
        db.insertWithOnConflict("category_refs", null, v, SQLiteDatabase.CONFLICT_REPLACE);
    }

    private static CategoryRef readCategory(SQLiteDatabase db, String productId) {
        try (Cursor c = db.query("category_refs", new String[]{"category_id"}, "product_id=?", new String[]{productId}, null, null, null)) {
            return c.moveToFirst() ? new CategoryRef(c.getString(0)) : null;
        }
    }

    private static CoreRow coreRow(SQLiteDatabase db, String id) {
        if (id == null || id.trim().isEmpty()) return null;
        try (Cursor c = db.query(
                "products",
                new String[]{"type","canonical_name","created_at_ms","record_origin"},
                "id=?", new String[]{id}, null, null, null)) {
            if (!c.moveToFirst()) return null;
            ProductType type = ProductType.valueOf(c.getString(0));
            String name = c.getString(1);
            long created = c.getLong(2);
            CatalogEntryV2.RecordOrigin origin = CatalogEntryV2.RecordOrigin.valueOf(c.getString(3));
            return new CoreRow(type, name, created, origin);
        }
    }

    private static boolean linkExists(SQLiteDatabase db, String receiptId, int itemOrdinal) {
        try (Cursor c = db.query(
                "item_links", new String[]{"product_id"},
                "receipt_id=? AND item_ordinal=?",
                new String[]{receiptId, Integer.toString(itemOrdinal)}, null, null, null)) {
            return c.moveToFirst();
        }
    }

    private static String merchantStorageKey(AliasContext context) {
        return context.scope == AliasContext.Scope.GLOBAL ? "" : context.merchantKey;
    }

    private static void putMeasure(ContentValues v, String amountKey, String unitKey, PackageMeasure measure) {
        if (measure == null) {
            v.putNull(amountKey);
            v.putNull(unitKey);
        } else {
            v.put(amountKey, measure.amount.toPlainString());
            v.put(unitKey, measure.unit.name());
        }
    }

    private static PackageMeasure readMeasure(Cursor c, String amountKey, String unitKey) {
        int amountIndex = c.getColumnIndexOrThrow(amountKey);
        int unitIndex = c.getColumnIndexOrThrow(unitKey);
        if (c.isNull(amountIndex) && c.isNull(unitIndex)) return null;
        if (c.isNull(amountIndex) || c.isNull(unitIndex)) throw new IllegalStateException("corrupt package measure");
        return new PackageMeasure(c.getString(amountIndex), SalesUnitCode.valueOf(c.getString(unitIndex)));
    }

    private static Integer nullableInt(Cursor c, String name) {
        int index = c.getColumnIndexOrThrow(name);
        return c.isNull(index) ? null : c.getInt(index);
    }

    private static void putEvidence(ContentValues v, CatalogField<?> field) {
        v.put("source", field.source.name());
        v.put("confidence", field.confidence.name());
        v.put("confirmation", field.confirmation.name());
    }

    private static CatalogField.Source source(Cursor c) {
        return CatalogField.Source.valueOf(text(c, "source"));
    }

    private static CatalogField.Confirmation confirmation(Cursor c) {
        return CatalogField.Confirmation.valueOf(text(c, "confirmation"));
    }

    private static CatalogField.Confidence confidence(Cursor c) {
        return CatalogField.Confidence.valueOf(text(c, "confidence"));
    }

    private static String text(Cursor c, String name) {
        return c.getString(c.getColumnIndexOrThrow(name));
    }

    private static final class CoreRow {
        final ProductType type;
        final String canonicalName;
        final long createdAtMillis;
        final CatalogEntryV2.RecordOrigin recordOrigin;

        CoreRow(ProductType type, String canonicalName, long createdAtMillis, CatalogEntryV2.RecordOrigin recordOrigin) {
            this.type = type;
            this.canonicalName = canonicalName;
            this.createdAtMillis = createdAtMillis;
            this.recordOrigin = recordOrigin;
        }
    }
}
