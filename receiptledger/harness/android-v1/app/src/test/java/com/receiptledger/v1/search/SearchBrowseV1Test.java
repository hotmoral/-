package com.receiptledger.v1.search;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.CategoryRef;
import com.receiptledger.v1.catalog.PackageMeasure;
import com.receiptledger.v1.catalog.ProductSpecification;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.catalog.SalesUnitCode;
import com.receiptledger.v1.category.CategoryTaxonomyV1;
import com.receiptledger.v1.item.ItemResolution;
import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.persistence.InMemoryReceiptStore;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.priceeval.PriceEvaluationServiceV1;
import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.IdentityResolution;
import com.receiptledger.v1.product.InMemoryProductCatalogStore;
import com.receiptledger.v1.product.ProductNameNormalizer;
import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.validation.ValidationStatus;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.Test;

public final class SearchBrowseV1Test {

    @Test public void canonicalStructuredAndCompactSearchRankDeterministically() {
        Fixture f = new Fixture();
        String milk = f.addStandard("r1", "2026-10-01", "이마트 강서", 1,
                "서우유1000ML", "서울우유 나100% 1L", "서울우유", "나100%", null,
                new ProductSpecification(new PackageMeasure("1", SalesUnitCode.LITER), null, null),
                CategoryTaxonomyV1.FOOD_DAIRY_MILK, 3000L);
        f.addStandard("r2", "2026-10-02", "이마트 강서", 2,
                "서울요구르트500", "서울 요구르트 500ml", "서울", "요구르트", null,
                new ProductSpecification(new PackageMeasure("500", SalesUnitCode.MILLILITER), null, null),
                CategoryTaxonomyV1.FOOD_DAIRY_YOGURT, 1800L);

        SearchBrowseResultV1 exact = f.service().search(SearchBrowseQueryV1.text("서울우유 나100% 1L", 10));
        assertEquals(1, exact.entries.size());
        assertEquals(milk, exact.entries.get(0).productId);
        assertEquals("CANONICAL_EXACT", exact.entries.get(0).matchReason);

        SearchBrowseResultV1 compact = f.service().search(SearchBrowseQueryV1.text("서울 우유 나100% 1L", 10));
        assertEquals(milk, compact.entries.get(0).productId);

        SearchBrowseResultV1 spec = f.service().search(SearchBrowseQueryV1.text("1000ML", 10));
        assertEquals(milk, spec.entries.get(0).productId);
        assertTrue(spec.entries.get(0).matchReason.startsWith("STRUCTURED_"));
    }

    @Test public void observedAndStoreSearchAreReadOnly() {
        Fixture f = new Fixture();
        String id = f.addStandard("r1", "2026-10-01", "홈플러스 강서점", 1,
                "특가우유1000", "매일우유 1L", "매일", "우유", null,
                new ProductSpecification(new PackageMeasure("1", SalesUnitCode.LITER), null, null),
                CategoryTaxonomyV1.FOOD_DAIRY_MILK, 2900L);
        int productsBefore = f.products.listProducts().size();
        int linksBefore = f.products.linksForProduct(id).size();

        SearchBrowseResultV1 observed = f.service().search(SearchBrowseQueryV1.text("특가우유1000", 10));
        assertEquals(id, observed.entries.get(0).productId);
        assertEquals("OBSERVED_EXACT", observed.entries.get(0).matchReason);

        SearchBrowseResultV1 store = f.service().search(SearchBrowseQueryV1.text("홈플러스 강서점", 10));
        assertEquals(id, store.entries.get(0).productId);
        assertEquals("STORE_EXACT", store.entries.get(0).matchReason);

        assertEquals(productsBefore, f.products.listProducts().size());
        assertEquals(linksBefore, f.products.linksForProduct(id).size());
    }

