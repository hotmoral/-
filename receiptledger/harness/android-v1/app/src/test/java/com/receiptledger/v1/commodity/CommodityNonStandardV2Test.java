package com.receiptledger.v1.commodity;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.CatalogKind;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.catalog.SalesUnitCode;
import com.receiptledger.v1.identity.IdentityKnowledgeV2;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import com.receiptledger.v1.product.ProductNameNormalizer;
import com.receiptledger.v1.semantics.ReceiptProductSemanticParser;
import com.receiptledger.v1.semantics.ReceiptProductSemantics;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.junit.Test;

public final class CommodityNonStandardV2Test {
    private static final ReceiptProductSemanticParser PARSER =
            new ReceiptProductSemanticParser(Arrays.asList("서울우유", "농심", "비비고"));
    private static final CommodityResolverV2 RESOLVER = new CommodityResolverV2();

    @Test public void exactCommodityNameGroupsAcrossHeterogeneousForms() {
        FakeStore store = seeded();
        for (String raw : Arrays.asList("감자 1봉", "감자 1KG", "감자 5개", "감자 1상자")) {
            CommodityGroupingDecisionV2 d = resolve(store, raw, "STORE_A");
            assertEquals(raw, CommodityGroupingDecisionV2.State.AUTO_GROUP, d.state);
            assertEquals("c_potato", d.catalogEntryId);
            assertEquals(CommodityGroupingDecisionV2.Authority.EXACT_COMMODITY_NAME, d.authority);
        }
    }

    @Test public void modifierBearingNamesAreSuggestionsNotAutomaticGrouping() {
        FakeStore store = seeded();
        CommodityGroupingDecisionV2 d = resolve(store, "국산 감자 1봉", "STORE_A");
        assertEquals(CommodityGroupingDecisionV2.State.REVIEW, d.state);
        assertEquals("c_potato", d.catalogEntryId);
        assertEquals(CommodityGroupingDecisionV2.Authority.COMMODITY_SUGGESTION, d.authority);
    }

    @Test public void lexicalSubstringDoesNotCreateUnsafeCommodityCandidate() {
        FakeStore store = seeded();
        assertEquals(CommodityGroupingDecisionV2.State.UNRESOLVED,
                resolve(store, "감자칩 1봉", "STORE_A").state);
        assertEquals(CommodityGroupingDecisionV2.State.UNRESOLVED,
                resolve(store, "감자전분 1KG", "STORE_A").state);
    }

    @Test public void standardProductCuesBlockSemanticCommodityAutoGroup() {
        FakeStore store = seeded();
        CommodityGroupingDecisionV2 d = resolve(store, "감자 100G 5입", "STORE_A");
        assertEquals(CommodityGroupingDecisionV2.State.REVIEW, d.state);
        assertEquals("c_potato", d.catalogEntryId);
    }

    @Test public void confirmedAliasReuseIsMerchantScopedAndCrossKindSafe() {
        FakeStore store = seeded();
        AliasContext learned = CommodityConfirmationV2.rememberConfirmedGrouping(
                store, "STORE_A", "국산 감자 1봉", "c_potato", false);
        assertEquals(AliasContext.Scope.MERCHANT, learned.scope);
        CommodityGroupingDecisionV2 sameStore = resolve(store, "국산 감자 1봉", "STORE_A");
        assertEquals(CommodityGroupingDecisionV2.State.AUTO_GROUP, sameStore.state);
        assertEquals(CommodityGroupingDecisionV2.Authority.MERCHANT_EXACT_ALIAS, sameStore.authority);
        assertEquals(CommodityGroupingDecisionV2.State.REVIEW,
                resolve(store, "국산 감자 1봉", "STORE_B").state);

        store.saveAliasV2(AliasContext.global(), "감자칩 1봉", "s_chips");
        CommodityGroupingDecisionV2 crossKind = resolve(store, "감자칩 1봉", "STORE_A");
        assertEquals(CommodityGroupingDecisionV2.State.REVIEW, crossKind.state);
        assertEquals(CommodityGroupingDecisionV2.Authority.CROSS_KIND_CONFLICT, crossKind.authority);
    }

    @Test public void purchaseFormPersistencePreservesRawEvidenceAndConfirmationState() {
        FakeStore store = seeded();
        int ordinal = 0;
        for (String raw : Arrays.asList(
                "감자 1봉", "감자 1KG", "감자 5개", "감자 1상자",
                "대파 1단", "사과 2팩", "양파 2KG", "당근 500G")) {
            ReceiptProductSemantics semantics = PARSER.parse(raw);
            assertNotNull(raw, semantics.purchaseForm);
            CommodityConfirmationV2.persistObservedPurchaseForm(store, "R1", ordinal, semantics.purchaseForm);
            CatalogField<PurchaseForm> saved = store.purchaseFormV2("R1", ordinal);
            assertTrue(saved.isPresent());
            assertEquals(semantics.purchaseForm.value.quantity, saved.value.quantity);
            assertEquals(semantics.purchaseForm.value.unit, saved.value.unit);
            assertEquals(semantics.purchaseForm.value.rawUnitLabel, saved.value.rawUnitLabel);
            assertEquals(CatalogField.Source.PARSED_FROM_RECEIPT, saved.source);
            assertEquals(CatalogField.Confirmation.UNCONFIRMED, saved.confirmation);
            ordinal++;
        }
    }

