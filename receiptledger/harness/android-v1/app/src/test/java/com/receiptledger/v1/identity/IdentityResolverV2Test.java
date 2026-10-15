package com.receiptledger.v1.identity;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.PackageMeasure;
import com.receiptledger.v1.catalog.ProductSpecification;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.catalog.SalesUnitCode;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.ProductNameNormalizer;
import com.receiptledger.v1.semantics.ReceiptProductSemanticParser;
import com.receiptledger.v1.semantics.ReceiptProductSemantics;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.Test;

public final class IdentityResolverV2Test {
    private final IdentityResolverV2 resolver = new IdentityResolverV2();
    private final ReceiptProductSemanticParser parser = new ReceiptProductSemanticParser(
            Arrays.asList("농심", "코카콜라", "비비고", "서울우유", "오뚜기", "해태"));

    @Test public void merchantExactAliasPrecedesDifferentGlobalAlias() {
        FakeKnowledge k = standardKnowledge();
        k.alias(AliasContext.global(), "매장코드A", "P5");
        k.alias(AliasContext.merchant("STORE-A"), "매장코드A", "P10");
        IdentityDecisionV2 d = resolver.resolve("매장코드A", "STORE-A", parser.parse("매장코드A"), k);
        assertEquals(IdentityDecisionV2.Status.AUTO_LINK, d.status);
        assertEquals(IdentityDecisionV2.Authority.MERCHANT_EXACT_ALIAS, d.authority);
        assertEquals("P10", d.catalogEntryId);
    }

    @Test public void exactAliasStrongContradictionFailsToReview() {
        FakeKnowledge k = standardKnowledge();
        k.alias(AliasContext.merchant("STORE-A"), "[농심] 신라면 10입", "P5");
        IdentityDecisionV2 d = resolver.resolve(
                "[농심] 신라면 10입", "STORE-A", parser.parse("[농심] 신라면 10입"), k);
        assertEquals(IdentityDecisionV2.Status.REVIEW, d.status);
        assertEquals(IdentityDecisionV2.Authority.ALIAS_CONFLICT, d.authority);
        assertTrue(d.includesCandidate("P5"));
    }

    @Test public void strictConfirmedSemanticsCanAutoLinkOnlyUniqueCompleteCandidate() {
        FakeKnowledge k = standardKnowledge();
        IdentityDecisionV2 d = resolver.resolve(
                "[농심] 신라면 5입", "STORE-A", parser.parse("[농심] 신라면 5입"), k);
        assertEquals(IdentityDecisionV2.Status.AUTO_LINK, d.status);
        assertEquals(IdentityDecisionV2.Authority.STRICT_SEMANTIC_EXACT, d.authority);
        assertEquals("P5", d.catalogEntryId);
    }

    @Test public void weakOrAmbiguousSemanticsRemainReviewGated() {
        FakeKnowledge k = standardKnowledge();
        IdentityDecisionV2 missingBrand = resolver.resolve(
                "신라면 5입", "STORE-A", parser.parse("신라면 5입"), k);
        assertEquals(IdentityDecisionV2.Status.REVIEW, missingBrand.status);
        assertEquals("P5", missingBrand.catalogEntryId);

        IdentityDecisionV2 ambiguousMeasure = resolver.resolve(
                "[비비고] 왕교자 1.05KG", "STORE-A", parser.parse("[비비고] 왕교자 1.05KG"), k);
        assertEquals(IdentityDecisionV2.Status.REVIEW, ambiguousMeasure.status);
        assertEquals("DUMP", ambiguousMeasure.catalogEntryId);
    }

    @Test public void duplicateStrictSemanticIdentityNeverMergesAutomatically() {
        FakeKnowledge k = standardKnowledge();
        k.add(standard("P5-DUP", "농심 신라면 5입 duplicate", "농심", "신라면", null, pack(5)));
        IdentityDecisionV2 d = resolver.resolve(
                "[농심] 신라면 5입", "STORE-A", parser.parse("[농심] 신라면 5입"), k);
        assertEquals(IdentityDecisionV2.Status.REVIEW, d.status);
        assertEquals(IdentityDecisionV2.Authority.SEMANTIC_AMBIGUOUS, d.authority);
        assertTrue(d.includesCandidate("P5"));
        assertTrue(d.includesCandidate("P5-DUP"));
    }

