package com.receiptledger.v1.performance;

import static org.junit.Assert.*;

import android.content.Context;
import android.database.Cursor;
import android.database.DatabaseUtils;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteStatement;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Debug;
import android.os.SystemClock;
import android.view.View;

import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.platform.app.InstrumentationRegistry;

import com.receiptledger.v1.archive.ImageArchivePolicy;
import com.receiptledger.v1.archive.ReceiptImageArchive;
import com.receiptledger.v1.archive.ReceiptRepository;
import com.receiptledger.v1.detail.ProductDetailServiceV1;
import com.receiptledger.v1.detail.ProductDetailV1;
import com.receiptledger.v1.detail.ProductPriceChartViewV1;
import com.receiptledger.v1.document.ProjectiveTransform;
import com.receiptledger.v1.item.ItemResolution;
import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.ocr.MlKitOcrEngine;
import com.receiptledger.v1.ocr.OcrDocument;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.persistence.ReceiptSchema;
import com.receiptledger.v1.persistence.SqliteReceiptStore;
import com.receiptledger.v1.priceeval.PriceEvaluationServiceV1;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.priceintel.PriceIntelligenceV2;
import com.receiptledger.v1.product.IdentityResolution;
import com.receiptledger.v1.product.ProductCatalogMigrationV2;
import com.receiptledger.v1.product.ProductCatalogSchema;
import com.receiptledger.v1.product.SqliteProductCatalogStore;
import com.receiptledger.v1.search.SearchBrowseQueryV1;
import com.receiptledger.v1.search.SearchBrowseResultV1;
import com.receiptledger.v1.search.SearchBrowseServiceV1;
import com.receiptledger.v1.validation.ValidationStatus;

import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Set;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;

import org.junit.Test;
import org.junit.runner.RunWith;

/** CP36 actual Android/SQLite/ML Kit runtime profile. */
@RunWith(AndroidJUnit4.class)
public final class PerformanceReliabilityInstrumentedTest {

    @Test public void canonicalAndroidRuntimeProfile() throws Exception {
        Context context = InstrumentationRegistry.getInstrumentation().getTargetContext();
        cleanup(context);

        SqliteScaleMetrics scale = measureSqliteSearchAndHistory(context);
        OcrMetrics ocr = measureOcr();
        MigrationMetrics migration = measureMigration(context);
        ArchiveMetrics archive = measureArchive(context);
        int reopenCycles = measureRepositoryAndReopen(context);

        String line = "CP36_ANDROID_METRICS version=1 "
                + "search_1k_ms=" + scale.search1kMs + " "
                + "search_10k_ms=" + scale.search10kMs + " "
                + "recent_10k_ms=" + scale.recent10kMs + " "
                + "search_10k_scanned=" + scale.search10kScanned + " "
                + "history_observations=" + scale.historyObservations + " "
                + "price_1k_ms=" + scale.price1kMs + " "
                + "detail_1k_ms=" + scale.detail1kMs + " "
                + "chart_1k_ms=" + scale.chart1kMs + " "
                + "ocr_cold_ms=" + ocr.coldMs + " "
                + "ocr_warm_median_ms=" + ocr.warmMedianMs + " "
                + "ocr_pss_before_kb=" + ocr.pssBeforeKb + " "
                + "ocr_pss_after_kb=" + ocr.pssAfterKb + " "
                + "migration_1k_ms=" + migration.elapsedMs + " "
                + "migration_rows=" + migration.rows + " "
                + "archive_files=" + archive.totalFiles + " "
                + "archive_removed=" + archive.removed + " "
                + "archive_ms=" + archive.elapsedMs + " "
                + "reopen_cycles=" + reopenCycles + " semantic_failures=0";
        File metrics = new File(context.getFilesDir(), "cp36-android-metrics.txt");
        try (FileWriter writer = new FileWriter(metrics, false)) {
            writer.write(line);
            writer.write('\n');
        }
        System.out.println(line);
    }

