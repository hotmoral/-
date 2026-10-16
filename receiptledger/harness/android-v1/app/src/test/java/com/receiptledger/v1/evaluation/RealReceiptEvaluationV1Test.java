package com.receiptledger.v1.evaluation;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.commoditydetail.CommodityDetailServiceV1;
import com.receiptledger.v1.commoditydetail.CommodityDetailV1;
import com.receiptledger.v1.detail.ProductDetailServiceV1;
import com.receiptledger.v1.detail.ProductDetailV1;
import com.receiptledger.v1.document.PointD;
import com.receiptledger.v1.document.Quad;
import com.receiptledger.v1.ocr.OcrBlock;
import com.receiptledger.v1.ocr.OcrDocument;
import com.receiptledger.v1.ocr.OcrElement;
import com.receiptledger.v1.ocr.OcrLine;
import com.receiptledger.v1.persistence.InMemoryReceiptStore;
import com.receiptledger.v1.persistence.PersistedItem;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.persistence.ReceiptRecordFactory;
import com.receiptledger.v1.priceeval.PriceEvaluationServiceV1;
import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.PriceCohortV2;
import com.receiptledger.v1.priceintel.PriceIntelligenceServiceV2;
import com.receiptledger.v1.priceintel.PriceIntelligenceV2;
import com.receiptledger.v1.priceintel.PriceObservationV2;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.IdentityResolution;
import com.receiptledger.v1.product.InMemoryProductCatalogStore;
import com.receiptledger.v1.product.LinkSource;
import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.recovery.RecognitionCandidate;
import com.receiptledger.v1.recovery.RecognitionPass;
import com.receiptledger.v1.recovery.ReceiptRecognitionPipeline;
import com.receiptledger.v1.review.CaptureReviewAssessmentV2;
import com.receiptledger.v1.semantics.ReceiptProductSemanticParser;
import com.receiptledger.v1.semantics.ReceiptProductSemantics;
import com.receiptledger.v1.validation.ValidationStatus;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

import org.junit.Test;

/** CP35 public-safe end-to-end evaluation over the frozen production services. */
public final class RealReceiptEvaluationV1Test {