    @Test public void formRelationSeparatesExactQuantityBasisFromSameFormAndIncomparable() {
        CommodityFormRelationV2 weight = CommodityFormRelationV2.classify(
                pf("1", SalesUnitCode.KILOGRAM, "kg"), pf("500", SalesUnitCode.GRAM, "g"));
        assertEquals(CommodityFormRelationV2.Relation.EXACT_NORMALIZABLE_QUANTITY, weight.relation);
        assertEquals(new BigDecimal("1000"), weight.leftBaseQuantity);
        assertEquals(new BigDecimal("500"), weight.rightBaseQuantity);

        CommodityFormRelationV2 volume = CommodityFormRelationV2.classify(
                pf("1", SalesUnitCode.LITER, "L"), pf("750", SalesUnitCode.MILLILITER, "ml"));
        assertEquals(CommodityFormRelationV2.Relation.EXACT_NORMALIZABLE_QUANTITY, volume.relation);

        assertEquals(CommodityFormRelationV2.Relation.SAME_FORM_ONLY,
                CommodityFormRelationV2.classify(pf("1", SalesUnitCode.BAG, "봉"), pf("2", SalesUnitCode.BAG, "봉")).relation);
        assertEquals(CommodityFormRelationV2.Relation.INCOMPARABLE,
                CommodityFormRelationV2.classify(pf("1", SalesUnitCode.BAG, "봉"), pf("1", SalesUnitCode.BOX, "상자")).relation);
        assertEquals(CommodityFormRelationV2.Relation.INCOMPARABLE,
                CommodityFormRelationV2.classify(pf("5", SalesUnitCode.EACH, "개"), pf("1", SalesUnitCode.KILOGRAM, "kg")).relation);
        assertEquals(CommodityFormRelationV2.Relation.SAME_FORM_ONLY,
                CommodityFormRelationV2.classify(pf("1", SalesUnitCode.OTHER, "망"), pf("2", SalesUnitCode.OTHER, "망")).relation);
    }

    @Test public void localGoldenMetricsKeepFalseGroupingZeroAndExposeFragmentationRisk() {
        FakeStore store = seeded();
        List<Fixture> fixtures = Arrays.asList(
                k("감자 1봉", "c_potato"), k("감자 1KG", "c_potato"), k("감자 5개", "c_potato"), k("감자 1상자", "c_potato"),
                k("대파 1단", "c_green"), k("대파 2단", "c_green"), k("대파 1봉", "c_green"),
                k("사과 5개", "c_apple"), k("사과 1봉", "c_apple"), k("사과 1상자", "c_apple"),
                k("양파 1봉", "c_onion"), k("양파 2KG", "c_onion"), k("양파 1상자", "c_onion"),
                k("당근 1봉", "c_carrot"), k("당근 1KG", "c_carrot"), k("당근 5개", "c_carrot"),
                k("토마토 1팩", "c_tomato"), k("토마토 500G", "c_tomato"),
                k("국산 감자 1봉", "c_potato"), k("햇 대파 1단", "c_green"),
                k("알감자 1봉", "c_potato"),
                n("감자칩 1봉"), n("감자전분 1KG"), n("서울우유 1L"), n("세탁세제 2L"));

        int known = 0, auto = 0, correctAuto = 0, incorrectAuto = 0, falseGroup = 0;
        int reviewSuggestions = 0, falseSplit = 0, negatives = 0;
        int rawCases = 0, rawPreserved = 0;
        int i = 0;
        for (Fixture f : fixtures) {
            ReceiptProductSemantics semantics = PARSER.parse(f.raw);
            CommodityGroupingDecisionV2 d = RESOLVER.resolve(f.raw, "METRIC_STORE", semantics, store);
            if (f.expectedId != null) {
                known++;
                if (d.state == CommodityGroupingDecisionV2.State.AUTO_GROUP) {
                    auto++;
                    if (f.expectedId.equals(d.catalogEntryId)) correctAuto++; else incorrectAuto++;
                } else if (d.state == CommodityGroupingDecisionV2.State.REVIEW && d.candidateIds.contains(f.expectedId)) {
                    reviewSuggestions++;
                } else {
                    falseSplit++;
                }
            } else {
                negatives++;
                if (d.state == CommodityGroupingDecisionV2.State.AUTO_GROUP) falseGroup++;
            }

            if (semantics.purchaseForm != null && rawCases < 12) {
                rawCases++;
                CommodityConfirmationV2.persistObservedPurchaseForm(store, "M", i, semantics.purchaseForm);
                CatalogField<PurchaseForm> saved = store.purchaseFormV2("M", i);
                if (saved.isPresent()
                        && saved.value.quantity.equals(semantics.purchaseForm.value.quantity)
                        && saved.value.unit == semantics.purchaseForm.value.unit
                        && saved.value.rawUnitLabel.equals(semantics.purchaseForm.value.rawUnitLabel)) {
                    rawPreserved++;
                }
            }
            i++;
        }

        String[][] repeats = new String[][]{
                {"국산 감자 1봉", "c_potato"}, {"햇 대파 1단", "c_green"}, {"홍로 사과 5개", "c_apple"}
        };
        int repeatReused = 0;
        for (String[] repeat : repeats) {
            CommodityConfirmationV2.rememberConfirmedGrouping(store, "REPEAT_STORE", repeat[0], repeat[1], false);
            CommodityGroupingDecisionV2 d = resolve(store, repeat[0], "REPEAT_STORE");
            if (d.state == CommodityGroupingDecisionV2.State.AUTO_GROUP && repeat[1].equals(d.catalogEntryId)) repeatReused++;
        }

        System.out.println("CP26_METRICS fixtures=" + fixtures.size()
                + " known_commodity=" + known
                + " auto_groups=" + auto
                + " correct_auto_groups=" + correctAuto
                + " incorrect_auto_groups=" + incorrectAuto
                + " false_group=" + falseGroup
                + " review_suggestions=" + reviewSuggestions
                + " false_split=" + falseSplit
                + " negative_fixtures=" + negatives
                + " raw_form_cases=" + rawCases
                + " raw_form_preserved=" + rawPreserved
                + " repeat_cases=" + repeats.length
                + " repeat_reused=" + repeatReused);

        assertEquals(0, incorrectAuto);
        assertEquals(0, falseGroup);
        assertEquals(18, correctAuto);
        assertEquals(2, reviewSuggestions);
        assertEquals(1, falseSplit);
        assertEquals(rawCases, rawPreserved);
        assertEquals(repeats.length, repeatReused);
    }