    private SqliteScaleMetrics measureSqliteSearchAndHistory(Context context) throws Exception {
        context.deleteDatabase(ReceiptSchema.DB_NAME);
        context.deleteDatabase(ProductCatalogSchema.DB_NAME);
        SqliteReceiptStore receipts = new SqliteReceiptStore(context);
        SqliteProductCatalogStore catalog = new SqliteProductCatalogStore(context);
        try {
            SQLiteDatabase rdb = receipts.getWritableDatabase();
            SQLiteDatabase pdb = catalog.getWritableDatabase();
            insertSearchRange(rdb, pdb, 0, 1_000);
            SearchBrowseServiceV1 discovery = discovery(receipts, catalog);

            long search1k = timeSearch(discovery, "상품00999", 1_000);

            insertSearchRange(rdb, pdb, 1_000, 10_000);
            long search10k = timeSearch(discovery, "상품09999", 10_000);
            long recent10k = timeRecent(discovery, "상품09999");

            insertHistory(rdb, pdb, 1_000);
            PriceIntelligenceServiceV2 priceService = new PriceIntelligenceServiceV2(receipts, catalog, catalog);
            long started = SystemClock.elapsedRealtimeNanos();
            PriceIntelligenceV2 intelligence = priceService.analyze("history-product");
            long priceMs = toMs(SystemClock.elapsedRealtimeNanos() - started);
            assertEquals(1_000, intelligence.observations.size());
            assertNotNull(intelligence.cohort("STANDARD_PACKAGE"));
            assertEquals(1_000, intelligence.cohort("STANDARD_PACKAGE").count());

            started = SystemClock.elapsedRealtimeNanos();
            ProductDetailV1 detail = new ProductDetailServiceV1(catalog, catalog, priceService).load("history-product");
            long detailMs = toMs(SystemClock.elapsedRealtimeNanos() - started);
            assertEquals(1_000, detail.purchases.size());
            assertEquals(1_000, detail.comparablePurchases().size());

            long chartMs = drawChart(detail, context);
            return new SqliteScaleMetrics(search1k, search10k, recent10k, 10_000,
                    intelligence.observations.size(), priceMs, detailMs, chartMs);
        } finally {
            catalog.close();
            receipts.close();
        }
    }

    private SearchBrowseServiceV1 discovery(SqliteReceiptStore receipts, SqliteProductCatalogStore catalog) {
        return new SearchBrowseServiceV1(
                receipts,
                catalog,
                catalog,
                new PriceIntelligenceServiceV2(receipts, catalog, catalog),
                new PriceEvaluationServiceV1());
    }

    private long timeSearch(SearchBrowseServiceV1 discovery, String target, int expectedScanned) {
        long started = SystemClock.elapsedRealtimeNanos();
        SearchBrowseResultV1 result = discovery.search(SearchBrowseQueryV1.text(target, 20));
        long elapsed = toMs(SystemClock.elapsedRealtimeNanos() - started);
        assertEquals(expectedScanned, result.catalogEntriesScanned);
        assertEquals(1, result.matchedEntriesBeforeLimit);
        assertEquals(1, result.returnedEntries);
        assertEquals(target, result.entries.get(0).canonicalName);
        return elapsed;
    }

    private long timeRecent(SearchBrowseServiceV1 discovery, String expectedNewest) {
        long started = SystemClock.elapsedRealtimeNanos();
        List<com.receiptledger.v1.search.SearchBrowseEntryV1> rows = discovery.recent(3);
        long elapsed = toMs(SystemClock.elapsedRealtimeNanos() - started);
        assertEquals(3, rows.size());
        assertEquals(expectedNewest, rows.get(0).canonicalName);
        return elapsed;
    }

