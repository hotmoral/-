package com.receiptledger.v1.performance;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.detail.ProductDetailServiceV1;
import com.receiptledger.v1.detail.ProductDetailV1;
import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.item.ItemResolution;
import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.ocr.OcrBlock;
import com.receiptledger.v1.ocr.OcrDocument;
import com.receiptledger.v1.ocr.OcrElement;
import com.receiptledger.v1.ocr.OcrLine;
import com.receiptledger.v1.persistence.InMemoryReceiptStore;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.persistence.ReceiptStore;
import com.receiptledger.v1.priceeval.PriceEvaluationServiceV1;
import com.receiptledger.v1.priceintel.PriceCohortV2;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.priceintel.PriceIntelligenceV2;
import com.receiptledger.v1.product.CatalogProduct;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.IdentityResolution;
import com.receiptledger.v1.product.InMemoryProductCatalogStore;
import com.receiptledger.v1.product.ItemLinkRef;
import com.receiptledger.v1.product.ProductCatalogStore;
import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.recovery.RecognitionCandidate;
import com.receiptledger.v1.recovery.RecognitionPass;
import com.receiptledger.v1.recovery.ReceiptRecognitionPipeline;
import com.receiptledger.v1.search.SearchBrowseEntryV1;
import com.receiptledger.v1.search.SearchBrowseQueryV1;
import com.receiptledger.v1.search.SearchBrowseResultV1;
import com.receiptledger.v1.search.SearchBrowseServiceV1;
import com.receiptledger.v1.validation.ValidationStatus;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Locale;
import java.util.Set;

import org.junit.Test;

/** CP36 deterministic structural scaling and reliability measurements. */
public final class PerformanceReliabilityV1Test {

    @Test public void canonicalStructuralScalingAndRecoveryAreDeterministic() {
        ScaleResult oneK = measureSearchScale(1_000);
        ScaleResult tenK = measureSearchScale(10_000);

        assertEquals(1_000, oneK.catalogScanned);
        assertEquals(10_000, tenK.catalogScanned);
        assertEquals(1_000, oneK.linkReads);
        assertEquals(10_000, tenK.linkReads);
        assertEquals(1_000, oneK.receiptReads);
        assertEquals(10_000, tenK.receiptReads);
        assertEquals(1_000, oneK.catalogV2Reads);
        assertEquals(10_000, tenK.catalogV2Reads);
        assertEquals(10, tenK.linkReads / oneK.linkReads);
        assertEquals(10, tenK.receiptReads / oneK.receiptReads);
        assertEquals(10, tenK.catalogV2Reads / oneK.catalogV2Reads);

        HistoryResult history = measureLongHistory(1_000);
        assertEquals(1_000, history.observations);
        assertEquals(1_000, history.detailRows);
        assertEquals(1_000, history.receiptReads);
        assertEquals(1_000, history.purchaseFormReads);
        assertEquals(1_999L, history.latestPrice);
        assertEquals(1_998L, history.previousPrice);

        int recoveryRepeats = assertRecoveryDeterministic(50);

        System.out.println(
                "CP36_JVM_METRICS version=1 "
                + "search_1k_products=" + oneK.catalogScanned + " "
                + "search_1k_link_reads=" + oneK.linkReads + " "
                + "search_1k_receipt_reads=" + oneK.receiptReads + " "
                + "search_1k_v2_reads=" + oneK.catalogV2Reads + " "
                + "search_1k_ms=" + oneK.elapsedMs + " "
                + "search_10k_products=" + tenK.catalogScanned + " "
                + "search_10k_link_reads=" + tenK.linkReads + " "
                + "search_10k_receipt_reads=" + tenK.receiptReads + " "
                + "search_10k_v2_reads=" + tenK.catalogV2Reads + " "
                + "search_10k_ms=" + tenK.elapsedMs + " "
                + "recent_10k_ms=" + tenK.recentElapsedMs + " "
                + "history_observations=" + history.observations + " "
                + "history_receipt_reads=" + history.receiptReads + " "
                + "history_form_reads=" + history.purchaseFormReads + " "
                + "history_price_ms=" + history.priceElapsedMs + " "
                + "history_detail_ms=" + history.detailElapsedMs + " "
                + "recovery_repeats=" + recoveryRepeats + " semantic_failures=0");
    }

