package com.receiptledger.v1.category;

import static org.junit.Assert.*;

import com.receiptledger.v1.catalog.AliasContext;
import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.catalog.CategoryRef;
import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.product.CatalogV2PersistenceStore;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.junit.Test;

public final class CategorySystemV1Test {
    @Test public void taxonomyIsBoundedStableAndAcyclic() {
        assertEquals(28, CategoryTaxonomyV1.all().size());
        assertEquals(2, CategoryTaxonomyV1.roots().size());
        Set<String> ids = new HashSet<>();
        for (CategoryNodeV1 node : CategoryTaxonomyV1.all()) {
            assertTrue(ids.add(node.id));
            Set<String> path = new HashSet<>();
            CategoryNodeV1 current = node;
            while (current != null) {
                assertTrue("cycle at " + node.id, path.add(current.id));
                current = current.parentId == null ? null : CategoryTaxonomyV1.require(current.parentId);
            }
        }
        assertEquals("식품", CategoryTaxonomyV1.require(CategoryTaxonomyV1.FOOD).displayNameKo);
        assertEquals("생활", CategoryTaxonomyV1.require(CategoryTaxonomyV1.HOUSEHOLD).displayNameKo);
    }

    @Test public void strongRulesAreAutoAssignableWhileGenericAndConflictingEvidenceReview() {
        CategoryClassifierV1 classifier = new CategoryClassifierV1();
        assertDecision(classifier, standard("a", "서울우유 1L"), CategoryDecisionV1.State.AUTO_ASSIGNABLE, CategoryTaxonomyV1.FOOD_DAIRY_MILK);
        assertDecision(classifier, standard("b", "비비고 왕교자"), CategoryDecisionV1.State.AUTO_ASSIGNABLE, CategoryTaxonomyV1.FOOD_FROZEN_DUMPLING);
        assertDecision(classifier, commodity("c", "감자"), CategoryDecisionV1.State.AUTO_ASSIGNABLE, CategoryTaxonomyV1.FOOD_PRODUCE_VEGETABLE);
        assertDecision(classifier, standard("d", "생활 세제"), CategoryDecisionV1.State.REVIEW, CategoryTaxonomyV1.HOUSEHOLD_CLEANING);
        assertDecision(classifier, standard("e", "우유 치즈"), CategoryDecisionV1.State.REVIEW, CategoryTaxonomyV1.FOOD_DAIRY_CHEESE);
        assertEquals(CategoryDecisionV1.State.UNRESOLVED, classifier.classify(standard("f", "기획상품 A")).state);
    }

    @Test public void persistedAssignmentIsReusedBeforeRules() {
        FakeStore store = new FakeStore();
        CatalogEntryV2 entry = standard("p1", "서울우유 1L");
        store.saveCatalogEntryV2(withCategory(entry, CategoryTaxonomyV1.FOOD_DAIRY_CHEESE));
        CategoryAssignmentServiceV1 service = new CategoryAssignmentServiceV1(store);
        CategoryDecisionV1 decision = service.decision("p1");
        assertEquals(CategoryDecisionV1.State.REUSE_PERSISTED, decision.state);
        assertEquals(CategoryTaxonomyV1.FOOD_DAIRY_CHEESE, decision.category.id);
    }

    @Test public void automaticSuggestionCanBePersistedAndThenReused() {
        FakeStore store = new FakeStore();
        store.saveCatalogEntryV2(standard("p2", "신라면 5입"));
        CategoryAssignmentServiceV1 service = new CategoryAssignmentServiceV1(store);
        assertEquals(CategoryDecisionV1.State.AUTO_ASSIGNABLE, service.decision("p2").state);
        assertEquals(CategoryTaxonomyV1.FOOD_NOODLES_RAMEN, service.acceptAutomaticSuggestion("p2").id);
        assertEquals(CategoryDecisionV1.State.REUSE_PERSISTED, service.decision("p2").state);
    }

    @Test public void userCorrectionReplacesOnlyCategoryAndIsReused() {
        FakeStore store = new FakeStore();
        CatalogEntryV2 before = standard("p3", "커피우유");
        store.saveCatalogEntryV2(before);
        CategoryAssignmentServiceV1 service = new CategoryAssignmentServiceV1(store);
        service.assign("p3", CategoryTaxonomyV1.ref(CategoryTaxonomyV1.FOOD_BEVERAGE_COFFEE));
        CatalogEntryV2 after = store.catalogEntryV2("p3");
        assertSameCore(before, after);
        assertEquals(CategoryTaxonomyV1.FOOD_BEVERAGE_COFFEE, after.category.id);
        assertEquals(CategoryDecisionV1.State.REUSE_PERSISTED, service.decision("p3").state);
    }

