package com.receiptledger.v1.design;

/** Semantic visual roles. Color is supplementary; user-facing text labels remain mandatory. */
public enum SemanticToneV1 {
    NEUTRAL(DesignTokensV1.COLOR_TEXT_PRIMARY, DesignTokensV1.COLOR_SURFACE_SUBTLE),
    PRIMARY(DesignTokensV1.COLOR_ON_PRIMARY, DesignTokensV1.COLOR_PRIMARY),
    POSITIVE(DesignTokensV1.COLOR_POSITIVE_TEXT, DesignTokensV1.COLOR_POSITIVE_BG),
    NEGATIVE(DesignTokensV1.COLOR_NEGATIVE_TEXT, DesignTokensV1.COLOR_NEGATIVE_BG),
    REVIEW(DesignTokensV1.COLOR_REVIEW_TEXT, DesignTokensV1.COLOR_REVIEW_BG),
    ERROR(DesignTokensV1.COLOR_ERROR_TEXT, DesignTokensV1.COLOR_ERROR_BG),
    INFO(DesignTokensV1.COLOR_INFO_TEXT, DesignTokensV1.COLOR_INFO_BG),
    DISABLED(DesignTokensV1.COLOR_TEXT_DISABLED, DesignTokensV1.COLOR_SURFACE_SUBTLE);

    public final int foregroundArgb;
    public final int backgroundArgb;

    SemanticToneV1(int foregroundArgb, int backgroundArgb) {
        this.foregroundArgb = foregroundArgb;
        this.backgroundArgb = backgroundArgb;
    }
}
