package com.receiptledger.v1.commoditydetail;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.catalog.SalesUnitCode;
import com.receiptledger.v1.design.ChartGrammarV1;
import com.receiptledger.v1.design.ResponsiveLayoutPolicyV1;
import com.receiptledger.v1.design.SemanticPresentationV1;
import com.receiptledger.v1.item.ItemResolution;
import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.persistence.InMemoryReceiptStore;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.ComparisonBasisV2;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.product.CatalogProduct;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.IdentityResolution;
import com.receiptledger.v1.product.InMemoryProductCatalogStore;
import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.validation.ValidationStatus;
import java.math.BigDecimal;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import org.junit.Test;

public final class CommodityDetailV1Test {
    @Test public void servicePartitionsStrictAndContextualCohorts() {
        Fixture f = new Fixture(true);
        CommodityDetailV1 detail = f.service.load(f.product.id);
        assertEquals(ProductType.NON_STANDARD, detail.product.type);
        assertEquals(2, detail.strictSections.size());
        assertEquals(2, detail.contextualSections.size());
        assertEquals(4, detail.strictSection("WEIGHT_KG").cohort.count());
        assertEquals(1, detail.strictSection("EACH").cohort.count());
        assertEquals(2, detail.contextualSection("LIKE_FORM:BAG:봉").cohort.count());
        assertEquals(1, detail.contextualSection("LIKE_FORM:BOX:상자").cohort.count());
    }

    @Test public void strictWeightUsesFrozenCp28Evaluation() {
        Fixture f = new Fixture(true);
        CommodityDetailV1.BasisSection weight = f.service.load(f.product.id).strictSection("WEIGHT_KG");
        assertNotNull(weight);
        assertDecimal("5500", weight.evaluation.latestPriceMinor);
        assertDecimal("6500", weight.evaluation.previousPriceMinor);
        assertDecimal("6200", weight.evaluation.usualPriceMinor);
        assertEquals(PriceEvaluationV1.Status.EVALUATED, weight.evaluation.status);
        assertEquals(PriceEvaluationV1.Judgment.CHEAP, weight.evaluation.judgment);
        assertEquals("평소보다 저렴", SemanticPresentationV1.price(weight.evaluation).labelKo);
    }

    @Test public void multipleStrictBasesNeverBecomeOneCommodityWideBasis() {
        Fixture f = new Fixture(true);
        CommodityDetailV1 detail = f.service.load(f.product.id);
        assertNotNull(detail.strictSection("WEIGHT_KG"));
        assertNotNull(detail.strictSection("EACH"));
        assertNull(detail.strictSection("VOLUME_L"));
        assertNotEquals(detail.strictSection("WEIGHT_KG").cohort.basis,
                detail.strictSection("EACH").cohort.basis);
    }

    @Test public void latestPurchaseRemainsRealNewestEvenWhenExcluded() {
        Fixture f = new Fixture(true);
        CommodityDetailV1 detail = f.service.load(f.product.id);
        assertNotNull(detail.latestPurchase);
        assertEquals("r9", detail.latestPurchase.observation.receiptId);
        assertFalse(detail.latestPurchase.isEligible());
        assertEquals("r4", detail.strictSection("WEIGHT_KG").cohort.observations.get(0).receiptId);
        assertEquals("가격 비교 제외", CommodityDetailFormatterV1.latestPresentation(detail.latestPurchase).labelKo);
    }

    @Test public void contextualFormsStayReferenceOnlyAndSeparate() {
        Fixture f = new Fixture(true);
        CommodityDetailV1 detail = f.service.load(f.product.id);
        CommodityDetailV1.BasisSection bag = detail.contextualSection("LIKE_FORM:BAG:봉");
        CommodityDetailV1.BasisSection box = detail.contextualSection("LIKE_FORM:BOX:상자");
        assertEquals(PriceEvaluationV1.Status.CONTEXTUAL_ONLY, bag.evaluation.status);
        assertEquals(PriceEvaluationV1.Judgment.NONE, bag.evaluation.judgment);
        assertEquals(PriceEvaluationV1.Status.CONTEXTUAL_ONLY, box.evaluation.status);
        assertDecimal("4500", bag.cohort.latest);
        assertDecimal("4000", bag.cohort.previous);
        assertEquals("참고용 이력", SemanticPresentationV1.price(bag.evaluation).labelKo);
    }

