package com.receiptledger.v1.performance;

import static org.junit.Assert.*;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;

import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.platform.app.InstrumentationRegistry;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.category.CategoryTaxonomyV1;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.persistence.ReceiptStore;
import com.receiptledger.v1.persistence.SqliteReceiptStore;
import com.receiptledger.v1.priceeval.PriceEvaluationServiceV1;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.product.CatalogProduct;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.IdentityResolution;
import com.receiptledger.v1.product.ItemLinkRef;
import com.receiptledger.v1.product.ProductCatalogSchema;
import com.receiptledger.v1.product.ProductCatalogStore;
import com.receiptledger.v1.product.ProductNameNormalizer;
import com.receiptledger.v1.product.SqliteProductCatalogStore;
import com.receiptledger.v1.search.SearchBrowseEntryV1;
import com.receiptledger.v1.search.SearchBrowseQueryV1;
import com.receiptledger.v1.search.SearchBrowseResultV1;
import com.receiptledger.v1.search.SearchBrowseServiceV1;
import com.receiptledger.v1.validation.ValidationStatus;

import java.util.List;
import java.util.Set;

import org.junit.Test;
import org.junit.runner.RunWith;

/** Direct semantic parity proof for the CP36 SQLite-only CP29 fast path. */
@RunWith(AndroidJUnit4.class)
public final class SearchBrowseSqliteParityInstrumentedTest {

    @Test public void sqliteFastPathMatchesFrozenGenericPathAndFailFastIntegrity() {
        Context context = InstrumentationRegistry.getInstrumentation().getTargetContext();
        context.deleteDatabase("receiptledger-v1.db");
        context.deleteDatabase(ProductCatalogSchema.DB_NAME);

        SqliteReceiptStore receipts = new SqliteReceiptStore(context);
        SqliteProductCatalogStore products = new SqliteProductCatalogStore(context);
        try {
            seed(receipts.getWritableDatabase(), products.getWritableDatabase());

            SearchBrowseServiceV1 fast = service(receipts, products, products);
            ReceiptStoreAdapter receiptAdapter = new ReceiptStoreAdapter(receipts);
            ProductStoreAdapter productAdapter = new ProductStoreAdapter(products);
            SearchBrowseServiceV1 frozen = service(receiptAdapter, productAdapter, productAdapter);

            assertResultSame(
                    frozen.search(SearchBrowseQueryV1.text("서울우유 나100% 1L", 20)),
                    fast.search(SearchBrowseQueryV1.text("서울우유 나100% 1L", 20)));
            assertResultSame(
                    frozen.search(SearchBrowseQueryV1.text("서울 우유 나100% 1L", 20)),
                    fast.search(SearchBrowseQueryV1.text("서울 우유 나100% 1L", 20)));
            assertResultSame(
                    frozen.search(SearchBrowseQueryV1.text("서울우유", 20)),
                    fast.search(SearchBrowseQueryV1.text("서울우유", 20)));
            assertResultSame(
                    frozen.search(SearchBrowseQueryV1.text("1000ML", 20)),
                    fast.search(SearchBrowseQueryV1.text("1000ML", 20)));
            assertResultSame(
                    frozen.search(SearchBrowseQueryV1.text("행사우유", 20)),
                    fast.search(SearchBrowseQueryV1.text("행사우유", 20)));
            assertResultSame(
                    frozen.search(SearchBrowseQueryV1.text("이마트 강서", 20)),
                    fast.search(SearchBrowseQueryV1.text("이마트 강서", 20)));
            assertResultSame(
                    frozen.search(new SearchBrowseQueryV1(null, null, "  이마트   강서  ", null, 20)),
                    fast.search(new SearchBrowseQueryV1(null, null, "  이마트   강서  ", null, 20)));
            assertEntriesSame(
                    frozen.byCategory(CategoryTaxonomyV1.FOOD_DAIRY, 20),
                    fast.byCategory(CategoryTaxonomyV1.FOOD_DAIRY, 20));
            assertEntriesSame(frozen.recent(20), fast.recent(20));
            assertEntriesSame(frozen.frequent(20), fast.frequent(20));

            SQLiteDatabase pdb = products.getWritableDatabase();
            pdb.execSQL("UPDATE catalog_fields SET source='UNKNOWN' WHERE product_id='p-milk' AND field_code='BRAND'");
            assertIntegrityFailure(frozen);
            assertIntegrityFailure(fast);
            pdb.execSQL("UPDATE catalog_fields SET source='USER_CONFIRMED' WHERE product_id='p-milk' AND field_code='BRAND'");

            System.out.println("CP36_SEARCH_PARITY cases=10 result_equivalent=1 fail_fast_equivalent=1");
        } finally {
            products.close();
            receipts.close();
            context.deleteDatabase("receiptledger-v1.db");
            context.deleteDatabase(ProductCatalogSchema.DB_NAME);
        }
    }