    @Test public void categoryDescendantsAndExactStoreFilterWork() {
        Fixture f = new Fixture();
        String milk = f.addStandard("m1", "2026-10-01", "이마트 강서", 1,
                "우유", "서울우유 1L", "서울우유", "우유", null,
                new ProductSpecification(new PackageMeasure("1", SalesUnitCode.LITER), null, null),
                CategoryTaxonomyV1.FOOD_DAIRY_MILK, 3000L);
        f.addStandard("n1", "2026-10-02", "롯데마트", 2,
                "라면", "신라면 5입", "농심", "신라면", null,
                new ProductSpecification(null, 5, null),
                CategoryTaxonomyV1.FOOD_NOODLES_RAMEN, 4200L);

        List<SearchBrowseEntryV1> food = f.service().byCategory(CategoryTaxonomyV1.FOOD, 10);
        assertEquals(2, food.size());
        List<SearchBrowseEntryV1> dairy = f.service().byCategory(CategoryTaxonomyV1.FOOD_DAIRY, 10);
        assertEquals(1, dairy.size());
        assertEquals(milk, dairy.get(0).productId);

        SearchBrowseResultV1 store = f.service().search(new SearchBrowseQueryV1(
                null, null, "  이마트   강서  ", null, 10));
        assertEquals(1, store.entries.size());
        assertEquals(milk, store.entries.get(0).productId);

        SearchBrowseResultV1 partialStore = f.service().search(new SearchBrowseQueryV1(
                null, null, "이마트", null, 10));
        assertTrue(partialStore.entries.isEmpty());
    }

    @Test public void recentAndFrequentUsePurchaseOccasionsDeterministically() {
        Fixture f = new Fixture();
        String frequent = f.addStandard("a1", "2026-09-01", "A", 1,
                "A", "자주산상품", "브랜드A", "상품A", null, null, CategoryTaxonomyV1.FOOD_SNACK, 1000L);
        f.linkExistingStandard(frequent, "자주산상품", "a2", "2026-09-05", "A", 2, "A2", 1100L);
        f.linkExistingStandard(frequent, "자주산상품", "a3", "2026-09-10", "B", 3, "A3", 1200L);
        String recent = f.addStandard("b1", "2026-10-10", "C", 4,
                "B", "최근상품", "브랜드B", "상품B", null, null, CategoryTaxonomyV1.FOOD_SNACK, 2000L);

        assertEquals(recent, f.service().recent(10).get(0).productId);
        assertEquals(frequent, f.service().frequent(10).get(0).productId);
        assertEquals(3, f.service().frequent(10).get(0).purchaseCount);
    }

    @Test public void blankQueryAndNoResultAreExplicit() {
        Fixture f = new Fixture();
        f.addStandard("r1", "2026-10-01", "A", 1,
                "우유", "우유", "A", "우유", null, null, CategoryTaxonomyV1.FOOD_DAIRY_MILK, 1000L);
        f.addCommodity("r2", "2026-10-02", "시장", 2, "감자", "감자", CategoryTaxonomyV1.FOOD_PRODUCE_VEGETABLE, 5000L, null);

        SearchBrowseResultV1 all = f.service().search(SearchBrowseQueryV1.all(10));
        assertEquals(2, all.catalogEntriesScanned);
        assertEquals(2, all.matchedEntriesBeforeLimit);
        assertEquals(2, all.returnedEntries);

        SearchBrowseResultV1 none = f.service().search(SearchBrowseQueryV1.text("존재하지않음", 10));
        assertEquals(2, none.catalogEntriesScanned);
        assertEquals(0, none.matchedEntriesBeforeLimit);
        assertTrue(none.entries.isEmpty());
    }