    @Test public void confirmationDefaultsToMerchantAndRepeatThenAutoLinks() {
        FakeKnowledge k = standardKnowledge();
        ReceiptProductSemantics s = parser.parse("특가코드77");
        IdentityDecisionV2 first = resolver.resolve("특가코드77", "STORE-Z", s, k);
        assertEquals(IdentityDecisionV2.Status.UNRESOLVED, first.status);

        AliasContext learned = IdentityConfirmationV2.rememberConfirmedAlias(
                k, "STORE-Z", "특가코드77", "P5", false);
        assertEquals(AliasContext.Scope.MERCHANT, learned.scope);

        IdentityDecisionV2 repeat = resolver.resolve("특가코드77", "STORE-Z", s, k);
        assertEquals(IdentityDecisionV2.Status.AUTO_LINK, repeat.status);
        assertEquals("P5", repeat.catalogEntryId);

        IdentityDecisionV2 otherStore = resolver.resolve("특가코드77", "STORE-Y", s, k);
        assertEquals(IdentityDecisionV2.Status.UNRESOLVED, otherStore.status);
    }

    @Test public void candidateRankingIsDeterministicAcrossEnumerationOrder() {
        FakeKnowledge forward = standardKnowledge();
        FakeKnowledge reverse = standardKnowledge();
        Collections.reverse(reverse.order);
        ReceiptProductSemantics s = parser.parse("신라면 5입");
        IdentityDecisionV2 a = resolver.resolve("신라면 5입", null, s, forward);
        IdentityDecisionV2 b = resolver.resolve("신라면 5입", null, s, reverse);
        assertEquals(a.status, b.status);
        assertEquals(a.authority, b.authority);
        assertEquals(a.catalogEntryId, b.catalogEntryId);
        assertEquals(a.rankedCandidateIds, b.rankedCandidateIds);
    }