    @Test public void canonicalPublicSafeCorpusRegistersPurchasesSafely() {
        Fixture f = new Fixture();
        ReceiptProductSemanticParser semantics = ReceiptProductSemanticParser.withoutBrandKnowledge();

        // RRE-01: new STANDARD product. Recognition is correct, but identity remains unresolved until confirmation.
        ReceiptRecord s1 = receipt("rre-01", 1L, "가상마트A", "2026-10-01",
                lines(line("서울우유1L", 3200, 1, 3200)), null, 3200, ValidationStatus.PASS);
        assertAutoConfirmed(s1);
        f.receipts.save(s1);
        ReceiptProductSemantics milkSemantics = semantics.parse(s1.items.get(0).name);
        assertNotNull(milkSemantics.productName);
        assertNotNull(milkSemantics.specification);
        assertFalse(f.products.resolveAndLinkExact(s1.id, 0, s1.items.get(0).name).classified());
        IdentityResolution milkConfirmed = f.products.confirm(
                s1.id, 0, s1.items.get(0).name, ProductType.STANDARD, "서울우유 1L", 1L);
        assertTrue(milkConfirmed.classified());
        String milkId = milkConfirmed.product.id;
        PriceCohortV2 milkOne = f.price().analyze(milkId).cohort("STANDARD_PACKAGE");
        assertNotNull(milkOne);
        assertEquals(1, milkOne.count());
        bd("3200", milkOne.latest);

        // RRE-02: confirmed exact alias reuses the same stable ID without creating another product.
        ReceiptRecord s2 = receipt("rre-02", 2L, "가상마트B", "2026-10-05",
                lines(line("서울우유1L", 3000, 1, 3000)), null, 3000, ValidationStatus.PASS);
        assertAutoConfirmed(s2);
        f.receipts.save(s2);
        IdentityResolution repeat = f.products.resolveAndLinkExact(s2.id, 0, s2.items.get(0).name);
        assertTrue(repeat.classified());
        assertEquals(LinkSource.EXACT_ALIAS, repeat.source);
        assertEquals(milkId, repeat.product.id);
        assertEquals(1, f.products.listProducts().size());
        PriceCohortV2 milkTwo = f.price().analyze(milkId).cohort("STANDARD_PACKAGE");
        assertEquals(2, milkTwo.count());
        bd("3000", milkTwo.latest);
        bd("3200", milkTwo.previous);

        // RRE-03: similarity is not authority. 900mL must not inherit the 1L alias.
        ReceiptRecord s3 = receipt("rre-03", 3L, "가상마트C", "2026-10-06",
                lines(line("서울우유900mL", 2900, 1, 2900)), null, 2900, ValidationStatus.PASS);
        assertAutoConfirmed(s3);
        f.receipts.save(s3);
        IdentityResolution similar = f.products.resolveAndLinkExact(s3.id, 0, s3.items.get(0).name);
        assertFalse(similar.classified());
        assertEquals(ProductType.UNCLASSIFIED, similar.type);
        assertEquals(2, f.products.linksForProduct(milkId).size());

        // RRE-04: one explicitly confirmed commodity, two physical forms, one strict WEIGHT_KG cohort.
        ReceiptRecord w1 = receipt("rre-04a", 4L, "가상시장", "2026-10-07",
                lines(line("감자 1kg", 6000, 1, 6000)), null, 6000, ValidationStatus.PASS);
        ReceiptRecord w2 = receipt("rre-04b", 5L, "가상시장", "2026-10-08",
                lines(line("감자 500g", 3300, 1, 3300)), null, 3300, ValidationStatus.PASS);
        assertAutoConfirmed(w1);
        assertAutoConfirmed(w2);
        f.receipts.save(w1);
        f.receipts.save(w2);
        IdentityResolution potato1 = f.products.confirm(w1.id, 0, w1.items.get(0).name,
                ProductType.NON_STANDARD, "감자", 4L);
        IdentityResolution potato2 = f.products.confirm(w2.id, 0, w2.items.get(0).name,
                ProductType.NON_STANDARD, "감자", 5L);
        assertEquals(potato1.product.id, potato2.product.id);
        String potatoId = potato1.product.id;
        saveParsedPurchaseForm(f, semantics, w1);
        saveParsedPurchaseForm(f, semantics, w2);
        PriceCohortV2 weight = f.price().analyze(potatoId).cohort("WEIGHT_KG");
        assertNotNull(weight);
        assertEquals(2, weight.count());
        bd("6600", weight.latest);
        bd("6000", weight.previous);

        // RRE-05: same commodity grouping does not make 봉 and 상자 mutually comparable.
        ReceiptRecord c1 = receipt("rre-05a", 6L, "가상시장", "2026-10-09",
                lines(line("감자 1봉", 4000, 1, 4000)), null, 4000, ValidationStatus.PASS);
        ReceiptRecord c2 = receipt("rre-05b", 7L, "가상시장", "2026-10-10",
                lines(line("감자 1상자", 15000, 1, 15000)), null, 15000, ValidationStatus.PASS);
        assertAutoConfirmed(c1);
        assertAutoConfirmed(c2);
        f.receipts.save(c1);
        f.receipts.save(c2);
        assertEquals(potatoId, f.products.confirm(c1.id, 0, c1.items.get(0).name,
                ProductType.NON_STANDARD, "감자", 6L).product.id);
        assertEquals(potatoId, f.products.confirm(c2.id, 0, c2.items.get(0).name,
                ProductType.NON_STANDARD, "감자", 7L).product.id);
        saveParsedPurchaseForm(f, semantics, c1);
        saveParsedPurchaseForm(f, semantics, c2);
        PriceIntelligenceV2 potato = f.price().analyze(potatoId);
        PriceCohortV2 bag = potato.cohort("LIKE_FORM:BAG:봉");
        PriceCohortV2 box = potato.cohort("LIKE_FORM:BOX:상자");
        assertNotNull(bag);
        assertNotNull(box);
        assertEquals(1, bag.count());
        assertEquals(1, box.count());
        assertEquals(2, potato.cohort("WEIGHT_KG").count());
        PriceEvaluationServiceV1 evaluator = new PriceEvaluationServiceV1();
        PriceEvaluationV1 bagEvaluation = evaluator.evaluate(bag);
        PriceEvaluationV1 boxEvaluation = evaluator.evaluate(box);
        assertEquals(PriceEvaluationV1.Status.CONTEXTUAL_ONLY, bagEvaluation.status);
        assertEquals(PriceEvaluationV1.Judgment.NONE, bagEvaluation.judgment);
        assertEquals(PriceEvaluationV1.Status.CONTEXTUAL_ONLY, boxEvaluation.status);
        assertEquals(PriceEvaluationV1.Judgment.NONE, boxEvaluation.judgment);

        // RRE-06: receipt-level discount over multiple items must not be allocated to milk.
        ReceiptRecord d1 = receipt("rre-06", 8L, "가상마트A", "2026-10-11",
                lines(line("서울우유1L", 3200, 1, 3200), line("신라면5입", 4990, 1, 4990)),
                -500L, 7690, ValidationStatus.PASS);
        assertAutoConfirmed(d1);
        f.receipts.save(d1);
        IdentityResolution discountMilk = f.products.resolveAndLinkExact(d1.id, 0, d1.items.get(0).name);
        assertTrue(discountMilk.classified());
        assertEquals(milkId, discountMilk.product.id);
        PriceIntelligenceV2 milkAfterDiscount = f.price().analyze(milkId);
        PriceObservationV2 discountObservation = observation(milkAfterDiscount, d1.id);
        assertNotNull(discountObservation);
        assertEquals(PriceObservationV2.Eligibility.UNALLOCATED_RECEIPT_DISCOUNT, discountObservation.eligibility);
        assertEquals(2, milkAfterDiscount.cohort("STANDARD_PACKAGE").count());

        // RRE-07: mismatch must be review-blocked and remains excluded even if invalid legacy data were linked.
        ReceiptRecord mismatch = receipt("rre-07", 9L, "가상마트D", "2026-10-12",
                lines(line("테스트과자", 2000, 1, 2000), line("테스트음료", 1500, 1, 1500)),
                null, 3000, ValidationStatus.MISMATCH);
        CaptureReviewAssessmentV2 mismatchAssessment = CaptureReviewAssessmentV2.assess(mismatch);
        assertEquals(CaptureReviewAssessmentV2.Decision.REVIEW_REQUIRED, mismatchAssessment.decision);
        assertTrue(mismatchAssessment.flags(CaptureReviewAssessmentV2.ReceiptField.PRINTED_TOTAL));
        assertTrue(mismatchAssessment.reviewItemCount() >= 1);
        f.receipts.save(mismatch);
        IdentityResolution invalidSnack = f.products.confirm(mismatch.id, 0, mismatch.items.get(0).name,
                ProductType.STANDARD, "테스트과자", 9L);
        PriceIntelligenceV2 invalidPrice = f.price().analyze(invalidSnack.product.id);
        assertEquals(0, invalidPrice.eligibleCount());
        assertEquals(PriceObservationV2.Eligibility.INVALID_RECEIPT,
                observation(invalidPrice, mismatch.id).eligibility);

        // RRE-08: CP31/32 projections must preserve exact receipt IDs and eligibility facts.
        ProductDetailV1 milkDetail = new ProductDetailServiceV1(f.products, f.v2, f.price()).load(milkId);
        assertEquals(3, milkDetail.purchases.size());
        assertEquals(2, milkDetail.comparablePurchases().size());
        assertReceiptIds(milkDetail.purchases, "rre-01", "rre-02", "rre-06");
        ProductDetailV1.PurchaseRow excludedRow = productRow(milkDetail, "rre-06");
        assertNotNull(excludedRow);
        assertFalse(excludedRow.comparable);
        assertEquals(PriceObservationV2.Eligibility.UNALLOCATED_RECEIPT_DISCOUNT, excludedRow.eligibility);

        CommodityDetailV1 potatoDetail = new CommodityDetailServiceV1(f.products, f.v2, f.price()).load(potatoId);
        assertEquals(4, potatoDetail.purchases.size());
        assertNotNull(potatoDetail.strictSection("WEIGHT_KG"));
        assertNotNull(potatoDetail.contextualSection("LIKE_FORM:BAG:봉"));
        assertNotNull(potatoDetail.contextualSection("LIKE_FORM:BOX:상자"));
        assertCommodityReceiptIds(potatoDetail, "rre-04a", "rre-04b", "rre-05a", "rre-05b");

        assertEquals(9, f.receipts.count());
        assertEquals(3, f.products.linksForProduct(milkId).size());
        assertEquals(4, f.products.linksForProduct(potatoId).size());

        System.out.println(
                "CP35_METRICS evaluation_version=1 fixtures=8 receipts=9 items=11 "
                + "structured_correct=9 auto_confirmed=8 review_required=1 "
                + "final_safe_registrations=7 exact_alias_reuse=2 conservative_unresolved=1 "
                + "false_auto_links=0 strict_weight_observations=2 contextual_cohorts=2 "
                + "discount_exclusions=1 invalid_exclusions=1 detail_trace_rows=7 schema_unchanged=1");
    }