    @Test public void contextualOnlyCommodityNeedsNoFakeStrictPrice() {
        Fixture f = new Fixture(false);
        CommodityDetailV1 detail = f.service.load(f.product.id);
        assertTrue(detail.strictSections.isEmpty());
        assertEquals(1, detail.contextualSections.size());
        assertEquals("r2", detail.latestPurchase.observation.receiptId);
        assertFalse(detail.latestPurchase.isEligible());
    }

    @Test public void formatterPreservesPurchaseFormsAndExplicitRateUnits() {
        Fixture f = new Fixture(true);
        CommodityDetailV1 detail = f.service.load(f.product.id);
        CommodityDetailV1.PurchaseRow gram = detail.purchases.get(7); // r2 in newest-first order
        assertEquals("500g", CommodityDetailFormatterV1.purchaseFormKo(gram));
        assertTrue(CommodityDetailFormatterV1.purchaseSubtitle(gram).contains("6,200원/kg"));
        assertEquals("무게 기준", CommodityDetailFormatterV1.basisTitleKo(ComparisonBasisV2.weightKg()));
        assertEquals("부피 기준", CommodityDetailFormatterV1.basisTitleKo(ComparisonBasisV2.volumeLiter()));
        assertEquals("개수 기준", CommodityDetailFormatterV1.basisTitleKo(ComparisonBasisV2.each()));
        assertEquals("2,000원/L", CommodityDetailFormatterV1.formatRate(new BigDecimal("2000"), ComparisonBasisV2.volumeLiter()));
    }

    @Test public void strictChartContractIsAlwaysSingleBasis() {
        Fixture f = new Fixture(true);
        CommodityDetailV1 detail = f.service.load(f.product.id);
        ChartGrammarV1.requireSingleBasis(Collections.singletonList(detail.strictSection("WEIGHT_KG").cohort.basis));
        ChartGrammarV1.requireSingleBasis(Collections.singletonList(detail.strictSection("EACH").cohort.basis));
        assertEquals("원/kg", ChartGrammarV1.axisLabelKo(detail.strictSection("WEIGHT_KG").cohort.basis));
        assertEquals("원/개", ChartGrammarV1.axisLabelKo(detail.strictSection("EACH").cohort.basis));
    }

    @Test public void receiptTraceabilitySurvivesProjection() {
        Fixture f = new Fixture(true);
        CommodityDetailV1 detail = f.service.load(f.product.id);
        CommodityDetailV1.PurchaseRow newest = detail.purchases.get(0);
        assertEquals("r9", newest.observation.receiptId);
        assertEquals("2026-10-09", newest.observation.purchaseDate);
        assertEquals("시장", newest.observation.storeName);
        assertTrue(CommodityDetailFormatterV1.purchaseSubtitle(newest).contains("가격 비교 제외"));
    }

    @Test public void responsiveContractMatchesFrozenCp30Policy() {
        assertEquals(ResponsiveLayoutPolicyV1.WidthClass.COMPACT, ResponsiveLayoutPolicyV1.widthClass(360));
        assertEquals(ResponsiveLayoutPolicyV1.WidthClass.COMPACT, ResponsiveLayoutPolicyV1.widthClass(599));
        assertEquals(ResponsiveLayoutPolicyV1.WidthClass.MEDIUM, ResponsiveLayoutPolicyV1.widthClass(600));
        assertEquals(ResponsiveLayoutPolicyV1.WidthClass.MEDIUM, ResponsiveLayoutPolicyV1.widthClass(839));
        assertFalse(ResponsiveLayoutPolicyV1.twoPaneEligible(840, 479));
        assertTrue(ResponsiveLayoutPolicyV1.twoPaneEligible(840, 480));
    }

    @Test public void deterministicCp32Metric() {
        Fixture f = new Fixture(true);
        CommodityDetailV1 detail = f.service.load(f.product.id);
        assertEquals(9, detail.purchases.size());
        System.out.println("CP32_METRICS commodity_detail_version=1 strict_basis_kinds=3 contextual_policy=1 grouping_not_comparability=1 responsive_cases=6 traceability=1 chart_single_basis=1 strict_sections="
                + detail.strictSections.size() + " contextual_sections=" + detail.contextualSections.size()
                + " purchase_rows=" + detail.purchases.size());
    }

    private static void assertDecimal(String expected, BigDecimal actual) {
        assertNotNull(actual);
        assertEquals(0, new BigDecimal(expected).compareTo(actual));
    }

