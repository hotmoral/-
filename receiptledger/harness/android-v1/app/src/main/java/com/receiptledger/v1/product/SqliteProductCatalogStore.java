package com.receiptledger.v1.product;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.PurchaseForm;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.UUID;

public final class SqliteProductCatalogStore extends SQLiteOpenHelper
        implements ProductCatalogStore, CatalogV2PersistenceStore {

    public SqliteProductCatalogStore(Context context) {
        super(context, ProductCatalogSchema.DB_NAME, null, ProductCatalogSchema.VERSION);
    }

    @Override public void onConfigure(SQLiteDatabase db) {
        super.onConfigure(db);
        db.setForeignKeyConstraintsEnabled(true);
    }

    @Override public void onCreate(SQLiteDatabase db) {
        db.execSQL(ProductCatalogSchema.CREATE_PRODUCTS);
        db.execSQL(ProductCatalogSchema.CREATE_ALIASES);
        db.execSQL(ProductCatalogSchema.CREATE_LINKS);
        db.execSQL(ProductCatalogSchema.CREATE_CATALOG_FIELDS);
        db.execSQL(ProductCatalogSchema.CREATE_PRODUCT_SPECIFICATIONS);
        db.execSQL(ProductCatalogSchema.CREATE_CATEGORY_REFS);
        db.execSQL(ProductCatalogSchema.CREATE_OBSERVATION_PURCHASE_FORMS);
        db.execSQL(ProductCatalogSchema.CREATE_LINK_PRODUCT_INDEX);
        db.execSQL(ProductCatalogSchema.CREATE_ALIAS_PRODUCT_INDEX);
        db.execSQL(ProductCatalogSchema.CREATE_CATALOG_FIELD_LOOKUP_INDEX);
        db.execSQL(ProductCatalogSchema.CREATE_CATEGORY_LOOKUP_INDEX);
    }

    @Override public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        ProductCatalogMigrationV2.migrate(db, oldVersion, newVersion);
    }

    @Override public IdentityResolution confirm(
            String receiptId,
            int ordinal,
            String rawAlias,
            ProductType type,
            String canonicalName,
            long now) {
        if (type == null || type == ProductType.UNCLASSIFIED) {
            throw new IllegalArgumentException("classified type required");
        }
        String canonicalKey = ProductNameNormalizer.key(canonicalName);
        String aliasKey = ProductNameNormalizer.key(rawAlias);
        if (canonicalKey.isEmpty() || aliasKey.isEmpty()) throw new IllegalArgumentException("name");

        SQLiteDatabase db = getWritableDatabase();
        db.beginTransaction();
        try {
            CatalogProduct product = byCanonical(db, canonicalKey);
            if (product != null && product.type != type) {
                throw new IllegalStateException("canonical name already exists with different type");
            }
            if (product == null) {
                product = new CatalogProduct(UUID.randomUUID().toString(), type, canonicalName, now);
                ContentValues v = new ContentValues();
                v.put("id", product.id);
                v.put("type", product.type.name());
                v.put("canonical_name", product.canonicalName);
                v.put("canonical_key", product.canonicalKey);
                v.put("created_at_ms", product.createdAtMillis);
                v.put("record_origin", CatalogEntryV2.RecordOrigin.LEGACY_V1.name());
                db.insertOrThrow("products", null, v);
            }
            CatalogV2Persistence.saveAlias(db, AliasContext.global(), rawAlias, product.id);
            writeLink(db, receiptId, ordinal, product.id, LinkSource.USER_CONFIRMED);
            db.setTransactionSuccessful();
            return IdentityResolution.linked(product, LinkSource.USER_CONFIRMED);
        } finally {
            db.endTransaction();
        }
    }

    @Override public IdentityResolution resolveAndLinkExact(String receiptId, int ordinal, String rawAlias) {
        SQLiteDatabase db = getWritableDatabase();
        String productId = CatalogV2Persistence.aliasProductId(db, AliasContext.global(), rawAlias);
        if (productId == null) return IdentityResolution.unclassified();
        CatalogProduct product = byId(db, productId);
        if (product == null) return IdentityResolution.unclassified();
        writeLink(db, receiptId, ordinal, product.id, LinkSource.EXACT_ALIAS);
        return IdentityResolution.linked(product, LinkSource.EXACT_ALIAS);
    }

    @Override public IdentityResolution itemResolution(String receiptId, int ordinal) {
        SQLiteDatabase db = getReadableDatabase();
        try (Cursor c = db.query(
                "item_links",
                new String[]{"product_id", "link_source"},
                "receipt_id=? AND item_ordinal=?",
                new String[]{receiptId, Integer.toString(ordinal)},
                null, null, null)) {
            if (!c.moveToFirst()) return IdentityResolution.unclassified();
            CatalogProduct product = byId(db, c.getString(0));
            if (product == null) return IdentityResolution.unclassified();
            return IdentityResolution.linked(product, source(c.getString(1)));
        }
    }

    @Override public CatalogProduct product(String id) {
        return byId(getReadableDatabase(), id);
    }

    @Override public List<CatalogProduct> listProducts() {
        List<CatalogProduct> out = new ArrayList<>();
        try (Cursor c = getReadableDatabase().query(
                "products", null, null, null, null, null, "canonical_name COLLATE NOCASE ASC")) {
            while (c.moveToNext()) out.add(readProduct(c));
        }
        return Collections.unmodifiableList(out);
    }

    @Override public List<ItemLinkRef> linksForProduct(String productId) {
        List<ItemLinkRef> out = new ArrayList<>();
        try (Cursor c = getReadableDatabase().query(
                "item_links",
                new String[]{"receipt_id", "item_ordinal", "link_source"},
                "product_id=?",
                new String[]{productId},
                null, null, "receipt_id ASC,item_ordinal ASC")) {
            while (c.moveToNext()) {
                out.add(new ItemLinkRef(c.getString(0), c.getInt(1), productId, source(c.getString(2))));
            }
        }
        return Collections.unmodifiableList(out);
    }

    @Override public void unlinkItem(String receiptId, int ordinal) {
        getWritableDatabase().delete(
                "item_links", "receipt_id=? AND item_ordinal=?", new String[]{receiptId, Integer.toString(ordinal)});
    }

    @Override public void unlinkReceipt(String receiptId) {
        getWritableDatabase().delete("item_links", "receipt_id=?", new String[]{receiptId});
    }

    @Override public CatalogEntryV2 catalogEntryV2(String catalogEntryId) {
        return CatalogV2Persistence.readCatalog(getReadableDatabase(), catalogEntryId);
    }

    @Override public void saveCatalogEntryV2(CatalogEntryV2 entry) {
        SQLiteDatabase db = getWritableDatabase();
        db.beginTransaction();
        try {
            CatalogV2Persistence.saveCatalog(db, entry);
            db.setTransactionSuccessful();
        } finally {
            db.endTransaction();
        }
    }

    @Override public void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId) {
        SQLiteDatabase db = getWritableDatabase();
        db.beginTransaction();
        try {
            CatalogV2Persistence.saveAlias(db, context, rawAlias, catalogEntryId);
            db.setTransactionSuccessful();
        } finally {
            db.endTransaction();
        }
    }

    @Override public String aliasCatalogEntryIdV2(AliasContext context, String rawAlias) {
        return CatalogV2Persistence.aliasProductId(getReadableDatabase(), context, rawAlias);
    }

    @Override public void savePurchaseFormV2(
            String receiptId, int itemOrdinal, CatalogField<PurchaseForm> purchaseForm) {
        SQLiteDatabase db = getWritableDatabase();
        db.beginTransaction();
        try {
            CatalogV2Persistence.savePurchaseForm(db, receiptId, itemOrdinal, purchaseForm);
            db.setTransactionSuccessful();
        } finally {
            db.endTransaction();
        }
    }

    @Override public CatalogField<PurchaseForm> purchaseFormV2(String receiptId, int itemOrdinal) {
        return CatalogV2Persistence.readPurchaseForm(getReadableDatabase(), receiptId, itemOrdinal);
    }

    private static void writeLink(SQLiteDatabase db, String receiptId, int ordinal, String productId, LinkSource linkSource) {
        ContentValues v = new ContentValues();
        v.put("receipt_id", receiptId);
        v.put("item_ordinal", ordinal);
        v.put("product_id", productId);
        v.put("link_source", linkSource.name());
        db.insertWithOnConflict("item_links", null, v, SQLiteDatabase.CONFLICT_REPLACE);
    }

    private static CatalogProduct byCanonical(SQLiteDatabase db, String key) {
        try (Cursor c = db.query("products", null, "canonical_key=?", new String[]{key}, null, null, null)) {
            return c.moveToFirst() ? readProduct(c) : null;
        }
    }

    private static CatalogProduct byId(SQLiteDatabase db, String id) {
        try (Cursor c = db.query("products", null, "id=?", new String[]{id}, null, null, null)) {
            return c.moveToFirst() ? readProduct(c) : null;
        }
    }

    private static CatalogProduct readProduct(Cursor c) {
        ProductType type;
        try {
            type = ProductType.valueOf(c.getString(c.getColumnIndexOrThrow("type")));
        } catch (Exception e) {
            type = ProductType.NON_STANDARD;
        }
        return new CatalogProduct(
                c.getString(c.getColumnIndexOrThrow("id")),
                type,
                c.getString(c.getColumnIndexOrThrow("canonical_name")),
                c.getLong(c.getColumnIndexOrThrow("created_at_ms")));
    }

    private static LinkSource source(String value) {
        try {
            return LinkSource.valueOf(value);
        } catch (Exception e) {
            return LinkSource.EXACT_ALIAS;
        }
    }
}