    private static void insertSearchRange(SQLiteDatabase rdb, SQLiteDatabase pdb, int start, int end) {
        rdb.beginTransaction();
        pdb.beginTransaction();
        SQLiteStatement receipt = rdb.compileStatement(
                "INSERT INTO receipts(id,created_at_ms,purchase_date,store_name,raw_ocr_text,printed_total,item_line_sum,discount_sum,computed_net,difference,validation_status,source_width,source_height,perspective_corrected) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)");
        SQLiteStatement item = rdb.compileStatement(
                "INSERT INTO receipt_items(receipt_id,ordinal,row_index,name,quantity,unit_price,line_amount,quantity_origin,unit_price_origin,line_amount_origin,resolution,reason) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)");
        SQLiteStatement product = pdb.compileStatement(
                "INSERT INTO products(id,type,canonical_name,canonical_key,created_at_ms,record_origin) VALUES(?,?,?,?,?,?)");
        SQLiteStatement link = pdb.compileStatement(
                "INSERT INTO item_links(receipt_id,item_ordinal,product_id,link_source) VALUES(?,?,?,?)");
        try {
            for (int i = start; i < end; i++) {
                String suffix = String.format(Locale.ROOT, "%05d", i);
                String receiptId = "scale-r-" + suffix;
                String productId = "scale-p-" + suffix;
                String name = "상품" + suffix;
                long price = 1_000L + i;

                receipt.clearBindings();
                receipt.bindString(1, receiptId);
                receipt.bindLong(2, i + 1L);
                receipt.bindString(3, "2026-10-01");
                receipt.bindString(4, "가상마트");
                receipt.bindString(5, name);
                receipt.bindLong(6, price);
                receipt.bindLong(7, price);
                receipt.bindLong(8, 0L);
                receipt.bindLong(9, price);
                receipt.bindLong(10, 0L);
                receipt.bindString(11, "PASS");
                receipt.bindLong(12, 180L);
                receipt.bindLong(13, 240L);
                receipt.bindLong(14, 0L);
                receipt.executeInsert();

                item.clearBindings();
                item.bindString(1, receiptId);
                item.bindLong(2, 0L);
                item.bindLong(3, 0L);
                item.bindString(4, name);
                item.bindLong(5, 1L);
                item.bindLong(6, price);
                item.bindLong(7, price);
                item.bindString(8, "PRINTED");
                item.bindString(9, "PRINTED");
                item.bindString(10, "PRINTED");
                item.bindString(11, "EXACT");
                item.bindString(12, "CP36_SCALE");
                item.executeInsert();

                product.clearBindings();
                product.bindString(1, productId);
                product.bindString(2, "STANDARD");
                product.bindString(3, name);
                product.bindString(4, name);
                product.bindLong(5, i + 1L);
                product.bindString(6, "LEGACY_V1");
                product.executeInsert();

                link.clearBindings();
                link.bindString(1, receiptId);
                link.bindLong(2, 0L);
                link.bindString(3, productId);
                link.bindString(4, "USER_CONFIRMED");
                link.executeInsert();
            }
            rdb.setTransactionSuccessful();
            pdb.setTransactionSuccessful();
        } finally {
            receipt.close();
            item.close();
            product.close();
            link.close();
            pdb.endTransaction();
            rdb.endTransaction();
        }
    }

    private static void insertHistory(SQLiteDatabase rdb, SQLiteDatabase pdb, int count) {
        pdb.execSQL("INSERT INTO products(id,type,canonical_name,canonical_key,created_at_ms,record_origin) VALUES('history-product','STANDARD','장기우유1L','장기우유1l',20000,'LEGACY_V1')");
        rdb.beginTransaction();
        pdb.beginTransaction();
        SQLiteStatement receipt = rdb.compileStatement(
                "INSERT INTO receipts(id,created_at_ms,purchase_date,store_name,raw_ocr_text,printed_total,item_line_sum,discount_sum,computed_net,difference,validation_status,source_width,source_height,perspective_corrected) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)");
        SQLiteStatement item = rdb.compileStatement(
                "INSERT INTO receipt_items(receipt_id,ordinal,row_index,name,quantity,unit_price,line_amount,quantity_origin,unit_price_origin,line_amount_origin,resolution,reason) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)");
        SQLiteStatement link = pdb.compileStatement(
                "INSERT INTO item_links(receipt_id,item_ordinal,product_id,link_source) VALUES(?,?,?,?)");
        try {
            for (int i = 0; i < count; i++) {
                String receiptId = "history-r-" + String.format(Locale.ROOT, "%04d", i);
                long price = 2_000L + i;
                receipt.clearBindings();
                receipt.bindString(1, receiptId);
                receipt.bindLong(2, 20_000L + i);
                receipt.bindString(3, "2026-10-02");
                receipt.bindString(4, "가상마트");
                receipt.bindString(5, "장기우유1L");
                receipt.bindLong(6, price);
                receipt.bindLong(7, price);
                receipt.bindLong(8, 0L);
                receipt.bindLong(9, price);
                receipt.bindLong(10, 0L);
                receipt.bindString(11, "PASS");
                receipt.bindLong(12, 180L);
                receipt.bindLong(13, 240L);
                receipt.bindLong(14, 0L);
                receipt.executeInsert();

                item.clearBindings();
                item.bindString(1, receiptId);
                item.bindLong(2, 0L);
                item.bindLong(3, 0L);
                item.bindString(4, "장기우유1L");
                item.bindLong(5, 1L);
                item.bindLong(6, price);
                item.bindLong(7, price);
                item.bindString(8, "PRINTED");
                item.bindString(9, "PRINTED");
                item.bindString(10, "PRINTED");
                item.bindString(11, "EXACT");
                item.bindString(12, "CP36_HISTORY");
                item.executeInsert();

                link.clearBindings();
                link.bindString(1, receiptId);
                link.bindLong(2, 0L);
                link.bindString(3, "history-product");
                link.bindString(4, "USER_CONFIRMED");
                link.executeInsert();
            }
            rdb.setTransactionSuccessful();
            pdb.setTransactionSuccessful();
        } finally {
            receipt.close();
            item.close();
            link.close();
            pdb.endTransaction();
            rdb.endTransaction();
        }
    }

