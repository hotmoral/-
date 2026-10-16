package com.receiptledger.v1.priceintel;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.catalog.SalesUnitCode;
import com.receiptledger.v1.item.ItemResolution;
import com.receiptledger.v1.item.ValueOrigin;
import com.receiptledger.v1.persistence.InMemoryReceiptStore;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.IdentityResolution;
import com.receiptledger.v1.product.InMemoryProductCatalogStore;
import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.validation.ValidationStatus;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.Test;

public final class PriceIntelligenceV2Test {

    @Test public void standardStatsAreDeterministicAndScopeAware() {
        Fixture f = new Fixture();
        f.receipts.save(receipt("r1", "2026-10-01", "마트A", 1, 0, ValidationStatus.PASS,
                item(0, "우유1L", 2, 3000L, 6000L)));
        f.receipts.save(receipt("r2", "2026-10-05", "마트B", 2, 0, ValidationStatus.PASS_WITH_WARNINGS,
                item(0, "우유1L", 1, 3200L, 3200L)));
        f.receipts.save(receipt("r3", "2026-10-10", "마트A", 3, 0, ValidationStatus.PASS,
                item(0, "우유1L", 1, 2800L, 2800L)));
        String id = linkAll(f.products, ProductType.STANDARD, "서울우유 1L", "우유1L", "r1", "r2", "r3");

        PriceIntelligenceV2 all = f.service().analyze(id);
        PriceCohortV2 c = all.cohort("STANDARD_PACKAGE");
        assertNotNull(c);
        assertEquals(3, c.count());
        bd("2800", c.latest);
        bd("3200", c.previous);
        bd("-400", c.delta);
        bd("2800", c.min);
        bd("3200", c.max);
        bd("3000", c.mean);
        bd("3000", c.median);
        bd("-12.5", c.deltaPercent);

        PriceCohortV2 store = f.service().analyze(id, PriceScopeV2.store("마트A")).cohort("STANDARD_PACKAGE");
        assertEquals(2, store.count());
        bd("2800", store.latest);
        bd("3000", store.previous);

        PriceCohortV2 period = f.service().analyze(id, PriceScopeV2.period("2026-10-02", "2026-10-10")).cohort("STANDARD_PACKAGE");
        assertEquals(2, period.count());
        bd("2800", period.latest);
        bd("3200", period.previous);
    }

    @Test public void soleItemDiscountIsExactlyAttributedButMultiItemDiscountIsExcluded() {
        Fixture f = new Fixture();
        f.receipts.save(receipt("r1", "2026-10-01", "마트", 1, -1000, ValidationStatus.PASS,
                item(0, "커피", 1, 5000L, 5000L)));
        List<PersistedItem> multi = new ArrayList<>();
        multi.add(item(0, "커피", 1, 5000L, 5000L));
        multi.add(item(1, "과자", 1, 2000L, 2000L));
        f.receipts.save(receipt("r2", "2026-10-02", "마트", 2, -1000, ValidationStatus.PASS, multi));
        String id = linkAll(f.products, ProductType.STANDARD, "커피", "커피", "r1", "r2");

        PriceIntelligenceV2 result = f.service().analyze(id);
        assertEquals(2, result.observations.size());
        PriceObservationV2 newest = result.observations.get(0);
        assertEquals(PriceObservationV2.Eligibility.UNALLOCATED_RECEIPT_DISCOUNT, newest.eligibility);
        PriceObservationV2 sole = result.observations.get(1);
        assertTrue(sole.isEligible());
        assertEquals(PriceObservationV2.DiscountTreatment.SOLE_ITEM_EXACT, sole.discountTreatment);
        bd("4000", sole.comparisonPriceMinor);
        assertEquals(1, result.cohort("STANDARD_PACKAGE").count());
    }

    @Test public void invalidReceiptAndConflictingItemArithmeticNeverEnterAggregates() {
        Fixture f = new Fixture();
        f.receipts.save(receipt("r1", "2026-10-01", "마트", 1, 0, ValidationStatus.MISMATCH,
                item(0, "라면", 1, 3000L, 3000L)));
        f.receipts.save(receipt("r2", "2026-10-02", "마트", 2, 0, ValidationStatus.PASS,
                item(0, "라면", 2, 3000L, 6100L)));
        String id = linkAll(f.products, ProductType.STANDARD, "라면", "라면", "r1", "r2");

        PriceIntelligenceV2 result = f.service().analyze(id);
        assertEquals(0, result.eligibleCount());
        assertEquals(2, result.excludedCount());
        assertEquals(PriceObservationV2.Eligibility.ITEM_PRICE_CONFLICT, result.observations.get(0).eligibility);
        assertEquals(PriceObservationV2.Eligibility.INVALID_RECEIPT, result.observations.get(1).eligibility);
        assertTrue(result.cohorts.isEmpty());
    }