    @Test public void priceChangeBrowseExcludesTypicalAndContextualCohorts() {
        Fixture f = new Fixture();
        String changed = f.addStandard("s1", "2026-09-01", "A", 1,
                "변동", "변동상품", "A", "변동", null, null, CategoryTaxonomyV1.FOOD_SNACK, 1000L);
        f.linkExistingStandard(changed, "변동상품", "s2", "2026-09-05", "A", 2, "변동2", 1000L);
        f.linkExistingStandard(changed, "변동상품", "s3", "2026-09-10", "A", 3, "변동3", 1000L);
        f.linkExistingStandard(changed, "변동상품", "s4", "2026-10-01", "A", 4, "변동4", 1300L);

        String typical = f.addStandard("t1", "2026-09-01", "B", 11,
                "평소", "평소상품", "B", "평소", null, null, CategoryTaxonomyV1.FOOD_SNACK, 1000L);
        f.linkExistingStandard(typical, "평소상품", "t2", "2026-09-05", "B", 12, "평소2", 1000L);
        f.linkExistingStandard(typical, "평소상품", "t3", "2026-09-10", "B", 13, "평소3", 1000L);
        f.linkExistingStandard(typical, "평소상품", "t4", "2026-10-01", "B", 14, "평소4", 1030L);

        String bag = f.addCommodity("c1", "2026-09-01", "시장", 21, "감자1봉", "감자",
                CategoryTaxonomyV1.FOOD_PRODUCE_VEGETABLE, 4000L, new PurchaseForm("1", SalesUnitCode.BAG, "봉"));
        f.linkExistingCommodity(bag, "감자", "c2", "2026-09-05", "시장", 22, "감자2봉", 8000L, new PurchaseForm("2", SalesUnitCode.BAG, "봉"));
        f.linkExistingCommodity(bag, "감자", "c3", "2026-09-10", "시장", 23, "감자3봉", 12000L, new PurchaseForm("3", SalesUnitCode.BAG, "봉"));
        f.linkExistingCommodity(bag, "감자", "c4", "2026-10-01", "시장", 24, "감자1봉", 6000L, new PurchaseForm("1", SalesUnitCode.BAG, "봉"));

        List<PriceChangeBrowseRowV1> rows = f.service().priceChanges(20);
        assertEquals(1, rows.size());
        assertEquals(changed, rows.get(0).productId);
        assertEquals(PriceEvaluationV1.Judgment.EXPENSIVE, rows.get(0).judgment);
        assertEquals("STANDARD_PACKAGE", rows.get(0).basisKey);
    }

    @Test public void commodityStrictBasesRemainSeparateInPriceChangeBrowse() {
        Fixture f = new Fixture();
        String potato = f.addCommodity("w1", "2026-09-01", "시장", 1, "감자1kg", "감자",
                CategoryTaxonomyV1.FOOD_PRODUCE_VEGETABLE, 5000L, new PurchaseForm("1", SalesUnitCode.KILOGRAM, "kg"));
        f.linkExistingCommodity(potato, "감자", "w2", "2026-09-05", "시장", 2, "감자1kg", 5000L, new PurchaseForm("1", SalesUnitCode.KILOGRAM, "kg"));
        f.linkExistingCommodity(potato, "감자", "w3", "2026-09-10", "시장", 3, "감자1kg", 5000L, new PurchaseForm("1", SalesUnitCode.KILOGRAM, "kg"));
        f.linkExistingCommodity(potato, "감자", "w4", "2026-10-01", "시장", 4, "감자1kg", 6000L, new PurchaseForm("1", SalesUnitCode.KILOGRAM, "kg"));
        f.linkExistingCommodity(potato, "감자", "e1", "2026-09-02", "시장", 11, "감자5개", 5000L, new PurchaseForm("5", SalesUnitCode.EACH, "개"));
        f.linkExistingCommodity(potato, "감자", "e2", "2026-09-06", "시장", 12, "감자5개", 5000L, new PurchaseForm("5", SalesUnitCode.EACH, "개"));
        f.linkExistingCommodity(potato, "감자", "e3", "2026-09-11", "시장", 13, "감자5개", 5000L, new PurchaseForm("5", SalesUnitCode.EACH, "개"));
        f.linkExistingCommodity(potato, "감자", "e4", "2026-10-02", "시장", 14, "감자5개", 4000L, new PurchaseForm("5", SalesUnitCode.EACH, "개"));

        List<PriceChangeBrowseRowV1> rows = f.service().priceChanges(20);
        int potatoRows = 0;
        boolean weight = false, each = false;
        for (PriceChangeBrowseRowV1 row : rows) {
            if (!potato.equals(row.productId)) continue;
            potatoRows++;
            if ("WEIGHT_KG".equals(row.basisKey)) weight = true;
            if ("EACH".equals(row.basisKey)) each = true;
        }
        assertEquals(2, potatoRows);
        assertTrue(weight);
        assertTrue(each);
    }