    private static void saveParsedPurchaseForm(Fixture f, ReceiptProductSemanticParser parser, ReceiptRecord record) {
        PersistedItem item = record.items.get(0);
        ReceiptProductSemantics parsed = parser.parse(item.name);
        assertNotNull("expected purchase-form evidence for " + item.name, parsed.purchaseForm);
        f.v2.savePurchaseFormV2(record.id, item.ordinal, parsed.purchaseForm.asCatalogField());
    }

    private static ReceiptRecord receipt(
            String id,
            long createdAt,
            String store,
            String date,
            List<ItemLine> items,
            Long discount,
            long total,
            ValidationStatus expectedStatus) {
        RecognitionCandidate candidate = recognize(store, date, items, discount, total);
        assertEquals(id, expectedStatus, candidate.validation.status);
        ReceiptRecord record = ReceiptRecordFactory.create(
                id, createdAt, candidate.document, candidate.structure, candidate.items,
                candidate.validation, 180, 240, false);
        assertEquals(id, store, record.storeName);
        assertEquals(id, date, record.purchaseDate);
        assertEquals(id, Long.valueOf(total), record.printedTotal);
        assertEquals(id, items.size(), record.items.size());
        assertEquals(id, expectedStatus, record.validationStatus);
        for (int i = 0; i < items.size(); i++) {
            ItemLine expected = items.get(i);
            PersistedItem actual = record.items.get(i);
            assertEquals(id + " name " + i, expected.name, actual.name);
            assertEquals(id + " quantity " + i, Integer.valueOf(expected.quantity), actual.quantity);
            assertEquals(id + " unit price " + i, Long.valueOf(expected.unitPrice), actual.unitPrice);
            assertEquals(id + " line amount " + i, Long.valueOf(expected.lineAmount), actual.lineAmount);
        }
        return record;
    }

