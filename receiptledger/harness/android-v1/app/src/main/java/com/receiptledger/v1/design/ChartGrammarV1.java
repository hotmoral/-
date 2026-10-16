package com.receiptledger.v1.design;

import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.priceintel.ComparisonBasisV2;
import java.util.List;

/** Chart/presentation guardrails. A visual series can never erase CP26/27 comparison-basis boundaries. */
public final class ChartGrammarV1 {
    private ChartGrammarV1() {}

    public static String seriesKey(String catalogId, ComparisonBasisV2 basis) {
        String id = catalogId == null ? "" : catalogId.trim();
        if (id.isEmpty() || basis == null) throw new IllegalArgumentException("series identity");
        return id + "|" + basis.key();
    }

    public static void requireSingleBasis(List<ComparisonBasisV2> bases) {
        if (bases == null || bases.isEmpty()) throw new IllegalArgumentException("bases");
        ComparisonBasisV2 first = bases.get(0);
        if (first == null) throw new IllegalArgumentException("basis");
        for (int i = 1; i < bases.size(); i++) {
            ComparisonBasisV2 next = bases.get(i);
            if (!first.equals(next)) throw new IllegalArgumentException("cross-basis chart series forbidden");
        }
    }

    public static String axisLabelKo(ComparisonBasisV2 basis) {
        if (basis == null) throw new IllegalArgumentException("basis");
        switch (basis.kind) {
            case STANDARD_PACKAGE:
                return "원/상품";
            case WEIGHT_KG:
                return "원/kg";
            case VOLUME_L:
                return "원/L";
            case EACH:
                return "원/개";
            case LIKE_FORM:
                return "참고 · 원/" + basis.displayUnit;
            default:
                throw new IllegalArgumentException("unknown basis");
        }
    }

    public static boolean showUsualPriceReference(PriceEvaluationV1.Status status) {
        return status == PriceEvaluationV1.Status.EVALUATED;
    }

    public static boolean allowJudgmentColor(PriceEvaluationV1.Status status) {
        return status == PriceEvaluationV1.Status.EVALUATED;
    }
}