    private static SearchBrowseServiceV1 service(
            ReceiptStore receipts,
            ProductCatalogStore products,
            CatalogV2PersistenceStore v2) {
        return new SearchBrowseServiceV1(
                receipts,
                products,
                v2,
                new PriceIntelligenceServiceV2(receipts, products, v2),
                new PriceEvaluationServiceV1());
    }

    private static void seed(SQLiteDatabase rdb, SQLiteDatabase pdb) {
        insertReceipt(rdb, "r-milk-1", 1L, "2026-10-01", "이마트 강서", "행사우유", 3000L);
        insertReceipt(rdb, "r-potato", 2L, "2026-10-03", "시장", "감자1봉", 5000L);
        insertReceipt(rdb, "r-milk-2", 3L, "2026-10-05", "이마트 강서", "서울우유행사", 3100L);

        pdb.execSQL(
                "INSERT INTO products(id,type,canonical_name,canonical_key,created_at_ms,record_origin) VALUES(?,?,?,?,?,?)",
                new Object[]{"p-milk", "STANDARD", "서울우유 나100% 1L",
                        ProductNameNormalizer.key("서울우유 나100% 1L"), 1L, "NATIVE_V2"});
        pdb.execSQL(
                "INSERT INTO products(id,type,canonical_name,canonical_key,created_at_ms,record_origin) VALUES(?,?,?,?,?,?)",
                new Object[]{"p-potato", "NON_STANDARD", "감자", ProductNameNormalizer.key("감자"), 2L, "NATIVE_V2"});

        insertField(pdb, "p-milk", "BRAND", "서울우유");
        insertField(pdb, "p-milk", "PRODUCT_NAME", "나100%");
        pdb.execSQL(
                "INSERT INTO product_specifications(product_id,net_amount,net_unit,pack_count,inner_amount,inner_unit,source,confidence,confirmation) VALUES(?,?,?,?,?,?,?,?,?)",
                new Object[]{"p-milk", "1", "LITER", null, null, null, "USER_CONFIRMED", "HIGH", "CONFIRMED"});
        pdb.execSQL(
                "INSERT INTO category_refs(product_id,category_id) VALUES(?,?)",
                new Object[]{"p-milk", CategoryTaxonomyV1.FOOD_DAIRY_MILK});
        pdb.execSQL(
                "INSERT INTO category_refs(product_id,category_id) VALUES(?,?)",
                new Object[]{"p-potato", CategoryTaxonomyV1.FOOD_PRODUCE_VEGETABLE});

        insertLink(pdb, "r-milk-1", 0, "p-milk", "USER_CONFIRMED");
        insertLink(pdb, "r-milk-2", 0, "p-milk", "EXACT_ALIAS");
        insertLink(pdb, "r-potato", 0, "p-potato", "USER_CONFIRMED");
    }

    private static void insertReceipt(
            SQLiteDatabase db,
            String id,
            long created,
            String date,
            String store,
            String itemName,
            long price) {
        db.execSQL(
                "INSERT INTO receipts(id,created_at_ms,purchase_date,store_name,raw_ocr_text,printed_total,item_line_sum,discount_sum,computed_net,difference,validation_status,source_width,source_height,perspective_corrected) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                new Object[]{id, created, date, store, itemName, price, price, 0L, price, 0L,
                        ValidationStatus.PASS.name(), 1080, 1600, 0});
        db.execSQL(
                "INSERT INTO receipt_items(receipt_id,ordinal,row_index,name,quantity,unit_price,line_amount,quantity_origin,unit_price_origin,line_amount_origin,resolution,reason) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                new Object[]{id, 0, 0, itemName, 1, price, price, "PRINTED", "PRINTED", "PRINTED", "EXACT", "CP36_PARITY"});
    }

    private static void insertField(SQLiteDatabase db, String productId, String code, String value) {
        db.execSQL(
                "INSERT INTO catalog_fields(product_id,field_code,value_text,value_key,source,confidence,confirmation) VALUES(?,?,?,?,?,?,?)",
                new Object[]{productId, code, value, ProductNameNormalizer.key(value), "USER_CONFIRMED", "HIGH", "CONFIRMED"});
    }

    private static void insertLink(SQLiteDatabase db, String receiptId, int ordinal, String productId, String source) {
        db.execSQL(
                "INSERT INTO item_links(receipt_id,item_ordinal,product_id,link_source) VALUES(?,?,?,?)",
                new Object[]{receiptId, ordinal, productId, source});
    }

    private static void assertIntegrityFailure(SearchBrowseServiceV1 service) {
        try {
            service.search(SearchBrowseQueryV1.text("서울우유", 20));
            fail("corrupt present catalog field must fail fast");
        } catch (IllegalArgumentException expected) {
            // expected
        }
    }