    @Test public void canonicalMetricsCoverDiscoveryAndBrowseContracts() {
        Fixture f = new Fixture();
        String milk = f.addStandard("m1", "2026-10-01", "이마트 강서", 1,
                "서우유1000", "서울우유 1L", "서울우유", "우유", null,
                new ProductSpecification(new PackageMeasure("1", SalesUnitCode.LITER), null, null),
                CategoryTaxonomyV1.FOOD_DAIRY_MILK, 3000L);
        f.linkExistingStandard(milk, "서울우유 1L", "m2", "2026-10-05", "이마트 강서", 2, "서울우유행사", 3100L);
        String ramen = f.addStandard("n1", "2026-10-03", "롯데마트", 3,
                "신라면5", "신라면 5입", "농심", "신라면", null,
                new ProductSpecification(null, 5, null), CategoryTaxonomyV1.FOOD_NOODLES_RAMEN, 4000L);
        f.addCommodity("c1", "2026-10-04", "시장", 4, "감자1kg", "감자",
                CategoryTaxonomyV1.FOOD_PRODUCE_VEGETABLE, 5000L, new PurchaseForm("1", SalesUnitCode.KILOGRAM, "kg"));

        SearchBrowseServiceV1 service = f.service();
        int exact = service.search(SearchBrowseQueryV1.text("서울우유 1L", 10)).returnedEntries;
        int compact = service.search(SearchBrowseQueryV1.text("서울 우유 1L", 10)).returnedEntries;
        int observed = service.search(SearchBrowseQueryV1.text("서울우유행사", 10)).returnedEntries;
        int category = service.byCategory(CategoryTaxonomyV1.FOOD, 10).size();
        int store = service.search(new SearchBrowseQueryV1(null, null, "이마트 강서", null, 10)).returnedEntries;
        int recent = service.recent(10).size();
        int frequent = service.frequent(10).size();
        int noResult = service.search(SearchBrowseQueryV1.text("없는상품", 10)).returnedEntries;
        int mutationChecks = f.products.listProducts().size() == 3 && f.products.linksForProduct(milk).size() == 2 ? 1 : 0;

        assertEquals(1, exact);
        assertEquals(1, compact);
        assertEquals(1, observed);
        assertEquals(3, category);
        assertEquals(1, store);
        assertEquals(3, recent);
        assertEquals(3, frequent);
        assertEquals(0, noResult);
        assertEquals(1, mutationChecks);

        System.out.println("CP29_METRICS documents=3 exact_hits=" + exact
                + " compact_hits=" + compact
                + " observed_hits=" + observed
                + " category_rows=" + category
                + " store_rows=" + store
                + " recent_rows=" + recent
                + " frequent_rows=" + frequent
                + " no_result_rows=" + noResult
                + " mutation_checks=" + mutationChecks
                + " diagnostics_scanned=" + service.search(SearchBrowseQueryV1.text("서울우유", 10)).catalogEntriesScanned);
    }

    private static final class Fixture {
        final InMemoryReceiptStore receipts = new InMemoryReceiptStore();
        final InMemoryProductCatalogStore products = new InMemoryProductCatalogStore();
        final FakeV2 v2 = new FakeV2();

        SearchBrowseServiceV1 service() {
            PriceIntelligenceServiceV2 prices = new PriceIntelligenceServiceV2(receipts, products, v2);
            return new SearchBrowseServiceV1(receipts, products, v2, prices, new PriceEvaluationServiceV1());
        }

        String addStandard(String receiptId, String date, String store, long created, String rawName,
                String canonicalName, String brand, String productName, String variant,
                ProductSpecification spec, String categoryId, long lineAmount) {
            saveReceipt(receiptId, date, store, created, rawName, lineAmount);
            IdentityResolution linked = products.confirm(receiptId, 0, rawName, ProductType.STANDARD, canonicalName, created);
            CatalogProductBuilder.saveStandard(v2, linked.product.id, canonicalName, brand, productName, variant, spec, categoryId, created);
            return linked.product.id;
        }

        void linkExistingStandard(String productId, String canonicalName, String receiptId, String date, String store,
                long created, String rawName, long lineAmount) {
            saveReceipt(receiptId, date, store, created, rawName, lineAmount);
            IdentityResolution linked = products.confirm(receiptId, 0, rawName, ProductType.STANDARD, canonicalName, created);
            assertEquals(productId, linked.product.id);
        }

