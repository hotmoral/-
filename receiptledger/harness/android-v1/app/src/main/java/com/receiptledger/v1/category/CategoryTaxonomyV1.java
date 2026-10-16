package com.receiptledger.v1.category;

import com.receiptledger.v1.catalog.CategoryRef;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Stable bounded taxonomy for V1 browsing. Custom category authoring is intentionally out of scope. */
public final class CategoryTaxonomyV1 {
    public static final String FOOD = "FOOD";
    public static final String FOOD_DAIRY = "FOOD_DAIRY";
    public static final String FOOD_DAIRY_MILK = "FOOD_DAIRY_MILK";
    public static final String FOOD_DAIRY_YOGURT = "FOOD_DAIRY_YOGURT";
    public static final String FOOD_DAIRY_CHEESE = "FOOD_DAIRY_CHEESE";
    public static final String FOOD_NOODLES = "FOOD_NOODLES";
    public static final String FOOD_NOODLES_RAMEN = "FOOD_NOODLES_RAMEN";
    public static final String FOOD_FROZEN = "FOOD_FROZEN";
    public static final String FOOD_FROZEN_DUMPLING = "FOOD_FROZEN_DUMPLING";
    public static final String FOOD_PRODUCE = "FOOD_PRODUCE";
    public static final String FOOD_PRODUCE_VEGETABLE = "FOOD_PRODUCE_VEGETABLE";
    public static final String FOOD_PRODUCE_FRUIT = "FOOD_PRODUCE_FRUIT";
    public static final String FOOD_GRAIN = "FOOD_GRAIN";
    public static final String FOOD_SNACK = "FOOD_SNACK";
    public static final String FOOD_BEVERAGE = "FOOD_BEVERAGE";
    public static final String FOOD_BEVERAGE_WATER = "FOOD_BEVERAGE_WATER";
    public static final String FOOD_BEVERAGE_COFFEE = "FOOD_BEVERAGE_COFFEE";
    public static final String FOOD_SAUCE_SEASONING = "FOOD_SAUCE_SEASONING";
    public static final String HOUSEHOLD = "HOUSEHOLD";
    public static final String HOUSEHOLD_CLEANING = "HOUSEHOLD_CLEANING";
    public static final String HOUSEHOLD_CLEANING_LAUNDRY = "HOUSEHOLD_CLEANING_LAUNDRY";
    public static final String HOUSEHOLD_CLEANING_DISH = "HOUSEHOLD_CLEANING_DISH";
    public static final String HOUSEHOLD_PAPER = "HOUSEHOLD_PAPER";
    public static final String HOUSEHOLD_PAPER_TOILET = "HOUSEHOLD_PAPER_TOILET";
    public static final String HOUSEHOLD_PAPER_WIPES = "HOUSEHOLD_PAPER_WIPES";
    public static final String HOUSEHOLD_PERSONAL_CARE = "HOUSEHOLD_PERSONAL_CARE";
    public static final String HOUSEHOLD_PERSONAL_CARE_ORAL = "HOUSEHOLD_PERSONAL_CARE_ORAL";
    public static final String HOUSEHOLD_PERSONAL_CARE_HAIR = "HOUSEHOLD_PERSONAL_CARE_HAIR";

    private static final Map<String, CategoryNodeV1> NODES;
    static {
        LinkedHashMap<String, CategoryNodeV1> m = new LinkedHashMap<>();
        add(m, FOOD, null, "식품");
        add(m, FOOD_DAIRY, FOOD, "유제품");
        add(m, FOOD_DAIRY_MILK, FOOD_DAIRY, "우유");
        add(m, FOOD_DAIRY_YOGURT, FOOD_DAIRY, "요구르트·요거트");
        add(m, FOOD_DAIRY_CHEESE, FOOD_DAIRY, "치즈");
        add(m, FOOD_NOODLES, FOOD, "면류");
        add(m, FOOD_NOODLES_RAMEN, FOOD_NOODLES, "라면");
        add(m, FOOD_FROZEN, FOOD, "냉동식품");
        add(m, FOOD_FROZEN_DUMPLING, FOOD_FROZEN, "만두·교자");
        add(m, FOOD_PRODUCE, FOOD, "농산물");
        add(m, FOOD_PRODUCE_VEGETABLE, FOOD_PRODUCE, "채소");
        add(m, FOOD_PRODUCE_FRUIT, FOOD_PRODUCE, "과일");
        add(m, FOOD_GRAIN, FOOD, "쌀·곡물");
        add(m, FOOD_SNACK, FOOD, "과자·스낵");
        add(m, FOOD_BEVERAGE, FOOD, "음료");
        add(m, FOOD_BEVERAGE_WATER, FOOD_BEVERAGE, "생수");
        add(m, FOOD_BEVERAGE_COFFEE, FOOD_BEVERAGE, "커피");
        add(m, FOOD_SAUCE_SEASONING, FOOD, "장류·소스·조미료");
        add(m, HOUSEHOLD, null, "생활");
        add(m, HOUSEHOLD_CLEANING, HOUSEHOLD, "세정·세탁");
        add(m, HOUSEHOLD_CLEANING_LAUNDRY, HOUSEHOLD_CLEANING, "세탁세제·유연제");
        add(m, HOUSEHOLD_CLEANING_DISH, HOUSEHOLD_CLEANING, "주방세제");
        add(m, HOUSEHOLD_PAPER, HOUSEHOLD, "종이·티슈");
        add(m, HOUSEHOLD_PAPER_TOILET, HOUSEHOLD_PAPER, "화장지");
        add(m, HOUSEHOLD_PAPER_WIPES, HOUSEHOLD_PAPER, "물티슈");
        add(m, HOUSEHOLD_PERSONAL_CARE, HOUSEHOLD, "개인위생");
        add(m, HOUSEHOLD_PERSONAL_CARE_ORAL, HOUSEHOLD_PERSONAL_CARE, "구강용품");
        add(m, HOUSEHOLD_PERSONAL_CARE_HAIR, HOUSEHOLD_PERSONAL_CARE, "헤어용품");
        for (CategoryNodeV1 node : m.values()) {
            if (node.parentId != null && !m.containsKey(node.parentId)) {
                throw new IllegalStateException("missing category parent: " + node.id);
            }
        }
        NODES = Collections.unmodifiableMap(m);
    }

    private CategoryTaxonomyV1() {}

    public static CategoryNodeV1 require(String id) {
        CategoryNodeV1 node = NODES.get(id);
        if (node == null) throw new IllegalArgumentException("unknown category: " + id);
        return node;
    }

    public static CategoryRef ref(String id) {
        require(id);
        return new CategoryRef(id);
    }

    public static List<CategoryNodeV1> all() {
        return Collections.unmodifiableList(new ArrayList<>(NODES.values()));
    }

    public static List<CategoryNodeV1> roots() {
        List<CategoryNodeV1> out = new ArrayList<>();
        for (CategoryNodeV1 node : NODES.values()) if (node.isRoot()) out.add(node);
        return Collections.unmodifiableList(out);
    }

    public static List<CategoryNodeV1> children(String parentId) {
        require(parentId);
        List<CategoryNodeV1> out = new ArrayList<>();
        for (CategoryNodeV1 node : NODES.values()) if (parentId.equals(node.parentId)) out.add(node);
        return Collections.unmodifiableList(out);
    }

    private static void add(Map<String, CategoryNodeV1> map, String id, String parentId, String displayNameKo) {
        CategoryNodeV1 node = new CategoryNodeV1(id, parentId, displayNameKo);
        if (map.put(id, node) != null) throw new IllegalStateException("duplicate category id: " + id);
    }
}