    private long drawChart(final ProductDetailV1 detail, final Context context) {
        final long[] elapsed = new long[1];
        final AtomicReference<Throwable> failure = new AtomicReference<>();
        InstrumentationRegistry.getInstrumentation().runOnMainSync(() -> {
            try {
                ProductPriceChartViewV1 chart = new ProductPriceChartViewV1(context);
                Bitmap output = Bitmap.createBitmap(1080, 660, Bitmap.Config.ARGB_8888);
                Canvas canvas = new Canvas(output);
                long started = SystemClock.elapsedRealtimeNanos();
                chart.setDetail(detail);
                chart.measure(
                        View.MeasureSpec.makeMeasureSpec(1080, View.MeasureSpec.EXACTLY),
                        View.MeasureSpec.makeMeasureSpec(660, View.MeasureSpec.EXACTLY));
                chart.layout(0, 0, 1080, 660);
                chart.draw(canvas);
                elapsed[0] = toMs(SystemClock.elapsedRealtimeNanos() - started);
                output.recycle();
            } catch (Throwable t) {
                failure.set(t);
            }
        });
        if (failure.get() != null) throw new AssertionError(failure.get());
        return elapsed[0];
    }

    private OcrMetrics measureOcr() throws Exception {
        Bitmap bitmap = syntheticReceiptBitmap();
        long before = Debug.getPss();
        MlKitOcrEngine engine = new MlKitOcrEngine();
        try {
            OcrRun cold = recognize(engine, bitmap);
            assertNotNull(cold.document);
            assertTrue(cold.document.rawText != null && !cold.document.rawText.trim().isEmpty());
            long[] warm = new long[3];
            for (int i = 0; i < warm.length; i++) {
                OcrRun run = recognize(engine, bitmap);
                assertNotNull(run.document);
                warm[i] = run.elapsedMs;
            }
            java.util.Arrays.sort(warm);
            long after = Debug.getPss();
            return new OcrMetrics(cold.elapsedMs, warm[1], before, after);
        } finally {
            engine.close();
            bitmap.recycle();
        }
    }

    private static OcrRun recognize(MlKitOcrEngine engine, Bitmap bitmap) throws Exception {
        CountDownLatch latch = new CountDownLatch(1);
        AtomicReference<OcrDocument> document = new AtomicReference<>();
        AtomicReference<Exception> error = new AtomicReference<>();
        long started = SystemClock.elapsedRealtimeNanos();
        engine.recognize(bitmap, ProjectiveTransform.identity(), new MlKitOcrEngine.Callback() {
            @Override public void onSuccess(OcrDocument result) {
                document.set(result);
                latch.countDown();
            }
            @Override public void onFailure(Exception failure) {
                error.set(failure);
                latch.countDown();
            }
        });
        assertTrue("OCR timeout", latch.await(20, TimeUnit.SECONDS));
        if (error.get() != null) throw error.get();
        return new OcrRun(toMs(SystemClock.elapsedRealtimeNanos() - started), document.get());
    }