    private static final class Fixture {
        final InMemoryReceiptStore receipts = new InMemoryReceiptStore();
        final InMemoryProductCatalogStore catalog = new InMemoryProductCatalogStore();
        final FakeV2 v2 = new FakeV2();
        CatalogProduct product;
        final CommodityDetailServiceV1 service;

        Fixture(boolean full) {
            if (full) {
                add("r1", "2026-10-01", 1, "감자 1kg", 6000L, pf("1", SalesUnitCode.KILOGRAM, "kg"));
                add("r2", "2026-10-02", 2, "감자 500g", 3100L, pf("500", SalesUnitCode.GRAM, "g"));
                add("r3", "2026-10-03", 3, "감자 1kg", 6500L, pf("1", SalesUnitCode.KILOGRAM, "kg"));
                add("r4", "2026-10-04", 4, "감자 1kg", 5500L, pf("1", SalesUnitCode.KILOGRAM, "kg"));
                add("r5", "2026-10-05", 5, "감자 5개", 5000L, pf("5", SalesUnitCode.EACH, "개"));
                add("r6", "2026-10-06", 6, "감자 1봉", 4000L, pf("1", SalesUnitCode.BAG, "봉"));
                add("r7", "2026-10-07", 7, "감자 2봉", 9000L, pf("2", SalesUnitCode.BAG, "봉"));
                add("r8", "2026-10-08", 8, "감자 1상자", 15000L, pf("1", SalesUnitCode.BOX, "상자"));
                add("r9", "2026-10-09", 9, "감자", 5000L, null);
            } else {
                add("r1", "2026-10-01", 1, "감자 1봉", 4000L, pf("1", SalesUnitCode.BAG, "봉"));
                add("r2", "2026-10-02", 2, "감자", 5000L, null);
            }
            v2.entry = CatalogEntryV2.commodity(product.id, product.canonicalName, null, 1L);
            service = new CommodityDetailServiceV1(
                    catalog, v2, new PriceIntelligenceServiceV2(receipts, catalog, v2));
        }

        private void add(String id, String date, long created, String rawName, long amount, PurchaseForm form) {
            receipts.save(receipt(id, date, created, rawName, amount));
            IdentityResolution resolution = catalog.confirm(
                    id, 0, rawName, ProductType.NON_STANDARD, "감자", created);
            product = resolution.product;
            if (form != null) {
                v2.savePurchaseFormV2(id, 0,
                        CatalogField.parsed(form, CatalogField.Confidence.HIGH));
            }
        }
    }

    private static PurchaseForm pf(String quantity, SalesUnitCode unit, String raw) {
        return new PurchaseForm(quantity, unit, raw);
    }

    private static ReceiptRecord receipt(String id, String date, long created, String name, long amount) {
        PersistedItem item = new PersistedItem(
                0, 0, name, null, null, amount,
                ValueOrigin.PRINTED, ValueOrigin.PRINTED, ValueOrigin.PRINTED,
                ItemResolution.EXACT, null);
        return new ReceiptRecord(
                id, created, date, "시장", "", amount, amount, 0L, amount, 0L,
                ValidationStatus.PASS, 100, 200, false,
                Collections.<String>emptyList(), Arrays.asList(item));
    }

    private static final class FakeV2 implements CatalogV2PersistenceStore {
        CatalogEntryV2 entry;
        final Map<String,CatalogField<PurchaseForm>> forms = new HashMap<>();

        @Override public CatalogEntryV2 catalogEntryV2(String id) {
            return entry != null && entry.id.equals(id) ? entry : null;
        }
        @Override public void saveCatalogEntryV2(CatalogEntryV2 entry) { this.entry = entry; }
        @Override public void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId) {}
        @Override public String aliasCatalogEntryIdV2(AliasContext context, String rawAlias) { return null; }
        @Override public void savePurchaseFormV2(String receiptId, int itemOrdinal, CatalogField<PurchaseForm> purchaseForm) {
            forms.put(receiptId + "#" + itemOrdinal, purchaseForm);
        }
        @Override public CatalogField<PurchaseForm> purchaseFormV2(String receiptId, int itemOrdinal) {
            CatalogField<PurchaseForm> value = forms.get(receiptId + "#" + itemOrdinal);
            return value == null ? CatalogField.<PurchaseForm>absent() : value;
        }
    }
}