        String addCommodity(String receiptId, String date, String store, long created, String rawName,
                String canonicalName, String categoryId, long lineAmount, PurchaseForm form) {
            saveReceipt(receiptId, date, store, created, rawName, lineAmount);
            IdentityResolution linked = products.confirm(receiptId, 0, rawName, ProductType.NON_STANDARD, canonicalName, created);
            v2.saveCatalogEntryV2(CatalogEntryV2.commodity(linked.product.id, canonicalName,
                    categoryId == null ? null : new CategoryRef(categoryId), created));
            if (form != null) v2.savePurchaseFormV2(receiptId, 0, CatalogField.userConfirmed(form));
            return linked.product.id;
        }

        void linkExistingCommodity(String productId, String canonicalName, String receiptId, String date, String store,
                long created, String rawName, long lineAmount, PurchaseForm form) {
            saveReceipt(receiptId, date, store, created, rawName, lineAmount);
            IdentityResolution linked = products.confirm(receiptId, 0, rawName, ProductType.NON_STANDARD, canonicalName, created);
            assertEquals(productId, linked.product.id);
            if (form != null) v2.savePurchaseFormV2(receiptId, 0, CatalogField.userConfirmed(form));
        }

        private void saveReceipt(String id, String date, String store, long created, String rawName, long lineAmount) {
            PersistedItem item = new PersistedItem(0, 0, rawName, 1, lineAmount, lineAmount,
                    ValueOrigin.PRINTED, ValueOrigin.PRINTED, ValueOrigin.PRINTED,
                    ItemResolution.EXACT, null);
            receipts.save(new ReceiptRecord(id, created, date, store, "", lineAmount, lineAmount, 0L,
                    lineAmount, 0L, ValidationStatus.PASS, 100, 100, false,
                    Collections.<String>emptyList(), Collections.singletonList(item)));
        }
    }

    private static final class CatalogProductBuilder {
        static void saveStandard(FakeV2 store, String id, String canonicalName, String brand, String productName,
                String variant, ProductSpecification spec, String categoryId, long created) {
            store.saveCatalogEntryV2(CatalogEntryV2.standard(
                    id,
                    canonicalName,
                    brand == null ? CatalogField.<String>absent() : CatalogField.userConfirmed(brand),
                    CatalogField.userConfirmed(productName),
                    variant == null ? CatalogField.<String>absent() : CatalogField.userConfirmed(variant),
                    spec == null ? CatalogField.<ProductSpecification>absent() : CatalogField.userConfirmed(spec),
                    categoryId == null ? null : new CategoryRef(categoryId),
                    created));
        }
    }

    private static final class FakeV2 implements CatalogV2PersistenceStore {
        private final Map<String, CatalogEntryV2> entries = new HashMap<>();
        private final Map<String, CatalogField<PurchaseForm>> forms = new HashMap<>();
        private final Map<String, String> aliases = new HashMap<>();

        @Override public CatalogEntryV2 catalogEntryV2(String catalogEntryId) { return entries.get(catalogEntryId); }
        @Override public void saveCatalogEntryV2(CatalogEntryV2 entry) { entries.put(entry.id, entry); }
        @Override public void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId) {
            aliases.put(context.toString() + "|" + ProductNameNormalizer.key(rawAlias), catalogEntryId);
        }
        @Override public String aliasCatalogEntryIdV2(AliasContext context, String rawAlias) {
            return aliases.get(context.toString() + "|" + ProductNameNormalizer.key(rawAlias));
        }
        @Override public void savePurchaseFormV2(String receiptId, int itemOrdinal, CatalogField<PurchaseForm> purchaseForm) {
            forms.put(receiptId + "#" + itemOrdinal, purchaseForm);
        }
        @Override public CatalogField<PurchaseForm> purchaseFormV2(String receiptId, int itemOrdinal) {
            CatalogField<PurchaseForm> field = forms.get(receiptId + "#" + itemOrdinal);
            return field == null ? CatalogField.<PurchaseForm>absent() : field;
        }
    }
}