    private static Bitmap syntheticReceiptBitmap() {
        Bitmap bitmap = Bitmap.createBitmap(1080, 1600, Bitmap.Config.ARGB_8888);
        Canvas canvas = new Canvas(bitmap);
        canvas.drawColor(Color.WHITE);
        Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
        paint.setColor(Color.BLACK);
        paint.setTextSize(52f);
        String[] lines = {
                "가상마트 영수증",
                "2026-10-16",
                "서울우유1L   1   3200",
                "신라면5입    1   4990",
                "감자 1kg     1   6000",
                "합계             14190"
        };
        float y = 150f;
        for (String line : lines) {
            canvas.drawText(line, 80f, y, paint);
            y += 130f;
        }
        return bitmap;
    }

    private MigrationMetrics measureMigration(Context context) {
        context.deleteDatabase(ProductCatalogSchema.DB_NAME);
        SQLiteDatabase legacy = context.openOrCreateDatabase(ProductCatalogSchema.DB_NAME, Context.MODE_PRIVATE, null);
        legacy.execSQL("PRAGMA foreign_keys=ON");
        legacy.execSQL("CREATE TABLE products (id TEXT PRIMARY KEY NOT NULL,type TEXT NOT NULL,canonical_name TEXT NOT NULL,canonical_key TEXT NOT NULL UNIQUE,created_at_ms INTEGER NOT NULL)");
        legacy.execSQL("CREATE TABLE aliases (alias_key TEXT PRIMARY KEY NOT NULL,raw_alias TEXT NOT NULL,product_id TEXT NOT NULL,FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)");
        legacy.execSQL("CREATE TABLE item_links (receipt_id TEXT NOT NULL,item_ordinal INTEGER NOT NULL,product_id TEXT NOT NULL,link_source TEXT NOT NULL,PRIMARY KEY(receipt_id,item_ordinal),FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE)");
        legacy.execSQL("CREATE INDEX idx_item_links_product ON item_links(product_id)");
        legacy.beginTransaction();
        SQLiteStatement product = legacy.compileStatement(
                "INSERT INTO products(id,type,canonical_name,canonical_key,created_at_ms) VALUES(?,?,?,?,?)");
        SQLiteStatement alias = legacy.compileStatement(
                "INSERT INTO aliases(alias_key,raw_alias,product_id) VALUES(?,?,?)");
        SQLiteStatement link = legacy.compileStatement(
                "INSERT INTO item_links(receipt_id,item_ordinal,product_id,link_source) VALUES(?,?,?,?)");
        try {
            for (int i = 0; i < 1_000; i++) {
                String suffix = String.format(Locale.ROOT, "%04d", i);
                String id = "m-p-" + suffix;
                String raw = "OLD-" + suffix;
                product.clearBindings();
                product.bindString(1, id);
                product.bindString(2, "STANDARD");
                product.bindString(3, "Migration " + suffix);
                product.bindString(4, com.receiptledger.v1.product.ProductNameNormalizer.key("Migration " + suffix));
                product.bindLong(5, i + 1L);
                product.executeInsert();
                alias.clearBindings();
                alias.bindString(1, com.receiptledger.v1.product.ProductNameNormalizer.key(raw));
                alias.bindString(2, raw);
                alias.bindString(3, id);
                alias.executeInsert();
                link.clearBindings();
                link.bindString(1, "m-r-" + suffix);
                link.bindLong(2, 0L);
                link.bindString(3, id);
                link.bindString(4, "USER_CONFIRMED");
                link.executeInsert();
            }
            legacy.setTransactionSuccessful();
        } finally {
            product.close();
            alias.close();
            link.close();
            legacy.endTransaction();
        }
        legacy.setVersion(1);
        legacy.close();

        long started = SystemClock.elapsedRealtimeNanos();
        SqliteProductCatalogStore migrated = new SqliteProductCatalogStore(context);
        SQLiteDatabase db = migrated.getWritableDatabase();
        long elapsed = toMs(SystemClock.elapsedRealtimeNanos() - started);
        try {
            assertEquals(2, db.getVersion());
            assertEquals(1_000L, DatabaseUtils.queryNumEntries(db, "products"));
            assertEquals(1_000L, DatabaseUtils.queryNumEntries(db, "aliases"));
            assertEquals(1_000L, DatabaseUtils.queryNumEntries(db, "item_links"));
            assertTrue(tableExists(db, "catalog_fields"));
            assertTrue(tableExists(db, "product_specifications"));
            assertTrue(tableExists(db, "category_refs"));
            assertTrue(tableExists(db, "observation_purchase_forms"));
            assertEquals("m-p-0999",
                    migrated.aliasCatalogEntryIdV2(com.receiptledger.v1.catalog.AliasContext.global(), "OLD-0999"));
            IdentityResolution linked = migrated.itemResolution("m-r-0999", 0);
            assertTrue(linked.classified());
            assertEquals("m-p-0999", linked.product.id);
            try {
                ProductCatalogMigrationV2.migrate(db, 2, 3);
                fail("unsupported migration must fail");
            } catch (IllegalStateException expected) {
                // expected
            }
        } finally {
            migrated.close();
        }
        return new MigrationMetrics(elapsed, 1_000);
    }

