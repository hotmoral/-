package com.receiptledger.v1.semantics;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.ProductSpecification;
import com.receiptledger.v1.catalog.PurchaseForm;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.Test;

public final class ReceiptProductSemanticParserTest {
    private static final ReceiptProductSemanticParser PARSER = new ReceiptProductSemanticParser(Arrays.asList(
            "서울우유", "농심", "비비고", "오뚜기", "매일우유", "코카콜라", "동원"));

    @Test public void parsedEvidenceNeverBecomesConfirmed() {
        ReceiptProductSemantics r = PARSER.parse("농심 신라면 5입");
        assertNotNull(r.brand);
        assertEquals(CatalogField.Confidence.HIGH, r.brand.confidence);
        assertEquals(CatalogField.Source.PARSED_FROM_RECEIPT, r.brand.asCatalogField().source);
        assertEquals(CatalogField.Confirmation.UNCONFIRMED, r.brand.asCatalogField().confirmation);
        assertFalse(r.brand.asCatalogField().isConfirmed());
    }

    @Test public void explicitMultipackProducesExactTotalAndInnerContent() {
        ReceiptProductSemantics r = PARSER.parse("주스 200MLX6");
        assertNotNull(r.specification);
        assertEquals("NET=VOLUME:1200|PACK=6|INNER=VOLUME:200", r.specification.value.candidateToken());
        assertFalse(r.measureAmbiguous);
        assertFalse(r.reviewRequired);
    }

    @Test public void standalonePhysicalMeasurePreservesBothReadingsAndRequiresReview() {
        ReceiptProductSemantics r = PARSER.parse("감자 1KG");
        assertEquals("감자", r.productName.value);
        assertEquals("NET=WEIGHT:1000|PACK=?|INNER=?", r.specification.value.candidateToken());
        assertEquals("1", r.purchaseForm.value.quantity.toPlainString());
        assertTrue(r.measureAmbiguous);
        assertTrue(r.reviewRequired);
    }

    @Test public void unknownBrandIsNotInventedFromFirstToken() {
        ReceiptProductSemantics r = PARSER.parse("새브랜드 초코바 50G");
        assertNull(r.brand);
        assertEquals("새브랜드 초코바", r.productName.value);
        assertTrue(r.reviewRequired);
    }

    @Test public void numericParentheticalPromotionIsNotVariant() {
        ReceiptProductSemantics r = PARSER.parse("제품A (1+1) 500G");
        assertNull(r.variant);
        assertEquals("제품A (1+1)", r.productName.value);
    }

    @Test public void strongAndContextSensitivePurchaseFormsStayDistinct() {
        ReceiptProductSemantics bag = PARSER.parse("감자 1봉");
        ReceiptProductSemantics pack = PARSER.parse("세제 리필 2팩");
        assertEquals(CatalogField.Confidence.HIGH, bag.purchaseForm.confidence);
        assertFalse(bag.reviewRequired);
        assertEquals(CatalogField.Confidence.MEDIUM, pack.purchaseForm.confidence);
        assertTrue(pack.reviewRequired);
    }

