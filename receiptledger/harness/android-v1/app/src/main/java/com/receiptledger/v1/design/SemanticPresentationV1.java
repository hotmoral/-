package com.receiptledger.v1.design;

import com.receiptledger.v1.priceeval.PriceEvaluationV1;
import com.receiptledger.v1.validation.ValidationStatus;

/** User-facing semantic wording. Raw enum names must not become final UI copy. */
public final class SemanticPresentationV1 {
    private SemanticPresentationV1() {}

    public static final class Presentation {
        public final String labelKo;
        public final String explanationKo;
        public final SemanticToneV1 tone;
        public final boolean judgment;

        private Presentation(String labelKo, String explanationKo, SemanticToneV1 tone, boolean judgment) {
            this.labelKo = required(labelKo, "labelKo");
            this.explanationKo = required(explanationKo, "explanationKo");
            if (tone == null) throw new IllegalArgumentException("tone");
            this.tone = tone;
            this.judgment = judgment;
        }
    }

    public static Presentation price(PriceEvaluationV1 evaluation) {
        if (evaluation == null) throw new IllegalArgumentException("evaluation");
        return price(evaluation.status, evaluation.judgment);
    }

    public static Presentation price(PriceEvaluationV1.Status status, PriceEvaluationV1.Judgment judgment) {
        if (status == null || judgment == null) throw new IllegalArgumentException("price state");
        switch (status) {
            case EVALUATED:
                switch (judgment) {
                    case VERY_CHEAP:
                        return p("평소보다 매우 저렴", "최근 구매이력의 평소가격보다 충분히 낮아요.", SemanticToneV1.POSITIVE, true);
                    case CHEAP:
                        return p("평소보다 저렴", "최근 구매이력의 평소가격보다 낮아요.", SemanticToneV1.POSITIVE, true);
                    case TYPICAL:
                        return p("평소 수준", "최근 구매이력의 평소가격 범위에 있어요.", SemanticToneV1.NEUTRAL, true);
                    case EXPENSIVE:
                        return p("평소보다 비쌈", "최근 구매이력의 평소가격보다 높아요.", SemanticToneV1.NEGATIVE, true);
                    case VERY_EXPENSIVE:
                        return p("평소보다 매우 비쌈", "최근 구매이력의 평소가격보다 충분히 높아요.", SemanticToneV1.NEGATIVE, true);
                    case NONE:
                    default:
                        throw new IllegalArgumentException("evaluated price requires judgment");
                }
            case INSUFFICIENT_HISTORY:
                return p("비교 데이터 부족", "과거 구매가 더 쌓이면 평소가격과 비교할 수 있어요.", SemanticToneV1.INFO, false);
            case CONTEXTUAL_ONLY:
                return p("참고용 이력", "포장 형태만 같아 직접적인 단위가격 판정은 하지 않아요.", SemanticToneV1.INFO, false);
            case NON_POSITIVE_BASELINE:
                return p("기준가격 확인 필요", "평소가격 기준을 만들 수 없어 가격판정을 보류했어요.", SemanticToneV1.REVIEW, false);
            default:
                throw new IllegalArgumentException("unknown price status");
        }
    }

    public static Presentation validation(ValidationStatus status) {
        if (status == null) throw new IllegalArgumentException("status");
        switch (status) {
            case PASS:
                return p("검증 완료", "영수증 합계와 상품 금액이 일치해요.", SemanticToneV1.POSITIVE, false);
            case PASS_WITH_WARNINGS:
                return p("확인 권장", "저장은 가능하지만 일부 항목을 한 번 더 확인하는 편이 좋아요.", SemanticToneV1.REVIEW, false);
            case MISMATCH:
                return p("금액 불일치", "상품 금액과 영수증 합계가 맞지 않아 확인이 필요해요.", SemanticToneV1.ERROR, false);
            case INCOMPLETE:
                return p("확인 필요", "비어 있거나 확정되지 않은 값이 있어요.", SemanticToneV1.REVIEW, false);
            default:
                throw new IllegalArgumentException("unknown validation status");
        }
    }

    /** Additive CP31 adapter for screen-specific semantic surfaces that still consume frozen tones. */
    public static Presentation display(String label, String explanation, SemanticToneV1 tone) {
        return p(label, explanation, tone, false);
    }

    private static Presentation p(String label, String explanation, SemanticToneV1 tone, boolean judgment) {
        return new Presentation(label, explanation, tone, judgment);
    }

    private static String required(String value, String name) {
        String clean = value == null ? "" : value.trim();
        if (clean.isEmpty()) throw new IllegalArgumentException(name);
        return clean;
    }
}