    private static boolean tableExists(SQLiteDatabase db, String name) {
        try (Cursor c = db.rawQuery(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", new String[]{name})) {
            return c.moveToFirst();
        }
    }

    private ArchiveMetrics measureArchive(Context context) throws Exception {
        File dir = new File(context.getFilesDir(), "receipt-images");
        deleteRecursively(dir);
        assertTrue(dir.mkdirs() || dir.isDirectory());
        Set<String> live = new HashSet<>();
        for (int i = 0; i < 1_000; i++) {
            String id = "live-" + i;
            live.add(id);
            touch(new File(dir, ImageArchivePolicy.fileName(id)));
        }
        for (int i = 0; i < 800; i++) {
            touch(new File(dir, ImageArchivePolicy.fileName("orphan-" + i)));
        }
        for (int i = 0; i < 200; i++) {
            touch(new File(dir, "stale.jpg.tmp-" + i));
        }
        int total = 2_000;
        ReceiptImageArchive archive = new ReceiptImageArchive(context);
        long started = SystemClock.elapsedRealtimeNanos();
        int removed = archive.reconcile(live);
        long elapsed = toMs(SystemClock.elapsedRealtimeNanos() - started);
        assertEquals(1_000, removed);
        for (String id : live) assertTrue(archive.exists(id));
        File[] remaining = dir.listFiles();
        assertNotNull(remaining);
        assertEquals(1_000, remaining.length);
        return new ArchiveMetrics(total, removed, elapsed);
    }

    private int measureRepositoryAndReopen(Context context) throws Exception {
        context.deleteDatabase(ReceiptSchema.DB_NAME);
        File dir = new File(context.getFilesDir(), "receipt-images");
        deleteRecursively(dir);
        ReceiptRecord record = syntheticRecord("reopen-receipt");
        Bitmap image = Bitmap.createBitmap(320, 480, Bitmap.Config.ARGB_8888);
        new Canvas(image).drawColor(Color.WHITE);
        ReceiptRepository first = new ReceiptRepository(context);
        first.save(record, image);
        first.close();
        image.recycle();

        ReceiptRepository reopened = new ReceiptRepository(context);
        try {
            assertNotNull(reopened.get(record.id));
            Bitmap sampled = reopened.loadImage(record.id, 256);
            assertNotNull(sampled);
            sampled.recycle();
            assertTrue(reopened.hasImage(record.id));
            new ReceiptImageArchive(context).delete(record.id);
            assertNotNull(reopened.get(record.id));
            assertNull(reopened.loadImage(record.id, 256));
            assertTrue(reopened.delete(record.id));
            assertNull(reopened.get(record.id));
            assertFalse(reopened.hasImage(record.id));
        } finally {
            reopened.close();
        }

        for (int i = 0; i < 10; i++) {
            SqliteReceiptStore receipts = new SqliteReceiptStore(context);
            SqliteProductCatalogStore catalog = new SqliteProductCatalogStore(context);
            try {
                assertTrue(receipts.count() >= 0);
                assertNotNull(catalog.listProducts());
            } finally {
                catalog.close();
                receipts.close();
            }
        }
        return 10;
    }

    private static ReceiptRecord syntheticRecord(String id) {
        PersistedItem item = new PersistedItem(
                0, 0, "테스트상품", 1, 3_200L, 3_200L,
                ValueOrigin.PRINTED, ValueOrigin.PRINTED, ValueOrigin.PRINTED,
                ItemResolution.EXACT, "CP36_REOPEN");
        return new ReceiptRecord(
                id, 1L, "2026-10-16", "가상마트", "테스트상품 3200",
                3_200L, 3_200L, 0L, 3_200L, 0L,
                ValidationStatus.PASS, 320, 480, false,
                Collections.<String>emptyList(), Collections.singletonList(item));
    }

    private static void touch(File file) throws Exception {
        try (FileOutputStream out = new FileOutputStream(file)) {
            out.write(0);
        }
    }

    private static void deleteRecursively(File file) {
        if (file == null || !file.exists()) return;
        if (file.isDirectory()) {
            File[] children = file.listFiles();
            if (children != null) for (File child : children) deleteRecursively(child);
        }
        if (!file.delete() && file.exists()) {
            throw new IllegalStateException("cannot delete " + file);
        }
    }

    private static void cleanup(Context context) {
        context.deleteDatabase(ReceiptSchema.DB_NAME);
        context.deleteDatabase(ProductCatalogSchema.DB_NAME);
        deleteRecursively(new File(context.getFilesDir(), "receipt-images"));
        File metrics = new File(context.getFilesDir(), "cp36-android-metrics.txt");
        if (metrics.exists()) metrics.delete();
    }

    private static long toMs(long nanos) {
        return Math.max(0L, nanos / 1_000_000L);
    }

    private static final class SqliteScaleMetrics {
        final long search1kMs;
        final long search10kMs;
        final long recent10kMs;
        final int search10kScanned;
        final int historyObservations;
        final long price1kMs;
        final long detail1kMs;
        final long chart1kMs;
        SqliteScaleMetrics(long search1kMs, long search10kMs, long recent10kMs,
                int search10kScanned, int historyObservations, long price1kMs,
                long detail1kMs, long chart1kMs) {
            this.search1kMs = search1kMs;
            this.search10kMs = search10kMs;
            this.recent10kMs = recent10kMs;
            this.search10kScanned = search10kScanned;
            this.historyObservations = historyObservations;
            this.price1kMs = price1kMs;
            this.detail1kMs = detail1kMs;
            this.chart1kMs = chart1kMs;
        }
    }

    private static final class OcrRun {
        final long elapsedMs;
        final OcrDocument document;
        OcrRun(long elapsedMs, OcrDocument document) {
            this.elapsedMs = elapsedMs;
            this.document = document;
        }
    }

    private static final class OcrMetrics {
        final long coldMs;
        final long warmMedianMs;
        final long pssBeforeKb;
        final long pssAfterKb;
        OcrMetrics(long coldMs, long warmMedianMs, long pssBeforeKb, long pssAfterKb) {
            this.coldMs = coldMs;
            this.warmMedianMs = warmMedianMs;
            this.pssBeforeKb = pssBeforeKb;
            this.pssAfterKb = pssAfterKb;
        }
    }

    private static final class MigrationMetrics {
        final long elapsedMs;
        final int rows;
        MigrationMetrics(long elapsedMs, int rows) {
            this.elapsedMs = elapsedMs;
            this.rows = rows;
        }
    }

    private static final class ArchiveMetrics {
        final int totalFiles;
        final int removed;
        final long elapsedMs;
        ArchiveMetrics(int totalFiles, int removed, long elapsedMs) {
            this.totalFiles = totalFiles;
            this.removed = removed;
            this.elapsedMs = elapsedMs;
        }
    }
}