    @Test public void categoryAssignmentDoesNotTouchIdentityOrAliases() {
        FakeStore store = new FakeStore();
        CatalogEntryV2 before = standard("stable-product-id", "샴푸");
        store.saveCatalogEntryV2(before);
        store.saveAliasV2(AliasContext.global(), "샴푸POS", before.id);
        int aliasesBefore = store.aliases.size();
        new CategoryAssignmentServiceV1(store).assign(before.id,
                CategoryTaxonomyV1.ref(CategoryTaxonomyV1.HOUSEHOLD_PERSONAL_CARE_HAIR));
        CatalogEntryV2 after = store.catalogEntryV2(before.id);
        assertSameCore(before, after);
        assertEquals("stable-product-id", after.id);
        assertEquals(aliasesBefore, store.aliases.size());
        assertEquals(before.id, store.aliasCatalogEntryIdV2(AliasContext.global(), "샴푸POS"));
    }

    @Test public void unknownCategoryCannotBePersisted() {
        FakeStore store = new FakeStore();
        store.saveCatalogEntryV2(standard("p4", "치약"));
        try {
            new CategoryAssignmentServiceV1(store).assign("p4", new CategoryRef("MADE_UP_CATEGORY"));
            fail("expected unknown category rejection");
        } catch (IllegalArgumentException expected) {
            assertTrue(expected.getMessage().contains("unknown category"));
        }
    }

