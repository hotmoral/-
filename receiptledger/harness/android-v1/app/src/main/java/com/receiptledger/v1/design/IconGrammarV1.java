package com.receiptledger.v1.design;

/** Stable icon semantics independent of any later drawable/icon-library choice. */
public enum IconGrammarV1 {
    ADD_RECEIPT("영수증 추가"),
    SEARCH("검색"),
    FILTER("필터"),
    RECEIPT("영수증"),
    PRODUCT("제품"),
    CATEGORY("카테고리"),
    PRICE_TREND("가격 변화"),
    REVIEW("확인 필요"),
    MORE("더보기"),
    DELETE("삭제");

    public final String contentDescriptionKo;

    IconGrammarV1(String contentDescriptionKo) {
        String clean = contentDescriptionKo == null ? "" : contentDescriptionKo.trim();
        if (clean.isEmpty()) throw new IllegalArgumentException("contentDescriptionKo");
        this.contentDescriptionKo = clean;
    }

    public int glyphSizeDp() { return DesignTokensV1.ICON_GLYPH_DP; }
    public int minimumHitTargetDp() { return DesignTokensV1.TOUCH_TARGET_MIN_DP; }

    /** Icon-only controls must always expose a non-empty spoken label. */
    public boolean validForIconOnlyControl() {
        return !contentDescriptionKo.isEmpty()
                && glyphSizeDp() <= minimumHitTargetDp()
                && minimumHitTargetDp() >= 48;
    }
}
