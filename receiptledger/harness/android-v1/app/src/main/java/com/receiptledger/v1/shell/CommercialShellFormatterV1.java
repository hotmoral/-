package com.receiptledger.v1.shell;

import com.receiptledger.v1.product.ProductType;
import com.receiptledger.v1.search.SearchBrowseEntryV1;

/** CP34 formatting only. It never derives identity, comparison basis or price judgment. */
public final class CommercialShellFormatterV1 {
    private CommercialShellFormatterV1() {}

    public static String resultRow(SearchBrowseEntryV1 entry) {
        if (entry == null) throw new IllegalArgumentException("entry");
        StringBuilder out = new StringBuilder();
        out.append(entry.canonicalName == null || entry.canonicalName.trim().isEmpty()
                ? "이름 없는 항목" : entry.canonicalName.trim());
        if (notBlank(entry.specificationSummary)) out.append(" · ").append(entry.specificationSummary.trim());
        out.append("\n").append(typeLabel(entry.type)).append(" · 구매 ").append(entry.purchaseCount).append("회");
        if (notBlank(entry.latestPurchaseDate)) out.append(" · 최근 ").append(entry.latestPurchaseDate.trim());
        if (notBlank(entry.latestStoreName)) out.append(" · ").append(entry.latestStoreName.trim());
        if (notBlank(entry.categoryPath)) out.append("\n").append(entry.categoryPath.trim());
        return out.toString();
    }

    static String typeLabel(ProductType type) {
        if (type == ProductType.STANDARD) return "제품";
        if (type == ProductType.NON_STANDARD) return "품목";
        return "미분류";
    }

    private static boolean notBlank(String value) {
        return value != null && !value.trim().isEmpty();
    }
}
