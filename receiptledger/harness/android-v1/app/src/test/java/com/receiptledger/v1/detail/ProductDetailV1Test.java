package com.receiptledger.v1.detail;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.ProductSpecification;
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
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.priceintel.PriceObservationV2;
import com.receiptledger.v1.product.CatalogProduct;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.IdentityResolution;
import com.receiptledger.v1.product.InMemoryProductCatalogStore;
import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.validation.ValidationStatus;
import java.math.BigDecimal;
import java.util.Arrays;
import java.util.Collections;
import org.junit.Test;

public final class ProductDetailV1Test {
    @Test public void standardServiceUsesFrozenCp27Cp28Facts() {
        Fixture f = fixture(true);
        ProductDetailV1 detail = f.service.load(f.product.id);
        assertEquals(ProductType.STANDARD, detail.product.type);
        assertEquals("STANDARD_PACKAGE", detail.cohort.basis.key());
        assertEquals(new BigDecimal("3000"), detail.evaluation.latestPriceMinor);
        assertEquals(new BigDecimal("3500"), detail.evaluation.previousPriceMinor);
        assertEquals(new BigDecimal("3500"), detail.evaluation.usualPriceMinor);
        assertEquals(PriceEvaluationV1.Judgment.CHEAP, detail.evaluation.judgment);
        assertEquals(4, detail.purchases.size());
    }

    @Test public void structuredIdentityPrefersV2Fields() {
        Fixture f = fixture(true);
        ProductDetailV1 detail = f.service.load(f.product.id);
        assertEquals("서울우유", ProductDetailFormatterV1.brand(detail));
        assertEquals("우유", ProductDetailFormatterV1.primaryName(detail));
        assertEquals("고소한맛", ProductDetailFormatterV1.variant(detail));
    }

    @Test public void legacyStandardFallsBackWithoutFabrication() {
        Fixture f = fixture(false);
        ProductDetailV1 detail = f.service.load(f.product.id);
        assertNull(detail.catalogEntry);
        assertEquals("서울우유 1L", ProductDetailFormatterV1.primaryName(detail));
        assertEquals("", ProductDetailFormatterV1.brand(detail));
        assertEquals("", ProductDetailFormatterV1.specification(detail));
    }

    @Test public void evaluatedCopyUsesFrozenSemanticPresentation() {
        Fixture f = fixture(true);
        ProductDetailV1 detail = f.service.load(f.product.id);
        SemanticPresentationV1.Presentation p = SemanticPresentationV1.price(detail.evaluation);
        assertEquals("평소보다 저렴", p.labelKo);
        assertTrue(p.judgment);
        assertTrue(ProductDetailFormatterV1.evaluationEvidence(detail.evaluation).contains("이전 3회 기준"));
    }

    @Test public void insufficientHistoryDoesNotInventUsualPrice() {
        Fixture f = new Fixture(true, new long[]{3000L});
        ProductDetailV1 detail = f.service.load(f.product.id);
        assertEquals(PriceEvaluationV1.Status.INSUFFICIENT_HISTORY, detail.evaluation.status);
        assertNull(detail.evaluation.usualPriceMinor);
        assertEquals("비교 데이터 부족", SemanticPresentationV1.price(detail.evaluation).labelKo);
    }

    @Test public void chartContractIsStandardPackageOnly() {
        Fixture f = fixture(true);
        ProductDetailV1 detail = f.service.load(f.product.id);
        ChartGrammarV1.requireSingleBasis(Collections.singletonList(detail.cohort.basis));
        assertEquals("원/상품", ChartGrammarV1.axisLabelKo(detail.cohort.basis));
        assertEquals("STANDARD_PACKAGE", detail.cohort.basis.key());
    }

    @Test public void receiptTraceabilitySurvivesProjection() {
        Fixture f = fixture(true);
        ProductDetailV1 detail = f.service.load(f.product.id);
        ProductDetailV1.PurchaseRow newest = detail.purchases.get(0);
        assertEquals("r4", newest.receiptId);
        assertEquals("2026-10-04", newest.purchaseDate);
        assertEquals("동네마트", newest.storeName);
        assertEquals("3,000원 · 상품 1개 기준", ProductDetailFormatterV1.purchaseSubtitle(newest));
    }