    @Test public void exactSourceRatioIsPreservedEvenWhenDecimalRepeats() {
        Fixture f = new Fixture();
        f.receipts.save(receipt("r1", "2026-10-01", "마트", 1, 0, ValidationStatus.PASS,
                item(0, "묶음상품", 3, null, 10000L)));
        String id = linkAll(f.products, ProductType.STANDARD, "묶음상품", "묶음상품", "r1");
        PriceObservationV2 o = f.service().analyze(id).observations.get(0);
        assertTrue(o.isEligible());
        bd("10000", o.sourceNumeratorMinor);
        bd("3", o.sourceDenominator);
        assertTrue(o.comparisonPriceMinor.toPlainString().startsWith("3333.333333"));
    }

    @Test public void commodityWeightNormalizesKgAndGramIntoOneStrictCohort() {
        Fixture f = new Fixture();
        f.receipts.save(receipt("r1", "2026-10-01", "시장", 1, 0, ValidationStatus.PASS,
                item(0, "감자 1kg", null, null, 6000L)));
        f.receipts.save(receipt("r2", "2026-10-08", "시장", 2, 0, ValidationStatus.PASS,
                item(0, "감자 500g", null, null, 3300L)));
        String id = linkAll(f.products, ProductType.NON_STANDARD, "감자", "감자 1kg", "r1");
        f.products.confirm("r2", 0, "감자 500g", ProductType.NON_STANDARD, "감자", 2);
        f.v2.savePurchaseFormV2("r1", 0, CatalogField.parsed(new PurchaseForm("1", SalesUnitCode.KILOGRAM, "kg"), CatalogField.Confidence.MEDIUM));
        f.v2.savePurchaseFormV2("r2", 0, CatalogField.parsed(new PurchaseForm("500", SalesUnitCode.GRAM, "g"), CatalogField.Confidence.MEDIUM));

        PriceCohortV2 c = f.service().analyze(id).cohort("WEIGHT_KG");
        assertNotNull(c);
        assertEquals(PriceCohortV2.Strength.STRICT_NORMALIZED, c.strength);
        assertEquals(2, c.count());
        bd("6600", c.latest);
        bd("6000", c.previous);
        bd("600", c.delta);
        bd("6300", c.mean);
    }

    @Test public void packageFormsStaySeparatedIntoContextualCohorts() {
        Fixture f = new Fixture();
        f.receipts.save(receipt("r1", "2026-10-01", "시장", 1, 0, ValidationStatus.PASS,
                item(0, "감자 1봉", null, null, 4000L)));
        f.receipts.save(receipt("r2", "2026-10-08", "시장", 2, 0, ValidationStatus.PASS,
                item(0, "감자 2봉", null, null, 9000L)));
        f.receipts.save(receipt("r3", "2026-10-09", "시장", 3, 0, ValidationStatus.PASS,
                item(0, "감자 1상자", null, null, 15000L)));
        String id = linkAll(f.products, ProductType.NON_STANDARD, "감자", "감자 1봉", "r1");
        f.products.confirm("r2", 0, "감자 2봉", ProductType.NON_STANDARD, "감자", 2);
        f.products.confirm("r3", 0, "감자 1상자", ProductType.NON_STANDARD, "감자", 3);
        f.v2.savePurchaseFormV2("r1", 0, CatalogField.parsed(new PurchaseForm("1", SalesUnitCode.BAG, "봉"), CatalogField.Confidence.HIGH));
        f.v2.savePurchaseFormV2("r2", 0, CatalogField.parsed(new PurchaseForm("2", SalesUnitCode.BAG, "봉"), CatalogField.Confidence.HIGH));
        f.v2.savePurchaseFormV2("r3", 0, CatalogField.parsed(new PurchaseForm("1", SalesUnitCode.BOX, "상자"), CatalogField.Confidence.HIGH));

        PriceIntelligenceV2 result = f.service().analyze(id);
        assertEquals(2, result.cohorts.size());
        PriceCohortV2 bag = result.cohort("LIKE_FORM:BAG:봉");
        PriceCohortV2 box = result.cohort("LIKE_FORM:BOX:상자");
        assertNotNull(bag);
        assertNotNull(box);
        assertEquals(PriceCohortV2.Strength.CONTEXTUAL_LIKE_FORM, bag.strength);
        assertEquals(2, bag.count());
        bd("4500", bag.latest);
        bd("4000", bag.previous);
        assertEquals(1, box.count());
        bd("15000", box.latest);
        assertNull(result.cohort("WEIGHT_KG"));
    }