    @Test public void metricsGoldenSet() {
        FakeKnowledge common = standardKnowledge();
        common.alias(AliasContext.merchant("A"), "A-R5", "P5");
        common.alias(AliasContext.merchant("A"), "A-R10", "P10");
        common.alias(AliasContext.global(), "G-R5", "P5");
        common.alias(AliasContext.global(), "G-R10", "P10");
        common.alias(AliasContext.global(), "OVERRIDE", "P5");
        common.alias(AliasContext.merchant("A"), "OVERRIDE", "P10");
        common.alias(AliasContext.merchant("A"), "REPEAT-1", "P5");
        common.alias(AliasContext.merchant("B"), "REPEAT-2", "P10");
        common.alias(AliasContext.global(), "REPEAT-3", "COLA");
        common.alias(AliasContext.merchant("A"), "감자코드", "POTATO");

        List<MetricCase> cases = new ArrayList<>();
        cases.add(c("A-R5", "A", "P5", true, false, common));
        cases.add(c("A-R10", "A", "P10", true, false, common));
        cases.add(c("G-R5", "B", "P5", true, false, common));
        cases.add(c("G-R10", null, "P10", true, false, common));
        cases.add(c("OVERRIDE", "A", "P10", true, false, common));
        cases.add(c("[농심] 신라면 5입", "A", "P5", true, false, common));
        cases.add(c("[농심] 신라면 10입", "A", "P10", true, false, common));
        cases.add(c("[코카콜라] 제로 6X200ML", "A", "COLA", true, false, common));
        cases.add(c("[오뚜기] 진라면 5입", "A", "JIN", true, false, common));
        cases.add(c("[해태] 홈런볼 4입", "A", "BALL", true, false, common));
        cases.add(c("신라면 5입", "A", "P5", true, false, common));
        cases.add(c("[비비고] 왕교자 1.05KG", "A", "DUMP", true, false, common));
        cases.add(c("[농심] 신라면", "A", "P5", true, false, common));
        cases.add(c("농심행사품", "A", "P5", true, false, common));
        cases.add(c("처음보는상품", "A", null, false, false, common));
        cases.add(c("REPEAT-1", "A", "P5", true, true, common));
        cases.add(c("REPEAT-2", "B", "P10", true, true, common));
        cases.add(c("REPEAT-3", "C", "COLA", true, true, common));
        cases.add(c("감자코드", "A", "POTATO", false, true, common));

        FakeKnowledge conflict = standardKnowledge();
        conflict.alias(AliasContext.merchant("A"), "[농심] 신라면 10입", "P5");
        cases.add(c("[농심] 신라면 10입", "A", "P5", true, false, conflict));
        FakeKnowledge conflictBrand = standardKnowledge();
        conflictBrand.alias(AliasContext.merchant("A"), "[오뚜기] 신라면 5입", "P5");
        cases.add(c("[오뚜기] 신라면 5입", "A", "P5", true, false, conflictBrand));

        FakeKnowledge duplicate = standardKnowledge();
        duplicate.add(standard("P5-DUP", "duplicate", "농심", "신라면", null, pack(5)));
        cases.add(c("[농심] 신라면 5입", "A", "P5", true, false, duplicate));

        cases.add(c("감자 1봉", "A", null, false, false, common));
        cases.add(c("양파", "A", null, false, false, common));

        int known = 0, auto = 0, correctAuto = 0, incorrectAuto = 0;
        int falseMerge = 0, falseSplit = 0, review = 0, unresolved = 0;
        int repeat = 0, repeatReused = 0;
        for (MetricCase mc : cases) {
            IdentityDecisionV2 d = resolver.resolve(mc.raw, mc.merchant, parser.parse(mc.raw), mc.knowledge);
            if (mc.metricKnown) known++;
            if (d.status == IdentityDecisionV2.Status.AUTO_LINK) {
                auto++;
                if (mc.expectedId != null && mc.expectedId.equals(d.catalogEntryId)) correctAuto++;
                else { incorrectAuto++; falseMerge++; }
            } else if (d.status == IdentityDecisionV2.Status.REVIEW) {
                review++;
            } else {
                unresolved++;
            }
            if (mc.metricKnown && mc.expectedId != null && !mc.expectedId.equals(d.catalogEntryId)
                    && !d.includesCandidate(mc.expectedId)) falseSplit++;
            if (mc.repeat) {
                repeat++;
                if (d.status == IdentityDecisionV2.Status.AUTO_LINK && mc.expectedId.equals(d.catalogEntryId)) repeatReused++;
            }
        }

        assertEquals(0, falseMerge);
        assertEquals(0, incorrectAuto);
        assertEquals(repeat, repeatReused);
        assertTrue(falseSplit * 20 <= known); // <= 5%
        assertTrue(auto > 0);
        assertTrue(review > 0);
        assertTrue(unresolved > 0);
        System.out.println("CP24_METRICS fixtures=" + cases.size()
                + " known_identity=" + known
                + " auto_links=" + auto
                + " correct_auto_links=" + correctAuto
                + " incorrect_auto_links=" + incorrectAuto
                + " false_merge=" + falseMerge
                + " false_split=" + falseSplit
                + " review_required=" + review
                + " unresolved=" + unresolved
                + " repeat_cases=" + repeat
                + " repeat_reused=" + repeatReused);
    }

    private static MetricCase c(String raw, String merchant, String expectedId, boolean metricKnown,
            boolean repeat, FakeKnowledge knowledge) {
        return new MetricCase(raw, merchant, expectedId, metricKnown, repeat, knowledge);
    }

    private static FakeKnowledge standardKnowledge() {
        FakeKnowledge k = new FakeKnowledge();
        k.add(standard("P5", "농심 신라면 5입", "농심", "신라면", null, pack(5)));
        k.add(standard("P10", "농심 신라면 10입", "농심", "신라면", null, pack(10)));
        k.add(standard("COLA", "코카콜라 제로 200mLx6", "코카콜라", "제로", null,
                multi("1200", SalesUnitCode.MILLILITER, 6, "200")));
        k.add(standard("JIN", "오뚜기 진라면 5입", "오뚜기", "진라면", null, pack(5)));
        k.add(standard("BALL", "해태 홈런볼 4입", "해태", "홈런볼", null, pack(4)));
        k.add(standard("DUMP", "비비고 왕교자 1.05kg", "비비고", "왕교자", null,
                measure("1.05", SalesUnitCode.KILOGRAM)));
        k.add(CatalogEntryV2.commodity("POTATO", "감자", null, 1L));
        return k;
    }