    private static ScaleResult measureSearchScale(int count) {
        CountingReceiptStore receipts = new CountingReceiptStore();
        CountingProductCatalogStore catalog = new CountingProductCatalogStore();
        CountingV2Store v2 = new CountingV2Store();
        for (int i = 0; i < count; i++) {
            String suffix = String.format(Locale.ROOT, "%05d", i);
            String receiptId = "scale-r-" + suffix;
            String name = "상품" + suffix;
            long price = 1_000L + i;
            receipts.save(receipt(receiptId, i + 1L, name, price));
            catalog.confirm(receiptId, 0, name, ProductType.STANDARD, name, i + 1L);
        }
        SearchBrowseServiceV1 service = new SearchBrowseServiceV1(
                receipts,
                catalog,
                v2,
                new PriceIntelligenceServiceV2(receipts, catalog, v2),
                new PriceEvaluationServiceV1());

        receipts.resetCounts();
        catalog.resetCounts();
        v2.resetCounts();
        String target = "상품" + String.format(Locale.ROOT, "%05d", count - 1);
        long started = System.nanoTime();
        SearchBrowseResultV1 result = service.search(SearchBrowseQueryV1.text(target, 20));
        long searchMs = nanosToMs(System.nanoTime() - started);
        assertEquals(count, result.catalogEntriesScanned);
        assertEquals(1, result.matchedEntriesBeforeLimit);
        assertEquals(1, result.returnedEntries);
        assertEquals(target, result.entries.get(0).canonicalName);
        int links = catalog.linkReads;
        int receiptReads = receipts.getCalls;
        int v2Reads = v2.catalogEntryReads;
        assertEquals(1, catalog.listCalls);

        receipts.resetCounts();
        catalog.resetCounts();
        v2.resetCounts();
        started = System.nanoTime();
        List<SearchBrowseEntryV1> recent = service.recent(3);
        long recentMs = nanosToMs(System.nanoTime() - started);
        assertEquals(3, recent.size());
        assertEquals(target, recent.get(0).canonicalName);
        assertEquals(count, catalog.linkReads);
        assertEquals(count, receipts.getCalls);
        assertEquals(count, v2.catalogEntryReads);

        return new ScaleResult(count, links, receiptReads, v2Reads, searchMs, recentMs);
    }

    private static HistoryResult measureLongHistory(int count) {
        CountingReceiptStore receipts = new CountingReceiptStore();
        CountingProductCatalogStore catalog = new CountingProductCatalogStore();
        CountingV2Store v2 = new CountingV2Store();
        String rawAlias = "장기우유1L";
        String productId = null;
        for (int i = 0; i < count; i++) {
            String receiptId = "history-r-" + String.format(Locale.ROOT, "%04d", i);
            long price = 1_000L + i;
            receipts.save(receipt(receiptId, i + 1L, rawAlias, price));
            IdentityResolution resolution;
            if (i == 0) {
                resolution = catalog.confirm(receiptId, 0, rawAlias,
                        ProductType.STANDARD, "장기 우유 1L", i + 1L);
                productId = resolution.product.id;
            } else {
                resolution = catalog.resolveAndLinkExact(receiptId, 0, rawAlias);
                assertTrue(resolution.classified());
                assertEquals(productId, resolution.product.id);
            }
        }

        PriceIntelligenceServiceV2 priceService = new PriceIntelligenceServiceV2(receipts, catalog, v2);
        receipts.resetCounts();
        catalog.resetCounts();
        v2.resetCounts();
        long started = System.nanoTime();
        PriceIntelligenceV2 intelligence = priceService.analyze(productId);
        long priceMs = nanosToMs(System.nanoTime() - started);
        PriceCohortV2 cohort = intelligence.cohort("STANDARD_PACKAGE");
        assertNotNull(cohort);
        assertEquals(count, cohort.count());
        assertEquals(0, cohort.latest.longValue() - (1_000L + count - 1));
        assertEquals(0, cohort.previous.longValue() - (1_000L + count - 2));
        int receiptReads = receipts.getCalls;
        int formReads = v2.purchaseFormReads;

        receipts.resetCounts();
        catalog.resetCounts();
        v2.resetCounts();
        started = System.nanoTime();
        ProductDetailV1 detail = new ProductDetailServiceV1(catalog, v2, priceService).load(productId);
        long detailMs = nanosToMs(System.nanoTime() - started);
        assertEquals(count, detail.purchases.size());
        assertEquals(count, detail.comparablePurchases().size());

        return new HistoryResult(
                intelligence.observations.size(),
                detail.purchases.size(),
                receiptReads,
                formReads,
                cohort.latest.longValue(),
                cohort.previous.longValue(),
                priceMs,
                detailMs);
    }