    @Test public void commodityWithoutPurchaseFormRemainsVisibleButExcluded() {
        Fixture f = new Fixture();
        f.receipts.save(receipt("r1", "2026-10-01", "시장", 1, 0, ValidationStatus.PASS,
                item(0, "사과", null, null, 5000L)));
        String id = linkAll(f.products, ProductType.NON_STANDARD, "사과", "사과", "r1");
        PriceIntelligenceV2 result = f.service().analyze(id);
        assertEquals(1, result.observations.size());
        assertEquals(PriceObservationV2.Eligibility.MISSING_PURCHASE_FORM, result.observations.get(0).eligibility);
        assertTrue(result.cohorts.isEmpty());
    }

    @Test public void canonicalMetricsCoverEligibilityComparabilityAndScope() {
        Fixture f = new Fixture();
        // STANDARD: 3 eligible + 1 multi-item discount exclusion + 1 invalid.
        f.receipts.save(receipt("s1", "2026-09-01", "A", 1, 0, ValidationStatus.PASS, item(0, "우유", 1, 3000L, 3000L)));
        f.receipts.save(receipt("s2", "2026-09-10", "B", 2, 0, ValidationStatus.PASS, item(0, "우유", 2, 3100L, 6200L)));
        f.receipts.save(receipt("s3", "2026-09-20", "A", 3, 0, ValidationStatus.PASS, item(0, "우유", 1, 2900L, 2900L)));
        List<PersistedItem> multi = new ArrayList<>(); multi.add(item(0,"우유",1,3000L,3000L)); multi.add(item(1,"과자",1,1000L,1000L));
        f.receipts.save(receipt("s4", "2026-09-25", "A", 4, -500, ValidationStatus.PASS, multi));
        f.receipts.save(receipt("s5", "2026-09-30", "A", 5, 0, ValidationStatus.INCOMPLETE, item(0,"우유",1,3000L,3000L)));
        String standard = linkAll(f.products, ProductType.STANDARD, "우유", "우유", "s1","s2","s3","s4","s5");
        PriceIntelligenceV2 sr = f.service().analyze(standard);

        // COMMODITY: two strict weight + two contextual bag + one missing form.
        f.receipts.save(receipt("c1", "2026-09-01", "시장", 11, 0, ValidationStatus.PASS, item(0,"감자1kg",null,null,6000L)));
        f.receipts.save(receipt("c2", "2026-09-05", "시장", 12, 0, ValidationStatus.PASS, item(0,"감자500g",null,null,3200L)));
        f.receipts.save(receipt("c3", "2026-09-10", "시장", 13, 0, ValidationStatus.PASS, item(0,"감자1봉",null,null,4000L)));
        f.receipts.save(receipt("c4", "2026-09-15", "시장", 14, 0, ValidationStatus.PASS, item(0,"감자2봉",null,null,9000L)));
        f.receipts.save(receipt("c5", "2026-09-20", "시장", 15, 0, ValidationStatus.PASS, item(0,"감자",null,null,5000L)));
        String commodity = linkAll(f.products, ProductType.NON_STANDARD, "감자", "감자1kg", "c1");
        f.products.confirm("c2",0,"감자500g",ProductType.NON_STANDARD,"감자",12);
        f.products.confirm("c3",0,"감자1봉",ProductType.NON_STANDARD,"감자",13);
        f.products.confirm("c4",0,"감자2봉",ProductType.NON_STANDARD,"감자",14);
        f.products.confirm("c5",0,"감자",ProductType.NON_STANDARD,"감자",15);
        f.v2.savePurchaseFormV2("c1",0,CatalogField.parsed(new PurchaseForm("1",SalesUnitCode.KILOGRAM,"kg"),CatalogField.Confidence.MEDIUM));
        f.v2.savePurchaseFormV2("c2",0,CatalogField.parsed(new PurchaseForm("500",SalesUnitCode.GRAM,"g"),CatalogField.Confidence.MEDIUM));
        f.v2.savePurchaseFormV2("c3",0,CatalogField.parsed(new PurchaseForm("1",SalesUnitCode.BAG,"봉"),CatalogField.Confidence.HIGH));
        f.v2.savePurchaseFormV2("c4",0,CatalogField.parsed(new PurchaseForm("2",SalesUnitCode.BAG,"봉"),CatalogField.Confidence.HIGH));
        PriceIntelligenceV2 cr = f.service().analyze(commodity);

        int excludedDiscount = count(sr, PriceObservationV2.Eligibility.UNALLOCATED_RECEIPT_DISCOUNT);
        int excludedInvalid = count(sr, PriceObservationV2.Eligibility.INVALID_RECEIPT);
        int missingForm = count(cr, PriceObservationV2.Eligibility.MISSING_PURCHASE_FORM);
        int strictCommodity = 0, contextualCommodity = 0;
        for (PriceCohortV2 c : cr.cohorts) {
            if (c.strength == PriceCohortV2.Strength.STRICT_NORMALIZED) strictCommodity++;
            else contextualCommodity++;
        }
        int scopeChecks = 0;
        if (f.service().analyze(standard, PriceScopeV2.store("A")).eligibleCount() == 2) scopeChecks++;
        if (f.service().analyze(standard, PriceScopeV2.period("2026-09-05","2026-09-22")).eligibleCount() == 2) scopeChecks++;

        int totalObservations = sr.observations.size() + cr.observations.size();
        int eligible = sr.eligibleCount() + cr.eligibleCount();
        System.out.println("CP27_METRICS observations=" + totalObservations
                + " eligible=" + eligible
                + " excluded_discount=" + excludedDiscount
                + " excluded_invalid=" + excludedInvalid
                + " missing_form=" + missingForm
                + " standard_cohorts=" + sr.cohorts.size()
                + " commodity_strict_cohorts=" + strictCommodity
                + " commodity_contextual_cohorts=" + contextualCommodity
                + " scope_checks=" + scopeChecks
                + " receipt_traceable_rates=" + eligible);

        assertEquals(10, totalObservations);
        assertEquals(7, eligible);
        assertEquals(1, excludedDiscount);
        assertEquals(1, excludedInvalid);
        assertEquals(1, missingForm);
        assertEquals(1, sr.cohorts.size());
        assertEquals(1, strictCommodity);
        assertEquals(1, contextualCommodity);
        assertEquals(2, scopeChecks);
    }