    @Test public void goldenMetricsExposeAutomationReviewAndConfirmedReuse() {
        CategoryClassifierV1 classifier = new CategoryClassifierV1();
        List<Fixture> fixtures = new ArrayList<>();
        auto(fixtures, "서울우유1L", CategoryTaxonomyV1.FOOD_DAIRY_MILK);
        auto(fixtures, "딸기우유", CategoryTaxonomyV1.FOOD_DAIRY_MILK);
        auto(fixtures, "요구르트", CategoryTaxonomyV1.FOOD_DAIRY_YOGURT);
        auto(fixtures, "그릭요거트", CategoryTaxonomyV1.FOOD_DAIRY_YOGURT);
        auto(fixtures, "체다치즈", CategoryTaxonomyV1.FOOD_DAIRY_CHEESE);
        auto(fixtures, "신라면5입", CategoryTaxonomyV1.FOOD_NOODLES_RAMEN);
        auto(fixtures, "진라면", CategoryTaxonomyV1.FOOD_NOODLES_RAMEN);
        auto(fixtures, "비비고왕교자", CategoryTaxonomyV1.FOOD_FROZEN_DUMPLING);
        auto(fixtures, "냉동만두", CategoryTaxonomyV1.FOOD_FROZEN_DUMPLING);
        autoCommodity(fixtures, "감자", CategoryTaxonomyV1.FOOD_PRODUCE_VEGETABLE);
        autoCommodity(fixtures, "양파", CategoryTaxonomyV1.FOOD_PRODUCE_VEGETABLE);
        autoCommodity(fixtures, "사과", CategoryTaxonomyV1.FOOD_PRODUCE_FRUIT);
        autoCommodity(fixtures, "바나나", CategoryTaxonomyV1.FOOD_PRODUCE_FRUIT);
        autoCommodity(fixtures, "쌀", CategoryTaxonomyV1.FOOD_GRAIN);
        auto(fixtures, "초코과자", CategoryTaxonomyV1.FOOD_SNACK);
        auto(fixtures, "제주삼다수생수", CategoryTaxonomyV1.FOOD_BEVERAGE_WATER);
        auto(fixtures, "원두커피", CategoryTaxonomyV1.FOOD_BEVERAGE_COFFEE);
        auto(fixtures, "고추장", CategoryTaxonomyV1.FOOD_SAUCE_SEASONING);
        auto(fixtures, "세탁세제", CategoryTaxonomyV1.HOUSEHOLD_CLEANING_LAUNDRY);
        auto(fixtures, "주방세제", CategoryTaxonomyV1.HOUSEHOLD_CLEANING_DISH);
        auto(fixtures, "3겹화장지", CategoryTaxonomyV1.HOUSEHOLD_PAPER_TOILET);
        auto(fixtures, "물티슈100매", CategoryTaxonomyV1.HOUSEHOLD_PAPER_WIPES);
        auto(fixtures, "치약", CategoryTaxonomyV1.HOUSEHOLD_PERSONAL_CARE_ORAL);
        auto(fixtures, "샴푸", CategoryTaxonomyV1.HOUSEHOLD_PERSONAL_CARE_HAIR);
        review(fixtures, "생활세제", CategoryTaxonomyV1.HOUSEHOLD_CLEANING);
        review(fixtures, "탄산음료", CategoryTaxonomyV1.FOOD_BEVERAGE);
        review(fixtures, "냉동식품", CategoryTaxonomyV1.FOOD_FROZEN);
        review(fixtures, "농산물꾸러미", CategoryTaxonomyV1.FOOD_PRODUCE);
        unresolved(fixtures, "멀티상품A");
        unresolved(fixtures, "기획상품B");

        int known = 0, autoSuggestions = 0, correctAuto = 0, incorrectAuto = 0, reviewRequired = 0, unresolved = 0;
        int ordinal = 0;
        for (Fixture f : fixtures) {
            CatalogEntryV2 entry = f.commodity ? commodity("fx" + ordinal, f.text) : standard("fx" + ordinal, f.text);
            CategoryDecisionV1 d = classifier.classify(entry);
            if (f.expectedCategory != null) known++;
            if (d.state == CategoryDecisionV1.State.AUTO_ASSIGNABLE) {
                autoSuggestions++;
                if (f.expectedCategory != null && f.expectedCategory.equals(d.category.id)) correctAuto++; else incorrectAuto++;
            }
            if (d.requiresReview()) reviewRequired++;
            if (d.state == CategoryDecisionV1.State.UNRESOLVED) unresolved++;
            assertEquals("state for " + f.text, f.expectedState, d.state);
            if (f.expectedCategory != null) assertEquals("category for " + f.text, f.expectedCategory, d.category.id);
            ordinal++;
        }

        FakeStore store = new FakeStore();
        String[] repeatNames = {"서울우유1L", "신라면5입", "치약", "물티슈100매"};
        int repeatCases = repeatNames.length, repeatReused = 0;
        for (int i = 0; i < repeatNames.length; i++) {
            String id = "repeat" + i;
            store.saveCatalogEntryV2(standard(id, repeatNames[i]));
            CategoryAssignmentServiceV1 service = new CategoryAssignmentServiceV1(store);
            assertTrue(service.decision(id).canAutoAssign());
            service.acceptAutomaticSuggestion(id);
            if (service.decision(id).state == CategoryDecisionV1.State.REUSE_PERSISTED) repeatReused++;
        }

        String[] correctionIds = {"corr1", "corr2", "corr3"};
        int correctionCases = correctionIds.length, correctionReused = 0;
        for (String id : correctionIds) {
            store.saveCatalogEntryV2(standard(id, "기획상품" + id));
            CategoryAssignmentServiceV1 service = new CategoryAssignmentServiceV1(store);
            service.assign(id, CategoryTaxonomyV1.ref(CategoryTaxonomyV1.FOOD_SNACK));
            if (service.decision(id).state == CategoryDecisionV1.State.REUSE_PERSISTED
                    && CategoryTaxonomyV1.FOOD_SNACK.equals(service.decision(id).category.id)) correctionReused++;
        }

        System.out.println("CP25_METRICS fixtures=" + fixtures.size()
                + " known_category=" + known
                + " auto_suggestions=" + autoSuggestions
                + " correct_auto_suggestions=" + correctAuto
                + " incorrect_auto_suggestions=" + incorrectAuto
                + " review_required=" + reviewRequired
                + " unresolved=" + unresolved
                + " repeat_cases=" + repeatCases
                + " repeat_reused=" + repeatReused
                + " correction_cases=" + correctionCases
                + " correction_reused=" + correctionReused);

        assertEquals(30, fixtures.size());
        assertEquals(28, known);
        assertEquals(24, autoSuggestions);
        assertEquals(24, correctAuto);
        assertEquals(0, incorrectAuto);
        assertEquals(6, reviewRequired);
        assertEquals(2, unresolved);
        assertEquals(repeatCases, repeatReused);
        assertEquals(correctionCases, correctionReused);
    }