    private static int assertRecoveryDeterministic(int repeats) {
        OcrDocument document = deterministicDocument();
        ReceiptRecognitionPipeline pipeline = new ReceiptRecognitionPipeline();
        RecognitionCandidate baseline = pipeline.evaluate(RecognitionPass.ORIGINAL, document);
        for (int i = 0; i < repeats; i++) {
            RecognitionCandidate next = pipeline.evaluate(RecognitionPass.ORIGINAL, document);
            assertEquals(baseline.score, next.score);
            assertEquals(baseline.validation.status, next.validation.status);
            assertEquals(baseline.items.items.size(), next.items.items.size());
            assertEquals(baseline.items.exactCount, next.items.exactCount);
            assertEquals(baseline.items.inferredCount, next.items.inferredCount);
            assertEquals(baseline.items.partialCount, next.items.partialCount);
            assertEquals(baseline.document.rawText, next.document.rawText);
            assertEquals(baseline.structure.totalAmount, next.structure.totalAmount);
        }
        return repeats;
    }

    private static OcrDocument deterministicDocument() {
        List<OcrElement> elements = new ArrayList<>();
        elements.add(token("가상마트", 10, 10, 60));
        elements.add(token("2026-10-16", 10, 30, 80));
        elements.add(token("우유", 10, 55, 30));
        elements.add(token("3200", 70, 55, 28));
        elements.add(token("1", 110, 55, 10));
        elements.add(token("3200", 135, 55, 28));
        elements.add(token("합계", 10, 85, 30));
        elements.add(token("3200", 135, 85, 28));
        OcrLine line = new OcrLine("synthetic", null, null, elements);
        OcrBlock block = new OcrBlock("synthetic", null, null, Collections.singletonList(line));
        return new OcrDocument("가상마트 2026-10-16 우유 3200 1 3200 합계 3200",
                180, 120, Collections.singletonList(block));
    }

    private static OcrElement token(String text, double x, double y, double width) {
        Quad q = new Quad(
                new PointD(x, y),
                new PointD(x + width, y),
                new PointD(x + width, y + 10),
                new PointD(x, y + 10));
        return new OcrElement(text, q, q);
    }

    private static ReceiptRecord receipt(String id, long createdAt, String name, long price) {
        PersistedItem item = new PersistedItem(
                0, 0, name, 1, price, price,
                ValueOrigin.PRINTED, ValueOrigin.PRINTED, ValueOrigin.PRINTED,
                ItemResolution.EXACT, "CP36_SYNTHETIC");
        return new ReceiptRecord(
                id,
                createdAt,
                "2026-10-01",
                "가상마트",
                name,
                price,
                price,
                0L,
                price,
                0L,
                ValidationStatus.PASS,
                180,
                240,
                false,
                Collections.<String>emptyList(),
                Collections.singletonList(item));
    }

    private static long nanosToMs(long nanos) {
        return Math.max(0L, nanos / 1_000_000L);
    }

    private static final class ScaleResult {
        final int catalogScanned;
        final int linkReads;
        final int receiptReads;
        final int catalogV2Reads;
        final long elapsedMs;
        final long recentElapsedMs;
        ScaleResult(int catalogScanned, int linkReads, int receiptReads, int catalogV2Reads,
                long elapsedMs, long recentElapsedMs) {
            this.catalogScanned = catalogScanned;
            this.linkReads = linkReads;
            this.receiptReads = receiptReads;
            this.catalogV2Reads = catalogV2Reads;
            this.elapsedMs = elapsedMs;
            this.recentElapsedMs = recentElapsedMs;
        }
    }

