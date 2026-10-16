package com.receiptledger.v1.commoditydetail;

import com.receiptledger.v1.catalog.PurchaseForm;
import com.receiptledger.v1.catalog.SalesUnitCode;
import com.receiptledger.v1.design.ChartGrammarV1;
import com.receiptledger.v1.design.SemanticPresentationV1;
import com.receiptledger.v1.design.SemanticToneV1;
import com.receiptledger.v1.detail.ProductDetailFormatterV1;
import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.ComparisonBasisV2;
import com.receiptledger.v1.priceintel.PriceObservationV2;
import java.math.BigDecimal;

/** Korean presentation helpers for CP32. */
public final class CommodityDetailFormatterV1 {
    private CommodityDetailFormatterV1() {}

    public static String primaryName(CommodityDetailV1 detail) {
        if (detail.catalogEntry != null) return clean(detail.catalogEntry.canonicalName, detail.product.canonicalName);
        return detail.product.canonicalName;
    }

    public static String formatWon(BigDecimal value) {
        return ProductDetailFormatterV1.formatWon(value);
    }

    public static String formatRate(BigDecimal value, ComparisonBasisV2 basis) {
        if (value == null) return "—";
        return formatWon(value) + "/" + unitForBasis(basis);
    }

    public static String basisTitleKo(ComparisonBasisV2 basis) {
        if (basis == null) return "비교 기준";
        switch (basis.kind) {
            case WEIGHT_KG: return "무게 기준";
            case VOLUME_L: return "부피 기준";
            case EACH: return "개수 기준";
            case LIKE_FORM: return "“" + clean(basis.displayUnit, "포장") + "” 형태";
            case STANDARD_PACKAGE:
            default: return "비교 기준";
        }
    }

    public static String basisDescriptionKo(ComparisonBasisV2 basis) {
        if (basis == null) return "";
        switch (basis.kind) {
            case WEIGHT_KG: return "kg로 정확히 환산 가능한 구매끼리만 비교해요.";
            case VOLUME_L: return "L로 정확히 환산 가능한 구매끼리만 비교해요.";
            case EACH: return "개수가 명확한 구매끼리만 비교해요.";
            case LIKE_FORM:
                return "같은 포장 표기끼리만 참고해요. kg·L·개 기준과 섞지 않아요.";
            case STANDARD_PACKAGE:
            default: return "";
        }
    }

    public static String basisMeta(CommodityDetailV1.BasisSection section) {
        return "실제 구매 " + section.cohort.count() + "회 · " + ChartGrammarV1.axisLabelKo(section.cohort.basis);
    }

    public static String sectionLatestContext(CommodityDetailV1.BasisSection section) {
        if (section.cohort.observations.isEmpty()) return "구매 기록 없음";
        PriceObservationV2 row = section.cohort.observations.get(0);
        return clean(row.purchaseDate, "날짜 미상") + " · " + clean(row.storeName, "매장 미상");
    }

    public static String purchaseFormKo(CommodityDetailV1.PurchaseRow row) {
        PurchaseForm form = row == null ? null : row.observation.purchaseForm;
        if (form == null) return "구매형태 미확인";
        return compact(form.quantity) + unitKo(form.unit, form.rawUnitLabel);
    }

    public static String purchaseAmountLabel(CommodityDetailV1.PurchaseRow row) {
        if (row == null) return "가격 기록";
        if (row.observation.isEligible() && row.observation.sourceNumeratorMinor != null) return "구매금액";
        if (row.observation.rawLineAmount != null) return "영수증 상품금액";
        return "가격 기록";
    }

    public static String purchaseAmount(CommodityDetailV1.PurchaseRow row) {
        BigDecimal amount = purchaseAmountMinor(row);
        return amount == null ? "—" : formatWon(amount);
    }

    public static BigDecimal purchaseAmountMinor(CommodityDetailV1.PurchaseRow row) {
        if (row == null) return null;
        PriceObservationV2 o = row.observation;
        if (o.isEligible() && o.sourceNumeratorMinor != null) return o.sourceNumeratorMinor;
        if (o.rawLineAmount != null && o.rawLineAmount >= 0) return BigDecimal.valueOf(o.rawLineAmount);
        return null;
    }

    public static String purchaseTitle(CommodityDetailV1.PurchaseRow row) {
        PriceObservationV2 o = row.observation;
        return clean(o.purchaseDate, "날짜 미상") + " · " + clean(o.storeName, "매장 미상");
    }