    private static void assertResultSame(SearchBrowseResultV1 expected, SearchBrowseResultV1 actual) {
        assertEquals(expected.normalizedQuery, actual.normalizedQuery);
        assertEquals(expected.catalogEntriesScanned, actual.catalogEntriesScanned);
        assertEquals(expected.matchedEntriesBeforeLimit, actual.matchedEntriesBeforeLimit);
        assertEquals(expected.returnedEntries, actual.returnedEntries);
        assertEntriesSame(expected.entries, actual.entries);
    }

    private static void assertEntriesSame(List<SearchBrowseEntryV1> expected, List<SearchBrowseEntryV1> actual) {
        assertEquals(expected.size(), actual.size());
        for (int i = 0; i < expected.size(); i++) assertEntrySame(expected.get(i), actual.get(i));
    }

    private static void assertEntrySame(SearchBrowseEntryV1 expected, SearchBrowseEntryV1 actual) {
        assertEquals(expected.productId, actual.productId);
        assertEquals(expected.type, actual.type);
        assertEquals(expected.canonicalName, actual.canonicalName);
        assertEquals(expected.brand, actual.brand);
        assertEquals(expected.productName, actual.productName);
        assertEquals(expected.variant, actual.variant);
        assertEquals(expected.specificationSummary, actual.specificationSummary);
        assertEquals(expected.categoryId, actual.categoryId);
        assertEquals(expected.categoryPath, actual.categoryPath);
        assertEquals(expected.observedItemNames, actual.observedItemNames);
        assertEquals(expected.stores, actual.stores);
        assertEquals(expected.purchaseCount, actual.purchaseCount);
        assertEquals(expected.latestPurchaseDate, actual.latestPurchaseDate);
        assertEquals(expected.latestStoreName, actual.latestStoreName);
        assertEquals(expected.latestCreatedAtMillis, actual.latestCreatedAtMillis);
        assertEquals(expected.relevanceScore, actual.relevanceScore);
        assertEquals(expected.matchReason, actual.matchReason);
    }

    private static final class ReceiptStoreAdapter implements ReceiptStore {
        private final SqliteReceiptStore delegate;
        ReceiptStoreAdapter(SqliteReceiptStore delegate) { this.delegate = delegate; }
        @Override public void save(ReceiptRecord record) { delegate.save(record); }
        @Override public ReceiptRecord get(String id) { return delegate.get(id); }
        @Override public List<ReceiptRecord> listNewestFirst(int limit) { return delegate.listNewestFirst(limit); }
        @Override public Set<String> ids() { return delegate.ids(); }
        @Override public int count() { return delegate.count(); }
        @Override public boolean delete(String id) { return delegate.delete(id); }
        @Override public void close() { }
    }

    private static final class ProductStoreAdapter implements ProductCatalogStore, CatalogV2PersistenceStore {
        private final SqliteProductCatalogStore delegate;
        ProductStoreAdapter(SqliteProductCatalogStore delegate) { this.delegate = delegate; }
        @Override public IdentityResolution confirm(String receiptId, int itemOrdinal, String rawAlias,
                com.receiptledger.v1.product.ProductType type, String canonicalName, long now) {
            return delegate.confirm(receiptId, itemOrdinal, rawAlias, type, canonicalName, now);
        }
        @Override public IdentityResolution resolveAndLinkExact(String receiptId, int itemOrdinal, String rawAlias) {
            return delegate.resolveAndLinkExact(receiptId, itemOrdinal, rawAlias);
        }
        @Override public IdentityResolution itemResolution(String receiptId, int itemOrdinal) {
            return delegate.itemResolution(receiptId, itemOrdinal);
        }
        @Override public CatalogProduct product(String productId) { return delegate.product(productId); }
        @Override public List<CatalogProduct> listProducts() { return delegate.listProducts(); }
        @Override public List<ItemLinkRef> linksForProduct(String productId) { return delegate.linksForProduct(productId); }
        @Override public void unlinkItem(String receiptId, int itemOrdinal) { delegate.unlinkItem(receiptId, itemOrdinal); }
        @Override public void unlinkReceipt(String receiptId) { delegate.unlinkReceipt(receiptId); }
        @Override public CatalogEntryV2 catalogEntryV2(String catalogEntryId) { return delegate.catalogEntryV2(catalogEntryId); }
        @Override public void saveCatalogEntryV2(CatalogEntryV2 entry) { delegate.saveCatalogEntryV2(entry); }
        @Override public void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId) {
            delegate.saveAliasV2(context, rawAlias, catalogEntryId);
        }
        @Override public String aliasCatalogEntryIdV2(AliasContext context, String rawAlias) {
            return delegate.aliasCatalogEntryIdV2(context, rawAlias);
        }
        @Override public void savePurchaseFormV2(String receiptId, int itemOrdinal, CatalogField<PurchaseForm> purchaseForm) {
            delegate.savePurchaseFormV2(receiptId, itemOrdinal, purchaseForm);
        }
        @Override public CatalogField<PurchaseForm> purchaseFormV2(String receiptId, int itemOrdinal) {
            return delegate.purchaseFormV2(receiptId, itemOrdinal);
        }
        @Override public void close() { }
    }
}