    private static int count(PriceIntelligenceV2 result, PriceObservationV2.Eligibility eligibility) {
        int n=0; for (PriceObservationV2 o : result.observations) if (o.eligibility == eligibility) n++; return n;
    }

    private static String linkAll(InMemoryProductCatalogStore products, ProductType type, String canonical,
            String alias, String... receiptIds) {
        IdentityResolution first = products.confirm(receiptIds[0], 0, alias, type, canonical, 1);
        for (int i=1;i<receiptIds.length;i++) products.resolveAndLinkExact(receiptIds[i], 0, alias);
        return first.product.id;
    }

    private static PersistedItem item(int ordinal, String name, Integer quantity, Long unitPrice, Long lineAmount) {
        return new PersistedItem(ordinal, ordinal + 1, name, quantity, unitPrice, lineAmount,
                quantity == null ? ValueOrigin.UNKNOWN : ValueOrigin.PRINTED,
                unitPrice == null ? ValueOrigin.UNKNOWN : ValueOrigin.PRINTED,
                lineAmount == null ? ValueOrigin.UNKNOWN : ValueOrigin.PRINTED,
                ItemResolution.EXACT, "test");
    }

    private static ReceiptRecord receipt(String id, String date, String store, long created, long discount,
            ValidationStatus status, PersistedItem... items) {
        List<PersistedItem> list = new ArrayList<>(); Collections.addAll(list, items);
        return receipt(id,date,store,created,discount,status,list);
    }

    private static ReceiptRecord receipt(String id, String date, String store, long created, long discount,
            ValidationStatus status, List<PersistedItem> items) {
        long sum=0; for (PersistedItem item : items) if (item.lineAmount != null) sum += item.lineAmount;
        long net=sum+discount;
        return new ReceiptRecord(id, created, date, store, "", net, sum, discount, net, 0L, status,
                100, 200, false, Collections.<String>emptyList(), items);
    }

    private static void bd(String expected, BigDecimal actual) {
        assertNotNull(actual);
        assertEquals(0, new BigDecimal(expected).compareTo(actual));
    }

    private static final class Fixture {
        final InMemoryReceiptStore receipts = new InMemoryReceiptStore();
        final InMemoryProductCatalogStore products = new InMemoryProductCatalogStore();
        final MemoryV2Store v2 = new MemoryV2Store();
        PriceIntelligenceServiceV2 service() { return new PriceIntelligenceServiceV2(receipts, products, v2); }
    }

    private static final class MemoryV2Store implements CatalogV2PersistenceStore {
        private final Map<String,CatalogField<PurchaseForm>> forms = new HashMap<>();
        @Override public CatalogEntryV2 catalogEntryV2(String id) { return null; }
        @Override public void saveCatalogEntryV2(CatalogEntryV2 entry) {}
        @Override public void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId) {}
        @Override public String aliasCatalogEntryIdV2(AliasContext context, String rawAlias) { return null; }
        @Override public void savePurchaseFormV2(String receiptId, int itemOrdinal, CatalogField<PurchaseForm> purchaseForm) {
            forms.put(receiptId + "#" + itemOrdinal, purchaseForm);
        }
        @Override public CatalogField<PurchaseForm> purchaseFormV2(String receiptId, int itemOrdinal) {
            CatalogField<PurchaseForm> field = forms.get(receiptId + "#" + itemOrdinal);
            return field == null ? CatalogField.<PurchaseForm>absent() : field;
        }
    }
}