    private static RecognitionCandidate recognize(
            String store, String date, List<ItemLine> items, Long discount, long total) {
        List<OcrElement> elements = new ArrayList<>();
        double y = 10;
        elements.add(token(store, 10, y, 55));
        y += 20;
        elements.add(token(date, 10, y, 58));
        StringBuilder raw = new StringBuilder().append(store).append('\n').append(date).append('\n');
        for (ItemLine item : items) {
            y += 20;
            elements.add(token(item.name, 10, y, 50));
            elements.add(token(money(item.unitPrice), 72, y, 30));
            elements.add(token(String.valueOf(item.quantity), 108, y, 10));
            elements.add(token(money(item.lineAmount), 128, y, 36));
            raw.append(item.name).append(' ').append(money(item.unitPrice)).append(' ')
                    .append(item.quantity).append(' ').append(money(item.lineAmount)).append('\n');
        }
        if (discount != null && discount != 0L) {
            y += 20;
            elements.add(token("쿠폰할인", 10, y, 42));
            elements.add(token(money(discount), 128, y, 36));
            raw.append("쿠폰할인 ").append(money(discount)).append('\n');
        }
        y += 20;
        elements.add(token("합계", 10, y, 20));
        elements.add(token(money(total), 128, y, 36));
        raw.append("합계 ").append(money(total)).append('\n');
        y += 20;
        elements.add(token("신용카드", 10, y, 42));
        elements.add(token(money(total), 128, y, 36));
        raw.append("신용카드 ").append(money(total));

        Collections.reverse(elements);
        OcrLine deliberatelyWrongMlKitLine = new OcrLine("all-in-one", null, null, elements);
        OcrDocument document = new OcrDocument(raw.toString(), 180, (int) y + 20,
                Collections.singletonList(new OcrBlock(
                        "all", null, null, Collections.singletonList(deliberatelyWrongMlKitLine))));
        return new ReceiptRecognitionPipeline().evaluate(RecognitionPass.ORIGINAL, document);
    }

