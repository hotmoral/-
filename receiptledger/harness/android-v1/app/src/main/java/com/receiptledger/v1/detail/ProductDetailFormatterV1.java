package com.receiptledger.v1.detail;

import com.receiptledger.v1.catalog.CatalogEntryV2;
import com.receiptledger.v1.catalog.PackageMeasure;
import com.receiptledger.v1.catalog.ProductSpecification;
import com.receiptledger.v1.catalog.SalesUnitCode;
import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.PriceObservationV2;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.text.NumberFormat;
import java.util.Locale;

/** Korean presentation helpers for CP31. Raw reason codes/enums never become the primary UI copy. */
public final class ProductDetailFormatterV1 {
    private ProductDetailFormatterV1() {}

    public static String primaryName(ProductDetailV1 detail) {
        CatalogEntryV2 entry = detail.catalogEntry;
        if (entry != null && entry.productName.isPresent()) return clean(entry.productName.value, detail.product.canonicalName);
        return detail.product.canonicalName;
    }

    public static String brand(ProductDetailV1 detail) {
        CatalogEntryV2 entry = detail.catalogEntry;
        return entry != null && entry.brand.isPresent() ? clean(entry.brand.value, "") : "";
    }

    public static String variant(ProductDetailV1 detail) {
        CatalogEntryV2 entry = detail.catalogEntry;
        return entry != null && entry.variant.isPresent() ? clean(entry.variant.value, "") : "";
    }

    public static String specification(ProductDetailV1 detail) {
        CatalogEntryV2 entry = detail.catalogEntry;
        if (entry == null || !entry.specification.isPresent()) return "";
        ProductSpecification s = entry.specification.value;
        StringBuilder out = new StringBuilder();
        if (s.netContent != null) append(out, formatMeasure(s.netContent));
        if (s.packCount != null) {
            String pack = s.packCount + "개입";
            if (s.innerUnitContent != null) pack += " · 개당 " + formatMeasure(s.innerUnitContent);
            append(out, pack);
        }
        return out.toString();
    }

    public static String formatWon(BigDecimal minor) {
        if (minor == null) return "—";
        BigDecimal normalized = minor.stripTrailingZeros();
        NumberFormat nf = NumberFormat.getNumberInstance(Locale.KOREA);
        nf.setGroupingUsed(true);
        if (normalized.scale() <= 0) {
            nf.setMaximumFractionDigits(0);
            nf.setMinimumFractionDigits(0);
        } else {
            nf.setMaximumFractionDigits(2);
            nf.setMinimumFractionDigits(0);
        }
        return nf.format(normalized) + "원";
    }

    public static String latestContext(ProductDetailV1 detail) {
        for (ProductDetailV1.PurchaseRow row : detail.purchases) {
            if (!row.comparable) continue;
            String date = clean(row.purchaseDate, "날짜 미상");
            String store = clean(row.storeName, "매장 미상");
            return date + " · " + store;
        }
        return "비교 가능한 구매 기록이 없습니다.";
    }

    public static String evaluationEvidence(PriceEvaluationV1 evaluation) {
        if (evaluation == null) return "";
        if (evaluation.status == PriceEvaluationV1.Status.EVALUATED && evaluation.usualPriceMinor != null) {
            String usual = formatWon(evaluation.usualPriceMinor);
            String delta = formatSignedWon(evaluation.deltaFromUsualMinor);
            String relation;
            if (evaluation.deltaFromUsualMinor == null || evaluation.deltaFromUsualMinor.signum() == 0) relation = "차이가 거의 없어요";
            else if (evaluation.deltaFromUsualMinor.signum() < 0) relation = delta + " 낮아요";
            else relation = delta + " 높아요";
            return "평소 " + usual + "보다 " + relation + " · 이전 " + evaluation.baselineCount + "회 기준";
        }
        if (evaluation.status == PriceEvaluationV1.Status.INSUFFICIENT_HISTORY) {
            return "평소가격 판단에는 이전 구매가 최소 " + evaluation.minimumPriorObservations + "회 필요해요.";
        }
        if (evaluation.status == PriceEvaluationV1.Status.CONTEXTUAL_ONLY) {
            return "직접 비교 가능한 단위가격이 아니어서 참고 이력으로만 보여요.";
        }
        return "신뢰할 수 있는 평소가격 기준을 만들 수 없어 판단을 보류했어요.";
    }

    public static String purchaseTitle(ProductDetailV1.PurchaseRow row) {
        String date = clean(row.purchaseDate, "날짜 미상");
        String store = clean(row.storeName, "매장 미상");
        return date + " · " + store;
    }

    public static String purchaseSubtitle(ProductDetailV1.PurchaseRow row) {
        if (row.comparable) return formatWon(row.comparisonPriceMinor) + " · 상품 1개 기준";
        return "가격 비교 제외 · " + exclusionKo(row.eligibility);
    }

    public static String chartAccessibilitySummary(ProductDetailV1 detail) {
        int count = detail.comparablePurchases().size();
        if (count == 0) return "가격 추세 그래프. 비교 가능한 구매 기록이 없습니다.";
        String latest = formatWon(detail.evaluation.latestPriceMinor);
        String usual = detail.evaluation.usualPriceMinor == null ? "평소가격 없음" : "평소가격 " + formatWon(detail.evaluation.usualPriceMinor);
        return "가격 추세 그래프. 실제 구매 " + count + "회, 최근 구매가 " + latest + ", " + usual + ".";
    }

    public static String exclusionKo(PriceObservationV2.Eligibility eligibility) {
        if (eligibility == null) return "비교 조건을 확인할 수 없음";
        switch (eligibility) {
            case INVALID_RECEIPT: return "영수증 검증이 완료되지 않음";
            case MISSING_ITEM_PRICE: return "상품 가격 정보 부족";
            case NEGATIVE_EFFECTIVE_AMOUNT: return "유효 구매금액 오류";
            case UNALLOCATED_RECEIPT_DISCOUNT: return "할인 금액을 이 상품에 확정 배분할 수 없음";
            case ITEM_PRICE_CONFLICT: return "단가와 합계 금액이 일치하지 않음";
            case MISSING_PURCHASE_FORM: return "구매 형태 정보 부족";
            case UNSUPPORTED_PURCHASE_FORM: return "안전한 비교 기준을 만들 수 없음";
            case ELIGIBLE:
            default: return "비교 가능";
        }
    }

    private static String formatSignedWon(BigDecimal value) {
        if (value == null) return "0원";
        String base = formatWon(value.abs());
        return value.signum() < 0 ? base : base;
    }

    private static String formatMeasure(PackageMeasure measure) {
        return compact(measure.amount) + unitKo(measure.unit);
    }

    private static String unitKo(SalesUnitCode unit) {
        switch (unit) {
            case EACH: return "개";
            case GRAM: return "g";
            case KILOGRAM: return "kg";
            case MILLILITER: return "mL";
            case LITER: return "L";
            default: return unit.name();
        }
    }

    private static String compact(BigDecimal value) {
        BigDecimal n = value.setScale(Math.max(0, Math.min(3, value.scale())), RoundingMode.HALF_UP).stripTrailingZeros();
        return n.scale() < 0 ? n.setScale(0).toPlainString() : n.toPlainString();
    }

    private static void append(StringBuilder out, String value) {
        if (value == null || value.trim().isEmpty()) return;
        if (out.length() > 0) out.append(" · ");
        out.append(value.trim());
    }

    private static String clean(String value, String fallback) {
        String v = value == null ? "" : value.trim();
        return v.isEmpty() ? fallback : v;
    }
}