    private static CommodityGroupingDecisionV2 resolve(FakeStore store, String raw, String merchant) {
        return RESOLVER.resolve(raw, merchant, PARSER.parse(raw), store);
    }

    private static PurchaseForm pf(String q, SalesUnitCode unit, String raw) {
        return new PurchaseForm(q, unit, raw);
    }

    private static Fixture k(String raw, String id) { return new Fixture(raw, id); }
    private static Fixture n(String raw) { return new Fixture(raw, null); }

    private static final class Fixture {
        final String raw;
        final String expectedId;
        Fixture(String raw, String expectedId) { this.raw = raw; this.expectedId = expectedId; }
    }

    private static FakeStore seeded() {
        FakeStore s = new FakeStore();
        s.add(CatalogEntryV2.commodity("c_potato", "감자", null, 1L));
        s.add(CatalogEntryV2.commodity("c_green", "대파", null, 2L));
        s.add(CatalogEntryV2.commodity("c_apple", "사과", null, 3L));
        s.add(CatalogEntryV2.commodity("c_onion", "양파", null, 4L));
        s.add(CatalogEntryV2.commodity("c_carrot", "당근", null, 5L));
        s.add(CatalogEntryV2.commodity("c_tomato", "토마토", null, 6L));
        s.add(CatalogEntryV2.rehydrate("s_chips", CatalogKind.STANDARD_PRODUCT, "감자칩",
                CatalogField.absent(), CatalogField.absent(), CatalogField.absent(), CatalogField.absent(),
                null, 7L, CatalogEntryV2.RecordOrigin.LEGACY_V1));
        return s;
    }

    private static final class FakeStore implements IdentityKnowledgeV2, CatalogV2PersistenceStore {
        final Map<String, CatalogEntryV2> entries = new LinkedHashMap<>();
        final Map<String, String> aliases = new LinkedHashMap<>();
        final Map<String, CatalogField<PurchaseForm>> forms = new LinkedHashMap<>();

        void add(CatalogEntryV2 entry) { entries.put(entry.id, entry); }

        @Override public String exactAliasCatalogEntryId(AliasContext context, String rawAlias) {
            return aliasCatalogEntryIdV2(context, rawAlias);
        }
        @Override public CatalogEntryV2 catalogEntry(String catalogEntryId) { return entries.get(catalogEntryId); }
        @Override public List<CatalogEntryV2> catalogEntries() { return Collections.unmodifiableList(new ArrayList<>(entries.values())); }
        @Override public CatalogEntryV2 catalogEntryV2(String catalogEntryId) { return entries.get(catalogEntryId); }
        @Override public void saveCatalogEntryV2(CatalogEntryV2 entry) { entries.put(entry.id, entry); }
        @Override public void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId) {
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