    private static void assertAutoConfirmed(ReceiptRecord record) {
        CaptureReviewAssessmentV2 assessment = CaptureReviewAssessmentV2.assess(record);
        assertEquals(record.id, CaptureReviewAssessmentV2.Decision.AUTO_CONFIRMED, assessment.decision);
        assertEquals(record.id, 0, assessment.reviewItemCount());
    }

    private static PriceObservationV2 observation(PriceIntelligenceV2 result, String receiptId) {
        for (PriceObservationV2 row : result.observations) if (receiptId.equals(row.receiptId)) return row;
        return null;
    }

    private static ProductDetailV1.PurchaseRow productRow(ProductDetailV1 detail, String receiptId) {
        for (ProductDetailV1.PurchaseRow row : detail.purchases) if (receiptId.equals(row.receiptId)) return row;
        return null;
    }

    private static void assertReceiptIds(List<ProductDetailV1.PurchaseRow> rows, String... expected) {
        Set<String> actual = new HashSet<>();
        for (ProductDetailV1.PurchaseRow row : rows) actual.add(row.receiptId);
        assertEquals(new HashSet<>(java.util.Arrays.asList(expected)), actual);
    }

    private static void assertCommodityReceiptIds(CommodityDetailV1 detail, String... expected) {
        Set<String> actual = new HashSet<>();
        for (CommodityDetailV1.PurchaseRow row : detail.purchases) actual.add(row.observation.receiptId);
        assertEquals(new HashSet<>(java.util.Arrays.asList(expected)), actual);
    }

    private static void bd(String expected, BigDecimal actual) {
        assertNotNull(actual);
        assertEquals(0, new BigDecimal(expected).compareTo(actual));
    }

    private static String money(long value) {
        return String.format(Locale.ROOT, "%,d", value);
    }

    private static ItemLine line(String name, long unitPrice, int quantity, long lineAmount) {
        return new ItemLine(name, unitPrice, quantity, lineAmount);
    }

    private static List<ItemLine> lines(ItemLine... values) {
        List<ItemLine> out = new ArrayList<>();
        Collections.addAll(out, values);
        return out;
    }

    private static OcrElement token(String text, double x, double y, double width) {
        Quad q = new Quad(new PointD(x, y), new PointD(x + width, y),
                new PointD(x + width, y + 10), new PointD(x, y + 10));
        return new OcrElement(text, q, q);
    }

    private static final class ItemLine {
        final String name;
        final long unitPrice;
        final int quantity;
        final long lineAmount;

        ItemLine(String name, long unitPrice, int quantity, long lineAmount) {
            this.name = name;
            this.unitPrice = unitPrice;
            this.quantity = quantity;
            this.lineAmount = lineAmount;
        }
    }

    private static final class Fixture {
        final InMemoryReceiptStore receipts = new InMemoryReceiptStore();
        final InMemoryProductCatalogStore products = new InMemoryProductCatalogStore();
        final MemoryV2Store v2 = new MemoryV2Store();

        PriceIntelligenceServiceV2 price() {
            return new PriceIntelligenceServiceV2(receipts, products, v2);
        }
    }

    private static final class MemoryV2Store implements CatalogV2PersistenceStore {
        private final Map<String, CatalogField<PurchaseForm>> forms = new HashMap<>();

        @Override public CatalogEntryV2 catalogEntryV2(String id) { return null; }
        @Override public void saveCatalogEntryV2(CatalogEntryV2 entry) {}
        @Override public void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId) {}
        @Override public String aliasCatalogEntryIdV2(AliasContext context, String rawAlias) { return null; }

        @Override public void savePurchaseFormV2(
                String receiptId, int itemOrdinal, CatalogField<PurchaseForm> purchaseForm) {
            forms.put(receiptId + "#" + itemOrdinal, purchaseForm);
        }

        @Override public CatalogField<PurchaseForm> purchaseFormV2(String receiptId, int itemOrdinal) {
            CatalogField<PurchaseForm> field = forms.get(receiptId + "#" + itemOrdinal);
            return field == null ? CatalogField.<PurchaseForm>absent() : field;
        }
    }
}
