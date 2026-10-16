package com.receiptledger.v1.design;

/** Reusable non-domain UI states. These are presentation contracts, not new business states. */
public final class UiStatePresentationV1 {
    public enum Kind {
        LOADING,
        EMPTY,
        NO_RESULT,
        REVIEW_REQUIRED,
        INSUFFICIENT_PRICE_HISTORY,
        CONTEXTUAL_PRICE_HISTORY,
        ERROR,
        DISABLED
    }

    public final Kind kind;
    public final String titleKo;
    public final String bodyKo;
    public final SemanticToneV1 tone;
    public final boolean actionAllowed;

    private UiStatePresentationV1(Kind kind, String titleKo, String bodyKo, SemanticToneV1 tone, boolean actionAllowed) {
        this.kind = kind;
        this.titleKo = titleKo;
        this.bodyKo = bodyKo;
        this.tone = tone;
        this.actionAllowed = actionAllowed;
    }

    public static UiStatePresentationV1 of(Kind kind) {
        if (kind == null) throw new IllegalArgumentException("kind");
        switch (kind) {
            case LOADING:
                return p(kind, "불러오는 중", "잠시 후 최신 정보를 표시해요.", SemanticToneV1.INFO, false);
            case EMPTY:
                return p(kind, "아직 기록이 없어요", "영수증을 저장하면 구매기록이 여기에 쌓여요.", SemanticToneV1.NEUTRAL, true);
            case NO_RESULT:
                return p(kind, "검색 결과가 없어요", "검색어나 필터를 바꿔보세요.", SemanticToneV1.NEUTRAL, true);
            case REVIEW_REQUIRED:
                return p(kind, "확인이 필요해요", "자동 판단이 안전하지 않은 항목만 확인해 주세요.", SemanticToneV1.REVIEW, true);
            case INSUFFICIENT_PRICE_HISTORY:
                return p(kind, "가격 기록이 더 필요해요", "과거 구매가 더 쌓이면 평소가격과 비교할 수 있어요.", SemanticToneV1.INFO, false);
            case CONTEXTUAL_PRICE_HISTORY:
                return p(kind, "참고용 가격이력", "포장 형태가 같아도 실제 용량이 다를 수 있어 직접 판정하지 않아요.", SemanticToneV1.INFO, false);
            case ERROR:
                return p(kind, "문제가 발생했어요", "입력이나 저장 상태를 확인한 뒤 다시 시도해 주세요.", SemanticToneV1.ERROR, true);
            case DISABLED:
                return p(kind, "지금은 사용할 수 없어요", "필요한 정보가 준비되면 사용할 수 있어요.", SemanticToneV1.DISABLED, false);
            default:
                throw new IllegalArgumentException("unknown kind");
        }
    }

    private static UiStatePresentationV1 p(Kind kind, String title, String body, SemanticToneV1 tone, boolean actionAllowed) {
        return new UiStatePresentationV1(kind, title, body, tone, actionAllowed);
    }
}