    @Test public void localGoldenMetricsMeetConservativeThresholds() {
        List<Fixture> fixtures = Arrays.asList(
                f("농심 신라면 5입", "농심", "신라면", null, "NET=?|PACK=5|INNER=?", null),
                f("오뚜기 진라면 (매운맛) 5입", "오뚜기", "진라면", "매운맛", "NET=?|PACK=5|INNER=?", null),
                f("주스 200MLX6", null, "주스", null, "NET=VOLUME:1200|PACK=6|INNER=VOLUME:200", null),
                f("탄산수 6X200ML", null, "탄산수", null, "NET=VOLUME:1200|PACK=6|INNER=VOLUME:200", null),
                f("동원 참치 100G 4입", "동원", "참치", null, "NET=WEIGHT:400|PACK=4|INNER=WEIGHT:100", null),
                f("코카콜라 제로 500ML 2입", "코카콜라", "제로", null, "NET=VOLUME:1000|PACK=2|INNER=VOLUME:500", null),
                f("서울우유 나100% 1000ML", "서울우유", "나100%", null, "NET=VOLUME:1000|PACK=?|INNER=?", "1000|MILLILITER"),
                f("비비고 왕교자 1.05KG", "비비고", "왕교자", null, "NET=WEIGHT:1050|PACK=?|INNER=?", "1.05|KILOGRAM"),
                f("감자 1KG", null, "감자", null, "NET=WEIGHT:1000|PACK=?|INNER=?", "1|KILOGRAM"),
                f("생수 2L", null, "생수", null, "NET=VOLUME:2000|PACK=?|INNER=?", "2|LITER"),
                f("감자 1봉", null, "감자", null, null, "1|BAG"),
                f("대파 1단", null, "대파", null, null, "1|BUNDLE"),
                f("과자 3봉", null, "과자", null, null, "3|BAG"),
                f("상품 1상자", null, "상품", null, null, "1|BOX"),
                f("사과 5개", null, "사과", null, null, "5|EACH"),
                f("세제 리필 2팩", null, "세제 리필", null, null, "2|PACK"),
                f("[브랜드X] 테스트제품 500G", "브랜드X", "테스트제품", null, "NET=WEIGHT:500|PACK=?|INNER=?", "500|GRAM"),
                f("요거트 (저지방) 450G", null, "요거트", "저지방", "NET=WEIGHT:450|PACK=?|INNER=?", "450|GRAM"),
                f("제품A (1+1) 500G", null, "제품A (1+1)", null, "NET=WEIGHT:500|PACK=?|INNER=?", "500|GRAM"),
                f("신라면10개입", null, "신라면", null, "NET=?|PACK=10|INNER=?", null),
                f("우유 1L 2입", null, "우유", null, "NET=VOLUME:2000|PACK=2|INNER=VOLUME:1000", null),
                f("양파", null, "양파", null, null, null),
                f("ABC123 9900", null, "ABC123 9900", null, null, null),
                f("", null, null, null, null, null),
                // Deliberate conservative misses: brand/variant knowledge is not guessed.
                f("새브랜드 초코바 50G", "새브랜드", "초코바", null, "NET=WEIGHT:50|PACK=?|INNER=?", "50|GRAM"),
                f("오뚜기 진라면 매운맛 5입", "오뚜기", "진라면", "매운맛", "NET=?|PACK=5|INNER=?", null));

        Counts counts = new Counts();
        int reviewRequired = 0;
        int semanticReady = 0;
        int ambiguous = 0;
        int ambiguousReviewed = 0;

        for (Fixture fixture : fixtures) {
            ReceiptProductSemantics actual = PARSER.parse(fixture.raw);
            score(counts, fixture.brand, value(actual.brand));
            score(counts, fixture.product, value(actual.productName));
            score(counts, fixture.variant, value(actual.variant));
            score(counts, fixture.spec, spec(actual.specification));
            score(counts, fixture.purchase, purchase(actual.purchaseForm));
            if (actual.reviewRequired) reviewRequired++; else semanticReady++;
            if (actual.measureAmbiguous) {
                ambiguous++;
                if (actual.reviewRequired) ambiguousReviewed++;
            }
        }

        ReceiptProductSemantics negativeA = PARSER.parse("ABC123 9900");
        ReceiptProductSemantics negativeB = PARSER.parse("");
        int noInventionNegatives = 0;
        if (negativeA.brand == null && negativeA.specification == null && negativeA.purchaseForm == null) noInventionNegatives++;
        if (negativeB.brand == null && negativeB.specification == null && negativeB.purchaseForm == null) noInventionNegatives++;

        long precisionPpm = counts.predicted == 0 ? 1_000_000L : counts.correct * 1_000_000L / counts.predicted;
        long recallPpm = counts.expected == 0 ? 1_000_000L : counts.correct * 1_000_000L / counts.expected;

        System.out.println("CP23_METRICS fixtures=" + fixtures.size()
                + " expected_fields=" + counts.expected
                + " predicted_fields=" + counts.predicted
                + " correct_fields=" + counts.correct
                + " precision_ppm=" + precisionPpm
                + " recall_ppm=" + recallPpm
                + " review_required=" + reviewRequired
                + " semantic_ready=" + semanticReady
                + " ambiguous=" + ambiguous
                + " ambiguous_reviewed=" + ambiguousReviewed
                + " no_invention_negatives=" + noInventionNegatives);

        assertTrue("precision", precisionPpm >= 900_000L);
        assertTrue("recall", recallPpm >= 850_000L);
        assertTrue("expected ambiguity coverage", ambiguous > 0);
        assertEquals("all ambiguity must require review", ambiguous, ambiguousReviewed);
        assertEquals("negative fixtures must not invent structured semantics", 2, noInventionNegatives);
    }

    private static String value(SemanticCandidate<String> candidate) {
        return candidate == null ? null : candidate.value;
    }

    private static String spec(SemanticCandidate<ProductSpecification> candidate) {
        return candidate == null ? null : candidate.value.candidateToken();
    }

    private static String purchase(SemanticCandidate<PurchaseForm> candidate) {
        if (candidate == null) return null;
        return candidate.value.quantity.toPlainString() + "|" + candidate.value.unit.name();
    }

    private static void score(Counts counts, String expected, String predicted) {
        if (expected != null) counts.expected++;
        if (predicted != null) counts.predicted++;
        if (expected != null && expected.equals(predicted)) counts.correct++;
    }

    private static Fixture f(String raw, String brand, String product, String variant, String spec, String purchase) {
        return new Fixture(raw, brand, product, variant, spec, purchase);
    }

    private static final class Counts { int expected; int predicted; int correct; }

    private static final class Fixture {
        final String raw, brand, product, variant, spec, purchase;
        Fixture(String raw, String brand, String product, String variant, String spec, String purchase) {
            this.raw = raw; this.brand = brand; this.product = product; this.variant = variant;
            this.spec = spec; this.purchase = purchase;
        }
    }
}