    private static void assertDecision(CategoryClassifierV1 classifier, CatalogEntryV2 entry,
            CategoryDecisionV1.State state, String categoryId) {
        CategoryDecisionV1 d = classifier.classify(entry);
        assertEquals(state, d.state);
        assertNotNull(d.category);
        assertEquals(categoryId, d.category.id);
    }

    private static CatalogEntryV2 standard(String id, String name) {
        return CatalogEntryV2.standard(id, name, CatalogField.<String>absent(), CatalogField.userConfirmed(name),
                CatalogField.<String>absent(), CatalogField.absent(), null, 1L);
    }

    private static CatalogEntryV2 commodity(String id, String name) {
        return CatalogEntryV2.commodity(id, name, null, 1L);
    }

    private static CatalogEntryV2 withCategory(CatalogEntryV2 old, String categoryId) {
        return CatalogEntryV2.rehydrate(old.id, old.kind, old.canonicalName, old.brand, old.productName, old.variant,
                old.specification, CategoryTaxonomyV1.ref(categoryId), old.createdAtMillis, old.recordOrigin);
    }

    private static void assertSameCore(CatalogEntryV2 before, CatalogEntryV2 after) {
        assertEquals(before.id, after.id);
        assertEquals(before.kind, after.kind);
        assertEquals(before.canonicalName, after.canonicalName);
        assertEquals(before.brand, after.brand);
        assertEquals(before.productName, after.productName);
        assertEquals(before.variant, after.variant);
        assertEquals(before.specification, after.specification);
        assertEquals(before.createdAtMillis, after.createdAtMillis);
        assertEquals(before.recordOrigin, after.recordOrigin);
    }

    private static void auto(List<Fixture> out, String text, String category) {
        out.add(new Fixture(text, category, CategoryDecisionV1.State.AUTO_ASSIGNABLE, false));
    }
    private static void autoCommodity(List<Fixture> out, String text, String category) {
        out.add(new Fixture(text, category, CategoryDecisionV1.State.AUTO_ASSIGNABLE, true));
    }
    private static void review(List<Fixture> out, String text, String category) {
        out.add(new Fixture(text, category, CategoryDecisionV1.State.REVIEW, false));
    }
    private static void unresolved(List<Fixture> out, String text) {
        out.add(new Fixture(text, null, CategoryDecisionV1.State.UNRESOLVED, false));
    }

    private static final class Fixture {
        final String text, expectedCategory;
        final CategoryDecisionV1.State expectedState;
        final boolean commodity;
        Fixture(String text, String expectedCategory, CategoryDecisionV1.State expectedState, boolean commodity) {
            this.text = text; this.expectedCategory = expectedCategory; this.expectedState = expectedState; this.commodity = commodity;
        }
    }

    private static final class FakeStore implements CatalogV2PersistenceStore {
        final Map<String, CatalogEntryV2> entries = new HashMap<>();
        final Map<String, String> aliases = new HashMap<>();
        final Map<String, CatalogField<PurchaseForm>> forms = new HashMap<>();

        @Override public CatalogEntryV2 catalogEntryV2(String id) { return entries.get(id); }
        @Override public void saveCatalogEntryV2(CatalogEntryV2 entry) { entries.put(entry.id, entry); }
        @Override public void saveAliasV2(AliasContext context, String rawAlias, String catalogEntryId) {
            aliases.put(context.toString() + "|" + rawAlias, catalogEntryId);
        }
        @Override public String aliasCatalogEntryIdV2(AliasContext context, String rawAlias) {
            return aliases.get(context.toString() + "|" + rawAlias);
        }
        @Override public void savePurchaseFormV2(String receiptId, int itemOrdinal, CatalogField<PurchaseForm> purchaseForm) {
            forms.put(receiptId + "#" + itemOrdinal, purchaseForm);
        }
        @Override public CatalogField<PurchaseForm> purchaseFormV2(String receiptId, int itemOrdinal) {
            CatalogField<PurchaseForm> value = forms.get(receiptId + "#" + itemOrdinal);
            return value == null ? CatalogField.<PurchaseForm>absent() : value;
        }
    }
}
