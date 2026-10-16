package com.receiptledger.v1.category;

import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.CatalogField;
import com.receiptledger.v1.product.ProductNameNormalizer;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Conservative local V1 category classifier. It produces browse metadata only. */
public final class CategoryClassifierV1 {
    public CategoryDecisionV1 classify(CatalogEntryV2 entry) {
        if (entry == null) throw new IllegalArgumentException("entry");
        if (entry.category != null) {
            CategoryTaxonomyV1.require(entry.category.id);
            return CategoryDecisionV1.reuse(entry.category);
        }

        String lexical = entry.productName.isPresent() ? entry.productName.value : entry.canonicalName;
        String lexicalCompact = compact(lexical);
        String combined = entry.canonicalName
                + (entry.productName.isPresent() ? " " + entry.productName.value : "")
                + (entry.variant.isPresent() ? " " + entry.variant.value : "");
        String text = compact(combined);

        Map<String, CategoryCandidateV1> hits = new LinkedHashMap<>();

        strongContains(hits, text, CategoryTaxonomyV1.FOOD_DAIRY_MILK, 120, "우유", "MILK");
        strongContains(hits, text, CategoryTaxonomyV1.FOOD_DAIRY_YOGURT, 120, "요구르트", "요거트", "YOGURT");
        strongContains(hits, text, CategoryTaxonomyV1.FOOD_DAIRY_CHEESE, 120, "치즈", "CHEESE");
        strongContains(hits, text, CategoryTaxonomyV1.FOOD_NOODLES_RAMEN, 120, "라면", "RAMEN");
        strongContains(hits, text, CategoryTaxonomyV1.FOOD_FROZEN_DUMPLING, 125, "만두", "교자");

        strongExact(hits, lexicalCompact, CategoryTaxonomyV1.FOOD_PRODUCE_VEGETABLE, 130,
                "감자", "고구마", "양파", "대파", "쪽파", "당근", "배추", "상추", "오이", "토마토", "마늘");
        strongExact(hits, lexicalCompact, CategoryTaxonomyV1.FOOD_PRODUCE_FRUIT, 130,
                "사과", "배", "바나나", "귤", "오렌지", "포도", "딸기", "복숭아", "수박");
        strongExact(hits, lexicalCompact, CategoryTaxonomyV1.FOOD_GRAIN, 130,
                "쌀", "현미", "보리", "잡곡", "찹쌀");

        strongContains(hits, text, CategoryTaxonomyV1.FOOD_BEVERAGE_WATER, 120, "생수", "MINERALWATER");
        strongContains(hits, text, CategoryTaxonomyV1.FOOD_BEVERAGE_COFFEE, 110, "커피", "COFFEE");
        strongContains(hits, text, CategoryTaxonomyV1.FOOD_SNACK, 105, "과자", "스낵", "초코파이");
        strongContains(hits, text, CategoryTaxonomyV1.FOOD_SAUCE_SEASONING, 115,
                "간장", "고추장", "된장", "케첩", "마요네즈", "소금", "후추");

        strongContains(hits, text, CategoryTaxonomyV1.HOUSEHOLD_CLEANING_LAUNDRY, 120,
                "세탁세제", "섬유유연제", "세탁비누");
        strongContains(hits, text, CategoryTaxonomyV1.HOUSEHOLD_CLEANING_DISH, 120,
                "주방세제", "퐁퐁", "식기세제");
        strongContains(hits, text, CategoryTaxonomyV1.HOUSEHOLD_PAPER_TOILET, 120,
                "화장지", "두루마리휴지", "롤휴지");
        strongContains(hits, text, CategoryTaxonomyV1.HOUSEHOLD_PAPER_WIPES, 120, "물티슈");
        strongContains(hits, text, CategoryTaxonomyV1.HOUSEHOLD_PERSONAL_CARE_ORAL, 120,
                "치약", "칫솔", "가글");
        strongContains(hits, text, CategoryTaxonomyV1.HOUSEHOLD_PERSONAL_CARE_HAIR, 120,
                "샴푸", "린스", "트리트먼트", "컨디셔너");

        mediumContains(hits, text, CategoryTaxonomyV1.FOOD_FROZEN, 70, "냉동");
        mediumContains(hits, text, CategoryTaxonomyV1.FOOD_BEVERAGE, 65, "음료");
        mediumContains(hits, text, CategoryTaxonomyV1.FOOD_PRODUCE, 65, "농산물");
        mediumContains(hits, text, CategoryTaxonomyV1.HOUSEHOLD_CLEANING, 65, "세제");

        List<CategoryCandidateV1> ranked = new ArrayList<>(hits.values());
        Collections.sort(ranked, new Comparator<CategoryCandidateV1>() {
            @Override public int compare(CategoryCandidateV1 a, CategoryCandidateV1 b) {
                int score = Integer.compare(b.score, a.score);
                return score != 0 ? score : a.category.id.compareTo(b.category.id);
            }
        });
        if (ranked.isEmpty()) return CategoryDecisionV1.unresolved();

        CategoryCandidateV1 top = ranked.get(0);
        CategoryCandidateV1 second = ranked.size() > 1 ? ranked.get(1) : null;
        if (top.confidence == CatalogField.Confidence.HIGH && (second == null || top.score > second.score)) {
            return CategoryDecisionV1.auto(top, ranked);
        }
        return CategoryDecisionV1.review(ranked,
                second != null && top.score == second.score ? "conflicting-category-evidence" : "medium-category-evidence");
    }

    private static void strongContains(Map<String, CategoryCandidateV1> hits, String text,
            String categoryId, int score, String... keywords) {
        if (containsAny(text, keywords)) offer(hits, categoryId, CatalogField.Confidence.HIGH, score, "strong-keyword");
    }

    private static void mediumContains(Map<String, CategoryCandidateV1> hits, String text,
            String categoryId, int score, String... keywords) {
        if (containsAny(text, keywords)) offer(hits, categoryId, CatalogField.Confidence.MEDIUM, score, "generic-keyword");
    }

    private static void strongExact(Map<String, CategoryCandidateV1> hits, String lexical,
            String categoryId, int score, String... terms) {
        for (String term : terms) {
            if (lexical.equals(compact(term))) {
                offer(hits, categoryId, CatalogField.Confidence.HIGH, score, "exact-commodity-name");
                return;
            }
        }
    }

    private static boolean containsAny(String text, String... keywords) {
        for (String keyword : keywords) if (text.contains(compact(keyword))) return true;
        return false;
    }

    private static void offer(Map<String, CategoryCandidateV1> hits, String categoryId,
            CatalogField.Confidence confidence, int score, String reason) {
        CategoryCandidateV1 existing = hits.get(categoryId);
        if (existing == null || score > existing.score) {
            hits.put(categoryId, new CategoryCandidateV1(CategoryTaxonomyV1.ref(categoryId), confidence, score, reason));
        }
    }

    private static String compact(String raw) {
        return ProductNameNormalizer.key(raw).replace(" ", "");
    }
}