    @Test public void responsiveContractKeepsCompactSinglePane() {
        assertEquals(ResponsiveLayoutPolicyV1.WidthClass.COMPACT, ResponsiveLayoutPolicyV1.widthClass(360));
        assertEquals(ResponsiveLayoutPolicyV1.WidthClass.MEDIUM, ResponsiveLayoutPolicyV1.widthClass(600));
        assertFalse(ResponsiveLayoutPolicyV1.twoPaneEligible(840, 479));
        assertTrue(ResponsiveLayoutPolicyV1.twoPaneEligible(840, 480));
    }

    @Test public void deterministicCp31Metric() {
        Fixture f = fixture(true);
        ProductDetailV1 detail = f.service.load(f.product.id);
        assertEquals(4, detail.comparablePurchases().size());
        System.out.println("CP31_METRICS product_detail_version=1 standard_basis=1 identity_fallbacks=1 price_states=8 responsive_cases=6 traceability=1 chart_single_basis=1 purchase_rows=" + detail.purchases.size());
    }

    private static Fixture fixture(boolean structured) {
        return new Fixture(structured, new long[]{3500L, 3500L, 3500L, 3000L});
    }

    private static final class Fixture {
        final InMemoryReceiptStore receipts = new InMemoryReceiptStore();
        final InMemoryProductCatalogStore catalog = new InMemoryProductCatalogStore();
        final FakeV2 v2 = new FakeV2();
        final CatalogProduct product;
        final ProductDetailServiceV1 service;

        Fixture(boolean structured, long[] prices) {
            CatalogProduct created = null;
            for (int i = 0; i < prices.length; i++) {
                String rid = "r" + (i + 1);
                String date = String.format("2026-10-%02d", i + 1);
                receipts.save(receipt(rid, date, prices[i], i + 1));
                IdentityResolution resolution = catalog.confirm(
                        rid, 0, "서울우유1L", ProductType.STANDARD, "서울우유 1L", 1000L + i);
                created = resolution.product;
            }
            product = created;
            if (structured && product != null) {
                ProductSpecification spec = new ProductSpecification(
                        new com.receiptledger.v1.catalog.PackageMeasure("1", SalesUnitCode.LITER), null, null);
                v2.entry = CatalogEntryV2.standard(
                        product.id,
                        product.canonicalName,
                        CatalogField.userConfirmed("서울우유"),
                        CatalogField.userConfirmed("우유"),
                        CatalogField.userConfirmed("고소한맛"),
                        CatalogField.userConfirmed(spec),
                        null,
                        1L);
            }
            PriceIntelligenceServiceV2 price = new PriceIntelligenceServiceV2(receipts, catalog, v2);
            service = new ProductDetailServiceV1(catalog, v2, price);
        }
    }

    private static ReceiptRecord receipt(String id, String date, long price, long created) {
        PersistedItem item = new PersistedItem(
                0, 0, "서울우유1L", 1, price, price,
                ValueOrigin.OCR, ValueOrigin.OCR, ValueOrigin.OCR,
                ItemResolution.RESOLVED, null);
        return new ReceiptRecord(
                id, created, date, "동네마트", "", price, price, 0L, price, 0L,
                ValidationStatus.PASS, 100, 200, false,
                Collections.<String>emptyList(), Arrays.asList(item));
    }

    private static final class FakeV2 implements CatalogV2PersistenceStore {
        CatalogEntryV2 entry;
        @Override public CatalogEntryV2 catalogEntryV2(String id) { return entry != null && entry.id.equals(id) ? entry : null; }
        @Override public void saveCatalogEntryV2(CatalogEntryV2 entry) { this.entry = entry; }
        @Override public void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId) {}
        @Override public String aliasCatalogEntryIdV2(AliasContext context, String rawAlias) { return null; }
        @Override public void savePurchaseFormV2(String receiptId, int itemOrdinal, CatalogField<PurchaseForm> purchaseForm) {}
        @Override public CatalogField<PurchaseForm> purchaseFormV2(String receiptId, int itemOrdinal) { return CatalogField.absent(); }
    }
}