    private static final class HistoryResult {
        final int observations;
        final int detailRows;
        final int receiptReads;
        final int purchaseFormReads;
        final long latestPrice;
        final long previousPrice;
        final long priceElapsedMs;
        final long detailElapsedMs;
        HistoryResult(int observations, int detailRows, int receiptReads, int purchaseFormReads,
                long latestPrice, long previousPrice, long priceElapsedMs, long detailElapsedMs) {
            this.observations = observations;
            this.detailRows = detailRows;
            this.receiptReads = receiptReads;
            this.purchaseFormReads = purchaseFormReads;
            this.latestPrice = latestPrice;
            this.previousPrice = previousPrice;
            this.priceElapsedMs = priceElapsedMs;
            this.detailElapsedMs = detailElapsedMs;
        }
    }

    private static final class CountingReceiptStore implements ReceiptStore {
        final InMemoryReceiptStore delegate = new InMemoryReceiptStore();
        int getCalls;
        int listCalls;
        @Override public void save(ReceiptRecord record) { delegate.save(record); }
        @Override public ReceiptRecord get(String id) { getCalls++; return delegate.get(id); }
        @Override public List<ReceiptRecord> listNewestFirst(int limit) {
            listCalls++;
            return delegate.listNewestFirst(limit);
        }
        @Override public Set<String> ids() { return delegate.ids(); }
        @Override public int count() { return delegate.count(); }
        @Override public boolean delete(String id) { return delegate.delete(id); }
        @Override public void close() { delegate.close(); }
        void resetCounts() { getCalls = 0; listCalls = 0; }
    }

    private static final class CountingProductCatalogStore implements ProductCatalogStore {
        final InMemoryProductCatalogStore delegate = new InMemoryProductCatalogStore();
        int listCalls;
        int linkReads;
        @Override public IdentityResolution confirm(String receiptId, int itemOrdinal, String rawAlias,
                ProductType type, String canonicalName, long now) {
            return delegate.confirm(receiptId, itemOrdinal, rawAlias, type, canonicalName, now);
        }
        @Override public IdentityResolution resolveAndLinkExact(String receiptId, int itemOrdinal, String rawAlias) {
            return delegate.resolveAndLinkExact(receiptId, itemOrdinal, rawAlias);
        }
        @Override public IdentityResolution itemResolution(String receiptId, int itemOrdinal) {
            return delegate.itemResolution(receiptId, itemOrdinal);
        }
        @Override public CatalogProduct product(String productId) { return delegate.product(productId); }
        @Override public List<CatalogProduct> listProducts() { listCalls++; return delegate.listProducts(); }
        @Override public List<ItemLinkRef> linksForProduct(String productId) {
            linkReads++;
            return delegate.linksForProduct(productId);
        }
        @Override public void unlinkItem(String receiptId, int itemOrdinal) { delegate.unlinkItem(receiptId, itemOrdinal); }
        @Override public void unlinkReceipt(String receiptId) { delegate.unlinkReceipt(receiptId); }
        @Override public void close() { delegate.close(); }
        void resetCounts() { listCalls = 0; linkReads = 0; }
    }

    private static final class CountingV2Store implements CatalogV2PersistenceStore {
        int catalogEntryReads;
        int purchaseFormReads;
        @Override public CatalogEntryV2 catalogEntryV2(String catalogEntryId) {
            catalogEntryReads++;
            return null;
        }
        @Override public void saveCatalogEntryV2(CatalogEntryV2 entry) {}
        @Override public void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId) {}
        @Override public String aliasCatalogEntryIdV2(AliasContext context, String rawAlias) { return null; }
        @Override public void savePurchaseFormV2(String receiptId, int itemOrdinal,
                CatalogField<PurchaseForm> purchaseForm) {}
        @Override public CatalogField<PurchaseForm> purchaseFormV2(String receiptId, int itemOrdinal) {
            purchaseFormReads++;
            return CatalogField.absent();
        }
        void resetCounts() { catalogEntryReads = 0; purchaseFormReads = 0; }
    }
}