    public static String purchaseSubtitle(CommodityDetailV1.PurchaseRow row) {
        PriceObservationV2 o = row.observation;
        String form = purchaseFormKo(row);
        String amount = purchaseAmount(row);
        if (!o.isEligible()) {
            return form + " · " + amount + " · 가격 비교 제외 · " + ProductDetailFormatterV1.exclusionKo(o.eligibility);
        }
        if (o.basis.isStrictNormalized()) {
            return form + " · " + amount + " · " + formatRate(o.comparisonPriceMinor, o.basis);
        }
        return form + " · " + amount + " · 참고 " + formatRate(o.comparisonPriceMinor, o.basis);
    }

    public static String latestContext(CommodityDetailV1.PurchaseRow row) {
        if (row == null) return "아직 연결된 구매 기록이 없습니다.";
        return purchaseFormKo(row) + " · " + purchaseTitle(row);
    }

    public static SemanticPresentationV1.Presentation latestPresentation(CommodityDetailV1.PurchaseRow row) {
        if (row == null) {
            return SemanticPresentationV1.display("구매 기록 없음", "영수증이 쌓이면 최근 구매형태와 가격을 확인할 수 있어요.", SemanticToneV1.INFO);
        }
        PriceObservationV2 o = row.observation;
        if (!o.isEligible()) {
            return SemanticPresentationV1.display("가격 비교 제외",
                    ProductDetailFormatterV1.exclusionKo(o.eligibility) + ". 원본 구매기록은 그대로 보존돼요.",
                    SemanticToneV1.REVIEW);
        }
        if (!o.basis.isStrictNormalized()) {
            return SemanticPresentationV1.display("참고용 구매",
                    "포장 형태는 직접 단위가격 판정을 하지 않아요. 같은 형태의 참고 이력으로만 봅니다.",
                    SemanticToneV1.INFO);
        }
        return SemanticPresentationV1.display("직접 비교 가능",
                basisTitleKo(o.basis) + " 안에서만 과거 가격과 비교합니다.", SemanticToneV1.INFO);
    }

    public static String evaluationEvidence(PriceEvaluationV1 evaluation) {
        return ProductDetailFormatterV1.evaluationEvidence(evaluation);
    }

    public static String contextualSummary(CommodityDetailV1.BasisSection section) {
        String latest = formatRate(section.cohort.latest, section.cohort.basis);
        String previous = section.cohort.previous == null ? "이전 기록 없음" : "이전 " + formatRate(section.cohort.previous, section.cohort.basis);
        return "최근 " + latest + " · " + previous + " · " + section.cohort.count() + "회";
    }

    public static String chartAccessibilitySummary(CommodityDetailV1.BasisSection section) {
        String basis = basisTitleKo(section.cohort.basis);
        String latest = formatRate(section.evaluation.latestPriceMinor, section.cohort.basis);
        String usual = section.evaluation.usualPriceMinor == null
                ? "평소가격 없음"
                : "평소가격 " + formatRate(section.evaluation.usualPriceMinor, section.cohort.basis);
        return basis + " 가격 추세 그래프. 실제 구매 " + section.cohort.count() + "회, 최근 " + latest + ", " + usual + ".";
    }

    private static String unitForBasis(ComparisonBasisV2 basis) {
        if (basis == null) return "단위";
        switch (basis.kind) {
            case WEIGHT_KG: return "kg";
            case VOLUME_L: return "L";
            case EACH: return "개";
            case LIKE_FORM: return clean(basis.displayUnit, "포장");
            case STANDARD_PACKAGE:
            default: return "상품";
        }
    }

    private static String unitKo(SalesUnitCode unit, String raw) {
        String rawClean = clean(raw, "");
        switch (unit) {
            case EACH: return "개";
            case GRAM: return "g";
            case KILOGRAM: return "kg";
            case MILLILITER: return "mL";
            case LITER: return "L";
            case BAG: return rawClean.isEmpty() ? "봉" : rawClean;
            case PACK: return rawClean.isEmpty() ? "팩" : rawClean;
            case BOX: return rawClean.isEmpty() ? "상자" : rawClean;
            case BUNDLE: return rawClean.isEmpty() ? "단" : rawClean;
            case OTHER: return rawClean.isEmpty() ? "기타" : rawClean;
            case UNKNOWN:
            default: return rawClean.isEmpty() ? "단위 미상" : rawClean;
        }
    }

    private static String compact(BigDecimal value) {
        BigDecimal n = value == null ? BigDecimal.ZERO : value.stripTrailingZeros();
        if (n.scale() < 0) n = n.setScale(0);
        return n.toPlainString();
    }

    private static String clean(String value, String fallback) {
        String v = value == null ? "" : value.trim();
        return v.isEmpty() ? fallback : v;
    }
}