    private static CatalogEntryV2 standard(String id, String canonical, String brand, String product,
            String variant, ProductSpecification specification) {
        return CatalogEntryV2.standard(id, canonical,
                brand == null ? CatalogField.<String>absent() : CatalogField.userConfirmed(brand),
                CatalogField.userConfirmed(product),
                variant == null ? CatalogField.<String>absent() : CatalogField.userConfirmed(variant),
                specification == null ? CatalogField.<ProductSpecification>absent() : CatalogField.userConfirmed(specification),
                null, 1L);
    }

    private static ProductSpecification pack(int count) {
        return new ProductSpecification(null, count, null);
    }

    private static ProductSpecification measure(String amount, SalesUnitCode unit) {
        return new ProductSpecification(new PackageMeasure(amount, unit), null, null);
    }

    private static ProductSpecification multi(String total, SalesUnitCode unit, int count, String inner) {
        return new ProductSpecification(new PackageMeasure(total, unit), count, new PackageMeasure(inner, unit));
    }

    private static final class MetricCase {
        final String raw, merchant, expectedId;
        final boolean metricKnown, repeat;
        final FakeKnowledge knowledge;
        MetricCase(String raw, String merchant, String expectedId, boolean metricKnown, boolean repeat, FakeKnowledge knowledge) {
            this.raw = raw; this.merchant = merchant; this.expectedId = expectedId;
            this.metricKnown = metricKnown; this.repeat = repeat; this.knowledge = knowledge;
        }
    }

    private static final class FakeKnowledge implements IdentityKnowledgeV2, CatalogV2PersistenceStore {
        final Map<String, CatalogEntryV2> entries = new HashMap<>();
        final List<CatalogEntryV2> order = new ArrayList<>();
        final Map<String, String> aliases = new HashMap<>();
        final Map<String, CatalogField<PurchaseForm>> forms = new HashMap<>();

        void add(CatalogEntryV2 entry) { entries.put(entry.id, entry); order.add(entry); }
        void alias(AliasContext context, String raw, String id) { aliases.put(aliasKey(context, raw), id); }

        @Override public String exactAliasCatalogEntryId(AliasContext context, String rawAlias) {
            return aliases.get(aliasKey(context, rawAlias));
        }
        @Override public CatalogEntryV2 catalogEntry(String catalogEntryId) { return entries.get(catalogEntryId); }
        @Override public List<CatalogEntryV2> catalogEntries() { return new ArrayList<>(order); }
        @Override public CatalogEntryV2 catalogEntryV2(String catalogEntryId) { return entries.get(catalogEntryId); }
        @Override public void saveCatalogEntryV2(CatalogEntryV2 entry) {
            if (!entries.containsKey(entry.id)) order.add(entry);
            entries.put(entry.id, entry);
        }
        @Override public void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId) {
            if (!entries.containsKey(catalogEntryId)) throw new IllegalArgumentException("catalogEntryId");
            aliases.put(aliasKey(context, rawAlias), catalogEntryId);
        }
        @Override public String aliasCatalogEntryIdV2(AliasContext context, String rawAlias) {
            return aliases.get(aliasKey(context, rawAlias));
        }
        @Override public void savePurchaseFormV2(String receiptId, int itemOrdinal, CatalogField<PurchaseForm> purchaseForm) {
            forms.put(receiptId + "#" + itemOrdinal, purchaseForm);
        }
        @Override public CatalogField<PurchaseForm> purchaseFormV2(String receiptId, int itemOrdinal) {
            CatalogField<PurchaseForm> value = forms.get(receiptId + "#" + itemOrdinal);
            return value == null ? CatalogField.<PurchaseForm>absent() : value;
        }
        private static String aliasKey(AliasContext context, String raw) {
            return context.toString() + "|" + ProductNameNormalizer.key(raw);
        }
    }
}
